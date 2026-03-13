#!/usr/bin/env python3
"""
Target Analyzer — Deep gap analysis for a single skill or agent.

Usage:
    analyze_target.py <path>         # e.g., skills/copywriting or agents/copywriter.md
    analyze_target.py <path> --json  # JSON output

Checks:
    - Section completeness vs canonical patterns
    - TODO placeholders
    - Empty sections
    - Version staleness
    - Learnings not integrated into main file
    - Registry drift (frontmatter vs skills-registry.json)
"""

import sys
import json
import re
from pathlib import Path


def find_project_root():
    """Walk up from script location to find project root."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return None


# Canonical sections for skills (from skill-patterns.md)
SKILL_SECTIONS = [
    "overview",
    "workflow",
    "commands",
    "resources",
]

SKILL_OPTIONAL = [
    "self-annealing",
    "integration",
    "quick start",
    "examples",
    "edge cases",
]

# Canonical sections for agents (from agent-patterns.md)
AGENT_SECTIONS = [
    "role",
    "capabilities",
    "skill integrations",
    "quality checklist",
    "model routing",
    "agent collaboration",
    "when not to use",
]

AGENT_OPTIONAL = [
    "examples",
    "edge cases",
    "self-annealing",
    "tools",
    "responsibilities",
    "reality check",
]


def detect_type(path):
    """Detect if path is a skill or agent."""
    path = Path(path)
    if path.is_dir():
        if (path / "SKILL.md").exists():
            return "skill", path / "SKILL.md"
    elif path.is_file() and path.suffix == ".md":
        # Could be an agent file
        if "agents" in str(path):
            return "agent", path
        if path.name == "SKILL.md":
            return "skill", path
    # Try as skill name
    root = find_project_root()
    if root:
        skill_path = root / "skills" / path.name / "SKILL.md"
        if skill_path.exists():
            return "skill", skill_path
        agent_path = root / "agents" / f"{path.name}.md"
        if agent_path.exists():
            return "agent", agent_path
    return None, None


def extract_sections(content):
    """Extract H2 section headers from markdown."""
    sections = []
    for line in content.split("\n"):
        match = re.match(r"^##\s+(.+)", line)
        if match:
            sections.append(match.group(1).strip().lower())
    return sections


def count_todos(content):
    """Count TODO placeholders."""
    todos = re.findall(r"\bTODO\b", content, re.IGNORECASE)
    tbd = re.findall(r"\bTBD\b", content, re.IGNORECASE)
    placeholders = re.findall(r"\[.*?placeholder.*?\]", content, re.IGNORECASE)
    return len(todos) + len(tbd) + len(placeholders)


def find_empty_sections(content):
    """Find sections with no content between headers."""
    empty = []
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if re.match(r"^##\s+", line):
            # Check if next non-empty line is another header or end of file
            has_content = False
            for j in range(i + 1, min(i + 10, len(lines))):
                stripped = lines[j].strip()
                if stripped and not re.match(r"^#", stripped):
                    has_content = True
                    break
                if re.match(r"^##?\s+", stripped):
                    break
            if not has_content:
                section_name = re.match(r"^##\s+(.+)", line).group(1)
                empty.append(section_name)
    return empty


def check_learnings_integration(target_path, target_type):
    """Check if learnings.md entries are reflected in the main file."""
    root = find_project_root()
    if not root:
        return 0, 0

    if target_type == "skill":
        skill_dir = target_path.parent
        learnings_path = skill_dir / "learnings.md"
    else:
        name = target_path.stem
        learnings_path = root / "agents" / f"{name}-learnings.md"

    if not learnings_path.exists():
        return 0, 0

    learnings_content = learnings_path.read_text()
    # Count non-empty bullet points in learnings
    learning_items = re.findall(r"^\s*[-*]\s+(.{10,})", learnings_content, re.MULTILINE)
    # Filter out placeholder items
    real_items = [
        item
        for item in learning_items
        if not re.match(r"^\(.*\)$", item.strip())
    ]

    return len(real_items), 0  # Can't easily verify integration without semantic analysis


def check_registry_drift(target_path, target_type):
    """Check if frontmatter matches skills-registry.json entry."""
    if target_type != "skill":
        return []

    root = find_project_root()
    if not root:
        return []

    registry_path = root / ".claude" / "skills" / "skills-registry.json"
    if not registry_path.exists():
        return ["Registry file not found"]

    content = target_path.read_text()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return ["No frontmatter in SKILL.md"]

    # Extract name from frontmatter
    name_match = re.search(r"^name:\s*(.+)", match.group(1), re.MULTILINE)
    if not name_match:
        return ["No name in frontmatter"]

    skill_name = name_match.group(1).strip()

    # Find in registry
    registry = json.loads(registry_path.read_text())
    registry_entry = None
    for skill in registry.get("skills", []):
        if skill.get("id") == skill_name:
            registry_entry = skill
            break

    if not registry_entry:
        return [f"Skill '{skill_name}' not found in skills-registry.json"]

    drifts = []
    # Check description match
    desc_match = re.search(r"^description:\s*(.+?)(?:\n[a-z]|\n---)", match.group(1), re.DOTALL)
    if desc_match:
        fm_desc = desc_match.group(1).strip()[:50]
        reg_desc = registry_entry.get("description", "")[:50]
        if fm_desc != reg_desc:
            drifts.append("Description differs between frontmatter and registry")

    # Check if triggers are just TODO
    if registry_entry.get("triggers") == ["TODO"]:
        drifts.append("Registry triggers still set to TODO")

    return drifts


def analyze(target_path_str):
    """Run full analysis on a target."""
    target_type, target_path = detect_type(Path(target_path_str))

    if not target_type or not target_path or not target_path.exists():
        return {"error": f"Could not find target: {target_path_str}"}

    content = target_path.read_text()
    sections = extract_sections(content)

    # Determine canonical sections
    if target_type == "skill":
        required = SKILL_SECTIONS
        optional = SKILL_OPTIONAL
    else:
        required = AGENT_SECTIONS
        optional = AGENT_OPTIONAL

    # Check completeness
    present_required = [s for s in required if any(s in sec for sec in sections)]
    missing_required = [s for s in required if not any(s in sec for sec in sections)]
    present_optional = [s for s in optional if any(s in sec for sec in sections)]

    completeness = len(present_required) / len(required) if required else 1.0

    # Other checks
    todo_count = count_todos(content)
    empty = find_empty_sections(content)
    learning_count, _ = check_learnings_integration(target_path, target_type)
    drifts = check_registry_drift(target_path, target_type)

    # Extract version
    version_match = re.search(r"version:\s*[\"']?(\d+\.\d+\.\d+)", content)
    version = version_match.group(1) if version_match else "not set"

    name = target_path.parent.name if target_type == "skill" else target_path.stem

    return {
        "name": name,
        "type": target_type,
        "path": str(target_path),
        "completeness": round(completeness, 2),
        "completeness_score": f"{len(present_required)}/{len(required)}",
        "version": version,
        "sections_present": present_required,
        "sections_missing": missing_required,
        "optional_present": present_optional,
        "todo_count": todo_count,
        "empty_sections": empty,
        "learnings_count": learning_count,
        "registry_drifts": drifts,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_target.py <path> [--json]")
        print()
        print("Examples:")
        print("  analyze_target.py skills/copywriting")
        print("  analyze_target.py agents/copywriter.md")
        sys.exit(1)

    target = sys.argv[1]
    output_json = "--json" in sys.argv

    result = analyze(target)

    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)

    if output_json:
        print(json.dumps(result, indent=2))
        return

    # Human-readable report
    score_pct = int(result["completeness"] * 100)
    print(f"# Analysis: {result['name']} ({result['type']})")
    print(f"**Path:** {result['path']}")
    print(f"**Version:** {result['version']}")
    print(f"**Completeness:** {score_pct}% ({result['completeness_score']} required sections)")
    print()

    if result["sections_present"]:
        print("## Present Sections (Required)")
        for s in result["sections_present"]:
            print(f"  + {s}")
        print()

    if result["sections_missing"]:
        print("## Missing Sections (Required)")
        for s in result["sections_missing"]:
            print(f"  - {s}")
        print()

    if result["optional_present"]:
        print("## Optional Sections Present")
        for s in result["optional_present"]:
            print(f"  ~ {s}")
        print()

    issues = []
    if result["todo_count"] > 0:
        issues.append(f"  ! {result['todo_count']} TODO/TBD placeholder(s)")
    if result["empty_sections"]:
        issues.append(f"  ! Empty sections: {', '.join(result['empty_sections'])}")
    if result["learnings_count"] > 0:
        issues.append(f"  ! {result['learnings_count']} learnings entries to review for integration")
    if result["registry_drifts"]:
        for d in result["registry_drifts"]:
            issues.append(f"  ! Registry: {d}")

    if issues:
        print("## Issues")
        for issue in issues:
            print(issue)
        print()


if __name__ == "__main__":
    main()
