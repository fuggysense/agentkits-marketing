#!/usr/bin/env python3
"""Provision a campaign metrics workbook by cloning tab STRUCTURE from a template.

Why this exists: a bare Google service account CANNOT create Sheets (no Drive of its
own). Creation/cloning runs under a human gcloud user token (Drive scope); the service
account is added as an EDITOR afterwards so the metrics pipeline can write at runtime.
Full background: ../references/sheet-auth.md

What it does:
  1. Auth via `gcloud auth print-access-token` (must carry Drive scope).
  2. For each requested tab, copy it from --source into the destination workbook with
     the Sheets `copyTo` API — preserving formatting, formulas, frozen rows, dimensions.
  3. Rename the copies ("Copy of X" -> "X") and delete any pre-existing/placeholder tabs.
  4. Clear DATA rows below each tab's header rows, so the template client's numbers/copy
     never leak into the new workbook. Header depth = max(frozenRows, 1), per-tab override
     via --keep.
  5. Share with the given accounts (the service account MUST be one of them, as editor).

Examples:
  # Reshape an existing (already-shared) workbook to mirror 9 tabs of a template
  provision_from_template.py \
    --source 14bh8k6S-... --into 1KqWJP... \
    --tabs "DAILY CALLS,WEEKLY CALLS,MONTHLY CALLS,KPIs,APPT,CREATIVES,AVATARS,COPY,OBF DATA" \
    --keep "APPT=2" \
    --share "neezanizam@neezanizam-492212.iam.gserviceaccount.com=writer,ops@1upsalesai.com=writer"

  # Create a brand-new workbook from a template
  provision_from_template.py --source 14bh8k6S-... --title "THOMSON RESERVE | Buyers" \
    --tabs "CREATIVES,COPY" --share "neezanizam@...=writer"
"""
import argparse
import json
import subprocess
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def gcloud_token() -> str:
    tok = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
    info = subprocess.check_output(
        ["curl", "-s", f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={tok}"],
        text=True,
    )
    if "auth/drive" not in info:
        sys.exit("gcloud token lacks Drive scope. Run: gcloud auth login --enable-gdrive-access")
    return tok


def col_letter(n: int) -> str:
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def main() -> None:
    ap = argparse.ArgumentParser(description="Clone tab structure from a template workbook.")
    ap.add_argument("--source", required=True, help="template spreadsheet id")
    ap.add_argument("--tabs", required=True, help="comma-separated source tab names to clone")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--into", help="existing destination spreadsheet id (reshape in place)")
    g.add_argument("--title", help="title for a NEW destination workbook")
    ap.add_argument("--share", default="", help='comma list of email=role (role: writer|reader)')
    ap.add_argument("--keep", default="", help='per-tab header rows to KEEP, e.g. "APPT=2,DAILY CALLS=2"')
    ap.add_argument("--no-clear", action="store_true", help="copy data too (do not clear rows below headers)")
    args = ap.parse_args()

    tabs = [t.strip() for t in args.tabs.split(",") if t.strip()]
    keep_override = {}
    for kv in (k for k in args.keep.split(",") if k.strip()):
        name, _, num = kv.rpartition("=")
        keep_override[name.strip()] = int(num)

    creds = Credentials(token=gcloud_token())
    sheets = build("sheets", "v4", credentials=creds, cache_discovery=False)
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    # source tab name -> {sheetId, frozenRows}
    src_meta = sheets.spreadsheets().get(spreadsheetId=args.source).execute()
    src = {}
    for s in src_meta["sheets"]:
        p = s["properties"]
        src[p["title"]] = {"id": p["sheetId"], "frozen": p.get("gridProperties", {}).get("frozenRowCount", 0)}
    missing = [t for t in tabs if t not in src]
    if missing:
        sys.exit(f"tabs not found in source: {missing}")

    # destination: existing or new
    if args.into:
        dest_id = args.into
        dmeta = sheets.spreadsheets().get(spreadsheetId=dest_id).execute()
        dest_url = dmeta["properties"].get("title")
        old_tab_ids = [s["properties"]["sheetId"] for s in dmeta["sheets"]]
    else:
        created = sheets.spreadsheets().create(
            body={"properties": {"title": args.title}},
            fields="spreadsheetId,spreadsheetUrl,sheets(properties(sheetId))",
        ).execute()
        dest_id = created["spreadsheetId"]
        dest_url = created["spreadsheetUrl"]
        old_tab_ids = [s["properties"]["sheetId"] for s in created["sheets"]]  # the default Sheet1

    # 1) copy each tab in, capturing its new sheetId + dims
    new_props = {}
    for t in tabs:
        cp = sheets.spreadsheets().sheets().copyTo(
            spreadsheetId=args.source, sheetId=src[t]["id"],
            body={"destinationSpreadsheetId": dest_id},
        ).execute()
        new_props[t] = cp  # {sheetId,title="Copy of T",gridProperties{rowCount,columnCount,frozenRowCount}}

    # 2) rename copies -> original names; 3) delete placeholders/default tabs
    requests = []
    for t, cp in new_props.items():
        requests.append({"updateSheetProperties": {
            "properties": {"sheetId": cp["sheetId"], "title": t}, "fields": "title"}})
    for sid in old_tab_ids:
        requests.append({"deleteSheet": {"sheetId": sid}})
    sheets.spreadsheets().batchUpdate(spreadsheetId=dest_id, body={"requests": requests}).execute()

    # 4) clear data rows below the header rows
    if not args.no_clear:
        clear_ranges = []
        for t, cp in new_props.items():
            gp = cp.get("gridProperties", {})
            rows, cols = gp.get("rowCount", 1000), gp.get("columnCount", 26)
            keep = keep_override.get(t, max(src[t]["frozen"], 1))
            if rows > keep:
                clear_ranges.append(f"'{t}'!A{keep+1}:{col_letter(cols)}{rows}")
        if clear_ranges:
            sheets.spreadsheets().values().batchClear(
                spreadsheetId=dest_id, body={"ranges": clear_ranges}).execute()

    # 5) share
    for pair in (p for p in args.share.split(",") if p.strip()):
        email, _, role = pair.rpartition("=")
        try:
            drive.permissions().create(
                fileId=dest_id, sendNotificationEmail=False,
                body={"type": "user", "role": role or "writer", "emailAddress": email.strip()},
            ).execute()
        except HttpError as e:
            print(f"  share {email}: FAILED {str(e)[:120]}", file=sys.stderr)

    # report
    final = sheets.spreadsheets().get(spreadsheetId=dest_id).execute()
    gids = {s["properties"]["title"]: s["properties"]["sheetId"] for s in final["sheets"]}
    print(json.dumps({
        "spreadsheet_id": dest_id,
        "url": f"https://docs.google.com/spreadsheets/d/{dest_id}/edit",
        "title": final["properties"]["title"],
        "tab_gids": gids,
    }, indent=2))


if __name__ == "__main__":
    main()
