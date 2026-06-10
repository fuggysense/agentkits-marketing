#!/usr/bin/env python3
"""Convert a legacy monolithic dct-tracker.json into the canonical per-DCT dct.json.

Deferred #8, proof scope (2026-06-08): this handles the 10-5-5 tracker shape only.
The legacy 3-2-2 shape (different cardinality, revision/provenance blocks) needs a
separate normalizer and is intentionally NOT supported here — the script fails loudly
on anything that isn't method "10-5-5" rather than guessing.

Design rules:
  - Lossless, enforced. Every source key must be accounted for (mapped into dct.json,
    relocated to a named campaign-level home, or dropped with a reason). A closing
    set-difference audit aborts the run if any source key is unaccounted — losslessness
    is structurally guaranteed, not left to the author's memory.
  - Merge, don't clobber. If a dct.json already exists, render state (which image slots are
    already rendered, their file paths) is carried forward by matching on `source`. An
    existing rendered image that finds no match in the new pool raises a loud warning
    instead of silently reverting to pending.
  - Fail-closed by default. Dry-run unless --write. Refuses to overwrite a live dct.json
    in dry-run even if --out points at it. Aborts on unknown keys unless --allow-unaccounted.
  - Image prompts live on the image slot (operator decision 2026-06-08):
    image_pool.images[].image_prompt holds the source prompt; `source` records which
    angle/variant it came from, so the pool stays flat (not angle-tied) while keeping lineage.

Usage:
  python3 scripts/migrate_tracker_to_dct.py --tracker <path>                 # dry-run, summary only
  python3 scripts/migrate_tracker_to_dct.py --tracker <t> --out <stage.json> # dry-run, stage a candidate to diff
  python3 scripts/migrate_tracker_to_dct.py --tracker <t> --write            # commit to the sibling dct.json
"""

import argparse
import json
from pathlib import Path

# Every source key must appear in one of these sets, or the closing audit aborts the run.
HANDLED_TOPLEVEL = {
    "_owner_skill", "_method", "client_slug", "metrics_campaign", "wave", "dct_number",
    "meta_ad_account_id", "meta_campaign_name", "meta_adset_name", "dct_structure",
    "creatives", "sheet_write_plan", "kpi_targets", "kill_rules", "known_blockers", "next_commands",
}
HANDLED_CREATIVE = {
    "batch", "format", "ad_name", "market_awareness", "market_sophistication", "angle",
    "angle_rationale", "persona", "status", "copy_1", "copy_2", "headline_1", "headline_2",
    "headline_drafts", "canva_link", "why_am_i_testing_this", "variations",
}
HANDLED_VARIATION = {"variant_id", "visual_style", "image_prompt", "canva_link"}

# Boilerplate explainer strings — regenerated per DCT, not migrated 1:1 from the tracker.
FORMAT_EXPLAINER = (
    "Meta Flexible Ad (10-5-5): up to 10 images + 5 primary texts + 5 headlines. "
    "Meta MIXES them — any image x any text x any headline. Images are a pool WITHIN "
    "this DCT, not tied to a specific text/headline/angle; one image = one DCT by default."
)
CONSTANT_EXPLAINER = "avatar + offer/destination (one ad set)"
TRACKING_EXPLAINER = (
    "ad set = blended CPL. Meta asset breakdown gives per-image, per-headline, per-text CTR "
    "SEPARATELY (directional, no conversions, no per-combination data). Promote a winner to "
    "its own ad set to scale + track cleanly."
)

# Tracker keys that are campaign-/wave-level, not per-DCT. They must NOT enter dct.json;
# the report records where each one belongs so a later phase can relocate them.
RELOCATION_MAP = {
    "meta_ad_account_id": "_brand/metrics-config.json (campaign ad_platforms.meta.ad_account_id)",
    "meta_campaign_name": "campaign CONTEXT.md frontmatter (meta_campaign_id) / metrics-config.json",
    "sheet_write_plan": "_brand/metrics-config.json (sheet_id + tab gids already live there)",
    "kpi_targets": "campaign-level _targets.json or CONTEXT.md (wave-level KPI, not per-DCT)",
    "kill_rules": "campaign-level _targets.json or CONTEXT.md (wave-level, not per-DCT)",
    "_owner_skill": "provenance only — kept in dct.json _provenance",
    "wave": "campaign CONTEXT.md / dcts index (per-wave grouping) — kept in _provenance",
}


def load_json(path):
    return json.loads(Path(path).read_text())


def pad_dct_id(dct_number):
    try:
        n = int(dct_number)
    except (TypeError, ValueError):
        raise SystemExit(f"dct_number must be numeric, got {dct_number!r}")
    return f"DCT{n:03d}"


