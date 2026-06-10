# Audience Insights Synthesis Template

Use this derivative when raw audience data includes any of:

- `pain_points`
- `failed_solutions`
- `desired_outcomes`
- `objections`
- `misconceptions`
- `golden_nuggets`
- `language_notes`
- Reddit / forum / review quotes

The goal is a clean marketing-useful synthesis that downstream concept, avatar, copy, and video workflows can read without parsing the full source-of-truth document.

Save project-level outputs as:

```text
clients/<project>/01_research/output/<YYMMDD>-audience-insights-synthesis.md
```

Always keep future synthesis outputs in this same research-stage folder. Do not save them inside a campaign concept folder unless the user explicitly asks for a campaign-local copy.

When extending research after a synthesis exists:

- Read the latest `*audience-insights-synthesis.md` first.
- Read only the specific supporting files it cites under `clients/<project>/01_research/output/agent-findings/` and `clients/<project>/01_research/output/raw/`.
- Add new agent findings under `clients/<project>/01_research/output/agent-findings/`.
- Add raw source captures under `clients/<project>/01_research/output/raw/<source>/`.
- Write a new dated synthesis in `clients/<project>/01_research/output/` instead of scattering updates across `_brand/` or campaign folders.

For legacy projects without the Jake stage folders, save as:

```text
clients/<project>/research/audience-insights-synthesis.md
```

## Rules

- Stay 100% true to the source data.
- Prioritise Reddit, forum, review, and comment-section language when available.
- Include only insights relevant to the brand's ICP, product, and service.
- Group similar entries where it improves readability.
- Do not invent quotes, personas, fears, claims, or objections.
- If a quote is rewritten for naturalness, mark it as rewritten and preserve source provenance.
- If a section has thin data, write `NEEDS MORE RESEARCH` rather than padding.
- Keep brand claims and compliance constraints separate from audience language.

## Output

```markdown
# Audience Insights Synthesis — {{Brand / Product}}

Generated: {{YYYY-MM-DD}}
Project: {{project}}
Product / offer: {{product_or_offer}}
Primary source files:
- {{source_1}}
- {{source_2}}

Research density:
- Reddit / forum sources: {{count_or_status}}
- Review / social sources: {{count_or_status}}
- Internal / existing creative sources: {{count_or_status}}
- Verbatim quote count used: {{count}}

## Categorized Insights

### Top Pain Points

| Pain Point | Description |
|---|---|
| {{short_title}} | {{1-2 line emotional reality behind it}} |

Group similar issues where appropriate. Only include pain points relevant to the ICP, product, and service.

### Failed Solutions

| Attempt | Why It Failed |
|---|---|
| {{what users tried}} | {{why it did not solve the problem}} |

Group similar failed attempts if needed. Only include attempts tied to the core offer or target problem.

### Desired Outcomes

| Outcome | Explanation |
|---|---|
| {{desired state}} | {{why it matters emotionally or practically}} |

### Objections

| Objection | Real Quote / Paraphrase |
|---|---|
| {{simple user hesitation}} | {{natural skeptical wording, sourced or marked as paraphrase}} |

Write the second column like the audience would speak, not like a strategist.

### Misconceptions

| Misconception | Clarification |
|---|---|
| {{wrong belief}} | {{correct understanding written simply}} |

Do not confuse misconceptions with objections. Misconception = wrong belief. Objection = reason not to buy.

### Golden Nuggets (Quotes From Reddit / Forums / Reviews)

Include only nuggets directly tied to the ICP, product, or service.

| Quote | Category | Source | Handling |
|---|---|---|---|
| "{{quote}}" | Frustration / Skepticism / Humor / Hopelessness / DIY struggle | {{source URL or file}} | Verbatim |
| "{{natural rewrite}}" | {{category}} | {{source URL or file}} | Rewritten from source; not invented |

If the original quote already sounds natural, keep it verbatim. If it is too formal or clunky, rewrite using the `language_notes` style while keeping provenance.

## Strategy Implications For {{Brand Name}}

| Opportunity | How {{Brand}} Can Win |
|---|---|
| {{marketing-relevant opportunity}} | {{practical implication for positioning, creative, offer, proof, or funnel}} |

## ICP Language Analysis

### Natural Tone
{{formal vs informal, polished vs raw, expert vs peer-to-peer}}

### Emotional Style
{{skeptical, stressed, proud, fed up, hopeful, ashamed, confused, etc.}}

### Vocabulary
- Terms they use: {{specific terms, phrases, slang, category words}}
- Terms to avoid: {{jargon, brand-speak, generic claims they reject}}

### Copywriting Tips
1. {{how to speak exactly like the ICP}}
2. {{real phrase or pattern to mirror}}
3. {{what to avoid}}

Use real examples where possible.

## Key Personas

### Persona Name ("Nickname")

- Age Range:
- Quick Summary:
- Desire:
- Pain point:
- Objection:
- Lifestyle:
- How they perceive risk:
- What activities they do:
- Their opinions:
- Their interests:
- Their values:
- How they speak:
- Evidence basis: {{source quotes/files or NEEDS MORE RESEARCH}}

Repeat for each distinct persona supported by the data.

## Excluded Or Low-Relevance Data

| Excluded item | Why excluded |
|---|---|
| {{source or insight}} | {{off-ICP, off-offer, unsupported, compliance risk, too generic}} |

## Research Gaps

- {{gap_1}}
- {{gap_2}}

## Downstream Use

- Feed `avatar-research` with Key Personas and ICP Language Analysis.
- Feed `video-concept-lab` with Top Pain Points, Golden Nuggets, Misconceptions, and Strategy Implications.
- Feed `ad-concept-engine` with Objections, Failed Solutions, and desired outcomes.
- Feed `video-brief-normalizer` only after concept approval; this file is research input, not a production brief.
```
