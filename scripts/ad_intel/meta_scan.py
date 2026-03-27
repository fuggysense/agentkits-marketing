"""Phase 2b: Meta Ad Library Scan via ScrapeCreators."""

import asyncio
import json
import time
from pathlib import Path

import aiohttp
from tqdm import tqdm
from tenacity import retry, stop_after_attempt, wait_exponential

from config import (
    SCRAPECREATORS_API_KEY,
    SCRAPECREATORS_RATE_LIMIT,
    DATA_DIR, load_blocklist,
)
from utils import normalize_domain

BASE_URL = "https://api.scrapecreators.com"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=3, max=20))
async def _search_meta_ads(
    session: aiohttp.ClientSession,
    keyword: str,
    country: str = "SG",
) -> dict:
    """Search Meta Ad Library for a keyword."""
    params = {"query": keyword, "country": country}
    headers = {"x-api-key": SCRAPECREATORS_API_KEY}

    async with session.get(
        f"{BASE_URL}/v1/facebook/adLibrary/search/ads",
        params=params, headers=headers,
    ) as resp:
        resp.raise_for_status()
        return await resp.json()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=3, max=20))
async def _get_company_ads(
    session: aiohttp.ClientSession,
    company: str,
) -> dict:
    """Get all active ads for a specific company."""
    params = {"company": company}
    headers = {"x-api-key": SCRAPECREATORS_API_KEY}

    async with session.get(
        f"{BASE_URL}/v1/facebook/adLibrary/company/ads",
        params=params, headers=headers,
    ) as resp:
        resp.raise_for_status()
        return await resp.json()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=3, max=20))
async def _search_meta_companies(
    session: aiohttp.ClientSession,
    keyword: str,
    country: str = "SG",
) -> dict:
    """Search Meta Ad Library for companies matching a keyword."""
    params = {"query": keyword, "country": country}
    headers = {"x-api-key": SCRAPECREATORS_API_KEY}

    async with session.get(
        f"{BASE_URL}/v1/facebook/adLibrary/search/companies",
        params=params, headers=headers,
    ) as resp:
        resp.raise_for_status()
        return await resp.json()


def _parse_ad_results(response: dict, keyword: str, blocklist: set[str]) -> list[dict]:
    """Parse ScrapeCreators ad search response.

    Response structure: {success, credits_remaining, searchResults: [...]}
    Each ad has: {ad_archive_id, page_id, snapshot: {page_name, body, link_url, ...}}
    """
    results = []
    ads = response.get("searchResults", response.get("data", response.get("results", [])))

    if isinstance(ads, dict):
        ads = ads.get("ads", ads.get("results", []))

    if not isinstance(ads, list):
        return results

    for ad in ads:
        snapshot = ad.get("snapshot", {})

        # Filter out media, ecommerce, and non-service-business page categories
        page_cats = [c.lower() for c in (snapshot.get("page_categories", []) or [])]
        excluded_categories = {
            "media/news company", "media", "news & media website",
            "magazine", "publisher", "newspaper", "blog",
            "e-commerce website", "shopping & retail", "product/service",
            "grocery store", "retail company", "clothing store",
            "app page", "community", "nonprofit organization",
            "government organization", "political organization",
        }
        if any(cat in excluded_categories for cat in page_cats):
            continue

        # Extract domain from link_url in snapshot
        link_url = snapshot.get("link_url", "") or ""
        domain = normalize_domain(link_url) if link_url else ""

        # Filter out redirect/platform domains that aren't the business website
        non_business_domains = {
            "fb.me", "l.facebook.com", "lm.facebook.com",
            "api.whatsapp.com", "wa.me", "bit.ly", "linktr.ee",
            "tinyurl.com", "t.co", "forms.gle", "docs.google.com",
        }
        # Filter out ecommerce / marketplace domains
        ecommerce_domains = {
            "shopee.sg", "lazada.sg", "amazon.sg", "qoo10.sg",
            "shopify.com", "etsy.com", "carousell.sg",
            "redmart.lazada.sg", "fairprice.com.sg",
        }
        if domain in non_business_domains or domain in ecommerce_domains:
            domain = ""

        if domain and domain in blocklist:
            continue

        # Extract text from body (can be string or dict)
        body = snapshot.get("body", {})
        ad_text = body.get("text", "") if isinstance(body, dict) else str(body)

        # Build FB page URL from page_id or profile URI
        page_id = ad.get("page_id", snapshot.get("page_id", ""))
        fb_page_url = snapshot.get("page_profile_uri", "")
        if not fb_page_url and page_id:
            fb_page_url = f"https://www.facebook.com/{page_id}/"

        # Extract spend from ad-level fields if available
        spend = ad.get("spend", ad.get("estimated_spend", {}))
        spend_min = spend.get("min", 0) if isinstance(spend, dict) else 0
        spend_max = spend.get("max", 0) if isinstance(spend, dict) else 0

        results.append({
            "keyword": keyword,
            "advertiser_name": snapshot.get("page_name", ""),
            "fb_page_url": fb_page_url,
            "fb_page_id": str(page_id),
            "domain": domain,
            "ad_text": ad_text[:500] if ad_text else "",
            "ad_title": snapshot.get("title", snapshot.get("link_description", "")),
            "image_url": (snapshot.get("images", [{}]) or [{}])[0].get("original_image_url", "") if snapshot.get("images") else "",
            "video_url": (snapshot.get("videos", [{}]) or [{}])[0].get("video_hd_url", "") if snapshot.get("videos") else "",
            "spend_min": spend_min,
            "spend_max": spend_max,
            "start_date": ad.get("start_date", ""),
            "is_active": True,  # search results are active ads
            "platforms": ad.get("publisher_platforms", []),
            "page_categories": snapshot.get("page_categories", []),
            "page_like_count": snapshot.get("page_like_count", 0),
            "display_format": snapshot.get("display_format", ""),
        })

    return results


