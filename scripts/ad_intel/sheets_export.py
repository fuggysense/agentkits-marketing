"""Phase 5: Google Sheets Export with industry tabs."""

import json
from datetime import datetime
from pathlib import Path

import gspread

from config import (
    GSHEETS_CREDENTIALS_FILE, GSHEETS_SHARE_EMAIL,
    VERTICALS, VERTICAL_DISPLAY_NAMES, DATA_DIR, OUTPUT_DIR,
)


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# OAuth credentials for user-owned sheets (bypasses service account storage quota)
_OAUTH_CLIENT_FILE = Path(__file__).resolve().parent.parent.parent / "credentials" / "oauth_client.json"
_OAUTH_TOKEN_FILE = Path(__file__).resolve().parent.parent.parent / "credentials" / "oauth_token.json"

# Target Google Drive folder for all ad intel sheets
DRIVE_FOLDER_ID = "17hdV8s0ugygFXvk44j7l1yB18Bf3WdEK"


def _get_gspread_client():
    """Get an authenticated gspread client.

    Priority:
      1. OAuth user credentials (creates sheets as the user, in their Drive)
      2. Service account (fallback)
    """
    # Try OAuth first
    if _OAUTH_TOKEN_FILE.exists():
        from google.oauth2.credentials import Credentials as OAuthCreds
        creds = OAuthCreds.from_authorized_user_file(str(_OAUTH_TOKEN_FILE), SCOPES)
        if creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request
            creds.refresh(Request())
            _OAUTH_TOKEN_FILE.write_text(creds.to_json())
        return gspread.authorize(creds)

    # Fallback to service account
    if Path(GSHEETS_CREDENTIALS_FILE).exists():
        from google.oauth2.service_account import Credentials as SACreds
        creds = SACreds.from_service_account_file(GSHEETS_CREDENTIALS_FILE, scopes=SCOPES)
        return gspread.authorize(creds)

    raise RuntimeError(
        "No Google credentials found. Run the OAuth flow first:\n"
        "  python sheets_export.py --auth"
    )


def run_oauth_flow():
    """One-time OAuth flow — opens browser for user consent, saves token."""
    from google_auth_oauthlib.flow import InstalledAppFlow

    if not _OAUTH_CLIENT_FILE.exists():
        raise RuntimeError(f"OAuth client file not found at {_OAUTH_CLIENT_FILE}")

    flow = InstalledAppFlow.from_client_secrets_file(str(_OAUTH_CLIENT_FILE), SCOPES)
    creds = flow.run_local_server(port=0)
    _OAUTH_TOKEN_FILE.write_text(creds.to_json())
    print(f"OAuth token saved to {_OAUTH_TOKEN_FILE}")
    return creds

# Column headers for all tabs
HEADERS = [
    "UID", "Business Name", "Score (1-10)", "Tier", "Vertical(s)",
    "Country",
    "Website", "FB Page",
    "Decision Maker", "First Name",
    "Phone", "Email", "WhatsApp",
    "Full Address (HQ)", "Postal Code", "Branch Count", "Branches",
    # Metadata columns
    "Page Title", "Meta Description", "OG Title", "OG Description",
    # Ad data
    "Google Keywords (count)", "Meta Spend Range", "Meta Ad Count",
    "Sample Ad Copy", "Landing Page",
    "First Seen", "Notes",
]


