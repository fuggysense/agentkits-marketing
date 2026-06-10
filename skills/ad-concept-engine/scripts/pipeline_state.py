#!/usr/bin/env python3
"""DCT pipeline state — the resume save-file for the ad-concept-engine conductor.

One pipeline-state.json per DCT (lives in the DCT workspace folder). It records which
phase the production is in, which gates are approved, and what to do next — so production
can be PAUSED at any point and ANY later session (even a fresh one, even a new client)
reads this file and knows exactly where to continue. Mirrors the vid-director
pipeline-state.json convention + campaign-runner's state_manager.py.

Usage:
  pipeline_state.py init   <state.json> --dct DCT010 --client neezanizam \
                           --campaign buyer-funnel --metrics-campaign buyer-funnel \
                           --method 10-5-5 --workspace clients/.../dct-10-5-5-proof-260603
  pipeline_state.py resume <state.json>          # the "you are here" card (READ THIS ON ENTRY)
  pipeline_state.py next   <state.json>          # just the next action, one line
  pipeline_state.py advance <state.json> --phase phase_3_render --status complete \
                           [--gate-status approved] [--output "10/10 rendered"] \
                           [--next "run allocate"] [--blocker "..."] [--clear-blockers]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE = SCRIPT_DIR.parent / "templates" / "dct-pipeline-state.template.json"

STATUS_GLYPH = {
    "complete": "✓", "in_progress": "◐", "not_started": "○",
}
VALID_STATUS = {"not_started", "in_progress", "complete", "skipped"} | {
    f"blocked_until_{x}" for x in
    ("phase_0", "gate_1", "gate_2", "phase_3", "phase_3b", "gate_3", "phase_4")
}


def today():
    return datetime.now().strftime("%Y-%m-%d")


def load(path):
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"no pipeline-state at {p} — run `init` first.")
    return json.loads(p.read_text())


def atomic_write(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    os.replace(tmp, p)


def compute_next(state):
    """First non-complete phase drives the default next action."""
    for name, ph in state["phases"].items():
        if ph.get("status") in ("complete", "skipped"):
            continue
        verb = "finish" if ph.get("status") == "in_progress" else "start"
        return f"{verb} {name} ({ph.get('title','')}) — owner: {ph.get('owner','')}"
    return "all phases complete — DCT ready (ads uploaded PAUSED for founder review)."


def cmd_init(args):
    tpl = json.loads(TEMPLATE.read_text())
    repl = {
        "{{dct_id}}": args.dct, "{{client}}": args.client, "{{campaign}}": args.campaign,
        "{{metrics_campaign}}": args.metrics_campaign or args.campaign,
        "{{dct_method}}": args.method, "{{workspace}}": args.workspace or "",
        "{{date}}": today(),
    }
    raw = json.dumps(tpl)
    for k, v in repl.items():
        raw = raw.replace(k, v)
    state = json.loads(raw)
    atomic_write(args.state, state)
    print(f"initialised pipeline-state -> {args.state}")
    print_card(state)


def cmd_advance(args):
    state = load(args.state)
    phases = state["phases"]
    if args.phase not in phases:
        raise SystemExit(f"unknown phase '{args.phase}'. Valid: {', '.join(phases)}")
    if args.status and args.status not in VALID_STATUS:
        raise SystemExit(f"invalid status '{args.status}'. Valid: {sorted(VALID_STATUS)}")
    ph = phases[args.phase]
    if args.status:
        ph["status"] = args.status
        if args.status == "complete":
            ph["completed_at"] = today()
    if args.gate_status:
        if "gate" not in ph:
            raise SystemExit(f"phase '{args.phase}' has no gate to set.")
        ph["gate_status"] = args.gate_status
    if args.output:
        ph.setdefault("outputs", []).append(args.output)
    if args.blocker:
        state.setdefault("blockers", []).append(args.blocker)
    if args.clear_blockers:
        state["blockers"] = []

    # current_phase = first non-complete phase
    state["current_phase"] = next(
        (n for n, p in phases.items() if p.get("status") not in ("complete", "skipped")),
        list(phases)[-1],
    )
    state["phase_status"] = phases[state["current_phase"]].get("status", "not_started")
    state["next_action"] = args.next or compute_next(state)
    state["last_updated"] = today()
    atomic_write(args.state, state)
    print(f"advanced {args.phase} -> {ph.get('status')}")
    print_card(state)


def print_card(state):
    bar = "━" * 56
    print(f"\n{bar}")
    print(f" {state['dct_id']} · {state.get('campaign','')} · {state.get('dct_method','')}")
    print(f" workspace: {state.get('workspace','')}")
    print(bar)
    cur = state.get("current_phase", "?")
    print(f" YOU ARE HERE: {cur} ({state.get('phase_status','?')})")
    print(f" NEXT: {state.get('next_action','?')}")
    print(bar)
    for name, ph in state["phases"].items():
        g = STATUS_GLYPH.get(ph.get("status"), "·")
        line = f"  {g} {name} — {ph.get('title','')}"
        st = ph.get("status", "")
        if st not in ("complete",):
            line += f"  [{st}]"
        gate = ph.get("gate")
        if gate:
            line += f"  ({gate}: {ph.get('gate_status','?')})"
        print(line)
        for o in ph.get("outputs", []):
            print(f"        └ {o}")
    if state.get("blockers"):
        print(bar)
        print(" BLOCKERS:")
        for b in state["blockers"]:
            print(f"  ! {b}")
    if state.get("pending_approvals"):
        print(" PENDING APPROVALS:", ", ".join(state["pending_approvals"]))
    print(bar + "\n")


def cmd_resume(args):
    print_card(load(args.state))


def cmd_next(args):
    print(load(args.state).get("next_action", "?"))


def main():
    ap = argparse.ArgumentParser(description="DCT pipeline resume state")
    sub = ap.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("init"); i.add_argument("state")
    i.add_argument("--dct", required=True); i.add_argument("--client", required=True)
    i.add_argument("--campaign", required=True); i.add_argument("--metrics-campaign")
    i.add_argument("--method", default="10-5-5"); i.add_argument("--workspace")
    i.set_defaults(func=cmd_init)

    r = sub.add_parser("resume"); r.add_argument("state"); r.set_defaults(func=cmd_resume)
    sub.add_parser("show", parents=[], add_help=True).add_argument("state")  # alias
    n = sub.add_parser("next"); n.add_argument("state"); n.set_defaults(func=cmd_next)

    a = sub.add_parser("advance"); a.add_argument("state")
    a.add_argument("--phase", required=True); a.add_argument("--status")
    a.add_argument("--gate-status"); a.add_argument("--output")
    a.add_argument("--next"); a.add_argument("--blocker")
    a.add_argument("--clear-blockers", action="store_true")
    a.set_defaults(func=cmd_advance)

    args = ap.parse_args()
    if getattr(args, "cmd", None) == "show":
        return cmd_resume(args)
    args.func(args)


if __name__ == "__main__":
    main()
