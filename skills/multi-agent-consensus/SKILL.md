---
name: multi-agent-consensus
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: strategy
difficulty: intermediate
description: >
  Spawn N agents with the same prompt (slight framing variations) to independently analyze a
  problem, then aggregate results by consensus. Use for decision-making, ranking options, strategic
  analysis, naming, positioning, or any problem where you want to filter hallucinations and surface
  high-variance ideas.
triggers:
  - consensus
  - poll agents
  - stochastic consensus
  - spawn N agents to analyze
  - multi-agent vote
  - what do multiple agents think
  - get multiple opinions
  - poll on
  - compare approaches
prerequisites: []
related_skills:
  - verification-loops
  - deep-research
  - prompt-contracts
agents:
  - brainstormer
  - researcher
  - planner
---

# Stochastic Multi-Agent Consensus

Spawn N agents (default 10) with identical context and near-identical prompts. Each independently analyzes and produces a structured response. Aggregate by finding consensus (mode), divergences (splits), and outliers (unique ideas).

**Why this works:** Exploits stochastic variation in LLM outputs. Like polling 10 experts instead of asking one. The mode filters out hallucinations and individual biases. Divergences reveal genuine judgment calls. Outliers surface creative ideas a single run would miss.

## Language & Quality Standards

**CRITICAL**: Respond in the same language the user is using.

## When to Use This Skill

- Choosing between campaign strategies or marketing approaches
- Naming products, features, or campaigns
- Ranking headline/CTA options for ad creative
- Strategic decisions (channel mix, pricing tiers, positioning angles)
- Any decision where you want multiple perspectives, not just one

**NOT for:** Factual lookups, simple tasks with one right answer, or tasks where speed matters more than thoroughness.

## Marketing-Specific Use Cases

| Decision Type | Agent Count | Framing Strategy |
|--------------|-------------|-----------------|
| Headline A/B ranking | 10 | Mix audience personas + psychology framings |
| Campaign strategy choice | 5-7 | Risk-averse, growth, contrarian, budget-constrained |
| Brand positioning | 10 | Customer-first, competitor-aware, founder-vision |
| Channel prioritization | 7 | ROI-focused, brand-building, speed-to-results |
| Pricing decisions | 10 | Value-based, competitive, psychological, cost-plus |

## Execution

### 1. Parse the request

Extract from the user's message:
- **Problem/question** to analyze
- **Agent count N** — default 10. User can override ("spawn 5 agents", "poll 20 agents")
- **Output format** — what each agent should produce (rankings, recommendations, yes/no decisions, scores, etc.)
- **Options list** (if applicable) — predefined options to rank/evaluate, or let agents generate their own

If the problem is vague, ask the user to sharpen it. N agents on a fuzzy prompt wastes tokens.

### 2. Design the structured output schema

Before spawning, define what each agent must return. This MUST be structured enough to aggregate. Examples:

- **Ranking task**: "Rank these 5 options from best to worst. Output as a numbered list 1-5."
- **Open recommendation**: "Propose your top 3 recommendations. For each: name, one-sentence rationale, confidence score 1-10."
- **Binary decision**: "Should we do X? Answer YES or NO, then give your top 3 reasons."
- **Scoring task**: "Score each option 1-10 on [criteria]. Output as `Option: Score`."

The schema must produce outputs that can be mechanically compared across agents.

### 3. Generate framing variations

Create N slightly different prompts. The core problem and output schema stay identical — only the framing/priming varies. This ensures stochastic diversity without changing the actual task.

Marketing-optimized variation strategies (cycle through these):
1. **Neutral baseline**: "Analyze the following marketing problem objectively."
2. **Risk-averse CMO**: "You are a conservative CMO who weighs downside risks and brand safety heavily."
3. **Growth hacker**: "You are an aggressive growth marketer who optimizes for speed and scale."
4. **Contrarian**: "Challenge conventional marketing wisdom. What does everyone else get wrong here?"
5. **First-principles**: "Reason from first principles. Ignore what's trendy or popular in marketing."
6. **Customer-empathy**: "Think from the end-customer perspective. What matters most to them?"
7. **Bootstrap/budget-constrained**: "Assume limited budget and no team. What's the highest-leverage move?"
8. **Long-term brand**: "Optimize for the 3-year brand outcome, not the 90-day metric."
9. **Data-driven**: "Focus only on what's measurable and provable. Ignore gut feeling."
10. **Systems thinker**: "Map the second and third-order effects. What cascades from each choice?"

