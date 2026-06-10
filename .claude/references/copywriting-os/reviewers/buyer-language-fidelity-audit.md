# Buyer Language Fidelity Audit — Post-Write Reviewer (sub-agent)

**Source:** Phase B anti-hallucination layer. Integrates Schwartz "enter the conversation" + Collier *The Robert Collier Letter Book* + cai #42 buyer-language channelling.

**Core principle:** "A fabricated buyer quote is a hallucination. A paraphrase that makes the buyer sound more articulate than the raw research is WORSE." Every buyer-language instance in the draft must trace to a research file. Every paraphrase must preserve register, emotional tone, and vocabulary level. Copy that lifts buyer language up-register destroys the Collier principle at its root: you are no longer entering their conversation — you are replacing it with your own.

**Agent model:** Sub-agent. Receives the draft + all research inputs listed below. Runs as one of four Phase B anti-hallucination reviewers in parallel. FAIL blocks ship regardless of Phase C verdict.

## Research Inputs

Load whichever files exist. Log any missing — reduce verdict confidence accordingly.

1. `clients/<slug>/research/buyer-language-dossier.md` — verbatim buyer quotes from Reddit, forums, interviews, surveys
2. `clients/<slug>/research/life-transition-dossier-*.md` — context quotes (glob; multiple files possible)
3. `clients/<slug>/avatars/*.md` — Raw Inner Dialogue blocks, first-person voice samples (glob)
4. `clients/<slug>/source-of-truth.md` §5.7 — ICP Language Analysis section
5. `clients/<slug>/testimonials/` — all testimonial files (glob)

## What Counts as Buyer Language in the Draft

Parse for the following. Each instance is a **buyer-language unit (BLU)**.

- **VERBATIM_QUOTE** — quotation marks attributed to a real buyer ("Riduan said: 'I was scared…'")
- **PARAPHRASED_THOUGHT** — first-person reader-state language ("you're lying awake wondering if…", italicised interior monologue, "the voice in your head says…")
- **TESTIMONIAL** — attributed snippet from a named person, quoted or paraphrased
- **CASE_STUDY_QUOTE** — named case study with specific claims, numbers, or direct speech

## Procedure

### Step 1 — Parse draft for all BLUs

Scan for: quotation marks (single and double), italics used as interior voice, openers like "You tell yourself…" or "The question you keep asking is…", attribution patterns ("As [Name] told us…", "[Name] said…"), "What our clients say" framings.

List every BLU with: draft line reference, raw text, and classified type.

### Step 2 — Source-match each BLU

**VERBATIM_QUOTE and TESTIMONIAL:** Search all research inputs for exact string match. Accept ≥90% fuzzy match (minor punctuation or whitespace variance only). No match = hallucination flag.

**PARAPHRASED_THOUGHT:** Search Raw Inner Dialogue blocks and buyer-language-dossier for the concept and closest vocabulary. Extract the nearest source quote. "It sounds plausible" is not a source — the quote must exist in a file.

**CASE_STUDY_QUOTE:** Verify named buyer exists in `testimonials/` or research notes. Verify every number (price, timeframe, result) matches the source file exactly. Any discrepancy = CRITICAL.

### Step 3 — Score drift for PARAPHRASED_THOUGHTs

Compare the draft paraphrase against its nearest source quote on two axes: **meaning** (does the substance change?) and **register** (does vocabulary level, formality, or cultural marker shift?).

Assign one drift score per BLU:

- **PASS** — meaning preserved, register preserved (including Singlish, blue-collar idiom, local marker)
- **DRIFT_LOW** — trivial polish; meaning and register intact; no semantic or tonal loss
- **DRIFT_HIGH** — register upshifted; buyer made more articulate or marketer-like than raw research; or Singlish / local marker dropped
- **DRIFT_FATAL** — meaning changed, OR no source found, OR register so upshifted the line could not have originated from the raw buyer

Register-drift reference patterns:

| Raw research | Draft version | Verdict |
|---|---|---|
| "I'm stuck lah, no clue what to do" | "I found myself in a state of uncertainty" | DRIFT_FATAL — register destroyed |
| "Scared I buy then market drop" | "I harboured concerns about market volatility" | DRIFT_FATAL — formalised |
| "Bo bian already" | "I had no other option" | DRIFT_HIGH — Singlish lost |
| "Macam feel like being cheated" | "It felt almost deceptive" | DRIFT_HIGH — local register dropped |
| "Just want steady income la" | "Seeking stable, predictable cash flow" | DRIFT_HIGH — professionalised |

### Step 4 — Assign severity to each violation

