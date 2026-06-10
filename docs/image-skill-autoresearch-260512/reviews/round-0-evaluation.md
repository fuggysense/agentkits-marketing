# Round 0 Evaluation

## Rubric

| Criterion | Points |
|---|---:|
| Subject / brief match | 25 |
| Structure / layout fidelity | 20 |
| Text / count / label accuracy | 20 |
| Routing correctness | 15 |
| Backend portability | 10 |
| Visual quality / no obvious artifact | 10 |

Critical fail overrides: wrong skill, wrong subject, missing required structure, unreadable required text, ignored identity constraints, or output cannot be visually evaluated.

## Score Matrix

| Candidate | Subject | Structure | Text | Routing | Portability | Visual | Total | Critical |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| A-001 product ad | 22 | 18 | 16 | 15 | 7 | 9 | 87 | Yes |
| B-006 diagram | 25 | 19 | 20 | 15 | 8 | 9 | 96 | No |
| C-002 UGC review | 24 | 19 | 20 | 15 | 9 | 9 | 96 | No |
| HF-003 marketplace card | 24 | 17 | 20 | 15 | 9 | 9 | 94 | No |

Mean score: 93.25.

Passing outputs at 90+ with no critical failures: 3/4.

## Findings

### A-001 Product Ad

Score: 87/100.

Critical failure: the bottle includes a visible `Voltsip` mark even though the brief asked for no extra logos/watermarks. Text and composition are otherwise strong.

Mutation: add a hard prompt rule for generic product ads: use brand name only in requested overlay text or on a plain removable paper tag; if no label is requested, product surface must be blank and unbranded.

### B-006 Diagram

Score: 96/100.

No critical failure. The node labels, title, and loop structure are correct. The only minor issue is that the orange callout arrow could target the Signal -> Decision transition more precisely.

Keep pattern: structured JSON/count-and-label prompts are strong for diagrams and exact-label layout work.

### C-002 UGC Review

Score: 96/100.

No critical failure. `DEW SERUM` is legible, hand anatomy is plausible, and the bathroom selfie context is strong. Slightly too polished for rough UGC.

Keep pattern: persistent actor seed plus everyday background clutter works. Next mutation should add more imperfection only when UGC authenticity is the primary objective.

### HF-003 Marketplace Card

Score: 94/100.

No critical failure. All three callouts are correct and the marketplace-card structure is clear. The product is slightly oversized/off-center.

Keep pattern: marketplace card prompts port well to Codex when feature count and banned marketplace badges are explicit.

## Stop Rule Status

Success stop not met. This is only loop 0, and one sample had a critical failure.

Next loop should rerender:

1. A-001 mutated product-ad prompt.
2. One regression sample from B-006, C-002, or HF-003.

Do not change canonical skills until the mutated A-001 passes and one regression sample stays above 90.
