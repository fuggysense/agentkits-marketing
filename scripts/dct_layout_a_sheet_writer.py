"""Layout-A 10-5-5 sheet writer — per-DCT row with ANGLE1…5 split into 5 columns.

Sibling of dct_10_5_5_sheet_writer.py. Same client family (10-5-5 Meta Flex), same
COPY tab, same service-account auth — but a DIFFERENT CREATIVES shape and a DIFFERENT
write strategy. Built 260617 to close the canonical-writer gap behind handoff decision #5
(Eugene Chieng sheet = "Layout A"). The shared config/auth/COPY logic is IMPORTED from
dct_10_5_5_sheet_writer (one source of truth) — only the Layout-A delta lives here.

What "Layout A" is (verified against Eugene's live sheet 260617 via the per-client SA):
  CREATIVES tab — 20 cols. Col A header is a literal SPACE (the BATCH key column),
    then STATUS, FORMAT, AD, MARKET AWARENESS, MARKET SOPHISTICATION,
    ANGLE1, ANGLE2, ANGLE3, ANGLE4, ANGLE5  ← the 5 angles each get their OWN column
    (this is the only structural difference from dct_10_5_5_sheet_writer, which joins
     the 5 angle names into ONE "ANGLE" cell), then "Why am I testing this?", PERSONA,
    CANVA LINK, then the metric cols CTR / CVR / CPA / CALLS / SPEND / DURATION.
  COPY tab — 12 cols, BYTE-IDENTICAL to the 10-5-5 COPY tab
    (BATCH, STATUS, COPY 1..5, HEADLINE 1..5). Reused verbatim via the base writer.

Write strategy = per-DCT UPSERT (not the base writer's full-wave rewrite):
  Each DCT is one row, keyed by its dct_id in col A. We find-or-append that row and write
  ONLY the strategy block — never STATUS, never the metric columns. This is what lets a
  NEW DCT join the sheet without disturbing rows already standing (e.g. DCT002, which was
  hand-populated 260610 and must not be touched).
    CREATIVES: write A (batch) + C:N (FORMAT … CANVA LINK, 12 cells). B (STATUS) and
               O:T (metrics) are left exactly as found — meta_puller / the operator own them.
    COPY:      write A (batch) + C:L (COPY 1..5, HEADLINE 1..5, 10 cells). B (STATUS) left as found.
  Copy text moves VERBATIM — never altered.

DCT discovery is folder-name agnostic: any subdir of dcts/ that contains a dct.json is a
DCT, and the BATCH key is read from dct.json's "dct_id" field (Eugene names folders
dct-002-math-blind, not DCT101 — the base writer's ^DCT\\d+$ regex would miss those).

Derived strategy columns (from dct.json, no fabrication):
  FORMAT                 = "Meta Flexible Ad (10-5-5)" (the method, like the base writer)
  AD                     = dct.json meta_adset
  MARKET AWARENESS       = distinct angle market_awareness values, with counts if mixed
  MARKET SOPHISTICATION  = distinct angle market_sophistication values, with counts if mixed
  ANGLE1..5              = '<id> - <name> ("<headline>")' per angle (matches the live row)
  Why am I testing this? = dct.json set_hypothesis | why_am_i_testing_this (set-level; "" if absent)
  PERSONA                = dct.json avatar
  CANVA LINK             = dct.json canva_link

Modes: dry-run (default) is network-free — prints the planned payload + per-DCT copy state,
  determines INSERT-vs-UPDATE only at live time. live (--mode live) validates the live header
  is actually Layout A (fail-closed if not), gates on every targeted DCT being 5/5 copy, then
  upserts via the service account (gspread, RAW). No human login, ever.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dct_10_5_5_sheet_writer as base  # noqa: E402  shared config/auth/COPY logic

# CREATIVES Layout-A header (20 cols) — verified against Eugene's live sheet 260617.
# Col A header is a literal space (" "); it is the BATCH key column regardless of label.
CREATIVES_HEADER_A = [
    " ", "STATUS", "FORMAT", "AD", "MARKET AWARENESS", "MARKET SOPHISTICATION",
    "ANGLE1", "ANGLE2", "ANGLE3", "ANGLE4", "ANGLE5",
    "Why am I testing this?", "PERSONA", "CANVA LINK",
    "CTR", "CVR", "CPA", "CALLS", "SPEND", "DURATION",
]
# The strategy block we actually write, in sheet order, columns C:N (FORMAT … CANVA LINK).
STRATEGY_COLS_A = [
    "FORMAT", "AD", "MARKET AWARENESS", "MARKET SOPHISTICATION",
    "ANGLE1", "ANGLE2", "ANGLE3", "ANGLE4", "ANGLE5",
    "Why am I testing this?", "PERSONA", "CANVA LINK",
]
# COPY data block in sheet order, columns C:L (the base 12-col COPY header minus BATCH+STATUS).
COPY_DATA_COLS = [
    "COPY 1", "COPY 2", "COPY 3", "COPY 4", "COPY 5",
    "HEADLINE 1", "HEADLINE 2", "HEADLINE 3", "HEADLINE 4", "HEADLINE 5",
]


def angle_cell(a: dict) -> str:
    """One ANGLE column: '<id> - <name> ("<headline>")' — matches Eugene's live DCT002 row."""
    aid = (a.get("id") or "").strip()
    name = (a.get("name") or "").strip()
    headline = (a.get("headline") or "").strip()
    if not (aid or name or headline):
        return ""
    label = " - ".join(p for p in (aid, name) if p)
    return f'{label} ("{headline}")' if headline else label


