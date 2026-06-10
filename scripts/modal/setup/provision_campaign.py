"""End-to-end campaign provisioner.

One command handles every new-campaign scenario:
  1. New client + new campaign   → scaffolds client folder, creates sheet, provisions tabs, writes config
  2. Existing client + new campaign  → creates new sheet, provisions tabs, migrates config to campaigns[] format, appends
  3. Existing client + existing campaign  → updates that campaign's tab gids (idempotent)

What this does NOT do:
  • Full client onboarding (icp.md, offer.md, brand-voice.md) — use /project:new for that
  • Meta ad account creation or campaign launch — you create the campaign in Meta Ads Manager first, then run this
  • Sharing the new sheet — pass --share-email to share with a viewer/editor

Usage:
    python3 scripts/modal/setup/provision_campaign.py \\
        --client-slug neezanizam \\
        --campaign-slug buyer-funnel \\
        --label BuyerFunnel \\
        --ad-account-id act_837789749619954 \\
        --meta-campaign-id 4048596882097890

Flags:
    --sheet-id <id>       Use existing sheet instead of creating a new one
    --share-email <email> Share the new sheet as editor (e.g. jerel@...)
    --force               Overwrite existing campaign block with same slug

The script is idempotent: re-running skips existing tabs and replaces the
campaign entry if --force is set.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(_REPO_ROOT / ".env")

sys.path.insert(0, str(_REPO_ROOT / "scripts" / "modal"))
sys.path.insert(0, str(_REPO_ROOT / "scripts" / "modal" / "setup"))

from sheets_writer import SheetsWriter  # noqa: E402
from provision_lp_tabs import (  # noqa: E402
    COLUMNS as LP_COLUMNS,
    _create_one_tab,
)

_CLIENTS_DIR = _REPO_ROOT / "clients"
_DEFAULT_CAMPAIGN_SLUG = "default"

# Columns shared across all LP funnel tabs — keep in sync with provision_lp_tabs.COLUMNS
_LP_COLUMN_NAMES = [c[0] for c in LP_COLUMNS]


# ── Sheet operations ────────────────────────────────────────────────────────


def _build_writer() -> SheetsWriter:
    creds_path = os.environ.get("GOOGLE_SHEETS_CREDS_PATH", "scripts/modal/credentials.json")
    if not os.path.isabs(creds_path):
        creds_path = str(_REPO_ROOT / creds_path)
    return SheetsWriter(service_account_path=creds_path)


def _create_blank_sheet(writer: SheetsWriter, title: str, share_email: str | None) -> tuple:
    """Create a new empty Google Sheet, share if requested, return (sheet, id)."""
    sheet = writer.client.create(title)
    print(f"✓ Created new sheet: '{title}'  (id={sheet.id})")

    if share_email:
        try:
            sheet.share(share_email, perm_type="user", role="writer", notify=False)
            print(f"✓ Shared as editor with {share_email}")
        except Exception as e:  # noqa: BLE001 — best-effort sharing
            print(f"⚠️  Sharing failed: {e}")

    return sheet, sheet.id


def _drop_default_sheet1(sheet) -> None:
    """Remove the auto-created 'Sheet1' tab if still empty."""
    for ws in sheet.worksheets():
        if ws.title == "Sheet1":
            try:
                sheet.del_worksheet(ws)
                print("✓ Removed default 'Sheet1'")
            except Exception as e:  # noqa: BLE001
                print(f"⚠️  Could not remove 'Sheet1': {e}")
            return


# ── Config operations ──────────────────────────────────────────────────────


def _ensure_client_folder(client_slug: str) -> Path:
    """Create the client folder if missing. Returns the folder path."""
    client_dir = _CLIENTS_DIR / client_slug
    if not client_dir.exists():
        client_dir.mkdir(parents=True)
        print(f"✓ Created new client folder: clients/{client_slug}/")
        # Subfolders the cron/snapshots expect
        (client_dir / "metrics").mkdir(exist_ok=True)
    return client_dir


def _load_or_create_config(client_slug: str, config_path: Path) -> dict:
    """Load existing metrics-config.json, or return a fresh one with campaigns[]."""
    if config_path.exists():
        return json.loads(config_path.read_text())
    print(f"✓ No existing config — creating fresh metrics-config.json")
    return {
        "_comment": f"Metrics automation config for {client_slug}. Multi-campaign format (campaigns[] array).",
        "client_slug": client_slug,
        "campaigns": [],
    }


def _migrate_flat_to_campaigns(config: dict) -> dict:
    """Convert a legacy flat config to campaigns[] format (if needed).

    Idempotent: configs already in the new format pass through unchanged.
    """
    if isinstance(config.get("campaigns"), list):
        return config  # already migrated

    legacy_keys = ("sheet_id", "sheet_url", "ad_platforms", "tabs",
                   "anomaly_thresholds", "hitl", "output_snapshots")
    if not any(k in config for k in legacy_keys):
        # Nothing to migrate — just add empty campaigns[]
        config["campaigns"] = []
        return config

    legacy_campaign = {
        "campaign_slug": _DEFAULT_CAMPAIGN_SLUG,
        **{k: config[k] for k in legacy_keys if k in config},
    }

    migrated = {
        "_comment": config.get("_comment", ""),
        "client_slug": config["client_slug"],
        "campaigns": [legacy_campaign],
    }
    print(f"✓ Migrated flat config → campaigns[] format (existing data kept as '{_DEFAULT_CAMPAIGN_SLUG}')")
    return migrated


def _build_lp_tab_spec(tab_name: str, gid: int, date_format: str, source: str, frequency: str) -> dict:
    return {
        "gid": str(gid),
        "name": tab_name,
        "columns": copy.copy(_LP_COLUMN_NAMES),
        "write_mode": "append",
        "frequency": frequency,
        "date_format": date_format,
        "source": source,
        "scope": "campaign_filtered",
        "blank_when_zero_submits": ["CPFS", "LP→FORM CVR", "CLICK→FORM CVR"],
        "blank_when_zero_appt": ["CPA"],
        "manual_columns": ["APPT", "CAPPT", "REVENUE", "NOTES"],
    }


def _build_campaign_entry(
    *,
    campaign_slug: str,
    label: str,
    sheet_id: str,
    ad_account_id: str,
    meta_campaign_id: str | None,
    tab_gids: dict,
) -> dict:
    campaign_filter = {
        "campaign_ids": [meta_campaign_id] if meta_campaign_id else [],
        "campaign_name_match": "",
    }

    return {
        "campaign_slug": campaign_slug,
        "label": label,
        "sheet_id": sheet_id,
        "sheet_url": f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit",
        "ad_platforms": {
            "meta": {
                "enabled": True,
                "ad_account_id": ad_account_id,
                "campaign_filter": campaign_filter,
            },
        },
        "tabs": {
            "lp_funnel": _build_lp_tab_spec(
                tab_name=f"LP-{label}",
                gid=tab_gids["daily"],
                date_format="DD/MM/YY",
                source="meta_insights_lp_funnel",
                frequency="daily",
            ),
            "lp_funnel_weekly": _build_lp_tab_spec(
                tab_name=f"LP-{label}-Weekly",
                gid=tab_gids["weekly"],
                date_format="DD/MM/YY TO DD/MM/YY",
                source="meta_insights_lp_funnel_period",
                frequency="weekly",
            ),
            "lp_funnel_monthly": _build_lp_tab_spec(
                tab_name=f"LP-{label}-Monthly",
                gid=tab_gids["monthly"],
                date_format="MMMM YYYY",
                source="meta_insights_lp_funnel_period",
                frequency="monthly",
            ),
        },
    }


# ── Main ───────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--client-slug", required=True,
                        help="Folder name under clients/ (created if missing)")
    parser.add_argument("--campaign-slug", required=True,
                        help="Campaign identifier (e.g. asset-progression, buyer-funnel)")
    parser.add_argument("--label", required=True,
                        help="Human-friendly label for sheet title + tab names (e.g. BuyerFunnel)")
    parser.add_argument("--ad-account-id", required=True,
                        help="Meta ad account id (act_XXXXXXXX)")
    parser.add_argument("--meta-campaign-id", default="",
                        help="Meta campaign id to filter to. Empty = account-level.")
    parser.add_argument("--sheet-id", default="",
                        help="Existing sheet to use. If omitted, creates a new blank sheet.")
    parser.add_argument("--share-email", default="",
                        help="Share the new sheet with this email as editor")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing campaign block with same slug")
    args = parser.parse_args()

    print()
    print(f"Provisioning campaign: {args.client_slug}/{args.campaign_slug}  ({args.label})")
    print()

    # 1. Client folder
    client_dir = _ensure_client_folder(args.client_slug)
    config_path = client_dir / "metrics-config.json"

    # 2. Sheet (create or use existing)
    writer = _build_writer()
    if args.sheet_id:
        sheet = writer.get_sheet(args.sheet_id)
        sheet_id = args.sheet_id
        print(f"✓ Using existing sheet (id={sheet_id})")
    else:
        title = f"{args.client_slug} — {args.label}"
        sheet, sheet_id = _create_blank_sheet(writer, title, args.share_email or None)

    # 3. Provision the 3 LP funnel tabs
    tab_gids = {}
    for period, suffix in [("daily", ""), ("weekly", "-Weekly"), ("monthly", "-Monthly")]:
        tab_name = f"LP-{args.label}{suffix}"
        tab_gids[period] = _create_one_tab(sheet, tab_name, period)

    # 4. Remove default Sheet1 now that LP tabs exist
    if not args.sheet_id:
        _drop_default_sheet1(sheet)

    # 5. Update metrics-config.json
    config = _load_or_create_config(args.client_slug, config_path)
    config = _migrate_flat_to_campaigns(config)

    new_campaign = _build_campaign_entry(
        campaign_slug=args.campaign_slug,
        label=args.label,
        sheet_id=sheet_id,
        ad_account_id=args.ad_account_id,
        meta_campaign_id=args.meta_campaign_id or None,
        tab_gids=tab_gids,
    )

    existing = [c for c in config["campaigns"] if c.get("campaign_slug") == args.campaign_slug]
    if existing and not args.force:
        print(f"⚠️  Campaign '{args.campaign_slug}' already in config. Re-run with --force to overwrite.")
        print(f"   (tabs were still provisioned/refreshed on the sheet)")
        return

    config["campaigns"] = [c for c in config["campaigns"] if c.get("campaign_slug") != args.campaign_slug]
    config["campaigns"].append(new_campaign)
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n")
    print(f"✓ Wrote {config_path.relative_to(_REPO_ROOT)}")

    # 6. Validate round-trip via load_client_config
    try:
        from config_loader import load_client_config
        load_client_config(args.client_slug, campaign_slug=args.campaign_slug)
        print("✓ Config validates")
    except Exception as e:  # noqa: BLE001
        print(f"⚠️  Config validation failed: {e}")

    print()
    print("🎉 Done. Summary:")
    print(f"  Sheet URL:   https://docs.google.com/spreadsheets/d/{sheet_id}/edit")
    print(f"  Daily tab:   gid {tab_gids['daily']}")
    print(f"  Weekly tab:  gid {tab_gids['weekly']}")
    print(f"  Monthly tab: gid {tab_gids['monthly']}")
    print(f"  Campaign:    {args.client_slug}/{args.campaign_slug}")
    print()
    print("Next: the daily cron (9am SGT) will auto-write the first row tomorrow.")
    print("To test now: modal run scripts/modal/marketing_metrics.py::run_for_client \\")
    print(f"                  --client-slug {args.client_slug} --campaign-slug {args.campaign_slug} --dry-run")


if __name__ == "__main__":
    main()
