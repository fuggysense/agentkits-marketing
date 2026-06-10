#!/usr/bin/env python3
"""scripts/backfill-ocr.py — OCR every image ad that has no ocr_text.

Uses Gemini 2.5 Flash Vision (3 rotating keys) to extract visible text verbatim.
Falls back across keys on quota/rate-limit errors.

Usage:
  python3 scripts/backfill-ocr.py                        # all missing
  python3 scripts/backfill-ocr.py --industry property-sg # one industry
  python3 scripts/backfill-ocr.py --limit 5              # stop after N
  python3 scripts/backfill-ocr.py --force                # re-OCR existing

Env: GHOST_DATABASE_URL, GEMINI_API_KEY / GEMINI_API_KEY_2 / GEMINI_API_KEY_3 (.env).
"""

import argparse
import base64
import json
import os
import pathlib
import sys
import time
import urllib.request
from urllib.error import URLError

import psycopg

try:
    from dotenv import load_dotenv
    load_dotenv(pathlib.Path(__file__).parent.parent / ".env")
except ImportError:
    pass

import google.generativeai as genai

DSN = os.environ["GHOST_DATABASE_URL"]

GEMINI_KEYS = [
    os.environ.get("GEMINI_API_KEY"),
    os.environ.get("GEMINI_API_KEY_2"),
    os.environ.get("GEMINI_API_KEY_3"),
]
GEMINI_KEYS = [k for k in GEMINI_KEYS if k]

OCR_MODEL = "gemini-2.5-flash"
OCR_PROMPT = (
    "Extract ALL visible text from this advertisement image. "
    "Output the text verbatim, preserve line breaks, no commentary, "
    "no introduction, no markdown. If there is no text, output exactly: [no text]"
)


def fetch_image_b64(url: str, timeout: int = 30) -> tuple[bytes, str]:
    """Download image, return (raw_bytes, mime_type)."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        ct = resp.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
    return data, ct


def ocr_with_gemini(image_bytes: bytes, mime: str, key_idx: int = 0) -> tuple[str, str, int]:
    """
    Run OCR using Gemini vision. Rotates keys on quota errors.
    Returns (text, model_used, key_idx_used).
    """
    last_err = None
    for attempt in range(len(GEMINI_KEYS)):
        ki = (key_idx + attempt) % len(GEMINI_KEYS)
        try:
            genai.configure(api_key=GEMINI_KEYS[ki])
            model = genai.GenerativeModel(OCR_MODEL)
            resp = model.generate_content(
                [
                    OCR_PROMPT,
                    {"mime_type": mime, "data": image_bytes},
                ],
                generation_config={"temperature": 0},
            )
            text = resp.text.strip()
            return text, OCR_MODEL, ki
        except Exception as e:
            err_str = str(e)
            last_err = err_str
            # Quota/rate-limit → try next key; other errors → raise immediately
            if any(x in err_str for x in ("429", "RESOURCE_EXHAUSTED", "quota", "rate")):
                print(f"  ! key[{ki}] quota ({err_str[:60]}); trying next key", file=sys.stderr)
                time.sleep(1)
                continue
            raise
    raise RuntimeError(f"all Gemini keys failed. last: {last_err}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--industry", help="Restrict to one industry slug")
    ap.add_argument("--limit", type=int, default=0, help="Stop after N ads (0 = all)")
    ap.add_argument("--force", action="store_true", help="Re-OCR even if ocr_text exists")
    args = ap.parse_args()

    if not GEMINI_KEYS:
        print("ERROR: no GEMINI_API_KEY found in env", file=sys.stderr)
        return 1

    conn = psycopg.connect(DSN, autocommit=True, connect_timeout=30)

    where = "WHERE a.format = 'IMAGE' AND a.asset_url IS NOT NULL"
    params: list = []
    if args.industry:
        where += " AND a.industry_slug = %s"
        params.append(args.industry)
    if not args.force:
        where += " AND a.ocr_text IS NULL"

    rows = conn.execute(
        f"""SELECT a.ad_archive_id, a.asset_url, a.industry_slug, a.page_id
            FROM ads a {where}
            ORDER BY a.days_running DESC NULLS LAST""",
        params,
    ).fetchall()

    if args.limit:
        rows = rows[: args.limit]

    print(
        f"Backfilling OCR for {len(rows)} image ads "
        f"(industry={args.industry or 'all'}, force={args.force})"
    )

    ok = 0
    fail = 0
    skipped = 0
    key_idx = 0  # start with first key; rotates on quota errors

    for i, (ad_id, asset_url, slug, page_id) in enumerate(rows, 1):
        print(f"\n[{i}/{len(rows)}] {ad_id}  {(asset_url or '')[:80]}")
        if not asset_url or not asset_url.startswith("http"):
            print("  ✗ no http URL; skipping")
            skipped += 1
            continue
        try:
            # Download image
            img_bytes, mime = fetch_image_b64(asset_url)
            if len(img_bytes) > 20_000_000:
                print(f"  ✗ image too large ({len(img_bytes)//1024}KB); skipping")
                skipped += 1
                continue

            # OCR via Gemini
            text, model_used, key_idx = ocr_with_gemini(img_bytes, mime, key_idx)

            if not text or text == "[no text]":
                # Still store the result so we don't re-attempt
                text = ""

            # Write to DB
            conn.execute(
                """UPDATE ads
                   SET ocr_text = %s,
                       ocr_extracted_at = now(),
                       ocr_model = %s
                   WHERE ad_archive_id = %s""",
                (text or None, model_used, ad_id),
            )
            char_count = len(text) if text else 0
            print(f"  ✓ {model_used} · {char_count} chars")
            ok += 1

        except URLError as e:
            print(f"  ✗ download failed: {e}")
            fail += 1
        except Exception as e:
            print(f"  ✗ {type(e).__name__}: {str(e)[:200]}")
            fail += 1

    print(f"\nDone. ok={ok}  fail={fail}  skipped={skipped}  total={len(rows)}")
    conn.close()
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
