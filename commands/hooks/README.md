---
description: How the /hooks:* command family works
version: "1.0.0"
brand: AgentKits Marketing by AityTech
---

# /hooks: command family

Three slash commands that all run on top of ONE underlying skill: **`script-skill`** (global, voice-locked).

| Command | Purpose | When to use |
|---|---|---|
| `/hooks:generate <concept>` | 20 voice-locked hooks for a concept, medium-depth output | Start of every batch |
| `/hooks:select` | Score those 20 hooks, pick top 2 with diversity check | After generation, before filming |
| `/hooks:analyze <hook>` | Deep-dive one hook + 7 rewrite variations | Optional — only when a chosen hook feels close but not quite |

## The architecture (one engine, three lenses)

```
                  ┌──────────────────────────────────┐
                  │       script-skill (engine)       │
                  │  ─ voice capture                  │
                  │  ─ hook database                  │
                  │  ─ 3-element framework            │
                  │  ─ de-AI / humanizer passes       │
                  └──────────────┬───────────────────┘
                                 │
       loaded with locked prompt config:
                                 │
        ┌────────────────────────┼─────────────────────────┐
        ▼                        ▼                         ▼
  /hooks:generate           /hooks:select            /hooks:analyze
  (20 hooks)                (top 2 of N)             (deep-dive 1 hook)
```

You don't need new skills for any of this. `script-skill` already covers the engine. The slash commands lock it into a specific workflow + output shape so the model can't drift.

## Deterministic inputs (loaded automatically per client)

All three commands load these from the active client folder (`clients/<client>/`):

**Required:**
- `brand-voice.md` — tone + patterns + constraints (covers the V.O.I.C.E. brand-voice file)
- `buyer-profile.md` — who we're talking to + their pain
- `icp.md` — identity / role / context
- `offer.md` — what we're selling + sales mechanism
- `channels.json` — channels + cadence + funnel structure
  - If `funnel-goal.json` (v0.5.2 plan format) also exists, it overrides `channels.json` for funnel split

**Optional but improves output:**
- `learnings.md` — past winners + hook-bank entries
- `story-bank.md` — proof material, case studies
- `voice/swipe-pools/<niche>/outlier-pool.jsonl` — competitor outliers

**Operator voice (only if your own writing style is part of the client work — usually skipped for client content):**
- `voice/jerel/brand-voice.md` etc. (V.O.I.C.E. files)

## Where this came from

Synthesized from 4 prompt drafts the operator pasted, mapped against the actual `clients/_template/` conventions in this repo. Cherry-picked deterministic inputs from Prompts A/B + selection criteria from Prompt C + fatal-mistake checklist from Prompt D. Voice-lock priority from the operator's v0.5.2 Michelle plan.

## To extend for a new client

1. `cp -R clients/_template clients/<new-client>` (or use a scaffolder)
2. Populate the 5 required files: `brand-voice.md`, `buyer-profile.md`, `icp.md`, `offer.md`, `channels.json`
3. Optional: drop a `learnings.md` if you already have hook-bank entries
4. Run `/hooks:generate <concept> --client <new-client>` (or cd into the client folder)
