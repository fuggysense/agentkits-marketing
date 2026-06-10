---
name: avatar-research
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: content
difficulty: intermediate
description: "Build/refresh buyer-profile.md with 3-7 micro-personas (motivation/pain/outcome/context/trigger) for video, static ads, email, landing pages, funnels. Feeds campaign-selection.json + downstream workspaces. Triggers: avatar research, build avatars, DCT avatars, audience segments, ad avatars."
triggers:
  - avatar research
  - build avatars
  - ad avatars
  - DCT avatars
  - audience segments
  - ads avatars
prerequisites:
  - marketing-psychology
  - paid-advertising
related_skills:
  - ad-concept-engine
  - copywriting
  - marketing-psychology
  - content-moat
agents:
  - persona-builder
  - researcher
  - brainstormer
mcp_integrations:
  optional:
    - scrapecreators
output_schema: buyer-profile-micro-persona-map
---

# Avatar Research

> Build or refresh `clients/<project>/_brand/buyer-profile.md` with 3-7 distinct micro-personas inside one buyer profile. A micro-persona is a targetable buyer context defined by motivation, pain, desired outcome, lifestyle/context, buying trigger, awareness, sophistication, core psychology, and market behavior. It is not a demographic character sheet and not a creative-output brief. Feeds campaign selection and every downstream deliverable workspace: video ads, static ads, email sequences, landing pages, funnels, lead magnets, and future artifact types.

## Graph Links

- Feeds into: `[[campaign-runner]]`, `[[ad-concept-engine]]`, `[[video-concept-lab]]`, `[[email-sequence]]`, `[[page-cro]]`, `[[copywriting]]`
- Draws from: `[[marketing-psychology]]`, `[[paid-advertising]]`
- Used by agents: `[[persona-builder]]`, `[[brainstormer]]`, `[[researcher]]`
- Related: `[[client-onboarding]]`, `[[offer-builder]]`

## When to Use This Skill

- Before running `/campaign:new`, `/ads:concepts`, `/copy:email`, `/copy:ad`, video concept work, landing-page work, or funnel planning
- When a project has one buyer profile but needs multiple ad audience segments
- When the user says "build avatars," "audience segments," "who are we targeting"
- When preparing any campaign that needs distinct messaging per audience segment
- Command: `/ads:avatars [project]`

## Prerequisites

**Required:**
- `clients/<project>/_brand/buyer-profile.md` — single source of truth for buyer psychology and micro-persona targeting
- `clients/<project>/_brand/icp.md` — demographics + buying behavior
- `clients/<project>/_brand/offer.md` — what we're selling and proof elements

**Foundation flexibility:** If `buyer-profile.md` doesn't exist but `icp.md` contains deep psychology (emotions, fears, Schwartz map, relationship impacts, past solutions tried), migrate/summarize that psychology into a new `buyer-profile.md` first, then add the Micro-Persona Map there. Do not make `_brand/avatars/*.md` the buyer-targeting source of truth. Check for these sections in icp.md before flagging buyer-profile.md as missing:
- Core Problem (emotional + situational) -> maps to micro-persona pain/context
- Top 5 Emotions -> maps to micro-persona primary emotion
- Top 5 Fears -> maps to micro-persona primary fear and beliefs to overcome
- Relationship Impacts -> enriches micro-persona lifestyle/context and relationship impact
- Past Solutions Tried -> maps to micro-persona past solutions tried and market behavior
- What They Don't Want To Do -> maps to micro-persona beliefs to overcome
- Schwartz Awareness Level Map -> maps to micro-persona awareness level
- Market Specifics (objections, blame, success factors) -> maps to micro-persona beliefs and market behavior

If NEITHER buyer-profile.md NOR a rich icp.md exists, route to `persona-builder` agent first.

**Deprecated output:** Separate `_brand/avatars/*.md` files are deprecated for buyer targeting. Keep them only for legacy references, downstream tooling that still requires structured files, or visual-character/mascot/presenter/face-lock work. New targeting work must update `_brand/buyer-profile.md`.

