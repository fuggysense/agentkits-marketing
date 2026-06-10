#!/usr/bin/env python3
"""Score-and-resolve gate for ad hooks/headlines. Reads a hooks JSON, then code-decides:
every hook must clear an average-score threshold AND carry an insight tag that resolves to a
real file at a real line/anchor. Fails the build (exit 1) listing exactly what broke.

Two jobs, per Ferres 03-angles-hooks-copy.md §"Hook rules": a hook must scroll-stop AND speak
to the avatar's real situation in their own language. This gate enforces the second half
mechanically — a hook is only as good as the research line it stands on. Untagged or
dangling-tag hooks are invalid output (headline-bank SKILL.md, "insight tag" rule).

INPUT SHAPE (the JSON headline-bank emits before output is final):
  [
    {
      "hook": "We overpaid maybe 40-50k on our first flat. Not twice.",
      "scores": {
        "clarity":             5,   # 1-5  does a cold reader get it in one pass
        "avatar_match":        5,   # 1-5  would THIS avatar think "that's me"
        "flow":                4,   # 1-5  reads aloud clean, greased-slide
        "insight_tag_resolves":5,   # 1-5  operator's confidence the tag is real (gate re-checks)
        "native_feel":         4    # 1-5  feed-native, not salesy / not an AI tell
      },
      "insight": "clients/_smoketest/00_inputs/research/voc-reddit-dump-260611.md#L36 — upgrader overpaid 40-50k, won't repeat"
    },
    ...
  ]

INSIGHT-TAG FORMAT (headline-bank SKILL.md):
  "<research-file>#<line-or-anchor> — <≤8-word paraphrase>"
  - <research-file>      : path to an existing file (absolute, or relative to --root / cwd)
  - #<line-or-anchor>    : #L<n> (1-based line) OR #<markdown-heading-or-anchor-text>
  - — <paraphrase>       : human gloss, not checked by the gate (presence not required)

PASS RULE (all must hold for every hook, else exit 1):
  1. avg of the five 1-5 scores >= --threshold (default 4.0)
  2. an "insight" tag is present and non-empty
  3. the tag's file exists
  4. the tag's #anchor resolves: a line number in range, OR an anchor string found in the file

Design rules (mirrors scripts/claim_gate.py):
  - Read-only. Never edits input. NO network / Meta / sheet / render calls. stdlib only.
  - Fail-closed: any failing hook exits 1 with a plain-language reason and the fix.
  - Anchor matching is forgiving: #L42 is exact; a text anchor matches a markdown heading
    slug ("## The Core Problem" -> #the-core-problem) or any verbatim substring in the file.

Usage:
  python3 scripts/hook_gate.py hooks.json
  python3 scripts/hook_gate.py hooks.json --threshold 4.0
  python3 scripts/hook_gate.py hooks.json --root "clients/_smoketest"   # resolve relative tags
  python3 scripts/hook_gate.py hooks.json --audit                       # report, always exit 0
"""

import argparse
import json
import os
import re
import sys

SCORE_KEYS = ("clarity", "avatar_match", "flow", "insight_tag_resolves", "native_feel")

# An insight tag splits on the LAST '#' before the anchor: "<file>#<anchor> — <gloss>".
# The em-dash gloss is optional and never validated.
RE_TAG = re.compile(r"^\s*(?P<file>.+?)#(?P<anchor>[^\s].*?)\s*(?:[—-]{1,2}\s.*)?$")
RE_LINE_ANCHOR = re.compile(r"^L?(\d+)$", re.IGNORECASE)


def _slugify_heading(text):
    """GitHub-style heading slug: lowercase, strip non-word, spaces -> hyphens."""
    s = text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s.strip("-")


def parse_tag(insight):
    """Return (file, anchor) from an insight tag, or (None, None) if unparseable."""
    if not insight or not isinstance(insight, str):
        return None, None
    m = RE_TAG.match(insight)
    if not m:
        return None, None
    return m.group("file").strip(), m.group("anchor").strip()


def resolve_file(file_ref, root):
    """Resolve a tag's file path against (a) as-given, (b) --root, (c) cwd. First hit wins."""
    candidates = [file_ref]
    if root:
        candidates.append(os.path.join(root, file_ref))
    candidates.append(os.path.join(os.getcwd(), file_ref))
    for c in candidates:
        if os.path.isfile(c):
            return os.path.abspath(c)
    return None


