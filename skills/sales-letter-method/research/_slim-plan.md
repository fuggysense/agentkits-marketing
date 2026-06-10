# Slim Plan — Phase 1a
Generated: 2026-05-27. Audit only — no edits applied yet. Jerel reviews before any edits run.

---

## SKILL.md Section-by-Section Verdict

| Section | Lines | Bytes (est) | Classification | Action |
|---|---|---|---|---|
| Frontmatter (YAML) | 1–50 | ~1.6K | L0-ESSENTIAL | Keep. Trim `related_skills` list from 10 → 5 most-used. Move `success_metrics` to `references/_metrics.md` (rarely consulted at routing time). |
| Graph Links block | 52–58 | ~0.9K | DEAD/REDUNDANT (Obsidian-only) | Cut. Wikilinks `[[…]]` don't render or route in Claude Code. Auto-generated `## Related` at L292/296 already covers cross-skill pointers. |
| Title + 1-line intent | 60–66 | ~0.5K | L0-ESSENTIAL | Keep. Already passes Q1 + Q2. |
| "When to use this skill" | 68–95 | ~2.1K | PARTIAL | Keep the `YES:` / `NO:` 8-line core (L70–74, 86–95). MIGRATE the 5-vertical guidance (L76–84) to `references/component-matrix.md` § Industry Tweaks (already exists). MIGRATE the "preferred invocation" + "ship as coded landing page" footnotes to `references/_invocation.md`. |
| 12-Component Framework + 5 Cross-Cutting | 98–124 | ~3.4K | MIGRATE-TO-REFERENCES | Heavy duplication with `references/component-matrix.md` Evaluation Matrix AND `prompt-template.md` lines 59–82. Reduce to a 5-line summary in SKILL.md: "12 components, 5 cross-cutting requirements. Full matrix → `references/component-matrix.md`. Default sequence → `references/_default-sequence.md`." Move L111–124 default sequence into a new `references/_default-sequence.md`. |
| 5-Phase Pipeline header | 126 | — | L0-ESSENTIAL | Keep as one-liner. |
| Phase 0 — Context Scan | 128–130 | ~0.4K | L0-ESSENTIAL | Keep (3 lines). |
| Phase 0.5 — Claim Audit | 131–143 | ~1.6K | MIGRATE-TO-REFERENCES | Move to new `references/phase-0-5-claim-audit.md`. Replace in SKILL.md with: "Phase 0.5 — Claim Audit. Produces 3-bucket inventory (CAN / CANNOT / CAREFUL). Mandatory for regulated verticals. Full playbook → `references/phase-0-5-claim-audit.md`." (3 lines). |
| Phase 0.7 — Mechanism + Offer Architecture | 145–171 | ~3.3K | DEAD/REDUNDANT in SKILL.md | `references/mechanism-architecture.md` is the playbook (14K bytes, headed "Phase 0.7 playbook"). SKILL.md is repeating the playbook's table of contents (A/B/C/D/E sub-steps). Cut to 2 lines: "Phase 0.7 — Mechanism + Offer Architecture (HITL gate). Required Phase 1 input. Full playbook → `references/mechanism-architecture.md`." |
| Phase 1 — Parallel Drafting | 172–178 | ~1.0K | L0-ESSENTIAL (trim) | Keep the parallel-drafting structure (Hook Half / Commit Half) — this is routing info every runner needs. Cut the L178 model TODO ("migrate to opus-4-7 by 2026-06-15") to a `corrections.md` / `learnings.md` entry — TODO comments rot in L0. |
| Phase 2 — Stitcher | 180–183 | ~0.7K | L0-ESSENTIAL (trim) | Keep one line. MIGRATE the cohesion-check detail to its existing `references/cohesion-check.md` (the pointer already exists). |
| Phase 3 — Conversion Gate | 185–201 | ~3.2K | MIGRATE-TO-REFERENCES | The 5-reviewer roster + precedence order + contract validation belongs in `references/phase-3-reviewer-stack.md`. SKILL.md keeps a 4-line summary: "Phase 3 — 5 parallel reviewers + synthesizer (mandatory). Roster + precedence + ship-block rules → `references/phase-3-reviewer-stack.md`." |
| Phase 4 — Polish + Pre-Ship Gate | 202–232 | ~3.0K | MIGRATE-TO-REFERENCES | Move pre-ship-reviewer + coherence-reviewer detail to `references/phase-4-preship.md`. SKILL.md keeps: "Phase 4 — Polish + pre-ship structural audit. FAIL on any lens = ship-block. Full spec → `references/phase-4-preship.md`." |
| Required Inputs | 233–246 | ~1.0K | L0-ESSENTIAL | Keep. This is routing-critical — every runner needs to know the 3 required client files upfront. Already passes Q1 + Q2. |
| Key References (load on demand) | 247–267 | ~1.7K | L0-ESSENTIAL | Keep, but **convert to the `_index.md` pattern** — fold this list INTO a new `references/_index.md` (the L4 router) and replace the section in SKILL.md with: "All on-demand references catalogued in `references/_index.md`." |
| Critical Rules | 268–279 | ~1.1K | MIGRATE-TO-BEST-PRACTICES | These are BP-claim shaped ("X is the primary lever," "fake scarcity destroys trust"). Each rule becomes a 1-line entry in a new `best-practices/_critical-rules.md` — or split across multiple BP files. Keep a 3-line "Hard rules" stub in SKILL.md pointing to it. |
| Common Failure Modes | 280–291 | ~1.0K | MIGRATE-TO-BEST-PRACTICES | Same shape as Critical Rules. Move to `best-practices/_failure-modes.md`. |
| Related (auto-generated) x2 | 292–301 | ~0.5K | DEAD/REDUNDANT | Two duplicate `## Related` headers (L292 and L296) — confirmed bug. Keep one auto-generated block. |

