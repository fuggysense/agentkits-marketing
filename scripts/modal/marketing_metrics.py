"""Modal app: marketing-metrics.

Three scheduled functions pull Meta Ads data and write to per-client
Google Sheets. Each run iterates active clients, catches per-client errors
so one failure doesn't block the rest, and logs a snapshot to
`clients/<slug>/metrics/` for audit.

Run modes:
  • Scheduled (cron)  — `daily_metrics`, `weekly_aggregation`, `monthly_aggregation`
  • Manual (local)    — `modal run marketing_metrics.py::run_for_client --client-slug aura`
"""

from __future__ import annotations

import json
import os
import traceback
from datetime import date, datetime, timedelta
from pathlib import Path

import modal


APP_NAME = "marketing-metrics"

# Marketing repo root — three levels up from this file
_ROOT = Path(__file__).resolve().parent.parent.parent
_LOCAL_CLIENTS_DIR = _ROOT / "clients"

# ── Modal image + mounts ────────────────────────────────────────────────────

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "requests>=2.31",
        "gspread>=6.0",
        "google-auth>=2.28",
        "google-api-python-client>=2.120",
        "python-dotenv>=1.0",
    )
    .add_local_python_source("config_loader", "meta_puller", "sheets_writer", "aggregator")
    .add_local_dir(_LOCAL_CLIENTS_DIR, remote_path="/root/clients")
)

app = modal.App(APP_NAME, image=image)

meta_secret = modal.Secret.from_name("meta-ads")
sheets_secret = modal.Secret.from_name("google-sheets")


# ── Shared helpers ──────────────────────────────────────────────────────────


def _log(msg: str) -> None:
    """Timestamped stdout logger (picked up by Modal dashboard)."""
    print(f"[{datetime.utcnow().isoformat(timespec='seconds')}Z] {msg}", flush=True)


def _snapshot_dir(client_slug: str) -> Path:
    """Return (and create) the metrics snapshot dir for a client."""
    # In Modal the mount is at /root/clients; locally it's the repo path.
    root_candidates = [Path("/root/clients"), _LOCAL_CLIENTS_DIR]
    root = next((p for p in root_candidates if p.exists()), _LOCAL_CLIENTS_DIR)
    out = root / client_slug / "metrics"
    out.mkdir(parents=True, exist_ok=True)
    return out


def _save_snapshot(client_slug: str, campaign_slug: str, kind: str, payload: dict) -> Path:
    """Save a JSON snapshot for audit/debugging.

    Filename encodes the campaign so one client with multiple campaigns doesn't
    collide: `<campaign>_<kind>_<stamp>.json`.
    """
    stamp = datetime.utcnow().strftime("%y%m%d_%H%M%S")
    out = _snapshot_dir(client_slug) / f"{campaign_slug}_{kind}_{stamp}.json"
    out.write_text(json.dumps(payload, indent=2, default=str))
    return out


def _build_sheets_writer():
    """Construct a SheetsWriter from GOOGLE_CREDS_JSON env var."""
    from sheets_writer import SheetsWriter

    creds_json = os.getenv("GOOGLE_CREDS_JSON", "")
    if not creds_json:
        raise RuntimeError(
            "GOOGLE_CREDS_JSON not set. Configure the 'google-sheets' Modal secret."
        )
    return SheetsWriter(service_account_json=creds_json)


def _build_meta_puller(ad_account_id: str):
    """Construct a MetaAdsPuller from META_ADS_ACCESS_TOKEN env var."""
    from meta_puller import MetaAdsPuller

    token = os.getenv("META_ADS_ACCESS_TOKEN", "")
    if not token:
        raise RuntimeError(
            "META_ADS_ACCESS_TOKEN not set. Configure the 'meta-ads' Modal secret."
        )
    return MetaAdsPuller(access_token=token, ad_account_id=ad_account_id)


# ── Per-client workers ──────────────────────────────────────────────────────


