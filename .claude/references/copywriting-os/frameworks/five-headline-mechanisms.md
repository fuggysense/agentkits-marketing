---
name: 5 Headline Mechanisms
source: cai #39, raw-newsletters/headline-laboratory-claude-project-skill.md
loaded_by:
  - frameworks/five-headline-mechanisms.md
purpose: The five psychological mechanisms behind every headline that has ever worked, with formulas, scoring rubric, and the "generate 10, score, recommend top 3" production protocol.
---

# 5 Headline Mechanisms

## Canonical definition

Every winning headline activates one or more of five psychological mechanisms — not formats, not templates, **mechanisms**. The Headline Laboratory generates 10 variations per project (2 per mechanism), scores each on Specificity / Emotional Pull / Clarity, and recommends a top 3 for A/B testing.

> "Every headline that's ever worked falls into one of five psychological categories. Not formats. Not templates. Mechanisms." — Mark Masters

> "They spend 80% of their time on body copy. But 80% of readers never get past the headline. You're polishing the furniture in a house nobody's entering." — Mark Masters

## The 5 elements

### 1. Curiosity Gap
Creates an incomplete pattern the brain must resolve. The mind hates open loops.

- Example (verbatim): *"The Weird Reason Most Diets Fail After Day 11"*
- Formulas:
  - The [Unexpected Adjective] Reason [Common Belief] Is Wrong
  - What [Authority/Group] Won't Tell You About [Topic]
  - The [Number] [Topic] Secrets Hidden in [Unexpected Place]
  - Why [Positive Action] Might Be [Negative Outcome]
- When to use: cold-traffic top-of-funnel, content hooks, anywhere you need to interrupt scrolling and force resolution.

### 2. Specific Benefit
Concrete outcome with numbers, timeframes, or precise results. Specificity equals believability.

- Example (verbatim): *"Add 2.3 Pounds of Muscle in 28 Days Without Changing Your Diet"*
- Formulas:
  - [Achieve Result] in [Timeframe] Without [Common Obstacle]
  - How to [Desired Outcome] in [Number] [Time Period]
  - The [Number]-Step System That [Specific Result]
  - Get [Specific Benefit] by [Specific Date/Timeframe]
- When to use: warm/aware audiences, sales pages where you can back specifics with proof, offer-presentation headlines.

### 3. Contrarian Hook
Challenges an assumed belief. Pattern interrupt that stops the scroll.

- Example (verbatim): *"Why Everything You Know About SEO Is Costing You Traffic"*
- Formulas:
  - Why [Common Advice] Is Destroying Your [Desired Outcome]
  - Stop [Common Practice] (Do This Instead)
  - The [Industry] Lie That's Costing You [Loss]
  - [Common "Good" Thing] Is Killing Your [Results]
- When to use: sophisticated/aware markets where the standard pitch is exhausted, thought-leadership positioning, content with a strong differentiating POV.

### 4. Fear/Risk
Highlights the cost of inaction. Loss aversion outweighs desire for gain.

- Example (verbatim): *"The $47,000 Mistake Hiding in Your Sales Page Right Now"*
- Formulas:
  - The $[Amount] Mistake Hiding in Your [Asset]
  - [Number] Warning Signs Your [Thing] Is About to Fail
  - Are You Making This [Costly Adjective] [Topic] Error?
  - What Happens When [Bad Outcome] (And How to Prevent It)
- When to use: audiences in active pain, audit/diagnostic offers, anything where the cost of doing nothing is concrete and quantifiable.

### 5. Identity Call
Speaks directly to who they are or who they want to become. Tribal recognition.

- Example (verbatim): *"For Copywriters Who Refuse to Compete on Price"*
- Formulas:
  - For [Identity] Who [Distinguishing Behavior]
  - The [Topic] Guide for [Specific Identity Type]
  - Why [Identity Group] Are Switching to [Solution]
  - [Identity]: Here's What [Other Group] Will Never Understand
- When to use: niche-specific offers, communities, premium positioning where the reader's self-concept is the buying trigger.

## Application rules

> "Every winning headline activates one or more of these mechanisms. No exceptions." — Mark Masters

**Production protocol (verbatim from the SKILL.md):**
1. **Context Check.** Confirm `product-context.md` is loaded with: product name, primary benefit, target audience, key differentiator. If missing, ask before generating.
2. **Generate exactly 10 headlines** — 2 per mechanism. Use the formulas as structural starting points, adapted to product context.
3. **Score each 1–10** on three axes:
   - Specificity (vague = low, concrete = high)
   - Emotional pull (flat = low, visceral = high)
   - Clarity (confusing = low, instant understanding = high)
4. **Recommend top 3** with one-sentence rationale and an A/B-testing note.

**Hard rules:**
- Never generate fewer than 10. Never skip a mechanism — even weak attempts in an unfit category surface contrasts that strengthen the strong ones.
- Headlines must reference real product context. Generic templates with [Brackets] left in are not deliverables.
- Top-3 picks should typically span at least 2 mechanisms — testing two Curiosity Gaps against each other is wasted variance.
- Update `winning-headlines.md` with tested winners (organized by mechanism, with product/client and result). The system gets smarter with every campaign.

