---
name: feedback-router
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: paid-media
difficulty: advanced
description: "Closes creative pipeline after DCT wave. Reads performance data, routes to NEW (research refresh), BETTER (angle refinement), or MORE (scale variants). Auto-appends learnings. Triggers: feedback router, wave feedback, dct feedback, performance routing, new better more, /ads:feedback. Requires: meta-ads, source-of-truth, ad-concept-engine."
triggers:
  - feedback router
  - wave feedback
  - dct feedback
  - performance routing
  - new better more
  - "/ads:feedback"
prerequisites:
  - ad-concept-engine
  - source-of-truth
related_skills:
  - source-of-truth
  - ad-concept-engine
  - avatar-research
  - paid-media-audit
  - meta-ads-uploader
  - analytics-attribution
agents:
  - researcher
  - tracking-specialist
mcp_integrations:
  required:
    - meta-ads
  optional:
    - google-analytics
success_metrics:
  - routing_accuracy
  - wave-over-wave_cpa_improvement
  - learnings_captured_per_wave
output_schema: feedback-route-decision
---

# Feedback Router — Stage 6 of Creative Pipeline

Owns the **Feedback** stage. Closes the loop sketched in the user's pipeline diagram: Research → Concept → Brief/Hooks → Create → Test → **Feedback (NEW back to Research / BETTER back to Brief-Hooks / MORE back to Create)**.

This is the only skill that owns the Feedback stage. Every other stage has its skill; without this, the pipeline is open-loop and waves can't compound learnings.

---

## What it does

After a DCT wave conclusion (typically 7-14 days post-launch with sufficient spend), this skill:

1. **Reads performance data:**
   - `clients/<project>/campaigns/dct-YYMMDD/dct-tracker.json` Performance table
   - CREATIVES + COPY sheet tab metrics (via gids in `metrics-config.json`)
   - Optional: pull live Meta Ads data via `meta-ads` MCP for freshest numbers

2. **Routes to ONE of three paths** based on `references/routing-criteria.md` thresholds:
   - **NEW** — back to Research stage (`/ads:source-of-truth <slug>` refresh)
   - **BETTER** — back to Brief/Hooks stage (`/ads:concepts <slug>` re-ideate within winning angle)
   - **MORE** — back to Create stage (`/ads:concepts <slug>` variant expansion in winning direction)

3. **Auto-appends wave-conclusion learnings** to:
   - `clients/<project>/learnings.md` (per Marketing CLAUDE.md self-annealing rule)
   - `clients/<project>/angles/iteration-log.md` (wave summary + winners + cuts)

4. **Reports the routing decision** with rationale tied to specific metrics, not vibes.

---

## When to invoke

- Manual: `/ads:feedback <slug> <wave>` after wave conclusion
- Auto-trigger candidates (future, not v1.0):
  - Cron schedule: weekly on Mondays for active campaigns
  - Post-spend threshold: when wave hits S$1500 spend OR 14 days, whichever first
  - Performance alert: when CPA shifts >40% from baseline

---

## Phases

### Phase 0 — Context Gate

Standard Marketing CLAUDE.md context check. Confirm:
- Client slug is valid (`clients/<slug>/` exists)
- Wave number is valid (`clients/<slug>/campaigns/dct-YYMMDD/dct-tracker.json` exists)
- `metrics-config.json` exists with valid sheet_id + tab gids
- Sufficient spend has accumulated (default: ≥S$200 or as defined in `routing-criteria.md`)

If any check fails → surface the gap, stop. Don't route on thin data.

### Phase 1 — Performance Read

Read the three data sources in parallel:

1. **dct-tracker.json Performance table** — the manually-filled or sheet-synced row-per-batch performance log
2. **CREATIVES sheet tab** — per-creative metric columns (CTR, CVR, CPA, hold-rate, frequency, spend)
3. **COPY sheet tab** — per-copy-variant metric columns (CTR by copy, CVR by copy)

Aggregate by:
- Angle (3 angles in current wave → 3 aggregated rows)
- Creative type (hook vs brief — which executes better at this sophistication level?)
- Format (Static vs Carousel vs UGC vs Founder vs VSL)
- Headline pattern (per the hook_pattern enum from ad-concept-engine v2.1+)

Save aggregated read to `clients/<slug>/campaigns/dct-YYMMDD/feedback-read.json` for traceability.

### Phase 2 — Route Decision

**Pre-step — industry pool drift check (NEW):**
Before applying routing thresholds, scan `swipe-files/<industry>/` (industry slug from `clients/<slug>/context-profile.json`) for **post-wave pattern drift**:
- Compare current `swipe-files/<industry>/stage-analysis.md` `last_modified` vs the previous wave's snapshot. If competitors have shifted mechanism inventory or new winners (`days_running > 30`) appeared since last wave, that's an external trigger for **NEW** route regardless of internal performance.
- Query `swipe-files/<industry>/ads-db.sqlite` for ads first-seen since wave start. If ≥3 new mechanisms emerged industry-wide that the current wave didn't address → flag **NEW** (industry shifted) or **BETTER** (mechanism-elaboration opportunity within winning angle).
- If pool stale (`stage-analysis.md` >30 days old) suggest `/ads:scrape-library <industry>` before final routing.

Then apply `references/routing-criteria.md` thresholds. Output ONE of:

