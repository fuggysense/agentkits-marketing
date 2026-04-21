#!/usr/bin/env python3
"""scripts/backfill-transcripts.py — transcribe every video ad that has no transcript.

Downloads (or reuses on-disk) the video, transcribes with Groq whisper-large-v3
(language locked to English — Singapore-English defeats auto-detect), writes to
Ghost `transcripts` table + a .txt sidecar next to the video.

Usage:
  python3 scripts/backfill-transcripts.py                        # all missing
  python3 scripts/backfill-transcripts.py --industry property-sg # one industry
  python3 scripts/backfill-transcripts.py --limit 5              # dry-run-ish
  python3 scripts/backfill-transcripts.py --force                # re-do existing

Env: GHOST_DATABASE_URL, GROQ_API_KEY (.env).
"""

import argparse
import os
import pathlib
import subprocess
import sys
import tempfile
from datetime import timedelta
from urllib.request import urlretrieve

import psycopg

try:
    from dotenv import load_dotenv
    load_dotenv(pathlib.Path(__file__).parent.parent / ".env")
except ImportError:
    pass

DSN = os.environ["GHOST_DATABASE_URL"]
GROQ_KEY = os.environ.get("GROQ_API_KEY")
SWIPE_DIR = pathlib.Path(__file__).parent.parent / "swipe-files"


def transcribe_groq(audio_path: pathlib.Path, language: str = "en") -> tuple[str, float | None, list]:
    """Returns (text, duration_sec, segments). Segments are timestamped chunks
    from verbose_json: [{id, start, end, text, ...}, ...]. Raises on failure."""
    import requests

    with open(audio_path, "rb") as f:
        resp = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {GROQ_KEY}"},
            data={
                "model": "whisper-large-v3",
                "language": language,
                "response_format": "verbose_json",
                "temperature": "0",
            },
            files={"file": (audio_path.name, f, "audio/mpeg")},
            timeout=120,
        )
    if resp.status_code != 200:
        raise RuntimeError(f"groq {resp.status_code}: {resp.text[:400]}")
    j = resp.json()
    return j.get("text", ""), j.get("duration"), j.get("segments", [])


def transcribe_faster_whisper(audio_path: pathlib.Path, language: str = "en") -> tuple[str, float | None, list]:
    """Fallback: local faster-whisper. Returns (text, duration, segments)."""
    from faster_whisper import WhisperModel

    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments_iter, info = model.transcribe(str(audio_path), language=language, beam_size=5)
    segments = []
    text_parts = []
    for s in segments_iter:
        segments.append({"id": s.id, "start": s.start, "end": s.end, "text": s.text})
        text_parts.append(s.text.strip())
    return " ".join(text_parts), info.duration, segments


def has_audio_stream(video_path: pathlib.Path) -> bool:
    """True if video contains at least one audio stream (else silent)."""
    for cand in ("/opt/homebrew/bin/ffprobe", "/usr/local/bin/ffprobe", "ffprobe"):
        try:
            r = subprocess.run(
                [cand, "-v", "error", "-select_streams", "a",
                 "-show_entries", "stream=codec_name", str(video_path)],
                capture_output=True, text=True, timeout=10,
            )
            if r.returncode == 0:
                return "codec_name" in r.stdout
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return True  # assume audio present if ffprobe unavailable; let ffmpeg error if wrong


def extract_audio(video_path: pathlib.Path, out_dir: pathlib.Path) -> pathlib.Path:
    """Use ffmpeg to rip audio only. 16kHz mono MP3 keeps request small."""
    ff = None
    for cand in ("/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg", "ffmpeg"):
        try:
            r = subprocess.run([cand, "-version"], capture_output=True, timeout=5)
            if r.returncode == 0:
                ff = cand
                break
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    if not ff:
        raise RuntimeError("ffmpeg not found")
    audio = out_dir / f"{video_path.stem}.mp3"
    subprocess.run(
        [ff, "-y", "-i", str(video_path), "-vn", "-ac", "1", "-ar", "16000",
         "-b:a", "32k", str(audio)],
        check=True,
        capture_output=True,
    )
    return audio


_SWIPE_ROOT = pathlib.Path(__file__).parent.parent / "swipe-files"


def _local_video_path(industry: str, page_id: str, ad_archive_id: str) -> pathlib.Path:
    """Deterministic local path saved by ingest-advertiser.py at scrape time."""
    return _SWIPE_ROOT / industry / "pages" / page_id / "ads" / "assets" / f"{ad_archive_id}.mp4"


