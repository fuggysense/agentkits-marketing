# Changelog

## 260424

### Created
- **Copywriting OS — 4 Phase B Anti-Hallucination Reviewers + 2 Pre-Write Grounding Builders.** New layer bolted onto `/copy` router between existing pre-write gates and existing Phase C persuasion-craft reviewers. Shipped via 6-agent parallel blast — 6 fresh `claude -p` Sonnet 4.6 workers orchestrated by `scripts/build_copyos_reviewers.py` with content-cached SP (~250K cache_read per worker on warm runs). Ravan pattern from `big-angle-spotter/scripts/run_pipeline.py`. Files:
  - `.claude/references/copywriting-os/reviewers/claim-verification-audit.md` (B1) — every factual claim traces to a grounding-file source; blocks on CRITICAL unsourced.
  - `.claude/references/copywriting-os/reviewers/forbidden-content-audit.md` (B2) — F1 banned phrases / F2 saturated angles / F3 voice drift / F4 AI-tell / F5 compliance / F6 hard-sell categories.
  - `.claude/references/copywriting-os/reviewers/specificity-audit.md` (B3) — weasel word density check, cross-refs grounding numbers, 40+ term reference list embedded.
  - `.claude/references/copywriting-os/reviewers/buyer-language-fidelity-audit.md` (B4) — verbatim-match for quotes, register-drift scoring for paraphrases, Singlish upshift detection with 6-row drift pattern table.
  - `.claude/references/copywriting-os/builders/proof-inventory-builder.md` — pre-write harvester feeding B1 via `clients/<slug>/copy-system/proof-inventory.md`.
  - `.claude/references/copywriting-os/builders/objection-matrix-builder.md` — pre-write harvester feeding drafter + existing Phase C objection-coverage-audit via `clients/<slug>/copy-system/objection-matrix.md`.
  - `scripts/build_copyos_reviewers.py` — 6-worker parallel orchestrator with `--labels` filter for selective rebuild and response-guard (rejects outputs not starting with `# `). First run clobbered on MCP-tool-write race; fixed by tightening SP output contract to forbid tool use and adding starts-with-`# ` validator.
  - Contributor: Jerel

### Updated
- **`commands/copy.md`** router — added Step 3b pre-write builders block (fires 2 sub-agents: proof-inventory + objection-matrix); expanded Step 5 from 5 to 9 post-write reviewers split into Phase B (grounding, strictly gating) + Phase C (persuasion craft, existing); Step 6 synthesise now resolves Phase B failures first.
- **`.claude/references/copywriting-os/_index.md`** — added Builders table (2 rows) + split Reviewers into Phase B (4 rows) and Phase C (5 rows).
- **`.claude/rules/details/routing-table.md`** Copywriting OS section — added pre-write builders row + Phase B vs Phase C reviewer rows.
- **`skills/sales-letter-method/SKILL.md`** — Phase 1 drafters (Hook Half + Commit Half) switched `2 Sonnet subagents` → `2 Opus 4.6 subagents`. Phase 2 stitcher explicitly labelled Opus 4.6. TODO marker for migration to `claude-opus-4-7` by 2026-06-15 (Opus 4.6 deprecation).
- **`/Users/jerel/AI workflows/big-angle-spotter/scripts/run_pipeline.py`** — global model policy: added `COPY_MODEL = "claude-opus-4-6"` + `REVIEW_MODEL = "claude-sonnet-4-6"` + per-step `MODEL_MAP` dict + `model_for_step(step_id, cli_override)` helper. Steps 01/07/07b/08/11/12 default to Opus 4.6 (copy-generating); 02/03/04/05/06/09/10/top3_extract stay on Sonnet 4.6 (review/ranking/extraction). CLI `--model` flag now an override (sentinel None default). TODO marker for 4.6 → 4.7 migration.
  - Inspired by: Jerel's request to apply Opus-for-copy / Sonnet-for-review split globally after Ravan-pattern research confirmed the big-angle-spotter pipeline fans out fresh `claude -p` workers per question — per-step routing is free once the orchestrator already knows which step is running.
  - Contributor: Jerel

## 260421

