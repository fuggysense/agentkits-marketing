#!/usr/bin/env python3
"""
Skill Graph Linker — semantic [[wiki-link]] injection for skills + agents.

Scans skills/*/SKILL.md and agents/*.md, computes TF-IDF cosine similarity
between their descriptions + first-paragraph context, writes:

  1. .claude/skill-graph.json        — full adjacency map
  2. Injects `## Related` block in each SKILL.md / agent .md with top-N
     [[wiki-linked]] neighbours (idempotent — replaces existing block)

Usage:
  python3 scripts/link-skills.py                # refresh all
  python3 scripts/link-skills.py --skill copywriting   # only one
  python3 scripts/link-skills.py --dry-run      # report only, no writes
  python3 scripts/link-skills.py --top 5        # neighbours per node (default 5)
  python3 scripts/link-skills.py --min 0.12     # min cosine to count (default 0.12)

Requires: scikit-learn, pyyaml (optional — falls back to regex parse)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    sys.stderr.write("Install sklearn: pip3 install scikit-learn\n")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
AGENTS_DIR = ROOT / "agents"
OUT_JSON = ROOT / ".claude" / "skill-graph.json"

BLOCK_START = "<!-- skill-graph:start -->"
BLOCK_END = "<!-- skill-graph:end -->"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


@dataclass
class Node:
    kind: str          # "skill" | "agent"
    name: str
    path: Path
    text: str          # description + triggers + first ~500 words body

    @property
    def wikilink(self) -> str:
        return f"[[{self.name}]]"


def parse_frontmatter(raw: str) -> tuple[dict, str]:
    """Crude YAML frontmatter extractor — returns (meta, body)."""
    m = FRONTMATTER_RE.match(raw)
    if not m:
        return {}, raw
    fm, body = m.group(1), raw[m.end():]
    meta: dict = {}
    current_key = None
    for line in fm.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            meta.setdefault(current_key, []).append(line[4:].strip().strip('"\''))
            continue
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            current_key = k.strip()
            v = v.strip().strip('"\'')
            meta[current_key] = v if v else []
    return meta, body


def load_skill(skill_dir: Path) -> Node | None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None
    raw = skill_md.read_text(encoding="utf-8", errors="ignore")
    meta, body = parse_frontmatter(raw)
    name = (meta.get("name") or skill_dir.name).strip()
    desc = meta.get("description", "") or ""
    triggers = meta.get("triggers") or []
    if isinstance(triggers, list):
        trig_txt = " ".join(triggers)
    else:
        trig_txt = str(triggers)
    body_snippet = " ".join(body.split()[:400])
    text = f"{name}. {desc} {trig_txt} {body_snippet}".strip()
    return Node("skill", name, skill_md, text)


def load_agent(agent_md: Path) -> Node | None:
    if agent_md.name.startswith("_") or "-learnings" in agent_md.stem:
        return None
    raw = agent_md.read_text(encoding="utf-8", errors="ignore")
    meta, body = parse_frontmatter(raw)
    name = (meta.get("name") or agent_md.stem).strip()
    desc = meta.get("description", "") or ""
    body_snippet = " ".join(body.split()[:400])
    text = f"{name}. {desc} {body_snippet}".strip()
    return Node("agent", name, agent_md, text)


def collect_nodes() -> list[Node]:
    nodes: list[Node] = []
    if SKILLS_DIR.exists():
        for sub in sorted(SKILLS_DIR.iterdir()):
            if not sub.is_dir() or sub.name in {"common", "schemas"}:
                continue
            n = load_skill(sub)
            if n:
                nodes.append(n)
    if AGENTS_DIR.exists():
        for md in sorted(AGENTS_DIR.glob("*.md")):
            n = load_agent(md)
            if n:
                nodes.append(n)
    return nodes


def compute_graph(nodes: list[Node], top: int, min_sim: float) -> dict:
    if len(nodes) < 2:
        return {}
    vec = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_df=0.9,
        min_df=1,
        sublinear_tf=True,
    )
    matrix = vec.fit_transform([n.text for n in nodes])
    sim = cosine_similarity(matrix)
    graph: dict = {}
    for i, node in enumerate(nodes):
        scored = [
            (nodes[j].name, nodes[j].kind, float(sim[i][j]))
            for j in range(len(nodes)) if j != i and sim[i][j] >= min_sim
        ]
        scored.sort(key=lambda t: t[2], reverse=True)
        neighbours = scored[:top]
        graph[node.name] = {
            "kind": node.kind,
            "path": str(node.path.relative_to(ROOT)),
            "neighbours": [
                {"name": n, "kind": k, "score": round(s, 4)}
                for n, k, s in neighbours
            ],
        }
    return graph


def format_block(node: Node, neighbours: list[dict]) -> str:
    if not neighbours:
        return ""
    lines = [BLOCK_START, "", "## Related"]
    lines.append("<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->")
    lines.append("")
    for n in neighbours:
        tag = "skill" if n["kind"] == "skill" else "agent"
        lines.append(f"- [[{n['name']}]] ({tag}, {n['score']:.2f})")
    lines.append("")
    lines.append(BLOCK_END)
    return "\n".join(lines)


def inject_block(path: Path, block: str) -> bool:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    if BLOCK_START in raw and BLOCK_END in raw:
        new = re.sub(
            re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END),
            block,
            raw,
            flags=re.DOTALL,
        )
    else:
        sep = "\n\n" if not raw.endswith("\n") else "\n"
        new = raw.rstrip() + sep + "\n" + block + "\n"
    if new == raw:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", help="Only update this one skill/agent name")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--min", type=float, default=0.12)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    nodes = collect_nodes()
    print(f"[link-skills] loaded {len(nodes)} nodes "
          f"({sum(1 for n in nodes if n.kind=='skill')} skills, "
          f"{sum(1 for n in nodes if n.kind=='agent')} agents)")

    graph = compute_graph(nodes, args.top, args.min)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    if not args.dry_run:
        OUT_JSON.write_text(json.dumps(graph, indent=2), encoding="utf-8")
        print(f"[link-skills] wrote {OUT_JSON.relative_to(ROOT)}")

    target = args.skill
    writes = 0
    for node in nodes:
        if target and node.name != target:
            continue
        neighbours = graph.get(node.name, {}).get("neighbours", [])
        block = format_block(node, neighbours)
        if args.dry_run:
            print(f"\n--- {node.name} ({node.kind}) ---")
            print(block or "(no neighbours above threshold)")
            continue
        if block and inject_block(node.path, block):
            writes += 1
    if not args.dry_run:
        print(f"[link-skills] injected Related blocks in {writes} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