## Diagnostic / scoring

Reviewer / generator output format:

```
## Generated Headlines

### Curiosity Gap
1. [Headline] — Score: X/10
2. [Headline] — Score: X/10

### Specific Benefit
1. [Headline] — Score: X/10
2. [Headline] — Score: X/10

### Contrarian Hook
1. [Headline] — Score: X/10
2. [Headline] — Score: X/10

### Fear/Risk
1. [Headline] — Score: X/10
2. [Headline] — Score: X/10

### Identity Call
1. [Headline] — Score: X/10
2. [Headline] — Score: X/10

---

## Top 3 Recommendations

1. [Headline] — [Mechanism] — Score: X/10
   Why: [One sentence rationale]

2. [Headline] — [Mechanism] — Score: X/10
   Why: [One sentence rationale]

3. [Headline] — [Mechanism] — Score: X/10
   Why: [One sentence rationale]

## Testing Notes
[Brief suggestion on which to A/B test first and why]
```

**Scoring rubric anchors:**
- **Specificity 10**: hard numbers, named timeframes, precise outcomes ("2.3 lbs in 28 days," "$47,000 mistake"). **Specificity 1**: vague abstractions ("fast results," "transform your business").
- **Emotional pull 10**: visceral language, identity stakes, vivid loss/gain framing. **Emotional pull 1**: flat description.
- **Clarity 10**: instant understanding without re-reading. **Clarity 1**: needs decoding; reader pauses.

A headline scoring < 6 average across the three axes should be discarded, not promoted to "top 3."

## Common failures

1. **Format instead of mechanism.** Writing "X reasons your Y is failing" because it's a familiar template, with no underlying psychological pull. The mechanism (Curiosity / Fear / Specificity / Contrarian / Identity) must be load-bearing — the format is just the structure.
2. **Round-number vagueness.** "Save time," "lose weight fast," "grow your business" — these score 1–3 on Specificity. Specific Benefit headlines must include numbers, timeframes, or measured outcomes.
3. **Single-mechanism testing.** A/B-testing two Curiosity Gaps against each other instead of one Curiosity Gap vs. one Specific Benefit. You learn nothing about which mechanism the audience responds to.
4. **Polishing body copy while neglecting headlines.** "80% of readers never get past the headline." A 2.1% → 4.7% conversion lift in the newsletter's case study came from changing one thing — the headline.

## Exact prompts (verbatim)

**Headline Laboratory Project — Custom Instructions:**

```
You are a direct response headline specialist. When generating headlines:
- Use the formulas in headline-formulas.md as structural templates
- Reference winning-headlines.md for proven patterns
- Pull product details from product-context.md
- Always generate options across all five mechanisms
- Score each headline 1-10 based on specificity, emotional pull, and clarity
- Recommend top 3 with brief rationale
```

**Headline Generator SKILL.md frontmatter:**

```
---
name: Headline Generator
description: Generates and scores 10 headline variations across five psychological mechanisms
version: 1.0
author: Mark Masters
---

# Headline Generator Skill

## Purpose
Generate 10 headline variations (2 per mechanism), score each, and recommend top 3.

## Process

### Step 1: Context Check
Confirm product-context.md is loaded. If missing key details, ask for:
- Product name
- Primary benefit
- Target audience
- Key differentiator

### Step 2: Generate Headlines
Create exactly 10 headlines:
- 2 Curiosity Gap
- 2 Specific Benefit
- 2 Contrarian Hook
- 2 Fear/Risk
- 2 Identity Call

Use formulas from headline-formulas.md as structural starting points. Adapt to
product context.

### Step 3: Score Each Headline
Rate each headline 1-10 based on:
- Specificity (vague = low, concrete = high)
- Emotional pull (flat = low, visceral = high)
- Clarity (confusing = low, instant understanding = high)

### Step 4: Output Format
[See output format above]
```

**`product-context.md` template (load before generating):**

```
# Current Product Context

## Product/Offer Name
[Name]

## What It Does
[One sentence]

## Primary Benefit
[The main outcome]

## Target Audience
[Who this is for]

## Key Differentiator
[What makes this different]

## Price Point
[Price or range]

## Biggest Objection
[What stops people from buying]
```

**`winning-headlines.md` (archive — populate after every campaign):**

```
# Winning Headlines Archive

## Curiosity Gap Winners
- [Headline] — [Product/Client] — [Result if known]

## Specific Benefit Winners
- [Headline] — [Product/Client] — [Result if known]

## Contrarian Hook Winners
- [Headline] — [Product/Client] — [Result if known]

## Fear/Risk Winners
- [Headline] — [Product/Client] — [Result if known]

## Identity Call Winners
- [Headline] — [Product/Client] — [Result if known]
```

> "Amateurs write headlines. Professionals deploy headline laboratories that generate, test, and optimize on command." — Mark Masters
