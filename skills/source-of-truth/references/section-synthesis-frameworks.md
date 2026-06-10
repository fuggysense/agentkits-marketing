# Section Synthesis Frameworks

How to convert raw research data + intake answers into the 26-section template content. Used during Phase 3.

**Read this entire file before starting Phase 3.** Each section has different source material, synthesis rules, and quality bars.

**Universal rules across all sections:**
- UK English throughout
- Verbatim buyer quotes only — never paraphrase, always attribute
- If data missing for any field, write `⚠️ NOT AVAILABLE — [reason]` (Marketing CLAUDE.md data reliability rule)
- For SG-based projects, load `skills/ad-concept-engine/references/sg-cultural-guidelines.md`

---

## Product-Type Branching (apply to every section)

`product_type` is captured in Phase 1 triage. Use it to route synthesis decisions per section. Enum values + the synthesis adjustments each unlocks:

| product_type | KPI defaults (§2) | Proof types to prioritise (§8) | CTA defaults (§15) | Format weighting (§12) | Urgency triggers (§3) |
|---|---|---|---|---|---|
| **ecom** | ROAS · MER · AOV | UGC unboxings · before/after · review screenshots · shipping/returns proof | "Add to cart" · "Shop now" · "Get yours" | Static + Carousel + UGC video | Stock countdown · sale deadline · seasonal |
| **SaaS** | CAC payback · activation rate · trial-to-paid · MQL→SQL | Free-trial signups · G2/Capterra reviews · feature demos · founder credibility | "Start free trial" · "Book demo" · "See it in action" | Demo video + Carousel + Founder video | Pricing change · feature deprecation · cohort caps |
| **service** (local/professional) | CPL · cost-per-booked-appointment · show-up rate | Testimonials with face+name · case studies · before/after · credentials | "Book consultation" · "Get a quote" · "Apply now" | Founder video + UGC testimonial + Static | Calendar scarcity · seasonal availability |
| **info** (course/coaching/community) | CPA-to-purchase · webinar registration · email signup | Student transformation stories · earnings/results screenshots · founder authority · cohort size | "Get instant access" · "Join the cohort" · "Reserve your spot" | VSL + Founder video + Long-form carousel | Cohort enrolment deadline · price increase · bonus expiration |
| **agency** (marketing/B2B services) | CPL · cost-per-booked-strategy-call · pipeline added | Client logos · revenue-impact case studies · process methodology proof · founder credentials | "Book a strategy call" · "See if we're a fit" · "Apply now" | Founder video + Case-study carousel + Long-form static | Limited client slots · quarterly intake · roster cap |
| **property** (real-estate consulting/agent services) | CPA-per-WhatsApp-verified-appointment · CPL · show-up rate | Past transactions volume · named-couple case studies · methodology branding · agent credentials | "Take the assessment" · "Book consultation" · "Talk to an architect" | Founder video + UGC + Static + Long-form carousel | Mortgage rate window · MOP timing · listing scarcity |

**Routing rule:** in every section's synthesis logic below, if a per-product-type adjustment is needed, the section MUST cite this table. If `product_type` is missing from intake, surface as ⚠️ MISSING INTAKE — re-ask before proceeding to Phase 3.

**Anti-pattern:** do NOT default to `property` examples or `service` defaults when `product_type=ecom` or `SaaS`. Each product type has fundamentally different proof currencies and CTA grammars.

---

## §1 Brand Snapshot

**Sources:** Phase 1 intake + WebFetch product page + `clients/<project>/context-profile.json` (if Mode A)

**Synthesis logic:**
- `brand_name`, `website_url`: from input or scraped `<meta og:site_name>` / domain
- `category`, `product_type`: from product-snapshot.md categorisation
- `core_offer`: extract the FIRST conversion-oriented offer mentioned on the homepage / pricing page (not generic brand pitch)
- `price_point`: from pricing page scrape, or intake answer
- `conversion_event`: derived from primary CTA on landing page (Buy = purchase, Book = call, Apply = application, etc.)
- `brand_constraints`: from intake answers (compliance, words to avoid)

**Quality bar:** if you can't determine the core offer in one sentence, intake failed — surface and ask.

---

## §2 Paid Media Objective (HITL-DECIDED)

**Sources:** Phase 1 intake + Phase 4 HITL answer

**Synthesis logic:**
- DRAFT in Phase 3: present 2-3 KPI candidates based on funnel stage and product type:
  - E-commerce + warm scale → ROAS / MER
  - Lead gen + new launch → CPA / CPL
  - SaaS + activation → CAC payback