**Duplication found (cut candidates):**
1. **`## Related` appears twice** (L292 + L296) — pure bug.
2. **12-component default sequence (L111–124)** duplicates `references/component-matrix.md` Evaluation Matrix AND `prompt-template.md` lines 59–82 COMPONENT INCLUSION CHECKLIST. Three sources of truth for the same list.
3. **Phase 0.7 sub-steps A/B/C/D/E (L150–166)** duplicate `references/mechanism-architecture.md`'s table of contents — 3.3K of pure echo.
4. **Cross-cutting requirements (L104–109)** duplicate `prompt-template.md` lines 50–55.

**Contradiction flagged:**
- SKILL.md L178 says "Model: claude-opus-4-6 ... TODO: migrate to claude-opus-4-7 by 2026-06-15." Today is 2026-05-27. Within the migration window but reads as stale. Decide on a model-source-of-truth (skill frontmatter? `references/_models.md`?) before the deadline.

---

## SKILL.md Slim Target

- **Current:** 301 lines / 24,361 bytes
- **Target:** ~95–115 lines / ~8–10K bytes
- **Reduction:** ~60% byte cut, ~65% line cut
- **What survives in L0:** frontmatter (trimmed) + 1-line intent + When-to-use (YES/NO core only) + 5-Phase pipeline (≤4 lines per phase, pointer to L4 playbook) + Required Inputs + 3-line pointer to `references/_index.md` + 3-line pointer to `best-practices/_index.md` + one auto-generated Related block.

**Self-audit against the writing-standard:**
- **Q1 (complete argument):** A fresh agent reading slimmed SKILL.md alone must understand (a) what this skill ships, (b) when to use it, (c) what client files are required, (d) the 5 phases in sequence, (e) where to fetch the detailed playbook for each phase. The current outline above covers all 5.
- **Q2 (Singapore 3rd-grade English):** "Phase 0.7 — Mechanism + Offer Architecture (HITL gate). Required Phase 1 input. Full playbook → `references/mechanism-architecture.md`." passes. "Five-emotional-states sequence companion to scene picker" does NOT pass — that phrasing lives in the playbook, not in L0.

---

## prompt-template.md Verdict

- **Classification:** **KEEP AS-IS at root, with one trim pass.** Not a candidate for migration to `references/` or splitting per letter type.
- **Reasoning:**
  - It is a single reusable copy-paste master prompt (the file says so on line 3: "Copy-paste-ready master prompt"). It is loaded **only once per draft run**, not at routing time, so it is NOT an L0 cost. Different file lifecycle from SKILL.md.
  - It is used by humans (paste into ChatGPT/Gemini/Cursor) AND by the `/content:sales-letter` slash command. Single-source-of-truth for the drafter persona.
  - Splitting per vertical (info-product / agency / coaching) would multiply files without reducing per-run load, and verticals already differ via `{{placeholders}}` + `references/component-matrix.md` Industry Tweaks — splitting would re-introduce duplication.
  - Moving to `references/` would orphan it from the `/content:sales-letter` slash command which currently expects it at skill root.
