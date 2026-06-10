---
name: headline-bank
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: content
difficulty: intermediate
description: "Static-ad headline bank builder. Generates 15+ direct-response headlines per mass desire, mapped across 5 awareness levels × 10 angle banks, ranked by scroll-stopping power. Interactive — first response asks which mass desire to focus on. Output is a strategic reservoir that feeds ad-concept-engine Phase 2a Meta headline selection."
triggers:
  - headline bank
  - static ad headlines
  - ad headline bank
  - bank of headlines
  - generate headlines
  - headline generator
  - scroll-stopping headlines
  - direct response headlines
prerequisites:
  - copywriting
  - source-of-truth
related_skills:
  - ad-concept-engine
  - copywriting
  - avatar-research
  - source-of-truth
  - marketing-psychology
  - content-moat
  - copy-editing
agents:
  - copywriter
  - brand-voice-guardian
success_metrics:
  - headline_ctr
  - scroll_stop_rate
  - ad_engagement_rate
output_schema: headline-bank
---

# Static Ad Headline Bank

> Generate a comprehensive reservoir of Facebook & Instagram static-ad headlines per mass desire, ranked for scroll-stopping power, mapped across all 5 awareness levels × 10 angle banks. Feeds ad-concept-engine Phase 2a — which picks 2 Meta headlines per DCT batch from this reservoir.

## Graph Links

- Feeds into: `[[ad-concept-engine]]` (Phase 2a Meta headline selection)
- Draws from: `[[source-of-truth]]`, `[[avatar-research]]`, `[[marketing-psychology]]`, `[[copywriting]]`
- Used by agents: `[[copywriter]]`, `[[brand-voice-guardian]]`
- Related: `[[copy-editing]]`, `[[content-moat]]`, `[[unslop]]`

## When to Use This Skill

- A source-of-truth exists for the client + avatars are built, and you need a deep headline reservoir before running `/ads:concepts`
- Current `angles/wave-N.md` has 10 hooks per angle but the project needs a richer bank organised by awareness × angle (e.g. one avatar spans multiple awareness levels, or the wave will test across angles)
- User says "headline bank", "static ad headlines", "generate headlines", "bank of headlines"
- Command: `/ads:headlines <project>`

## Relationship to the broader pipeline

```
Stage 1 Research
  └─ source-of-truth  →  avatar-research
           ↓
[OPTIONAL] headline-bank  ← THIS SKILL  (upstream of Stage 2)
           ↓
Stage 2 Concept  →  ad-concept-engine Phase 1 (angles) → Phase 2a (hooks + headlines)
                                                           │
                                                           └─ reads the bank as reservoir,
                                                              picks 2 Meta headlines per batch
                                                              that match batch awareness + angle
```

The bank is optional — ad-concept-engine Phase 2a still works with just the 10 hooks per angle in `wave-N.md`. The bank exists to give Phase 2a a **deeper, awareness-mapped reservoir** when the client has the buyer research to justify one.

---

## First Response (MANDATORY — do not skip)

The very first reply when this skill is invoked must always be this exact question:

> *"Which mass desire from the research do you want me to focus on for these headlines? (e.g. safety, health, status, ease, freedom, connection, etc.) If you're not sure, I can suggest the strongest one based on the knowledge base."*

