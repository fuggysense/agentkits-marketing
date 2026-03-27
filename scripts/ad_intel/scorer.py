"""Phase 3: Merge & Score — cross-reference Google + Meta results, assign 1-10 score."""

import json
from collections import defaultdict
from pathlib import Path

from config import DATA_DIR, VERTICALS, load_blocklist
from utils import normalize_domain, fuzzy_business_match, clean_business_name, detect_country


def _build_domain_index(
    google_results: dict[str, list[dict]],
    meta_results: dict[str, list[dict]],
) -> dict[str, dict]:
    """Build a master index keyed by normalized domain.

    Each entry aggregates data from both Google and Meta sources.
    """
    index: dict[str, dict] = {}
    blocklist = load_blocklist()

    # Index Google results
    for vertical, ads in google_results.items():
        for ad in ads:
            domain = ad.get("domain", "")
            if not domain or domain in blocklist:
                continue

            if domain not in index:
                index[domain] = {
                    "domain": domain,
                    "business_name": "",
                    "verticals": set(),
                    "google_keywords": [],
                    "google_ads": [],
                    "google_top_positions": 0,
                    "meta_ads": [],
                    "meta_advertiser_name": "",
                    "meta_fb_page_url": "",
                    "meta_fb_page_id": "",
                    "meta_spend_min": 0,
                    "meta_spend_max": 0,
                    "meta_ad_count": 0,
                    "meta_is_active": False,
                    "landing_pages": set(),
                    "sample_ad_copy": "",
                }

            entry = index[domain]
            entry["verticals"].add(vertical)
            # New scanner returns aggregated keywords list per domain
            if ad.get("keywords"):
                entry["google_keywords"].extend(ad["keywords"])
            else:
                entry["google_keywords"].append(ad["keyword"])
            entry["google_ads"].append(ad)
            entry["landing_pages"].add(ad.get("url", ""))

            if ad.get("is_top") or ad.get("top_positions", 0) > 0:
                entry["google_top_positions"] += ad.get("top_positions", 1 if ad.get("is_top") else 0)

            # Paid ads verification from DataForSEO Labs
            if ad.get("has_paid_ads"):
                entry["google_has_paid_ads"] = True
                entry["google_paid_keyword_count"] = max(
                    entry.get("google_paid_keyword_count", 0),
                    ad.get("paid_keyword_count", 0),
                )

            # CPC data
            if ad.get("avg_cpc", 0) > entry.get("google_avg_cpc", 0):
                entry["google_avg_cpc"] = ad["avg_cpc"]

            # Use first ad copy as sample
            if not entry["sample_ad_copy"] and ad.get("title"):
                entry["sample_ad_copy"] = f"{ad['title']} — {ad.get('description', '')}"

    # Index Meta results
    for vertical, ads in meta_results.items():
        for ad in ads:
            domain = ad.get("domain", "")
            advertiser = ad.get("advertiser_name", "")

            # Try domain match first
            if domain and domain not in blocklist:
                if domain not in index:
                    index[domain] = {
                        "domain": domain,
                        "business_name": advertiser,
                        "verticals": set(),
                        "google_keywords": [],
                        "google_ads": [],
                        "google_top_positions": 0,
                        "meta_ads": [],
                        "meta_advertiser_name": advertiser,
                        "meta_fb_page_url": ad.get("fb_page_url", ""),
                        "meta_fb_page_id": ad.get("fb_page_id", ""),
                        "meta_spend_min": 0,
                        "meta_spend_max": 0,
                        "meta_ad_count": 0,
                        "meta_is_active": False,
                        "landing_pages": set(),
                        "sample_ad_copy": "",
                    }

                entry = index[domain]
                entry["verticals"].add(vertical)
                entry["meta_ads"].append(ad)
                entry["meta_advertiser_name"] = entry["meta_advertiser_name"] or advertiser
                entry["meta_fb_page_url"] = entry["meta_fb_page_url"] or ad.get("fb_page_url", "")
                entry["meta_fb_page_id"] = entry["meta_fb_page_id"] or ad.get("fb_page_id", "")

                # Accumulate spend
                entry["meta_spend_min"] = max(entry["meta_spend_min"], ad.get("spend_min", 0))
                entry["meta_spend_max"] = max(entry["meta_spend_max"], ad.get("spend_max", 0))
                entry["meta_ad_count"] += 1
                entry["meta_is_active"] = entry["meta_is_active"] or ad.get("is_active", False)

                if not entry["sample_ad_copy"] and ad.get("ad_text"):
                    entry["sample_ad_copy"] = ad["ad_text"][:200]
            else:
                # No domain — try fuzzy match by business name against existing entries
                if advertiser:
                    matched = False
                    cleaned_adv = clean_business_name(advertiser)
                    for existing_domain, entry in index.items():
                        existing_name = clean_business_name(
                            entry.get("business_name", "") or entry.get("meta_advertiser_name", "")
                        )
                        if existing_name and fuzzy_business_match(cleaned_adv, existing_name):
                            entry["verticals"].add(vertical)
                            entry["meta_ads"].append(ad)
                            entry["meta_advertiser_name"] = entry["meta_advertiser_name"] or advertiser
                            entry["meta_fb_page_url"] = entry["meta_fb_page_url"] or ad.get("fb_page_url", "")
                            entry["meta_ad_count"] += 1
                            matched = True
                            break

                    if not matched:
                        # Create entry with empty domain (keyed by advertiser name)
                        key = f"_meta_{advertiser}"
                        if key not in index:
                            index[key] = {
                                "domain": "",
                                "business_name": advertiser,
                                "verticals": {vertical},
                                "google_keywords": [],
                                "google_ads": [],
                                "google_top_positions": 0,
                                "meta_ads": [ad],
                                "meta_advertiser_name": advertiser,
                                "meta_fb_page_url": ad.get("fb_page_url", ""),
                                "meta_fb_page_id": ad.get("fb_page_id", ""),
                                "meta_spend_min": ad.get("spend_min", 0),
                                "meta_spend_max": ad.get("spend_max", 0),
                                "meta_ad_count": 1,
                                "meta_is_active": ad.get("is_active", False),
                                "landing_pages": set(),
                                "sample_ad_copy": (ad.get("ad_text", "") or "")[:200],
                            }

    return index


