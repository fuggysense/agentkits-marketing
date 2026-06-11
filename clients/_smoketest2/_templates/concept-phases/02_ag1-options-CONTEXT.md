# CONTEXT — Phase 02: AG1 Options (HARD STOP)

Canonical stage contract. Per-concept `02_ag1-options/CONTEXT.md` points here.

## Inputs

- Layer 4 (working): `../01_strategy/creative-diversity-map.json`
- Layer 4 (working): `../00_inputs/input-manifest.json`
- Layer 3 (reference): `clients/takekine/_brand/brand-voice.md`, `buyer-profile.md`, `funnel.md`
- Layer 3 (reference): `clients/takekine/_brand/big-ideas/<id>.md` if declared — enforce allowed/forbidden expressions
- Layer 3 (reference): `clients/takekine/_swipe/winning-ads/` for proven hook mechanics (extract patterns, not surface copy)

## Process

`video-concept-seeder` produces concept options + hook variants. `eval-buyer-fit` (Sonnet, persistent, 3-cycle cap) MUST pass with `verdict: "PASS"` and `fired_at_phase: "4.6"` before `html-publisher` renders the AG1 page (vid-director.md §4 + §9). `html-publisher` then renders `approval-gate-1.html` and syncs to `~/plans-vault/takekine/ag1/`. Operator approves/rejects via `approval-1.json`.

## Outputs

- `concepts.json` — concept options with per-option hook, mechanism, proof mode, visual treatment
  - Each concept block must include `key_moments[]` (3–5 sync peaks) — seeder populates at generation time
- `concept-pack.md` — operator-editable markdown summary of all concepts (one section per concept: outcome statement, visual philosophy, hook A/B, spine, key moments, reasoning). Generated from `_templates/concept-pack-template.md`. This is the U-shaped intervention surface — operator edits this between AG1 review and script-pack production; pack-builder reads it before Step 2.
- `script-drafts.json` + `script-drafts.md` — pre-AG1 draft scripts written by `video-prompt-pack-builder` in `draft_pre_ag1` mode (vid-director.md §2 Phase 1.5). Scene-by-scene structure: `# / time_range / visual_direction / voice_over / purpose`. Sum of scene durations = `concept-brief.json.duration_target_seconds`. **Output contract:** `_templates/concept-phases/ag1-card-template.md` (LOCKED v1.0).
- `suno-briefs.json` — sung-concept-only Suno music brief (genre, tempo, vocal note, lyric variants). Written by pack-builder when `concept-brief.json.script_mode == "singing"`.
- `hook-variants.json` — per-concept hook variants (multiple opening lines per concept)
- `approval-gate-1.html` — rendered review page. **Card structure is LOCKED** — see `_templates/concept-phases/ag1-card-template.md`. html-publisher MUST be dispatched with `structure_brief_ref` pointing to that file.
- `approval-1.json` — operator decision (approve / reject / modify + notes)
  - **Hard stop:** No phase 03 work until `approval-1.json.status == "approved"`
  - **Done:** all artifacts present, `pipeline-state.json.ag1` set, eval `buyer-fit-cycle-N.json` PASS recorded