def resolve_video_path(asset_url: str, industry: str = "", page_id: str = "",
                       ad_archive_id: str = "") -> pathlib.Path | None:
    """Resolve to a local file. Prefers the deterministic local copy
    (which doesn't expire) over the Meta CDN URL (which does).

    Order:
      1. swipe-files/<industry>/pages/<page_id>/ads/assets/<ad>.mp4 if present
      2. file:// URL
      3. absolute local path
      4. None (caller must download from http url)
    """
    if industry and page_id and ad_archive_id:
        local = _local_video_path(industry, page_id, ad_archive_id)
        if local.exists() and local.stat().st_size > 0:
            return local
    if not asset_url:
        return None
    if asset_url.startswith("file://"):
        p = pathlib.Path(asset_url.replace("file://", ""))
        return p if p.exists() else None
    if asset_url.startswith("/") and pathlib.Path(asset_url).exists():
        return pathlib.Path(asset_url)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--industry", help="Restrict to one industry slug")
    ap.add_argument("--limit", type=int, default=0, help="Stop after N ads (0 = all)")
    ap.add_argument("--force", action="store_true", help="Re-transcribe even if row exists")
    ap.add_argument("--engine", choices=["groq", "faster-whisper", "auto"], default="auto")
    args = ap.parse_args()

    if args.engine in ("groq", "auto") and not GROQ_KEY:
        print("WARN: GROQ_API_KEY missing — falling back to faster-whisper", file=sys.stderr)
        args.engine = "faster-whisper"

    conn = psycopg.connect(DSN, autocommit=True, connect_timeout=30)

    filter_clause = "WHERE a.format = 'VIDEO' AND a.asset_url IS NOT NULL"
    params: list = []
    if args.industry:
        filter_clause += " AND a.industry_slug = %s"
        params.append(args.industry)
    if not args.force:
        filter_clause += " AND a.ad_archive_id NOT IN (SELECT ad_archive_id FROM transcripts)"

    rows = conn.execute(
        f"""SELECT a.ad_archive_id, a.asset_url, a.page_id, a.industry_slug
            FROM ads a {filter_clause}
            ORDER BY a.days_running DESC NULLS LAST""",
        params,
    ).fetchall()

    if args.limit:
        rows = rows[: args.limit]

    print(f"Backfilling {len(rows)} video transcripts "
          f"(industry={args.industry or 'all'}, engine={args.engine})")

    ok = 0
    fail = 0
    skipped = 0
    for i, (ad_id, asset_url, page_id, slug) in enumerate(rows, 1):
        print(f"\n[{i}/{len(rows)}] {ad_id}  {asset_url[:80] if asset_url else '(none)'}")
        try:
            with tempfile.TemporaryDirectory() as td:
                tmp = pathlib.Path(td)
                vpath = resolve_video_path(asset_url, slug, page_id, ad_id)
                if vpath is None:
                    # Download from http(s)
                    if not asset_url or not asset_url.startswith("http"):
                        print("  ✗ no resolvable URL; skipping")
                        skipped += 1
                        continue
                    vpath = tmp / f"{ad_id}.mp4"
                    urlretrieve(asset_url, vpath)

                # Silent-video guard — many property ads are text-overlay only
                # with no audio track. Mark them with status='no_audio' so they
                # don't retry on every backfill, and continue.
                if not has_audio_stream(vpath):
                    conn.execute(
                        """INSERT INTO transcripts (ad_archive_id, text, language, duration_sec, status)
                           VALUES (%s, '', NULL, 0, 'no_audio')
                           ON CONFLICT (ad_archive_id) DO UPDATE SET
                               status = 'no_audio', text = '', created_at = now()""",
                        (ad_id,),
                    )
                    print("  ⊘ silent video (no audio stream) — marked no_audio")
                    skipped += 1
                    continue

                # Extract audio
                audio = extract_audio(vpath, tmp)
                # Transcribe
                engine = args.engine
                if engine == "auto":
                    engine = "groq"
                try:
                    if engine == "groq":
                        text, dur, segments = transcribe_groq(audio, language="en")
                    else:
                        text, dur, segments = transcribe_faster_whisper(audio, language="en")
                except Exception as e:
                    if args.engine == "auto" and "groq" in str(e).lower():
                        print(f"  ! groq failed ({str(e)[:80]}); retry local")
                        text, dur, segments = transcribe_faster_whisper(audio, language="en")
                        engine = "faster-whisper"
                    else:
                        raise
                if not text.strip():
                    print("  ✗ empty transcript")
                    fail += 1
                    continue
                # Write to DB
                import json as _json
                conn.execute(
                    """INSERT INTO transcripts (ad_archive_id, text, language, duration_sec, segments, status)
                       VALUES (%s, %s, 'en', %s, %s::jsonb, 'ok')
                       ON CONFLICT (ad_archive_id) DO UPDATE SET
                           text = EXCLUDED.text, language = 'en',
                           duration_sec = EXCLUDED.duration_sec,
                           segments = EXCLUDED.segments,
                           status = 'ok',
                           created_at = now()""",
                    (ad_id, text, dur, _json.dumps(segments) if segments else None),
                )
                # Sidecar .txt for disk backup
                if slug and page_id:
                    sidecar_dir = SWIPE_DIR / slug / "pages" / page_id / "ads"
                    sidecar_dir.mkdir(parents=True, exist_ok=True)
                    sidecar = sidecar_dir / f"{ad_id}-transcript.txt"
                    sidecar.write_text(text)
                dur_str = str(timedelta(seconds=int(dur))) if dur else "?"
                print(f"  ✓ {engine} · {len(text)} chars · {dur_str}")
                ok += 1
        except Exception as e:
            print(f"  ✗ {type(e).__name__}: {str(e)[:200]}")
            fail += 1

    print(f"\nDone. ok={ok}  fail={fail}  skipped={skipped}  total={len(rows)}")
    conn.close()
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
