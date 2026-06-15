"""10-5-5 sheet writer — maps per-DCT dct.json → CREATIVES + COPY rows.

Originally Thomson-Reserve-specific; generalized 260611 to any 10-5-5 client by
reading sheet_id, tab names, the DCT list, and the service-account credentials path
from the client's _brand/metrics-config.json (`--client` / `--campaign` / `--config`).

Why this exists (not ad_concept_sheet_writer.py):
  The legacy ad_concept_sheet_writer.py reads ONE dct-tracker.json with a `creatives[]`
  array and a 3-2-2 COPY shape (COPY 1/2 + HEADLINE 1/2). 10-5-5 clients have NO
  dct-tracker.json — their data lives in dcts/DCT<NNN>/dct.json (one file per DCT, each
  with an `angles[]` array of 5 + an `image_pool.images[]`). And the method here is 10-5-5
  (5 copies + 5 headlines per DCT). So we remap angles[]→rows fresh.

Mapping (per the contract + clients/neezanizam/CLAUDE.md DCT law):
  CREATIVES tab — ONE row per DCT (= one ad set = one audience). Strategy columns:
    BATCH = DCT id (DCT101..105)
    FORMAT = "Meta Flexible Ad (10-5-5)"
    AD = meta_adset (e.g. TR_DCT101_Flex_5angles)
    MARKET AWARENESS / MARKET SOPHISTICATION = from angle A01 (uniform within a DCT here)
    ANGLE = the 5 angle names joined (the 5 angles that vary inside this DCT)
    PERSONA = avatar
    CANVA LINK = BLANK (no Canva docs for TR — GPT PNGs in dcts/DCT1NN/images/)
    metric cols (STATUS/CTR/CVR/CPA/CALLS/SPEND/DURATION) = untouched (meta_puller's)
  COPY tab — ONE row per DCT, 10-5-5 shape:
    STATUS, COPY 1..5 (= angles[].primary_text), HEADLINE 1..5 (= angles[].headline)
    Copy text moved VERBATIM — never altered.

Modes: dry-run (default, no network) prints the planned payload + per-DCT copy-fill state.
  The live write path is intentionally NOT implemented here yet — gws auth must be valid
  AND all 5 dct.json copy fields committed first. See the report for the live-write command.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import psych_coverage_tally as pct  # noqa: E402  (sibling module in scripts/)

REPO_ROOT = Path(__file__).resolve().parent.parent
# Agency-default service-account creds. Used only as a fallback when the client's
# metrics-config.json names no per-client credentials path — and only with a loud warning.
DEFAULT_CREDENTIALS_PATH = REPO_ROOT / "scripts" / "modal" / "credentials.json"
DCT_DIR_RE = re.compile(r"^DCT\d+$")

# LIVE sheet header verified 260609 via gws +read. The "Why am I testing this?" column
# (index 7) exists on the live CREATIVES tab between ANGLE and PERSONA — keep it.
CREATIVES_HEADER = [
    "BATCH", "STATUS", "FORMAT", "AD", "MARKET AWARENESS",
    "MARKET SOPHISTICATION", "ANGLE", "Why am I testing this?", "PERSONA", "CANVA LINK",
    "CTR", "CVR", "CPA", "CALLS", "SPEND", "DURATION",
]
# Columns this writer fills (strategy only); STATUS + the metric cols stay blank.
CREATIVES_STRATEGY = {"BATCH", "FORMAT", "AD", "MARKET AWARENESS",
                      "MARKET SOPHISTICATION", "ANGLE", "PERSONA", "CANVA LINK",
                      "PSYCH COVERAGE"}

# COPY tab live header was 3-2-2 (BATCH,STATUS,COPY 1,COPY 2,HEADLINE 1,HEADLINE 2);
# widened to 10-5-5 (12 cols) 260609. BATCH is col A (keying column).
COPY_HEADER = [
    "BATCH", "STATUS",
    "COPY 1", "COPY 2", "COPY 3", "COPY 4", "COPY 5",
    "HEADLINE 1", "HEADLINE 2", "HEADLINE 3", "HEADLINE 4", "HEADLINE 5",
]


def effective_creatives_header(dcts: list[dict]) -> list[str]:
    """CREATIVES_HEADER + 'PSYCH COVERAGE', but ONLY when at least one DCT in scope
    carries v2 psych_coverage tags. Untagged waves stay byte-identical (16 cols, A:P)
    and the existing metric columns never shift position — keeps meta_puller's writes safe.
    The psych column is appended at the END (after the metric cols) for the same reason.
    """
    if any(pct.compute_tally(d).get("n_tagged", 0) > 0 for d in dcts):
        return CREATIVES_HEADER + ["PSYCH COVERAGE"]
    return list(CREATIVES_HEADER)


def load_config(client_slug: str, campaign_slug: str, config_override: Path | None) -> dict:
    """Resolve the per-campaign metrics-config block.

    Config location drifted across the 260504 ICM reorg: older clients keep it at the
    client root, reorganised clients moved it under _brand/. Check root first (back-compat),
    then _brand/; first hit wins. --config overrides the search entirely. Then flatten the
    requested campaigns[] entry so callers see config["sheet_id"] / config["tabs"].
    """
    client_dir = REPO_ROOT / "clients" / client_slug
    if config_override is not None:
        config_path = config_override if config_override.exists() else None
        searched = str(config_override)
    else:
        candidate_paths = [
            client_dir / "metrics-config.json",
            client_dir / "_brand" / "metrics-config.json",
        ]
        config_path = next((p for p in candidate_paths if p.exists()), None)
        searched = " or ".join(str(p) for p in candidate_paths)
    if config_path is None:
        sys.exit(
            f"No metrics-config.json found (looked in: {searched}). "
            f"Run /sheets:provision for client '{client_slug}' first."
        )

    raw = json.loads(config_path.read_text())
    if "sheet_id" not in raw and "campaigns" in raw and raw["campaigns"]:
        campaign = next(
            (c for c in raw["campaigns"] if c.get("campaign_slug") == campaign_slug),
            None,
        )
        if not campaign:
            slugs = [c.get("campaign_slug") for c in raw["campaigns"]]
            sys.exit(f"--campaign '{campaign_slug}' not found in {config_path}. Available: {slugs}")
        config = {**raw, **campaign}
    else:
        config = raw

    if not config.get("sheet_id"):
        sys.exit(f"metrics-config for '{campaign_slug}' has no sheet_id (config: {config_path}).")
    tabs = config.get("tabs", {})
    missing = [t for t in ("creatives", "copy") if t not in tabs]
    if missing:
        sys.exit(
            f"metrics-config for '{campaign_slug}' missing required tab entries: {missing}. "
            "This writer needs both 'creatives' and 'copy' tab definitions."
        )
    config["_config_path"] = str(config_path)
    return config


def resolve_credentials(config: dict) -> Path:
    """Pick the service-account credentials file, honoring a per-client path if named.

    metrics-config may name a per-client creds file at provisioning.credentials_path
    (relative to the repo root or absolute). If absent, fall back to the agency-default
    scripts/modal/credentials.json WITH a loud warning naming the SA email in use.
    """
    prov = config.get("provisioning", {})
    raw_path = prov.get("credentials_path")
    if raw_path:
        p = Path(raw_path)
        if not p.is_absolute():
            p = REPO_ROOT / p
        if not p.exists():
            sys.exit(f"provisioning.credentials_path points to a missing file: {p}")
        return p

    # Fallback — loud warning naming the SA email actually in use.
    sa_email = prov.get("service_account", "<not set in metrics-config.provisioning>")
    creds_email = "<unreadable>"
    if DEFAULT_CREDENTIALS_PATH.exists():
        try:
            creds_email = json.loads(DEFAULT_CREDENTIALS_PATH.read_text()).get("client_email", "<no client_email>")
        except (json.JSONDecodeError, OSError):
            pass
    print(
        "⚠️  WARNING: metrics-config names no provisioning.credentials_path — "
        f"falling back to agency-default {DEFAULT_CREDENTIALS_PATH}.\n"
        f"    SA named in config:  {sa_email}\n"
        f"    SA in default creds: {creds_email}",
        file=sys.stderr,
    )
    return DEFAULT_CREDENTIALS_PATH


def discover_dct_ids(dcts_dir: Path) -> list[str]:
    """The DCT list is the dcts/DCT<NNN>/ folders, sorted — not a hardcoded array."""
    return sorted(d.name for d in dcts_dir.iterdir() if d.is_dir() and DCT_DIR_RE.match(d.name))


def load_dct(dcts_dir: Path, dct_id: str) -> dict:
    p = dcts_dir / dct_id / "dct.json"
    if not p.exists():
        raise FileNotFoundError(f"Missing {p}")
    return json.loads(p.read_text())


def angle_copy_state(d: dict) -> tuple[int, int]:
    angles = d.get("angles", [])
    filled = sum(
        1 for a in angles
        if (a.get("headline") or "").strip() and (a.get("primary_text") or "").strip()
    )
    return filled, len(angles)


def build_creatives_row(d: dict) -> dict:
    angles = d.get("angles", [])
    a0 = angles[0] if angles else {}
    angle_names = " | ".join(
        f"{a.get('id')}:{a.get('name')}" for a in angles if a.get("name")
    ) or " | ".join(a.get("id", "") for a in angles)
    return {
        "BATCH": d.get("dct_id", ""),
        "FORMAT": "Meta Flexible Ad (10-5-5)",
        "AD": d.get("meta_adset", ""),
        "MARKET AWARENESS": a0.get("market_awareness", ""),
        "MARKET SOPHISTICATION": a0.get("market_sophistication", ""),
        "ANGLE": angle_names,
        "PERSONA": d.get("avatar", ""),
        "CANVA LINK": "",  # TR has no Canva docs — GPT PNGs only
        "PSYCH COVERAGE": pct.summarize_tally(d),  # v2 coverage aggregate ("" if untagged)
    }


def build_copy_row(d: dict) -> dict:
    angles = d.get("angles", [])
    # pad/truncate to exactly 5
    angles = (angles + [{}] * 5)[:5]
    # STATUS column left BLANK — it is meta_puller's/lifecycle's, not ours.
    row = {"BATCH": d.get("dct_id", ""), "STATUS": ""}
    for i, a in enumerate(angles, start=1):
        row[f"COPY {i}"] = a.get("primary_text", "") or ""
        row[f"HEADLINE {i}"] = a.get("headline", "") or ""
    return row


def _gws_update(spreadsheet_id: str, a1_range: str, values: list[list]) -> dict:
    """values update via gws CLI — body passed as JSON string (handles newlines/commas)."""
    params = json.dumps({
        "spreadsheetId": spreadsheet_id,
        "range": a1_range,
        "valueInputOption": "RAW",
    })
    body = json.dumps({"values": values})
    proc = subprocess.run(
        ["gws", "sheets", "spreadsheets", "values", "update",
         "--params", params, "--json", body, "--format", "json"],
        capture_output=True, text=True,
    )
    out = "\n".join(l for l in proc.stdout.splitlines() if "keyring" not in l)
    if proc.returncode != 0:
        raise RuntimeError(f"gws update failed ({a1_range}): {proc.stderr or out}")
    return json.loads(out) if out.strip() else {}


def live_write(dcts_dir: Path, sheet_id: str, dct_ids: list[str],
               creatives_tab: str, copy_tab: str) -> None:
    dcts = [load_dct(dcts_dir, dct_id) for dct_id in dct_ids]
    cr_header = effective_creatives_header(dcts)
    last_col = chr(ord("A") + len(cr_header) - 1)  # P (16) normally; Q (17) when psych active
    rows_cr, rows_cp = [], []
    for dct_id, d in zip(dct_ids, dcts):
        filled, total = angle_copy_state(d)
        if filled != total or total == 0:
            sys.exit(f"ABORT: {dct_id} copy not 5/5 ({filled}/{total}). Refusing live write.")
        cr = build_creatives_row(d)
        cp = build_copy_row(d)
        rows_cr.append([cr.get(c, "") for c in cr_header])
        rows_cp.append([cp.get(c, "") for c in COPY_HEADER])

    # 1) widen + set COPY header row (12 cols) — overwrites the old 3-2-2 header verbatim
    print(f"Writing COPY header (10-5-5, 12 cols) -> '{copy_tab}'!A1:L1")
    _gws_update(sheet_id, f"'{copy_tab}'!A1:L1", [COPY_HEADER])

    # 1b) only when the psych column is active, label its header cell ALONE — leaves the
    # 260609-verified A1:P1 CREATIVES header untouched, so no metric column ever reorders.
    if len(cr_header) > len(CREATIVES_HEADER):
        print(f"Writing PSYCH COVERAGE header -> '{creatives_tab}'!{last_col}1")
        _gws_update(sheet_id, f"'{creatives_tab}'!{last_col}1", [["PSYCH COVERAGE"]])

    # 2) CREATIVES data rows at A2 (A:{last_col} — 16 cols, or 17 when psych active).
    print(f"Writing {len(rows_cr)} CREATIVES rows -> '{creatives_tab}'!A2:{last_col}{1+len(rows_cr)}")
    _gws_update(sheet_id, f"'{creatives_tab}'!A2:{last_col}{1+len(rows_cr)}", rows_cr)

    # 3) COPY data rows at A2 (12 cols A:L)
    print(f"Writing {len(rows_cp)} COPY rows -> '{copy_tab}'!A2:L{1+len(rows_cp)}")
    _gws_update(sheet_id, f"'{copy_tab}'!A2:L{1+len(rows_cp)}", rows_cp)
    print("LIVE WRITE COMPLETE.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--client", required=True, help="Client slug (e.g. neezanizam)")
    ap.add_argument("--campaign", required=True,
                    help="Folder campaign slug under clients/<client>/campaigns/ (where dcts/ lives)")
    ap.add_argument("--metrics-campaign", default=None,
                    help="metrics-config campaigns[] slug to write against. "
                         "If omitted, defaults to --campaign.")
    ap.add_argument("--config", default=None,
                    help="Explicit path to metrics-config.json. Overrides the "
                         "client-root / _brand/ auto-search.")
    ap.add_argument("--mode", choices=["dry-run", "live"], default="dry-run",
                    help="dry-run: print payload only. live: write to the sheet via gws.")
    args = ap.parse_args()

    dcts_dir = REPO_ROOT / "clients" / args.client / "campaigns" / args.campaign / "dcts"
    if not dcts_dir.exists():
        sys.exit(f"No dcts/ dir at {dcts_dir}")

    metrics_campaign = args.metrics_campaign or args.campaign
    config_override = Path(args.config).expanduser() if args.config else None
    config = load_config(args.client, metrics_campaign, config_override)
    credentials_path = resolve_credentials(config)
    sheet_id = config["sheet_id"]
    creatives_tab = config["tabs"]["creatives"].get("name", "CREATIVES")
    copy_tab = config["tabs"]["copy"].get("name", "COPY")

    dct_ids = discover_dct_ids(dcts_dir)
    if not dct_ids:
        sys.exit(f"No DCT<NNN>/ folders found under {dcts_dir}")

    if args.mode == "live":
        live_write(dcts_dir, sheet_id, dct_ids, creatives_tab, copy_tab)
        return

    print(f"# DRY-RUN — {args.client}/{args.campaign} 10-5-5 sheet payload")
    print(f"# (no sheet read/write performed — auth/copy-commit gated)")
    print(f"# config:      {config['_config_path']}")
    print(f"# metrics-campaign: {metrics_campaign}")
    print(f"# sheet_id:    {sheet_id}")
    print(f"# tabs:        CREATIVES='{creatives_tab}'  COPY='{copy_tab}'")
    print(f"# credentials: {credentials_path}")
    print(f"# DCTs:        {dct_ids}\n")
    dcts = [load_dct(dcts_dir, dct_id) for dct_id in dct_ids]
    cr_header = effective_creatives_header(dcts)
    psych_on = len(cr_header) > len(CREATIVES_HEADER)
    print(f"CREATIVES header ({len(cr_header)} cols): {cr_header}"
          + ("  [PSYCH COVERAGE active — >=1 DCT tagged]" if psych_on else ""))
    print(f"COPY header ({len(COPY_HEADER)} cols): {COPY_HEADER}\n")

    all_ready = True
    for dct_id, d in zip(dct_ids, dcts):
        filled, total = angle_copy_state(d)
        if filled != total or total == 0:
            all_ready = False
        cr = build_creatives_row(d)
        cp = build_copy_row(d)
        pool = d.get("image_pool", {})
        imgs = pool.get("images", []) if isinstance(pool, dict) else []

        print(f"===== {dct_id}  (copy {filled}/{total} filled · {len(imgs)} images) =====")
        if pct.compute_tally(d).get("n_tagged", 0):
            print(pct.format_tally(d))
        print("  CREATIVES row:")
        for col in cr_header:
            val = cr.get(col, "")
            tag = "" if col in CREATIVES_STRATEGY else "  [blank — meta_puller/STATUS]"
            shown = (val[:90] + "…") if isinstance(val, str) and len(val) > 90 else val
            print(f"    {col:<22} = {shown!r}{tag}")
        print("  COPY row:")
        print(f"    STATUS                 = {cp['STATUS']!r}")
        for i in range(1, 6):
            h = cp[f"HEADLINE {i}"]
            c = cp[f"COPY {i}"]
            hs = (h[:60] + "…") if len(h) > 60 else h
            cs = (c[:60] + "…") if len(c) > 60 else c
            print(f"    HEADLINE {i}             = {hs!r}")
            print(f"    COPY {i}                 = {cs!r}")
        print()

    print("-" * 60)
    if all_ready:
        print(f"READY: all {len(dct_ids)} DCTs have full copy. Safe to proceed to live write once auth is valid.")
    else:
        print("HOLD: one or more DCTs still PENDING_COPY (orchestrator writing copy in parallel).")
        print("Do NOT live-write until every DCT shows 5/5 copy filled.")


if __name__ == "__main__":
    main()