### Created
- **`seedance-ugc-director`** skill (v1.0.0, global at `~/.claude/skills/seedance-ugc-director/`) — Opinionated one-shot Seedance 2.0 UGC ad director. Takes a script/concept, outputs Pinterest creator refs + @Image1/2/3 mapping + Hook→Problem/Proof→Benefit/Demo→CTA 15s segment prompts + anti-cinematic keyword bans (NEVER: cinematic, dolly, bokeh, color grade, LUT, etc.) + room-tone matched audio presets (bathroom/kitchen/car/outdoors/etc.) + natural dialogue rules (contractions, fillers). No clarifying questions — strict output format. Supersedes Mode 3 of `seedance-prompt`.
  - Inspired by: downloaded `seedance-20-ugc-ad-director.skill` (community-shared skill pack)
  - Contributor: Jerel

### Updated
- **`seedance-prompt`** skill (1.0.0 → 1.1.0) — Retired Mode 3 (Ad Creative / NanoBananaPro sequences) and all related cross-references. Now two modes only: T2I (character sheets, scene images, environments) and I2V (animate existing images). Frontmatter description rewritten; routing table now points UGC ad requests to `seedance-ugc-director`.
- **`video-director`** skill (global 1.0.0 → 1.1.0) — Frontmatter description updated, added explicit "When to Use a Different Skill" routing table. Seedance 2.0 UGC ads now route to `seedance-ugc-director`.
- **`video-director`** skill (local `skills/video-director/SKILL.md` v2.0.0) — "NOT for" list + routing table updated: Seedance UGC → `seedance-ugc-director`, Seedance character sheets/I2V → `seedance-prompt`, Higgsfield persistent-actor → `ugc-creator`.
- **`ugc-creator`** skill — Frontmatter description now explicit that this is Higgsfield-only and routes Seedance UGC ads to `seedance-ugc-director`.
- **`.claude/rules/details/routing-table.md`** — Added entries for `seedance-ugc-director`, `seedance-prompt`, `ugc-creator`; updated `video-director` row with routing note.
- **`.claude/rules/details/skills-catalog.md`** — Added `seedance-ugc-director`, `seedance-effects`, `seedance-loop`, `seedance-motion`, `ugc-creator`, `ai-filmmaking` entries to Content & Copy Skills section; updated `video-director` + `seedance-prompt` entries with retirement/routing notes.
- **`video-factory`** skill (1.0.0 → 2.0.0) — Dynamic two-axis routing refactor. Replaces linear 5-phase pipeline with a Phase 0 dispatcher that (A) picks one of 6 content-type pipelines — `ugc-seedance` / `cinematic-narrative` / `property-showcase` / `product-arugc` / `motion-graphics` / `webpage-loop` — and (B) scans `clients/<project>/` state, writes `video-factory-state.json` manifest, skips phases whose outputs are fresh (<6mo soft-warn). New: `references/phase-0-dispatcher.md` + `references/pipelines/<6 archetypes>.md`. Edited: all 5 phase files carry `## Preconditions / Outputs / Skippable if output fresh?` headers so the dispatcher can reason about state without re-reading whole files. Sonnet sub-agent pattern (via Agent tool `model: "sonnet"`) documented for Phase 1 research + Phase 3 isolation-layer parallelization. SKILL.md rewritten as thin dispatcher (463 → 167 lines). Stale `seedance-prompt (Ad Creative mode)` references replaced with routing notes to `seedance-ugc-director`. UGC defined as avatar+env+action+product(optional); talking-head routes through `ugc-seedance` with `product: null`.
  - Inspired by: two-axis routing discussion (content-type × state-aware execution) in session 260421
  - Contributor: Jerel
