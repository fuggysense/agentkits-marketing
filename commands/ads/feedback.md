---
description: Read DCT wave performance + route the next action to NEW (research refresh) / BETTER (concept refinement) / MORE (variant expansion). Closes the 6-stage creative pipeline loop.
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: <client-slug> <wave-number>
---

## Purpose

After a DCT wave concludes (typically 7-14 days post-launch with sufficient spend), this command reads the wave's performance data, applies routing thresholds, and outputs ONE of three next actions:

- **NEW** — back to Research (`/ads:source-of-truth <slug>` refresh) when the buyer has shifted
- **BETTER** — back to Brief/Hooks (`/ads:concepts <slug> --refine`) when winning angle is clear but execution needs work
- **MORE** — back to Create (`/ads:concepts <slug> --expand`) when winning combo is proven and ready to scale

This closes the 6-stage creative pipeline loop. Without this, waves don't compound — you launch wave 2 from the same Phase 1 thinking as wave 1.

## Input

`$ARGUMENTS` — `<client-slug> <wave-number>`

Examples:
- `/ads:feedback neezanizam 1` — route after Wave 1 of neezanizam concludes
- `/ads:feedback aura 3` — route after Wave 3 of aura concludes

## Prerequisites

Before running, ensure:
- [ ] Context Gate passed — session has WHO + WHAT PROJECT established
- [ ] `clients/<slug>/campaigns/dct-YYMMDD/dct-tracker.json` exists for the wave
- [ ] `clients/<slug>/metrics-config.json` exists with valid `sheet_id` + tab gids
- [ ] Sufficient spend has accumulated per wave (default ≥S$200/creative, ≥S$600/batch, ≥7 days, ≥5,000 impressions/creative — overridable in metrics-config.json)
- [ ] Performance table in dct-tracker.json populated (or sheet metric columns synced)
- [ ] Optional: `meta` CLI authed (`ACCESS_TOKEN=$META_ACCESS_TOKEN`) for live freshest numbers

## Workflow

This command activates the `feedback-router` skill. Full phase breakdown lives in `skills/feedback-router/SKILL.md`. Summary:

### Phase 0 — Context Gate
Verify all prerequisites above. If any fail, surface the gap, stop. Don't route on thin data.

### Phase 1 — Performance Read (parallel)
Read in parallel:
1. `clients/<slug>/campaigns/dct-YYMMDD/dct-tracker.json` Performance table
2. CREATIVES sheet tab metrics (via gid in metrics-config.json)
3. COPY sheet tab metrics (via gid)
4. Optional: live Meta Ads pull via the `meta` CLI (`meta ads insights get -o json`)

Aggregate by angle, creative_type (hook vs brief), format, headline pattern. Save to `clients/<slug>/campaigns/dct-YYMMDD/feedback-read.json`.

### Phase 2 — Route Decision
Apply thresholds from `skills/feedback-router/references/routing-criteria.md`. Pick ONE: NEW / BETTER / MORE.

Precedence rule when ambiguous: BETTER > MORE > NEW.

### Phase 3 — Learnings Capture (auto)
Auto-append wave-conclusion entry to:
- `clients/<slug>/learnings.md` (per Marketing CLAUDE.md self-annealing rule)
- `clients/<slug>/angles/iteration-log.md` (wave summary + winners + cuts)

Save raw decision artifact to `clients/<slug>/campaigns/dct-YYMMDD/feedback-decision.json`.

### Phase 4 — Hand-off
Print routing decision + recommended next slash command. User approves and runs the command.

**Critical rule:** this command does NOT auto-execute the routed next action. It outputs the recommendation. User runs the command if they agree. Keeps HITL at every loop boundary.

## Hand-off Message Format

```
✓ Wave [N] feedback decision: [NEW | BETTER | MORE]

WINNING ANGLE: [Angle name]
  CPA: S$[X] (vs target S$[Y], baseline S$[Z])
  CTR: [X]% · Hold-rate: [X]% · Frequency: [X] · Spend: S$[X]

UNDERPERFORMING:
  [Angle name]: CPA S$[X] (cut)
  [Angle name]: CPA S$[X] (warning, hold for now)

DIAGNOSIS: [1-2 sentences tied to specific metrics — what pattern was identified]

NEXT ACTION: [exact slash command]
  [1-2 sentences on scope: what stays locked, what gets varied]

Learnings auto-appended to:
  clients/<slug>/learnings.md
  clients/<slug>/angles/iteration-log.md
```

## Output files

- `clients/<slug>/campaigns/dct-YYMMDD/feedback-read.json` — aggregated performance read
- `clients/<slug>/campaigns/dct-YYMMDD/feedback-decision.json` — full routing decision artifact
- Append to `clients/<slug>/learnings.md`
- Append to `clients/<slug>/angles/iteration-log.md`

## Errors and edge cases

- **INSUFFICIENT_DATA** — pre-routing gate failed (spend, duration, impressions, or population missing). Surface the gap with exact threshold delta. Don't route.
- **AMBIGUOUS_WINNER** — no angle clearly outperforms within thresholds. Recommend extending the wave by 5-7 days OR splitting spend evenly for one more cycle before routing.
- **DATA_MISMATCH** — sheet metrics don't match dct-tracker.json (sync drift). Surface, ask user which to trust, log discrepancy in feedback-read.json.

## See also

- `skills/feedback-router/SKILL.md` — full skill spec
- `skills/feedback-router/references/routing-criteria.md` — exact thresholds per route
- `skills/feedback-router/references/learnings-template.md` — auto-append format
- `.claude/workflows/creative-pipeline.md` — 6-stage workflow this command closes
