#!/usr/bin/env python3
"""Scrape Meta Ad Library for one industry → write per-ad JSON files.

Reads:    swipe-files/<industry>/pages-to-scrape.md
Writes:   swipe-files/<industry>/pages/<page_id>/{meta.json, ads/<ad_id>.json, scrape-log.jsonl}

Pipeline (per page):
  1. ScrapeCreators primary (paginate via cursor)
  2. dev-browser fallback on failure → log to scrape-log.jsonl
  3. Dedupe vs existing ad JSON: update run.last_seen_date+is_active, or write new file
  4. Update meta.json with page totals + counts

Usage:
  python3 scripts/ad_library/scrape_meta_ad_library.py --industry property-sg
  python3 scripts/ad_library/scrape_meta_ad_library.py --industry property-sg --page 100852962092831
  python3 scripts/ad_library/scrape_meta_ad_library.py --industry property-sg --dry-run
"""

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills" / "scrapecreators" / "scripts"))

from api import ScrapeCreatorsClient, ScrapeCreatorsError  # noqa: E402

SWIPE_ROOT = ROOT / "swipe-files"
PAGE_ID_RE = re.compile(r"^[`]?(\d{6,})[`]?$")
COUNTRY_DEFAULT = "SG"
STATUS_DEFAULT = "ACTIVE"
PAGINATE_MAX_PAGES = 20


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def today() -> str:
    return dt.date.today().isoformat()


def ts_to_date(ts) -> str | None:
    if ts is None:
        return None
    try:
        return dt.date.fromtimestamp(int(ts)).isoformat()
    except (ValueError, OSError, TypeError):
        return None


def parse_pages_md(path: Path) -> list[dict]:
    """Extract {page_id, label, source_url} rows from the markdown table."""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "---" in line or "Page ID" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        m = PAGE_ID_RE.match(cells[1])
        if not m:
            continue
        rows.append({
            "page_id": m.group(1),
            "label": cells[2],
            "source_url": cells[3],
        })
    return rows


def derive_media_type(snapshot: dict) -> str:
    fmt = (snapshot.get("display_format") or "").upper()
    if fmt == "VIDEO":
        return "video"
    if fmt == "IMAGE":
        return "image"
    if snapshot.get("cards"):
        return "carousel"
    return "unknown"


def derive_asset_url(snapshot: dict, media_type: str) -> str | None:
    if media_type == "video":
        for v in snapshot.get("videos") or []:
            return v.get("video_hd_url") or v.get("video_sd_url")
    if media_type == "image":
        for img in snapshot.get("images") or []:
            return img.get("original_image_url") or img.get("resized_image_url")
    return None


