# Checkpoint Questions — Phase 4 HITL Gate

The 4 strategic decisions only humans should make. Presented as ONE batched AskUserQuestion call at the end of Phase 3 synthesis, before Phase 5 write.

**Rules:**
- All 4 questions in ONE call (multi-question single payload)
- Each question presents 2-3 AI-drafted candidates + rationale (so user picks, doesn't freehand)
- Use `preview` field on options for §9 and §10 where side-by-side comparison helps
- "Other" allowed on all questions for user override
- User's answers finalise §2, §9, §10, §16 in the doc and update §22 summary

---

## Q1 — §2 Primary KPI

**Header:** `Primary KPI`
**Single-select, 3-4 options (tailored by conversion goal):**

### Draft logic by conversion goal

**If Q1 (Phase 1) = Purchase:**
```
Options:
1. ROAS (target: X.X) — Recommended
   Description: Return on ad spend. Standard for e-commerce. Target derived from intake Q3 price point × category benchmark.
2. MER (target: X.Xx)
   Description: Media efficiency ratio (total revenue / total ad spend). Use if you track multi-touch attribution or blended channels.
3. CPA (target: $X)
   Description: Cost per purchase. Use if you don't trust your attribution / revenue tracking yet.
```

**If Q1 = Lead / application:**
```
Options:
1. CPA / CPL (target: $X) — Recommended
   Description: Cost per qualified lead. Standard for lead gen. Target derived from intake Q3 × category benchmark (e.g. real estate SG: $30-80 CPL).
2. Booked-call cost (CBC, target: $X)
   Description: Cost per completed sales call (deeper-funnel KPI). Use if form-fills are noisy / low-quality.
3. Qualified-lead rate (QLR %)
   Description: % of leads that pass qualification. Use when spend is less of a constraint than lead quality.
```

**If Q1 = Trial / signup:**
```
Options:
1. CAC payback period (target: X months) — Recommended
   Description: Months to recoup customer acquisition cost. Standard for SaaS with monthly subscriptions.
2. CPA (target: $X)
   Description: Cost per trial signup. Simpler but doesn't account for activation/conversion to paid.
3. Activated-trial cost
   Description: Cost per trial that reaches "aha moment" (product-defined). Best if you have product analytics wired.
```

### Rationale line for every draft

Always include a one-line rationale explaining WHY this target came out of research (e.g. "Target $55 CPL derived from competitor benchmark range $45-80 + your premium positioning pulls it toward the top of that range"). Never invent targets.

---

## Q2 — §9 Core Message (use `preview` field)

**Header:** `Core message`
**Single-select, 3 options with previews:**

```
Option A — Problem-led
Preview:
  Core: "Most [audience] are stuck in [specific pain] because [why generic solutions fail]."
  Supporting 1: [pain agitation]
  Supporting 2: [why now matters]
  Supporting 3: [what the ideal alternative looks like]

Option B — Outcome-led (Recommended if sophistication ≤ 3)
Preview:
  Core: "[Specific transformation] in [timeframe], without [thing they dread]."
  Supporting 1: [proof that this happens]
  Supporting 2: [why this path vs. alternatives]
  Supporting 3: [what their life looks like after]

Option C — Mechanism-led (Recommended if sophistication ≥ 4)
Preview:
  Core: "[Unique mechanism] that makes [outcome] [X times] [faster/easier/safer] than [standard approach]."
  Supporting 1: [how the mechanism works]
  Supporting 2: [why this mechanism is defensible]
  Supporting 3: [what it means for the buyer]
```

### Recommendation logic

- Sophistication 1-2: Option B (outcome-led — buyer still believes outcomes are possible)
- Sophistication 3: Option A (problem-led — buyer burned by outcome claims, needs problem framing)
- Sophistication 4-5: Option C (mechanism-led — buyer saturated with both problem and outcome framings)

Draft each option from research synthesis. For project-type-specific examples (property, SaaS, ecom, services, info, agency), see `references/examples-by-product-type.md`.

### Allow custom

User can click "Other" and paste their own core message. If they do, skill must rebuild §9 ladder + §10 priority angles against the custom message.

---

## Q3 — §10 Priority Angles (multi-select, pick 3 of 6-8)

**Header:** `Top 3 angles`
**Multi-select: true, 6-8 drafted angles to pick 3 from:**

Draft angles to span the 6 angle categories (problem-aware / desire / product / offer / proof / contrarian). Include at minimum:
- 2 problem-aware angles (different problem framings)
- 1 desire-led
- 1 offer-led or product-led
- 1 proof-led
- 1 contrarian / pattern-interrupt

### Option format

```
Angle option:
  Label: "[Short name, <6 words]"
  Description: "[1 sentence: core idea] · Best for: [which segment] · Format: [static / carousel / UGC / founder / demo / VSL] · Risk: [what could go wrong]"
```

### Recommendation markers

Mark the AI's top-3 picks with "(Recommended #N)" — e.g. "(Recommended #1 — highest-leverage given market sophistication)". User can accept all 3 or override.

### Per-product-type expected draft patterns

See `references/examples-by-product-type.md` for full draft sets per product type (ecom, SaaS, service, info, agency, property). Each set shows angle drafts, recommended-pick rationale, and risk notes calibrated to that product type's buyer psychology + sophistication ladder.

Do NOT default to property examples when `product_type` is anything else.

---

## Q4 — §16 First Variable to Test

**Header:** `First test variable`
**Single-select, 4-5 options:**

```
1. Hook (Recommended if awareness mostly Problem-Aware OR first-frame holds are weak)
   Description: Test 3 hook variants per angle with identical body. Highest leverage when scroll-stop is the bottleneck.

2. Angle (Recommended if sophistication 4-5)
   Description: Test 3 distinct angles with same hook style. Highest leverage when market is saturated and needs new entry points.

3. Proof type (Recommended if §8 proof inventory is thin OR trust objection dominates)
   Description: Test UGC vs founder vs data vs testimonial. Highest leverage when belief is the bottleneck.

4. Format (Recommended if competitive swipe shows format homogeneity)
   Description: Test static vs carousel vs video vs UGC. Highest leverage when everyone in the category uses the same format.

5. CTA (rarely recommended first)
   Description: Test assessment/quiz/book-call/download variations. Usually a second-wave test after hook+angle are dialled in.

6. Offer (only if research reveals offer breakdown)
   Description: Test price, bonus, guarantee variations. Deep strategy change — confirm §3 is the actual bottleneck before this.
```

### Recommendation logic

Based on synthesis from Phase 3:
- Awareness distribution from §4: if >50% of market is Problem-Aware → hook leverage highest
- Sophistication from §4: if ≥ 4 → angle leverage highest
- Proof thinness from §8: if < 3 strong proof assets → proof leverage highest
- Competitor format diversity from swipe files: if all same format → format leverage highest

Always mark ONE option as "Recommended" with rationale. Do NOT show recommendations on 2+ options — that creates decision paralysis.

### Per-product-type recommendation patterns

See `references/examples-by-product-type.md` for sophistication-driven recommendations per product type. General rule: when sophistication ≥4 AND competitor ads cluster on the same hook pattern, **angle leverage is highest** (recommend Angle as first test variable).

---

## AskUserQuestion Call Construction

Put all 4 questions in ONE batched call. Do NOT split across multiple calls.

Order matters: Q1 → Q2 → Q3 → Q4 (KPI first because it anchors the other decisions; angles last because they depend on message choice).

Use `preview` field for Q2 only. Q1/Q3/Q4 use plain labels + descriptions.

Max 4 options per question (AskUserQuestion tool limit). If more candidates exist, surface the top 4 by recommendation score + include "Other" for custom input.

---

## After Answers Return

1. **Update in-memory draft** for §2, §9, §10, §16
2. **Cascade updates** to:
   - §4 segment table — if user picked angles targeting specific avatars, mark those segments as "priority for first DCT"
   - §22 Strategy Summary — rebuild from the finalised §2, §9, §10, §16
   - §10 + §11 in SoT → bootstrap `angles/wave-1.md` + `angles/hook-library.md` from finalised content, then strip the SoT sections to pointer blocks
3. **Update the derivative files** (pain-objection-proof, swipe-file-buyers/sellers, angles/wave-1.md + hook-library.md). Core message lives inline in SoT §9 — no separate messaging-hierarchy.md.
4. **Proceed to Phase 5** write

---

## Fail-safe: User Hits "Skip"

If user bypasses the checkpoint entirely (`/skip` or deny):
- Use AI-recommended defaults for all 4 questions
- Flag in §22 Strategy Summary: "⚠️ Strategic decisions auto-selected by AI — review before first DCT spend"
- Write the doc
- Log to learnings.md: `- YYMMDD | HITL skipped | AI defaults used for §2, §9, §10, §16 | recommend manual review`
