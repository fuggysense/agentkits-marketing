#!/usr/bin/env python3
"""Source-or-cut policy for ad claims. Extracts checkable claims from a dct.json (or copy
.md) and either reports their source status (--audit) or fails the build on any unsourced
claim (--gate).

A "checkable claim" is a hard, falsifiable number a reviewer could be sued over: currency
figures, percentages, "X out of Y" ratios, and quantified superlatives ("the #1", "3x more").
Vague quantifiers ("thousands", "most"), years, image dimensions, and percentages that only
appear inside a disclaimer are NOT claims — they need no source.

Source resolution runs in order and stops at the first hit:
  1. Ledger     — a `claims:` block in the dct.json maps a claim to a source path + anchor.
  2. Whitelist  — prices/offsets that appear in the client's _brand/offer.md count as sourced.
  3. Auto-trace — the number/phrase is found verbatim in the client's research dirs
                  (00_inputs/, _swipe/research/, _brand/) or ~/AI workflows/research-vault/.
A claim that survives all three is UNSOURCED.

Design rules:
  - Read-only. Never edits the input. Never makes network/Meta/sheet/render calls.
  - Fail-closed in --gate: any unsourced claim exits 1 with a plain-language message naming
    the claim, the file, and the three ways to fix it (add source / reword / cut).
  - Pragmatic false-positive control. Better to wave through a borderline non-claim than to
    block every years/dimension/disclaimer number — the gate must stay usable.
  - Shape-tolerant. Accepts the current per-DCT image_pool shape, the canonical flat
    top-level image_pool, and the legacy creatives[] shape.

Usage:
  python3 scripts/claim_gate.py --audit <dct.json | copy.md>
  python3 scripts/claim_gate.py --gate  <dct.json | copy.md>
  python3 scripts/claim_gate.py --audit <dct.json> --no-trace   # skip filesystem auto-trace
"""

import argparse
import json
import os
import re
import sys

HOME = os.path.expanduser("~")
RESEARCH_VAULT = os.path.join(HOME, "AI workflows", "research-vault")

# Fields that carry rendered/visible claim text (where an unsourced number is most dangerous).
CLAIM_TEXT_FIELDS = (
    "primary_text",
    "copy_1",
    "copy_2",
    "compression_text",
    "headline",
    "headline_1",
    "headline_2",
    "text_on_image_hook",
    "bridge_line",
    "image_prompt",
    "visual_style",
)


# --- Extraction ------------------------------------------------------------------

# A currency figure: $214,300 or S$4,500 or S$1.6m or "$2 million". Captures the whole token
# including a trailing scale word/letter so "$2 million" is not truncated to "$2".
RE_CURRENCY = re.compile(
    r"(?:S\$|US\$|\$)\s?\d[\d,]*(?:\.\d+)?"
    r"(?:\s?(?:[mkbMKB]\b|million|thousand|billion|mil\b))?",
    re.IGNORECASE,
)
# A bare percentage: 73%, 2.5%.
RE_PERCENT = re.compile(r"\b\d[\d,]*(?:\.\d+)?\s?%")
# "X out of Y" / "X in Y" ratios.
RE_RATIO = re.compile(r"\b\d[\d,]*\s+(?:out\s+of|in)\s+\d[\d,]*\b", re.IGNORECASE)
# Quantified superlatives / multipliers: "2.3x more", "the #1", "3 to 1".
RE_MULTIPLIER = re.compile(r"\b\d+(?:\.\d+)?\s?x\b", re.IGNORECASE)
RE_RANKED = re.compile(r"#\s?1\b|\bno\.?\s?1\b", re.IGNORECASE)

# Years (1900-2099) and standalone "20xx" — not claims on their own.
RE_YEAR = re.compile(r"\b(?:19|20)\d{2}\b")
# Image dimensions / aspect ratios / opacity that show up in image prompts.
RE_DIMENSION = re.compile(
    r"\b\d+\s?(?:px|:\d+|x\d+)\b|\b\d+%\s+opacity\b|\d+:\d+\s+crop", re.IGNORECASE
)
# Layout percentages inside an image prompt ("top 28% of the frame", "occupies 28%",
# "lower third", "about 92% opacity") describe composition, not a claim about the world.
RE_LAYOUT_PCT = re.compile(
    r"\b(?:top|bottom|lower|upper|about|roughly|around|occupies?|spanning|fills?)\s+"
    r"(?:the\s+)?\d[\d.]*\s?%"
    r"|\d[\d.]*\s?%\s+(?:of\s+the\s+)?(?:frame|image|height|width|crop|opacity|opaque)",
    re.IGNORECASE,
)