- **ArcAds prompting-methods cherry-pick** — 5 patterns stolen from `krusemediallc/arcads-claude-code` and integrated across 6 skills (prompting techniques only, no product adoption). Touched: (1) `seedance-ugc-director` (global) — **Technical-Flaws-as-Features** (prescribes UGC imperfections: camera shake, off-centre framing, finger shadow, audio hum, handheld breathing) + **Structured Input Anatomy** 9-layer scaffold. (2) `image-generation` (local) — **For Character Consistency** (CRITICAL CHARACTER LIKENESS block) + **Iteration Protocol** (2-regen cap + if-then diagnostics). (3) `avatar-research` — downstream LIKENESS handoff note. (4) `script-skill` (global) — Formula `seconds = word_count / 2.5` + WPS calibration for slow/fast speakers. (5) `video-director` (local) — **Script → Duration Auto-Mapping** + **Iteration Protocol** (5-symptom diagnostic table). All body-only edits, no YAML changes, skill-graph refresh not required. Plan + findings: `docs/plans/260421-arcads-review/`.
  - **Post-Codex rollback (same session):** Adversarial review via `codex:rescue` flagged 4 critical + 3 medium issues. Rolled back: jump-cut bullet from Technical-Flaws (contradicted "Single continuous shot" contract), entire Expression Phrase Bank (unverified CTR rankings), model duration enum tables in script-skill + video-director (Sora 2 Pro enums unverifiable, replaced with "check model docs" pointer), 2 pseudo-fix rows in video-director Iteration Protocol (lighting-via-character-bible + AI-slick-via-ambient-room-tone), entire `big-angle-spotter` CHARACTER LIKENESS Addendum (dead-weight post-run manual process in a thin-orchestrator skill). Remaining cherry-pick is verified, contradiction-free, and concise. Review output: Codex session via `codex:codex-rescue` subagent, 260421.
  - Inspired by: `krusemediallc/arcads-claude-code` (GitHub — 2 skills: `arcads-external-api`, `generate-youtube-thumbnail`)
  - Contributor: Jerel
- **`big-angle-spotter`** pipeline (global at `~/AI workflows/big-angle-spotter/`) — Added **Step 07b `angle_rationale`** between steps 7 and 8. Fresh Sonnet worker reads step 07 expansion, outputs exactly 3 paragraphs (120–180 words) in third-person descriptive voice: §1 uncomfortable truth, §2 angle + psychological trigger, §3 reframe. This 07b output is the strategic rationale that now populates column G (ANGLE) of the NeezaNizam CREATIVES sheet. Pipeline change at `scripts/run_pipeline.py` — STEP_7B constant + step tuple insertion + int/str step ID handling in `save_step_output` + `Any` import. Downstream: `scripts/ad_concept_sheet_writer.py:374` `_build_creatives_row()` prefers `angle_rationale` over short angle title (shipped same day, no schema break — falls back to `angle` for legacy trackers). Standalone backfiller `scripts/backfill_angle_rationale.py` patches existing DCT trackers post-hoc; surgical G-column patcher `scripts/patch_angle_cell.py` updates live cells with pre/post snapshots + HITL prompt. DCT1 + DCT2 back-patched in-session (G5/G6 updated).
  - Inspired by: Jerel's handoff feedback that column G should carry strategic reasoning, not a short label — reviewed against competitor sheet examples (Referral Dependency Exposure, Pipeline Fragility)
  - Contributor: Jerel
- **NeezaNizam Wave 1 DCT3** (`clients/neezanizam/campaigns/dct-260421/`) — Ran `big-angle-spotter` for Avatar 1 (Hesitant Calculator) with cross-pollinated EXISTING_ANGLES (DCT1 "Wrong Three Numbers" + DCT2 "Post-Split Unbuyability" + 7 saturated competitor angles). Pipeline produced angle **Spousal Deadlock** — wife-initiator / husband-hesitator reframe positioning the consultation as third-party arbitration rather than property advice. Blue-ocean territory: 0 of 15 active Propnex ads target the spousal-alignment axis (verified 260417 buyer-language refresh). Silver Bullet: *"The hesitating spouse isn't waiting for better numbers. They're waiting for someone who isn't you to tell them the numbers are right."* Top-3 headlines + 3 static ad prompts (rank1 cinematic two-person / rank2 split-screen couple / rank3 mock-document spreadsheet) + 3-paragraph 07b rationale produced. Tracker at `campaigns/dct-260421/dct-tracker.json` with ONE creatives[] entry and 3 nested visual_variants[] per 260420 locked sheet-row semantics. Pending: image generation → Canva assembly → sheet write (preview→HITL→write) → /ads:upload.
  - Contributor: Jerel (directed the Avatar 1 re-use + cross-pollination)