- FINALISE in Phase 4 from HITL pick.
- `cold_priority`, `warm_priority`, `hot_priority`, `retargeting_logic`: write as 1-sentence directives, drawn from §9 messaging hierarchy.

---

## §3 Product and Offer Details

**Sources:** WebFetch + intake + (Mode A) `clients/<project>/offer.md`

**Synthesis logic:**
- Use `offer-builder` skill's deliverable schema as the structural model — but skip the 5-phase construction process (we're documenting an existing offer, not building one).
- `functional_breakdown`: pull from product page features section + FAQ
- `offer_details`: scrape pricing/checkout pages for promo, guarantee, fulfillment terms
- `why_offer_converts`: triangulate from buyer-language-dossier (what they say convinced them) + competitor positioning gaps

**Anti-pattern:** do NOT generate "why it converts" from nothing. If buyer-language-dossier has zero conversion signals, mark this subsection as ⚠️ NOT AVAILABLE.

---

## §4 Audience Profile

**Sources:** `marketing-psychology` skill (Schwartz model, sophistication ladder) + buyer-language-dossier + market-research.md

**Synthesis logic:**
- `awareness`, `awareness_reason`: map dominant buyer language to Schwartz levels:
  - "I just want my [problem] gone" → Problem-Aware
  - "I've tried [generic solution category]" → Solution-Aware
  - "Should I use [Product A] or [Product B]?" → Product-Aware
  - "Is [your product] worth it?" → Most Aware
- `sophistication`: map market research findings to Schwartz 5 stages (1=virgin claim, 5=identification). If market has 10+ established competitors all making similar claims → Stage 4-5.
- `Schwartz Sophistication Stage Map`: copy the 5-row template from `marketing-psychology/references/schwartz-stages.md` and fill the FOR-THIS-MARKET column for each row
- `Segment Breakdown`: if research surfaced 1-5 distinct buyer subgroups, populate. If only 1 dominant segment, only fill row 1 and explicitly note "single dominant segment — no DCT segmentation by audience needed; segment by angle instead."

---

## §5 Buyer Profile Extraction (CRITICAL — DO NOT DUPLICATE avatar-research)

**Sources:** buyer-language-dossier.md (primary) + product reviews + Reddit threads + competitor ad copy

**Use:** `skills/avatar-research/SKILL.md` Phase 1.5 Sales Copy Extraction framework. Apply that framework to research data instead of generating from scratch.

**14-dimension synthesis:**

| Dim | Source | Rule |
|---|---|---|
| 1 Demographic | research-extracted (Reddit user profiles, review demographics) + intake | If sparse, mark "directional only" |
| 2 Core Problem | TOP 3 most-repeated problem framings in dossier | Quote verbatim with attribution |
| 3 Top Emotions | tag emotional words in dossier; rank by frequency | Use buyer's exact emotion words, not mapped synonyms |
| 4 Fears | extract `"I'm afraid..."`, `"What if..."`, `"I worry..."` patterns | Verbatim |
| 5 Relationship Impacts | extract mentions of family, partner, work, identity in problem context | Verbatim if available; otherwise mark NOT AVAILABLE |
| 6 Past Solutions Tried | extract `"I tried..."`, `"I used to..."`, `"I bought..."` patterns | Include WHY they failed (next sentence usually) |
| 7 Don't Want To Do | extract negation patterns: `"I don't want to..."`, `"I refuse to..."`, `"I'm not going to..."` | Strong filter — these are anti-features for the offer |
| 8 Perfect Solution Outcome | extract `"I just want..."`, `"All I need is..."`, `"If only..."` | These ARE the desired-state ad hooks |
| 9 Transformation Effects | extract aspirational identity statements about life-after | Use to fuel desire-led angles |
| 10 Market Specifics | from market-research.md + competitor-ads | What's overused / what proof matters / what framing resonates |
| 11 Success Hinges On | extract trust-signal mentions: `"I'd buy if..."`, `"Show me..."` | These are objection-removers |
| 12 Must Give Up | hardest dimension — extract resistance to required change | Often the unspoken truth a brand should acknowledge |
| 13 Who They Blame | extract blame language: `"the problem is..."`, `"[entity] makes it impossible..."` | Address carefully — never make them feel blamed themselves |
| 14 Top General Objections | rank from competitor-ad rebuttals + Reddit complaint threads | Cover all 7 categories: Price / Trust / Fit / Timing / Effort / Proof / Alternative |