- **Trim pass (proposed, ~3–4K byte cut):**
  - Lines 50–55 (CROSS-CUTTING REQUIREMENTS) — already in SKILL.md and `references/`. Replace with: "See `references/cross-cutting.md` (or inline summary)."
  - Lines 113–350 COMPONENT SPECIFICATIONS — currently restates what `references/component-matrix.md` already owns. Two options: (a) cut entirely and have the prompt say "Follow `references/component-matrix.md` per component" or (b) keep — the master prompt benefits from being self-contained when pasted into ChatGPT/Gemini where references don't auto-resolve.
  - **Recommendation:** keep (b) — self-containment is the whole point of a copy-paste prompt. Trim only the 50–55 cross-cutting echo and the L389–415 FAILURE CONDITIONS / TONE TARGETS if those are duplicated in reviewers.
- **Proposed action:** Defer prompt-template.md trimming to a separate Phase 1b after SKILL.md slim lands. Don't touch in Phase 1a.

---

## best-practices/_index.md Skeleton

**Proposed format:** markdown table with structured frontmatter — agents fetch this file first, then load only the BP files matching their reviewer role.

**Fields per entry (5 columns):**
1. `file` — path relative to `best-practices/` (e.g. `ps-architecture.md`)
2. `claim` — one-sentence BP claim (Q2-passing)
3. `load_when` — trigger phrase (matches the L4 references pattern)
4. `applies_to` — which component(s) or pipeline phase the BP governs (e.g. `12-ps-block`, `5-phase-pipeline`, `all`)
5. `reviewer-fit` — which Phase 3 reviewer most uses it (`buyer-lens`, `copy-chief`, `self-contained`, `eval-halbert`, `eval-sales-letter`, or `all`)

**Where `_writing-standard.md` sits:** **Header note above the table**, not a row. It is meta — it governs how every BP and reference is written, including the index itself. Treating it as one row among many buries it.

**Proposed shape (Markdown, ~40 lines once Wave 1 retrofits land):**

```markdown
---
file_type: best-practices-index
load_when: any agent is about to draft, review, or retrofit a sales-letter best-practice file; any Phase 3 reviewer is starting a pass
last_updated: 2026-05-27
---

# Best Practices — Index

> **Read first:** [_writing-standard.md](_writing-standard.md) — the two-question lens (Q1 complete argument + Q2 Singapore 3rd-grade English). Every BP file below has been written against it. Every output you produce must pass it.

## How to use this index

1. Identify your role (which Phase 3 reviewer, or which component you are drafting).
2. Scan the `reviewer-fit` and `applies_to` columns.
3. Load ONLY the BP files that match. Do not load the whole folder.

## Catalogue

| file | claim | load_when | applies_to | reviewer-fit |
|---|---|---|---|---|
| [ps-architecture.md](ps-architecture.md) | A P.S. that re-states the offer outperforms a P.S. that summarises | reviewer is grading the closing/P.S. section; writer is drafting the close | 12-ps-block | copy-chief, self-contained |
| _(future entry)_ | _(distilled BP claim, Q2-passing)_ | _(trigger phrase)_ | _(component or phase)_ | _(reviewer or all)_ |

## Roadmap

- Current count: 1 BP file (+ 1 writing standard header note).
- Wave 1 (Phase 1a outputs): `_critical-rules.md`, `_failure-modes.md` migrated from SKILL.md.
- Wave 2 (Phase 2 retrofits): per-component BPs distilled from `references/` claims — target ~15 entries.
```

**Entry count (current → projected):** 1 row today (ps-architecture) → ~3 rows post-Phase-1a (+_critical-rules, +_failure-modes) → ~15 rows after Wave 2 retrofits.

---

## Risks / Decisions Jerel needs to make

