---
file_type: reference
component: all-12 + 5-cross-cutting
load_when: Phase 0 Context Scan picks which components to write; reviewer asks "is this letter missing a required move?"
loads_from_research: classical-exemplars (7 letters), strong-exemplars (8 modern letters)
last_updated: 2026-05-27
---

# The 12-Component Matrix

## What this file is about

A sales letter is built from a fixed set of moves. Twelve of them. Not every letter uses all twelve — Phase 0 picks the ones that fit the offer. This file tells you which ones to include, which ones to cut, and which ones to bend per industry.

On top of the twelve there are five threads that must run through every letter — objection handling, who-it's-for, trust signals, mechanism proof, and section-to-section flow. Miss one and the Conversion Gate auto-rejects.

**Rule:** the offer picks the components. Don't force a move that doesn't fit. A transactional cash-buy letter (Syncom XiJt) has no mechanism because there is no transformation — just "we buy, we pay cash." Forcing one would read fake.

---

## The 12 components

| # | Component | Include by default | Skip if | Modify if |
|---|---|---|---|---|
| 1 | Headline + sub | ALWAYS | never | — |
| 2 | Lead | ALWAYS | never | — |
| 3 | Pain cycle / why most fail | YES | audience has no "old way" to dismantle (rare) | solution-aware → soften to "most approaches fall short because" |
| 4 | Integrity tie-down | YES for cold | warm / branded / existing relationship | — |
| 5 | Mechanism | USUALLY | transactional offer with no transformation (e.g. cash-buy real estate) | no named system → invent one |
| 6 | Proof stack | YES if results exist | — | no results → pivot to credentials, methodology, sample work |
| 7 | Offer breakdown | ALWAYS | never | — |
| 8 | Bonus stack | YES if real bonuses | no real bonuses — never invent | multi-part offer with no bonuses → convert to "what's included" |
| 9 | Light scarcity | YES if real cap | no real cap → SKIP (fake scarcity destroys trust) | — |
| 10 | Guarantee stack | ALWAYS | never — primary conversion lever | no money-back possible → no-pitch / value-pay / outcome / PWYW |
| 11 | CTA | ALWAYS | never | — |
| 12 | P.S. block | ALWAYS for letters 1,500+ words | very short letters (under 800 words) | full spec → `best-practices/ps-architecture.md` |

The full 12-row checklist evidence sits in `research/classical-exemplars/annotated/*.md` and `research/strong-exemplars/annotated/*.md`. Every annotated letter scores each component PRESENT / IMPLIED / ABSENT with verbatim evidence.

---

## What the evidence shows

- **Headline, Lead, CTA**: present in all 15 annotated letters. Non-negotiable.
- **P.S. block**: present in 7/7 classical letters, **0/8** modern letters. The single biggest gap modern letters carry. See `best-practices/ps-architecture.md`.
- **Mechanism**: named in 5/7 classical, 2/8 modern. Modern letters lean on "vast network of lenders" or "advanced machine" — descriptive language, no brand. Naming the mechanism is the strongest under-used move.
- **Guarantee**: present in 6/7 classical (often hard money-back), present in 6/8 modern (mostly soft behavioral promises). Verbal-only guarantees are weaker than money-back or PWYW.
- **Scarcity**: present in 4/7 classical, 2/8 modern. Modern letters are missing real time pressure. Forced scarcity reads worse than no scarcity — only include if real.

---

## 5 cross-cutting requirements

These are NOT new components. They are threads that must run through the existing 12. Conversion Gate rejects letters that miss them.

**R1. Objection architecture** — Full spec: `references/objection-architecture.md`. The top 5-7 of 10 canonical objections handled inline in the body; the rest in FAQ. Risk handled in guarantee, never raised-without-answered.

**R2. Qualification** — Full spec: `references/qualification-patterns.md`. At least one of: "who this is for" (testable conditions), "who this isn't for" (real disqualifiers), or readiness criteria. Chester Buczynski's "if you're under $500,000 in annual revenue this is not for you" is a clean disqualifier — gates by size and signals confidence.

**R3. Trust density** — Full spec: `references/trust-density.md`. 5+ distinct signal types across 3+ components. Every confident claim paired with a credibility signal within 3 sentences. Hopkins-Schlitz is the masterclass: 50-year reputation, 4,000-ft wells, 1,200 yeast experiments, plate glass, twice-daily cleaning — six trust signals in two paragraphs.

**R4. Mechanism justification** — Full spec: `references/mechanism-justification.md`. Mechanism (component 5) has 5 jobs now: name it, describe function, visualize journey, **justify** (cause-effect / contrast / first-principles / constraint), anchor with numbers + time.

**R5. Cohesion** — Full spec: `references/cohesion-check.md`. Phase 2 Stitcher runs the 11-boundary check. `jump` rate ≤ 15% total, 0 at the 5 critical boundaries (H→S, S→L, L→P, P→M, CTA→PS).

---

## Industry tweaks

Each vertical has its own emphasis. The named mechanism, the proof type that matters, the scarcity that's real.

