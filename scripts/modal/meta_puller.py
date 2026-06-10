"""Meta Marketing API puller for daily account + per-ad insights.

Graph API v22.0. Uses a long-lived user or system-user access token.
Handles rate limit (200 calls / hour / user), token expiry, and invalid
account errors with retries and clear messages.
"""

from __future__ import annotations

import json
import re
import time
from typing import Any

import requests


META_API_VERSION = "v22.0"
META_API_BASE = f"https://graph.facebook.com/{META_API_VERSION}"

# Meta's documented action_type keys we care about
ACTION_LEADS = "lead"
ACTION_APPOINTMENTS = "schedule"  # "Schedule" custom conversion / standard event
ACTION_PURCHASES = "purchase"
ACTION_LANDING_PAGE_VIEW = "landing_page_view"

# Batch ID regex — matches DCT followed by digits (e.g. DCT1, DCT42)
BATCH_ID_PATTERN = re.compile(r"DCT\d+")

# Retry/backoff
MAX_RETRIES = 4
INITIAL_BACKOFF = 5  # seconds
RATE_LIMIT_BACKOFF = 60  # seconds when Meta says slow down


class MetaAPIError(RuntimeError):
    """Raised when the Meta Graph API returns an unrecoverable error."""


class MetaAdsPuller:
    """Pulls insights from Meta Marketing API for a single ad account."""

    def __init__(self, access_token: str, ad_account_id: str) -> None:
        if not access_token:
            raise RuntimeError(
                "META_ADS_ACCESS_TOKEN not set. See setup in plan."
            )
        if not ad_account_id:
            raise RuntimeError("ad_account_id required (format: act_XXXXXXXX).")

        self.access_token = access_token
        # Normalise: Meta expects `act_<id>` in the path
        self.ad_account_id = (
            ad_account_id if ad_account_id.startswith("act_") else f"act_{ad_account_id}"
        )

    # ── Public API ──────────────────────────────────────────────────────────

    def get_daily_account_insights(self, date: str) -> dict:
        """Get aggregated account-level insights for a single day.

        Args:
            date: ISO date string (YYYY-MM-DD).

        Returns:
            Dict with keys: date, spend, impressions, clicks, ctr, cpm, leads,
            appointments, revenue, cvr, cpl, cpoc, octr.
        """
        params = {
            "fields": (
                "spend,impressions,clicks,ctr,cpm,"
                "actions,action_values,outbound_clicks,outbound_clicks_ctr"
            ),
            "time_range": f'{{"since":"{date}","until":"{date}"}}',
            "level": "account",
        }
        data = self._get(f"/{self.ad_account_id}/insights", params)
        rows = data.get("data", [])
        if not rows:
            return self._empty_daily_row(date)
        return self._parse_daily_row(rows[0], date)

    def get_per_ad_insights(self, since: str, until: str) -> list[dict]:
        """Get per-ad insights for a date range.

        Args:
            since: ISO date (YYYY-MM-DD) inclusive start.
            until: ISO date (YYYY-MM-DD) inclusive end.

        Returns:
            List of dicts: {ad_id, name, status, batch_id, ctr, cvr, cpa,
            calls, spend, duration_days}.
        """
        time_range = f'{{"since":"{since}","until":"{until}"}}'
        params = {
            "fields": (
                "id,name,status,created_time,"
                "insights.time_range(" + time_range + "){"
                "spend,impressions,clicks,ctr,actions,cost_per_action_type"
                "}"
            ),
            "limit": 100,
        }

        ads: list[dict] = []
        url = f"{META_API_BASE}/{self.ad_account_id}/ads"
        page_params: dict[str, Any] = {**params, "access_token": self.access_token}

        while True:
            payload = self._request("GET", url, params=page_params)
            for ad in payload.get("data", []):
                ads.append(self._parse_ad_row(ad, since, until))
            paging = payload.get("paging", {})
            next_url = paging.get("next")
            if not next_url:
                break
            # For paging we hit the next URL directly; params already baked in
            url = next_url
            page_params = {}

        return ads

    def get_period_lp_funnel_insights(
        self,
        since: str,
        until: str,
        campaign_ids: list[str] | None = None,
    ) -> dict:
        """Get LP-funnel-shaped insights for an arbitrary date range.

        Used for weekly + monthly rollups. Single API call so REACH reflects
        true uniques across the period (not summed daily reach which overcounts).

        Args:
            since: ISO start date (YYYY-MM-DD), inclusive.
            until: ISO end date (YYYY-MM-DD), inclusive.
            campaign_ids: Optional campaign filter.

        Returns:
            Same dict shape as get_daily_lp_funnel_insights — keyed by canonical
            LP funnel field names. The 'date' field carries `since` for caller use.
        """
        params = {
            "fields": (
                "spend,impressions,reach,inline_link_clicks,clicks,"
                "ctr,cpc,cpm,actions"
            ),
            "time_range": f'{{"since":"{since}","until":"{until}"}}',
            "level": "account",
        }
        if campaign_ids:
            params["filtering"] = json.dumps([{
                "field": "campaign.id",
                "operator": "IN",
                "value": list(campaign_ids),
            }])

        data = self._get(f"/{self.ad_account_id}/insights", params)
        rows = data.get("data", [])
        if not rows:
            return self._empty_lp_funnel_row(since)
        return self._parse_lp_funnel_row(rows[0], since)

    def get_daily_lp_funnel_insights(
        self,
        date: str,
        campaign_ids: list[str] | None = None,
    ) -> dict:
        """Get LP-funnel-shaped insights for a single day.

        Pulls reach, inline_link_clicks, cpc, landing_page_view, lead — the
        fields needed for an external-LP conversion funnel. Optionally filters
        to specific campaigns.

        Args:
            date: ISO date string (YYYY-MM-DD).
            campaign_ids: List of campaign IDs to filter to. If None or empty,
                          returns account-level totals.

        Returns:
            Dict keyed by canonical LP funnel field names (see _parse_lp_funnel_row).
            All ratio metrics stored as decimal fractions (sheet cells formatted as %).
        """
        params = {
            "fields": (
                "spend,impressions,reach,inline_link_clicks,clicks,"
                "ctr,cpc,cpm,actions"
            ),
            "time_range": f'{{"since":"{date}","until":"{date}"}}',
            "level": "account",
        }
        if campaign_ids:
            params["filtering"] = json.dumps([{
                "field": "campaign.id",
                "operator": "IN",
                "value": list(campaign_ids),
            }])

        data = self._get(f"/{self.ad_account_id}/insights", params)
        rows = data.get("data", [])
        if not rows:
            return self._empty_lp_funnel_row(date)
        return self._parse_lp_funnel_row(rows[0], date)

    @staticmethod
    def extract_batch_id(ad_name: str) -> str | None:
        """Extract the DCT batch id from an ad name, e.g. 'DCT3 - HL1 - C2'."""
        if not ad_name:
            return None
        match = BATCH_ID_PATTERN.search(ad_name)
        return match.group(0) if match else None

    # ── HTTP + error handling ───────────────────────────────────────────────

    def _get(self, path: str, params: dict) -> dict:
        """GET wrapper that injects access_token and handles retries."""
        url = f"{META_API_BASE}{path}"
        merged = {**params, "access_token": self.access_token}
        return self._request("GET", url, params=merged)

    def _request(self, method: str, url: str, params: dict | None = None) -> dict:
        """Send an HTTP request with retry/backoff for rate limits and 5xx."""
        backoff = INITIAL_BACKOFF
        last_error: Exception | None = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = requests.request(method, url, params=params, timeout=60)
            except requests.RequestException as e:
                last_error = e
                time.sleep(backoff)
                backoff *= 2
                continue

            if resp.status_code == 200:
                return resp.json()

            # Parse Meta error payload if possible
            try:
                err = resp.json().get("error", {})
            except ValueError:
                err = {}
            code = err.get("code")
            subcode = err.get("error_subcode")
            message = err.get("message", resp.text[:400])

            # 190 = invalid/expired token. Don't retry — fail loud.
            if code == 190:
                raise MetaAPIError(
                    f"Meta access token invalid or expired (code 190): {message}. "
                    "Refresh META_ADS_ACCESS_TOKEN."
                )

            # 100 / subcode 33 = nonexistent object (bad ad account id)
            if code == 100 and subcode == 33:
                raise MetaAPIError(
                    f"Ad account {self.ad_account_id} not found or no access. "
                    f"Check ad_account_id in metrics-config.json. ({message})"
                )

            # 17 / 4 / 613 = user request limit hit — back off longer
            if code in (4, 17, 32, 613):
                wait = RATE_LIMIT_BACKOFF * attempt
                last_error = MetaAPIError(f"Rate limited (code {code}): {message}")
                time.sleep(wait)
                continue

            # 5xx — retry with backoff
            if 500 <= resp.status_code < 600:
                last_error = MetaAPIError(
                    f"Meta API {resp.status_code} on attempt {attempt}: {message}"
                )
                time.sleep(backoff)
                backoff *= 2
                continue

            # Other 4xx — fail loud
            raise MetaAPIError(
                f"Meta API error {resp.status_code} "
                f"(code={code}, subcode={subcode}): {message}"
            )

        raise MetaAPIError(
            f"Meta API request failed after {MAX_RETRIES} attempts: {last_error}"
        )

    # ── Parsing helpers ─────────────────────────────────────────────────────

    @staticmethod
    def _sum_action(actions: list[dict], key: str) -> float:
        """Sum values for a given action_type across the `actions` array."""
        if not actions:
            return 0.0
        total = 0.0
        for action in actions:
            if action.get("action_type") == key:
                try:
                    total += float(action.get("value", 0))
                except (TypeError, ValueError):
                    continue
        return total

    @staticmethod
    def _safe_float(value: Any, default: float = 0.0) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _safe_div(num: float, denom: float) -> float:
        return (num / denom) if denom else 0.0

    def _empty_lp_funnel_row(self, date: str) -> dict:
        """Empty LP funnel dict — used when Meta returns no data for the day."""
        return {
            "date": date,
            "spend": 0.0,
            "impressions": 0,
            "reach": 0,
            "link_clicks": 0,
            "lp_views": 0,
            "ctr": 0.0,
            "cpc": 0.0,
            "cpm": 0.0,
            "cplv": 0.0,
            "form_submits": 0,
            "cpfs": 0.0,
            "lp_to_form_cvr": 0.0,
            "click_to_form_cvr": 0.0,
        }

    def _parse_lp_funnel_row(self, row: dict, date: str) -> dict:
        """Convert one Meta insights row into LP funnel canonical dict.

        All ratio metrics returned as decimal fractions (e.g. 0.0163 = 1.63%).
        Sheet cells formatted as percentage will display correctly.
        """
        spend = self._safe_float(row.get("spend"))
        impressions = int(self._safe_float(row.get("impressions")))
        reach = int(self._safe_float(row.get("reach")))
        link_clicks = int(self._safe_float(row.get("inline_link_clicks")))
        # Compute CTR/CPC from LINK clicks (not all clicks) for lead-gen funnels.
        # Meta's `ctr`/`cpc` fields use all-click denominators which don't align
        # with what the SUMMARY row aggregates. Recompute from link_clicks here
        # so daily rows and summary stay consistent.
        ctr = self._safe_div(link_clicks, impressions)
        cpc = self._safe_div(spend, link_clicks)
        cpm = self._safe_float(row.get("cpm"))

        actions = row.get("actions", []) or []
        lp_views = int(self._sum_action(actions, ACTION_LANDING_PAGE_VIEW))
        form_submits = int(self._sum_action(actions, ACTION_LEADS))

        # Derived metrics — all decimal fractions for ratios
        cplv = self._safe_div(spend, lp_views)
        cpfs = self._safe_div(spend, form_submits)
        lp_to_form = self._safe_div(form_submits, lp_views)
        click_to_form = self._safe_div(form_submits, link_clicks)

        return {
            "date": date,
            "spend": round(spend, 2),
            "impressions": impressions,
            "reach": reach,
            "link_clicks": link_clicks,
            "lp_views": lp_views,
            "ctr": round(ctr, 6),
            "cpc": round(cpc, 2),
            "cpm": round(cpm, 2),
            "cplv": round(cplv, 2),
            "form_submits": form_submits,
            "cpfs": round(cpfs, 2),
            "lp_to_form_cvr": round(lp_to_form, 6),
            "click_to_form_cvr": round(click_to_form, 6),
        }

    def _empty_daily_row(self, date: str) -> dict:
        return {
            "date": date,
            "spend": 0.0,
            "impressions": 0,
            "clicks": 0,
            "ctr": 0.0,
            "cpm": 0.0,
            "leads": 0,
            "appointments": 0,
            "revenue": 0.0,
            "cvr": 0.0,
            "cpl": 0.0,
            "cpoc": 0.0,
            "octr": 0.0,
        }

    def _parse_daily_row(self, row: dict, date: str) -> dict:
        """Convert one Meta insights row into our canonical daily dict."""
        spend = self._safe_float(row.get("spend"))
        impressions = int(self._safe_float(row.get("impressions")))
        clicks = int(self._safe_float(row.get("clicks")))
        # Meta returns CTR already in percentage form (e.g. 2.96 = 2.96%).
        # Store as decimal fraction so sheet cells formatted as % render correctly.
        ctr = self._safe_float(row.get("ctr")) / 100
        cpm = self._safe_float(row.get("cpm"))

        actions = row.get("actions", []) or []
        action_values = row.get("action_values", []) or []

        leads = int(self._sum_action(actions, ACTION_LEADS))
        appointments = int(self._sum_action(actions, ACTION_APPOINTMENTS))
        revenue = self._sum_action(action_values, ACTION_PURCHASES)

        outbound_clicks_list = row.get("outbound_clicks", []) or []
        outbound_clicks = 0
        for entry in outbound_clicks_list:
            if entry.get("action_type") == "outbound_click":
                outbound_clicks += int(self._safe_float(entry.get("value")))

        octr_list = row.get("outbound_clicks_ctr", []) or []
        octr = 0.0
        for entry in octr_list:
            if entry.get("action_type") == "outbound_click":
                # Meta returns OCTR in percentage form; store as fraction.
                octr = self._safe_float(entry.get("value")) / 100
                break

        return {
            "date": date,
            "spend": round(spend, 2),
            "impressions": impressions,
            "clicks": clicks,
            "ctr": round(ctr, 4),
            "cpm": round(cpm, 2),
            "leads": leads,
            "appointments": appointments,
            "revenue": round(revenue, 2),
            "cvr": round(self._safe_div(leads, clicks), 6),
            "cpl": round(self._safe_div(spend, leads), 2),
            "cpoc": round(self._safe_div(spend, outbound_clicks), 2),
            "octr": round(octr, 6),
        }

    def _parse_ad_row(self, ad: dict, since: str, until: str) -> dict:
        """Flatten a nested ad + insights object into our per-ad dict."""
        name = ad.get("name", "")
        insights_rows = ((ad.get("insights") or {}).get("data") or [])
        insights = insights_rows[0] if insights_rows else {}

        spend = self._safe_float(insights.get("spend"))
        clicks = int(self._safe_float(insights.get("clicks")))
        # Meta returns CTR in percent form; store as fraction for sheet % cells.
        ctr = self._safe_float(insights.get("ctr")) / 100

        actions = insights.get("actions", []) or []
        leads = int(self._sum_action(actions, ACTION_LEADS))
        appointments = int(self._sum_action(actions, ACTION_APPOINTMENTS))
        calls = leads  # "calls" in sheet == lead conversions in Meta parlance

        # Cost per action — prefer Meta's own cost_per_action_type.lead when present
        cpa = 0.0
        for entry in insights.get("cost_per_action_type", []) or []:
            if entry.get("action_type") == ACTION_LEADS:
                cpa = self._safe_float(entry.get("value"))
                break
        if cpa == 0.0:
            cpa = self._safe_div(spend, leads)

        # Duration in days: clamp the requested window, fall back to ad age
        try:
            from datetime import date as _date
            s = _date.fromisoformat(since)
            u = _date.fromisoformat(until)
            duration_days = max((u - s).days + 1, 1)
        except ValueError:
            duration_days = 1

        return {
            "ad_id": ad.get("id", ""),
            "name": name,
            "status": ad.get("status", ""),
            "batch_id": self.extract_batch_id(name),
            "ctr": round(ctr, 6),
            "cvr": round(self._safe_div(leads, clicks), 6),
            "cpa": round(cpa, 2),
            "calls": calls,
            "spend": round(spend, 2),
            "duration_days": duration_days,
            "appointments": appointments,
        }
