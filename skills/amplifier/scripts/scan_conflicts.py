#!/usr/bin/env python3
"""
Conflict Scanner — Detects overlapping triggers, capabilities, and naming issues.

Usage:
    scan_conflicts.py                    # Scan everything
    scan_conflicts.py --target copywriting  # Scan conflicts for one skill/agent
    scan_conflicts.py --json             # Output as JSON

Detects:
    - Trigger overlaps (same trigger in multiple skills)
    - Agent capability overlap (Jaccard similarity > 0.5)
    - Name collisions (Levenshtein distance <= 2)
"""

import sys
import json
import re
from pathlib import Path
from collections import defaultdict


def find_project_root():
    """Walk up from script location to find project root (has CLAUDE.md)."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return None


def find_registry(root):
    """Find skills-registry.json."""
    # Check .claude/skills/ first (actual location)
    candidate = root / ".claude" / "skills" / "skills-registry.json"
    if candidate.exists():
        return candidate
    # Fallback to root
    candidate = root / "skills-registry.json"
    if candidate.exists():
        return candidate
    return None


def levenshtein(s1, s2):
    """Compute Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
    return prev_row[-1]


def jaccard_similarity(set_a, set_b):
    """Compute Jaccard similarity between two sets."""
    if not set_a and not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union) if union else 0.0


def parse_agent_capabilities(agent_path):
    """Extract capabilities from an agent .md file."""
    content = agent_path.read_text()
    capabilities = set()

    # Extract from skill integrations, tools, responsibilities sections
    lines = content.split("\n")
    in_capabilities = False
    for line in lines:
        lower = line.lower().strip()
        if any(
            kw in lower
            for kw in [
                "## capabilities",
                "## responsibilities",
                "## skills",
                "## tools",
                "## skill integrations",
            ]
        ):
            in_capabilities = True
            continue
        if in_capabilities:
            if line.startswith("## "):
                in_capabilities = False
                continue
            # Extract bullet items
            match = re.match(r"^\s*[-*]\s+[`]*([^`\n:]+)", line)
            if match:
                cap = match.group(1).strip().lower()
                if len(cap) > 2:
                    capabilities.add(cap)

    return capabilities


def load_skills_from_registry(registry_path):
    """Load skill data from registry."""
    data = json.loads(registry_path.read_text())
    skills = {}
    for skill in data.get("skills", []):
        skill_id = skill.get("id", "")
        skills[skill_id] = {
            "triggers": [t.lower() for t in skill.get("triggers", [])],
            "category": skill.get("category", ""),
            "agents": skill.get("agents", []),
            "description": skill.get("description", ""),
        }
    return skills


def scan_trigger_overlaps(skills, target=None):
    """Find triggers that appear in multiple skills."""
    trigger_index = defaultdict(list)
    for skill_id, data in skills.items():
        for trigger in data["triggers"]:
            trigger_index[trigger].append(skill_id)

    conflicts = []
    for trigger, skill_ids in trigger_index.items():
        if len(skill_ids) > 1:
            if target and target not in skill_ids:
                continue
            # Cross-category = high severity
            categories = {skills[s]["category"] for s in skill_ids}
            severity = "HIGH" if len(categories) > 1 else "MEDIUM"
            conflicts.append(
                {
                    "type": "trigger_overlap",
                    "trigger": trigger,
                    "skills": skill_ids,
                    "severity": severity,
                    "categories": list(categories),
                }
            )

    return sorted(conflicts, key=lambda c: (c["severity"] == "MEDIUM", c["trigger"]))


