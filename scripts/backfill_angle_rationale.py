#!/usr/bin/env python3
"""Backfill `07b_angle_rationale.md` into an existing big-angle-spotter DCT run dir.

Re-uses the system prompt written to `system_prompt.txt` at original run time
plus the `07_expansion.md` output. Invokes a fresh Sonnet `claude -p` worker
to produce a 3-paragraph strategic rationale suitable for the ANGLE column of
the CREATIVES sheet.

Usage:
    python3 scripts/backfill_angle_rationale.py \\
        --dct-dir clients/neezanizam/angles/big-angle-spotter/wave-1/DCT1

    python3 scripts/backfill_angle_rationale.py \\
        --dct-dir clients/neezanizam/angles/big-angle-spotter/wave-1/DCT1 \\
        --tracker clients/neezanizam/campaigns/buyer-funnel/CBO_Test_BuyerFunnel_Apr26/W1_DCT1_Broad_HesitantCalculator_3NumberTest_50/dct-tracker.json

When `--tracker` is passed, also patches the tracker's
`creatives[0].angle_rationale` field so `ad_concept_sheet_writer.py` will pick
it up on the next sheet write.

Stdlib only. Python 3.9+.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path


_TRAILING_GARBAGE_RE = re.compile(r"[\x00-\x1f\s]+$")
WORKER_TIMEOUT_SEC = 600


STEP_7B_PROMPT = """You are writing the strategic rationale for this angle that will sit in the ANGLE column of the client's ad-testing Google Sheet. A marketing operator reads this cell to understand, at a glance, what the angle attacks, the psychological trigger it activates, and how it reframes the buyer's thinking.

Compress the angle expansion above (step 07) into EXACTLY 3 paragraphs, 120-180 words total. Third-person descriptive voice ("This angle attacks…" / "The creative forces…" / "It reframes…"). NOT second-person, NOT first-person.

Paragraph 1 — The uncomfortable truth (40-60 words): What this angle attacks. The gap between how the persona sees themselves today and what's actually happening underneath. Be specific about the surface story vs. the hidden reality.

Paragraph 2 — The angle + the trigger (40-60 words): Name the angle in 2-4 words (e.g. "Referral Dependency Exposure", "Pipeline Fragility"). Then describe the psychological mechanism it activates — the specific fear, identity threat, status anxiety, or cognitive dissonance. Link it to what the persona literally feels in the moment.

Paragraph 3 — The reframe (40-60 words): How the angle repositions what success means for this persona. Shift them from "I already have X" to "X is not the real win — Y is". End on the new definition of winning.

Hard rules:
- UK English (realise, colour, behaviour, optimise, centre)
- No AI-triplets ("not X, not Y, but Z")
- No corny / cringey / LinkedIn-influencer energy
- No banned persona words — honour the tonal contract from your system prompt's PERSONA field
- Third-person descriptive throughout
- Silver Bullet sentence may be referenced but not quoted verbatim — compress, don't copy

Output: exactly 3 paragraphs, blank line between each. No headings. No bullets. No preamble. No "Here is the rationale:" prefix. Just the 3 paragraphs."""


def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)


def invoke_worker(system_prompt: str, prompt: str, label: str, dry_run: bool) -> str:
    session_id = str(uuid.uuid4())
    cmd = [
        "claude",
        "-p",
        "--model", "sonnet",
        "--session-id", session_id,
        "--system-prompt", system_prompt,
        "--tools", "",
        "--output-format", "json",
        "--dangerously-skip-permissions",
        "--no-session-persistence",
        prompt,
    ]
    if dry_run:
        log(f"DRY-RUN [{label}] would invoke claude -p (session {session_id[:8]})")
        return "(dry-run rationale — three paragraphs would appear here)"

    log(f"[{label}] spawning fresh Sonnet worker (session {session_id[:8]})")
    t0 = datetime.now()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=WORKER_TIMEOUT_SEC,
        )
    except subprocess.TimeoutExpired:
        raise SystemExit(f"[{label}] claude -p exceeded {WORKER_TIMEOUT_SEC}s timeout")

    dt = (datetime.now() - t0).total_seconds()
    if proc.returncode != 0:
        log(f"[{label}] claude -p exited {proc.returncode}: {proc.stderr[:500]}", "ERROR")
        raise SystemExit(f"[{label}] worker failed")

    stdout_clean = _TRAILING_GARBAGE_RE.sub("", proc.stdout)
    try:
        data = json.loads(stdout_clean)
    except json.JSONDecodeError:
        log(f"[{label}] non-JSON stdout head: {proc.stdout[:500]}", "ERROR")
        raise SystemExit(f"[{label}] worker returned non-JSON output")

    if data.get("is_error"):
        raise SystemExit(f"[{label}] worker reported error: {data.get('result', '')[:500]}")

    log(f"[{label}] done in {dt:.1f}s — {data.get('usage', {}).get('output_tokens', 0)} out tokens")
    return data["result"]


def main() -> int:
    ap = argparse.ArgumentParser(description="Backfill 07b_angle_rationale.md into an existing big-angle-spotter run dir.")
    ap.add_argument("--dct-dir", required=True, help="Path to DCT folder containing 07_expansion.md + system_prompt.txt + inputs.json")
    ap.add_argument("--tracker", help="Optional: path to dct-tracker.json to patch with angle_rationale field")
    ap.add_argument("--dry-run", action="store_true", help="Print commands, skip actual claude -p invocation")
    ap.add_argument("--force", action="store_true", help="Overwrite existing 07b_angle_rationale.md")
    args = ap.parse_args()

    dct_dir = Path(args.dct_dir).resolve()
    if not dct_dir.is_dir():
        raise SystemExit(f"DCT directory not found: {dct_dir}")

    expansion_path = dct_dir / "07_expansion.md"
    sp_path = dct_dir / "system_prompt.txt"
    if not expansion_path.exists():
        raise SystemExit(f"07_expansion.md not found in {dct_dir}")
    if not sp_path.exists():
        raise SystemExit(f"system_prompt.txt not found in {dct_dir}")

    output_path = dct_dir / "07b_angle_rationale.md"
    if output_path.exists() and not args.force:
        raise SystemExit(f"{output_path} already exists — use --force to overwrite")

    system_prompt = sp_path.read_text()
    expansion = expansion_path.read_text().strip()

    # Build minimal-context prompt in the same format run_pipeline.py uses for deps.
    context = (
        "## Input — expansion (from step 07)\n"
        "\n"
        f"{expansion}\n"
        "\n"
        "---\n"
        "\n"
    )
    full_prompt = context + STEP_7B_PROMPT

    rationale = invoke_worker(system_prompt, full_prompt, label="step07b", dry_run=args.dry_run)

    output_path.write_text(rationale.strip() + "\n")
    log(f"wrote {output_path}")

    if args.tracker:
        tracker_path = Path(args.tracker).resolve()
        if not tracker_path.exists():
            raise SystemExit(f"tracker not found: {tracker_path}")
        if args.dry_run:
            log(f"DRY-RUN would patch {tracker_path} creatives[0].angle_rationale")
        else:
            tracker = json.loads(tracker_path.read_text())
            creatives = tracker.get("creatives", [])
            if not creatives:
                raise SystemExit(f"tracker has no creatives[]: {tracker_path}")
            creatives[0]["angle_rationale"] = rationale.strip()
            tracker_path.write_text(json.dumps(tracker, indent=2) + "\n")
            log(f"patched {tracker_path} creatives[0].angle_rationale")

    print(f"\n✅ Rationale ready: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
