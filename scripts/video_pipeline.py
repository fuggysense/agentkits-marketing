#!/usr/bin/env python3
"""Minimal local video-pipeline command runner for zero-credit schema tests."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CLIENTS_DIR = REPO_ROOT / "clients"
SKILL_ROOT = Path.home() / ".claude" / "skills"
STYLE_ROOT = SKILL_ROOT / "video-factory" / "references" / "style-profiles"
SCHEMA_VERSION = "1.0"
PHASES = ["concept", "stills", "beat-sheet", "motion", "render", "final"]

GATE_PATHS = {
    "stills": Path("01-stills/_gate.json"),
    "beat-sheet": Path("02-beat-sheet/_gate.json"),
    "motion": Path("04-motion/_gate.json"),
    "render": Path("05-runs/_gate.json"),
}

EXPECTED_ARTIFACTS = {
    "stills": [
        "01-stills/01-character-base.md",
        "01-stills/01-character-base.png",
        "01-stills/03-scene-plate-1.md",
        "01-stills/03-scene-plate-1.png",
    ],
    "beat-sheet": [
        "02-beat-sheet/v1/prompt.md",
        "02-beat-sheet/v1/composite.png",
        "02-beat-sheet/v1/frames.json",
    ],
    "motion": [
        "04-motion/shot-01.md",
        "04-motion/shot-01.json",
        "04-motion/_shotlist.md",
    ],
    "render": [
        "05-runs/render-01/outputs/final.mp4",
        "05-runs/render-01/manifest.json",
        "05-runs/render-01/verdict.md",
    ],
}

CONCEPT_SOURCES = [
    ("context-profile.json", "business identity"),
    ("brand-voice.md", "how the brand talks"),
    ("icp.md", "buyer profile"),
    ("offer.md", "what is sold"),
    ("awareness-stage.md", "where buyer is in the funnel"),
    ("learnings.md", "recent corrections and highest-priority tone notes"),
]

REQUIRED_STYLE_FIELDS = [
    "recommended_motion_engine",
    "recommended_engine_adapter",
]
REQUIRED_PROMPT_BLOCK_HEADINGS = [
    "## Universal Positive",
    "## Universal Negative",
    "## Universal Closing",
]


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def today_suffix() -> str:
    return datetime.now().astimezone().strftime("%y%m%d")


def slug_ok(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9][a-z0-9-]*[a-z0-9]", value))


def campaign_slug_ok(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9][a-z0-9_-]*[a-z0-9]", value))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def path_label(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def extract_frontmatter(path: Path) -> str:
    text = path.read_text()
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise SystemExit(f"missing frontmatter: {path}")
    return match.group(1)


def frontmatter_field(fm: str, key: str) -> str | None:
    lines = fm.splitlines()
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if not stripped.startswith(f"{key}:"):
            continue
        value = stripped.split(":", 1)[1].strip()
        if value and value not in {">-", "|", ">"}:
            return value.strip('"').strip("'")
        collected: list[str] = []
        for next_line in lines[i + 1 :]:
            if next_line and not next_line.startswith((" ", "-")):
                break
            if next_line.strip():
                collected.append(next_line.strip())
        return " ".join(collected).strip()
    return None


def frontmatter_has_block(fm: str, key: str) -> bool:
    return bool(re.search(rf"^{re.escape(key)}:\n(?:  .+\n?)+", fm, re.M))


def validate_style_profile(style: str) -> dict[str, str]:
    profile = STYLE_ROOT / style / "SKILL.md"
    if not profile.exists():
        raise SystemExit(f"style profile not found: {profile}")
    fm = extract_frontmatter(profile)
    values: dict[str, str] = {}
    missing: list[str] = []
    for field in REQUIRED_STYLE_FIELDS:
        value = frontmatter_field(fm, field)
        if not value:
            missing.append(field)
        else:
            values[field] = value
    if missing:
        raise SystemExit(
            "style profile missing required field(s): " + ", ".join(missing)
        )
    prompt_blocks = profile.parent / "prompt-blocks.md"
    if prompt_blocks.exists():
        prompt_text = prompt_blocks.read_text()
        missing_blocks = [
            heading for heading in REQUIRED_PROMPT_BLOCK_HEADINGS if heading not in prompt_text
        ]
        if missing_blocks:
            raise SystemExit(
                "style profile prompt-blocks.md missing required section(s): "
                + ", ".join(missing_blocks)
            )
        values["prompt_blocks_path"] = str(prompt_blocks)
    else:
        legacy_required = [
            "universal_positive",
            "universal_negative",
            "universal_closing",
        ]
        legacy_missing = [field for field in legacy_required if not frontmatter_field(fm, field)]
        if legacy_missing:
            raise SystemExit(
                "style profile missing prompt-blocks.md and legacy field(s): "
                + ", ".join(legacy_missing)
            )
    return values


def validate_adapter_contract(adapter: str) -> dict[str, str]:
    skill = SKILL_ROOT / adapter / "SKILL.md"
    if not skill.exists():
        raise SystemExit(f"engine adapter skill not found: {skill}")
    fm = extract_frontmatter(skill)
    if not frontmatter_has_block(fm, "adapter_contract"):
        raise SystemExit(f"adapter_contract missing: {skill}")
    values: dict[str, str] = {}
    for field in [
        "underlying_model",
        "input_fields",
        "output_format",
        "positives_slot",
        "negatives_slot",
        "closing_slot",
        "modes_supported",
    ]:
        value = frontmatter_field(fm, field)
        if not value:
            raise SystemExit(f"adapter_contract missing field {field}: {skill}")
        values[field] = value
    return values


def validate_engine_adapter_pair(engine: str, adapter: str) -> None:
    contract = validate_adapter_contract(adapter)
    underlying = contract["underlying_model"]
    if engine != underlying:
        raise SystemExit(
            f"engine/adapter mismatch: engine '{engine}' does not match {adapter}.adapter_contract.underlying_model '{underlying}'"
        )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_project(project: str) -> Path:
    direct = Path(project)
    if direct.exists():
        return direct.resolve()
    matches = sorted(CLIENTS_DIR.glob(f"*/videos/{project}"))
    matches += sorted(
        CLIENTS_DIR.glob(f"*/campaigns/*/video-concepts/*/06_generation-runs/{project}")
    )
    if not matches:
        raise SystemExit(f"video project not found: {project}")
    if len(matches) > 1:
        raise SystemExit(
            "ambiguous video project: "
            + ", ".join(str(path.relative_to(REPO_ROOT)) for path in matches)
        )
    return matches[0]


def gate_path(project_dir: Path, gate: str) -> Path:
    if gate not in GATE_PATHS:
        raise SystemExit(f"gate has no explicit _gate.json in W1/W2: {gate}")
    return project_dir / GATE_PATHS[gate]


def initial_gate(phase: str, at: str) -> dict[str, Any]:
    return {
        "phase": phase,
        "status": "pending",
        "expected_artifacts": EXPECTED_ARTIFACTS[phase],
        "in_progress_artifacts": [],
        "completed_artifacts": [],
        "upstream_hashes": {},
        "approved_at": None,
        "approved_by": None,
        "notes": "phase scaffolded; no artifacts generated yet",
        "history": [
            {
                "status": "pending",
                "at": at,
                "reason": "phase scaffolded; no artifacts generated yet",
            }
        ],
    }


def source_section(client_dir: Path, filename: str, label: str, n: int) -> str:
    path = client_dir / filename
    heading = f"## Priority {n} — {filename} ({label})"
    if not path.exists():
        return f"{heading}\n\n_Missing in client folder._\n"
    rel = path.relative_to(REPO_ROOT)
    return f"{heading}\n\nSource: `{rel}`\n\n```text\n{path.read_text().strip()}\n```\n"


def write_concept(project_dir: Path, client_dir: Path, client: str, slug: str, at: str) -> None:
    sections = [
        source_section(client_dir, filename, label, i)
        for i, (filename, label) in enumerate(CONCEPT_SOURCES, start=1)
    ]
    content = f"""---
