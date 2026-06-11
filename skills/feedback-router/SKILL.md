---
name: feedback-router
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: paid-media
difficulty: advanced
description: "Closes creative pipeline after DCT wave. Reads performance data, routes to NEW (research refresh), BETTER (angle refinement), or MORE (scale variants). Auto-appends learnings. Triggers: feedback router, wave feedback, dct feedback, performance routing, new better more. Requires: source-of-truth, ad-concept-engine. Live numbers via the meta CLI (read verbs only)."
triggers:
  - feedback router
  - wave feedback
  - dct feedback
  - performance routing
  - new better more
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
data_sources:
  required:
    - meta_cli_read_only   # ~/.local/bin/meta — read verbs only (insights get / campaign list). No MCP.
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

1. **Reads performance data** (current shape first, legacy fallback last):
   - **Current — the wave's `dct.json`.** One per workspace at `clients/<slug>/campaigns/<campaign>/dcts/<dct>/dct.json` (10-5-5 conductor clients) or `clients/<slug>/campaigns/<campaign>/dct.json` (flat). Each DCT entry carries an `image_pool` (the within-DCT pool of images Meta mixes) plus `angle_id`, `meta_adset`, `creative_type`, `market_awareness/sophistication`. The router maps performance ONTO these entries — the unit of analysis is the DCT/ad-set + its `image_pool` members.
   - **Synced metric tabs** written by the generalized sheet writer (`scripts/ad_concept_sheet_writer.py`): the CREATIVES tab (per-ad metric columns `STATUS, CTR, CVR, CPA, CALLS, SPEND, DURATION` — owned by `sheets-updater`/`meta_puller`, keyed by the `BATCH` column = the DCT/angle id) and the COPY tab. gids live in `clients/<slug>/_brand/metrics-config.json` → `tabs.creatives` / `tabs.copy`. For 10-5-5 test waves, read the `creatives_test` / `copy_test` tabs instead. Respect the writer's column boundary: strategy columns are static, metric columns carry the performance you route on.
   - **Legacy fallback — `dct-tracker.json`.** Older waves (pre-`dct.json`, e.g. `clients/neezanizam/campaigns/.../dcts/<dct>/dct-tracker.json`) carry a `creatives[]` array (`batch` / `angle` / metric fields) instead of `dcts[].image_pool`. If `dct.json` is absent and `dct-tracker.json` is present, read it the same way — `batch` maps to the DCT/angle key. Documented as fallback only; do not write new waves in this shape.
   - **Live freshest numbers — the `meta` CLI, read verbs only.** No meta-ads MCP exists. To refresh per-ad insights at decision time: `source ~/.claude/.env && export ACCESS_TOKEN="$META_ACCESS_TOKEN"`, verify `meta auth status`, then read with `meta ads insights get --ad-account-id act_… -o json` (scope to the client's `ad_platforms.meta.ad_account_id`). `insights get` / `campaign list` / `adaccount get` are billing-safe reads. NEVER `create`/`update`/`delete` from this skill — the router diagnoses, it does not touch live ads. Route the CLI call through a subagent so raw insight dumps stay out of the router's context. (Per `.claude/rules/mcp-integrations.md`.)

2. **Routes to ONE of three paths** based on `references/routing-criteria.md` thresholds + `references/media-buying-doctrine.md` reasoning. All three are **intent-routed** — the router emits a plain-English next action, not a dead slash command:
   - **NEW** — back to Research. Intent: refresh via the `source-of-truth` skill (§5 Buyer Profile + §10 Angles); if the buyer map itself shifted, rebuild `buyer-profile.md` via the `avatar-research` skill first.
   - **BETTER** — back to Brief/Hooks. Intent: `ad-concept-engine` in Conductor Mode, "refine within `<winning-angle>`."
   - **MORE** — back to Create. Intent: `ad-concept-engine` in Conductor Mode, "expand `<winning-batch>`" at the 80/20 mix.

3. **Auto-appends wave-conclusion learnings** to:
   - `clients/<project>/learnings.md` (per Marketing CLAUDE.md self-annealing rule)
   - `clients/<project>/angles/iteration-log.md` (wave summary + winners + cuts)

4. **Reports the routing decision** with rationale tied to specific metrics, not vibes.

---

## When to invoke

- By intent, after a wave concludes: *"feedback router for `<slug>` wave `<N>`,"* *"route the `<slug>` wave,"* *"dct feedback `<slug>`."* No slash command — the routing layer lands these here.
- Auto-trigger candidates (future, not v1.0):
  - Cron schedule: weekly on Mondays for active campaigns
  - Post-spend threshold: when the wave hits the client's batch-spend gate (default 600 in client currency, or 14 days, whichever first) — read `feedback_thresholds.min_spend_per_batch` from `_brand/metrics-config.json`
  - Performance alert: when CPA shifts past the client's `buyer_shift_cpa_delta_pct` (default 40%) from baseline

---

## Phases

### Phase 0 — Context Gate

Standard Marketing CLAUDE.md context check (establish the context receipt: client, campaign, workspace, phase, loaded paths). Confirm:
- Client slug is valid (`clients/<slug>/` exists)
- The wave workspace resolves and carries performance data: a `dct.json` (current — `clients/<slug>/campaigns/<campaign>/dcts/<dct>/dct.json` or the flat `campaigns/<campaign>/dct.json`) with the wave's DCT entries, OR a legacy `dct-tracker.json` in the same folder (fallback only)
- `_brand/metrics-config.json` exists with a valid `sheet_id` (or `campaigns[].sheet_id`) + the `creatives` / `copy` tab gids
- Read `feedback_thresholds` from `_brand/metrics-config.json` (fall back to legacy `feedback_router_thresholds`, then to `routing-criteria.md` defaults) and resolve the client currency. Confirm spend has accumulated against the resolved `min_spend_per_batch` — NOT a hardcoded S$ figure.

If any check fails → surface the gap, stop. Don't route on thin data.

### Phase 1 — Performance Read

Read the data sources in parallel:

1. **The wave's `dct.json` (current)** — the per-DCT entries (`dcts[]`) with `angle_id`, `meta_adset`, `creative_type`, and each entry's `image_pool`. This is the spine the router maps metrics onto. *(Legacy fallback: `dct-tracker.json`'s `creatives[]` array — `batch`/`angle`/metric fields — read identically when `dct.json` is absent.)*
2. **CREATIVES sheet tab** — per-ad metric columns (`CTR, CVR, CPA, CALLS, SPEND, DURATION`), keyed by the `BATCH` column (= DCT/angle id). Written by `sheets-updater`/`meta_puller`. For 10-5-5 test waves use `creatives_test`.
3. **COPY sheet tab** — per-copy-variant text + status (CTR-by-copy where the platform breaks it out).
4. **Optional live refresh** — `meta ads insights get` (read verb, billing-safe) via a subagent, if the sheet numbers are stale at decision time.

Aggregate by:
- Angle / DCT (each DCT entry = one ad set = one aggregated row)
- Creative type (hook vs brief — which executes better at this sophistication level?)
- Format (Static vs Carousel vs UGC vs Founder vs VSL)
- Within a DCT, which `image_pool` members drove the asset-level CTR (Meta's per-image breakdown is directional, no per-combination conversions — note that limit, do not over-read it)

Save aggregated read to the wave workspace `feedback-read.json` for traceability.

### Phase 2 — Route Decision

**Pre-step A — TCPR kill / fatigue pass (per `references/media-buying-doctrine.md`):**
Before routing, settle each DCT/creative's kill-or-keep using the doctrine, not gut feel:
- **3x-TCPR kill rule** (doctrine §1): a creative is only eligible for a CUT once it has spent `tcpr × tcpr_kill_multiple` (client config) — below that, a bad CPA is noise. Clear disasters (≥5x TCPR, dead CTR) may be killed early.
- **Fatigue trigger** (doctrine §3): mark a former winner as fatigued only when ALL THREE hold — frequency > 3, 7d CPA 30%+ worse than its prior 30d, and thumbstop/CTR/watch-time down vs its winning period. Fatigue across EVERY variant at once is a wave-level NEW/BETTER signal, not a single rotation.

**Pre-step B — comment-mining objection refresh (standing input, doctrine §5):**
Pull the freshest objections in the buyers' own words from the comments under this wave's ads and competitor ads (route the scrape through a subagent — `reddit` / `scrapecreators` / `research` buyer-language mode — and keep only the distilled objection deltas, not raw threads). These feed the NEXT batch's brief:
- New objections since last batch → new copy beats to answer.
- Objections that kept recurring despite being answered → the answer isn't landing; rework, don't repeat.
- An objection appearing across many comments → promote it to a standalone angle.

**Pre-step C — industry pool drift check:**
Scan `swipe-files/<industry>/` (industry slug from `clients/<slug>/context-profile.json`) for **post-wave pattern drift**:
- Compare current `swipe-files/<industry>/stage-analysis.md` `last_modified` vs the previous wave's snapshot. If competitors shifted mechanism inventory or new winners (`days_running > 30`) appeared since last wave, that's an external trigger for **NEW** regardless of internal performance.
- Query `swipe-files/<industry>/ads-db.sqlite` for ads first-seen since wave start. If ≥3 new mechanisms emerged industry-wide that the wave didn't address → flag **NEW** (industry shifted) or **BETTER** (mechanism-elaboration within winning angle).
- If the pool is stale (`stage-analysis.md` >30 days old), route to the `ad-library-scraper` skill (intent: "scrape the `<industry>` ad library") before final routing.

Then apply `references/routing-criteria.md` thresholds. Output ONE of:

**Route: NEW** — research refresh
- Triggered when: all angles in wave underperform OR audience CPA shifted past the client's `buyer_shift_cpa_delta_pct` from baseline OR creative fatigue across ALL variants OR external market signal indicates buyer shift OR **industry pool drift detected (pre-step C)**
- Action (intent): refresh via the `source-of-truth` skill (re-mine buyer language with the §5 / §10 sections; carry the comment-mined objection deltas in); if the buyer MAP shifted (persona dead/born), rebuild `buyer-profile.md` via the `avatar-research` skill first. (Intent-routed — the `/ads:source-of-truth` / `/ads:avatars` commands are dead.)
- Cost: highest (full research cycle). Reserve for genuine buyer shifts.

**Route: BETTER** — concept refinement (or TAM-widening)
- Triggered when: winning angle clear (one angle outperforms), but hook/copy elements within it drag CTR or hold-rate — OR a single narrow angle's CPA is climbing with moderate frequency (**TAM exhaustion**, doctrine §6: angle pool scooped, copy not broken).
- Action (intent): `ad-concept-engine` in Conductor Mode, "refine within `<winning-angle>`" (or "widen `<exhausted-angle>` into sibling angles" if TAM-exhaustion is the diagnosis). The conductor locks the angle and cues big-angle-spotter → headline-bank. Apply the 80/20 next-batch mix (doctrine §4). (Intent-routed — the `/ads:concepts --refine` command is dead.)
- Cost: medium (re-ideate with the angle locked).

**Route: MORE** — variant expansion at 80/20
- Triggered when: a specific winner beats baseline by ≥25% on CPA AND has headroom (frequency below the client's `fatigue_frequency_floor`, CTR holding).
- Action (intent): `ad-concept-engine` in Conductor Mode, "expand `<winning-batch>`." Run the next batch at the **80/20 mix** (doctrine §4): ~80% iterations of the winner's structure + proven swipes, ~20% genuinely fresh — NOT five clones of the winner. Locked: angle, creative_type, format, headline pattern. (Intent-routed — the `/ads:concepts --expand` command is dead.)
- Cost: lowest (locked angle + locked execution direction).

If multiple routes qualify → pick the one with highest leverage per `routing-criteria.md` precedence rule (default: BETTER > MORE > NEW when ambiguous, because BETTER unlocks larger scale once nailed). A NEW trigger overrides BETTER/MORE — optimising a wrong target is wasted spend.

### Phase 3 — Learnings Capture

Auto-append to TWO files (per `references/learnings-template.md`):

1. **`clients/<slug>/learnings.md`** — wave summary entry following the self-annealing rule from Marketing CLAUDE.md
2. **`clients/<slug>/angles/iteration-log.md`** — wave-N entry (winners, cuts, what was learned about the buyer or the angle)

Save raw decision artifact to `clients/<slug>/campaigns/dct-YYMMDD/feedback-decision.json` for audit trail.

### Phase 4 — Hand-off

Print the routing decision + the recommended next INTENT (the operator hands it to the conductor — there is no slash command). Currency follows the client config; the example below is a SGD client. Example output:

```
Wave 1 feedback decision: BETTER

WINNING ANGLE: Angle 2 — Wife-Initiator Reframe
  CPA: S$247 (vs target S$300, baseline S$600) · cleared 3x TCPR
  CTR: 2.1% · Hold-rate: 31% · Frequency: 1.8 · Spend: S$650

UNDERPERFORMING (all cleared 3x TCPR before cut):
  Angle 1: CPA S$520 (cut)
  Angle 3 Layer A: CPA S$430 (cut)
  Angle 3 Layer B: CPA S$380 (warning, hold for now)

DIAGNOSIS: Angle 2 won decisively but its UGC image_pool members outperformed
  the Founder ones ~3x on asset-level CTR. Hypothesis: wife-voice resonance is
  in the PERFORMER, not the FOUNDER explanation. No fatigue (freq 1.8, CTR holding).

COMMENT-MINING DELTA (feeds next batch): "is the 4.5k a one-time fee or per-property?"
  recurred 6x under the winning ad — answer it in the next batch's copy.

NEXT INTENT: ad-concept-engine (Conductor Mode) — "refine within Angle 2: Wife-Initiator
  Reframe for neezanizam." Next batch at 80/20: ~80% UGC iterations (new performer
  profiles + scene-1 hooks, answer the fee-clarity objection), ~20% fresh. Lock angle,
  hook pattern, copy framework.

Learnings auto-appended to:
  clients/neezanizam/learnings.md
  clients/neezanizam/angles/iteration-log.md
```

---

## Anti-patterns

- **Don't cut a creative below its 3x-TCPR spend.** Below the client's `tcpr × tcpr_kill_multiple` (or the `min_spend_per_creative` floor if no TCPR set), a bad CPA is statistical noise, not a verdict (doctrine §1).
- **Don't pick NEW just because results are mixed.** Mixed results usually mean BETTER or MORE — NEW is for fundamental buyer shifts, not iteration.
- **Don't let one outlier batch trigger MORE.** A batch beating baseline by 100% on tiny spend is noise, not signal.
- **Don't read MORE as "clone the winner."** MORE is the 80/20 next batch (doctrine §4) — most iterates the winner, a fifth plants fresh concepts so the angle pool refills.
- **Don't call rising CPA on a narrow angle "fatigue" by reflex.** If frequency is moderate, it's likely TAM exhaustion (doctrine §6) — widen the angle, don't just refresh the same maxed-out note.
- **Don't write or mutate live ads.** The router reads (`meta ads insights get` and the sheet) and diagnoses. `create`/`update`/`delete` are never this skill's job.
- **Don't skip the learnings capture step.** Routing without logging breaks the compounding loop — next wave doesn't benefit from this wave.
- **Don't fabricate metrics.** If sheet/`dct.json` data is incomplete, surface the gap and ask the user to fill before routing.

---

## Integration with the 6-stage pipeline

All stages are intent-routed (no slash commands — the routing layer in `.claude/rules/routing-overrides.md` lands plain-English asks on the right skill):

```
Research      → source-of-truth skill                 [HITL: 4 strategic decisions]
Concept       → ad-concept-engine (Conductor, angles)  [HITL: 6-8 angles per avatar]
Brief + Hooks → ad-concept-engine (Conductor, hooks)   [HITL: per-batch creative direction]
Create        → image-generation + vid-director        [HITL: per-creative approval]
Test          → meta-ads-uploader                       (ads created PAUSED)
Feedback      → THIS SKILL                              [routes back to NEW / BETTER / MORE]
```

The router does NOT execute the routed action and never writes to live ads. It outputs the recommended next INTENT + rationale. The operator approves and hands the intent to the conductor. HITL holds at every loop boundary.

---

## Related

- Reads from: the wave's `dct.json` (`dcts[].image_pool`, current shape) — legacy `dct-tracker.json` (`creatives[]`) as fallback
- Reads from: CREATIVES + COPY sheet tabs (gids in `_brand/metrics-config.json`), written by `scripts/ad_concept_sheet_writer.py`; metric columns filled by `sheets-updater`/`meta_puller`
- Optional reads from: the `meta` CLI (`meta ads insights get`, read verb, billing-safe) for live numbers — there is NO meta-ads MCP
- Reads config: `_brand/metrics-config.json` → `feedback_thresholds` (legacy `feedback_router_thresholds` fallback) for thresholds + currency
- Writes to: `clients/<slug>/learnings.md`, `clients/<slug>/angles/iteration-log.md`, and the wave workspace `feedback-{read,decision}.json`
- Triggers downstream (by intent): `source-of-truth` + `avatar-research` skills (NEW) · `ad-concept-engine` Conductor Mode (BETTER + MORE)
- Doctrine: `references/media-buying-doctrine.md` (kill/scale/fatigue/80-20/TAM) · thresholds: `references/routing-criteria.md`
- Companion skills: `paid-media-audit` (deeper diagnostic if NEW route picked), `analytics-attribution` (cross-channel attribution context)

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[sheets-updater]] (skill, 0.12)

<!-- skill-graph:end -->
