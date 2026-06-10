#!/usr/bin/env python3
"""Research-completeness gate. Checks a client's research against the niche-adaptive
"research complete" contract in clients/<slug>/_brand/research-brief.md before any avatar,
angle, or ad work runs.

The contract is a YAML block inside research-brief.md (see clients/_template/_brand/
research-brief.md). It names, per niche: required source types, a minimum verbatim-phrase
count, required artifacts (mapped to THIS repo's names), compliance constraints, and a
thin-data fallback ladder. Defaults are the Ferres floor (3 named docs, >=20 verbatim
phrases, gap analysis, human read-through, re-run-if-thin).

Resolution runs against BOTH:
  - the client folders   — 00_inputs/, _swipe/research/, _brand/
  - the research-vault   — ~/AI workflows/research-vault/markets/* (operator-stored research)

If the client has NO research-brief.md, the gate falls back to the Ferres-floor defaults
baked in below and SAYS SO at the top of the scorecard.

Design rules (mirrors scripts/claim_gate.py):
  - Read-only. Never edits anything. No network / Meta / sheet / render calls.
  - stdlib only. The YAML block is parsed by a small purpose-built reader, not PyYAML.
  - Fail-closed: any FAIL item exits 1 with a plain-language, actionable scorecard.

Usage:
  python3 scripts/research_gate.py --client clients/<slug>
  python3 scripts/research_gate.py --client clients/<slug> --json
"""

import argparse
import glob
import json
import os
import re
import sys

HOME = os.path.expanduser("~")
RESEARCH_VAULT = os.path.join(HOME, "AI workflows", "research-vault")
VAULT_MARKETS = os.path.join(RESEARCH_VAULT, "markets")

TEXT_EXTS = (".md", ".json", ".txt", ".ndjson", ".jsonl")


# --- Ferres-floor defaults (used verbatim when a client has no research-brief.md) --------
# These mirror clients/_template/_brand/research-brief.md. Kept in sync by hand; the template
# is the human-readable canonical source, this is the machine fallback.
FERRES_FLOOR = {
    "niche": "(unknown — no research-brief.md)",
    "floor_profile": "ferres-default",
    "required_sources": [
        {"id": "voice_of_customer",
         "match": ["voc", "reddit", "review", "forum", "comment", "quote"]},
        {"id": "competitor_intel",
         "match": ["competitor", "competitive-landscape", "swipe", "ad-library"]},
        {"id": "market_context",
         "match": ["market", "market-stats", "trend", "category"]},
        {"id": "client_assets",
         "match": ["offer", "onboarding", "winning-ad", "landing", "vsl", "transcript"]},
    ],
    "min_verbatim_phrases": 20,
    "required_artifacts": [
        {"id": "icp_equivalent",
         "what": "Buyer-language dossier / buyer-profile psychology (ICP-equivalent)",
         "resolves_to": [
             "00_inputs/research/voc-*.md",
             "00_inputs/market/buyer-language.md",
             "_brand/buyer-profile.md",
             "research-vault: language-map.md|fears.md|frustrations.md|desired-outcomes.md",
         ]},
        {"id": "competitor_doc",
         "what": "Competitor analysis (models, weaknesses, differentiation)",
         "resolves_to": [
             "00_inputs/research/competitor-*.md",
             "00_inputs/market/competitors/competitor-index.md",
             "research-vault: competitive-landscape.md",
         ]},
        {"id": "market_doc",
         "what": "Market research (trends, stats, pain hierarchy, timing)",
         "resolves_to": [
             "00_inputs/research/market-*.md",
             "00_inputs/market/awareness-sophistication.md",
             "research-vault: sophistication-schwartz.md|awareness-schwartz.md|trigger-events.md",
         ]},
        {"id": "gap_analysis",
         "what": "Gap analysis (buyer language vs what the offer answers)",
         "resolves_to": [
             "00_inputs/research/*gap*.md",
             "00_inputs/market/awareness-sophistication.md",
             "_brand/buyer-profile.md",
         ]},
    ],
    "compliance_constraints": [
        {"id": "claims_have_sources",
         "note": "Enforced downstream by scripts/claim_gate.py --gate."},
        {"id": "platform_policy",
         "note": "Niche ad-platform landmines (income/health/personal-attribute claims)."},
    ],
    "thin_data_fallback": [
        {"step": "lean_on_competitors"},
        {"step": "reuse_existing_research"},
        {"step": "quick_brief_shortcut"},
        {"step": "rerun_with_more_context"},
        {"step": "operator_override"},
    ],
    "human_read_through": {"required": True,
                           "record_in": "00_inputs/research/README.md or _baseline"},
}


