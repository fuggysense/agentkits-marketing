---
description: Guided new client/project onboarding — scaffold, interview, enrich, validate, activate
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [project-name]
---

## Prerequisites

- `clients/_template/` must exist with icp.md, offer.md, brand-voice.md, channels.json

---

## Context Loading

1. Load client-onboarding skill: `skills/client-onboarding/SKILL.md`
2. Load discovery questions: `skills/client-onboarding/references/discovery-questions.md`

---

## Workflow

### Step 0: Get Project Name

If provided as argument, use it. Otherwise ask:
**"What's the project name? Use slug format (lowercase, hyphens). Example: `acme-plumbing`"**

Validate: lowercase, hyphens only, no spaces.

### Step 1: Check for Conflicts

If `clients/<project-name>/` already exists, warn and ask: overwrite or pick different name.

### Step 2: Scaffold

```bash
cp -r "clients/_template/" "clients/<project-name>/"
mkdir -p "clients/<project-name>/campaigns"
mkdir -p "clients/<project-name>/feedback"
```

Check `voice/` for existing voice profiles (exclude README.md). Report what's found.

### Step 3: Discovery Interview

Follow the interview flow from the skill's Phase 2. Ask questions from `references/discovery-questions.md` in this order:
1. **ICP** → write to `clients/<project>/icp.md`
2. **Offer** → write to `clients/<project>/offer.md`
3. **Brand Voice** → write to `clients/<project>/brand-voice.md`
4. **Channels** → write to `clients/<project>/channels.json`

Ask one section at a time. Accept "skip" to leave defaults.

### Step 4: Offer Enrichment

Present optional agent routing (Phase 3 from skill):
- Deep buyer persona → `persona-builder` agent
- Competitor research → `researcher` agent
- Voice profile → `/brand:voice` skill
- Brand validation → `brand-voice-guardian` agent
- Skip → move to validation

### Step 5: Validate

Run Phase 4 readiness checklist. Output score and gaps.

### Step 6: Activate

Set project as active session context. Load voice + project layers. Suggest first campaign type based on channels + offer.

---

## Output Location

Project created at: `clients/<project-name>/`
