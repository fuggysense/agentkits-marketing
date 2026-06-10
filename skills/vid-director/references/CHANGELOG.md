# vid-director — Changelog

Pure history. Never auto-loaded. Load only when the operator asks "what changed in v0.X?" or wants to roll back.

## v0.6 — 2026-05-18

**Theme:** Align orchestrator + all subagents with `clients/_template/` canonical folder contract.

**Vocabulary changes:**
- `concept-input-packet.json` → **`concept-brief.json`** (workspace ROOT, not inside `00_inputs/`)
- `persona_id` (buyer axis) → **`micro_persona_id`** (sourced from `_brand/buyer-profile.md`)
- `actor_structure_id` (5th axis) → **`visual_character_id`** (sourced from `_brand/visual-characters/`)
- Strategy Map axes: `Micro-Persona × Angle × Awareness × Format × Visual-Character`
- `_brand/avatars/` is now legacy/tooling only — buyer targeting moves to `_brand/buyer-profile.md` micro-personas
- `_brand/big-ideas/` is GONE — Creative Pattern + Big Idea premise now live INSIDE `concept-brief.json`
- `input-image-plan.json` → **`input-image-manifest.json`**

**Folder layout:**
- All AG1 artifacts move to `<workspace>/02_ag1-options/` (was loose in workspace root)
- All AG2 artifacts move to `<workspace>/07_review/` for review files; `03_scripts/`, `04_input-images/`, `05_prompt-packs/` for the pack itself
- Generated clips + ffmpeg assembly live at `<workspace>/06_generation-runs/<run-id>/`

**New term: `campaign-selection.json`** — campaign-root contract listing in-scope `00_inputs/` entries + in-scope `micro_persona_id`s. Required reading before concept work. Concept-briefs MUST select within this scope.

**Reading order (template-prescribed):** `_campaigns-index.json` → `campaign-index.json` → `campaign-selection.json` → workspace `artifact-manifest.json` → `pipeline-state.json` → `concept-brief.json` → folder-local `CLAUDE.md`. Replaces the old `artifact-manifest → pipeline-state → campaign-index` order.

**§5 rewrite — preflight delegation:**
- vid-director no longer scaffolds client folders, `_brand/` files, campaigns, or workspaces by hand
- Detects missing context and delegates to `Skill("client-onboarding")`, `Skill("avatar-research")`, `Skill("brand-scaffolder")`, `/campaign:new`, `/video:new`
- Refuses to proceed when workspace or `_brand/buyer-profile.md` is empty scaffolding

**New failure modes (§11):**
- 14. Workspace missing → refuse + delegate to `/video:new`
- 15. `_brand/buyer-profile.md` empty → delegate to `Skill("avatar-research")`
- 16. `campaign-selection.json` missing → halt + delegate to `/campaign:new`
- 17. `concept-brief.json` selects `micro_persona_id` outside `campaign-selection.json` scope → halt
- 18. `concept-brief.json` selects `visual_character_id` with no matching file in `_brand/visual-characters/` → halt
- 19. vid-director attempts hand-scaffold → routing failure

**Files modified:**
- `prompts/orchestrators/vid-director.md` (full rewrite v0.5 → v0.6)
- `agents/video-concept-seeder.md` (template alignment, paths, vocab)
- `agents/video-hook-variant-generator.md` (template alignment, paths, vocab)
- `agents/prompt-preview-stub-builder.md` (template alignment, paths, vocab)
- `agents/video-prompt-pack-builder.md` (template alignment, paths, vocab)
- `prompts/orchestrators/vid-director/EDITING.md` (refresh references)
- `prompts/orchestrators/vid-director/CHANGELOG.md` (this entry)

Backup of v0.5 at: `vid-director-v0.5.md.bak-<timestamp>` (auto-created via `cp` before write — verify with `ls vid-director*.bak*`).

## v0.5 — 2026-05-18 (superseded by v0.6)

Unified video router. Renamed §3 "Engine Routing Table" → "Video Generation System Routing Table" to reflect that Video Factory + higgsfield-prompts + executor are components in ONE stack, not competing engines. Added persistent-iterative-chat vs one-shot dispatch runtime annotations per subagent. Introduced Micro-Persona term (partial v0.4 hold-over still used `Actor Structure`).

