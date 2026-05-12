---
description: Score the 20 generated hooks, pick top 2 for testing with diversity check. Wraps script-skill.
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [--input <path-to-generate-output>] [--client <client-slug>]
---

# /hooks:select

**Underlying skill: `script-skill`**. This command locks the skill into a scoring + selection workflow on top of an existing `/hooks:generate` batch.

---

## Step 1 — Resolve inputs

| Input | Source | Required? |
|---|---|---|
| Generated hooks (the 20) | `--input` path, OR the most recent file in `clients/<client>/02_script/output/*-hooks-generate.md` | **Required** |
| Buyer profile + ICP | `clients/<client>/buyer-profile.md` + `icp.md` | **Required** |
| Offer + channels | `clients/<client>/offer.md` + `channels.json` (or `funnel-goal.json`) | **Required** |
| Brand voice | `clients/<client>/brand-voice.md` | **Required** |
| Past hook performance | `clients/<client>/learnings.md` "winners" section | Optional |
| Current control (winning ad) | `clients/<client>/learnings.md` "current-control" entry | Optional — if absent, score against rolling average |

If no control exists (e.g. first batch for a pilot client), the baseline is **"best entry in learnings.md hook-bank"** or **"no baseline yet — first batch"**.

## Step 2 — Scoring criteria (1-10 each, 60 max)

Score every hook against all six. Subscores must be defended with one short reason each.

| # | Criterion | What it measures |
|---|---|---|
| 1 | **Scroll-Stop Power** | Pattern interrupt strength in first 3 seconds. Does it stop someone mid-feed? |
| 2 | **Emotional Trigger Strength** | Depth of psychological impact. Felt, not just intellectual. |
| 3 | **Audience Alignment** | How well does it map to `buyer-profile.md` pain + `icp.md` identity? |
| 4 | **Conversion Potential** | Likelihood the hook delivers on the funnel-stage's job. TOFU = follow/save; MOFU = DM/profile-visit; BOFU = booked call. |
| 5 | **Algorithm Optimization** | Engagement signal density (early watch-through, save, share). Will the algorithm boost? |
| 6 | **Differentiation Factor** | How distinct vs control + hook-bank entries from `learnings.md`. |

## Step 3 — Selection rules (the 2 picks must satisfy ALL of these)

1. **Top 2 by total score** — highest two go through (ties broken by Differentiation Factor).
2. **Different emotional triggers** — picks must hit DIFFERENT primary trigger families. If top 2 share a trigger, swap in next-highest from a different family.
3. **Funnel-stage OR format OR archetype divergence** — must differ on at least one of the three. No near-clones.
4. **Voice-fit floor** — both picks ≥ 8/10. Below = drop regardless of total score.
5. **Originality floor** — both picks ≥ 65/100. Below = drop.

## Step 4 — Emotional trigger families (for diversity check)

Tag each hook with its primary trigger before scoring:

- **Fear** — loss aversion, "before it's too late"
- **Curiosity** — gap-driven, "the thing nobody tells you"
- **Identity** — "the kind of [role] who..."
- **Aspiration** — vision-of-future / Magician archetype outcomes
- **Anger / Justice** — calling out a bad pattern
- **Relief** — "you don't have to do [hard thing]"
- **Pride** — credentialing the audience

## Step 5 — Output schema

### Pre-selection scorecard (all 20 hooks)

```
| Hook | Funnel | Format | Trigger | Scroll | Emot | Align | Conv | Algo | Diff | TOTAL |
|------|--------|--------|---------|--------|------|-------|------|------|------|-------|
| #1   | TOFU   | Q'tion | Curio   | 8      | 7    | 9     | 6    | 7    | 6    | 43    |
...
| #20  | BOFU   | List   | Fear    | 6      | 8    | 8     | 9    | 7    | 9    | 47    |
```

### THE 2 PICKS

```
==== PICK A — Hook #N — [Funnel · Format · Trigger family] — Total Score: X/60 ====

Text:
"[hook text]"

Subscores: scroll=X · emot=X · align=X · conv=X · algo=X · diff=X

Why it will beat the baseline:
[2-3 sentences citing specific buyer-profile pain + outlier pattern borrowed (if any) + why the algorithm rewards this shape]

Primary psychological trigger:
[One of the 7 families + 1 sentence on why this audience responds]

What makes it superior to the other 18:
[2-3 sentences naming closest runners-up + decisive criterion]

Predicted performance vs control:
[Qualitative: "hook rate ↑ 30-50% vs current best"; cite mechanism, not vibes]


==== PICK B — Hook #N — [Funnel · Format · Trigger family] — Total Score: X/60 ====
[same structure]


==== Diversity check ====
- Trigger A: [...]
- Trigger B: [...] ← must be different
- Funnel stages: A vs B
- Formats: A vs B
- Archetypes: A vs B
- ✓ diverse enough? [yes / no — explain]


==== Test plan ====
- Run as A/B test for [N] days OR until [N] impressions per variant.
- Primary metric: hook rate × hold rate, weighted per channels.json/funnel-goal.json
- Decision rule: variant with composite score > 3× rolling 4-week average wins; loser → /hooks:analyze decomposition.


==== Rest of the field ====
Top 5 unranked (3-7): [Hook IDs + one-line "why passed over" each]
Bottom 5 (dropped): [Hook IDs + one-line "why dropped" — usually voice-fit or originality floor]
```

## Step 6 — Self-check before emitting

- [ ] Both picks scored ≥ 8/10 on voice fit
- [ ] Both picks scored ≥ 65/100 on originality
- [ ] Different trigger families
- [ ] Differ on funnel stage OR format OR archetype
- [ ] Subscores defended with one-line reasoning
- [ ] Predicted lift cites a *specific* mechanism
- [ ] Diversity check passes

If any check fails: re-evaluate or explain why the rule had to bend.

## Step 7 — Persist

Write to `clients/<client>/02_script/output/<YYYY-WW>-hooks-select.md` next to the generate batch.

Append to `clients/<client>/learnings.md` under `## Hook selections`:
```
- YYYY-MM-DD · 2 picks: #X (trigger=Y) + #Z (trigger=W) · top total scores: X/60, X/60
```

## RUN

Score all 20 hooks. Apply selection rules. Emit the scorecard + 2 picks + test plan in the exact schema. Persist.