**Route: NEW** — research refresh
- Triggered when: all angles in wave underperform OR audience CPA shifted >40% from baseline OR creative fatigue across all variants OR external market signal indicates buyer shift OR **industry pool drift detected (pre-step above)**
- Action: `/ads:source-of-truth <slug>` (re-mine buyer language; check if avatars have shifted; refresh §5 Buyer Profile + §10 Angles)
- Cost: highest (full research cycle). Reserve for genuine buyer shifts.

**Route: BETTER** — concept refinement
- Triggered when: winning angle clear (1 of 3 angles outperforms), but specific hook/copy elements within that angle are driving low CTR or low hold-rate
- Action: `/ads:concepts <slug> --refine <winning-angle>` (re-ideate hooks/headlines/copy within the winning angle; keep angle locked, change execution)
- Cost: medium (Phase 2 re-run with locked Phase 1 input).

**Route: MORE** — variant expansion
- Triggered when: winning combo clear (specific batch beats baseline by ≥25% on CPA), AND headroom exists to scale (frequency <2.5, CTR holding)
- Action: `/ads:concepts <slug> --expand <winning-batch>` (generate more variants in winning angle/format/hook direction; spawn 5-8 new creatives mirroring the winner)
- Cost: lowest (locked angle + locked execution direction).

If multiple routes qualify → pick the one with highest leverage per `routing-criteria.md` precedence rule (default: BETTER > MORE > NEW when ambiguous, because BETTER unlocks larger scale once nailed).

### Phase 3 — Learnings Capture

Auto-append to TWO files (per `references/learnings-template.md`):

1. **`clients/<slug>/learnings.md`** — wave summary entry following the self-annealing rule from Marketing CLAUDE.md
2. **`clients/<slug>/angles/iteration-log.md`** — wave-N entry (winners, cuts, what was learned about the buyer or the angle)

Save raw decision artifact to `clients/<slug>/campaigns/dct-YYMMDD/feedback-decision.json` for audit trail.

### Phase 4 — Hand-off

Print the routing decision + recommended next slash command. Example output:

```
Wave 1 feedback decision: BETTER

WINNING ANGLE: Angle 2 — Wife-Initiator Reframe
  CPA: S$247 (vs target S$300, baseline S$600)
  CTR: 2.1% · Hold-rate: 31% · Frequency: 1.8 · Spend: S$650

UNDERPERFORMING:
  Angle 1: CPA S$520 (cut)
  Angle 3 Layer A: CPA S$430 (cut)
  Angle 3 Layer B: CPA S$380 (warning, hold for now)

DIAGNOSIS: Angle 2 won decisively but UGC variant (DCT004) outperformed Founder variant (DCT005) by 3x on hold-rate.
  Hypothesis: wife-voice resonance is in the PERFORMER, not the FOUNDER explanation.

NEXT ACTION: /ads:concepts neezanizam --refine "Angle 2: Wife-Initiator Reframe"
  Generate 5 new UGC variants with different performer profiles + different scene-1 hooks.
  Keep angle, hook pattern, and copy framework locked.

Learnings auto-appended to:
  clients/neezanizam/learnings.md
  clients/neezanizam/angles/iteration-log.md
```

---

## Anti-patterns

- **Don't route on <S$200 spend per creative.** Statistical noise.
- **Don't pick NEW just because results are mixed.** Mixed results usually mean BETTER or MORE — NEW is for fundamental buyer shifts, not iteration.
- **Don't let one outlier batch trigger MORE.** A batch beating baseline by 100% on tiny spend is noise, not signal.
- **Don't skip the learnings capture step.** Routing without logging breaks the compounding loop — next wave doesn't benefit from this wave.
- **Don't fabricate metrics.** If sheet data is incomplete, surface the gap and ask user to fill before routing.

---

## Integration with the 6-stage pipeline

```
Research      → /ads:source-of-truth <slug>          [HITL: 4 strategic decisions]
Concept       → /ads:concepts <slug> (Phase 1 only)  [HITL: 6-8 angles per avatar]
Brief + Hooks → /ads:concepts <slug> (Phase 2a + 2b) [HITL: per-batch creative direction]
Create        → image-generation + video-director    [HITL: per-creative approval]
Test          → /ads:upload <slug>                   (meta-ads-uploader, ads created PAUSED)
Feedback      → /ads:feedback <slug> <wave>          [routes back to NEW / BETTER / MORE]
                            ↑ THIS SKILL
```

The router does NOT execute the routed action. It outputs the recommended next slash command + rationale. User approves and runs the command. This keeps HITL at every loop boundary.

---

## Related

- Reads from: `clients/<slug>/campaigns/dct-YYMMDD/dct-tracker.json` (ad-concept-engine output)
- Reads from: CREATIVES + COPY sheet tabs (gids in `metrics-config.json`)
- Optional reads from: `meta-ads` MCP for live numbers
- Writes to: `clients/<slug>/learnings.md`, `clients/<slug>/angles/iteration-log.md`, `clients/<slug>/campaigns/dct-YYMMDD/feedback-{read,decision}.json`
- Triggers downstream: `/ads:source-of-truth` (NEW route) · `/ads:concepts` (BETTER + MORE routes)
- Companion skills: `paid-media-audit` (deeper diagnostic if NEW route picked), `analytics-attribution` (cross-channel attribution context)

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[sheets-updater]] (skill, 0.12)

<!-- skill-graph:end -->