def _assert_10_5_5_shape(tracker, structure):
    """Fail loud on anything that isn't genuinely a 10-5-5 tracker — label AND shape."""
    method = structure.get("method")
    if method != "10-5-5":
        raise SystemExit(
            f"This converter handles method '10-5-5' only; dct_structure.method is '{method}'. "
            "The legacy 3-2-2 normalizer is a separate, deferred job."
        )
    top_method = tracker.get("_method")
    if top_method is not None and top_method != method:
        raise SystemExit(
            f"tracker disagrees with itself: _method='{top_method}' vs "
            f"dct_structure.method='{method}'. Resolve before migrating."
        )
    # Cardinality: a mislabelled 3-2-2 (2 copies/headlines per angle) must not slip through.
    cpa = structure.get("copies_per_angle")
    hpa = structure.get("headlines_per_angle")
    if cpa not in (None, 1) or hpa not in (None, 1):
        raise SystemExit(
            f"declared copies_per_angle={cpa}, headlines_per_angle={hpa} — not the 10-5-5 "
            "one-copy/one-headline-per-angle shape this converter handles."
        )
    declared_angles = structure.get("angles")
    creatives = tracker.get("creatives", [])
    if declared_angles is not None and len(creatives) != declared_angles:
        raise SystemExit(
            f"declared {declared_angles} angles but creatives[] has {len(creatives)}. "
            "Structural mismatch — fix the tracker before migrating."
        )


