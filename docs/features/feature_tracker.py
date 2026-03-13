#!/usr/bin/env python3
"""
Feature Tracker Dashboard
Scans feature files and displays status overview.

Usage:
  python3 docs/features/feature_tracker.py              # Full dashboard
  python3 docs/features/feature_tracker.py --status shipped  # Filter by status
  python3 docs/features/feature_tracker.py --json        # JSON output
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

FEATURES_DIR = Path(__file__).resolve().parent


def parse_feature(filepath: Path) -> dict:
    """Extract frontmatter from a feature file."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return {}

    if not content.startswith("---"):
        return {}

    end = content.find("---", 3)
    if end == -1:
        return {}

    frontmatter = content[3:end].strip()
    result = {"file": filepath.name}

    for line in frontmatter.split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip().strip('"').strip("'")

    return result


def scan_features() -> list:
    """Scan all feature files."""
    features = []
    for f in sorted(FEATURES_DIR.glob("FEATURE-*.md")):
        feat = parse_feature(f)
        if feat:
            features.append(feat)
    return features


def display_dashboard(features: list, status_filter: str = None) -> None:
    """Print feature dashboard."""
    if status_filter:
        features = [f for f in features if f.get("status", "").lower() == status_filter.lower()]

    if not features:
        print("No features found." if not status_filter else f"No features with status '{status_filter}'")
        return

    # Status counts
    counts = {}
    for f in features:
        s = f.get("status", "unknown")
        counts[s] = counts.get(s, 0) + 1

    print("## Feature Tracker Dashboard\n")
    print("### Status Overview")
    status_order = ["idea", "feasible", "building", "testing", "shipped", "needs-fix", "parked", "retired"]
    status_icons = {
        "idea": "💡", "feasible": "✅", "building": "🔨", "testing": "🧪",
        "shipped": "🚀", "needs-fix": "🔧", "parked": "⏸️", "retired": "📦"
    }
    for s in status_order:
        if s in counts:
            print(f"  {status_icons.get(s, '•')} {s}: {counts[s]}")
    print()

    # Feature list
    print("### Features\n")
    print(f"| {'#':<5} | {'Name':<35} | {'Status':<12} | {'Shipped':<10} | {'Satisfaction':<13} | {'Usage':<10} |")
    print(f"|{'-'*6}:|{'-'*36}:|{'-'*13}:|{'-'*11}:|{'-'*14}:|{'-'*11}:|")

    for f in features:
        num = f.get("number", "?")
        name = f.get("name", "Unnamed")[:35]
        status = f.get("status", "?")
        shipped = f.get("shipped_date", "—")
        satisfaction = f.get("satisfaction", "—")
        usage = f.get("usage_frequency", "—")
        print(f"| {num:<5} | {name:<35} | {status:<12} | {shipped:<10} | {satisfaction:<13} | {usage:<10} |")

    print(f"\nTotal: {len(features)} features")


def main():
    features = scan_features()

    if "--json" in sys.argv:
        print(json.dumps(features, indent=2))
        return

    status_filter = None
    if "--status" in sys.argv:
        idx = sys.argv.index("--status")
        if idx + 1 < len(sys.argv):
            status_filter = sys.argv[idx + 1]

    display_dashboard(features, status_filter)


if __name__ == "__main__":
    main()