def _parse_company_results(response: dict, keyword: str) -> list[dict]:
    """Parse ScrapeCreators company search response.

    Returns list of company dicts with name and page info for deep-dive.
    """
    results = []
    companies = response.get("companies", response.get("data", response.get("results", [])))

    if isinstance(companies, dict):
        companies = companies.get("companies", companies.get("results", []))

    if not isinstance(companies, list):
        return results

    for company in companies:
        name = company.get("name", company.get("page_name", ""))
        if not name:
            continue

        page_id = company.get("page_id", company.get("id", ""))
        fb_url = company.get("page_profile_uri", "")
        if not fb_url and page_id:
            fb_url = f"https://www.facebook.com/{page_id}/"

        results.append({
            "keyword": keyword,
            "advertiser_name": name,
            "fb_page_url": fb_url,
            "fb_page_id": str(page_id),
            "domain": "",  # unknown until we scrape the FB page
            "source": "company_search",
        })

    return results


async def scan_meta_ads(
    keywords_by_vertical: dict[str, list[str]],
    progress: bool = True,
    max_keywords_per_vertical: int = 50,
) -> dict[str, list[dict]]:
    """Scan Meta Ad Library for all verticals.

    Two-step strategy:
      Step 1: Keyword ad search (existing) — discover advertisers by ad content
      Step 2: Company search (new) — discover companies by name/vertical keyword

    Uses a subset of keywords per vertical (top base terms)
    since Meta search is broader than Google SERP.
    """
    if not SCRAPECREATORS_API_KEY:
        raise RuntimeError(
            "ScrapeCreators API key not set. Add SCRAPECREATORS_API_KEY to .env"
        )

    blocklist = load_blocklist()
    all_results: dict[str, list[dict]] = {}

    async with aiohttp.ClientSession() as session:
        for vertical, keywords in keywords_by_vertical.items():
            vertical_results = []
            subset = keywords[:max_keywords_per_vertical]

            # ── Step 1: Keyword ad search (existing) ──
            desc = f"Meta ads: {vertical}"
            iterator = tqdm(subset, desc=desc) if progress else subset

            for kw in iterator:
                try:
                    response = await _search_meta_ads(session, kw)
                    parsed = _parse_ad_results(response, kw, blocklist)
                    vertical_results.extend(parsed)
                except Exception as e:
                    print(f"  Meta ad search error for '{kw}': {e}")

                await asyncio.sleep(SCRAPECREATORS_RATE_LIMIT)

            # ── Step 2: Company search (new — catches businesses keyword search misses) ──
            # Track existing FB page IDs/names so we don't add duplicates
            seen_pages = {
                ad.get("fb_page_id") for ad in vertical_results if ad.get("fb_page_id")
            }
            seen_names = {
                ad.get("advertiser_name", "").lower() for ad in vertical_results
            }

            desc2 = f"Meta companies: {vertical}"
            iterator2 = tqdm(subset, desc=desc2) if progress else subset

            for kw in iterator2:
                try:
                    response = await _search_meta_companies(session, kw)
                    companies = _parse_company_results(response, kw)
                    for co in companies:
                        # Skip if we already found this company via ad search
                        if co["fb_page_id"] in seen_pages:
                            continue
                        if co["advertiser_name"].lower() in seen_names:
                            continue
                        # Add as a minimal entry — domain resolved later
                        vertical_results.append({
                            **co,
                            "ad_text": "",
                            "ad_title": "",
                            "image_url": "",
                            "video_url": "",
                            "spend_min": 0,
                            "spend_max": 0,
                            "start_date": "",
                            "is_active": True,
                            "platforms": [],
                            "page_categories": [],
                            "page_like_count": 0,
                            "display_format": "",
                        })
                        seen_pages.add(co["fb_page_id"])
                        seen_names.add(co["advertiser_name"].lower())
                except Exception as e:
                    print(f"  Meta company search error for '{kw}': {e}")

                await asyncio.sleep(SCRAPECREATORS_RATE_LIMIT)

            all_results[vertical] = vertical_results

    return all_results