def _run_daily_for_client(
    client_slug: str,
    campaign_slug: str,
    config: dict,
    target_date: str,
    dry_run: bool = False,
) -> dict:
    """Pull yesterday's Meta metrics and append to DAILY CALLS + update CREATIVES."""
    sheet_id = config["sheet_id"]
    ad_account_id = config["ad_platforms"]["meta"]["ad_account_id"]

    puller = _build_meta_puller(ad_account_id)
    writer = _build_sheets_writer()

    # Account-level daily insights
    daily = puller.get_daily_account_insights(target_date)

    # Map canonical keys → DAILY CALLS column names
    daily_row = {
        "DATE": datetime.fromisoformat(target_date).strftime("%d/%m/%y"),
        "LEAD": daily["leads"],
        "CPL": daily["cpl"],
        "APPT": 0,  # filled manually by client
        "CAPPT": 0,  # filled manually by client
        "REVENUE": daily["revenue"],
        "AMOUNT SPENT": daily["spend"],
        "CVR": daily["cvr"],
        "CPM": daily["cpm"],
        "CPOC": daily["cpoc"],
        "OCTR": daily["octr"],
        "NOTES": "",
    }

    # Per-ad insights for the same day → CREATIVES metric columns
    ad_rows = puller.get_per_ad_insights(target_date, target_date)

    snapshot = {
        "client_slug": client_slug,
        "campaign_slug": campaign_slug,
        "target_date": target_date,
        "daily_row": daily_row,
        "ad_rows": ad_rows,
    }
    _save_snapshot(client_slug, campaign_slug, "daily", snapshot)

    if dry_run:
        _log(f"[{client_slug}/{campaign_slug}] dry_run=True — skipping sheet writes")
        return snapshot

    sheet = writer.get_sheet(sheet_id)

    # DAILY CALLS write — DISABLED. Replaced by LP-AssetProgression tab below.
    # The DAILY CALLS tab still exists in the sheet as historical reference,
    # but new daily rows are no longer appended. To re-enable, restore this block.
    # daily_cfg = config["tabs"]["daily_calls"]
    # daily_tab = writer.get_tab(sheet, daily_cfg["gid"])
    # writer.append_row(daily_tab, daily_row, daily_cfg["columns"])

    # CREATIVES updates (keyed by batch_id)
    creatives_cfg = config["tabs"]["creatives"]
    creatives_tab = writer.get_tab(sheet, creatives_cfg["gid"])
    metric_cols = creatives_cfg.get("metric_columns", [])
    protected_cols = creatives_cfg.get("protected_columns", [])

    # Aggregate ad-level metrics up to the batch
    by_batch: dict[str, dict] = {}
    for ad in ad_rows:
        batch_id = ad.get("batch_id")
        if not batch_id:
            continue
        bucket = by_batch.setdefault(
            batch_id,
            {"spend": 0.0, "calls": 0, "impressions": 0, "clicks": 0, "status": ad.get("status", "")},
        )
        bucket["spend"] += ad["spend"]
        bucket["calls"] += ad["calls"]
        # status: any ACTIVE wins over PAUSED
        if ad.get("status") == "ACTIVE":
            bucket["status"] = "ACTIVE"

    for batch_id, agg in by_batch.items():
        updates = {col: agg.get(col.lower(), "") for col in metric_cols if col.lower() in agg}
        # CTR/CVR/CPA — recompute from totals where possible
        if "CTR" in metric_cols:
            updates["CTR"] = 0  # per-ad only; leave 0 until we collect impressions
        if "SPEND" in metric_cols:
            updates["SPEND"] = round(agg["spend"], 2)
        if "CALLS" in metric_cols:
            updates["CALLS"] = agg["calls"]
        if "CPA" in metric_cols:
            updates["CPA"] = round(agg["spend"] / agg["calls"], 2) if agg["calls"] else 0
        if "STATUS" in metric_cols:
            updates["STATUS"] = agg["status"]
        try:
            writer.update_metric_columns(
                creatives_tab, batch_id, updates, protected_cols
            )
        except ValueError as e:
            _log(f"[{client_slug}/{campaign_slug}] skip batch {batch_id}: {e}")

    # LP funnel tab — campaign-filtered, new schema (only if configured)
    lp_cfg = config.get("tabs", {}).get("lp_funnel")
    if lp_cfg:
        _write_lp_funnel_row(
            client_slug=client_slug,
            campaign_slug=campaign_slug,
            target_date=target_date,
            puller=puller,
            writer=writer,
            sheet=sheet,
            meta_cfg=config["ad_platforms"]["meta"],
            lp_cfg=lp_cfg,
        )

    return snapshot


