---
name: Scout Mode — Research Command Center custom instructions
source: cai #35, raw-newsletters/research-command-center-scout-system-claude-projects-skills.md
loaded_by: research/buyer-language miners, avatar-research, source-of-truth, deep-research, copywriting reviewers needing primary VOC quotes
purpose: Loads Mark Masters' Research Command Center Project custom instructions verbatim plus the three Scout Skills (VOC, Competitive, Pattern), so any chat operating against a research corpus extracts verbatim customer language, competitor gaps, and cross-source patterns instead of generic summaries.
---

# Scout Mode — Research Command Center

## What this is

A Claude Project (static intelligence storage) plus three sibling Skills (dynamic scouts) that turn a pile of unorganized research files into a permanent intelligence base. The Project holds raw VOC, competitor teardowns, support tickets, surveys, and reviews. The Skills scout that base for verbatim language, undefended competitor territory, and cross-source patterns. Outputs are tactical — exact quotes, frequency counts, and named opportunity windows — not paraphrased summaries.

## Inputs / prerequisites

Minimum viable intelligence before deploying:
- 20+ customer reviews/comments (Amazon, G2, Trustpilot, Reddit, YouTube)
- 5 competitor campaigns (FB Ad Library, screenshotted email sequences, sales pages)
- 10+ support tickets or complaints (last 90 days)
- 1 customer survey with 20+ raw responses (NOT summaries)
- Optional but high-leverage: customer interview transcripts (verbatim), sales call recordings, lost deal analysis

File hygiene:
- Interviews: one file per interview, named `Interview_Customer_Date.txt`
- Surveys: raw response data only, never cleaned summaries
- Reviews: span 1-star through 5-star
- Support tickets: include verbatim language, not paraphrased

## The framework / process

Two-component architecture:

1. **Project = static storage.** A Claude Project named "Research Command Center" holds up to 100 files in its knowledge base. Documents are auto-cached, available across every chat in that Project, and scaled via RAG when context limits hit.
2. **Skills = dynamic scouts.** Three SKILL.md files (`voc-scout`, `competitive-scout`, `pattern-scout`) zipped and uploaded via Settings → Skills. Each scout has one job and activates automatically when its description matches the request.

Deployment sequence:
1. Build Research Intelligence folder structure (subfolders per source type).
2. Upload files to Project knowledge base, 5 at a time.
3. Paste Project Custom Instructions (verbatim block below).
4. Enable Settings → Labs → "Use custom skills" + "Code execution".
5. ZIP each scout folder (not the contents — the folder itself).
6. Upload via Settings → Skills, verify "Active".
7. Test each scout individually, then run integrated deployment.

Weekly Scout Protocol Mark's $10K/month copywriters run:

| Day | Source mined | Scout deployed | Output |
|-----|--------------|----------------|--------|
| Mon | Sales call transcripts | VOC | Objection-handling language |
| Tue | Competitor campaigns | Competitive | Positioning opportunities |
| Wed | Customer reviews | Pattern | Emerging desire patterns |
| Thu | Support tickets | VOC | Problem/solution language |
| Fri | All sources | All three | Complete intelligence report |

## Outputs

- **Power phrases** — verbatim customer quotes with frequency counts
- **Repeat patterns** — phrases mentioned 3+ times across sources
- **Transformation language** — before/after VOC for hero stories
- **Objection patterns** — themed concerns with exact language
- **Competitor claims map** — what every competitor is and isn't saying
- **Undefended territories** — emotional/positioning gaps with no defender
- **Pattern correlations** — cross-source connections (e.g. "82% of converters mention 'overwhelm' before 'clarity'")
- **Opportunity windows** — time-sensitive angles with evidence

Final form is a tactical brief, not a research deck.

## Application rules / scoring

Pass criteria for a deployed scout network:
- Scout returns at least one phrase you forgot was in your research → VOC working
- Scout identifies 3+ positioning angles → Competitive working
- Scout surfaces a pattern you hadn't noticed → Pattern working
- Insights are actionable today, not "interesting" → corpus quality is sufficient

Fail signals:
- Generic responses → Project instructions didn't save, or you're in a regular chat instead of the Project
- Surface-level insights → corpus has summaries, not raw transcripts
- No patterns → fewer than 20 data points, or single-source corpus
- Skills not activating → description over 200 chars, or YAML frontmatter malformed

## Exact prompts / templates / system instructions

### Project Custom Instructions (paste verbatim into Project Instructions panel)

```
You have access to comprehensive market research for copywriting projects. You are a scout gathering intelligence.

ALWAYS:
- Extract exact customer language from transcripts (verbatim quotes)
- Scout for patterns across multiple data sources
- Reference specific data points with numbers when making claims
- Address real objections using actual words from sales calls
- Use proven hooks from the swipe file with performance data
- Scout competitor territories for gaps and opportunities
- Ground all copy in actual field intelligence, not assumptions
- Identify emotional triggers competitors are missing
- Spot emerging trends before they become obvious
- Report opportunities with specific evidence and examples
- Connect disparate data points to reveal hidden insights
- Prioritize recent data but note historical patterns
- Flag conflicting intelligence for human review

WHEN ANALYZING:
- Look for what's NOT being said as much as what is
- Track frequency of mentions to gauge importance
- Note emotional intensity, not just content
- Identify transformation language for stories
- Find unique mechanisms no one else claims
- Spot new problems entering the market

WHEN REPORTING:
- Lead with most actionable intelligence
- Provide exact quotes, not paraphrases
- Include context (source, date, frequency)
- Highlight contrarian insights
- Suggest specific applications for findings
- Connect insights to revenue opportunities

Your mission: Transform raw research into tactical advantages.
```

