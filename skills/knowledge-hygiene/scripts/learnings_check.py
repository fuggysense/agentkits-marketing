#!/usr/bin/env python3
"""
Learnings Integration Check — Compare learnings.md entries vs parent SKILL.md.

Usage:
    learnings_check.py              # Full report
    learnings_check.py --summary    # One-line summary
    learnings_check.py --json       # JSON output
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


def extract_confirmed_patterns(learnings_content):
    """Extract bullet items from '## Confirmed Patterns' section."""
    patterns = []
    in_section = False

    for line in learnings_content.split("\n"):
        if re.match(r"^##\s+Confirmed Patterns", line, re.IGNORECASE):
            in_section = True
            continue
        if in_section:
            if re.match(r"^##\s+", line):
                break
            match = re.match(r"^\s*[-*]\s+(.{10,})", line)
            if match:
                item = match.group(1).strip()
                # Skip placeholder items
                if not re.match(r"^\(.*\)$", item):
                    patterns.append(item)

    return patterns


def extract_keywords(text, min_len=5):
    """Extract significant keywords from text for matching."""
    # Remove markdown formatting
    text = re.sub(r"[`*_\[\]()]", " ", text)
    words = set()
    for word in text.lower().split():
        word = re.sub(r"[^a-z0-9-]", "", word)
        if len(word) >= min_len:
            words.add(word)
    return words


def check_integration(learnings_path, parent_path):
    """Check how many learnings patterns appear in the parent file."""
    learnings_content = learnings_path.read_text()
    parent_content = parent_path.read_text().lower()

    patterns = extract_confirmed_patterns(learnings_content)
    if not patterns:
        return {"total": 0, "unintegrated": 0, "samples": []}

    unintegrated = []
    for pattern in patterns:
        # Extract keywords from pattern and check if they appear in parent
        keywords = extract_keywords(pattern)
        if not keywords:
            continue
        # Consider integrated if >60% of keywords appear in parent
        matches = sum(1 for kw in keywords if kw in parent_content)
        ratio = matches / len(keywords) if keywords else 0
        if ratio < 0.6:
            unintegrated.append(pattern[:80])

    return {
        "total": len(patterns),
        "unintegrated": len(unintegrated),
        "samples": unintegrated[:3],
    }


def scan_all(root):
    """Scan all learnings files."""
    results = []

    # Skill learnings
    skills_dir = root / "skills"
    if skills_dir.exists():
        for learnings_path in sorted(skills_dir.glob("*/learnings.md")):
            skill_name = learnings_path.parent.name
            parent_path = learnings_path.parent / "SKILL.md"
            if not parent_path.exists():
                continue

            info = check_integration(learnings_path, parent_path)
            if info["total"] > 0:
                results.append({
                    "name": skill_name,
                    "type": "skill",
                    "total_learnings": info["total"],
                    "unintegrated_count": info["unintegrated"],
                    "sample_unintegrated": info["samples"],
                })

    # Agent learnings
    agents_dir = root / "agents"
    if agents_dir.exists():
        for learnings_path in sorted(agents_dir.glob("*-learnings.md")):
            agent_name = learnings_path.stem.replace("-learnings", "")
            agent_path = agents_dir / f"{agent_name}.md"
            if not agent_path.exists():
                continue

            info = check_integration(learnings_path, agent_path)
            if info["total"] > 0:
                results.append({
                    "name": agent_name,
                    "type": "agent",
                    "total_learnings": info["total"],
                    "unintegrated_count": info["unintegrated"],
                    "sample_unintegrated": info["samples"],
                })

    # Sort by unintegrated count descending
    results.sort(key=lambda r: -r["unintegrated_count"])
    return results


def main():
    output_json = "--json" in sys.argv
    summary_mode = "--summary" in sys.argv

    root = find_project_root()
    if not root:
        print("Error: Could not find project root (no CLAUDE.md found).")
        sys.exit(1)

    results = scan_all(root)

    if output_json:
        print(json.dumps(results, indent=2))
        return

    needs_attention = [r for r in results if r["unintegrated_count"] > 0]

    if summary_mode:
        if not needs_attention:
            print("Learnings: All integrated.")
        else:
            items = [f"{r['name']}: {r['unintegrated_count']}" for r in needs_attention[:5]]
            print(f"Learnings: {len(needs_attention)} with unintegrated entries ({', '.join(items)})")
        return

    # Full report
    print("# Learnings Integration Check\n")
    if not results:
        print("No learnings files with confirmed patterns found.")
        return

    print(f"| Name | Type | Total | Unintegrated | Sample |")
    print(f"|------|------|-------|-------------|--------|")
    for r in results:
        sample = r["sample_unintegrated"][0][:50] + "..." if r["sample_unintegrated"] else "—"
        status = f"**{r['unintegrated_count']}**" if r["unintegrated_count"] > 0 else "0"
        print(f"| {r['name']} | {r['type']} | {r['total_learnings']} | {status} | {sample} |")

    print(f"\n**Summary:** {len(needs_attention)} need attention, {len(results) - len(needs_attention)} clean")


if __name__ == "__main__":
    main()
