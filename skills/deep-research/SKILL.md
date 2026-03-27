---
name: deep-research
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: research
difficulty: intermediate
description: >
  Multi-agent parallel research orchestrator. Decomposes any research topic into 3-6 specialized
  angles using MECE principles, spawns sub-agents to cover each angle simultaneously, runs gap
  analysis, then synthesizes findings into one comprehensive document. 90.2% better results than
  single-agent research (Anthropic eval).
triggers:
  - deep research
  - thorough research
  - research everything about
  - cover every angle
  - comprehensive research
  - spawn research agents
  - find everything about
  - research doc
  - exhaustive research
  - multi-agent research
prerequisites: []
related_skills:
  - marketing-fundamentals
  - competitor-alternatives
  - content-strategy
  - analytics-attribution
  - content-moat
agents:
  - researcher
  - brainstormer
  - planner
---

## Graph Links
- **Feeds into:** [[content-moat]], [[competitor-alternatives]]
- **Draws from:** (independent — research engine)
- **Used by agents:** [[researcher]]
- **Related:** [[content-strategy]]

# Deep Research Skill

Multi-agent parallel research orchestrator. Decomposes any research topic into 3-6 specialized angles using MECE principles, spawns sub-agents to cover each angle simultaneously, runs gap analysis, then synthesizes findings into one comprehensive document.

Anthropic's own multi-agent research system outperforms single-agent by **90.2%**. Same model, same tools — the only difference is how you split the work. Each agent gets the full context window for its specific angle instead of sharing one window across everything.

## Language & Quality Standards

**CRITICAL**: Respond in the same language the user is using.

## When to Use This Skill

- User asks for "deep research", "thorough research", "research everything about"
- User wants comprehensive coverage of a topic (not a quick lookup)
- User needs a research document for strategic decisions
- Competitor deep dives, market analysis, technology evaluation
- Any task requiring 3+ web searches across different angles

**NOT for:** Quick lookups, single questions, fact checks. Use `researcher` agent directly for those.

## How It Works

```
         [Broad: Decompose question]
              /        \
    [Narrow: 3-6 parallel agents]     ← Wave 1
              \        /
         [Evaluate: Gap analysis]
              /        \
    [Deep: 1-2 targeted agents]       ← Wave 2 (if needed)
              \        /
         [Synthesize: Final report]
```

Start wide, go narrow in parallel, identify gaps, go deep on gaps, synthesize.

## Research Orchestration Process

### Phase 1: Gather Context

Before spawning any agents:

1. **Note today's date** — run `date` if unsure. Inject this into every sub-agent prompt so they search for current information. Without date context, agents search for and cite outdated information.
2. **Clarify purpose** if unclear — ask "What will you use this research for?" The answer shapes everything.
3. **Ask about sources** — ask the user:
   - "Are there specific sources you want me to prioritize?"
   - Options: specific people/accounts, specific sites/communities, URLs to anchor around, or "no, use defaults"
   - This separates surface-level research from genuinely useful findings. Default web search scrapes the obvious. User-directed sources find the stuff nobody else is writing about.

### Phase 2: MECE Decomposition

Break the topic into **Mutually Exclusive, Collectively Exhaustive** angles. Each angle:
- Does NOT overlap with any other (prevents duplicate work)
- Together they cover everything relevant (no gaps)
- Is specific enough for one agent to investigate thoroughly

**Common decomposition patterns:**

| Research Type | Typical Angles |
|--------------|----------------|
| Market/Competitor | Market size + trends, Competitor landscape, Customer pain points, Pricing + business models |
| Content/Platform | General best practices, Niche-specific strategies, Real examples with metrics, Psychology/copywriting principles |
| Technology | Current state/ecosystem, Real code patterns (GitHub), Community sentiment, Comparisons/alternatives |
| Business Strategy | Market data/benchmarks, Practitioner strategies, Competitive landscape, Community discourse |

