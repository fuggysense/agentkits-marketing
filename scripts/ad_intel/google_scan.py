"""Phase 2a: Google Presence + Ads Scan via DataForSEO.

Strategy (adapted from smoke test findings):
  - DataForSEO's organic SERP endpoint does NOT return paid ad items
  - Instead we combine 3 endpoints:
    1. SERP organic → find businesses ranking for vertical keywords (organic + local_pack)
    2. Keywords Data → CPC + competition per keyword (confirms ad activity on keyword)
    3. Labs ranked_keywords → check specific domains for type=paid entries (confirms advertiser)
"""

import asyncio
import json
import base64
from pathlib import Path
from collections import defaultdict

import aiohttp
from tqdm import tqdm
from tenacity import retry, stop_after_attempt, wait_exponential

from config import (
    DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD,
    DATAFORSEO_BATCH_SIZE, DATAFORSEO_PARALLEL_BATCHES,
    DATA_DIR, load_blocklist,
)
from utils import normalize_domain, chunk_list

SERP_URL = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
KW_VOLUME_URL = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
RANKED_KW_URL = "https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live"


def _auth_header() -> str:
    creds = f"{DATAFORSEO_LOGIN}:{DATAFORSEO_PASSWORD}"
    return "Basic " + base64.b64encode(creds.encode()).decode()


# ── Step 1: SERP Organic — find businesses ────────────────────────────────────

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=15))
async def _serp_batch(session: aiohttp.ClientSession, keywords: list[str]) -> list[dict]:
    """POST batch of keywords to SERP organic endpoint."""
    tasks = [
        {
            "keyword": kw,
            "location_name": "Singapore",
            "language_code": "en",
            "device": "desktop",
            "depth": 10,
        }
        for kw in keywords
    ]
    async with session.post(SERP_URL, json=tasks) as resp:
        resp.raise_for_status()
        data = await resp.json()
    return data.get("tasks", [])


def _parse_serp_results(tasks_response: list[dict], blocklist: set[str]) -> list[dict]:
    """Extract business domains from organic + local_pack SERP results."""
    results = []
    for task in tasks_response:
        keyword = task.get("data", {}).get("keyword", "")
        task_result = task.get("result", [])
        if not task_result:
            continue

        items = task_result[0].get("items", [])
        for item in items:
            item_type = item.get("type", "")
            if item_type not in ("organic", "local_pack"):
                continue

            # Handle None values — local_pack items sometimes have None url/domain
            raw_url = item.get("url") or ""
            raw_domain = item.get("domain") or ""
            domain = normalize_domain(raw_url or raw_domain)
            if not domain or domain in blocklist:
                continue

            results.append({
                "keyword": keyword,
                "domain": domain,
                "title": item.get("title") or "",
                "description": item.get("description") or "",
                "url": raw_url,
                "position": item.get("rank_absolute", 0),
                "is_top": item.get("rank_absolute", 99) <= 5,
                "serp_type": item_type,
                "is_paid": item.get("is_paid", False),
                "phone": item.get("phone") or "",
            })
    return results


# ── Step 2: Keyword CPC data ─────────────────────────────────────────────────

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=15))
async def _get_keyword_data(
    session: aiohttp.ClientSession, keywords: list[str],
) -> dict[str, dict]:
    """Get CPC + competition for keywords. Returns keyword → data."""
    tasks = [{
        "keywords": keywords,
        "location_name": "Singapore",
        "language_code": "en",
    }]
    async with session.post(KW_VOLUME_URL, json=tasks) as resp:
        resp.raise_for_status()
        data = await resp.json()

    kw_data = {}
    for task in data.get("tasks", []):
        for result in task.get("result", []):
            if result and result.get("keyword"):
                kw_data[result["keyword"]] = {
                    "search_volume": result.get("search_volume", 0),
                    "cpc": result.get("cpc", 0),
                    "competition": result.get("competition", ""),
                    "competition_index": result.get("competition_index", 0),
                }
    return kw_data