# --- Minimal YAML reader (scoped to the research_brief: block shape) --------------------

def _strip_comment(line):
    """Remove a trailing ' # comment' that is not inside quotes. Good enough for this block."""
    in_q = None
    out = []
    for ch in line:
        if in_q:
            out.append(ch)
            if ch == in_q:
                in_q = None
        elif ch in "\"'":
            in_q = ch
            out.append(ch)
        elif ch == "#":
            # treat as comment only if preceded by whitespace or start
            if out and out[-1] not in " \t":
                out.append(ch)
            else:
                break
        else:
            out.append(ch)
    return "".join(out).rstrip()


def _scalar(tok):
    tok = tok.strip()
    if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in "\"'":
        return tok[1:-1]
    if tok.lower() in ("true", "false"):
        return tok.lower() == "true"
    if re.fullmatch(r"-?\d+", tok):
        return int(tok)
    return tok


def _inline_list(tok):
    """Parse `["a", "b"]` inline flow lists."""
    inner = tok.strip()[1:-1].strip()
    if not inner:
        return []
    parts = re.split(r",\s*", inner)
    return [_scalar(p) for p in parts]


def extract_yaml_block(text):
    """Pull the first fenced ```yaml ... ``` block from a markdown file."""
    m = re.search(r"```ya?ml\s*\n(.*?)```", text, re.DOTALL)
    return m.group(1) if m else None


def parse_brief_yaml(block):
    """Parse the research_brief: YAML block into a dict.

    Purpose-built for the shapes used in research-brief.md: a top-level `research_brief:`
    mapping whose values are scalars, lists-of-scalars, or lists-of-mappings (each list item
    a `- key: val` block with sibling indented `key: val` lines, and `match: [..]` inline
    lists). NOT a general YAML parser — only what this contract needs. stdlib only.
    """
    lines = [_strip_comment(l) for l in block.splitlines()]
    # Find the research_brief: root and its indent.
    root_idx = None
    for i, l in enumerate(lines):
        if l.strip() == "research_brief:" or l.rstrip().endswith("research_brief:"):
            root_idx = i
            break
    if root_idx is None:
        return None
    base = len(lines[root_idx]) - len(lines[root_idx].lstrip())
    body = lines[root_idx + 1:]

    result = {}
    i = 0
    n = len(body)

    def indent(s):
        return len(s) - len(s.lstrip())

    while i < n:
        line = body[i]
        if not line.strip():
            i += 1
            continue
        ind = indent(line)
        if ind <= base:
            break  # back to top level — block ended
        stripped = line.strip()
        if ":" not in stripped:
            i += 1
            continue
        key, _, rest = stripped.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest and rest.startswith("["):
            result[key] = _inline_list(rest)
            i += 1
        elif rest:
            result[key] = _scalar(rest)
            i += 1
        else:
            # nested block: either a list (next non-blank line is "- ...") or a mapping
            j = i + 1
            while j < n and not body[j].strip():
                j += 1
            if j >= n:
                i = j
                continue
            child_ind = indent(body[j])
            if child_ind <= ind:
                result[key] = None
                i = j
                continue
            if body[j].strip().startswith("- "):
                val, i = _parse_list(body, j, child_ind, indent)
            else:
                val, i = _parse_map(body, j, child_ind, indent)
            result[key] = val
    return result


def _parse_map(body, start, map_ind, indent):
    """Parse an indented `key: val` mapping starting at `start`. Returns (dict, next_idx)."""
    out = {}
    i = start
    n = len(body)
    while i < n:
        line = body[i]
        if not line.strip():
            i += 1
            continue
        if indent(line) < map_ind:
            break
        if indent(line) > map_ind:
            i += 1
            continue
        stripped = line.strip()
        key, _, rest = stripped.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest.startswith("["):
            out[key] = _inline_list(rest)
        elif rest:
            out[key] = _scalar(rest)
        else:
            out[key] = None
        i += 1
    return out, i