---

## Scalable Campaign Integration

Buyer targeting is build-once client foundation. This skill never creates campaign or deliverable workspaces. It writes the reusable audience layer that campaigns select from.

**Source of truth:**

```text
clients/<project>/_brand/buyer-profile.md
```

**Campaign selection layer:**

```text
clients/<project>/campaigns/<campaign>/campaign-selection.json
```

Campaigns should select one or more `micro_persona_id` values from `_brand/buyer-profile.md`. Do not copy the whole buyer profile into the campaign.

**Deliverable workspace layer:**

```text
clients/<project>/campaigns/<campaign>/<artifact-family>/<artifact-slug>/workspace-brief.json
```

Examples:

```text
campaigns/spring-launch/video-concepts/hair-drain-ferritin-gap/concept-brief.json
campaigns/spring-launch/email-sequences/post-purchase-nurture/workspace-brief.json
campaigns/spring-launch/funnel-pages/ferritin-quiz-lp/workspace-brief.json
campaigns/spring-launch/ad-concepts/meta-dct-wave-01/workspace-brief.json
```

Each workspace brief should reference selected `micro_persona_id` values plus the specific product, proof, swipe, and research input IDs from `00_inputs/input-manifest.json`. It must not duplicate `_brand/buyer-profile.md` or broad input folders.

**Naming rule:** prefer `micro_persona_id` for targeting. Use `avatar_id` only for legacy/tooling exports or visual-character/persona assets.

---

## Process: 4 Phases + 2 HITL Gates

### Phase 0: Context Load + Foundation Check

**Role:** Orchestrator (main context)

0. **Check the research-vault FIRST — never commission research that already exists.** Before generating any Phase 2 external-research prompts, list `~/AI workflows/research-vault/markets/` for dossiers matching this client's market (e.g. `sg-property-*`, or the relevant category). If a matching market folder exists and is fresh (<60 days — check the newest aspect-file mtime), MINE it to ground the micro-personas: aspect files include `fears.md`, `frustrations.md`, `desired-outcomes.md`, `trigger-events.md`, `trusted-voices.md`, `sophistication-schwartz.md`, `awareness-schwartz.md`, `competitive-landscape.md`. Pull verbatim quotes + validated Schwartz/sophistication from there. Only run Phase 2 research for the GAPS the vault doesn't cover. Tell the user which vault dossiers were found and their freshness. (Dispatch a sub-agent to read the dossiers so raw research stays out of the orchestrator context.)

1. Load foundation files:
   - `clients/<project>/_brand/buyer-profile.md` — emotions, fears, Schwartz levels, objections
   - `clients/<project>/_brand/icp.md` — demographics, psychographics, buying behavior
   - `clients/<project>/_brand/offer.md` — value proposition, proof elements, case studies
   - `clients/<project>/_brand/brand-voice.md` — tone constraints
   - `clients/<project>/_brand/story-bank.md` — client stories (if exists)

2. Check whether `clients/<project>/_brand/buyer-profile.md` already contains `## MICRO-PERSONA MAP`:
   - If yes and <60 days old: offer to refresh, extend, or skip
   - If yes and >60 days old: recommend refresh
   - If no: proceed to Phase 1
   - If `_brand/avatars/` exists, treat it as legacy/tooling input only. Mine useful insights, but do not update it as the targeting source unless the user explicitly asks for legacy/tooling output.

3. Verify foundation completeness. Flag gaps:
   - buyer-profile.md must have: Core Problem, Top 5 Emotions, Top 5 Fears, Schwartz Map, Micro-Persona Map
   - icp.md must have: qualification boundary, category context, buying behavior, and where they congregate
   - offer.md must have: Core Offer, Proof Elements

---

### Phase 1: Micro-Persona Hypothesis Generation

**Role:** Orchestrator with marketing-psychology knowledge