def _biz_to_row(biz: dict) -> list:
    """Convert a business dict to a spreadsheet row."""
    spend_range = ""
    if biz.get("meta_spend_min") or biz.get("meta_spend_max"):
        spend_range = f"${biz.get('meta_spend_min', 0):,}-${biz.get('meta_spend_max', 0):,}"

    return [
        biz.get("uid", ""),
        biz.get("business_name", ""),
        biz.get("score", 0),
        biz.get("tier", "").upper(),
        ", ".join(biz.get("verticals", [])),
        biz.get("country", ""),
        biz.get("website", ""),
        biz.get("fb_page_url", ""),
        biz.get("decision_maker_full_name", ""),
        biz.get("decision_maker_first_name", ""),
        biz.get("phone", ""),
        biz.get("email", ""),
        biz.get("whatsapp", ""),
        biz.get("full_address", ""),
        biz.get("postal_code", ""),
        biz.get("branch_count") or "",
        biz.get("branches_display", ""),
        # Metadata
        biz.get("page_title", ""),
        biz.get("meta_description", ""),
        biz.get("og_title", ""),
        biz.get("og_description", ""),
        # Ad data — show blank instead of 0 when no data
        biz.get("google_keyword_count") or "",
        spend_range,
        biz.get("meta_ad_count") or "",
        (biz.get("sample_ad_copy", "") or "")[:200],
        (biz.get("landing_pages", [""])[0] if biz.get("landing_pages") else ""),
        biz.get("first_seen", ""),
        biz.get("notes", ""),
    ]


def _apply_formatting(spreadsheet, worksheet):
    """Apply conditional formatting: green (8-10), yellow (4-7), red (1-3)."""
    # Format header row
    worksheet.format("1:1", {
        "textFormat": {"bold": True},
        "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.3},
        "textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1}, "bold": True},
    })

    # Freeze header row
    worksheet.freeze(rows=1)

    # Auto-resize first few columns
    # (gspread doesn't support auto-resize directly, but we set column widths)

    # Conditional formatting on Score column (B)
    rules = gspread.utils.ExportFormat  # noqa — just checking availability
    # Note: gspread conditional formatting requires batch_update with raw API
    # We'll use the spreadsheets API directly
    sheet_id = worksheet.id

    requests = [
        # Green: score 8-10
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": sheet_id, "startColumnIndex": 2, "endColumnIndex": 3}],
                    "booleanRule": {
                        "condition": {"type": "NUMBER_GREATER_THAN_EQ", "values": [{"userEnteredValue": "8"}]},
                        "format": {"backgroundColor": {"red": 0.72, "green": 0.88, "blue": 0.72}},
                    },
                },
                "index": 0,
            }
        },
        # Yellow: score 4-7
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": sheet_id, "startColumnIndex": 2, "endColumnIndex": 3}],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [{"userEnteredValue": "=AND(C2>=4, C2<8)"}],
                        },
                        "format": {"backgroundColor": {"red": 1, "green": 0.95, "blue": 0.6}},
                    },
                },
                "index": 1,
            }
        },
        # Red: score 1-3
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": sheet_id, "startColumnIndex": 2, "endColumnIndex": 3}],
                    "booleanRule": {
                        "condition": {"type": "NUMBER_LESS_THAN", "values": [{"userEnteredValue": "4"}]},
                        "format": {"backgroundColor": {"red": 0.96, "green": 0.7, "blue": 0.7}},
                    },
                },
                "index": 2,
            }
        },
    ]

    try:
        spreadsheet.batch_update({"requests": requests})
    except Exception as e:
        print(f"  Warning: conditional formatting failed: {e}")


