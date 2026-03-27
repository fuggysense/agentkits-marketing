"""Phase 4: Contact + Location + Metadata Extraction.

4-layer approach:
  Layer 1: crawl4ai (bulk, fast, free) — HTML + metadata
  Layer 2: Groq LLM extraction (fast, free tier) — structured contact/location data
  Layer 3: Firecrawl fallback (JS-heavy sites)
  Layer 4: FB page scrape (bonus contacts via ScrapeCreators)

Metadata layer (free — crawl4ai already hits the pages):
  - <title>, <meta name="description">, OG tags
  - Reveals positioning, keywords, social messaging angle
  - Enables "your ads say X but your site says Y" personalization
"""

import asyncio
import json
import re
from html.parser import HTMLParser
from pathlib import Path

from config import (
    GROQ_API_KEY, GROQ_MODEL, GROQ_RPM,
    FIRECRAWL_API_KEY, FIRECRAWL_FALLBACK_BUDGET,
    SCRAPECREATORS_API_KEY, SCRAPECREATORS_RATE_LIMIT,
    CRAWL4AI_CONCURRENCY,
    DATA_DIR,
)
from utils import extract_sg_phones, extract_emails, extract_whatsapp, extract_sg_postals

# ── Metadata Extractor ───────────────────────────────────────────────────────

class MetadataExtractor(HTMLParser):
    """Extract <title>, meta description, and OG tags from HTML."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self._in_title = False
        self.meta_description = ""
        self.og_title = ""
        self.og_description = ""
        self.og_image = ""
        self.og_type = ""
        self.og_site_name = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = (attrs_dict.get("name") or "").lower()
            prop = (attrs_dict.get("property") or "").lower()
            content = attrs_dict.get("content", "")

            if name == "description":
                self.meta_description = content
            elif prop == "og:title":
                self.og_title = content
            elif prop == "og:description":
                self.og_description = content
            elif prop == "og:image":
                self.og_image = content
            elif prop == "og:type":
                self.og_type = content
            elif prop == "og:site_name":
                self.og_site_name = content

    def handle_data(self, data):
        if self._in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def to_dict(self) -> dict:
        return {
            "page_title": self.title.strip(),
            "meta_description": self.meta_description.strip(),
            "og_title": self.og_title.strip(),
            "og_description": self.og_description.strip(),
            "og_image": self.og_image.strip(),
            "og_type": self.og_type.strip(),
            "og_site_name": self.og_site_name.strip(),
        }


def extract_metadata(html: str) -> dict:
    """Extract page metadata from HTML string."""
    parser = MetadataExtractor()
    try:
        parser.feed(html)
    except Exception:
        pass
    return parser.to_dict()


# ── Layer 1: crawl4ai ────────────────────────────────────────────────────────

async def _crawl_pages(domains: list[str]) -> dict[str, dict]:
    """Crawl homepage + /contact for each domain. Returns domain → {html, pages}."""
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

    results: dict[str, dict] = {}
    sem = asyncio.Semaphore(CRAWL4AI_CONCURRENCY)

    browser_cfg = BrowserConfig(headless=True)
    crawl_cfg = CrawlerRunConfig(
        word_count_threshold=10,
        exclude_external_links=True,
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        async def _crawl_one(domain: str):
            async with sem:
                combined_html = ""
                pages_crawled = []

                for path in ["", "/contact", "/about", "/about-us", "/contact-us",
                             "/team", "/our-team", "/locations"]:
                    url = f"https://{domain}{path}"
                    try:
                        result = await crawler.arun(url, config=crawl_cfg)
                        if not result.success or not result.html:
                            continue
                        # Skip 404 / not-found pages
                        status = getattr(result, "status_code", 200) or 200
                        if status == 404:
                            continue
                        html_lower = result.html[:3000].lower()
                        if any(sig in html_lower for sig in [
                            "page not found", "404 not found", "404 error",
                            "<title>404", "error 404",
                        ]):
                            continue
                        combined_html += f"\n<!-- PAGE: {url} -->\n{result.html}"
                        pages_crawled.append(url)
                    except Exception:
                        continue

                results[domain] = {
                    "html": combined_html,
                    "pages": pages_crawled,
                    "success": bool(combined_html),
                }

        tasks = [_crawl_one(d) for d in domains]
        await asyncio.gather(*tasks, return_exceptions=True)

    return results


# ── Layer 2: Groq LLM extraction ─────────────────────────────────────────────

GROQ_EXTRACTION_PROMPT = """Extract contact information, location data, and the key decision maker from this website HTML.
Return ONLY valid JSON matching this schema exactly:

