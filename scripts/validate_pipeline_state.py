#!/usr/bin/env python3
"""Validate pipeline-state.json files against the canonical (permissive) schema.

The schema spec lives in scripts/pipeline_state_schema.json. This validator implements
that contract in plain Python — no jsonschema dependency, so it runs anywhere python3 does.

It NEVER repairs a file. It tells you what is wrong, which file, and what to do.

Usage:
  validate_pipeline_state.py <file> [<file> ...]   # check named files
  validate_pipeline_state.py --all                 # scan clients/*/campaigns recursively
  validate_pipeline_state.py --all --strict        # treat WARNs as failures too

Exit codes: 0 = all clean (warnings allowed unless --strict), 1 = at least one FAIL.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

WHERE_FIELDS = ("client", "campaign", "workspace", "workspace_id", "concept_slug", "workspace_slug")
PHASE_FIELDS = ("current_phase", "phase", "current_stage")
WHEN_FIELDS = ("last_updated", "updated_at", "last_modified", "created_date", "created")

CANONICAL_WHERE = ("client", "campaign")
CANONICAL_PHASE = "current_phase"
CANONICAL_WHEN = "last_updated"

# Phase tokens seen in the wild. Membership = recognized (no warning).
KNOWN_PHASES = {
    # dct lane
    "phase_0_context", "phase_1_angles", "phase_2_assembly", "phase_3_render",
    "phase_3b_allocate", "phase_3_creative_gate", "phase_4_sheet", "phase_5_upload",
    "PARKED", "PARTIAL_UPLOAD__BLOCKED_SG_ADVERTISER_VERIFICATION",
    # video-concept lane
    "phase_0_preflight", "phase_1_strategy", "phase_2_ag1_options", "phase_3_scripts",
    "phase_4_synthesis", "phase_5_ag1", "phase_6_refinement", "phase_7_ag2",
    "ag1_review", "ag1_review_pending_operator_taste_pass",
    # sales-letter lane
    "phase_0_foundation", "phase_1_leads", "phase_2_spine", "phase_3_body_draft",
    "phase_4_gate", "phase_5_assembly", "phase_6_ship",
}
# A phase value matching one of these is accepted without warning even if not in KNOWN_PHASES.
PHASE_PATTERNS = (
    re.compile(r"^phase_[0-9]+[a-z]?(_[a-z0-9]+)*$"),  # phase_3b_allocate etc.
    re.compile(r"^x-.+"),                               # explicit custom
    re.compile(r"^[A-Z][A-Z0-9_]+$"),                   # SHOUTING status tokens
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}([T ].*)?$")


class Finding:
    __slots__ = ("level", "msg", "fix")

    def __init__(self, level, msg, fix=""):
        self.level = level  # "FAIL" or "WARN"
        self.msg = msg
        self.fix = fix


def first_present(d, fields):
    for f in fields:
        if f in d and d[f] not in (None, ""):
            return f
    return None


def validate_doc(doc):
    """Return list[Finding] for one already-parsed JSON document (a dict)."""
    findings = []

    if not isinstance(doc, dict):
        findings.append(Finding(
            "FAIL",
            f"top-level value is a {type(doc).__name__}, not a JSON object",
            "a pipeline-state file must be a single JSON object {...}",
        ))
        return findings

    # --- WHERE family (required) ---
    where = first_present(doc, WHERE_FIELDS)
    if where is None:
        findings.append(Finding(
            "FAIL",
            "no WHERE identity field — none of: " + ", ".join(WHERE_FIELDS),
            "add `client` + `campaign`, or a `workspace` path string "
            "(e.g. clients/<slug>/campaigns/<campaign>/...)",
        ))
    else:
        has_canon = all(f in doc and doc[f] not in (None, "") for f in CANONICAL_WHERE)
        # `workspace`/`workspace_id` path-string also satisfies canonical-equivalent WHERE.
        path_like = any(
            isinstance(doc.get(f), str) and "/" in doc.get(f, "")
            for f in ("workspace", "workspace_id")
        )
        if not has_canon and not path_like:
            findings.append(Finding(
                "WARN",
                f"WHERE satisfied by alias `{where}` only — canonical is `client` + `campaign`",
                "add explicit `client` and `campaign` keys when next editing this file",
            ))

    # --- PHASE family (required) ---
    phase_field = None
    for f in PHASE_FIELDS:
        if f in doc:
            phase_field = f
            break
    if phase_field is None:
        findings.append(Finding(
            "FAIL",
            "no PHASE field — none of: " + ", ".join(PHASE_FIELDS),
            "add `current_phase` naming the current pipeline phase",
        ))
    else:
        val = doc[phase_field]
        if val in (None, ""):
            findings.append(Finding(
                "FAIL",
                f"`{phase_field}` is present but null/empty",
                "set it to a real phase token (e.g. phase_3_render) or x-<custom>",
            ))
        else:
            if phase_field != CANONICAL_PHASE:
                findings.append(Finding(
                    "WARN",
                    f"PHASE named via alias `{phase_field}` — canonical is `current_phase`",
                    "rename to `current_phase` when next editing",
                ))
            sval = str(val)
            recognized = sval in KNOWN_PHASES or any(p.match(sval) for p in PHASE_PATTERNS)
            if not recognized:
                findings.append(Finding(
                    "WARN",
                    f"phase value `{sval}` is not a known token and is not x-prefixed",
                    "if intentional/custom, prefix it with `x-` so it reads as deliberate",
                ))

    # --- WHEN family (required) ---
    when = first_present(doc, WHEN_FIELDS)
    if when is None:
        findings.append(Finding(
            "FAIL",
            "no WHEN field — none of: " + ", ".join(WHEN_FIELDS),
            "add `last_updated` as an ISO date (YYYY-MM-DD)",
        ))
    else:
        if when != CANONICAL_WHEN:
            findings.append(Finding(
                "WARN",
                f"WHEN named via alias `{when}` — canonical is `last_updated`",
                "rename to `last_updated` when next editing",
            ))
        wval = doc[when]
        if isinstance(wval, str) and not DATE_RE.match(wval):
            findings.append(Finding(
                "WARN",
                f"`{when}` value `{wval}` is not an ISO date (YYYY-MM-DD / full ISO)",
                "use a YYYY-MM-DD stamp so freshness sorts correctly",
            ))

    # --- phases block sanity (optional, but if present must be an object) ---
    if "phases" in doc and not isinstance(doc["phases"], dict):
        findings.append(Finding(
            "WARN",
            f"`phases` is a {type(doc['phases']).__name__}, expected an object map",
            "phases should map phase_name -> {status, ...}",
        ))

    return findings


def validate_file(path):
    """Return (findings, parsed_or_None). A parse failure yields one FAIL finding."""
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
    except OSError as e:
        return [Finding("FAIL", f"cannot read file: {e}", "check the path exists and is readable")], None
    try:
        doc = json.loads(text)
    except json.JSONDecodeError as e:
        return [Finding(
            "FAIL",
            f"invalid JSON: {e.msg} at line {e.lineno} col {e.colno}",
            "fix the JSON syntax (trailing comma? unquoted key? truncated file?)",
        )], None
    return validate_doc(doc), doc


def discover():
    """All pipeline-state.json under clients/*/campaigns, skipping _archive."""
    out = []
    base = REPO_ROOT / "clients"
    if not base.exists():
        return out
    for f in sorted(base.glob("*/campaigns/**/pipeline-state.json")):
        if "_archive" in f.parts:
            continue
        out.append(f)
    return out


