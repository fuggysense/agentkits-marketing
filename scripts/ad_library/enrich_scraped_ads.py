#!/usr/bin/env python3
"""L2 + L3 enrichment for ads in an industry swipe pool.

L2 (per ad where run.days_running > 30):
  - video → download asset → faster-whisper → write <ad>-transcript.txt
  - image → download asset → pytesseract OCR → write <ad>-image-ocr.txt
L3 (per L2-enriched ad):
  - bundle (primary_text + headline + transcript_or_ocr)
  - call scripts/research-llm.sh kilo "<prompt>" --model "nvidia/nemotron-3-super-120b-a12b:free"
  - parse JSON response → fill enrichment.detected_* + schwartz_*

Skips ads already enriched (idempotent). Failures are logged, never raised.

Usage:
  python3 scripts/ad_library/enrich_scraped_ads.py --industry property-sg
  python3 scripts/ad_library/enrich_scraped_ads.py --industry property-sg --skip-classifier
  python3 scripts/ad_library/enrich_scraped_ads.py --industry property-sg --threshold-days 14
"""

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
SWIPE_ROOT = ROOT / "swipe-files"
RESEARCH_LLM = ROOT / "scripts" / "research-llm.sh"
KILO_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"
WHISPER_MODEL = "small"  # balance speed/quality on CPU
HTTP_TIMEOUT = 60
DOWNLOAD_CHUNK = 1 << 16

CLASSIFIER_PROMPT = """You are a paid-ads strategist. Classify ONE Meta ad against \
Eugene Schwartz's frameworks. Reply with STRICT JSON only — no prose, no markdown.

Schema:
{
  "detected_hooks": ["short hook line", ...],
  "detected_angle": "one short phrase",
  "detected_mass_desire": "wealth | safety | status | ease | sex | comfort | health | family | curiosity | other",
  "schwartz_awareness_estimate": "Unaware | Problem-Aware | Solution-Aware | Product-Aware | Most Aware",
  "schwartz_sophistication_stage": "1 | 2 | 3 | 4 | 5"
}

AD CONTEXT:
"""


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def append_log(industry_dir: Path, page_id: str, entry: dict) -> None:
    log_path = industry_dir / "pages" / page_id / "scrape-log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": now_iso(), "page_id": page_id, **entry},
                            ensure_ascii=False) + "\n")


def download(url: str, dest: Path) -> bool:
    try:
        with requests.get(url, stream=True, timeout=HTTP_TIMEOUT) as r:
            r.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            with dest.open("wb") as f:
                for chunk in r.iter_content(DOWNLOAD_CHUNK):
                    if chunk:
                        f.write(chunk)
        return True
    except Exception:  # noqa: BLE001
        return False


def transcribe_video(path: Path) -> str | None:
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("WARN: faster-whisper not installed; skipping video transcription",
              file=sys.stderr)
        return None
    try:
        model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
        segments, _ = model.transcribe(str(path), beam_size=5)
        return " ".join(s.text.strip() for s in segments).strip() or None
    except Exception as e:  # noqa: BLE001
        print(f"WARN: whisper failed on {path.name}: {e}", file=sys.stderr)
        return None


def ocr_image(path: Path) -> str | None:
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        print("WARN: pytesseract/Pillow not installed; skipping image OCR",
              file=sys.stderr)
        return None
    try:
        return pytesseract.image_to_string(Image.open(path)).strip() or None
    except Exception as e:  # noqa: BLE001
        print(f"WARN: OCR failed on {path.name}: {e}", file=sys.stderr)
        return None


def call_classifier(prompt: str) -> dict | None:
    if not RESEARCH_LLM.exists():
        print(f"WARN: {RESEARCH_LLM} missing; skip classifier", file=sys.stderr)
        return None
    try:
        out = subprocess.run(
            ["bash", str(RESEARCH_LLM), "kilo", prompt, "--model", KILO_MODEL],
            capture_output=True, text=True, timeout=120,
            env={**os.environ},
        )
        if out.returncode != 0:
            print(f"WARN: kilo exit={out.returncode} stderr={out.stderr[:200]}",
                  file=sys.stderr)
            return None
        text = out.stdout.strip()
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            return None
        envelope = json.loads(text[start:end + 1])
        # research-llm.sh returns {"provider","model","success","result":"<escaped json>","tokens_used"}
        if isinstance(envelope, dict) and "result" in envelope:
            inner = envelope["result"]
            if isinstance(inner, str):
                s = inner.find("{")
                e = inner.rfind("}")
                if s == -1 or e == -1:
                    return None
                return json.loads(inner[s:e + 1])
            return inner
        return envelope
    except Exception as e:  # noqa: BLE001
        print(f"WARN: classifier exception: {e}", file=sys.stderr)
        return None


