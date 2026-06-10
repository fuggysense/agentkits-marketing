#!/usr/bin/env python3
"""Validate video-concept-lab progressive-disclosure graph paths and key contracts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
SKILL_ROOT = SCRIPT_PATH.parents[1]
MARKETING_ROOT = SCRIPT_PATH.parents[3]
GRAPH_PATH = SKILL_ROOT / "REFERENCE_GRAPH.json"


def resolve_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return MARKETING_ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    if not GRAPH_PATH.exists():
        print(f"FAIL missing graph: {GRAPH_PATH}")
        return 1

    graph = json.loads(read_text(GRAPH_PATH))
    nodes = graph.get("nodes", {})
    loadouts = graph.get("loadouts", {})

    if not nodes:
        failures.append("graph has no nodes")
    if not loadouts:
        failures.append("graph has no loadouts")
    if "dr_singing_solution_aware_l3_concept" not in loadouts:
        failures.append("graph missing combined singing + solution-aware L3 loadout")

    for node_id, node in nodes.items():
        path_value = node.get("path")
        if not path_value:
            failures.append(f"node {node_id} missing path")
            continue
        if "02_concepts" in path_value:
            failures.append(f"node {node_id} uses stale 02_concepts path")
        if path_value == "proof-density-audit.md" or path_value.endswith("/proof-density-audit.md") and not path_value.startswith(".claude/"):
            failures.append(f"node {node_id} uses bare proof-density-audit path")
        resolved = resolve_path(path_value)
        if not resolved.exists():
            failures.append(f"node {node_id} path missing: {path_value}")

    for loadout_id, loadout in loadouts.items():
        required = loadout.get("required_nodes", [])
        if not required and "extends" not in loadout:
            failures.append(f"loadout {loadout_id} has no required_nodes and no extends")
        for key in ("required_nodes", "conditional_nodes", "source_nodes_available_on_conflict"):
            for node_id in loadout.get(key, []):
                if node_id not in nodes:
                    failures.append(f"loadout {loadout_id} references unknown {key} node {node_id}")
        parent = loadout.get("extends")
        if parent and parent not in loadouts:
            failures.append(f"loadout {loadout_id} extends unknown loadout {parent}")
    combined = loadouts.get("dr_singing_solution_aware_l3_concept", {})
    if combined and combined.get("extends") != "dr_solution_aware_l3_concept":
        failures.append("combined singing + solution-aware L3 loadout must extend dr_solution_aware_l3_concept")
    if combined and "singing_layer" not in combined.get("required_nodes", []):
        failures.append("combined singing + solution-aware L3 loadout must require singing_layer")

    seeder_path = Path("/Users/jerel/.claude/agents/video-concept-seeder.md")
    universal_eval_path = Path("/Users/jerel/.claude/agents/eval-video-universal.md")
    flow_eval_path = Path("/Users/jerel/.claude/agents/eval-video-flow-compliance.md")

    if seeder_path.exists():
        seeder_text = read_text(seeder_path)
        if "REFERENCE_GRAPH.json" not in seeder_text:
            failures.append("video-concept-seeder does not reference REFERENCE_GRAPH.json")
        if "methodology_receipt" not in seeder_text:
            failures.append("video-concept-seeder does not require methodology_receipt")

    for path in (universal_eval_path, flow_eval_path):
        if path.exists():
            text = read_text(path)
            if "concept-brief.json" not in text:
                failures.append(f"{path.name} does not reference concept-brief.json")
            if "expected_methodology_loadout_id" not in text:
                failures.append(f"{path.name} does not require expected_methodology_loadout_id")
            if "routing_verdict" not in text or "methodology_receipt_check" not in text:
                failures.append(f"{path.name} does not emit receipt routing verdict")
            if "methodology_receipt_seen" in text:
                failures.append(f"{path.name} still uses weak methodology_receipt_seen flag")

    active_contracts = [
        MARKETING_ROOT / "CLAUDE.md",
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "INDEX.md",
        SKILL_ROOT / "references/general/context-pack.md",
        SKILL_ROOT / "references/general/concept-generation.md",
        SKILL_ROOT / "references/general/creative-lanes-methodology.md",
        SKILL_ROOT / "references/general/stage-4-discrediting.md",
        SKILL_ROOT / "references/general/common-enemy-bridge.md",
        SKILL_ROOT / "references/general/video-compression-by-duration.md",
        SKILL_ROOT / "references/general/output-schema.md",
        SKILL_ROOT / "references/general/concept-input-packet.md",
        MARKETING_ROOT / "scripts/scaffold-client.sh",
        MARKETING_ROOT / "clients/README.md",
        MARKETING_ROOT / "skills/campaign-runner/templates/campaign-types/video-content.yaml",
        Path("/Users/jerel/.claude/prompts/orchestrators/vid-director.md"),
        Path("/Users/jerel/.claude/prompts/orchestrators/vid-director-flow.html"),
        seeder_path,
        universal_eval_path,
        flow_eval_path,
        Path("/Users/jerel/.claude/agents/eval-buyer-fit.md"),
    ]
    for path in active_contracts:
        if path.exists():
            for line_no, line in enumerate(read_text(path).splitlines(), start=1):
                if "02_concepts" in line and "not `02_concepts" not in line and "legacy" not in line.lower():
                    failures.append(f"active contract contains stale 02_concepts: {path}:{line_no}")

    if failures:
        print("REFERENCE_GRAPH_VALIDATION=FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("REFERENCE_GRAPH_VALIDATION=PASS")
    print(f"nodes={len(nodes)} loadouts={len(loadouts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