{{
  "business_name": "",
  "phone": "",
  "email": "",
  "whatsapp": "",
  "full_address": "",
  "postal_code": "",
  "is_hq": true,
  "branches": [
    {{"name": "", "address": "", "postal": ""}}
  ],
  "branch_count": 0,
  "decision_maker_full_name": "",
  "decision_maker_first_name": "",
  "decision_maker_title": ""
}}

Rules:
- phone: Singapore format (8 digits starting with 6/8/9), include +65 prefix
- postal_code: 6-digit Singapore postal code from the HQ/main address
- is_hq: true if this is the head office or only location
- branches: list ALL unique physical locations found. If only one address, branches should be empty and branch_count=0
- If "Head Office", "Main Office", or "HQ" is labeled, that address goes in full_address
- If no explicit HQ, use the first/most prominent address

Decision maker rules:
- Look for titles: Founder, CEO, Director, Owner, Principal, Managing Director, Co-Founder
- Look for "Dr." prefix on medical/dental/aesthetic sites
- Look in "About the founder", "Meet the team", "Our team", "About us" sections
- If multiple people found, pick the most senior: Founder > CEO > Managing Director > Director > Owner
- decision_maker_first_name: the first/given name only (e.g., "Nijam" from "Dr Nijam Latiff")
- If no clear decision maker found, leave all three fields empty — do NOT guess

