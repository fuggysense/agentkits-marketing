# Beat Sheet Director Round 2 Summary

Date: 2026-05-13

Model profile: `gpt_image_2`, `resolution=1k`, `quality=medium`.

Run folder: `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/docs/beat-sheet-director-autoresearch-260513-round2`

## Workflow Tested

1. Fresh-context generator sub-agents created compact scene-level beat sheets.
2. Each generator rendered one visual-only GPT Image 2 storyboard image through Higgsfield.
3. Fresh-context evaluator sub-agents inspected one rendered image each plus its Markdown spec.
4. Evaluators scored against the updated contract: scene <= 15s, explicit time ranges, visual-only render, production breakdown, and Seedance handoff.

## Results

| Case | Use case | Render | Score | Critical failures |
|---|---|---|---:|---|
| G1 | UGC bathroom serum test | `renders/G1-ugc.png` | 96 | None |
| G2 | DTC sunscreen demo | `renders/G2-dtc.png` | 96 | None |
| G3 | Cinematic neon courier | `renders/G3-cinematic.png` | 96 | None |
| G4 | Motion/app promo | `renders/G4-motion.png` | 96 | None |
| G5 | Property walkthrough | `renders/G5-property.png` | 95 | None |

Average score: 95.8 / 100.

All five renders completed with the requested 1K medium profile:

| Case | Aspect | Dimensions |
|---|---|---|
| G1 | 9:16 | 752 x 1344 |
| G2 | 1:1 | 1024 x 1024 |
| G3 | 16:9 | 1344 x 752 |
| G4 | 9:16 | 752 x 1344 |
| G5 | 16:9 | 1344 x 752 |

## Errors Logged

### G1 UGC

- Panel 5 result beat was not distinct enough from the inspection/application beats.
- Product label was fully evaluable only in close product-facing panels; background/sink product instances were too small or angled.

### G2 DTC

- Panel 3 cropped/angled the tube during the squeeze demo, weakening the label lock.
- Validation wording should separate rendered-image constraints from downstream Seedance handoff content.

### G3 Cinematic

- Panel 3 pursuit cue could be more reflection-led.
- Panel 1 environmental signage pulled some attention, though it was not a production overlay.

### G4 Motion/App

- Panel 2's morphing cards should stay more clearly anchored inside the phone screen.
- Tiny pill marks should become abstract glints/blocks so validators do not read them as hidden microcopy.

### G5 Property

- Panel 2 and panel 4 repeat the balcony/view composition too much.
- Gutters are slightly heavier than ideal.
- Production breakdown includes one spoken agent line; remove it if downstream video must be no-dialogue.
- Singapore specificity could be stronger through non-text visual cues.

## Contract Drift Found

- G1 used `Range` instead of the exact `Time Range` column name.
- G1 carried Seedance handoff content inside a table column but did not create a dedicated `## Seedance handoff` section.
- Some generated specs used title/header variants like `GPT Image 2 Prompt` instead of the canonical `GPT Image 2 prompt (visual reference)`.

These are not render failures, but they show the skill should enforce canonical headings more tightly.

## Recommended Skill Changes

1. Add a stricter heading/schema check:
   - Required scene sections: `GPT Image 2 prompt (visual reference)`, `Production breakdown`, `Seedance handoff`.
   - Required production table column: `Time Range`, not `Range`.

2. Strengthen product-label lock:
   - If exact label text is required, specify which panels must carry readable label text.
   - In action/demo panels, either keep label flat/readable or explicitly turn the product away so unreadable microtext is not evaluated.

3. Tighten compact composition:
   - For app/motion boards, keep morphing UI elements inside the device unless the brief explicitly asks for out-of-screen dimensionality.
   - Replace tiny text-like UI marks with non-text glints, abstract blocks, or larger unlabeled shapes.

4. Clarify dialogue defaults:
   - Dialogue/VO belongs in Markdown handoff only.
   - If the user did not ask for spoken lines, default to `-` in Dialogue / Voiceover and keep ambient sound only.

5. Improve property specificity:
   - Require each property panel to own a distinct walkthrough beat.
   - Add non-text regional cues only when useful, without fake signage or readable labels.

## Verdict

The updated architecture is working: the rendered image stays clean and visual-only, while the Markdown carries the production detail for Seedance. The next improvement pass should focus on schema strictness and product-label handling, not on the core visual-only split.
