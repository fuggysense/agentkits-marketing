"""Config loader for the Modal marketing metrics app.

Reads per-client `metrics-config.json` files and resolves credentials from
either a local `.env` or Modal secrets (injected as env vars).
"""

import json
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # Modal runtime may not have python-dotenv
    load_dotenv = None  # type: ignore[assignment]


# Marketing repo root — three levels up from this file (scripts/modal/config_loader.py).
# In Modal, scripts are flattened to /root/ so the parent-relative path breaks;
# prefer the explicit mount at /root/clients when present.
_ROOT = Path(__file__).resolve().parent.parent.parent
_MODAL_CLIENTS_DIR = Path("/root/clients")
_CLIENTS_DIR = _MODAL_CLIENTS_DIR if _MODAL_CLIENTS_DIR.exists() else _ROOT / "clients"

_REQUIRED_TOP_LEVEL = ("client_slug",)
_REQUIRED_PER_CAMPAIGN = ("sheet_id", "ad_platforms", "tabs")
_PLACEHOLDER_PREFIXES = ("{{", "act_XXX", "XXX")
_DEFAULT_CAMPAIGN_SLUG = "default"

# metrics-config.json may live in either the client's `_brand/` folder (current
# convention) or directly at the client root (legacy). Searched in priority order,
# first match wins. This rule applies to every client — no per-client special-casing,
# so moving a client's config into `_brand/` needs no code change here.
_CONFIG_REL_PATHS = ("_brand/metrics-config.json", "metrics-config.json")


def _is_placeholder(value: str) -> bool:
    """Return True if a config value is still a template placeholder."""
    if not value:
        return True
    return any(value.startswith(p) for p in _PLACEHOLDER_PREFIXES)


def _resolve_config_path(client_slug: str) -> Path | None:
    """Return the first existing metrics-config.json for a client, or None.

    Searches `_CONFIG_REL_PATHS` in order so the loader works whether a client
    keeps the file under `_brand/` (current convention) or at the client root
    (legacy) — without any per-client special-casing.
    """
    base = _CLIENTS_DIR / client_slug
    for rel in _CONFIG_REL_PATHS:
        candidate = base / rel
        if candidate.exists():
            return candidate
    return None


def _load_raw_client_file(client_slug: str) -> dict:
    """Load the raw metrics-config.json for a client — no normalisation."""
    config_path = _resolve_config_path(client_slug)
    if config_path is None:
        searched = ", ".join(
            str(_CLIENTS_DIR / client_slug / rel) for rel in _CONFIG_REL_PATHS
        )
        raise FileNotFoundError(
            f"metrics-config.json not found for client '{client_slug}' "
            f"(searched: {searched})"
        )
    try:
        return json.loads(config_path.read_text())
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {config_path}: {e}") from e


def _campaign_entries(raw: dict) -> list[dict]:
    """Return list of campaign blocks from a raw client config.

    Supports two schemas:
      • New (multi-campaign): {"campaigns": [ {campaign_slug, sheet_id, ad_platforms, tabs, ...}, ... ]}
      • Legacy flat (single campaign): {"sheet_id": "...", "ad_platforms": {...}, "tabs": {...}}

    Legacy flat configs are normalised to a single-entry list with
    campaign_slug = "default".
    """
    campaigns = raw.get("campaigns")
    if isinstance(campaigns, list) and campaigns:
        return campaigns

    # Legacy flat — treat the whole config as one campaign block
    return [{
        "campaign_slug": _DEFAULT_CAMPAIGN_SLUG,
        **{k: raw[k] for k in ("sheet_id", "sheet_url", "ad_platforms", "tabs",
                                "anomaly_thresholds", "hitl", "output_snapshots")
           if k in raw},
    }]


def _validate_campaign(client_slug: str, campaign: dict) -> None:
    """Validate a single campaign block has required fields."""
    missing = [f for f in _REQUIRED_PER_CAMPAIGN if f not in campaign]
    if missing:
        cs = campaign.get("campaign_slug", "<unknown>")
        raise ValueError(
            f"Campaign '{cs}' in client '{client_slug}' missing required fields: {missing}"
        )
    if "meta" not in campaign.get("ad_platforms", {}):
        cs = campaign.get("campaign_slug", "<unknown>")
        raise ValueError(
            f"Campaign '{cs}' in client '{client_slug}' missing ad_platforms.meta"
        )