phase: concept
status: approved
approved_at: {at}
approved_by: video:new
source_priority: [context-profile.json, brand-voice.md, icp.md, offer.md, awareness-stage.md, learnings.md]
---

# Concept Seed — {client} / {slug}

This zero-credit concept seed was generated from existing client research. Later priority files override earlier files where they conflict.

{chr(10).join(sections)}
"""
    (project_dir / "00-concept.md").write_text(content)


def concept_output_dir(client: str, campaign: str, concept_slug: str) -> Path:
    return (
        CLIENTS_DIR
        / client
        / "campaigns"
        / campaign
        / "video-concepts"
        / concept_slug
    )


def find_approval_file(folder: Path) -> Path:
    for candidate in [
        folder / "07_review" / "approval-2.json",
        folder / "02_ag1-options" / "approval-1.json",
        folder / "02_concepts" / "approval-1.json",
        folder / "brief-pack" / "approval-2.json",
        folder / "approval.json",  # legacy
        folder / "approval-1.json",
    ]:
        if candidate.exists():
            return candidate
    raise SystemExit(
        "missing approval file: expected 07_review/approval-2.json "
        f"(or legacy approval.json) in {folder}"
    )


def load_concept_handoff(client: str, campaign: str, concept_slug: str) -> tuple[Path, dict[str, Any], dict[str, Any], Path]:
    folder = concept_output_dir(client, campaign, concept_slug)
    if not folder.is_dir():
        raise SystemExit(f"concept output folder not found: {folder}")
    handoff_path = folder / "05_prompt-packs" / "video-factory-handoff.json"
    legacy_handoff_path = folder / "video-factory-handoff.json"
    if not handoff_path.exists() and legacy_handoff_path.exists():
        handoff_path = legacy_handoff_path
    approval_path = find_approval_file(folder)
    handoff = load_json(handoff_path) if handoff_path.exists() else {}
    approval = load_json(approval_path)
    if handoff and handoff.get("handoff_type") not in {
        "video-concept-lab-to-video-factory",  # legacy
        "video-brief-normalizer-to-video-factory",
    }:
        raise SystemExit(f"unsupported handoff_type: {handoff.get('handoff_type')}")
    for key, expected in {
        "client": client,
        "campaign": campaign,
        "concept_slug": concept_slug,
    }.items():
        if handoff and handoff.get(key) != expected:
            raise SystemExit(
                f"handoff {key} mismatch: expected '{expected}', got '{handoff.get(key)}'"
            )
        if approval.get(key) != expected:
            raise SystemExit(
                f"approval {key} mismatch: expected '{expected}', got '{approval.get(key)}'"
            )
    return folder, handoff, approval, approval_path


def require_handoff_files(handoff: dict[str, Any], folder: Path) -> dict[str, Path]:
    if not handoff:
        raise SystemExit("missing 05_prompt-packs/video-factory-handoff.json")
    paths: dict[str, Path] = {}
    for name, value in handoff.get("source_files", {}).items():
        if not value:
            continue
        raw_path = Path(value)
        if raw_path.is_absolute():
            path = raw_path
        else:
            folder_candidate = folder / raw_path
            repo_candidate = REPO_ROOT / raw_path
            path = folder_candidate if folder_candidate.exists() else repo_candidate
        if not path.exists():
            raise SystemExit(f"handoff source file missing ({name}): {path}")
        paths[name] = path
    new_required = [
        "concept_pack_json",
        "concept_pack_markdown",
        "final_script",
        "visual_treatment",
        "google_docs_brief",
        "video_brief_markdown",
        "video_brief_json",
        "input_image_plan",
        "canonical_prompt_pack_json",
        "manual_run_guide",
        "higgsfield_seedance_adapter",
    ]
    legacy_required = [
        "concept_pack_json",
        "concept_pack_markdown",
        "winner_script",
        "image_handoff",
    ]
    if all(required in paths for required in new_required):
        return paths
    if all(required in paths for required in legacy_required):
        return paths
    missing = [required for required in new_required if required not in paths]
    raise SystemExit(
        "handoff missing required source_files for brief-pack flow: "
        + ", ".join(missing)
    )
    return paths


def render_segments_for_duration(duration: int, cap: int = 15) -> int:
    return max(1, (duration + cap - 1) // cap)


def render_units_for_duration(duration: int, cap: int = 15) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    remaining = duration
    index = 1
    while remaining > 0:
        unit_duration = min(cap, remaining)
        units.append(
            {
                "unit_id": f"scene-{index:02d}",
                "duration_seconds": unit_duration,
                "max_render_segment_seconds": cap,
            }
        )
        remaining -= unit_duration
        index += 1
    return units or [
        {
            "unit_id": "scene-01",
            "duration_seconds": cap,
            "max_render_segment_seconds": cap,
        }
    ]


def validate_video_brief_contract(
    paths: dict[str, Path], handoff: dict[str, Any]
) -> dict[str, int]:
    if "video_brief_json" not in paths:
        return {}
    brief = load_json(paths["video_brief_json"])
    fmt = brief.get("format", {})
    intent = handoff.get("model_agnostic_render_intent", {})
    raw_duration = (
        fmt.get("duration_seconds_estimate")
        or brief.get("duration_seconds_estimate")
        or intent.get("duration_seconds_estimate")
    )
    if raw_duration is None:
        raise SystemExit(
            f"video brief missing duration_seconds_estimate: {paths['video_brief_json']}"
        )
    duration = int(raw_duration)
    cap = int(
        fmt.get("render_segment_cap_seconds")
        or fmt.get("max_render_segment_seconds")
        or 15
    )
    if cap > 15:
        raise SystemExit(
            f"video brief render segment cap must be <=15s, got {cap}: {paths['video_brief_json']}"
        )
    expected_segments = render_segments_for_duration(duration, cap)
    declared_segments = fmt.get("segments_count")
    if declared_segments is not None and int(declared_segments) != expected_segments:
        raise SystemExit(
            "video brief segments_count mismatch: "
            f"expected {expected_segments} for {duration}s at <= {cap}s, "
            f"got {declared_segments}: {paths['video_brief_json']}"
        )
    return {
        "duration_seconds_estimate": duration,
        "render_segment_cap_seconds": cap,
        "segments_count": expected_segments,
    }


def selected_concept_from_pack(concept_pack: dict[str, Any], selected_concept: str) -> dict[str, Any]:
    for concept in concept_pack.get("concepts", []):
        if concept.get("concept_id") == selected_concept:
            return concept
    raise SystemExit(f"selected concept '{selected_concept}' not found in concept-pack.json")


def approved_concept_ids(approval: dict[str, Any]) -> list[str]:
    approved_ids = approval.get("approved_concept_ids") or []
    selected = approval.get("selected_concept_id") or approval.get("recommended_concept_id")
    if selected and selected not in approved_ids:
        approved_ids.append(selected)
    return approved_ids


def review_target(folder: Path) -> Path:
    for candidate in [
        folder / "05_prompt-packs" / "brief-pack" / "google-docs-brief.md",
        folder / "05_prompt-packs" / "brief-pack" / "video-brief.md",
        folder / "02_ag1-options" / "concept-pack.md",
        folder / "02_concepts" / "concept-pack.md",
        folder / "brief-pack" / "google-docs-brief.md",
        folder / "brief-pack" / "video-brief.md",
        folder / "concept-pack.md",
    ]:
        if candidate.exists():
            return candidate
    return folder


def handoff_approval_error(
    folder: Path,
    approval: dict[str, Any],
    approval_path: Path,
    handoff_exists: bool,
) -> str | None:
    stage = approval.get("approval_stage")
    if stage == "concept":
        return (
            "Approval Gate 1 is approved for concept only; Approval Gate 2 is required before Video Factory.\n"
            f"Run script/visual refinement and video-brief-normalizer, then approve: {folder / '07_review' / 'approval-2.json'}"
        )
    status = approval.get("status")
    if status != "approved":
        return (
            f"brief-pack approval is '{status}', not 'approved'.\n"
            f"Review: {review_target(folder)}\n"
            f"Update approval file before creating a Video Factory project: {approval_path}"
        )
    if not handoff_exists:
        return (
            "brief-pack approval is approved, but 05_prompt-packs/video-factory-handoff.json is missing.\n"
            f"Create it from the approved video brief before creating a Video Factory project: {folder / '05_prompt-packs' / 'video-factory-handoff.json'}"
        )
    approved_ids = approved_concept_ids(approval)
    if not approved_ids:
        return f"approval file is approved but approved_concept_ids/selected_concept_id is empty: {approval_path}"
    return None


def write_concept_from_handoff(
    project_dir: Path,
    *,
    handoff: dict[str, Any],
    approval: dict[str, Any],
    paths: dict[str, Path],
    concept_pack: dict[str, Any],
    concept: dict[str, Any],
    selected_concept: str,
    at: str,
) -> None:
    intent = handoff.get("model_agnostic_render_intent", {})
    rel_sources = {name: path_label(path) for name, path in paths.items()}
    source_hashes = {
        name: sha256(path)
        for name, path in paths.items()
        if path.is_file()
    }
    script_path = paths.get("final_script") or paths["winner_script"]
    production_brief_path = (
        paths.get("video_brief_markdown")
        or paths.get("image_handoff")
        or script_path
    )
    script_text = script_path.read_text().strip()
    production_brief_text = production_brief_path.read_text().strip()
    visual_text = (
        paths["visual_treatment"].read_text().strip()
        if "visual_treatment" in paths
        else ""
    )
    required_edits = concept_pack.get("recommended_winner", {}).get(
        "required_edits_before_production", []
    )
    concept_title = concept.get("concept_title", selected_concept)
    content = f"""---
