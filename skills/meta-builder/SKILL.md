---
name: meta-builder
description: Creates new agents and skills with built-in feedback loops. Use this when you need to scaffold a new agent persona, build a repeatable skill workflow, or evolve existing agents/skills through self-annealing iteration.
---

# Meta Builder

## Overview

Meta Builder is a skill that creates other agents and skills. It walks through clarification, decides the right artifact type, scaffolds it from templates, wires in feedback loops, and registers the result. Every created artifact ships with self-annealing capabilities so it improves through use.

## Decision Logic: Agent vs Skill

Use these criteria to decide what to build:

### Build an AGENT when:
- The artifact needs a **role or persona** (e.g., "Marketing Strategist", "Code Reviewer")
- It requires **model routing** (choosing between haiku/sonnet/opus based on task complexity)
- It **delegates work** to other agents or invokes skills
- It needs **persistent context** about who it is and how it behaves across conversations

### Build a SKILL when:
- The artifact is a **repeatable workflow** (e.g., "create a blog post", "audit SEO")
- It benefits from **bundled scripts, references, or assets**
- It encapsulates **domain-specific knowledge** that any agent could use
- It has clear **inputs and outputs** with defined quality criteria

**When in doubt:** If it has a personality, it's an agent. If it has a procedure, it's a skill.

## Workflow

### 1. CLARIFY

Ask questions until you are 95% clear on:

- **Problem**: What specific problem does this solve?
- **User**: Who will use it and in what context?
- **Type**: Agent or skill (use decision logic above)?
- **Inputs/Outputs**: What goes in, what comes out?
- **HITL Gates**: Where must a human approve before proceeding?
- **Success Metrics**: How do we know it's working?

Do not proceed until clarity threshold is met. Ask focused, specific questions — not open-ended brainstorming.

### 2. DECIDE

Apply the decision logic above. State the decision and the primary reason. Example:

> "This is a **skill** because it's a repeatable SEO audit workflow with clear inputs (URL) and outputs (report). No persona needed."

### 3. BUILD

**For an Agent:**
1. Run `scripts/init_agent.py <name> --path <target-path>`
2. Fill in the generated template using `references/agent-patterns.md`
3. Define model routing, skill integrations, and quality checklist

**For a Skill:**
1. Run `scripts/init_skill.py <name> --path <target-path>`
2. Fill in the generated template using `references/skill-patterns.md`
3. Add scripts, references, and assets as needed
4. Validate with `scripts/quick_validate.py <skill-path>`

### 4. FEEDBACK LOOP

Every created artifact gets a feedback loop. See `references/feedback-loops.md` for full patterns.

1. **Self-Annealing**: Include error-handling directives that update behavior on failure
2. **Performance Tracking**: Add a "What worked / What didn't" section to outputs
3. **HITL Gate**: Present the artifact to the human for approval before finalizing
4. **Iteration Prompt**: End with "Use this, then tell me what to improve"

### 5. REGISTER

- **Skills**: Run `scripts/register.py skill <name> --description "<desc>"` to add to `skills-registry.json`
- **Agents**: Run `scripts/register.py agent <name> --description "<desc>"` to get routing table instructions

## Resources

### scripts/
- `init_agent.py` — Scaffold a new agent .md file
- `init_skill.py` — Scaffold a new skill directory
- `register.py` — Register a skill or agent
- `quick_validate.py` — Validate skill structure
- `package_skill.py` — Package a skill for distribution

### references/
- `agent-patterns.md` — How to write agent .md files
- `skill-patterns.md` — How to write skills
- `feedback-loops.md` — How to build feedback loops
- `output-patterns.md` — Output formatting patterns
- `workflows.md` — Workflow design patterns

### templates/
- `agent-template.md` — Blank agent template
- `skill-template/SKILL.md` — Blank skill template