# Phrases that, when wrapping a number, mark it as a disclaimer/illustrative — not a claim.
DISCLAIMER_MARKERS = (
    "illustrative",
    "for example",
    "e.g.",
    "set dressing",
    "fictional",
    "placeholder",
    "sample only",
    "negative prompt",
)

# Vague quantifiers carry no digit, so the regexes never catch them — listed here only as
# documentation of what we intentionally do NOT treat as a checkable claim.
VAGUE_QUANTIFIERS = ("thousands", "hundreds", "millions", "most", "many", "several")


def _strip_disclaimer_spans(text):
    """Return text with disclaimer-marked spans blanked, so numbers inside them are ignored.

    A number is "inside a disclaimer" if a disclaimer marker appears within the same sentence.
    We split on sentence-ish boundaries and drop any sentence carrying a marker.
    """
    out = []
    for sentence in re.split(r"(?<=[.!?])\s+|\n", text):
        low = sentence.lower()
        if any(m in low for m in DISCLAIMER_MARKERS):
            continue
        out.append(sentence)
    return " ".join(out)


def _is_dimension_or_year(token, context):
    """True when a numeric token is a year or an image dimension/opacity — not a claim."""
    if RE_YEAR.fullmatch(token.strip()):
        return True
    # Opacity / aspect / px around the token in its local context.
    if RE_DIMENSION.search(context):
        # Only suppress if the matched dimension actually contains this token.
        for m in RE_DIMENSION.finditer(context):
            if token.strip() in m.group(0):
                return True
    return False


def extract_claims_from_text(text, where):
    """Yield {claim, where, kind} for each checkable claim in a single text field."""
    if not text or not isinstance(text, str):
        return
    cleaned = _strip_disclaimer_spans(text)
    seen = set()
    found = []

    def emit(match, kind, raw_text):
        claim = match.group(0).strip().rstrip(".,;:")
        local = raw_text[max(0, match.start() - 25) : match.end() + 25]
        if kind == "percent" and RE_LAYOUT_PCT.search(local):
            return
        if _is_dimension_or_year(claim, local):
            return
        key = (claim, kind)
        if key in seen:
            return
        seen.add(key)
        # Wider sentence context, used by the trace to require the claim's SUBJECT (not just
        # its number) to co-occur in a source file — a bare "73%" matches anything.
        sentence = raw_text[max(0, match.start() - 90) : match.end() + 90]
        found.append({"claim": claim, "where": where, "kind": kind, "context": sentence})

    for rx, kind in (
        (RE_CURRENCY, "currency"),
        (RE_PERCENT, "percent"),
        (RE_RATIO, "ratio"),
        (RE_MULTIPLIER, "multiplier"),
        (RE_RANKED, "superlative"),
    ):
        for m in rx.finditer(cleaned):
            emit(m, kind, cleaned)
    return found


