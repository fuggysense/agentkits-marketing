# Component Inclusion Matrix

Context-aware logic for Phase 0 Context Scan. The orchestrator reads client files, evaluates the offer, and decides which of the 12 components to include, skip, or modify.

**Rule:** Context-first, framework-second. Never force a component that doesn't fit.

---

## Evaluation Matrix

| # | Component | Include By Default | Skip If... | Modify If... |
|---|-----------|-------------------|------------|--------------|
| 1 | Headline + Sub | ALWAYS | Never skip | — |
| 2 | Lead | ALWAYS | Never skip | — |
| 3 | Pain Cycle / Why Most Fail | YES | Audience has no clear "old way" to dismantle (rare) | Audience is solution-aware → soften into "most approaches fall short because" |
| 4 | Integrity Tie-Down | YES for cold traffic | Warm/branded/existing-relationship traffic | — |
| 5 | Mechanism | ALWAYS | Never skip | No named system → invent one that fits |
| 6 | Proof Stack | YES if results exist | — | No results yet → pivot entire stack to credentials/methodology/sample work |
| 7 | Offer Breakdown | ALWAYS | Never skip | — |
| 8 | Bonus Stack | YES if real bonuses | No real bonuses offered | Convert to "what's included" list if no bonuses but multi-part offer |
| 9 | Light Scarcity | YES if real capacity limit | No real cap → SKIP ENTIRELY (fake scarcity destroys trust) | — |
| 10 | Guarantee Stack | ALWAYS | Never skip — primary conversion lever | No money-back possible → use no-pitch / value-pay / outcome variants |
| 11 | CTA | ALWAYS | Never skip | — |
| 12 | FAQ (5 objections) | ALWAYS | Never skip — this is the moat | — |
| 13 | PS Line | ALWAYS | Never skip | — |

---

## Phase 0 Scan — What To Read

Auto-read these client files and extract signals:

### `clients/<slug>/context-profile.json`
- `business_type` → service / consulting / coaching / real estate / agency
- `offer_type` → consultation / audit / strategy session / discovery call
- `traffic_source` → FB / IG / Google / LinkedIn (Schwartz level inference)
- `results_available` → boolean (drives component 6)
- `capacity_limit` → integer or null (drives component 9)

### `clients/<slug>/offer.md`
- Deliverables list → feeds component 7
- Bonuses listed → drives component 8 (skip if empty)
- Guarantee language → feeds component 10 (flag if missing, require user input)
- Timeframe → "results in X days" anchor for component 5

### `clients/<slug>/buyer-profile.md`
- Pain points → feeds components 3 + 11 (FAQ)
- Past attempts → feeds component 3 (old way to dismantle)
- Objections → feeds component 11 (FAQ structure)
- Awareness level → Schwartz level → drives component 1 headline approach

### `clients/<slug>/avatars/` (if exists)
- Top 5 Deep Fears → feed into PS line (component 13)
- Raw Inner Dialogue → tone for Lead (component 2)
- Desired Transformation → Dream Outcome for Headline (component 1)
- Relationship Impact → emotional layers for Pain Cycle (component 3)

### `clients/<slug>/source-of-truth.md` (if exists)
- Section 5.5 Golden Nuggets → steal-worthy copy angles
- Section 5.7 ICP Language → verbatim phrasing for Lead + Pain
- Section 7.5 Misconceptions → fuel for component 3 dismantling

### `clients/<slug>/brand-voice.md`
- Tone anchors → every component
- Forbidden words/phrases → hard constraints
- Signature moves → weave into Lead + PS

---

## HITL Gate Output Format

After auto-scan, present this to user for 1-screen review:

```
PHASE 0 CONTEXT SCAN — [client-slug]

Offer type: [consultation / audit / strategy session]
Traffic: Cold [FB/IG] → Schwartz Level [2-3]
Baseline metrics: Opt-in [X%], CTR [Y%], CPC [$Z]
Target: Opt-in > [baseline × 1.5]

COMPONENT INCLUSION:
✓ 1 Headline + Sub        [confirmed]
✓ 2 Lead                  [confirmed]
✓ 3 Pain Cycle            [confirmed — uses "cold lead chase" loop]
✓ 4 Integrity Tie-Down    [cold traffic → include]
✓ 5 Mechanism             [confirmed — "[X] Method"]
✓ 6 Proof Stack           [12 client testimonials available]
✓ 7 Offer Breakdown       [confirmed]
✗ 8 Bonus Stack           [SKIP — no bonuses in offer.md]
✓ 9 Light Scarcity        [5 consultations/month confirmed]
✓ 10 Guarantee Stack      [using value-pay variant — $100 Grab]
✓ 11 CTA                  [confirmed]
✓ 12 FAQ (5 objections)   [confirmed]
✓ 13 PS Line              [confirmed]

MISSING INPUTS:
- [ ] Specific client result numbers for proof stack (have testimonials, need $ figures)
- [ ] Guarantee amount for value-pay variant (recommend $100 Grab or similar)

Proceed? [Y/n] Adjust? [specify which component]
```

