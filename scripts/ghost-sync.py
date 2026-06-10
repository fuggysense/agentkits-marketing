#!/usr/bin/env python3
"""scripts/ghost-sync.py — sync SQLite swipe DB → Ghost Postgres.

Final step of /ads:scrape-library. Idempotent. Safe to re-run.

What it does:
  1. Reads swipe-files/<industry>/ads-db.sqlite (canonical source)
  2. Upserts industries → pages → ads → transcripts → classifications
  3. Temporal reconciliation: ads that were ACTIVE last run but absent from this
     scrape get flipped to INACTIVE with stopped_date=today
  4. Embedding refresh via LiteLLM (provider-agnostic, Matryoshka 1024-dim)
  5. Refreshes _agent_readme stats snapshot

Usage:
  python3 scripts/ghost-sync.py property-sg
  python3 scripts/ghost-sync.py property-sg --reembed-all   # after provider swap

Env (from .env):
  GHOST_DATABASE_URL, EMBEDDING_PROVIDER, EMBEDDING_MODEL, EMBEDDING_TARGET_DIM,
  OLLAMA_API_BASE (optional — defaults to http://localhost:11434)
"""

import os
import re
import sys
import json
import sqlite3
import hashlib
import pathlib
import argparse
from datetime import date, datetime, timedelta

import psycopg

try:
    from dotenv import load_dotenv
    load_dotenv(pathlib.Path(__file__).parent.parent / ".env")
except ImportError:
    pass  # env may already be set

DSN = os.environ["GHOST_DATABASE_URL"]
EMBEDDING_PROVIDER = os.environ.get("EMBEDDING_PROVIDER", "ollama")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "ollama/nomic-embed-text")
TARGET_DIM = int(os.environ.get("EMBEDDING_TARGET_DIM", 1024))
OLLAMA_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")

SWIPE_DIR = pathlib.Path(__file__).parent.parent / "swipe-files"
MEDIA_MAP = {"image": "IMAGE", "video": "VIDEO", "carousel": "CAROUSEL"}


