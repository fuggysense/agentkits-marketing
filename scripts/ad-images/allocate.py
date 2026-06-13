#!/usr/bin/env python3
"""allocate — Build #10. Sole writer of dct.json image_pool + _assets.json.

Contract locked 2026-06-08 in docs/ad-image-tooling-overlap-260608.md:
  - allocate <dct-workspace> <render-file>: MOVE (not copy) a render into
    dcts/<DCT>/images/DCT<NNN>-img-<NN>.png, auto-assigning the next slot.
    Prefers the slot whose `source` matches the render's filename (the pool is
    pre-seeded with variant provenance); else first free pending slot.
  - CHECK-ALL-THEN-MOVE: pool not full, slot free, both JSON files writable.
    Any check fails -> abort, nothing changed. Roll the file back on a write
    failure after the move.
  - Pool full -> refuse, suggest sibling DCTs with room (same avatar first,
    then same offer), never discard the render.
  - --reconcile: sync statuses for renders that already landed directly in
    images/ (render.py current-shape writes there), register them in the
    ledger, and recompute the image_pool.rendered invariant.
  - Dry-run by DEFAULT. Pass --write to commit.

Usage:
    python3 scripts/ad-images/allocate.py <dct-workspace-or-dct.json> <render-file> [--write]
    python3 scripts/ad-images/allocate.py <dct-workspace-or-dct.json> --reconcile [--write]
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

SGT = timezone(timedelta(hours=8))


def fail(msg: str) -> None:
    sys.exit(f"allocate: {msg}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        fail(f"{path} is not valid JSON: {e}")


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def resolve_dct(arg: str) -> tuple[Path, dict]:
    p = Path(arg)
    dct_path = p if p.name == "dct.json" else p / "dct.json"
    if not dct_path.exists():
        fail(f"no dct.json at {dct_path}")
    data = load_json(dct_path)
    pool = data.get("image_pool")
    if not (isinstance(pool, dict) and isinstance(pool.get("images"), list)):
        fail(f"{dct_path} has no image_pool.images[] — not a current-shape dct.json")
    return dct_path, data


def find_ledger(workspace: Path) -> Path:
    """Walk up from the DCT workspace to the campaign dir holding _assets/_assets.json."""
    for parent in [workspace, *workspace.parents]:
        candidate = parent / "_assets" / "_assets.json"
        if candidate.exists():
            return candidate
        if parent.name == "campaigns" or parent.name == "clients":
            break
    fail(f"no _assets/_assets.json found above {workspace}")


def recompute_rendered(data: dict) -> None:
    images = data["image_pool"]["images"]
    data["image_pool"]["rendered"] = sum(1 for i in images if i.get("status") == "rendered")


def ledger_entry_for(ledger: dict, *, file_rel: str = None, image_id: str = None) -> dict | None:
    for e in ledger.get("images", []):
        if image_id and e.get("id") == image_id:
            return e
        if file_rel and e.get("file") == file_rel:
            return e
    return None


def consistency_check(dct_path: Path, data: dict, ledger_path: Path, ledger: dict) -> list[str]:
    """Cheap post-write insurance: every rendered slot's file exists; every slot id
    marked rendered has an allocated ledger entry pointing at the same file."""
    problems = []
    workspace = dct_path.parent
    campaign_dir = ledger_path.parent.parent
    for img in data["image_pool"]["images"]:
        if img.get("status") != "rendered":
            continue
        f = img.get("file")
        if not f or not (workspace / f).exists():
            problems.append(f"{img['id']}: status=rendered but file missing ({f})")
            continue
        entry = ledger_entry_for(ledger, image_id=img["id"])
        if entry is None:
            problems.append(f"{img['id']}: rendered in dct.json but absent from ledger")
        elif entry.get("status") not in ("allocated", "published"):
            problems.append(f"{img['id']}: ledger status {entry.get('status')!r}, expected allocated/published")
        else:
            ledger_file = campaign_dir / entry.get("file", "")
            if ledger_file.resolve() != (workspace / f).resolve():
                problems.append(f"{img['id']}: file path disagrees (dct={f}, ledger={entry.get('file')})")
    target = data["image_pool"].get("target", 10)
    if len([i for i in data["image_pool"]["images"]]) > 10:
        problems.append(f"pool has >10 images (target {target}) — exceeds Meta Flex cap")
    return problems


def suggest_siblings(dct_path: Path, data: dict) -> list[str]:
    """Sibling DCTs in the same campaign with a free slot. Same avatar first, then same offer."""
    dcts_dir = dct_path.parent.parent
    out = []
    for sibling in sorted(dcts_dir.iterdir()) if dcts_dir.is_dir() else []:
        sib_dct = sibling / "dct.json"
        if sibling == dct_path.parent or not sib_dct.exists():
            continue
        sd = load_json(sib_dct)
        pool = sd.get("image_pool", {})
        images = pool.get("images", [])
        free = sum(1 for i in images if i.get("status") == "pending")
        if free == 0 and len(images) >= 10:
            continue
        rank = 0 if sd.get("avatar") == data.get("avatar") else (1 if sd.get("offer") == data.get("offer") else 2)
        out.append((rank, f"{sd.get('dct_id', sibling.name)} ({sd.get('avatar', '?')}, {len(images) - free}/10) at {sibling}"))
    return [s for _, s in sorted(out)]


def do_allocate(dct_path: Path, data: dict, render: Path, write: bool) -> None:
    workspace = dct_path.parent
    ledger_path = find_ledger(workspace)
    ledger = load_json(ledger_path)
    campaign_dir = ledger_path.parent.parent
    images = data["image_pool"]["images"]

    if not render.exists():
        fail(f"render file not found: {render}")

    # pool full? (rule 4: refuse -> reroute -> never discard)
    free_slots = [i for i in images if i.get("status") == "pending"]
    if not free_slots:
        sibs = suggest_siblings(dct_path, data)
        msg = f"{data.get('dct_id')} pool is full ({len(images)}/10)."
        if sibs:
            msg += " Siblings with room:\n  " + "\n  ".join(sibs)
        else:
            msg += f" No sibling DCT has room — render stays where it is ({render})."
        fail(msg)

    # slot pick: source-match first (pool slots are pre-seeded with variant provenance), else first pending
    slot = next((i for i in free_slots if i.get("source") == render.name), free_slots[0])
    target = workspace / "images" / f"{slot['id']}.png"
    if target.exists():
        fail(f"target {target} already exists but slot {slot['id']} is pending — drift; run --reconcile first")

    # ledger entry for this render (match by relative path or stem)
    try:
        render_rel = str(render.resolve().relative_to(campaign_dir.resolve()))
    except ValueError:
        render_rel = None
    lentry = ledger_entry_for(ledger, file_rel=render_rel) or ledger_entry_for(ledger, image_id=render.stem)

    plan = [
        f"DCT:        {data.get('dct_id')} ({dct_path})",
        f"render:     {render}",
        f"slot:       {slot['id']}  (matched by {'source' if slot.get('source') == render.name else 'next-free'})",
        f"move to:    {target}",
        f"dct.json:   {slot['id']}.file = images/{slot['id']}.png, status pending->rendered, source = {render.name}",
        f"ledger:     {ledger_path}",
        f"            entry {'UPDATE ' + lentry['id'] if lentry else 'CREATE ' + slot['id']} -> status allocated, allocated_to [{data.get('dct_id')}]",
    ]
    print("\n".join(plan))
    if not write:
        print("\nDRY-RUN — nothing moved. Re-run with --write to commit.")
        return

    # CHECK-ALL-THEN-MOVE
    for f in (dct_path, ledger_path):
        if not f.exists():
            fail(f"{f} missing — aborting, nothing changed")
    target.parent.mkdir(parents=True, exist_ok=True)

    shutil.move(str(render), str(target))
    try:
        slot["file"] = f"images/{slot['id']}.png"
        slot["status"] = "rendered"
        slot["source"] = render.name
        recompute_rendered(data)
        save_json(dct_path, data)

        target_rel = str(target.resolve().relative_to(campaign_dir.resolve()))
        if lentry is None:
            lentry = {"id": slot["id"], "kind": "image", "rendered_at": None, "prompt_source": None, "notes": ""}
            ledger.setdefault("images", []).append(lentry)
        lentry["id"] = slot["id"]
        lentry["file"] = target_rel
        lentry["status"] = "allocated"
        lentry["allocated_to"] = [data.get("dct_id")]
        lentry["rendered_at"] = lentry.get("rendered_at") or datetime.now(SGT).strftime("%y%m%d")
        ledger["count"] = len(ledger.get("images", []))
        by_status = {}
        for e in ledger["images"]:
            by_status[e.get("status", "?")] = by_status.get(e.get("status", "?"), 0) + 1
        ledger["by_status"] = by_status
        ledger["updated"] = datetime.now(SGT).strftime("%y%m%d")
        save_json(ledger_path, ledger)
    except Exception as e:
        shutil.move(str(target), str(render))  # roll back the move
        fail(f"write failed after move — file rolled back to {render}. Error: {e}")

    problems = consistency_check(dct_path, data, ledger_path, ledger)
    if problems:
        print("⚠️  post-write consistency check found drift (allocation committed, fix these):")
        print("  " + "\n  ".join(problems))
    else:
        print(f"✅ allocated {slot['id']} — dct.json + ledger in lockstep.")


def do_reconcile(dct_path: Path, data: dict, write: bool) -> None:
    """Sync state for renders that landed directly in images/ (render.py writes there),
    register them in the ledger, recompute the rendered invariant."""
    workspace = dct_path.parent
    ledger_path = find_ledger(workspace)
    ledger = load_json(ledger_path)
    campaign_dir = ledger_path.parent.parent
    changes = []

    for slot in data["image_pool"]["images"]:
        expected = workspace / "images" / f"{slot['id']}.png"
        on_disk = expected.exists()
        if on_disk and slot.get("status") != "rendered":
            changes.append(f"dct.json: {slot['id']} status {slot.get('status')!r} -> rendered (file on disk)")
            slot["status"] = "rendered"
            slot["file"] = f"images/{slot['id']}.png"
        if not on_disk and slot.get("status") == "rendered":
            changes.append(f"dct.json: {slot['id']} status rendered -> pending (file MISSING on disk)")
            slot["status"] = "pending"
            slot["file"] = None
        if on_disk:
            entry = ledger_entry_for(ledger, image_id=slot["id"])
            rel = str(expected.resolve().relative_to(campaign_dir.resolve()))
            if entry is None:
                changes.append(f"ledger: CREATE {slot['id']} (allocated -> {data.get('dct_id')})")
                ledger.setdefault("images", []).append({
                    "id": slot["id"], "file": rel, "kind": "image", "status": "allocated",
                    "allocated_to": [data.get("dct_id")], "rendered_at": None,
                    "prompt_source": None, "notes": "registered by allocate --reconcile",
                })
            elif entry.get("file") != rel or entry.get("status") not in ("allocated", "published"):
                changes.append(f"ledger: UPDATE {slot['id']} file/status -> {rel}, allocated")
                entry["file"] = rel
                if entry.get("status") != "published":
                    entry["status"] = "allocated"
                entry["allocated_to"] = [data.get("dct_id")]

    old_rendered = data["image_pool"].get("rendered")
    recompute_rendered(data)
    if data["image_pool"]["rendered"] != old_rendered:
        changes.append(f"dct.json: image_pool.rendered {old_rendered} -> {data['image_pool']['rendered']}")

    if not changes:
        print("nothing to reconcile — dct.json, ledger, and disk agree.")
        return
    print("reconcile plan:\n  " + "\n  ".join(changes))
    if not write:
        print("\nDRY-RUN — nothing written. Re-run with --write to commit.")
        return

    ledger["count"] = len(ledger.get("images", []))
    by_status = {}
    for e in ledger["images"]:
        by_status[e.get("status", "?")] = by_status.get(e.get("status", "?"), 0) + 1
    ledger["by_status"] = by_status
    ledger["updated"] = datetime.now(SGT).strftime("%y%m%d")
    save_json(dct_path, data)
    save_json(ledger_path, ledger)

    problems = consistency_check(dct_path, data, ledger_path, ledger)
    if problems:
        print("⚠️  residual drift after reconcile:")
        print("  " + "\n  ".join(problems))
    else:
        print("✅ reconciled — dct.json + ledger in lockstep.")


def main() -> None:
    ap = argparse.ArgumentParser(prog="allocate", description=__doc__.splitlines()[0])
    ap.add_argument("dct", help="DCT workspace dir or path to its dct.json")
    ap.add_argument("render", nargs="?", help="render file to allocate (omit with --reconcile)")
    ap.add_argument("--reconcile", action="store_true", help="sync statuses for renders already in images/")
    ap.add_argument("--write", action="store_true", help="commit (default is dry-run)")
    args = ap.parse_args()

    dct_path, data = resolve_dct(args.dct)
    if args.reconcile:
        if args.render:
            fail("--reconcile takes no render file")
        do_reconcile(dct_path, data, args.write)
    else:
        if not args.render:
            fail("need a render file (or --reconcile)")
        do_allocate(dct_path, data, Path(args.render), args.write)


if __name__ == "__main__":
    main()
