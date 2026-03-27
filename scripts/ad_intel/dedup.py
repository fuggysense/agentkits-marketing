"""Phase 4.5: Deduplication + HQ Resolution + Chain Detection."""

import json
from collections import defaultdict
from pathlib import Path

from config import DATA_DIR
from utils import normalize_domain, fuzzy_business_match, clean_business_name


CHAIN_THRESHOLD = 10  # branches >= this → flagged as chain


def _merge_entries(primary: dict, duplicate: dict) -> dict:
    """Merge a duplicate entry into the primary, keeping best data."""
    merged = {**primary}

    # Merge verticals
    v1 = set(primary.get("verticals", []))
    v2 = set(duplicate.get("verticals", []))
    merged["verticals"] = sorted(v1 | v2)

    # Keep higher score
    merged["score"] = max(primary.get("score", 0), duplicate.get("score", 0))

    # Merge Google keyword counts
    merged["google_keyword_count"] = (
        primary.get("google_keyword_count", 0) + duplicate.get("google_keyword_count", 0)
    )

    # Merge Meta ad counts
    merged["meta_ad_count"] = max(
        primary.get("meta_ad_count", 0), duplicate.get("meta_ad_count", 0)
    )
    merged["meta_spend_max"] = max(
        primary.get("meta_spend_max", 0), duplicate.get("meta_spend_max", 0)
    )

    # Fill missing contact data from duplicate
    for field in ["phone", "email", "whatsapp", "full_address", "postal_code",
                   "fb_page_url", "fb_page_id", "page_title", "meta_description",
                   "og_title", "og_description"]:
        if not merged.get(field) and duplicate.get(field):
            merged[field] = duplicate[field]

    # Merge branches
    existing_branches = {
        b.get("address", ""): b for b in merged.get("branches", [])
    }
    for branch in duplicate.get("branches", []):
        addr = branch.get("address", "")
        if addr and addr not in existing_branches:
            existing_branches[addr] = branch
    merged["branches"] = list(existing_branches.values())
    merged["branch_count"] = len(merged["branches"])

    # Merge landing pages
    lp1 = set(primary.get("landing_pages", []))
    lp2 = set(duplicate.get("landing_pages", []))
    merged["landing_pages"] = sorted(lp1 | lp2)

    # Keep best ad copy
    if not merged.get("sample_ad_copy") and duplicate.get("sample_ad_copy"):
        merged["sample_ad_copy"] = duplicate["sample_ad_copy"]

    return merged


