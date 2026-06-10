# Video Hook Variants Index

Purpose: compact routing map — load what you need, not the whole reference folder.

## Entry Contract

- `SKILL.md` defines the boundary and the high-level methodology.
- `REFERENCE_GRAPH.json` defines the exact reference loadouts.
- `video-hook-variant-generator` is the only runtime hook generator in the `vid-director` pipeline.
- Every dispatch must include `methodology_loadout_id` and return `methodology_receipt`.

## Loadout Selection

| Intent | Loadout ID | What to read |
|---|---|---|
| Standard A/B hook pair (≥1 element) | `standard_hook_variant` | three-hook-types + three-elements + lego-bricks + four-horsemen + modern-w-order + six-question-checklist |
| Elite A/B hook pair (all 3 elements required) | `elite_hook_variant` | standard loadout + nuclear-hooks examples |
| Multi-clip A/B paired production | `multi_clip_hook_pair` | standard loadout + output schema + body-shared contract rules |
| Audit existing hooks, no generation | `hook_audit_only` | six-question-checklist + common-mistakes + four-horsemen + three-element-checklist |

## Downstream Ownership

- `video-hook-variant-generator` writes `02_ag1-options/hook-variants-draft.json` and returns `methodology_receipt`.
- Orchestrator synthesizes into final concept pack.
- Hook variants feed directly into AG1 review surface.

## Known Path Rules

- Hook variants always go to `02_ag1-options/hook-variants-draft.json`, not `02_concepts/`.
- `concept-brief.json` is canonical for claim_risk + allowed/forbidden expressions.
- `three-element-checklist.md` (existing agent's checklist) and `six-question-checklist.md` (operator's 6-Q) are complementary, not duplicates — load both for `standard_hook_variant`.
- Example bank lives in `references/examples/`. Framework files reference it; they do not duplicate it.

## Reference Structure

```
references/
├── frameworks/         # methodology (load from REFERENCE_GRAPH.json)
├── checks/             # pre-flight checklists and audits
├── examples/
│   ├── by-type/        # Visual / Text / Verbal examples
│   ├── by-element/     # Relatability / Sensationalism / Stakes examples
│   └── combined/       # nuclear hooks (all 3 elements)
└── patterns/           # operator-curated learnings over time
```
