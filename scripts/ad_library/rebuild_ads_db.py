#!/usr/bin/env python3
"""Rebuild swipe-files/<industry>/ads-db.sqlite from per-ad JSON files.

Walks every ad JSON in the industry, flattens nested fields into columns,
drops + recreates the ads + pages tables (idempotent rebuild).

Usage:
  python3 scripts/ad_library/rebuild_ads_db.py --industry property-sg
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SWIPE_ROOT = ROOT / "swipe-files"

ADS_SCHEMA = """
CREATE TABLE ads (
  ad_archive_id           TEXT PRIMARY KEY,
  page_id                 TEXT NOT NULL,
  page_name               TEXT,
  industry                TEXT,
  scrape_date             TEXT,
  scrape_source           TEXT,
  first_seen_date         TEXT,
  last_seen_date          TEXT,
  days_running            INTEGER,
  is_active               INTEGER,
  media_type              TEXT,
  display_format          TEXT,
  asset_local_path        TEXT,
  asset_remote_url        TEXT,
  publisher_platform      TEXT,
  primary_text            TEXT,
  headline                TEXT,
  description             TEXT,
  cta_button_text         TEXT,
  cta_type                TEXT,
  cta_link                TEXT,
  caption                 TEXT,
  video_transcript_path   TEXT,
  image_ocr_path          TEXT,
  detected_hooks          TEXT,
  detected_angle          TEXT,
  detected_mass_desire    TEXT,
  schwartz_awareness      TEXT,
  schwartz_sophistication TEXT,
  classifier_model        TEXT,
  classified_at           TEXT,
  countries               TEXT,
  page_categories         TEXT
);
CREATE INDEX idx_ads_page         ON ads(page_id);
CREATE INDEX idx_ads_days         ON ads(days_running);
CREATE INDEX idx_ads_active       ON ads(is_active);
CREATE INDEX idx_ads_stage        ON ads(schwartz_sophistication);
CREATE INDEX idx_ads_media_type   ON ads(media_type);
"""

PAGES_SCHEMA = """
CREATE TABLE pages (
  page_id                 TEXT PRIMARY KEY,
  page_name               TEXT,
  industry                TEXT,
  page_profile_uri        TEXT,
  page_profile_picture_url TEXT,
  page_categories         TEXT,
  page_like_count         INTEGER,
  first_scraped           TEXT,
  last_scraped            TEXT,
  scrape_count            INTEGER,
  ads_collected_total     INTEGER,
  ads_active_last_scrape  INTEGER,
  source_url_label        TEXT
);
"""


def flatten_ad(ad: dict) -> tuple:
    run = ad.get("run") or {}
    cre = ad.get("creative") or {}
    cop = ad.get("copy") or {}
    enr = ad.get("enrichment") or {}
    tgt = ad.get("targeting_hints") or {}
    return (
        ad.get("ad_archive_id"),
        ad.get("page_id"),
        ad.get("page_name"),
        ad.get("industry"),
        ad.get("scrape_date"),
        ad.get("scrape_source"),
        run.get("first_seen_date"),
        run.get("last_seen_date"),
        run.get("days_running"),
        1 if run.get("is_active") else 0,
        cre.get("media_type"),
        cre.get("format"),
        cre.get("asset_local_path"),
        cre.get("asset_remote_url"),
        json.dumps(cre.get("publisher_platform") or []),
        cop.get("primary_text"),
        cop.get("headline"),
        cop.get("description"),
        cop.get("cta_button_text"),
        cop.get("cta_type"),
        cop.get("cta_link"),
        cop.get("caption"),
        enr.get("video_transcript_path"),
        enr.get("image_ocr_path"),
        json.dumps(enr.get("detected_hooks") or []),
        enr.get("detected_angle"),
        enr.get("detected_mass_desire"),
        enr.get("schwartz_awareness_estimate"),
        enr.get("schwartz_sophistication_stage"),
        enr.get("classifier_model"),
        enr.get("classified_at"),
        json.dumps(tgt.get("countries") or []),
        json.dumps(tgt.get("page_categories") or []),
    )


def flatten_page(meta: dict) -> tuple:
    return (
        meta.get("page_id"),
        meta.get("page_name"),
        meta.get("industry"),
        meta.get("page_profile_uri"),
        meta.get("page_profile_picture_url"),
        json.dumps(meta.get("page_categories") or []),
        meta.get("page_like_count"),
        meta.get("first_scraped"),
        meta.get("last_scraped"),
        meta.get("scrape_count"),
        meta.get("ads_collected_total"),
        meta.get("ads_active_last_scrape"),
        meta.get("source_url_label"),
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--industry", required=True)
    args = ap.parse_args()

    industry_dir = SWIPE_ROOT / args.industry
    if not industry_dir.exists():
        print(f"ERR: {industry_dir} not found", file=sys.stderr)
        return 1

    db_path = industry_dir / "ads-db.sqlite"
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(ADS_SCHEMA)
        conn.executescript(PAGES_SCHEMA)

        ad_rows = []
        for ad_file in sorted(industry_dir.glob("pages/*/ads/*.json")):
            try:
                ad_rows.append(flatten_ad(json.loads(ad_file.read_text(encoding="utf-8"))))
            except Exception as e:  # noqa: BLE001
                print(f"WARN: skipping {ad_file}: {e}", file=sys.stderr)
        if ad_rows:
            placeholders = ",".join(["?"] * len(ad_rows[0]))
            conn.executemany(f"INSERT INTO ads VALUES ({placeholders})", ad_rows)

        page_rows = []
        for meta_file in sorted(industry_dir.glob("pages/*/meta.json")):
            try:
                page_rows.append(flatten_page(json.loads(meta_file.read_text(encoding="utf-8"))))
            except Exception as e:  # noqa: BLE001
                print(f"WARN: skipping {meta_file}: {e}", file=sys.stderr)
        if page_rows:
            placeholders = ",".join(["?"] * len(page_rows[0]))
            conn.executemany(f"INSERT INTO pages VALUES ({placeholders})", page_rows)

        conn.commit()
    finally:
        conn.close()

    print(f"[rebuild] db={db_path.relative_to(ROOT)} ads={len(ad_rows)} pages={len(page_rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
