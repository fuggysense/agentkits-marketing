# CONTEXT — Phase 03: Scripts

Canonical stage contract. Per-concept `03_scripts/CONTEXT.md` points here. Runs only after AG1 approval.

## Inputs

- Layer 4 (working): `../02_ag1-options/approval-1.json` (must be `approved`)
- Layer 4 (working): `../02_ag1-options/concepts.json` + approved hook variant from `hook-variants.json`
- Layer 3 (reference): `clients/takekine/_brand/brand-voice.md` (verbatim phrases, banned phrases)
- Layer 3 (reference): `clients/takekine/_brand/funnel.md` (rung budget — script length must fit the chosen ad rung)
- Layer 3 (reference): `clients/takekine/_brand/funnel-research/sales-letter-extract-*.md` (claim guardrails, ad→SL handoff)

## Process

Script writer (script-skill or copywriter agent per vid-director.md §2 phase 3) drafts the full ad script for the approved concept + hook. Honors rung budget (15s / 30s / 45s / 60s / 90s). Preserves the curiosity gap — do NOT name the SL's mechanism (DMT1 etc.); reference "a biological ceiling" or "the route" instead. No medical or specific outcome numbers in the ad copy.

## Outputs

- `script-pack.md` — full script with beats, dialog, on-screen text, B-roll cues, CTA
  - Must open with `## Pack Reasoning` section: methodology loadout ID, diversity-gate summary, L3 gate result per concept, why this persona/campaign combination targets the micro-persona's jaded failure state. Source: `concept-pack.md` reasoning block + script-stage decisions.
  - Must include `## Key Moments` section per concept (propagated from `concepts.json[].key_moments[]`): 3–5 sync peaks where visual + audio must land together. These are non-negotiable render review criteria.
  - **Done:** script honors rung budget, no banned phrases, no specific outcome numbers, hands off to SL at the declared awareness rung, ready for visual planning