User confirms or adjusts → drafters receive finalized matrix → Phase 1 begins.

---

## Decision Heuristics

### When to SKIP a component entirely

- **Bonus Stack (8):** No real bonuses exist. Don't invent them.
- **Light Scarcity (9):** No real capacity limit. Fake scarcity reads as manipulation.

### When to MODIFY a component

- **Proof Stack (6) with no proof:** Pivot to methodology-credentials. List what frameworks inform the method (Hormozi, Kennedy, Halbert), who mentored the founder, industry data supporting the approach.
- **Guarantee Stack (10) for free consultation:** Can't offer money-back. Use no-pitch ("if we can't help in 10 min, we end the call"), value-pay ("waste your time = we pay you"), or outcome ("3 insights or we pay").
- **Mechanism (5) with no named system:** Invent one. "The [Client Name] Method" or "The [Industry] Framework." Must be branded.

### When to DEMAND user input before drafting

- Offer.md missing concrete deliverables
- Buyer-profile.md missing specific objections
- No guarantee mechanic specified AND client won't offer money-back
- Claimed results have no backing documents

Do NOT proceed with drafting if any of these are missing. Surface to user and wait.

### Voice register / narrator POV (ask upfront — auto-reject if guessed)

Long-form letters fail when the narrator's identity is ambiguous. The reader can tell the voice was guessed and the register drifts mid-letter. Resolve narrator POV BEFORE drafting:

> Who narrates this letter?
>
> 1. **The avatar themselves** — high relatability, low authority. Best for emotional-led offers.
> 2. **A peer who solved the same problem** — relatable + outcome-credible. Most letters work here.
> 3. **A former clinician / former operator / retired specialist** — high authority. **MEDIUM regulatory risk in medical/financial verticals.**
> 4. **A current clinician / current licensed operator** — **DO NOT recommend.** FTC disclosure issues + Meta ad-policy risks. Use "former" framing or "peer who consulted with their clinician" instead.
> 5. **A journalist / independent researcher** — high authority, requires real credentials.
> 6. **The operator (the person selling)** — direct, common in service / agency / coaching. Halbert's "Dear [avatar]" pattern lives here.
> 7. **Custom** — operator specifies (founder origin story, partner POV, etc.)

**Capture the choice in Phase 0 output.** All drafters in Phase 1 receive the chosen register and must hold it consistently. Mid-letter register drift = auto-reject in Conversion Gate.

**Regulatory warning:** If the operator chooses option 4 (current clinician) or any narrator making product recommendations in a regulated vertical (health / finance / legal), surface the compliance risk before drafting. Default to option 3 ("former") or option 2 ("peer who consulted") instead.

---

## Industry Tweaks (not client-specific — industry-level guidance)

### Real Estate (SG)
- Weave MOP / CPF / en-bloc / school zone language where relevant
- Component 3: dismantle "traditional agent approach" (prospecting, cold calls, Zillow leads)
- Component 5: name the methodology (Entry Price Pattern, Transaction Timing, etc.)
- Component 6: include local client names + districts for hyper-local proof

### Real Estate (US)
- Weave MLS / off-market / cash buyer language
- Component 3: dismantle "list and wait" or "Zillow-dependent" workflows
- Component 5: tech-forward mechanism framing (AI, data, automation)

### Consulting / Agency
- Component 4: strong integrity tie-down (audience is skeptical)
- Component 5: emphasize DONE-FOR-YOU over DIY
- Component 6: case studies with $ figures > testimonial quotes

### Coaching / Info Product
- Component 5: numbered framework ("7 Laws," "5 Keys," "3 Phases")
- Component 6: graduated case study ladder (small → large wins)
- Component 1: outcome + timeframe ("retire X years earlier")

---

## Vertical-Specific Failure Modes (Phase 0 enrichment)

Industry Tweaks (above) tells you what to *emphasize* per vertical. Failure Modes tells you what specific *prior-attempt scenes* to dramatize in the Pain Cycle (Component 3).

Every vertical has 2–3 canonical "tried-and-failed" stories the prospect has already lived through. If your letter doesn't name one of these specifically — with sensory detail the prospect would recognize — the Pain Cycle reads as generic. The reader feels seen only when their exact failure scene appears on the page.

**Phase 0 must extract these from `buyer-profile.md` (or interview the operator) BEFORE drafting.**