1. **Model source-of-truth.** SKILL.md L178 hard-codes `claude-opus-4-6` with a 2026-06-15 migration TODO. Where does the model decision live going forward? Options: (a) skill frontmatter `default_model: claude-opus-4-7`, (b) a `references/_models.md` lookup, (c) leave inline in Phase 1. The Phase 1a slim needs this answered — otherwise the model line gets moved to a reference and the migration deadline gets buried.

2. **Critical Rules + Common Failure Modes — one BP file or many?** Two options: (a) two big files `best-practices/_critical-rules.md` and `best-practices/_failure-modes.md` (12 rules total, all in one place — high discoverability, but each agent loads all of them whether relevant or not), or (b) split per-component (12 small files — perfect targeting but heavier index). Recommendation: (a) for Phase 1a, decompose later if the files grow past ~30 entries.

3. **Graph Links block (L52–58).** Confirm Obsidian wikilinks are dead in this workspace. If Jerel still uses Obsidian over `Marketing/skills/`, the graph-links block stays. If not, it's pure cut.

4. **Phase 0.5 + Phase 0.7 — separate playbooks or merged?** Phase 0.7 already has its own playbook (`mechanism-architecture.md`). Phase 0.5 currently has no playbook file. Do we create `phase-0-5-claim-audit.md` alongside, or merge both into a single `phase-0-architecture.md`? Recommendation: keep separate — they have different audit pairs and different HITL gates.

---

## Order of operations (if Jerel approves)

1. **Resolve the 4 decisions above.** No file edits start until model source-of-truth + BP-file granularity + Obsidian-link verdict + Phase 0.5/0.7 split are confirmed.
2. **Create the new reference + BP stubs first** (empty files with frontmatter only): `references/_index.md`, `references/_default-sequence.md`, `references/phase-0-5-claim-audit.md`, `references/phase-3-reviewer-stack.md`, `references/phase-4-preship.md`, `references/_invocation.md` (optional), `best-practices/_index.md`, `best-practices/_critical-rules.md`, `best-practices/_failure-modes.md`. Stubs only — no content yet. This makes the routing pointers from slim-SKILL.md valid before content lands.
3. **Migrate content into the new stubs.** Cut from SKILL.md → paste into stub → run Q1 + Q2 lens on the migrated chunk → adjust phrasing. One file per commit.
4. **Slim SKILL.md.** With every migration target file in place, rewrite SKILL.md top-to-bottom against the target outline above. Target ~100 lines. Re-read cold against Q1 + Q2 before saving.
5. **Verify routing.** Open SKILL.md fresh in a new agent context. Can it (a) decide whether the skill matches a request, (b) identify which reference file to load next, (c) find the master prompt? If any of the three fails, slim went too far.
6. **(Deferred to Phase 1b)** Trim `prompt-template.md` cross-cutting echo. Out of scope for Phase 1a.

---

## Honest call — is 24K too bloated for an advanced-tier skill?

Partly yes, partly no.

**The honest "yes" side:** ~10–12K of SKILL.md right now is duplication, not depth. Phase 0.7 sub-steps echo `mechanism-architecture.md`. Cross-cutting echo `prompt-template.md`. The default-sequence list lives in three places. The two `## Related` headers are a literal bug. None of that is "long-form sales letters are genuinely complex" — that's drift.

**The honest "no" side:** Long-form direct-response IS genuinely complex enough to warrant a 24K skill folder *in total* (and the existing `references/` + `best-practices/` total ~115K across 13 files — that's appropriate for an advanced skill). The question is what lives in L0 (SKILL.md, always loaded) vs L4 (references, fetched on demand). The skill doesn't need to lose depth — it needs to lose **redundant depth in L0**.

**Where I would push back on Jerel's framing:** the goal is not "compress SKILL.md to 80 lines because ICM says so." The goal is "every L0 token has to pay rent in every session, every reference token only pays rent when fetched." If 95 lines does the routing job, great. If 115 lines does it cleaner and passes Q1 standalone, take the extra 20. The one-screen rule is a guideline, not a kill criterion. Don't optimize for token count at the expense of completeness — that violates Q1.

**Net call:** proceed with the slim. Aim for ~100 lines but don't sacrifice Q1-completeness to hit it. The duplication cut alone will free ~12K bytes — that's the prize.
