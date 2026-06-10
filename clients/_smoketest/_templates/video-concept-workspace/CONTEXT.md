# CONTEXT — {{concept_slug}} concept workspace

ICM L1 routing file. Tells agents where to go next.

## What lives here

This workspace holds all phase artifacts for one AI-video concept from input selection through final render review.

| Folder | Phase | Gate |
|---|---|---|
| `00_inputs/` | Input pinning + manifest | — |
| `01_strategy/` | Creative strategy + diversity map | — |
| `02_ag1-options/` | Concept pack + Approval Gate 1 | AG1 HARD STOP |
| `03_scripts/` | Scripts + visual treatment | — |
| `04_input-images/` | Visual reference + start frames | — |
| `05_prompt-packs/` | Canonical prompt pack + brief pack | — |
| `06_generation-runs/` | Clip render runs | — |
| `07_review/` | Render QA + Approval Gate 2 | AG2 HARD STOP |
| `eval/` | Buyer-fit + compliance evaluations | Pre-AG1/AG2 |

## Stage contracts

Canonical per-phase Inputs/Process/Outputs contracts live in:
`../../../../_templates/concept-phases/<phase>-CONTEXT.md`

Each phase folder's own `CONTEXT.md` points there. Do not duplicate the contract here.

## Entry protocol

1. Read `pipeline-state.json` — get `current_phase` and `legal_next_actions`.
2. Read `artifact-manifest.json` — confirm which artifacts are `present` vs `missing`.
3. Navigate to the current phase folder and read its `CONTEXT.md` for the stage contract.
4. Proceed. Do not skip the phase `CONTEXT.md` read.

## Conflict rule

When agent file I/O specs conflict with this CONTEXT.md or `artifact-manifest.json`, **this file wins**. Agent files describe one agent's contract — they are not workspace structure.
