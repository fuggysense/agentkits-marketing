# Task Plan — Copywriting OS Build

**Session start:** 2026-04-24
**Operator:** Jerel
**Goal:** Build a general-purpose copywriting service (separate from Fuggy's Media SG property agency) with (a) a new umbrella skill `skills/copywriting-os/` orchestrating existing skills, (b) a duplicable client folder template `clients/_template/copy-system/`, and (c) a minimized onboarding form that leverages Claude Code scraping for YouTube/channel/testimonials. Source of wisdom: 12 newsletters from https://www.copywriting.ai/archive.

**Phased scope — this session is Phase 1 only (HITL gate before Phase 2).**

## Guardrails (from user directives)

- DFY first, DWY (sell the system) later — architecture must not foreclose either path
- 80–90% automated, 10–20% human taste
- Output quality must beat "most copywriters in the world" — human taste is the final variable, nothing else
- Replicable: one command duplicates the whole OS into any new project folder
- Minimize onboarding friction: replace manual form fields with Claude Code scraping wherever possible
- Covers 4 copy domains: sales letters, emails, ads, multi-client management
- Ties into existing: sales-letter-method, ad-concept-engine, copywriting, email-sequence, content-moat, unslop, writing, scrapecreators, transcribe, voice/, ad-library-scraper, avatar-research, headline-bank, big-angle-spotter
- NeezaNizam 3-reviewer task PARKED (see progress.md)

## Phases

### Phase 1 — Scrape + audit + propose (THIS SESSION)

| # | Phase | Status | Output |
|---|-------|--------|--------|
| 1.1 | Scout archive (main-agent fallback, sub-agents rate-limited) — 12 newsletters identified, 10 slugs confirmed, 2 TBD | **COMPLETE** (with 2 slugs to resolve in 1.3) | `findings.md` §1 |
| 1.2 | Audit marketing profile (main-agent fallback) — 18 skills + 6 agents + onboarding flow + gaps | **COMPLETE** | `findings.md` §2 |
| 1.3 | Bulk fetch + index 12 newsletters via `ctx_fetch_and_index` into sandbox; 12 structured deep extractions via targeted `ctx_search` queries | **COMPLETE** (2 minor gaps flagged for Phase 2: #41 A/B-test verdict, #36 objection categories 4 + 6) | `findings.md` §3 |
| 1.4 | Synthesized cross-newsletter patterns (§4), proposed `copywriting-os` umbrella skill architecture (§5), onboarding form rewrite sketch (§6) | **COMPLETE** | `findings.md` §4, §5, §6 |
| 1.5 | Write handoff file + mark progress close + HITL gate | **COMPLETE** | `docs/handoff/2026-04-24-copywriting-os-phase-1.md` |

### Phase 1.5 — Remaining 35 newsletter deep-reads (DEFERRED, pending Jerel call)

**Triggered by:** Jerel's push-back 2026-04-24 — initial count of 12 was wrong; sitemap authoritative list = 47 newsletters. 35 not yet deep-read. Full list + top-10 priority in `findings.md` §1.C / §1.D.

Options:
- **1.5a Full 35:** bulk fetch via `ctx_fetch_and_index` + targeted extraction (~60 min main-agent work; sub-agents if rate-limit resets)
- **1.5b Top 10 priority only:** Hormozi $100M, onboarding-from-clients, positioning AI copywriter, AI landing pages, AI emails, Framework Arsenal, hidden AI patterns emails, story structure, legend architecture, fundamentals
- **1.5c Skip for now:** proceed to Phase 2 with the 12 we have; loop back as enrichment after Phase 2 ships

### Phase 1.6 — Architecture viability recheck (COMPLETE IN findings.md §7)

**Triggered by:** Jerel's push-back on context-bleed risk. §7 in findings.md delivers honest analysis + architecture shift: ship `copywriting-os` as `commands/copy.md` + `references/copywriting-os/` + context-mode sandbox for reference library + sub-agent delegation for heavy modules, **instead of** a fat auto-activating skill. Eliminates system-prompt bloat and per-session stacking. Phase 2 plan needs to reflect this shift before building — see §7.C.

### Phase 2 — Build (REVISED to command-based architecture per §7.C; dogfood swapped to Jerel-uploaded sales letter)

**Locked decisions from Jerel 2026-04-24:**
- Phase 1.5a (full 35 deep-reads): YES, running now
- Architecture shift (§7.C command-based): YES
- Phase 2 sequencing: **awaiting Jerel's pick** — see 2.X recommendation below
- Dogfood material: Jerel-uploaded sales letter (replaces NeezaNizam)
- Phase 4 gap-fills: after Phase 2

Revised 9-task subphase list (dropped auto-skill scaffolding, added `/copy` command + sandbox-first reference store):

| # | Subphase | Deliverable | Depends on |
|---|----------|-------------|------------|
| 2.1 | ✅ **Built `/copy` router command** | `commands/copy.md` — visible in skills catalog | — |
| 2.2 | ✅ **Built 5 sub-commands** — `/copy:sales-letter`, `/copy:email`, `/copy:landing`, `/copy:ad`, `/copy:headline` | `commands/copy/*.md` ×5 — all visible in skills catalog | 2.1 |
| 2.3 | ✅ **Built 3 pre-write gate fragments** — channeling-check, coat-of-arms-generator, one-person-seed | `.claude/references/copywriting-os/gates/*.md` ×3 | — |
| 2.4 | ✅ **Built 5 post-write reviewer fragments** — one-person-enforcement (post-write split), proof-density-audit, emotional-sequence-audit, objection-coverage-audit, teardown-reviewer | `.claude/references/copywriting-os/reviewers/*.md` ×5 | — |
| 2.5 | ⏭️ **Framework library files — DEFERRED (sandbox already holds all 47 newsletters via `ctx_search`; static framework cards are nice-to-have)**. Schedule if needed for DWY productization in Phase 3. | `.claude/references/copywriting-os/frameworks/*.md` ×10-12 (optional) | — |
| 2.6 | ⏭️ **Existing skill upgrades — DEFERRED (reviewers are self-contained enough to function without the in-skill upgrades for dogfood)**. Will revisit after dogfood if reviewers surface specific gaps. | Upgraded `skills/headline-bank/`, `skills/sales-letter-method/`, `skills/big-angle-spotter/` | (reviewers pass dogfood) |

### Phase 2.11 — External integration (COMPLETE 2026-04-24)

High-priority wiring fixes triggered by Jerel's post-build audit:
- ✅ `teardown-reviewer.md` dangling ref to non-existent `frameworks/failure-mode-library.md` removed (library is inlined in the reviewer file)
- ✅ `.claude/rules/details/commands.md` updated with new "Copywriting OS" section listing `/copy` + 5 sub-commands
- ✅ `.claude/rules/details/routing-table.md` updated with new "Copywriting OS" section documenting router + sub-commands + gates + reviewers + client workspace + sandbox library
- ✅ 6 SKILL.md frontmatter updated with `preferred_invocation: /copy:*` field so skill discovery surfaces the wrapper: `sales-letter-method`, `copywriting`, `email-sequence`, `ad-concept-engine`, `big-angle-spotter`, `headline-bank`

### Phase 3 — DWY Productization + deferred enrichment (FUTURE sessions)

**3.1 Extract cai #40 two verbatim Claude Skill prompts** into standalone reference files (DWY pack seeds):
- `.claude/references/copywriting-os/frameworks/landing-page-skill-cai40.md` — full "# Landing Page Copy Generator" system prompt from cai #40, paste-and-go
- `.claude/references/copywriting-os/frameworks/email-4day-skill-cai40.md` — full "# 4-Day Sales Email Sequence Builder" system prompt from cai #40, paste-and-go
Source: ctx_search source "cai #40 two-claude-skills" — materialize into files before sandbox TTL risk.

**3.2 Extract top-10 priority older newsletters** into structured reference cards (see Phase 1.5 priority list in findings.md §1.D):
- cai #18 Hormozi $100M offer applied to copy → `frameworks/hormozi-offer.md`
- cai #14 Framework Arsenal → `frameworks/framework-arsenal.md`
- cai #40 (older, different — need to disambiguate) Using AI to get what you need from clients → `frameworks/client-onboarding-with-ai.md`
- cai #42 (older) How to position AI copywriter → `frameworks/positioning-ai-copywriter.md`
- cai #37 (older) AI copywriting landing pages → compare against our `copywriting` skill
- cai #39 (older) AI copywriting email marketing → compare against `email-sequence`
- cai #26 Hidden AI patterns in emails → expand `reviewers/teardown-reviewer.md` email subsection
- cai #17 Masters command sequence story structure → `frameworks/story-structure.md`
- cai #29 Legend architecture origin story → `frameworks/legend-architecture.md`
- cai #36/#44/#46/#47 AI copywriting + Direct Response fundamentals → `frameworks/fundamentals-primer.md`

Source: all indexed in context-mode sandbox; risk = 24h TTL. Consider running Phase 3.2 early in next session to avoid re-fetch.

**3.3 In-skill upgrades** (Phase 2.6 revisited):
- `skills/headline-bank/` — add 5-mechanism axis natively (supplement to the existing 5 awareness × 10 angle matrix)
- `skills/sales-letter-method/` — tag each of the 12 components with its emotional state (from cai #37 mapping in `reviewers/emotional-sequence-audit.md`)
- `skills/big-angle-spotter/` — Step 10-12 enforce mechanism diversity (each of 3 produced headlines from different mechanism)

**3.4 DWY single-file claude.ai-uploadable skill exports** (cai #40 template pattern):
- `sales-letter-method-lite.md` (trim down to single uploadable file)
- `landing-page.md`
- `email-4day.md`
- `headline-lab.md`
- `proof-arsenal.md`
- `objection-destroyer.md`
- `emotion-engine.md`
- `scout-system.md`

**3.5 Run `python3 scripts/link-skills.py`** to include copywriting-os in `.claude/skill-graph.json` (per project CLAUDE.md mandate).

**3.6 Phase 2.8 + 2.9 original** (onboarding form + training docs) — run after the Jerel-uploaded sales letter dogfood completes.

### Phase 4 — Gap-fills (FUTURE sessions, after Phase 3)

- 4.1 Full-read cai #41 "First Draft vs Edit Layer" → extract verdict + codify `copy-workflow-router.md`
- 4.2 Full-read cai #36 → confirm objection categories 4 + 6 definitions; update `reviewers/objection-coverage-audit.md` + `clients/_template/copy-system/objection-matrix.md`
- 4.3 Full-read cai #26 → expand `reviewers/teardown-reviewer.md` email-specific failure-mode sub-library
| 2.7 | ✅ **Built `clients/_template/copy-system/` scaffold** — README + copy-brief template + coat-of-arms template + scout-instructions + proof-inventory + objection-matrix + 5 outputs/ subdirs + 5 swipe-file/ subdirs + runs.md + 7 per-gate log stubs. 16 files total. | Folder tree + templates | 2.3, 2.4 |
| 2.8 | **Build `/project:new-copy` command + autofill pipeline** — the ≤10-question onboarding form from §6 + post-submit orchestration of `ctx_fetch_and_index` (website) + `scrapecreators` (social) + `transcribe` (YouTube + testimonials) + `chrome-mcp` (reviews) + `ad-library-scraper` (industry ads); HITL preview gate before activation | Command + pipeline script + HITL flow | — (can parallelize with 2.1-2.7) |
| 2.9 | **Write training docs** — `operator-quickstart.md` (for Jerel/team), `trainee-first-project.md` (junior copywriter), `dwy-client-onboarding.md` (future DWY clients) | 3 markdown docs under `.claude/references/copywriting-os/training/` | 2.1-2.8 |
| **2.X** | **Dogfood on Jerel-uploaded sales letter** — test full `/copy:sales-letter` pipeline (all pre/post gates) on a NEW letter Jerel uploads. Replaces NeezaNizam as dogfood material. NeezaNizam stays parked. | v2 letter + first `quality-gates/` log entries | Depends on Jerel's sequencing pick below |

### Sequencing — LOCKED: Option A (Jerel 2026-04-24)

**Phase 2 batch 1 (2.1-2.7 — core):** router + sub-commands + 3 pre-write gates + 4 post-write reviewers + sandbox reference library + skill upgrades (headline-bank / sales-letter-method / big-angle-spotter) + `clients/_template/copy-system/` scaffold.

**Phase 2 dogfood (2.X):** test `/copy:sales-letter` end-to-end on the sales letter Jerel uploads.

**Phase 2 batch 2 (2.8-2.9 — onboarding + training):** after 2.X validates write-side works.

### Phase 3 — DWY Productization (FUTURE, after Phase 2 stabilizes)

- 3.1 Extract single-file claude.ai-uploadable versions of top skills per #40 pattern: `sales-letter-method-lite.md`, `landing-page.md`, `email-4-day.md`, `headline-lab.md`, `proof-arsenal.md`, `objection-destroyer.md`, `emotion-engine.md`, `scout-system.md`
- 3.2 DWY onboarding + training package
- 3.3 Pricing + delivery mechanics

### Phase 4 — Gap-fills from Phase 1 flags (CAN RUN ANYTIME)

- 4.1 Full-read #41 "First Draft vs Edit Layer" → extract Peggy/Mark verdict → codify `copy-workflow-router.md` decision logic
- 4.2 Full-read #36 "Objection Destroyer" → confirm objection categories 4 and 6 → complete `six-objection-categories.md` reference

### Phase 5 — Re-architect copy + ads + image gen stack (2026-05-04, IN PROGRESS)

**Trigger:** Jerel pasted a zero-fluff architecture-review handoff prompt + Eduba/Jake `vault-toolkit` ICM (L0-L4) + 60/30/10 framework. Goal: defeat context bloat, decide global vs local folder placement, extend Copywriting OS pattern from copy-only to creative-wide (ad copy + ad images + video prompts).

**Constraint:** Review-first, implement-after. HITL gate after 5.1. No file moves/deletions until Jerel approves.

| # | Subphase | Deliverable | Status |
|---|----------|-------------|--------|
| 5.1 | Architecture review (20-section format from handoff prompt) — verdict, diagnosis, ICM layer audit, folder reorg proposal, migration plan, pre-mortem, assumption audit | `docs/architecture-review-260504.md` | **COMPLETE — awaiting Jerel HITL** |
| 5.2 | Reorganize `clients/<slug>/` to ICM L3/L4 split — `_brand/` (L3) + `_swipe/` (L3) + `campaigns/<c>/` (L4) + `output/` (L4) | Per-client folder reorg + CLAUDE.md update | pending HITL |
| 5.3 | Finish rules-index pattern — move `details/{commands,routing-table,skills-catalog}.md` out of auto-load. Project CLAUDE.md becomes ~50-line map. Auto-loaded routing tables eliminated. | `.claude/rules/_index.md` complete + parent `CLAUDE.md` slimmed | **COMPLETE 2026-05-04** — CLAUDE.md 279→83 lines (70% reduction). 13 split files in `docs/system-rules/` + `learnings/`. `details/` moved from `.claude/rules/` to `docs/system-rules/`. Awaiting verify on next session restart + commit. |
| 5.4 | Delete confirmed-retired skills — 4× `seedance-*` (loop, motion, prompt, effects) + `directors-cut` + global `video-director` + `filmmaking` + Jerel-pick `marketing-studio-director` + `remotion-best-practices`. Plus refactor: higgsfield (MCP-first), ugc-creator (new char sheet template), gpt-image-2 ↔ beat-sheet cross-refs. | Skill folder cleanup + 4 refactors | **COMPLETE 2026-05-04** — 9 SKILL.md → SKILL.md.retired-260504 (reversible). higgsfield + ugc-creator + gpt-image-2-director + beat-sheet-director updated. |
| 5.5 | Build `creative-os/` extending `copywriting-os` pattern to ad images + video prompts — `gates/` (brand-fit, format-check, ICP-resonance) + `reviewers/` (visual-claim, brand-voice-fidelity, scroll-stop, mechanism-diversity) + wire `/ads:concepts` Phase 3a to route through them | `.claude/references/creative-os/` ×8-10 files + `commands/creative.md` router | pending HITL |
| 5.6 | Stage contracts (L2) — write `01_research/CONTEXT.md`, `02_angles/CONTEXT.md`, `03_render/CONTEXT.md`, `04_test/CONTEXT.md`, `05_feedback/CONTEXT.md` for the 6-stage creative pipeline. Each <500 tokens. Loaded only when stage runs. | 5 CONTEXT.md files | pending HITL |
| 5.7 | Verification dogfood — run a full client through the new structure (NeezaNizam Wave 3 or new client). Time-track context tokens used vs current setup. Target: 40%+ reduction. | Dogfood log + token audit | pending 5.2-5.6 |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| Sub-agent rate limit hit (resets 11:40am SGT) — both scout + audit agents returned `You've hit your limit` | 1 | Pivoted Phase 1.1 + 1.2 to main-agent execution (WebFetch + local Read). Phase 1.3 will use `ctx_fetch_and_index` (sandbox) to keep 12 newsletters out of main context. Dormant agent IDs preserved: scout `abfef69d19dfdc697`, audit `a297bdb965aafcea4` — can resume post-reset if needed. |

## Decisions locked this session

- **Architecture:** Umbrella skill + client template (NOT rewrite sales-letter-method, NOT pure scaffold)
- **Scope:** Phase 1 only — scrape, audit, propose. No build until Jerel approves.
- **Service line:** Separate general copywriting service. Fuggy's Media (property agent lead gen) untouched.
- **NeezaNizam:** Parked. Resumes through new OS in Phase 2.5 dogfooding.

## Context Gate (per project CLAUDE.md)

This is a cross-cutting meta-project (system build, not client output). Context gate satisfied: no single-client voice load required. V.O.I.C.E. files for Jerel will be loaded if/when writing copy during dogfooding in Phase 2.
