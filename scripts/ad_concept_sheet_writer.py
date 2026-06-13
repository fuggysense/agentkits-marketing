"""Ad Concept sheet writer — writes CREATIVES + COPY tabs for any client.

Owner: ad-concept-engine skill.

Scope (260417 boundary):
  - This writer owns the CREATIVES and COPY tabs.
  - AVATARS tab is OWNED by source-of-truth via `scripts/source_of_truth_sheet_writer.py`.
  - Metric columns (STATUS, CTR, CVR, CPA, CALLS, SPEND, DURATION) are OWNED by
    sheets-updater / meta_puller — this writer NEVER touches them.
  - Strategy columns (BATCH, FORMAT, AD, MARKET AWARENESS, MARKET SOPHISTICATION,
    ANGLE, PERSONA, CANVA LINK) are this writer's responsibility.

Reads:
  - clients/<slug>/metrics-config.json  (sheet_id + tabs schema)
  - clients/<slug>/campaigns/<campaign>/dct-tracker.json  (creative specs)

Writes:
  - CREATIVES tab: one row per batch with strategy columns filled, metric columns
    left blank (meta_puller fills them later).
  - COPY tab: one row per batch with STATUS=DRAFT + headlines + copies.

Safety:
  - HITL preview before every write.
  - Pre-write snapshot of both tabs saved to clients/<slug>/sheet-snapshots/.
  - Refuses to overwrite existing batch rows (use --overwrite to force).
  - Refuses to touch protected / metric columns even if forced.

Usage
-----
    # Preview for a specific client + campaign + batch list
    python3 scripts/ad_concept_sheet_writer.py \\
        --client neezanizam \\
        --campaign dct-260417 \\
        --batches DCT001 \\
        --mode preview

    # Write after approval
    python3 scripts/ad_concept_sheet_writer.py \\
        --client neezanizam \\
        --campaign dct-260417 \\
        --batches DCT001 \\
        --mode write

    # All batches in a campaign
    python3 scripts/ad_concept_sheet_writer.py \\
        --client neezanizam \\
        --campaign dct-260417 \\
        --mode preview

    # Dry-run — shows what would be written without any sheet read/write
    python3 scripts/ad_concept_sheet_writer.py \\
        --client neezanizam \\
        --campaign dct-260417 \\
        --mode dry-run

Prerequisites per client
------------------------
1. The service account (see scripts/modal/credentials.json `client_email`) must
   have Editor access on the client's Google Sheet.
2. clients/<slug>/metrics-config.json must have both `creatives` and `copy` tab
   entries with correct gid values.
3. The CREATIVES tab header row must contain columns for: BATCH, STATUS, FORMAT,
   AD, MARKET AWARENESS, MARKET SOPHISTICATION, ANGLE, PERSONA. CANVA LINK is
   optional — written only if the header contains it.
4. The COPY tab header row must contain: STATUS, COPY 1, COPY 2, HEADLINE 1,
   HEADLINE 2. (BATCH column is optional — written if present to key rows.)
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
# NOTE: `from modal.sheets_writer import SheetsWriter` is imported lazily inside
# __init__ (only when NOT dry-run) so that --mode dry-run runs with zero network
# dependencies (gspread/google-auth need not be installed to validate a tracker).


SGT = ZoneInfo("Asia/Singapore")
REPO_ROOT = Path(__file__).resolve().parent.parent
CREDENTIALS_PATH = REPO_ROOT / "scripts" / "modal" / "credentials.json"

# Columns this writer is allowed to write to in CREATIVES
CREATIVES_STRATEGY_COLUMNS = [
    "BATCH",
    "FORMAT",
    "AD",
    "MARKET AWARENESS",
    "MARKET SOPHISTICATION",
    "ANGLE",
    "PERSONA",
    "CANVA LINK",
]

# Columns this writer MUST NEVER overwrite in CREATIVES
CREATIVES_METRIC_COLUMNS = [
    "STATUS",
    "CTR",
    "CVR",
    "CPA",
    "CALLS",
    "SPEND",
    "DURATION",
]

# Required columns in COPY tab (will error if missing from header)
COPY_REQUIRED_COLUMNS = [
    "STATUS",
    "COPY 1",
    "COPY 2",
    "HEADLINE 1",
    "HEADLINE 2",
]


class AdConceptSheetWriter:
    def __init__(
        self,
        client_slug: str,
        campaign_slug: str | None = None,
        batch_filter: list[str] | None = None,
        overwrite: bool = False,
        dry_run: bool = False,
        metrics_campaign: str = "default",
        wave: int | None = None,
        dct: int | None = None,
        campaign_path: str | None = None,
        allow_missing_canva: bool = False,
    ):
        self.client_slug = client_slug
        self.campaign_slug = campaign_slug
        self.batch_filter = set(batch_filter) if batch_filter else None
        self.overwrite = overwrite
        self.dry_run = dry_run
        self.metrics_campaign = metrics_campaign
        self.wave = wave
        self.dct = dct
        self.campaign_path = campaign_path
        self.allow_missing_canva = allow_missing_canva

        self.client_dir = REPO_ROOT / "clients" / client_slug
        self.campaign_dir = self._resolve_campaign_dir()
        # Preserve a display slug for logs/preview even when we resolved via --wave/--dct.
        if not self.campaign_slug:
            self.campaign_slug = self.campaign_dir.name

        self.config = self._load_config()
        self.tracker = self._load_tracker()
        self.batches = self._select_batches()
        self._validate_canva_links()

        if not self.dry_run:
            from modal.sheets_writer import SheetsWriter  # lazy: avoids gspread import in dry-run

            self.writer = SheetsWriter(service_account_path=str(CREDENTIALS_PATH))
            self.sheet = self.writer.get_sheet(self.config["sheet_id"])
            self.creatives_tab = self.writer.get_tab(
                self.sheet, self.config["tabs"]["creatives"]["gid"]
            )
            self.copy_tab = self.writer.get_tab(
                self.sheet, self.config["tabs"]["copy"]["gid"]
            )
            self._validate_headers()
        else:
            self.writer = None
            self.sheet = None
            self.creatives_tab = None
            self.copy_tab = None

    # ── Setup ───────────────────────────────────────────────────────────────

    def _resolve_campaign_dir(self) -> Path:
        """Resolve the campaign folder where dct-tracker.json lives.

        Three accepted input modes (one of them is required):

        1. ``--campaign-path <relative-path>`` — full relative path under the client
           folder, e.g.::

               buyer-funnel/CBO_Test_BuyerFunnel_Apr26/W1_DCT2_Broad_LifeTransition_PricedOut_50

           Resolved as ``<client_dir>/campaigns/<campaign_path>``. Escape hatch when
           the auto-resolution cannot guess the Meta Campaign folder.

        2. ``--wave <N> --dct <N>`` (+ ``--metrics-campaign <funnel>``) — auto-resolve
           to the new nested Meta hierarchy::

               <client_dir>/campaigns/<metrics-campaign>/<meta-campaign>/W<N>_DCT<N>_*/

           Scans the metrics-campaign folder for exactly ONE Meta Campaign subfolder
           and ONE matching W<N>_DCT<N>_* Ad Set folder. Errors if ambiguous.

        3. ``--campaign <slug>`` — legacy flat path ``<client_dir>/campaigns/<slug>/``.
           Kept for backward compat with the pre-restructure layout (dct-260417 etc).
        """
        # Mode 1 — explicit full path override
        if self.campaign_path:
            path = self.client_dir / "campaigns" / self.campaign_path
            if not path.exists():
                raise FileNotFoundError(
                    f"--campaign-path resolved to {path} but it does not exist."
                )
            return path

        # Mode 2 — auto-resolve from wave + dct
        if self.wave is not None and self.dct is not None:
            if not self.metrics_campaign:
                raise ValueError(
                    "--wave/--dct requires --metrics-campaign (the nested path is "
                    "clients/<slug>/campaigns/<metrics-campaign>/<meta-campaign>/W<N>_DCT<N>_*)."
                )
            metrics_dir = self.client_dir / "campaigns" / self.metrics_campaign
            if not metrics_dir.exists():
                raise FileNotFoundError(
                    f"Metrics-campaign folder not found: {metrics_dir}. "
                    f"Create it and the Meta Campaign subfolder first."
                )
            meta_campaign_dirs = sorted(
                [d for d in metrics_dir.iterdir() if d.is_dir() and not d.name.startswith(".")],
                key=lambda d: d.stat().st_mtime,
                reverse=True,
            )
            if not meta_campaign_dirs:
                raise FileNotFoundError(
                    f"No Meta Campaign subfolders under {metrics_dir}. "
                    f"Expected a folder like CBO_Test_BuyerFunnel_Apr26/ here."
                )
            if len(meta_campaign_dirs) > 1:
                names = [d.name for d in meta_campaign_dirs]
                raise ValueError(
                    f"Multiple Meta Campaign folders under {metrics_dir}: {names}. "
                    f"Use --campaign-path to disambiguate which one to write against."
                )
            meta_campaign_dir = meta_campaign_dirs[0]
            pattern = f"W{self.wave}_DCT{self.dct}_*"
            matches = list(meta_campaign_dir.glob(pattern))
            if not matches:
                raise FileNotFoundError(
                    f"No Ad Set folder matching '{pattern}' under {meta_campaign_dir}. "
                    f"Expected a folder like W1_DCT2_Broad_LifeTransition_PricedOut_50/."
                )
            if len(matches) > 1:
                names = [m.name for m in matches]
                raise ValueError(
                    f"Multiple Ad Set folders match '{pattern}' under {meta_campaign_dir}: {names}. "
                    f"Ad Set names must be unique per (wave, dct) pair."
                )
            return matches[0]

        # Mode 3 — legacy flat slug
        if self.campaign_slug:
            return self.client_dir / "campaigns" / self.campaign_slug

        raise ValueError(
            "Must provide ONE of: --campaign <slug> (legacy), "
            "--campaign-path <relative-path> (escape hatch), "
            "or (--wave <N> AND --dct <N>) (new hierarchy, recommended)."
        )

    def _load_config(self) -> dict:
        # Config location drifted across the 260504 ICM reorg: older clients keep it at
        # the client root (hazecraft), reorganised clients moved it under _brand/
        # (neezanizam, eugene-chieng, harmony-wellness). Check root first (back-compat),
        # then _brand/. First hit wins.
        candidate_paths = [
            self.client_dir / "metrics-config.json",
            self.client_dir / "_brand" / "metrics-config.json",
        ]
        config_path = next((p for p in candidate_paths if p.exists()), None)
        if config_path is None:
            searched = " or ".join(str(p) for p in candidate_paths)
            raise FileNotFoundError(
                f"No metrics-config.json found (looked in: {searched}). "
                f"Run /sheets:provision for client '{self.client_slug}' before writing."
            )
        raw = json.loads(config_path.read_text())
        # 260419: configs evolved to use campaigns[]; flatten the requested
        # metrics-campaign so downstream code keeps working with self.config["sheet_id"] / ["tabs"].
        # 260420: if metrics_campaign is None (no flag passed), use campaigns[0] so
        # array-order in metrics-config.json controls the per-client default.
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
                        f"--metrics-campaign '{self.metrics_campaign}' not found. "
                        f"Available: {slugs}"
                    )
            config = {**raw, **campaign}
        else:
            config = raw
        tabs = config.get("tabs", {})
        missing = [t for t in ("creatives", "copy") if t not in tabs]
        if missing:
            raise ValueError(
                f"metrics-config.json for '{self.client_slug}' missing required tab entries: {missing}. "
                "This writer needs both 'creatives' and 'copy' tab definitions."
            )
        return config

    def _load_tracker(self) -> dict:
        # dct.json (current 10-5-5 shape, docs/dct-json-schema.md) wins when present;
        # legacy dct-tracker.json stays the path for 3-2-2 workspaces (byte-identical
        # behavior when no dct.json exists).
        dct_path = self.campaign_dir / "dct.json"
        if dct_path.exists():
            data = json.loads(dct_path.read_text())
            if isinstance(data.get("angles"), list) and data.get("dct_method") == "10-5-5":
                return self._adapt_dct_json(data, dct_path)
            raise ValueError(
                f"{dct_path} exists but is not a valid 10-5-5 dct.json "
                "(need angles[] + dct_method='10-5-5'). Fix the file or remove it "
                "to fall back to dct-tracker.json."
            )
        tracker_path = self.campaign_dir / "dct-tracker.json"
        if not tracker_path.exists():
            raise FileNotFoundError(
                f"No dct.json or dct-tracker.json at {self.campaign_dir}. "
                f"Run /ads:concepts for client '{self.client_slug}' campaign '{self.campaign_slug}' first."
            )
        tracker = json.loads(tracker_path.read_text())
        if "creatives" not in tracker or not isinstance(tracker["creatives"], list):
            raise ValueError(
                f"dct-tracker.json missing required 'creatives' array at {tracker_path}."
            )
        return tracker

    @staticmethod
    def _adapt_dct_json(data: dict, path: Path) -> dict:
        """Map a dct.json (angles[] shape) onto the legacy creatives[] batch shape.

        One row per angle (5/wave). batch id = '<dct_id>-<angle_id>' (e.g. DCT010-A01).
        copy_2/headline_2 stay empty — 10-5-5 carries 1 copy + 1 headline per angle.
        """
        dct_id = data.get("dct_id", "")
        if not dct_id:
            raise ValueError(f"{path} missing dct_id.")
        # 10-5-5 Canva is ONE shared design per wave (canva_push.py imports all
        # renders as pages of a single design and writes a TOP-LEVEL canva_link).
        # There is no per-angle link in this model, so every angle-row carries the
        # wave's shared link. A per-angle canva_link still wins if one ever lands.
        wave_canva_link = data.get("canva_link", "")
        creatives = []
        for a in data["angles"]:
            creatives.append({
                "batch": f"{dct_id}-{a.get('id', '')}",
                "ad_name": a.get("ad_name", ""),
                "angle": a.get("name", ""),
                "angle_rationale": a.get("angle_rationale", ""),
                "copy_1": a.get("primary_text", ""),
                "copy_2": "",
                "headline_1": a.get("headline", ""),
                "headline_2": "",
                "headline_drafts": a.get("headline_drafts", []),
                "market_awareness": a.get("market_awareness", ""),
                "market_sophistication": a.get("market_sophistication", ""),
                "persona": data.get("avatar", ""),
                "format": a.get("format", ""),
                "status": a.get("status", "DRAFT"),
                "why_am_i_testing_this": a.get("why_am_i_testing_this", ""),
                "canva_link": a.get("canva_link") or wave_canva_link,
            })
        return {
            "creatives": creatives,
            "dct_structure": {"method": "10-5-5"},
            "_source": str(path),
        }

    def _select_batches(self) -> list[dict]:
        all_batches = self.tracker["creatives"]
        if self.batch_filter is None:
            return all_batches
        selected = [b for b in all_batches if b.get("batch") in self.batch_filter]
        if not selected:
            raise ValueError(
                f"No batches in tracker matched filter {sorted(self.batch_filter)}. "
                f"Available batches: {[b.get('batch') for b in all_batches]}"
            )
        missing_from_filter = self.batch_filter - {b.get("batch") for b in selected}
        if missing_from_filter:
            raise ValueError(
                f"Filter included batches not found in tracker: {sorted(missing_from_filter)}"
            )
        return selected

    def _validate_canva_links(self) -> None:
        """Refuse to write if any batch has a missing / empty / "TBD" canva_link.

        Locked 260421 after DCT3 shipped to neezanizam sheet with CANVA LINK="TBD"
        and required a surgical cell patch. Canonical workflow: create the Canva
        design FIRST, populate tracker, THEN write to sheet. Never ship a
        placeholder to column J.

        Run `python3 scripts/create_canva_design.py --client <c> --campaign <c>`
        to auto-create a design via the `one` CLI + patch every canva_link field
        in the tracker in one shot, then re-run this writer.
        """
        # Test-tab-only bypass: --allow-missing-canva skips the no-TBD gate, but ONLY when
        # BOTH target tabs are TEST tabs (name contains "TEST"). Keeps the 260421
        # no-placeholder-to-live rule intact for real tabs while letting a 10-5-5 SHAPE
        # proof land in throwaway TEST tabs with canva_link deliberately empty.
        if self.allow_missing_canva:
            tab_names = [
                str(self.config.get("tabs", {}).get("creatives", {}).get("name", "")),
                str(self.config.get("tabs", {}).get("copy", {}).get("name", "")),
            ]
            if not all("TEST" in n.upper() for n in tab_names):
                raise SystemExit(
                    "--allow-missing-canva is permitted ONLY when BOTH target tabs are TEST "
                    f"tabs (name contains 'TEST'). Got tab names: {tab_names}. Refusing to "
                    "bypass the canva gate on non-test tabs (260421 no-TBD rule)."
                )
            print(
                "⚠️  CANVA GATE BYPASSED (--allow-missing-canva) — TEST tabs only. "
                "canva_link written EMPTY. Never use on live tabs."
            )
            return
        PLACEHOLDER_TOKENS = {"", "tbd", "todo", "pending", "none", "null"}
        bad = []
        for b in self.batches:
            link = (b.get("canva_link") or "").strip()
            if link.lower() in PLACEHOLDER_TOKENS:
                bad.append((b.get("batch", "<no-batch>"), link or "<missing>"))
        if bad:
            details = "\n".join(f"    - {batch}: {val!r}" for batch, val in bad)
            is_10_5_5 = (self.tracker.get("dct_structure") or {}).get("method") == "10-5-5"
            if is_10_5_5:
                # dct.json (10-5-5) Canva = ONE shared design per wave. canva_push.py
                # imports the rendered PNGs as pages of a single design and writes the
                # top-level canva_link the adapter shares across all angle-rows.
                dct_json = self.campaign_dir / "dct.json"
                fix = (
                    "Canonical fix for 10-5-5 (one command):\n"
                    f"    python3 scripts/canva_push.py --dct {dct_json}\n\n"
                    "This stitches the wave's rendered images into one PDF, imports it to\n"
                    "Canva as a single multi-page design, and writes the top-level\n"
                    "canva_link into dct.json (shared by every angle-row). Requires the\n"
                    "images to be rendered first (phase_3). Re-run this writer after."
                )
            else:
                fix = (
                    "Canonical fix (one command):\n"
                    f"    python3 scripts/create_canva_design.py \\\n"
                    f"        --client {self.client_slug} \\\n"
                    f"        --campaign {self.campaign_slug or '<slug>'}\n\n"
                    "This creates the Canva design via `one` CLI, writes the real URL into\n"
                    "creatives[0].canva_link + every visual_variants[].canva_link + the matching\n"
                    "canva_design_id fields, then you re-run this writer."
                )
            raise SystemExit(
                "Refusing to write — one or more batches have a placeholder canva_link:\n"
                f"{details}\n\n"
                f"{fix}\n\n"
                "Never ship 'TBD' to column J — see clients/neezanizam/learnings.md "
                "'Mistakes Not to Repeat'."
            )

    def _validate_headers(self) -> None:
        """Verify required columns exist in both tab headers before any write."""
        cr_header = [h.strip() for h in self.creatives_tab.row_values(1)]
        required_cr = [
            "BATCH", "FORMAT", "AD", "MARKET AWARENESS",
            "MARKET SOPHISTICATION", "ANGLE", "PERSONA",
        ]
        missing_cr = [c for c in required_cr if c not in cr_header]
        if missing_cr:
            raise ValueError(
                f"CREATIVES tab header missing required columns: {missing_cr}. "
                f"Current header: {cr_header}. "
                "Fix the sheet column headers before writing."
            )
        self._canva_link_in_sheet = "CANVA LINK" in cr_header

        cp_header = [h.strip() for h in self.copy_tab.row_values(1)]
        missing_cp = [c for c in COPY_REQUIRED_COLUMNS if c not in cp_header]
        if missing_cp:
            raise ValueError(
                f"COPY tab header missing required columns: {missing_cp}. "
                f"Current header: {cp_header}. "
                "Fix the sheet column headers before writing."
            )
        self._copy_has_batch_column = "BATCH" in cp_header
        self._creatives_header = cr_header
        self._copy_header = cp_header

    # ── Row builders ────────────────────────────────────────────────────────

    def _build_creatives_row(self, batch: dict) -> dict:
        """Map a tracker batch to a dict keyed by CREATIVES column name.

        Only strategy columns are filled. Metric columns are intentionally left
        absent — meta_puller will populate them later.

        Optional columns written only if the sheet header contains them:
          - CANVA LINK            ← batch.canva_link
          - Why am I testing this? ← batch.why_am_i_testing_this
        """
        # ANGLE column prefers the 3-paragraph strategic rationale (big-angle-spotter
        # step 07b output) when present. Falls back to the short angle title for
        # legacy trackers that pre-date the 07b step.
        angle_value = batch.get("angle_rationale") or batch.get("angle", "")
        row = {
            "BATCH": batch.get("batch", ""),
            "FORMAT": batch.get("format", ""),
            "AD": batch.get("ad_name", ""),
            "MARKET AWARENESS": batch.get("market_awareness", ""),
            "MARKET SOPHISTICATION": batch.get("market_sophistication", ""),
            "ANGLE": angle_value,
            "PERSONA": batch.get("persona", ""),
        }
        canva_link = batch.get("canva_link")
        if canva_link:
            row["CANVA LINK"] = canva_link
        rationale = batch.get("why_am_i_testing_this")
        if rationale:
            row["Why am I testing this?"] = rationale
        return row

    def _build_copy_row(self, batch: dict) -> dict:
        row = {
            "STATUS": batch.get("status", "DRAFT"),
            "COPY 1": batch.get("copy_1", ""),
            "COPY 2": batch.get("copy_2", ""),
            "HEADLINE 1": batch.get("headline_1", ""),
            "HEADLINE 2": batch.get("headline_2", ""),
        }
        if getattr(self, "_copy_has_batch_column", False):
            row["BATCH"] = batch.get("batch", "")
        return row

    # ── Duplicate detection ─────────────────────────────────────────────────

    def _find_existing_creatives_rows(self) -> dict[str, int]:
        """Return {batch_id: row_num} for batches already present in CREATIVES."""
        col_values = self.creatives_tab.col_values(1)  # BATCH is column A
        existing = {}
        for idx, val in enumerate(col_values, start=1):
            batch_id = (val or "").strip()
            if batch_id and batch_id in {b.get("batch") for b in self.batches}:
                existing[batch_id] = idx
        return existing

    # ── Preview ─────────────────────────────────────────────────────────────

    def build_preview(self) -> str:
        today = datetime.now(SGT).strftime("%Y-%m-%d")
        cr_cfg = self.config["tabs"]["creatives"]
        cp_cfg = self.config["tabs"]["copy"]
        # Method is documentation-only here: 10-5-5 trackers carry 1 copy + 1 headline
        # per angle (copy_2/headline_2 empty), so the COPY preview hides the empty 2nd
        # slots. Absent dct_structure.method, behaves exactly as before (3-2-2).
        method = (self.tracker.get("dct_structure") or {}).get("method", "3-2-2")

        lines = [
            f"# Sheet Write Preview — {self.client_slug} / {self.campaign_slug} — {today}",
            "",
            f"**Target sheet:** {self.config.get('sheet_url', self.config['sheet_id'])}",
            f"**Method:** {method}"
            + ("  ·  5 angles × 2 variations → 5 rows (1 copy + 1 headline each)" if method == "10-5-5" else ""),
            f"**Batches to write:** {len(self.batches)} → {[b.get('batch') for b in self.batches]}",
            f"**Service account (must have Editor):** see scripts/modal/credentials.json `client_email`",
            "",
            "**Writer scope:** CREATIVES + COPY tabs only. "
            "AVATARS tab is source-of-truth's. Metric columns are meta_puller's — never touched here.",
            "",
        ]

        if self.dry_run:
            lines += ["**MODE: dry-run** — no sheet read/write performed. Showing planned payload only.", ""]
        else:
            existing = self._find_existing_creatives_rows()
            if existing:
                lines += [
                    f"⚠️  **{len(existing)} batch(es) already exist in CREATIVES:** {list(existing.keys())}",
                    f"    Overwrite mode: {'ON' if self.overwrite else 'OFF (will refuse to write duplicates)'}",
                    "",
                ]

        lines += [
            f"## CREATIVES tab (gid {cr_cfg['gid']})",
            f"Will **append** {len(self.batches)} row(s). Strategy columns only — metric columns left blank.",
            "",
        ]
        for b in self.batches:
            row = self._build_creatives_row(b)
            lines.append(f"  **{row.get('BATCH')}** — {row.get('FORMAT')} — {row.get('AD')[:80]}")
            lines.append(f"     Angle: {row.get('ANGLE')} · Persona: {row.get('PERSONA')}")
            lines.append(f"     Awareness: {row.get('MARKET AWARENESS')} · Soph: {row.get('MARKET SOPHISTICATION')}")
            if "CANVA LINK" in row:
                lines.append(f"     Canva: {row['CANVA LINK']}")
            else:
                canva_note = "(CANVA LINK empty — user fills after Canva doc built)"
                lines.append(f"     Canva: {canva_note}")
            lines.append("")

        lines += [
            f"## COPY tab (gid {cp_cfg['gid']})",
            f"Will **append** {len(self.batches)} row(s). STATUS=DRAFT.",
            "",
        ]
        for b in self.batches:
            row = self._build_copy_row(b)
            batch_id = b.get("batch", "")
            lines.append(f"  **{batch_id}** · {row.get('STATUS')}")
            lines.append(f"     H1: {row.get('HEADLINE 1')}")
            if method != "10-5-5":
                lines.append(f"     H2: {row.get('HEADLINE 2')}")
            lines.append(f"     Copy1: {row.get('COPY 1', '')[:100]}...")
            if method != "10-5-5":
                lines.append(f"     Copy2: {row.get('COPY 2', '')[:100]}...")
            lines.append("")

        lines += [
            "---",
            "",
            "Proceed with CREATIVES + COPY tab writes? (type 'yes' to confirm)",
        ]
        return "\n".join(lines)

    # ── Snapshot ────────────────────────────────────────────────────────────

    def take_snapshot(self, stage: str = "pre") -> Path:
        snapshot_dir = self.client_dir / "sheet-snapshots"
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(SGT).strftime("%y%m%d-%H%M")
        filename = f"{stamp}-{stage}-ad-concept-write-{self.campaign_slug}.json"
        snapshot_path = snapshot_dir / filename

        snapshot: dict[str, Any] = {
            "taken_at": datetime.now(SGT).isoformat(),
            "stage": stage,
            "client": self.client_slug,
            "campaign": self.campaign_slug,
            "batches_in_scope": [b.get("batch") for b in self.batches],
            "tabs": {
                "creatives": {
                    "gid": self.config["tabs"]["creatives"]["gid"],
                    "values": self.creatives_tab.get_all_values(),
                },
                "copy": {
                    "gid": self.config["tabs"]["copy"]["gid"],
                    "values": self.copy_tab.get_all_values(),
                },
            },
        }
        snapshot_path.write_text(json.dumps(snapshot, indent=2))
        return snapshot_path

    # ── Write ───────────────────────────────────────────────────────────────

    def _append_to_tab(self, tab, row_dict: dict, header: list[str]) -> None:
        values = [row_dict.get(col, "") for col in header]
        tab.append_row(values, value_input_option="USER_ENTERED")

    def _check_no_protected_write(self, row_dict: dict, forbidden: list[str]) -> None:
        collisions = set(row_dict.keys()) & set(forbidden)
        if collisions:
            raise RuntimeError(
                f"Refusing to write to protected/metric columns: {sorted(collisions)}. "
                "This is a safety violation — fix the row builder."
            )

    def write(self) -> dict:
        if self.dry_run:
            raise RuntimeError("Cannot call write() in dry-run mode.")

        existing = self._find_existing_creatives_rows()
        if existing and not self.overwrite:
            raise RuntimeError(
                f"Batches already exist in CREATIVES: {list(existing.keys())}. "
                "Re-run with --overwrite to force (not yet implemented — manual delete required for now)."
            )

        pre_snapshot = self.take_snapshot(stage="pre")

        creatives_written = 0
        copy_written = 0

        for batch in self.batches:
            cr_row = self._build_creatives_row(batch)
            self._check_no_protected_write(cr_row, CREATIVES_METRIC_COLUMNS)
            # Strip CANVA LINK if sheet header doesn't have it
            if not self._canva_link_in_sheet:
                cr_row.pop("CANVA LINK", None)
            self._append_to_tab(self.creatives_tab, cr_row, self._creatives_header)
            creatives_written += 1

            cp_row = self._build_copy_row(batch)
            self._append_to_tab(self.copy_tab, cp_row, self._copy_header)
            copy_written += 1

        post_snapshot = self.take_snapshot(stage="post")

        return {
            "pre_snapshot": str(pre_snapshot),
            "post_snapshot": str(post_snapshot),
            "creatives_rows_written": creatives_written,
            "copy_rows_written": copy_written,
            "batches": [b.get("batch") for b in self.batches],
            "written_at": datetime.now(SGT).isoformat(),
            "not_written": (
                "Metric columns (STATUS / CTR / CVR / CPA / CALLS / SPEND / DURATION) "
                "are meta_puller's scope. AVATARS tab is source-of-truth's scope."
            ),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--client", required=True, help="Client slug (e.g. neezanizam)")
    parser.add_argument(
        "--campaign",
        default=None,
        help=(
            "Legacy flat campaign slug (e.g. dct-260417). Resolves to "
            "clients/<slug>/campaigns/<campaign>/. Use this only for pre-restructure "
            "folders. Pre-Apr26 waves should migrate to --wave/--dct or --campaign-path."
        ),
    )
    parser.add_argument(
        "--wave",
        type=int,
        default=None,
        help=(
            "Wave number under the new Meta hierarchy. Combine with --dct + --metrics-campaign "
            "to auto-resolve the Ad Set folder: clients/<slug>/campaigns/<metrics-campaign>/"
            "<meta-campaign>/W<wave>_DCT<dct>_*/. Requires exactly ONE Meta Campaign folder "
            "under the metrics-campaign and exactly ONE matching Ad Set folder."
        ),
    )
    parser.add_argument(
        "--dct",
        type=int,
        default=None,
        help="DCT number (one angle = one DCT = one Ad Set). Pairs with --wave.",
    )
    parser.add_argument(
        "--campaign-path",
        default=None,
        help=(
            "Escape hatch: explicit relative path under clients/<slug>/campaigns/. "
            "Use when --wave/--dct can't auto-resolve (e.g. multiple Meta Campaigns exist "
            "under the same metrics-campaign). Example: "
            "buyer-funnel/CBO_Test_BuyerFunnel_Apr26/W1_DCT2_Broad_LifeTransition_PricedOut_50"
        ),
    )
    parser.add_argument(
        "--batches",
        default=None,
        help="Comma-separated batch ids to write (e.g. DCT001,DCT002). Default: all batches in tracker.",
    )
    parser.add_argument(
        "--mode",
        choices=["preview", "write", "dry-run"],
        default="preview",
        help="preview: print HITL preview (reads sheet). dry-run: print planned payload (no sheet read). write: snapshot + append.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Force write even if batch ids already exist in CREATIVES (NOT YET IMPLEMENTED — will raise).",
    )
    parser.add_argument(
        "--metrics-campaign",
        default=None,
        help="Which metrics-config.json campaign to write to. If omitted, uses campaigns[0] (first in array — swap order in metrics-config.json to change the per-client default).",
    )
    parser.add_argument(
        "--allow-missing-canva",
        action="store_true",
        help=(
            "TEST-TAB ONLY escape hatch: skip the no-placeholder canva_link gate so a "
            "10-5-5 shape proof can land with canva_link empty. Refuses unless BOTH target "
            "tabs are named *TEST*. Never use against live CREATIVES/COPY tabs."
        ),
    )
    args = parser.parse_args()

    # Exactly one of --campaign / --campaign-path / (--wave + --dct) must be provided.
    mode_flags = [
        bool(args.campaign),
        bool(args.campaign_path),
        bool(args.wave is not None and args.dct is not None),
    ]
    if sum(mode_flags) != 1:
        parser.error(
            "Must provide EXACTLY ONE of: --campaign <slug> (legacy), "
            "--campaign-path <relative-path> (escape hatch), "
            "or both --wave <N> --dct <N> (new hierarchy)."
        )

    batch_filter = None
    if args.batches:
        batch_filter = [b.strip() for b in args.batches.split(",") if b.strip()]

    writer = AdConceptSheetWriter(
        client_slug=args.client,
        campaign_slug=args.campaign,
        batch_filter=batch_filter,
        overwrite=args.overwrite,
        dry_run=(args.mode == "dry-run"),
        metrics_campaign=args.metrics_campaign,
        wave=args.wave,
        dct=args.dct,
        campaign_path=args.campaign_path,
        allow_missing_canva=args.allow_missing_canva,
    )

    if args.mode in ("preview", "dry-run"):
        print(writer.build_preview())
        return

    print(writer.build_preview())
    print()
    confirm = input("Proceed with CREATIVES + COPY tab writes? (type 'yes' to confirm): ").strip().lower()
    if confirm != "yes":
        print("Aborted. No sheet changes made.")
        return

    result = writer.write()
    print("\n✓ Ad concept sheet write complete:")
    print(f"  CREATIVES rows written: {result['creatives_rows_written']}")
    print(f"  COPY rows written:      {result['copy_rows_written']}")
    print(f"  Batches:                {result['batches']}")
    print(f"  Pre-write snapshot:     {result['pre_snapshot']}")
    print(f"  Post-write snapshot:    {result['post_snapshot']}")
    print(f"\nNot written by this script: {result['not_written']}")


if __name__ == "__main__":
    main()
