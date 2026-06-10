# G4 Motion Evaluation

Case: G4 liquid-glass finance app onboarding

Read confirmed: yes

## Score

96 / 100

## Rubric Breakdown

| Category | Points | Score | Notes |
|---|---:|---:|---|
| Skill contract | 20 | 20 | Markdown provides a visual-only GPT Image prompt, explicit 9:16 target, four-frame 2x2 instruction, production breakdown, validation summary, and Seedance handoff. |
| Grid / layout | 20 | 20 | Rendered image is a clear 2x2 grid with four panels and black gutters. Each panel keeps the same centered phone product composition. |
| Subject / story fidelity | 20 | 19 | Strong match to the requested finance onboarding arc: empty dashboard, rising cards, organized insight cards, completed dashboard with highlighted tile. Minor deduction because panel 2's floating cards extend outside the phone and read slightly like external overlays rather than only an in-app morph. |
| No-text / UI abstraction control | 15 | 15 | No readable UI text, numbers, logos, captions, timestamps, panel labels, or brand marks are visible. Placeholder bars remain abstract. |
| Motion / app mode fidelity | 15 | 13 | The markdown gives contiguous explicit ranges and a plausible morph sequence from 0.0s to 15.0s. The still storyboard communicates app-state evolution well, though the rendered reference itself only implies motion and panel 2's external card emergence could be tightened for a more strictly screen-native app transition. |
| Artifact control | 10 | 9 | The image is clean and free of dense overlays, director notes, SFX/BGM text, captions, and timestamps. Minor risk: some tiny pill shapes could be interpreted as microcopy by a strict downstream evaluator, though they are not legible. |

## Critical Failures

None.

## Errors Logged

- No critical grid failure: the image is a four-panel 2x2 storyboard.
- No readable or invented UI copy/numbers detected.
- No wrong-subject failure: image and markdown are finance-app onboarding.
- No dense overlay text, captions, timestamps, director notes, SFX, or BGM visible in the rendered image.
- Storyboard is evaluable.

## Change Recommendations

1. Keep panel 2's morphing cards more clearly inside the phone screen bounds, or make their emergence visibly anchored to the screen glass, to avoid reading as unrelated overlay cards.
2. In future image prompts, replace very small horizontal pill marks with non-textual glints or abstract blocks when possible, reducing the chance that validators interpret them as hidden microcopy.
3. Keep the production table and Seedance handoff as written; the timing is explicit, contiguous, and suitable for downstream generation.