def summarize_dim(angles: list[dict], key: str) -> str:
    """Distinct angle values for `key`, order-preserving. Single value → plain;
    mixed → 'val (xN); val2 (xM)'. Deterministic, no fabrication."""
    counts: "OrderedDict[str, int]" = OrderedDict()
    for a in angles:
        v = (a.get(key) or "").strip()
        if v:
            counts[v] = counts.get(v, 0) + 1
    if not counts:
        return ""
    if len(counts) == 1:
        return next(iter(counts))
    return "; ".join(f"{v} (x{n})" for v, n in counts.items())


def build_creatives_strategy_a(d: dict) -> list[str]:
    """The 12 CREATIVES strategy cells for columns C:N."""
    angles_raw = d.get("angles", [])
    angles = (angles_raw + [{}] * 5)[:5]  # pad/truncate to exactly 5 angle columns
    vals = {
        "FORMAT": "Meta Flexible Ad (10-5-5)",
        "AD": d.get("meta_adset", "") or "",
        "MARKET AWARENESS": summarize_dim(angles_raw, "market_awareness"),
        "MARKET SOPHISTICATION": summarize_dim(angles_raw, "market_sophistication"),
        "ANGLE1": angle_cell(angles[0]),
        "ANGLE2": angle_cell(angles[1]),
        "ANGLE3": angle_cell(angles[2]),
        "ANGLE4": angle_cell(angles[3]),
        "ANGLE5": angle_cell(angles[4]),
        "Why am I testing this?": (
            d.get("set_hypothesis") or d.get("why_am_i_testing_this") or ""
        ),
        "PERSONA": d.get("avatar", "") or "",
        "CANVA LINK": d.get("canva_link", "") or "",
    }
    return [vals[c] for c in STRATEGY_COLS_A]


def build_copy_data_a(d: dict) -> list[str]:
    """The 10 COPY cells for columns C:L (COPY 1..5, HEADLINE 1..5) — reuses the base row builder."""
    cp = base.build_copy_row(d)  # verbatim copy text, never altered
    return [cp.get(c, "") for c in COPY_DATA_COLS]