def _parse_list(body, start, item_ind, indent):
    """Parse a `- ...` list starting at `start`. Items may be scalars or mappings.

    A `- key: val` introduces a mapping item; sibling `key: val` lines at item_ind+2 join it.
    A bare `- val` is a scalar item. Returns (list, next_idx).
    """
    items = []
    i = start
    n = len(body)
    while i < n:
        line = body[i]
        if not line.strip():
            i += 1
            continue
        ind = indent(line)
        if ind < item_ind:
            break
        if ind > item_ind:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("- "):
            break
        content = stripped[2:].strip()
        if ":" in content and not content.startswith(("\"", "'")):
            # mapping item — first pair on the dash line, rest are deeper-indented siblings
            key, _, rest = content.partition(":")
            item = {}
            rest = rest.strip()
            if rest.startswith("["):
                item[key.strip()] = _inline_list(rest)
            elif rest:
                item[key.strip()] = _scalar(rest)
            else:
                item[key.strip()] = None
            i += 1
            # absorb sibling key:val lines deeper than item_ind. A sibling whose value is
            # empty and is followed by a deeper `- ...` block is itself a nested list.
            while i < n:
                sib = body[i]
                if not sib.strip():
                    i += 1
                    continue
                sind = indent(sib)
                if sind <= item_ind:
                    break
                sstr = sib.strip()
                if sstr.startswith("- "):
                    break  # a deeper bare dash with no parent key — stop (shouldn't happen here)
                k2, _, r2 = sstr.partition(":")
                r2 = r2.strip()
                if r2.startswith("["):
                    item[k2.strip()] = _inline_list(r2)
                    i += 1
                elif r2:
                    item[k2.strip()] = _scalar(r2)
                    i += 1
                else:
                    # empty value — look ahead for a deeper nested list/map
                    j = i + 1
                    while j < n and not body[j].strip():
                        j += 1
                    if j < n and indent(body[j]) > sind:
                        if body[j].strip().startswith("- "):
                            nested, i = _parse_list(body, j, indent(body[j]), indent)
                        else:
                            nested, i = _parse_map(body, j, indent(body[j]), indent)
                        item[k2.strip()] = nested
                    else:
                        item[k2.strip()] = None
                        i += 1
            items.append(item)
        else:
            items.append(_scalar(content))
            i += 1
    return items, i


# --- Brief loading ----------------------------------------------------------------------

def load_brief(client_root):
    """Return (brief_dict, used_default_bool). Falls back to FERRES_FLOOR when absent/unparseable."""
    path = os.path.join(client_root, "_brand", "research-brief.md")
    if not os.path.isfile(path):
        return dict(FERRES_FLOOR), True
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    block = extract_yaml_block(text)
    if not block:
        return dict(FERRES_FLOOR), True
    parsed = parse_brief_yaml(block)
    if not parsed:
        return dict(FERRES_FLOOR), True
    # Merge onto the floor so a partial brief still has every knob.
    merged = dict(FERRES_FLOOR)
    merged.update({k: v for k, v in parsed.items() if v is not None})
    return merged, False


# --- Filesystem resolution --------------------------------------------------------------

def client_source_dirs(client_root):
    """Directories that hold this client's research."""
    dirs = []
    for sub in ("00_inputs", os.path.join("_swipe", "research"), "_brand"):
        d = os.path.join(client_root, sub)
        if os.path.isdir(d):
            dirs.append(d)
    return dirs


def iter_text_files(dirs):
    for root in dirs:
        if not os.path.isdir(root):
            continue
        for dirpath, _dn, filenames in os.walk(root):
            for fn in filenames:
                if fn.lower().endswith(TEXT_EXTS):
                    yield os.path.join(dirpath, fn)


def matched_vault_markets(niche, client_slug):
    """Vault market dossiers whose folder name shares a token with the niche / slug.

    Conservative: a vault dossier counts as 'this client's research' only when its folder
    name shares a meaningful token with the niche string or the client slug. Avoids a generic
    'market' match pulling in unrelated dossiers.
    """
    if not os.path.isdir(VAULT_MARKETS):
        return []
    tokens = set()
    for src in (str(niche or ""), str(client_slug or "")):
        for t in re.findall(r"[a-z]{3,}", src.lower()):
            if t not in ("the", "and", "for", "advisory", "default", "unknown", "ferres"):
                tokens.add(t)
    hits = []
    for entry in sorted(os.listdir(VAULT_MARKETS)):
        full = os.path.join(VAULT_MARKETS, entry)
        if not os.path.isdir(full):
            continue
        name_tokens = set(re.findall(r"[a-z]{3,}", entry.lower()))
        if tokens & name_tokens:
            hits.append(full)
    return hits


# --- Verbatim-phrase counting -----------------------------------------------------------

# A verbatim customer phrase looks like one of:
#   1. "..." quoted line, optionally numbered ('1. "we..."') — the dominant VOC-dump shape.
#   2. a markdown blockquote line that contains a quoted span.
# We count DISTINCT quoted spans of >=4 words across the client's research files. Quotes
# under 4 words (e.g. a 1-word tag) don't count as a "language pattern".
RE_QUOTED_SPAN = re.compile(r"[\"“]([^\"“”]{12,})[\"”]")


