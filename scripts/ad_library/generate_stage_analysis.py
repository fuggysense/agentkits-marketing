#!/usr/bin/env python3
"""Generate Schwartz 5-stage market sophistication analysis from ads-db.sqlite.

Reads:    swipe-files/<industry>/ads-db.sqlite
Synthesis: scripts/research-llm.sh kilo "<prompt>" --model nvidia/nemotron-3-super-...
Writes:   swipe-files/<industry>/stage-analysis.draft.md  (HITL approves → renames to stage-analysis.md)

Per Q6 — auto-draft after every scrape; HITL gate before commit.

Usage:
  python3 scripts/ad_library/generate_stage_analysis.py --industry property-sg
  python3 scripts/ad_library/generate_stage_analysis.py --industry property-sg --top 15
  python3 scripts/ad_library/generate_stage_analysis.py --industry property-sg --dry-run  # print prompt only
"""

import argparse
import datetime as dt
import json
import os
import sqlite3
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SWIPE_ROOT = ROOT / "swipe-files"
RESEARCH_LLM = ROOT / "scripts" / "research-llm.sh"
KILO_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"


PROMPT_HEADER = """You are a senior paid-ads strategist applying Eugene Schwartz's \
5-stage market sophistication framework + 5-level awareness model.

Stages:
  1: First to market — make any claim
  2: Direct competitors — enlarge / amplify the claim
  3: Claims saturated — introduce a new MECHANISM (HOW it works)
  4: Mechanisms common — elaborate the mechanism (surer, faster, easier)
  5: Market exhausted — shift to IDENTIFICATION (who they are, not what product does)

Below is the actual ad pool for ONE industry. Analyze it on TWO axes:
  AXIS A — STRUCTURAL: which Schwartz stage, what mechanisms saturate, what claims repeat.
  AXIS B — BUYER-SEGMENT: WHICH demographic / life-stage / cultural / financial identity \
each ad targets. Then identify which buyer segments NO competitor in the pool addresses.

CRITICAL: do not conflate "blue ocean mechanism" with "blue ocean buyer". A mechanism gap \
is a claim/feature nobody offers. A buyer gap is a real human group nobody is talking to. \
Both matter. Most analyses miss the buyer-gap axis entirely.

Output MARKDOWN. No preamble, no apologies — start with the H1.

REQUIRED SECTIONS (in order):
  # <Industry> — Schwartz Stage Analysis (<scrape date>)
  ## Executive Summary
    - Stage assessment (one of 2/3/4/5) + confidence (low/med/high) + 2-sentence rationale
  ## Evidence
    - N ads in pool, N running >90 days (durable winners), N running >30 days
  ## Top 10 Winners by Duration
    - bullet list: page_name | days_running | hook (first 60 chars)
  ## Buyer Segments Currently Targeted (AXIS B — observed)
    - bullet list, EACH with: segment name | demographic/life-stage signals | which advertisers target it | mass desire | sophistication stage they're at
    - infer from the ad copy itself: who is the speaker addressing? what financial situation, life moment, identity, or pain do they assume?
    - aim for 4-7 distinct segments; combine near-duplicates
  ## Mechanism Inventory (AXIS A — observed)
    - distinct "how it works" framings (bullet list)
  ## Claim Inventory (AXIS A — observed)
    - distinct "what you get" framings (bullet list)
  ## Blue Boxes (claims/mechanisms ALL competitors make — AVOID re-using)
    - bullets
  ## Blue Ocean Gaps — Mechanism (Axis A)
    - claims/mechanisms NO competitor uses, ranked by leverage
  ## Blue Ocean Gaps — Buyer Segments (Axis B)
    - demographic/life-stage/cultural buyer groups NO competitor in the pool addresses
    - examples to consider (include if missing from observed): life-transition (divorce/widow/inheritance/aging-parent), foreigner/PR facing ABSD, first-time HDB applicant, cultural-segment specific (Malay/Muslim, Chinese-language only, Tamil), seller-side (cash-out timing), downsizing-empty-nester, HDB MOP just hit, en-bloc displaced
    - rank by leverage = (buyer pool size in SG) × (purchasing power) × (urgency of decision)
  ## Strategic Recommendation
    - where new clients should play next on BOTH axes (stack a blue-ocean buyer segment with a blue-ocean mechanism for max differentiation)
    - what to avoid + why
    - which existing winning advertiser is the closest competitive threat to the recommended play

Be specific. Cite ad evidence by page_name + days_running. No generic platitudes. \
Sacrifice grammar for concision.

INDUSTRY DATA:
"""


