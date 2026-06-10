# Objection Matrix Builder — Pre-Write Grounding Support

**Source:** Mark Masters, cai #36 — 6 objection categories framework. Pre-write grounding layer. Feeds the drafter + `reviewers/objection-coverage-audit.md`.

**Core principle:** Before copy is drafted, map every objection the buyer actually raises — sourced from research, forums, sales calls, churn interviews, support tickets — into 6 canonical categories. Each objection pairs with a handler grounded in THIS client's real context, not generic copywriting advice. The drafter pre-empts objections rather than ignoring them; `objection-coverage-audit` verifies all 6 categories were addressed.

**Agent model:** Builder sub-agent. Fires PRE-DRAFT in parallel with `proof-inventory-builder`. Writes `clients/<slug>/copy-system/objection-matrix.md`. Output consumed by: the drafter (pre-emption guidance) + `reviewers/objection-coverage-audit.md` (verification pass).

## Inputs

Read all files that exist. Skip gracefully if absent; log which were missing in the metadata block.

| File | What to extract |
|------|----------------|
| `clients/<slug>/buyer-profile.md` | Pain points, fears, hesitations |
| `clients/<slug>/learnings.md` | Objections the operator has heard repeatedly |
| `clients/<slug>/source-of-truth.md` | §7 Objections, §7.5 Misconceptions (if present) |
| `clients/<slug>/faqs.md` | Questions that mask objections |
| `clients/<slug>/research/buyer-language-dossier.md` | Raw buyer concerns, verbatim forum/review language |
| `clients/<slug>/avatars/*.md` | Top 5 Deep Fears + Objections blocks per avatar |
| `clients/<slug>/interviews/*.md` | Sales-call transcripts, churn interviews |

## The 6 Objection Categories (cai #36)

| Code | Category | Canonical signal |
|------|----------|-----------------|
| **O1** | **Price** | "Too expensive / not in budget / cheaper alternative exists" |
| **O2** | **Trust** | "You might not deliver / I don't know you / social proof thin" |
| **O3** | **Fit** | "Doesn't apply to me / my situation is different / too small/big/early/late" |
| **O4** | **Timing** | "Not now / I'll come back later / need to think about it" |
| **O5** | **Authority** | "Need to ask my spouse/partner/boss / can't decide alone" |
| **O6** | **Effort** | "Too hard to implement / steep learning curve / I don't have time" |

## Procedure

### Step 1 — Load inputs

Read every file in the Inputs table. Note each as PRESENT or ABSENT. If fewer than 3 input files exist, prepend a `THIN_BASE` warning to the output metadata block but continue — do not abort.

### Step 2 — Extract objection-shaped statements

Scan all loaded content for any sentence expressing: hesitation, fear, comparison to alternatives, deferral, delegation to another decision-maker, or effort concern. Pull verbatim where the source is concise (forum post, testimonial, interview quote). Paraphrase only when the source is discursive (long transcript). Record source file + section/line reference for every extracted statement — no orphan objections.

### Step 3 — Classify into O1–O6

Assign each extracted statement its single best-fit category code. If a statement genuinely spans two categories (e.g., "it's too expensive AND I'd need to convince my business partner"), log it in both category tables AND add it to the Cross-category section with both codes noted.

### Step 4 — Write grounded handlers

For each objection, write a handler of 1–3 sentences that:

1. Acknowledges the objection without dismissing it
2. Reframes or resolves it using a specific client fact, proof element, mechanism, or testimonial drawn from the input files — no generic reassurance
3. Matches the client's voice register (use `buyer-language-dossier.md` as the register reference; preserve Singlish or UK English where client voice demands)

If no grounded handler can be assembled from available client material, flag the objection `HANDLER_GAP` and leave the handler field blank. The operator must supply the missing proof before copy ships.

### Step 5 — Flag category gaps

If any of O1–O6 has fewer than 2 concrete objections sourced from this client's buyers (not generic examples), mark the category `GAP`. Log it in the Gaps section with a specific research action (e.g., "Run 3 buyer interviews focused on pricing hesitation — ask: what made you pause before buying?").

### Step 6 — Rank by source frequency

Within each category, order objections by number of distinct source files they appear in (highest first). Ties broken by source recency: interviews > `learnings.md` > `buyer-profile.md` > `buyer-language-dossier.md`.

### Step 7 — Emit output

Write `clients/<slug>/copy-system/objection-matrix.md`. If the file already exists, back it up to `objection-matrix.md.prev` before overwriting.

## Output Schema

