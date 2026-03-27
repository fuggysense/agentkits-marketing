## Graph Links
- **Parent skill:** [[offer-builder]]
- **Sibling references:** [[audit-checklists]], [[carrier-trust-signals]], [[deployment-scripts]], [[identity-frameworks]], [[raw-pour-questions]], [[viability-scoring]]
- **Related skills:** [[pricing-strategy]], [[copywriting]], [[launch-strategy]]

# Offer Document Template

## Purpose
Step 9 of the offer-building process. This is the master document that captures everything built in Steps 1-8. It writes to `clients/<project>/offer.md` and serves as the source of truth for all downstream marketing.

---

## The 8 Sections

### Section 1: Core Offer
The elevator pitch. If someone asks "what do you do?" this is the answer.

```markdown
## Core Offer
- **Name:** [offer name — can be a product name, service name, or program name]
- **One-Line Description:** [I help (who) achieve (what) by (how)]
- **Price:** [amount or pricing model]
- **Delivery Method:** [1:1, group, self-serve, SaaS, productized service, etc.]
- **Timeline:** [how long to deliver the promised result]
```

### Section 2: Viability Scores
Captured from Steps 2 and 7.

```markdown
## Viability Scores

### OV Gate (Step 2)
| Dimension | Score |
|-----------|-------|
| Demand | X/5 |
| Clarity | X/5 |
| Ownership | X/5 |
| Proof | X/5 |
| **Average** | **X.X/5** |

### Vending Machine Score (Step 7)
| Dimension | Score |
|-----------|-------|
| Demand | X/10 |
| Clarity | X/10 |
| Offer | X/10 |
| Proof | X/10 |
| **Average** | **X.X/10** |
```

### Section 3: Identity Map
From the House Framework + 11PM Thought (Steps 3-4).

```markdown
## Identity Map

### Offer House
- **Land (Market):** [specific segment]
- **Foundation (Identity):** [why you]
- **Walls (Mechanism):** [named method / unique approach]
- **Roof (Promise):** [specific outcome]

### 11PM Thought
- **The thought:** "[their words]"
- **Category:** [fear/frustration/ambition/shame/overwhelm/impatience]
- **How we address it:** [connection to offer]
```

### Section 4: Micro Offer
The minimum viable version (Steps 5-6).

```markdown
## Micro Offer
- **What:** [smallest version that delivers a result]
- **Price:** [entry price point]
- **Promise:** [specific, small outcome]
- **Timeline:** [how fast]
- **Purpose:** [lead magnet / tripwire / trust builder / proof of concept]
```

### Section 5: Value Proposition
Expanded from Raw Pour answers.

```markdown
## Value Proposition
- **Primary Benefit:** [the #1 thing they get]
- **Supporting Benefits:**
  1. [benefit 2]
  2. [benefit 3]
  3. [benefit 4]
- **Unique Mechanism:** [what makes your approach different — named if possible]
- **Transformation:** [before state → after state]
```

### Section 6: Proof Elements
From Raw Pour Q5 + Carrier Trust Signals (Step 8).

```markdown
## Proof Elements

### Case Studies
- [customer name/type]: [outcome with numbers and timeline]

### Testimonials
- "[quote]" — [name, title]

### Data Points
- [metric]: [number]

### Carrier Trust Signals
| Signal | Score (0-3) | Evidence |
|--------|-------------|----------|
| Results Proof | | |
| Social Proof | | |
| Authority Proof | | |
| Mechanism Proof | | |
| Risk Reversal | | |
| Specificity | | |
| Demonstration | | |
| **Total** | **X/21** | |
```

### Section 7: Guarantee & Risk Reversal
From Raw Pour Q9 + trust signal work.

```markdown
## Guarantee / Risk Reversal
- **Type:** [money-back / performance / hybrid]
- **Terms:** [specific conditions]
- **Duration:** [timeframe]
- **Why it works:** [connects to buyer's 11PM fear]
```

### Section 8: Urgency & Scarcity
Natural urgency built into the offer.

```markdown
## Urgency / Scarcity
- **Type:** [natural deadline / capacity limit / price increase / cohort-based]
- **Mechanism:** [why it's real, not manufactured]
- **How to communicate:** [specific language]
```

---

## Usage Notes

- This template is the **target output** of the offer-builder skill
- It replaces the simpler `clients/_template/offer.md` during the build process
- All 8 sections don't need to be complete — [TBD] is fine for gaps
- The document should be readable as a standalone brief — any marketer should be able to pick it up and write copy, ads, or landing pages from it
