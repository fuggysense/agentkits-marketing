"""Aggregate daily metrics into weekly/monthly rollups.

Weighted averages are computed properly (e.g. CTR = total clicks / total
impressions, NOT mean of daily CTRs) so the rollup reflects reality.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any


_DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%y", "%d/%m/%Y", "%m/%d/%Y")


def _parse_date(value: Any) -> date | None:
    """Best-effort date parsing. Returns None if unparseable."""
    if value is None or value == "":
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    s = str(value).strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _num(value: Any, default: float = 0.0) -> float:
    """Coerce to float, tolerating '1,234.56', '$12.50', '12%'."""
    if value is None or value == "":
        return default
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).replace(",", "").replace("$", "").replace("%", "").strip()
    try:
        return float(s)
    except ValueError:
        return default


def _safe_div(num: float, denom: float) -> float:
    """Return 0.0 instead of raising ZeroDivisionError."""
    return num / denom if denom else 0.0


class MetricsAggregator:
    """Roll up daily metric rows into weekly/monthly summaries."""

    # ── Public API ──────────────────────────────────────────────────────────

    def aggregate_daily_to_weekly(
        self,
        daily_rows: list[dict],
        week_start: str,
        week_end: str,
    ) -> dict:
        """Collapse a week of daily rows into one WEEKLY CALLS row.

        Args:
            daily_rows: List of dicts as read from the DAILY CALLS tab.
            week_start: ISO date string — inclusive start of the week.
            week_end:   ISO date string — inclusive end of the week.

        Returns:
            Dict keyed by WEEKLY CALLS column names (see _weekly_row).
        """
        date_label = self._format_date_range(week_start, week_end)
        return self._rollup(daily_rows, date_label, period="week")

    def aggregate_weekly_to_monthly(
        self,
        weekly_rows: list[dict],
        month_name: str,
    ) -> dict:
        """Collapse weekly rows into one MONTHLY CALLS row.

        Args:
            weekly_rows: List of dicts from the WEEKLY CALLS tab.
            month_name:  Human label for the DATE column (e.g. "April").

        Returns:
            Dict keyed by MONTHLY CALLS column names.
        """
        return self._rollup(weekly_rows, month_name, period="month")

    def pull_daily_rows_for_week(
        self,
        sheets_writer,
        daily_tab,
        week_start: str,
        week_end: str,
    ) -> list[dict]:
        """Fetch daily rows from the sheet that fall within [week_start, week_end]."""
        start = _parse_date(week_start)
        end = _parse_date(week_end)
        if not start or not end:
            raise ValueError(
                f"Invalid week bounds: start={week_start!r}, end={week_end!r}"
            )

        all_rows = sheets_writer.read_all_rows(daily_tab)
        in_range: list[dict] = []
        for row in all_rows:
            row_date = _parse_date(row.get("DATE", row.get("date")))
            if row_date and start <= row_date <= end:
                in_range.append(row)
        return in_range

    # ── Internals ───────────────────────────────────────────────────────────

    def _rollup(
        self,
        rows: list[dict],
        date_label: str,
        period: str,
    ) -> dict:
        """Shared weekly/monthly rollup logic.

        Uses weighted averages: we sum the underlying totals (spend,
        impressions, clicks, leads, etc.) and derive the ratio metrics from
        those totals rather than averaging daily/weekly ratios.
        """
        totals = {
            "spend": 0.0,
            "impressions": 0,
            "clicks": 0,
            "leads": 0,
            "appointments": 0,
            "confirmed_appointments": 0,
            "revenue": 0.0,
            "outbound_clicks": 0,
        }

        for row in rows:
            totals["spend"] += _num(row.get("AMOUNT SPENT", row.get("spend")))
            totals["impressions"] += int(_num(row.get("IMPRESSIONS", row.get("impressions"))))
            totals["clicks"] += int(_num(row.get("CLICKS", row.get("clicks"))))
            totals["leads"] += int(_num(row.get("LEAD", row.get("leads"))))
            totals["appointments"] += int(_num(row.get("APPT", row.get("appointments"))))
            totals["confirmed_appointments"] += int(
                _num(row.get("CAPPT", row.get("confirmed_appointments")))
            )
            totals["revenue"] += _num(row.get("REVENUE", row.get("revenue")))
            totals["outbound_clicks"] += int(
                _num(row.get("OUTBOUND_CLICKS", row.get("outbound_clicks")))
            )

        # Ratio metrics stored as decimal fractions (0–1). Sheet cells formatted
        # as percentage render correctly; keeps daily/weekly/monthly consistent.
        ctr = _safe_div(totals["clicks"], totals["impressions"])
        cvr = _safe_div(totals["leads"], totals["clicks"])
        cpm = _safe_div(totals["spend"], totals["impressions"]) * 1000
        cpl = _safe_div(totals["spend"], totals["leads"])
        cpoc = _safe_div(totals["spend"], totals["outbound_clicks"])
        octr = _safe_div(totals["outbound_clicks"], totals["impressions"])
        roas = _safe_div(totals["revenue"], totals["spend"])

        row: dict = {
            "DATE": date_label,
            "APPT": totals["appointments"],
            "CAPPT": totals["confirmed_appointments"],
            "REVENUE": round(totals["revenue"], 2),
            "AMOUNT SPENT": round(totals["spend"], 2),
            "ROAS": round(roas, 2),
            "CVR": round(cvr, 6),
            "CPM": round(cpm, 2),
            "CPOC": round(cpoc, 2),
            "OCTR": round(octr, 6),
            "NOTES": "",
        }
        # CTR/CPL aren't in the weekly template but are useful for debugging
        row["_ctr"] = round(ctr, 6)
        row["_cpl"] = round(cpl, 2)
        row["_period"] = period
        return row

    @staticmethod
    def _format_date_range(start: str, end: str) -> str:
        """Format '2026-04-06' + '2026-04-12' -> '06/04/26 TO 12/04/26'."""
        s = _parse_date(start)
        e = _parse_date(end)
        if not s or not e:
            return f"{start} TO {end}"
        return f"{s.strftime('%d/%m/%y')} TO {e.strftime('%d/%m/%y')}"
