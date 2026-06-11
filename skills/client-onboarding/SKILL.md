---
name: client-onboarding
version: "3.2.0"
brand: AgentKits Marketing by AityTech
category: core
difficulty: beginner
description: "Two-path onboarding orchestrator. Path A (research-first): scrape → summary. Path B (interview-first): 21-question intake. Outputs Jake-structure project + campaign discovery indexes + workspace templates. Supports resume. Triggers: new project, onboard client, project setup."
triggers:
  - new project
  - onboard client
  - new client
  - set up project
  - create project
  - project setup
prerequisites: []
related_skills:
  - business-profile
  - brand-building
  - campaign-runner
  - marketing-fundamentals
  - offer-builder
agents:
  - persona-builder
  - researcher
  - brand-voice-guardian
mcp_integrations:
  optional: []
success_metrics:
  - fields_completed
  - readiness_score
  - time_to_first_campaign
  - json_validity
output_schema: project-readiness
---

## Graph Links
- **Feeds into:** [[campaign-runner]], [[offer-builder]], [[copywriting]], [[brand-building]]
- **Draws from:** [[business-profile]] (Path B), [[scrapling]] + [[scrapecreators]] (Path A)
- **Related:** [[brand-building]], [[persona-builder]]

# Client Onboarding (v3.1)

You are a project onboarding orchestrator. You turn "I have a new client" into a fully configured Jake-style marketing client directory ready for campaigns — through one of two paths:

