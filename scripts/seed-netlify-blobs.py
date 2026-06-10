#!/usr/bin/env python3
"""scripts/seed-netlify-blobs.py — upload scraped creative assets to Netlify Blobs.

Runs once per industry (or after scraping new advertisers) to move video/image
assets off local disk and onto Netlify's object store so the dashboard can
serve them via signed URLs.

Two modes:
  - LIVE: NETLIFY_BLOBS_TOKEN + NETLIFY_SITE_ID set in .env → uploads, updates
    ads.asset_url to blobs://<store>/<key> reference, the dashboard resolves
    at request time via Netlify's @netlify/blobs SDK.
  - DRY-RUN: missing env → prints a manifest of what would be uploaded and
    exits 0. Useful before Netlify setup is ready.

Usage:
  python3 scripts/seed-netlify-blobs.py property-sg
  python3 scripts/seed-netlify-blobs.py property-sg --dry-run   # force

Reference: https://docs.netlify.com/blobs/overview/
"""

import os
import sys
import json
import shutil
import pathlib
import argparse
import mimetypes
import subprocess
from urllib.request import Request, urlopen
from urllib.error import HTTPError

import psycopg

try:
    from dotenv import load_dotenv
    load_dotenv(pathlib.Path(__file__).parent.parent / ".env")
except ImportError:
    pass

DSN = os.environ["GHOST_DATABASE_URL"]
TOKEN = os.environ.get("NETLIFY_BLOBS_TOKEN")
SITE_ID = os.environ.get("NETLIFY_SITE_ID")
STORE_NAME = os.environ.get("NETLIFY_BLOBS_STORE", "swipe-ads")

SWIPE_DIR = pathlib.Path(__file__).parent.parent / "swipe-files"

# Compression defaults (overridable via CLI or env). These produced ~46%
# size reduction on vertical 720x1280 ads in smoke tests (13M → 7M), with
# quality still usable for dashboard previews.
FFMPEG_CRF = int(os.environ.get("VIDEO_CRF", 28))
FFMPEG_SHORT_SIDE = int(os.environ.get("VIDEO_SHORT_SIDE", 540))
FFMPEG_AUDIO_KBPS = int(os.environ.get("VIDEO_AUDIO_KBPS", 64))


def find_ffmpeg():
    """Prefer homebrew ffmpeg — user's /Users/jerel/.darkbloom/bin/ffmpeg is
    broken (missing dylib) so `which ffmpeg` can resolve to a non-working
    binary."""
    for candidate in ("/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"):
        if pathlib.Path(candidate).exists():
            return candidate
    return shutil.which("ffmpeg")


def compress_video(src, dst, ffmpeg_bin):
    """Transcode to h264/aac, scale short-side to target, CRF-tuned."""
    short = FFMPEG_SHORT_SIDE
    vf = f"scale='if(gt(iw,ih),-2,{short})':'if(gt(iw,ih),{short},-2)'"
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg_bin, "-y", "-i", str(src),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", str(FFMPEG_CRF),
        "-c:a", "aac", "-b:a", f"{FFMPEG_AUDIO_KBPS}k",
        "-movflags", "+faststart",
        str(dst),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not dst.exists():
        raise RuntimeError(f"ffmpeg failed: {r.stderr[-500:]}")
    return dst


def collect_assets(conn, slug):
    """Return [(ad_archive_id, local_path, asset_type, content_type)]."""
    rows = conn.execute(
        """
        SELECT ad_archive_id, asset_url, asset_type
        FROM ads
        WHERE industry_slug = %s
          AND asset_url IS NOT NULL
          AND (asset_url LIKE 'file://%%' OR asset_url NOT LIKE '%%://%%')
        """,
        (slug,),
    ).fetchall()
    out = []
    for ad_id, url, a_type in rows:
        path = url.replace("file://", "") if url.startswith("file://") else url
        p = pathlib.Path(path)
        if not p.exists():
            continue
        ct, _ = mimetypes.guess_type(str(p))
        out.append((ad_id, p, a_type, ct or "application/octet-stream"))
    return out


