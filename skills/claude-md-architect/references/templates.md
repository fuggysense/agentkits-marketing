## Graph Links
- **Parent skill:** [[claude-md-architect]]

# CLAUDE.md Templates

## Key Principles

- **Concise**: Dense, human-readable; one line per concept when possible
- **Actionable**: Commands copy-paste ready, paths real and verified
- **Project-specific**: Document patterns unique to THIS project, not generic marketing advice
- **Current**: All info reflects actual codebase state
- **Router-first**: Point to where depth lives, don't inline it

---

## Template: Marketing Agent Kit (Root)

For the main project CLAUDE.md — the one that every session loads.

```markdown
# [Project Name]

[One-line: what this is and who it serves]

## Role & Responsibilities

[What Claude does in this project — analyze, delegate, execute]

## Startup Files (read every session)

- `SOUL.md` — Communication tone, writing rules
- `USER.md` — Operator context (who, preferences, tools)
- `cron-registry.json` — Scheduled tasks to restore

## Workflows

- **Primary:** `./.claude/workflows/primary-workflow.md`
- [Other workflows as needed]

**CRITICAL — DATA RELIABILITY:** [One-line rule about never fabricating data]

**CRITICAL — CONTEXT GATE:** [How to identify WHO before any skill runs]

## Reference Files (read on demand)

- **Rules index:** `.claude/rules/_index.md` (load recipes + pointers)
- **Always-hot:** `.claude/rules/{skill-activation,mcp-integrations}.md`
- **Large refs:** `.claude/rules/details/{commands,routing-table,skills-catalog}.md` — fetch only when needed

## HITL Gates

### Requires Approval
- [List of actions needing human sign-off]

### Auto-Executes
- [List of safe autonomous actions]

## Session End Protocol

0. `/ops:claude-md` — auto-capture learnings
1. [Distributed learning steps]

## Learnings

### Confirmed Patterns
- [Pattern — because: reason]

### Mistakes Not to Repeat
- [Mistake — because: what happened]

### Open Threads
- [Unfinished work with context]
```

**Target: 150-200 lines.** Extract heavy sections to `.claude/rules/`.

---

## Template: Client Project CLAUDE.md

For `clients/<project>/CLAUDE.md` — overrides and additions specific to one client.

```markdown
# [Client Name]

[One-line: what this client does, target market]

## Context Files

- `context-profile.json` — Business identity (read FIRST)
- `icp.md` — Ideal customer profile
- `offer.md` — Core offer details
- `brand-voice.md` — Tone overrides (if different from voice/)
- `channels.json` — Active channels config
- `learnings.md` — What works for this client

## Active Campaigns

| Campaign | Phase | Next Action |
|----------|-------|-------------|
| [name] | [execution/optimization] | [what's next] |

## Client-Specific Rules

- [Override or addition — because: reason]

## Gotchas

- [Client-specific quirk — because: what happened]
```

**Target: 50-100 lines.** NEVER repeat root CLAUDE.md content.

---

## Template: Global CLAUDE.md

For `~/.claude/CLAUDE.md` — applies to ALL projects on this machine.

```markdown
# Global Instructions

## [Tool Strategy Section]
[Tool selection rules that apply everywhere]

## [Quality Rules]
[Anti-sycophancy, token optimization, etc.]

## [Automation Philosophy]
[When to automate vs manual, 10x bar]
```

**Target: 100-150 lines.** Only universal preferences, never project-specific.

---

## Template: Nested/Subdirectory CLAUDE.md

For folders with different conventions (e.g., `scripts/`, `skills/`).

```markdown
# [Folder Name]

[One-line purpose of this directory]

## Conventions

- [Convention unique to this folder — because: reason]

## Key Files

- `[file]` — [purpose, not obvious from name]

## Gotchas

- [Non-obvious thing — because: what happened]
```

**Target: 30-50 lines max.** Two rules: (1) NEVER repeat root content. (2) NEVER describe what's discoverable.

---

## Anti-Patterns (Never Do This)

### 1. Directory Listings
```markdown
## Bad
skills/
  copywriting/
  seo-mastery/
  ...
```
Claude finds files faster on its own. Directory listings waste 14-22% extra reasoning tokens.

### 2. Skill/Agent Descriptions
```markdown
## Bad
The copywriting skill handles marketing page copy, headlines, and CTAs.
```
This is in `routing-table.md` and `skills-catalog.md`. Don't duplicate.

### 3. Generic Advice
```markdown
## Bad
Always A/B test your headlines before launching.
```
Universal knowledge. Not project-specific.

### 4. Auto-Generated Content
ETH Zurich (Feb 2026): Auto-generated CLAUDE.md files reduce success rate 0.5-3% and increase cost 20%+. NEVER use `claude init` or auto-generate without interview.