def normalize_10_5_5(tracker, existing_dct):
    """Return (dct_dict, report_dict). Pure transform; no I/O."""
    report = {"emitted": [], "relocated": [], "dropped": [], "warnings": [], "unaccounted": []}

    structure = tracker.get("dct_structure", {})
    _assert_10_5_5_shape(tracker, structure)
    method = structure["method"]

    creatives = tracker.get("creatives", [])
    if not creatives:
        raise SystemExit("tracker has no creatives[] — nothing to convert")

    dct_id = pad_dct_id(tracker["dct_number"])

    # Avatar: one DCT = one avatar. Take the first, warn if creatives disagree or it's empty.
    personas = {c.get("persona") for c in creatives if c.get("persona")}
    avatar = creatives[0].get("persona", "")
    if not avatar:
        report["warnings"].append("creatives[0] has no persona — avatar is empty; set it before use.")
    if len(personas) > 1:
        report["warnings"].append(
            f"creatives disagree on persona ({sorted(personas)}) — took '{avatar}'. "
            "A DCT should be one avatar; check the source."
        )

    # Carry campaign_type + offer from an existing dct.json when present; else sane defaults.
    campaign_type = (existing_dct or {}).get("campaign_type", "dct")
    offer = (existing_dct or {}).get("offer", tracker.get("metrics_campaign", ""))
    if not (existing_dct or {}).get("offer"):
        report["warnings"].append(
            f"offer not in tracker — defaulted to metrics_campaign '{offer}'. Confirm."
        )

    # DCT-level status: derive from creatives (all DRAFT -> draft) unless existing says otherwise.
    creative_statuses = {(c.get("status") or "").lower() for c in creatives}
    status = (existing_dct or {}).get("status") or (
        "draft" if creative_statuses <= {"draft", ""} else "mixed"
    )

    # --- angles[] : one angle per creative, carrying ALL per-angle metadata (lossless) ---
    angles = []
    for c in creatives:
        batch = c["batch"]  # e.g. DCT010-A01
        angle_id = batch.split("-")[-1]  # A01
        angles.append({
            "id": angle_id,
            "name": c.get("angle", ""),
            "headline": c.get("headline_1", ""),
            "primary_text": c.get("copy_1", ""),
            "format": c.get("format", "Static"),
            "ad_name": c.get("ad_name", ""),
            "market_awareness": c.get("market_awareness", ""),
            "market_sophistication": c.get("market_sophistication", ""),
            "angle_rationale": c.get("angle_rationale", ""),
            "why_am_i_testing_this": c.get("why_am_i_testing_this", ""),
            "headline_drafts": c.get("headline_drafts", []),
            "status": c.get("status", "DRAFT"),
        })
        # In 10-5-5 there is exactly 1 copy + 1 headline per angle; copy_2/headline_2 are empty.
        for empty_key in ("copy_2", "headline_2"):
            if (c.get(empty_key) or "").strip():
                report["warnings"].append(
                    f"{batch}.{empty_key} was non-empty in a 10-5-5 tracker — not migrated."
                )
                report["dropped"].append(
                    {"key": f"creatives[{batch}].{empty_key}", "value": c.get(empty_key),
                     "reason": "10-5-5 single-copy/headline-per-angle; review if unexpected"}
                )
    report["emitted"].append(f"angles[] x{len(angles)} (with per-angle metadata + headline_drafts)")

    # --- image_pool : flat pool, prompts on the slot, render state merged from existing ---
    existing_imgs = ((existing_dct or {}).get("image_pool", {}) or {}).get("images", [])
    existing_by_source = {img.get("source"): img for img in existing_imgs if img.get("source")}

    images = []
    slot = 1
    for c in creatives:
        batch = c["batch"]
        for var_index, var in enumerate(c.get("variations", []), start=1):
            vid = var.get("variant_id") or f"v{var_index}"
            if not var.get("variant_id"):
                report["warnings"].append(
                    f"{batch} variation #{var_index} missing variant_id — fabricated '{vid}'; "
                    "source naming may not match a future re-render."
                )
            source = f"{batch}-{vid}.png"  # provenance: which angle/variant this prompt is
            prior = existing_by_source.get(source, {})
            rendered = (prior.get("status") == "rendered") and bool(prior.get("file"))
            images.append({
                "id": f"{dct_id}-img-{slot:02d}",
                "file": prior.get("file") if rendered else None,
                "status": "rendered" if rendered else "pending",
                "source": source,
                "visual_style": var.get("visual_style", ""),
                "image_prompt": var.get("image_prompt", ""),
            })
            slot += 1

    # Orphan check: an existing rendered image that finds no home in the new pool is state loss.
    matched_sources = {img["source"] for img in images}
    for src, prior in existing_by_source.items():
        if prior.get("status") == "rendered" and src not in matched_sources:
            report["warnings"].append(
                f"existing rendered image source '{src}' has NO match in the new pool — "
                "render state would be lost; investigate before --write."
            )

    rendered_count = sum(1 for i in images if i["status"] == "rendered")
    image_pool = {
        "target": structure.get("total_creatives", len(images)),
        "rendered": rendered_count,
        "id_format": f"{dct_id}-img-<NN>",
        "images": images,
    }
    report["emitted"].append(
        f"image_pool.images[] x{len(images)} (image_prompt on each slot; "
        f"{rendered_count} render state merged from existing dct.json)"
    )

    # canva_link is inspected at BOTH the angle and variation level (neither has a home yet).
    angle_canva = any((c.get("canva_link") or "").strip() for c in creatives)
    var_canva = any((v.get("canva_link") or "").strip()
                    for c in creatives for v in c.get("variations", []))
    if angle_canva or var_canva:
        report["dropped"].append(
            {"key": "canva_link (angle and/or variation)", "value": "(some non-empty)",
             "reason": "canva home is a Phase-3 sheet-writer decision; non-empty values NOT migrated"}
        )
        report["warnings"].append(
            "non-empty canva_link found in source but not migrated (canva home is Phase-3) — review."
        )
    else:
        report["dropped"].append(
            {"key": "canva_link (angle + variation)", "value": "(all empty)",
             "reason": "canva home is a Phase-3 sheet-writer decision; empty in source, not migrated"}
        )

    # --- top-level assembly (clean schema) ---
    dct = {
        "dct_id": dct_id,
        "campaign": tracker.get("metrics_campaign", ""),
        "campaign_type": campaign_type,
        "metrics_campaign": tracker.get("metrics_campaign", ""),
        "avatar": avatar,
        "offer": offer,
        "meta_adset": tracker.get("meta_adset_name", ""),
        "status": status,
        "dct_method": method,
        "format": FORMAT_EXPLAINER,
        "constant": CONSTANT_EXPLAINER,
        "angles": angles,
        "image_pool": image_pool,
        "tracking": TRACKING_EXPLAINER,
        "_provenance": {
            "migrated_from": "dct-tracker.json",
            "owner_skill": tracker.get("_owner_skill", ""),
            "wave": tracker.get("wave"),
            "dct_number": tracker.get("dct_number"),
            "method": method,
        },
    }

    # --- record relocations + intentional drops for the audit ---
    for key, home in RELOCATION_MAP.items():
        if key in tracker:
            if key in ("_owner_skill", "wave"):
                report["relocated"].append({"key": key, "home": home, "value_kept_in": "dct._provenance"})
            else:
                report["relocated"].append({"key": key, "home": home, "value": tracker.get(key)})
    for key in ("known_blockers", "next_commands"):
        if key in tracker:
            report["dropped"].append(
                {"key": key, "value": tracker.get(key), "reason": "ephemeral working notes — drop"}
            )
    if "_method" in tracker:
        report["dropped"].append(
            {"key": "_method", "value": tracker.get("_method"),
             "reason": "duplicate of dct_structure.method -> dct.dct_method"}
        )
    if "dct_structure" in tracker:
        report["dropped"].append(
            {"key": "dct_structure", "value": structure,
             "reason": "method -> dct.dct_method; remaining fields are derivable counts"}
        )
    if "client_slug" in tracker:
        report["dropped"].append(
            {"key": "client_slug", "value": tracker.get("client_slug"),
             "reason": "client identity is the folder path, not a per-DCT field"}
        )

    # --- closing losslessness audit: every source key must be accounted for ---
    for k in tracker:
        if k not in HANDLED_TOPLEVEL:
            report["unaccounted"].append({"level": "tracker", "key": k})
    for c in creatives:
        for k in c:
            if k not in HANDLED_CREATIVE:
                report["unaccounted"].append({"level": "creative", "batch": c.get("batch"), "key": k})
        for var in c.get("variations", []):
            for k in var:
                if k not in HANDLED_VARIATION:
                    report["unaccounted"].append(
                        {"level": "variation", "batch": c.get("batch"), "key": k}
                    )

    return dct, report