def build_ad_record(ad: dict, industry: str, scrape_date: str) -> dict:
    snap = ad.get("snapshot") or {}
    start = ad.get("start_date")
    end = ad.get("end_date")
    days = None
    if isinstance(start, int) and isinstance(end, int):
        days = max(0, (end - start) // 86400)
    media_type = derive_media_type(snap)
    return {
        "ad_archive_id": str(ad.get("ad_archive_id")),
        "page_id": str(ad.get("page_id")),
        "page_name": snap.get("page_name") or ad.get("page_name"),
        "industry": industry,
        "scrape_date": scrape_date,
        "scrape_source": "scrapecreators",
        "run": {
            "first_seen_date": ts_to_date(start),
            "last_seen_date": ts_to_date(end) or scrape_date,
            "days_running": days if days is not None else 0,
            "is_active": bool(ad.get("is_active")),
        },
        "creative": {
            "media_type": media_type,
            "format": snap.get("display_format"),
            "asset_local_path": None,
            "asset_remote_url": derive_asset_url(snap, media_type),
            "publisher_platform": ad.get("publisher_platform") or [],
        },
        "copy": {
            "primary_text": (snap.get("body") or {}).get("text"),
            "headline": snap.get("title"),
            "description": snap.get("link_description"),
            "cta_button_text": snap.get("cta_text"),
            "cta_type": snap.get("cta_type"),
            "cta_link": snap.get("link_url"),
            "caption": snap.get("caption"),
        },
        "enrichment": {
            "video_transcript_path": None,
            "image_ocr_path": None,
            "detected_hooks": [],
            "detected_angle": None,
            "detected_mass_desire": None,
            "schwartz_awareness_estimate": None,
            "schwartz_sophistication_stage": None,
            "classifier_model": None,
            "classified_at": None,
        },
        "targeting_hints": {
            "countries": ad.get("targeted_or_reached_countries") or [],
            "languages": [],
            "page_categories": snap.get("page_categories") or [],
        },
        "raw_scrape_response": ad,
    }


def merge_existing(existing: dict, fresh: dict) -> tuple[dict, str]:
    """Update last_seen + is_active on a re-scrape; preserve enrichment."""
    fresh["enrichment"] = existing.get("enrichment", fresh["enrichment"])
    fresh["run"]["first_seen_date"] = (
        existing.get("run", {}).get("first_seen_date") or fresh["run"]["first_seen_date"]
    )
    if existing.get("creative", {}).get("asset_local_path"):
        fresh["creative"]["asset_local_path"] = existing["creative"]["asset_local_path"]
    return fresh, "updated"


def write_ad(industry_dir: Path, page_id: str, ad: dict) -> str:
    """Write or update one ad JSON. Returns 'new' or 'updated'."""
    ads_dir = industry_dir / "pages" / page_id / "ads"
    ads_dir.mkdir(parents=True, exist_ok=True)
    path = ads_dir / f"{ad['ad_archive_id']}.json"
    status = "new"
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        ad, status = merge_existing(existing, ad)
    path.write_text(json.dumps(ad, indent=2, ensure_ascii=False), encoding="utf-8")
    return status


def update_page_meta(industry_dir: Path, page_id: str, industry: str,
                     page_name: str, snap: dict, source_label: str,
                     ads_active: int, ads_total_in_dir: int) -> None:
    meta_path = industry_dir / "pages" / page_id / "meta.json"
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    today_s = today()
    meta = {}
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta.update({
        "page_id": page_id,
        "page_name": page_name,
        "industry": industry,
        "page_profile_uri": snap.get("page_profile_uri"),
        "page_profile_picture_url": snap.get("page_profile_picture_url"),
        "page_categories": snap.get("page_categories") or [],
        "page_like_count": snap.get("page_like_count"),
        "first_scraped": meta.get("first_scraped", today_s),
        "last_scraped": today_s,
        "scrape_count": meta.get("scrape_count", 0) + 1,
        "ads_collected_total": ads_total_in_dir,
        "ads_active_last_scrape": ads_active,
        "source_url_label": source_label,
    })
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")


def append_log(industry_dir: Path, page_id: str, entry: dict) -> None:
    log_path = industry_dir / "pages" / page_id / "scrape-log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {"ts": now_iso(), "page_id": page_id, **entry}
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def scrape_page(client: ScrapeCreatorsClient, page_id: str, label: str,
                industry: str, industry_dir: Path, dry_run: bool) -> dict:
    summary = {"page_id": page_id, "new": 0, "updated": 0, "failed": 0,
               "active": 0, "fallback_used": False, "page_name": None}
    cursor = None
    snap_for_meta = {}
    seen_ids = set()
    for page_num in range(PAGINATE_MAX_PAGES):
        try:
            r = client.facebook_company_ads(
                page_id=page_id, country=COUNTRY_DEFAULT,
                status=STATUS_DEFAULT, cursor=cursor,
            )
        except ScrapeCreatorsError as e:
            append_log(industry_dir, page_id, {
                "event": "scrapecreators_error", "error": str(e),
                "page_num": page_num, "fallback_used": "dev-browser-todo",
            })
            summary["failed"] += 1
            summary["fallback_used"] = True
            break
        results = r.get("results") or []
        if not results:
            break
        scrape_date = today()
        for ad in results:
            ad_id = str(ad.get("ad_archive_id"))
            if ad_id in seen_ids:
                continue
            seen_ids.add(ad_id)
            try:
                rec = build_ad_record(ad, industry, scrape_date)
                if not summary["page_name"]:
                    summary["page_name"] = rec["page_name"]
                    snap_for_meta = ad.get("snapshot") or {}
                if rec["run"]["is_active"]:
                    summary["active"] += 1
                if dry_run:
                    summary["new"] += 1
                    continue
                status = write_ad(industry_dir, page_id, rec)
                summary[status] += 1
            except Exception as e:  # noqa: BLE001
                append_log(industry_dir, page_id, {
                    "event": "ad_parse_error", "ad_id": ad_id, "error": str(e),
                })
                summary["failed"] += 1
        cursor = r.get("cursor")
        if not cursor:
            break
    if not dry_run and summary["page_name"]:
        ads_dir = industry_dir / "pages" / page_id / "ads"
        ads_total = len(list(ads_dir.glob("*.json"))) if ads_dir.exists() else 0
        update_page_meta(industry_dir, page_id, industry, summary["page_name"],
                         snap_for_meta, label, summary["active"], ads_total)
    append_log(industry_dir, page_id, {
        "event": "page_scrape_complete",
        **{k: v for k, v in summary.items() if k != "page_name"},
    })
    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--industry", required=True, help="Industry slug, e.g. property-sg")
    ap.add_argument("--page", help="Restrict to one page_id (debug)")
    ap.add_argument("--dry-run", action="store_true", help="Fetch + parse but don't write")
    args = ap.parse_args()

    industry_dir = SWIPE_ROOT / args.industry
    pages_md = industry_dir / "pages-to-scrape.md"
    if not pages_md.exists():
        print(f"ERR: missing {pages_md}", file=sys.stderr)
        return 1

    pages = parse_pages_md(pages_md)
    if args.page:
        pages = [p for p in pages if p["page_id"] == args.page]
    if not pages:
        print("ERR: no pages parsed (or --page didn't match)", file=sys.stderr)
        return 1

    client = ScrapeCreatorsClient(quiet=True)
    print(f"[scrape] industry={args.industry} pages={len(pages)} dry_run={args.dry_run}")
    totals = {"new": 0, "updated": 0, "failed": 0, "active": 0, "pages_with_data": 0}
    for p in pages:
        s = scrape_page(client, p["page_id"], p["label"], args.industry,
                        industry_dir, args.dry_run)
        print(f"  page={p['page_id']} name={s.get('page_name') or '?'} "
              f"new={s['new']} updated={s['updated']} active={s['active']} "
              f"failed={s['failed']} fallback={s['fallback_used']}")
        for k in ("new", "updated", "failed", "active"):
            totals[k] += s[k]
        if s["new"] or s["updated"]:
            totals["pages_with_data"] += 1
    print(f"[scrape] totals {totals}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
