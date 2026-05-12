# hooks-select

**Activates:** `script-skill` (global, voice-locked).
**Input:** the output of `hooks-generate.md` (20 hooks).
**Output:** top 2 hooks scored, ranked, with diversity check + predicted lift vs control.
**Purpose:** convert raw hook output into a decision — which 2 do you test this week.

---

## DETERMINISTIC INPUTS (HARD-LOAD)

| # | Input | Path | Required? |
|---|---|---|---|
| 1 | The 20 generated hooks | (paste or path to file) | **Required** |
| 2 | Funnel-goal | `clients/<client>/_config/funnel-goal.json` | **Required** |
| 3 | Buyer profile + ICP | `clients/<client>/_config/buyer-profile.md` + `icp.md` | **Required** |
| 4 | Hook bank (for differentiation comparison) | `clients/<client>/06_learn/hook-bank.md` | Optional |
| 5 | Baseline / control ad (if exists) | `clients/<client>/06_learn/winners/<id>.md` | Optional |

If no control exists (e.g. Michelle's pilot, first batch), the baseline is "best entry in hook-bank" or "no baseline — measuring against rolling average."

---

## SCORING CRITERIA (1-10 each, total 60)

Score every hook against all six. Subscores must be defended with one short reason each.

| # | Criterion | What it measures |
|---|---|---|
| 1 | **Scroll-Stop Power** | Pattern interrupt strength in first 3 seconds. Does it stop someone mid-feed? |
| 2 | **Emotional Trigger Strength** | Depth of psychological impact. Does it create a *felt* reaction (not just intellectual interest)? |
| 3 | **Audience Alignment** | How well does it map to `buyer-profile.md` pain points and `icp.md` identity? |
| 4 | **Conversion Potential** | Likelihood the hook delivers on the funnel-stage's job. TOFU job = follow/save; MOFU = DM/profile-visit; BOFU = booked call. |
| 5 | **Algorithm Optimization** | Engagement signal density (early watch-through, save, share). Will the algorithm boost this? |
| 6 | **Differentiation Factor** | How distinct vs control + hook-bank. Is this *new ground* or a remix? |

---

## SELECTION RULES (the 2 picks must satisfy ALL of these)

1. **Top 2 by total score** — highest two go through (ties broken by Differentiation Factor).
2. **Different emotional triggers** — pick 2 must hit DIFFERENT primary triggers (e.g., one fear-based + one curiosity-based). If the top 2 by score share a trigger, swap in the next-highest from a different trigger family.
3. **Funnel-stage OR archetype divergence** — the 2 must differ on at least one of: funnel stage, format, or archetype. No two near-clones in the test.
4. **Voice-fit floor** — both picks must have voice fit ≥ 8/10. Below that = drop regardless of total score (you can't ship hooks the client wouldn't say).
5. **Originality floor** — both picks must have originality ≥ 65/100. Below that = drop (we're not testing remixes of existing winners; that's repurposing, not testing).

---

## EMOTIONAL TRIGGER FAMILIES (for diversity check)

The 2 picks must come from DIFFERENT families. Tag each hook with its primary trigger:

- **Fear** — loss aversion, "before it's too late", consequence framing
- **Curiosity** — gap-driven, "the thing nobody tells you"
- **Identity** — "the kind of [role] who..." / belonging signals
- **Aspiration** — vision-of-future / Magician archetype outcomes
- **Anger / Justice** — calling out a bad pattern, contrarian energy
- **Relief** — "you don't have to do [hard thing] anymore"
- **Pride** — credentialing the audience ("if you're already doing X...")

---

## OUTPUT SCHEMA

### Pre-selection scorecard (all 20 hooks)

```
| Hook | Funnel | Format | Trigger | Scroll | Emot | Align | Conv | Algo | Diff | TOTAL |
|------|--------|--------|---------|--------|------|-------|------|------|------|-------|
| #1   | TOFU   | Q'tion | Curio   | 8      | 7    | 9     | 6    | 7    | 6    | 43    |
| #2   | ...    | ...    | ...     | ...    | ...  | ...   | ...  | ...  | ...  | ...   |
| ...  |        |        |         |        |      |       |      |      |      |       |
| #20  | BOFU   | List   | Fear    | 6      | 8    | 8     | 9    | 7    | 9    | 47    |
```

### THE 2 PICKS

```
==== PICK A — Hook #N — [Funnel · Format · Trigger family] — Total Score: X/60 ====

Text:
"[hook text]"

Subscores: scroll=X · emot=X · align=X · conv=X · algo=X · diff=X

Why it will beat the baseline:
[2-3 sentences citing the specific buyer-profile pain it hits, the specific outlier pattern it borrows from (if any), and why the algorithm rewards this shape]

Primary psychological trigger:
[One of the 7 trigger families, plus 1 sentence on why this audience responds to it]

What makes it superior to the other 18:
[2-3 sentences naming the 2-3 closest runners-up and why this one wins on the decisive criterion]

Predicted performance vs control:
[Qualitative: "hook rate ↑ 30-50% vs current best; hold rate likely similar; saves likely ↑ because [reason]"]


==== PICK B — Hook #N — [Funnel · Format · Trigger family] — Total Score: X/60 ====
[same structure]


==== Diversity check ====
- Trigger A: [PICK A's trigger family]
- Trigger B: [PICK B's trigger family] ← must be different
- Funnel stages: [A's stage] vs [B's stage]
- Formats: [A's format] vs [B's format]
- Archetypes: [A's archetype] vs [B's archetype]
- ✓ diverse enough? [yes / no — explain]


==== Test plan ====
- Run as A/B test for [N] days OR until [N] impressions per variant.
- Primary metric: [hook rate × hold rate, weighted per funnel-goal.json's `winner_metric_weights`]
- Decision rule: variant with composite score > 3× rolling 4-week average is the new winner; loser gets decomposed.
- Loser handling: even the losing pick deserves a Stage-06 decomposition note ("why didn't this land?"). Append to hook-bank.md.


==== Rest of the field ====
Top 5 ranked (not picked): [Hook #X, Hook #Y, Hook #Z, Hook #W, Hook #V — with one-line reason each for why each was passed over]
Bottom 5 (dropped): [Hook IDs + one-line reason — usually voice-fit floor or originality floor]
```

---

## SELF-CHECK BEFORE EMITTING

- [ ] Both picks scored ≥ 8/10 on voice fit
- [ ] Both picks scored ≥ 65/100 on originality
- [ ] Both picks come from different trigger families
- [ ] Both picks differ on funnel stage OR format OR archetype
- [ ] Subscores defended with one-line reasoning each
- [ ] Predicted lift cited a *specific* mechanism, not vibes
- [ ] Diversity check passes

If any check fails: re-evaluate and either pick different hooks or explain why the rule had to bend.

---

## RUN

Score all 20 hooks. Apply selection rules. Emit the scorecard + 2 picks + test plan in the exact schema above.
