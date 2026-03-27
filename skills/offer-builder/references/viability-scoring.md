## Graph Links
- **Parent skill:** [[offer-builder]]
- **Sibling references:** [[audit-checklists]], [[carrier-trust-signals]], [[deployment-scripts]], [[identity-frameworks]], [[offer-document-template]], [[raw-pour-questions]]
- **Related skills:** [[pricing-strategy]], [[copywriting]], [[launch-strategy]]

# Offer Viability Scoring

## Purpose
Two scoring systems that gate whether an offer is ready to build (micro) and ready to deploy (full). Used at Steps 2 and 7 respectively.

---

## System 1: OV Gate (Offer Viability Gate)

**When:** Step 2, after Raw Pour. Quick check — should we keep building or pivot?

**Scale:** 1-5 per dimension, gate at average ≥ 3.0

### Dimensions

| Dimension | 1 (Weak) | 3 (Viable) | 5 (Strong) |
|-----------|----------|------------|------------|
| **D — Demand** | "I think people want this" | Evidence of search volume or waitlist | Paying customers or validated demand data |
| **C — Clarity** | Can't explain in 1 sentence | Clear to insiders, fuzzy to outsiders | A stranger gets it in 10 seconds |
| **O — Ownership** | Anyone could offer this | Some differentiation | Clear unfair advantage / unique mechanism |
| **P — Proof** | No results yet | Anecdotal evidence or early results | Hard numbers, case studies, testimonials |

### Scoring

```
OV Score = (D + C + O + P) / 4

≥ 3.0 → PASS — proceed to identity extraction
2.0-2.9 → CONDITIONAL — proceed but flag weak areas for strengthening
< 2.0 → STOP — offer needs fundamental rework before building
```

### Output Format

```
## OV Gate Score

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Demand | X/5 | [brief evidence] |
| Clarity | X/5 | [brief evidence] |
| Ownership | X/5 | [brief evidence] |
| Proof | X/5 | [brief evidence] |

**Average: X.X/5** → [PASS/CONDITIONAL/STOP]
[If CONDITIONAL: flag which dimensions need strengthening]
```

---

## System 2: Vending Machine Score (VMS)

**When:** Step 7, after micro offer is built. Full readiness check — is this offer "vending machine ready" (put money in, get result out)?

**Scale:** 0-10 per dimension, gate at average ≥ 7.0

### Dimensions

| Dimension | 0-3 (Not Ready) | 4-6 (Getting There) | 7-10 (Ready) |
|-----------|-----------------|----------------------|---------------|
| **D — Demand** | No validation | Some interest signals | Proven demand (sales, waitlist, search volume) |
| **C — Clarity** | Confusing, needs explanation | Clear to target audience | Crystal clear — could be a vending machine label |
| **O — Offer strength** | Commoditized, nothing special | Some differentiation | Irresistible — hard to say no at this price |
| **P — Proof** | Zero proof | Testimonials or early results | Hard ROI data, case studies, guarantees |

### Scoring

```
VMS = (D + C + O + P) / 4

≥ 7.0 → DEPLOY — offer is ready for market
5.0-6.9 → STRENGTHEN — improve weak dimensions before deploying
< 5.0 → REBUILD — offer needs significant rework
```

### Output Format

```
## Vending Machine Score

| Dimension | Score | Evidence | Gap to 7+ |
|-----------|-------|----------|-----------|
| Demand | X/10 | [evidence] | [what's needed] |
| Clarity | X/10 | [evidence] | [what's needed] |
| Offer | X/10 | [evidence] | [what's needed] |
| Proof | X/10 | [evidence] | [what's needed] |

**Average: X.X/10** → [DEPLOY/STRENGTHEN/REBUILD]
[Specific actions to close gaps]
```

---

## Relationship Between Scores

- OV Gate is a **quick filter** — can you explain it, does anyone want it, can you prove it?
- VMS is a **deployment check** — is it strong enough to sell without you in the room?
- Same DCOP dimensions, different depth and threshold
- An offer can pass OV Gate but fail VMS — that's expected. The build process between Steps 2-7 is where the score climbs.