def rel(path):
    try:
        return str(Path(path).resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def main():
    ap = argparse.ArgumentParser(description="Validate pipeline-state.json files (permissive schema).")
    ap.add_argument("files", nargs="*", help="explicit files to check")
    ap.add_argument("--all", action="store_true", help="scan clients/*/campaigns recursively")
    ap.add_argument("--strict", action="store_true", help="treat WARN as failure")
    args = ap.parse_args()

    if args.all:
        targets = discover()
        if args.files:
            targets += [Path(x) for x in args.files]
    elif args.files:
        targets = [Path(x) for x in args.files]
    else:
        ap.error("give one or more files, or --all")

    if not targets:
        print("no pipeline-state.json files found to validate.")
        return 0

    n_fail = n_warn = n_clean = 0
    failed_files = []

    for t in targets:
        findings, _ = validate_file(t)
        fails = [f for f in findings if f.level == "FAIL"]
        warns = [f for f in findings if f.level == "WARN"]
        label = rel(t)
        if not findings:
            n_clean += 1
            print(f"OK    {label}")
            continue
        if fails:
            n_fail += 1
            failed_files.append(label)
            print(f"FAIL  {label}")
        else:
            n_warn += 1
            print(f"WARN  {label}")
        for f in fails:
            print(f"        [FAIL] {f.msg}")
            if f.fix:
                print(f"               -> {f.fix}")
        for f in warns:
            print(f"        [warn] {f.msg}")
            if f.fix:
                print(f"               -> {f.fix}")

    print()
    print(f"summary: {n_clean} clean, {n_warn} warn-only, {n_fail} failed "
          f"({len(targets)} checked)")
    if failed_files:
        print("failed files:")
        for fl in failed_files:
            print(f"  - {fl}")

    if n_fail:
        return 1
    if args.strict and n_warn:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
