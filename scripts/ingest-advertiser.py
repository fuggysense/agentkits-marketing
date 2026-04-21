#!/usr/bin/env python3
"""scripts/ingest-advertiser.py — scrape one advertiser via ScrapeCreators
and upsert into the Ghost Postgres DB.

Called by the Swipe dashboard's /api/scrape-advertiser endpoint. Also usable
standalone from CLI.

Usage:
  python3 scripts/ingest-advertiser.py <page_id> <industry_slug> [--depth active|full] [--country SG]

Output: single JSON line on stdout
  {"ok": true, "page_id": "...", "page_name": "...", "ads_inserted": N, "ads_updated": N, "ad_ids": [...]}

Exit codes: 0 = success, 1 = fatal error (JSON error on stdout).
"""

import argparse
import json
import os
import pathlib
import sys
import time
import urllib.request
from datetime import datetime, date, timedelta
from typing import Any
from urllib.error import URLError

sys.path.insert(
    0,
    str(pathlib.Path(__file__).parent.parent / "skills" / "scrapecreators" / "scripts"),
)

from api import ScrapeCreatorsClient  # noqa: E402

try:
    from dotenv import load_dotenv
    load_dotenv(pathlib.Path(__file__).parent.parent / ".env")
except ImportError:
    pass

import psycopg  # noqa: E402

DSN = os.environ.get("GHOST_DATABASE_URL")
SC_KEY = os.environ.get("SCRAPECREATORS_API_KEY")

# OCR config — Gemini 2.5 Flash Vision
_GEMINI_KEYS = [
    os.environ.get("GEMINI_API_KEY"),
    os.environ.get("GEMINI_API_KEY_2"),
    os.environ.get("GEMINI_API_KEY_3"),
]
_GEMINI_KEYS = [k for k in _GEMINI_KEYS if k]
_OCR_MODEL = "gemini-2.5-flash"
_OCR_PROMPT = (
    "Extract ALL visible text from this advertisement image. "
    "Output the text verbatim, preserve line breaks, no commentary, "
    "no introduction, no markdown. If there is no text, output exactly: [no text]"
)