### Scout #1 — VOC Scout (`voc-scout/SKILL.md`)

```
---
name: voc-scout
description: Scout customer conversations to extract powerful language and emotional triggers for copy
---

# VOC Scout - Customer Language Extractor

## Your Mission
Scout all customer research to extract language that converts.

## Extraction Protocol

### Phase 1: Emotional Language Scan
- Identify words that carry emotional weight
- Mark phrases repeated 3+ times
- Capture transformation moments
- Note specific pain descriptions

### Phase 2: Pattern Recognition
- Group similar complaints
- Identify desire patterns
- Map objection themes
- Track satisfaction triggers

### Phase 3: Hook Extraction
- Pull quotable phrases
- Identify story beginnings
- Extract comparison language
- Capture "aha" moments

## Output Format
- **Power Phrases**: [exact quotes with emotional weight]
- **Repeat Patterns**: [phrases appearing multiple times]
- **Transformation Language**: [before/after descriptions]
- **Objection Patterns**: [common concerns]
- **Hook Candidates**: [attention-grabbing statements]
```

### Scout #2 — Competitive Intelligence Scout (`competitive-scout/SKILL.md`)

```
---
name: competitive-scout
description: Scout competitor positioning to identify gaps and opportunities for market differentiation
---

# Competitive Scout - Market Gap Identifier

## Your Mission
Scout competitor campaigns to identify undefended market positions.

## Reconnaissance Protocol

### Phase 1: Territory Mapping
- Document all competitor claims
- Map their emotional territories
- Identify their core angles
- Track their proof elements

### Phase 2: Gap Analysis
- Find emotions they don't address
- Identify audiences they ignore
- Spot mechanisms they don't claim
- Locate proof they can't provide

### Phase 3: Opportunity Identification
- Undefended value propositions
- Emotional territories available
- Unique mechanism opportunities
- Counter-positioning angles

## Output Format
- **Competitor Claims Map**: [what they're saying]
- **Undefended Territories**: [what they're NOT saying]
- **Positioning Opportunities**: [how to differentiate]
- **Counter-Narratives**: [how to reframe]
- **Proof Advantages**: [evidence they can't match]
```

### Scout #3 — Pattern Recognition Scout (`pattern-scout/SKILL.md`)

```
---
name: pattern-scout
description: Scout across market research data to identify recurring themes and emerging opportunities
---

# Pattern Scout - Opportunity Spotter

## Your Mission
Identify patterns across all intelligence sources that reveal hidden opportunities.

## Analysis Protocol

### Phase 1: Cross-Reference Intelligence
- Connect customer complaints to competitor gaps
- Link objections to missing proof elements
- Match desires to unaddressed emotions
- Correlate success stories to patterns

### Phase 2: Trend Identification
- Spot increasing mention frequency
- Identify emerging concerns
- Track shifting priorities
- Monitor new comparison points

### Phase 3: Opportunity Prediction
- Hidden desires becoming visible
- Problems growing in urgency
- Gaps widening in market
- Angles becoming available

## Output Format
- **Emerging Patterns**: [trends gaining momentum]
- **Hidden Connections**: [non-obvious relationships]
- **Opportunity Windows**: [time-sensitive angles]
- **Predictive Insights**: [where market is heading]
- **Strategic Advantages**: [patterns competitors miss]
```

### Advanced scout commands

- `"VOC scout: Find transformation language from our happiest customers"`
- `"Competitive scout: What proof elements are competitors using that we could counter?"`
- `"Pattern scout: What's the emotional journey from problem awareness to purchase?"`
- `"All scouts: Build a campaign angle based on current intelligence"`

## Common failures

1. **ZIPing the SKILL.md instead of the folder.** Skills won't load. Right-click the folder itself → Compress.
2. **Description over 200 characters.** Skills won't auto-activate. Trim to one sharp sentence describing the action.
3. **Uploading summaries instead of transcripts.** Scouts return generic insights because there's no verbatim language to extract.
4. **Working in a regular chat, not the Project.** Custom instructions don't apply, knowledge base isn't loaded, scouts pull from training data instead of your corpus.

## When to use vs skip

**Use when:**
- Starting any new client engagement with existing research files
- Writing a sales page, VSL, or email sequence and need verbatim VOC
- Auditing whether competitor positioning has unclaimed territory
- Running weekly intelligence cycles for retainer clients

**Skip when:**
- You don't yet have minimum viable intelligence (20 reviews / 5 competitors / 10 tickets / 1 survey) — gather first, deploy second
- You're writing for a market you've never sold into and have zero corpus — this amplifies intelligence, it can't manufacture it