# ── Step 3: Check if domain runs paid ads ─────────────────────────────────────

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=15))
async def _check_paid_ads(
    session: aiohttp.ClientSession, domain: str,
) -> dict:
    """Check if a domain has paid keyword rankings via DataForSEO Labs."""
    tasks = [{
        "target": domain,
        "location_name": "Singapore",
        "language_code": "en",
        "limit": 20,
        "filters": ["ranked_serp_element.serp_item.type", "=", "paid"],
    }]
    async with session.post(RANKED_KW_URL, json=tasks) as resp:
        resp.raise_for_status()
        data = await resp.json()

    task = data.get("tasks", [{}])[0]
    result = (task.get("result") or [{}])[0] or {}
    items = result.get("items", [])

    paid_keywords = []
    for item in items:
        kd = item.get("keyword_data", {})
        ki = kd.get("keyword_info", {})
        paid_keywords.append({
            "keyword": kd.get("keyword", ""),
            "cpc": ki.get("cpc", 0),
            "search_volume": ki.get("search_volume", 0),
        })

    return {
        "domain": domain,
        "has_paid_ads": len(paid_keywords) > 0,
        "paid_keyword_count": len(paid_keywords),
        "paid_keywords": paid_keywords,
        "total_paid_in_db": result.get("total_count", 0),
    }


# ── Orchestrator ──────────────────────────────────────────────────────────────

