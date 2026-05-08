# Stackworks Letter — Skeleton Summary

**Source:** `scratch/audits/stackworks/copy/stackworks-letter.md`
**Word count:** ~1,310
**Extractor version:** 0.1.0
**Extracted:** 2026-05-07
**Phase 2:** completed (no upstream artifacts existed for this one-off audit)
**Speculation ratio:** 0.0 — no halt

---

## Headline finding

The letter is **structurally articulate but proof-starved** and has a **dual-mechanism naming problem**. It dismisses competing paths cleanly (private banker + DIY investor — both with structural-failure-mode framing, which is strong), but the proof chain that should validate Stack itself never lands. The brand "Stack" and the trademarked method "TripleStack™" are introduced ~475 words apart, creating mechanism ambiguity for the reader.

---

## Re-entry routing (per skeleton-contract.md routing table)

Stages flagged in priority order (lowest priority = highest urgency):

| Priority | Trigger | Re-enter at | Notes |
|---|---|---|---|
| **1** | `branded_terms.length = 2` (Stack + TripleStack™); TripleStack™ arrives at word ~510 | **UMP regen** | The product name and the proprietary method name compete. Reader has to figure out which is the mechanism. Either consolidate (TripleStack™ becomes Stack's only branded asset) or sequence the relationship explicitly early. |
| **3** | `trust_chain_gaps.length = 7` | **Proof inventory rebuild** | Largest single weakness. No named customer outcomes anywhere. "Why us" is credentials-only. Acquisition interest claim has both parties anonymous. Tesla/Amazon/Nvidia is decorative analogy, not transferred proof. |
| **4** | `cta_architecture.elements_present.length = 5` (below 9-element bar) | **CTA rewrite** | CTA word count is fine (118, under 210 ceiling). Missing: guarantee, self-validation checkpoint, PS, value recap, scarcity beyond "limited number," risk reversal. |
| **5** | `motifs.execution.anchor = 0.4`; `time, energy, attention.anchor = 0.25` | **Coherence audit / motif scrub** | "Execution" appears 17 times — many decorative. "Time, energy, attention" repeated as triplet without each repetition earning new proof. |

Priority 2 (L4 location) does not strictly fire — L4 lands in body via "You run your business on systems. Your capital deserves the same." — but it's a weak L4. Soft flag, not a hard re-entry trigger.

Priority 0 hard stops: not triggered. Speculation ratio = 0.0. Vertical leakage is borderline (4 verticals detected, but no explicit declared segment to compare against — letter is trying to address all four simultaneously).

---

## Key flags by section

### UMP (mechanism)
- **Two competing branded terms** — "Stack" (product, ~32 mentions, arrives word 36) and "TripleStack™" (method, 3 mentions, arrives word 510). Reader gets the *system* concept early but the *named mechanism* late.
- **Prior-solution link is structural** (strong) — the letter explicitly contrasts against private bankers and DIY investors with structural reasoning, not feelings. This is good. Don't lose it in regen.

### Identity ladder
- **L1, L2, L3 land cleanly** in headline → lede → body.
- **L4 is weak** — present in body via the systems-builder identity line, but never explicitly names "the investor who decides." For a high-ticket suitability-gated offer, L4 carries disproportionate weight. Consider strengthening before/in the close.

### Proof inventory (the lens-blind track)
The biggest finding. The letter has **zero named customer outcomes**. Every trust signal is either:
- Founder credential (JPMorgan, Citibank, 2 decades) — about the operator, not the customer
- Anonymous validation ("an investment bank and a global family office") — unverifiable
- Decorative analogy (Tesla/Amazon/Nvidia) — feels like proof, isn't proof

This is fixable but only via voice-mining → real customer material. If Stack is too new for testimonials, the founder-credibility frame needs to do double the work it currently does (e.g., a specific named institutional desk Jason ran, a specific deal flow, a specific named mentor — anything concrete).

### Concentration alternatives
- **3 dismissed paths, all structural-failure-mode** (private banker, DIY, manual wealth management). This is strong execution — don't lose it.

### CTA
- **Under quality bar** (5 of 11 elements). Word count fine. Missing the quiet but high-leverage elements: self-validation checkpoint, PS, value recap, risk-reversal language. Suitability-gated offers especially need a self-validation checkpoint — the reader needs a way to internally answer "is this me?" right before clicking.

### Motifs
- "Execution" overused decoratively (17 mentions, 0.4 anchor). The word becomes wallpaper.
- "Time, energy, attention" recited 4× as a triplet but each recitation doesn't earn new claim weight.

---

## Recommended sequence (operator's call, not the skill's)

1. **UMP consolidation first** — decide whether the brand-mechanism is "Stack" or "TripleStack™" and let one carry the load. Probably collapse to one.
2. **Proof inventory** — voice-mine for named outcomes; if unavailable, deepen the founder-as-proof frame with specifics.
3. **CTA architecture** — add self-validation checkpoint + PS + value recap.
4. **Motif scrub** — cut decorative repetitions of "execution" and the time/energy/attention triplet.

---

## What this skeleton does NOT do

- Does not regenerate any copy (per skill anti-patterns).
- Does not score the letter on a rubric — that's the `pre-ship-checklist-reviewer` separately.
- Does not make the taste call on which stage to re-enter — operator decides from the routing table above.
