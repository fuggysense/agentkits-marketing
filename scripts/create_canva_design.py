#!/usr/bin/env python3
"""Create a Canva design for a DCT campaign + patch the tracker.

NOTE (260610): this script serves LEGACY dct-tracker.json workspaces and only
creates an EMPTY design. For dct.json (10-5-5) workspaces use
scripts/canva_push.py — it also Drive-links the renders and uploads them into
the Canva library, idempotently.

Why this exists
---------------
`ad_concept_sheet_writer.py` refuses to write if any batch has canva_link="TBD"
(gate added 260421 after DCT3 shipped with a placeholder). This script closes
the loop: one command creates the Canva design via the `one` CLI, extracts the
design ID, and patches every `canva_link` + `canva_design_id` field in the
tracker (top-level creatives[0] + every visual_variants[] entry).

Usage
-----
    python3 scripts/create_canva_design.py \
        --client neezanizam \
        --campaign dct-260421

    # Then the writer will accept the tracker:
    python3 scripts/ad_concept_sheet_writer.py \
        --client neezanizam --campaign dct-260421 \
        --metrics-campaign buyer-funnel --mode write

Flags
-----
    --client        Client slug (required).
    --campaign      Campaign slug — folder under clients/<client>/campaigns/ (required).
    --batch         Only patch this batch's creatives[] entry. Default: first entry.
    --width         Canvas width in pixels. Default: 1080.
    --height        Canvas height in pixels. Default: 1080.
    --title         Override design title. Default: tracker's canva_title or auto-generated.
    --force         Overwrite existing canva_link even if it's already a real URL.
    --dry-run       Print what would happen without calling Canva or modifying tracker.

Prerequisites
-------------
- `one` CLI installed + authenticated (`one whoami` should return user info).
- Canva connected (`one list` should show canva as operational).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# `one` CLI constants for the Canva "Create a Design" action.
CANVA_CREATE_DESIGN_ACTION = "conn_mod_def::GJ1DEFdLB4w::bKcK46NBRsyKBMMkoMJn_w"
CANVA_CONNECTION_KEY = "live::canva::default::a7dda6c201db4e75bde87c2493dc017f"

# Placeholder values that trigger re-creation (case-insensitive).
PLACEHOLDER_TOKENS = {"", "tbd", "todo", "pending", "none", "null"}


def is_placeholder(value: str | None) -> bool:
    return (value or "").strip().lower() in PLACEHOLDER_TOKENS


def resolve_tracker_path(client: str, campaign: str) -> Path:
    """Handle both flat (dct-260421) and nested (buyer-funnel/CBO.../W1_DCT3.../) layouts."""
    flat = REPO_ROOT / "clients" / client / "campaigns" / campaign / "dct-tracker.json"
    if flat.exists():
        return flat
    # Nested fallback: scan for dct-tracker.json under campaigns/<something>/<campaign>/
    campaigns_dir = REPO_ROOT / "clients" / client / "campaigns"
    matches = list(campaigns_dir.rglob(f"**/{campaign}/dct-tracker.json"))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise SystemExit(
            f"Ambiguous --campaign '{campaign}' — multiple trackers match:\n  "
            + "\n  ".join(str(m.relative_to(REPO_ROOT)) for m in matches)
            + "\nPass the full relative path as --campaign instead."
        )
    raise SystemExit(
        f"No tracker found for --client {client} --campaign {campaign}. "
        f"Expected at {flat.relative_to(REPO_ROOT)} (or a nested equivalent)."
    )


def generate_title(tracker: dict, creative: dict, client: str, campaign: str) -> str:
    """Prefer tracker's canva_title, else build from client/campaign/batch/angle."""
    explicit = creative.get("canva_title") or tracker.get("canva_title")
    if explicit:
        return explicit
    batch = creative.get("batch", "UNKNOWN")
    angle = creative.get("angle", "untitled").lower().replace(" ", "-")
    angle = re.sub(r"[^a-z0-9-]", "", angle)[:40]
    return f"{client}_{campaign}_{batch}_{angle}"


