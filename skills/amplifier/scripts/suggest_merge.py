#!/usr/bin/env python3
"""
Merge Suggester — Identifies tightly coupled artifact pairs and recommends merges.

Uses similarity scores + dependency graph analysis.

Usage:
    suggest_merge.py                    # Default threshold 2
    suggest_merge.py --threshold 1      # More aggressive suggestions
    suggest_merge.py --json             # JSON output

Scoring:
    +1  Same category
    +1  Share >50% triggers
    +1  One is a subset of the other (all triggers of A appear in B)
    -1  Different difficulty levels
    -1  Both have >20 lines of unique content

    Score > 2 = Recommend merge
    Score 1-2 = Review manually
    Score < 1 = Keep separate
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


def load_registry(root):
    """Load skills registry."""
    registry_path = root / ".claude" / "skills" / "skills-registry.json"
    if not registry_path.exists():
        return {}
    return json.loads(registry_path.read_text())


def load_dependency_graph(registry):
    """Extract dependency graph from registry."""
    return registry.get("dependencyGraph", {})


def check_circular_deps(dep_graph):
    """Find circular dependencies."""
    circular = []
    for skill, deps in dep_graph.items():
        for dep in deps:
            if dep in dep_graph and skill in dep_graph[dep]:
                pair = tuple(sorted([skill, dep]))
                if pair not in circular:
                    circular.append(pair)
    return circular


def compute_trigger_overlap(skills_a, skills_b):
    """Compute trigger overlap ratio."""
    triggers_a = set(t.lower() for t in skills_a.get("triggers", []))
    triggers_b = set(t.lower() for t in skills_b.get("triggers", []))
    if not triggers_a or not triggers_b:
        return 0.0, False
    shared = triggers_a & triggers_b
    overlap = len(shared) / min(len(triggers_a), len(triggers_b))
    is_subset = triggers_a.issubset(triggers_b) or triggers_b.issubset(triggers_a)
    return overlap, is_subset


def count_unique_lines(root, skill_id):
    """Count non-boilerplate lines in a skill's SKILL.md."""
    skill_md = root / "skills" / skill_id / "SKILL.md"
    if not skill_md.exists():
        # Try nested path like document-skills/docx
        skill_md = root / "skills" / skill_id / "SKILL.md"
        if not skill_md.exists():
            return 0
    content = skill_md.read_text()
    # Remove frontmatter
    parts = content.split("---", 2)
    if len(parts) >= 3:
        body = parts[2]
    else:
        body = content
    lines = [l for l in body.strip().split("\n") if l.strip() and not l.startswith("#")]
    return len(lines)


def score_pair(skill_a, skill_b, data_a, data_b, root, dep_graph):
    """Score a pair for merge recommendation."""
    score = 0
    reasons = []

    # Same category
    if data_a.get("category") == data_b.get("category"):
        score += 1
        reasons.append(f"Same category: {data_a.get('category')}")

    # Trigger overlap
    overlap, is_subset = compute_trigger_overlap(data_a, data_b)
    if overlap > 0.5:
        score += 1
        reasons.append(f"Share {overlap:.0%} triggers")
    if is_subset:
        score += 1
        reasons.append("One is a trigger subset of the other")

    # Circular dependency
    if (skill_a in dep_graph.get(skill_b, []) and
            skill_b in dep_graph.get(skill_a, [])):
        score += 1
        reasons.append("Circular dependency detected")

    # Different difficulty = keep separate
    if data_a.get("difficulty") != data_b.get("difficulty"):
        score -= 1
        reasons.append(f"Different difficulty: {data_a.get('difficulty')} vs {data_b.get('difficulty')}")

    # Both have substantial unique content = keep separate
    lines_a = count_unique_lines(root, skill_a)
    lines_b = count_unique_lines(root, skill_b)
    if lines_a > 20 and lines_b > 20:
        score -= 1
        reasons.append(f"Both have substantial content ({lines_a} + {lines_b} lines)")

    return score, reasons


def main():
    threshold = 2
    output_json = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--threshold" and i + 1 < len(args):
            threshold = int(args[i + 1])
            i += 2
        elif args[i] == "--json":
            output_json = True
            i += 1
        else:
            i += 1

    root = find_project_root()
    if not root:
        print("Error: Could not find project root.")
        sys.exit(1)

    registry = load_registry(root)
    dep_graph = load_dependency_graph(registry)
    skills = {s["id"]: s for s in registry.get("skills", [])}

    # Score all pairs
    results = []
    skill_ids = list(skills.keys())
    for i in range(len(skill_ids)):
        for j in range(i + 1, len(skill_ids)):
            a, b = skill_ids[i], skill_ids[j]
            score, reasons = score_pair(a, b, skills[a], skills[b], root, dep_graph)
            if score >= 1:  # Only show scores >= 1
                if score > threshold:
                    recommendation = "MERGE"
                elif score >= threshold:
                    recommendation = "REVIEW"
                else:
                    recommendation = "KEEP SEPARATE"
                results.append({
                    "pair": [a, b],
                    "score": score,
                    "recommendation": recommendation,
                    "reasons": reasons,
                })

    results.sort(key=lambda r: -r["score"])

    if output_json:
        print(json.dumps(results, indent=2))
        return

    # Human-readable
    print(f"# Merge Suggestions (threshold: {threshold})")
    print(f"Analyzed {len(skill_ids)} skills, found {len(results)} candidate pair(s)\n")

    # Circular deps
    circular = check_circular_deps(dep_graph)
    if circular:
        print("## Circular Dependencies")
        for a, b in circular:
            print(f"  ! {a} <-> {b}")
        print()

    if not results:
        print("No merge candidates found.")
        return

    for r in results:
        print(f"  [{r['recommendation']}] (score: {r['score']}) {r['pair'][0]} + {r['pair'][1]}")
        for reason in r["reasons"]:
            print(f"    - {reason}")
        print()


if __name__ == "__main__":
    main()
