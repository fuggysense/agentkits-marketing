"""Source of Truth sheet writer — writes AVATARS tab only.

SCOPE (260417 correction — see skills/source-of-truth/corrections.md):
  - This writer owns the AVATARS tab ONLY.
  - CREATIVES + COPY tabs are OWNED by ad-concept-engine via a separate
    `scripts/ad_concept_sheet_writer.py` (not yet built).
  - Rule: source-of-truth owns STRATEGY (avatars, angles, messaging).
          ad-concept-engine owns EXECUTION (DCT tracker, creative specs, copy).
          They do not overlap.

Reads:
  - clients/<slug>/metrics-config.json  (sheet_id + avatars tab gid)
  - clients/<slug>/source-of-truth-draft.json  (avatars array)

Takes a pre-write snapshot of the AVATARS tab, surfaces a HITL preview,
then writes narrative-per-row to the AVATARS tab.

Usage
-----
    python3 scripts/source_of_truth_sheet_writer.py \\
        --client neezanizam \\
        --draft clients/neezanizam/source-of-truth-draft.json \\
        --mode preview

    python3 scripts/source_of_truth_sheet_writer.py \\
        --client neezanizam \\
        --draft clients/neezanizam/source-of-truth-draft.json \\
        --mode write

Draft JSON shape expected
-------------------------
{
  "avatars": [
    {"name": "Avatar 1: The Hesitant Calculator",
     "narrative": "<full markdown>"},
    ...
  ]
}
Other keys in the draft JSON (hitl_decisions, research findings, etc.) are
permitted and ignored by this writer.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from modal.sheets_writer import SheetsWriter  # noqa: E402


SGT = ZoneInfo("Asia/Singapore")
REPO_ROOT = Path(__file__).resolve().parent.parent
CREDENTIALS_PATH = REPO_ROOT / "scripts" / "modal" / "credentials.json"


class SourceOfTruthSheetWriter:
    def __init__(self, client_slug: str, draft_path: Path, metrics_campaign: str = "default"):
        self.client_slug = client_slug
        self.draft_path = draft_path
        self.metrics_campaign = metrics_campaign
        self.client_dir = REPO_ROOT / "clients" / client_slug

        self.config = self._load_config()
        self.draft = self._load_draft()
        self.writer = SheetsWriter(service_account_path=str(CREDENTIALS_PATH))
        self.sheet = self.writer.get_sheet(self.config["sheet_id"])

        self._validate_tabs()

    # ── Setup ───────────────────────────────────────────────────────────────

    def _load_config(self) -> dict:
        config_path = self.client_dir / "metrics-config.json"
        if not config_path.exists():
            raise FileNotFoundError(
                f"No metrics-config.json at {config_path}. "
                "Run /sheets:provision for this client before writing source-of-truth."
            )
        raw = json.loads(config_path.read_text())
        # 260419: configs evolved to use campaigns[]; flatten the requested
        # metrics-campaign so downstream code keeps working with self.config["sheet_id"] / ["tabs"].
        # If metrics_campaign is None (no --metrics-campaign flag passed), use campaigns[0]
        # so swapping campaign array order is a valid way to set the default per-client.
        if "sheet_id" not in raw and "campaigns" in raw and raw["campaigns"]:
            if self.metrics_campaign is None:
                campaign = raw["campaigns"][0]
            else:
                campaign = next(
                    (c for c in raw["campaigns"] if c.get("campaign_slug") == self.metrics_campaign),
                    None,
                )
                if not campaign:
                    slugs = [c.get("campaign_slug") for c in raw["campaigns"]]
                    raise ValueError(
                        f"--metrics-campaign '{self.metrics_campaign}' not found. Available: {slugs}"
                    )
            return {**raw, **campaign}
        return raw

    def _load_draft(self) -> dict:
        if not self.draft_path.exists():
            raise FileNotFoundError(f"Draft JSON not found: {self.draft_path}")
        draft = json.loads(self.draft_path.read_text())
        if "avatars" not in draft:
            raise ValueError(
                "Draft JSON missing required 'avatars' key. "
                "Other strategy keys (hitl_decisions, research_refresh_findings_260417) are optional."
            )
        if not isinstance(draft["avatars"], list) or not draft["avatars"]:
            raise ValueError("Draft JSON 'avatars' must be a non-empty list.")
        return draft

    def _validate_tabs(self) -> None:
        if "avatars" not in self.config["tabs"]:
            raise ValueError(
                "metrics-config.json missing required 'avatars' tab. "
                "This writer only touches the AVATARS tab. "
                "CREATIVES and COPY tabs are owned by ad-concept-engine."
            )

    # ── Preview ─────────────────────────────────────────────────────────────

    def build_preview(self) -> str:
        today = datetime.now(SGT).strftime("%Y-%m-%d")
        avatars_cfg = self.config["tabs"]["avatars"]

        lines = [
            f"# Sheet Write Preview — {self.client_slug} — {today}",
            "",
            f"Target sheet: {self.config['sheet_url']}",
            "",
            f"**Writer scope:** AVATARS tab ONLY. "
            "CREATIVES + COPY tabs belong to ad-concept-engine (separate writer).",
            "",
            f"## AVATARS tab (gid {avatars_cfg['gid']})",
            f"Will **replace** existing content with {len(self.draft['avatars'])} rows.",
            "",
        ]
        for avatar in self.draft["avatars"]:
            preview = (avatar["narrative"] or "").replace("\n", " ")[:120]
            lines.append(f"  - **{avatar['name']}** — {preview}...")

        lines += [
            "",
            "---",
            "",
            "Proceed with AVATARS tab write? (type 'yes' to confirm)",
        ]
        return "\n".join(lines)

    # ── Snapshot (pre-write safety) ─────────────────────────────────────────

    def take_snapshot(self) -> Path:
        snapshot_dir = self.client_dir / "sheet-snapshots"
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(SGT).strftime("%y%m%d-%H%M")
        snapshot_path = snapshot_dir / f"{stamp}-pre-sot-avatars-write.json"

        snapshot: dict[str, Any] = {
            "taken_at": datetime.now(SGT).isoformat(),
            "scope": "avatars_only",
            "tabs": {},
        }
        tab = self.writer.get_tab(self.sheet, self.config["tabs"]["avatars"]["gid"])
        snapshot["tabs"]["avatars"] = {
            "gid": self.config["tabs"]["avatars"]["gid"],
            "values": tab.get_all_values(),
        }
        snapshot_path.write_text(json.dumps(snapshot, indent=2))
        return snapshot_path

    # ── Writes (AVATARS ONLY) ───────────────────────────────────────────────

    def write_avatars(self) -> int:
        tab = self.writer.get_tab(self.sheet, self.config["tabs"]["avatars"]["gid"])
        tab.clear()
        tab.append_row(
            ["AVATAR", "NARRATIVE", "LAST UPDATED"],
            value_input_option="USER_ENTERED",
        )
        today = datetime.now(SGT).strftime("%Y-%m-%d")
        for avatar in self.draft["avatars"]:
            tab.append_row(
                [avatar["name"], avatar["narrative"], today],
                value_input_option="USER_ENTERED",
            )
        return len(self.draft["avatars"])

    def run_write(self) -> dict:
        snapshot_path = self.take_snapshot()
        avatars_n = self.write_avatars()
        return {
            "snapshot": str(snapshot_path),
            "avatars_written": avatars_n,
            "written_at": datetime.now(SGT).isoformat(),
            "not_written": (
                "CREATIVES + COPY tabs — those are ad-concept-engine's scope. "
                "Run scripts/ad_concept_sheet_writer.py (not yet built) "
                "after /ads:concepts generates dct-tracker.json."
            ),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--client", required=True, help="Client slug (e.g. neezanizam)")
    parser.add_argument("--draft", required=True, help="Path to source-of-truth draft JSON")
    parser.add_argument(
        "--mode",
        choices=["preview", "write"],
        default="preview",
        help="preview = print preview only; write = take snapshot + write AVATARS tab",
    )
    parser.add_argument(
        "--metrics-campaign",
        default=None,
        help="Which metrics-config.json campaign to write to. If omitted, uses campaigns[0] (first in array — swap order in metrics-config.json to change the per-client default).",
    )
    args = parser.parse_args()

    writer = SourceOfTruthSheetWriter(
        args.client, Path(args.draft), metrics_campaign=args.metrics_campaign
    )

    if args.mode == "preview":
        print(writer.build_preview())
        return

    print(writer.build_preview())
    print()
    confirm = input("Proceed with AVATARS tab write? (type 'yes' to confirm): ").strip().lower()
    if confirm != "yes":
        print("Aborted. No sheet changes made.")
        return

    result = writer.run_write()
    print("\n✓ AVATARS tab write complete:")
    print(f"  AVATARS: {result['avatars_written']} rows")
    print(f"  Pre-write snapshot: {result['snapshot']}")
    print(f"\nNot written by this script: {result['not_written']}")


if __name__ == "__main__":
    main()