---

## 260324

### Updated
- **`website-design`** skill — Integrated 3 aesthetic modes (Soft, Minimalist, Brutalist) as new reference file `aesthetic-modes.md`. Added option 5 to Mode B Step 2 aesthetic direction. Added 4 banned patterns to `aesthetic-guidelines.md` (serif in dashboards, uncustomized shadcn defaults, emojis in markup, Space Grotesk). Added 3 fonts to `cinematic-presets.md` (Fraunces, Monument Extended, Switzer). Each mode defines complete palette, typography, surface treatment (Double-Bezel, ultra-flat, zero-radius), component rules, and motion philosophy translated to HTML+Tailwind+GSAP stack.
  - Inspired by: Leonxlnx/taste-skill (repo — soft-skill, minimalist-skill, brutalist-skill sub-skills)
  - Contributor: Jerel

---

## 260320

### Updated
- **`copy-editing`** skill — Sweep 8 quality gate (5-dimension scoring rubric, 35/50 minimum to deliver), 3 new sections in `overused-ai-patterns.md` (Performative Emphasis & Meta-Commentary, Vague Declaratives, Structural Anti-Patterns), new `de-ai-transformations.md` reference with 10 before/after examples. Checklist updated with quality gate item.
  - Inspired by: hardikpandya/stop-slop (repo — MIT, curated de-AI rubric + examples)
  - Contributor: Jerel

---

## 260319

### Created
- **`unslop`** skill (v1.0.0) — Domain-specific AI pattern detection using mshumer/unslop. Generates empirical avoidance profiles by sampling model defaults for specific content domains (LinkedIn posts, SaaS landing pages, emails, etc.). Becomes Layer 1 of the 4-layer de-AI stack: unslop profile (soft) → overused-ai-patterns (hard) → corrections.md (hard) → V.O.I.C.E. (positive target). Commands: `/unslop:profile`, `/unslop:refresh`, `/unslop:list`. Profiles stored in `skills/unslop/profiles/`, domain metadata in `references/domain-catalog.md`.
  - Inspired by: mshumer/unslop (tool — empirical AI default detection)
  - Contributor: Jerel

### Updated
- **`copy-editing`** skill — Sweep 8 (De-AI) now loads unslop profiles as Layer 1 soft constraints alongside overused-ai-patterns.md hard constraints. Updated process steps, checklist, and references.
- **`copywriting`** skill — Added De-AI Layer Loading section before writing to pre-load domain-matching unslop profiles.
- **`linkedin-content`** skill — Added Unslop Profile subsection under Banned AI Vocabulary for domain-specific layer loading.
- **`email-sequence`** skill — Added De-AI Layer Loading section for email-specific AI default avoidance.
- **`copywriter`** agent — Context Loading step 3.7 now loads matching unslop profile from `skills/unslop/profiles/`.
- **`brand-voice-guardian`** agent — Context Loading step 3.5 now loads matching unslop profile for content type review.
- Updated `skills-registry.json`, `routing-table.md`, `skills-catalog.md`, `commands.md` with unslop registration.

---

## 260317

### Updated
- **`website-design`** skill (v4.1.0 → v5.0.0) — Paper.design MCP integration for bidirectional visual design workflows. New Mode D (Paper-First) for importing designs from Paper and converting to HTML/Tailwind. Modes A-C enhanced with optional Paper push/pull when available. 24 MCP tools (11 read, 13 write) for design token extraction, JSX export, HTML preview. New reference file `paper-integration.md`. Paper integration docs added to `skills/integrations/paper/`. Updated registry, routing table, skills catalog, MCP integrations.
  - Inspired by: Paper.design (tool — MCP-enabled design editor)
  - Contributor: Jerel

---

## 260316