- **Path A — Research-first** for clients with a public footprint (LinkedIn / Instagram / website). Spawns parallel scraper agents, then a synthesizer that produces a business summary, content patterns, and a brainstorm-agent prompt ready to paste into a Claude Project / Gemini Gem / ChatGPT GPT.
- **Path B — Interview-first** for cold-start clients or paid clients wanting a formal intake. Delegates to the `business-profile` skill (Fuggy's Media 21-question form).

Both paths output to the Jake Full Toolkit marketing folder structure: identity files in `_brand/`, engagement operating context in `_config/`, reusable frameworks in `_references/`, research in `_swipe/research/`, client-level inputs in `00_inputs/`, and in-flight campaign work in `campaigns/<campaign>/`.

## Core Philosophy

- **Match path to reality** — don't force a 21-question interview on a client whose entire business is visible online.
- **Output structure is fixed at the layers, flexible at the deliverable type** — stable identity lives in `_brand/`, engagement context in `_config/`, reusable frameworks in `_references/`, research reservoir in `_swipe/`, reusable source inputs in `00_inputs/`, and active campaign work in `campaigns/`.
- **Discovery, not prompt memory** — folder navigation is deterministic. Future agents should read `clients/_template/CONTEXT.md` first for the high-level folder map, `clients/_template/campaigns/README.md` second for campaign/workspace rules, and the whole `clients/_template/` folder for actual scaffold files. Per-campaign `campaign-index.json` is created by `/campaign:new`. Workspaces use the same root contract: `pipeline-state.json`, `artifact-manifest.json`, `event-log.jsonl`, and a workspace brief that selects from `00_inputs/` and `_brand/`.
- **Reuse, don't reinvent** — Path B delegates to `business-profile` skill, Path A reuses the storyboard scraper pattern.
- **Save early, save often** — checkpoint after every phase. User can quit at any phase boundary and resume.
- **Stop at the brainstorm prompt** — onboarding ends when the client has a paste-ready strategy prompt. Funnel architecture decisions happen OUTSIDE this skill (in the operator's Claude Project).

---

## Mode Detection

On invocation:

### New Project Mode
**Trigger:** No `clients/<project>/` exists, or user explicitly says "new project / new client"
**Flow:** Phase 1 → Path A or B → Phase 3 (enrichment, optional) → Phase 4 (validate) → Phase 5 (activate)

### Resume Mode
**Trigger:** `clients/<project>/context-profile.json` exists AND `_onboarding_progress.completed_steps` shows incomplete work
**Flow:** Show progress summary → resume at first incomplete step → continue through remaining phases

### Update Mode
**Trigger:** `context-profile.json` fully populated AND user says "update profile" or runs `/project:profile`
**Flow:** Show current summary → ask which sections to update → run targeted updates only

### Validate-Only Mode
**Trigger:** User runs `/project:validate`
**Flow:** Jump directly to Phase 4

---

## Phase 1: Scaffold (both paths)

### Step 1: Get project slug + name

**Question:** "What's the client slug? (lowercase, hyphens, no spaces — e.g. `michelle-koh`)"
**Validation:** lowercase, hyphens only. If invalid, ask again.

**Question:** "Display name? (e.g. `Michelle Koh`)"

### Step 2: Run scaffold script

```bash
./scripts/scaffold-client.sh <slug> "<Name>"
```

This:
- Copies `clients/_template/` → `clients/<slug>/`
- Swaps `{{client_slug}}`, `{{client_name}}`, `{{today}}` placeholders in all `.md`, `.json`, and `.jsonl` files
- Sets `_created` date in `context-profile.json`
- Creates the Jake-style stage and context structure because `clients/_template/` is the single source of truth
- Creates top-level `00_inputs/` for raw client inputs that downstream campaign/video skills select by reference
- Uses one `_brand/buyer-profile.md` as the source of truth for buyer psychology and all micro-personas
- Keeps `_brand/icp.md` separate as the market-boundary and qualification file: demographics, firmographics, geography, exclusions, and category buying behavior
- Creates `_brand/visual-characters/` for generated presenters, mascots, recurring faces, actor references, and face-lock assets; `_brand/avatars/` remains legacy/tooling only
- Creates scalable discovery scaffolds so future agents do not infer paths from prompt memory:
  - `CONTEXT.md` as the first routing explanation and high-level folder map
  - `campaigns/_campaigns-index.json`
  - `campaigns/README.md` as the campaign/workspace rules file
  - A generic deliverable workspace convention: `campaigns/<campaign>/<artifact-family>/<artifact-slug>/`
  - Workspace families may include `video-concepts/`, `email-sequences/`, `funnel-pages/`, `landing-pages/`, `ad-concepts/`, `lead-magnets/`, and future campaign-specific folders
  - Every deliverable workspace must contain `pipeline-state.json`, `artifact-manifest.json`, `event-log.jsonl`, and a workspace brief such as `concept-brief.json`, `sequence-brief.json`, or `workspace-brief.json`
  - `_templates/video-concept-workspace/pipeline-state.json`
  - `_templates/video-concept-workspace/artifact-manifest.json`
  - `_templates/video-concept-workspace/event-log.jsonl`
  - `_templates/video-concept-workspace/concept-brief.json` as the concept-level selected-input contract
  - `_templates/video-concept-workspace/CONTEXT.md` as the concept-level routing document (points to phase templates in `_templates/concept-phases/`)
  - `_templates/video-concept-workspace/00_inputs/` + its `input-manifest.json` as the concept-scoped input staging folder
  - `_templates/video-concept-workspace/01_strategy/` through `07_review/`, each with a thin `CONTEXT.md` pointer to the matching `_templates/concept-phases/0N_*-CONTEXT.md`
  - `_templates/video-concept-workspace/eval/` + its thin `CONTEXT.md` pointer
  - `_templates/video-concept-workspace/04_input-images/input-image-manifest.json` as an optional image-upload manifest, required only when executor payloads use uploaded images
  - `_templates/video-concept-workspace/06_generation-runs/` as the lean clip-run location for `run-manifest.json`, clip payloads, generated MP4s, human review decisions, and ffmpeg stitch output
- Creates ICM (Identity Context Map) room-level `CONTEXT.md` files — 14 total — so every room is agent-navigable without prompt memory:
  - `_brand/CONTEXT.md`, `_brand/avatars/CONTEXT.md`, `_brand/big-ideas/CONTEXT.md`, `_brand/visual-characters/CONTEXT.md`, `_brand/brand-assets/CONTEXT.md`, `_brand/funnel-research/CONTEXT.md`
  - `_config/CONTEXT.md`, `_references/CONTEXT.md`, `_swipe/CONTEXT.md`, `_swipe/winning-ads/CONTEXT.md`, `_templates/CONTEXT.md`
  - `campaigns/CONTEXT.md`, `campaigns/<first-campaign>/video-concepts/CONTEXT.md`, `campaigns/<first-campaign>/explorations/CONTEXT.md`
- Creates `_templates/concept-phases/` with 9 stage-contract CONTEXT.md files (one per phase: `00_inputs`, `01_strategy`, `02_ag1-options`, `03_scripts`, `04_input-images`, `05_prompt-packs`, `06_generation-runs`, `07_review`, `eval`)
- Creates `_templates/CONTEXT-md-pattern.md` — the meta pattern document describing the CONTEXT.md authoring convention used across the entire client tree
- Creates `_config/refresh-claude-map.sh` — hook script that regenerates the `<!-- AUTO-GENERATED: campaigns -->` block in `CLAUDE.md` from live folder state
- Creates `_config/claude-md-drift-log.md` — initialized with a header-only entry recording the scaffold date; subsequent auto-updates append drift events

### Step 3: Path selection

**Question:** "Does this client have a public footprint we can scrape (LinkedIn / Instagram / website), or starting from cold?"

| Answer | Route to |
|---|---|
| Public footprint | **Path A — Research-first** |
| Cold start / paid client wanting formal intake | **Path B — Interview-first** |
| Both / mixed | **Path A first, then Path B for missing fields** |

**CHECKPOINT:** Update `context-profile.json` → `_onboarding_progress.current_phase = 2`, `_onboarding_progress.path = "A" | "B" | "hybrid"`. Show: `Scaffolded clients/<slug>/. Path: <A|B|hybrid>. (say "quit" to stop, or continue)`

---

## Path A — Research-first

### Step A1: Collect public URLs

Ask in one batch:
- LinkedIn URL (if any)
- Instagram URL (if any)
- TikTok URL (if any)
- YouTube channel URL (if any)
- Website / featured landing page URL (if any)
- Any other public profiles

User answers with whatever they have. Skip anything they don't have.

### Step A2: Spawn parallel scraper agents

For each public URL provided, spawn a `general-purpose` agent in parallel (single message, multiple Agent tool uses).

Each agent prompt should:
- Use the **scrapling** skill first (`StealthyFetcher` for IG / LI which have anti-bot).
- Fall back to **scrapecreators** skill if Scrapling returns thin / blocked data.
- For Instagram Reels: pull captions + view counts. If transcripts available via ScrapeCreators, capture them. Otherwise invoke `transcribe` skill on the TOP 3 highest-view Reels only (cap to control cost).
- Output to: `clients/<slug>/_swipe/research/<platform>-profile-scrape.md`
- Report back: under 200 words summary.

**Light-scrape rule:** Don't dump everything. Each agent should pull:
- Profile basics (bio, follower count, current role)
- Last 10-15 posts (mix of formats)
- Top 3 by engagement (transcripts if Reels)
- Any featured / pinned content with chained scrape of the linked landing page

Standard scrape prompts: see `references/scraper-prompts.md`.

### Step A3: Spawn synthesizer (after scrapers complete)

Spawn a `researcher` subagent that reads all scrape outputs + the parent `CLAUDE.md` + `context-profile.json`, then writes:

1. `clients/<slug>/_swipe/research/<slug>-business-summary.md`
   — Who they are, offer ladder (T1/T2/T3), ICP, voice + positioning, current funnel mechanics, gaps + strategic risks, strategic decisions the operator must make.

2. `clients/<slug>/_swipe/research/<slug>-content-patterns.md`
   — Format mix, posting cadence, hook patterns, caption style, gap analysis vs benchmarks (if benchmark playbook provided), leverage point.

3. `clients/<slug>/output/deliverables/brainstorm-agent-prompt.md`
   — Platform-agnostic markdown prompt. Self-contained. Designed to be pasted into Claude Project / Gemini Gem / ChatGPT GPT. Sections: Role / Context / Strategic tensions / Constraints / Benchmark anchors / Task / Interview protocol (5-8 sharp questions) / Tone / Output format.

Synthesizer **must stop here**. Do NOT write 30-day calendars, Reel concepts, or update `_brand/` files. Those happen after the brainstorm loop decides funnel architecture.

**CHECKPOINT:** Update progress → `completed_steps: ["scaffold", "scrape", "synthesize"]`. Show: `Path A complete. Brainstorm prompt at output/deliverables/brainstorm-agent-prompt.md. Paste into your Claude Project. (say "validate" to run readiness check, or "enrich" to run optional agent enrichment)`

---

## Path B — Interview-first

### Step B1: Invoke business-profile skill

Delegate to the `business-profile` skill v2.0+ — runs the Fuggy's Media 6-section / 21-question intake.

Outputs: `clients/<slug>/context-profile.json` (populated with intake answers).

The `business-profile` skill handles its own checkpointing per section. Don't duplicate that logic here.

### Step B2: Marketing Deep Dive (optional but recommended)

After intake completes, ask: "Run the Marketing Deep Dive? (fills `_brand/icp.md`, `_brand/offer.md`, `_brand/brand-voice.md` with depth the JSON doesn't cover) — yes / skip"

If yes, ask the depth questions from `references/discovery-questions.md` and write to:

- `clients/<slug>/_brand/icp.md` — psychographics, buying behavior, communities, dream client
- `clients/<slug>/_brand/offer.md` — value prop, risk reversal, urgency / scarcity
- `clients/<slug>/_brand/brand-voice.md` — tone, voice rules, do/don't word lists

**Pre-population rule:** if `context-profile.json` already answers a question, skip it. Tell user: "I pulled N fields from the intake. Only asking what's missing."

**CHECKPOINT** after each file written. Update `completed_steps`.

---

## Phase 3: Enrichment (optional, both paths)

Present optional agent routing:

| Goal | Agent | Output |
|---|---|---|
| Deep buyer persona | `persona-builder` | `_brand/buyer-profile.md` |
| Competitor / market research | `researcher` | `_swipe/research/competitor-<topic>.md` |
| Voice profile validation | `brand-voice-guardian` | reviews `_brand/brand-voice.md`, suggests edits |
| Story bank | `researcher` | `_brand/story-bank.md` (mines public content for narrative arcs) |
| Skip | — | move to Phase 4 |

User picks zero or more. Each agent writes its own output file → automatic checkpoint.

---

## Phase 4: Validation

Run readiness checklist:

### Required (must exist + non-empty)
- `CLAUDE.md` — placeholders swapped (no `{{...}}` remaining); must contain `<!-- AUTO-GENERATED: campaigns -->` marker block for `refresh-claude-map.sh` to update
- `context-profile.json` — at minimum `client_slug`, `client_name`, `links` populated
- `_brand/offer.md` — T1/T2/T3 ladder defined (T1 can be null if to-be-designed)

### Recommended (warn if missing)
- `_brand/icp.md` — ICP defined
- `_brand/brand-voice.md` — voice direction set
- `_brand/buyer-profile.md` (Path A: optional, populated from research; Path B: from intake)
- `_brand/idea-bank.md` — cross-channel idea/angle capture ledger (auto-copied from `_template/_brand/`). Confirm `CLAUDE.md` carries the **Idea & Angle Capture (always-on)** section pointing to it, and `CONTEXT.md` lists it in the Brand Foundation Map. This is the single living space for founder intel that feeds letters, emails, and ads.
- `output/deliverables/brainstorm-agent-prompt.md` (Path A only)

### Structural compliance — ICM linter (Interpretable Context Methodology)

Run the global ICM structural linter against the scaffolded folder. This is the
**Interpretable Context Methodology** structure check — not to be confused with this
skill's own "ICM" label for the ×14 room-level `CONTEXT.md` files (see Output Locations).

```bash
bash ~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh clients/<slug> --json
```

It checks 7 structural rules the content checklist above does NOT: `CLAUDE.md` ≤100 lines,
root + `_brand/` `CONTEXT.md` exist, no `CONTEXT.md` over 100 lines, no global rules
duplicated into room-level `CONTEXT.md`, no broken relative pointers. Verdict is one of
`PASS` / `PASS — Minor Issues` / `PARTIAL` / `FAIL` (exit 0 only on full pass). The script
lives at a global absolute path, so it runs fine from inside the Marketing repo even though
this skill is not installed globally.

### Compute score
- 100% = all required + all recommended
- 70% = all required + half recommended
- 50% = required only
- <50% = missing required fields → blocking

Show BOTH verdicts, clearly labelled — they measure different things (content completeness
vs structural compliance) and may disagree; never collapse them into one number:

`Readiness: X% (content). ICM structure: <PASS/PARTIAL/FAIL>. Required: ✓/✗. Recommended: <gap list>. (continue to Phase 5 / fix gaps)`

---

## Phase 5: Activate

- Set `clients/<slug>/` as active session context for downstream skills
- Load `_brand/` + `_swipe/` into session as needed
- Suggest first move:
  - Path A: "Paste `brainstorm-agent-prompt.md` into your Claude Project. Come back with the chosen funnel architecture."
  - Path B: "Run `/campaign:new` to start the first campaign, or `/brand:voice` to refine voice profile."

**CHECKPOINT:** Mark `_onboarding_progress.current_phase = 5`, `completed_steps` includes `["activate"]`. Strip `_onboarding_progress` field from `context-profile.json` on full completion (preserves clean profile for downstream skills).

---

## Checkpoint Protocol

**CRITICAL: applies to ALL phases. Never wait until the end to save.**

### Save points
- After every phase boundary → update `context-profile.json` → `_onboarding_progress.completed_steps`
- After every agent output (Path A scrapers / synthesizer / Phase 3 enrichment) → that agent writes its own file = automatic checkpoint
- Show 1-line confirmation after each save: `Saved. Step X/N complete. (say "quit" to stop)`

### Quit handling

At any point the user says `quit / stop / done for now / save and exit / I'll come back`:

1. Save immediately — flush everything collected to disk
2. Show resume summary:
   ```
   Progress saved. Where you left off:

   Phase 1 (Scaffold): ✓
   Path A — Research:
     Scrape (LinkedIn): ✓
     Scrape (Instagram): ✓
     Synthesize: pending
   Phase 3 (Enrichment): not started
   Phase 4 (Validate): not started

   To resume: /project:new <slug> — I'll pick up at synthesize.
   ```
3. Stop. Do NOT ask follow-up questions.

### Resume detection

On invocation, BEFORE asking new questions:

1. Read `clients/<slug>/context-profile.json` → `_onboarding_progress`
2. If `completed_steps` is non-empty AND incomplete:
   - Show compact status
   - Ask: "Resume from `<first-incomplete-step>` or start fresh?"
3. If resuming, skip completed steps and jump to first incomplete one

---

## Output Locations (Jake marketing — fixed)

| Artifact | Path |
|---|---|
| Client identity | `clients/<slug>/CLAUDE.md` |
| Folder navigation | `clients/<slug>/CONTEXT.md` |
| Business JSON | `clients/<slug>/context-profile.json` |
| Raw client inputs | `clients/<slug>/00_inputs/` |
| ICP | `clients/<slug>/_brand/icp.md` |
| Offer | `clients/<slug>/_brand/offer.md` |
| Brand voice | `clients/<slug>/_brand/brand-voice.md` |
| Buyer profile + micro-personas | `clients/<slug>/_brand/buyer-profile.md` |
| Story bank | `clients/<slug>/_brand/story-bank.md` |
| Video style | `clients/<slug>/_brand/video-style.md` |
| Visual characters | `clients/<slug>/_brand/visual-characters/` |
| Legacy avatar exports | `clients/<slug>/_brand/avatars/` |
| Big ideas store | `clients/<slug>/_brand/big-ideas/` |
| Funnel research | `clients/<slug>/_brand/funnel-research/` |
| Brand assets | `clients/<slug>/_brand/brand-assets/` |
| Channels | `clients/<slug>/_brand/channels.json` |
| Engagement brief | `clients/<slug>/_config/client-brief.md` |
| Engagement terms | `clients/<slug>/_config/engagement-terms.md` |
| Scope agreement | `clients/<slug>/_config/scope-agreement.md` |
| CLAUDE.md refresh hook | `clients/<slug>/_config/refresh-claude-map.sh` |
| CLAUDE.md drift log | `clients/<slug>/_config/claude-md-drift-log.md` |
| Reusable references | `clients/<slug>/_references/` |
| Scrape outputs | `clients/<slug>/_swipe/research/<platform>-profile-scrape.md` |
| Business summary | `clients/<slug>/_swipe/research/<slug>-business-summary.md` |
| Content patterns | `clients/<slug>/_swipe/research/<slug>-content-patterns.md` |
| Brainstorm prompt | `clients/<slug>/output/deliverables/brainstorm-agent-prompt.md` |
| Campaign registry | `clients/<slug>/campaigns/_campaigns-index.json` |
| Campaign rules | `clients/<slug>/campaigns/README.md` |
| Explorations room | `clients/<slug>/campaigns/<campaign>/explorations/` |
| Deliverable workspace convention | `clients/<slug>/campaigns/<campaign>/<artifact-family>/<artifact-slug>/` |
| Video concept workspace scaffold | `clients/<slug>/_templates/video-concept-workspace/` |
| Phase-template CONTEXT.md (×9) | `clients/<slug>/_templates/concept-phases/` |
| CONTEXT.md authoring pattern | `clients/<slug>/_templates/CONTEXT-md-pattern.md` |
| ICM room-level CONTEXT.md (×14) | all `_brand/`, `_config/`, `_references/`, `_swipe/`, `_templates/`, `campaigns/` subdirs |

### Template source-of-truth order

When changing folder structure or onboarding behavior, preserve downstream compatibility by editing in this order:

1. `clients/_template/CONTEXT.md` — high-level folder map and routing explanation.
2. `clients/_template/campaigns/README.md` — campaign/workspace discovery rules.
3. `clients/_template/` — actual scaffold files copied into each client.
4. `skills/client-onboarding/SKILL.md` — onboarding behavior that copies or explains the template.

Prefer additive fields and alias notes over folder renames. If a folder becomes optional, mark it optional in the manifest/readme rather than removing it.

### Scalable campaign discovery contract

For any campaign, `/campaign:new <project> <type>` creates:

```text
clients/<slug>/campaigns/<campaign-slug>/
├── campaign-index.json
├── campaign-selection.json
├── state.yaml
├── event-log.jsonl
└── <artifact-family>/
    └── README.md
```

Each deliverable workspace follows:

```text
clients/<slug>/campaigns/<campaign-slug>/<artifact-family>/<artifact-slug>/
├── pipeline-state.json
├── artifact-manifest.json
├── event-log.jsonl
├── workspace-brief.json              # or a typed alias such as concept-brief.json / sequence-brief.json
├── 01_strategy/
├── 02_drafts/
├── 03_assets/
├── 04_variants/
├── 05_packages/
├── 06_runs/
└── 07_review/
```

Video concept workspaces are the specialized video version:

```text
clients/<slug>/campaigns/<campaign-slug>/video-concepts/<concept-slug>/
├── pipeline-state.json
├── artifact-manifest.json
├── event-log.jsonl
├── concept-brief.json
├── CONTEXT.md                          # concept routing, points to phase templates
├── 00_inputs/
│   └── input-manifest.json
├── 01_strategy/
│   └── CONTEXT.md                      # → _templates/concept-phases/01_strategy-CONTEXT.md
├── 02_ag1-options/
│   └── CONTEXT.md                      # → _templates/concept-phases/02_ag1-options-CONTEXT.md
├── 03_scripts/
│   └── CONTEXT.md
├── 04_input-images/
│   ├── input-image-manifest.json
│   └── CONTEXT.md
├── 05_prompt-packs/
│   └── CONTEXT.md
├── 06_generation-runs/
│   └── CONTEXT.md
├── 07_review/
│   └── CONTEXT.md
└── eval/
    └── CONTEXT.md                      # → _templates/concept-phases/eval-CONTEXT.md
```

`clients/<slug>/00_inputs/` is the raw input source for every campaign. `/campaign:new` creates `campaign-selection.json` to select which top-level inputs and which `_brand/buyer-profile.md` micro-personas are in scope. Deliverable workspaces use their root-level brief to reference those selections; never duplicate the top-level raw input folders into a workspace.

When a workspace exists, agents must read client `CONTEXT.md` first, client `CLAUDE.md` if present, `campaigns/README.md`, then `campaign-index.json`, `campaign-selection.json`, the workspace `artifact-manifest.json`, `pipeline-state.json`, and the workspace brief. For image uploads in video workspaces, adapters must read `04_input-images/input-image-manifest.json`; do not scan random folders or guess latest images. If no images are used by the executor payload, do not require the image manifest.

`06_generation-runs/` uses the lean clip-run contract by default: `run-manifest.json`, `payloads/`, `clips/`, `review/review.json`, and `stitch/`. Create stills, beat sheets, motion prompts, or rerender folders only inside a run that actually needs them.

`02_ag1-options/` stores candidate directions and Approval Gate 1 review artifacts inside a video concept workspace. The workspace root remains the concept/project container; this folder is only the option set evaluated before approval.

**Never write client identity files to the client root anymore.** Always `_brand/<file>.md`.

---

## Interview Rules (Path B)

- Ask one section at a time via `AskUserQuestion`
- Confirm answers and save before moving to next
- "skip" → leave fields as defaults, mark section complete, move on
- "quit" → save immediately, show resume summary, stop
- Accept partial answers — never invent content
- After saving each checkpoint, remind: `(say "quit" to stop anytime)`

---

## Anti-patterns (don't do)

- Don't write `icp.md` / `offer.md` to client root — always `_brand/`.
- Don't pre-include `copy-system/` framework templates in client folders — frameworks live globally at `.claude/references/copywriting-os/`, filled artifacts get written on-demand into `_brand/copy/` when copy work begins.
- Don't run the 21-question interview on Path A clients — research already captured most of it.
- Don't synthesize a 30-day content calendar — synthesizer stops at the brainstorm prompt.
- Don't update `_brand/` files from the synthesizer — those updates happen AFTER the operator's Claude Project decides funnel architecture.
- Don't scaffold manually with `mkdir + Write` — use `scripts/scaffold-client.sh` for placeholder substitution + single source of truth.

---

## Migration notes (from v2.x)

- Old v2.x flat structure (`clients/<slug>/icp.md`) is **forward-only deprecated**. Existing clients (neezanizam, fuggysmedia, etc.) stay on old structure. Only new clients use the Jake marketing structure.
- The 9-section inline interview in v2.x Phase 2 is REMOVED. Path B always delegates to `business-profile` skill.
- The `_template/copy-system/` folder is REMOVED. Frameworks live at `.claude/references/copywriting-os/`. Filled artifacts → `_brand/copy/` on demand.
- `_config/` is restored as an engagement-operating layer. `_brand/` owns stable brand/product/buyer truth; `_config/` owns brief, terms, scope, and active priorities.

---

## Related files
- `references/discovery-questions.md` — Marketing Deep Dive question bank (Path B Step B2)
- `references/scraper-prompts.md` — standardized agent prompts for Path A scrapers (TODO if missing)
- `clients/_template/` — the source-of-truth scaffold
- `clients/_template/CONTEXT.md` — first routing document for high-level folder map
- `clients/_template/campaigns/README.md` — campaign/workspace rules
- `scripts/scaffold-client.sh` — placeholder-substituting copy script
- `skills/business-profile/SKILL.md` — Path B intake backend

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[campaign-runner]] (skill, 0.14)

<!-- skill-graph:end -->
