#!/usr/bin/env python3
"""
Registry Script - Registers a new skill or agent

Usage:
    register.py skill <name> --description <desc>
    register.py agent <name> --description <desc>

Examples:
    register.py skill seo-audit --description "Runs a technical SEO audit on a URL"
    register.py agent content-strategist --description "Plans content calendars"
"""

import sys
import json
from pathlib import Path


def find_registry():
    """Find skills-registry.json by walking up from this script's location."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        candidate = current / "skills-registry.json"
        if candidate.exists():
            return candidate
        current = current.parent
    return None


def register_skill(name, description):
    """Add a skill entry to skills-registry.json."""
    registry_path = find_registry()

    if not registry_path:
        print("Error: skills-registry.json not found.")
        print("Create it at the project root or run this from within the project.")
        return False

    # Validate the skill directory exists
    project_root = registry_path.parent
    skill_path = project_root / "skills" / name
    if not skill_path.exists():
        print(f"Error: Skill directory not found: {skill_path}")
        print("Create the skill first with init_skill.py, then register it.")
        return False

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: SKILL.md not found in {skill_path}")
        return False

    # Load existing registry
    try:
        registry = json.loads(registry_path.read_text())
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error reading registry: {e}")
        return False

    # Ensure skills array exists
    if "skills" not in registry:
        registry["skills"] = []

    # Check for duplicates
    for skill in registry["skills"]:
        if skill.get("id") == name:
            print(f"Error: Skill '{name}' is already registered.")
            return False

    # Detect references
    has_references = (skill_path / "references").exists() and any(
        (skill_path / "references").iterdir()
    )

    # Build entry
    entry = {
        "id": name,
        "name": " ".join(w.capitalize() for w in name.split("-")),
        "path": f"skills/{name}",
        "category": "TODO",
        "version": "1.0.0",
        "difficulty": "intermediate",
        "description": description,
        "triggers": ["TODO"],
        "prerequisites": [],
        "relatedSkills": [],
        "agents": [],
        "mcpIntegrations": [],
        "successMetrics": ["TODO"],
        "hasReferences": has_references,
    }

    registry["skills"].append(entry)

    try:
        registry_path.write_text(json.dumps(registry, indent=2) + "\n")
    except Exception as e:
        print(f"Error writing registry: {e}")
        return False

    print(f"Skill '{name}' registered in {registry_path}")
    print()
    print("Next steps:")
    print("1. Edit skills-registry.json to fill in TODO fields:")
    print("   - category, triggers, successMetrics")
    print("   - prerequisites, relatedSkills, agents")
    print("2. Set the correct difficulty level")

    return True


def register_agent(name, description):
    """Print instructions for adding an agent to the routing table."""
    # Validate the agent file exists somewhere reasonable
    project_root = Path(__file__).resolve().parent
    for _ in range(10):
        if (project_root / "CLAUDE.md").exists() or (
            project_root / "skills-registry.json"
        ).exists():
            break
        project_root = project_root.parent

    print(f"Agent '{name}' is ready for registration.")
    print()
    print("Add the following to your CLAUDE.md routing table:")
    print()
    print(f"### {' '.join(w.capitalize() for w in name.split('-'))}")
    print(f"- **Agent**: `{name}`")
    print(f"- **Description**: {description}")
    print(f"- **Triggers**: [TODO: Add trigger keywords]")
    print(f"- **Model**: [TODO: haiku/sonnet/opus]")
    print()
    print("Then add to any relevant skill's `agents` array in skills-registry.json.")

    return True


def main():
    if len(sys.argv) < 5 or sys.argv[3] != "--description":
        print("Usage: register.py <type> <name> --description <desc>")
        print()
        print("Types: skill, agent")
        print()
        print("Examples:")
        print(
            '  register.py skill seo-audit --description "Runs a technical SEO audit"'
        )
        print(
            '  register.py agent content-strategist --description "Plans content calendars"'
        )
        sys.exit(1)

    item_type = sys.argv[1]
    name = sys.argv[2]
    description = " ".join(sys.argv[4:])

    if item_type == "skill":
        success = register_skill(name, description)
    elif item_type == "agent":
        success = register_agent(name, description)
    else:
        print(f"Error: Unknown type '{item_type}'. Use 'skill' or 'agent'.")
        sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