HTML (truncated to 8000 chars):
{html}"""


async def _groq_extract(client, html: str, domain: str) -> dict:
    """Use Groq to extract structured contact data from HTML."""
    truncated = html[:8000]

    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=GROQ_MODEL,
            messages=[
                {"role": "user", "content": GROQ_EXTRACTION_PROMPT.format(html=truncated)},
            ],
            temperature=0.1,
            max_tokens=800,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        result["extraction_source"] = "groq"
        return result
    except Exception as e:
        return {"error": str(e), "extraction_source": "groq_failed"}


# ── Layer 3: Firecrawl fallback ──────────────────────────────────────────────

async def _firecrawl_extract(domain: str) -> dict:
    """Fallback: use Firecrawl for JS-heavy sites."""
    if not FIRECRAWL_API_KEY:
        return {"error": "No Firecrawl API key", "extraction_source": "firecrawl_skipped"}

    import aiohttp

    url = "https://api.firecrawl.dev/v1/scrape"
    headers = {"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}
    payload = {
        "url": f"https://{domain}",
        "formats": ["html"],
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                resp.raise_for_status()
                data = await resp.json()
                html = data.get("data", {}).get("html", "")
                return {"html": html, "extraction_source": "firecrawl"}
    except Exception as e:
        return {"error": str(e), "extraction_source": "firecrawl_failed"}


# ── Layer 4: FB page scrape ──────────────────────────────────────────────────

async def _fb_page_scrape(fb_page_url: str) -> dict:
    """Bonus: extract contact info from Facebook business page."""
    if not SCRAPECREATORS_API_KEY or not fb_page_url:
        return {}

    import aiohttp

    params = {"url": fb_page_url}  # ScrapeCreators uses 'url' not 'query'
    headers = {"x-api-key": SCRAPECREATORS_API_KEY}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.scrapecreators.com/v1/facebook/profile",
                params=params, headers=headers,
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return {
                    "fb_phone": data.get("phone", ""),
                    "fb_email": data.get("email", ""),
                    "fb_address": data.get("address", ""),
                    "fb_website": data.get("website", ""),
                }
    except Exception:
        return {}


# ── Orchestrator ─────────────────────────────────────────────────────────────

async def extract_contacts(
    businesses: list[dict],
    progress: bool = True,
) -> list[dict]:
    """Run full 4-layer contact + location + metadata extraction.

    Takes scored businesses, returns enriched list with contact data + metadata.
    """
    if not GROQ_API_KEY:
        raise RuntimeError("Groq API key not set. Add GROQ_API_KEY to .env")

    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)

    # Filter to businesses with domains
    with_domain = [b for b in businesses if b.get("domain")]
    domains = [b["domain"] for b in with_domain]

    print(f"Layer 1: Crawling {len(domains)} domains with crawl4ai...")
    crawl_results = await _crawl_pages(domains)

    # Track Firecrawl usage
    firecrawl_used = 0
    enriched = []

    for i, biz in enumerate(with_domain):
        domain = biz["domain"]
        crawl = crawl_results.get(domain, {})
        html = crawl.get("html", "")
        contact_data = {}
        metadata = {}

        # ── Metadata extraction (free — from crawl4ai HTML) ──
        if html:
            metadata = extract_metadata(html)

        # ── Layer 2: Groq extraction ──
        if html:
            contact_data = await _groq_extract(client, html, domain)
            await asyncio.sleep(60 / GROQ_RPM)  # Rate limit
        else:
            # ── Layer 3: Firecrawl fallback ──
            if firecrawl_used < FIRECRAWL_FALLBACK_BUDGET:
                fc_result = await _firecrawl_extract(domain)
                if fc_result.get("html"):
                    html = fc_result["html"]
                    metadata = extract_metadata(html)
                    contact_data = await _groq_extract(client, html, domain)
                    await asyncio.sleep(60 / GROQ_RPM)
                    firecrawl_used += 1

        # ── Layer 4: FB page bonus data ──
        fb_data = {}
        if biz.get("fb_page_url"):
            fb_data = await _fb_page_scrape(biz["fb_page_url"])
            await asyncio.sleep(SCRAPECREATORS_RATE_LIMIT)

        # ── Regex fallback: extract directly from HTML ──
        regex_phones = extract_sg_phones(html) if html else []
        regex_emails = extract_emails(html) if html else []
        regex_whatsapp = extract_whatsapp(html) if html else []
        regex_postals = extract_sg_postals(html) if html else []

        # ── Merge all sources ──
        def _valid_sg_phone(p: str) -> bool:
            """Reject placeholder/dummy SG numbers."""
            if not p:
                return False
            digits = p.strip().replace(" ", "").replace("-", "").replace("+", "").lstrip("65")
            if len(digits) != 8:
                return False
            # Reject repeating patterns like 90000000, 88888888, 12345678
            if len(set(digits)) <= 2:
                return False
            return True

        groq_phone = contact_data.get("phone", "")
        fb_phone_val = fb_data.get("fb_phone", "")
        regex_phone_val = regex_phones[0] if regex_phones else ""

        phone = (
            (groq_phone if _valid_sg_phone(groq_phone) else "")
            or (fb_phone_val if _valid_sg_phone(fb_phone_val) else "")
            or (regex_phone_val if _valid_sg_phone(regex_phone_val) else "")
            or groq_phone or fb_phone_val or regex_phone_val  # last resort: take anything
        )
        email = (
            contact_data.get("email")
            or fb_data.get("fb_email")
            or (regex_emails[0] if regex_emails else "")
        )
        whatsapp_raw = contact_data.get("whatsapp") or (regex_whatsapp[0] if regex_whatsapp else "")
        # Normalize to clickable wa.me/ link
        if whatsapp_raw:
            digits = whatsapp_raw.strip().replace(" ", "").replace("-", "").replace("+", "")
            # Ensure country code — default to 65 (SG) if bare 8-digit number
            if len(digits) == 8 and digits[0] in "689":
                digits = "65" + digits
            whatsapp = f"https://wa.me/{digits}"
        else:
            whatsapp = ""
        address = (
            contact_data.get("full_address")
            or fb_data.get("fb_address")
            or ""
        )
        postal = (
            contact_data.get("postal_code")
            or (regex_postals[0] if regex_postals else "")
        )

        # ── Decision maker: merge Groq + FB page name ──
        dm_full = contact_data.get("decision_maker_full_name", "")
        dm_first = contact_data.get("decision_maker_first_name", "")
        dm_title = contact_data.get("decision_maker_title", "")

        # FB personal pages often have the owner as the page name (e.g., "Dr Nijam Latiff")
        if not dm_full and biz.get("meta_advertiser_name"):
            fb_name = biz["meta_advertiser_name"]
            # Heuristic: if the FB page name looks like a person's name (2-4 words,
            # starts with Dr/Mr/Ms or is title-cased without common biz suffixes)
            _name_parts = fb_name.strip().split()
            _has_title = _name_parts[0].rstrip(".").lower() in {"dr", "mr", "ms", "mrs", "prof"}
            _no_biz_suffix = not any(
                w.lower() in {"pte", "ltd", "clinic", "dental", "centre", "center",
                               "studio", "academy", "group", "services", "holdings"}
                for w in _name_parts
            )
            if _has_title and 2 <= len(_name_parts) <= 5:
                dm_full = fb_name
                dm_first = _name_parts[1] if len(_name_parts) > 1 else ""
                dm_title = _name_parts[0].rstrip(".")
            elif _no_biz_suffix and 2 <= len(_name_parts) <= 3 and fb_name[0].isupper():
                # Might be a personal name — store but don't set title
                dm_full = fb_name
                dm_first = _name_parts[0]

        enriched_biz = {
            **biz,
            # Contact
            "phone": phone,
            "email": email,
            "whatsapp": whatsapp,
            # Location
            "full_address": address,
            "postal_code": postal,
            "is_hq": contact_data.get("is_hq", True),
            "branches": contact_data.get("branches", []),
            "branch_count": contact_data.get("branch_count", 0),
            # Decision maker
            "decision_maker_full_name": dm_full,
            "decision_maker_first_name": dm_first,
            "decision_maker_title": dm_title,
            # Metadata (the new free layer)
            "page_title": metadata.get("page_title", ""),
            "meta_description": metadata.get("meta_description", ""),
            "og_title": metadata.get("og_title", ""),
            "og_description": metadata.get("og_description", ""),
            "og_image": metadata.get("og_image", ""),
            # Extraction meta
            "extraction_source": contact_data.get("extraction_source", "none"),
            "pages_crawled": crawl.get("pages", []),
            "fb_bonus_data": bool(fb_data),
        }
        enriched.append(enriched_biz)

        if progress and (i + 1) % 10 == 0:
            print(f"  Extracted {i + 1}/{len(with_domain)} businesses")

    # Add businesses without domains (Meta-only)
    no_domain = [b for b in businesses if not b.get("domain")]
    for biz in no_domain:
        enriched_biz = {
            **biz,
            "phone": "", "email": "", "whatsapp": "",
            "full_address": "", "postal_code": "",
            "is_hq": True, "branches": [], "branch_count": 0,
            "decision_maker_full_name": "", "decision_maker_first_name": "",
            "decision_maker_title": "",
            "page_title": "", "meta_description": "",
            "og_title": "", "og_description": "", "og_image": "",
            "extraction_source": "none",
            "pages_crawled": [],
            "fb_bonus_data": False,
        }
        # Try FB page if available
        if biz.get("fb_page_url"):
            fb_data = await _fb_page_scrape(biz["fb_page_url"])
            if fb_data:
                enriched_biz["phone"] = fb_data.get("fb_phone", "")
                enriched_biz["email"] = fb_data.get("fb_email", "")
                enriched_biz["full_address"] = fb_data.get("fb_address", "")
                enriched_biz["fb_bonus_data"] = True
            await asyncio.sleep(SCRAPECREATORS_RATE_LIMIT)
        enriched.append(enriched_biz)

    print(f"Firecrawl credits used: {firecrawl_used}")
    return enriched


def save_contacts(contacts: list[dict], path: Path | None = None) -> Path:
    """Save enriched contacts to JSON."""
    out = path or (DATA_DIR / "contacts.json")

    # Calculate yield stats
    total = len(contacts)
    stats = {
        "phone": sum(1 for c in contacts if c.get("phone")),
        "email": sum(1 for c in contacts if c.get("email")),
        "whatsapp": sum(1 for c in contacts if c.get("whatsapp")),
        "address": sum(1 for c in contacts if c.get("full_address")),
        "postal": sum(1 for c in contacts if c.get("postal_code")),
        "decision_maker": sum(1 for c in contacts if c.get("decision_maker_full_name")),
        "metadata": sum(1 for c in contacts if c.get("page_title")),
    }

    payload = {
        "total_contacts": total,
        "yield_stats": {k: f"{v}/{total} ({v/total:.0%})" for k, v in stats.items()} if total else {},
        "contacts": contacts,
    }
    out.write_text(json.dumps(payload, indent=2, default=str))
    return out


def load_contacts(path: Path | None = None) -> list[dict]:
    """Load enriched contacts from JSON."""
    p = path or (DATA_DIR / "contacts.json")
    data = json.loads(p.read_text())
    return data["contacts"]


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from scorer import load_scored

    businesses = load_scored()
    contacts = asyncio.run(extract_contacts(businesses))
    out = save_contacts(contacts)

    total = len(contacts)
    phones = sum(1 for c in contacts if c.get("phone"))
    emails = sum(1 for c in contacts if c.get("email"))
    meta = sum(1 for c in contacts if c.get("page_title"))
    print(f"\nExtracted contacts for {total} businesses")
    print(f"  Phone: {phones}/{total}")
    print(f"  Email: {emails}/{total}")
    print(f"  Metadata: {meta}/{total}")
    print(f"Saved to {out}")
