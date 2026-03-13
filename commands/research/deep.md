---
description: "Launch multi-agent deep research on any topic (MECE decomposition, parallel agents, gap analysis)"
argument-hint: "[topic to research]"
---

# Deep Research

Activate the `deep-research` skill from `skills/deep-research/SKILL.md`.

## Workflow

1. Read `skills/deep-research/SKILL.md` for the full orchestration process
2. Follow Phase 1-5 exactly as documented
3. Get today's date: `date +%Y-%m-%d`
4. If user provided a topic via argument, use that. Otherwise ask.
5. Clarify purpose and preferred sources
6. Decompose into 3-6 MECE angles
7. Spawn parallel sub-agents (Agent tool, subagent_type: "researcher" or "general-purpose")
8. Run gap analysis on all results
9. Synthesize into single document
10. Save to `docs/research/[topic]-[date].md`

## Context Gate

Check if a project context is needed. Pure research tasks may skip the context gate per CLAUDE.md rules.

## Arguments

If the user passed `$ARGUMENTS`, treat it as the research topic and proceed directly to Phase 1.
