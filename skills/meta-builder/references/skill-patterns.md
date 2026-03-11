# Skill Patterns

How to write skills for the AgentKits Marketing system.

## Anatomy of a Skill

A skill is a directory containing:

```
skill-name/
  SKILL.md          # Required — the skill definition
  scripts/          # Optional — executable code
  references/       # Optional — context docs loaded by Claude
  assets/           # Optional — files used in output (templates, images)
```

## SKILL.md Structure

### YAML Frontmatter

```yaml
---
name: skill-name
description: What this skill does and when to use it. Be specific about triggers — what user requests or scenarios activate this skill.
---
```

| Field | Required | Rules |
|-------|----------|-------|
| `name` | Yes | Hyphen-case, lowercase, max 64 chars, must match directory name |
| `description` | Yes | Max 1024 chars, no angle brackets, include trigger scenarios |

### Body

The body follows the skill's natural structure. Common patterns:

**Workflow-Based** (sequential processes):
```
## Overview → ## Workflow → ## Step 1 → ## Step 2...
```

**Task-Based** (tool collections):
```
## Overview → ## Quick Start → ## Task 1 → ## Task 2...
```

**Reference-Based** (standards/specs):
```
## Overview → ## Guidelines → ## Specifications...
```

**Capabilities-Based** (integrated features):
```
## Overview → ## Core Capabilities → ### 1. Feature...
```

Mix patterns as needed. Most skills combine workflow + task-based.

## Progressive Disclosure

Keep SKILL.md lean. It should be the entry point, not the encyclopedia.

**In SKILL.md:** Overview, workflow steps, quick reference, links to details
**In references/:** Deep documentation, API refs, comprehensive guides
**In scripts/:** Executable logic that Claude runs or reads for context
**In assets/:** Templates, images, fonts — files used in output

Rule of thumb: If a section in SKILL.md exceeds ~50 lines, extract it to `references/`.

## Registration

Every skill gets registered in `skills-registry.json`. Required fields:

```json
{
  "id": "skill-name",
  "name": "Skill Name",
  "path": "skills/skill-name",
  "category": "marketing|content|technical|analytics|meta",
  "version": "1.0.0",
  "difficulty": "beginner|intermediate|advanced",
  "description": "What it does",
  "triggers": ["keyword1", "keyword2"],
  "prerequisites": [],
  "relatedSkills": [],
  "agents": ["agent-name"],
  "mcpIntegrations": [],
  "successMetrics": ["metric1", "metric2"],
  "hasReferences": true
}
```

### Field Guide

| Field | Purpose |
|-------|---------|
| `id` | Matches directory name and SKILL.md `name` |
| `triggers` | Keywords/phrases that should activate this skill |
| `prerequisites` | Skills that must exist for this one to work |
| `relatedSkills` | Skills often used alongside this one |
| `agents` | Which agents can invoke this skill |
| `mcpIntegrations` | MCP servers this skill uses (e.g., Gmail, Firecrawl) |
| `successMetrics` | How to measure if the skill is working |
| `hasReferences` | Whether the skill has a `references/` directory |

## Quality Criteria

A good skill:

1. **Solves one problem well** — clear scope, no mission creep
2. **Has obvious triggers** — you can describe when to use it in one sentence
3. **Produces consistent output** — same input yields same-quality output
4. **Fails gracefully** — handles edge cases with helpful messages
5. **Includes validation** — run `quick_validate.py` before shipping
6. **Documents its resources** — every script and reference is listed in SKILL.md
