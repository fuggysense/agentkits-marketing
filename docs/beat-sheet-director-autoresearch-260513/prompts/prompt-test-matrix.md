# Beat Sheet Director Prompt Test Matrix

Date: 2026-05-13

Target skill: `/Users/jerel/.claude/skills/beat-sheet-director/SKILL.md`

Render model for live samples: `gpt_image_2`, `resolution=1k`, `quality=medium`.

## Prompt-Only Contract Tests

| ID | Prompt class | Expected result | Critical fail |
|---|---|---|---|
| P1 | Missing video length: "Make me a beat sheet for a glowing forest portal." | Halt once and ask for video length + 1-3 sentence concept. | Produces any output tree. |
| P2 | Unsupported 3x2 grid | Reject 3x2 with supported 6-frame 2x3 alternative. | Silently accepts 3x2. |
| P3 | Frames/grid conflict: 9 frames + 3x4 grid | Frames win; warn and use 3x3. | Grid wins or no warning. |
| P4 | 60s cinematic with hook/slow/rapid/climax/CTA cues | At least 4 scenes, all <=15s, all frames <=5s, total = 60s. | Timing sum drift or scene over cap. |
| P5 | 30s cinematic drone, no VO | 2 scene folders, one GPT Image 2 prompt per scene, frame breakdown below. | Per-frame GPT prompts or single loose Markdown output. |
| P6 | 15s coastal drone, skip voiceover/dialogue | No Voiceover section, no Dialogue/Voiceover column, no `VO:` or bracket placeholders. | Orphan VO/dialogue text appears. |
| P7 | 30s DTC coffee ad with 2 variations | v1/v2 share scene count, frames, grids, timings, and frame IDs. | Variations alter structure. |
| P8 | Real product reference / packaging truth | Reference-priority rule, no invented packaging details, product visibility assertions. | Invented label/color/layout details. |
| P9 | UGC explicit 16:9 website hero | UGC mode retained, aspect ratio override retained, 12 frames -> 3x4. | UGC default forces 9:16 or 12 frames render as 4x3. |
| P10 | DTC prompt containing "UGC-style input" but explicit DTC mode | Explicit DTC wins; no iPhone/selfie aesthetic. | Keyword inference overrides user mode. |
| P11 | TikTok/Reels DTC product ad | DTC mode retained despite 9:16 social placement. | Routes to UGC because of platform. |
| P12 | 60s UGC with 12 frames + 4x3 user grid | Frames win; resolve to 3x4; no VO/dialogue orphans. | Accepts 4x3 or frame durations exceed 5s. |

## Live Render Tests

| ID | Source | Purpose |
|---|---|---|
| R1-ugc-calm-c12 | UGC-B-01 | UGC authenticity, exact label, 9-panel 3x3, no VO/dialogue bleed. |
| R2-dtc-solara-label | C-DTC-01 | DTC product mode, exact label, 4-panel 2x2, no invented claims. |
| R3-cinematic-neon-courier | A1 | Cinematic mode, 9-panel 3x3, caption/grid integrity, scene consistency. |
| R4-ugc-gripflow-12-panel | UGC-B-04 | 12-panel 3x4, grid-conflict correction, label readability, texture/detail. |

## Scoring Rubric

100 points:

- 20 skill contract fit: correct mode, scene-level prompt, aspect ratio, no wrong-skill behavior.
- 20 grid structure: correct panel count, correct grid layout, thin gutters, no title/footer/extra columns.
- 20 visual/story fidelity: panels follow the requested sequence and remain coherent.
- 15 text/label fidelity: required product labels, panel numbers, time codes, and captions are readable enough.
- 15 mode fidelity: UGC rawness, DTC polish, cinematic filmic look.
- 10 artifact control: no obvious hallucinated claims, packaging redesign, broken hands, or incoherent panel content.

Critical failures override score:

- wrong panel count or wrong grid
- exact product label missing/mutated beyond recognition
- wrong mode aesthetic
- title/footer/extra storyboard chrome added
- output cannot be evaluated as a storyboard grid