def upload_to_netlify(ad_id, local_path, content_type):
    """PUT to Netlify Blobs REST API. Returns the blob key."""
    key = f"{ad_id}{local_path.suffix}"
    url = f"https://api.netlify.com/api/v1/blobs/{SITE_ID}/{STORE_NAME}/{key}"
    data = local_path.read_bytes()
    req = Request(
        url,
        data=data,
        method="PUT",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": content_type,
        },
    )
    try:
        with urlopen(req, timeout=60) as resp:
            if resp.status in (200, 201):
                return f"blobs://{STORE_NAME}/{key}"
            raise RuntimeError(f"unexpected status {resp.status}")
    except HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"Netlify {e.code}: {body}") from None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("industry", help="industry slug, e.g. property-sg")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print manifest without uploading")
    ap.add_argument("--compress", action="store_true",
                    help="ffmpeg-compress videos before upload (cached in "
                         "swipe-files/<industry>/compressed/)")
    ap.add_argument("--no-compress", action="store_true",
                    help="Force raw upload even if --compress would have run")
    args = ap.parse_args()

    conn = psycopg.connect(DSN, connect_timeout=30, autocommit=True)
    assets = collect_assets(conn, args.industry)

    if not assets:
        print(f"No local assets to upload for {args.industry}")
        return

    dry = args.dry_run or not (TOKEN and SITE_ID)
    compress = args.compress and not args.no_compress
    ffmpeg_bin = find_ffmpeg() if compress else None
    if compress and not ffmpeg_bin:
        print("WARN: --compress requested but no working ffmpeg found; "
              "falling back to raw upload", file=sys.stderr)
        compress = False

    compressed_dir = SWIPE_DIR / args.industry / "compressed"
    if dry and not args.dry_run:
        print("NETLIFY_BLOBS_TOKEN or NETLIFY_SITE_ID not set — running in dry-run")
        print("Set both in .env then re-run without --dry-run to upload")
        print()

    total_bytes = sum(p.stat().st_size for _, p, *_ in assets)
    print(f"Industry:     {args.industry}")
    print(f"Assets:       {len(assets)} files, {total_bytes/1_000_000:.1f} MB raw")
    print(f"Store:        {STORE_NAME}")
    print(f"Mode:         {'DRY-RUN' if dry else 'LIVE'}")
    print(f"Compression:  {'ON (CRF %d, short %dpx)' % (FFMPEG_CRF, FFMPEG_SHORT_SIDE) if compress else 'OFF'}")
    print()

    uploaded = 0
    failed = 0
    compressed_total = 0
    for ad_id, path, a_type, ct in assets:
        upload_path = path
        if compress and a_type == "video":
            cached = compressed_dir / f"{ad_id}{path.suffix}"
            if cached.exists() and cached.stat().st_mtime >= path.stat().st_mtime:
                upload_path = cached
            else:
                try:
                    compress_video(path, cached, ffmpeg_bin)
                    upload_path = cached
                except Exception as e:
                    print(f"  [WARN] compression failed for {ad_id}: {e}",
                          file=sys.stderr)
                    # fall back to raw

        src_kb = path.stat().st_size / 1024
        out_kb = upload_path.stat().st_size / 1024
        ratio = f"{src_kb:6.0f}KB"
        if upload_path != path:
            ratio = f"{src_kb:6.0f}→{out_kb:<6.0f}KB"
            compressed_total += upload_path.stat().st_size

        if dry:
            print(f"  [dry] {ad_id}  {a_type:5}  {ratio}  {upload_path.name}")
            continue

        try:
            blob_ref = upload_to_netlify(ad_id, upload_path, ct)
            conn.execute(
                "UPDATE ads SET asset_url = %s WHERE ad_archive_id = %s",
                (blob_ref, ad_id),
            )
            uploaded += 1
            print(f"  [OK]  {ad_id}  {ratio}  -> {blob_ref}")
        except Exception as e:
            failed += 1
            print(f"  [ERR] {ad_id}  {e}", file=sys.stderr)

    print()
    if compress and compressed_total:
        saved_pct = (1 - compressed_total / total_bytes) * 100
        print(f"Compressed total: {compressed_total/1_000_000:.1f} MB "
              f"({saved_pct:.0f}% saved vs raw)")
    print(f"Done. uploaded={uploaded}  failed={failed}  total={len(assets)}")
    conn.close()


if __name__ == "__main__":
    main()
