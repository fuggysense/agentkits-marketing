# skills-registry.json here is STALE — do not load it

`skills/skills-registry.json` is a 51-skill snapshot from 2026-03-14. The repo has ~132 skills now, so this copy is missing ~80 of them and points at 8 SKILL.md files that no longer exist (5 archived, 2 orphaned, 1 global false-positive).

**Canonical registry:** `.claude/rules/skills-registry.json` (132 skills). Load that one.

Kept on disk for git history and the drift tool's fallback search. The drift detector (`skills/knowledge-hygiene/scripts/registry_drift.py`) now reads `.claude/rules/` first. Marked during rebuild M3.7 / M4.3 (E-15).
