# Objection Architecture

The teardown's #1 conversion upgrade. The current skill handles objections only inside the FAQ (5 slots). That's insufficient. Serious buyers raise objections *while reading*, not only at the bottom. Handle them inline with scaffolded preempts, then consolidate remaining skepticism in FAQ.

**Rule:** objection handling is now a **required** component (promoted from partial coverage).

---

## The 10 Objections Every Long Letter Must Resolve

Ordered by frequency in post-click drop-off analysis (across 8 competitor pages scraped + Hormozi/Halbert diagnostic patterns):

| # | Objection | Typical thought | Where to resolve |
|---|-----------|-----------------|------------------|
| 1 | **Fit** | "This wasn't built for someone like me." | Lead + Qualification block + FAQ.Preference |
| 2 | **Trust** | "Why should I believe the claims?" | Proof Stack + Trust Density markers + FAQ.Authority |
| 3 | **Timing** | "Is now the right time?" | Pain Cycle (cost of waiting) + PS line |
| 4 | **Risk** | "What if this doesn't work for me?" | Guarantee Stack (primary) + FAQ.Money |
| 5 | **Effort** | "How much work is required from me?" | Mechanism + Offer Breakdown (timeline + role) |
| 6 | **Speed** | "How long until meaningful progress?" | Mechanism (time anchors) + Proof (time windows) |
| 7 | **Prior failure** | "I've tried similar things before." | Pain Cycle (dismantle old way) + Mechanism (why this is different) |
| 8 | **Alternatives** | "Why this instead of competitor/DIY?" | Mechanism (differentiation) + FAQ.Preference |
| 9 | **Authority/decision** | "Do I need someone else's buy-in?" | FAQ.Authority + CTA friction reducer |
| 10 | **Post-click reality** | "What actually happens after I book?" | CTA + FAQ.Stall + PS line |

---

## Resolution Pattern Template

For every objection addressed in body copy (not just FAQ), use this micro-structure:

```
1. NAME the concern in their own words (2-5 words, italicized or set off):
   *"But will this work for my specific situation?"*

2. LEGITIMIZE it without patronizing:
   That's the right question to ask — most approaches break down here.

3. RESOLVE it with mechanism, proof, or qualification (pick one, not all):
   The [Mechanism Name] handles [specific sub-case] because [cause-and-effect logic].
   OR: Out of [N] clients we've worked with, [X%] fit [this exact profile].
   OR: This is built specifically for [criteria] — if that's not you, this isn't for you.

4. BRIDGE back to momentum:
   Which is why, instead of [failed alternative], we [distinct move].
```

**Not every objection needs all 4 steps.** Mid-body preempts can compress to NAME + RESOLVE. FAQ entries should be NAME + RESOLVE (2 sentences).

---

## Placement Map

Wire objections into the existing 12-component flow:

