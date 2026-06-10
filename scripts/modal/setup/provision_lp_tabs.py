"""Provision LP funnel tabs in any client's Google Sheet.

Creates 3 tabs with consistent structure for an external-LP conversion funnel:
  • LP-<label>           — daily rows (one per day)
  • LP-<label>-Weekly    — weekly rollups (one per ISO week)
  • LP-<label>-Monthly   — monthly rollups (one per calendar month)

All three share the same column set and color/format conventions:
  • Front 9 columns (uncoloured) = client-facing reporting metrics
  • Back 9 columns (yellow/pink/blue tints) = agency diagnostic metrics
  • Row 1 = headers, Row 2 = SUMMARY (auto formulas), Row 3 = descriptions
  • Top 3 rows frozen

Usage:
    python3 scripts/modal/setup/provision_lp_tabs.py \\
        --client-slug neezanizam \\
        --label AssetProgression

Re-running with the same label is safe — existing tabs are skipped.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(_REPO_ROOT / ".env")

sys.path.insert(0, str(_REPO_ROOT / "scripts" / "modal"))
from sheets_writer import SheetsWriter  # noqa: E402


# ── Column definitions (shared across daily/weekly/monthly) ─────────────────

# (header, description, number_format, color_tag)
COLUMNS = [
    ("DATE",            "",                                                                                          "DATE",   None),
    ("SPEND",           "Cost base. Every downstream metric is judged against this.",                                 "MONEY",  None),
    ("FORM SUBMITS",    "Core conversion. The moment traffic becomes a captured lead.",                               "INT",    None),
    ("CPFS",            "True cost per lead. The headline efficiency metric.",                                        "MONEY",  None),
    ("LP→FORM CVR",     "How well the LP converts. Weak = messaging, trust, CTA, or form friction.",                  "PCT",    None),
    ("APPT",            "Leads who booked a call. Measures lead quality + follow-up effectiveness.",                  "INT",    None),
    ("CAPPT",           "Booked calls that actually showed up. Distinguishes intent from real attendance.",           "INT",    None),
    ("CPA",             "Cost per booked call. Cheap leads who never book have no value — this catches that.",        "MONEY",  None),
    ("REVENUE",         "The outcome. Every other metric only matters in relation to this.",                          "MONEY",  None),
    ("IMPRESSIONS",     "Delivery volume. Low = limited budget, weak ad approval, or poor delivery.",                 "INT",    "yellow"),
    ("REACH",           "Unique people reached. Reveals saturation — new prospects vs repeat exposure.",              "INT",    "yellow"),
    ("LINK CLICKS",     "Did the ad spark interest? Weak clicks = creative, angle, or offer problem.",                "INT",    "yellow"),
    ("LP VIEWS",        "Visits after the click. Clicks ≫ LP views = page speed, tracking, or pre-load bounce.",      "INT",    "yellow"),
    ("CTR",             "Attention efficiency. Low CTR = weak relevance or hook-audience mismatch.",                  "PCT",    "blue"),
    ("CPC",             "Traffic cost. Catches creeping price inflation even when CVR holds steady.",                 "MONEY",  "pink"),
    ("CPM",             "Auction cost per 1k impressions. Rising CPM = saturation or competitor pressure.",           "MONEY",  "pink"),
    ("CPLV",            "True traffic cost — only counts visits that fully loaded. More honest than CPC.",            "MONEY",  "pink"),
    ("CLICK→FORM CVR",  "End-to-end ad-to-lead rate. Diagnoses whether the leak is on the ad or the page.",           "PCT",    "blue"),
    ("NOTES",           "",                                                                                          "TEXT",   None),
]

SUMMARY_FORMULAS = {
    "DATE":            '"SUMMARY (auto)"',
    "SPEND":           "=SUM(B4:B)",
    "FORM SUBMITS":    "=SUM(C4:C)",
    "CPFS":            '=IFERROR(SUM(B4:B)/SUM(C4:C),"")',
    "LP→FORM CVR":     '=IFERROR(SUM(C4:C)/SUM(M4:M),"")',
    "APPT":            "=SUM(F4:F)",
    "CAPPT":           "=SUM(G4:G)",
    "CPA":             '=IFERROR(SUM(B4:B)/SUM(F4:F),"")',
    "REVENUE":         "=SUM(I4:I)",
    "IMPRESSIONS":     "=SUM(J4:J)",
    "REACH":           "=SUM(K4:K)",   # Caveat: daily reach summed overcounts unique people
    "LINK CLICKS":     "=SUM(L4:L)",
    "LP VIEWS":        "=SUM(M4:M)",
    "CTR":             '=IFERROR(SUM(L4:L)/SUM(J4:J),"")',
    "CPC":             '=IFERROR(SUM(B4:B)/SUM(L4:L),"")',
    "CPM":             '=IFERROR(SUM(B4:B)/SUM(J4:J)*1000,"")',
    "CPLV":            '=IFERROR(SUM(B4:B)/SUM(M4:M),"")',
    "CLICK→FORM CVR":  '=IFERROR(SUM(C4:C)/SUM(L4:L),"")',
    "NOTES":           '"auto"',
}

# DATE format varies per tab type — daily is real DATE, weekly/monthly are TEXT labels
DATE_FORMAT_OVERRIDES = {
    "weekly":  "TEXT",
    "monthly": "TEXT",
}

# ── Color presets (RGB 0–1) ─────────────────────────────────────────────────
COLOR_HEADER       = {"red": 0.10, "green": 0.10, "blue": 0.10}
COLOR_SUMMARY      = {"red": 0.30, "green": 0.30, "blue": 0.30}
COLOR_DESC         = {"red": 0.93, "green": 0.93, "blue": 0.93}
COLOR_YELLOW_TINT  = {"red": 1.00, "green": 0.96, "blue": 0.80}
COLOR_PINK_TINT    = {"red": 0.98, "green": 0.86, "blue": 0.88}
COLOR_BLUE_TINT    = {"red": 0.82, "green": 0.91, "blue": 0.98}
WHITE              = {"red": 1.0, "green": 1.0, "blue": 1.0}

NUMBER_FORMATS = {
    "MONEY": {"type": "CURRENCY", "pattern": "$#,##0.00"},
    "INT":   {"type": "NUMBER",   "pattern": "#,##0"},
    "PCT":   {"type": "PERCENT",  "pattern": "0.00%"},
    "DATE":  {"type": "DATE",     "pattern": "dd/mm/yy"},
    "TEXT":  {"type": "TEXT",     "pattern": "@"},
}


def _build_writer() -> SheetsWriter:
    creds_path = os.environ.get("GOOGLE_SHEETS_CREDS_PATH", "scripts/modal/credentials.json")
    if not os.path.isabs(creds_path):
        creds_path = str(_REPO_ROOT / creds_path)
    return SheetsWriter(service_account_path=creds_path)


def _load_client_metrics_config(client_slug: str) -> dict:
    cfg_path = _REPO_ROOT / "clients" / client_slug / "metrics-config.json"
    if not cfg_path.exists():
        raise SystemExit(f"metrics-config.json not found: {cfg_path}")
    return json.loads(cfg_path.read_text())


def _create_one_tab(sheet, tab_name: str, period: str) -> int:
    """Create a single tab with full LP funnel structure. Returns gid.

    period: "daily" | "weekly" | "monthly" — controls DATE column format only.
    """
    existing = {ws.title: ws for ws in sheet.worksheets()}
    if tab_name in existing:
        ws = existing[tab_name]
        print(f"  ⏭  {tab_name} exists (gid={ws.id}) — skipping creation")
        return ws.id

    n_cols = len(COLUMNS)
    ws = sheet.add_worksheet(title=tab_name, rows=200, cols=n_cols)
    print(f"  ✓ Created {tab_name} (gid={ws.id})")

    headers = [c[0] for c in COLUMNS]
    ws.update(values=[headers], range_name="A1", value_input_option="USER_ENTERED")

    summary_row = []
    for header, _, _, _ in COLUMNS:
        f = SUMMARY_FORMULAS.get(header, "")
        if f.startswith("="):
            summary_row.append(f)
        elif f.startswith('"') and f.endswith('"'):
            summary_row.append(f[1:-1])
        else:
            summary_row.append("")
    ws.update(values=[summary_row], range_name="A2", value_input_option="USER_ENTERED")

    descriptions = [c[1] for c in COLUMNS]
    ws.update(values=[descriptions], range_name="A3", value_input_option="USER_ENTERED")

    sheet_id = ws.id
    requests: list[dict] = []

    # Freeze top 3 rows
    requests.append({"updateSheetProperties": {
        "properties": {"sheetId": sheet_id, "gridProperties": {"frozenRowCount": 3}},
        "fields": "gridProperties.frozenRowCount",
    }})

    # Header row
    requests.append({"repeatCell": {
        "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": n_cols},
        "cell": {"userEnteredFormat": {
            "backgroundColor": COLOR_HEADER,
            "textFormat": {"foregroundColor": WHITE, "bold": True, "fontSize": 10},
            "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE",
        }},
        "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)",
    }})

    # Summary row
    requests.append({"repeatCell": {
        "range": {"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": 2, "startColumnIndex": 0, "endColumnIndex": n_cols},
        "cell": {"userEnteredFormat": {
            "backgroundColor": COLOR_SUMMARY,
            "textFormat": {"foregroundColor": WHITE, "bold": True, "fontSize": 10},
            "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE",
        }},
        "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)",
    }})

    # Description row
    requests.append({"repeatCell": {
        "range": {"sheetId": sheet_id, "startRowIndex": 2, "endRowIndex": 3, "startColumnIndex": 0, "endColumnIndex": n_cols},
        "cell": {"userEnteredFormat": {
            "backgroundColor": COLOR_DESC,
            "textFormat": {"italic": True, "fontSize": 9},
            "wrapStrategy": "WRAP", "verticalAlignment": "TOP",
        }},
        "fields": "userEnteredFormat(backgroundColor,textFormat,wrapStrategy,verticalAlignment)",
    }})

    # Per-column number formats
    for idx, (header, _, fmt_key, _) in enumerate(COLUMNS):
        # Override DATE → TEXT for weekly/monthly tabs (date column is a label string)
        if header == "DATE" and period in DATE_FORMAT_OVERRIDES:
            fmt_key = DATE_FORMAT_OVERRIDES[period]
        fmt = NUMBER_FORMATS.get(fmt_key)
        if not fmt or fmt_key == "TEXT":
            continue
        # Apply to row 2 (summary) + rows 4–200 (data)
        for row_range in [(1, 2), (3, 200)]:
            requests.append({"repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": row_range[0], "endRowIndex": row_range[1],
                          "startColumnIndex": idx, "endColumnIndex": idx + 1},
                "cell": {"userEnteredFormat": {"numberFormat": fmt}},
                "fields": "userEnteredFormat.numberFormat",
            }})

    # Per-column tints (data rows only)
    color_map = {"yellow": COLOR_YELLOW_TINT, "pink": COLOR_PINK_TINT, "blue": COLOR_BLUE_TINT}
    for idx, (_, _, _, color_tag) in enumerate(COLUMNS):
        if color_tag and color_tag in color_map:
            requests.append({"repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 3, "endRowIndex": 200,
                          "startColumnIndex": idx, "endColumnIndex": idx + 1},
                "cell": {"userEnteredFormat": {"backgroundColor": color_map[color_tag]}},
                "fields": "userEnteredFormat.backgroundColor",
            }})

    # Column widths
    for idx, (header, _, fmt_key, _) in enumerate(COLUMNS):
        if header == "NOTES":
            width = 200
        elif header == "DATE":
            width = 140 if period in DATE_FORMAT_OVERRIDES else 80  # wider for date ranges
        elif fmt_key == "PCT":
            width = 110
        else:
            width = 95
        requests.append({"updateDimensionProperties": {
            "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": idx, "endIndex": idx + 1},
            "properties": {"pixelSize": width}, "fields": "pixelSize",
        }})

    # Description row height
    requests.append({"updateDimensionProperties": {
        "range": {"sheetId": sheet_id, "dimension": "ROWS", "startIndex": 2, "endIndex": 3},
        "properties": {"pixelSize": 60}, "fields": "pixelSize",
    }})

    sheet.batch_update({"requests": requests})
    return sheet_id


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--client-slug", required=True, help="Folder name under clients/")
    parser.add_argument("--label",       required=True, help="LP label suffix (e.g. AssetProgression)")
    parser.add_argument("--sheet-id",    default=None, help="Override sheet_id (defaults to client config)")
    args = parser.parse_args()

    cfg = _load_client_metrics_config(args.client_slug)
    sheet_id = args.sheet_id or cfg["sheet_id"]
    writer = _build_writer()
    sheet = writer.get_sheet(sheet_id)

    print(f"Provisioning LP funnel tabs for '{args.client_slug}' "
          f"(sheet={sheet_id}, label={args.label})")
    print()

    results = {}
    for period, suffix in [("daily", ""), ("weekly", "-Weekly"), ("monthly", "-Monthly")]:
        tab_name = f"LP-{args.label}{suffix}"
        gid = _create_one_tab(sheet, tab_name, period)
        results[period] = {"name": tab_name, "gid": gid}

    print()
    print("📋 Add this snippet to clients/<slug>/metrics-config.json under 'tabs':")
    print()
    snippet = {
        "lp_funnel": _tab_spec(results["daily"], "DD/MM/YY", "meta_insights_lp_funnel"),
        "lp_funnel_weekly": _tab_spec(results["weekly"], "DD/MM/YY TO DD/MM/YY", "meta_insights_lp_funnel_period"),
        "lp_funnel_monthly": _tab_spec(results["monthly"], "MMMM YYYY", "meta_insights_lp_funnel_period"),
    }
    print(json.dumps(snippet, indent=2))


def _tab_spec(tab: dict, date_format: str, source: str) -> dict:
    return {
        "gid": str(tab["gid"]),
        "name": tab["name"],
        "columns": [c[0] for c in COLUMNS],
        "write_mode": "append",
        "frequency": source.split("_")[-1] if "period" not in source else "weekly_or_monthly",
        "date_format": date_format,
        "source": source,
        "scope": "campaign_filtered",
        "blank_when_zero_submits": ["CPFS", "LP→FORM CVR", "CLICK→FORM CVR"],
        "blank_when_zero_appt": ["CPA"],
        "manual_columns": ["APPT", "CAPPT", "REVENUE", "NOTES"],
    }


if __name__ == "__main__":
    main()
