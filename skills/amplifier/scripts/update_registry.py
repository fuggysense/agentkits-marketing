#!/usr/bin/env python3
"""
Registry Updater — Syncs a skill's frontmatter with its skills-registry.json entry.

Unlike register.py (which creates new entries), this updates existing entries
after a skill has been amplified.

Usage:
    update_registry.py <skill-name>

Syncs: description, version, hasReferences
Validates: no duplicate triggers introduced
"""

import sys
import json
import re
from pathlib import Path


def find_project_root():
    """Walk up to find project root."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return None


def parse_frontmatter(skill_md_path):
    """Extract frontmatter fields from SKILL.md."""
    content = skill_md_path.read_text()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    fm_text = match.group(1)
    result = {}

    # Extract name
    m = re.search(r"^name:\s*(.+)", fm_text, re.MULTILINE)
    if m:
        result["name"] = m.group(1).strip()

    # Extract description (may be multi-line)
    m = re.search(r"^description:\s*(.+?)(?=\n[a-z]|\Z)", fm_text, re.MULTILINE | re.DOTALL)
    if m:
        result["description"] = " ".join(m.group(1).strip().split())

    # Extract version
    m = re.search(r"^version:\s*[\"']?(\d+\.\d+\.\d+)", fm_text, re.MULTILINE)
    if m:
        result["version"] = m.group(1)

    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: update_registry.py <skill-name>")
        print()
        print("Example:")
        print("  update_registry.py copywriting")
        sys.exit(1)

    skill_name = sys.argv[1]

    root = find_project_root()
    if not root:
        print("Error: Could not find project root.")
        sys.exit(1)

    # Find skill
    skill_dir = root / "skills" / skill_name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: Skill not found at {skill_dir}")
        sys.exit(1)

    # Parse frontmatter
    fm = parse_frontmatter(skill_md)
    if not fm:
        print("Error: Could not parse frontmatter from SKILL.md")
        sys.exit(1)

    # Load registry
    registry_path = root / ".claude" / "skills" / "skills-registry.json"
    if not registry_path.exists():
        print("Error: skills-registry.json not found.")
        sys.exit(1)

    registry = json.loads(registry_path.read_text())

    # Find entry
    entry_idx = None
    for i, skill in enumerate(registry.get("skills", [])):
        if skill.get("id") == skill_name:
            entry_idx = i
            break

    if entry_idx is None:
        print(f"Error: Skill '{skill_name}' not found in registry.")
        print("Use meta-builder's register.py to create a new entry first.")
        sys.exit(1)

    entry = registry["skills"][entry_idx]
    changes = []

    # Sync description
    if "description" in fm and fm["description"] != entry.get("description"):
        entry["description"] = fm["description"]
        changes.append("description")

    # Sync version
    if "version" in fm and fm["version"] != entry.get("version"):
        entry["version"] = fm["version"]
        changes.append("version")

    # Sync hasReferences
    has_refs = (skill_dir / "references").exists() and any(
        (skill_dir / "references").iterdir()
    )
    if has_refs != entry.get("hasReferences"):
        entry["hasReferences"] = has_refs
        changes.append("hasReferences")

    # Check for duplicate triggers across all skills
    my_triggers = set(t.lower() for t in entry.get("triggers", []))
    for other in registry.get("skills", []):
        if other.get("id") == skill_name:
            continue
        other_triggers = set(t.lower() for t in other.get("triggers", []))
        dupes = my_triggers & other_triggers
        if dupes:
            print(f"Warning: Shared triggers with '{other['id']}': {', '.join(dupes)}")

    if not changes:
        print(f"No changes needed for '{skill_name}' — registry is in sync.")
        return

    # Write back
    registry["skills"][entry_idx] = entry
    registry_path.write_text(json.dumps(registry, indent=2) + "\n")

    print(f"Updated '{skill_name}' in registry: {', '.join(changes)}")


if __name__ == "__main__":
    main()