def discover_dct_dirs(dcts_dir: Path) -> list[str]:
    """Folder-name agnostic: any subdir of dcts/ that holds a dct.json. Sorted."""
    return sorted(
        d.name for d in dcts_dir.iterdir() if d.is_dir() and (d / "dct.json").exists()
    )


def validate_layout_a(cre_header: list[str], copy_header: list[str]) -> list[str]:
    """Confirm the live sheet really is Layout A before any write. Returns problems (empty = ok)."""
    problems: list[str] = []
    expect_angles = ["ANGLE1", "ANGLE2", "ANGLE3", "ANGLE4", "ANGLE5"]
    # Anchor the left edge (cols C:F) too, not just the ANGLE block — otherwise a
    # horizontally shifted sheet with an intact ANGLE1..5 run would pass and then the
    # C:N write would land mis-aligned.
    expect_left = ["FORMAT", "AD", "MARKET AWARENESS", "MARKET SOPHISTICATION"]
    if cre_header[2:6] != expect_left:
        problems.append(
            f"CREATIVES cols C:F must be {expect_left}, found {cre_header[2:6]!r}"
        )
    if cre_header[6:11] != expect_angles:
        problems.append(
            f"CREATIVES cols G:K must be {expect_angles}, found {cre_header[6:11]!r}"
        )
    if "CANVA LINK" not in cre_header:
        problems.append("CREATIVES header has no 'CANVA LINK' column")
    if copy_header[:12] != base.COPY_HEADER:
        problems.append(
            f"COPY header must be the 10-5-5 shape {base.COPY_HEADER}, found {copy_header[:12]!r}"
        )
    return problems


def _col_a_index(ws) -> tuple[dict[str, int], int]:
    """Map non-empty col-A value → 1-indexed row; plus the true next append row.

    Append row is computed from the LAST row that holds any value across the whole grid,
    not len(col_values(1)) — gspread's col_values truncates at the last non-empty col-A
    cell, so a row pre-seeded with STATUS/metrics but a blank col A (or a blank row above
    real data) could otherwise be appended ON TOP of. We always land strictly below all
    existing content so a new batch key can never inherit another row's STATUS/metrics.
    """
    grid = ws.get_all_values()
    idx: dict[str, int] = {}
    last_used = 0
    for i, row in enumerate(grid, start=1):
        key = (row[0] if row else "").strip()
        if key:
            idx[key] = i
        if any((c or "").strip() for c in row):
            last_used = i
    return idx, last_used + 1


def init_headers(sheet_id: str, creatives_tab: str, copy_tab: str, credentials_path: Path) -> None:
    """Stamp the Layout-A headers onto a sheet (one-time, when converting a sheet TO Layout A).

    Writes CREATIVES row 1 = the 20-col Layout-A header (col A is a literal space, ANGLE1..5
    split, metric tail) and COPY row 1 = the 12-col 10-5-5 header. Header row ONLY — never
    touches data rows. After this, the normal live upsert (which validates the header) will run.
    """
    sa_email = json.loads(credentials_path.read_text()).get("client_email", "<unknown>")
    print(f"Auth: service account {sa_email} (gspread) — no human login")
    sheet = base._open_sheet(credentials_path).get_sheet(sheet_id)
    print(f"Stamping CREATIVES Layout-A header (20 cols) -> '{creatives_tab}'!A1:T1")
    base._sa_update(sheet, f"'{creatives_tab}'!A1:T1", [CREATIVES_HEADER_A])
    print(f"Stamping COPY 10-5-5 header (12 cols) -> '{copy_tab}'!A1:L1")
    base._sa_update(sheet, f"'{copy_tab}'!A1:L1", [base.COPY_HEADER])
    print("HEADERS STAMPED.")


