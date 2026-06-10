# Channeling Check — Pre-Write Gate

**Source:** Eugene Schwartz, *Breakthrough Advertising* (1966) + Robert Collier (1937) + Peggy Burnett's 34-piece AI-copy audit.

**Core principle (Schwartz):** "Copy cannot create desire for a product. It can only take the hopes, dreams, fears, and desires that already exist in the hearts of millions of people, and focus those already-existing desires onto a particular product."

**Operational principle (Collier):** "Enter the conversation already happening in the customer's mind."

**Diagnostic (Peggy's audit):** 23/34 AI-generated pieces tried to CREATE desire, 11 CHANNELED existing. The 11 had ~40% higher time-on-page. AI's default is to create — because the prompt is usually written from the seller's perspective, so the output centers on the product.

## Gate position

Before a single word of copy is generated. Fires first in the pre-write chain.

## Procedure

Before the writer model generates anything, it MUST produce this block and have it pass. Inject into the writer's system instructions:

```
## CHANNELING CHECK — required before writing

Existing desire we are channeling: <1 sentence, specific, concrete. NOT "wants to grow" or "needs more leads". Instead: a named hope/fear/frustration the buyer already has before they ever heard of us.>

Evidence this desire exists (verbatim quote + source file:line): "<exact quote from buyer-profile.md, testimonials, sales call transcripts, reviews, or social comments>" — <source:line>

Reader's internal conversation at the moment they see this copy:
<1 sentence. A named moment. Time of day + location + what they're doing or feeling. NOT demographic. NOT "scrolling Facebook and sees the ad".>

Am I CHANNELING this existing desire, or trying to CREATE a new one?
- CHANNELING = PASS, proceed
- CREATING = STOP. Don't write yet. Go find a real existing desire or tell the operator the buyer-profile is too thin.
```

## What failure looks like (reject, do not write)

- "Customers want to grow their business" — abstract / category-speak
- "Marketers want better attribution" — product-framed
- "Busy professionals want more time" — generic
- "Imagine a world where..." opening — fantasy creation
- Any opening that names the PRODUCT or SOLUTION before it names the READER's already-existing state

## What pass looks like

- "Existing desire: to stop feeling like an amateur when the HDB upgrade topic comes up at family dinners. Evidence: buyer-profile.md:47 — 'I just nod and say I'll think about it because I don't want to look stupid in front of my brother.' Reader moment: Sunday 10pm, spouse asleep, laptop open on couch, third tab is the PropertyGuru listing they've looked at six times this week and still can't commit to."
- "Existing desire: to explain the pricing decision to a board that doesn't understand why retention matters. Evidence: call-transcripts/2025-Q3.md:211 — 'I can't go to the board with a vibe check.' Reader moment: Thursday 4:47pm, 13 minutes before board prep call, looking at a dashboard they can't copy-paste into a slide."

## Post-opening spot check (after first paragraph drafted)

Read the first 2 paragraphs of the draft:
- Do they describe the reader's world? → CHANNELING, pass
- Do they describe the product / solution / company / fantasy outcome? → CREATING, reject and re-open

## Logging

Append one row to `clients/<slug>/copy-system/quality-gates/channeling-log.md`:
`| YYMMDD-HHMM | output file | existing desire | evidence source | reader moment | verdict |`
