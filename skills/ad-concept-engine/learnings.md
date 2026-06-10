# Ad Concept Engine — Learnings

> ⚠ **N=1 WARNING:** The learnings below are derived from a single client run (NeezaNizam, SG property, 260406). They are *priors*, not laws. Revisit and generalise only after ≥3 completed live campaigns. Do not apply patterns from this file as hard rules to other clients without verification.

> Accumulated learnings from running this skill across clients.

## Confirmed Patterns

- External validation (Perplexity + Grok) before committing to angles catches cultural blind spots and factual weaknesses that internal scoring misses. Worth the extra step.
- Named-couple testimonial angles (Fahmy & Aida style) consistently outrank abstract benefit angles for Solution-Aware audiences. Real names + specific outcome = highest conversion potential.
- Blue ocean angles (topics no competitor addresses) are the highest-value output of this skill. The Islamic financing angle for NeezaNizam had zero competition in SG property advertising.

### Phase 2 split — Hooks (statics) vs Briefs (videos) (260418)

**Rule:** Phase 2 in this skill ROUTES by format. Static + Carousel → Phase 2a (Hooks: text-on-image hook + visual concept + image prompt). UGC / Founder Video / UGC Testimonial / Demo / VSL → Phase 2b (Briefs: full production-ready brief with 6 scene breakdown + performer notes + audio specs + graphics + technical specs + timing map). Each batch's `creative_type` field in dct-tracker.json records which path: `"hook"` or `"brief"`.

**Why:** the previous Phase 2 lumped video and static into one "creative" output with a `format` field. UGC/Founder/VSL batches got one-line creative direction notes — not enough for a UGC creator or video editor to execute without 5 follow-up questions per batch. Briefs need scene-by-scene, performer direction, timing map, audio specs. Statics need visual concept type + on-image hook + image prompt. Same Phase 2 doesn't serve both.

**How to apply:** look at the batch's `format` first. Route to 2a or 2b. Both paths still produce headlines + ad copy + CTA (those fill Meta fields regardless of format). Only the visual deliverable differs. Use `references/video-brief-template.md` as the brief structure. Quality bar: if a brief reads as one paragraph, it failed.

### Multi-product readiness (260418)

**Rule:** all examples in `references/sophistication-creative-map.md` now show 6 product types per Schwartz level (ecom / SaaS / service / info / agency / property). When generating angles or hooks, pull from the row matching the client's `product_type` (set in `clients/<project>/offer.md` Product Classification block).

**Why:** the previous map had property examples only. Running this skill on a SaaS or ecom client produced property-shaped angles. Now: every L1-L5 description has 6 product-type examples and the routing is explicit.

**How to apply:** load the client's `product_type` from offer.md Product Classification block. Filter the sophistication-creative-map example column to the matching product type. NEVER paste a property example for an ecom client.

## Angle Generation Insights

- Unaware-level angles are the biggest gap in most client ad portfolios. Clients default to Solution-Aware and Product-Aware messaging.
- Angles that validate buyer fears ("you're right to be scared, here's why the math still works") outperform angles that dismiss fears ("your fear is wrong").
- Specificity bias (exact numbers: "3 numbers", "729 families") signals insider knowledge and stops scrolls better than vague benefit claims.

## Headline Patterns That Work

- Story headlines with named characters from the client's case studies outperform all other types for Solution-Aware audiences.
- Question headlines that mirror the buyer's internal dialogue ("Do you keep telling your spouse...") create instant identification.
- UK English is non-negotiable for SG market — even one US spelling breaks trust with educated Singaporean audience.

## Image Prompt Learnings

- 3 concepts per angle (12 total for 4 angles) is the right volume — gives enough variety to test without overwhelming.
- UGC-style selfie format bypasses ad blindness for Unaware audiences.
- Split-screen before/after is strongest for Solution-Aware transformation proof.
- Text-heavy bold graphics work for Problem-Aware (they're seeking information, not lifestyle imagery).

## Anti-Patterns (What Doesn't Work)

- "Mortgage as retirement fund" reframe falls flat for Muslim audience (riba sensitivity) and for any audience that is rightly afraid of overextension.
- Shaming angles ("you've spent more time on phone plans than...") trigger defensiveness in anxious personas.
- Agent brag / authority angles ("22 years, 729 families") are invisible in cold traffic — agents have a trust deficit in SG.
- Generic "clients who were unsure" social proof is too vague to stop a scroll.

## Client-Specific Notes

### NeezaNizam (260406)
- First run. 4 angles selected: war chest (Unaware), Fahmy story (Solution-Aware), 3 numbers (Problem-Aware), Islamic financing (Blue Ocean).
- Islamic financing angle is genuinely differentiated — no competitor addressing riba concerns.
- Perplexity flagged: HDB resale supply surging 56% in 2026-2028, so urgency/FOMO angles need softer framing than 2022-era ads.
- The buyer persona (Hafiz & Siti) responds to "we" framing and couple-based decision narratives.