async def scan_google_ads(
    keywords_by_vertical: dict[str, list[str]],
    progress: bool = True,
    check_paid: bool = True,
    max_domains_to_check: int = 50,
) -> dict[str, list[dict]]:
    """Scan Google for businesses in each vertical, verify ad activity.

    Returns dict mapping vertical → list of business results with ad signals.
    """
    if not DATAFORSEO_LOGIN or not DATAFORSEO_PASSWORD:
        raise RuntimeError("DataForSEO credentials not set.")

    blocklist = load_blocklist()
    headers = {"Authorization": _auth_header(), "Content-Type": "application/json"}
    all_results: dict[str, list[dict]] = {}
    domain_paid_cache: dict[str, dict] = {}

    async with aiohttp.ClientSession(headers=headers) as session:
        for vertical, keywords in keywords_by_vertical.items():
            if progress:
                print(f"\n── {vertical} ({len(keywords)} keywords) ──")

            # Step 1: SERP scan
            serp_results = []
            batches = chunk_list(keywords, DATAFORSEO_BATCH_SIZE)
            sem = asyncio.Semaphore(DATAFORSEO_PARALLEL_BATCHES)

            async def _do_batch(batch):
                async with sem:
                    return await _serp_batch(session, batch)

            tasks = [_do_batch(b) for b in batches]
            for coro in asyncio.as_completed(tasks):
                try:
                    response = await coro
                    serp_results.extend(_parse_serp_results(response, blocklist))
                except Exception as e:
                    print(f"  SERP batch error: {e}")

            # Unique domains found
            domain_hits: dict[str, list[dict]] = defaultdict(list)
            for r in serp_results:
                domain_hits[r["domain"]].append(r)

            if progress:
                print(f"  SERP: {len(serp_results)} results, {len(domain_hits)} unique domains")

            # Step 2: Keyword CPC data (one batch per vertical)
            kw_data = {}
            try:
                # Chunk keywords for CPC lookup (max 1000 per request)
                for kw_chunk in chunk_list(keywords, 700):
                    chunk_data = await _get_keyword_data(session, kw_chunk)
                    kw_data.update(chunk_data)
            except Exception as e:
                print(f"  CPC data error: {e}")

            # Step 3: Check paid ads for top domains
            if check_paid:
                # Sort domains by hit count, check top N
                sorted_domains = sorted(
                    domain_hits.keys(),
                    key=lambda d: len(domain_hits[d]),
                    reverse=True,
                )[:max_domains_to_check]

                checked = 0
                for domain in sorted_domains:
                    if domain in domain_paid_cache:
                        continue
                    try:
                        paid_info = await _check_paid_ads(session, domain)
                        domain_paid_cache[domain] = paid_info
                        checked += 1
                        if checked % 10 == 0 and progress:
                            print(f"  Paid check: {checked}/{len(sorted_domains)}")
                    except Exception as e:
                        domain_paid_cache[domain] = {"has_paid_ads": False, "paid_keyword_count": 0}

                if progress:
                    ads_confirmed = sum(
                        1 for d in sorted_domains if domain_paid_cache.get(d, {}).get("has_paid_ads")
                    )
                    print(f"  Paid ads confirmed: {ads_confirmed}/{len(sorted_domains)} domains")

            # Build final results per domain
            vertical_results = []
            for domain, hits in domain_hits.items():
                # Aggregate keyword appearances
                kw_appearances = list({h["keyword"] for h in hits})
                top_positions = sum(1 for h in hits if h.get("is_top"))

                # CPC data for the keywords this domain appeared on
                avg_cpc = 0
                kw_cpcs = [kw_data.get(kw, {}).get("cpc", 0) or 0 for kw in kw_appearances]
                kw_cpcs = [c for c in kw_cpcs if c and c > 0]
                if kw_cpcs:
                    avg_cpc = sum(kw_cpcs) / len(kw_cpcs)

                # Paid ads info
                paid_info = domain_paid_cache.get(domain, {})

                # Best hit for sample data
                best_hit = max(hits, key=lambda h: h.get("position", 999) * -1)

                vertical_results.append({
                    "keyword": kw_appearances[0] if kw_appearances else "",
                    "domain": domain,
                    "title": best_hit.get("title", ""),
                    "description": best_hit.get("description", ""),
                    "url": best_hit.get("url", ""),
                    "display_url": "",
                    "position": best_hit.get("position", 0),
                    "is_top": top_positions > 0,
                    "serp_type": best_hit.get("serp_type", "organic"),
                    "phone": best_hit.get("phone", ""),
                    # Aggregated signals
                    "keyword_count": len(kw_appearances),
                    "keywords": kw_appearances[:20],
                    "top_positions": top_positions,
                    "avg_cpc": round(avg_cpc, 2),
                    # Paid verification
                    "has_paid_ads": paid_info.get("has_paid_ads", False),
                    "paid_keyword_count": paid_info.get("paid_keyword_count", 0),
                    "total_paid_in_db": paid_info.get("total_paid_in_db", 0),
                    "extensions": {"sitelinks": []},
                })

            all_results[vertical] = vertical_results

    return all_results


def save_google_results(results: dict[str, list[dict]], path: Path | None = None) -> Path:
    """Save Google scan results to JSON."""
    out = path or (DATA_DIR / "google_results.json")
    total = sum(len(v) for v in results.values())
    payload = {
        "total_businesses": total,
        "verticals": {
            v: {"count": len(biz), "ads": biz}
            for v, biz in results.items()
        },
    }
    out.write_text(json.dumps(payload, indent=2))
    return out


def load_google_results(path: Path | None = None) -> dict[str, list[dict]]:
    """Load Google scan results from JSON."""
    p = path or (DATA_DIR / "google_results.json")
    data = json.loads(p.read_text())
    return {v: info["ads"] for v, info in data["verticals"].items()}


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from keywords import load_keywords

    keywords = load_keywords()
    results = asyncio.run(scan_google_ads(keywords))
    out = save_google_results(results)
    total = sum(len(v) for v in results.values())
    print(f"\nFound {total} businesses across {len(results)} verticals")
    for v, biz_list in results.items():
        paid = sum(1 for b in biz_list if b.get("has_paid_ads"))
        print(f"  {v}: {len(biz_list)} businesses ({paid} confirmed advertisers)")
    print(f"Saved to {out}")