phase: concept
status: approved
approved_at: {approval.get('approved_at') or at}
approved_by: {approval.get('approved_by') or 'approval file'}
source: video-concept-lab
concept_pack_schema: {concept_pack.get('schema_version')}
campaign: {handoff['campaign']}
concept_slug: {handoff['concept_slug']}
selected_concept_id: {selected_concept}
recommended_ad_format: {intent.get('recommended_ad_format') or concept.get('recommended_ad_format')}
use_case: {intent.get('use_case')}
truth_source: {intent.get('truth_source')}
mode: {intent.get('mode')}
script_path: {path_label(script_path)}
visual_treatment_path: {rel_sources.get('visual_treatment', '')}
video_brief_path: {path_label(production_brief_path)}
handoff_path: clients/{handoff['client']}/campaigns/{handoff['campaign']}/video-concepts/{handoff['concept_slug']}/05_prompt-packs/video-factory-handoff.json
---

# Approved Concept — {concept_title}

Client: `{handoff['client']}`
Campaign: `{handoff['campaign']}`
Concept slug: `{handoff['concept_slug']}`
Selected concept: `{selected_concept}`

## Resume Contract

This video project was imported from Video Concept Lab. It is safe to resume from this folder with `/video:resume`.

The concept is approved. Render remains blocked until input images, beat sheet, render prompt, and `renderRequest.json` are approved.

## Model-Agnostic Render Intent

```json
{json.dumps(intent, indent=2, ensure_ascii=False)}
```

## Selected Concept

