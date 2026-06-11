#!/usr/bin/env python3
"""Status board. One line per client telling you where every client's work sits.

Answers "where is every client / what's next / who is blocking" without opening a single
folder by hand. Reads each client's campaign registry + the campaign-index / state files
the registry points at + folder truth, and prints one terse line per client:

    <client>: <campaign/workspace> @ <phase> — next: <action> — blocked on: <who>

It also flags stale state: when a campaign-index's last_updated lags the newest artifact
mtime under that campaign by more than STALE_DAYS, the line gets a "[stale: ...]" tag. That
catches the common failure where work happened on disk but nobody bumped the index.

Truth precedence per campaign:
  1. campaign-index.json (or the state_file the registry names: state.yaml)
  2. the active workspace's pipeline-state.json (deepest current phase + blockers)
  3. folder truth (mtimes, which subfolders exist) when neither names a phase

Design rules (mirrors scripts/research_gate.py and scripts/claim_gate.py):
  - Read-only. Never edits anything. No network / Meta / sheet / render calls.
  - Stdlib only. No YAML dep — a tiny line reader pulls the handful of scalar keys we need.
  - Plain text, capped under 40 lines so it stays a glance, not a report.

Usage:
    python3 scripts/status_board.py                 # all clients
    python3 scripts/status_board.py eugene-chieng    # one client
    python3 scripts/status_board.py --json            # machine-readable
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import date, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENTS = os.path.join(REPO, "clients")
STALE_DAYS = 3
MAX_LINES = 40
SKIP_DIRS = ("_archive", "_template")  # also catches _template.old via prefix check
# Folders that aren't real artifacts when scanning for newest mtime.
MTIME_SKIP = {".git", "node_modules", "__pycache__", ".DS_Store", "_archive"}


def is_skipped(name: str) -> bool:
    return any(name == d or name.startswith(d) for d in SKIP_DIRS)


def load_json(path: str):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def read_yaml_scalars(path: str, keys: set[str]) -> dict:
    """Pull a few top-level-ish scalar keys out of a YAML file without a YAML dep.

    Good enough for state.yaml — we only want phase/stage/next/blocker strings, not
    full structure. Matches 'key: value' anywhere, last write wins. Lists under a key
    (next_actions:) are not parsed; we fall back to first '- ' item after the key.
    """
    found: dict[str, str] = {}
    pending_list_key = None
    try:
        with open(path, encoding="utf-8") as fh:
            for raw in fh:
                line = raw.rstrip("\n")
                stripped = line.strip()
                if pending_list_key and stripped.startswith("- "):
                    found.setdefault(pending_list_key, stripped[2:].strip().strip('"'))
                    pending_list_key = None
                    continue
                if ":" not in stripped or stripped.startswith("#"):
                    continue
                key, _, val = stripped.partition(":")
                key = key.strip()
                val = val.strip().strip('"')
                if key in keys:
                    if val == "":  # likely a list/block follows
                        pending_list_key = key
                    else:
                        found[key] = val
    except OSError:
        return {}
    return found


def parse_date(s) -> date | None:
    if not s or not isinstance(s, str):
        return None
    s = s.strip().strip('"')
    for fmt in ("%Y-%m-%d", "%y%m%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def newest_mtime(folder: str) -> float:
    """Newest mtime of any file under folder, skipping noise dirs. 0 if empty/missing."""
    newest = 0.0
    if not os.path.isdir(folder):
        return newest
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in MTIME_SKIP]
        for f in files:
            if f == ".DS_Store":
                continue
            try:
                m = os.path.getmtime(os.path.join(root, f))
            except OSError:
                continue
            if m > newest:
                newest = m
    return newest


def truncate(s: str, n: int) -> str:
    s = " ".join(str(s).split())
    # Surfaced values are verbatim from data files; normalize arrows/curly quotes to ASCII
    # so the board stays plain text regardless of what a tracker happens to contain.
    for bad, good in (("→", "->"), ("⇒", "=>"), ("“", '"'), ("”", '"'), ("‘", "'"), ("’", "'")):
        s = s.replace(bad, good)
    return s if len(s) <= n else s[: n - 1].rstrip() + "..."


def classify_block(*texts: str) -> str:
    """Map free-text stage/blocker strings to one of: operator, client, gate, nothing."""
    blob = " ".join(t for t in texts if t).lower()
    if not blob:
        return "nothing"
    # Order matters — gate language is most specific, then operator, then client.
    if any(w in blob for w in ("gate", "approval", "approve", "ag1", "ag2", "ag0", "sign-off", "sign off")):
        return "gate"
    if any(w in blob for w in ("operator", "review", "taste pass", "hitl", "pending review", "decision")):
        return "operator"
    if any(w in blob for w in ("client", "founder", "eugene-side", "eugene-confirmed", "awaiting client", "client-side")):
        return "client"
    return "nothing"


def pipeline_state_summary(ps: dict) -> tuple[str, list[str]]:
    """Return (current_phase, blockers[]) from a pipeline-state.json of either shape."""
    phase = ps.get("current_phase") or ps.get("current_stage") or ""
    blockers: list[str] = []
    phases = ps.get("phases")
    if isinstance(phases, dict):
        for pname, pdata in phases.items():
            if isinstance(pdata, dict):
                bl = pdata.get("blockers")
                if isinstance(bl, list):
                    blockers.extend(str(b) for b in bl)
                elif pdata.get("status") == "blocked" and pdata.get("note"):
                    blockers.append(str(pdata["note"]))
    pa = ps.get("pending_approvals")
    if isinstance(pa, list):
        blockers.extend(str(p) for p in pa)
    return phase, blockers


def resolve_tracker(client_dir: str, camp: dict) -> dict | None:
    """Resolve a DCT-tracker campaign entry (neezanizam shape) — no phase string on disk,
    so we synthesize phase from the metrics_campaign + render/upload signals in the tracker."""
    rel = camp.get("tracker_path")
    if not rel:
        return None
    tpath = os.path.join(client_dir, rel)
    tr = load_json(tpath)
    if not isinstance(tr, dict):
        return None
    slug = camp.get("campaign_slug", "?")
    funnel = tr.get("metrics_campaign") or camp.get("metrics_campaign") or ""
    # Normalize noisy funnel labels (e.g. "buyer-funnel (inferred from CLAUDE.md)") so
    # the per-funnel collapse groups them with their clean siblings.
    funnel = funnel.split("(")[0].strip()
    method = camp.get("method", "")
    blockers = tr.get("known_blockers") or []
    nexts = tr.get("next_commands") or []
    # Phase proxy: any canva_link empty / render pending => pre-production; else ready-to-upload.
    raw = json.dumps(tr).lower()
    if "render" in " ".join(nexts[:1]).lower() or "image_prompts" in raw and "canva_link" in raw:
        phase = f"{funnel} / images-pending" if funnel else "images-pending"
    elif blockers:
        phase = f"{funnel} / blocked" if funnel else "blocked"
    else:
        phase = f"{funnel} / ready" if funnel else "ready"
    if method:
        phase += f" ({method})"
    next_action = (nexts[0] if nexts else "") or "(none recorded)"
    blocked = classify_block(phase, *(str(b) for b in blockers), next_action)
    return {
        "slug": slug,
        "phase": phase,
        "next": next_action,
        "blocked": blocked,
        "stale": None,
        "status": camp.get("status", ""),
        "funnel": funnel,
        "mtime": newest_mtime(os.path.dirname(tpath)),
    }


def resolve_campaign(client_dir: str, camp: dict) -> dict:
    """Resolve one campaign registry entry into phase/next/blocked/stale facts."""
    slug = camp.get("campaign_slug") or camp.get("campaign_name") or "?"
    status = camp.get("status", "")
    phase = camp.get("current_stage") or camp.get("current_gate") or status or ""
    next_action = ""
    blocker_texts: list[str] = []

    # Locate the campaign root folder for mtime + deeper reads.
    camp_path = None
    for key in ("path", "campaign_index", "state_file", "tracker_path"):
        rel = camp.get(key)
        if rel:
            cand = os.path.join(client_dir, "campaigns", rel) if not rel.startswith("campaigns/") else os.path.join(client_dir, rel)
            camp_path = os.path.dirname(cand) if cand.endswith((".json", ".yaml", ".yml")) else cand
            break

    last_updated = None

    # Layer 1: campaign-index.json
    ci_rel = camp.get("campaign_index")
    if ci_rel:
        ci_path = os.path.join(client_dir, ci_rel) if ci_rel.startswith("campaigns/") else os.path.join(client_dir, "campaigns", ci_rel)
        ci = load_json(ci_path)
        if isinstance(ci, dict):
            phase = ci.get("current_stage") or ci.get("current_gate") or phase
            next_action = ci.get("next_action") or next_action
            last_updated = ci.get("last_updated") or last_updated
            if ci.get("operator_review_required"):
                blocker_texts.append("operator review required")
            camp_path = os.path.dirname(ci_path)

    # Layer 1b: state.yaml (takekine)
    sf_rel = camp.get("state_file")
    if sf_rel and not next_action:
        sf_path = os.path.join(client_dir, sf_rel) if sf_rel.startswith("campaigns/") else os.path.join(client_dir, "campaigns", sf_rel)
        yk = read_yaml_scalars(sf_path, {"current_stage", "current_gate", "phase", "last_action", "last_session", "next_skill"})
        phase = yk.get("current_stage") or yk.get("phase") or phase
        next_action = next_action or yk.get("next_skill") or yk.get("last_action") or ""
        # state.yaml's next_actions list — grab first item
        na = read_yaml_scalars(sf_path, {"next_actions"})
        if na.get("next_actions") and not next_action:
            next_action = na["next_actions"]

    # Layer 2: deepest active workspace pipeline-state.json
    ws_rel = None
    reg = camp.get("workspace_registry")
    if isinstance(reg, list) and reg:
        ws_rel = reg[0].get("pipeline_state")
    if ws_rel:
        ws_path = os.path.join(os.path.dirname(ci_path) if ci_rel else client_dir, ws_rel)
        ps = load_json(ws_path)
        if isinstance(ps, dict):
            ph, bl = pipeline_state_summary(ps)
            if ph:
                phase = ph
            blocker_texts.extend(bl)

    blocked = classify_block(phase, status, next_action, *blocker_texts)

    # Stale check: last_updated vs newest artifact mtime under the campaign folder.
    stale = None
    lu_date = parse_date(last_updated)
    if lu_date and camp_path and os.path.isdir(camp_path):
        nm = newest_mtime(camp_path)
        if nm:
            lu_epoch = time.mktime(lu_date.timetuple())
            lag_days = (nm - lu_epoch) / 86400.0
            if lag_days > STALE_DAYS:
                art_date = datetime.fromtimestamp(nm).date().isoformat()
                stale = f"index {last_updated} < artifact {art_date}"

    return {
        "slug": slug,
        "phase": phase or "unknown",
        "next": next_action or "(none recorded)",
        "blocked": blocked,
        "stale": stale,
        "status": status,
    }


def pick_active(campaigns: list[dict]) -> list[dict]:
    """Prefer active/in-flight campaigns; drop archived and template stubs."""
    out = []
    for c in campaigns:
        slug = (c.get("campaign_slug") or "")
        status = (c.get("status") or "").lower()
        if status in ("archived",) or slug.startswith("_") or "{{" in slug or slug == "_example-campaign":
            continue
        out.append(c)
    return out


def scan_client(client: str) -> list[dict]:
    """Return resolved campaign rows for a client (may be empty)."""
    client_dir = os.path.join(CLIENTS, client)
    idx_path = os.path.join(client_dir, "campaigns", "_campaigns-index.json")
    rows: list[dict] = []
    idx = load_json(idx_path)
    if isinstance(idx, dict) and isinstance(idx.get("campaigns"), list):
        tracker_rows: list[dict] = []
        for camp in pick_active(idx["campaigns"]):
            if camp.get("tracker_path"):
                tr = resolve_tracker(client_dir, camp)
                if tr:
                    tracker_rows.append(tr)
            else:
                rows.append(resolve_campaign(client_dir, camp))
        # Collapse DCT-tracker clients: newest DCT per funnel only (keeps output terse,
        # honors clients with parallel funnels like neezanizam's buyer-funnel vs asset-progression).
        if tracker_rows:
            by_funnel: dict[str, dict] = {}
            for tr in tracker_rows:
                f = tr.get("funnel") or tr["slug"]
                if f not in by_funnel or tr.get("mtime", 0) > by_funnel[f].get("mtime", 0):
                    by_funnel[f] = tr
            counts: dict[str, int] = {}
            for tr in tracker_rows:
                f = tr.get("funnel") or tr["slug"]
                counts[f] = counts.get(f, 0) + 1
            for f, tr in by_funnel.items():
                if counts[f] > 1:
                    tr["extra_count"] = counts[f] - 1
                rows.append(tr)
        return rows

    # No index — folder truth fallback: list campaign subfolders by newest mtime.
    camp_root = os.path.join(client_dir, "campaigns")
    subs = []
    if os.path.isdir(camp_root):
        for name in os.listdir(camp_root):
            full = os.path.join(camp_root, name)
            if os.path.isdir(full) and not is_skipped(name) and not name.startswith("_"):
                subs.append((name, newest_mtime(full)))
    if subs:
        subs.sort(key=lambda t: t[1], reverse=True)
        name, _ = subs[0]
        rows.append({
            "slug": name,
            "phase": "unindexed (no _campaigns-index.json)",
            "next": "register campaign in _campaigns-index.json",
            "blocked": "operator",
            "stale": None,
            "status": "",
            "extra_count": len(subs) - 1,
        })
    return rows


def format_line(client: str, row: dict) -> str:
    parts = [
        f"{client}: {row['slug']} @ {truncate(row['phase'], 48)}",
        f"next: {truncate(row['next'], 60)}",
        f"blocked on: {row['blocked']}",
    ]
    line = " — ".join(parts)
    if row.get("stale"):
        line += f"  [stale: {row['stale']}]"
    if row.get("extra_count"):
        line += f"  (+{row['extra_count']} more campaign folders)"
    return line


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    targets = [a for a in argv if not a.startswith("--")]

    all_clients = sorted(
        d for d in os.listdir(CLIENTS)
        if os.path.isdir(os.path.join(CLIENTS, d)) and not is_skipped(d)
    )
    if targets:
        all_clients = [c for c in all_clients if c in targets]

    results = []
    for client in all_clients:
        rows = scan_client(client)
        if rows:
            results.append((client, rows))
        else:
            results.append((client, [{"slug": "(no campaigns)", "phase": "idle", "next": "(none)", "blocked": "nothing", "stale": None, "status": ""}]))

    if as_json:
        out = {c: rows for c, rows in results}
        print(json.dumps(out, indent=2))
        return 0

    today = date.today().isoformat()
    lines = [f"STATUS BOARD — {today} (stale flag: index lags artifact by >{STALE_DAYS}d)"]
    for client, rows in results:
        for row in rows:
            lines.append(format_line(client, row))

    if len(lines) > MAX_LINES:
        kept = lines[: MAX_LINES - 1]
        kept.append(f"… {len(lines) - (MAX_LINES - 1)} more line(s) suppressed (pass a client name to narrow).")
        lines = kept

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
