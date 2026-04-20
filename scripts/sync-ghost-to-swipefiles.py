#!/usr/bin/env python3
"""Mirror Ghost Postgres → swipe-files/ filesystem (repo).

One-way pull. For every page in an industry, writes:
  swipe-files/<industry>/pages/<page_id>/page.json
  swipe-files/<industry>/pages/<page_id>/ads/<ad_archive_id>.json

Each ad JSON carries metadata, body text, transcript, OCR, and classification
(if present). Asset URLs are preserved as Meta CDN links — assets are NOT
downloaded. Idempotent: writes only when content differs.

Usage:
  python3 scripts/sync-ghost-to-swipefiles.py --industry property-sg
  python3 scripts/sync-ghost-to-swipefiles.py --all-industries
  python3 scripts/sync-ghost-to-swipefiles.py --industry property-sg --dry-run
"""

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

ROOT = Path(__file__).resolve().parents[1]
SWIPE_ROOT = ROOT / "swipe-files"
DEFAULT_DB = os.environ.get("GHOST_DATABASE_URL")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def json_default(o):
    import decimal
    if isinstance(o, (dt.datetime, dt.date)):
        return o.isoformat()
    if isinstance(o, decimal.Decimal):
        return float(o)
    raise TypeError(f"not serializable: {type(o)}")


def dump_json(path: Path, data, dry_run: bool = False) -> bool:
    """Write JSON only if content differs. Returns True if would-write/did-write."""
    new = json.dumps(data, indent=2, ensure_ascii=False,
                     sort_keys=True, default=json_default)
    if path.exists():
        try:
            if path.read_text(encoding="utf-8") == new:
                return False
        except OSError:
            pass
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new, encoding="utf-8")
    return True


def sync_industry(conn, industry: str, dry_run: bool) -> dict:
    stats = {"industry": industry, "pages_written": 0, "ads_written": 0,
             "pages_skipped": 0, "ads_skipped": 0}

    industry_dir = SWIPE_ROOT / industry
    pages_dir = industry_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""
            SELECT page_id, industry_slug, name, url, profile_pic_url, category,
                   verified, meta, first_scraped_at, last_scraped_at,
                   last_active_scrape_at, last_full_scrape_at, full_history_complete
            FROM pages WHERE industry_slug = %s ORDER BY page_id
        """, (industry,))
        pages = cur.fetchall()

    for page in pages:
        page_id = page["page_id"]
        page_path = pages_dir / page_id / "page.json"
        if dump_json(page_path, page, dry_run):
            stats["pages_written"] += 1
            if dry_run: print(f"  would write page {page_id}")
        else:
            stats["pages_skipped"] += 1

        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT a.ad_archive_id, a.page_id, a.format, a.platforms,
                       a.headline, a.body_text, a.cta_text, a.asset_url, a.asset_type,
                       a.meta_library_url, a.status, a.start_date, a.first_seen_date,
                       a.last_seen_active_date, a.stopped_date, a.days_running,
                       a.regions, a.is_winner, a.is_active, a.ocr_text,
                       a.ocr_extracted_at, a.ocr_model,
                       t.text AS transcript_text,
                       t.language AS transcript_language,
                       t.duration_sec AS transcript_duration_sec,
                       c.schwartz_stage, c.angle, c.avatar_fit, c.blue_box_category,
                       c.model AS classifier_model, c.confidence AS classifier_confidence,
                       c.raw_response AS classifier_raw
                FROM ads a
                LEFT JOIN transcripts t ON t.ad_archive_id = a.ad_archive_id
                LEFT JOIN classifications c ON c.ad_archive_id = a.ad_archive_id
                WHERE a.page_id = %s
                ORDER BY a.ad_archive_id
            """, (page_id,))
            ads = cur.fetchall()

        ads_dir = pages_dir / page_id / "ads"
        ads_dir.mkdir(parents=True, exist_ok=True)
        for ad in ads:
            ad_id = ad["ad_archive_id"]
            ad_path = ads_dir / f"{ad_id}.json"
            # Strip tsv (Postgres internal) & raw (bulky, not useful in repo)
            ad.pop("tsv", None)
            if dump_json(ad_path, ad, dry_run):
                stats["ads_written"] += 1
                if dry_run: print(f"    would write ad {ad_id}")
            else:
                stats["ads_skipped"] += 1

    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--industry")
    ap.add_argument("--all-industries", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--db", default=DEFAULT_DB)
    args = ap.parse_args()

    if not args.db:
        print("ERROR: GHOST_DATABASE_URL env var or --db required", file=sys.stderr)
        return 2
    if not (args.industry or args.all_industries):
        print("ERROR: provide --industry SLUG or --all-industries", file=sys.stderr)
        return 2

    print(f"[{now_iso()}] sync-ghost-to-swipefiles dry_run={args.dry_run}")

    with psycopg.connect(args.db) as conn:
        if args.all_industries:
            with conn.cursor() as cur:
                cur.execute("SELECT slug FROM industries ORDER BY slug")
                slugs = [r[0] for r in cur.fetchall()]
        else:
            slugs = [args.industry]

        for slug in slugs:
            stats = sync_industry(conn, slug, args.dry_run)
            print(f"  {slug}: pages_written={stats['pages_written']} "
                  f"ads_written={stats['ads_written']} "
                  f"pages_skipped={stats['pages_skipped']} "
                  f"ads_skipped={stats['ads_skipped']}")

    print(f"[{now_iso()}] done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