```
## OBJECTION MATRIX
Client: <slug>
Built: YYMMDD-HHMM
Sources loaded: N / 7  (missing: <list absent files>)
Total objections extracted: N
Handler gaps (HANDLER_GAP): N
Category gaps (GAP): N / 6
Flags: [THIN_BASE] [LOW_VOLUME] [OK]

---

### O1 — Price
_"Too expensive, not in budget, cheaper alternative exists."_

| # | Objection | Source | Handler | Proof source | Tone note |
|---|-----------|--------|---------|--------------|-----------|
| 1 | "I can get a freelancer to do this for half the price" | buyer-language-dossier.md §Pricing | "Freelancers quote the deliverable; we own the outcome. [Client X] recovered 3× the fee in month one — see case study in learnings §4." | learnings.md §4, case study John D. | Calm, no defensiveness |
| 2 | HANDLER_GAP — "It's a lot for a small business" | interviews/call-01.md §12 | [operator to supply — no matching proof in files] | — | — |

[Repeat table structure for O2 – O6]

---

### Cross-category objections
| Objection | Primary | Secondary | Handler | Proof source |
|-----------|---------|-----------|---------|--------------|
| "I want to try it but I need to check with my accountant first" | O5 Authority | O1 Price | "We can hold your spot for 48 hours and send you a one-page ROI summary to share — [Client Y] used it to get sign-off in a day." | learnings.md §7 |

---

### Gaps
| Category | Status | Objections found | Research action |
|----------|--------|-----------------|----------------|
| O5 — Authority | GAP | 0 concrete | Interview 3 recent buyers: "Who else was involved in your decision?" |
| O6 — Effort | GAP | 1 (below threshold) | Pull support tickets for setup/onboarding complaints |

---

### Pre-emption priority (drafter guide)
| Category | Lead objection to address first | Appears in N sources | Placement suggestion |
|----------|---------------------------------|----------------------|---------------------|
| O1 | "I can get a freelancer cheaper" | 4 / 7 | Price justification — above first CTA |
| O2 | "I've never heard of you" | 3 / 7 | Hero section — social proof cluster |
| O3 | "I'm too early-stage for this" | 2 / 7 | Fit qualifier — lead copy |
| O4 | "Let me think about it" | 3 / 7 | Urgency/scarcity block — below guarantee |
| O5 | [GAP — insufficient data] | — | — |
| O6 | "I don't have time to set this up" | 2 / 7 | Mechanism section — effort-reduction proof |
```

## Failure Thresholds

- Any O1–O6 category with **zero** concrete client-sourced objections → **CRITICAL GAP**: builder emits file with a `⚠️ CRITICAL` header on that category; drafter MUST NOT proceed without operator resolution
- Any handler missing a proof-source reference → **HANDLER_GAP** (MEDIUM): listed in Gaps section; handler ships to drafter marked ungrounded — drafter may use it but must not cite it as proven
- Fewer than **12 objections** total across all 6 categories → **LOW_VOLUME** (HIGH): thin base; recommend research refresh before drafting commences
- Fewer than **3 source files** loaded → **THIN_BASE** (HIGH): output is indicative only; all handlers treated as provisional; flag in copy brief
- A handler that resolves an objection using only reassurance language ("it's actually easy!") without a client-specific fact → **HANDLER_GAP** regardless of whether a source reference exists; reassurance is not proof

## The Two Quick Wins to Look For First

1. **Timing masking Price or Trust** — when O4 entries outnumber O1 + O2 combined, flag: *"Timing objections may be concealing unresolved Price or Trust concerns — probe before drafting O4 handlers."* "I need to think about it" rarely means time; it usually means unresolved doubt.

2. **Effort objections without mechanism copy** — O6 cannot be resolved with reassurance alone. Every O6 handler must cite a specific mechanism: a setup time, a done-for-you component, a step count, or a case study of a non-technical buyer who succeeded. Any O6 handler that contains the words "easy", "simple", or "straightforward" without a mechanism following immediately → flag as `HANDLER_GAP`.

## Invocation

- Called pre-draft by all `/copy:*` sub-commands in parallel with `proof-inventory-builder`
- Manual re-run: `/copy:build-objections <slug>` (roadmap item — add to `commands/copy/`)
- Re-runs overwrite `objection-matrix.md`; previous version backed up to `objection-matrix.md.prev`

## Logging

Append to `clients/<slug>/copy-system/quality-gates/builder-log.md` (shared log with proof-inventory-builder):

`| YYMMDD-HHMM | objection-matrix-builder | sources N/7 | objections N | handler-gaps N | category-gaps N/6 | THIN_BASE/LOW_VOLUME/OK |`
