# CONTEXT — _smoketest Root

> FICTIONAL SMOKE-TEST DATA — client "Meridian Property Advisory" is not a real client. Regression baseline.

## What lives here

Meridian Property Advisory's client workspace. Jake Full Toolkit architecture adapted for marketing delivery: stable context is separated from campaign execution, and every stage has an explicit output handoff.

## Entry Protocol

Before doing anything else, run these checks in order. Other agents and orchestrators (vid-director, etc.) treat this section as canonical for client-level entry.

1. **RESUME CHECK (mandatory first action):** Read `campaigns/_campaigns-index.json`. If any campaign has `status: "active"` AND its `active_workspaces[]` array is non-empty, halt fresh-start work and surface a Resume Card per `campaigns/README.md` §Resume Protocol. Ambiguous operator phrasing ("help me get started", "let's make an ad", "what's next") MUST NOT force a cold-start when active workspaces exist. Only proceed to fresh-start when the operator explicitly confirms "start a fresh concept" or "new campaign".

2. **Read order precedence:**
   - `CLAUDE.md` (routing law) — overrides everything below
   - `CONTEXT.md` (this file — folder map + entry protocol)
   - `context-profile.json` (client facts)
   - Then proceed to "How to use it" below for level-2 reading order.

3. **Conflict rule:** when an agent's own `.md` (e.g. `~/.claude/agents/<name>.md`) describes a workspace path that conflicts with what `CONTEXT.md` or `campaigns/README.md` documents, **CONTEXT.md and campaigns/README.md win.** Agent files describe one agent's I/O contract — they are NEVER the workspace's canonical structure. This rule exists because resume sessions previously skipped CONTEXT.md and treated agent-file specs as workspace truth, manufacturing false path conflicts.

## Layer Map

| Layer | Files | Purpose |
|---|---|---|
| L0 | `CLAUDE.md`, `context-profile.json` | Always-on identity and project facts |
| L1 | `CONTEXT.md` | This routing file |
| L2 | `00_inputs/`, numbered stage `CONTEXT.md` files | Client input bank plus stage contracts and handoff rules |
| L3 | `_brand/`, `_config/`, `_references/`, `_swipe/` | Stable or reusable context, including client-confirmed video reference routing |
| L4 | campaign folders, typed deliverable workspaces, video runs, outputs | Working artifacts for this run; campaigns use discovery indexes |

## Brand Foundation Map

Keep buyer files separated by job, not by habit:

| File / Folder | Job | Do Not Use For |
|---|---|---|
| `_brand/icp.md` | Market boundary: demographics, firmographics, geography, eligibility, exclusions, category buying behavior, and broad audience constraints | Deep buyer psychology or ad-targeting micro-personas |
| `_brand/buyer-profile.md` | Buyer psychology: core emotional problem, fears, past solutions, transformation, and 3-7 micro-personas | Demographic ICP qualification or campaign-specific creative choices |
| `_brand/idea-bank.md` | Living cross-channel capture of fresh angles, founder intel, and campaign ideas (persona × channel × status). Feeds letters, emails, ads. Append on any new founder intel. | The locked strategy spine (`big-ideas/`) or finished proof stories (`story-bank.md`) |
| `_brand/visual-characters/` | Optional generated presenters, mascots, recurring faces, or character references for image/video work | Buyer targeting |
| `_brand/avatars/` | Legacy/tooling exports only when an older workflow requires one-file-per-avatar files | Canonical buyer targeting |

Campaigns select `micro_persona_id` values from `_brand/buyer-profile.md`; they do not copy or fork buyer profiles.

## Stage Map