def load_client_config(client_slug: str, campaign_slug: str | None = None) -> dict:
    """Load and validate a single campaign's config.

    Args:
        client_slug: Folder name under `clients/`.
        campaign_slug: Campaign to load. If None:
          - legacy flat configs return as-is (single implicit "default" campaign)
          - new-format configs with one campaign auto-select it
          - new-format configs with multiple campaigns raise ValueError

    Returns:
        Parsed campaign config dict with `client_slug` injected.

    Raises:
        FileNotFoundError: Config file missing.
        ValueError: Required fields missing, or ambiguous campaign selection.
    """
    raw = _load_raw_client_file(client_slug)
    missing_top = [f for f in _REQUIRED_TOP_LEVEL if f not in raw]
    if missing_top:
        raise ValueError(
            f"Config for '{client_slug}' missing required top-level fields: {missing_top}"
        )

    entries = _campaign_entries(raw)

    if campaign_slug is None:
        if len(entries) == 1:
            campaign = entries[0]
        else:
            slugs = [e.get("campaign_slug") for e in entries]
            raise ValueError(
                f"Client '{client_slug}' has multiple campaigns {slugs}; "
                f"pass campaign_slug to disambiguate."
            )
    else:
        matches = [e for e in entries if e.get("campaign_slug") == campaign_slug]
        if not matches:
            slugs = [e.get("campaign_slug") for e in entries]
            raise ValueError(
                f"Campaign '{campaign_slug}' not found for client '{client_slug}'. "
                f"Available: {slugs}"
            )
        campaign = matches[0]

    _validate_campaign(client_slug, campaign)
    # Inject client_slug for downstream convenience
    return {"client_slug": client_slug, **campaign}


def list_active_campaigns() -> list[dict]:
    """Return all active Meta campaigns across every client.

    An entry is "active" iff ad_platforms.meta.enabled == true AND
    ad_account_id is not a placeholder. Works for both legacy flat and new
    campaigns[] configs.

    Returns:
        List of dicts: {"client_slug", "campaign_slug", "config"}.
        `config` is the campaign block with client_slug injected.
    """
    if not _CLIENTS_DIR.exists():
        return []

    out: list[dict] = []
    for child in sorted(_CLIENTS_DIR.iterdir()):
        if not child.is_dir() or child.name == "_template":
            continue
        try:
            raw = _load_raw_client_file(child.name)
        except (FileNotFoundError, ValueError):
            continue

        for campaign in _campaign_entries(raw):
            meta = campaign.get("ad_platforms", {}).get("meta", {})
            if not meta.get("enabled"):
                continue
            ad_account_id = meta.get("ad_account_id", "")
            if _is_placeholder(ad_account_id):
                continue

            # Skip the _template scaffolding key nested inside `tabs`
            # (some templated configs include illustrative blocks with placeholders)
            tabs = campaign.get("tabs", {})
            if any(k.startswith("_") for k in tabs.keys() if isinstance(k, str)):
                # strip helper keys so the downstream code doesn't trip on them
                campaign = {**campaign, "tabs": {k: v for k, v in tabs.items() if not k.startswith("_")}}

            out.append({
                "client_slug": child.name,
                "campaign_slug": campaign.get("campaign_slug", _DEFAULT_CAMPAIGN_SLUG),
                "config": {"client_slug": child.name, **campaign},
            })

    return out


def list_active_clients() -> list[str]:
    """Legacy helper — return unique client slugs with at least one active campaign.

    Kept for backward compat with older callers; prefer list_active_campaigns().
    """
    return sorted({entry["client_slug"] for entry in list_active_campaigns()})


def load_env() -> dict:
    """Load credentials from `.env` (local) or Modal secrets (injected env).

    Returns:
        Dict with META_ADS_ACCESS_TOKEN and GOOGLE_CREDS_JSON.
        Values may be empty strings if not configured.

    Raises:
        RuntimeError: Neither source provides any credentials.
    """
    if load_dotenv is not None:
        env_path = _ROOT / ".env"
        if env_path.exists():
            load_dotenv(env_path)

    token = os.getenv("META_ADS_ACCESS_TOKEN", "")
    creds = os.getenv("GOOGLE_CREDS_JSON", "")

    if not token and not creds:
        raise RuntimeError(
            "Neither META_ADS_ACCESS_TOKEN nor GOOGLE_CREDS_JSON is set. "
            "Configure them in .env locally or as Modal secrets "
            "('meta-ads' and 'google-sheets')."
        )

    return {
        "META_ADS_ACCESS_TOKEN": token,
        "GOOGLE_CREDS_JSON": creds,
    }
