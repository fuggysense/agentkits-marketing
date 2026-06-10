---
name: sales-letter-audit
description: "Audit finished sales letters via Schwartz/Halbert lens: awareness, sophistication, channel, A/B-pile, specificity. Diagnostic + client briefs. NOT for greenfield — for judgment only. Hand rewrites to sales-letter-method."
---

# Sales Letter Audit

You are reading the letter the way **Eugene Schwartz** reads it — through awareness and sophistication, through channel-vs-create, through the moment of arrival. You are reading it the way **Gary Halbert** sorts mail — A-pile or B-pile, written to one person or to a category, specific enough to make the reader feel known or generic enough to be sent to anyone.

You are not improving the letter. You are judging it.

The audit ends with a brief. **The brief is not a rewrite.** Deeper persuasion work — UMP rebuild, identity ladder, proof inventory, objection matrix, channeling depth, offer architecture — happens downstream in `sales-letter-method`, which is the forward pipeline this skill feeds into. This skill stops at diagnosis.

## Required inputs

- A finished sales letter at a known path (typically `clients/<project>/copy/<letter-name>.md`, or pasted at run-time into a `scratch/audits/<project>/` sandbox)
- The project's stage_outputs directory (to detect which upstream artifacts already exist), OR `clients/<project>/` for projects using the `sales-letter-method` skill convention

If the source letter is missing, halt and ask the user for the path.

## The job

Read a finished sales letter and produce a `letter-skeleton.json` that conforms to the skeleton contract (see `skeleton-contract.md` in this skill folder). The skeleton lets the operator (or a downstream regen skill) route back into the forward pipeline at the broken stage instead of regenerating from scratch.

Two distinct outputs:
1. **Structural skeleton** (`<letter>-skeleton.json`) — sits next to the source letter
2. **Inferred upstream research** (sandbox) — if Phase 2 ran, writes to `clients/<project>/reverse/{purple-ocean,mass-desires,customer-avatar}-inferred.md`. Requires human approval before it can overwrite real stage artifacts.

## Procedure

### Step −2: Anchor the three goals (HARD GATE — DO NOT SKIP)

Before reading the letter, the operator (or calling skill) must declare three things explicitly. If any are missing, halt and ask:

1. **Purpose of letter** — one sentence on what this letter is trying to make happen.
2. **CTA target** — one sentence on what the CTA button needs to achieve (e.g., "Request Private Access → suitability application form → assessment call").
3. **Final goal** — one sentence on the actual outcome being chased (e.g., "Qualified applicants who pass suitability and become Stack clients").

Without these three anchors, every audit finding is judged against an assumed goal that may be wrong. Record verbatim in `extraction_metadata.declared_anchors`.

### Step −1: Detect client context branch (loaded is the default expectation; cold is the exception)

Auto-detect whether a `clients/<project>/` folder is loaded for the active project. **Loaded is the default expectation** — every production audit should ground findings in the buyer dossier. Cold is the rare exception (greenfield letters with no client research yet).

- **Loaded** (path exists with `context-profile.json`, `icp.md`, `offer.md`, `buyer-profile.md`, AND `avatars/01-...md` through `avatars/05-...md`): set `context_branch = "loaded"`. **MANDATORY:** before scoring any finding, read `buyer-profile.md` in full AND every `avatars/*.md` file in full. These are the verbatim buyer-language source. Every `[H]` and `[M]` finding will be checked against this dossier in Step 9c. Skip the heavy reverse-inference work (Phase 2).
- **Cold** (no client folder, or dossier missing/sparse): set `context_branch = "cold"`. Run the full heavy-inference path — Purple Ocean / Mass Desires / Customer Avatar inferred from the letter alone. **Emit a visible warning at the top of the operator brief and client brief:** "⚠ Audit ran without buyer dossier — every finding is reviewer-judgment-only, not VOC-traceable. Recommend running `buyer-language-researcher` before re-judging."

Record `context_branch` in `extraction_metadata`.

### Step 0: Detect upstream artifact state

Check for existing stage outputs:
- `stage_outputs/03_purple_ocean.md`
- `stage_outputs/04_mass_desires.md`
- `stage_outputs/05_customer_avatar.md`

If ALL three exist and have non-trivial content (>200 words each, not just headers): **set `phase_2_should_run = false`**. Phase 1 still runs.

If ANY of the three is missing, empty, or stub-only: **set `phase_2_should_run = true`**.

Record the detected state in `extraction_metadata`.

### Step 1: Read the source letter in full

Don't skim. Word-level positions matter — the contract requires `arrival_word_index` for the UMP, `word_index` for each identity layer, exact verbatim quotes for concentration alternatives.

Number the words as you read so you can cite positions accurately.

---

## Phase 1 — Structural Extraction (ALWAYS RUNS)