def _ocr_image(asset_url: str) -> str | None:
    """Download image and OCR via Gemini Vision. Returns text or None on failure.
    Never raises — OCR failure must not break ingestion."""
    if not _GEMINI_KEYS or not asset_url or not asset_url.startswith("http"):
        return None
    try:
        import google.generativeai as genai
        req = urllib.request.Request(asset_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            img_bytes = resp.read()
            mime = resp.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
        if len(img_bytes) > 20_000_000:
            return None
        last_err = None
        for ki, key in enumerate(_GEMINI_KEYS):
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel(_OCR_MODEL)
                result = model.generate_content(
                    [_OCR_PROMPT, {"mime_type": mime, "data": img_bytes}],
                    generation_config={"temperature": 0},
                )
                text = result.text.strip()
                return None if (not text or text == "[no text]") else text
            except Exception as e:
                last_err = str(e)
                if any(x in last_err for x in ("429", "RESOURCE_EXHAUSTED", "quota", "rate")):
                    time.sleep(1)
                    continue
                raise
        print(f"WARN: OCR all keys failed: {last_err}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"WARN: OCR skipped ({type(e).__name__}: {str(e)[:120]})", file=sys.stderr)
        return None


def _should_ocr(conn, ad_archive_id: str) -> bool:
    """True if this image ad doesn't have OCR text yet."""
    row = conn.execute(
        "SELECT ocr_text FROM ads WHERE ad_archive_id = %s", (ad_archive_id,)
    ).fetchone()
    return row is not None and row[0] is None


_SWIPE_ROOT = pathlib.Path(__file__).parent.parent / "swipe-files"


def _local_video_path(industry: str, page_id: str, ad_archive_id: str) -> pathlib.Path:
    """Deterministic local path for a video asset. Matches enrich_scraped_ads convention."""
    return _SWIPE_ROOT / industry / "pages" / page_id / "ads" / "assets" / f"{ad_archive_id}.mp4"


def _resolve_ffmpeg() -> str | None:
    """Find a working ffmpeg binary, skipping the known-broken ~/.darkbloom symlink."""
    import shutil
    found = shutil.which("ffmpeg")
    if found and ".darkbloom" not in found:
        return found
    for candidate in ("/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"):
        if pathlib.Path(candidate).exists():
            return candidate
    return None


def _compress_video(src: pathlib.Path, dest: pathlib.Path) -> bool:
    """Compress src → dest at 720p H.264 CRF 25 AAC 128k (HandBrake "Fast 720p"
    preset equivalent). Returns True on success."""
    import subprocess
    ff = _resolve_ffmpeg()
    if not ff:
        return False
    try:
        result = subprocess.run(
            [
                ff, "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(src),
                "-vf", "scale='min(1280,iw)':'min(720,ih)':"
                       "force_original_aspect_ratio=decrease:force_divisible_by=2",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "25",
                "-c:a", "aac",
                "-b:a", "128k",
                "-movflags", "+faststart",
                str(dest),
            ],
            capture_output=True, text=True, timeout=300,
        )
        if result.returncode != 0:
            print(f"WARN: ffmpeg compress failed rc={result.returncode} {result.stderr[:200]}", file=sys.stderr)
            return False
        return dest.exists() and dest.stat().st_size > 0
    except Exception as e:
        print(f"WARN: ffmpeg compress exception: {e}", file=sys.stderr)
        return False


def _save_video_asset(asset_url: str, industry: str, page_id: str, ad_archive_id: str) -> pathlib.Path | None:
    """Download + compress video to a persistent local path.

    Meta CDN URLs expire within days, so we save a compressed local copy at
    scrape time so downstream transcription keeps working. Idempotent —
    returns existing file if already saved. Never raises.

    Flow: HTTP download to temp → ffmpeg 720p/CRF25/AAC128k → final path.
    If ffmpeg unavailable, stores the raw download uncompressed (still works,
    just bigger). Typical ~80% size reduction after compression.
    """
    if not asset_url or not asset_url.startswith("http"):
        return None
    dest = _local_video_path(industry, page_id, ad_archive_id)
    if dest.exists() and dest.stat().st_size > 0:
        return dest

    import tempfile
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Download raw to a temp file in the same directory (same filesystem for atomic rename)
    raw_tmp = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=dest.parent, prefix=f".{ad_archive_id}-raw-", suffix=".mp4", delete=False
        ) as tf:
            raw_tmp = pathlib.Path(tf.name)
            req = urllib.request.Request(asset_url, headers={"User-Agent": "Mozilla/5.0"})
            max_size = 500_000_000  # 500MB input cap (before compression)
            total = 0
            with urllib.request.urlopen(req, timeout=60) as resp:
                while chunk := resp.read(65536):
                    total += len(chunk)
                    if total > max_size:
                        raw_tmp.unlink(missing_ok=True)
                        print(f"WARN: video {ad_archive_id} raw exceeded 500MB; aborted", file=sys.stderr)
                        return None
                    tf.write(chunk)

        # Compress to final destination; if ffmpeg missing/fails, keep raw as-is.
        if _compress_video(raw_tmp, dest):
            # Success — remove raw, keep compressed
            raw_tmp.unlink(missing_ok=True)
        else:
            # Compression unavailable or failed — move raw into place as fallback.
            raw_tmp.rename(dest)
            print(f"INFO: video {ad_archive_id} stored uncompressed (ffmpeg unavailable or failed)", file=sys.stderr)
        return dest
    except Exception as e:
        print(f"WARN: video save failed for {ad_archive_id}: {type(e).__name__}: {str(e)[:120]}", file=sys.stderr)
        if raw_tmp and raw_tmp.exists():
            raw_tmp.unlink(missing_ok=True)
        if dest.exists() and dest.stat().st_size == 0:
            dest.unlink(missing_ok=True)
        return None


def parse_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        # Meta sends ISO8601 "2026-01-15T08:00:00.000Z" OR epoch
        if isinstance(s, (int, float)) or (isinstance(s, str) and s.isdigit()):
            return datetime.fromtimestamp(int(s)).date()
        return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
    except (ValueError, TypeError):
        return None


def ensure_industry(conn, slug: str):
    conn.execute(
        """
        INSERT INTO industries (slug, name)
        VALUES (%s, %s)
        ON CONFLICT (slug) DO NOTHING
        """,
        (slug, slug.replace("-", " ").title()),
    )


def upsert_page(conn, slug: str, page_id: str, snap: dict) -> str:
    name = snap.get("page_name") or f"Page {page_id}"
    conn.execute(
        """
        INSERT INTO pages (
            page_id, industry_slug, name, url, profile_pic_url, category,
            meta, first_scraped_at, last_scraped_at, last_active_scrape_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, now(), now(), now())
        ON CONFLICT (page_id) DO UPDATE SET
            name = EXCLUDED.name,
            url = COALESCE(EXCLUDED.url, pages.url),
            profile_pic_url = COALESCE(EXCLUDED.profile_pic_url, pages.profile_pic_url),
            last_scraped_at = now(),
            last_active_scrape_at = now()
        """,
        (
            page_id,
            slug,
            name,
            snap.get("page_profile_uri"),
            snap.get("page_profile_picture_url"),
            (snap.get("page_categories") or [None])[0] if isinstance(snap.get("page_categories"), list) else None,
            json.dumps(
                {
                    k: snap.get(k)
                    for k in ("page_like_count", "page_is_deleted", "byline")
                    if snap.get(k) is not None
                }
            ),
        ),
    )
    return name


def upsert_ad(conn, slug: str, page_id: str, ad: dict) -> tuple[bool, str]:
    """Returns (was_insert, ad_archive_id)."""
    ad_archive_id = str(ad.get("ad_archive_id") or ad.get("id") or "")
    if not ad_archive_id:
        raise ValueError("ad has no archive_id")
    snap = ad.get("snapshot") or {}

    # Dates: Meta gives start_date_string as ISO; end_date_string when inactive
    start_raw = (
        ad.get("start_date_string")
        or ad.get("start_date")
        or snap.get("start_date")
    )
    end_raw = ad.get("end_date_string") or ad.get("end_date")
    start_d = parse_date(start_raw)
    is_active_flag = ad.get("is_active")
    if is_active_flag is None:
        is_active_flag = not end_raw  # fallback: active if no end date
    status = "ACTIVE" if is_active_flag else "INACTIVE"
    today = date.today()
    last_seen_active = today if status == "ACTIVE" else None
    stopped = parse_date(end_raw) if status == "INACTIVE" else None
    # days_running: prefer Meta's field, else derive
    days_running = snap.get("days_running")
    if days_running is None and start_d:
        if status == "ACTIVE":
            days_running = (today - start_d).days
        elif stopped:
            days_running = (stopped - start_d).days

    body = snap.get("body") or {}
    body_text = body.get("text") if isinstance(body, dict) else str(body)
    headline = snap.get("title")
    cta_text = snap.get("cta_text")
    link_url = snap.get("link_url")

    # Asset resolution
    videos = snap.get("videos") or []
    images = snap.get("images") or []
    cards = snap.get("cards") or []
    display_format = snap.get("display_format") or ""
    if videos:
        media = "video"
        fmt = "VIDEO"
        asset_url = (
            videos[0].get("video_hd_url")
            or videos[0].get("video_sd_url")
            or videos[0].get("video_preview_image_url")
        )
    elif cards:
        media = "carousel"
        fmt = "CAROUSEL"
        first_card_img = (cards[0] or {}).get("original_image_url") or (cards[0] or {}).get("resized_image_url")
        asset_url = first_card_img
    elif images:
        media = "image"
        fmt = "IMAGE"
        asset_url = (
            images[0].get("original_image_url")
            or images[0].get("resized_image_url")
        )
    else:
        media = "image"
        fmt = display_format.upper() or None
        asset_url = None

    platforms = ad.get("publisher_platform") or snap.get("publisher_platforms") or []
    if isinstance(platforms, str):
        platforms = [platforms]
    regions = ad.get("reached_countries") or []
    if isinstance(regions, str):
        regions = [regions]

    # Check if existed already (for insert vs update reporting)
    existed = conn.execute(
        "SELECT 1 FROM ads WHERE ad_archive_id = %s", (ad_archive_id,)
    ).fetchone()

    conn.execute(
        """
        INSERT INTO ads (
            ad_archive_id, industry_slug, page_id, format, platforms,
            headline, body_text, cta_text, asset_url, asset_type,
            status, start_date, first_seen_date, last_seen_active_date,
            stopped_date, days_running, regions, raw
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s::jsonb)
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
            stopped_date = COALESCE(ads.stopped_date, EXCLUDED.stopped_date),
            days_running = EXCLUDED.days_running,
            regions = EXCLUDED.regions,
            raw = EXCLUDED.raw
        """,
        (
            ad_archive_id,
            slug,
            page_id,
            fmt,
            platforms,
            headline,
            body_text,
            cta_text,
            asset_url,
            media,
            status,
            start_d,
            date.today(),
            last_seen_active,
            stopped,
            days_running,
            regions,
            json.dumps(ad, default=str),
        ),
    )
    return (not existed, ad_archive_id)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("page_id")
    ap.add_argument("industry_slug")
    ap.add_argument("--depth", choices=["active", "full"], default="active")
    ap.add_argument("--country", default="SG")
    ap.add_argument("--max-pages", type=int, default=8)
    args = ap.parse_args()

    if not DSN or not SC_KEY:
        print(json.dumps({"ok": False, "error": "missing GHOST_DATABASE_URL or SCRAPECREATORS_API_KEY in env"}))
        return 1

    sc = ScrapeCreatorsClient(api_key=SC_KEY)
    status_filter = "ALL" if args.depth == "full" else "ACTIVE"

    try:
        conn = psycopg.connect(DSN, autocommit=True, connect_timeout=30)
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"db connect failed: {e}"}))
        return 1

    ensure_industry(conn, args.industry_slug)

    # Log the scrape run
    run_id = conn.execute(
        "INSERT INTO scrape_runs (industry_slug, status) VALUES (%s, 'running') RETURNING id",
        (args.industry_slug,),
    ).fetchone()[0]

    all_ads: list[dict] = []
    page_name = None
    cursor = None
    try:
        for _ in range(args.max_pages):
            kwargs: dict[str, Any] = {
                "page_id": args.page_id,
                "country": args.country,
                "status": status_filter,
            }
            if cursor:
                kwargs["cursor"] = cursor
            resp = sc.facebook_company_ads(**kwargs)
            if not isinstance(resp, dict):
                break
            batch = resp.get("results") or []
            if not batch:
                break
            all_ads.extend(batch)
            # Grab page metadata from first ad's snapshot
            if page_name is None and batch:
                page_name = upsert_page(conn, args.industry_slug, args.page_id, batch[0].get("snapshot") or {})
            cursor = resp.get("cursor")
            if not cursor or args.depth == "active":
                break

        if not all_ads:
            print(json.dumps({
                "ok": False,
                "error": f"no ads returned for page_id {args.page_id} (country={args.country}, status={status_filter})",
                "page_id": args.page_id,
            }))
            conn.execute(
                "UPDATE scrape_runs SET finished_at=now(), status='error', error_text=%s WHERE id=%s",
                (f"no ads for page_id {args.page_id}", run_id),
            )
            return 1

        inserted = 0
        updated = 0
        ad_ids: list[str] = []
        for ad in all_ads:
            try:
                was_insert, aid = upsert_ad(conn, args.industry_slug, args.page_id, ad)
                if was_insert:
                    inserted += 1
                else:
                    updated += 1
                ad_ids.append(aid)

                # Save video assets locally — Meta CDN URLs expire in days,
                # so downstream transcription needs a persistent copy.
                snap = ad.get("snapshot") or {}
                videos = snap.get("videos") or []
                if videos:
                    video_url = (
                        videos[0].get("video_hd_url")
                        or videos[0].get("video_sd_url")
                    )
                    if video_url:
                        _save_video_asset(video_url, args.industry_slug, args.page_id, aid)

                # OCR image ads inline — non-fatal if it fails
                images = snap.get("images") or []
                if images and (was_insert or _should_ocr(conn, aid)):
                    asset_url = (
                        images[0].get("original_image_url")
                        or images[0].get("resized_image_url")
                    )
                    ocr_text = _ocr_image(asset_url)
                    if ocr_text is not None:
                        conn.execute(
                            """UPDATE ads SET ocr_text = %s,
                               ocr_extracted_at = now(), ocr_model = %s
                               WHERE ad_archive_id = %s""",
                            (ocr_text, _OCR_MODEL, aid),
                        )
            except Exception as e:
                print(f"WARN: ad upsert failed: {e}", file=sys.stderr)

        conn.execute(
            "UPDATE scrape_runs SET finished_at=now(), status='success', pages_scraped=1, ads_found=%s, ads_new=%s WHERE id=%s",
            (len(all_ads), inserted, run_id),
        )

        # Fire off transcript backfill as a detached background task so this
        # call returns quickly. Groq whisper-large-v3, language='en', processes
        # whichever video ads from this scrape don't yet have a transcript row.
        transcripts_queued = 0
        if inserted or updated:
            try:
                import subprocess
                script = pathlib.Path(__file__).parent / "backfill-transcripts.py"
                if script.exists():
                    log_dir = pathlib.Path("/tmp/swipe-backfill-logs")
                    log_dir.mkdir(exist_ok=True)
                    log_file = log_dir / f"transcribe-{args.industry_slug}-{int(datetime.now().timestamp())}.log"
                    subprocess.Popen(
                        ["python3", str(script), "--industry", args.industry_slug],
                        stdout=open(log_file, "w"),
                        stderr=subprocess.STDOUT,
                        start_new_session=True,  # detach so parent can exit
                        cwd=str(pathlib.Path(__file__).parent.parent),
                    )
                    transcripts_queued = 1
            except Exception as e:
                print(f"WARN: could not spawn transcript backfill: {e}", file=sys.stderr)

        print(json.dumps({
            "ok": True,
            "page_id": args.page_id,
            "page_name": page_name,
            "industry": args.industry_slug,
            "depth": args.depth,
            "ads_total": len(all_ads),
            "ads_inserted": inserted,
            "ads_updated": updated,
            "ad_ids": ad_ids[:20],  # cap so JSON stays small
            "transcripts_queued": transcripts_queued,
        }))
        return 0
    except Exception as e:
        conn.execute(
            "UPDATE scrape_runs SET finished_at=now(), status='error', error_text=%s WHERE id=%s",
            (str(e), run_id),
        )
        print(json.dumps({"ok": False, "error": str(e), "page_id": args.page_id}))
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