**Quote density target:** every dimension should have 2-5 verbatim quotes if data permits. If <1 quote per dimension on average, dossier was thin → flag and recommend re-running buyer-language-researcher with broader sources.

**Buyer Language Bank:** organise all collected verbatim quotes by category. This becomes the single most-cited section by `ad-concept-engine`.

---

## §5.5 Golden Nuggets (curated swipe-file)

**Sources:** buyer-language-dossier verbatim quotes + product/competitor reviews (via scrapecreators) + comment-section dives (via scrapecreators)

**Synthesis logic:**
- Filter ALL collected verbatim quotes through this gate: *would this work as ad copy as-is, or with minimal rewriting?* If yes → golden nugget. If only useful for understanding the buyer → stays in §5 Language Bank.
- Categorise each nugget into one of 6 buckets: Frustration · Skepticism · Humor/sarcasm · Hopelessness · DIY struggle · "Holy grail" descriptions
- Target: 15-30 nuggets minimum. Bias toward Frustration + Skepticism + DIY struggle (highest ad-copy ROI).
- For each nugget: capture verbatim form + source URL/thread/timestamp + suggested ad-copy use (which angle/format).
- **Rewriting rule:** if a verbatim quote is too clunky/long for ad copy, rewrite using the §5.7 ICP voice. Mark as `[rewritten from: <source>]`. Never invent quotes — that violates the data-reliability rule.
- **Anti-pattern:** do NOT include nuggets unrelated to brand's ICP, product, or service. A funny generic quote about taxes is not a nugget for a SaaS marketing tool.

**Quality bar:** if you have <10 nuggets, the dossier was thin or the filter was too tight. Re-mine.

---

## §5.7 ICP Language Analysis

**Sources:** §5 Buyer Language Bank + §5.5 Golden Nuggets + competitor-ad analysis (via paid-media-audit)

**Synthesis logic:**
- **Tone:** read 50+ collected quotes. Score on dimensions: formal↔informal, polite↔raw, peer-to-peer↔aspirational, professional↔casual. Lock the dominant register in 1 sentence.
- **Emotional style:** identify the dominant emotional baseline (skeptical / stressed / proud / fed-up / hopeful / resigned / cynical / earnest). Single dominant + secondary.
- **Vocabulary they USE:** extract specific terms, jargon, slang, brand names that recur. Aim for 15-30 specific phrases.
- **Vocabulary they REJECT:** extract corporate-register words that NEVER appear in their language. These are the "do not use in ad copy" words. Aim for 10-20.
- **Sentence-length default:** sample 20 random quotes. Average word count. Flag if dominant pattern is short staccato (<8 words avg) vs unspooling (>20 words avg) vs mixed.
- **Punctuation tells:** lowercase-only? excessive periods? em-dashes? all-caps emphasis? abbreviations (lol, fr, ngl, etc)?
- **Copywriting tips:** translate the above into 5-8 actionable rules a copywriter can apply ("write in lowercase except brand names", "default to <12 word sentences", "use 'btw' instead of 'by the way'", etc.)

**Output format:** consolidated narrative + bulleted rules. This becomes the file `copywriting`, `script-skill`, and `ad-concept-engine` all reference for tone matching.

**Quality bar:** if a copywriter from outside the brand can't replicate the voice from this section alone, you haven't gone deep enough. Add 5+ more example phrases.

---

## §6 Pain Points and Emotional Drivers

**Sources:** buyer-language-dossier + reviews

**Synthesis logic:**
- Functional pain points: rank by frequency of mention in dossier. List top 5.
- Emotional pain points: extract emotional reactions to the functional problems. Use the 6-category template (frustrated/embarrassed/anxious/overwhelmed/guilty/skeptical) but only fill what shows up in research.
- Desired emotional states: invert the pain points — what's the opposite they want?
- Emotional driver prioritisation table: rank the 8 standard drivers (relief, confidence, convenience, status, fear-of-stuck, time, money, simplicity) by how often they appear in buyer language. Top 3 = primary drivers for ad copy.

---

## §7 Objections

**Sources:** buyer-language-dossier (Reddit objections, comment threads) + competitor-ads (objections their ads attempt to handle reveal which objections are universal in this market)

**Synthesis logic:**
- Cover all 7 standard categories: Price / Trust / Fit / Timing / Effort / Proof / Alternative comparison
- For each, extract verbatim objection in buyer's words
- Objection handling table: for each objection, identify root cause + best proof from §8 + which funnel stage to address it (hook / body / landing page / retargeting)
- If a category has zero buyer-language data, write the standard category template line + mark `⚠️ NEEDS BUYER VALIDATION` — don't fabricate.