### Step 2: Extract `meta`

- `word_count` — exact count
- `audience_inferred` — best guess at the target segment from internal evidence (who the letter speaks to, what life context appears)
- `verticals_detected` — list ALL audience verticals the letter touches. If the letter speaks to two segments, list both. This is the segment-leakage canary (e.g., a "first-timer" headline that contains upgrader content).

### Step 3: Extract `ump` (Unique Mechanism Position)

- `articulated_concept` — the conceptual UMP in plain language (e.g., "structurally-impossible-to-derive-alone number")
- `branded_terms[]` — every trademarked / capitalized mechanism name. For each: `name`, `occurrence_count`, `first_appearance_word_index`. Multiple branded terms = proliferation risk; flag for `unique-mechanism` re-entry.
- `arrival_word_index` — at what word position is the mechanism first articulated. >500 = late arrival, flag.
- `prior_solution_link` — does the UMP explicitly contrast against existing alternatives?
  - `structural` — the letter names a prior solution and shows why it can't produce the UMP's outcome
  - `implicit` — the contrast is gestured at but not made explicit
  - `absent` — no link to prior solutions

#### Step 3a: MAGIC name check

For the primary branded mechanism name found in the letter (the dominant entry in `branded_terms[]`), score 5 booleans against the MAGIC framework:

- **M (Magnetic reason)** — does the name imply WHY this exists / WHY now? (e.g., "Grand Opening", "Founders' Cohort", "Pre-Launch Beta")
- **A (Avatar)** — does the name call out the specific buyer segment? (e.g., "for first-time SG private property buyers")
- **G (Goal)** — does the name state the dream outcome?
- **I (Interval)** — does the name include a timeline? ("28-Day", "Quarterly")
- **C (Container)** — does the name use a unique container word? (Blueprint / Protocol / System / Method / Stack)

Output `magic_name_check` with shape `{ name_under_test, m, a, g, i, c, score (0–5), missing[] }`.

**Score interpretation:** ≤2 means the mechanism name is generic / not MAGIC-wrapped. Surface as `[M]` finding in the operator brief and route to `sales-letter-method` Phase 0.7 (mechanism architecture).

#### Step 3b: Discredit-Old-Solutions check

For each named alternative the letter dismisses, record an entry in `discredit_old_solutions[]` with shape:

```
{
  alternative_name,
  dismissal_quote,
  dismissal_word_index,
  dismissal_type: "named-with-structural-failure" | "named-no-structural-failure" | "category-only" | "absent",
  structural_failure_mode: string | null
}
```

Concrete check: does the letter name actual competitors / alternatives BY NAME and explain WHY they fail at the math/process level? Or does it stay vague ("most tools", "the usual approach") without naming, or name without explaining?

**Routing:**
- All entries `category-only`, OR `discredit_old_solutions[]` is empty → `[H]` finding (no discredit work at all). Route to `sales-letter-method` Phase 0.7.
- Dismissals named but lack `structural_failure_mode` → `[M]` finding.

This is distinct from `concentration_alternatives` (Step 7), which catches dismissals at the prose level. Step 3b catches them at the UMP/positioning level — does the letter situate itself against named competitors, or stay in a vacuum?

### Step 4: Extract `identity_ladder`

For each Schwartz layer (l1 through l4), find the moment in the letter where that layer is engaged. Record:
- `quote` — verbatim sentence
- `word_index` — position
- `location` — `headline | lede | body | close | ps | absent`

Layer mapping:
- **L1 (problem-aware)** — naming the felt problem
- **L2 (solution-aware)** — gesturing at solution categories
- **L3 (outcome-aware)** — "this is how you finish it" / mechanism delivery
- **L4 (post-decision)** — identity of the person who decides ("the couple who decides", "the one who chose this path"). If only in PS, that's a flag.

### Step 5: Map `motifs`

Identify repeated phrases that appear 3+ times. For each:
- `phrase` — exact text
- `count` — number of occurrences
- `anchor_claims_per_occurrence` — 0.0 to 1.0 — what fraction of occurrences carry actual proof weight (anchored to a claim, number, or named outcome) vs. decorative repetition.

This is the "earning repetition" check. Score by reading each occurrence in context.

### Step 6: Headline/body coherence

- `headline_phrases[]` — the 2-4 distinctive phrases in the headline + subhead
- `echo_count_per_phrase` — how many times each appears in the body. <2 echoes = headline orphan (broken coherence).

### Step 7: Concentration alternatives

Find every place where the letter dismisses an alternative path (showflat visit, agent-led tour, calculator-only research, etc.). For each:
- `alternative` — what's being dismissed
- `dismissal_type` — `feeling` (names a feeling like "stressful" or "rushed") OR `structural-failure-mode` (names a specific math/process failure)
- `quote` — verbatim

