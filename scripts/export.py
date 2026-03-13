#!/usr/bin/env python3
"""
Export tool for Agent Kit Marketing.

Usage:
    python3 scripts/export.py --system-only              # Framework only, no client/voice data
    python3 scripts/export.py --client 1up-sales-ai       # Client data + system (for client delivery)
    python3 scripts/export.py --client-data-only 1up-sales-ai  # Just the client folder as zip
    python3 scripts/export.py --list                      # List available clients

Options:
    --output DIR    Output directory (default: ./exports/)
    --format zip    Export format: zip or folder (default: zip)
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories that are part of the shared system
SYSTEM_DIRS = [
    "agents",
    "skills",
    ".claude",
    "context",
    "docs",
    "scripts",
    "voice",  # included in system export but without personal content
]

SYSTEM_FILES = [
    "CLAUDE.md",
    "README.md",
    "MEMORY.md",
]

# Directories/files to always exclude from exports
ALWAYS_EXCLUDE = [
    ".git",
    ".DS_Store",
    "__pycache__",
    "node_modules",
    "exports",  # don't export the exports folder
]

# Directories with sensitive/personal data - excluded from system-only export
PERSONAL_DIRS = [
    "clients",   # all client data
    "voice",     # personal voice profiles
]

# Files within client dirs to exclude when sharing with clients (internal only)
INTERNAL_ONLY_PATTERNS = [
    "*-learnings.md",
    "*-attribution.md",
    "learnings.md",
    "attribution.md",
]


def get_clients():
    """List available client projects."""
    clients_dir = REPO_ROOT / "clients"
    if not clients_dir.exists():
        return []
    return [
        d.name for d in clients_dir.iterdir()
        if d.is_dir() and d.name != "_template" and not d.name.startswith(".")
    ]


def should_exclude(path, exclude_patterns=None):
    """Check if a path should be excluded."""
    parts = Path(path).parts
    for exc in ALWAYS_EXCLUDE:
        if exc in parts:
            return True
    if exclude_patterns:
        name = Path(path).name
        for pattern in exclude_patterns:
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern:
                return True
    return False


def copy_tree(src, dst, exclude_patterns=None):
    """Copy directory tree with exclusions."""
    src = Path(src)
    dst = Path(dst)
    if not src.exists():
        return
    for item in src.rglob("*"):
        rel = item.relative_to(src)
        if should_exclude(rel, exclude_patterns):
            continue
        dest_path = dst / rel
        if item.is_dir():
            dest_path.mkdir(parents=True, exist_ok=True)
        else:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_path)


def export_system_only(output_dir, fmt="zip"):
    """Export framework without any client or personal data."""
    timestamp = datetime.now().strftime("%y%m%d")
    export_name = f"agentkit-marketing-system-{timestamp}"
    export_path = output_dir / export_name

    print(f"Exporting system framework to {export_path}...")

    # Copy system directories (skip personal ones)
    for d in SYSTEM_DIRS:
        if d in PERSONAL_DIRS:
            continue
        src = REPO_ROOT / d
        if src.exists():
            copy_tree(src, export_path / d)

    # Copy clients/_template/ only
    template_src = REPO_ROOT / "clients" / "_template"
    if template_src.exists():
        copy_tree(template_src, export_path / "clients" / "_template")

    # Copy voice README only (framework, not personal profiles)
    voice_readme = REPO_ROOT / "voice" / "README.md"
    if voice_readme.exists():
        (export_path / "voice").mkdir(parents=True, exist_ok=True)
        shutil.copy2(voice_readme, export_path / "voice" / "README.md")

    # Copy system files
    for f in SYSTEM_FILES:
        src = REPO_ROOT / f
        if src.exists():
            shutil.copy2(src, export_path / f)

    file_count = sum(1 for _ in export_path.rglob("*") if _.is_file())
    print(f"  {file_count} files copied")

    if fmt == "zip":
        zip_path = shutil.make_archive(str(export_path), "zip", output_dir, export_name)
        shutil.rmtree(export_path)
        print(f"  Zipped: {zip_path}")
        return zip_path
    return str(export_path)


def export_client(client_name, output_dir, fmt="zip", include_system=True):
    """Export a specific client's data, optionally with the system."""
    clients = get_clients()
    if client_name not in clients:
        print(f"Error: Client '{client_name}' not found. Available: {', '.join(clients)}")
        sys.exit(1)

    timestamp = datetime.now().strftime("%y%m%d")

    if include_system:
        export_name = f"agentkit-{client_name}-{timestamp}"
    else:
        export_name = f"{client_name}-data-{timestamp}"

    export_path = output_dir / export_name

    if include_system:
        print(f"Exporting system + client '{client_name}' to {export_path}...")
        # Copy full system first
        for d in SYSTEM_DIRS:
            if d == "clients":
                continue
            src = REPO_ROOT / d
            if src.exists():
                copy_tree(src, export_path / d)
        for f in SYSTEM_FILES:
            src = REPO_ROOT / f
            if src.exists():
                shutil.copy2(src, export_path / f)
        # Copy template
        template_src = REPO_ROOT / "clients" / "_template"
        if template_src.exists():
            copy_tree(template_src, export_path / "clients" / "_template")
    else:
        print(f"Exporting client data only for '{client_name}' to {export_path}...")

    # Copy the specific client folder
    client_src = REPO_ROOT / "clients" / client_name
    client_dst = export_path / "clients" / client_name if include_system else export_path
    copy_tree(client_src, client_dst)

    file_count = sum(1 for _ in export_path.rglob("*") if _.is_file())
    print(f"  {file_count} files copied")

    if fmt == "zip":
        zip_path = shutil.make_archive(str(export_path), "zip", output_dir, export_name)
        shutil.rmtree(export_path)
        print(f"  Zipped: {zip_path}")
        return zip_path
    return str(export_path)


def main():
    parser = argparse.ArgumentParser(description="Export Agent Kit Marketing components")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--system-only", action="store_true", help="Export framework only (no client data)")
    group.add_argument("--client", type=str, help="Export client data + system framework")
    group.add_argument("--client-data-only", type=str, help="Export only the client folder")
    group.add_argument("--list", action="store_true", help="List available clients")

    parser.add_argument("--output", type=str, default=None, help="Output directory")
    parser.add_argument("--format", choices=["zip", "folder"], default="zip", help="Export format")

    args = parser.parse_args()

    if args.list:
        clients = get_clients()
        if clients:
            print("Available clients:")
            for c in sorted(clients):
                client_path = REPO_ROOT / "clients" / c
                files = sum(1 for _ in client_path.rglob("*") if _.is_file())
                print(f"  {c} ({files} files)")
        else:
            print("No clients found.")
        return

    output_dir = Path(args.output) if args.output else REPO_ROOT / "exports"
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.system_only:
        result = export_system_only(output_dir, args.format)
    elif args.client:
        result = export_client(args.client, output_dir, args.format, include_system=True)
    elif args.client_data_only:
        result = export_client(args.client_data_only, output_dir, args.format, include_system=False)

    print(f"\nDone! Export at: {result}")


if __name__ == "__main__":
    main()
