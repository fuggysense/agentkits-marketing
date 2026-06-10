# 07_review/

**What lives here:** Approval Gate 2 (post-refinement, pre-production) artifacts.

Expected files:
- `approval-gate-2.html` — operator review surface (also published to `plans.genflos.com/<client>/ag2/...`)
- `approval-2.json` — structured operator decision (approve / reject / modify)
- `eval-buyer-fit-cycle-N.json` (or under `../eval/`) — must verdict `PASS` with `fired_at_phase: "6.5"` before HTML publish

**Load to do X:**
- Publish AG2 review → eval gate must PASS first (see `routing-overrides.md` brand-alignment evaluator gate).
- Unblock `06_generation-runs/` → `approval-2.json` verdict must be approved.

**Owner agent:** `video-brief-normalizer` (assembles AG2 brief) → `eval-buyer-fit` (gate) → `html-publisher` (review surface).
