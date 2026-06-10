# Routing Criteria — NEW / BETTER / MORE

Hard thresholds the feedback-router uses to pick the next stage. These are **defaults**. Per-client overrides live in `clients/<slug>/_brand/metrics-config.json` under a `feedback_thresholds` block (see §Threshold tuning). If that block is absent, the defaults on this page apply.

**Currency follows the client.** The numbers below are written with `S$` because the reference client is Singapore-based, but the currency is whatever the client's `metrics-config.json` reports (the `ad_platforms.meta.ad_account_id` account currency, surfaced in the metrics tabs). When the router prints a gate or a threshold, it uses the client's currency symbol, not a hardcoded `S$`. Read `feedback_thresholds.currency` if present; otherwise infer from the client's sheet. Never assert `S$` for a non-SG client.

> Ferres grounding: the spend gates below are this skill's house thresholds. The deeper *kill/scale* doctrine — the 3x-TCPR rule, fatigue 3-condition trigger, vertical/horizontal scaling, 80/20 next-batch mix, TAM exhaustion — lives in `media-buying-doctrine.md`. This file = numbers; that file = the reasoning behind a route.

---

## Pre-routing gates

Before any route can fire, ALL of these must be true (values shown are defaults; client `feedback_thresholds` overrides them, currency follows client):

| Gate | Default | Why |
|---|---|---|
| Min spend per creative | 200 (client currency) | Statistical noise floor. Cross-check the doctrine's 3x-TCPR rule: a creative must also have cleared 3x the client's TCPR before a cut. |
| Min spend per batch (sum of creatives) | 600 (client currency) | 3 creatives × min |
| Min wave duration | 7 days | Smooth weekday/weekend variation |
| Min impressions per creative | 5,000 | Ad-delivery learning phase |
| Performance data present | yes | The wave's `dct.json` (current shape) carries it, or the synced sheet tabs do, or — legacy — `dct-tracker.json` |

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

**Action (intent, not a command):** route to the `source-of-truth` skill to refresh §5 Buyer Profile + §10 Angles; if the buyer *map itself* shifted (new persona, dead persona), route to the `avatar-research` skill to rebuild `buyer-profile.md` first — it owns the avatars and chains the research sub-steps. (Both are intent-routed per `.claude/rules/routing-overrides.md`; the old `/ads:source-of-truth` / `/ads:avatars` commands are dead.) Feed the wave's comment-mined objection deltas (`media-buying-doctrine.md` §5) into the refresh as a standing input.

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

**Action (intent, not a command):** route to `ad-concept-engine` in Conductor Mode with a "refine within winning angle" brief — *"new ad concepts for `<slug>`, refine within `<winning-angle-name>`."* The conductor reads `pipeline-state.json`, locks the angle, and cues `big-angle-spotter` → `headline-bank` to re-ideate hooks/copy. (Intent-routed per `.claude/rules/routing-overrides.md` "DCT conductor" entry; the old `/ads:concepts --refine` command is dead.)
- Keep angle locked, change execution; target the identified failure pattern.
- Apply the 80/20 next-batch mix (`media-buying-doctrine.md` §4): ~80% iterations of the proven structure, ~20% fresh.
- If the symptom is rising CPA on a narrow angle with moderate frequency, name TAM exhaustion (`media-buying-doctrine.md` §6) and widen the angle instead of polishing a maxed-out note.

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

**Action (intent, not a command):** route to `ad-concept-engine` in Conductor Mode with an "expand the winner" brief — *"next angle wave for `<slug>`, expand `<winning-batch-id>`."* (Intent-routed per `.claude/rules/routing-overrides.md`; the old `/ads:concepts --expand` command is dead.)
- Run the next batch at the 80/20 mix (`media-buying-doctrine.md` §4): ~80% iterations of the winner's structure + proven swipes, ~20% genuinely fresh concepts so the angle pool keeps refilling. MORE is NOT "five clones of the winner."
- Locked: same angle, same creative_type (hook OR brief), same format, same headline pattern.
- Vary: secondary visual element, performer cast, scene 1 entry, copy framework variant — anchored on the winner's structural choices.

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