def _is_verbatim_source(fp):
    """Only count quotes from research-bearing prose, not config JSON.

    A verbatim customer phrase lives in a VOC dump, a research/market markdown file, or the
    buyer-profile. A quoted string inside metrics-config.json or a routing config is metadata,
    not customer language — counting it would inflate the floor dishonestly.
    """
    low = fp.lower()
    if low.endswith((".json", ".jsonl", ".ndjson")):
        return False
    return (
        os.sep + "research" + os.sep in low
        or os.sep + "market" + os.sep in low
        or os.path.basename(low) in ("buyer-profile.md", "buyer-language.md", "icp.md",
                                     "story-bank.md")
    )


def count_verbatim_phrases(dirs):
    """Count distinct quoted customer phrases (>=4 words) across the client's research prose.

    Scoped to research/market files + buyer-profile (see _is_verbatim_source) so config JSON
    strings never pad the count. Returns (count, up-to-3 samples)."""
    seen = set()
    sample = []
    for fp in iter_text_files(dirs):
        if not _is_verbatim_source(fp):
            continue
        try:
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                body = fh.read()
        except OSError:
            continue
        for m in RE_QUOTED_SPAN.finditer(body):
            phrase = m.group(1).strip()
            if len(phrase.split()) < 4:
                continue
            norm = re.sub(r"\s+", " ", phrase.lower())
            if norm in seen:
                continue
            seen.add(norm)
            if len(sample) < 3:
                sample.append((phrase[:70], os.path.relpath(fp, HOME)))
    return len(seen), sample


# --- Requirement resolution -------------------------------------------------------------

def _file_has_real_content(fp, min_nonblank_lines=3):
    """A template file with only headers/blank lines should NOT satisfy a requirement.

    Counts non-blank, non-pure-header lines. An empty buyer-language.md (just '## Pains'
    headers) fails this; a filled one passes.
    """
    try:
        with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
            lines = fh.readlines()
    except OSError:
        return False
    real = 0
    for l in lines:
        s = l.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        if s.startswith(">") and "fictional" in s.lower():
            continue  # smoke-test data banner
        real += 1
    return real >= min_nonblank_lines


def resolve_source_type(src, client_dirs, vault_dirs):
    """A source type is SATISFIED if any client-or-vault file's NAME matches a keyword AND
    the file carries real content. Returns (ok, evidence_path_or_none)."""
    keywords = [k.lower() for k in (src.get("match") or [])]
    if not keywords:
        return True, "(no keywords — auto-pass)"
    for fp in iter_text_files(client_dirs + vault_dirs):
        name = os.path.basename(fp).lower()
        if any(k in name for k in keywords) and _file_has_real_content(fp, 2):
            return True, os.path.relpath(fp, HOME)
    return False, None


def _resolve_path_spec(spec, client_root, vault_dirs):
    """Resolve one resolves_to entry. Returns (matched_path_or_none).

    Two forms:
      - 'research-vault: a.md|b.md'  -> any of those aspect files inside a matched vault dossier
      - a client-relative glob       -> glob under client_root, file must have real content
    """
    spec = spec.strip()
    if spec.lower().startswith("research-vault:"):
        names = [s.strip() for s in spec.split(":", 1)[1].split("|") if s.strip()]
        for vd in vault_dirs:
            for nm in names:
                cand = os.path.join(vd, nm)
                if os.path.isfile(cand) and _file_has_real_content(cand, 2):
                    return os.path.relpath(cand, HOME)
        return None
    # client-relative glob
    for match in sorted(glob.glob(os.path.join(client_root, spec))):
        if os.path.isfile(match) and _file_has_real_content(match, 2):
            return os.path.relpath(match, HOME)
    return None


def resolve_artifact(art, client_root, vault_dirs):
    """An artifact is SATISFIED if ANY of its resolves_to specs resolves. Returns (ok, evidence)."""
    for spec in (art.get("resolves_to") or []):
        hit = _resolve_path_spec(spec, client_root, vault_dirs)
        if hit:
            return True, hit
    return False, None


# --- Scorecard --------------------------------------------------------------------------