`feeling` dismissals are weak. `structural-failure-mode` is strong.

### Step 8: CTA architecture

Cross-check the letter's close (last ~300 words + PS) against the 11-element CTA checklist (canonical reference: `Marketing/skills/sales-letter-method/references/objection-architecture.md` → CTA Architecture). Output:
- `elements_present[]` — which of the 11 are present
- `word_count` — total words in the CTA section
- `guarantee_present` — boolean
- `self_validation_checkpoint_present` — boolean (does the close give the reader a way to self-test their own readiness before clicking?)

### Step 9: Proof inventory

This is the lens-blind track. Structural reviewers can pass a letter that has structural integrity but a broken trust chain in a specific section. Don't skip this.

- `named_outcomes[]` — every claim of "X happened to Y" or "Y did Z." Mark `is_placeholder: true` when the name is `[INSERT: ...]`.
- `numbers[]` — every quantitative claim. Mark `is_placeholder: true` for unfilled brackets.
- `trust_chain_gaps[]` — sections where credibility breaks. Specifically check: does each major claim section name a real outcome with a real person? "Why us" sections that rely only on credentials (not named outcomes) go here. So do "results" sections without names attached.

Output gaps as plain-language descriptions: e.g., `"'Why us' section relies on credentials only — no named first-timer outcome to anchor the trust claim"`.

### Step 9c: VOC anchor pass (loaded path only)

**Run only if `context_branch == "loaded"`.** On cold path, skip — there is no dossier to anchor against; emit the cold-path warning instead.

After collecting `trust_chain_gaps[]` (Step 9), walk every gap AND every other Phase 1 finding heading toward the brief, then look in the dossier (`buyer-profile.md` + `avatars/01..05.md`) for a verbatim buyer quote that speaks to the same concern. Record matches in `proof_inventory.voc_anchored_findings[]` with shape:

```
{
  finding_id,                 // e.g. "trust_chain_gap_2", "ump_arrival_late", "cta_missing_guarantee"
  letter_quote,               // verbatim from the letter
  letter_word_index,
  buyer_quote,                // verbatim from buyer-profile.md or avatars/*.md
  buyer_source,               // e.g. "u/Kind-Onion-6015, r/singaporefi" or "avatar-03 / verbatim quotes / line 14"
  match_strength: "direct" | "adjacent" | "no-match"
}
```

Match-strength rubric:
- **direct** — buyer quote articulates the same concern in the same register (1:1 anchor)
- **adjacent** — buyer quote is in the same emotional/objection family but not 1:1 (still usable as anchor with mild rephrase)
- **no-match** — no quote in the dossier maps to this finding (finding is reviewer-judgment-only — must be tagged `[no-VOC]` in the brief)

**Routing signal:** if `> 50%` of brief-bound findings end up `match_strength: "no-match"`, the dossier may be incomplete. Recommend a `buyer-language-researcher` refresh before re-audit. Record this signal in `extraction_metadata` as `voc_anchor_coverage`.

This step is what turns the brief from "framework lens speaking" to "buyer language speaking through the framework lens." Step 14b enforces the 3-line shape that surfaces these anchors.

### Step 9b: AI-pattern audit of source letter

Run both anti-AI checklists against the source letter. Capture matches in a new field `proof_inventory.ai_pattern_flags` (skeleton-contract.md schema bump — see contract for shape).

Checklists (load both — they cover different registers):
- `skills/copy-editing/references/overused-ai-patterns.md` — marketing/copy register: Big Contrast, Revelation Hook, Elliptical Setup, Great Reframe, Philosophical Reduction, prohibited words, formatting tells
- `skills/copy-editing/references/anti-ai-patterns.md` — analytical/encyclopedic register: negative parallelisms, vague attributions, false ranges, elegant variation, copulative avoidance, rule of three

For each match found in the source letter, record:
- `pattern` — name from the checklist (e.g. "Big Contrast", "Negative parallelism", "Revelation Hook")
- `source_file` — which checklist flagged it
- `quote` — verbatim text from the source letter
- `word_index` — position in the letter
- `severity`:
  - `soft-flag` — pattern still works for buyers but reads as default-AI in 2026; A/B test against a direct alternative
  - `hard-flag` — visibly trips a sophisticated reader; should be rewritten before ship

This is a separate concern from Step 9's `trust_chain_gaps`. Proof gaps = what the letter fails to evidence. AI-pattern flags = how the letter sounds. Both can fire simultaneously.

The plain-English brief (Step 14b) must surface every match in a "Patterns to flag" section between "What's working" and "What's broken". `hard-flag` matches get explicit rewrite recommendations; `soft-flag` matches get A/B test recommendations.