async def deep_dive_top_companies(
    businesses: list[dict],
    min_score: int = 4,
    progress: bool = True,
) -> dict[str, dict]:
    """Deep-dive: get ALL active ads for top-scoring businesses.

    Called after scoring. For businesses scoring >= min_score,
    fetches their full ad catalog via the company/ads endpoint.
    Returns {business_name: {ads: [...], ad_count: N}}.
    """
    if not SCRAPECREATORS_API_KEY:
        return {}

    targets = [b for b in businesses if b.get("score", 0) >= min_score and b.get("business_name")]

    if not targets:
        return {}

    if progress:
        print(f"Deep-diving {len(targets)} businesses (score >= {min_score})...")

    results = {}
    async with aiohttp.ClientSession() as session:
        for i, biz in enumerate(targets):
            name = biz["business_name"]
            try:
                response = await _get_company_ads(session, name)
                ads = response.get("ads", response.get("data", response.get("results", [])))
                if isinstance(ads, dict):
                    ads = ads.get("ads", ads.get("results", []))
                if not isinstance(ads, list):
                    ads = []

                results[name] = {
                    "ad_count": len(ads),
                    "ads": ads[:20],  # store up to 20 for sample ad copy
                }
            except Exception as e:
                results[name] = {"error": str(e), "ad_count": 0, "ads": []}

            await asyncio.sleep(SCRAPECREATORS_RATE_LIMIT)

            if progress and (i + 1) % 10 == 0:
                print(f"  Deep-dived {i + 1}/{len(targets)} companies")

    if progress:
        total_ads = sum(r.get("ad_count", 0) for r in results.values())
        print(f"  Deep-dive complete: {total_ads} total ads from {len(results)} companies")

    return results


# ── FB Page → Website/Contact Resolution ──────────────────────────────────────

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=3, max=20))
async def _scrape_fb_page(
    session: aiohttp.ClientSession,
    fb_page_url: str,
) -> dict:
    """Scrape a Facebook business page for website, phone, email, address."""
    headers = {"x-api-key": SCRAPECREATORS_API_KEY}
    params = {"url": fb_page_url}  # ScrapeCreators uses 'url' not 'query'

    async with session.get(
        f"{BASE_URL}/v1/facebook/profile",
        params=params, headers=headers,
    ) as resp:
        resp.raise_for_status()
        data = await resp.json()

    # Response is flat — fields at top level (not nested under 'data')
    return {
        "website": data.get("website", ""),
        "phone": data.get("phone", data.get("phone_number", "")),
        "email": data.get("email", ""),
        "address": data.get("address", ""),
        "city": data.get("city", ""),
        "country": data.get("country", ""),
        "about": data.get("pageIntro", data.get("about", "")),
        "category": data.get("category", ""),
    }