### Real Estate (SG first-time buyers)
- **Excel-sheet research spiral** — couple builds a spreadsheet, runs the math, builds another, never decides
- **Showflat-tour exhaustion** — 5+ weekends of viewings, "let's sleep on it," nothing closes
- **Calculator-only research** — bank affordability calc shows what they'll lend, not what to actually buy
- **Conflicting agent advice** — three agents, three different "best" districts, paralysis

### DTC supplements / wellness
- **Stack-and-pray** — 4-6 supplements running simultaneously, no idea which is doing what
- **Doctor dismissal** — "your numbers are normal, you're just stressed" with no path forward
- **Melatonin / first-line failure** — tried the obvious, brief help, then back to baseline (or worse)
- **Brand-hopping** — switching brands of the same category looking for the one that works

### B2B SaaS / agency / consulting
- **Tool-stack consolidation attempt** — bought 4 tools, integration broke, back to spreadsheets
- **In-house hire that didn't stick** — hired a specialist, 6 months in, output below DIY baseline
- **DIY-then-burn-out** — operator tried to learn it themselves, lost 3 months, still on square one
- **"We just need better processes"** — wrote the SOP, nobody follows it, drift returns within weeks

### Coaching / info product
- **Course-graveyard** — 3+ courses purchased, none completed past Module 2
- **Free content paralysis** — saved 100+ YouTube videos, watched none, still stuck
- **Mentor-mismatch** — paid for 1:1 coaching that didn't fit the operator's actual context
- **Identity-incongruent method** — tried a system designed for someone with a different starting identity (extrovert system applied to introvert operator)

### Application

Pick 2-3 failure modes that match the avatar in `buyer-profile.md`. Drop them into Component 3 (Pain Cycle) as named scenes — verbatim language, sensory detail, the specific moment of recognition. Test: would the prospect read this and think "that's exactly what happened to me"? If not, the failure mode isn't sharp enough.

If `buyer-profile.md` doesn't surface concrete prior-attempt failures, **halt drafting and surface to operator** before Phase 1. Generic Pain Cycles auto-reject in Conversion Gate.

---

## Cross-Cutting Requirements (NEW — promoted from partial coverage)

These are NOT new components — they are **threads that must run through existing components**. Conversion Gate will auto-reject letters that miss them.

### R1. Objection Architecture (required)

Full spec: `references/objection-architecture.md`.

10 canonical objections mapped to placement across components 3, 5, 6, 7, 9, 10, 11, 12, 13. Body copy preempts the top 5-7 inline; FAQ consolidates residual. Risk objection is resolved in Guarantee Stack, never mentioned-without-handled.

### R2. Qualification (required — at least 1 block)

Full spec: `references/qualification-patterns.md`.

At minimum one of these blocks must appear:
- **Who this is for** (testable conditions) — in Lead or mid-body
- **Who this isn't for** (real disqualifiers) — after Offer or before Guarantee
- **Readiness criteria** — immediately before final CTA

Letter length determines how many blocks to include (see qualification-patterns.md calibration table).

### R3. Trust Density (required — 5+ signals minimum)

Full spec: `references/trust-density.md`.

≥ 5 distinct signal types across the 10 listed (constraint disclosure, realistic timeline, named conditions, transparent process, proof with context, who-it-isn't-for, operator realism, specific numbers, operational visibility, appropriate hedging). Distributed across 3+ components. Every confident claim paired with a credibility signal within 3 sentences.

### R4. Mechanism Justification (extends Component 5)

Full spec: `references/mechanism-justification.md`.

Component 5 (Mechanism) now has **5 jobs**, not 4:
1. Name the system
2. Describe function
3. Visualize + compress journey
4. **JUSTIFY** — use 1-2 of 4 patterns (Cause-and-Effect / Contrast / First-Principles / Constraint)
5. Anchor with numbers + time

### R5. Cohesion (stitcher requirement)

Full spec: `references/cohesion-check.md`.

Phase 2 Stitcher must run a cohesion check across all 11 section boundaries. `jump` rate ≤ 15% total; 0 `jump` at the 5 critical boundaries (H→S, S→L, L→P, P→M, CTA→PS).

---

## Updated Conversion Gate Checks

Conversion Gate now verifies (in addition to existing checks):

- [ ] All 10 canonical objections addressed somewhere (inline or FAQ)
- [ ] At least 1 qualification block present with testable conditions
- [ ] ≥ 5 trust signal types used, distributed across 3+ components
- [ ] Mechanism section contains at least 1 of the 4 justification patterns
- [ ] Cohesion report shows ≤ 15% `jump` transitions, 0 at critical boundaries
- [ ] Markup convention applied: `(h)`, `(b)`, `(u)` per `references/markup-convention.md`

---

## Reminder

Do not cargo-cult Hormozi. His 13 components were designed for high-ticket info products with disclosed prices. This skill is for lead-gen consultations where the price isn't disclosed. Adapt, don't obey.
