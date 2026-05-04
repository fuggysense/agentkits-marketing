# Skill Graph (Semantic Linking) — MANDATORY

Every `skills/<name>/SKILL.md` and `agents/<name>.md` carries an auto-managed `## Related` block of the top-5 semantically nearest skills/agents (TF-IDF cosine over frontmatter description + triggers + body). This is the graphify-style INFERRED edge layer on top of the explicit `[[wiki-links]]` humans write by hand.

**Source of truth:** `scripts/link-skills.py` — writes `.claude/skill-graph.json` + injects `<!-- skill-graph:start --> ... <!-- skill-graph:end -->` blocks.

## Rules

1. **On skill or agent creation** (human, skill-builder, skill-amplifier, or any agent that writes a new SKILL.md / agent .md): immediately run `python3 scripts/link-skills.py --skill <name>` as the final step. The new node must appear in the graph before the task is marked complete.

2. **On skill or agent edit** that changes the YAML `description` or `triggers`: re-run the same command. Body-only edits can skip.

3. **Weekly global refresh:** `/ops:weekly` runs `python3 scripts/link-skills.py` (no args) to rebuild the full graph and catch drift.

4. **Never hand-edit** the content between `<!-- skill-graph:start -->` and `<!-- skill-graph:end -->` — it will be overwritten on next run. Put manual curated wiki-links in a separate `## See also` section above the auto block.

5. **Routing priority:** when selecting related skills for a task, prefer explicit human-authored `[[wiki-links]]` over auto-generated ones. Auto-links are discovery aids, not rulings.

## Threshold tuning
Defaults: `--top 5 --min 0.12`. Raise `--min` for fewer, higher-confidence links; lower for broader graph. Don't edit defaults without logging the change in `docs/changelog.md`.