Using buyer-profile.md as the foundation, generate 4-6 micro-persona hypotheses by segmenting along buyer psychology and context, not demographics alone:

**Segmentation axes:**
- **Schwartz awareness level** — an Unaware avatar behaves differently from a Solution-Aware avatar
- **Market sophistication** — a Level 2 buyer who's never seen property ads vs a Level 4 buyer who's been burned
- **Motivation** — what they are trying to protect, gain, avoid, prove, or become
- **Pain** — the acute problem or tension that makes the category matter
- **Desired outcome** — the concrete after-state they want
- **Lifestyle/context** — where the problem shows up in daily life, routines, roles, constraints, or environment
- **Buying trigger** — what event pushed them to consider this NOW
- **Failed solution history** — what they've already tried and how it shapes their skepticism
- **Cultural/values segment** — religious considerations, family structure, community identity
- **Market behavior and distinctness** — what they have seen, rejected, still notice, and what makes this segment meaningfully different

For each hypothesis, provide:

```
| # | Working Name | Motivation | Pain | Desired Outcome | Awareness | Soph Level | Buying Trigger | Distinct Because |
|---|--------------|------------|------|-----------------|-----------|------------|----------------|----------------------|
| 1 | "The ..." | Protect family security | Confused by... | Confident decision | Problem-Aware | L3 | Renewal deadline | Has a different trigger and skepticism pattern |
```

### HITL Gate 1: Micro-Persona Selection

Present the 4-6 hypotheses as a scannable table. User actions:
- Select 3+ to develop fully
- Merge similar hypotheses
- Rename micro-personas
- Suggest new ones the data missed
- Request a specific segment ("what about devout Muslim families?")

Proceed only with selected micro-personas. Final map should usually contain 3-7 micro-personas.

---

### Phase 1.5: Sales Copy Extraction (Optional)

**Trigger:** User has existing sales copy, landing pages, or marketing materials to mine for buyer psychology. Skip if no copy exists.

**Role:** Orchestrator applying consumer psychology extraction

After micro-persona selection, ask:
> "Do you have any sales copy, landing pages, or marketing materials I can extract buyer psychology from? This deepens the micro-persona map with language, emotional triggers, and proof patterns already proven to resonate."

If yes, extract using this framework:

**Extraction checklist (parse the copy for each):**

| Element | What to Look For |
|---------|-----------------|
| **Demographics** | Who is addressed? Age clues, career stage, life situation, income signals |
| **Core Problem** | What emotional + situational challenge is named or implied? |
| **Emotions Triggered** | What feelings does the copy validate or agitate? Look for pain amplification sections |
| **Fears Invoked** | What worst-case scenarios? What "if you don't act" consequences? |
| **Relationship Impacts** | How does the copy say this problem affects family, work, social life? |
| **Past Solutions Referenced** | What "you've tried X but..." language? Failed approaches mentioned? |
| **Resistances Addressed** | What objections are preemptively handled? What does the buyer not want to do? |
| **Transformation Promised** | What "after" state? What life looks like post-solution? |
| **Market Psychology** | What must the buyer believe? Who is blamed? What must they give up? |
| **Language Patterns** | Exact phrases, slang, emotional vocabulary the copy uses to connect |
| **Proof Elements** | What social proof, data points, testimonials, guarantees are used? |

**Output:** A structured extraction per micro-persona — map each finding to the specific micro-persona it enriches:

```
## Copy Extraction → Micro-Persona Mapping

### Micro-Persona 1: [Name]
- Emotions found: [from copy] → enriches "Day-to-Day Struggles" + "Buying Emotion"
- Language patterns: [exact phrases] → enriches raw inner dialogue and messages seen/rejected
- Fears invoked: [from copy] → enriches "Beliefs We Must Overcome"
- Proof or claim patterns: [from copy] → record as messages seen before, not as recommendations

### Micro-Persona 2: [Name]
...
```