**Scale effort to complexity:**
- Simple factual topic: 3 agents
- Multi-faceted topic: 4-5 agents
- Complex strategic topic: 5-6 agents (hard cap — more agents = more overlap)

### Phase 3: Spawn Parallel Sub-Agents

Spawn sub-agents in parallel using the Agent tool. Every sub-agent prompt MUST include these 6 elements:

1. **WHO** — who the research is for and what they do
2. **WHY** — the specific purpose
3. **WHAT ANGLE** — specific scope AND explicit boundaries: "Cover X. Do NOT cover Y — another agent handles that."
4. **HOW** — which tools to use (WebSearch, WebFetch, etc.)
5. **SEARCH STRATEGY** — "Start with SHORT, BROAD queries (2-4 words). Evaluate results. Then progressively narrow focus."
6. **SOURCE QUALITY** — "Prefer: practitioner blogs, official docs, academic papers, primary sources. Avoid: SEO content farms, listicles, aggregator sites."

#### Sub-Agent Prompt Template

```
You are researching [ANGLE] for [USER CONTEXT — who they are and what they do].

TODAY'S DATE: [INSERT CURRENT DATE]

PURPOSE: [WHY this research matters — what the user will do with it]

YOUR ANGLE: [SPECIFIC SCOPE — what you cover]
BOUNDARIES: [What you do NOT cover — other agents handle those angles]

SEARCH STRATEGY:
- Start with short, broad queries (2-4 words)
- Evaluate what's available, then progressively narrow
- Cross-reference claims across multiple sources
- Aim for 2+ independent sources per key finding

SOURCE QUALITY: Prefer practitioner blogs, official docs, engineering posts, primary
sources. Avoid SEO content farms and listicles.

TOOLS TO USE: [SPECIFIC tools for this angle]
- Use `scripts/linkup.sh search "query" --output sourcedAnswer --citations` for queries needing sourced answers
- Use `scripts/linkup.sh search "query" --include-domains "domain1.com,domain2.com"` when user specified priority sources
- Use `scripts/linkup.sh search "query" --from YYYY-MM-DD --to YYYY-MM-DD` for time-bounded research
- Use WebSearch for broad general queries — run both in parallel for best coverage

QUALITY BAR: Be exhaustive. Extract every actionable insight, specific number, concrete
example, framework, and contrarian take. Density matters — thin research is useless.
Include sources/URLs for everything. If you find only 3 bullet points, you failed.

OUTPUT FORMAT:
## Key Findings
[Numbered list with inline source citations]

## Evidence Quality
[Which findings are well-sourced vs. speculative]

## Contradictions Found
[Any conflicting information between sources]

## Notable Quotes
[Direct quotes from authoritative sources with attribution]

## Sources
[Full list with URLs]
```

### Phase 3.5: Async Deep Research (Optional)

For "deep" depth requests or complex strategic topics, sub-agents can fire off Linkup async research in parallel with their own work:

1. Start async task: `scripts/linkup.sh research "specific research question" --citations`
2. Capture the returned task ID
3. Continue normal WebSearch + Linkup search work
4. Before finishing, poll: `scripts/linkup.sh research-status <task-id>`
5. If results are ready, merge findings into output; if still processing, note the task ID for the orchestrator to poll during gap analysis

This is optional — only use when the topic warrants deep async research AND the sub-agent has other work to do while waiting.

### Phase 4: Gap Analysis

After ALL sub-agents return — process them as a batch, not one at a time:

1. Review all findings together
2. Check: does each MECE angle have 2+ independent sources?
3. Identify contradictions between agent findings
4. Identify coverage gaps — topics no agent covered adequately
5. **If significant gaps exist**: spawn 1-2 targeted follow-up agents (Wave 2)

### Phase 5: Synthesize Into Document

Cross-reference all findings and produce ONE comprehensive document. Do NOT simply concatenate agent outputs — synthesize them.

**Document structure:**