def iter_dct_text_fields(dct):
    """Yield (text, where_label) for every claim-bearing field across all dct shapes.

    Handles: per-DCT image_pool (dcts[].image_pool.images[]), canonical flat top-level
    image_pool, angles[]/creatives[] with their own text + drafts, and legacy creatives[].
    """
    def emit_record(rec, prefix):
        rid = rec.get("id") or rec.get("ad_name") or rec.get("dct_id") or prefix
        for field in CLAIM_TEXT_FIELDS:
            val = rec.get(field)
            if isinstance(val, str) and val.strip():
                yield val, f"{prefix}:{rid}.{field}"
        for draft in rec.get("headline_drafts", []) or []:
            if isinstance(draft, str) and draft.strip():
                yield draft, f"{prefix}:{rid}.headline_draft"

    def emit_image_pool(pool, prefix):
        for img in (pool or {}).get("images", []) or []:
            yield from emit_record(img, f"{prefix}-image")

    # Top-level convenience fields (rare, but cheap to cover).
    for field in ("offer", "constant"):
        val = dct.get(field)
        if isinstance(val, str):
            yield val, f"dct.{field}"

    # Canonical flat top-level image_pool.
    if isinstance(dct.get("image_pool"), dict):
        yield from emit_image_pool(dct["image_pool"], "dct")

    # angles[] (canonical 10-5-5 with one flat pool) or creatives[] (legacy).
    for coll_name in ("angles", "creatives"):
        for rec in dct.get(coll_name, []) or []:
            yield from emit_record(rec, coll_name[:-1])

    # Per-DCT shape: dcts[] each carrying copy fields + their own image_pool.
    for d in dct.get("dcts", []) or []:
        yield from emit_record(d, "dct")
        if isinstance(d.get("image_pool"), dict):
            yield from emit_image_pool(d["image_pool"], d.get("dct_id", "dct"))


def extract_claims(path):
    """Return (claims, dct_or_none, kind) for a dct.json or a copy .md file."""
    if path.endswith(".json"):
        with open(path, "r", encoding="utf-8") as fh:
            dct = json.load(fh)
        claims = []
        for text, where in iter_dct_text_fields(dct):
            claims.extend(extract_claims_from_text(text, where) or [])
        return claims, dct, "json"
    # Markdown / plain text copy file: scan the whole body.
    with open(path, "r", encoding="utf-8") as fh:
        body = fh.read()
    claims = extract_claims_from_text(body, os.path.basename(path)) or []
    return claims, None, "md"


# --- Source resolution -----------------------------------------------------------

def _normalize_number(claim):
    """Strip currency symbols, separators, and scale suffixes to a comparable digit string.

    '$214,300' -> '214300'; 'S$1.6m' -> '1.6m'; '73%' -> '73'. Used for whitelist + trace
    so '$4,500' in copy matches 'S$4,500' in offer.md.
    """
    n = claim.strip()
    n = re.sub(r"^(?:S\$|US\$|\$)", "", n)
    n = n.rstrip("%").strip()
    n = n.replace(",", "")
    return n.lower()


def load_ledger(dct):
    """Return {normalized_number_or_phrase: source_string} from a `claims:` ledger block.

    The ledger lives at dct['claims'] as either a list of {claim, source} objects or a
    flat {claim: source} map. Each entry asserts a source path + line/anchor for one claim.
    """
    ledger = {}
    raw = (dct or {}).get("claims")
    if isinstance(raw, dict):
        items = raw.items()
    elif isinstance(raw, list):
        items = [
            (e.get("claim"), e.get("source"))
            for e in raw
            if isinstance(e, dict) and e.get("claim")
        ]
    else:
        items = []
    for claim, source in items:
        if not claim or not source:
            continue
        ledger[_normalize_number(str(claim))] = source
        ledger[str(claim).strip().lower()] = source
    return ledger


def client_root_for(path):
    """Walk up from the input file to the clients/<slug>/ root, if any."""
    parts = os.path.abspath(path).split(os.sep)
    if "clients" in parts:
        i = parts.index("clients")
        if i + 1 < len(parts):
            return os.sep.join(parts[: i + 2])
    return None


def gather_source_dirs(client_root):
    """Return the list of directories auto-trace will grep for a claim's number/phrase."""
    dirs = []
    if client_root:
        for sub in ("00_inputs", os.path.join("_swipe", "research"), "_brand"):
            d = os.path.join(client_root, sub)
            if os.path.isdir(d):
                dirs.append(d)
    if os.path.isdir(RESEARCH_VAULT):
        dirs.append(RESEARCH_VAULT)
    return dirs


def load_offer_whitelist(client_root):
    """Numbers (normalized) that appear in _brand/offer.md — prices/offsets count as sourced."""
    if not client_root:
        return set()
    offer = os.path.join(client_root, "_brand", "offer.md")
    if not os.path.isfile(offer):
        return set()
    with open(offer, "r", encoding="utf-8") as fh:
        body = fh.read()
    nums = set()
    for rx in (RE_CURRENCY, RE_PERCENT):
        for m in rx.finditer(body):
            nums.add(_normalize_number(m.group(0)))
    return nums