def enrich_ad(ad_path: Path, industry_dir: Path, threshold_days: int,
              run_classifier: bool) -> dict:
    summary = {"l2_done": False, "l3_done": False, "skipped": False, "errors": []}
    ad = json.loads(ad_path.read_text(encoding="utf-8"))
    days = ad.get("run", {}).get("days_running", 0)
    if days <= threshold_days:
        summary["skipped"] = True
        return summary

    page_id = ad["page_id"]
    ad_id = ad["ad_archive_id"]
    media_type = ad.get("creative", {}).get("media_type")
    asset_url = ad.get("creative", {}).get("asset_remote_url")
    enr = ad.setdefault("enrichment", {})

    # L2 — transcribe / OCR
    text_for_classifier = None
    if media_type == "video" and asset_url and not enr.get("video_transcript_path"):
        ext = ".mp4"
        asset_path = ad_path.parent / "assets" / f"{ad_id}{ext}"
        transcript_path = ad_path.parent / f"{ad_id}-transcript.txt"
        if download(asset_url, asset_path):
            text = transcribe_video(asset_path)
            if text:
                transcript_path.write_text(text, encoding="utf-8")
                enr["video_transcript_path"] = str(transcript_path.relative_to(industry_dir))
                ad["creative"]["asset_local_path"] = str(asset_path.relative_to(industry_dir))
                text_for_classifier = text
                summary["l2_done"] = True
            else:
                summary["errors"].append("transcribe_failed")
        else:
            summary["errors"].append("download_failed")
    elif media_type == "image" and asset_url and not enr.get("image_ocr_path"):
        ext = ".jpg"
        asset_path = ad_path.parent / "assets" / f"{ad_id}{ext}"
        ocr_path = ad_path.parent / f"{ad_id}-image-ocr.txt"
        if download(asset_url, asset_path):
            text = ocr_image(asset_path)
            if text:
                ocr_path.write_text(text, encoding="utf-8")
                enr["image_ocr_path"] = str(ocr_path.relative_to(industry_dir))
                ad["creative"]["asset_local_path"] = str(asset_path.relative_to(industry_dir))
                text_for_classifier = text
                summary["l2_done"] = True
            else:
                summary["errors"].append("ocr_failed")
        else:
            summary["errors"].append("download_failed")
    else:
        # already enriched OR unsupported — pull existing text for classifier
        for key in ("video_transcript_path", "image_ocr_path"):
            p = enr.get(key)
            if p:
                full = industry_dir / p
                if full.exists():
                    text_for_classifier = full.read_text(encoding="utf-8")
                break

    # L3 — classifier (only if we have something to classify and not already done)
    if run_classifier and text_for_classifier and not enr.get("classified_at"):
        copy_blob = "\n".join(filter(None, [
            ad.get("copy", {}).get("primary_text"),
            ad.get("copy", {}).get("headline"),
            text_for_classifier,
        ]))[:8000]
        result = call_classifier(CLASSIFIER_PROMPT + copy_blob)
        if result:
            for k in ("detected_hooks", "detected_angle", "detected_mass_desire",
                      "schwartz_awareness_estimate", "schwartz_sophistication_stage"):
                if k in result:
                    enr[k] = result[k]
            enr["classifier_model"] = KILO_MODEL
            enr["classified_at"] = now_iso()
            summary["l3_done"] = True
        else:
            summary["errors"].append("classifier_failed")

    if summary["l2_done"] or summary["l3_done"]:
        ad_path.write_text(json.dumps(ad, indent=2, ensure_ascii=False), encoding="utf-8")
        append_log(industry_dir, page_id, {
            "event": "enrich_complete", "ad_id": ad_id,
            "l2": summary["l2_done"], "l3": summary["l3_done"],
            "errors": summary["errors"],
        })
    elif summary["errors"]:
        append_log(industry_dir, page_id, {
            "event": "enrich_failed", "ad_id": ad_id, "errors": summary["errors"],
        })
    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--industry", required=True)
    ap.add_argument("--threshold-days", type=int, default=30,
                    help="Only enrich ads with run.days_running > N (default 30 per Q3)")
    ap.add_argument("--skip-classifier", action="store_true",
                    help="L2 only; skip L3 Kilo→Nemotron pass")
    args = ap.parse_args()

    industry_dir = SWIPE_ROOT / args.industry
    if not industry_dir.exists():
        print(f"ERR: {industry_dir} not found", file=sys.stderr)
        return 1

    ad_files = sorted(industry_dir.glob("pages/*/ads/*.json"))
    print(f"[enrich] industry={args.industry} candidates={len(ad_files)} "
          f"threshold_days={args.threshold_days} classifier={not args.skip_classifier}")

    totals = {"l2": 0, "l3": 0, "skipped": 0, "errors": 0}
    for path in ad_files:
        s = enrich_ad(path, industry_dir, args.threshold_days,
                      run_classifier=not args.skip_classifier)
        totals["l2"] += int(s["l2_done"])
        totals["l3"] += int(s["l3_done"])
        totals["skipped"] += int(s["skipped"])
        totals["errors"] += len(s["errors"])
    print(f"[enrich] totals {totals}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