def call_one_canva_create(title: str, width: int, height: int) -> dict:
    """Invoke `one actions execute canva ...` and return parsed response."""
    payload = json.dumps(
        {
            "title": title,
            "design_type": {"type": "custom", "width": width, "height": height},
        }
    )
    cmd = [
        "one", "actions", "execute", "canva",
        CANVA_CREATE_DESIGN_ACTION,
        CANVA_CONNECTION_KEY,
        "--data", payload,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise SystemExit(
            f"`one` CLI exited {result.returncode}.\nstderr:\n{result.stderr}\nstdout:\n{result.stdout}"
        )

    # Extract the JSON response block — `one` prints a spinner + "Response:" header
    # before the actual JSON. Find the first '{' after "Response:".
    stdout = result.stdout
    anchor = stdout.find("Response:")
    if anchor < 0:
        raise SystemExit(f"Could not find 'Response:' in `one` output:\n{stdout}")
    json_start = stdout.find("{", anchor)
    if json_start < 0:
        raise SystemExit(f"Could not find JSON start after 'Response:':\n{stdout[anchor:]}")

    # Parse by balancing braces (the response is followed by more output).
    depth = 0
    end = None
    for i, ch in enumerate(stdout[json_start:], start=json_start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end is None:
        raise SystemExit(f"Unbalanced JSON in `one` response:\n{stdout[json_start:]}")

    try:
        return json.loads(stdout[json_start:end])
    except json.JSONDecodeError as e:
        raise SystemExit(f"Failed to parse JSON: {e}\nRaw:\n{stdout[json_start:end]}")


def patch_tracker(tracker_path: Path, batch_filter: str | None, design_id: str, design_url: str) -> list[str]:
    """Patch every canva_link + canva_design_id field inside the matching creatives[]
    entry (top-level + nested visual_variants[]). Returns list of changed paths."""
    tracker = json.loads(tracker_path.read_text())
    creatives = tracker.get("creatives", [])
    if not creatives:
        raise SystemExit(f"Tracker has no creatives[]: {tracker_path}")

    changed: list[str] = []
    for i, c in enumerate(creatives):
        if batch_filter and c.get("batch") != batch_filter:
            continue
        if not is_placeholder(c.get("canva_link")) and c.get("canva_link") != design_url:
            # Already a real URL — only overwrite when caller forced it (handled upstream)
            pass
        c["canva_link"] = design_url
        c["canva_design_id"] = design_id
        changed.append(f"creatives[{i}] (batch={c.get('batch')}): canva_link + canva_design_id")
        for j, v in enumerate(c.get("visual_variants", []) or []):
            v["canva_link"] = design_url
            v["canva_design_id"] = design_id
            changed.append(
                f"creatives[{i}].visual_variants[{j}] (variant={v.get('variant')}): canva_link + canva_design_id"
            )
        if batch_filter:
            break

    tracker_path.write_text(json.dumps(tracker, indent=2, ensure_ascii=False) + "\n")
    return changed


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a Canva design + patch dct-tracker.json.")
    ap.add_argument("--client", required=True, help="Client slug (e.g. neezanizam).")
    ap.add_argument("--campaign", required=True, help="Campaign slug (folder under clients/<c>/campaigns/).")
    ap.add_argument("--batch", help="Only patch this batch's creatives[] entry. Default: first entry.")
    ap.add_argument("--width", type=int, default=1080, help="Canvas width px. Default: 1080.")
    ap.add_argument("--height", type=int, default=1080, help="Canvas height px. Default: 1080.")
    ap.add_argument("--title", help="Override design title.")
    ap.add_argument("--force", action="store_true", help="Overwrite existing canva_link even if it's a real URL.")
    ap.add_argument("--dry-run", action="store_true", help="Preview without calling Canva or patching.")
    args = ap.parse_args()

    tracker_path = resolve_tracker_path(args.client, args.campaign)
    tracker = json.loads(tracker_path.read_text())
    creatives = tracker.get("creatives", [])
    if not creatives:
        raise SystemExit(f"Tracker has no creatives[]: {tracker_path}")

    # Pick the target creative
    if args.batch:
        target = next((c for c in creatives if c.get("batch") == args.batch), None)
        if target is None:
            raise SystemExit(
                f"No creative with batch='{args.batch}' in tracker. "
                f"Available: {[c.get('batch') for c in creatives]}"
            )
    else:
        target = creatives[0]

    # Skip if already a real URL (unless --force)
    existing = target.get("canva_link", "")
    if not is_placeholder(existing) and not args.force:
        print(f"Creative '{target.get('batch')}' already has canva_link={existing!r}.")
        print(f"Pass --force to overwrite. Tracker: {tracker_path.relative_to(REPO_ROOT)}")
        return 0

    title = args.title or generate_title(tracker, target, args.client, args.campaign)
    print(f"Tracker: {tracker_path.relative_to(REPO_ROOT)}")
    print(f"Target batch: {target.get('batch')}")
    print(f"Design title: {title}")
    print(f"Dimensions: {args.width}x{args.height}")
    print(f"Existing canva_link: {existing!r}")
    print()

    if args.dry_run:
        print("DRY RUN — would call `one actions execute canva` + patch tracker.")
        return 0

    print("Calling `one actions execute canva` (Create a Design)...")
    response = call_one_canva_create(title, args.width, args.height)
    design = response.get("design") or {}
    design_id = design.get("id")
    if not design_id:
        raise SystemExit(f"No design.id in Canva response:\n{json.dumps(response, indent=2)}")

    # Canonical clean URL (matches DCT1/DCT2/DCT003 pattern in this repo)
    design_url = f"https://www.canva.com/design/{design_id}/edit"

    print(f"Created Canva design: id={design_id}")
    print(f"URL: {design_url}")
    print()

    changed = patch_tracker(tracker_path, args.batch, design_id, design_url)
    print("Tracker patched:")
    for line in changed:
        print(f"  - {line}")
    print()
    print(f"Next: python3 scripts/ad_concept_sheet_writer.py --client {args.client} \\")
    print(f"          --campaign {args.campaign} --metrics-campaign <funnel> --mode preview")
    return 0


if __name__ == "__main__":
    sys.exit(main())