def _write_lp_funnel_row(
    *,
    client_slug: str,
    campaign_slug: str,
    target_date: str,
    puller,
    writer,
    sheet,
    meta_cfg: dict,
    lp_cfg: dict,
) -> None:
    """Pull campaign-filtered LP funnel insights and append to the LP tab.

    Applies the blank-cell rule: ratio columns dependent on form submits
    render blank (not 0 or "$0.00") when no submits were captured.
    """
    campaign_ids = (
        meta_cfg.get("campaign_filter", {}).get("campaign_ids") or None
    )
    lp = puller.get_daily_lp_funnel_insights(target_date, campaign_ids=campaign_ids)

    submits = lp["form_submits"]
    appt = 0  # manual entry — written empty, client fills in later
    blank_no_submits = set(lp_cfg.get("blank_when_zero_submits", []))
    blank_no_appt = set(lp_cfg.get("blank_when_zero_appt", []))

    def _blank_or(value, key: str):
        if key in blank_no_submits and submits == 0:
            return ""
        if key in blank_no_appt and appt == 0:
            return ""
        return value

    # Send ISO date so Sheets parses unambiguously regardless of locale.
    # The LP-AssetProgression DATE column is formatted as DD/MM/YY for display.
    row = {
        "DATE":             target_date,  # ISO YYYY-MM-DD
        "SPEND":            lp["spend"],
        "FORM SUBMITS":     submits if submits else "",
        "CPFS":             _blank_or(lp["cpfs"], "CPFS"),
        "LP→FORM CVR":      _blank_or(lp["lp_to_form_cvr"], "LP→FORM CVR"),
        "APPT":             "",  # manual
        "CAPPT":            "",  # manual
        "CPA":              _blank_or("", "CPA"),  # derived from manual APPT
        "REVENUE":          "",  # manual
        "IMPRESSIONS":      lp["impressions"],
        "REACH":            lp["reach"],
        "LINK CLICKS":      lp["link_clicks"],
        "LP VIEWS":         lp["lp_views"],
        "CTR":              lp["ctr"],
        "CPC":              lp["cpc"],
        "CPM":              lp["cpm"],
        "CPLV":             lp["cplv"],
        "CLICK→FORM CVR":   _blank_or(lp["click_to_form_cvr"], "CLICK→FORM CVR"),
        "NOTES":            "",
    }

    _save_snapshot(client_slug, campaign_slug, "lp_funnel", {"target_date": target_date, "row": row, "raw": lp})

    lp_tab = writer.get_tab(sheet, lp_cfg["gid"])
    writer.append_row(lp_tab, row, lp_cfg["columns"])
    _log(f"[{client_slug}/{campaign_slug}] LP funnel row appended for {target_date}")


def _write_lp_funnel_period_row(
    *,
    client_slug: str,
    campaign_slug: str,
    since: str,
    until: str,
    period_label: str,
    snapshot_kind: str,
    puller,
    writer,
    sheet,
    meta_cfg: dict,
    period_cfg: dict,
) -> dict:
    """Pull period-scoped LP funnel insights and append to a weekly/monthly tab.

    Single Meta API call for the [since, until] window so REACH is true unique
    audience for the period (not summed daily reach which overcounts).
    """
    campaign_ids = (
        meta_cfg.get("campaign_filter", {}).get("campaign_ids") or None
    )
    lp = puller.get_period_lp_funnel_insights(since, until, campaign_ids=campaign_ids)

    submits = lp["form_submits"]
    blank_no_submits = set(period_cfg.get("blank_when_zero_submits", []))
    blank_no_appt = set(period_cfg.get("blank_when_zero_appt", []))

    def _blank_or(value, key):
        if key in blank_no_submits and submits == 0:
            return ""
        if key in blank_no_appt:
            return ""  # APPT manual + always 0 from API
        return value

    row = {
        "DATE":             period_label,
        "SPEND":            lp["spend"],
        "FORM SUBMITS":     submits if submits else "",
        "CPFS":             _blank_or(lp["cpfs"], "CPFS"),
        "LP→FORM CVR":      _blank_or(lp["lp_to_form_cvr"], "LP→FORM CVR"),
        "APPT":             "",
        "CAPPT":            "",
        "CPA":              "",
        "REVENUE":          "",
        "IMPRESSIONS":      lp["impressions"],
        "REACH":            lp["reach"],
        "LINK CLICKS":      lp["link_clicks"],
        "LP VIEWS":         lp["lp_views"],
        "CTR":              lp["ctr"],
        "CPC":              lp["cpc"],
        "CPM":              lp["cpm"],
        "CPLV":             lp["cplv"],
        "CLICK→FORM CVR":   _blank_or(lp["click_to_form_cvr"], "CLICK→FORM CVR"),
        "NOTES":            "",
    }

    _save_snapshot(client_slug, campaign_slug, snapshot_kind, {
        "since": since, "until": until, "label": period_label, "row": row, "raw": lp,
    })

    tab = writer.get_tab(sheet, period_cfg["gid"])
    writer.append_row(tab, row, period_cfg["columns"])
    _log(f"[{client_slug}/{campaign_slug}] LP funnel {snapshot_kind} row appended ({period_label})")
    return row