| Component | Objections resolved inline |
|-----------|----------------------------|
| 1-2 Headline + Sub | None (too early — raises objections, doesn't resolve) |
| 3 Pain Cycle | Prior failure (7), Timing (3) |
| 4 Integrity Tie-Down | Fit (1) — soft preempt |
| 5 Mechanism | Effort (5), Speed (6), Alternatives (8), Prior failure (7) |
| 6 Proof Stack | Trust (2) |
| 7 Offer Breakdown | Effort (5), Post-click reality (10) |
| 9 Scarcity | Timing (3) — only if real cap |
| 10 Guarantee | Risk (4) — primary lever |
| 11 CTA | Post-click reality (10) via friction reducer |
| 12 FAQ | Consolidates residual: Time, Money, Authority, Stall, Preference |
| 13 PS | Timing (3) final push, Fit (1) reassurance |

---

## Failure Modes (auto-reject in Conversion Gate)

- Listing objections without resolving them (acknowledgment ≠ answer)
- Using FAQ as dumping ground for objections that should've been resolved inline
- Resolving with claims alone, no mechanism or proof
- Overhandling — if 10+ objection preempts appear, the letter sounds defensive
- Generic reassurance ("we've got you covered") — always substitute specific answer

---

## Anti-Patterns to Avoid

- **"Some might say..."** — distances the reader; they are the some
- **"You might be wondering..."** — fine once, tedious repeated
- **"I know what you're thinking..."** — presumptuous; use only if you'll answer with specificity
- **Stacking 5 objections in a row** — breaks narrative rhythm; spread them across components

---

## Diagnostic Test

Before Conversion Gate approves the letter, verify:

- [ ] Each of the 10 objections appears somewhere (inline resolution OR FAQ)
- [ ] Risk objection is resolved in Guarantee Stack, not just mentioned
- [ ] Fit objection appears in at least 2 places (body + FAQ)
- [ ] Prior-failure objection is explicit in Pain Cycle (old way names the failure pattern)
- [ ] Post-click reality is described specifically ("30-minute call with our strategist, no pitch")
- [ ] No objection is "handled" by assertion alone — mechanism/proof/qualification is present

If any box unchecked → Conversion Gate fails → loop back to Phase 2.

---

## CTA Architecture (11-Element Checklist)

The CTA closing block is where objection resolution becomes commitment. `prompt-template.md` §11 sets the goals; this checklist is the structural audit.

**Target length:** 180-210 words for the closing CTA block (excluding PS).

**The 11 required elements** (every long-form letter's closing block should contain at least 8 of these — under 8 = WEAK; under 6 = FAIL):

| # | Element | What it does | Word budget |
|---|---------|--------------|-------------|
| 1 | **Mirror their situation** | Restate where the reader is right now in 1-2 sentences. Recognition before request. | 40-50 |
| 2 | **Reframe what's at stake** | Name the actual cost of staying stuck — not generic "you'll fall behind" but the specific consequence in their world. | 15-25 |
| 3 | **Brief mechanism reminder** | One-line callback to the UMP/UMS. Not a re-explanation — a touchpoint. | 25-35 |
| 4 | **Consequences of inaction** | What happens in 30/60/90 days if nothing changes. Concrete, sensory, tied to the avatar's life. | 35-45 |
| 5 | **Pivot to fixable** | Explicit reframe: "This is fixable" / "This stops here" / "There's a way out." 5-10 words. | 5-10 |
| 6 | **Guarantee or risk reversal** | The primary conversion lever. See `references/guarantee-variants.md`. | 35-45 |
| 7 | **Self-validation checkpoint** | Give the reader a way to self-test their fit before clicking ("If you nodded to any of the above…", "If you're at the point where…"). | 20-30 |
| 8 | **Permission language** | Lower the threshold: "Only book if you're actually ready to…", "If now isn't right, this can wait." Permission is conversion's lubricant. | 25-35 |
| 9 | **Urgency with specific cost-of-waiting** | If real scarcity exists, name it concretely. If not, name the daily/weekly cost of inaction instead. | 25-35 |
| 10 | **Mission completion frame** | The identity the reader steps into by booking — not a feature, an identity move. | 25-35 |
| 11 | **The link** | Standalone line. The actual CTA. Not buried in a paragraph. | 1 line |

**Self-audit procedure (run before Conversion Gate):**

1. Count CTA block words. If > 210 → tighten. If > 250 → restructure (likely rehashing body).
2. Mark which of the 11 elements are present. Count.
3. If guarantee element is absent → auto-fail. The guarantee is the primary conversion lever; it cannot live only in the body.
4. If self-validation checkpoint is absent → flag. The reader needs a way to self-test fit; without it, fit-objection traffic clicks off.
5. If mission completion frame is absent → identity-layer letters lose their identity payoff. Add it.

**Common failure patterns:**

- CTA under 100 words missing most elements (operator treated CTA as "the button")
- CTA over 250 words rehashing the body (operator hid the action behind one more pitch)
- PS overloaded because main CTA underbuilt (PS doing CTA's structural job)
- Pivot-to-fixable missing — letter ends in pain instead of agency
- Mission completion missing — letter ends at outcome, not identity

**Reference back to `prompt-template.md` §11:** §11 gives the goal (benefit-oriented copy + friction reducer). This checklist is the structural audit. Both apply — §11 governs the button + below-button copy; this checklist governs the full closing block leading into it.
