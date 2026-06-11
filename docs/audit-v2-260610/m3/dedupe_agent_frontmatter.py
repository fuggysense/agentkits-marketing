#!/usr/bin/env python3
"""Dedupe duplicate entries inside YAML `agents:` frontmatter lists created by
the dead-agent repoint (multiple dead agents collapsed onto one survivor)."""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
changed = []
for base in ("skills", "commands"):
    for p in (ROOT / base).rglob("*.md"):
        if "_archive" in p.parts:
            continue
        lines = p.read_text(encoding="utf-8").split("\n")
        out, i, touched = [], 0, []
        while i < len(lines):
            if re.match(r"^agents:\s*$", lines[i]):
                out.append(lines[i]); i += 1
                seen, block = [], []
                while i < len(lines) and re.match(r"^\s*-\s+[\w-]+\s*$", lines[i]):
                    name = lines[i].strip()[2:].strip()
                    if name not in seen:
                        seen.append(name); out.append(lines[i])
                    else:
                        touched.append(name)
                    i += 1
                continue
            out.append(lines[i]); i += 1
        if touched:
            if "--apply" in sys.argv:
                p.write_text("\n".join(out), encoding="utf-8")
            changed.append((str(p.relative_to(ROOT)), touched))
mode = "APPLIED" if "--apply" in sys.argv else "DRY-RUN"
print(f"[{mode}] frontmatter dedupe — files: {len(changed)}")
for rel, t in changed:
    print(f"  {rel}: removed dup {t}")
