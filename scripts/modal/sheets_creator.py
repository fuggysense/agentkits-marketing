"""Provision new client Google Sheets from a master template.

Copies the template via Drive API, clears data rows (preserving headers and
any formula rows), shares with the client, optionally transfers ownership to
Jerel, and writes a filled `metrics-config.json` into `clients/<slug>/`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Marketing repo root — three levels up from this file
_ROOT = Path(__file__).resolve().parent.parent.parent
_CLIENTS_DIR = _ROOT / "clients"
_TEMPLATE_CONFIG_PATH = _CLIENTS_DIR / "_template" / "metrics-config.json"


class SheetsCreator:
    """Create and configure per-client metrics sheets from the master template."""

    def __init__(
        self,
        template_sheet_id: str,
        service_account_json: str | dict | None = None,
        service_account_path: str | None = None,
    ) -> None:
        if not template_sheet_id:
            raise RuntimeError(
                "template_sheet_id required. Set MASTER_METRICS_TEMPLATE_ID."
            )

        if service_account_json:
            info = (
                json.loads(service_account_json)
                if isinstance(service_account_json, str)
                else service_account_json
            )
            self.creds = Credentials.from_service_account_info(info, scopes=SCOPES)
        elif service_account_path:
            self.creds = Credentials.from_service_account_file(
                service_account_path, scopes=SCOPES
            )
        else:
            raise RuntimeError(
                "GOOGLE_CREDS_JSON not set and no service_account_path given. "
                "See setup in plan."
            )

        self.template_sheet_id = template_sheet_id
        self.gc = gspread.authorize(self.creds)
        self.drive = build("drive", "v3", credentials=self.creds)

    # ── Create + clone ──────────────────────────────────────────────────────

    def create_from_template(self, new_title: str) -> dict:
        """Duplicate the master template and return the new sheet's metadata.

        Returns:
            {"sheet_id": str, "sheet_url": str, "tab_gids": {tab_name: gid}}
        """
        try:
            copied = (
                self.drive.files()
                .copy(
                    fileId=self.template_sheet_id,
                    body={"name": new_title},
                    supportsAllDrives=True,
                )
                .execute()
            )
        except HttpError as e:
            raise RuntimeError(
                f"Drive API copy failed: {e}. Verify the service account has "
                "at least Viewer access to the template sheet."
            ) from e

        sheet_id = copied["id"]
        sheet = self.gc.open_by_key(sheet_id)

        tab_gids = {ws.title: ws.id for ws in sheet.worksheets()}
        return {
            "sheet_id": sheet_id,
            "sheet_url": sheet.url,
            "tab_gids": tab_gids,
        }

    # ── Clean template content ──────────────────────────────────────────────

    def clear_data_rows(self, sheet) -> None:
        """Clear data rows in every tab, preserving the header (row 1) and
        any row that contains a formula.
        """
        for ws in sheet.worksheets():
            values = ws.get_all_values()
            if len(values) <= 1:
                continue  # header only

            # Fetch raw formulas so we can tell which rows are formula-driven
            formulas_resp = ws.spreadsheet.values_get(
                f"'{ws.title}'",
                params={"valueRenderOption": "FORMULA"},
            )
            formula_grid = formulas_resp.get("values", [])

            rows_to_clear: list[str] = []
            for row_idx in range(2, len(values) + 1):  # 1-indexed, skip header
                formula_row = (
                    formula_grid[row_idx - 1] if row_idx - 1 < len(formula_grid) else []
                )
                has_formula = any(
                    isinstance(cell, str) and cell.startswith("=")
                    for cell in formula_row
                )
                if has_formula:
                    continue
                rows_to_clear.append(
                    f"'{ws.title}'!A{row_idx}:ZZ{row_idx}"
                )

            if rows_to_clear:
                ws.spreadsheet.values_batch_clear({"ranges": rows_to_clear})

    # ── Sharing + ownership ─────────────────────────────────────────────────

    def share_with(
        self,
        sheet_id: str,
        email: str,
        role: str = "writer",
        notify: bool = False,
    ) -> None:
        """Share the sheet with `email` as the given role (reader|writer|commenter)."""
        if role not in ("reader", "writer", "commenter"):
            raise ValueError(f"Invalid share role: {role}")
        if not email:
            raise ValueError("email required for share_with")

        self.drive.permissions().create(
            fileId=sheet_id,
            body={"type": "user", "role": role, "emailAddress": email},
            sendNotificationEmail=notify,
            supportsAllDrives=True,
        ).execute()

    def transfer_ownership(self, sheet_id: str, owner_email: str) -> None:
        """Transfer ownership to `owner_email` (consumer Gmail only)."""
        if not owner_email:
            raise ValueError("owner_email required for transfer_ownership")

        try:
            self.drive.permissions().create(
                fileId=sheet_id,
                body={"type": "user", "role": "owner", "emailAddress": owner_email},
                transferOwnership=True,
                sendNotificationEmail=True,
                supportsAllDrives=True,
            ).execute()
        except HttpError as e:
            raise RuntimeError(
                f"Ownership transfer to {owner_email} failed: {e}. "
                "Consumer Gmail transfers may require manual acceptance, and "
                "Workspace-to-Workspace transfers need admin tooling."
            ) from e

    # ── Config generation ───────────────────────────────────────────────────

    def generate_metrics_config(
        self,
        client_slug: str,
        sheet_id: str,
        tab_gids: dict,
        sheet_url: str = "",
        ad_account_id: str = "",
    ) -> dict:
        """Render `clients/_template/metrics-config.json` with real values.

        Placeholders filled:
          {{CLIENT_SLUG}}, {{GOOGLE_SHEET_ID}}, {{GOOGLE_SHEET_URL}},
          {{META_AD_ACCOUNT_ID}}, {{GID_DAILY_CALLS}}, {{GID_WEEKLY_CALLS}},
          {{GID_MONTHLY_CALLS}}, {{GID_KPIS}}, {{GID_CREATIVES}},
          {{GID_COPY}}, {{GID_AVATARS}}.
        """
        if not _TEMPLATE_CONFIG_PATH.exists():
            raise FileNotFoundError(
                f"Template config not found at {_TEMPLATE_CONFIG_PATH}"
            )

        raw = _TEMPLATE_CONFIG_PATH.read_text()

        # Map template tab names → config placeholder keys
        placeholder_map = {
            "DAILY CALLS": "{{GID_DAILY_CALLS}}",
            "WEEKLY CALLS": "{{GID_WEEKLY_CALLS}}",
            "MONTHLY CALLS": "{{GID_MONTHLY_CALLS}}",
            "KPIs": "{{GID_KPIS}}",
            "CREATIVES": "{{GID_CREATIVES}}",
            "COPY": "{{GID_COPY}}",
            "AVATARS": "{{GID_AVATARS}}",
        }
        for tab_name, placeholder in placeholder_map.items():
            gid = tab_gids.get(tab_name)
            if gid is None:
                raise ValueError(
                    f"Template sheet missing expected tab '{tab_name}'. "
                    f"Actual tabs: {list(tab_gids.keys())}"
                )
            raw = raw.replace(placeholder, str(gid))

        raw = raw.replace("{{CLIENT_SLUG}}", client_slug)
        raw = raw.replace("{{GOOGLE_SHEET_ID}}", sheet_id)
        raw = raw.replace("{{GOOGLE_SHEET_URL}}", sheet_url)
        raw = raw.replace("{{META_AD_ACCOUNT_ID}}", ad_account_id or "")

        return json.loads(raw)

    def save_config(self, client_slug: str, config: dict) -> Path:
        """Write config to `clients/<slug>/metrics-config.json` and return path."""
        client_dir = _CLIENTS_DIR / client_slug
        client_dir.mkdir(parents=True, exist_ok=True)
        out = client_dir / "metrics-config.json"
        out.write_text(json.dumps(config, indent=2) + "\n")
        return out