```json
{json.dumps(concept, indent=2, ensure_ascii=False)}
```

## Required Edits Before Production

{chr(10).join(f"- {item}" for item in required_edits) if required_edits else "- None recorded."}

## Source Files

{chr(10).join(f"- `{name}`: `{path}`" for name, path in rel_sources.items())}

## Source Hashes

```json
{json.dumps(source_hashes, indent=2, ensure_ascii=False)}
```

## Final Script

{script_text}

## Visual Treatment

{visual_text if visual_text else '_No separate visual treatment supplied in legacy handoff._'}

## Normalized AI Production Brief

{production_brief_text}
"""
    (project_dir / "00-concept.md").write_text(content)


def load_lock(project_dir: Path) -> dict[str, Any]:
    lock_path = project_dir / "lock.json"
    if not lock_path.exists():
        raise SystemExit(f"missing lock.json: {lock_path}")
    lock = load_json(lock_path)
    if lock.get("schema_version") != SCHEMA_VERSION:
        raise SystemExit(
            f"lock.json schema_version '{lock.get('schema_version')}' does not match current schema '{SCHEMA_VERSION}'"
        )
    return lock


def gate_status_for_index(project_dir: Path, phase: str) -> str:
    if phase == "concept":
        return "approved" if (project_dir / "00-concept.md").exists() else "not-started"
    if phase == "final":
        return "not-started"
    path = gate_path(project_dir, phase)
    if not path.exists():
        return "not-started"
    gate = load_json(path)
    status = gate.get("status")
    if status == "approved":
        return "approved"
    if status in {"executing", "blocked"}:
        return status
    if gate.get("in_progress_artifacts") or gate.get("completed_artifacts"):
        return "pending"
    return "not-started"


def all_statuses(project_dir: Path) -> dict[str, str]:
    return {phase: gate_status_for_index(project_dir, phase) for phase in PHASES}


def first_unapproved(statuses: dict[str, str]) -> str:
    for phase in PHASES:
        if statuses.get(phase) != "approved":
            return phase
    return "final"


def gate_symbol(status: str) -> str:
    return {
        "approved": "[✓]",
        "pending": "[⏳]",
        "blocked": "[⚠]",
        "executing": "[▶]",
        "not-started": "[—]",
    }.get(status, "[—]")


def concept_approval(project_dir: Path) -> tuple[str, str]:
    text = (project_dir / "00-concept.md").read_text()
    approved_at = re.search(r"^approved_at:\s*(.+)$", text, re.M)
    approved_by = re.search(r"^approved_by:\s*(.+)$", text, re.M)
    return (
        approved_at.group(1).strip() if approved_at else "unknown-time",
        approved_by.group(1).strip() if approved_by else "unknown",
    )


def gate_line(project_dir: Path, phase: str, status: str) -> str:
    label = f"{phase:<13}"
    if phase == "concept" and status == "approved":
        approved_at, approved_by = concept_approval(project_dir)
        return f"  [✓] {label} (approved {approved_at} by {approved_by})"
    if phase in GATE_PATHS and (project_dir / GATE_PATHS[phase]).exists():
        gate = load_json(project_dir / GATE_PATHS[phase])
        if status == "approved":
            extra = f"approved {gate.get('approved_at')}"
            if phase == "beat-sheet" and gate.get("winner_variation"):
                extra += f", winner {gate['winner_variation']}"
            return f"  [✓] {label} ({extra})"
    if status == "pending":
        return f"  [⏳] {label} (pending)"
    if status == "executing":
        return f"  [▶] {label} (executing)"
    if status == "blocked":
        return f"  [⚠] {label} (blocked)"
    return f"  [—] {label} (not-started)"


def next_step(project_id: str, blocked_on: str) -> str:
    if blocked_on == "stills":
        return f"Run /video:resume {project_id} to start stills planning; no Higgsfield credits are spent until render approval."
    if blocked_on == "beat-sheet":
        return f"Review 01-stills outputs, then run /video:approve {project_id} stills."
    if blocked_on == "motion":
        return f"Review 02-beat-sheet/v1/frames.json, then run /video:approve {project_id} beat-sheet."
    if blocked_on == "render":
        return f"Review 04-motion/shot-*.md, then run /video:approve {project_id} motion."
    if blocked_on == "final":
        return f"Review 05-runs/render-01/outputs/, then run /video:approve {project_id} render."
    return "All gates approved; archive or retarget if needed."


def write_index(project_dir: Path, last_sub_agent: str) -> None:
    lock = load_lock(project_dir)
    statuses = all_statuses(project_dir)
    blocked_on = first_unapproved(statuses)
    touched = now_iso()
    credits_spent = int(lock.get("credits_spent", 0))
    budget = int(lock.get("budget_credits", 0))
    remaining = max(budget - credits_spent, 0)
    phase_yaml = "\n".join(f"  {phase}: {statuses[phase]}" for phase in PHASES)
    table = "\n".join(
        f"| {phase} | {phase_path(phase)} | {status_label(statuses[phase])} |"
        for phase in PHASES
    )
    content = f"""---
project_id: {lock['project_id']}
last_touched: {touched}
last_sub_agent: {last_sub_agent}
phase_status:
{phase_yaml}
blocked_on: {blocked_on}
credits_spent: {credits_spent}
credits_remaining: {remaining}
---

# {lock['client']} — {lock['video_slug']} ({lock['duration_seconds']}s)

Style: {lock['style_preset']} · Model route: {lock['engine']} / {lock['engine_adapter']} · Aspect: {lock['aspect_ratio']} · Budget: {credits_spent}/{budget} used

## Files

| Phase | Path | Status |
|---|---|---|
{table}

## Next step

