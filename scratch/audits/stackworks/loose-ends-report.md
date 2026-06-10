# Loose-ends report — letter-reverse-engineer skill upgrade

Generated: 2026-05-07 (SGT)

---

## Task 1: Schema bump in skeleton-contract.md — DONE

**What changed:**
- `proof_inventory.required` updated from `["named_outcomes", "numbers", "trust_chain_gaps"]` to include `"ai_pattern_flags"`
- New `ai_pattern_flags` array field added inside `proof_inventory.properties`, after `trust_chain_gaps`. Shape matches the spec exactly: items require `pattern`, `source_file` (enum: `overused-ai-patterns.md` | `anti-ai-patterns.md`), `quote`, `word_index`, `severity` (enum: `soft-flag` | `hard-flag`).
- Status line bumped from `v0.1 (draft)` to `v0.2 (draft)`.

**File:** `skills/letter-reverse-engineer/skeleton-contract.md`

**No surprises.** The schema was clean; the insertion point after `trust_chain_gaps` was unambiguous.

---

## Task 2: "Handoff to forward pipeline" section in SKILL.md — DONE

**What changed:**
- New section `## Handoff to the forward pipeline (sales-letter-method)` added immediately before `## Anti-patterns`.
- Covers: skill scope (audit only), forward pipeline location (`skills/sales-letter-method/`), what the forward pipeline owns, three example routing-table → pipeline-phase mappings, `/copy:sales-letter` slash command note, and instruction to start forward work in a separate session.
- Word count: ~170 words (under 200 limit).

**File:** `skills/letter-reverse-engineer/SKILL.md`

**No surprises.** Section placed correctly; Anti-patterns section preserved intact.

---

## Task 3: Global command path fix — NO CHANGE NEEDED

**What was found:**
- File: `~/.claude/commands/writing/references/anti-ai-patterns.md`
- Content: the full Wikipedia "Signs of AI writing" article (~55K tokens), embedded directly. This is the full content itself — not a slim wrapper that references the project file path.
- Per task instructions: full-content command files are left alone. There is no project path reference to update.

**No changes made.**

---

## Unresolved

None. All three tasks are closed.