def live_write(dcts_dir: Path, sheet_id: str, dct_folders: list[str],
               creatives_tab: str, copy_tab: str, credentials_path: Path) -> None:
    pairs = [(f, base.load_dct(dcts_dir, f)) for f in dct_folders]

    # Copy-completeness gate — refuse the whole write if any targeted DCT is below 5/5.
    for folder, d in pairs:
        filled, total = base.angle_copy_state(d)
        if filled != total or total == 0:
            sys.exit(
                f"ABORT: {d.get('dct_id', folder)} copy not 5/5 ({filled}/{total}). "
                "Refusing live write."
            )

    sa_email = json.loads(credentials_path.read_text()).get("client_email", "<unknown>")
    print(f"Auth: service account {sa_email} (gspread) — no human login")
    sheet = base._open_sheet(credentials_path).get_sheet(sheet_id)
    cre_ws = sheet.worksheet(creatives_tab)
    copy_ws = sheet.worksheet(copy_tab)

    problems = validate_layout_a(cre_ws.row_values(1), copy_ws.row_values(1))
    if problems:
        sys.exit("ABORT: target sheet is not Layout A —\n  - " + "\n  - ".join(problems))

    cre_idx, cre_next = _col_a_index(cre_ws)
    copy_idx, copy_next = _col_a_index(copy_ws)

    for folder, d in pairs:
        bid = (d.get("dct_id", "") or "").strip() or folder

        cr = cre_idx.get(bid)
        if cr is None:
            cr = cre_next
            cre_next += 1
            cre_idx[bid] = cr
            cr_action = "APPEND"
        else:
            cr_action = "UPDATE"
        strat = build_creatives_strategy_a(d)
        if len(strat) != 12:
            sys.exit(f"BUG: CREATIVES strategy row for {bid} is {len(strat)} cells, expected 12 (C:N).")
        base._sa_update(sheet, f"'{creatives_tab}'!A{cr}", [[bid]])
        base._sa_update(sheet, f"'{creatives_tab}'!C{cr}:N{cr}", [strat])

        cp = copy_idx.get(bid)
        if cp is None:
            cp = copy_next
            copy_next += 1
            copy_idx[bid] = cp
            cp_action = "APPEND"
        else:
            cp_action = "UPDATE"
        copy_data = build_copy_data_a(d)
        if len(copy_data) != 10:
            sys.exit(f"BUG: COPY data row for {bid} is {len(copy_data)} cells, expected 10 (C:L).")
        base._sa_update(sheet, f"'{copy_tab}'!A{cp}", [[bid]])
        base._sa_update(sheet, f"'{copy_tab}'!C{cp}:L{cp}", [copy_data])

        print(
            f"  {bid}: CREATIVES {cr_action} row {cr} (A + C:N) · "
            f"COPY {cp_action} row {cp} (A + C:L) — STATUS + metrics untouched"
        )
    print("LIVE WRITE COMPLETE.")