{next_step(lock['project_id'], blocked_on)}
"""
    (project_dir / "INDEX.md").write_text(content)


def status_label(status: str) -> str:
    if status == "approved":
        return "✓ approved"
    if status == "pending":
        return "⏳ pending HITL"
    if status == "executing":
        return "▶ executing"
    if status == "blocked":
        return "⚠ blocked"
    return "— not started"


def phase_path(phase: str) -> str:
    return {
        "concept": "00-concept.md",
        "stills": "01-stills/",
        "beat-sheet": "02-beat-sheet/v1/",
        "motion": "04-motion/",
        "render": "05-runs/",
        "final": "05-runs/render-NN/verdict.md",
    }[phase]


def clip_ids_for_segments(segments_count: int) -> list[str]:
    return [f"clip-{index:02d}" for index in range(1, max(segments_count, 1) + 1)]


def write_clip_run_files(
    project_dir: Path,
    *,
    lock: dict[str, Any],
    handoff: dict[str, Any],
    source_hashes: dict[str, str],
) -> None:
    clip_ids = clip_ids_for_segments(int(lock.get("segments_count") or 1))
    adapter_path = "05_prompt-packs/model-adapters/higgsfield-seedance.json"
    clips = []
    for order, clip_id in enumerate(clip_ids, start=1):
        clip_dir = project_dir / "clips" / clip_id
        clip_dir.mkdir(parents=True, exist_ok=True)
        payload_path = project_dir / "payloads" / f"{clip_id}.json"
        output_path = clip_dir / "output.mp4"
        payload = {
            "schema_version": SCHEMA_VERSION,
            "clip_id": clip_id,
            "stitch_order": order,
            "status": "pending_payload_compile",
            "source_adapter": adapter_path,
            "source_handoff": "concept-source-handoff.json",
            "notes": "Replace this placeholder with the approved executor payload before rendering.",
        }
        write_json(payload_path, payload)
        clips.append(
            {
                "clip_id": clip_id,
                "stitch_order": order,
                "payload_path": path_label(payload_path),
                "output_path": path_label(output_path),
                "review_status": "pending",
                "retry_requested": False,
            }
        )

    review = {
        "schema_version": SCHEMA_VERSION,
        "project_id": lock["project_id"],
        "review_stage": "clip_review",
        "clips": [
            {
                "clip_id": clip["clip_id"],
                "status": "pending",
                "notes": "",
                "retry_reason": "",
            }
            for clip in clips
        ],
        "stitch_approved": False,
    }
    write_json(project_dir / "review" / "review.json", review)

    filelist_lines = "\n".join(
        f"# file '../clips/{clip['clip_id']}/output.mp4'" for clip in clips
    )
    (project_dir / "stitch" / "ffmpeg-command.sh").write_text(
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n\n"
        "# Uncomment approved clips in filelist.txt, then run this script.\n"
        "ffmpeg -f concat -safe 0 -i stitch/filelist.txt -c copy stitch/final.mp4\n"
    )
    (project_dir / "stitch" / "filelist.txt").write_text(filelist_lines + "\n")

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "run_mode": "clip-run",
        "project_id": lock["project_id"],
        "created_at": lock["created_at"],
        "source": lock.get("concept_source", {}),
        "source_hashes": source_hashes,
        "executor": {
            "engine": lock.get("engine"),
            "engine_adapter": lock.get("engine_adapter"),
            "status": lock.get("engine_selection_status", "deferred"),
        },
        "clips": clips,
        "review_path": path_label(project_dir / "review" / "review.json"),
        "stitch": {
            "filelist_path": path_label(project_dir / "stitch" / "filelist.txt"),
            "command_path": path_label(project_dir / "stitch" / "ffmpeg-command.sh"),
            "output_path": path_label(project_dir / "stitch" / "final.mp4"),
        },
        "optional_helper_folders": [
            "stills/",
            "beat-sheets/",
            "motion-prompts/",
            "rerenders/",
        ],
        "handoff_type": handoff.get("handoff_type"),
    }
    write_json(project_dir / "run-manifest.json", manifest)


def write_clip_run_index(project_dir: Path, last_sub_agent: str) -> None:
    lock = load_lock(project_dir)
    manifest = load_json(project_dir / "run-manifest.json")
    review = load_json(project_dir / "review" / "review.json")
    touched = now_iso()
    review_by_id = {clip["clip_id"]: clip for clip in review.get("clips", [])}
    rows = []
    approved_clip_count = 0
    rendered_clip_count = 0
    for clip in manifest.get("clips", []):
        output_path = repo_path(clip["output_path"])
        rendered = output_path.exists()
        rendered_clip_count += 1 if rendered else 0
        status = review_by_id.get(clip["clip_id"], {}).get("status", "pending")
        approved_clip_count += 1 if status == "approved" else 0
        rows.append(
            f"| {clip['clip_id']} | {clip['payload_path']} | {clip['output_path']} | {'yes' if rendered else 'no'} | {status} |"
        )

    next_step = "Compile approved payloads and render missing clips."
    if rendered_clip_count == len(manifest.get("clips", [])):
        next_step = "Review generated clips in review/review.json."
    if approved_clip_count:
        next_step = "Update stitch/filelist.txt with approved clips, then run stitch/ffmpeg-command.sh."
    if (project_dir / "stitch" / "final.mp4").exists():
        next_step = "Review stitch/final.mp4 and archive accepted deliverables."

    content = f"""---
project_id: {lock['project_id']}
run_mode: clip-run
last_touched: {touched}
last_sub_agent: {last_sub_agent}
rendered_clips: {rendered_clip_count}
approved_clips: {approved_clip_count}
---

# {lock['client']} — {lock['video_slug']} ({lock['duration_seconds']}s)

Model route: {lock['engine']} / {lock['engine_adapter']} · Aspect: {lock['aspect_ratio']}

## Clips

| Clip | Payload | Output | Rendered | Review |
|---|---|---|---|---|
{chr(10).join(rows)}

## Stitch

- Filelist: `{manifest['stitch']['filelist_path']}`
- Command: `{manifest['stitch']['command_path']}`
- Output: `{manifest['stitch']['output_path']}`

## Next step

