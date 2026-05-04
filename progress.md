# Progress Log — Copywriting OS

## Session: 2026-04-24 (Phase 1 kickoff)

### Locked decisions (via AskUserQuestion)
1. Architecture: umbrella skill + client template
2. Scope: Phase 1 only (scrape + audit + propose, HITL gate)
3. Service line: separate general copywriting service (Fuggy's Media untouched)
4. NeezaNizam task: parked

### NeezaNizam handoff state (parked)
From prior session handoff. Resume through new OS in Phase 2.5 dogfooding.
- 3-reviewer stack (buyer-lens + copy-chief + self-contained) NOT fired
- Letter at `clients/neezanizam/sales-letters/260421-v1.md` still carries: 4-sentence scene headline, RAM/SPOT branded terms, defensive "why" stacks, missing markup
- Deferred fixes: Option B headline, declassify "Third Number" mechanism, founder photo, FAQ intro rewrite, case study specifics
- Skills ready for fire: `skills/sales-letter-method/reviewers/self-contained-reviewer.md`, Phase 3 orchestration in `commands/content/sales-letter.md`

### Phase 1 execution log

- **2026-04-24 (Phase 1.1 scout — main-agent fallback):** Sub-agent rate-limited at kickoff. Pivoted to main-agent + context-mode. Fetched + indexed `/archive` pages 1-4 via `ctx_fetch_and_index`. 12 newsletters identified; 10 slugs confirmed, 2 still uncertain (Issues 36, 38). §1 written to findings.md.
- **2026-04-24 (Phase 1.2 audit — main-agent fallback):** Batch-read SKILL.md frontmatter for 18 copywriting-relevant skills + 6 agents + client template core files via `ctx_batch_execute` (indexed into sandbox, queried via `ctx_search` to keep bodies out of main context). §2 written to findings.md — covers skill scope, agent roles, onboarding flow, onboarding-automation matrix (form can shrink 21 → ~10 questions + 3 URLs), infrastructure, gaps.
- **Phase 1.1 + 1.2 status:** functionally complete. 2 newsletter slugs will be resolved during Phase 1.3 bulk fetch.
- **2026-04-24 (Phase 1.3 deep extraction — main-agent + context-mode):** Bulk-fetched 12 newsletters via `ctx_fetch_and_index` (~241KB into sandbox). Ran targeted `ctx_search` passes for gap-fills (objection categories, A/B test verdict, Collier prompt examples, coat-of-arms template, proof types). Wrote 12-newsletter deep extractions to findings.md §3 — each with core thesis, frameworks, tactical moves, copy examples, novel-vs-our-stack, quotable gold, cross-links. 2 minor gaps flagged for Phase 4 follow-up (#41 verdict, #36 categories 4+6).
- **2026-04-24 (Phase 1.4 synthesis):** Wrote findings.md §4 (cross-newsletter consensus + contradictions + 12-item gap matrix + "gold we already own" map), §5 (full `copywriting-os` umbrella skill architecture + client folder scaffold + orchestration flow + DFY/DWY paths + quality-ceiling thesis), §6 (onboarding form rewrite: 21 Qs → 10 Qs + 3 URL drops + autofill pipeline + HITL review gate + net-impact table + DWY path).
- **2026-04-24 (Phase 1.5 handoff):** Updated task_plan.md Phase 2 with 10 refined subphases + Phase 3 (DWY productization) + Phase 4 (Phase 1 gap-fills). Wrote handoff file at `docs/handoff/2026-04-24-copywriting-os-phase-1.md`. **HITL gate reached — Phase 2 awaits Jerel approval of §5 architecture.**

### Phase 1 CLOSED. Phase 2 IN PROGRESS.

### Phase 2 execution log

- **2026-04-24 (Phase 1.5a):** Bulk-indexed remaining 35 newsletters via 3 ctx_execute batches (~670KB into sandbox). Combined with the 12 already in KB = all 47 queryable via `ctx_search`.
- **2026-04-24 (Phase 2.1 + 2.3 + 2.4):** Locked Option A sequencing. Built 10 files:
  - `commands/copy.md` — router (zero system-prompt weight, appears in skills catalog as `/copy`)
  - `.claude/references/copywriting-os/_index.md` — reference library index
  - `.claude/references/copywriting-os/gates/channeling-check.md` — Schwartz/Collier pre-write gate
  - `.claude/references/copywriting-os/gates/coat-of-arms-generator.md` — Halbert portrait generator
  - `.claude/references/copywriting-os/gates/one-person-seed.md` — Halbert writer instruction injection
  - `.claude/references/copywriting-os/reviewers/one-person-enforcement.md` — post-write declaration verifier
  - `.claude/references/copywriting-os/reviewers/proof-density-audit.md` — 6 proof types coverage
  - `.claude/references/copywriting-os/reviewers/emotional-sequence-audit.md` — 6 states ordering check
  - `.claude/references/copywriting-os/reviewers/objection-coverage-audit.md` — 6 categories coverage (4+6 flagged for Phase 4.2 confirm)
  - `.claude/references/copywriting-os/reviewers/teardown-reviewer.md` — element-by-element failure-mode library
- **2026-04-24 (Phase 2.2):** Built 5 sub-commands in `commands/copy/`: `sales-letter.md`, `email.md`, `landing.md`, `ad.md`, `headline.md`. All visible in skills catalog (`copy:sales-letter`, `copy:email`, `copy:landing`, `copy:ad`, `copy:headline`).
- **2026-04-24 (Phase 2.7):** Scaffolded `clients/_template/copy-system/` with 16 files: README, copy-brief template, coat-of-arms template, scout-instructions template, proof-inventory template, objection-matrix template, 5 outputs/ subdirs with .gitkeep, 5 swipe-file/ subdirs with .gitkeep, runs.md manifest + 7 per-gate log stubs. Ready to scaffold into any client project.

### Phase 2 status: CORE FUNCTIONAL

- ✅ 2.1 `/copy` router
- ✅ 2.2 5 sub-commands
- ✅ 2.3 3 pre-write gates
- ✅ 2.4 5 post-write reviewers (including one-person split)
- ⏭️ 2.5 Framework library files — DEFERRED (sandbox has all 47 newsletters queryable; static framework cards are nice-to-have, not blocking)
- ⏭️ 2.6 Existing skill upgrades — DEFERRED (headline-bank mechanism axis + sales-letter component-to-state mapping + big-angle-spotter mechanism diversity; NOT blocking dogfood because reviewers are self-contained)
- ✅ 2.7 Client template folder scaffold

**Copywriting OS is functional end-to-end for a sales letter dogfood.** Awaiting Jerel's sales letter upload.

### Errors

_None yet._

### Files created this session

- `task_plan.md` (root)
- `findings.md` (root)
- `progress.md` (root — this file)

---

## Session: 2026-05-04 (Phase 5 — Re-architecture review)

### Trigger
Jerel pasted a zero-fluff architecture-review handoff prompt + read Eduba/Jake `vault-toolkit` (ICM L0-L4 layer model + 60/30/10 framework). Asked for: (a) catalog of all copy/ads/marketing skills + agents project + global, (b) folder structure analysis, (c) overlap detection + sequencing, (d) usability scoring per persona, (e) re-architecture recommendation with global-vs-local client placement decision, (f) extend Copywriting OS pattern to ad copy + ad image generation, (g) defeat context bloat.

### Skill choice
`planning-with-files:plan` selected over `superpowers:writing-plans` and `superpowers:brainstorming`. Reasons: (1) file-based state survives context clears (the bloat the user is fighting), (2) hypothesis already exists (ReAct + ToT-lite + judges), so this is critical-review not blank-page brainstorming, (3) handoff demands multi-section markdown deliverable matching task_plan + findings + progress structure, (4) writing-plans is downstream (post-approval).

### Phase 5.1 actions
- Inspected `Jake_fulltoolkit/vault-toolkit/` — read constraints 03 (context hygiene) + 06 (layer triage) + content-production architecture CLAUDE.md + CONTEXT.md
- Catalogued all relevant skills + agents (project + global) using already-loaded routing tables — no fresh file reads needed for the inventory
- Sampled folder structures: `skills/copywriting/`, `skills/sales-letter-method/`, `skills/big-angle-spotter/`, `skills/ad-concept-engine/`, `.claude/references/copywriting-os/`
- Wrote 20-section architecture review at `docs/architecture-review-260504.md`
- Appended Phase 5 (5.1-5.7) to task_plan.md
- Did NOT execute any reorg, deletions, or new skill builds. HITL gate respected per handoff prompt.

### Files created/modified this session
- `task_plan.md` — appended Phase 5 (5.1-5.7)
- `progress.md` — this entry
- `docs/architecture-review-260504.md` — 20-section review (NEW)

### Open at HITL gate
Verdict: lightly refactor (don't re-architect). 3 first-priority changes proposed in §19 of the review. Awaiting Jerel approval before any file moves.

### 5.3 execution log (2026-05-04)
Jerel approved verdict + migration plan, picked 5.3 first.

**Moves:**
- `.claude/rules/details/{commands,routing-table,skills-catalog}.md` → `docs/system-rules/details/` (via `git mv`)

**New rule files** (`docs/system-rules/`):
- `operating-model.md` — owner + 80/20 HITL split
- `hitl-gates.md` — what needs approval, what auto-executes
- `analysis-framework.md` — 4-factor scoring (40/30/20/10)
- `self-annealing.md` — fix → log → update → test → strengthen
- `correction-capture.md` — what counts as a correction, where it logs
- `telegram-messaging.md` — multi-message reply format
- `session-end-protocol.md` — 8-step wrap (claude-md, learnings, corrections, changelog, living files)
- `session-start-protocol.md` — silent dashboard (git, ops, projects, campaigns, crons)
- `skill-graph-rule.md` — link-skills.py mandate
- `obsidian-context.md` — vault paths + voice/project two-layer model

**New learnings** (`learnings/`):
- `session-state.md` — confirmed patterns + mistakes-not-to-repeat
- `telegram-debugging.md` — MANDATORY process-first debug order
- `open-threads.md` — recurring scheduled checks + WIP

**Modified:**
- `.claude/rules/_index.md` — updated all `details/*` paths to point to `docs/system-rules/details/*`. Added on-demand sections for new rule files + learnings. Net-zero growth rule documented.
- `CLAUDE.md` — replaced with 83-line slim version. Kept only L0 essentials: role, startup files, critical workflow rules (data reliability, context discipline, marketing rules), context gate (full procedure inline because invoked every skill/agent call), workflow pointers, reference files index, hard pointers (telegram broken / session start / etc), token budget rule, one-liner operating model + obsidian context.

**Token impact (estimated):**
- Before: parent CLAUDE.md (~250 lines) + nested CLAUDE.md (~115) + 6 rule files including 3 large `details/*` files = ~12-18K tokens auto-loaded
- After: parent CLAUDE.md (~85 lines) + nested CLAUDE.md unchanged + small rule files only (`_index`, `routing-overrides`, `routing-table`, `mcp-integrations`, `skill-activation`) ≈ target ≤6K tokens auto-loaded
- **Verification pending:** restart session, run `/context`, count tokens. Target ≥40% reduction.

**NOT done (deliberate):**
- No commit. Per global rule: "NEVER commit unless explicitly asked." Files are in working tree, ready for Jerel to review and commit (or roll back via `git restore`).
- No deletion of any source content — everything moved or pointed to. `git restore` on these paths reverts cleanly.
- Did not touch user global `~/.claude/CLAUDE.md` (out of project scope).
- Did not touch nested `clients/neezanizam/CLAUDE.md` (covered in 5.2).
- Did not modify settings.json hooks (skill-router.sh still tells the model to consult routing-table.md and routing-overrides.md — these stay live, that's by design).

### Files created/modified this 5.3 sub-session
**Modified:**
- `CLAUDE.md`
- `.claude/rules/_index.md`
- `task_plan.md` (5.3 status update)
- `progress.md` (this log)

**Created:**
- `docs/system-rules/{operating-model,hitl-gates,analysis-framework,self-annealing,correction-capture,telegram-messaging,session-end-protocol,session-start-protocol,skill-graph-rule,obsidian-context}.md` (10 files)
- `learnings/{session-state,telegram-debugging,open-threads}.md` (3 files)

**Renamed (git mv):**
- `.claude/rules/details/commands.md` → `docs/system-rules/details/commands.md`
- `.claude/rules/details/routing-table.md` → `docs/system-rules/details/routing-table.md`
- `.claude/rules/details/skills-catalog.md` → `docs/system-rules/details/skills-catalog.md`

### 5.4 execution log (2026-05-04)
Jerel reviewed the video/visual skill inventory, marked specific keep/cut/refactor decisions.

**Retired (9 skills, all GLOBAL `~/.claude/skills/`)** — `mv SKILL.md → SKILL.md.retired-260504` (reversible by `mv` back):
- `seedance-effects` (frontmatter said RETIRED — absorbed into seedance-director)
- `seedance-loop` (RETIRED — absorbed)
- `seedance-motion` (RETIRED — absorbed)
- `seedance-prompt` (RETIRED — absorbed)
- `filmmaking` (RETIRED — absorbed into ai-filmmaking)
- `directors-cut` (RETIRED — absorbed into ai-filmmaking)
- `video-director` GLOBAL (RETIRED — narrative absorbed into ai-filmmaking; project version stays live)
- `marketing-studio-director` (Jerel: delete because higgsfield MCP supersedes)
- `remotion-best-practices` (Jerel: delete)

Other files in each retired skill folder (corrections.md, references/, scripts/, lib/) preserved for institutional memory + recovery.

**Refactored:**
- **`skills/higgsfield/SKILL.md`** (PROJECT) — added "Execution backend selection" section at top: MCP-first (`mcp__higgsfield__*` if available) with documented expected tool surface (`generate_image`, `generate_video`, `list_models`, `check_credits`, `get_generation`), browser fallback for current sessions where MCP not installed. Same model router applies regardless of backend.
- **`~/.claude/skills/ugc-creator/SKILL.md`** (GLOBAL) — added new section "CHARACTER REFERENCE SHEET TEMPLATE" with Jerel's full Cinematic Character Concept Art Sheet template (CHARACTER CORE / PERSONALITY / MAIN IDENTITY & SCALE / HEAD DETAIL / COLOR PALETTE / WARDROBE / NOTES / CLOSE-UP / LAYOUT RULES). Added field-mapping table from existing actor.json to template fields. Added optional `narrative` block schema for actor.json to capture archetype/personality_traits/etc. Render path routes to gpt-image-2-director (default), image-generation, or higgsfield.
- **`~/.claude/skills/gpt-image-2-director/SKILL.md`** — added "When to use a sibling skill instead" cross-ref table pointing to beat-sheet-director (videos), image-generation/higgsfield (UGC faces), seedance-* (videos), ugc-creator (character sheets).
- **`~/.claude/skills/beat-sheet-director/SKILL.md`** — added matching cross-ref table pointing back to gpt-image-2-director (single images) + seedance for videos + ugc-creator for character sheets.

**Decision: Don't merge gpt-image-2-director and beat-sheet-director.** Beat-sheet IS GPT Image 2's specialized video-storyboard mode, but its output format (panel grid w/ timecodes/captions) is distinct enough that merging would bloat the parent. Cross-references make the relationship explicit.

**NOT done (deliberate):**
- Did not delete folder contents — only mv'd SKILL.md → SKILL.md.retired-260504. Easy revert.
- Did not update `docs/system-rules/details/routing-table.md` or `details/skills-catalog.md` to remove retired skills entries. The auto-generated `.claude/rules/routing-table.md` will refresh on next SessionStart hook (refresh-registry.js scans for SKILL.md presence). Manual catalog cleanup queued for a future hygiene pass — they're already on-demand-only so don't bloat session.
- Did not touch `seedance-ugc-director` (frontmatter says RETIRED but Jerel kept on default per "rest do the default" — frontmatter discrepancy noted for future hygiene pass).

### Files created/modified this 5.4 sub-session
**Modified (4 SKILL.md):**
- `skills/higgsfield/SKILL.md`
- `~/.claude/skills/ugc-creator/SKILL.md`
- `~/.claude/skills/gpt-image-2-director/SKILL.md`
- `~/.claude/skills/beat-sheet-director/SKILL.md`

**Renamed (9 SKILL.md → SKILL.md.retired-260504):**
- `~/.claude/skills/{seedance-effects, seedance-loop, seedance-motion, seedance-prompt, filmmaking, directors-cut, video-director, marketing-studio-director, remotion-best-practices}/SKILL.md`

**Modified (planning):**
- `task_plan.md` — 5.4 marked complete
- `progress.md` — this log

---

### 5.2 execution log (2026-05-04)
Jerel: "sure do a snapshot and /session-handoff afterwards, keeping in mind the jake organising"

**Pre-reorg snapshot:** `clients/neezanizam-260504-pre-reorg/` (50M, rsync from working folder). Single-command rollback if reorg fails: `rm -rf clients/neezanizam && mv clients/neezanizam-260504-pre-reorg clients/neezanizam`.

**Reorg executed (Jake/Eduba ICM L0/L3/L4):**

| New path | Was | Layer |
|----------|-----|-------|
| `clients/neezanizam/CLAUDE.md, context-profile.json` | (root) | L0 always-loaded |
| `_brand/{icp,offer,brand-voice,buyer-profile,channels,learnings,source-of-truth,source-of-truth-draft,story-bank,asset-map,notebooklm,metrics-config}.md/json + .bak files` | (root) | L3 stable identity |
| `_brand/avatars/` | `avatars/` | L3 |
| `_brand/brand-assets/{DESIGN, font, reference, "everything else"}` | `brand/` | L3 |
| `_swipe/research/` | `research/` | L3 research |
| `_swipe/competitor-ads/` | `competitor-ads/` | L3 |
| `_swipe/swipe-file{,-buyers,-sellers}.md` | (root) | L3 |
| `_swipe/hook-library.md, wave-reserved-angles.md` | `angles/` | L3 reservoir |
| `_swipe/headline-banks/wave-{1,2}-headline-bank.md` | `angles/` | L3 reservoir |
| `campaigns/angles/{README, wave-1, wave-2, wave-1-vs-stage-analysis, iteration-log}.md, big-angle-spotter/` | `angles/` | L4 working |
| `campaigns/big-angle-spotter-runs/` | (root) | L4 |
| `campaigns/{feedback, metrics, funnel, sheet-snapshots}/` | (root) | L4 |
| `campaigns/dashboard.html` | (root) | L4 |
| `output/sales-letters/` | `sales-letters/` | L4 deliverables |
| `output/deliverables/` | `deliverables/` | L4 |

**Top level after reorg (10 items):** `.claude/, .DS_Store, CLAUDE.md, context-profile.json, _brand/, _swipe/, assets/ (empty placeholder), campaigns/, output/`. Down from 38 items.

**Nested CLAUDE.md updates:**
- Replaced flat file routing table with new ICM-aware version + visual structure tree at top
- Updated 6-stage pipeline references (e.g., `angles/big-angle-spotter/` → `campaigns/angles/big-angle-spotter/`, `research/big-ideas/` → `_swipe/research/big-ideas/`)
- Updated Active Work paths (Wave 1 headline bank → `_swipe/headline-banks/`)
- Updated Never Do clauses (saturated angles in `_brand/learnings.md`, angle/hook/wave data in `campaigns/angles/`)
- Updated Branding pointer (`brand/DESIGN/` → `_brand/brand-assets/DESIGN/`)

**Real code fix:** `scripts/patch_angle_cell.py:145` — `clients/<slug>/sheet-snapshots/` → `clients/<slug>/campaigns/sheet-snapshots/`. (Was the only real path-building code; rest were docstrings/usage examples.)

**Symlink preserved:** `_swipe/research/big-ideas/` (points to `~/AI workflows/nn-ads-big-ideas/`) survived the move (rsync preserves symlinks).

### Phase 5.2.5 — Cleanup queue (post-reorg, do later)

These do NOT block the reorg from working but should be touched in a hygiene pass to keep the system honest:

**Script docstrings/usage examples with old paths (cosmetic, won't break code):**
- `scripts/phase4_acceptance_test.py` line 9 — sales-letters/ path in docstring
- `scripts/backfill_angle_rationale.py` lines 11, 14 — `--dct-dir` examples
- `scripts/ad_concept_sheet_writer.py` lines 24, 359 — comment strings
- `scripts/source_of_truth_sheet_writer.py` lines 13, 22, 27 — `--draft` examples
- `scripts/reddit.py` line 17 — `--output-dir` example

**Copywriting OS reviewer templates (`scripts/build_copyos_reviewers.py`):**
- Lines 147-485: TEMPLATE STRINGS that get written into reviewer markdown files when the script runs. Templates reference `clients/<slug>/source-of-truth.md`, `clients/<slug>/research/*.md`, `clients/<slug>/learnings.md`, `clients/<slug>/brand-voice.md`, `clients/<slug>/angles/iteration-log.md`. Need to update to new ICM paths AND re-run the script to regenerate the shipped reviewer files at `.claude/references/copywriting-os/reviewers/`.

**Already-shipped reviewer files** (at `.claude/references/copywriting-os/reviewers/`) likely reference old paths — verify and update on next session.

**Decision (Phase 5.2.5 priority):** the ICM reorg is functional for interactive use (Claude reads new paths from updated nested CLAUDE.md). Scripts using old paths will fail with clear errors. Address scripts as encountered OR batch-update during next `/ops:weekly`. Snapshot at `clients/neezanizam-260504-pre-reorg/` stays until Wave 2 ships and operator confirms no regressions, then delete.

### Files created/modified this 5.2 sub-session
**Created (snapshot):**
- `clients/neezanizam-260504-pre-reorg/` (50M, full mirror — gitignore?)

**Modified:**
- `clients/neezanizam/CLAUDE.md` — full ICM-aware rewrite of routing table + 6-stage pipeline + active work + never-do paths + branding pointer
- `scripts/patch_angle_cell.py:145` — real code path updated
- `task_plan.md` — 5.2 marked complete + 5.2.5 cleanup phase added
- `progress.md` — this log

**File-system changes (clients/neezanizam/):**
- 13 root-level files moved into `_brand/`
- 1 dir (`avatars/`) moved into `_brand/`, 1 dir (`brand/`) renamed to `_brand/brand-assets/`
- 2 dirs (`research/`, `competitor-ads/`) moved into `_swipe/`
- 3 swipe-file md's + 2 reservoir md's moved into `_swipe/`
- 2 headline banks moved into `_swipe/headline-banks/`
- 5 angles md's + 1 dir + 1 README moved into `campaigns/angles/`
- 6 dirs (big-angle-spotter-runs, feedback, metrics, funnel, sheet-snapshots) + 1 file (dashboard.html) moved into `campaigns/`
- 2 dirs (sales-letters, deliverables) moved into `output/`
- 0 deletes — all moves preserve content

### 5-Question Reboot Check
| Question | Answer |
|----------|--------|
| Where am I? | Phase 5.1 complete. HITL gate before 5.2. |
| Where am I going? | 5.2 client folder ICM split → 5.3 rules-index finish → 5.4 dead-skill purge → 5.5 creative-os build → 5.6 stage contracts → 5.7 dogfood |
| What's the goal? | Defeat context bloat + extend Copywriting OS pattern to ads/images without re-architecting working primitives |
| What have I learned? | See `docs/architecture-review-260504.md` |
| What have I done? | See above |
