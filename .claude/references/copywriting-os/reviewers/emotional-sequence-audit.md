# Emotional Sequence Audit — Post-Write Reviewer (sub-agent)

**Source:** Mark Masters, "Advanced AI Emotion Engine for High-Converting Copywriting" (cai #37, 32-min issue — densest of the 12).

**Core principle:** Every prospect moves through 6 emotional states between "no" and "yes." Sequential. Cannot skip. "You can write the most compelling copy in the world and still lose the sale if the emotional sequence is wrong. The difference between 0.9% and 2.4% isn't talent. It's architecture."

**Agent model:** Sub-agent. Receives the draft. Independent of other reviewers.

## The 6 States (order matters — each requires the previous)

1. **Indifference** — "I don't care about this." Default. Reader is scrolling, distracted, thinking about lunch.
2. **Pain** — "I feel the problem." Reader's world is named; the friction they already live with is surfaced.
3. **Understanding** — "I grasp the mechanism of the problem." Reader sees WHY the problem happens (not just that it hurts).
4. **Hope** — "A solution to this kind of problem exists." Possibility restored.
5. **Belief** — "THIS specific solution works." Proof, mechanism, specifics map the claim to their situation.
6. **Desire** — "I want it now." The commitment motion.

### The Chain Rule (verbatim from cai #37)

> "You can't make someone desire something they don't believe will work. You can't make them believe it works if they have no hope. You can't give them hope if they don't understand their problem. You can't make them understand their problem if they don't feel pain. You can't make them feel pain if they're indifferent."

## Procedure

### Step 1 — Walk top to bottom and tag each section

Break the draft into components (by heading, paragraph break, or logical unit). For each, label the dominant emotional state it serves.

### Step 2 — Verify order is monotonic

- ✅ Monotonic: 1 → 1 → 2 → 2 → 3 → 4 → 4 → 5 → 5 → 6
- ❌ Skip: 1 → 2 → 4 (missed 3 Understanding)
- ❌ Reversal: 1 → 2 → 5 → 3 (went to Belief then back to Understanding)

Back-and-forth within a single state is fine. Skipping or reversing is not.

### Step 3 — Check for state coverage

All 6 states must have at least one component serving them. Any missing state → FAIL.

### Step 4 — Check the Indifference→Pain flip specifically

The first 2-3 components must move the reader past Indifference into Pain. If the reader is still indifferent after 3 components, the copy fails on opening regardless of what comes later.

## Output schema

```
## EMOTIONAL SEQUENCE AUDIT
Components tagged (in draft order):
1. <first 8 words of component> → State <N> (<state name>)
2. ...
N. ...

State coverage: <list which of 6 appear>
States missing: <list>

Order check: MONOTONIC / SKIPS / REVERSALS
<If SKIPS: "Missing state <X> between component <i> and <j> — reader has no <state> but copy jumps to <state X+2>">
<If REVERSALS: "State <X> appears on line <L1>, then state <X-N> on line <L2>">

Indifference→Pain flip: PASS (happens by component <N>) / FAIL (still indifferent by component 3)

Verdict: PASS (all 6 covered AND monotonic AND opening flip works) / FAIL

Top 3 specific revisions:
1. <between component X and Y — add content to serve state Z — suggested copy: "<example>">
2. ...
3. ...
```

## Failure thresholds

- Any of the 6 states completely missing → FAIL
- Any skip or reversal → FAIL
- Indifference→Pain flip still incomplete by component 3 → FAIL (the opening is dead)

## Mapping to sales-letter-method 12 components (cross-reference)

When upgrade 2.6 ships, `skills/sales-letter-method/` will tag each of its 12 components with the emotional state it owns. This reviewer then checks if the writer's output honored those tags. The mapping (proposed):

1. Hook → Indifference → Pain
2. Problem → Pain
3. Agitation → Pain
4. Mechanism → Understanding
5. Solution → Understanding → Hope
6. Social Proof → Belief
7. Offer → Belief → Desire
8. Guarantee → Belief (risk removal)
9. Bonus → Desire
10. Urgency → Desire
11. CTA → Desire (commitment)
12. PS → Desire (second commit window)

When skills/sales-letter-method upgrades, this reviewer can cross-check draft-component-to-state alignment AND sequence.

## Logging

Append to `clients/<slug>/copy-system/quality-gates/emotional-sequence-log.md`:
`| YYMMDD-HHMM | output file | states covered N/6 | order monotonic Y/N | opening flip Y/N | verdict |`
