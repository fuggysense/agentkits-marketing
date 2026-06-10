# Beat Sheet Director AutoResearch Round 3

Date: 2026-05-13

## Scope

Tested the annotated full-sheet beat-sheet workflow across four industries and styles using GPT-5.5 worker-generated prompts and built-in GPT image generation. No Higgsfield CLI was used.

## Rendered Samples

| Test | Aspect | Frames | Path | Result |
|---|---:|---:|---|---|
| Healthcare telehealth check-in | 4:5 | 6 | `renders/health-4x5-telehealth.png` | Pass |
| Street-food UGC grilled cheese | 9:16 | 6 | `renders/food-9x16-nightmarket.png` | Pass |
| Fintech fraud shield | 16:9 | 4 | `renders/fintech-16x9-fraud.png` | Pass |
| Fashion modular jacket | 1:1 | 9 | `renders/fashion-1x1-studio.png` | Partial |

## Findings

1. The updated annotation-lane structure works for 4- and 6-beat sheets. Healthcare, food, and fintech kept text outside the panels, used row-major order, and preserved readable beat rows.
2. Right-side annotation columns become too dense at 9 beats. The fashion sample followed the structure, but row wrapping clipped the final SFX at the bottom.
3. The text model obeyed the traversal contract well after the previous patch. Prompts consistently included row-major left-to-right, top-to-bottom order.
4. The visual model still needs a compact text budget. Long `Action:` sentences and multi-cue `SFX:` lists are the main failure source, not the panel imagery.

## Skill Changes Applied

- Added invariant `I20` to `beat-sheet-director/SKILL.md`.
- Added validation `V17`.
- Added annotation compactness rules:
  - `Action:` must be 3-7 words.
  - `SFX:` must be 1-2 cue phrases.
  - Avoid comma-heavy rows.
  - For 9+ beats, widen the right column to 34-40% or switch to a bottom annotation band.
- Added matching eval coverage in `beat-sheet-director/evals.json`.

## Next Test

Rerun the 1:1 fashion case with compact rows before using 9- or 12-frame sheets in production.
