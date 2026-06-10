# Routing Criteria — NEW / BETTER / MORE

Hard thresholds the feedback-router uses to pick the next stage. These are defaults — clients can override in `clients/<slug>/metrics-config.json` under a `feedback_router_thresholds` block.

---

## Pre-routing gates

Before any route can fire, ALL of these must be true:

| Gate | Default | Why |
|---|---|---|
| Min spend per creative | S$200 | Statistical noise floor |
| Min spend per batch (sum of creatives) | S$600 | 3 creatives × min |
| Min wave duration | 7 days | Smooth weekday/weekend variation |
| Min impressions per creative | 5,000 | Ad-delivery learning phase |
| dct-tracker.json Performance table populated | yes | Source of truth for routing |

If any pre-routing gate fails → output: `INSUFFICIENT_DATA`. Do not route. Surface the gap.

---

## Route: NEW (Research refresh)

Triggered when ANY of the following:

| Trigger | Threshold |
|---|---|
| All angles in wave underperform | Every angle's CPA > 2x KPI target |
| Audience CPA shifted dramatically | Wave-over-wave CPA delta > 40% (worse) AND not creative-fatigue-explainable |
| Creative fatigue across ALL variants | Every creative's frequency > 3.5 AND CTR declined > 30% from week 1 to week 2 |
| External market signal | User-flagged event: regulatory change, viral counter-narrative, major competitor entry |
| Audience demographic drift | Sheet-tracked CPA-by-age or CPA-by-region shifts > 50% in winning segment |

**Action:** `/ads:source-of-truth <slug>` (refresh §5 Buyer Profile + §10 Angles + check if avatars themselves shifted)

**Rationale logged:** which trigger fired + the metric values + the inference

---

## Route: BETTER (Concept refinement within winning angle)

Triggered when ALL of the following:

| Condition | Threshold |
|---|---|
| Winning angle clear | One angle's CPA ≤ KPI target AND ≤ 0.7x next-best angle CPA |
| Within winning angle, hook/copy variance is wide | Best vs worst creative within winning angle differs by ≥40% on CTR or hold-rate |
| Specific failure pattern identifiable | Either: (a) low hold-rate (hook problem), (b) high CTR + low CVR (copy/LP problem), (c) format-specific gap (UGC > Founder or vice-versa) |
| Headroom to scale exists | Frequency on winning batch < 2.5 |

**Action:** `/ads:concepts <slug> --refine "<winning-angle-name>"`
- Re-run Phase 2a (Hooks) and/or Phase 2b (Briefs) within the winning angle
- Generate 5-8 new variants targeting the identified failure pattern
- Keep angle locked, change execution

**Rationale logged:** winning angle + failure pattern + what to test next

---

## Route: MORE (Variant expansion in winning direction)

Triggered when ALL of the following:

| Condition | Threshold |
|---|---|
| Winning combo clear (specific creative) | One creative's CPA ≤ 0.75x KPI target AND ≤ 0.6x next-best in same batch |
| Headroom to scale | Frequency on winning creative < 2.5 AND CTR holding (week-2 CTR ≥ 0.8x week-1 CTR) |
| Creative quality consistency | Hold-rate ≥ 25% (proves the audience genuinely engages, not just clicks) |
| No fatigue signal yet | Spend trajectory per impression NOT trending up (CPM stable) |

**Action:** `/ads:concepts <slug> --expand "<winning-batch-id>"`
- Spawn 5-8 new variants mirroring the winner
- Same angle, same creative_type (hook OR brief), same format, same headline pattern
- Vary: secondary visual element, performer cast, scene 1 entry, copy framework variant — but anchor on the winner's structural choices

**Rationale logged:** winning batch + what stays locked + what gets varied

---

## Precedence rule (when multiple routes qualify)

```
BETTER > MORE > NEW
```

**Why:** BETTER unlocks larger potential scale once execution-level gaps close. MORE only scales the existing winner — caps at the audience's natural saturation. NEW is the highest-cost path; reserve it for genuine buyer shifts.

**Override condition:** if NEW triggers fire AND BETTER/MORE also qualify, NEW wins. Buyer shift means BETTER/MORE will be optimising the wrong target.

---

## Threshold tuning

These thresholds are starting defaults. After 5+ waves across multiple clients, calibrate per client by adding to `clients/<slug>/metrics-config.json`:

```json
{
  "feedback_router_thresholds": {
    "min_spend_per_creative": 200,
    "min_wave_duration_days": 7,
    "winning_angle_cpa_ratio_to_next_best": 0.7,
    "winning_creative_cpa_ratio_to_kpi": 0.75,
    "fatigue_frequency_floor": 2.5,
    "buyer_shift_cpa_delta_pct": 40
  }
}
```

If overrides are absent, defaults from this file apply.

---

## What the router output looks like

Every routing decision produces a structured artifact at `clients/<slug>/campaigns/dct-YYMMDD/feedback-decision.json`:

```json
{
  "wave": 1,
  "decision_at": "2026-04-25T14:30:00+08:00",
  "route": "BETTER",
  "winning_angle": "Angle 2: Wife-Initiator Reframe",
  "winning_metrics": {
    "cpa": 247,
    "ctr_pct": 2.1,
    "hold_rate_pct": 31,
    "frequency": 1.8,
    "spend_sgd": 650
  },
  "underperforming": [
    {"angle": "Angle 1: The 3-Number Test", "cpa": 520, "action": "cut"},
    {"angle": "Angle 3 Layer A: Bad Agent (Anti-hard-sell)", "cpa": 430, "action": "cut"},
    {"angle": "Angle 3 Layer B: Bad Agent (Anti-discount)", "cpa": 380, "action": "warning_hold"}
  ],
  "failure_pattern_identified": "Within Angle 2, UGC variant outperformed Founder variant 3x on hold-rate. Hypothesis: wife-voice resonance is in the PERFORMER, not the FOUNDER explanation.",
  "next_action": "/ads:concepts neezanizam --refine \"Angle 2: Wife-Initiator Reframe\"",
  "next_action_scope": "Generate 5 new UGC variants with different performer profiles + different scene-1 hooks. Keep angle, hook pattern, copy framework locked.",
  "thresholds_used": "defaults",
  "raw_data_path": "clients/neezanizam/campaigns/dct-260417/feedback-read.json"
}
```