These thresholds are starting defaults. After 5+ waves across multiple clients, calibrate per client by adding a `feedback_thresholds` block to `clients/<slug>/_brand/metrics-config.json`:

```json
{
  "feedback_thresholds": {
    "currency": "SGD",
    "tcpr": 100,
    "tcpr_kill_multiple": 3,
    "min_spend_per_creative": 200,
    "min_spend_per_batch": 600,
    "min_wave_duration_days": 7,
    "min_impressions_per_creative": 5000,
    "winning_angle_cpa_ratio_to_next_best": 0.7,
    "winning_creative_cpa_ratio_to_kpi": 0.75,
    "fatigue_frequency_floor": 2.5,
    "buyer_shift_cpa_delta_pct": 40
  }
}
```

Resolution order the router applies:

1. `_brand/metrics-config.json` → `feedback_thresholds{}` (canonical key).
2. Legacy fallback: an older `feedback_router_thresholds{}` block (same fields, no `currency`/`tcpr`) is still honored if `feedback_thresholds` is absent — read it, but on the next write migrate the client to `feedback_thresholds`.
3. Neither present → defaults from this file, currency inferred from the client's ad account.

`tcpr` + `tcpr_kill_multiple` feed the doctrine's 3x-TCPR kill rule (`media-buying-doctrine.md` §1). A creative is only eligible for a CUT once it has spent `tcpr × tcpr_kill_multiple` in the client's currency. If `tcpr` is unset, fall back to the `min_spend_per_creative` floor alone and note in the rationale that the TCPR kill gate was skipped (no target set).

---

## What the router output looks like

Every routing decision produces a structured artifact at `clients/<slug>/campaigns/dct-YYMMDD/feedback-decision.json`:

```json
{
  "wave": 1,
  "decision_at": "2026-04-25T14:30:00+08:00",
  "route": "BETTER",
  "winning_angle": "Angle 2: Wife-Initiator Reframe",
  "currency": "SGD",
  "winning_metrics": {
    "cpa": 247,
    "ctr_pct": 2.1,
    "hold_rate_pct": 31,
    "frequency": 1.8,
    "spend": 650
  },
  "underperforming": [
    {"angle": "Angle 1: The 3-Number Test", "cpa": 520, "action": "cut", "tcpr_kill_cleared": true},
    {"angle": "Angle 3 Layer A: Bad Agent (Anti-hard-sell)", "cpa": 430, "action": "cut", "tcpr_kill_cleared": true},
    {"angle": "Angle 3 Layer B: Bad Agent (Anti-discount)", "cpa": 380, "action": "warning_hold"}
  ],
  "failure_pattern_identified": "Within Angle 2, UGC variant outperformed Founder variant 3x on hold-rate. Hypothesis: wife-voice resonance is in the PERFORMER, not the FOUNDER explanation.",
  "next_action_intent": "ad-concept-engine Conductor Mode — refine within \"Angle 2: Wife-Initiator Reframe\" (intent-routed, no slash command)",
  "next_action_scope": "Generate the next batch at the 80/20 mix (~80% UGC iterations of the winner with new performer profiles + new scene-1 hooks, ~20% fresh). Keep angle, hook pattern, copy framework locked.",
  "thresholds_used": "feedback_thresholds (client metrics-config) or defaults",
  "raw_data_path": "clients/neezanizam/campaigns/dct-260417/feedback-read.json"
}
```

`spend_sgd` was renamed to a currency-agnostic `spend` + a sibling `currency` field — the symbol follows the client, never hardcoded SGD. `next_action` (a dead slash command) was replaced by `next_action_intent` (a routing instruction the operator hands to the conductor).