def parse_json_array(s):
    if not s:
        return []
    try:
        v = json.loads(s)
        return v if isinstance(v, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def parse_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def derive_start_date(first_seen, last_seen, days_running, is_active):
    """SQLite doesn't store Meta's ground-truth start_date. Derive it:
    - ACTIVE: last_seen - days_running (Meta's ad age anchor)
    - Otherwise: first_seen (lower bound from our observations)
    """
    ls = parse_date(last_seen)
    fs = parse_date(first_seen)
    if is_active and ls and days_running is not None:
        return ls - timedelta(days=int(days_running))
    return fs


def sync_industry(conn, slug):
    """Populate industries from stage-analysis.md."""
    path = SWIPE_DIR / slug / "stage-analysis.md"
    text = path.read_text() if path.exists() else ""
    stage_m = re.search(r"Stage assessment:\*\*\s*(\d)", text)
    stage = int(stage_m.group(1)) if stage_m else None
    conf_m = re.search(r"confidence:\*\*\s*(\w+)", text)
    conf = conf_m.group(1).lower() if conf_m else None
    name = slug.replace("-", " ").title()
    conn.execute(
        """
        INSERT INTO industries (slug, name, schwartz_stage, stage_confidence, stage_analysis_md)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (slug) DO UPDATE SET
            name = EXCLUDED.name,
            schwartz_stage = EXCLUDED.schwartz_stage,
            stage_confidence = EXCLUDED.stage_confidence,
            stage_analysis_md = EXCLUDED.stage_analysis_md
        """,
        (slug, name, stage, conf, text),
    )


def sync_pages(conn, slug, sqlite_conn):
    rows = sqlite_conn.execute(
        "SELECT * FROM pages WHERE industry=?", (slug,)
    ).fetchall()
    for r in rows:
        r = dict(r)
        meta = {
            k: r[k]
            for k in (
                "page_like_count",
                "scrape_count",
                "ads_collected_total",
                "ads_active_last_scrape",
                "source_url_label",
            )
            if r.get(k) is not None
        }
        cats = parse_json_array(r.get("page_categories"))
        category = cats[0] if cats else None
        conn.execute(
            """
            INSERT INTO pages (
              page_id, industry_slug, name, url, profile_pic_url, category, meta,
              first_scraped_at, last_scraped_at, last_active_scrape_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s)
            ON CONFLICT (page_id) DO UPDATE SET
                name = EXCLUDED.name,
                url = EXCLUDED.url,
                profile_pic_url = EXCLUDED.profile_pic_url,
                category = EXCLUDED.category,
                meta = EXCLUDED.meta,
                last_scraped_at = EXCLUDED.last_scraped_at,
                last_active_scrape_at = EXCLUDED.last_active_scrape_at
            """,
            (
                r["page_id"],
                slug,
                r.get("page_name"),
                r.get("page_profile_uri"),
                r.get("page_profile_picture_url"),
                category,
                json.dumps(meta),
                r.get("first_scraped"),
                r.get("last_scraped"),
                r.get("last_scraped"),
            ),
        )
    return len(rows)


def resolve_asset_url(slug, asset_path, asset_remote_url):
    if not asset_path:
        return asset_remote_url or None
    if asset_path.startswith(("http://", "https://", "file://", "blobs://")):
        return asset_path
    p = pathlib.Path(asset_path)
    if not p.is_absolute():
        p = (SWIPE_DIR / slug / asset_path).resolve()
    return f"file://{p}" if p.exists() else (asset_remote_url or f"file://{p}")


def sync_ads(conn, slug, sqlite_conn):
    rows = sqlite_conn.execute(
        "SELECT * FROM ads WHERE industry=?", (slug,)
    ).fetchall()

    # Snapshot previously-ACTIVE ids
    prev_active = {
        r[0]
        for r in conn.execute(
            "SELECT ad_archive_id FROM ads WHERE industry_slug=%s AND status='ACTIVE'",
            (slug,),
        ).fetchall()
    }
    currently_active = {
        r["ad_archive_id"] for r in rows if r["is_active"]
    }
    newly_stopped = prev_active - currently_active

    for r in rows:
        r = dict(r)
        status = "ACTIVE" if r.get("is_active") else "INACTIVE"
        start_d = derive_start_date(
            r.get("first_seen_date"),
            r.get("last_seen_date"),
            r.get("days_running"),
            r.get("is_active"),
        )
        asset_url = resolve_asset_url(
            slug, r.get("asset_local_path"), r.get("asset_remote_url")
        )
        media = (r.get("media_type") or "").lower()
        fmt = MEDIA_MAP.get(media, media.upper() if media else None)
        asset_type = "video" if media == "video" else "image"

        conn.execute(
            """
            INSERT INTO ads (
                ad_archive_id, industry_slug, page_id, format, platforms,
                headline, body_text, cta_text, asset_url, asset_type,
                status, start_date, first_seen_date, last_seen_active_date,
                days_running, regions, raw
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s::jsonb)
            ON CONFLICT (ad_archive_id) DO UPDATE SET
                page_id = EXCLUDED.page_id,
                format = EXCLUDED.format,
                platforms = EXCLUDED.platforms,
                headline = EXCLUDED.headline,
                body_text = EXCLUDED.body_text,
                cta_text = EXCLUDED.cta_text,
                asset_url = EXCLUDED.asset_url,
                asset_type = EXCLUDED.asset_type,
                status = EXCLUDED.status,
                start_date = COALESCE(ads.start_date, EXCLUDED.start_date),
                first_seen_date = LEAST(
                    COALESCE(ads.first_seen_date, EXCLUDED.first_seen_date),
                    EXCLUDED.first_seen_date
                ),
                last_seen_active_date = CASE
                    WHEN EXCLUDED.status = 'ACTIVE'
                      THEN GREATEST(
                        COALESCE(ads.last_seen_active_date, EXCLUDED.last_seen_active_date),
                        EXCLUDED.last_seen_active_date
                      )
                    ELSE ads.last_seen_active_date
                END,
                days_running = EXCLUDED.days_running,
                regions = EXCLUDED.regions,
                raw = EXCLUDED.raw
            """,
            (
                r["ad_archive_id"],
                slug,
                r["page_id"],
                fmt,
                parse_json_array(r.get("publisher_platform")),
                r.get("headline"),
                r.get("primary_text"),
                r.get("cta_button_text"),
                asset_url,
                asset_type,
                status,
                start_d,
                parse_date(r.get("first_seen_date")),
                parse_date(r.get("last_seen_date")) if status == "ACTIVE" else None,
                r.get("days_running"),
                parse_json_array(r.get("countries")),
                json.dumps(dict(r), default=str),
            ),
        )

    if newly_stopped:
        conn.execute(
            """
            UPDATE ads SET status='INACTIVE', stopped_date=CURRENT_DATE
            WHERE ad_archive_id = ANY(%s) AND stopped_date IS NULL
            """,
            (list(newly_stopped),),
        )
    return len(rows), len(newly_stopped)


def sync_transcripts(conn, slug, sqlite_conn):
    rows = sqlite_conn.execute(
        """SELECT ad_archive_id, video_transcript_path FROM ads
           WHERE industry=? AND video_transcript_path IS NOT NULL
             AND video_transcript_path != ''""",
        (slug,),
    ).fetchall()
    count = 0
    for r in rows:
        tp = r["video_transcript_path"]
        p = pathlib.Path(tp)
        if not p.is_absolute():
            p = SWIPE_DIR / slug / tp
        if not p.exists():
            continue
        text = p.read_text()
        conn.execute(
            """
            INSERT INTO transcripts (ad_archive_id, text) VALUES (%s, %s)
            ON CONFLICT (ad_archive_id) DO UPDATE SET
                text = EXCLUDED.text, created_at = now()
            """,
            (r["ad_archive_id"], text),
        )
        count += 1
    return count


def sync_classifications(conn, slug, sqlite_conn):
    rows = sqlite_conn.execute(
        """SELECT ad_archive_id, detected_angle, schwartz_awareness,
                  schwartz_sophistication, detected_mass_desire, detected_hooks,
                  classifier_model
           FROM ads WHERE industry=?""",
        (slug,),
    ).fetchall()
    count = 0
    for r in rows:
        r = dict(r)
        if not any(
            r.get(k)
            for k in ("detected_angle", "schwartz_sophistication", "schwartz_awareness")
        ):
            continue
        stage_text = (
            r.get("schwartz_sophistication") or r.get("schwartz_awareness") or ""
        )
        m = re.search(r"\d", str(stage_text))
        stage = int(m.group(0)) if m else None
        raw = {
            k: r[k]
            for k in (
                "detected_hooks",
                "detected_mass_desire",
                "schwartz_awareness",
                "schwartz_sophistication",
            )
            if r.get(k)
        }
        conn.execute(
            """
            INSERT INTO classifications
                (ad_archive_id, schwartz_stage, angle, model, raw_response)
            VALUES (%s, %s, %s, %s, %s::jsonb)
            ON CONFLICT (ad_archive_id) DO UPDATE SET
                schwartz_stage = EXCLUDED.schwartz_stage,
                angle = EXCLUDED.angle,
                model = EXCLUDED.model,
                raw_response = EXCLUDED.raw_response
            """,
            (
                r["ad_archive_id"],
                stage,
                r.get("detected_angle"),
                r.get("classifier_model") or "unknown",
                json.dumps(raw),
            ),
        )
        count += 1
    return count


def sync_embeddings(conn, slug):
    """Embed ads missing an active row via LiteLLM."""
    from litellm import embedding as litellm_embedding

    provider_id = f"{EMBEDDING_PROVIDER}:{EMBEDDING_MODEL.split('/')[-1]}"
    rows = conn.execute(
        """
        SELECT a.ad_archive_id, a.headline, a.body_text, t.text AS transcript
        FROM ads a
        LEFT JOIN transcripts t USING (ad_archive_id)
        LEFT JOIN ad_embeddings e ON e.ad_archive_id = a.ad_archive_id
            AND e.provider = %s AND e.is_active
        WHERE a.industry_slug = %s AND e.ad_archive_id IS NULL
        """,
        (provider_id, slug),
    ).fetchall()

    if not rows:
        return 0

    kwargs = {"model": EMBEDDING_MODEL}
    if EMBEDDING_PROVIDER == "ollama":
        kwargs["api_base"] = OLLAMA_API_BASE

    embedded = 0
    for ad_id, headline, body, transcript in rows:
        text = "\n".join(filter(None, [headline, body, transcript])).strip()
        if not text:
            continue
        input_hash = hashlib.sha256(text.encode()).hexdigest()
        resp = litellm_embedding(input=[text], **kwargs)
        raw_vec = resp["data"][0]["embedding"]
        native_dim = len(raw_vec)
        vec = (
            raw_vec[:TARGET_DIM]
            if native_dim >= TARGET_DIM
            else raw_vec + [0.0] * (TARGET_DIM - native_dim)
        )
        # Format as pgvector string literal
        vec_str = "[" + ",".join(f"{x:.6f}" for x in vec) + "]"
        conn.execute(
            """
            INSERT INTO ad_embeddings (
                ad_archive_id, provider, model_version, dim, embedding, native_dim,
                input_hash, is_active
            ) VALUES (%s, %s, %s, %s, %s::vector, %s, %s, true)
            ON CONFLICT (ad_archive_id, provider) DO UPDATE SET
                embedding = EXCLUDED.embedding,
                native_dim = EXCLUDED.native_dim,
                input_hash = EXCLUDED.input_hash,
                model_version = EXCLUDED.model_version,
                is_active = true,
                created_at = now()
            """,
            (
                ad_id,
                provider_id,
                EMBEDDING_MODEL,
                TARGET_DIM,
                vec_str,
                native_dim,
                input_hash,
            ),
        )
        embedded += 1

    conn.execute(
        """
        UPDATE ad_embeddings SET is_active=false
        WHERE provider != %s AND ad_archive_id IN (
            SELECT ad_archive_id FROM ads WHERE industry_slug = %s
        )
        """,
        (provider_id, slug),
    )
    return embedded


def update_agent_readme(conn):
    snap = conn.execute(
        """
        SELECT
          (SELECT COUNT(*) FROM industries),
          (SELECT COUNT(*) FROM pages),
          (SELECT COUNT(*) FROM ads),
          (SELECT COUNT(*) FROM ads WHERE status='ACTIVE'),
          (SELECT COUNT(*) FROM ads WHERE is_winner),
          (SELECT COUNT(*) FROM transcripts),
          (SELECT COUNT(*) FROM classifications),
          (SELECT provider FROM ad_embeddings WHERE is_active
            ORDER BY created_at DESC LIMIT 1)
        """
    ).fetchone()
    stats = (
        f"## Stats snapshot (as of {date.today().isoformat()})\n\n"
        f"- industries: {snap[0]}\n"
        f"- pages: {snap[1]}\n"
        f"- ads total: {snap[2]}  |  active: {snap[3]}  |  winners: {snap[4]}\n"
        f"- transcripts: {snap[5]}\n"
        f"- classifications: {snap[6]}\n"
        f"- active embedding provider: {snap[7] or 'none yet'}\n\n"
    )
    provider_block = (
        f"## Current active embedding provider\n\n"
        f"{snap[7] or 'none yet'}\n\n"
    )

    cur = conn.execute("SELECT content FROM _agent_readme WHERE id=1")
    content = cur.fetchone()[0]
    content = re.sub(
        r"## Stats snapshot.*?(?=\n## |\Z)", stats, content, flags=re.DOTALL
    )
    content = re.sub(
        r"## Current active embedding provider.*?(?=\n## |\Z)",
        provider_block,
        content,
        flags=re.DOTALL,
    )
    conn.execute(
        "UPDATE _agent_readme SET content=%s, updated_at=now() WHERE id=1",
        (content,),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("industry", help="industry slug, e.g. property-sg")
    ap.add_argument("--reembed-all", action="store_true",
                    help="Wipe embeddings and re-embed everything (after provider swap)")
    args = ap.parse_args()
    slug = args.industry

    sqlite_path = SWIPE_DIR / slug / "ads-db.sqlite"
    if not sqlite_path.exists():
        print(f"ERROR: {sqlite_path} not found", file=sys.stderr)
        sys.exit(1)

    sqlite_conn = sqlite3.connect(str(sqlite_path))
    sqlite_conn.row_factory = sqlite3.Row

    conn = psycopg.connect(DSN, connect_timeout=30, autocommit=True)

    # Industry row must exist before scrape_runs FK can reference it.
    sync_industry(conn, slug)

    run_id = conn.execute(
        "INSERT INTO scrape_runs (industry_slug, status) VALUES (%s, 'running') RETURNING id",
        (slug,),
    ).fetchone()[0]

    try:
        pages_n = sync_pages(conn, slug, sqlite_conn)
        ads_n, stopped_n = sync_ads(conn, slug, sqlite_conn)
        transcripts_n = sync_transcripts(conn, slug, sqlite_conn)
        classif_n = sync_classifications(conn, slug, sqlite_conn)

        if args.reembed_all:
            conn.execute(
                """DELETE FROM ad_embeddings WHERE ad_archive_id IN
                   (SELECT ad_archive_id FROM ads WHERE industry_slug=%s)""",
                (slug,),
            )

        embedded_n = sync_embeddings(conn, slug)
        update_agent_readme(conn)

        conn.execute(
            """UPDATE scrape_runs SET finished_at=now(), status='success',
                   pages_scraped=%s, ads_found=%s WHERE id=%s""",
            (pages_n, ads_n, run_id),
        )

        print(f"SYNC OK — {slug}")
        print(f"  pages: {pages_n}")
        print(f"  ads: {ads_n}  (newly_stopped this run: {stopped_n})")
        print(f"  transcripts: {transcripts_n}")
        print(f"  classifications: {classif_n}")
        print(f"  new embeddings: {embedded_n}")
        print(f"  provider: {EMBEDDING_PROVIDER}:{EMBEDDING_MODEL}")
    except Exception as e:
        conn.execute(
            "UPDATE scrape_runs SET finished_at=now(), status='error', error_text=%s WHERE id=%s",
            (str(e), run_id),
        )
        raise
    finally:
        sqlite_conn.close()
        conn.close()


if __name__ == "__main__":
    main()
