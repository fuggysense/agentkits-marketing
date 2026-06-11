# 04_review — Review Contract

Review production output before anything ships. The internal and client-facing quality gate.

## Inputs

- L4 (working): approved concept/script from the campaign workspace at `../campaigns/<campaign>/video-concepts/<concept-slug>/02_ag1-options/` (AG1 surfaces) and `/03_scripts/` (locked scripts post-AG1) — the canonical path, NOT `02_script/output/` for campaign work. Production assets from `03_production/output/`.
- L3 (reference): campaign brief and scope, brand constraints, claims/compliance notes, and `../_brand/asset-map.md`.

## Process

1. Check output against the campaign brief and approved concept.
2. Check claims, disclaimers, product fidelity, and brand constraints.
3. Check whether input images, beat sheets, prompts, and renders match the approved route.
4. Produce specific revision notes when work returns to `02_script` or `03_production`.
5. Mark outputs approved only when they can move to handoff or launch without hidden fixes.

## Outputs

- `output/<YYMMDD>-review-notes.md`, `output/<YYMMDD>-revision-request.md`, `output/<YYMMDD>-approval-record.md`.
  - Done: the deliverable is approved, or the next revision is scoped clearly enough that the builder does not have to guess.
