#!/usr/bin/env python3
"""
Freshness Audit — Scan docs for staleness vs expected update frequency.

Usage:
    freshness_audit.py              # Full report
    freshness_audit.py --summary    # One-line summary
    freshness_audit.py --json       # JSON output
"""

import sys
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timedelta


def find_project_root():
    """Walk up from script location to find project root."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return None


# Update frequency map from documentation-management.md
# Maps document filename patterns to max days before considered stale
FREQUENCY_MAP = {
    # Strategic Documents
    "brand-guidelines.md": {"label": "Quarterly or brand refresh", "max_days": 100},
    "content-style-guide.md": {"label": "As needed", "max_days": 90},
    "channel-strategies.md": {"label": "Quarterly", "max_days": 100},
    # Operational Documents
    "campaign-playbooks.md": {"label": "After each campaign", "max_days": 90},
    "analytics-setup.md": {"label": "When tracking changes", "max_days": 90},
    "usage-guide.md": {"label": "With system updates", "max_days": 90},
    # Project Documents
    "project-overview-pdr.md": {"label": "Project changes", "max_days": 90},
    "project-roadmap.md": {"label": "Weekly", "max_days": 10},
}


def get_last_modified_git(file_path, root):
    """Get last modified date from git log."""
    try:
        result = subprocess.run(
            ["git", "log", "--format=%ai", "-1", "--", str(file_path)],
            capture_output=True, text=True, cwd=str(root), timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            date_str = result.stdout.strip().split(" ")[0]
            return datetime.strptime(date_str, "%Y-%m-%d")
    except (subprocess.TimeoutExpired, ValueError):
        pass
    return None


def get_last_modified_fs(file_path):
    """Fallback: get last modified date from filesystem."""
    try:
        mtime = file_path.stat().st_mtime
        return datetime.fromtimestamp(mtime)
    except OSError:
        return None


def audit(root):
    """Run freshness audit on docs/ directory."""
    docs_dir = root / "docs"
    if not docs_dir.exists():
        return []

    results = []
    now = datetime.now()

    for doc_file in sorted(docs_dir.glob("*.md")):
        filename = doc_file.name
        freq_info = FREQUENCY_MAP.get(filename)

        if not freq_info:
            # Unknown doc — use 90-day default
            freq_info = {"label": "Unknown (90d default)", "max_days": 90}

        # Try git first, fall back to filesystem
        last_modified = get_last_modified_git(doc_file, root)
        source = "git"
        if not last_modified:
            last_modified = get_last_modified_fs(doc_file)
            source = "fs"

        if not last_modified:
            results.append({
                "file": filename,
                "last_modified": "unknown",
                "expected_frequency": freq_info["label"],
                "days_overdue": -1,
                "status": "unknown",
            })
            continue

        age_days = (now - last_modified).days
        max_days = freq_info["max_days"]
        days_overdue = max(0, age_days - max_days)

        results.append({
            "file": filename,
            "last_modified": last_modified.strftime("%Y-%m-%d"),
            "last_modified_source": source,
            "expected_frequency": freq_info["label"],
            "max_days": max_days,
            "age_days": age_days,
            "days_overdue": days_overdue,
            "status": "overdue" if days_overdue > 0 else "fresh",
        })

    # Sort: most overdue first
    results.sort(key=lambda r: -r.get("days_overdue", -1))
    return results


def main():
    output_json = "--json" in sys.argv
    summary_mode = "--summary" in sys.argv

    root = find_project_root()
    if not root:
        print("Error: Could not find project root (no CLAUDE.md found).")
        sys.exit(1)

    results = audit(root)

    if output_json:
        print(json.dumps(results, indent=2))
        return

    overdue = [r for r in results if r["status"] == "overdue"]

    if summary_mode:
        if not overdue:
            print("Docs: All fresh.")
        else:
            items = [f"{r['file'].replace('.md','')} {r['days_overdue']}d" for r in overdue[:5]]
            print(f"Docs: {len(overdue)} overdue ({', '.join(items)})")
        return

    # Full report
    print("# Freshness Audit\n")
    if not results:
        print("No docs found in docs/")
        return

    print(f"| Document | Last Modified | Expected | Age | Status |")
    print(f"|----------|--------------|----------|-----|--------|")
    for r in results:
        status_icon = "OVERDUE" if r["status"] == "overdue" else "fresh"
        age = f"{r.get('age_days', '?')}d"
        print(f"| {r['file']} | {r['last_modified']} | {r['expected_frequency']} | {age} | {status_icon} |")

    print(f"\n**Summary:** {len(overdue)} overdue, {len(results) - len(overdue)} fresh")


if __name__ == "__main__":
    main()