def scan_agent_capability_overlaps(root, target=None):
    """Find agents with overlapping capabilities (Jaccard > 0.5)."""
    agents_dir = root / "agents"
    if not agents_dir.exists():
        return []

    agents = {}
    for agent_file in agents_dir.glob("*.md"):
        name = agent_file.stem
        if name.endswith("-learnings") or name.endswith("-attribution"):
            continue
        if name == "README":
            continue
        agents[name] = parse_agent_capabilities(agent_file)

    conflicts = []
    agent_names = list(agents.keys())
    for i in range(len(agent_names)):
        for j in range(i + 1, len(agent_names)):
            a, b = agent_names[i], agent_names[j]
            if target and target not in (a, b):
                continue
            sim = jaccard_similarity(agents[a], agents[b])
            if sim > 0.5:
                shared = agents[a] & agents[b]
                conflicts.append(
                    {
                        "type": "capability_overlap",
                        "agents": [a, b],
                        "jaccard": round(sim, 3),
                        "shared_capabilities": list(shared)[:10],
                        "severity": "HIGH" if sim > 0.7 else "MEDIUM",
                    }
                )

    return sorted(conflicts, key=lambda c: -c["jaccard"])


def scan_name_collisions(skills, root, target=None):
    """Find skill/agent names within Levenshtein distance <= 2."""
    all_names = list(skills.keys())

    # Add agent names
    agents_dir = root / "agents"
    if agents_dir.exists():
        for f in agents_dir.glob("*.md"):
            name = f.stem
            if not name.endswith("-learnings") and not name.endswith("-attribution") and name != "README":
                all_names.append(f"agent:{name}")

    collisions = []
    for i in range(len(all_names)):
        for j in range(i + 1, len(all_names)):
            a_raw, b_raw = all_names[i], all_names[j]
            a = a_raw.replace("agent:", "")
            b = b_raw.replace("agent:", "")
            if a == b:
                continue
            if target and target not in (a, b):
                continue
            dist = levenshtein(a, b)
            if dist <= 2 and dist > 0:
                collisions.append(
                    {
                        "type": "name_collision",
                        "names": [a_raw, b_raw],
                        "distance": dist,
                        "severity": "LOW" if dist == 2 else "MEDIUM",
                    }
                )

    return sorted(collisions, key=lambda c: c["distance"])


def main():
    target = None
    output_json = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--target" and i + 1 < len(args):
            target = args[i + 1]
            i += 2
        elif args[i] == "--json":
            output_json = True
            i += 1
        else:
            i += 1

    root = find_project_root()
    if not root:
        print("Error: Could not find project root (no CLAUDE.md found).")
        sys.exit(1)

    registry_path = find_registry(root)
    if not registry_path:
        print("Error: skills-registry.json not found.")
        sys.exit(1)

    skills = load_skills_from_registry(registry_path)

    # Run all scans
    trigger_conflicts = scan_trigger_overlaps(skills, target)
    capability_conflicts = scan_agent_capability_overlaps(root, target)
    name_collisions = scan_name_collisions(skills, root, target)

    all_conflicts = trigger_conflicts + capability_conflicts + name_collisions

    if output_json:
        print(json.dumps(all_conflicts, indent=2))
        return

    # Human-readable output
    scope = f" for '{target}'" if target else ""
    print(f"# Conflict Scan Report{scope}")
    print(f"Found {len(all_conflicts)} issue(s)\n")

    if not all_conflicts:
        print("No conflicts detected.")
        return

    # Group by type
    for conflict_type, label in [
        ("trigger_overlap", "Trigger Overlaps"),
        ("capability_overlap", "Agent Capability Overlaps"),
        ("name_collision", "Name Collisions"),
    ]:
        typed = [c for c in all_conflicts if c["type"] == conflict_type]
        if not typed:
            continue
        print(f"## {label} ({len(typed)})\n")
        for c in typed:
            sev = c["severity"]
            if conflict_type == "trigger_overlap":
                print(
                    f"  [{sev}] \"{c['trigger']}\" -> {', '.join(c['skills'])}"
                    f"  (categories: {', '.join(c['categories'])})"
                )
            elif conflict_type == "capability_overlap":
                print(
                    f"  [{sev}] {c['agents'][0]} <-> {c['agents'][1]}"
                    f"  (Jaccard: {c['jaccard']}, shared: {', '.join(c['shared_capabilities'][:5])})"
                )
            elif conflict_type == "name_collision":
                print(
                    f"  [{sev}] {c['names'][0]} ~ {c['names'][1]}"
                    f"  (distance: {c['distance']})"
                )
        print()


if __name__ == "__main__":
    main()