def deduplicate(contacts: list[dict]) -> list[dict]:
    """Run 4-layer deduplication on enriched business list.

    Layer 1: Domain dedup (exact match)
    Layer 2: Business name fuzzy match
    Layer 3: Multi-branch → HQ resolution
    Layer 4: Chain/franchise detection
    """
    # ── Layer 1: Domain Dedup ──
    domain_groups: dict[str, list[dict]] = defaultdict(list)
    no_domain: list[dict] = []

    for biz in contacts:
        domain = normalize_domain(biz.get("domain", ""))
        if domain:
            domain_groups[domain].append(biz)
        else:
            no_domain.append(biz)

    # Merge same-domain entries
    domain_merged: dict[str, dict] = {}
    for domain, entries in domain_groups.items():
        primary = entries[0]
        for dup in entries[1:]:
            primary = _merge_entries(primary, dup)
        domain_merged[domain] = primary

    # ── Layer 2: Business Name Fuzzy Match ──
    # Try to match no-domain entries to domain entries by name
    unmatched: list[dict] = []
    for biz in no_domain:
        name = clean_business_name(biz.get("business_name", ""))
        matched = False
        if name:
            for domain, entry in domain_merged.items():
                existing_name = clean_business_name(
                    entry.get("business_name", "") or entry.get("meta_advertiser_name", "")
                )
                if existing_name and fuzzy_business_match(name, existing_name):
                    domain_merged[domain] = _merge_entries(entry, biz)
                    matched = True
                    break
        if not matched:
            unmatched.append(biz)

    # Also fuzzy match domain entries against each other
    # (catches cases like abcdental.com and abcdentalclinic.com)
    domains = list(domain_merged.keys())
    merged_away: set[str] = set()

    for i, d1 in enumerate(domains):
        if d1 in merged_away:
            continue
        e1 = domain_merged[d1]
        name1 = clean_business_name(e1.get("business_name", ""))
        phone1 = e1.get("phone", "")

        for d2 in domains[i + 1:]:
            if d2 in merged_away:
                continue
            e2 = domain_merged[d2]
            name2 = clean_business_name(e2.get("business_name", ""))
            phone2 = e2.get("phone", "")

            # Same phone = definitely same business
            if phone1 and phone2 and phone1 == phone2:
                domain_merged[d1] = _merge_entries(e1, e2)
                merged_away.add(d2)
            # Fuzzy name match (high threshold to avoid false positives)
            elif name1 and name2 and fuzzy_business_match(name1, name2, threshold=85):
                domain_merged[d1] = _merge_entries(e1, e2)
                merged_away.add(d2)

    # Remove merged-away entries
    for d in merged_away:
        del domain_merged[d]

    # Combine
    all_businesses = list(domain_merged.values()) + unmatched

    # ── Layer 3: HQ Resolution ──
    for biz in all_businesses:
        branches = biz.get("branches", [])
        if branches:
            biz["branch_count"] = len(branches)
            # Format branches as string for sheets
            biz["branches_display"] = ", ".join(
                f"{b.get('name', 'Branch')} ({b.get('postal', 'N/A')})"
                for b in branches
            )
        else:
            biz["branch_count"] = 0
            biz["branches_display"] = ""

    # ── Layer 4: Chain Detection ──
    for biz in all_businesses:
        if biz.get("branch_count", 0) >= CHAIN_THRESHOLD:
            biz["is_chain"] = True
            notes = biz.get("notes", "")
            biz["notes"] = f"CHAIN ({biz['branch_count']} locations). {notes}".strip()
        else:
            biz["is_chain"] = False

    # Re-score tiers
    for biz in all_businesses:
        score = biz.get("score", 0)
        if score >= 8:
            biz["tier"] = "hot"
        elif score >= 4:
            biz["tier"] = "warm"
        else:
            biz["tier"] = "cold"

    # Sort by score descending
    all_businesses.sort(key=lambda x: (-x.get("score", 0), x.get("business_name", "")))

    return all_businesses


def save_deduped(businesses: list[dict], path: Path | None = None) -> Path:
    """Save deduplicated businesses to JSON."""
    out = path or (DATA_DIR / "deduped_businesses.json")
    chains = sum(1 for b in businesses if b.get("is_chain"))
    multi_branch = sum(1 for b in businesses if b.get("branch_count", 0) > 1)

    payload = {
        "total_businesses": len(businesses),
        "chains_flagged": chains,
        "multi_branch": multi_branch,
        "businesses": businesses,
    }
    out.write_text(json.dumps(payload, indent=2, default=str))
    return out


def load_deduped(path: Path | None = None) -> list[dict]:
    """Load deduplicated businesses from JSON."""
    p = path or (DATA_DIR / "deduped_businesses.json")
    data = json.loads(p.read_text())
    return data["businesses"]


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from contact_scraper import load_contacts

    contacts = load_contacts()
    print(f"Before dedup: {len(contacts)} entries")

    deduped = deduplicate(contacts)
    out = save_deduped(deduped)

    chains = sum(1 for b in deduped if b.get("is_chain"))
    multi = sum(1 for b in deduped if b.get("branch_count", 0) > 1)

    print(f"After dedup: {len(deduped)} entries")
    print(f"  Chains flagged: {chains}")
    print(f"  Multi-branch: {multi}")
    print(f"Saved to {out}")