def _score_business(entry: dict) -> int:
    """Calculate 1-10 score based on ad signals."""
    score = 0

    # Google keyword appearances (organic + local_pack presence)
    kw_count = len(set(entry.get("google_keywords", [])))
    if kw_count >= 15:
        score += 2
    elif kw_count >= 8:
        score += 1.5
    elif kw_count >= 1:
        score += 1

    # Google top position
    if entry.get("google_top_positions", 0) > 0:
        score += 1

    # Confirmed Google Ads (from DataForSEO Labs ranked_keywords)
    if entry.get("google_has_paid_ads"):
        score += 2  # confirmed advertiser is a strong signal
    elif entry.get("google_avg_cpc", 0) >= 3:
        score += 1  # high-CPC keyword = likely ads ecosystem

    # Meta spend range (treat as SGD) — when available
    spend_max = entry.get("meta_spend_max", 0)
    if spend_max >= 5000:
        score += 3
    elif spend_max >= 1000:
        score += 2
    elif spend_max > 0:
        score += 1

    # Meta ad volume (proxy for spend when spend data unavailable)
    meta_count = entry.get("meta_ad_count", 0)
    if spend_max == 0:  # no spend data — use ad count as proxy
        if meta_count >= 10:
            score += 3
        elif meta_count >= 5:
            score += 2
        elif meta_count >= 1:
            score += 1

    # Active on BOTH platforms
    has_google = len(entry.get("google_ads", [])) > 0
    has_meta = len(entry.get("meta_ads", [])) > 0
    if has_google and has_meta:
        score += 1

    # Multiple active Meta ads (bonus on top of volume score)
    if meta_count >= 15:
        score += 1

    return min(int(round(score)), 10)


