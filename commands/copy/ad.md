---
description: Generate ad copy (primary text + headlines + descriptions) for paid campaigns with copywriting-OS gates wrapped around the existing ad-concept-engine + big-angle-spotter pipeline. Invoke via `/copy ad <client-slug> [angle-name]`.
version: "0.1.0"
brand: AgentKits Marketing by AityTech
argument-hint: <client-slug> [angle-name if targeting a specific existing angle] [avatar if >1]
---

## What this does

Wraps `skills/ad-concept-engine/` + `skills/big-angle-spotter/` with copywriting-OS gates + reviewers. Produces ad-ready copy (primary text variants + headline variants + description variants) for Meta / Google / TikTok paid placements.

**Relationship to existing ads pipeline:** the 6-stage creative pipeline (`/ads:source-of-truth` → `/ads:avatars` → `/ads:big-angle-spotter` → `/ads:concepts` → `/ads:upload` → `/ads:feedback`) stays intact. This command wraps the COPY output of that pipeline with universal gates + reviewers. Use for standalone ad copy generation OR to add gate-enforcement to a concepts-engine wave.

## Step 1 — Shared context

See `commands/copy.md` Step 2. Plus:
- `clients/<slug>/source-of-truth.md` (if exists — §5.5 Golden Nuggets, §5.7 ICP Language)
- `clients/<slug>/angles/<angle-name>/` (if targeting a specific angle from big-angle-spotter run)
- `swipe-files/<industry>/` (auto-loaded if industry set in context-profile)

## Step 2 — Pre-write gates

Same 3 gates. **Tighter enforcement for ads** — ads have ~3 seconds to flip Indifference→Pain, so channeling-check + coat-of-arms are EXTRA critical.

## Step 3 — Resolve angle

If `$2` is an angle name that exists under `clients/<slug>/angles/`, load that angle's winning headlines + ad prompts as reference.

If no angle specified:
- Prompt the operator: "Which angle? Pick from existing (list) OR 'new' to trigger big-angle-spotter first."
- If "new" → delegate to `/ads:big-angle-spotter` first, then return here with the produced angle.

## Step 4 — Delegate to existing `/content:ads` or `/ads:concepts`

For simple ad copy generation:
```
/content:ads <slug> <angle>
```

For full DCT wave (3 creatives × 2 headlines × 2 ad copies):
```
/ads:concepts <slug> <angle>
```

Sub-agent execution.

## Step 5 — Post-write reviewers (ad-adapted)

5 sub-agents. Ad-specific tweaks:

1. **one-person-enforcement** — IMAGINED READER required per ad variant
2. **proof-density-audit** — ads have compressed space, relax to ≥50% density; PUSH SPECIFICITY type hardest (round numbers = fail)
3. **emotional-sequence-audit** — compressed: primary-text must flip Indifference→Pain in first line AND land on Hope OR Desire by CTA. Skip intermediate states is OK for ads due to space.
4. **objection-coverage-audit** — not every ad covers all 6; must cover Price + Trust + one relevant other (Authority if high-ticket, Timing if urgent offer). Mark others N/A with reason.
5. **teardown-reviewer** — ad-element adaptation: Hero = primary text first line + headline; Body = rest of primary text; Proof = any inline; CTA = headline/description + button. Critical failures: generic hook + fake urgency = auto-FAIL.

## Step 6 — Synthesize + revise

Same as `/copy:sales-letter`. Revision cycles ≤2.

## Step 7 — Ship + log

- **Output:** `clients/<slug>/angles/<angle>/ad-copy-<YYMMDD>.md` (structured: primary-text variants, headline variants, description variants)
- **DCT tracker row:** if invoked via `/ads:concepts`, the existing `dct-tracker.json` entry adds a `gates-passed` field with all 5 reviewer verdicts
- **Logs + learnings:** standard + append to `skills/ad-concept-engine/learnings.md` + `skills/big-angle-spotter/learnings.md`

## Prerequisites

All `/copy` prerequisites PLUS:
- Target placement(s) known — Meta feed / Reels / Stories / Google / TikTok — because format constraints differ
- Angle identified OR permission to run big-angle-spotter first

## Related

- Underlying skills: `skills/ad-concept-engine/`, `skills/big-angle-spotter/`, `skills/headline-bank/`, `skills/avatar-research/`
- Existing commands wrapped: `commands/content/ads.md`, `commands/ads/concepts.md`
- Upstream: `skills/source-of-truth/`, `/ads:scrape-library`
- Parent router: `commands/copy.md`