---

## §7.5 Misconceptions

**Sources:** buyer-language-dossier + Reddit/forum threads where buyers state wrong beliefs + competitor ads that try to reframe wrong beliefs

**Synthesis logic:**
- Difference vs §7 objections: objection = "I won't buy because X" (reasoned hesitation). Misconception = "I think X is true and it's not" (factual error in their mental model).
- Extract patterns: `"I thought..."`, `"I always assumed..."`, `"isn't it true that..."`, `"why does everyone say..."`, `"I heard that..."`
- For each misconception: state the wrong belief in their words + write the clarification simply (no jargon, no defensive tone).
- Tag ad use: where in the funnel does correcting this misconception have highest leverage? (cold = surprise reframe / warm = educational carousel / hot = direct rebuttal in body copy)
- Aim for 5-10 misconceptions. Misconceptions are HIGHER leverage than objections — reframing a wrong belief opens a new mental category, while answering an objection only closes a known door.

**Anti-pattern:** do NOT confuse a misconception with an objection. "It's too expensive" = objection. "I thought all SaaS tools require credit card upfront for a trial" = misconception.

**Quality bar:** every misconception must be sourced to a real buyer quote (or pattern across multiple quotes). No invented wrong beliefs.

---

## §8 Proof Assets

**Sources:** product-snapshot.md (testimonial sections, case studies linked) + (if exists) `clients/<project>/proof-elements.md` + paid-media-audit data (top-performing creatives often reveal which proof types convert)

**Synthesis logic:**
- Proof Inventory: list every proof asset found, categorised (review / before-after / UGC / case study / founder cred / press / clinical / demo / comparison / data / volume / rating / repeat-purchase / guarantee / community / influencer)
- Proof Inventory Table: rate each by Strength (High/Medium/Low) and Best Ad Use
- Proof Gaps: explicitly list what's missing. This drives §19 asset request checklist.

---

## §9 Messaging Hierarchy (NET-NEW — HITL-DECIDED)

**Sources:** §1-8 synthesis (this is the FIRST section that synthesises from prior sections, not from raw research)

**Synthesis logic:**
- DRAFT 3 messaging hierarchy candidates in Phase 3, each with a different lead message:
  - **Candidate A — Problem-led:** core message names the pain in buyer's words
  - **Candidate B — Outcome-led:** core message names the desired transformation
  - **Candidate C — Mechanism-led:** core message names the unique HOW (best for sophistication 4-5 markets)
- For each candidate, draft supporting messages 1-5
- HITL Phase 4 picks one → finalise.
- Message Prioritisation by Funnel Stage: derive from chosen candidate. Cold = problem/outcome, warm = mechanism + proof, hot = offer + urgency.
- Message Ladder: 6-step ladder using the chosen candidate's messages.

---

## §10 Ad Angles (NET-NEW — HITL-DECIDED)