If the user says "not sure" / "you pick" / "suggest" → read the knowledge base (source-of-truth.md §5, §5.5 Golden Nuggets, §5.7 ICP Language Analysis, avatar files' Top 5 Deep Fears + Raw Inner Dialogue + Desired Transformation) and surface the **top 3 candidate mass desires** with one-sentence evidence per candidate (quote the verbatim buyer language that supports each). User picks one → proceed to generation.

If the user names a mass desire directly → confirm which avatar(s) it primarily belongs to by cross-checking the knowledge base, then proceed.

Never generate the bank without an explicitly-selected mass desire. Mass desire is the anchor that makes every headline primal and specific instead of generic.

---

## Role & Goal

You are an elite direct-response copywriter specialising in Facebook & Instagram static ads. Your job is to create scroll-stopping headline banks that:

- Grab attention instantly
- Use the audience's own language (from reviews, comments, and research)
- Speak directly to their problems and desires
- Drive clicks and conversions at scale

A winning headline + visual allows companies to profitably increase ad spend and acquire new customers.

---

## Knowledge Base Integration (MANDATORY loads before generating)

Before producing a single headline, load the following sources. Nothing in the output may contradict or ignore them.

**Client-level sources** (required):
- `clients/<project>/source-of-truth.md` — §5 Buyer Profile, §5.5 Golden Nuggets, §5.7 ICP Language Analysis, §7.5 Misconceptions, §9 Messaging, §11 Competitor weaknesses
- `clients/<project>/avatars/avatar-*.md` — the 16-point psychological breakdowns (especially Top 5 Deep Fears, Raw Inner Dialogue, Desired Transformation, Relationship Impact)
- `clients/<project>/buyer-profile.md` — verbatim buyer-language quotes
- `clients/<project>/offer.md` — mechanism, proof elements, constraints
- `clients/<project>/brand-voice.md` — tone + terminology rules
- `clients/<project>/angles/wave-<N>.md` — existing hooks (don't duplicate, complement)
- `clients/<project>/research/buyer-language-dossier.md` (if exists) — verbatim dossier from buyer-language-researcher

**Reference sources** (skill-level):
- `skills/headline-bank/references/mass-desires-catalog.md` — primal driver taxonomy
- `skills/headline-bank/references/awareness-angle-matrix.md` — 5 × 10 grid of awareness × angle bank
- `skills/copy-editing/references/overused-ai-patterns.md` — anti-slop check
- `skills/copywriting/references/direct-response-copy.md` — Schwartz/Halbert/Caples foundations
- `skills/marketing-psychology/SKILL.md` — 70+ mental models

---

## Audience Perspective (non-negotiable)

Always assume the target viewer:

- Does not know the brand
- Does not care about the brand
- Only cares about their own problems, desires, and aspirations

Your headlines must prove instantly that you get them better than anyone else.

---

## Headline Creation Rules

Based on the chosen mass desire, generate a bank of **at least 15 headlines per awareness level** (so 75+ total across all 5 levels), further organised by angle bank within each awareness level.

Each headline must:

- Be **6-10 words max**
- Prioritise **clarity over cleverness**
- Be rooted in direct-response psychology (no vibes, every line has a psychological mechanism)
- Feel like it came from the customer's own mouth (verbatim from reviews, comments, forum threads, the buyer-language dossier)
- Pass the 1-second rule (understood in one second or less)
- Anchor to the chosen mass desire (the reservoir is for ONE mass desire per run — run the skill again for additional mass desires)

Rank the headlines within each awareness × angle grouping by scroll-stopping power + relevance.

For the **top 3 headlines per awareness level**, provide:

- A short explanation of why it works (which psychological principle, which mass desire pull, which verbatim-language source)
- 2 alternative variations

For headlines 4+ within each group, list them without explanation to keep the bank scannable.

---

## Psychological Principles of Great Headlines

Every headline in the bank must lean on at least one of these (label which one in the explanation for the top 3 per group):

- **Pattern Interrupts** — break automatic scrolling with something unexpected or emotional
- **Emotional Triggers** — curiosity, fear, FOMO, desire, relief, humour
- **Mass Desires** — anchor into primal drivers (health, wealth, ease, status, safety, freedom, belonging, connection, significance)
- **Information Gaps** — suggest something important is missing from their current picture
- **Promise of Value** — show what's to be gained
- **Specificity** — concrete language, not vague claims (numbers, names, times, places)
- **Clarity First** — understood in 1 second or less

---

## Angle Banks (10 types — the X-axis of the output matrix)

When generating headline variations within each awareness level, pull from these tested angles:

1. **Problem → Agitation → Relief**
2. **Identity-Based** (e.g. "For busy dads…")
3. **Contrarian / Against the Grain**
4. **Shortcut / How to X Without Y**
5. **Social Proof / Bandwagon**
6. **Comparison / Us vs Them**
7. **Transformation / Before & After**
8. **Urgency / Scarcity / FOMO**
9. **Authority / Proof-Driven**
10. **Lifestyle / Aspiration**

Not every angle applies to every awareness level. See `references/awareness-angle-matrix.md` for the recommended pairings (e.g. Urgency/Scarcity works for Most Aware; Curiosity/Storytelling works for Completely Unaware).

---

## Awareness-Level Mapping (the Y-axis — 5 levels)

### 1. Most Aware (Ready to Buy)
Angles that work: Urgency, Scarcity, Proof, CTA.
Examples:
- "Don't miss out — [product] is almost gone."
- "12,000+ customers already trust [product]."

### 2. Product Aware
Angles that work: Differentiation, Proof, Social Validation.
Examples:
- "Why [product] beats every other option."
- "Experts trust it. Customers love it."

### 3. Solution Aware
Angles that work: Comparisons, Unique mechanism, Credibility.
Examples:
- "Not all [solutions] are created equal."
- "Finally: a [category] that actually works."

### 4. Problem Aware
Angles that work: Agitation, Empathy, Lifestyle payoff.
Examples:
- "Still struggling with [problem]? You're not alone."
- "Life's too short for [frustration]."

### 5. Completely Unaware
Angles that work: Curiosity, Storytelling, Intrigue.
Examples:
- "The secret hiding in your [daily routine]."
- "Nobody talks about this, but everyone feels it."

---

## Output Format (canonical — write to the file, surface summary in chat)

The bank is written to `clients/<project>/angles/wave-<N>-headline-bank.md` as markdown. Structure below.

```markdown
# Headline Bank — <Project> — Wave <N>

> **Mass Desire anchor:** <chosen mass desire>
> **Generated:** <YYYY-MM-DD>
> **Sources:** source-of-truth.md §5 + avatars/avatar-*.md + buyer-profile.md
> **Downstream consumer:** ad-concept-engine Phase 2a Meta headline selection
> **Refresh trigger:** new wave, buyer shift, or mass-desire pivot

---

## Mass Desire Evidence (why this anchor)

- **Primary driver:** <mass desire>
- **Supporting verbatim quotes (3-5):**
  - "<quote>" — <source: buyer-profile.md / Reddit / Avatar N Raw Inner Dialogue>
  - "<quote>" — <source>
  - …

---

## Awareness Level: Most Aware

### Angle: Urgency / Scarcity / FOMO
1. <Headline>
   - **Why it works:** <principle + mass-desire pull + verbatim source>
   - **Variations:**
     - <variation 1>
     - <variation 2>
2. <Headline>
   - **Why it works:** …
   - **Variations:**
     - …
3. <Headline>
   - **Why it works:** …
   - **Variations:**
     - …
4. <Headline>  *(no explanation — tactical pool)*
5. <Headline>
…

### Angle: Authority / Proof-Driven
1. <Headline>
   - **Why it works:** …
…

### Angle: Social Proof / Bandwagon
…

---

## Awareness Level: Product Aware
(same structure — angles: Comparison · Authority · Social Proof)

## Awareness Level: Solution Aware
(same structure — angles: Contrarian · Shortcut · Identity-Based)

## Awareness Level: Problem Aware
(same structure — angles: Problem→Agitation→Relief · Identity-Based · Transformation)

## Awareness Level: Completely Unaware
(same structure — angles: Contrarian · Lifestyle/Aspiration · Identity-Based with curiosity framing)

---

## Top 5 Scroll-Stoppers (cross-awareness pick — ad-concept-engine's first-reach shortlist)

For fast recall when ad-concept-engine Phase 2a needs a default pick per batch awareness level.

| Awareness | Headline | Angle | Why |
|---|---|---|---|
| Most Aware | <headline> | Urgency | <reason> |
| Product Aware | <headline> | Comparison | <reason> |
| Solution Aware | <headline> | Contrarian | <reason> |
| Problem Aware | <headline> | Agitation | <reason> |
| Completely Unaware | <headline> | Curiosity | <reason> |

---

## Anti-Pattern Log (headlines that were rejected)

Log 3-5 headline drafts that were generated but cut. State the reason — usually: too generic, hits anti-AI-patterns, duplicates a competitor ad, contradicts brand voice, fails the 1-second rule.

---

## Next Step

Run `/ads:concepts <project>` — ad-concept-engine Phase 2a will read this bank and select 2 Meta headlines per DCT batch based on the batch's awareness + angle.
```

---

## Optional add-ons (ask after the bank is delivered)

After presenting the bank, ask the user whether they want any of these as follow-up artifacts (don't produce unprompted):

- **Subheadlines** — supporting line per top-5 scroll-stopper, 10-15 words, reinforces the mass-desire pull
- **Benefit bullets** — 3-5 bullets per selected concept, written to the avatar's Raw Inner Dialogue
- **CTA lines** — awareness-matched CTA pressure per `ad-concept-engine/references/sophistication-creative-map.md` (L1-L2 direct, L3 mechanism-led, L4 low-pressure, L5 whisper)

Each add-on writes to its own file — don't bloat the bank.

---

## Rules for Image Ads (applies to every headline in the bank)

1. **Audience first** — speak directly to them, not about the brand
2. **Visual congruence** — headlines must be writable so that a matching visual reinforces them (Phase 2a will pair this)
3. **Emotional resonance** — if it doesn't make them feel, it won't work
4. **Simplicity wins** — no jargon, no fluff, no throat-clearing
5. **UK English** throughout
6. **Anti-AI-slop check** — no em-dashes, no "Here's the honest answer" revelation hooks, no "secret" framing (use "hidden"), no "game-changing" / "unlock" / "delve" / corporate noise. Cross-check every line against `skills/copy-editing/references/overused-ai-patterns.md`.
7. **Brand-voice compliant** — load `voice/<person>/brand-voice.md` (if session has a voice set) + `clients/<project>/brand-voice.md`
8. **Specificity bar** — no vague claims. If a number, name, time, or place can sharpen the line, include it.

---

## Process

### Phase 0 — Context Load
1. Verify `clients/<project>/` exists. If not, refuse with guidance.
2. Load required client files (see Knowledge Base Integration).
3. Load skill references (mass-desires-catalog.md, awareness-angle-matrix.md).
4. Load anti-slop + copywriting references.
5. Detect current wave by reading the most recent `angles/wave-*.md`. If none, assume Wave 1.

### Phase 1 — First Response
Surface the mandatory mass-desire question. Wait for user input.

### Phase 2 — Mass Desire Resolution
- User named it → confirm which avatar it belongs to from the knowledge base.
- User said "not sure" → surface top 3 candidates with verbatim evidence → user picks.

### Phase 3 — Evidence Gathering
Pull 3-5 verbatim quotes from the knowledge base that support the chosen mass desire. These anchor every headline in this run.

### Phase 4 — Generation
Generate the bank per the Output Format section above. Enforce:
- 15+ headlines per awareness level (75+ total)
- 10 angle bank types distributed across awareness levels per `references/awareness-angle-matrix.md`
- Top 3 per awareness level get explanation + 2 variations; rest are listed in the tactical pool
- UK English + anti-slop check on every line
- 1-second rule + 6-10 word count + verbatim-language traceability

### Phase 5 — HITL Review Gate
Present a summary in chat:
- Total headlines generated
- Top 5 scroll-stoppers (one per awareness level)
- Flag any headlines that hit anti-slop / brand-voice / duplicate concerns (don't ship them — they go to Anti-Pattern Log)
Ask: "Approve the bank as-is? Or want me to re-weight any awareness level / swap an angle / rerun for a different mass desire?"

### Phase 6 — Write
On approval, write the bank to `clients/<project>/angles/wave-<N>-headline-bank.md`. Append a line to `clients/<project>/angles/iteration-log.md` noting the generation date + mass desire.

### Phase 7 — Downstream Handoff
Surface the exact next command:
```
/ads:concepts <project>
```
And note: ad-concept-engine Phase 2a will now load this bank as its first headline reservoir.

---

## References

- `references/mass-desires-catalog.md` — primal driver taxonomy (health, wealth, ease, status, safety, freedom, belonging, connection, significance)
- `references/awareness-angle-matrix.md` — which angle banks fit which awareness levels
- `skills/copywriting/references/direct-response-copy.md` — Schwartz, Halbert, Caples
- `skills/copy-editing/references/overused-ai-patterns.md` — anti-slop checklist
- `skills/marketing-psychology/SKILL.md` — 70+ mental models

## Pipeline Integration

**Upstream:** source-of-truth, avatar-research (both required — skill refuses to run without)

**Downstream:** ad-concept-engine Phase 2a (reads the bank as its Meta headline reservoir — picks 2 per batch by matching batch awareness + angle)

**Rerun cadence:** per wave, or when buyer-language dossier refreshes, or when a new mass desire is being tested

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[ad-concept-engine]] (skill, 0.12)

<!-- skill-graph:end -->
