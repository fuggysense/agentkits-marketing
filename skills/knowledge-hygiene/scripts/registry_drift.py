#!/usr/bin/env python3
"""
Registry Drift Detection — Validate skills-registry.json vs actual SKILL.md files.

Usage:
    registry_drift.py              # Full report
    registry_drift.py --summary    # One-line summary
    registry_drift.py --json       # JSON output
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


def find_registry(root):
    """Find skills-registry.json."""
    for candidate in [
        root / "skills" / "skills-registry.json",
        root / ".claude" / "skills" / "skills-registry.json",
    ]:
        if candidate.exists():
            return candidate
    return None


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown file."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    fm = {}
    for line in match.group(1).split("\n"):
        kv = re.match(r"^(\w[\w-]*):\s*(.+)", line)
        if kv:
            key = kv.group(1).strip()
            val = kv.group(2).strip().strip('"').strip("'")
            fm[key] = val
    return fm


def extract_triggers_from_frontmatter(content):
    """Extract triggers list from YAML frontmatter."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return []

    triggers = []
    in_triggers = False
    for line in match.group(1).split("\n"):
        if re.match(r"^triggers:\s*$", line):
            in_triggers = True
            continue
        if in_triggers:
            trigger_match = re.match(r"^\s+-\s+(.+)", line)
            if trigger_match:
                triggers.append(trigger_match.group(1).strip())
            else:
                break
    return triggers


# Deprecated terms to flag (from MEMORY.md corrections)
DEPRECATED_TERMS = {
    "JARM": "Should use 'AI agent automation (email/WhatsApp)' instead",
}


def scan_drift(root):
    """Compare registry entries against actual SKILL.md files."""
    registry_path = find_registry(root)
    if not registry_path:
        return {"error": "skills-registry.json not found", "drifts": [], "missing_files": [], "deprecated": []}

    registry = json.loads(registry_path.read_text())
    skills = registry.get("skills", [])

    drifts = []
    missing_files = []
    deprecated_found = []

    for skill in skills:
        skill_id = skill.get("id", "")

        # Find actual SKILL.md
        skill_path = root / "skills" / skill_id / "SKILL.md"
        # Handle nested paths like document-skills/docx
        if not skill_path.exists() and "/" in skill_id:
            skill_path = root / "skills" / skill_id / "SKILL.md"

        if not skill_path.exists():
            missing_files.append(skill_id)
            continue

        content = skill_path.read_text()
        fm = parse_frontmatter(content)

        # Check version
        reg_version = skill.get("version", "")
        fm_version = fm.get("version", "")
        if reg_version and fm_version and reg_version != fm_version:
            drifts.append({
                "skill": skill_id,
                "field": "version",
                "registry_value": reg_version,
                "actual_value": fm_version,
            })

        # Check description (first 50 chars)
        reg_desc = skill.get("description", "")[:50]
        fm_desc = fm.get("description", "")[:50]
        if reg_desc and fm_desc and reg_desc != fm_desc:
            drifts.append({
                "skill": skill_id,
                "field": "description",
                "registry_value": reg_desc,
                "actual_value": fm_desc,
            })

        # Check for TODO triggers in registry
        reg_triggers = skill.get("triggers", [])
        if reg_triggers == ["TODO"]:
            drifts.append({
                "skill": skill_id,
                "field": "triggers",
                "registry_value": "['TODO']",
                "actual_value": "needs real triggers",
            })

        # Check for deprecated terms
        for term, reason in DEPRECATED_TERMS.items():
            if term in content:
                deprecated_found.append({
                    "skill": skill_id,
                    "term": term,
                    "reason": reason,
                })

    return {
        "drifts": drifts,
        "missing_files": missing_files,
        "deprecated": deprecated_found,
        "total_skills": len(skills),
    }


def main():
    output_json = "--json" in sys.argv
    summary_mode = "--summary" in sys.argv

    root = find_project_root()
    if not root:
        print("Error: Could not find project root (no CLAUDE.md found).")
        sys.exit(1)

    result = scan_drift(root)

    if "error" in result and not result["drifts"]:
        print(f"Error: {result['error']}")
        sys.exit(1)

    if output_json:
        print(json.dumps(result, indent=2))
        return

    total_issues = len(result["drifts"]) + len(result["missing_files"]) + len(result["deprecated"])

    if summary_mode:
        if total_issues == 0:
            print("Registry: Clean.")
        else:
            parts = []
            if result["drifts"]:
                parts.append(f"{len(result['drifts'])} field mismatches")
            if result["missing_files"]:
                parts.append(f"{len(result['missing_files'])} missing SKILL.md")
            if result["deprecated"]:
                parts.append(f"{len(result['deprecated'])} deprecated terms")
            print(f"Registry: {total_issues} issues ({', '.join(parts)})")
        return

    # Full report
    print("# Registry Drift Detection\n")
    print(f"Scanned {result['total_skills']} skills in registry.\n")

    if result["drifts"]:
        print("## Field Mismatches\n")
        print("| Skill | Field | Registry | Actual |")
        print("|-------|-------|----------|--------|")
        for d in result["drifts"]:
            print(f"| {d['skill']} | {d['field']} | {d['registry_value'][:40]} | {d['actual_value'][:40]} |")
        print()

    if result["missing_files"]:
        print("## Missing SKILL.md Files\n")
        for m in result["missing_files"]:
            print(f"  - {m}")
        print()

    if result["deprecated"]:
        print("## Deprecated Terms Found\n")
        for dep in result["deprecated"]:
            print(f"  - **{dep['skill']}**: uses '{dep['term']}' — {dep['reason']}")
        print()

    if total_issues == 0:
        print("No drift detected. Registry is clean.")

    print(f"\n**Summary:** {total_issues} total issues")


if __name__ == "__main__":
    main()
