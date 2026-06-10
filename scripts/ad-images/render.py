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

  # render straight from a dct.json image_pool (current shape)
  render.py --from-tracker clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/dct.json \
            --image DCT002-img-01 --dry-run
  # whole pool at once (dry-run resolves every image_prompt; render gated by --confirm-all)
  render.py --from-tracker .../dct.json --dry-run
  # filter the pool by angle, then variant
  render.py --from-tracker .../dct.json --batch A02 --variant v1 --dry-run

  # legacy creatives[]/variations[] shape (auto-detected; force with --legacy-shape)
  render.py --from-tracker .../dct-tracker.json --batch DCT010-A01 --variant v1 --dry-run
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
CLAIM_GATE = Path("/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/scripts/claim_gate.py")


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


def run_claim_gate(tracker_path, skip):
    """Run the claim gate over a tracker before rendering.

    The gate (scripts/claim_gate.py) is being built in parallel. This hook NO-OPs
    gracefully (warns) when it is absent so render.py never blocks on a missing tool.
    --skip-claim-gate opts out explicitly, with a logged warning either way.
    """
    if skip:
        print("⚠️  claim gate SKIPPED (--skip-claim-gate) — claims not verified before render", file=sys.stderr)
        return {"status": "skipped"}
    if not CLAIM_GATE.exists():
        print(f"⚠️  claim gate not found at {CLAIM_GATE} — skipping (built in parallel)", file=sys.stderr)
        return {"status": "absent"}
    cmd = [sys.executable, str(CLAIM_GATE), "--gate", str(tracker_path)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(
            f"claim gate FAILED (exit {proc.returncode}) on {tracker_path}:\n{proc.stdout.strip()}\n{proc.stderr.strip()}\n"
            "Fix the flagged claims or re-run with --skip-claim-gate to override."
        )
    if proc.stdout.strip():
        print(proc.stdout.strip())
    return {"status": "passed"}


def detect_shape(data):
    """Return 'current' for dct.json (image_pool.images[]), else 'legacy'."""
    pool = data.get("image_pool")
    if isinstance(pool, dict) and isinstance(pool.get("images"), list):
        return "current"
    return "legacy"


def resolve_prompt_from_image(img, tracker_path):
    """Pull the prompt out of one image_pool image (inline or file-reference)."""
    if img.get("image_prompt"):
        return img["image_prompt"]
    ref = img.get("image_prompt_file")
    if ref:
        p = (Path(tracker_path).parent / ref) if not Path(ref).is_absolute() else Path(ref)
        if not p.exists():
            p = Path.cwd() / ref  # fall back to repo-root-relative
        blob = json.loads(p.read_text())
        return blob.get("image_prompt") or json.dumps(blob)
    raise SystemExit(f"image {img.get('id')!r} has no image_prompt or image_prompt_file")


def resolve_current_shape(data, tracker_path, image_id, batch, variant):
    """Resolve one-or-more (id, prompt) pairs from a dct.json image_pool.

    Selection precedence:
      --image <id>          -> exactly that image
      --batch <angle_id>    -> all pool images with matching angle_id (+ --variant if given)
      (nothing)             -> the whole pool
    """
    images = data["image_pool"]["images"]

    if image_id:
        img = next((i for i in images if i.get("id") == image_id), None)
        if img is None:
            ids = ", ".join(i.get("id", "?") for i in images)
            raise SystemExit(f"image {image_id!r} not in pool. Available: {ids}")
        return [(img["id"], resolve_prompt_from_image(img, tracker_path))]

    if batch:
        picked = [i for i in images if i.get("angle_id") == batch]
        if variant:
            picked = [i for i in picked if i.get("variant_id") == variant]
        if not picked:
            angles = sorted({i.get("angle_id") for i in images if i.get("angle_id")})
            raise SystemExit(
                f"no pool image with angle_id={batch!r}"
                + (f" + variant_id={variant!r}" if variant else "")
                + f". Angles present: {', '.join(angles)}"
            )
        return [(i["id"], resolve_prompt_from_image(i, tracker_path)) for i in picked]

    # whole pool
    return [(i["id"], resolve_prompt_from_image(i, tracker_path)) for i in images]


def resolve_legacy_shape(data, tracker_path, batch, variant):
    """Pull a variant's image_prompt out of a legacy creatives[]/variations[] tracker.

    Handles both the inline `image_prompt` string and the file-reference
    convention (`image_prompt_file` -> a JSON file holding the prompt).
    """
    if not batch:
        raise SystemExit("legacy shape needs --batch (e.g. DCT010-A01)")
    creatives = data.get("creatives") or data.get("ads") or []
    entry = next((c for c in creatives if c.get("batch") == batch), None)
    if entry is None:
        raise SystemExit(f"batch {batch!r} not found in {tracker_path}")
    variations = entry.get("variations") or []
    var = next((v for v in variations if v.get("variant_id") == variant or v.get("variant") == variant), None)
    if var is None:
        raise SystemExit(f"variant {variant!r} not found under {batch}")
    if var.get("image_prompt"):
        return [(f"{batch}-{variant}", var["image_prompt"])]
    ref = var.get("image_prompt_file")
    if ref:
        p = (Path(tracker_path).parent / ref) if not Path(ref).is_absolute() else Path(ref)
        if not p.exists():
            p = Path.cwd() / ref  # fall back to repo-root-relative
        blob = json.loads(p.read_text())
        return [(f"{batch}-{variant}", blob.get("image_prompt") or json.dumps(blob))]
    raise SystemExit(f"no image_prompt or image_prompt_file on {batch}/{variant}")


def out_path_for(tracker_path, shape, key):
    """Default render target. Current shape ships into images/<id>.png next to dct.json
    (matching where the pool already references files); legacy keeps the renders/ subdir."""
    parent = Path(tracker_path).parent
    if shape == "current":
        return parent / "images" / f"{key}.png"
    return parent / "image-prompts" / "renders" / f"{key}.png"


# ---- main ----------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(prog="render.py", description="Render an ad image through a swappable engine.")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--prompt", help="final image prompt to render")
    src.add_argument("--from-tracker", help="path to a dct.json (current shape) or legacy dct-tracker.json")
    ap.add_argument("--image", help="current shape: pool image id, e.g. DCT002-img-01")
    ap.add_argument("--batch", help="angle_id (current shape) or batch id (legacy), e.g. A02 / DCT010-A01")
    ap.add_argument("--variant", help="variant id, e.g. v1 (filters current shape, required for legacy)")
    ap.add_argument("--legacy-shape", action="store_true", help="force the legacy creatives[]/variations[] parser (otherwise auto-detected)")
    ap.add_argument("--skip-claim-gate", action="store_true", help="skip claim_gate.py pre-render check (logs a warning)")
    ap.add_argument("--out", "-o", help="output PNG path (auto-derived for tracker mode if omitted; single selection only)")
    ap.add_argument("--engine", default=DEFAULT_ENGINE, help=f"image engine (default {DEFAULT_ENGINE})")
    ap.add_argument("--style", help="style key (metadata + traceability; the orchestrator uses it to craft the prompt)")
    ap.add_argument("--size", default="1024x1024", help="1024x1024 (1:1, default) | 1024x1536 | 1536x1024 | auto")
    ap.add_argument("--quality", default="high", help="low | medium | high (default) | auto")
    ap.add_argument("--ref", action="append", default=[], help="reference image (repeatable, e.g. product shot)")
    ap.add_argument("--confirm-all", action="store_true", help="required to REALLY render a whole pool (>1 image) at once")
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

    # resolve the prompt(s) -> list of (key, prompt)
    if args.from_tracker:
        run_claim_gate(args.from_tracker, args.skip_claim_gate)
        data = json.loads(Path(args.from_tracker).read_text())
        shape = "legacy" if args.legacy_shape else detect_shape(data)
        if shape == "current":
            jobs = resolve_current_shape(data, args.from_tracker, args.image, args.batch, args.variant)
        else:
            jobs = resolve_legacy_shape(data, args.from_tracker, args.batch, args.variant)
    elif args.prompt:
        if not args.out:
            raise SystemExit("--prompt needs --out")
        shape = "inline"
        jobs = [(None, args.prompt)]
    else:
        raise SystemExit("give either --prompt or --from-tracker")

    if args.out and len(jobs) > 1:
        raise SystemExit("--out only works with a single selection; drop it (paths auto-derive) or narrow with --image/--batch")
    if not args.dry_run and len(jobs) > 1 and not args.confirm_all:
        raise SystemExit(f"about to render {len(jobs)} images for real — re-run with --confirm-all, or narrow with --image/--batch (or use --dry-run)")

    engine = ENGINES[args.engine]
    rendered, dry_previews = 0, []

    for key, prompt in jobs:
        if args.from_tracker:
            out = Path(args.out) if args.out else out_path_for(args.from_tracker, shape, key)
        else:
            out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)

        result = engine(prompt, out, args.size, args.quality, args.ref, args.dry_run)

        if args.dry_run:
            dry_previews.append((key, out, prompt, result["would_run"]))
            continue

        # sidecar log — every render leaves a trail of what made it
        meta = {
            "rendered_at": datetime.now().isoformat(timespec="seconds"),
            "engine": args.engine,
            "style": args.style,
            "size": args.size,
            "quality": args.quality,
            "refs": args.ref,
            "source": args.from_tracker or "inline-prompt",
            "shape": shape,
            "key": key,
            "prompt": prompt,
            "out": str(out),
            "dry_run": False,
        }
        meta_path = out.with_suffix(out.suffix + ".meta.json")
        meta_path.write_text(json.dumps(meta, indent=2))
        print(f"✅ rendered → {out}")
        print(f"   log      → {meta_path}")
        rendered += 1

    if args.dry_run:
        print("── DRY RUN (no credits spent) ─────────────────────────────")
        print(f"engine : {args.engine}")
        print(f"style  : {args.style or '(none specified)'}")
        print(f"shape  : {shape}")
        print(f"jobs   : {len(dry_previews)}")
        for key, out, prompt, would_run in dry_previews:
            print("\n" + "─" * 60)
            print(f"id     : {key or '(inline)'}")
            print(f"out    : {out}")
            print(f"size   : {args.size}   quality: {args.quality}")
            if args.ref:
                print(f"refs   : {', '.join(args.ref)}")
            print(f"\nprompt :\n{prompt}\n")
            print(f"would run: {' '.join(would_run)}")
        print("\nApprove? re-run the same command without --dry-run (add --confirm-all for a whole pool).")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