def score_businesses(
    google_results: dict[str, list[dict]],
    meta_results: dict[str, list[dict]],
) -> list[dict]:
    """Merge Google + Meta results and score each business.

    Returns list of scored business dicts, sorted by score desc.
    """
    index = _build_domain_index(google_results, meta_results)

    scored = []
    for key, entry in index.items():
        # Skip businesses with no evidence of paid advertising
        has_google_ads = entry.get("google_has_paid_ads", False)
        has_meta_ads = len(entry.get("meta_ads", [])) > 0
        if not has_google_ads and not has_meta_ads:
            continue

        score = _score_business(entry)

        # Determine tier
        if score >= 8:
            tier = "hot"
        elif score >= 4:
            tier = "warm"
        else:
            tier = "cold"

        # Determine business name
        name = (
            entry.get("business_name")
            or entry.get("meta_advertiser_name")
            or entry.get("domain")
            or key
        )

        # Unique ID: domain > fb_page_id > slugified name
        # Used for dedup across monthly runs
        domain = entry["domain"]
        fb_id = entry.get("meta_fb_page_id", "")
        uid = domain or (f"fb:{fb_id}" if fb_id else f"name:{name.lower().replace(' ', '-')[:40]}")

        # Collect FB contact data from meta ads (filled by resolve_missing_domains)
        fb_phone = ""
        fb_email = ""
        fb_address = ""
        fb_country = ""
        for ad in entry.get("meta_ads", []):
            fb_phone = fb_phone or ad.get("fb_phone", "")
            fb_email = fb_email or ad.get("fb_email", "")
            fb_address = fb_address or ad.get("fb_address", "")
            fb_country = fb_country or ad.get("fb_country", "")

        # Google local_pack sometimes has phone
        google_phone = ""
        for ad in entry.get("google_ads", []):
            google_phone = google_phone or ad.get("phone", "")

        # Detect country from available signals
        best_phone = fb_phone or google_phone
        country = detect_country(
            phone=best_phone,
            domain=domain,
            address=fb_address,
        )
        # Fallback: use FB country field
        if not country and fb_country:
            country = fb_country[:2].upper()

        # Collect advertiser name for decision-maker extraction in Phase 4
        meta_advertiser = entry.get("meta_advertiser_name", "")

        scored.append({
            "uid": uid,
            "business_name": name,
            "domain": domain,
            "score": score,
            "tier": tier,
            "verticals": sorted(entry["verticals"]),
            "country": country,
            "website": f"https://{domain}" if domain else "",
            "fb_page_url": entry.get("meta_fb_page_url", ""),
            "fb_page_id": fb_id,
            "meta_advertiser_name": meta_advertiser,
            # Pre-extracted contacts from FB + Google local pack
            "fb_phone": fb_phone,
            "fb_email": fb_email,
            "fb_address": fb_address,
            "google_phone": google_phone,
            # Ad signals
            "google_keyword_count": len(set(entry.get("google_keywords", []))),
            "google_top_positions": entry.get("google_top_positions", 0),
            "meta_spend_min": entry.get("meta_spend_min", 0),
            "meta_spend_max": entry.get("meta_spend_max", 0),
            "meta_ad_count": entry.get("meta_ad_count", 0),
            "meta_is_active": entry.get("meta_is_active", False),
            "sample_ad_copy": entry.get("sample_ad_copy", ""),
            "landing_pages": sorted(entry.get("landing_pages", set())),
        })

    # Sort by score descending, then by name
    scored.sort(key=lambda x: (-x["score"], x["business_name"]))
    return scored


def save_scored(businesses: list[dict], path: Path | None = None) -> Path:
    """Save scored businesses to JSON."""
    out = path or (DATA_DIR / "scored_businesses.json")
    tiers = defaultdict(int)
    for b in businesses:
        tiers[b["tier"]] += 1

    payload = {
        "total_businesses": len(businesses),
        "tier_breakdown": dict(tiers),
        "businesses": businesses,
    }
    out.write_text(json.dumps(payload, indent=2))
    return out


def load_scored(path: Path | None = None) -> list[dict]:
    """Load scored businesses from JSON."""
    p = path or (DATA_DIR / "scored_businesses.json")
    data = json.loads(p.read_text())
    return data["businesses"]


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from google_scan import load_google_results
    from meta_scan import load_meta_results

    google = load_google_results()
    meta = load_meta_results()
    scored = score_businesses(google, meta)
    out = save_scored(scored)

    tiers = defaultdict(int)
    for b in scored:
        tiers[b["tier"]] += 1

    print(f"Scored {len(scored)} businesses")
    print(f"  Hot (8-10): {tiers['hot']}")
    print(f"  Warm (4-7): {tiers['warm']}")
    print(f"  Cold (1-3): {tiers['cold']}")
    print(f"Saved to {out}")