def _run_weekly_for_client(
    client_slug: str,
    campaign_slug: str,
    config: dict,
    dry_run: bool = False,
) -> dict:
    """Aggregate last 7 daily rows into one WEEKLY CALLS row."""
    from aggregator import MetricsAggregator

    writer = _build_sheets_writer()
    aggregator = MetricsAggregator()

    today = date.today()
    week_end = today - timedelta(days=1)  # yesterday
    week_start = week_end - timedelta(days=6)  # 7-day window

    sheet = writer.get_sheet(config["sheet_id"])

    # Legacy DAILY CALLS aggregation — only if both tabs exist in this campaign's config
    legacy_daily_cfg = config.get("tabs", {}).get("daily_calls")
    legacy_weekly_cfg = config.get("tabs", {}).get("weekly_calls")
    has_legacy = bool(legacy_daily_cfg and legacy_weekly_cfg)

    if has_legacy:
        daily_tab = writer.get_tab(sheet, legacy_daily_cfg["gid"])
        weekly_tab = writer.get_tab(sheet, legacy_weekly_cfg["gid"])
        daily_rows = aggregator.pull_daily_rows_for_week(
            writer, daily_tab, week_start.isoformat(), week_end.isoformat()
        )
        weekly_row = aggregator.aggregate_daily_to_weekly(
            daily_rows, week_start.isoformat(), week_end.isoformat()
        )
    else:
        daily_rows = []
        weekly_row = None

    snapshot = {
        "client_slug": client_slug,
        "campaign_slug": campaign_slug,
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "daily_rows_in_range": len(daily_rows),
        "weekly_row": weekly_row,
    }
    _save_snapshot(client_slug, campaign_slug, "weekly", snapshot)

    if dry_run:
        _log(f"[{client_slug}/{campaign_slug}] dry_run=True — skipping weekly write")
        return snapshot

    if has_legacy and weekly_row is not None:
        writer.append_row(
            weekly_tab,
            weekly_row,
            legacy_weekly_cfg["columns"],
        )

    # LP funnel weekly — period-scoped Meta API call (not aggregated from daily)
    lp_weekly_cfg = config.get("tabs", {}).get("lp_funnel_weekly")
    if lp_weekly_cfg:
        meta_cfg = config["ad_platforms"]["meta"]
        puller = _build_meta_puller(meta_cfg["ad_account_id"])
        period_label = f"{week_start.strftime('%d/%m/%y')} TO {week_end.strftime('%d/%m/%y')}"
        _write_lp_funnel_period_row(
            client_slug=client_slug,
            campaign_slug=campaign_slug,
            since=week_start.isoformat(),
            until=week_end.isoformat(),
            period_label=period_label,
            snapshot_kind="lp_funnel_weekly",
            puller=puller,
            writer=writer,
            sheet=sheet,
            meta_cfg=meta_cfg,
            period_cfg=lp_weekly_cfg,
        )

    return snapshot


