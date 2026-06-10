## Graph Links
- **Parent skill:** [[claude-md-architect]]

# CLAUDE.md Update Guidelines

## Core Principle

Only add information that will genuinely help future sessions. The context window is precious — every line must earn its place.

## What TO Add

### 1. Skill/Agent Routing Discovered

```markdown
## Routing
- For video scripts → use `script-skill` (not `copywriting`)
- For TikTok content → use `tiktok-slideshows` (handles full lifecycle)
```

Why: 56% skill miss rate without explicit routing (Vercel benchmark).

### 2. Gotchas from Real Incidents

```markdown
## Gotchas
- Telegram bot state dir is RELATIVE to plugin dir, not ~/.claude/channels/ — check with `ps -p <PID> -E`
- faster-whisper auto-detect misidentifies SG English as Malay — always force language='en'
```

Why: Prevents repeating debugging sessions.

### 3. Context Load Order / Dependencies

```markdown
## Context
- Voice files load BEFORE project files (voice = person, project = business)
- context-profile.json must exist before any skill can run for a client
```

Why: Order matters — wrong sequence causes skills to miss context.

### 4. Session Protocols That Worked

```markdown
## Session End
0. /ops:claude-md (auto-capture learnings)
1. Log to skill learnings.md
2. Triage corrections.md
```

Why: Compounding loop — each session improves the next.

### 5. HITL Gates Learned from Experience

```markdown
## Gates
- Never publish to Postiz without approval — schedule only
- CRO changes need screenshot before/after
```

Why: Prevents irreversible actions.

## What NOT to Add

### 1. Skill/Agent Descriptions

Bad:
```markdown
The copywriting skill handles marketing page copy, headlines, and CTAs.
```

The routing table already has this. Duplication = bloat.

### 2. Generic Marketing Advice

Bad:
```markdown
Always test your headlines before publishing.
Use clear CTAs on landing pages.
```

This is universal knowledge, not project-specific.

### 3. One-Off Fixes

Bad:
```markdown
Fixed a typo in the AURA offer document on 2026-03-15.
```

Won't recur. Goes in git history, not CLAUDE.md.

### 4. Verbose Explanations

Bad:
```markdown
The V.O.I.C.E. system is a 5-file framework that captures the user's
personal writing voice. V stands for Voice (brand-voice.md), O stands
for Origin (about-me.md), I stands for...
```

Good:
```markdown
V.O.I.C.E.: brand-voice.md (V), about-me.md (O), working-style.md (I), compound-ideas.md (C), voice-examples.md (E)
```

### 5. Content That Belongs Elsewhere

| If the learning is about... | Put it in... | NOT in CLAUDE.md |
|---|---|---|
| A specific skill's behavior | `skills/<skill>/learnings.md` | |
| A one-off correction | `skills/<skill>/corrections.md` | |
| A specific client pattern | `clients/<project>/learnings.md` | |
| How Jerel likes to work | `USER.md` | |
| Communication style rules | `SOUL.md` | |
| Changelog entries | `docs/changelog.md` | |

## Diff Format for Proposed Updates

For each suggested change:

```markdown
### Update: ./CLAUDE.md

**Why:** Telegram state dir gotcha discovered — prevents future pairing debug sessions.

```diff
 ## Learnings

 ### Mistakes Not to Repeat
+- Telegram bot state dir is RELATIVE (.claude/telegram from plugin CWD), not ~/.claude/channels/. Always check `ps -p <PID> -E | grep TELEGRAM_STATE_DIR` first.
```
```

## Validation Checklist

Before finalizing an update, verify:

- [ ] Each addition is project-specific (not generic advice)
- [ ] No overlap with routing-table.md, skills-catalog.md, or commands.md
- [ ] File paths referenced actually exist
- [ ] Line count stays under 200 (ideal) / 300 (hard max)
- [ ] Every rule has a "because" (implicit or explicit)
- [ ] Would a new session find this helpful? (one-line test)
- [ ] Content is in the RIGHT file (not learnings.md or corrections.md material)
