---
description: Generate a headline bank using the 5 psychological mechanisms (Curiosity / Specific-Benefit / Contrarian / Fear-Risk / Identity-Call) × awareness levels × angle banks. Wraps existing headline-bank skill with copywriting-OS mechanism diversity enforcement. Invoke via `/copy headline <client-slug>`.
version: "0.1.0"
brand: AgentKits Marketing by AityTech
argument-hint: <client-slug> [mass-desire focus] [mechanism: curiosity | specific | contrarian | fear | identity | all]
---

## What this does

Wraps `skills/headline-bank/` with copywriting-OS gates + MECHANISM DIVERSITY enforcement from Mark Masters cai #39 ("The Headline Lab That Controls 80% of Your Results").

**Core principle (cai #39):** every winning headline activates one or more of 5 psychological MECHANISMS (not formats, not templates — mechanisms). A good headline bank covers multiple mechanisms so you can test which resonates with your audience.

**Upgrade from base headline-bank skill:** the existing skill organizes by awareness × angle. This wrapper ADDS the 5-mechanism axis as a required diversity constraint — every batch must contain ≥N headlines per mechanism.

## The 5 Headline Mechanisms (cai #39)

1. **Curiosity Gap** — incomplete pattern the brain must resolve
   *"The Weird Reason Most Diets Fail After Day 11"*
2. **Specific Benefit** — concrete outcome with numbers, timeframes, precise results
   *"Add 2.3 Pounds of Muscle in 28 Days Without Changing Your Diet"*
3. **Contrarian Hook** — challenges an assumed belief; pattern interrupt
   *"Why Everything You Know About SEO Is Costing You Traffic"*
4. **Fear / Risk** — cost of inaction; loss aversion
   *"The $47,000 Mistake Hiding in Your Sales Page Right Now"*
5. **Identity Call** — tribal recognition; speaks to who they are or want to become
   *"For Copywriters Who Refuse to Compete on Price"*

## Step 1 — Shared context

See `commands/copy.md` Step 2. Plus:
- Mass desire (from `source-of-truth.md` if exists; else ask operator per `skills/headline-bank/` existing interactive flow)
- Awareness level (Schwartz 1-5)

## Step 2 — Pre-write gates

1. **Channeling Check** — existing desire + reader's internal conversation (applies to headlines just as strongly as body copy)
2. **Coat of Arms** — headline language must come from buyer vocabulary, not brand vocabulary
3. **One-Person Seed** — each headline imagined as sent to ONE specific person

## Step 3 — Resolve mechanism scope

- If `$3` = `all` (default) → generate full bank: 5 mechanisms × 5 awareness levels × 10 angle banks = large combinatorial
- If `$3` = specific mechanism → focus bank on just that mechanism (useful for A/B test on a single axis)

## Step 4 — Delegate to existing `/ads:headlines`

```
/ads:headlines <slug>
```

Sub-agent execution. Inject the 5-mechanism diversity requirement into the skill's prompt: "Every 10-headline batch MUST cover all 5 mechanisms (minimum 1 per mechanism, max 3 per mechanism). Tag each headline with its mechanism."

## Step 5 — Post-write reviewers (headline-specific)

Reduced reviewer set for headlines (they're short):

1. **one-person-enforcement** — the writer must declare who the bank was written for
2. **mechanism-diversity check** (custom, not in the universal reviewer set):
   ```
   For each 10-headline batch, verify:
   - All 5 mechanisms represented (1-3 per mechanism)
   - No mechanism dominates (>4 of 10)
   - Each headline correctly tagged with its mechanism
   - Tagging accuracy: sub-agent reviews 3 random headlines per mechanism to verify taxonomy match
   ```
3. **specificity audit** (subset of proof-density-audit, mechanism #2 Specific Benefit only) — any round number in a Specific-Benefit headline = FAIL; push to exact number
4. **teardown-reviewer** (Hero element only — H1/H2/H3/H4 failure modes applied to each headline)

Skip: proof-density (full version), emotional-sequence (single headline doesn't have a sequence), objection-coverage (not a full-letter concern) — these kick in once headlines integrate into longer copy.

## Step 6 — Ship + log

- **Output:** `clients/<slug>/copy-system/outputs/headlines/<YYMMDD>-<mass-desire>.md` (bank organized by mechanism × awareness × angle)
- **Bank format:** structured markdown with columns: headline | mechanism | awareness | angle bank | tested? | performance (populated later from `/ads:feedback`)
- **Cross-file:** append to `swipe-files/<industry>/our-headlines.md` as candidate swipe material for future runs

## Prerequisites

All `/copy` prerequisites PLUS:
- Mass desire identified (interactive prompt if missing)
- Awareness level known OR will span all 5

## Related

- Underlying skill: `skills/headline-bank/` (will be upgraded in Phase 2.6 to integrate 5-mechanism axis natively)
- Existing command wrapped: `commands/ads/headlines.md`
- Parent router: `commands/copy.md`
- Cai #39 source: Mark Masters Headline Laboratory
- Phase 2.6 dependency: native headline-bank skill upgrade for mechanism axis
