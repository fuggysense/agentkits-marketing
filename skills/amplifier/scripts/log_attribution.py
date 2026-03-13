#!/usr/bin/env python3
"""
Attribution Logger — Tracks origin and inspiration for every amplification.

Usage:
    log_attribution.py <target-path> --source "..." --type "..." --summary "..."
    log_attribution.py <target-path> --source "..." --type "..." --summary "..." --date 260311

Target path examples:
    skills/copywriting        -> creates/appends skills/copywriting/attribution.md
    agents/copywriter.md      -> creates/appends agents/copywriter-attribution.md

Types: repo | person | article | campaign-result | internal-review | competitor-analysis
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime


VALID_TYPES = {
    "repo",
    "person",
    "article",
    "campaign-result",
    "internal-review",
    "competitor-analysis",
}

TEMPLATE = """# Attribution Log — {name}

> Tracks origin and inspiration for every amplification.

"""


def find_project_root():
    """Walk up to find project root."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return None


def get_today():
    """Get today's date in YYMMDD format using system date."""
    try:
        result = subprocess.run(
            ["date", "+%y%m%d"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip()
    except Exception:
        return datetime.now().strftime("%y%m%d")


def resolve_attribution_path(target_path_str, root):
    """Determine where the attribution.md file should go."""
    target = Path(target_path_str)

    # If it's a skill directory
    skill_dir = root / "skills" / target.name
    if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
        name = target.name
        return skill_dir / "attribution.md", name

    # If full path given
    if target.is_dir() and (target / "SKILL.md").exists():
        name = target.name
        return target / "attribution.md", name

    # If it's an agent file
    if "agents" in str(target):
        name = target.stem.replace("-attribution", "")
        return root / "agents" / f"{name}-attribution.md", name

    # Try as agent name
    agent_file = root / "agents" / f"{target.name}.md"
    if agent_file.exists():
        name = target.name
        return root / "agents" / f"{name}-attribution.md", name

    # Try as skill name
    if skill_dir.is_dir():
        return skill_dir / "attribution.md", target.name

    return None, None


def main():
    args = sys.argv[1:]

    if len(args) < 7:
        print("Usage: log_attribution.py <target-path> --source '...' --type '...' --summary '...' [--date YYMMDD]")
        print()
        print("Types: repo | person | article | campaign-result | internal-review | competitor-analysis")
        sys.exit(1)

    target_path = args[0]
    source = None
    attr_type = None
    summary = None
    date = None

    i = 1
    while i < len(args):
        if args[i] == "--source" and i + 1 < len(args):
            source = args[i + 1]
            i += 2
        elif args[i] == "--type" and i + 1 < len(args):
            attr_type = args[i + 1]
            i += 2
        elif args[i] == "--summary" and i + 1 < len(args):
            summary = args[i + 1]
            i += 2
        elif args[i] == "--date" and i + 1 < len(args):
            date = args[i + 1]
            i += 2
        else:
            i += 1

    if not all([source, attr_type, summary]):
        print("Error: --source, --type, and --summary are all required.")
        sys.exit(1)

    if attr_type not in VALID_TYPES:
        print(f"Error: Invalid type '{attr_type}'. Must be one of: {', '.join(sorted(VALID_TYPES))}")
        sys.exit(1)

    if not date:
        date = get_today()

    root = find_project_root()
    if not root:
        print("Error: Could not find project root.")
        sys.exit(1)

    attr_path, name = resolve_attribution_path(target_path, root)
    if not attr_path:
        print(f"Error: Could not resolve target '{target_path}'.")
        sys.exit(1)

    # Create or append
    if attr_path.exists():
        content = attr_path.read_text()
    else:
        content = TEMPLATE.format(name=name)

    # Append entry
    entry = f"""### {date} — Amplification
- **Source**: {source}
- **Type**: {attr_type}
- **Changes**: {summary}
- **Rationale**: Improvement identified during amplification workflow

"""
    content += entry
    attr_path.write_text(content)

    print(f"Attribution logged: {attr_path}")
    print(f"  Source: {source}")
    print(f"  Type: {attr_type}")


if __name__ == "__main__":
    main()