**Why this step exists:** structural extraction (Steps 2-9) catches what the letter does and doesn't do. It does not catch what the letter *sounds like*. A letter can pass every structural check and still read as AI-default. Step 9b closes that gap.

---

## Phase 2 — Inheritance Inference (CONDITIONAL)

**Run only if Step 0 set `phase_2_should_run = true`.** Otherwise skip to Step 13 with `inheritance_contracts: null`.

### Step 10: Infer purple_ocean

From the letter's audience signals, life-context details, and emotional vocabulary, infer the purple-ocean carve-out the letter is targeting. Be specific (not "first-time buyers" — instead "SG private-property first-timers, dual-income, post-launch FOMO, Excel-sheet-research personality").

Mark confidence: `high | partial | speculation`.

### Step 11: Infer mass_desires

What 2-4 mass desires does the letter activate? Pull from desire claims, future-pacing language, and the implied "what I want" the letter answers. Mark each with confidence.

### Step 12: Infer customer_avatar

A 1-paragraph avatar sketch grounded in evidence from the letter. Include: demographic guesses, identity-level fears, the specific decision they're stuck inside. Mark confidence.

Write all three to `clients/<project>/reverse/<artifact>-inferred.md` (one file per artifact). These are sandbox outputs — never overwrite stage artifacts directly.

---

## Step 13: Compute extraction_metadata

- `extracted_at` — ISO timestamp
- `extractor_version` — current skill version (start at `0.1.0`)
- `phase_2_status` — `"completed" | "skipped_upstream_present"`
- `speculation_ratio` — count of fields marked `speculation` divided by total fields with confidence markers. Phase 1 fields don't have confidence markers (they're observed, not inferred), so this only applies to Phase 2 outputs.

If `speculation_ratio > 0.30`, the consumer (operator or downstream skill) MUST halt for human review before any regen routing.

## Step 14: Write outputs

1. **Skeleton JSON:** `clients/<project>/copy/<letter-name>-skeleton.json` (conforms to `skeleton-contract.md`)
2. **Technical summary:** `clients/<project>/copy/<letter-name>-skeleton-summary.md` — one-page summary of what was extracted, key flags, recommended re-entry stage based on the contract's routing table. Uses framework vocabulary (UMP, identity ladder, motifs, etc.) — written for downstream skills and operators familiar with the forward pipeline.
3. **Inferred research (if Phase 2 ran):** `clients/<project>/reverse/{purple-ocean,mass-desires,customer-avatar}-inferred.md`