**Integration rule:** Extracted psychology supplements but does NOT replace external research (Phase 2). Copy extraction shows what WORKED in past messaging. External research reveals what the AUDIENCE actually thinks/feels/says. Both are needed — one is the marketer's lens, the other is the buyer's lens.

**If no sales copy exists:** Skip this phase entirely. The external research in Phase 2 compensates.

---

### Phase 2: External Research Prompts

For each selected micro-persona, generate **3 copy-paste-ready prompts** — one each for Perplexity, Grok, and ChatGPT. Each prompt is tailored to that platform's strengths.

**Present to user:**
> "Here are your research prompts. Copy each one to the relevant platform, run it, and paste the results back here. I'll compile everything into the Micro-Persona Map in buyer-profile.md."

**Prompt templates** (see `references/` for full versions):

**Perplexity prompt** (factual/data — cite sources):
Focuses on: real demographics, market data, competing products in the market, pricing, market size, regulatory context. Asks for citations.

**Grok prompt** (social sentiment — X/Twitter + Reddit):
Focuses on: what real people say about this problem, language they use, frustrations they express, solutions they mention, beliefs/objections that come up. Searches social platforms.

**ChatGPT prompt** (synthesis — expand from buyer-profile):
Focuses on: taking the existing buyer-profile.md excerpt and generating the micro-persona fields for this specific sub-segment. Deeper psychological analysis, belief structures, status aspirations.

Each prompt includes:
- Product/service context (from offer.md)
- Market/geography (from icp.md)
- Micro-persona description (from hypothesis)
- Relevant buyer-profile.md excerpt (emotional foundation)
- The exact Micro-Persona Map fields to fill

**User runs prompts externally, then pastes results back.**

---

### Phase 2.5: Market Sophistication Audit

**Role:** Orchestrator + external research (Perplexity/Grok)

**Purpose:** Determine the REAL sophistication level for each micro-persona by researching what marketing messages they've already been exposed to. Sophistication level drives creative strategy in `ad-concept-engine` — getting it wrong means writing ads that either talk down to cynical buyers or over-complicate for fresh audiences.

**Trigger:** Runs after external research returns (Phase 2) and before compilation (Phase 3). Can also run standalone if the Micro-Persona Map already exists but sophistication needs validation.

**For each micro-persona, research and document:**

#### Step 1: Ad Landscape Scan

Generate a Perplexity prompt per micro-persona:

```
Search for ads, marketing messages, and promotional content targeting {micro_persona_description} in {geography} for {product_category}.

I need to understand what marketing messages this audience has ALREADY been exposed to — this determines how sophisticated/cynical they are about claims in this space.

1. **Competing ads they've seen** — What Facebook/Instagram/TikTok ads are running right now in {geography} for {product_category}? What do the headlines say? What visual styles are used? Name specific brands and campaigns.

2. **Marketing claims in circulation** — What promises are commonly made in this product category? (Examples will vary by product type — e.g., for SaaS: "10x faster", "no credit card", "AI-powered"; for ecom: "free shipping", "30-day returns", "clinically proven"; for services: "satisfaction guaranteed", "same-day booking", "no obligation".) List the top 10 most common claims for THIS product/market.

3. **Seminars/webinars/events** — What seminars, masterclasses, webinars, or live events exist in {geography} for this category? Who runs them? What do they promise?

4. **Content marketing saturation** — How many YouTube channels, blogs, Instagram accounts, and TikTok creators are producing content for this audience? Is the space crowded or sparse?

5. **Regulatory/industry noise** — Are there news articles, regulator warnings (e.g. SEC, FDA, MAS, CEA — whatever applies), or government campaigns that have shaped how this audience views {product_category} marketing?

6. **Claims that have been debunked** — What marketing claims has this audience seen AND rejected? Search forums for call-outs, complaints, and "this is BS" reactions.

Cite sources. Focus on {geography}-specific data.
```

Generate a Grok prompt per micro-persona:

