#!/usr/bin/env python3
"""
Phase 4 — fire B1-B4 reviewers against NeezaNizam v1 draft.

4 fresh `claude -p` Sonnet 4.6 workers in parallel. Content-cached SP holds
grounding files + draft (~75K tokens). Per-worker prompt contains only the
reviewer spec + execute instruction.

Outputs land in clients/neezanizam/sales-letters/260421-v1-reviews/b{1-4}-*.md.
"""

import json
import os
import re
import subprocess
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

def _repo_root() -> Path:
    """Repo root via MARKETING_REPO_ROOT env, else this file's parent.parent
    (this script lives in scripts/)."""
    env = os.environ.get("MARKETING_REPO_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


REPO = _repo_root()
CLIENT = REPO / "clients/neezanizam"
DRAFT = CLIENT / "sales-letters/260421-v1.md"
REVIEWS_DIR = CLIENT / "sales-letters/260421-v1-reviews"
OS_DIR = REPO / ".claude/references/copywriting-os"
LOG_DIR = REVIEWS_DIR / "build-logs"
REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "claude-sonnet-4-6"
TIMEOUT = 900
_TRAIL = re.compile(r"[\x00-\x1f\s]+$")


def read_safe(p: Path) -> str:
    try:
        return p.read_text()
    except Exception:
        return f"[FILE NOT FOUND: {p}]"


def load_dir(d: Path) -> str:
    if not d.exists():
        return f"[DIRECTORY NOT FOUND: {d}]"
    parts = []
    for p in sorted(d.glob("*.md")):
        parts.append(f"--- FILE: {p.relative_to(CLIENT)} ---")
        parts.append(p.read_text())
        parts.append("")
    return "\n".join(parts)


# Build shared SP with all grounding files + draft
SP_PARTS = [
    "# Role",
    "",
    "You are a sub-agent in the Copywriting OS. You execute ONE specific reviewer specification against a client sales letter draft. You produce a structured audit report matching the reviewer's output schema exactly.",
    "",
    "# Client: neezanizam",
    "",
    "Singapore property agents (husband-and-wife team) selling advisory consultation to HDB upgraders and private condo buyers. Voice is measured, evidence-based, consultative; avoids hard-sell language. Voice register frequently carries Singlish markers in raw buyer research.",
    "",
    "# Draft under review — sales-letters/260421-v1.md",
    "",
    "```",
    read_safe(DRAFT),
    "```",
    "",
    "# Grounding file 1 — context-profile.json",
    "",
    "```json",
    read_safe(CLIENT / "context-profile.json"),
    "```",
    "",
    "# Grounding file 2 — source-of-truth.md",
    "",
    read_safe(CLIENT / "source-of-truth.md"),
    "",
    "# Grounding file 3 — buyer-profile.md",
    "",
    read_safe(CLIENT / "buyer-profile.md"),
    "",
    "# Grounding file 4 — research/buyer-language-dossier.md",
    "",
    read_safe(CLIENT / "research/buyer-language-dossier.md"),
    "",
    "# Grounding file 5 — research/life-transition-dossier-260418.md",
    "",
    read_safe(CLIENT / "research/life-transition-dossier-260418.md"),
    "",
    "# Grounding file 6 — avatars/ (all files in directory)",
    "",
    load_dir(CLIENT / "avatars"),
    "",
    "# Grounding file 7 — learnings.md",
    "",
    read_safe(CLIENT / "learnings.md"),
    "",
    "# Output contract",
    "",
    "- Your response IS the audit report. Return it inline as your text output.",
    "- Do NOT call any tool, write to any file, or upload anywhere. The orchestrator writes your response.",
    "- FIRST CHARACTER of your response must be `#`. FIRST LINE must be the report title.",
    "- No meta-preamble. No 'Here is the audit'. No 'File written'. No trailing summary of what you did.",
    "- Output schema MUST match the reviewer spec's `## Output Schema` block verbatim in structure.",
    "- Populate every field with real findings. If a section is genuinely empty, write 'None found' — not 'N/A' or '-'.",
    "- Use exact draft line numbers where cited. UK English throughout.",
    "- Target length: proportional to findings. A thorough audit of a 329-line draft typically lands 80-200 lines.",
]
SP = "\n".join(SP_PARTS)


def run_worker(prompt: str, output_path: Path, label: str) -> dict:
    session = str(uuid.uuid4())
    cmd = [
        "claude", "-p",
        "--model", MODEL,
        "--tools", "",
        "--output-format", "json",
        "--dangerously-skip-permissions",
        "--no-session-persistence",
        "--session-id", session,
        "--system-prompt", SP,
        prompt,
    ]
    t0 = datetime.now()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return {"label": label, "ok": False, "error": f"timeout after {TIMEOUT}s", "dt": TIMEOUT}
    dt = (datetime.now() - t0).total_seconds()
    if proc.returncode != 0:
        return {"label": label, "ok": False, "error": proc.stderr[:800], "dt": dt}
    try:
        data = json.loads(_TRAIL.sub("", proc.stdout))
    except json.JSONDecodeError:
        return {"label": label, "ok": False, "error": f"non-JSON head: {proc.stdout[:400]}", "dt": dt}
    if data.get("is_error"):
        return {"label": label, "ok": False, "error": data.get("result", "")[:800], "dt": dt}

    result = data["result"]
    if not result.lstrip().startswith("# "):
        return {"label": label, "ok": False,
                "error": f"response does not start with '# '. Head: {result[:300]}", "dt": dt}
    output_path.write_text(result.rstrip() + "\n")
    usage = data.get("usage", {})
    cost = data.get("total_cost_usd", 0)
    (LOG_DIR / f"{label}.log.json").write_text(json.dumps({
        "label": label, "dt_sec": dt,
        "in_tok": usage.get("input_tokens", 0),
        "out_tok": usage.get("output_tokens", 0),
        "cache_read": usage.get("cache_read_input_tokens", 0),
        "cost_usd": cost, "session": session,
        "output_path": str(output_path),
    }, indent=2))
    return {"label": label, "ok": True, "path": str(output_path), "dt": dt,
            "out_tok": usage.get("output_tokens", 0),
            "cache_read": usage.get("cache_read_input_tokens", 0),
            "cost": cost}


REVIEWER_PROMPTS = [
    ("B1_claim_verification", "claim-verification-audit.md",
     REVIEWS_DIR / "b1-claim-verification.md"),
    ("B2_forbidden_content", "forbidden-content-audit.md",
     REVIEWS_DIR / "b2-forbidden-content.md"),
    ("B3_specificity", "specificity-audit.md",
     REVIEWS_DIR / "b3-specificity.md"),
    ("B4_buyer_language_fidelity", "buyer-language-fidelity-audit.md",
     REVIEWS_DIR / "b4-buyer-language-fidelity.md"),
]


def build_prompt(spec_filename: str) -> str:
    spec_path = OS_DIR / "reviewers" / spec_filename
    spec = spec_path.read_text()
    return f"""# Reviewer specification — follow exactly

{spec}

---

# Instruction

Execute the reviewer above against the draft in the system prompt. Use the grounding files in the system prompt as your source of truth. Produce the full audit report matching the Output Schema in the spec. Start your response with `#` as the title line. No preamble."""


def main():
    print(f"[{datetime.now():%H:%M:%S}] Phase 4 acceptance test — B1-B4 on NeezaNizam v1", flush=True)
    print(f"[{datetime.now():%H:%M:%S}] Model: {MODEL}, SP length: {len(SP)} chars ({len(SP)//4} est tokens)", flush=True)
    print("", flush=True)

    t0 = datetime.now()
    results = []
    tasks = [(label, build_prompt(spec), out) for (label, spec, out) in REVIEWER_PROMPTS]
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(run_worker, prompt, out, label): label for (label, prompt, out) in tasks}
        for f in as_completed(futures):
            r = f.result()
            results.append(r)
            status = "OK " if r["ok"] else "FAIL"
            if r["ok"]:
                print(f"[{datetime.now():%H:%M:%S}] {status} [{r['label']}] {r['dt']:.1f}s "
                      f"out={r['out_tok']} cache_read={r.get('cache_read', 0)} ${r['cost']:.4f} "
                      f"→ {Path(r['path']).name}", flush=True)
            else:
                print(f"[{datetime.now():%H:%M:%S}] {status} [{r['label']}] {r['dt']:.1f}s — {r['error'][:200]}", flush=True)

    total_dt = (datetime.now() - t0).total_seconds()
    ok_count = sum(1 for r in results if r["ok"])
    total_cost = sum(r.get("cost", 0) for r in results)
    print("", flush=True)
    print(f"[{datetime.now():%H:%M:%S}] SUMMARY: {ok_count}/4 ok, total {total_dt:.1f}s, ${total_cost:.4f}", flush=True)
    (LOG_DIR / f"run-{datetime.now():%Y%m%d-%H%M%S}.json").write_text(
        json.dumps({"results": results, "total_dt": total_dt, "total_cost": total_cost}, indent=2, default=str)
    )
    return 0 if ok_count == 4 else 1


if __name__ == "__main__":
    sys.exit(main())