## v0.4 — 2026-05-18

**Theme:** Make the orchestrator a slim router. Delegate data-flow to destination files.

**Cuts (~17-19k tokens reclaimed, 31.6k → ~12-14k target):**
- §13 Higgsfield CLI reference → removed (duplicates `~/.claude/skills/higgsfield/SKILL.md`)
- §12 render path bash examples → removed (duplicates higgsfield skill + video-factory skill)
- §17 concept-block schema → moved INTO `video-concept-seeder.md` (the agent that writes it)
- §17 hook-variant schema → already lived in `video-hook-variant-generator.md`; vid-director duplication removed
- §17 input-image-plan + canonical-prompt-pack + approval-2 schemas → moved INTO new `video-prompt-pack-builder.md`
- §9 Phase 4.5 7-subsection detail → moved INTO new `prompt-preview-stub-builder.md`
- §21 verbose chat output examples → moved to sidecar `examples.md` (load on demand)
- §22 versioning → moved here (CHANGELOG.md)
- §23 self-editing meta → moved to sidecar `EDITING.md` (load on demand)
- §16 extensibility → folded into EDITING.md
- §15 multi-flow handling → tightened to a 3-line note

**New subagents:**
- `prompt-preview-stub-builder.md` (Sonnet, one-shot) — owns Phase 4.5 preview stubs
- `video-prompt-pack-builder.md` (Opus, iterative) — owns post-AG1 scripts/prompts/adapters/manual-run-guide/approval-2

**New sidecars (load on demand):**
- `vid-director/EDITING.md`
- `vid-director/CHANGELOG.md` (this file)
- `vid-director/examples.md` (optional — only if drift surfaces)

**Routing principle introduced:**
- Orchestrator OWNS: pipeline shape, engine routing decisions + WHY, HITL gates, operator commands, subagent roster.
- Destination files OWN: data flow, schemas, CLI patterns, model gotchas, methodology.
- Orchestrator should PROPOSE new agents when gaps surface (see EDITING.md "When to propose a NEW subagent").

## v0.3 — 2026-05-18 (superseded by v0.4)

Model-agnostic creative-diversity orchestrator with Higgsfield as a first-class prompt/execution stack. Added strategy map gate before AG0, explicit `Persona × Angle × Awareness × Format × Actors` contract, concept references to `strategy_map_id` + `combination_id`, AG2 prompt/input-image approval, canonical prompt packs, manual-any-model guide, Higgsfield/Seedance adapter path that uses repo-local flow/media skills without letting model syntax rewrite approved strategy.

Backup at: `vid-director-v0.3.md.bak-<timestamp>`

## v0.2 — 2026-05-17 (superseded by v0.3)

Master Higgsfield-native orchestrator. Wraps Video Factory + higgsfield-prompts + Higgsfield CLI. Added engine routing table, AG1 render prompt preview, surgical revisions, flow-explainer Haiku subagent (5 subagents total), multi-flow handling, extensibility hooks for Sora/Kling/Veo, expanded tool allowlist for ffmpeg + higgsfield CLI + curl + jq, post-AG1 render path with retry budget.

Backup at: `vid-director-v0.1.md.bak`

## v0.1 — 2026-05-17

Council-validated MVP, concept-only, stops at AG1. 2 generators + 2 text-only evaluators. Video Factory and Higgsfield CLI out of scope.

## Future versions

- **v0.5**: add `video-script-writer` if scripts in `video-prompt-pack-builder` need finer methodology splits after 1-2 cycles
- **v0.5**: add `render-quality-evaluator` subagent powered by Gemini 3.1 Pro analyzer (Video Factory v0.2+ scope)
- **v0.5**: add failure telemetry (`corrections.md` per client) when patterns emerge
- **v0.5**: add `eval-video-hook-body-continuity` (Frankenstein detection) if AG1 review surfaces the need
- **v0.6**: add Sora/Kling/Veo direct API adapters once Higgsfield CLI gains those models OR direct integrations land