**Sources:** §5 buyer profile (emotional + practical entry points) + competitor swipe file (what angles competitors are running — and what they're NOT running)

**Synthesis logic:**
- Generate 6-8 distinct angles spanning the 6 categories:
  - Problem-Aware (2 angles — different problem framings)
  - Desire-Led (1-2)
  - Product-Led (1)
  - Offer-Led (1)
  - Proof-Led (1)
  - Contrarian / Pattern Interrupt (1-2 — high-leverage in saturated markets)
- Angle Development Table: each angle gets core idea (1 sentence), best buyer segment (link to §4 segment), best format (§12), risk note
- HITL Phase 4 picks top 3 → mark in template.

**Anti-pattern:** do NOT generate angles that are simply rephrasings of the same hook. Each angle must take a fundamentally different psychological entry point.

---

## §11 Hook Library (NET-NEW)

**Sources:** §5 buyer language bank + §10 angles + `marketing-psychology` mental models

**Synthesis logic:**
- For each of the top 3 priority angles (from §10 Phase 4 pick), generate 4-5 hooks across the 5 hook types:
  - Direct Problem
  - Desire
  - Proof
  - Contrarian
  - Offer
- Hook Writing Grid: tag each hook with its angle, awareness level, funnel stage, format. This is the file `ad-concept-engine` reads when generating DCT batches.
- Use buyer language bank verbatim phrases where possible. A hook quoting a real Reddit thread > a hook written in copywriter voice.
- Anti-AI slop check via `skills/copy-editing/references/overused-ai-patterns.md`

**Quality bar:** if a hook could apply to ANY product in the category, rewrite it. Specificity is the hook's job.

---

## §12-15 Formats / Scripts / Visuals / CTAs (STATIC REFERENCE)

**Sources:** static reference content from `paid-advertising` + `ad-concept-engine` skills

**Synthesis logic:**
- Sections 12, 13, 15 are largely static — copy from the template as-is. Customise only:
  - §12 format recommendations (which formats best fit THIS buyer's media consumption habits — pulled from research dossier)
  - §13 short-form / UGC / founder script templates with project-specific {{vars}} filled
  - §15 CTA testing table with project-specific CTAs
- §14 Visual Guidance: customise the e-comm vs info-product subsections to match product type. Pull visual language from competitor swipe file (what visual styles are dominant in this category).

---

## §16 Testing Framework (HITL-DECIDED)

**Sources:** `ab-test-setup` skill framework + research-driven priority

**Synthesis logic:**
- DRAFT in Phase 3: rank the 8 testing variables (hook, angle, offer, proof, format, CTA, visual, script) by leverage based on:
  - If awareness is mostly Problem-Aware → hook leverage is highest (test hooks first)
  - If sophistication is 4-5 → angle leverage is highest (saturated market — need new entry points)
  - If §8 proof is thin → proof type leverage is highest (test proof variants first to find what builds belief)
  - If competitor swipe shows everyone using same format → format leverage is highest (differentiate on format)
- Present top 3 candidates to HITL Phase 4. User picks #1.
- Creative Testing Matrix + Test Planning Table: design first DCT batch around the chosen variable.

---

## §17 Iteration Rules

**Source:** static `ab-test-setup` decision matrix.

**Customisation:** only the `when_to_iterate` opening list — write 4-6 project-specific iteration triggers based on §1-9.

---

## §18 Performance Feedback Loop

**Sources:** static template + (if exists) `clients/<project>/.meta-ad-account-id` triggered paid-media-audit findings

**Synthesis logic:**
- If paid-media-audit ran in Phase 2: pre-populate Learning Log Template with the top 5 findings from the audit.
- If no audit data: leave Learning Log Template empty — note "Populate after first DCT batch completes Week 1 of spend."

---

## §19 Asset Request Checklist

**Source:** §8 proof gaps + standard checklist

**Synthesis logic:**
- Pre-tick `[x]` items that exist (verified from research dossiers)
- Leave `[ ]` items that are missing
- Asset Gap Table: for each missing-but-critical asset, fill rows with Why It Matters + Impact + Owner (default: client) + Due Date (default: 7 days)

---

## §20 AI Prompt for Creative Development

**Source:** static template — fill {{project_slug}}, {{brand_name}}, {{core_offer}}, {{primary_kpi}}, and the 3 priority angles.

**Quality bar:** the prompt should be copy-pasteable into `/ads:concepts` or `/content:ads` and produce a usable first draft without further context.

---

## §21 Script QA Checklist

**Source:** static — pulled from `skills/ad-concept-engine/references/headline-validation-checklist.md`

---

## §22 Strategy Summary (HITL-FINALISED)

**Source:** synthesis of all prior sections

**Synthesis logic:**
- Phase 3 drafts the one-pager pulling from §1-21
- Phase 4 HITL: present the draft summary as PREVIEW in the AskUserQuestion checkpoint — user can rewrite any line via the "Other" answer
- Strategy Alignment Check: must all be `[x]` before write. If any unchecked, surface to user before writing.

---

## §23 Quick-Start Fill Section

**Source:** distilled from §1-22

**Synthesis logic:** write this section LAST. It's the minimum-viable extract for team members who only have time to read one page. Every field comes from §1-22 — never write anything new here.

---

## §24-26 Workflow / Naming / Final Notes

**Source:** static — copy from template as-is. No customisation.

---

## Quality Gates Before Write

Before Phase 5 writes the doc, verify:
- [ ] All §5 dimensions have at least 1 verbatim quote OR are marked NOT AVAILABLE
- [ ] §9, §10, §16 reflect Phase 4 HITL answers, not Phase 3 drafts
- [ ] §22 Strategy Alignment Check items are all `[x]`
- [ ] No fabricated statistics, fake testimonials, or invented competitor data
- [ ] UK English spelling throughout (run a spot-check on common words: organize→organise, color→colour)
- [ ] If SG project: SG cultural guidelines applied (no inappropriate religious/cultural framing)
- [ ] All `{{variable}}` placeholders filled or replaced with NOT AVAILABLE markers

If any gate fails, fix before writing. Don't write a half-filled doc.
