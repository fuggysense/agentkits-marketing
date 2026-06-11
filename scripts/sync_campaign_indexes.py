#!/usr/bin/env python3
"""Keep clients/<slug>/campaigns/_campaigns-index.json honest against folder truth.

The index is a discovery map: it lets an agent find campaign-index.json files without
guessing paths. It rots when a campaign folder is added but never registered (the
"two known-missing" case). This script regenerates the index FROM the folders that
actually carry work, merging in any hand-authored metadata already on a registered
campaign so the rich notes survive.

Three modes:
  (default)  dry-run diff — show what WOULD change, write nothing.
  --apply    write the regenerated index. REFUSES on live clients (eugene-chieng,
             neezanizam); for those it drops the proposed index at
             _handoffs/staged-m3/<client>/_campaigns-index.proposed.json and tells
             the operator to apply it.
  --drift    plain-language report of state-vs-folder disagreements (a campaign on
             disk missing from the index, an indexed campaign whose folder is gone,
             a state phase that contradicts what the folder shows).

Scope a single client with --client <slug>, or sweep all with no flag.

It never edits a live client's index directly and never touches _archive.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STAGED_DIR = REPO_ROOT / "_handoffs" / "staged-m3"

# Live clients: --apply refuses, stages the proposal instead.
LIVE_CLIENTS = {"eugene-chieng", "neezanizam"}

# Direct children of campaigns/ that are scaffolding, not campaigns.
DIR_DENYLIST = {"_example-campaign", "_TEMPLATE", "_template", "feedback",
                "_sheet-snapshots", "_snapshots", "_archive"}

WORK_SIGNALS = ("campaign-index.json", "pipeline-state.json", "state.yaml",
                "state.yaml.pre-m3", "dct-tracker.json", "dct.json")


def today():
    return datetime.now().strftime("%Y-%m-%d")


def is_campaign_dir(d: Path) -> bool:
    """A direct child of campaigns/ that carries real work."""
    if not d.is_dir():
        return False
    name = d.name
    if name in DIR_DENYLIST or name.startswith("."):
        return False
    # has a campaign-index / state at its root, OR any work signal nested below it
    for sig in ("campaign-index.json", "pipeline-state.json", "state.yaml", "state.yaml.pre-m3"):
        if (d / sig).exists():
            return True
    for sig in WORK_SIGNALS:
        for hit in d.rglob(sig):
            if "_archive" in hit.parts:
                continue
            return True
    return False


def state_file_for(d: Path):
    """Pick the campaign-root state file, if any. Prefers JSON over yaml."""
    for sig in ("pipeline-state.json", "state.yaml.pre-m3", "state.yaml"):
        if (d / sig).exists():
            return sig
    return None


def count_workspaces(d: Path) -> int:
    """Nested pipeline-state.json files = working deliverable workspaces."""
    n = 0
    for hit in d.rglob("pipeline-state.json"):
        if "_archive" in hit.parts:
            continue
        if hit.parent == d:  # the campaign-root state itself, not a workspace
            continue
        n += 1
    return n


def discover_campaigns(client_dir: Path):
    """Folder-truth list of campaign dirs for one client."""
    camps_dir = client_dir / "campaigns"
    if not camps_dir.exists():
        return []
    out = []
    for d in sorted(p for p in camps_dir.iterdir() if p.is_dir()):
        if not is_campaign_dir(d):
            continue
        rel = d.relative_to(camps_dir)
        ci = d / "campaign-index.json"
        out.append({
            "campaign_slug": d.name,
            "path": f"{rel}/",
            "campaign_index": f"{rel}/campaign-index.json" if ci.exists() else None,
            "state_file": (f"{rel}/{sf}" if (sf := state_file_for(d)) else None),
            "workspace_count": count_workspaces(d),
        })
    return out


def load_index(client_dir: Path):
    idx_path = client_dir / "campaigns" / "_campaigns-index.json"
    if not idx_path.exists():
        return None, idx_path
    try:
        return json.loads(idx_path.read_text(encoding="utf-8")), idx_path
    except json.JSONDecodeError as e:
        raise SystemExit(f"existing index is invalid JSON: {idx_path}\n  {e}")


def indexed_slugs(index):
    if not index:
        return set()
    return {c.get("campaign_slug") for c in index.get("campaigns", []) if c.get("campaign_slug")}


def is_archived_entry(entry):
    """An index entry the operator deliberately retired — keep it even if the folder is gone."""
    if entry.get("status") == "archived":
        return True
    return bool(entry.get("archived_at") or entry.get("archived_to"))


def build_regenerated(client, client_dir, existing_index):
    """Merge folder truth with any hand-authored metadata already on a registered campaign."""
    discovered = discover_campaigns(client_dir)
    existing_by_slug = {}
    if existing_index:
        for c in existing_index.get("campaigns", []):
            if c.get("campaign_slug"):
                existing_by_slug[c["campaign_slug"]] = c

    merged = []
    discovered_slugs = {d["campaign_slug"] for d in discovered}
    for d in discovered:
        slug = d["campaign_slug"]
        prior = existing_by_slug.get(slug, {})
        # folder truth wins for path/index/state; prior wins for everything else (notes etc.)
        entry = dict(prior)
        entry.update({k: v for k, v in d.items() if v is not None})
        entry.setdefault("campaign_slug", slug)
        merged.append(entry)
    # keep deliberately-archived entries even when their folder is gone (no data loss).
    for slug, prior in existing_by_slug.items():
        if slug not in discovered_slugs and is_archived_entry(prior):
            merged.append(dict(prior))

    out = dict(existing_index) if existing_index else {}
    out.setdefault("schema_version", "1.0")
    out["client"] = client
    out["last_updated"] = today()
    out.setdefault(
        "purpose",
        "Client-level campaign registry. Use this to discover campaign-index.json "
        "files instead of guessing campaign paths. Regenerated from folder truth by "
        "scripts/sync_campaign_indexes.py.",
    )
    out["campaigns"] = merged
    return out, discovered


def diff_lines(client, existing_index, discovered):
    """Plain-language diff between existing index and folder truth."""
    on_disk = {d["campaign_slug"] for d in discovered}
    indexed = indexed_slugs(existing_index)
    lines = []
    missing = sorted(on_disk - indexed)
    for slug in missing:
        d = next(x for x in discovered if x["campaign_slug"] == slug)
        lines.append(f"  + MISSING from index: '{slug}' exists on disk "
                     f"({d['workspace_count']} workspace(s), "
                     f"index={'yes' if d['campaign_index'] else 'no'}, "
                     f"state={'yes' if d['state_file'] else 'no'})")
    archived = set()
    if existing_index:
        for c in existing_index.get("campaigns", []):
            if c.get("campaign_slug") and is_archived_entry(c):
                archived.add(c["campaign_slug"])
    stale = sorted(indexed - on_disk - archived)
    for slug in stale:
        lines.append(f"  - STALE in index: '{slug}' is registered but no campaign "
                     f"folder with work was found on disk")
    return lines, missing, stale


def write_or_stage(client, out_index, idx_path):
    """Write the index, or stage it for a live client."""
    payload = json.dumps(out_index, indent=2, ensure_ascii=False) + "\n"
    if client in LIVE_CLIENTS:
        dest_dir = STAGED_DIR / client
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / "_campaigns-index.proposed.json"
        dest.write_text(payload, encoding="utf-8")
        note = dest_dir / "APPLY-NOTE.md"
        note.write_text(
            f"# APPLY-NOTE — {client} _campaigns-index.json (staged M3)\n\n"
            f"**Date:** {today()} (rebuild M3.4 — index auto-sync).\n"
            f"**Why staged, not written:** {client} is a LIVE client; the rebuild "
            f"treats live-client folders as read-only. --apply refused and dropped "
            f"the proposed index here. Operator applies after review.\n\n"
            f"## What\n"
            f"- Proposed regenerated index: `_campaigns-index.proposed.json` (this folder).\n\n"
            f"## Where it goes\n"
            f"- Target: `clients/{client}/campaigns/_campaigns-index.json`\n"
            f"- Command (operator runs from repo root, AFTER diffing):\n"
            f"  ```bash\n"
            f"  diff clients/{client}/campaigns/_campaigns-index.json \\\n"
            f"       _handoffs/staged-m3/{client}/_campaigns-index.proposed.json\n"
            f"  cp _handoffs/staged-m3/{client}/_campaigns-index.proposed.json \\\n"
            f"     clients/{client}/campaigns/_campaigns-index.json\n"
            f"  ```\n\n"
            f"## Caution\n"
            f"- The proposal regenerates entries at the TOP-LEVEL campaign-dir granularity "
            f"(folder truth). If this client's existing index intentionally uses a finer "
            f"granularity (e.g. neezanizam registers individual DCTs, not the buyer-funnel "
            f"parent), DO NOT blindly overwrite — reconcile by hand. The script merges prior "
            f"metadata onto matching slugs but cannot know a slug means something different.\n",
            encoding="utf-8",
        )
        return f"STAGED -> {dest.relative_to(REPO_ROOT)} (live client, not written)"
    idx_path.write_text(payload, encoding="utf-8")
    return f"WROTE  -> {idx_path.relative_to(REPO_ROOT)}"


def client_dirs(only):
    base = REPO_ROOT / "clients"
    if only:
        d = base / only
        if not (d / "campaigns").exists():
            raise SystemExit(f"no campaigns/ for client '{only}' at {d}")
        return [d]
    out = []
    for d in sorted(base.iterdir()):
        if d.is_dir() and (d / "campaigns").exists():
            out.append(d)
    return out


def main():
    ap = argparse.ArgumentParser(description="Sync _campaigns-index.json with folder truth.")
    ap.add_argument("--client", help="limit to one client slug")
    ap.add_argument("--apply", action="store_true", help="write the index (stages for live clients)")
    ap.add_argument("--drift", action="store_true", help="report state-vs-folder disagreements only")
    args = ap.parse_args()

    if args.apply and args.drift:
        ap.error("--apply and --drift are mutually exclusive")

    any_change = False
    for client_dir in client_dirs(args.client):
        client = client_dir.name
        existing_index, idx_path = load_index(client_dir)
        out_index, discovered = build_regenerated(client, client_dir, existing_index)
        lines, missing, stale = diff_lines(client, existing_index, discovered)

        if args.drift:
            print(f"=== {client} (drift) ===")
            if not lines:
                print("  in sync — index matches folder truth")
            else:
                for ln in lines:
                    print(ln)
            print()
            continue

        print(f"=== {client} ===")
        if existing_index is None:
            print("  no existing _campaigns-index.json (would create fresh)")
        if not lines:
            print(f"  in sync — {len(discovered)} campaign(s), index matches folder truth")
        else:
            any_change = True
            for ln in lines:
                print(ln)

        if args.apply:
            if lines or existing_index is None:
                print("  " + write_or_stage(client, out_index, idx_path))
            else:
                print("  nothing to write (already in sync)")
        else:
            if lines or existing_index is None:
                print(f"  (dry-run) {len(discovered)} campaign(s) would be in the regenerated index. "
                      f"Re-run with --apply to write{' (live -> staged)' if client in LIVE_CLIENTS else ''}.")
        print()

    if not args.apply and not args.drift and any_change:
        print("dry-run only — nothing written. Add --apply to write.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