{next_step}
"""
    (project_dir / "INDEX.md").write_text(content)


def command_new(args: argparse.Namespace) -> None:
    if not slug_ok(args.client):
        raise SystemExit("client must be lowercase kebab-case")
    if not slug_ok(args.slug):
        raise SystemExit("video slug must be lowercase kebab-case")
    client_dir = CLIENTS_DIR / args.client
    if not client_dir.is_dir():
        raise SystemExit(f"client folder not found: {client_dir}")

    style_values = validate_style_profile(args.style)
    adapter = args.engine_adapter or style_values["recommended_engine_adapter"]
    engine = args.engine or style_values["recommended_motion_engine"]
    validate_engine_adapter_pair(engine, adapter)

    project_id = f"{args.slug}-{today_suffix()}"
    project_dir = client_dir / "videos" / project_id
    if project_dir.exists():
        raise SystemExit(f"video project already exists: {project_dir}")

    at = now_iso()
    for folder in [
        project_dir,
        project_dir / "01-stills",
        project_dir / "02-beat-sheet" / "v1",
        project_dir / "04-motion",
        project_dir / "05-runs",
    ]:
        folder.mkdir(parents=True, exist_ok=False)

    lock = {
        "schema_version": SCHEMA_VERSION,
        "project_id": project_id,
        "client": args.client,
        "video_slug": args.slug,
        "created_at": at,
        "duration_class": "short" if args.duration < 60 else "medium",
        "duration_seconds": args.duration,
        "aspect_ratio": args.aspect_ratio,
        "use_case": args.use_case,
        "style_preset": args.style,
        "product_mode": args.product_mode,
        "character_id": None,
        "wardrobe_id": None,
        "engine": engine,
        "engine_adapter": adapter,
        "brand_assets": {
            "product_hero": None,
            "logo": None,
            "character_ref": None,
            "brand_palette": None,
        },
        "audio": {
            "voiceover_script": args.voiceover_script or "",
            "cut_tempo": "TBD",
            "sfx_universal": [],
        },
        "budget_credits": args.budget_credits,
        "budget_stop_threshold": args.budget_stop_threshold,
        "photoreal_stack_ref": None,
        "hero_frames": "TBD-via-testing",
        "style_profile_path": str(STYLE_ROOT / args.style) + "/",
        "retarget_history": [],
    }
    write_json(project_dir / "lock.json", lock)
    write_concept(project_dir, client_dir, args.client, args.slug, at)

    for phase in ["stills", "beat-sheet", "motion", "render"]:
        write_json(gate_path(project_dir, phase), initial_gate(phase, at))

    write_index(project_dir, "video:new")
    print(f"Project {project_id} initialized.")
    print(f"Path: {project_dir}")
    print(f"Run /video:status {project_id} to confirm.")


def command_validate_handoff(args: argparse.Namespace) -> None:
    folder, handoff, approval, approval_path = load_concept_handoff(
        args.client, args.campaign, args.concept_slug
    )
    handoff_exists = bool(handoff)
    paths: dict[str, Path] = {}
    concept_pack: dict[str, Any] = {}
    if handoff_exists:
        paths = require_handoff_files(handoff, folder)
        segment_plan = validate_video_brief_contract(paths, handoff)
        concept_pack = load_json(paths["concept_pack_json"])
    else:
        segment_plan = {}
        concept_pack_path = folder / "02_ag1-options" / "concept-pack.json"
        if not concept_pack_path.exists():
            concept_pack_path = folder / "02_concepts" / "concept-pack.json"
        if not concept_pack_path.exists():
            concept_pack_path = folder / "concept-pack.json"
        if concept_pack_path.exists():
            concept_pack = load_json(concept_pack_path)
    selected = (
        args.selected_concept
        or approval.get("selected_concept_id")
        or approval.get("recommended_concept_id")
    )
    if not selected:
        raise SystemExit("selected concept required: pass --selected-concept <concept-id>")
    if concept_pack:
        selected_concept_from_pack(concept_pack, selected)
    approval_error = handoff_approval_error(
        folder, approval, approval_path, handoff_exists
    )
    print(f"HANDOFF: {folder / '05_prompt-packs' / 'video-factory-handoff.json'}")
    print(f"APPROVAL: {approval_path}")
    print(f"SELECTED: {selected}")
    print(f"STATUS: {approval.get('status')}")
    if paths:
        print("SOURCES:")
        for name, path in paths.items():
            print(f"  {name}: {path}")
    if segment_plan:
        print(
            "SEGMENTS: "
            f"{segment_plan['segments_count']} render unit(s), "
            f"<= {segment_plan['render_segment_cap_seconds']}s each"
        )
    if approval_error:
        print()
        print("BLOCKED:")
        print(approval_error)
        if args.require_approved:
            raise SystemExit(1)
    else:
        print("READY: approved handoff can create a Video Factory project")


def command_new_from_concept(args: argparse.Namespace) -> None:
    if not slug_ok(args.client):
        raise SystemExit("client must be lowercase kebab-case")
    if not campaign_slug_ok(args.campaign):
        raise SystemExit("campaign must be lowercase with hyphens or underscores")
    if not slug_ok(args.concept_slug):
        raise SystemExit("concept slug must be lowercase kebab-case")

    client_dir = CLIENTS_DIR / args.client
    if not client_dir.is_dir():
        raise SystemExit(f"client folder not found: {client_dir}")

    folder, handoff, approval, approval_path = load_concept_handoff(
        args.client, args.campaign, args.concept_slug
    )
    approval_error = handoff_approval_error(
        folder, approval, approval_path, bool(handoff)
    )
    if approval_error and not args.allow_pending:
        raise SystemExit(approval_error)
    paths = require_handoff_files(handoff, folder)
    segment_plan = validate_video_brief_contract(paths, handoff)

    concept_pack = load_json(paths["concept_pack_json"])
    selected = args.selected_concept
    if not selected:
        approved_ids = approved_concept_ids(approval)
        selected = approved_ids[0] if approved_ids else approval.get("recommended_concept_id")
    if not selected:
        raise SystemExit("selected concept required: pass --selected-concept <concept-id>")
    if approval.get("status") == "approved" and selected not in approved_concept_ids(approval):
        raise SystemExit(
            f"selected concept '{selected}' is not approved by {approval_path}"
        )
    concept = selected_concept_from_pack(concept_pack, selected)

    intent = handoff.get("model_agnostic_render_intent", {})
    project_slug = args.video_slug or args.concept_slug
    if not slug_ok(project_slug):
        raise SystemExit("video slug must be lowercase kebab-case")
    project_id = f"{project_slug}-{today_suffix()}"
    project_dir = folder / "06_generation-runs" / project_id
    if project_dir.exists():
        raise SystemExit(f"video project already exists: {project_dir}")

    at = now_iso()
    for folder_path in [
        project_dir,
        project_dir / "payloads",
        project_dir / "clips",
        project_dir / "review",
        project_dir / "stitch",
    ]:
        folder_path.mkdir(parents=True, exist_ok=False)

    duration = (
        args.duration
        or int(segment_plan.get("duration_seconds_estimate") or 0)
        or int(intent.get("duration_seconds_estimate") or 45)
    )
    aspect_ratio = args.aspect_ratio or intent.get("aspect_ratio") or "9:16"
    segment_cap = int(segment_plan.get("render_segment_cap_seconds") or 15)
    segments_count = render_segments_for_duration(duration, segment_cap)
    style = args.style or intent.get("style_profile") or "deferred"
    engine = args.engine or "deferred"
    adapter = args.engine_adapter or "deferred"
    if style != "deferred":
        style_values = validate_style_profile(style)
        adapter = args.engine_adapter or style_values["recommended_engine_adapter"]
        engine = args.engine or style_values["recommended_motion_engine"]
        validate_engine_adapter_pair(engine, adapter)

    source_hashes = {
        name: sha256(path)
        for name, path in paths.items()
        if path.is_file()
    }
    script_source_path = paths.get("final_script") or paths["winner_script"]
    production_brief_source_path = (
        paths.get("video_brief_markdown")
        or paths.get("image_handoff")
        or script_source_path
    )
    rel_handoff = folder / "05_prompt-packs" / "video-factory-handoff.json"
    rel_approval = approval_path
    lock = {
        "schema_version": SCHEMA_VERSION,
        "run_mode": "clip-run",
        "project_id": project_id,
        "client": args.client,
        "campaign": args.campaign,
        "video_slug": project_slug,
        "created_at": at,
        "duration_class": "short" if duration < 60 else "medium",
        "duration_seconds": duration,
        "render_segment_cap_seconds": segment_cap,
        "segments_count": segments_count,
        "render_units": render_units_for_duration(duration, segment_cap),
        "aspect_ratio": aspect_ratio,
        "use_case": intent.get("use_case") or args.use_case,
        "truth_source": intent.get("truth_source"),
        "mode": intent.get("mode"),
        "recommended_ad_format": intent.get("recommended_ad_format")
        or concept.get("recommended_ad_format"),
        "style_preset": style,
        "product_mode": args.product_mode,
        "character_id": None,
        "wardrobe_id": None,
        "engine": engine,
        "engine_adapter": adapter,
        "engine_selection_status": handoff.get("engine_selection", {}).get(
            "status", "deferred"
        ),
        "brand_assets": {
            "product_hero": None,
            "logo": None,
            "character_ref": None,
            "brand_palette": None,
        },
        "audio": {
            "voiceover_script": path_label(script_source_path),
            "cut_tempo": "TBD",
            "sfx_universal": [],
        },
        "concept_source": {
            "source": "video-concept-lab",
            "concept_slug": args.concept_slug,
            "selected_concept_id": selected,
            "approval_path": path_label(rel_approval),
            "handoff_path": path_label(rel_handoff),
            "concept_pack_path": path_label(paths["concept_pack_json"]),
            "script_path": path_label(script_source_path),
            "visual_treatment_path": path_label(paths["visual_treatment"])
            if "visual_treatment" in paths
            else None,
            "video_brief_path": path_label(production_brief_source_path),
            "approved_at": approval.get("approved_at"),
            "approved_by": approval.get("approved_by"),
            "source_hashes": source_hashes,
        },
        "input_asset_requirements": handoff.get("input_asset_requirements", {}),
        "budget_credits": args.budget_credits,
        "budget_stop_threshold": args.budget_stop_threshold,
        "photoreal_stack_ref": None,
        "hero_frames": "TBD-via-testing",
        "style_profile_path": None if style == "deferred" else str(STYLE_ROOT / style) + "/",
        "retarget_history": [],
    }
    write_json(project_dir / "lock.json", lock)
    write_concept_from_handoff(
        project_dir,
        handoff=handoff,
        approval=approval,
        paths=paths,
        concept_pack=concept_pack,
        concept=concept,
        selected_concept=selected,
        at=at,
    )
    write_json(project_dir / "concept-source-handoff.json", handoff)
    write_clip_run_files(
        project_dir,
        lock=lock,
        handoff=handoff,
        source_hashes=source_hashes,
    )
    write_clip_run_index(project_dir, "video:new-from-concept")
    print(f"Project {project_id} initialized from approved concept.")
    print(f"Path: {project_dir}")
    print(f"Run /video:status {project_id} to confirm.")


def command_status(args: argparse.Namespace) -> None:
    project_dir = find_project(args.project)
    lock = load_lock(project_dir)
    if lock.get("run_mode") == "clip-run":
        write_clip_run_index(project_dir, "video:status")
        print((project_dir / "INDEX.md").read_text())
        return
    statuses = all_statuses(project_dir)
    blocked_on = first_unapproved(statuses)
    index_text = (project_dir / "INDEX.md").read_text()
    last_touched_match = re.search(r"^last_touched:\s*(.+)$", index_text, re.M)
    last_touched = last_touched_match.group(1).strip() if last_touched_match else lock["created_at"]
    credits_spent = int(lock.get("credits_spent", 0))
    budget = int(lock.get("budget_credits", 0))
    percent = int(round((credits_spent / budget) * 100)) if budget else 0

    print(f"PROJECT: {lock['project_id']}")
    print(f"LAST TOUCHED: {relative_time(last_touched)} — {last_touched}")
    print(f"STYLE: {lock['style_preset']}                       ENGINE: {lock['engine']} / {lock['engine_adapter']}")
    print(f"ASPECT: {lock['aspect_ratio']}                      BUDGET: {credits_spent}/{budget} ({percent}% used)")
    print()
    print("GATES:")
    for phase in PHASES:
        print(gate_line(project_dir, phase, statuses[phase]))
    print()
    print(f"BLOCKED ON: {blocked_on}")
    print(f"NEXT STEP: {next_step(lock['project_id'], blocked_on)}")


def relative_time(iso_value: str) -> str:
    try:
        stamp = datetime.fromisoformat(iso_value)
        delta = datetime.now().astimezone() - stamp
    except ValueError:
        return "unknown"
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return "0 minutes ago"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} minutes ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hours ago"
    return f"{hours // 24} days ago"


def upstream_paths(gate: str) -> list[Path]:
    return {
        "stills": [Path("00-concept.md")],
        "beat-sheet": [Path("00-concept.md"), GATE_PATHS["stills"]],
        "motion": [Path("00-concept.md"), GATE_PATHS["beat-sheet"]],
        "render": [Path("00-concept.md"), GATE_PATHS["motion"]],
    }.get(gate, [])


def required_upstream_gates(gate: str) -> list[str]:
    return {
        "stills": ["concept"],
        "beat-sheet": ["stills"],
        "motion": ["beat-sheet"],
        "render": ["motion"],
    }.get(gate, [])


def validate_upstream_approved(project_dir: Path, gate: str) -> None:
    statuses = all_statuses(project_dir)
    missing = [
        upstream
        for upstream in required_upstream_gates(gate)
        if statuses.get(upstream) != "approved"
    ]
    if missing:
        raise SystemExit(
            f"cannot approve {gate}: upstream gate(s) not approved: {', '.join(missing)}"
        )


def validate_expected_artifacts(project_dir: Path, gate: dict[str, Any]) -> None:
    missing: list[str] = []
    empty: list[str] = []
    for artifact in gate.get("expected_artifacts", []):
        path = project_dir / artifact
        if not path.exists():
            missing.append(artifact)
        elif path.is_file() and path.stat().st_size == 0:
            empty.append(artifact)
    if missing or empty:
        detail = []
        if missing:
            detail.append("missing: " + ", ".join(missing))
        if empty:
            detail.append("empty: " + ", ".join(empty))
        raise SystemExit(
            f"cannot approve {gate.get('phase')}: expected artifacts are not complete ({'; '.join(detail)})"
        )


def command_approve(args: argparse.Namespace) -> None:
    project_dir = find_project(args.project)
    load_lock(project_dir)
    if args.gate == "concept":
        if not (project_dir / "00-concept.md").exists():
            raise SystemExit("cannot approve concept: 00-concept.md missing")
        write_index(project_dir, "video:approve")
        print(f"concept already approved for {project_dir.name}")
        return

    path = gate_path(project_dir, args.gate)
    gate = load_json(path)
    validate_upstream_approved(project_dir, args.gate)
    validate_expected_artifacts(project_dir, gate)
    hashes = {}
    for rel in upstream_paths(args.gate):
        candidate = project_dir / rel
        if candidate.exists() and candidate.is_file():
            hashes[str(rel)] = sha256(candidate)
    gate["upstream_hashes"] = hashes
    gate["status"] = "approved"
    gate["approved_at"] = now_iso()
    gate["approved_by"] = args.approved_by
    gate["notes"] = args.notes
    gate.setdefault("history", []).append(
        {
            "status": "approved",
            "at": gate["approved_at"],
            "reason": args.notes or f"{args.gate} approved by /video:approve",
        }
    )
    if args.gate == "beat-sheet" and "winner_variation" not in gate:
        gate["winner_variation"] = "v1"
    write_json(path, gate)
    write_index(project_dir, "video:approve")
    print(f"{args.gate} approved for {project_dir.name}")


def command_resume(args: argparse.Namespace) -> None:
    project_dir = find_project(args.project)
    lock = load_lock(project_dir)
    statuses = all_statuses(project_dir)
    blocked_on = first_unapproved(statuses)
    print(f"Next phase: {blocked_on}")
    print(f"Invoke: {resume_invocation(lock, blocked_on)}")
    print("W1/W2 mode: manual dispatch only; no sub-agent was auto-started.")


def resume_invocation(lock: dict[str, Any], blocked_on: str) -> str:
    project = lock["project_id"]
    if blocked_on == "stills":
        return (
            f"/skills:select video-factory project={project} phase=stills "
            f"style_preset={lock['style_preset']} engine_adapter={lock['engine_adapter']}"
        )
    if blocked_on == "beat-sheet":
        return f"/skills:select beat-sheet-director project={project} phase=beat-sheet"
    if blocked_on == "motion":
        return (
            f"/skills:select {lock['engine_adapter']} project={project} phase=motion "
            f"style_preset={lock['style_preset']}"
        )
    if blocked_on == "render":
        return f"/skills:select higgsfield-generate project={project} phase=render"
    if blocked_on == "final":
        return f"review 05-runs for {project} and write verdict.md"
    return "no-op; all gates approved"


def command_validate_preflight(_: argparse.Namespace) -> None:
    validate_style_profile("crochet-handcrafted")
    validate_adapter_contract("cinema-worldbuilder")
    validate_adapter_contract("seedance-director")
    print("preflight ok: crochet-handcrafted style profile and adapter contracts are present")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Video pipeline W1/W2 local runner")
    sub = parser.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new")
    new.add_argument("client")
    new.add_argument("slug")
    new.add_argument("--style", default="crochet-handcrafted")
    new.add_argument("--engine")
    new.add_argument("--engine-adapter")
    new.add_argument("--duration", type=int, default=15)
    new.add_argument("--aspect-ratio", default="9:16")
    new.add_argument("--use-case", default="ugc-seedance")
    new.add_argument("--product-mode", default="generic")
    new.add_argument("--budget-credits", type=int, default=200)
    new.add_argument("--budget-stop-threshold", type=float, default=0.8)
    new.add_argument("--voiceover-script")
    new.set_defaults(func=command_new)

    validate_handoff = sub.add_parser("validate-handoff")
    validate_handoff.add_argument("client")
    validate_handoff.add_argument("campaign")
    validate_handoff.add_argument("concept_slug")
    validate_handoff.add_argument("--selected-concept")
    validate_handoff.add_argument("--require-approved", action="store_true")
    validate_handoff.set_defaults(func=command_validate_handoff)

    new_from_concept = sub.add_parser("new-from-concept")
    new_from_concept.add_argument("client")
    new_from_concept.add_argument("campaign")
    new_from_concept.add_argument("concept_slug")
    new_from_concept.add_argument("--selected-concept")
    new_from_concept.add_argument("--video-slug")
    new_from_concept.add_argument("--style")
    new_from_concept.add_argument("--engine")
    new_from_concept.add_argument("--engine-adapter")
    new_from_concept.add_argument("--duration", type=int)
    new_from_concept.add_argument("--aspect-ratio")
    new_from_concept.add_argument("--use-case", default="ugc-ad")
    new_from_concept.add_argument("--product-mode", default="generic")
    new_from_concept.add_argument("--budget-credits", type=int, default=200)
    new_from_concept.add_argument("--budget-stop-threshold", type=float, default=0.8)
    new_from_concept.add_argument("--allow-pending", action="store_true")
    new_from_concept.set_defaults(func=command_new_from_concept)

    status = sub.add_parser("status")
    status.add_argument("project")
    status.set_defaults(func=command_status)

    approve = sub.add_parser("approve")
    approve.add_argument("project")
    approve.add_argument("gate", choices=PHASES)
    approve.add_argument("--approved-by", default="jerel")
    approve.add_argument("--notes")
    approve.set_defaults(func=command_approve)

    resume = sub.add_parser("resume")
    resume.add_argument("project")
    resume.set_defaults(func=command_resume)

    validate = sub.add_parser("validate-preflight")
    validate.set_defaults(func=command_validate_preflight)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