def _preview(dcts_dir: Path, dct_folders: list[str], creatives_tab: str, copy_tab: str,
             sheet_id: str, credentials_path: Path, config_path: str) -> None:
    print(f"# DRY-RUN — Layout A 10-5-5 sheet payload")
    print(f"# (no sheet read/write — INSERT vs UPDATE row is decided at live time by BATCH upsert)")
    print(f"# config:      {config_path}")
    print(f"# sheet_id:    {sheet_id}")
    print(f"# tabs:        CREATIVES='{creatives_tab}'  COPY='{copy_tab}'")
    print(f"# credentials: {credentials_path}")
    print(f"# DCTs:        {dct_folders}\n")
    print(f"CREATIVES write footprint: A (BATCH) + C:N (12 strategy cols) — "
          f"STATUS (B) + metrics (O:T) left as found")
    print(f"COPY write footprint:      A (BATCH) + C:L (10 cells) — STATUS (B) left as found\n")

    all_ready = True
    for folder in dct_folders:
        d = base.load_dct(dcts_dir, folder)
        bid = (d.get("dct_id", "") or "").strip() or folder
        filled, total = base.angle_copy_state(d)
        if filled != total or total == 0:
            all_ready = False
        strat = build_creatives_strategy_a(d)
        copy_data = build_copy_data_a(d)

        print(f"===== {bid}  (folder {folder} · copy {filled}/{total} filled) =====")
        print("  CREATIVES strategy (C:N):")
        for col, val in zip(STRATEGY_COLS_A, strat):
            shown = (val[:90] + "…") if isinstance(val, str) and len(val) > 90 else val
            print(f"    {col:<22} = {shown!r}")
        print("  COPY (C:L):")
        for col, val in zip(COPY_DATA_COLS, copy_data):
            shown = (val[:70] + "…") if isinstance(val, str) and len(val) > 70 else val
            print(f"    {col:<12} = {shown!r}")
        print()

    print("-" * 60)
    if all_ready:
        print(f"READY: all {len(dct_folders)} DCT(s) have full 5/5 copy. Safe to live-write.")
    else:
        print("HOLD: one or more DCTs below 5/5 copy. live mode will ABORT until every DCT is 5/5.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--client", required=True, help="Client slug (e.g. eugene-chieng)")
    ap.add_argument("--campaign", required=True,
                    help="Folder campaign slug under clients/<client>/campaigns/ (where dcts/ lives)")
    ap.add_argument("--metrics-campaign", default=None,
                    help="metrics-config campaigns[] slug to write against. Defaults to --campaign.")
    ap.add_argument("--dct", default=None,
                    help="Target a single DCT folder (e.g. dct-003-foo). Default: all discovered DCTs.")
    ap.add_argument("--config", default=None,
                    help="Explicit path to metrics-config.json (overrides client-root / _brand/ auto-search).")
    ap.add_argument("--mode", choices=["dry-run", "live"], default="dry-run",
                    help="dry-run: print payload only. live: upsert to the sheet via the service account.")
    ap.add_argument("--init-headers", action="store_true",
                    help="One-time: stamp the Layout-A headers (CREATIVES 20-col + COPY 12-col) onto "
                         "the sheet when converting it TO Layout A. Header row only. Needs --mode live to write.")
    args = ap.parse_args()

    dcts_dir = base.REPO_ROOT / "clients" / args.client / "campaigns" / args.campaign / "dcts"
    if not dcts_dir.exists():
        sys.exit(f"No dcts/ dir at {dcts_dir}")

    metrics_campaign = args.metrics_campaign or args.campaign
    config_override = Path(args.config).expanduser() if args.config else None
    config = base.load_config(args.client, metrics_campaign, config_override)
    credentials_path = base.resolve_credentials(config)
    sheet_id = config["sheet_id"]
    creatives_tab = config["tabs"]["creatives"].get("name", "CREATIVES")
    copy_tab = config["tabs"]["copy"].get("name", "COPY")

    if args.init_headers:
        if args.mode != "live":
            print("# DRY-RUN init-headers (no write). Would stamp:")
            print(f"#   '{creatives_tab}'!A1:T1 = {CREATIVES_HEADER_A}")
            print(f"#   '{copy_tab}'!A1:L1 = {base.COPY_HEADER}")
            return
        init_headers(sheet_id, creatives_tab, copy_tab, credentials_path)
        return

    if args.dct:
        if not (dcts_dir / args.dct / "dct.json").exists():
            sys.exit(f"--dct '{args.dct}' has no dct.json under {dcts_dir}")
        dct_folders = [args.dct]
    else:
        dct_folders = discover_dct_dirs(dcts_dir)
    if not dct_folders:
        sys.exit(f"No DCT folders (subdir with dct.json) found under {dcts_dir}")

    if args.mode == "live":
        live_write(dcts_dir, sheet_id, dct_folders, creatives_tab, copy_tab, credentials_path)
        return

    _preview(dcts_dir, dct_folders, creatives_tab, copy_tab, sheet_id,
             credentials_path, config["_config_path"])


if __name__ == "__main__":
    main()