def anchor_resolves(path, anchor):
    """True if the anchor points at something real in the file.

    #L<n>      -> 1-based line number must be within the file's line count.
    #<text>    -> matches a markdown-heading slug in the file, OR appears verbatim
                  (case-insensitive substring) anywhere in the body.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            lines = fh.readlines()
    except OSError:
        return False
    body = "".join(lines)

    m = RE_LINE_ANCHOR.match(anchor)
    if m:
        n = int(m.group(1))
        return 1 <= n <= len(lines)

    want = _slugify_heading(anchor)
    for ln in lines:
        if ln.lstrip().startswith("#"):
            heading = ln.lstrip("#").strip()
            if _slugify_heading(heading) == want or heading.lower() == anchor.lower():
                return True
    return anchor.lower() in body.lower()


def avg_score(scores):
    """Mean of the five 1-5 dimensions. Returns (avg, missing_keys, bad_keys)."""
    missing = [k for k in SCORE_KEYS if k not in (scores or {})]
    vals, bad = [], []
    for k in SCORE_KEYS:
        v = (scores or {}).get(k)
        if isinstance(v, (int, float)) and 1 <= v <= 5:
            vals.append(float(v))
        elif v is not None:
            bad.append(k)
    avg = sum(vals) / len(vals) if vals else 0.0
    return avg, missing, bad


def evaluate(hooks, threshold, root):
    """Return a list of per-hook result dicts."""
    results = []
    for i, h in enumerate(hooks):
        hook_text = (h.get("hook") or "").strip() if isinstance(h, dict) else ""
        scores = h.get("scores") if isinstance(h, dict) else None
        insight = h.get("insight") if isinstance(h, dict) else None

        avg, missing, bad = avg_score(scores)
        fails = []

        if missing:
            fails.append(f"missing score dimension(s): {', '.join(missing)}")
        if bad:
            fails.append(f"score(s) not in 1-5: {', '.join(bad)}")
        if avg < threshold:
            fails.append(f"avg score {avg:.2f} below threshold {threshold:.2f}")

        file_ref, anchor = parse_tag(insight)
        if not insight:
            fails.append("no insight tag (untagged hooks are invalid output)")
        elif file_ref is None:
            fails.append(
                f'insight tag unparseable: "{insight}" '
                "(expected <file>#<line-or-anchor> — <paraphrase>)"
            )
        else:
            resolved = resolve_file(file_ref, root)
            if not resolved:
                fails.append(f"insight file not found: {file_ref}")
            elif not anchor_resolves(resolved, anchor):
                fails.append(f"insight anchor does not resolve: #{anchor} in {file_ref}")

        results.append({
            "index": i,
            "hook": hook_text,
            "avg": avg,
            "insight": insight or "",
            "fails": fails,
            "pass": not fails,
        })
    return results


def run(path, threshold, root, audit):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        print("error: hooks JSON must be a top-level array of hook objects", file=sys.stderr)
        return 2

    results = evaluate(data, threshold, root)
    failed = [r for r in results if not r["pass"]]

    if audit:
        print(f"HOOK GATE — AUDIT\nfile: {path}")
        print(f"threshold: {threshold:.2f}   hooks: {len(results)}   failing: {len(failed)}\n")
        for r in results:
            tag = "PASS" if r["pass"] else "FAIL"
            short = (r["hook"][:60] + "…") if len(r["hook"]) > 61 else r["hook"]
            print(f"  [{tag}] avg {r['avg']:.2f}  \"{short}\"")
            for f in r["fails"]:
                print(f"         - {f}")
        return 0

    if not failed:
        print(f"HOOK GATE — PASS  ({len(results)} hooks, all clear threshold {threshold:.2f} "
              "and resolve their insight tag)")
        print(f"file: {path}")
        return 0

    print(f"HOOK GATE — FAIL  ({len(failed)} of {len(results)} hooks blocked)")
    print(f"file: {path}\n")
    print("Never ship a blocked hook. Each must be fixed before the copy is final:\n")
    for r in failed:
        short = (r["hook"][:70] + "…") if len(r["hook"]) > 71 else r["hook"]
        print(f"  HOOK #{r['index']}: \"{short or '(empty)'}\"")
        for f in r["fails"]:
            print(f"    - {f}")
        print("    fix one of: (a) raise the weak dimension(s) and re-score, "
              "(b) point the insight tag at a real file#line/anchor, or (c) cut the hook.\n")
    return 1


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Score + insight-tag gate for ad hooks/headlines (see --help for shape).")
    p.add_argument("hooks", metavar="HOOKS_JSON", help="path to the hooks JSON array")
    p.add_argument("--threshold", type=float, default=4.0,
                   help="minimum average of the five 1-5 scores (default 4.0)")
    p.add_argument("--root", default=None,
                   help="base dir for resolving relative insight-tag file paths "
                        "(e.g. clients/<slug>); cwd is also tried")
    p.add_argument("--audit", action="store_true",
                   help="print the per-hook table and always exit 0 (no fail-closed)")
    args = p.parse_args(argv)

    if not os.path.isfile(args.hooks):
        print(f"error: file not found: {args.hooks}", file=sys.stderr)
        return 2
    return run(args.hooks, args.threshold, args.root, args.audit)


if __name__ == "__main__":
    sys.exit(main())
