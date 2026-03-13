---
description: Run readiness check on an existing project's configuration files
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [project-name]
---

## Prerequisites

- Project must exist in `clients/<project>/`

---

## Context Loading

1. Load client-onboarding skill: `skills/client-onboarding/SKILL.md`

---

## Workflow

### Step 1: Identify Project

If provided as argument, use it. Otherwise list available projects from `clients/` (exclude `_template/`) and ask user to pick.

### Step 2: Read Project Files

Read all 4 files:
- `clients/<project>/icp.md`
- `clients/<project>/offer.md`
- `clients/<project>/brand-voice.md`
- `clients/<project>/channels.json`

### Step 3: Run Readiness Checklist

Score each section per Phase 4 of the client-onboarding skill:

**ICP (icp.md):**
- [ ] Demographics: Industry + Company Size filled
- [ ] Psychographics: at least 2 specific pain points
- [ ] Where They Congregate: at least 1 entry

**Offer (offer.md):**
- [ ] Price or pricing model listed
- [ ] One-Line Description filled
- [ ] At least 1 proof element
- [ ] Primary benefit stated

**Brand Voice (brand-voice.md):**
- [ ] At least 2 messaging pillars or tone adjustments
- [ ] At least 1 on-brand example

**Channels (channels.json):**
- [ ] At least 1 primary channel listed

**Voice Profile:**
- [ ] Voice directory exists in `voice/`

### Step 4: Output Report

```
Readiness: X/Y checks passing

✅ Passing:
- [list passing checks]

❌ Missing:
- [list failing checks with specific gaps]

📋 Next actions:
- [what to fill to reach 100%]
```

### Step 5: Offer to Fix

If gaps exist, ask: "Want to fill in the missing sections now?" and walk through just the incomplete parts using discovery questions from `skills/client-onboarding/references/discovery-questions.md`.
