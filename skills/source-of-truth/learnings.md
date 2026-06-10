# Learnings — source-of-truth

Confirmed patterns, validated approaches, and promoted corrections from this skill.

## Confirmed Patterns

### Separation of Concerns — source-of-truth vs ad-concept-engine (260417)

**Rule:** source-of-truth owns STRATEGY. ad-concept-engine owns EXECUTION. No overlap.

| Layer | source-of-truth produces | ad-concept-engine produces |
|---|---|---|
| Strategy | Angles (§10), hooks library (§11), messaging hierarchy (§9), avatars (narrative), HITL decisions, research findings | — |
| Execution | — | DCT batch IDs (DCT001...), FORMAT, AD name, COPY 1/2, HEADLINE 1/2, image prompts, DCT tracker |

**File conventions:**
- `clients/<project>/source-of-truth.md` + `source-of-truth-draft.json` — strategy only, slow-moving foundation
- `clients/<project>/angles/` folder — wave-iterating strategy built upon SoT (260418 architecture decision; replaces older root `angles-hooks-library.md`)
- `clients/<project>/campaigns/dct-YYMMDD/dct-tracker.json` — ad-concept-engine output
- `clients/<project>/avatars/` — avatar-research output (narrative, reused as strategy layer)

### Foundation vs Wave-Iterating Split (260418)

**Rule:** SoT changes only on major buyer shifts or scheduled refresh. Anything that iterates per wave (angles, hooks, testing matrices, kill rules per wave) lives in `clients/<project>/angles/`.

**Why:** mixing wave-iterating strategy into SoT forced full-doc rewrites for tactical iteration. Three problems compounded: (1) the strategic foundation became unstable, (2) git history showed waves of "small angle tweak" commits in a doc meant to be quarterly-stable, (3) downstream consumers (ad-concept-engine) had to re-parse a 1300-line doc for a 100-line update.

**How to apply:** in any new client SoT generation, after Phase 5 writes the canonical doc, immediately bootstrap `angles/` folder + strip §10/§11/§16 wave-specific tables to pointer blocks. SoT keeps section anchors but content lives in angles folder. Cadence note in SoT header: "monthly light touch · quarterly full · stability contract: angles/ owns wave iteration."

**Build-upon contract:** every angles file cites the SoT sections it draws from at the top. If those SoT sections change, re-validate the angle file.

**Sheet integration:**
- `source_of_truth_sheet_writer.py` writes AVATARS tab ONLY
- `ad_concept_sheet_writer.py` (ad-concept-engine owned) writes CREATIVES + COPY tabs
- sheets-updater (existing) writes metric columns only — never strategy columns

**Violation to never repeat:** mixing DCT creative specs into source-of-truth-draft.json creates duplicate state across two skills and confuses sheet-writer ownership. If the question is "does this data include a BATCH ID, a Meta ad format, or a specific ad copy string?" → it's ad-concept-engine's data, NOT source-of-truth's.

## What Works

<!-- Patterns that produced strong outputs in real client runs -->

### Phase A multi-product upgrade (260418)

**Rule:** every Phase 1 triage call MUST start with Q0 (product_type enum: ecom / SaaS / service / info / agency / property). All downstream synthesis branches off this answer per the table in `references/section-synthesis-frameworks.md`.

**Why:** the framework was written generically but the in-line examples in `checkpoint-questions.md` were neezanizam (property) only. Running this skill against a SaaS or ecom client without explicit product_type routing produced property-shaped angles + property-shaped CTAs + property-shaped proof — wrong currency for the buyer. Now: product_type drives KPI defaults, proof prioritisation, CTA grammar, format weighting, urgency triggers, and angle pool.

**How to apply:** load `references/examples-by-product-type.md` and pull the section matching `product_type` for Phase 4 HITL drafting. Never paste a generic angle pattern without specificity.

### New sections added (260418)

- **§5.5 Golden Nuggets** — curated swipe-file ready quotes (different from Language Bank: nuggets are publishable as ad copy as-is or with minimal rewriting). 6 buckets: frustration / skepticism / humor-sarcasm / hopelessness / DIY-struggle / "holy grail". Target 15-30 nuggets.
- **§5.7 ICP Language Analysis** — consolidated tone/style/vocabulary/punctuation guide. Single source for any copywriter touching the brand. Eliminates spread across §4 + §5.
- **§7.5 Misconceptions** — wrong beliefs the audience holds (different from objections — misconceptions = factual errors in mental model, objections = reasoned hesitations). Higher leverage than objections because reframing opens new mental categories.

### Raw doc upload as Phase 0.5 (260418)

**Rule:** before spawning fresh research in Phase 2, ask if the user has existing raw artifacts (PDF, transcripts, surveys, sales-call notes). Save to `clients/<project>/research/raw/uploaded-YYMMDD-<source>.<ext>` and pass extracted fields into `buyer-language-researcher` as a primary input.

**Why:** existing voice-of-customer data is higher signal than fresh scrapes. Internal docs are biased toward what the brand thinks the buyer says, so always still triangulate against external mining — but starting with the user's own data prevents redundant work.

**How to apply:** `references/research-pipeline.md` Phase 0.5 documents the trigger + processing + cite rule.

### scrapecreators is canonical, not GigaBrain or Reddit Answers (260418)

**Rule:** `scrapecreators` skill is the single source for raw social/forum/comment mining (covers Reddit, TikTok, IG, YouTube, X, Threads, Pinterest, LinkedIn, FB + 19 other platforms via one API). Do NOT add GigaBrain, Reddit Answers, or other duplicate scrapers.

**Why:** user explicitly flagged the duplication. scrapecreators already covers everything those alternatives offer. Adding more scrapers = more API keys, more failure modes, more context overhead, no marginal coverage.

**How to apply:** `buyer-language-researcher` agent uses scrapecreators (+ DataForSEO + NotebookLM + WebFetch) under the hood. If a future scraper claim arrives ("but X covers Y better!"), test against existing scrapecreators output first before adding.

## What Doesn't Work

<!-- Approaches that consistently produced weak / rewritten output -->

## Promoted Corrections (3+ repeats)

<!-- When the same correction shows up 3+ times in corrections.md, move it here as a rule -->

## Per-Client Notes

<!-- Patterns specific to a client/category that should NOT be generalised -->
