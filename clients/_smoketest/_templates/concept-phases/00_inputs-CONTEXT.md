# CONTEXT — Phase 00: Inputs

Canonical stage contract. Per-concept `00_inputs/CONTEXT.md` points here.

## Inputs

- Layer 4 (working): the concept's `../concept-brief.md` + `../pipeline-state.json`
- Layer 3 (reference): `clients/takekine/_brand/buyer-profile.md`
- Layer 3 (reference): `clients/takekine/_brand/funnel.md`
- Layer 3 (reference): `clients/takekine/_brand/offer.md`
- Layer 3 (reference): `clients/takekine/_brand/big-ideas/_index.md` (if concept declares a Big Idea)
- Layer 3 (reference): `clients/takekine/_swipe/winning-ads/` (when concept-brief cites swipes)

## Process

Resolve every input the concept needs and pin it. Owning agent is the orchestrator dispatching `video-concept-seeder` (vid-director.md §2 phase 0). Inputs are normalized into one manifest so every downstream phase reads from a single source. No creative work happens here — this phase just stages the materials.

## Outputs

- `input-manifest.json` — pinned input paths, hashes if any, micro_persona_id, big_idea_id, declared visual_character_id (or null)
  - **Done:** manifest lists every input cited by `concept-brief.md`, no broken paths, `pipeline-state.json.phase` advances to `01_strategy`
