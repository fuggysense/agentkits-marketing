# Stackworks Letter — Skeleton Summary V4

**Source:** `scratch/audits/stackworks/copy/stackworks-letter.md`
**Audited:** 2026-05-08 (SGT)
**Extractor version:** 0.4.0
**Context branch:** loaded — full buyer dossier (buyer-profile.md + 5 avatars)
**Phase 2:** skipped (upstream dossier present)
**VOC anchor coverage:** 91% (10 of 11 findings dossier-grounded)

---

## Declared anchors

- **Purpose:** Convert SG property investors ($400K–$2M unallocated reserves) into qualified applicants.
- **CTA target:** Request Private Access → suitability application → 1:1 assessment call.
- **Final goal:** Qualified applicants who pass suitability and become Stackworks clients ($500K+ allocations).

---

## Meta

- **Word count:** ~1,102
- **Audience inferred:** Generic "private investor" — no property-investor specificity detected.
- **Verticals detected:** Generic time-poor private investor + DIY trader (Path Two framing).
- **Segment leakage:** PRESENT. The declared target segment (SG property investor with stranded ABSD/cycle capital) is not addressed, acknowledged, or named anywhere in the letter. The DIY trader framing (Path Two) may actively repel the property investor who has never identified as a trader.

---

## UMP

- **Articulated concept:** Rules-based automated execution across three dimensions (price, time, position size) in the currency market.
- **Primary branded term:** TripleStack™ — arrives at word ~395. Late.
- **Arrival flag:** UMP articulated at word 395. ~300 words of lede, problem framing, and alternative dismissal before the mechanism is named.
- **Prior solution link:** `implicit` — two paths named and dismissed (private banker, DIY investor) but neither discredited with a structural failure mode. All named alternatives in the dossier (Endowus, T-bills, structured notes, robo-advisors) are absent.

### MAGIC check — TripleStack™

| Letter | Score |
|---|---|
| M — Magnetic reason (why now?) | No |
| A — Avatar (buyer segment?) | No |
| G — Goal (dream outcome?) | No |
| I — Interval (timeline?) | No |
| C — Container word | Yes |
| **Score** | **1/5** |

Verdict: `[M]` — mechanism name is generic. Route to Phase 0.7 (mechanism architecture).

### Discredit-old-solutions inventory

| Alternative | Dismissal type | Notes |
|---|---|---|
| Private banker | named-no-structural-failure | Conflict of interest named; no specific failure mode |
| DIY investor | named-no-structural-failure | Behavioral failure named; no math |
| Endowus | absent | Not mentioned |
| T-bills / SSBs | absent | Not mentioned |
| Structured notes / ILPs | absent | Not mentioned |
| Stashaway / Syfe | absent | Not mentioned |

`[H]` finding: The alternatives the dossier shows this buyer is actually using right now — T-bills, Endowus, private banker structured notes — are not named and not discredited. The letter competes against a strawman (the private banker relationship broadly) and leaves the real competition unaddressed.

---

## Identity ladder

| Layer | Status | Notes |
|---|---|---|
| L1 — Problem aware | ✅ Word 1 | "You don't have a strategy problem. You have an execution problem." Strong. |
| L2 — Solution aware | ⚠️ Word 115 | Two paths named but weakly. Buyer who doesn't identify as either path may not see themselves. |
| L3 — Outcome aware | ✅ Word 290 | "Your capital stays active. Your life stays yours." Present but generic. |
| L4 — Post-decision identity | ❌ Absent | Letter never crystallises who the buyer *becomes* after deciding. No identity moment. |

---

## Motifs

| Phrase | Count | Anchor ratio | Flag |
|---|---|---|---|
| "time, energy and/or attention" | 4 | 0.0 | Repetition fatigue — zero proof weight across all 4 uses |
| "execution" | 9 | 0.28 | Overused connective |
| "rules-based / rules" | 4 | 0.75 | Earning its repetition |
| "your capital" | 6 | 0.33 | Partially earning |

---

## CTA architecture

- **Present (4 of 11 elements):** Explicit action label, application-only framing, scarcity signal, no-commitment at application stage.
- **Absent (7 of 11):** Guarantee, self-validation checkpoint near CTA, named outcome near CTA, return story near CTA, urgency mechanism, liquidity statement, minimum investment, MAS licence reference.
- **CTA word count:** 133 words. Thin.

---

## Proof inventory

- **Named outcomes:** Zero.
- **Numbers:** Zero (no return figures, no track record duration, no minimum investment).
- **Trust chain gaps:** 6 critical gaps — MAS licence absent, no audited track record, no auditor named, no liquidity terms, no named client outcomes, anonymous "unsolicited validation" with no attribution.

---

## AI-pattern flags summary

| Pattern | Source | Severity |
|---|---|---|
| Big Contrast / Negative Listing ("No screens. No daily burden. No emotional execution.") | overused-ai-patterns.md §3 + §Negative Listing | hard-flag |
| Negative Parallelism ("not because they were wrong... but because they could not execute") | anti-ai-patterns.md §8 | hard-flag |
| Rule of Three (×6 groupings: Time/Energy/Attention; Tesla/Amazon/Nvidia; cleanly/consistently/without emotion; etc.) | anti-ai-patterns.md §9 + overused-ai-patterns.md | hard-flag |
| Dramatic Fragmentation ("No screens. Rules run. Not feelings.") | overused-ai-patterns.md §Dramatic Fragmentation | hard-flag |
| Big Contrast opener ("strategy problem / execution problem") | overused-ai-patterns.md §3 | soft-flag |
| False Agency ("The market moves while you're in a meeting") | overused-ai-patterns.md §False Agency | soft-flag |
| Philosophical Reduction ("Your capital stays active. Your life stays yours.") | overused-ai-patterns.md §5 | soft-flag |
| Bold-start-colon inline formatting throughout TripleStack™ section | anti-ai-patterns.md §13 | soft-flag |

4 hard flags. 4 soft flags. Anti-AI score: 2/5.

---

## VOC anchor coverage

10 of 11 findings have direct or adjacent dossier match. 1 finding (MAGIC name check) is `[no-VOC]`.

Coverage exceeds 50% threshold — dossier is adequate for this audit. No `buyer-language-researcher` refresh required.

---

## Routing signal

| Priority | Issue | Route to |
|---|---|---|
| 1 | Segment lock — letter speaks to generic private investor, not SG property investor with stranded capital | Phase 0 (avatar re-anchor) |
| 2 | UMP / MAGIC rebuild — TripleStack™ scores 1/5 | Phase 0.7 (mechanism architecture) |
| 3 | Proof inventory — zero named outcomes, no numbers, no MAS licence, no auditor | Phase 2 (proof and trust chain) |
| 4 | CTA architecture — thin close, no trust anchors near CTA | CTA architecture phase |

**Recommended re-entry:** `sales-letter-method` Phase 0 → Phase 0.7 → Phase 2 → CTA.

---

## Ship readiness

| Dimension | Score | Read |
|---|---|---|
| Conversion potential | 2 | Has structural bones but speaks to wrong segment and has zero proof. Trust chain is broken. |
| Grammar & clarity | 3 | Clean but repetitive. "Execution" used 9 times. AI-default sentence structures throughout. |
| Anti-AI / AI-like tendencies | 2 | 4 hard flags. Negative listing, rule of three, dramatic fragmentation, negative parallelism. |
| Mobile readability | 3 | Reasonable formatting but roman-numeral blocks and the bold-inline-header structure are corporate, not mobile-friendly. |
| **Overall** | **2** | Governed by conversion potential and anti-AI scores. HOLD — blockers present. |
