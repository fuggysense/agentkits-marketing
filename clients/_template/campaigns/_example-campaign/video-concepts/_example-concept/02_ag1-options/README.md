# 02_ag1-options/

**What lives here:** Approval Gate 1 surface — candidate concept directions before the operator picks a winner.

Expected files (in roughly this order):
- `concepts-draft.json`, `hook-variants-draft.json`, `inputs-used.json` (raw seeder output)
- evaluator outputs (e.g. `eval-buyer-fit-cycle-N.json` — written to `../eval/` per vid-director §4)
- `concepts.json`, `concept-pack.{md,json,html}` (Phase 4 synthesis)
- `approval-1.json` (operator decision — approve / reject / modify per concept)

**Load to do X:**
- Run concept generation → load `../concept-brief.json` + `../01_strategy/creative-diversity-map.json` + `skills/video-concept-lab/SKILL.md`, then invoke `video-concept-seeder`.
- Publish AG1 review page → eval must verdict `PASS` first (see `routing-overrides.md` brand-alignment evaluator gate).

**Owner agent:** `video-concept-seeder` (generator) → `eval-buyer-fit` (gate) → `html-publisher` (review surface).