# Words too generic to anchor a claim's subject — ignored when matching context keywords.
# Two groups: ordinary stopwords, plus art-direction vocabulary that pollutes image_prompt
# context (a stat baked into a prompt is surrounded by styling words like "Straits Times
# business feature statistic spreadsheet" — those match research SOURCE indexes by chance and
# must not be allowed to anchor a trace).
STOPWORDS = frozenset("""a an the of to in on at for and or but with from by your you their his
her our its this that these those is are was were be been being do does did has have had will
would can could should may might it they them he she we i as not no than then so but if when
over under more less most least one two second home buyers buyer singapore sg per annum
straits times business feature statistic statistics spreadsheet bold large single small plain
loud like beside background editorial headline caption card image prompt style visual clean
premium restrained muted neutral palette typography wordmark text font serif sans line band
photograph photographic documentary realism render scene frame top bottom corner negative""".split())


def _claim_keywords(context):
    """Distinctive subject words from a claim's surrounding sentence, used to anchor a trace.

    'overpay', 'buyers', 'second home' etc. minus stopwords. A trace on a non-distinctive
    number (a bare percentage) must also hit one of these in the SAME file to count.
    """
    words = re.findall(r"[a-z]{4,}", context.lower())
    return [w for w in words if w not in STOPWORDS]


PROXIMITY = 200  # chars: how close a subject keyword must sit to the number to count.


def _grep_dirs(needle, dirs, require_any=None, min_hits=0):
    """Return the first file under any dir containing `needle` (literal, case-insensitive).

    If `require_any` is given, the number alone is not enough: at least `min_hits` DISTINCT
    subject keywords must appear WITHIN ~200 chars of one occurrence of the number in the
    same file. Same-file-but-far-apart does not count — that is how a bare '73%' coincidentally
    matched an unrelated scrape that merely also contained the word 'overpay'. stdlib only.
    """
    needle_low = needle.lower()
    require_low = [w.lower() for w in (require_any or [])]
    for root in dirs:
        for dirpath, _dirnames, filenames in os.walk(root):
            for fn in filenames:
                if not fn.lower().endswith((".md", ".json", ".txt", ".ndjson", ".jsonl")):
                    continue
                fp = os.path.join(dirpath, fn)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                        body = fh.read().lower()
                except (OSError, UnicodeError):
                    continue
                if needle_low not in body:
                    continue
                if not require_low:
                    return fp
                start = 0
                while True:
                    idx = body.find(needle_low, start)
                    if idx == -1:
                        break
                    window = body[max(0, idx - PROXIMITY): idx + len(needle_low) + PROXIMITY]
                    if len({w for w in require_low if w in window}) >= max(1, min_hits):
                        return fp
                    start = idx + len(needle_low)
    return None


def resolve_source(claim, ledger, whitelist, source_dirs, trace):
    """Resolve one claim to (status, detail). status in {ledger, offer, traced, UNSOURCED}."""
    norm = _normalize_number(claim["claim"])
    raw_low = claim["claim"].strip().lower()

    if norm in ledger:
        return "ledger", ledger[norm]
    if raw_low in ledger:
        return "ledger", ledger[raw_low]
    if norm in whitelist:
        return "offer", "_brand/offer.md"
    if trace and source_dirs:
        digits = re.sub(r"[^\d]", "", norm)
        # A 4+ digit currency figure ($214,300) is distinctive enough to anchor on alone.
        # Everything else — percentages, ratios, multipliers, small currency — is the
        # high-risk fabrication class. A bare "73%" matching some corpus proves nothing, so
        # the number must co-occur with the claim's distinctive SUBJECT words, near it.
        if claim["kind"] == "currency" and len(digits) >= 4:
            need, min_hits = None, 0
        else:
            need = _claim_keywords(claim.get("context", ""))
            # Require TWO distinct subject words near the number for non-currency / soft stats
            # (one common word like "overpay" or "buyers" co-occurs by chance; two rarely do).
            min_hits = 1 if claim["kind"] == "currency" else 2
        for cand in _trace_candidates(claim["claim"]):
            hit = _grep_dirs(cand, source_dirs, require_any=need, min_hits=min_hits)
            if hit:
                return "traced", os.path.relpath(hit, HOME)
    return "UNSOURCED", ""