```
Search X/Twitter, Reddit, HardwareZone, and forums for {micro_persona_description} in {geography} reacting to {product_category} marketing.

I need to know: how jaded is this audience?

1. **Ads they mock** — Search for posts making fun of property ads, agent marketing, or upgrade promises. What specific phrases or formats do they ridicule?

2. **Claims they call BS on** — What marketing promises trigger immediate rejection? What phrases make them comment "scam" or "just want commission"?

3. **What still works** — Despite the cynicism, what marketing approaches do they engage with? What posts get saves, shares, or genuine questions (not mockery)?

4. **Trust signals they respect** — What makes them pause and take something seriously? Data? Named case studies? Anti-hype tone? Specific credentials?

5. **Ad formats they scroll past** — What visual styles, headlines, or CTAs are so overused that they've become invisible?

Search r/singaporefi, r/askSingapore, HardwareZone EDMW for "{product_category} ad", "agent marketing", "property seminar", "this is why I don't trust agents."
```

#### Step 2: Sophistication Level Assignment

Using the research, assign each micro-persona a sophistication level with EVIDENCE:

```markdown
## Sophistication Assessment — Micro-Persona [N]: [Name]

### Level: L[1-5]

### Evidence (what they've been exposed to)
- [X] competing brands running ads to this segment
- [X] common claims in circulation (list top 5)
- [X] claims they've seen AND rejected
- [X] ad formats that are now invisible to them

### What still breaks through at this level
- [Specific creative approaches from the research]

### Creative strategy implication
- Lead with: [what to open with]
- Support with: [secondary elements]
- Never lead with: [what's dead at this level]
```

#### Step 3: Cross-Micro-Persona Sophistication Matrix

Compile into a single matrix inside `clients/<project>/_brand/buyer-profile.md` under `## MICRO-PERSONA MAP`:

```markdown
### Sophistication Matrix

| Micro-Persona | Soph Level | Messages Seen | Messages Rejected | What Breaks Through | Creative Lead |
|---------------|------------|---------------|-------------------|---------------------|---------------|
| [Name] | L[N] | [count/description] | [top 3 rejected claims] | [approach] | [what opens the ad] |
```

**Output:** update `clients/<project>/_brand/buyer-profile.md`. Optional legacy/tooling output may mirror this to `_brand/avatars/sophistication-map.md` only if a downstream process still requires it.

This file is consumed by `ad-concept-engine` Phase 1 (Angle Generation) and Phase 2 (DCT Batch Assembly) to ensure creative strategy matches sophistication level. See `ad-concept-engine/references/sophistication-creative-map.md` for the L1-L5 creative framework.

### HITL Gate 2.5: Sophistication Validation (Optional)

If the user has direct experience with the market ("I've seen their ads, they're super cynical"), present the matrix and ask for corrections. Skip if user defers to the research.

---

### Phase 3: Micro-Persona Compilation

**Role:** Orchestrator (synthesis)

For each micro-persona, compile the pasted research into the standardized Micro-Persona Map format inside `buyer-profile.md`:

```markdown
## MICRO-PERSONA MAP

> Targeting source of truth. Keep 3-7 micro-personas here. These are buyer motivation/context segments, not demographic character files.

### Micro-Persona [N]: [Name]

> [One-sentence description of the motivation/context that makes this a distinct buying segment]

| Field | Value |
|-------|-------|
| Motivation | [what they are trying to protect/gain/avoid/prove/become] |
| Pain | [acute problem or tension] |
| Desired Outcome | [concrete after-state] |
| Lifestyle / Context | [where this shows up in daily life, routines, roles, constraints, or environment] |
| Buying Trigger | [event that pushes action now] |
| Awareness Level | [Schwartz level] |
| Sophistication Level | [1-5] |
| Language | [specific phrases, objections, vocabulary, or self-talk] |
| Proof | [proof elements that this segment trusts] |
| What Makes This Segment Distinct | [why this is not just a demographic split] |
| Source Confidence | [high / medium / low + reason] |

#### Psychology

- **Primary emotion:** [from buyer-profile mapping]
- **Primary fear:** [from buyer-profile mapping]
- **Beliefs to overcome:** [beliefs and counters]
- **Past solutions tried:** [what they tried and why it failed]
- **Raw inner dialogue:** [verbatim or inferred self-talk]
- **Relationship impact:** [family/work/self-worth effects]

#### Market Behavior

- **Similar products considered:** [products or alternatives they looked at]
- **Why those fell short:** [what disappointed them or made them skeptical]
- **Messages seen before:** [claims, angles, or market promises they have already encountered]
- **Messages rejected:** [claims, phrases, or formats they distrust]
- **What still breaks through at the buyer-truth level:** [non-creative description of what gets attention, not a finished angle]
- **Evidence sources:** [links, pasted research, quotes, or source notes]
```