async def resolve_missing_domains(
    results: dict[str, list[dict]],
    progress: bool = True,
) -> dict[str, list[dict]]:
    """For Meta ads with no website domain, scrape FB page to get it.

    Also extracts phone, email, address from FB pages.
    Returns updated results with domains + fb_contact_* fields filled in.
    """
    if not SCRAPECREATORS_API_KEY:
        return results

    # Collect unique FB pages that need resolution (across all verticals)
    pages_to_scrape: dict[str, str] = {}  # fb_page_url → fb_page_id
    for vertical, ads in results.items():
        for ad in ads:
            if not ad.get("domain") and ad.get("fb_page_url"):
                url = ad["fb_page_url"]
                if url not in pages_to_scrape:
                    pages_to_scrape[url] = ad.get("fb_page_id", "")

    if not pages_to_scrape:
        return results

    if progress:
        print(f"  Resolving {len(pages_to_scrape)} FB pages for missing domains...")

    # Scrape FB pages
    fb_data: dict[str, dict] = {}
    async with aiohttp.ClientSession() as session:
        for i, (fb_url, fb_id) in enumerate(pages_to_scrape.items()):
            try:
                data = await _scrape_fb_page(session, fb_url)
                fb_data[fb_url] = data
            except Exception as e:
                fb_data[fb_url] = {"error": str(e)}

            await asyncio.sleep(SCRAPECREATORS_RATE_LIMIT)

            if progress and (i + 1) % 10 == 0:
                print(f"    Scraped {i + 1}/{len(pages_to_scrape)} FB pages")

    # Update results with resolved data
    resolved_count = 0
    for vertical, ads in results.items():
        for ad in ads:
            fb_url = ad.get("fb_page_url", "")
            if fb_url in fb_data:
                fb = fb_data[fb_url]

                # Resolve domain from FB website
                if not ad.get("domain") and fb.get("website"):
                    new_domain = normalize_domain(fb["website"])
                    # Filter out platform domains
                    non_biz = {"fb.me", "l.facebook.com", "api.whatsapp.com",
                               "wa.me", "bit.ly", "linktr.ee", "tinyurl.com"}
                    if new_domain and new_domain not in non_biz:
                        ad["domain"] = new_domain
                        resolved_count += 1

                # Store FB contact data for later use
                ad["fb_phone"] = fb.get("phone", "")
                ad["fb_email"] = fb.get("email", "")
                ad["fb_address"] = fb.get("address", "")
                ad["fb_city"] = fb.get("city", "")
                ad["fb_country"] = fb.get("country", "")

    if progress:
        print(f"  Resolved {resolved_count}/{len(pages_to_scrape)} domains from FB pages")

    return results


def save_meta_results(results: dict[str, list[dict]], path: Path | None = None) -> Path:
    """Save Meta scan results to JSON."""
    out = path or (DATA_DIR / "meta_results.json")
    total = sum(len(v) for v in results.values())
    payload = {
        "total_ads": total,
        "verticals": {
            v: {"count": len(ads), "ads": ads}
            for v, ads in results.items()
        },
    }
    out.write_text(json.dumps(payload, indent=2))
    return out


def load_meta_results(path: Path | None = None) -> dict[str, list[dict]]:
    """Load Meta scan results from JSON."""
    p = path or (DATA_DIR / "meta_results.json")
    data = json.loads(p.read_text())
    return {v: info["ads"] for v, info in data["verticals"].items()}


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from keywords import load_keywords

    keywords = load_keywords()
    results = asyncio.run(scan_meta_ads(keywords))
    out = save_meta_results(results)
    total = sum(len(v) for v in results.values())
    print(f"Found {total} Meta ads across {len(results)} verticals")
    for v, ads in results.items():
        names = {a["advertiser_name"] for a in ads if a["advertiser_name"]}
        print(f"  {v}: {len(ads)} ads from {len(names)} unique advertisers")
    print(f"Saved to {out}")