def _trace_candidates(claim_text):
    """Distinctive strings to grep for one claim. Avoids coincidental matches on tiny numbers.

    Always traces the claim exactly as written ('2.5%', '$200k', '73%'). For large currency
    figures (4+ significant digits, e.g. '$214,300') it also traces the bare-digit and
    comma-formatted variants, since those are distinctive enough that a stray match is unlikely.
    A short bare number is NEVER traced on its own — '$2' or '73' would match anything.
    """
    raw = claim_text.strip()
    # As-written token carries its symbol/decimal/suffix, so it is distinctive on its own
    # (e.g. '2.5%', '$200k', '$214,300'). A bare integer with no symbol is too generic.
    cands = {raw}
    digits = re.sub(r"[^\d]", "", _normalize_number(claim_text))
    if len(digits) >= 4:
        cands.add(digits)
        cands.add(f"{int(digits):,}")
    return {c for c in cands if c}


# --- Modes -----------------------------------------------------------------------

def run(path, mode, trace):
    claims, dct, _kind = extract_claims(path)
    client_root = client_root_for(path)
    ledger = load_ledger(dct)
    whitelist = load_offer_whitelist(client_root)
    source_dirs = gather_source_dirs(client_root)

    resolved = []
    for c in claims:
        status, detail = resolve_source(c, ledger, whitelist, source_dirs, trace)
        resolved.append({**c, "status": status, "detail": detail})

    unsourced = [r for r in resolved if r["status"] == "UNSOURCED"]

    if mode == "audit":
        print(f"CLAIM GATE — AUDIT\nfile: {path}")
        print(f"client root: {client_root or '(none)'}")
        print(f"claims found: {len(resolved)}   unsourced: {len(unsourced)}   "
              f"trace: {'on' if trace else 'off'}\n")
        if not resolved:
            print("No checkable claims extracted.")
            return 0
        w_claim = max(len("claim"), *(len(r["claim"]) for r in resolved))
        w_where = max(len("where"), *(len(r["where"]) for r in resolved))
        print(f"{'claim'.ljust(w_claim)}  {'where'.ljust(w_where)}  source-status")
        print(f"{'-' * w_claim}  {'-' * w_where}  {'-' * 13}")
        for r in resolved:
            tag = r["status"] if r["status"] == "UNSOURCED" else f"{r['status']}: {r['detail']}"
            print(f"{r['claim'].ljust(w_claim)}  {r['where'].ljust(w_where)}  {tag}")
        return 0

    # gate mode
    if not unsourced:
        print(f"CLAIM GATE — PASS  ({len(resolved)} claims, all sourced)\nfile: {path}")
        return 0
    print(f"CLAIM GATE — FAIL  ({len(unsourced)} unsourced of {len(resolved)} claims)")
    print(f"file: {path}\n")
    print("Never bypass silently. Each claim below must be fixed before render:\n")
    for r in unsourced:
        print(f"  UNSOURCED: \"{r['claim']}\"  ({r['kind']})")
        print(f"    at: {r['where']}")
        print(f"    in: {path}")
        print("    fix one of: (a) add a source to the dct.json `claims:` ledger "
              "(path + line/anchor), (b) reword without the number, or (c) cut the claim.\n")
    return 1


def main(argv=None):
    p = argparse.ArgumentParser(description="Source-or-cut claim gate for ad dct.json / copy.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--audit", metavar="PATH", help="report claim/source table, exit 0")
    g.add_argument("--gate", metavar="PATH", help="exit 1 on any unsourced claim")
    p.add_argument("--no-trace", action="store_true",
                   help="skip filesystem auto-trace (ledger + offer whitelist only)")
    args = p.parse_args(argv)

    path = args.audit or args.gate
    mode = "audit" if args.audit else "gate"
    if not os.path.isfile(path):
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2
    return run(path, mode, trace=not args.no_trace)


if __name__ == "__main__":
    sys.exit(main())
