#!/usr/bin/env python3
"""Render an ad image from a final prompt, through a swappable engine.

The orchestrator (Claude) crafts the prompt using a style from styles/ — that's the
creative step. This script is the mechanical step: take a finished prompt and turn it
into a saved PNG. Default engine is GPT Image 2 (Azure); add another by dropping one
function into ENGINES.

The approval gate: run with --dry-run first to see exactly what would be sent and
where it lands, with zero credit spend. Drop --dry-run to actually render.

Examples
  # list what's available
  render.py --list-styles
  render.py --list-engines

  # preview (no credits), then render a hand-crafted prompt
  render.py --prompt "documentary photo, ..." --out out/a01-v1.png --style dr-clean-static --dry-run
  render.py --prompt "documentary photo, ..." --out out/a01-v1.png --style dr-clean-static

  # render straight from a dct-tracker.json image_prompt
  render.py --from-tracker clients/neezanizam/campaigns/dct-10-5-5-proof-260603/dct-tracker.json \
            --batch DCT010-A01 --variant v1 --dry-run
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "styles" / "_registry.json"
GPT_IMAGE_2 = Path.home() / ".claude" / "scripts" / "gpt-image-2"


# ---- engines -------------------------------------------------------------
# Each engine: (prompt, out, size, quality, refs, dry_run) -> dict result.
# To add Nano Banana / Higgsfield / any CLI later: write one function, register it
# in ENGINES below. Nothing else changes.

def engine_gpt_image_2(prompt, out, size, quality, refs, dry_run):
    if not GPT_IMAGE_2.exists():
        raise SystemExit(f"executor not found: {GPT_IMAGE_2}")
    cmd = [str(GPT_IMAGE_2), prompt, "--out", str(out), "--size", size, "--quality", quality]
    for r in refs:
        cmd += ["--ref", r]
    if dry_run:
        return {"would_run": cmd}
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"gpt-image-2 failed (exit {proc.returncode}):\n{proc.stderr.strip()}")
    return {"ran": cmd, "stdout": proc.stdout.strip()}


ENGINES = {
    "gpt-image-2": engine_gpt_image_2,
    # "nano-banana": engine_nano_banana,      # add when the Vertex path is wired + tested
    # "higgsfield":  engine_higgsfield,
}
DEFAULT_ENGINE = "gpt-image-2"


# ---- helpers -------------------------------------------------------------

def load_registry():
    return json.loads(REGISTRY.read_text())


def prompt_from_tracker(tracker_path, batch, variant):
    """Pull a variant's image_prompt out of a dct-tracker.json.

    Handles both the inline `image_prompt` string and the file-reference
    convention (`image_prompt_file` -> a JSON file holding the prompt).
    """
    data = json.loads(Path(tracker_path).read_text())
    creatives = data.get("creatives") or data.get("ads") or []
    entry = next((c for c in creatives if c.get("batch") == batch), None)
    if entry is None:
        raise SystemExit(f"batch {batch!r} not found in {tracker_path}")
    variations = entry.get("variations") or []
    var = next((v for v in variations if v.get("variant_id") == variant or v.get("variant") == variant), None)
    if var is None:
        raise SystemExit(f"variant {variant!r} not found under {batch}")
    if var.get("image_prompt"):
        return var["image_prompt"]
    ref = var.get("image_prompt_file")
    if ref:
        p = (Path(tracker_path).parent / ref) if not Path(ref).is_absolute() else Path(ref)
        if not p.exists():
            p = Path.cwd() / ref  # fall back to repo-root-relative
        blob = json.loads(p.read_text())
        return blob.get("image_prompt") or json.dumps(blob)
    raise SystemExit(f"no image_prompt or image_prompt_file on {batch}/{variant}")


# ---- main ----------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(prog="render.py", description="Render an ad image through a swappable engine.")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--prompt", help="final image prompt to render")
    src.add_argument("--from-tracker", help="path to a dct-tracker.json")
    ap.add_argument("--batch", help="with --from-tracker: which batch, e.g. DCT010-A01")
    ap.add_argument("--variant", default="v1", help="with --from-tracker: which variant (default v1)")
    ap.add_argument("--out", "-o", help="output PNG path (auto-derived for tracker mode if omitted)")
    ap.add_argument("--engine", default=DEFAULT_ENGINE, help=f"image engine (default {DEFAULT_ENGINE})")
    ap.add_argument("--style", help="style key (metadata + traceability; the orchestrator uses it to craft the prompt)")
    ap.add_argument("--size", default="1024x1024", help="1024x1024 (1:1, default) | 1024x1536 | 1536x1024 | auto")
    ap.add_argument("--quality", default="high", help="low | medium | high (default) | auto")
    ap.add_argument("--ref", action="append", default=[], help="reference image (repeatable, e.g. product shot)")
    ap.add_argument("--dry-run", action="store_true", help="the approval gate: show what would happen, spend nothing")
    ap.add_argument("--list-styles", action="store_true")
    ap.add_argument("--list-engines", action="store_true")
    args = ap.parse_args()

    if args.list_engines:
        print("Engines:")
        for k in ENGINES:
            print(f"  {k}{'  (default)' if k == DEFAULT_ENGINE else ''}")
        return 0

    reg = load_registry()
    if args.list_styles:
        print(f"Styles (default: {reg['default_style']}):")
        for key, s in reg["styles"].items():
            print(f"  {key:<18} {s['label']}\n{'':20}{s['use_when']}")
        return 0

    if args.engine not in ENGINES:
        raise SystemExit(f"unknown engine {args.engine!r}. Available: {', '.join(ENGINES)}")
    if args.style and args.style not in reg["styles"]:
        raise SystemExit(f"unknown style {args.style!r}. Run --list-styles.")

    # resolve the prompt
    if args.from_tracker:
        if not args.batch:
            raise SystemExit("--from-tracker needs --batch (and optionally --variant)")
        prompt = prompt_from_tracker(args.from_tracker, args.batch, args.variant)
        out = args.out or str(Path(args.from_tracker).parent / "image-prompts" / "renders" / f"{args.batch}-{args.variant}.png")
    elif args.prompt:
        prompt = args.prompt
        out = args.out
    else:
        raise SystemExit("give either --prompt or --from-tracker")
    if not out:
        raise SystemExit("--out is required (could not auto-derive)")

    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    engine = ENGINES[args.engine]
    result = engine(prompt, out_path, args.size, args.quality, args.ref, args.dry_run)

    # sidecar log — every render leaves a trail of what made it
    meta = {
        "rendered_at": datetime.now().isoformat(timespec="seconds"),
        "engine": args.engine,
        "style": args.style,
        "size": args.size,
        "quality": args.quality,
        "refs": args.ref,
        "source": args.from_tracker or "inline-prompt",
        "batch": args.batch,
        "variant": args.variant if args.from_tracker else None,
        "prompt": prompt,
        "out": str(out_path),
        "dry_run": args.dry_run,
    }

    if args.dry_run:
        print("── DRY RUN (no credits spent) ─────────────────────────────")
        print(f"engine : {args.engine}")
        print(f"style  : {args.style or '(none specified)'}")
        print(f"out    : {out_path}")
        print(f"size   : {args.size}   quality: {args.quality}")
        if args.ref:
            print(f"refs   : {', '.join(args.ref)}")
        print(f"\nprompt :\n{prompt}\n")
        print(f"would run: {' '.join(result['would_run'])}")
        print("\nApprove? re-run the same command without --dry-run.")
        return 0

    meta_path = out_path.with_suffix(out_path.suffix + ".meta.json")
    meta_path.write_text(json.dumps(meta, indent=2))
    print(f"✅ rendered → {out_path}")
    print(f"   log      → {meta_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
