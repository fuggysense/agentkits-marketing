# Coat of Arms Generator — Pre-Write Gate

**Source:** Gary Halbert — "Coat of Arms" method. Expanded + named for AI prompting by Mark Masters (cai #44).

**Core principle:** Before writing copy for a product, build a detailed, non-demographic portrait of the audience. What they read, what they fear, what they spend on without thinking, what they lied about at parties, what they'd never admit to wanting but absolutely want. Reference this portrait before EVERY write.

**Why it matters:** The audience understanding never makes it into the prompt. Our `buyer-profile.md` + `avatars/` already contain richer data than Halbert had (Schwartz awareness, 16-point psychological breakdown). But that data isn't prompt-ready. This gate converts it into a ~200-word prompt-ready portrait.

## Gate position

After channeling-check passes. Before the writer prompt is finalized.

## Procedure

### 1. Source check

Target file: `clients/<slug>/copy-system/coat-of-arms-<avatar>.md`

- If file exists AND was last modified within 90 days AND `buyer-profile.md` hasn't changed since → load as-is, skip to step 3.
- Otherwise → generate (step 2).

### 2. Generate

Read:
- `clients/<slug>/buyer-profile.md`
- `clients/<slug>/avatars/<avatar>.md`
- `clients/<slug>/source-of-truth.md` (if exists — pull §5.5 Golden Nuggets, §5.7 ICP Language Analysis)
- Testimonial quotes from `clients/<slug>/copy-system/proof-inventory.md` (if exists)

Fill this template — every slot required, no TBD allowed:

```
AUDIENCE COAT OF ARMS: <avatar name>

Who they are (specific, not demographic):
<2 sentences. Role + company-stage or life-stage + situation. NOT "B2B marketing directors age 35-50." INSTEAD "Marketing directors at B2B SaaS companies between Series A and Series C, typically the 2nd or 3rd marketing hire, reporting to a founder who doesn't quite understand what they do.">

What they read (specific publications / newsletters / substacks):
<3-5 names>

Podcasts they listen to in the car / on walks:
<2-3 names>

Twitter / LinkedIn / YouTube accounts they actually open (not just follow):
<3-5 handles>

What they fear — not "growth challenges", specific fears:
<3-5 bullets, each with verbatim language from buyer-profile or call transcripts>

What they spend money on without thinking:
<2-3 specifics>

What they've lied about at parties / social settings:
<1-2 items — the status games they play>

What they'd never admit wanting but absolutely want:
<1-2 items — the hidden real motivation>

Language patterns they use (verbatim, not paraphrased):
<5-10 short phrases the model should reuse>

Language patterns they find cringe / would never use:
<3-5 items — jargon, corporate-speak, AI-default phrases they'd roll eyes at>
```

### 3. Write to disk

Save to `clients/<slug>/copy-system/coat-of-arms-<avatar>.md`. If only one avatar exists, also symlink or copy to `coat-of-arms.md`.

### 4. Inject into writer prompt

Add to system instructions:

```
Read the coat of arms in your context before generating any copy. When you write, reference specifics from it. At the end of your response, list which coat-of-arms specifics you actually used. (Enforced by the one-person-enforcement reviewer.)
```

## What failure looks like (reject, do not generate)

- Demographic-only portrait ("35-50, urban, $100K+ HHI, married, 1-2 kids") → reject
- Generic fears ("wants to grow", "needs more leads", "frustrated with ROI") → reject
- Language patterns written in OUR voice instead of buyer's voice → reject
- Any slot with "TBD" or "varies" → reject

## Staleness

Regenerate when:
- `buyer-profile.md` has been edited since last coat generation
- New testimonials or sales-call transcripts have been added
- 90+ days since last generation

## Logging

Append to `clients/<slug>/copy-system/quality-gates/coat-log.md`:
`| YYMMDD | avatar | generated-from (buyer-profile version / SoT / testimonials) | slot completeness N/11 | operator approved Y/N |`