```markdown
# [Topic Name]

Research compiled [date]. [N] parallel research tracks synthesized.

**Purpose**: [What this research will be used for]
**Sources**: [N] web sources, [N] code examples, etc.

---

## Executive Summary
[3-5 bullet points — the most important findings]

---

## Part 1: [Angle Name]
### [Sub-topic]
[Dense, actionable content with specific numbers and examples]

---

## Contradictions & Open Questions
[Where sources disagreed, what remains unresolved]

---

## Key Takeaways
[Numbered list of the most actionable insights]

---

## Sources
[All sources cited, organized by section]
```

**Quality gate — do NOT save until ALL pass:**
- Specific numbers present, not just generalities
- Concrete examples from real companies/creators included
- Sources attributed throughout
- Contradictions flagged (not hidden)
- The user would learn something genuinely new

## Output Location

Save research documents to: `./docs/research/[topic-slug]-[YYYY-MM-DD].md`

## External LLM Synthesis (Token-Saving Option)

The biggest token cost in deep research isn't the searching — it's the **synthesis**. Each sub-agent processes 10+ pages of raw search results into structured findings. That processing can be offloaded to cheaper models.

### How It Works

Sub-agents still use WebSearch/Linkup for the actual searching (gathering). But the synthesis step — reading raw results and producing structured findings — gets piped to `scripts/research-llm.sh`:

```
Sub-agent workflow:
1. WebSearch / Linkup  →  raw results (gathering)
2. research-llm.sh     →  structured summary (synthesis)  ← token savings here
3. Return summary to orchestrator (Claude)
```

### Sub-Agent Synthesis Command

After gathering raw search results, sub-agents can run:

```bash
# Pipe raw findings to cheap LLM for synthesis
scripts/research-llm.sh auto "Synthesize these raw search findings into structured research output.

RAW FINDINGS:
[paste raw search results here]

OUTPUT FORMAT:
## Key Findings
[Numbered list with inline source citations]
## Evidence Quality
[Which findings are well-sourced vs. speculative]
## Sources
[Full list with URLs]"
```

The script returns JSON with a `result` field containing the structured synthesis. The sub-agent passes this back to the orchestrator.

### When to Use

- **Use external LLM:** When research has 3+ sub-agents each processing many search results (biggest savings)
- **Stay on Claude:** When synthesis requires nuanced judgment, creative connection-making, or the topic is highly specialized
- **HITL gate:** Ask the user which research backend to use before spawning sub-agents

### Available Models

| Provider | Model | Best For |
|----------|-------|----------|
| Kilo Gateway | `minimax/minimax-m2.5` (default) | General research synthesis, cheapest |
| Kilo Gateway | `nvidia/nemotron-3-super` | More complex synthesis, still cheap |
| Gemini CLI | `gemini-2.5-flash` | Fallback, good general quality |
| Auto | tries Kilo → Gemini | Set-and-forget |

---

## The 5 Pitfalls That Kill Research Quality

1. **Duplicate work** — without explicit "do NOT cover X" boundaries, agents overlap. MECE decomposition prevents this.
2. **Overly-specific search queries** — agents default to long queries. Explicitly prompt "start broad (2-4 words), then narrow."
3. **SEO content farm results** — add source quality heuristics to every prompt.
4. **Anchoring bias** — if you read Agent 1's findings before Agent 2 returns, you'll filter through Agent 1's frame. Batch ALL results.
5. **"Good enough" stopping** — require 2+ sources per finding. One source is an opinion. Two sources is a pattern.

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| Multi-agent vs single-agent quality | +90.2% | Anthropic internal eval |
| Research time reduction (parallel) | Up to 90% | Anthropic engineering blog |
| Token usage vs single-turn chat | ~15x more | Anthropic engineering blog |
| Optimal sub-agent count | 3-5 parallel | Anthropic + OpenAI convergence |

## Related Commands

- `/research:market` — Market research (uses this skill for deep mode)
- `/research:persona` — Buyer persona research
- `/research:trend` — Industry trend analysis
- `/competitor:deep` — Deep competitor analysis
