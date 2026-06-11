# CONTEXT — _smoketest2 Root

## What lives here

VitalKit Labs's client workspace. Jake Full Toolkit architecture adapted for marketing delivery: stable context (L3) is separated from per-run campaign execution (L4), and every stage has an explicit output handoff. This file (L1) is the folder map and stage-routing law for the client.

## Entry Protocol

Run these checks in order before anything else. Other agents and orchestrators (vid-director, etc.) treat this section as canonical for client-level entry.

1. **RESUME CHECK (mandatory first action):** Read `campaigns/_campaigns-index.json`. If any campaign has `status: "active"` AND a non-empty `active_workspaces[]`, halt fresh-start work and surface a Resume Card per `campaigns/README.md` § Resume Protocol. Ambiguous phrasing ("help me get started", "let's make an ad", "what's next") MUST NOT force a cold-start when active workspaces exist. Proceed to fresh-start only when the operator explicitly confirms "start a fresh concept" or "new campaign".
2. **Read order:** `CLAUDE.md` (routing law, overrides everything) → this `CONTEXT.md` (folder map + entry protocol) → `context-profile.json` (client facts) → § How to use it below for L2 reading order.
3. **Conflict rule:** when an agent's own `.md` describes a workspace path that conflicts with `CONTEXT.md` or `campaigns/README.md`, **CONTEXT.md and campaigns/README.md win.** Agent files describe one agent's I/O contract — never the workspace's canonical structure. (Resume sessions previously skipped CONTEXT.md and treated agent specs as truth, manufacturing false path conflicts.)

## Layer Map

| Layer | Files | Purpose |
|---|---|---|
| L0 | `CLAUDE.md`, `context-profile.json` | Always-on identity and project facts |
| L1 | `CONTEXT.md` | This routing file |
| L2 | `00_inputs/`, numbered stage `CONTEXT.md` files | Client input bank plus stage contracts and handoff rules |
| L3 | `_brand/`, `_config/`, `_references/`, `_swipe/` | Stable or reusable context (read `_brand/CONTEXT.md` first) |
| L4 | campaign folders, typed deliverable workspaces, video runs, outputs | Per-run working artifacts; campaigns use discovery indexes |

## Brand Foundation Map

Keep buyer files separated by job, not by habit:

| File / Folder | Job | Do Not Use For |
|---|---|---|
| `_brand/icp.md` | Market boundary: demographics, geography, eligibility, exclusions, category buying behavior | Buyer psychology or ad-targeting micro-personas |
| `_brand/buyer-profile.md` | Buyer psychology: core emotional problem, fears, past solutions, transformation, 3-7 micro-personas | Demographic ICP qualification or campaign-specific creative |
| `_brand/idea-bank.md` | Living cross-channel capture of fresh angles, founder intel, campaign ideas (persona × channel × status). Feeds letters, emails, ads. | The locked strategy spine (`big-ideas/`) or finished proof stories (`story-bank.md`) |
| `_brand/visual-characters/` | Optional generated presenters, mascots, recurring faces, character references | Buyer targeting |
| `_brand/avatars/` | Legacy/tooling exports only when an older workflow requires one-file-per-avatar files | Canonical buyer targeting |

Campaigns select `micro_persona_id` values from `_brand/buyer-profile.md`; they never copy or fork buyer profiles. Full `_brand/` file map: `_brand/CONTEXT.md`.

## Stage Map

| Stage | Purpose | Output | Review Gate |
|---|---|---|---|
| `00_inputs` | Reusable input bank: product, market/buyer, competitors, research | `00_inputs/input-manifest.json` | Indexed before campaigns/concepts select |
| `01_research` | Market, buyer, competitor, product, source-of-truth research | `01_research/output/` | Synthesized before concept/script work |
| `02_script` | Legacy/non-campaign drafts only. **All campaign video concept work lives under `campaigns/<campaign>/video-concepts/<concept-slug>/02_ag1-options/` + `/03_scripts/` — never inside `02_script/`.** | `02_script/output/` (legacy only) | User approves direction before production |
| `03_production` | Input assets, image prompts, beat sheets, render prompts | `03_production/output/` | User approves images, beat sheets, prompts before render |
| `04_review` | Internal/client review, revision notes, QA, compliance checks | `04_review/output/` | Approved or returned to 02/03 with scoped notes |
| `05_handoff` | Final delivery, documentation, lessons, promoted assets | `05_handoff/output/` | Deliverable accepted, learnings captured |
| `06_measure` | Weekly analytics snapshot + scorecard; feeds findings back to 01_research | `06_measure/output/` | Insights promoted to `_brand/learnings.md` |

## How to use it

1. Read this `CONTEXT.md` first for the folder map and routing.
2. Read `CLAUDE.md` + `context-profile.json` for local rules and client identity.
3. For campaign/workspace rules, read `campaigns/README.md` before guessing paths.
4. Read `00_inputs/input-manifest.json` when the task needs product, market/buyer, competitor, or research inputs.
5. Load `_brand/` (start at `_brand/CONTEXT.md`) for stable brand, product, buyer, offer, claim, visual-character, video-style context, and `_brand/higgsfield-reference-routing.json` for video prompt routing.
6. Load `_config/` for this engagement's brief, scope, priorities, terms; `_references/` + `_swipe/research/` only for reusable frameworks or source research.
7. Work inside the active numbered stage or `campaigns/<campaign>/`, then write reviewed final assets to `output/deliverables/`.

## Campaign Discovery

For campaign work, read in order: `campaigns/_campaigns-index.json` → `campaigns/<campaign>/campaign-index.json` → `campaign-selection.json` → the active workspace `artifact-manifest.json` → `pipeline-state.json` → workspace brief. Do not guess paths.

Generic campaign workspaces follow `campaigns/<campaign>/<artifact-family>/<artifact-slug>/` (e.g. `video-concepts/`, `email-sequences/`, `funnel-pages/`, `ad-concepts/`). Each owns `pipeline-state.json`, `artifact-manifest.json`, `event-log.jsonl`, and a typed brief.

AI-video concept workspaces (`campaigns/<campaign>/video-concepts/<concept-slug>/`) specialize this pattern with phase folders `00_inputs/`…`07_review/` plus `eval/`. `concept-brief.json` is the canonical selected-input contract — it references `00_inputs/input-manifest.json` entries and must not duplicate client-level input folders. Legacy alias `concept-input-packet.json` is accepted in older workspaces only. `02_ag1-options/` is the AG1 review pack, not a second concept root. Each phase folder's `CONTEXT.md` points to the canonical stage contract at `_templates/concept-phases/<phase>-CONTEXT.md` — do not write stage contracts in phase folders.

**Simple concept route:** for "generate concepts" / "run the concept stage" / "create AG1 options" from inside a concept workspace, route through `concept-brief.json` + `01_strategy/creative-diversity-map.json` + the `video-concept-lab` rubric → the `video-concept-seeder` agent → `02_ag1-options/concepts-draft.json` → Phase 4 synthesis (`concept-pack.{md,json,html}` + `approval-1.json`). `video-concept-lab` is methodology only, not a second generator. If `concept-brief.json` or `creative-diversity-map.json` is missing, stop and create/approve those first.

## Active phase

Currently: **not-started** — no active phase until onboarding chooses a path. Next: [the next phase + trigger condition].