def main():
    ap = argparse.ArgumentParser(description="Convert legacy dct-tracker.json -> canonical dct.json (10-5-5 only)")
    ap.add_argument("--tracker", required=True, help="path to the source dct-tracker.json")
    ap.add_argument("--out", help="candidate dct.json output path (default: sibling dct.json)")
    ap.add_argument("--existing", help="existing dct.json to merge render state from (default: sibling dct.json)")
    ap.add_argument("--report", help="migration report JSON output path (default: <out>.migration-report.json)")
    ap.add_argument("--write", action="store_true", help="commit to the live dct.json (default: dry-run)")
    ap.add_argument("--allow-unaccounted", action="store_true",
                    help="proceed even if the source has keys this converter doesn't recognize (records them)")
    args = ap.parse_args()

    tracker_path = Path(args.tracker)
    if not tracker_path.exists():
        raise SystemExit(f"tracker not found: {tracker_path}")
    tracker = load_json(tracker_path)

    sibling_dct = tracker_path.parent / "dct.json"
    existing_path = Path(args.existing) if args.existing else sibling_dct
    existing_dct = load_json(existing_path) if existing_path.exists() else None

    out_path = Path(args.out) if args.out else sibling_dct
    report_path = Path(args.report) if args.report else out_path.with_suffix(".migration-report.json")

    # Fail-closed: never overwrite a live dct.json during a dry-run, even if --out points at it.
    if not args.write and out_path.resolve() == sibling_dct.resolve():
        raise SystemExit(
            f"refusing to write the live dct.json in dry-run: {out_path}\n"
            "Pass --write to commit, or --out a staging path to inspect a candidate first."
        )

    dct, report = normalize_10_5_5(tracker, existing_dct)
    report["source_tracker"] = str(tracker_path)
    report["existing_dct"] = str(existing_path) if existing_dct else None
    report["target_dct"] = str(out_path)

    # Losslessness gate.
    if report["unaccounted"] and not args.allow_unaccounted:
        keys = ", ".join(f"{u['level']}:{u['key']}" for u in report["unaccounted"])
        raise SystemExit(
            f"ABORT — {len(report['unaccounted'])} source key(s) this converter does not recognize: {keys}\n"
            "Losslessness cannot be guaranteed. Teach the converter where they go, or re-run with "
            "--allow-unaccounted to record them as unhandled and proceed."
        )

    summary = (
        f"DCT {dct['dct_id']}  ({dct['dct_method']})\n"
        f"  angles: {len(dct['angles'])}   images: {len(dct['image_pool']['images'])} "
        f"(rendered {dct['image_pool']['rendered']})\n"
        f"  emitted: {len(report['emitted'])}  relocated: {len(report['relocated'])}  "
        f"dropped: {len(report['dropped'])}  warnings: {len(report['warnings'])}  "
        f"unaccounted: {len(report['unaccounted'])}"
    )

    will_write = args.write or bool(args.out)
    if will_write:
        out_path.write_text(json.dumps(dct, indent=2, ensure_ascii=False) + "\n")
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        tag = "WROTE" if args.write else "[dry-run] staged"
        print(f"{tag} {out_path}\n{tag} {report_path}\n\n{summary}")
        if not args.write:
            print("\nRun with --write to commit to the live dct.json.")
    else:
        print(f"[dry-run] no --out given; nothing written.\n\n{summary}\n\nRun with --write to commit.")
    if report["warnings"]:
        print("\nWARNINGS:")
        for w in report["warnings"]:
            print(f"  - {w}")


if __name__ == "__main__":
    main()
