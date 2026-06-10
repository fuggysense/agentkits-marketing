# CONTEXT — Phase 06: Generation Runs

Canonical stage contract. Per-concept `06_generation-runs/CONTEXT.md` points here.

## Inputs

- Layer 4 (working): `../05_prompt-packs/canonical-prompt-pack.json`
- Layer 4 (working): `../05_prompt-packs/model-adapters/<model>.json` (matching the chosen executor)
- Layer 4 (working): `../04_input-images/input-image-manifest.json` (resolved reference paths)

## Process

`video-factory` (vid-director.md §2 phase 6) dispatches the prompt pack to the chosen executor (Higgsfield, Seedance, Kling, VEO via Vertex). One subfolder per run, named `<run-id>/`. Each run carries its own `run-manifest.json` recording prompt versions, model, params, output paths, cost, and HITL state.

## Outputs

- `<run-id>/run-manifest.json` — what was run, with what, where outputs landed, cost
- `<run-id>/clips/` — generated MP4s (or links if media lives outside repo)
- `<run-id>/notes.md` — operator notes, regen rationale, what failed
  - **Done:** every script beat has at least one acceptable clip, `pipeline-state.json` records the selected take per beat, ready for AG2 stitch
