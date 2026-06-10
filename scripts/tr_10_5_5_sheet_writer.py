"""Thomson Reserve 10-5-5 sheet writer — maps per-DCT dct.json → CREATIVES + COPY rows.

Why this exists (not ad_concept_sheet_writer.py):
  The legacy ad_concept_sheet_writer.py reads ONE dct-tracker.json with a `creatives[]`
  array and a 3-2-2 COPY shape (COPY 1/2 + HEADLINE 1/2). Thomson Reserve has NO
  dct-tracker.json — its data lives in dcts/DCT1NN/dct.json (one file per DCT, each with
  an `angles[]` array of 5 + an `image_pool.images[]`). And the method here is 10-5-5
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
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DCT_IDS = ["DCT101", "DCT102", "DCT103", "DCT104", "DCT105"]
SHEET_ID = "1KqWJP08h8BPr8ygH1ADnmrDPuGaH3p7v4O3WS6WoAtM"

# LIVE sheet header verified 260609 via gws +read. The "Why am I testing this?" column
# (index 7) exists on the live CREATIVES tab between ANGLE and PERSONA — keep it.
CREATIVES_HEADER = [
    "BATCH", "STATUS", "FORMAT", "AD", "MARKET AWARENESS",
    "MARKET SOPHISTICATION", "ANGLE", "Why am I testing this?", "PERSONA", "CANVA LINK",
    "CTR", "CVR", "CPA", "CALLS", "SPEND", "DURATION",
]
# Columns this writer fills (strategy only); STATUS + the metric cols stay blank.
CREATIVES_STRATEGY = {"BATCH", "FORMAT", "AD", "MARKET AWARENESS",
                      "MARKET SOPHISTICATION", "ANGLE", "PERSONA", "CANVA LINK"}

# COPY tab live header was 3-2-2 (BATCH,STATUS,COPY 1,COPY 2,HEADLINE 1,HEADLINE 2);
# widened to 10-5-5 (12 cols) 260609. BATCH is col A (keying column).
COPY_HEADER = [
    "BATCH", "STATUS",
    "COPY 1", "COPY 2", "COPY 3", "COPY 4", "COPY 5",
    "HEADLINE 1", "HEADLINE 2", "HEADLINE 3", "HEADLINE 4", "HEADLINE 5",
]


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


def live_write(dcts_dir: Path) -> None:
    rows_cr, rows_cp = [], []
    for dct_id in DCT_IDS:
        d = load_dct(dcts_dir, dct_id)
        filled, total = angle_copy_state(d)
        if filled != total or total == 0:
            sys.exit(f"ABORT: {dct_id} copy not 5/5 ({filled}/{total}). Refusing live write.")
        cr = build_creatives_row(d)
        cp = build_copy_row(d)
        rows_cr.append([cr.get(c, "") for c in CREATIVES_HEADER])
        rows_cp.append([cp.get(c, "") for c in COPY_HEADER])

    # 1) widen + set COPY header row (12 cols) — overwrites the old 3-2-2 header verbatim
    print("Writing COPY header (10-5-5, 12 cols) -> COPY!A1:L1")
    _gws_update(SHEET_ID, "COPY!A1:L1", [COPY_HEADER])

    # 2) CREATIVES data rows at A2 (16 cols A:P). Blank metric/STATUS cols included as "".
    print(f"Writing {len(rows_cr)} CREATIVES rows -> CREATIVES!A2:P{1+len(rows_cr)}")
    _gws_update(SHEET_ID, f"CREATIVES!A2:P{1+len(rows_cr)}", rows_cr)

    # 3) COPY data rows at A2 (12 cols A:L)
    print(f"Writing {len(rows_cp)} COPY rows -> COPY!A2:L{1+len(rows_cp)}")
    _gws_update(SHEET_ID, f"COPY!A2:L{1+len(rows_cp)}", rows_cp)
    print("LIVE WRITE COMPLETE.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--client", default="neezanizam")
    ap.add_argument("--campaign", default="thomson-reserve")
    ap.add_argument("--mode", choices=["dry-run", "live"], default="dry-run",
                    help="dry-run: print payload only. live: write to the TR sheet via gws.")
    args = ap.parse_args()

    dcts_dir = REPO_ROOT / "clients" / args.client / "campaigns" / args.campaign / "dcts"
    if not dcts_dir.exists():
        sys.exit(f"No dcts/ dir at {dcts_dir}")

    if args.mode == "live":
        live_write(dcts_dir)
        return

    print(f"# DRY-RUN — {args.client}/{args.campaign} 10-5-5 sheet payload")
    print(f"# (no sheet read/write performed — auth/copy-commit gated)\n")
    print(f"CREATIVES header ({len(CREATIVES_HEADER)} cols): {CREATIVES_HEADER}")
    print(f"COPY header ({len(COPY_HEADER)} cols): {COPY_HEADER}\n")

    all_ready = True
    for dct_id in DCT_IDS:
        d = load_dct(dcts_dir, dct_id)
        filled, total = angle_copy_state(d)
        if filled != total or total == 0:
            all_ready = False
        cr = build_creatives_row(d)
        cp = build_copy_row(d)
        pool = d.get("image_pool", {})
        imgs = pool.get("images", []) if isinstance(pool, dict) else []

        print(f"===== {dct_id}  (copy {filled}/{total} filled · {len(imgs)} images) =====")
        print("  CREATIVES row:")
        for col in CREATIVES_HEADER:
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
        print("READY: all 5 DCTs have full copy. Safe to proceed to live write once auth is valid.")
    else:
        print("HOLD: one or more DCTs still PENDING_COPY (orchestrator writing copy in parallel).")
        print("Do NOT live-write until every DCT shows 5/5 copy filled.")


if __name__ == "__main__":
    main()