### Info products / coaching (high-ticket)
- **Component 5**: numbered framework. Chester Buczynski named his "7 Sales Laws." Karbo invented "Dyna/Psyc." Coaches need a proprietary label — descriptive language ("our coaching method") reads generic.
- **Component 6**: graduated case study ladder (small → large wins). George Ten anchored his $97 offer against his "$2,500 program, 81 students paid" Stripe screenshot.
- **Component 9**: qualifier scarcity beats deadline scarcity. "Under $500K — not for you" (Green Industry) signals confidence and filters the list.

### Agency / consulting / B2B
- **Component 4**: strong integrity tie-down — this audience is the most skeptical in the corpus.
- **Component 5**: DONE-FOR-YOU over DIY framing.
- **Component 6**: named-client case studies with $ figures. RoofGrow's "DTH Roofing NY, Mike's Roofing NM, Cool Roofs OH, Keystone Exterior — $300k in 30 days" is the template. Aggregate proof ("150+ roofers") is weak; specific names are strong.

### Financial services / lending
- **Component 5**: usually descriptive, not branded ("vast network of lenders" — Joe Bellantuono, Brendon Luu). The credential carries the load instead.
- **Component 6**: tenure proof. "30 years on Wall Street" (Bellantuono). "500+ home buyers" (Luu).
- **Component 10**: behavioral promise instead of money-back. "I will NEVER waste your time / NEVER hit you with hidden fees" (Luu). Lender-paid models can't offer refunds — the guarantee has to be a stance.
- Compliance: extra care on claim language. Loose words in the body re-appear in the P.S.

### Real estate (transactional cash-buy)
- **Component 5**: SKIP. "We buy, we pay cash, period" (Syncom XiJt). No transformation, no mechanism. Forcing one reads fake.
- **Component 6**: geographic affinity beats credentials. "We are Polk County residents" outperforms "we have 20 years of experience."
- **Component 7**: explicit deliverable list ("no closing costs, no renovations, no hidden fees, no commissions, no catch") functions as the guarantee.

### Real estate (advisor / agent / first-time buyer)
- **Component 3**: dramatize a named failure scene. SG: Excel-sheet research spiral, showflat-tour exhaustion, conflicting agent advice. US: list-and-wait, Zillow-dependent. Generic Pain Cycles auto-reject.
- **Component 5**: name the methodology — Entry Price Pattern, Transaction Timing.
- **Component 6**: local client names + districts for hyper-local proof.

### DTC supplements / wellness
- **Component 3**: name the prior-attempt failure — stack-and-pray (4-6 supplements at once), doctor dismissal ("your numbers are normal"), first-line failure (melatonin → back to baseline), brand-hopping.
- **Component 5**: must be science-anchored AND safe-feeling. Schwartz's "modern Chinese Medicine" hit both — ancient authority plus "modern" safety prefix.
- **Component 6**: process specificity. Hopkins-Schlitz proved this for any consumable: "plate-glass rooms, filtered air, white-wood pulp, 4,000-foot wells, 1,200 experiments." Stats do the work testimonials would in coaching.
- **Component 10**: must clear FTC. No "cure" language. Money-back is standard.

---

## Voice register / narrator POV (resolve BEFORE drafting)

Letters fail when the narrator's identity is ambiguous. Mid-letter drift = auto-reject. Pick one and hold it:

1. **The avatar themselves** — high relatability, low authority.
2. **A peer who solved the same problem** — relatable + outcome-credible. Most letters work here.
3. **A former clinician / former operator / retired specialist** — high authority. MEDIUM regulatory risk in medical/financial.
4. **A current clinician / current licensed operator** — DO NOT recommend. FTC + Meta ad-policy risk.
5. **A journalist / independent researcher** — high authority, real credentials required.
6. **The operator** — direct. Halbert's "Dear [avatar]" pattern lives here. Most modern letters in the corpus use this.
7. **Custom** — operator specifies (founder origin story, partner POV, etc.)

Capture in Phase 0. All drafters in Phase 1 receive the chosen register.

---

## Reviewer checks (Conversion Gate)

- [ ] All 10 canonical objections addressed (inline or FAQ)
- [ ] At least 1 qualification block with testable conditions
- [ ] 5+ trust signal types, distributed across 3+ components
- [ ] Mechanism has at least 1 of the 4 justification patterns
- [ ] Cohesion ≤ 15% jump transitions, 0 at critical boundaries- [ ] P.S. block present for letters 1,500+ words (see `best-practices/ps-architecture.md`)
- [ ] Narrator POV held consistently end to end

---

## Linked files

- `best-practices/ps-architecture.md` — full P.S. spec (Component 12)
- `best-practices/fact-headlines.md` — Component 1 craft
- `best-practices/damaging-admission.md` — cross-cutting trust move
- `best-practices/cohesion-check.md` — Phase 2 boundary check (R5)
- `references/qualification-patterns.md` — Component 2 + R2 spec
- `references/trust-density.md` — R3 spec
- `references/objection-architecture.md` — R1 spec
- `references/mechanism-justification.md` — R4 spec
- `references/copy-gems.md` — universal-gap inventory (line ~184: P.S. listed as one of four moves 8/8 modern letters missed)
- `research/classical-exemplars/annotated/*.md` — 7 letters, full 12-row checklist each
- `research/strong-exemplars/annotated/*.md` — 8 modern letters, same checklist