def _run_monthly_for_client(
    client_slug: str,
    campaign_slug: str,
    config: dict,
    dry_run: bool = False,
) -> dict:
    """Aggregate last month's weekly rows into one MONTHLY CALLS row."""
    from aggregator import MetricsAggregator

    writer = _build_sheets_writer()
    aggregator = MetricsAggregator()

    today = date.today()
    # Last full calendar month
    first_of_this_month = today.replace(day=1)
    last_month_end = first_of_this_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    month_name = last_month_start.strftime("%B")

    sheet = writer.get_sheet(config["sheet_id"])

    # Legacy WEEKLY→MONTHLY aggregation — only if both tabs exist
    legacy_weekly_cfg = config.get("tabs", {}).get("weekly_calls")
    legacy_monthly_cfg = config.get("tabs", {}).get("monthly_calls")
    has_legacy = bool(legacy_weekly_cfg and legacy_monthly_cfg)

    if has_legacy:
        weekly_tab = writer.get_tab(sheet, legacy_weekly_cfg["gid"])
        monthly_tab = writer.get_tab(sheet, legacy_monthly_cfg["gid"])
        all_weekly = writer.read_all_rows(weekly_tab)
        month_start_str = last_month_start.strftime("/%m/%y")
        in_range = [r for r in all_weekly if month_start_str in str(r.get("DATE", ""))]
        monthly_row = aggregator.aggregate_weekly_to_monthly(in_range, month_name)
    else:
        in_range = []
        monthly_row = None

    snapshot = {
        "client_slug": client_slug,
        "campaign_slug": campaign_slug,
        "month": month_name,
        "weekly_rows_in_range": len(in_range),
        "monthly_row": monthly_row,
    }
    _save_snapshot(client_slug, campaign_slug, "monthly", snapshot)

    if dry_run:
        _log(f"[{client_slug}/{campaign_slug}] dry_run=True — skipping monthly write")
        return snapshot

    if has_legacy and monthly_row is not None:
        writer.append_row(
            monthly_tab,
            monthly_row,
            legacy_monthly_cfg["columns"],
        )

    # LP funnel monthly — period-scoped Meta API call
    lp_monthly_cfg = config.get("tabs", {}).get("lp_funnel_monthly")
    if lp_monthly_cfg:
        meta_cfg = config["ad_platforms"]["meta"]
        puller = _build_meta_puller(meta_cfg["ad_account_id"])
        period_label = last_month_start.strftime("%B %Y")
        _write_lp_funnel_period_row(
            client_slug=client_slug,
            campaign_slug=campaign_slug,
            since=last_month_start.isoformat(),
            until=last_month_end.isoformat(),
            period_label=period_label,
            snapshot_kind="lp_funnel_monthly",
            puller=puller,
            writer=writer,
            sheet=sheet,
            meta_cfg=meta_cfg,
            period_cfg=lp_monthly_cfg,
        )

    return snapshot


# ── Orchestration ───────────────────────────────────────────────────────────


def _fan_out(worker, label: str, **kwargs) -> dict:
    """Run `worker(client_slug, campaign_slug, config, **kwargs)` across every
    active (client, campaign) pair. Each failure is isolated so one broken
    campaign doesn't block the rest.
    """
    from config_loader import list_active_campaigns

    entries = list_active_campaigns()
    _log(f"{label}: processing {len(entries)} active campaigns across {len({e['client_slug'] for e in entries})} clients")

    successes: list[str] = []
    failures: list[dict] = []

    for entry in entries:
        client_slug = entry["client_slug"]
        campaign_slug = entry["campaign_slug"]
        config = entry["config"]
        tag = f"{client_slug}/{campaign_slug}"
        try:
            worker(client_slug, campaign_slug, config, **kwargs)
            successes.append(tag)
            _log(f"{label} [{tag}] OK")
        except Exception as e:  # noqa: BLE001 — we want per-campaign isolation
            failures.append({"client_slug": client_slug, "campaign_slug": campaign_slug, "error": str(e)})
            _log(f"{label} [{tag}] FAIL: {e}")
            _log(traceback.format_exc())

    summary = {
        "campaigns_processed": len(entries),
        "successes": successes,
        "failures": failures,
    }
    _log(f"{label} complete: {summary}")
    return summary