For N > 10, cycle back through. For N < 10, pick the first N.

### 4. Spawn all N agents in parallel

Use the Agent tool to spawn all N agents simultaneously.

Config for each:
- `subagent_type: "general-purpose"`
- `model: "sonnet"` (cost-efficient — each agent does focused analysis, not deep research)

#### Agent prompt template

```
{framing_variation}

PROBLEM:
{problem}

{context — brand voice, ICP, offer, competitor data, any relevant background}

{output_schema}

Be specific and concrete. Give real recommendations, not vague advice. If you're uncertain about something, say so explicitly with a confidence level.

Write your response directly — do not write to any files.
```

**Important**: Agents return their output directly (not to files). This keeps aggregation simple.

### 5. Aggregate results

Once all N agents have returned, perform mechanical aggregation:

#### For ranking tasks:
- Assign points: 1st place = N points, 2nd = N-1, etc.
- Sum points across all agents for each option
- Report final ranking by total points

#### For recommendation tasks:
- Group similar recommendations (fuzzy match on name/concept)
- Count how many agents proposed each recommendation
- Categorize:
  - **Consensus** (7+/N agree): High-confidence recommendations
  - **Divergence** (4-6/N): Genuine judgment calls — flag for user decision
  - **Outlier** (1-3/N): High-variance ideas — potentially creative, potentially noise

#### For scoring tasks:
- Calculate mean, median, and standard deviation per option
- Flag options with high variance (std dev > 2) — agents disagree here

#### For binary decisions:
- Count YES vs NO
- Report the split and summarize the strongest arguments from each side

### 6. Write the aggregation report

Write to `active/consensus/consensus_report.md`:

```markdown
# Multi-Agent Consensus Report

**Problem**: {problem}
**Agents**: {N}
**Date**: {date}

## Consensus (agreed by {X}+/{N} agents)
{Items most agents converged on — these are your safe bets}

## Divergences (split {X}/{Y})
{Items where agents disagreed roughly evenly — these are genuine judgment calls that need human decision}

## Outliers (proposed by 1-{Z} agents)
{Unique ideas from individual agents — high variance, potentially high value. Flag which framing produced them.}

## Raw Rankings / Scores
{Full aggregation table}

## Individual Agent Responses
{Summary of each agent's response with their framing variation noted}
```

### 7. Deliver results

Present to the user:
- **One-paragraph summary** of the consensus finding
- **Top 3 consensus items** (what most agents agreed on)
- **Top divergence** (the most interesting split — where human judgment is needed)
- **Most interesting outlier** (the creative idea worth considering)
- File path to full report

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| N | 10 | Number of agents to spawn |
| model | sonnet | Model for each agent (sonnet for cost, opus for depth) |
| output | ranking | Output type: ranking, recommendation, score, binary |

User can override any of these: "poll 5 opus agents on..." or "score these options with 15 agents".

## Cost considerations

- 10 sonnet agents: ~$0.30-0.50 total for a focused analysis
- 10 opus agents: ~$3-5 total — only use when user explicitly requests opus
- Default to sonnet unless told otherwise
- For binary yes/no decisions, 5 agents is usually sufficient

## Edge cases

- **N < 3**: Warn the user that consensus requires at least 3 agents. Minimum 3.
- **Ambiguous problem**: Ask user to clarify before spawning. Don't burn N * tokens on vagueness.
- **All agents agree**: Great — high confidence. Report consensus and note the unanimity.
- **No consensus (even split)**: Report the split honestly. This IS the finding — the problem genuinely has no dominant answer.
- **Existing report**: Overwrite `active/consensus/` — these are ephemeral analysis artifacts.
- **Agent failure**: If an agent returns garbage or fails, exclude it from aggregation and note the effective N.