| Stage | Purpose | Main Inputs | Output Location | Review Gate |
|---|---|---|---|---|
| `00_inputs` | Reusable client input bank for product, market/buyer, competitors, and research | intake docs, product assets, interviews, source research | `00_inputs/input-manifest.json` | Inputs are indexed before campaigns or concepts select them |
| `01_research` | Market, buyer, competitor, product, and source-of-truth research | client brief, website, existing assets, `00_inputs/`, `_references/` | `01_research/output/` | Research is synthesized before concept/script work |
| `02_script` | Legacy/general script work and non-campaign drafts only. **All campaign video concept work lives under `campaigns/<campaign>/video-concepts/<concept-slug>/02_ag1-options/` and `/03_scripts/` per the canonical workspace contract — never inside `02_script/`.** | selected input refs, research output, `_brand/`, `_config/scope-agreement.md` | `campaigns/<campaign>/video-concepts/<concept-slug>/` for video work, `02_script/output/` only for non-campaign legacy drafts | User approves direction before production assets |
| `03_production` | Input assets, image prompts, beat sheets, render prompts, and production prep | approved scripts, selected product assets, visual characters if needed | `03_production/output/` | User approves input images, beat sheets, and prompts before render |
| `04_review` | Internal/client review, revision notes, QA, compliance checks | production outputs, campaign brief, scope | `04_review/output/` | Approved or returned to stage 02/03 with scoped revision notes |
| `05_handoff` | Final delivery, documentation, lessons, promoted assets | approved outputs and review notes | `05_handoff/output/` | Deliverable accepted and reusable learnings captured |
| `06_measure` | Weekly analytics snapshot + scorecard; feeds findings back into 01_research | live platform data (YouTube Studio, IG Insights) | `06_measure/output/` | Scorecard reviewed; insights promoted to `_brand/learnings.md` |

## How to use it

1. Read this `CONTEXT.md` first for the high-level folder map and routing explanation.
2. Read `CLAUDE.md` and `context-profile.json` for local instructions and client identity.
3. For campaign/workspace rules, read `campaigns/README.md` before guessing paths.
4. For actual scaffold files, inspect the full `clients/_template/` shape copied into this client.
5. Read `00_inputs/input-manifest.json` when the task needs product, market/buyer, competitor, or research inputs. Personas are part of market/buyer context, not a separate top-level input family.
6. Load `_brand/` for stable brand, product, buyer profile, offer, claim, visual-character, video style context, and `_brand/higgsfield-reference-routing.json` when video prompt routing is involved.
7. Load `_config/` for this engagement's current brief, scope, priorities, and terms.
8. Load `_references/` and `_swipe/research/` only when the task needs reusable frameworks or source research.
9. Work inside the active numbered stage or `campaigns/<campaign>/`, then write reviewed final assets to `output/deliverables/`.
10. For campaign work, read `campaigns/_campaigns-index.json`, then `campaigns/<campaign>/campaign-index.json`, then `campaign-selection.json`, then the active workspace `artifact-manifest.json`, `pipeline-state.json`, and workspace brief before touching files.

## Campaign Discovery

Client-level campaign registry:

```text
campaigns/_campaigns-index.json
```

Generic campaign workspaces:

```text
campaigns/<campaign>/<artifact-family>/<artifact-slug>/
```

Examples:

```text
campaigns/<campaign>/video-concepts/<concept-slug>/
campaigns/<campaign>/email-sequences/<sequence-slug>/
campaigns/<campaign>/funnel-pages/<page-slug>/
campaigns/<campaign>/ad-concepts/<batch-slug>/
```

AI-video concept workspaces specialize this pattern:

```text
campaigns/<campaign>/video-concepts/<concept-slug>/
```

Required per concept workspace:

```text
pipeline-state.json
artifact-manifest.json
event-log.jsonl
concept-brief.json
01_strategy/
02_ag1-options/
03_scripts/
04_input-images/
05_prompt-packs/
06_generation-runs/
07_review/
```

`concept-brief.json` is the selected-input contract for the concept. It references entries from `00_inputs/input-manifest.json` and records the chosen product, market/buyer, competitor, and research inputs. It must not duplicate the full client-level input folders.

`02_ag1-options/` stores the candidate directions and AG1 review pack created inside the workspace. The workspace root can still have a concept slug; this folder is not a second concept root.

`04_input-images/` is present so visual-input workflows have a stable home, but it is only active when the selected executor payload uses uploaded images, start frames, style sheets, or references.

`06_generation-runs/` uses the lean clip-run contract by default: each run should have `run-manifest.json`, `payloads/`, `clips/`, `review/review.json`, and `stitch/`. Optional stills, beat sheets, motion prompts, and rerenders live inside the run only when the workflow actually uses them.

## Active phase

Currently: **research-seeded** — fictional research pack written to `00_inputs/research/`; thin `_brand/` seeds in place. No campaign active.

Next: `01_research` synthesis or `avatar-research` (build `_brand/buyer-profile.md` micro-personas from the VoC dump) — triggered when a later baseline pass exercises a downstream skill against this material.
