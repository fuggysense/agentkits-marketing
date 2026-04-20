#!/usr/bin/env python3
"""DB-native classifier for unclassified Ghost Postgres ads.

Parallel, multi-model. Reads unclassified ads from Postgres, runs them through
Nemotron (via Kilo gateway) and/or Gemini CLI in a worker pool, writes results
back to `classifications`.

Usage:
  python3 scripts/ad_library/classify-unclassified.py --industry property-sg
  python3 scripts/ad_library/classify-unclassified.py --industry property-sg --workers 10 --models kilo,gemini
  python3 scripts/ad_library/classify-unclassified.py --industry property-sg --limit 5 --dry-run
"""

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parents[2]
RESEARCH_LLM = ROOT / "scripts" / "research-llm.sh"
KILO_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"
GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_DB = os.environ.get("GHOST_DATABASE_URL") or (
    "postgresql://tsdbadmin:wgax2jxyn8lok6m5@bl3xi4d6dy.dela09izuq.tsdb.cloud.timescale.com:31082/tsdb?sslmode=require"
)

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

_print_lock = threading.Lock()


def log(msg: str):
    with _print_lock:
        print(msg, flush=True)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def parse_first_json(text: str) -> dict | None:
    """Find the first balanced {...} block in text and json.loads it."""
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for i, ch in enumerate(text[start:], start=start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start:i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def call_kilo(prompt: str) -> dict | None:
    if not RESEARCH_LLM.exists():
        return None
    try:
        out = subprocess.run(
            ["bash", str(RESEARCH_LLM), "kilo", prompt, "--model", KILO_MODEL],
            capture_output=True, text=True, timeout=180,
            env={**os.environ},
        )
        if out.returncode != 0:
            return None
        envelope = parse_first_json(out.stdout)
        if not envelope:
            return None
        if isinstance(envelope, dict) and "result" in envelope:
            inner = envelope["result"]
            return parse_first_json(inner) if isinstance(inner, str) else inner
        return envelope
    except Exception:
        return None


def call_gemini(prompt: str) -> dict | None:
    """Use gemini CLI headlessly. Returns the classifier JSON or None."""
    full_prompt = (
        "You are a classifier. Reply with STRICT JSON only, no prose, no markdown fences.\n\n"
        + prompt
    )
    try:
        out = subprocess.run(
            ["gemini", "-p", full_prompt, "--output-format", "json",
             "-m", GEMINI_MODEL],
            capture_output=True, text=True, timeout=180,
            env={**os.environ},
        )
        if out.returncode != 0:
            return None
        envelope = parse_first_json(out.stdout)
        if not envelope or "response" not in envelope:
            return None
        inner = envelope["response"]
        if isinstance(inner, str):
            # strip possible ```json ... ``` fences
            s = inner.strip()
            if s.startswith("```"):
                s = s.split("\n", 1)[-1]
                if s.endswith("```"):
                    s = s.rsplit("```", 1)[0]
            return parse_first_json(s) or parse_first_json(inner)
        return inner
    except Exception:
        return None


MODEL_REGISTRY = {
    "kilo":   {"callable": call_kilo,   "db_name": KILO_MODEL},
    "gemini": {"callable": call_gemini, "db_name": GEMINI_MODEL},
}


def parse_stage(val) -> int | None:
    if val is None:
        return None
    if isinstance(val, int):
        return val if 1 <= val <= 5 else None
    try:
        n = int(str(val).strip().split()[0])
        return n if 1 <= n <= 5 else None
    except (ValueError, IndexError):
        return None


def fetch_unclassified(cur, industry: str, limit: int | None) -> list[dict]:
    sql = """
        SELECT a.ad_archive_id,
               COALESCE(p.name, '') AS page_name,
               COALESCE(a.headline, '') AS headline,
               COALESCE(a.body_text, '') AS body_text,
               COALESCE(t.text, '') AS transcript,
               COALESCE(a.ocr_text, '') AS ocr_text,
               a.days_running
        FROM ads a
        JOIN pages p ON p.page_id = a.page_id
        LEFT JOIN classifications c ON c.ad_archive_id = a.ad_archive_id
        LEFT JOIN transcripts t ON t.ad_archive_id = a.ad_archive_id
        WHERE p.industry_slug = %s
          AND c.ad_archive_id IS NULL
          AND (
            LENGTH(COALESCE(a.body_text, '')) > 30
            OR t.text IS NOT NULL
            OR a.ocr_text IS NOT NULL
          )
        ORDER BY a.days_running DESC NULLS LAST
    """
    if limit:
        sql += f" LIMIT {int(limit)}"
    cur.execute(sql, (industry,))
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def build_copy_blob(ad: dict) -> str:
    parts = [
        f"Advertiser: {ad['page_name']}" if ad['page_name'] else None,
        ad['headline'] or None,
        ad['body_text'] or None,
        ad['transcript'] or None,
        ad['ocr_text'] or None,
    ]
    return "\n---\n".join(p for p in parts if p)[:8000]


def classify_one(ad: dict, model_key: str) -> dict | None:
    """Classify one ad with the given model. Returns dict ready for DB insert or None."""
    blob = build_copy_blob(ad)
    if len(blob) < 40:
        return {"ad_archive_id": ad["ad_archive_id"], "skipped": "too_little_text"}
    result = MODEL_REGISTRY[model_key]["callable"](CLASSIFIER_PROMPT + blob)
    if not result:
        return None
    stage = parse_stage(result.get("schwartz_sophistication_stage"))
    angle = result.get("detected_angle")
    raw_for_db = {
        "detected_hooks": json.dumps(result.get("detected_hooks"))
                          if result.get("detected_hooks") is not None else None,
        "detected_angle": angle,
        "detected_mass_desire": result.get("detected_mass_desire"),
        "schwartz_awareness": result.get("schwartz_awareness_estimate"),
        "schwartz_sophistication": result.get("schwartz_sophistication_stage"),
    }
    return {
        "ad_archive_id": ad["ad_archive_id"],
        "page_name": ad["page_name"],
        "schwartz_stage": stage,
        "angle": angle,
        "mass_desire": result.get("detected_mass_desire"),
        "model": MODEL_REGISTRY[model_key]["db_name"],
        "raw": raw_for_db,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--industry", required=True, help="industry_slug (e.g. property-sg)")
    ap.add_argument("--limit", type=int, default=None, help="max ads to classify this run")
    ap.add_argument("--dry-run", action="store_true", help="run classifier but don't write")
    ap.add_argument("--models", default="kilo,gemini",
                    help="comma-separated model keys; round-robin assignment. Options: kilo, gemini")
    ap.add_argument("--workers", type=int, default=10, help="max parallel classifier requests")
    ap.add_argument("--db", default=DEFAULT_DB)
    args = ap.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    for m in models:
        if m not in MODEL_REGISTRY:
            print(f"ERROR: unknown model '{m}'. Options: {list(MODEL_REGISTRY)}", file=sys.stderr)
            return 2

    log(f"[{now_iso()}] classify-unclassified industry={args.industry} "
        f"limit={args.limit} dry_run={args.dry_run} models={models} workers={args.workers}")

    with psycopg.connect(args.db) as conn:
        with conn.cursor() as cur:
            ads = fetch_unclassified(cur, args.industry, args.limit)

        log(f"  {len(ads)} unclassified ads with text signal")
        if not ads:
            return 0

        # Round-robin model assignment
        work = [(ad, models[i % len(models)]) for i, ad in enumerate(ads)]

        stats = {"ok": 0, "fail": 0, "skipped": 0, "by_model": {m: 0 for m in models}}

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(classify_one, ad, m): (ad, m) for ad, m in work}
            for i, fut in enumerate(as_completed(futures), 1):
                ad, m = futures[fut]
                ad_id = ad["ad_archive_id"]
                try:
                    result = fut.result()
                except Exception as e:
                    log(f"  [{i}/{len(ads)}] {ad_id} [{m}] EXC {e}")
                    stats["fail"] += 1
                    continue
                if result is None:
                    log(f"  [{i}/{len(ads)}] {ad_id} [{m}] FAIL")
                    stats["fail"] += 1
                    continue
                if "skipped" in result:
                    log(f"  [{i}/{len(ads)}] {ad_id} [{m}] skip ({result['skipped']})")
                    stats["skipped"] += 1
                    continue

                log(f"  [{i}/{len(ads)}] {ad_id} [{m}] angle='{result['angle']}' "
                    f"stage={result['schwartz_stage']} desire={result['mass_desire']} "
                    f"| {result['page_name'][:30]}")

                if args.dry_run:
                    stats["ok"] += 1
                    stats["by_model"][m] += 1
                    continue

                with conn.cursor() as wcur:
                    wcur.execute("""
                        INSERT INTO classifications
                          (ad_archive_id, schwartz_stage, angle, avatar_fit, blue_box_category,
                           model, confidence, raw_response)
                        VALUES (%s, %s, %s, NULL, NULL, %s, NULL, %s)
                        ON CONFLICT (ad_archive_id) DO UPDATE SET
                          schwartz_stage = EXCLUDED.schwartz_stage,
                          angle = EXCLUDED.angle,
                          model = EXCLUDED.model,
                          raw_response = EXCLUDED.raw_response
                    """, (result["ad_archive_id"], result["schwartz_stage"],
                          result["angle"], result["model"], json.dumps(result["raw"])))
                    conn.commit()
                stats["ok"] += 1
                stats["by_model"][m] += 1

        log(f"\n[{now_iso()}] done  ok={stats['ok']}  fail={stats['fail']}  "
            f"skipped={stats['skipped']}  by_model={stats['by_model']}")
        return 0 if stats["fail"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
