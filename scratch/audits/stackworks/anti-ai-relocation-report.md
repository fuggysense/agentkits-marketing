# Anti-AI Patterns Relocation Report

**Date:** 2026-05-07 (SGT)
**Operation:** Relocate `context/writing/anti-ai-patterns.md` → `skills/copy-editing/references/anti-ai-patterns.md`

---

## Step 1: Consumers found (before)

### Full-path references (`context/writing/anti-ai-patterns.md`)
| File | Line | Nature |
|------|------|--------|
| `scratch/audits/stackworks/unslop-vs-anti-ai-research.md` | 12, 70 | Historical audit notes (documenting pre-relocation state — descriptive, not load-time pointers) |
| `scratch/audits/stackworks/copy/stackworks-letter-plain-english-brief.md` | 39 | Active reference in self-audit section |

### Filename-only references (`anti-ai-patterns.md`)
None found outside the above files.

### Global skill file
`~/.claude/commands/writing/references/anti-ai-patterns.md` — 55K-token reference document; this IS the file (a copy), not a consumer of the project path. Out of scope.

---

## Step 2: Move

```
git mv context/writing/anti-ai-patterns.md skills/copy-editing/references/anti-ai-patterns.md
```
Git status confirms: `R  context/writing/anti-ai-patterns.md -> skills/copy-editing/references/anti-ai-patterns.md`

`context/writing/` retained (still contains `copywriting-frameworks.md`, `marketing-frameworks.md`).

---

## Step 3–7: Edits made

### `scratch/audits/stackworks/copy/stackworks-letter-plain-english-brief.md` (Step 3)
- Line 39: `context/writing/anti-ai-patterns.md` → `skills/copy-editing/references/anti-ai-patterns.md`

### `skills/unslop/SKILL.md` (Step 4)
- Line 46 (Layer 2 stack diagram): Updated to `copy-editing/references/{overused-ai-patterns,anti-ai-patterns}.md` with register labels
- Line 169 (consumer table): Added `anti-ai-patterns.md` alongside `overused-ai-patterns.md` for copy-editing Sweep 8
- Line 205–206 (References section): Added `anti-ai-patterns.md` entry with register label

### `skills/copy-editing/SKILL.md` (Step 5)
- Sweep 8 References block: Added `references/anti-ai-patterns.md` with register note
- Sweep 8 4-layer stack diagram: Layer 2 updated to `overused-ai-patterns + anti-ai-patterns`
- Sweep 8 Process step 1: Updated to load both files
- References section (bottom): Added `references/anti-ai-patterns.md` entry

### `skills/letter-reverse-engineer/SKILL.md` (Step 6)
- No changes needed. Step 14b confirmed clean — no overused-ai-patterns or anti-ai-patterns references exist. The task brief described "recently added Step 14b Anti-AI pass instructions" but these were not present in the file.

### `writing:references:anti-ai-patterns` skill (Step 7)
- Located at `~/.claude/commands/writing/references/anti-ai-patterns.md` — this is the 55K-token reference document itself (global command), not a pointer to the project file. No path references inside it to update. Scope: out of project.

---

## Step 8: Skill-graph refresh

`scripts/link-skills.py` requires `scikit-learn` (not installed). Script errored with: `Install sklearn: pip3 install scikit-learn`. Skipped per plan instructions.

---

## Step 9: Verification results

**Old path zero-hit check:** `context/writing/anti-ai-patterns` still appears in:
- `scratch/audits/stackworks/unslop-vs-anti-ai-research.md` (lines 12, 70) — kept intentionally. These are historical audit notes recording the pre-relocation orphan state. Updating them would corrupt the audit record.

**New file confirmed:** `skills/copy-editing/references/anti-ai-patterns.md` ✓

**Consumer wiring confirmed:**
- `skills/unslop/SKILL.md` — references new path in Layer 2 stack, consumer table, and References section ✓
- `skills/copy-editing/SKILL.md` — references new path in Sweep 8 block, Layer 2 diagram, Process step 1, and References section ✓
- `skills/letter-reverse-engineer/SKILL.md` — no wiring added (Step 14b had no anti-ai references to begin with) ✓
- Global `writing:references:anti-ai-patterns` command — out of scope (is the document, not a consumer) ✓

---

## Deviations from plan

1. **Step 6 (letter-reverse-engineer):** The brief described "recently added Step 14b Anti-AI pass instructions" referencing `overused-ai-patterns.md`. Actual file inspection found no such references in Step 14b — the section covers plain-English translation only. No edit was made.
2. **Step 7 (writing:references:anti-ai-patterns skill):** The skill is a global command at `~/.claude/commands/writing/references/anti-ai-patterns.md`. It IS the reference document (55K tokens), not a project-level pointer. No path to update.
3. **Historical audit file:** `unslop-vs-anti-ai-research.md` references the old path as historical description. Left unchanged to preserve audit integrity.

---

## Relocation clean?

Yes. The file has moved with git history preserved. All active load-time consumers (`copy-editing/SKILL.md`, `unslop/SKILL.md`) now point at the new location. The de-AI stack is wired. No orphans remain in the active skill layer.
