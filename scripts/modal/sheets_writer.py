"""Google Sheets writer for the Modal metrics app.

Wraps gspread with helpers tailored to the template sheet layout:
  - Append daily/weekly/monthly rows
  - Update only metric columns on the CREATIVES tab (respects protected cols)
  - Update specific KPI cells by A1 notation
"""

from __future__ import annotations

import json
from typing import Any

import gspread
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class ProtectedColumnError(RuntimeError):
    """Raised when attempting to write to a protected column."""


class SheetsWriter:
    """Authenticated gspread client with metric-sheet-specific helpers."""

    def __init__(
        self,
        service_account_json: str | dict | None = None,
        service_account_path: str | None = None,
    ) -> None:
        """Construct from either a JSON string/dict (Modal secret) or a file path.

        Args:
            service_account_json: Raw JSON string or parsed dict of creds.
            service_account_path: Path to a local service-account JSON file.
        """
        if service_account_json:
            info = (
                json.loads(service_account_json)
                if isinstance(service_account_json, str)
                else service_account_json
            )
            creds = Credentials.from_service_account_info(info, scopes=SCOPES)
        elif service_account_path:
            creds = Credentials.from_service_account_file(
                service_account_path, scopes=SCOPES
            )
        else:
            raise RuntimeError(
                "GOOGLE_CREDS_JSON not set and no service_account_path given. "
                "See setup in plan."
            )

        self.client = gspread.authorize(creds)

    # ── Sheet / tab access ──────────────────────────────────────────────────

    def get_sheet(self, sheet_id: str):
        """Open a spreadsheet by its ID."""
        return self.client.open_by_key(sheet_id)

    def get_tab(self, sheet, gid: int | str):
        """Return the worksheet with the given gid (sheet id)."""
        target_gid = int(gid)
        for ws in sheet.worksheets():
            if ws.id == target_gid:
                return ws
        raise ValueError(f"Tab with gid={gid} not found in sheet {sheet.id}")

    # ── Row operations ──────────────────────────────────────────────────────

    def append_row(
        self,
        tab,
        row_dict: dict,
        columns: list[str],
    ) -> None:
        """Append a row by mapping `row_dict` to `columns` order.

        Missing keys are written as empty strings.
        """
        values = [self._coerce(row_dict.get(col, "")) for col in columns]
        tab.append_row(values, value_input_option="USER_ENTERED")

    def update_metric_columns(
        self,
        tab,
        batch_id: str,
        metric_columns: dict,
        protected_columns: list[str],
    ) -> None:
        """Update metric cells for the row whose col A matches `batch_id`.

        Raises ProtectedColumnError if `metric_columns` collides with
        `protected_columns`.
        """
        forbidden = set(metric_columns.keys()) & set(protected_columns)
        if forbidden:
            raise ProtectedColumnError(
                f"Refusing to overwrite protected columns: {sorted(forbidden)}"
            )

        row_num = self.find_row_by_id(tab, batch_id, id_column=1)
        if row_num is None:
            raise ValueError(
                f"Batch id '{batch_id}' not found in column A of '{tab.title}'. "
                "Add the row manually before pushing metrics."
            )

        batch_updates: list[dict[str, Any]] = []
        for col_name, value in metric_columns.items():
            col_letter = self.column_name_to_letter(tab, col_name)
            batch_updates.append({
                "range": f"{col_letter}{row_num}",
                "values": [[self._coerce(value)]],
            })

        if batch_updates:
            tab.batch_update(batch_updates, value_input_option="USER_ENTERED")

    def update_cells(self, tab, cell_updates: dict) -> None:
        """Update specific cells by A1 notation. Used for the KPIs tab.

        Args:
            cell_updates: {"B2": 142.50, "B3": 38.00, ...}
        """
        if not cell_updates:
            return
        batch = [
            {"range": addr, "values": [[self._coerce(val)]]}
            for addr, val in cell_updates.items()
        ]
        tab.batch_update(batch, value_input_option="USER_ENTERED")

    # ── Lookups ─────────────────────────────────────────────────────────────

    def find_row_by_id(
        self,
        tab,
        id_value: str,
        id_column: int = 1,
    ) -> int | None:
        """Return 1-indexed row number matching `id_value` in `id_column`."""
        col_values = tab.col_values(id_column)
        for idx, val in enumerate(col_values, start=1):
            if (val or "").strip() == id_value.strip():
                return idx
        return None

    def column_name_to_letter(self, tab, column_name: str) -> str:
        """Look up column_name in header row 1, return the column's A1 letter."""
        header = tab.row_values(1)
        for idx, name in enumerate(header, start=1):
            if (name or "").strip().lower() == column_name.strip().lower():
                return self._col_index_to_letter(idx)
        raise ValueError(
            f"Column '{column_name}' not found in header of '{tab.title}'. "
            f"Header: {header}"
        )

    # ── Read helpers ────────────────────────────────────────────────────────

    def read_all_rows(self, tab) -> list[dict]:
        """Return all data rows as dicts keyed by header row values."""
        return tab.get_all_records()

    # ── Internals ───────────────────────────────────────────────────────────

    @staticmethod
    def _col_index_to_letter(idx: int) -> str:
        """1 -> 'A', 27 -> 'AA', etc."""
        if idx < 1:
            raise ValueError(f"Column index must be >= 1, got {idx}")
        letters = ""
        n = idx
        while n > 0:
            n, rem = divmod(n - 1, 26)
            letters = chr(65 + rem) + letters
        return letters

    @staticmethod
    def _coerce(value: Any) -> Any:
        """Coerce None to empty string, keep numbers + strings as-is."""
        if value is None:
            return ""
        if isinstance(value, (int, float, str)):
            return value
        return str(value)
