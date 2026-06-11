# CONTEXT — Phase 01: Strategy

Canonical stage contract. Per-concept `01_strategy/CONTEXT.md` points here.

## Inputs

- Layer 4 (working): `../00_inputs/input-manifest.json`
- Layer 3 (reference): `clients/takekine/_brand/funnel.md` (Iman lanes, awareness rung, ad→SL handoff)
- Layer 3 (reference): `clients/takekine/_brand/buyer-profile.md` (resolve `micro_persona_id`)
- Layer 3 (reference): `clients/takekine/_brand/funnel-research/sales-letter-extract-*.md` (handoff rung, claim guardrails)
- Layer 3 (reference): `.claude/references/copywriting-os/frameworks/schwartz-channeling.md` (when Solution-Aware / Stage-3 concepts)

## Process

`video-concept-seeder` (vid-director.md §2 phase 1) builds the 4-axis creative diversity map: hook mechanism × creative lane × proof mode × visual treatment. Strategy must satisfy the funnel handoff constraint (current production SL opens Solution-Aware). No scripts, no visuals — pure strategic axes.

## Outputs

- `creative-diversity-map.json` — 4-axis matrix, locked persona, locked Iman lane, locked awareness rung, declared big_idea_id (if any)
  - **Done:** map is internally consistent (lane × persona × rung), no banned phrasings from `big-ideas/<id>.md` carried forward, `pipeline-state.json.phase` advances to `02_ag1-options`