Do NOT regenerate any letter copy. Do NOT score the letter on a rubric (that's a separate review step — see `Marketing/skills/sales-letter-method/reviewers/pre-ship-checklist-reviewer.md`). Do NOT make taste calls about which stage to re-enter (operator + skeleton-contract routing table do that).

## Step 14b: Write the plain-English brief (Operator Audit Brief)

Translate the skeleton + technical summary into an operator-facing audit brief at `clients/<project>/copy/<letter-name>-plain-english-brief.md`.

**Register: OPERATOR-FACING.** Full framework vocabulary, named copywriters, master attributions intact — for Jerel's eyes only. Not for client distribution.

Open with: (1) a 1-line purpose statement declaring the four audit dimensions, and (2) a 1-line scope distinction stating this is first-pass and deeper rewrite work lives in `sales-letter-method`.

Every finding MUST be tagged `[H]`, `[M]`, or `[L]` inline at the heading (H = blocks ship-readiness or core conversion; M = costs measurable conversion but not blocking; L = polish or style).

### VOC-anchored 3-line shape (MANDATORY for [H] and [M] findings)

Every `[H]` and `[M]` finding MUST adopt the 3-line shape that surfaces the dossier anchor produced in Step 9c:

```
### [H] <finding title — state the cost directly>
Letter: "<verbatim from letter>"
Buyer (<source>): "<verbatim from dossier>"
Cost: <one-line direct cost statement, no diplomatic ramp>
→ Resolves: <action>
```

If no relevant buyer quote exists for a finding (Step 9c flagged it `match_strength: "no-match"`), append `[no-VOC]` to the heading: `### [H] <finding> [no-VOC]`. The brief still works — the tag flags reviewer-judgment-only items so the operator can see at a glance which findings are dossier-grounded vs not.

`[L]` polish findings keep the 1-line shape (do not force the 3-line shape on style items — the operator overhead isn't worth it for low-severity work).

On cold path (`context_branch == "cold"`), every finding is reviewer-judgment-only by definition. Tag every `[H]`/`[M]` heading with `[no-VOC]` and skip the `Buyer:` line in the 3-line shape. The cold-path warning at the top of the brief explains why.

### Required structure (4-section format)

```
# [Letter Name] — Operator Audit Brief

[1-line purpose: "First-pass operator audit. Four dimensions: conversion potential, grammar & clarity, anti-AI / AI-like tendencies, notes & recommendations."]
[1-line scope: "First-pass only. Deeper rewrite work downstream in sales-letter-method."]

[Header block: source path, audited date, declared_anchors verbatim,
context_branch, links to skeleton.json + summary.md]

**Severity legend:** [H] = High priority. Fix before sending traffic. Major conversion, trust, or positioning issue. [M] = Medium priority. Important, but not usually a deal-breaker. [L] = Low priority. Polish, clarity, or testing note.

## Summary scores (1–5, 5 = strongest)

| Dimension | Score | One-line read |
|---|---|---|
| Conversion potential | N | ... |
| Grammar & clarity | N | ... |
| Anti-AI / AI-like tendencies | N | ... |
| Mobile readability | N | ... |
| **Overall ship readiness** | N | ... |

## Conversion Potential
One-line read for EVERY major copy element (coverage discipline — even working elements):
- Headline: [read] [H/M/L only if flagged]
- Lead / subhead: [read]
- Benefits: [read] [H/M/L if flagged]
- Proof: [read] [H/M/L if flagged]
- CTA: [read] [H/M/L if flagged]

Strategic findings (3–5 numbered, each with → Recommendation #N pointer and [H/M/L] tag)

## Grammar & Clarity
Sentence-level findings / Repetition fatigue / Mobile readability / Singapore-streets test (SG-targeted only; drop for non-SG)
Each finding tagged [H/M/L].

## Anti-AI / AI-like tendencies
[OPEN WITH: one sentence declaring which signals were checked — em-dash density, rule-of-three stacking, Big Contrast form, negative parallelism, no-X stacking, aphoristic reduction, revelation hooks, AI-default vocabulary. Methodology transparency = systematic, not vibes-based.]
### Hard flags — rewrite before ship   [pattern + checklist source + verbatim quote + explicit fix or A/B candidate]
### Soft flags — work for buyers, A/B-worthy   [same shape]

## Notes & Recommendations
[Numbered list. Each item tagged [H/M/L]. Action sentence + → "Resolves: §X #Y" traceability back to specific finding.]
```

### Scoring rubric (1–5)

For each of the 5 summary-score dimensions, anchor the score against these definitions:

- **5 — Ship-ready.** No structural issues; minor polish only.
- **4 — Strong with fixable gaps.** A few specific items to address; nothing blocking.
- **3 — Mixed.** Real strengths AND real gaps. Worth fixing before ship.
- **2 — Has blockers.** One or more items that will visibly trip a sophisticated reader.
- **1 — Foundational rebuild.** The dimension fails its job; needs upstream re-derivation.

The **Overall ship readiness** score is the lowest of the four sub-scores (the weakest dimension governs).

### Sub-section content guidance

**Conversion Potential** — "Headline / benefits / CTA quick-check" uses three lines:
- Headline grabs attention: ✅ / ⚠️ / ❌ with one-line reason
- Benefits clear: ✅ / ⚠️ / ❌ with one-line reason
- CTA strength: ✅ / ⚠️ / ❌ with one-line reason

**Grammar & Clarity — Sentence-level findings:** name long/confusing sentences with their word counts and quote them in italics. Provide a suggested split as a concrete rewrite. 1–3 examples is plenty.

**Grammar & Clarity — Repetition fatigue:** flag motifs from the skeleton's `motifs[]` field (Step 5 output) where `anchor_claims_per_occurrence < 0.5`. Include exact occurrence counts.

**Grammar & Clarity — Mobile readability:** check paragraph density, list formatting, scroll comfort on phone. Flag long quoted blocks or roman-numeral structures that take vertical space.

**Grammar & Clarity — Singapore-streets test:** only include for SG-targeted letters. Flags jargon that fails the "smart non-specialist on the MRT" test. No Singlish — but also no jargon. Drop this sub-section entirely for non-SG audiences (US, EU, etc.).

**Anti-AI Detection** — every flag must include: pattern name, exact checklist source citation (e.g., `overused-ai-patterns.md §3 — Big Contrast`), verbatim quote(s) from the letter, and either a specific fix or an A/B test candidate.

**Notes & Recommendations** — every numbered action ties back to a specific finding via "→ Resolves: §X #Y" pointer. This makes the audit traceable: a reader can see exactly which finding each action addresses.

### Translation rules (jargon → plain English)

- "UMP" → "the named mechanism" or "what makes Stack different"
- "identity ladder L4 missing" → "the letter never names who the buyer becomes after deciding"
- "concentration alternatives dismissed with structural-failure-mode" → "the letter explains why other paths actually fail, not just why they feel bad"
- "motifs not earning anchor_claims" → "phrase X is repeated but the repetition doesn't carry new proof"
- "trust chain gaps" → "places where the reader is asked to believe a claim with nothing concrete attached"
- "branded term proliferation" → "two named mechanisms competing for the same job"
- "self-validation checkpoint" → "a place near the end where the reader can quietly answer 'is this me?' before clicking"

### Hard constraints

- No sub-section longer than 6 bullets (sub-sections inside a dimension; the overall brief can be longer).
- Every claim must reference a specific quote, section, or number from the letter — no abstract assertions.
- The whole brief targets 800–1,200 words with the 4-dimension structure (was 400–600 in the old single-section format).
- If you find yourself reaching for framework vocabulary, rewrite the sentence using the table above.
- **Target Hemingway reading grade ≤5.** Short sentences (most under 14 words). Common words. Active voice. No subordinate clauses unless unavoidable. Singapore-streets test: a smart non-specialist should read it without a dictionary. No Singlish.
- **Run BOTH anti-AI checklists against the SOURCE LETTER** (not against your own brief writing). `skills/copy-editing/references/overused-ai-patterns.md` (marketing register: Big Contrast, Revelation Hook, Elliptical Setup, Great Reframe, Philosophical Reduction). `skills/copy-editing/references/anti-ai-patterns.md` (analytical register: negative parallelisms, vague attributions, false ranges, elegant variation, copulative avoidance, rule of three, em-dash density). One pass, both apply.
- **Surface source-letter AI-pattern flags prominently in a `## Patterns to flag` section** between "What's working" and "What's broken". This is the deliverable's main anti-AI value-add. Group findings as `### Hard flags — rewrite before ship` and `### Soft flags — work for buyers, but A/B-worthy`. Each entry: pattern name, source checklist + section, verbatim quote(s) from the letter, and a specific fix or A/B suggestion.
- **Do NOT include a self-audit of your own brief writing in the deliverable.** The brief's purpose is to expose patterns in the SOURCE LETTER, not to document your own rewrites. (Internal pipeline-quality tracking belongs in a separate log file, not in the operator-facing brief.)
- **Apply the anti-AI checklists to your own writing as a private quality check** before finalising — but the result is invisible to the operator. The brief should read as if it landed clean on the first try.
- **Replacement candidates for high-leverage elements (operator-facing register):** for headline, subheadline, and CTA pre-button line, surface 2–3 specific replacement candidates with full framework attribution intact (e.g. "candidate 1 uses Halbert one-person seed + dossier §3 power words", "candidate 2 channels Schwartz Stage 3 mechanism register", "candidate 3 collapses Big Contrast and seeds coat-of-arms specificity"). Operator must see candidates AND the reasoning behind each so they can validate before the client-facing brief ships. This is the operator-side mirror of the client-facing rule below; the exception is scoped to these 3 elements only — body copy stays WHAT-not-HOW.
- **Severity legend MUST appear** between the header block and the summary scores. Verbatim text per skill specification.

## Step 15: Gate A — produce client-facing brief? Y/N

HITL gate. Default no — not every audit run targets a prospect. Surface to the user:

> "Operator audit brief is complete. Produce client-facing lead-magnet brief? (Y/N)"

If N, skip to Step 17 handoff.

## Step 16: Client-facing brief (lead magnet)

If Gate A passed, produce a client-facing brief at `scratch/audits/<project>/copy/<letter-name>-client-brief.md` (or `clients/<project>/copy/<letter-name>-client-brief.md` if `context_branch = "loaded"`).

**Canonical template reference:** `scratch/audits/stackworks/copy/stackworks-letter-client-brief-v3.md` — validated V3 register (tone + structure). V4 (downstream pilot) will be the new VOC-anchored exemplar once Track C ships it. Match V3's register and tone; layer in the v0.4 VOC-anchored 3-line shape on top.

### Template constraints (hard rules from corrections.md)

**Voice:** Jerel first-person, friend-tone. Open with "Hey [Name]."

**Register: CLIENT-FACING — enforce strictly:**
- Zero named copywriters: no Schwartz, Halbert, Ogilvy, Caples, or any other name
- Zero "strong copywriters do X" / "what good copywriters do" framing — dropped entirely
- Zero framework names: no "coat of arms," "A-pile," "one-person rule," "identity ladder," etc.
- Plain business-owner language throughout. Describe WHY a thing works, never WHO said it works
- Mechanical principle language: "What converts instead is...", "The reason this matters is...", "Letters that earn the click do this differently."

**4-section structure (symmetric with operator brief):**

```
# Notes on the [Project] letter

*From Jerel · [Date] · For [Client Name]*

---

Hey [Name]. [Cold read + editor pass framing — 2 sentences.]

[1-line purpose: "This is a first-pass audit. I'm looking at four things: [list them]."]
[1-line scope: "This is first-pass only. Deeper rewrite work exists if you want it. That is a separate engagement."]

[Brief pre-read note: strategic items vs. AI hygiene — which to read first and why.]

**Severity legend**
[H] High priority — fix before sending traffic. Major conversion, trust, or positioning issue.
[M] Medium priority — important, but not usually a deal-breaker.
[L] Low priority — polish, clarity, or testing note.

---

## Conversion potential

### What is already working
[3–5 findings, each with verbatim quote and mechanical explanation of WHY it works]

### Strategic findings
[H/M/L tagged. Use the 3-line VOC-anchored shape for every [H] and [M] finding — client-facing register (no copywriter names, mechanical principle language):

```
### [H] <finding title — state the cost directly>
What's in the letter: "<verbatim from letter>"
What buyers actually say: "<verbatim from dossier — strip subreddit usernames; describe the source as 'a buyer in your segment said' or 'one prospect put it this way'>"
Cost: <one-line direct cost statement>
```

Append `[no-VOC]` to the heading if Step 9c found no dossier match. On cold path, every finding gets `[no-VOC]` and the "What buyers actually say:" line is omitted.

WHAT-not-HOW for strategic items: diagnose, describe principle mechanically, show the cost.
Do NOT prescribe rewrites for strategic findings.
Brand-vs-product: frame as client-answerable question with trade-offs visible (including de-identified outcome options).
Outcomes gap: state options without prescribing testimonial-collection.]

### Element reads
Headline / Lead-subhead / Benefits / Proof / CTA — one-line read each, with [H/M/L] tags where flagged.

---

## Grammar & clarity
[Sentence-level findings with suggested splits. Repetition fatigue with counts.]
Each finding tagged [H/M/L].

---

## Anti-AI / AI-like tendencies

[OPEN WITH: one sentence listing the specific patterns checked — em-dash density, rule-of-three stacking, etc.]

[Mechanical descriptions. HOW for AI hygiene only — find-and-replace swaps for em-dashes, rule-of-three, Big Contrast, etc. Give exact replacement candidates.]
Each finding tagged [H/M/L].

---

## Notes & recommendations

[Client-answerable questions + action items.]
Each item tagged [H/M/L] with → "Resolves: §X #Y" traceability.

[Close with "If you only fix one thing this week:" recommendation — the single highest-leverage item.]

---

Let me know what you think about it for now.
```

### Hard constraints on client-facing brief

- **Sentence-case headings throughout** (e.g., "Conversion potential" not "Conversion Potential")
- **No em-dashes in own prose** — em-dashes only inside quoted source-letter text
- **Closing verbatim:** "Let me know what you think about it for now."
- **Severity tags:** every finding tagged `[H]`, `[M]`, or `[L]`
- **WHAT-not-HOW** for strategic items: diagnose and show the cost — do not prescribe rewrites
- **HOW for AI hygiene:** mechanical swaps are fine to provide (they are housekeeping, not strategy)
- **Replacement candidates for high-leverage elements:** for headline, subheadline, and CTA pre-button line, the brief MUST provide 2–3 specific replacement candidates grounded in the buyer dossier's verbatim language. Each candidate sits inside the Element reads block under the relevant element, with explicit angle differentiation (e.g. "specific situation angle / peace-of-mind angle / structural alternative angle") and a one-sentence "the reason these candidates work" mechanical explanation. Other elements (benefits, proof, mid-letter sections) keep WHAT-not-HOW. Reason: headline / subheadline / CTA pre-button line are high-leverage enough that 3 candidates serve the client more than diagnosis alone, AND the dossier provides the source language to ground them. The exception ends at these 3 elements — do not extend to the rest of the letter.
- **Coverage discipline:** every major copy element (Headline, Lead, Benefits, Proof, CTA) gets a one-line read in the element reads block — even working elements
- **Methodology transparency:** Anti-AI section must open with one sentence listing the specific signals checked
- **Honesty over diplomacy:** friend-tone is honest-tone, not diplomatic-tone. State the cost of each problem directly. No hedging, no mid-paragraph diplomatic ramps
- **Length:** scales with source letter (1.5–2× source letter word count)
- **No "→ Resolves" pointers for the operator:** the client version uses the same traceability pattern in Notes & Recommendations
- **Severity legend required** in client brief between opening framing and first section divider. Verbatim text per skill specification.

## Output paths summary

```
clients/<project>/
├── copy/
│   ├── <letter-name>.md                       (source — not modified)
│   ├── <letter-name>-skeleton.json            (Phase 1 + 2 output)
│   ├── <letter-name>-skeleton-summary.md      (technical companion)
│   └── <letter-name>-plain-english-brief.md   (operator-facing brief)
└── reverse/                                   (only if Phase 2 ran)
    ├── purple-ocean-inferred.md
    ├── mass-desires-inferred.md
    └── customer-avatar-inferred.md
```

## Validation

Test fixtures with expected outputs live in `tests/` next to this SKILL.md. Each fixture references a real letter and lists field-level expectations. SKILL.md describes the generic contract; fixtures verify it against specific inputs.

Current fixtures:
- `tests/v4-firsttime.md` — Neeza & Nizam first-time-buyer letter

## Step 17: Handoff to the forward pipeline (sales-letter-method)

This skill is audit and diagnosis only. It does not write or rewrite copy.

After the skeleton is produced, the operator reads the routing table in `skeleton-contract.md` and re-enters the forward pipeline at the stage that matches the highest-priority signal. The forward pipeline lives at `skills/sales-letter-method/` — it owns all the regeneration work: Schwartz channeling, Halbert one-person seed and coat-of-arms, Hormozi offer stack, Collier "enter the conversation", legend architecture, five headline mechanisms, six emotional states, six proof types, and six objection categories.

Routing table signals map to forward pipeline phases as follows (examples — see `skeleton-contract.md` for the full table):

- Priority 1 (UMP regen) → `sales-letter-method` Phase 0.5 (mechanism naming) + Phase 1 (UMP derivation)
- Priority 3 (proof inventory rebuild) → `sales-letter-method` Phase 2 (voice mining)
- Priority 4 (CTA rewrite) → `sales-letter-method` CTA architecture phase

The slash command `/copy:sales-letter` wraps the forward pipeline entry point if invoked from a clean session. For mid-session work, load `skills/sales-letter-method/SKILL.md` directly and start at the identified phase.

Do not attempt to run the forward pipeline inside `sales-letter-audit`. The audit ends when outputs are written. Forward work begins in a separate session.

## Anti-patterns

- Do NOT regenerate copy. This skill only extracts.
- Do NOT skip the trust_chain_gaps step. Structural reviewers are blind to it; this skill must catch it.
- Do NOT overwrite stage_outputs/ with inferred research. Sandbox to `reverse/` only.
- Do NOT compute confidence on Phase 1 fields. They're observed structurally, not inferred.
- Do NOT halt on Phase 1 alone. Halts only fire after Phase 2's `speculation_ratio` is computed (or on the `verticals_detected` segment-leakage canary).
- Do NOT trust the letter's declared audience. Always derive `audience_inferred` and `verticals_detected` independently — the segment-leakage canary depends on cross-checking the letter against its stated segment.

## Sub-agent guidance

The trigger for using a sub-agent is **not letter length alone** — it's parent-context heaviness and the parallelism opportunity.

### Decision rules

1. **In-session (default).** Letter <2000 words AND parent context is light (<100K tokens accumulated). Run the skill in the current session. This is the typical case. No sub-agent overhead.

2. **Single Sonnet sub-agent (1 level, isolation).** Parent context is heavy (>100K tokens accumulated) and you want to protect it. Spawn ONE Sonnet sub-agent to run the whole skill end-to-end and return only the skeleton + summary paths. Use when the parent is mid-conversation with heavy prior work.

3. **Parallel Sonnet sub-agents (1 level, fan-out).** Letter >2000 words. Phase 1 steps 4–9 can fan out into 4–6 parallel sub-extractions (one per field group: identity_ladder, motifs, headline_body_coherence, concentration_alternatives, cta_architecture, proof_inventory). Each sub-agent receives the full letter and returns its slot of the skeleton. Phase 2 inference must remain serial because each inference refines the next.

### Anti-pattern: nested sub-agents

Do NOT spawn a Sonnet sub-agent that itself spawns another Sonnet sub-agent for this skill. Nesting is serial — it adds 30–60s of context-rehydration latency per layer with no parallelism gain. Debuggability collapses (errors must bubble through layers). The pattern is rarely justifiable; if you think you need it, you almost certainly want parallel fan-out at one level instead.

### Why "letter length" is the wrong primary trigger

Length determines whether parallelism *helps*. Context heaviness determines whether *isolation* helps. They're orthogonal. A 1000-word letter audited mid-conversation in a 150K-token session is a sub-agent candidate. A 3000-word letter audited fresh in a clean session is a parallel-fan-out candidate. A 1000-word letter audited fresh stays in-session.

## Related

- Contract: `skeleton-contract.md` (in this skill folder)
- Sibling skill (different concern, different repo): `Marketing/skills/sales-letter-method/` — the forward pipeline this skill is the inverse of
- Audit (different concern): `Marketing/skills/sales-letter-method/reviewers/pre-ship-checklist-reviewer.md` (5-lens audit; doesn't extract structure)

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[sales-letter-auditor]] (agent, 0.15)

<!-- skill-graph:end -->