def fetch_pool(db_path: Path, top: int) -> dict:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        ads_total = conn.execute("SELECT COUNT(*) AS n FROM ads").fetchone()["n"]
        ads_30d = conn.execute(
            "SELECT COUNT(*) AS n FROM ads WHERE days_running > 30"
        ).fetchone()["n"]
        ads_90d = conn.execute(
            "SELECT COUNT(*) AS n FROM ads WHERE days_running > 90"
        ).fetchone()["n"]
        winners = [dict(r) for r in conn.execute("""
            SELECT page_name, days_running, headline, primary_text, media_type,
                   detected_angle, detected_mass_desire,
                   schwartz_awareness, schwartz_sophistication
            FROM ads
            ORDER BY days_running DESC
            LIMIT ?
        """, (top,)).fetchall()]
        all_ads = [dict(r) for r in conn.execute("""
            SELECT page_name, days_running, headline, primary_text,
                   detected_angle, detected_mass_desire,
                   schwartz_awareness, schwartz_sophistication
            FROM ads
            ORDER BY days_running DESC
        """).fetchall()]
        pages = [dict(r) for r in conn.execute("""
            SELECT page_name, page_categories, ads_collected_total
            FROM pages
        """).fetchall()]
    finally:
        conn.close()
    return {
        "totals": {"ads": ads_total, "running_30d": ads_30d, "running_90d": ads_90d},
        "winners": winners,
        "all_ads": all_ads,
        "pages": pages,
    }


def truncate(s: str | None, n: int) -> str:
    if not s:
        return ""
    s = s.replace("\n", " ").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def render_corpus(pool: dict) -> str:
    lines = [
        f"Pool totals: {pool['totals']}",
        f"Pages tracked: {len(pool['pages'])}",
        "",
        "## Top winners (sorted by days_running)",
    ]
    for ad in pool["winners"]:
        lines.append(
            f"- {ad['page_name']} | {ad['days_running']}d | {ad.get('media_type') or '?'}"
            f" | headline: {truncate(ad.get('headline'), 100)}"
            f" | body: {truncate(ad.get('primary_text'), 200)}"
            f" | angle: {ad.get('detected_angle') or '-'}"
            f" | desire: {ad.get('detected_mass_desire') or '-'}"
            f" | awareness: {ad.get('schwartz_awareness') or '-'}"
            f" | stage_guess: {ad.get('schwartz_sophistication') or '-'}"
        )
    lines.append("")
    lines.append("## Compact ad inventory (page_name | days | headline | body summary)")
    # Free models have ~6K output cap — keep input lean to leave room for analysis
    for ad in pool["all_ads"][:50]:
        lines.append(
            f"- {ad['page_name']} | {ad['days_running']}d | {truncate(ad.get('headline'), 60)} || "
            f"{truncate(ad.get('primary_text'), 90)}"
        )
    return "\n".join(lines)


def call_kilo(prompt: str) -> str | None:
    if not RESEARCH_LLM.exists():
        print(f"ERR: {RESEARCH_LLM} missing", file=sys.stderr)
        return None
    try:
        out = subprocess.run(
            ["bash", str(RESEARCH_LLM), "kilo", prompt, "--model", KILO_MODEL],
            capture_output=True, text=True, timeout=240,
            env={**os.environ},
        )
        if out.returncode != 0:
            print(f"ERR: kilo exit={out.returncode} stderr={out.stderr[:400]}",
                  file=sys.stderr)
            return None
        # research-llm.sh wraps output in {"provider","result":"<markdown>","tokens_used"}
        text = out.stdout.strip()
        try:
            envelope = json.loads(text)
            if isinstance(envelope, dict) and "result" in envelope:
                return envelope["result"]
        except json.JSONDecodeError:
            pass
        return text
    except Exception as e:  # noqa: BLE001
        print(f"ERR: kilo exception: {e}", file=sys.stderr)
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--industry", required=True)
    ap.add_argument("--top", type=int, default=10, help="Top N winners to highlight")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print prompt only; don't call Kilo or write file")
    args = ap.parse_args()

    industry_dir = SWIPE_ROOT / args.industry
    db_path = industry_dir / "ads-db.sqlite"
    if not db_path.exists():
        print(f"ERR: {db_path} not found — run rebuild_ads_db.py first",
              file=sys.stderr)
        return 1

    pool = fetch_pool(db_path, args.top)
    if pool["totals"]["ads"] == 0:
        print("ERR: zero ads in db — nothing to analyze", file=sys.stderr)
        return 1

    industry_label = args.industry.replace("-", " ").title()
    today = dt.date.today().isoformat()
    prompt = PROMPT_HEADER + render_corpus(pool) + textwrap.dedent(f"""

        OUTPUT CONTEXT:
        - industry: {industry_label}
        - scrape_date: {today}
    """)

    print(f"[stage-analysis] industry={args.industry} ads={pool['totals']['ads']} "
          f"running_30d={pool['totals']['running_30d']} prompt_chars={len(prompt)}")

    if args.dry_run:
        print("--- PROMPT ---")
        print(prompt[:2000])
        print(f"... ({len(prompt) - 2000} chars truncated)" if len(prompt) > 2000 else "")
        return 0

    draft = call_kilo(prompt)
    if not draft:
        return 2

    out_path = industry_dir / "stage-analysis.draft.md"
    out_path.write_text(draft + "\n", encoding="utf-8")
    print(f"[stage-analysis] draft written → {out_path.relative_to(ROOT)}")
    print("Next: review the draft, edit if needed, then rename to stage-analysis.md to commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