### Created
- **`meta-ads-uploader`** skill (v1.0.0) — End-to-end pipeline for uploading ad creatives to Meta (Facebook/Instagram). MetaAdsClient class with image/video upload, single + dynamic creative creation, PAUSED ad creation. CLI with validate/preview/upload-media/full/status commands. Creative bundle JSON format bridges copywriting + image-generation output → Meta API. Resumable runs via results sidecar file. Auto-converts WebP/TIFF/HEIC to PNG. HITL gates: bundle review, media confirm, creative preview, go-live (always PAUSED). Updated campaign-runner execution-playbook (Manual → meta-ads-uploader), skills-registry, dependency-graph, routing-table, skills-catalog, commands.
  - Inspired by: ScrapeCreatorsClient (pattern), Meta Marketing API v22.0 (API)
  - Contributor: Jerel

---

## 260315

### Created
- **`scrapecreators`** skill (v1.0.0) — Universal social intelligence API client for 25+ platforms. ScrapeCreatorsClient class with 100+ endpoint methods, CLI with subcommands per platform, auto-pagination, credit tracking, typed exceptions. Extracted and generalized from `tiktok-slideshows/scripts/competitor_scan.py`. Refactored competitor_scan.py to import from shared module.
  - Inspired by: ScrapeCreators API (service), competitor_scan.py (existing pattern)
  - Contributor: Jerel

---

## 260314

