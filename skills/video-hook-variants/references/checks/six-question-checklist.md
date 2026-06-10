# Six-Question Checklist

Run on every hook before delivery. This is the operator's primary quality gate.

## The Six Questions

1. **Topic clarity:** Is the topic crystal clear in ≤3 seconds?
2. **Curiosity gap:** Does it open an immediate curiosity gap?
3. **Three Elements:** Does it contain ≥1 of: Relatability / Sensationalism / Stakes?
4. **Simplicity:** Can a 6–7-year-old understand it?
5. **Value delivery:** Is value (visual / text / verbal) delivered in the first 1–2 seconds?
6. **Contrast:** Does it create contrast (what people believe vs. what you're showing)?

## Scoring Logic

| Score | Rating |
|---|---|
| Yes to Q1–Q4 + ≥1 element in Q3 | Strong |
| Yes to Q1–Q6 + 2 elements in Q3 | Very strong |
| Yes to Q1–Q6 + all 3 elements in Q3 | Elite |

A hook that fails Q1 or Q4 is not delivered — no matter how strong the other questions score. Both are non-negotiable.

## Notes on Each Question

**Q1 — Topic clarity:** the six-year-old test (topic-level, not jargon-level). Not "does the viewer understand the offer" — just "does the viewer know what this video IS about."

**Q2 — Curiosity gap:** the brain must subconsciously demand "what happens next?" If there is no open loop, no unresolved tension, no contrast setup — this fails.

**Q3 — Three elements:** see `references/frameworks/three-elements.md` for full definitions. Under high claim_risk, Sensationalism must be validated against `allowed_expressions` before being counted as a pass.

**Q4 — Simplicity:** not "does a child understand the business model" — "does a child understand the topic and the emotional setup in one second." Abstract claims, coded setups, and industry jargon fail this automatically.

**Q5 — Value delivery:** value is not limited to education. Entertainment, humor, aspiration, motivation, and inspiration all count. If the hook makes the viewer expect humor, that is valid value. Do not force every hook into a problem-fix mold.

**Q6 — Contrast:** explicit Point A → Point B distance. Engineer this deliberately. Bigger gap = stronger pull. See `references/frameworks/four-horsemen.md` (Disinterest section) for the mechanism.

## Output Field

Record in hook-variants-draft.json (implicit via individual audit fields):
- `topic_clarity_passes_six_year_old_test: true/false`
- `on_target_curiosity_passes: true/false`
- `elements_hit: [...]`
- `four_horsemen_check` covers Q5 (Delay) and Q6 (Disinterest)