def build_scorecard(client_root, brief, used_default):
    slug = os.path.basename(os.path.abspath(client_root))
    niche = brief.get("niche", "(unset)")
    client_dirs = client_source_dirs(client_root)
    vault_dirs = matched_vault_markets(niche, slug)

    items = []  # each: {category, id, label, pass, evidence, fix}

    # 1. required sources
    for src in brief.get("required_sources", []):
        ok, ev = resolve_source_type(src, client_dirs, vault_dirs)
        items.append({
            "category": "source", "id": src.get("id", "?"),
            "label": f"source type: {src.get('id', '?')}",
            "pass": ok, "evidence": ev,
            "fix": ("supply a file whose name matches one of "
                    f"{src.get('match')} in 00_inputs/ or _swipe/research/ (with real content)"),
        })

    # 2. verbatim phrases
    min_phrases = int(brief.get("min_verbatim_phrases", 20) or 20)
    count, sample = count_verbatim_phrases(client_dirs)
    ph_ok = count >= min_phrases
    sample_str = "; ".join(f'"{s}…" ({p})' for s, p in sample) if sample else "(none found)"
    items.append({
        "category": "verbatim", "id": "min_verbatim_phrases",
        "label": f"verbatim phrases: {count}/{min_phrases}",
        "pass": ph_ok, "evidence": sample_str,
        "fix": (f"add quoted customer phrases (>=4 words each) to research files until you "
                f"reach {min_phrases}; you have {count}"),
    })

    # 3. required artifacts
    for art in brief.get("required_artifacts", []):
        ok, ev = resolve_artifact(art, client_root, vault_dirs)
        items.append({
            "category": "artifact", "id": art.get("id", "?"),
            "label": f"artifact: {art.get('id', '?')} — {art.get('what', '')}",
            "pass": ok, "evidence": ev,
            "fix": ("create one of: " + " | ".join(art.get("resolves_to", []))),
        })

    # 4. compliance constraints — checked as NAMED-PRESENT (the brief must carry them)
    for cc in brief.get("compliance_constraints", []):
        named = bool(cc.get("id"))
        items.append({
            "category": "compliance", "id": cc.get("id", "?"),
            "label": f"compliance named: {cc.get('id', '?')}",
            "pass": named, "evidence": cc.get("note", ""),
            "fix": "name this constraint in research-brief.md compliance_constraints[]",
        })

    overall = all(it["pass"] for it in items)
    return {
        "client": slug,
        "client_root": os.path.relpath(client_root, HOME),
        "niche": niche,
        "used_default_floor": used_default,
        "vault_dossiers_matched": [os.path.relpath(v, HOME) for v in vault_dirs],
        "overall": "PASS" if overall else "FAIL",
        "items": items,
        "thin_data_fallback": [s.get("step") for s in brief.get("thin_data_fallback", [])],
        "human_read_through": brief.get("human_read_through", {}),
    }


def print_human(card):
    print("RESEARCH GATE")
    print(f"client: {card['client']}   niche: {card['niche']}")
    if card["used_default_floor"]:
        print("NOTE: no _brand/research-brief.md found — using the Ferres-floor defaults "
              "(3 named artifacts, >=20 verbatim phrases, gap analysis). Add a research-brief.md "
              "to tune this per niche.")
    if card["vault_dossiers_matched"]:
        print(f"research-vault dossiers in scope: {', '.join(card['vault_dossiers_matched'])}")
    else:
        print("research-vault dossiers in scope: (none matched by niche/slug)")
    print()

    width = max((len(it["label"]) for it in card["items"]), default=10)
    for it in card["items"]:
        mark = "PASS" if it["pass"] else "FAIL"
        line = f"  [{mark}] {it['label'].ljust(width)}"
        if it["pass"] and it["evidence"]:
            line += f"   <- {it['evidence']}"
        print(line)
        if not it["pass"]:
            print(f"         fix: {it['fix']}")
    print()
    print(f"OVERALL: {card['overall']}")
    if card["overall"] == "FAIL":
        print("\nResearch is not complete. Do NOT generate from thin research. Options:")
        print("  - close each FAIL above, OR")
        print("  - walk the thin-data fallback ladder: "
              + " -> ".join(card["thin_data_fallback"]))
        print("  - last resort: operator records a research_gate_override (with reason) "
              "in the campaign's pipeline-state.json")
    hr = card.get("human_read_through") or {}
    if hr.get("required"):
        print(f"\nReminder: human read-through is required (record in: {hr.get('record_in', '?')}). "
              "The gate cannot verify this — a person must.")


def main(argv=None):
    p = argparse.ArgumentParser(description="Research-completeness gate for a client.")
    p.add_argument("--client", required=True, metavar="PATH",
                   help="path to clients/<slug> (the client root)")
    p.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = p.parse_args(argv)

    client_root = os.path.abspath(args.client)
    if not os.path.isdir(client_root):
        print(f"error: client root not found: {args.client}", file=sys.stderr)
        return 2

    brief, used_default = load_brief(client_root)
    card = build_scorecard(client_root, brief, used_default)

    if args.json:
        print(json.dumps(card, indent=2))
    else:
        print_human(card)

    return 0 if card["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