def export_to_sheets(
    businesses: list[dict],
    title: str | None = None,
    previous_data: list[dict] | None = None,
) -> str:
    """Export businesses to Google Sheets with industry tabs.

    Returns the spreadsheet URL.
    """
    gc = _get_gspread_client()

    date_str = datetime.now().strftime("%y%m%d")
    sheet_title = title or f"1UP Singapore Ad Intelligence — {date_str}"

    spreadsheet = gc.create(sheet_title, folder_id=DRIVE_FOLDER_ID)

    # ── Tab 1: All (Scored) ──
    ws_all = spreadsheet.sheet1
    ws_all.update_title("All (Scored)")
    rows = [HEADERS] + [_biz_to_row(b) for b in businesses]
    ws_all.update(rows, value_input_option="USER_ENTERED")
    _apply_formatting(spreadsheet, ws_all)

    # ── Industry tabs ──
    for vertical in VERTICALS:
        display_name = VERTICAL_DISPLAY_NAMES.get(vertical, vertical)
        filtered = [b for b in businesses if vertical in b.get("verticals", [])]

        if not filtered:
            continue

        ws = spreadsheet.add_worksheet(title=display_name, rows=len(filtered) + 1, cols=len(HEADERS))
        rows = [HEADERS] + [_biz_to_row(b) for b in filtered]
        ws.update(rows, value_input_option="USER_ENTERED")
        _apply_formatting(spreadsheet, ws)

    # ── "New This Month" tab (diff detection) ──
    if previous_data is not None:
        prev_domains = {b.get("domain", "") for b in previous_data if b.get("domain")}
        new_businesses = [b for b in businesses if b.get("domain") and b["domain"] not in prev_domains]

        if new_businesses:
            ws_new = spreadsheet.add_worksheet(
                title=f"New This Month — {date_str}",
                rows=len(new_businesses) + 1,
                cols=len(HEADERS),
            )
            rows = [HEADERS] + [_biz_to_row(b) for b in new_businesses]
            ws_new.update(rows, value_input_option="USER_ENTERED")
            _apply_formatting(spreadsheet, ws_new)

    return spreadsheet.url


def create_spreadsheet(title: str | None = None, folder_id: str | None = None) -> tuple:
    """Create a new Google Sheet and return (spreadsheet, url).

    Uses OAuth credentials to create the sheet in the user's Drive folder.
    """
    gc = _get_gspread_client()

    date_str = datetime.now().strftime("%y%m%d")
    sheet_title = title or f"1UP Singapore Ad Intelligence — {date_str}"

    target_folder = folder_id or DRIVE_FOLDER_ID
    spreadsheet = gc.create(sheet_title, folder_id=target_folder)

    # Rename default Sheet1 — will be used by first vertical
    spreadsheet.sheet1.update_title("_placeholder")

    return spreadsheet, spreadsheet.url


def open_spreadsheet(url: str) -> object:
    """Re-open an existing spreadsheet by URL (for resuming across phases)."""
    gc = _get_gspread_client()
    return gc.open_by_url(url)


def add_vertical_tab(
    spreadsheet,
    vertical: str,
    businesses: list[dict],
) -> None:
    """Add a single vertical's data as a new tab to an existing spreadsheet.

    Called after each vertical completes its full pipeline.
    """
    display_name = VERTICAL_DISPLAY_NAMES.get(vertical, vertical)

    # If placeholder tab still exists, rename and use it instead of adding
    try:
        placeholder = spreadsheet.worksheet("_placeholder")
        placeholder.update_title(display_name)
        ws = placeholder
    except gspread.exceptions.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(
            title=display_name,
            rows=max(len(businesses) + 1, 2),
            cols=len(HEADERS),
        )

    rows = [HEADERS] + [_biz_to_row(b) for b in businesses]
    ws.update(rows, value_input_option="USER_ENTERED")
    _apply_formatting(spreadsheet, ws)


def export_to_csv(businesses: list[dict], path: Path | None = None) -> Path:
    """Fallback: export to CSV if Google Sheets credentials unavailable."""
    import csv

    date_str = datetime.now().strftime("%y%m%d")
    out = path or (OUTPUT_DIR / f"sg_ad_intel_{date_str}.csv")

    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        for biz in businesses:
            writer.writerow(_biz_to_row(biz))

    return out


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if "--auth" in sys.argv:
        run_oauth_flow()
        sys.exit(0)

    from dedup import load_deduped

    businesses = load_deduped()
    print(f"Exporting {len(businesses)} businesses...")

    try:
        url = export_to_sheets(businesses)
        print(f"Google Sheet created: {url}")
    except Exception as e:
        print(f"Google Sheets failed ({e}), falling back to CSV...")
        csv_path = export_to_csv(businesses)
        print(f"CSV exported to {csv_path}")
