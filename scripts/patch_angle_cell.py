#!/usr/bin/env python3
"""Surgical patch: update ONLY the ANGLE column (G) for existing CREATIVES rows
that have been backfilled with an `angle_rationale` field in their dct-tracker.json.

Use after `backfill_angle_rationale.py` has populated the tracker — this script
reads each tracker, finds the matching row in the CREATIVES tab by BATCH, and
writes only the ANGLE cell. Takes a pre-snapshot first. Nothing else touched.

Usage:
    python3 scripts/patch_angle_cell.py \\
        --client neezanizam \\
        --metrics-campaign buyer-funnel \\
        --trackers \\
            "clients/neezanizam/campaigns/buyer-funnel/CBO_Test_BuyerFunnel_Apr26/W1_DCT1_Broad_HesitantCalculator_3NumberTest_50/dct-tracker.json" \\
            "clients/neezanizam/campaigns/buyer-funnel/CBO_Test_BuyerFunnel_Apr26/W1_DCT2_Broad_LifeTransition_PricedOut_50/dct-tracker.json" \\
        --mode preview

    # After reviewing the preview, re-run with --mode write.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from modal.sheets_writer import SheetsWriter  # noqa: E402


SGT = ZoneInfo("Asia/Singapore")
REPO_ROOT = Path(__file__).resolve().parent.parent
CREDENTIALS_PATH = REPO_ROOT / "scripts" / "modal" / "credentials.json"


def load_metrics_config(client_slug: str) -> dict:
    path = REPO_ROOT / "clients" / client_slug / "metrics-config.json"
    if not path.exists():
        raise SystemExit(f"metrics-config.json not found for client: {path}")
    return json.loads(path.read_text())


def pick_campaign_config(metrics_cfg: dict, name: str) -> dict:
    campaigns = metrics_cfg.get("campaigns", [])
    for c in campaigns:
        if c.get("campaign_slug") == name:
            return c
    raise SystemExit(f"metrics-campaign '{name}' not found in metrics-config. Options: {[c.get('campaign_slug') for c in campaigns]}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Patch ANGLE column for existing CREATIVES rows.")
    ap.add_argument("--client", required=True)
    ap.add_argument("--metrics-campaign", required=True)
    ap.add_argument("--trackers", nargs="+", required=True, help="One or more dct-tracker.json paths")
    ap.add_argument("--mode", choices=["preview", "write"], default="preview")
    args = ap.parse_args()

    metrics_cfg = load_metrics_config(args.client)
    campaign_cfg = pick_campaign_config(metrics_cfg, args.metrics_campaign)
    # Top-level sheet_id is the authoritative location; campaign entry carries the tab schema.
    sheet_id = metrics_cfg.get("sheet_id") or campaign_cfg.get("sheet_id")
    if not sheet_id:
        raise SystemExit("sheet_id not found in metrics-config (top-level or campaign-level).")
    creatives_tab_cfg = campaign_cfg["tabs"]["creatives"]

    # Connect
    writer = SheetsWriter(service_account_path=str(CREDENTIALS_PATH))
    sheet = writer.get_sheet(sheet_id)
    creatives_tab = writer.get_tab(sheet, creatives_tab_cfg["gid"])

    # Validate header
    header = [h.strip() for h in creatives_tab.row_values(1)]
    if "BATCH" not in header:
        raise SystemExit(f"CREATIVES tab missing BATCH column. Header: {header}")
    if "ANGLE" not in header:
        raise SystemExit(f"CREATIVES tab missing ANGLE column. Header: {header}")
    batch_col_idx = header.index("BATCH") + 1  # 1-indexed
    angle_col_idx = header.index("ANGLE") + 1  # 1-indexed — column G if order is standard
    angle_col_letter = chr(ord("A") + angle_col_idx - 1)

    # Build patches: {batch_id: (row_num, new_value)}
    patches = []
    for tp in args.trackers:
        tp_path = Path(tp).resolve()
        if not tp_path.exists():
            raise SystemExit(f"tracker not found: {tp_path}")
        t = json.loads(tp_path.read_text())
        creatives = t.get("creatives", [])
        if not creatives:
            raise SystemExit(f"tracker has no creatives[]: {tp}")
        c = creatives[0]
        batch_id = c.get("batch")
        rationale = c.get("angle_rationale")
        if not batch_id:
            raise SystemExit(f"tracker creative has no batch: {tp}")
        if not rationale:
            raise SystemExit(f"tracker creative missing angle_rationale: {tp}. Run backfill_angle_rationale.py first.")
        patches.append({"batch_id": batch_id, "rationale": rationale, "tracker": str(tp_path)})

    # Look up row numbers
    batch_col_values = creatives_tab.col_values(batch_col_idx)
    for p in patches:
        row_num = None
        for idx, val in enumerate(batch_col_values, start=1):
            if (val or "").strip() == p["batch_id"]:
                row_num = idx
                break
        if row_num is None:
            raise SystemExit(f"batch '{p['batch_id']}' not found in CREATIVES column {batch_col_letter} (BATCH is col {chr(ord('A') + batch_col_idx - 1)})")
        p["row_num"] = row_num
        p["cell_addr"] = f"{angle_col_letter}{row_num}"
        # Read current value for preview
        p["current_value"] = creatives_tab.cell(row_num, angle_col_idx).value or ""

    # Preview
    print(f"\n# ANGLE Cell Patch — {args.client} / {args.metrics_campaign} — {datetime.now(SGT).strftime('%Y-%m-%d %H:%M SGT')}\n")
    print(f"**Sheet:** https://docs.google.com/spreadsheets/d/{sheet_id}/edit")
    print(f"**Tab:** CREATIVES (gid {creatives_tab_cfg.get('gid', 'unknown')})")
    print(f"**Column:** {angle_col_letter} (ANGLE, 1-indexed {angle_col_idx})\n")
    for p in patches:
        print(f"## {p['batch_id']} → row {p['row_num']}, cell {p['cell_addr']}")
        print(f"**Source tracker:** `{p['tracker']}`")
        print(f"**Current value** (len {len(p['current_value'])}):")
        print(f"> {p['current_value'][:200]}{'...' if len(p['current_value']) > 200 else ''}")
        print(f"\n**New value** (len {len(p['rationale'])}):")
        for line in p["rationale"].split("\n"):
            print(f"> {line}")
        print()

    if args.mode == "preview":
        print("---\nPreview only. Re-run with --mode write to apply.")
        return 0

    # Confirm
    resp = input("\nProceed with ANGLE cell writes? (type 'yes' to confirm): ").strip().lower()
    if resp != "yes":
        print("Aborted.")
        return 1

    # Pre-snapshot (Phase 5.2 ICM reorg: sheet-snapshots moved under campaigns/)
    snapshot_dir = REPO_ROOT / "clients" / args.client / "campaigns" / "sheet-snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(SGT).strftime("%y%m%d-%H%M")
    pre_path = snapshot_dir / f"{stamp}-pre-angle-patch.json"
    all_values = creatives_tab.get_all_values()
    pre_path.write_text(json.dumps({"tab_gid": creatives_tab_cfg["gid"], "rows": all_values}, indent=2))
    print(f"Pre-snapshot: {pre_path}")

    # Apply patches via batch_update
    batch = [
        {"range": p["cell_addr"], "values": [[p["rationale"]]]}
        for p in patches
    ]
    creatives_tab.batch_update(batch, value_input_option="USER_ENTERED")
    print(f"Patched {len(patches)} cells.")

    # Post-snapshot
    post_path = snapshot_dir / f"{stamp}-post-angle-patch.json"
    all_values_post = creatives_tab.get_all_values()
    post_path.write_text(json.dumps({"tab_gid": creatives_tab_cfg["gid"], "rows": all_values_post}, indent=2))
    print(f"Post-snapshot: {post_path}")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