**Quality checks during compilation:**
- Flag any section where external research was thin — offer to fill from buyer-profile.md
- Cross-check demographics against icp.md for consistency
- Verify Schwartz level assignment matches the research evidence
- Ensure each micro-persona is genuinely DISTINCT from the others by motivation, pain, outcome, context, trigger, awareness, sophistication, psychology, or market behavior
- Do not split micro-personas only by age, gender, income, or job title. Demographics can add context, but they are not the persona definition.

### HITL Gate 2: Micro-Persona Approval

Present all compiled micro-personas side by side. For each micro-persona show:
- Quick reference card
- One-paragraph summary
- How it differs from the other micro-personas

User actions:
- Approve all
- Edit specific sections
- Request re-research on weak points
- Merge or split micro-personas
- Add a new micro-persona

---

### Phase 4: Save Buyer Profile

1. Update `clients/<project>/_brand/buyer-profile.md`.
2. Add or refresh `## MICRO-PERSONA MAP`.
3. Keep 3-7 micro-personas in the map.
4. Add a refresh log entry inside buyer-profile.md:

```markdown
### Micro-Persona Refresh Log

| Date | Action | Reason | Sources |
|------|--------|--------|---------|
| YYMMDD | Created/Refreshed | Initial avatar research | Perplexity, Grok, ChatGPT |
```

5. Ensure the buyer-profile.md header says:
   `> Micro-personas for ad targeting live in this file under ## MICRO-PERSONA MAP.`

6. Do not create or update `_brand/avatars/*.md` for targeting unless the user explicitly asks for legacy/tooling exports.

7. Inform user: "Buyer-profile micro-personas ready. Run `/ads:concepts [project]` to generate DCT batches."

---

## Pipeline Integration

**Upstream:** Requires completed buyer-profile.md + icp.md + offer.md. If missing, route to:
- `client-onboarding` (full setup)
- `persona-builder` agent (buyer profile only)

**Downstream:** `buyer-profile.md` Micro-Persona Map is consumed by:
- `ad-concept-engine` v2.0 — generates DCT batches per micro-persona
- `copywriting` — can use micro-persona messaging guidance for landing pages
- `campaign-runner` — audience targeting aligned to micro-persona segments
- `image-generation` — only when a micro-persona is translated into a visual character, mascot, or recurring face. In that case, create visual-character references separately and prepend the CRITICAL CHARACTER LIKENESS block to every prompt. Required for face-lock consistency across ad creative, thumbnails, and UGC sequences. See `skills/image-generation/SKILL.md` § For Character Consistency for the full pattern + expression phrase bank.

**Refresh cadence:** Every 60 days, or when:
- New market data changes the audience landscape
- Campaign results show a micro-persona underperforming (reassess assumptions)
- Product/offer changes significantly
- User requests with "refresh avatars"

---

## Pipeline: How This Skill Relates to Persona-Builder and Client-Onboarding

Three tools, three jobs, zero overlap:

