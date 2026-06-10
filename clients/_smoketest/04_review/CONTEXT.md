# 04_review — Review Contract

Review production output before anything ships. This is the internal and client-facing quality gate.

## Inputs

- Approved concept/script from the selected campaign workspace at `campaigns/<campaign>/video-concepts/<concept-slug>/02_ag1-options/` (AG1 surfaces) and `/03_scripts/` (locked scripts post-AG1). This is the canonical path — do not look in `02_script/output/` for campaign concept work.
- Production assets from `03_production/output/`
- Campaign brief and scope agreement
- Brand constraints, claims/compliance notes, and asset map

## Process

1. Check output against the campaign brief and approved concept.
2. Check claims, disclaimers, product fidelity, and brand constraints.
3. Check whether input images, beat sheets, prompts, and renders match the approved route.
4. Produce specific revision notes when work returns to `02_script` or `03_production`.
5. Mark outputs as approved only when they can move to handoff or launch without hidden fixes.

## Output convention

- `output/<YYMMDD>-review-notes.md`
- `output/<YYMMDD>-revision-request.md`
- `output/<YYMMDD>-approval-record.md`

## Done looks like

The deliverable is approved, or the next revision is scoped clearly enough that the builder does not need to guess.
