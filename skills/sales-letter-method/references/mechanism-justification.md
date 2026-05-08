# Mechanism Justification

The teardown's sharpest criticism: "mechanism naming without mechanism justification." A named system (*"The 17-Day Approval Method"*) is a confidence signal, not a conviction signal. Serious buyers want cause-and-effect logic — *why* does this method produce the outcome better than alternatives?

This file extends Component 5 (Mechanism) from the prompt template. The mechanism should now do **5 jobs**, not 4.

---

## The 5 Jobs of a Mechanism

The current prompt-template lists 4:
1. Name the system
2. Describe function, not tools
3. Visual clarity + rhythm
4. Numbers + time anchors

Add **Job 5: Justify why the mechanism works.**

---

## Job 5: Mechanism Justification

The reader should close the mechanism section thinking: *"I see why this produces different results than the old way."*

Use one or more of these 4 justification patterns:

### Pattern A — Cause-and-Effect Chain

Explain the reason each step produces its result.

**Template:**
```
Step 1 — [action]. This works because [underlying cause].
Step 2 — [action]. Which means [downstream effect].
Step 3 — [action]. By this stage, [observable outcome].
```

**Example (from Syncom scrape):**
```
Step 1 — We rebuild your landing page using a 6-second comprehension test.
This works because (b)76% of cold traffic decides to click or leave within 6 seconds(b) — every layout element gets tested against that threshold.

Step 2 — We run 3 hook angles in parallel for 14 days.
Which means we see which pain point the algorithm amplifies, not which one we guess is right.

Step 3 — We double down on the winning angle with 5 fresh creatives.
By this stage, (h)CPL is 40-60% lower than the baseline week(h), because the algorithm has learned who converts.
```

### Pattern B — Contrast Against Conventional

Show what everyone else does and why it underperforms.

**Template:**
```
Most [industry operators] do [conventional approach].
The problem with that is [specific failure mode].
Instead, this method [contrasting move] — which [outcome].
```

**Example:**
```
Most mortgage brokers chase pre-approvals by volume — 50 leads in, 2 closings out.
The problem: 96% of those leads are tire-kickers, and the broker burns 30 hours on unconvertible files.
Instead, this method pre-qualifies with 4 income-documentation checks (b)before(b) the first call — so 8 of every 10 consultations are closeable. The close rate goes up because the top of the funnel shrinks.
```

### Pattern C — First-Principles Reasoning

Derive the method from a foundational truth the reader can verify.

**Template:**
```
[Foundational truth the reader will agree with].
Which means [logical implication].
Which is why this method [specific design choice].
```

**Example:**
```
Cold traffic on Meta sees your ad for 1.7 seconds on average before deciding to scroll past.
Which means the first frame of your creative has to do 80% of the work — the copy only gets looked at if the image wins.
Which is why this method leads with a visual hook test (not a headline test) — we find the winning image first, then optimize the headline around it.
```

### Pattern D — Constraint Acknowledgment

Explain the tradeoff the method makes and why the tradeoff favors the reader.

**Template:**
```
This method deliberately gives up [X] in exchange for [Y].
Because for someone in your situation, [Y] matters more than [X].
```

**Example:**
```
This method deliberately gives up "scale fast, worry about close rate later."
Because for a solo agent with limited hours, booking 30 appointments a month that don't close is worse than booking 8 that do.
We optimize for close-rate-per-hour, not lead-volume-per-dollar. The math works differently.
```

---

## Length Calibration

Mechanism justification shouldn't bloat the section. Targets:

| Letter length | Justification words |
|---------------|---------------------|
| 800 words | 50-80 |
| 1,200 words | 80-150 |
| 1,800+ words | 150-250 |

Enough to build conviction. Not so much it reads like a whitepaper.

---

## Choosing the Right Pattern

| Offer context | Best justification pattern |
|---------------|---------------------------|
| Broad market + skeptical audience | B (Contrast) — differentiates strongly |
| Technical / analytical buyer (SaaS, finance, consulting) | A (Cause-and-Effect) + C (First-Principles) |
| Trade / niche professional (roofing, real estate, landscaping) | B (Contrast) + D (Constraint) |
| Coaching / info product | C (First-Principles) — establishes authority through logic |
| Health / wellness / any regulated industry | A (Cause-and-Effect) — safer tone, more defensible |

---

## Integration With Existing Mechanism Section

The current prompt-template Component 5 structure stays the same. Insert justification **between Job 3 (visual clarity) and Job 4 (numbers + time anchors)**:

```
1. NAME the system
2. DESCRIBE function (not tools)
3. VISUALIZE + compress the journey
4. JUSTIFY — pick 1-2 of Patterns A/B/C/D
5. ANCHOR with numbers + time
```

This keeps the mechanism section tight but gives it conviction weight.

---

## Failure Modes (auto-reject)

- Named mechanism with no explanation of why it works
- Justification that's really just re-asserting the outcome ("it works because it works")
- Cause-and-effect claims with no underlying principle ("this converts because it's better")
- Over-justification — 500 words of theory, reader checks out
- Justification in vague corporate language ("leveraging proprietary frameworks")

---

## Diagnostic Test

Before Conversion Gate approves:

- [ ] Mechanism section includes at least 1 of Patterns A/B/C/D
- [ ] Justification uses verifiable reasoning (cause-and-effect, contrast, first-principles, or constraint)
- [ ] No vague justification phrases ("leverage," "holistic," "proprietary" without content)
- [ ] Justification length matches letter length (see calibration table)
- [ ] Reader can articulate, in one sentence, *why* this mechanism outperforms the old way