- **CRITICAL** — VERBATIM_QUOTE or TESTIMONIAL with no source match (fabricated quote)
- **CRITICAL** — CASE_STUDY_QUOTE with mismatched numbers or non-existent named buyer
- **HIGH** — DRIFT_FATAL on any PARAPHRASED_THOUGHT
- **MEDIUM** — DRIFT_HIGH register upshift on PARAPHRASED_THOUGHT
- **LOW** — DRIFT_LOW minor polish; note only

### Step 5 — Register audit (whole-draft pass)

Step back from individual BLUs. Ask: what register does the raw research show collectively — Singlish, UK English, blue-collar, professional, anxious first-timer, seasoned investor? Does the draft's buyer-language sections as a whole match that register, or does it trend formal, polished, or neutral? Flag any systematic drift even where individual lines passed Step 3. Systematic drift = escalate to HIGH.

## Output schema

```
## BUYER LANGUAGE FIDELITY AUDIT

Research inputs loaded:
- buyer-language-dossier.md: [FOUND / NOT FOUND]
- life-transition-dossier: [FOUND N files / NOT FOUND]
- avatars/*.md: [FOUND N files / NOT FOUND]
- source-of-truth.md §5.7: [FOUND / NOT FOUND]
- testimonials/: [FOUND N files / NOT FOUND]

Total BLUs detected: N
  VERBATIM_QUOTE: N
  PARAPHRASED_THOUGHT: N
  TESTIMONIAL: N
  CASE_STUDY_QUOTE: N

Fidelity scores:
  Verbatim-matched (VERBATIM / TESTIMONIAL / CASE_STUDY): N of N
  Paraphrase PASS: N
  DRIFT_LOW: N
  DRIFT_HIGH: N
  DRIFT_FATAL / no source: N

Violations (ordered CRITICAL → LOW):
1. [CRITICAL] Line X — VERBATIM_QUOTE — "…draft text…"
   Source match: NONE FOUND. Searched: buyer-language-dossier.md, testimonials/
   Action: Remove or replace with sourced verbatim quote.

2. [HIGH] Line X — PARAPHRASED_THOUGHT — DRIFT_FATAL
   Draft: "I harboured concerns about market volatility"
   Nearest source: buyer-language-dossier.md L47 — "Scared I buy then market drop"
   Register delta: formal vocabulary / Singlish stripped
   Rewrite: "Scared I buy then market drop" (or paraphrase preserving 'scared' + syntax)

3. [MEDIUM] Line X — PARAPHRASED_THOUGHT — DRIFT_HIGH
   Draft: "…"
   Nearest source: "…" — [file, line]
   Register delta: <describe specific loss>
   Suggested downshift: "…"

Register audit:
  Raw research register: [Singlish / UK English / blue-collar / professional / mixed]
  Draft buyer-language register: [matches / trends formal / trends neutral / mixed drift]
  Systematic drift: [YES — describe pattern / NO]

Verdict: PASS / FAIL
Reason: <one line>
```

## Failure thresholds

- Any CRITICAL (fabricated quote or mismatched case-study figure) → auto-FAIL, block ship
- Any HIGH (DRIFT_FATAL paraphrase) → FAIL
- More than 2 MEDIUM (DRIFT_HIGH) → FAIL
- Systematic register drift confirmed in Step 5 → escalate to HIGH, FAIL

PASS requires: zero CRITICAL, zero HIGH, ≤2 MEDIUM, no systematic register drift.

## The four cheap wins to look for first

1. **Grep quotation marks first** — every pair gets source-matched before anything else. A fabricated quote inside quotation marks is the most egregious failure mode and the fastest to catch.
2. **Formal vocabulary scan** — search buyer-language sections for: *harboured, endeavoured, pertaining to, sought to, faced with the prospect of, in a state of*. Any of these in a paraphrased buyer voice is almost always DRIFT_FATAL. Flag immediately.
3. **Singlish presence check** — if raw research contains *lah / lor / bo bian / macam / shiok / confirm plus chop* and the draft buyer-language sections contain none, systematic upshift drift is near-certain. Run Step 5 first for these clients before spending time on individual BLUs.
4. **Testimonial name verification** — every named buyer in the draft must exist in `testimonials/` or research notes. One grep, five seconds. Catches hallucinated names before the draft ships.

## Logging

Append to `clients/<slug>/copy-system/quality-gates/buyer-language-fidelity-log.md`:
`| YYMMDD-HHMM | output file | BLUs N | verbatim-matched N | drift-fatal N | drift-high N | critical N | verdict |`