### Created
- **`autoresearch`** meta-skill (v1.0.0) — Autonomous skill optimization via Karpathy's generate → evaluate → mutate → keep/discard pattern. Global skill at `~/.claude/skills/autoresearch/`. 7 Python scripts (orchestrator, rubric_bootstrap, scenario_generator, safety, scheduler, trust_tracker, feedback_loop), 4 YAML templates, 1 deep reference doc, 12 slash commands. Phase 1 (MVP) active, Phases 2-4 scaffolded. Per-client isolation via `clients/<project>/autoresearch/`. Trust graduation L0→L3. Safety rails: budget caps, kill switch, auto-revert. ~$0.50-1.00/run.
  - Inspired by: Karpathy (person — [autoresearch](https://github.com/karpathy/autoresearch) pattern), Jerel (person — skill booster concept)
  - Contributor: Jerel

### Amplified
- **`video-director`** skill (v1.0.0 → v2.0.0) — Major upgrade: 11 → 14 video types (+Walk-and-Talk, Driver's Seat, At-Home Demo), 3 new reference files (character-bible-template, seed-management, client-campaign-audit), Sora 2 Pro platform features (Characters API, Video Edits, Clip Extension, Batch API, Storyboard Mode), UGC automation via Kie.ai, 8K shot prompting, emotional block dialogue cues, weak→strong prompt transformations, post-production pipeline, Creative Director pattern, seed bracketing (~60% cost reduction)
  - Inspired by: Mikoslab (11 PDFs — character bibles, 8K prompting, seed bracketing, post-production, campaign audit), OpenAI (Sora 2 Prompting Guide), Lucas Walter (UGC automation, 3 archetypes, Kie.ai pipeline)
  - Contributor: Jerel
- **`image-generation`** skill — Added NB Pro advanced features (style saving, annotation), two image workflows (Objects vs Characters paths), Seedream 4 character alternative
  - Inspired by: Mikoslab (NB Pro features), Jerel
  - Contributor: Jerel
- **`model-selection-guide.md`** reference — Added VEO 3.1 ingredients approach, production budget rule, image-to-video dominance (90%), two image workflows, Sora 2 Pro platform features (Characters API, clip extension 6x/120s, video edits, batch API, storyboard mode), Kie.ai API gateway, seed bracketing cross-reference, discrete duration values, creativity tradeoff
  - Inspired by: Mikoslab, OpenAI Sora 2 Guide, Lucas Walter
  - Contributor: Jerel
- **`cinematography-reference.md`** reference — Added 8K Shot Prompting section with camera body specifications (RED Komodo, ARRI Alexa LF, Sony FX6, Canon C70, Blackmagic 6K)
  - Inspired by: Mikoslab (8K shot prompting)
  - Contributor: Jerel
- **`realism-tricks.md`** reference — Added Post-Production Pipeline, Emotional Block Dialogue Cues, Weak→Strong Prompt Transformations, Image Input First-Frame Control, Dialogue Formatting Best Practice, Characters API + text fallback to Character Consistency Framework
  - Inspired by: Mikoslab (emotional blocks, post-production), OpenAI (dialogue formatting), Lucas Walter (weak→strong)
  - Contributor: Jerel
- **`nano-banana-full-guide.md`** reference — Added NB Pro advanced features, style prompt saving, annotation workflow, Seedream 4 character alternative
  - Inspired by: Mikoslab (NB Pro)
  - Contributor: Jerel
- **`tiktok-content.yaml`** template — Added slideshow script framework, viral format study step, character-based account option
  - Inspired by: Mikoslab (TikTok script framework)
  - Contributor: Jerel

### Updated
- `skills/skills-registry.json` — added autoresearch entry in specialized category
- `skills/dependency-graph.md` — added autoresearch to Meta Track
- `.claude/rules/routing-table.md` — added autoresearch to skills table
- `.claude/rules/skills-catalog.md` — added autoresearch to System Tools
- `.claude/rules/commands.md` — added 12 `/autoresearch:*` commands
- `commands/ops/weekly.md` — added Step 6: autoresearch rotation check
- `commands/ops/monthly.md` — added autoresearch summary section to knowledge hygiene

---

## 260313

### Created
- **`content-moat`** skill (v1.0.0) — Content ideation + layering strategy for copycat-resistant content. 5 originality frameworks (Collision, Proprietary Insight, Perspective Flip, Format Translation, Compound Stacking), 10-layer catalog with implementation guides, copycat resistance scoring, pipeline integration with video-director/image-generation/copywriting/linkedin-content. Verified via prompt-contract + verification-loop.
  - Inspired by: Jerel (person — observations on AI content wave), beechinour (person — layering concept), yangmun (person — format originality case study)
  - Contributor: Jerel
- **`video-director`** skill (v1.0.0) — AI video prompt generation for marketing ads. 11 video types, 3 pipelines (Direct, Image-First, Localized), 5-Part Prompt Formula, HITL review gates, full Production SOP, 4 reference files (video-type-catalog, realism-tricks, model-selection-guide, cinematography-reference)
  - Inspired by: David Roberts (AI Ad Guys — @recap_david), snubroot (Veo 3.1 Meta Framework — GitHub snubroot/Veo-3-Meta-Framework)
  - Contributor: Jerel
- **`changelog`** — Central change log with inspired-by attribution tracking
  - Inspired by: Jerel (person) — need for cross-session visibility into what changed
  - Contributor: Jerel

### Amplified
- **`image-generation`** skill — added HITL Prompt Review Gate, Video Reference Image Mode, `video-director` to related_skills
  - Inspired by: David Roberts (AI Ad Guys), Jerel (HITL philosophy)
  - Contributor: Jerel
- **`realism-tricks.md`** reference — added Character Consistency Framework, Transition Realism, Negative Prompt Format Guide
  - Inspired by: snubroot (Veo 3.1 Meta Framework)
  - Contributor: Jerel
- **`model-selection-guide.md`** reference — updated to Kling 3.0, added prompt length constraints table, technical specs
  - Inspired by: snubroot (Veo 3.1 Meta Framework)
  - Contributor: Jerel
- **`learnings.md`** (video-director) — added troubleshooting matrix, additional confirmed patterns
  - Inspired by: snubroot (Veo 3.1 Meta Framework)
  - Contributor: Jerel
- **`copywriting`** references — added cross-references to video-director in ad-creative-frameworks.md and video-ad-scripts.md
  - Inspired by: Jerel (pipeline integration)
  - Contributor: Jerel
- **`copywriter`** agent — added video-director to skill integrations
  - Inspired by: Jerel (pipeline integration)
  - Contributor: Jerel

### Updated
- **`amplifier`** skill — added changelog append step to Phase 4
  - Inspired by: Jerel (person) — changelog integration
  - Contributor: Jerel
- **`meta-builder`** skill — added changelog append on new artifact creation
  - Inspired by: Jerel (person) — changelog integration
  - Contributor: Jerel
- **`CLAUDE.md`** — added changelog step to Session End Protocol
  - Inspired by: Jerel (person) — changelog integration
  - Contributor: Jerel
