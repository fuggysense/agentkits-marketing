---
description: Guided new client/project onboarding — Path A (research-first) or Path B (interview-first), Jake marketing folder + Option B discovery indexes
version: "3.1.0"
brand: AgentKits Marketing by AityTech
argument-hint: [project-slug]
---

## Prerequisites

- `clients/_template/` exists with Jake marketing structure and Option B discovery templates (see `skills/client-onboarding/SKILL.md` v3.1)
- `scripts/scaffold-client.sh` exists and is executable
- `skills/client-onboarding/SKILL.md` v3.1 available
- `skills/business-profile/SKILL.md` v2.0+ available (Path B backend)

---

## Context Loading

1. Load `skills/client-onboarding/SKILL.md` — the orchestrator (v3.1)
2. Discovery questions: `skills/client-onboarding/references/discovery-questions.md` (Path B only, on demand)

---

## Workflow

### Step 0: Get project slug

If provided as argument, use it. Otherwise ask:
**"What's the client slug? (lowercase, hyphens, no spaces — e.g. `michelle-koh`)"**

Validate: lowercase, hyphens only, no spaces.

Also ask for display name: **"Display name? (e.g. `Michelle Koh`)"**

### Step 1: Check for conflicts

If `clients/<slug>/` already exists:
- If `context-profile.json` shows incomplete onboarding → offer to **resume**
- If fully populated → offer to **update profile** instead (route to `/project:profile`)
- Otherwise → ask: overwrite or pick different slug?

### Step 2: Scaffold

```bash
./scripts/scaffold-client.sh <slug> "<Name>"
```

This copies `clients/_template/` → `clients/<slug>/` and swaps `{{placeholders}}` in `.md`, `.json`, and `.jsonl` scaffold files. The new client folder gets whatever the template currently defines, including the Jake marketing structure (`_brand/`, `_config/`, `_references/`, `_swipe/`, `01_research/` through `05_handoff/`, `campaigns/`, `videos/`, `CLAUDE.md`, `CONTEXT.md`, `context-profile.json`) plus Option B discovery scaffolds:

- `campaigns/_campaigns-index.json` — client-level campaign registry
- `campaigns/README.md` — campaign workspace rules
- `_templates/video-concept-workspace/` — reusable concept-workspace scaffold containing `pipeline-state.json`, `artifact-manifest.json`, and `event-log.jsonl`

Per-campaign `campaign-index.json` files are created by `/campaign:new`, not `/project:new`, because the campaign slug does not exist during client onboarding.

### Step 3: Path selection

Ask: **"Does this client have a public footprint we can scrape (LinkedIn / Instagram / website), or starting from cold?"**

- Public footprint → **Path A** (Research-first)
- Cold / paid formal intake → **Path B** (Interview-first)
- Both → **Hybrid** (A first, B for missing fields)

### Step 4: Execute path

Hand off to `client-onboarding` SKILL.md — it owns the path-specific logic (scrapers + synthesizer for Path A, `business-profile` skill delegation for Path B).

### Step 5: Optional enrichment

After path completes, offer Phase 3 enrichment agents (persona-builder, researcher, brand-voice-guardian, story-bank). User picks zero or more.

### Step 6: Validate

Run Phase 4 readiness check. Show score + gaps.

### Step 7: Activate

Set project as active session context. Suggest first move based on path:
- Path A: paste `output/deliverables/brainstorm-agent-prompt.md` into Claude Project
- Path B: run `/campaign:new` or `/brand:voice`

---

## Output Location

`clients/<slug>/` — Jake-style structure (see `skills/client-onboarding/SKILL.md` "Output Locations" table)

---

## Quit / Resume

User can quit at any step. State is saved in `clients/<slug>/context-profile.json` → `_onboarding_progress`. Re-running `/project:new <slug>` resumes at first incomplete step.

---

## Migration note

v2.x flat structure is deprecated — forward-only. Existing clients (neezanizam, fuggysmedia, etc.) stay on old structure. New clients use Jake-style. See `skills/client-onboarding/SKILL.md` "Migration notes" for details.
