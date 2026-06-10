# Video Concept Lab Index

Purpose: compact routing map for concept ideation without loading the whole reference folder.

## Entry Contract

- `SKILL.md` defines the boundary and the high-level process.
- `REFERENCE_GRAPH.json` defines the exact reference loadouts.
- `video-concept-seeder` is the only runtime concept generator in the `vid-director` pipeline.
- Every concept-stage dispatch must include `methodology_loadout_id` and return `methodology_receipt`.

## Loadout Selection

| Intent | Loadout | What to read |
|---|---|---|
| Brand-lift / awareness video concepts | `brand_awareness_concept` | Brand methodology + taxonomy + concept-generation refs |
| Standard direct-response concepts | `dr_standard_concept` | `dr-foundation.md` + taxonomy + generation/scoring refs |
| Singing direct-response concepts | `dr_singing_concept` | Standard DR + `singing-ads-layer.md` |
| Solution-aware L3+ concepts | `dr_solution_aware_l3_concept` | Standard DR + discrediting/common-enemy/proof refs |
| Singing + Solution-aware L3+ concepts | `dr_singing_solution_aware_l3_concept` | Solution-aware L3+ + `singing-ads-layer.md` |
| Existing pack quality/diversity audit | `pack_audit` | Diversity audit + scoring/success refs |
| Initial image/style-sheet requirements only | `image_handoff_only` | Image handoff gate only |

## Runtime Principle

`dr-foundation.md` is the runtime DR concept methodology. The older split files (`core-framework.md`, `lf8-market-translation.md`, `concept-stage-mandatory-checks.md`, `iman-take-260518.md`) remain source/audit references and are loaded only when a conflict or audit requires them.

## Downstream Ownership

- `video-concept-seeder` writes `02_ag1-options/concepts-draft.json` and `02_ag1-options/inputs-used.json`.
- The orchestrator synthesizes `02_ag1-options/concepts.json`, `concept-pack.{md,json,html}`, and `approval-1.json`.
- `video-prompt-pack-builder` runs after AG1 for scripts, input-image manifests, prompt packs, adapters, and AG2.
- `video-brief-normalizer` is post-AG1/post-script refinement and never runs during raw concept ideation.

## Known Path Rules

- Use `02_ag1-options/*`, not `02_concepts/*`.
- Use `concept-brief.json` as canonical; `concept-input-packet.json` is only a legacy alias.
- Use `references/general/success-criteria.md`, not `references/success-criteria.md`.
- Use `references/general/output-schema.md`, not `references/output-schema.md`.
- Use `.claude/references/copywriting-os/reviewers/proof-density-audit.md`, not bare `proof-density-audit.md`.
