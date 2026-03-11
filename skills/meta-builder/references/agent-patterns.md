# Agent Patterns

How to write agent `.md` files for the AgentKits Marketing system.

## File Structure

An agent is a single `.md` file with YAML frontmatter and a structured body.

## YAML Frontmatter

```yaml
---
name: agent-name
version: "1.0.0"
brand: "AgentKits Marketing by AityTech"
description: |
  One-line summary of the agent's role.

  <examples>
  <example>
  <user>Example user request</user>
  <response>How the agent would respond (brief)</response>
  </example>
  <example>
  <user>Another example request</user>
  <response>Another example response</response>
  </example>
  </examples>
model: sonnet
---
```

### Frontmatter Fields

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Hyphen-case identifier |
| `version` | Yes | Semver, start at `"1.0.0"` |
| `brand` | Yes | Always `"AgentKits Marketing by AityTech"` |
| `description` | Yes | Summary + XML examples showing input/output pairs |
| `model` | Yes | `haiku` (fast/cheap), `sonnet` (balanced), `opus` (complex reasoning) |

### Model Selection Guide

- **haiku**: Simple routing, classification, formatting tasks
- **sonnet**: Most agents — writing, analysis, strategy, general knowledge work
- **opus**: Complex multi-step reasoning, nuanced judgment, creative direction

## Body Sections

Every agent `.md` body follows this section order. Not all sections are required for every agent, but this is the canonical structure.

### 1. Language Directive

Set the communication style. Be specific.

```markdown
## Language Directive

Write in a direct, professional tone. Use short sentences. Avoid jargon unless the user uses it first. Default to American English.
```

### 2. Context Loading

Define what context the agent needs and how to gather it.

```markdown
## Context Loading

Before responding, load:
1. The user's project context from CLAUDE.md
2. Any referenced files or URLs
3. Previous conversation context if continuing a thread
```

### 3. Reasoning Process

How the agent should think through problems.

```markdown
## Reasoning Process

1. Identify the core request
2. Determine if this requires delegation to a skill or sub-agent
3. Plan the response structure before writing
4. Validate output against quality checklist before delivering
```

### 4. Skill Integration

Which skills this agent can invoke and when.

```markdown
## Skill Integration

- **seo-audit**: Invoke when user asks about search performance or optimization
- **content-writer**: Delegate long-form content creation
- **brand-voice**: Always check brand consistency before publishing
```

### 5. Role Responsibilities

What this agent owns and what it delegates.

```markdown
## Role Responsibilities

**Owns:**
- Marketing strategy recommendations
- Campaign planning and calendar management

**Delegates:**
- Content creation → content-writer skill
- Technical SEO → seo-audit skill
```

### 6. Core Capabilities

Numbered list of what the agent can do.

```markdown
## Core Capabilities

1. **Campaign Strategy** — Plan multi-channel marketing campaigns
2. **Performance Analysis** — Interpret analytics and recommend adjustments
3. **Competitive Research** — Analyze competitor positioning and messaging
```

### 7. Process

Step-by-step workflow the agent follows.

```markdown
## Process

1. Receive and clarify the request
2. Gather necessary context
3. Execute or delegate
4. Present results with reasoning
5. Ask for feedback
```

### 8. Output Formats

Define how the agent structures its responses.

```markdown
## Output Formats

- **Strategy docs**: Use H2 headers, bullet points, and a summary table
- **Quick answers**: 1-3 sentences, no formatting
- **Reports**: Executive summary → Findings → Recommendations
```

### 9. Tool Usage Guidelines

Rules for when and how the agent uses tools.

```markdown
## Tool Usage Guidelines

- Always use WebFetch before Firecrawl for URL retrieval
- Read files before editing them
- Use Grep for searching, not bash grep
```

### 10. Quality Checklist

Self-check before delivering output.

```markdown
## Quality Checklist

Before delivering any response, verify:
- [ ] Directly answers the user's question
- [ ] Consistent with brand voice
- [ ] Actionable — user knows what to do next
- [ ] No hallucinated data or URLs
- [ ] Appropriate length for the request
```

### 11. Edge Cases

How to handle unusual situations.

```markdown
## Edge Cases

- **Ambiguous request**: Ask one clarifying question, then proceed with best interpretation
- **Out of scope**: State what you can't do and suggest who/what can
- **Conflicting instructions**: Follow the most specific instruction; flag the conflict
```

## Best Practices

1. **Be specific over generic** — "Write in AP style" beats "Write well"
2. **Show, don't tell** — XML examples in frontmatter are worth more than paragraphs of description
3. **Limit scope** — An agent that does 3 things well beats one that does 10 things poorly
4. **Wire in feedback** — Every agent should ask "Did this help? What should I adjust?"
5. **Version intentionally** — Bump minor for behavior changes, major for role changes
