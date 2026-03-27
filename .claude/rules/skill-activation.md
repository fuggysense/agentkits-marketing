# Skill & Agent Activation Rule

**MANDATORY. NO EXCEPTIONS.**

Never freehand analysis from model training knowledge. Always activate the relevant repo skills AND/OR agents first.

## Process

1. When user requests any marketing task, identify which **skills** (`skills/`) and **agents** (`agents/`) from the repo are relevant
   - Check `skills-catalog.md` and `routing-table.md` for the best matches
   - Skills = specialized knowledge frameworks (invoked via `/skill`)
   - Agents = autonomous workers with specific expertise (invoked via Agent tool)
2. Present the recommended skills AND agents to the user with a brief "why" for each
3. Ask for confirmation BEFORE running any of them
4. Only after user confirms, activate in the right order:
   - Skills first (load the knowledge/framework)
   - Agents second (execute using that knowledge)
4.5. **Load corrections** — After activating a skill, read its `corrections.md` (if it exists and is non-empty). Apply these as hard constraints on the current task — they represent the user's explicit preferences from past sessions.
5. Never skip this step — even if you "know" the answer from training

## When to Use Skills vs Agents vs Both

| Scenario | Use |
|----------|-----|
| Need a framework/checklist/scoring rubric | Skill |
| Need autonomous execution or review | Agent |
| Need deep analysis with structured output | Both — skill loads the framework, agent applies it |
| Research or competitive intel | Agent (researcher, attraction-specialist) |
| Content creation or rewriting | Skill (copywriting, copy-editing) + Agent (copywriter) |
| Multi-perspective review | Multiple agents (solopreneur, startup-founder, brand-voice-guardian) |

## Why

The repo contains curated, battle-tested frameworks in `skills/` and domain-expert agents in `agents/` that produce more structured, repeatable output than freestyling from training data. The knowledge lives in the repo, not in the model's head.

`corrections.md` captures the user's real-time corrections from previous sessions. Loading before work begins means the skill "remembers" what was corrected last time. This is the compounding loop — each session's corrections make the next session's first draft better.