# ── Scheduled entrypoints ───────────────────────────────────────────────────


@app.function(
    schedule=modal.Cron("0 1 * * *"),  # 1am UTC = 9am SGT
    secrets=[meta_secret, sheets_secret],
    timeout=60 * 30,
)
def daily_metrics() -> dict:
    """Daily cron: pull yesterday's Meta data for every active (client, campaign)."""
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    def worker(client_slug: str, campaign_slug: str, config: dict, **_: object) -> None:
        _run_daily_for_client(client_slug, campaign_slug, config, yesterday, dry_run=False)

    return _fan_out(worker, label="daily_metrics")


@app.function(
    schedule=modal.Cron("0 2 * * 0"),  # Sun 2am UTC = 10am SGT
    secrets=[meta_secret, sheets_secret],
    timeout=60 * 30,
)
def weekly_aggregation() -> dict:
    """Weekly cron: roll last 7 daily rows into one WEEKLY CALLS row per campaign."""

    def worker(client_slug: str, campaign_slug: str, config: dict, **_: object) -> None:
        _run_weekly_for_client(client_slug, campaign_slug, config, dry_run=False)

    return _fan_out(worker, label="weekly_aggregation")


@app.function(
    schedule=modal.Cron("0 2 1 * *"),  # 1st of month 2am UTC = 10am SGT
    secrets=[meta_secret, sheets_secret],
    timeout=60 * 30,
)
def monthly_aggregation() -> dict:
    """Monthly cron: roll last month's weekly rows into one MONTHLY CALLS row per campaign."""

    def worker(client_slug: str, campaign_slug: str, config: dict, **_: object) -> None:
        _run_monthly_for_client(client_slug, campaign_slug, config, dry_run=False)

    return _fan_out(worker, label="monthly_aggregation")


# ── Manual invocation ───────────────────────────────────────────────────────


@app.local_entrypoint()
def run_for_client(
    client_slug: str,
    period: str = "daily",
    target_date: str = "",
    dry_run: bool = False,
    campaign_slug: str = "",
) -> None:
    """Run a single client/campaign's pipeline manually from the CLI.

    Usage:
        modal run marketing_metrics.py::run_for_client --client-slug aura
        modal run marketing_metrics.py::run_for_client \\
            --client-slug aura --period weekly --dry-run
        modal run marketing_metrics.py::run_for_client \\
            --client-slug neezanizam --campaign-slug asset-progression

    Args:
        client_slug: Folder name under clients/.
        period: "daily" | "weekly" | "monthly".
        target_date: ISO date for daily runs. Defaults to yesterday.
        dry_run: If True, fetch + log but don't write to the sheet.
        campaign_slug: Specific campaign to run. If empty, auto-selects the
                       single campaign (legacy or one-campaign configs) or
                       errors if multiple exist.
    """
    run_in_modal.remote(client_slug, period, target_date, dry_run, campaign_slug)


@app.function(secrets=[meta_secret, sheets_secret], timeout=60 * 20)
def run_in_modal(
    client_slug: str,
    period: str,
    target_date: str,
    dry_run: bool,
    campaign_slug: str = "",
) -> dict:
    """Inner implementation of run_for_client (runs inside Modal)."""
    from config_loader import load_client_config

    # Resolve campaign — empty string → None → auto-select
    cs = campaign_slug or None
    config = load_client_config(client_slug, campaign_slug=cs)
    resolved_slug = config.get("campaign_slug", "default")

    _log(
        f"Manual run: {client_slug}/{resolved_slug} period={period} "
        f"target_date={target_date or '(auto)'} dry_run={dry_run}"
    )

    match period:
        case "daily":
            td = target_date or (date.today() - timedelta(days=1)).isoformat()
            return _run_daily_for_client(client_slug, resolved_slug, config, td, dry_run=dry_run)
        case "weekly":
            return _run_weekly_for_client(client_slug, resolved_slug, config, dry_run=dry_run)
        case "monthly":
            return _run_monthly_for_client(client_slug, resolved_slug, config, dry_run=dry_run)
        case _:
            raise ValueError(
                f"Unknown period '{period}'. Use 'daily', 'weekly', or 'monthly'."
            )