| Tool | Job | Produces | When to Use |
|------|-----|----------|-------------|
| **Client-onboarding** | Set up the business | `context-profile.json`, `icp.md`, `offer.md`, `brand-voice.md`, `channels.json` | First time setup for any project |
| **Persona-builder** | Understand the buyer deeply | `buyer-profile.md` (emotions, fears, relationships, transformation, Schwartz map) | When you need ONE deep psychological profile. Mode A = extract from copy. Mode B = interactive discovery. Mode C = enrich existing. |
| **Avatar-research** | Segment the buyer for ads | `buyer-profile.md` Micro-Persona Map (3-7 sub-segments with motivation, pain, outcome, context, trigger, awareness, sophistication, psychology, and market behavior) | Before running `/ads:concepts` for DCT. Requires buyer-profile.md + icp.md + offer.md. |

**The flow:**
```
Client-onboarding → icp.md + offer.md (foundation)
                  ↓
Persona-builder (optional) → buyer-profile.md (deep psychology)
                  ↓
Avatar-research → buyer-profile.md Micro-Persona Map (segmented for ads)
                  ↓
Ad-concept-engine → DCT batches (ready for Meta)
```

**Section ownership (no duplication):**

| Data Point | Lives In | NOT In |
|------------|----------|--------|
| Demographics, firmographics | `icp.md` | NOT in buyer-profile.md (references icp.md) |
| Business context, competitors, tools | `context-profile.json` | NOT repeated in icp.md |
| Deep emotions, fears, relationships | `buyer-profile.md` | NOT in icp.md (unless no buyer-profile exists) |
| Schwartz level (primary, one buyer) | `buyer-profile.md` | — |
| Schwartz level (per sub-segment) | `buyer-profile.md` Micro-Persona Map | Different from buyer-profile's single primary assignment |
| Solutions tried + why failed | `buyer-profile.md` general sections + Micro-Persona Map refinements | Do not fork into separate targeting files |
| Buyer psychology and segment-level market behavior | `buyer-profile.md` Micro-Persona Map | Do not turn this into campaign creative guidance |
| Ad-specific angles, formats, proof choices, visual style | Campaign/workspace artifacts such as `creative-diversity-map.json`, `concept-brief.json`, `concepts.json`, scripts, and prompt packs | NOT in buyer-profile.md |
| Transformation effects on relationships | `buyer-profile.md` general sections + Micro-Persona Map refinements | Segment-level differences stay in the map |
| Objections with reframes | `buyer-profile.md` general sections + Micro-Persona Map per-segment notes | Different scope: general vs targeted |

**When buyer-profile.md doesn't exist but icp.md is rich:**
Some projects build deep psychology directly into icp.md (emotions, fears, Schwartz map, past solutions, relationship impacts). In that case, use icp.md as the psychological source material, but create/update `buyer-profile.md` as the canonical buyer-targeting file before saving the Micro-Persona Map.

**Legacy avatar files:**
`_brand/avatars/_index.md`, `_brand/avatars/avatar-<slug>.md`, and `_brand/avatars/avatar-<slug>.json` are no longer the source of truth for buyer targeting. Use them only when:
- A legacy downstream tool still requires one-file-per-avatar exports.
- The project needs visual-character, mascot, presenter, or face-lock references.
- The user explicitly asks for separate avatar files.

When legacy files are generated, each file must link back to `../buyer-profile.md#micro-persona-map` and state that buyer targeting authority lives in buyer-profile.md.

---

## References

- `references/avatar-template.md` — Legacy one-file-per-avatar structure; use only for tooling exports or visual-character references
- `references/perplexity-prompt-template.md` — Factual/data research prompt
- `references/grok-prompt-template.md` — Social sentiment research prompt
- `references/chatgpt-prompt-template.md` — Synthesis/expansion research prompt
- `skills/marketing-psychology/SKILL.md` — 70+ mental models for segmentation
- `skills/copywriting/references/direct-response-copy.md` — Schwartz awareness levels
- `agents/persona-builder.md` — Can validate/enrich avatars via Mode C

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[persona-builder]] (agent, 0.12)

<!-- skill-graph:end -->
