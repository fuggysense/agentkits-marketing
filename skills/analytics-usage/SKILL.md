---
name: analytics-usage
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: operations
difficulty: beginner
description: Track and analyze which skills and agents you use most. Find your 80/20 — which 20% of tools drive 80% of your results. Global tracking across all clients/projects.
triggers:
  - usage analytics
  - skill usage
  - agent usage
  - what do I use most
  - pareto
  - 80/20
prerequisites: []
related_skills:
  - analytics-attribution
agents: []
mcp_integrations: {}
---

## Graph Links
- **Feeds into:** (meta-skill -- tracks usage)
- **Draws from:** (all skills -- data source)
- **Used by agents:** (system-level)
- **Related:** [[knowledge-hygiene]]

# Usage Analytics

Track every skill and agent invocation automatically. Find your 80/20.

## How It Works

A global PostToolUse hook (`~/.claude/analytics/track.sh`) fires on every tool call and logs:

| What | How |
|------|-----|
| **Skill invocations** | Captured when you use any `/skill` slash command |
| **Agent delegations** | Captured when any Agent tool is spawned |
| **Files created/edited** | Proxy metric for output volume |
| **Git commits** | Proxy metric for shipped work |
| **Client context** | Auto-detected from `clients/` folder paths |

Data stored in: `~/.claude/analytics/usage.db` (SQLite)

## Commands

Run reports by asking Claude or using these directly:

```
/analytics:usage                  # Overview dashboard
/analytics:usage pareto           # 80/20 analysis
/analytics:usage clients          # Usage by client
/analytics:usage trend            # Weekly/daily trends
/analytics:usage unused           # Skills & agents never used
/analytics:usage productivity     # Output proxy metrics
/analytics:usage raw              # Last 50 raw events
```

### Period Filters

Add a time period after any mode:

```
/analytics:usage pareto 30d       # Last 30 days
/analytics:usage trend 7d         # Last 7 days
/analytics:usage clients 90d      # Last 90 days
```

Periods: `all` (default), `7d`, `30d`, `90d`

## Execution

When the user asks for usage analytics:

1. Parse the requested mode and period from their message
2. Run the report script: `~/.claude/analytics/report.sh [mode] [period]`
3. Present the results clearly
4. If they ask for pareto/80-20, highlight the vital few and suggest dropping or consolidating the trivial many
5. If they ask what's unused, suggest trying or removing unused skills/agents

## Interpretation Guide

- **High usage + high output (files/commits)** = your power tools
- **High usage + low output** = might be over-relying on research/planning without shipping
- **Low usage + high output** = efficient tools — use them more
- **Never used** = candidates for removal or intentional trial
