# CONTEXT — Phase 07: Review (AG2 HARD STOP)

Canonical stage contract. Per-concept `07_review/CONTEXT.md` points here.

## Inputs

- Layer 4 (working): `../06_generation-runs/<selected-run>/run-manifest.json` + selected clips
- Layer 4 (working): `../03_scripts/script-pack.md`
- Layer 4 (working): `../02_ag1-options/approval-1.json` (AG1 baseline for compare)
- Layer 3 (reference): `clients/takekine/_brand/funnel.md`, `brand-voice.md`, `funnel-research/sales-letter-extract-*.md` (claim guardrails on the final cut)

## Process

`eval-buyer-fit` (Sonnet, persistent, 3-cycle cap) MUST pass with `verdict: "PASS"` and `fired_at_phase: "6.5"` before `html-publisher` renders the AG2 page (vid-director.md §4 + §9 + §11). `html-publisher` then renders `approval-gate-2.html`, syncs to `~/plans-vault/takekine/ag2/`. Operator approves/rejects via `approval-2.json`. On approve → handoff. On reject → loop back to phase 03, 05, or 06 per notes.

## Outputs

- `approval-gate-2.html` — rendered review page with stitched preview
- `approval-2.json` — operator decision (approve / reject / modify + revision scope)
  - **Hard stop:** No campaign-level handoff until `approval-2.json.status == "approved"`
  - **Done:** AG2 approved, eval `buyer-fit-cycle-N.json` PASS recorded at phase 6.5, `pipeline-state.json.ag2` set, learnings flow to `../../../_brand/learnings.md`
