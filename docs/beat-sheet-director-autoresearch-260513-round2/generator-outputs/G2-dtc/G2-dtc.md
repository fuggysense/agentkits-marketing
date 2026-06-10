# G2-dtc — Solara SPF 50 Bathroom Ledge Demo

> Polished DTC product ad scene for a mineral sunscreen tube labeled exactly "SOLARA SPF 50" on a bathroom stone ledge, moving from ledge reveal to squeeze demo to final hero. 12.0s, 1 scene, DTC mode, 1:1, 4 frames in a 2x2 grid.

## GPT Image 2 prompt (visual reference)

Paste this single visual-only prompt into GPT Image 2 to render the full scene as a 2x2 grid:

> Create a 1:1 clean DTC commercial, Sony FX3, 35mm prime lens, soft natural daylight, polished color grading, brand-forward storyboard grid for Scene 1 of "Solara SPF 50 Bathroom Ledge Demo" — 2x2 layout, 4 panels on a clean black canvas, panels separated by thin black gutters only.
>
> Overarching scene theme: a premium mineral sunscreen product demo in a calm modern bathroom. The same matte off-white squeeze tube sits on a pale limestone bathroom ledge beside a softly blurred chrome faucet and warm neutral tile. Soft morning daylight comes from frame left, creating clean highlights, gentle shadows, and accurate product color. Product packaging stays consistent across all panels, and the readable tube label is exactly "SOLARA SPF 50".
>
> Panels (left-to-right, top-to-bottom):
>
> Panel 1: The SOLARA SPF 50 tube rests upright on the stone ledge with a clean bathroom reflection behind it.
>
> Panel 2: A well-groomed hand reaches in and tilts the tube toward camera, label still readable.
>
> Panel 3: The hand squeezes a neat ribbon of white mineral sunscreen onto two fingertips above the ledge.
>
> Panel 4: Final hero composition with the tube standing beside the smooth sunscreen ribbon on the stone ledge.
>
> Product label lock: the only readable product text is exactly "SOLARA SPF 50". Keep the label large, straight, flat to camera, and readable in product-facing panels. Do not add extra words, logos, badges, seals, ratings, certifications, slogans, SPF claims beyond the exact label, reef-safe claims, water-resistant claims, medical claims, or decorative marketing copy.
>
> Claim hygiene: no additional readable text anywhere in the image except "SOLARA SPF 50" on the tube. Avoid visual or written performance claims, clinical symbols, doctor-approved cues, award badges, sustainability cues, or before/after implications.
>
> Action evidence: at least two panels show active product use, including hand interaction and squeeze texture.
>
> Environment: modern bathroom stone ledge, Midday, Clear. Mood: Hopeful. Visual style: clean DTC commercial photography, premium skincare ad, soft natural daylight, polished warm-neutral grade, shallow but not aggressive depth of field, realistic hand texture, real bathroom materials, accurate product color.
>
> Camera/lens feel: shot on Sony FX3, Spherical Cooke, 50mm Standard, natural.
>
> Below each panel: no caption bands, no subtitles, no timestamps, no panel numbers, no explanatory overlays.
>
> Forbidden: no title banner, no footer, no colored gridlines, no director's note, no VO or dialogue text, no SFX or music cue, no camera-movement commands, no production tables, no overlay text, no timestamps. Plain black canvas with 4 visual panels arranged in 2x2, and the only readable text is the product label "SOLARA SPF 50".
>
> Render at 1:1 aspect ratio.

---

## Production breakdown

Each row is one panel inside the scene. Use this as the shot-list source when generating downstream video clips. Time ranges are explicit and contiguous.

| Frame | Time Range | Tag | Visible Action | Motion / Camera Intent | SFX / Ambient Sound | Music Cue | Seedance Notes |
|---|---|---|---|---|---|---|---|
| v1.s1.f1 | 0.0s to 3.0s | HOOK | The SOLARA SPF 50 tube rests upright on the stone ledge. The bathroom reflection stays soft and uncluttered. | Close-Up · Eye Level · Static | natural room tone; faint bathroom ambience | Minimal piano, soft opening pulse | Start from @Image1 panel 1. Lock tube shape, label text, stone ledge, daylight direction, and bathroom material palette. |
| v1.s1.f2 | 3.0s to 6.0s | VALUE | A well-groomed hand enters and tilts the tube toward camera. The label remains flat, centered, and readable. | Medium Close · Eye Level · Slow Dolly In | natural room tone; subtle hand contact on matte tube | Minimal piano, gentle lift | Continue from @Image1 panel 2. Preserve exact label "SOLARA SPF 50"; no added package text or badges. |
| v1.s1.f3 | 6.0s to 9.0s | DEMO | The hand squeezes a clean ribbon of white mineral sunscreen onto two fingertips. The product texture looks creamy and controlled. | Extreme Close · High Angle · Push In | natural room tone; soft squeeze and fingertip contact | Minimal piano, tactile accent | Use @Image1 panel 3 as the demo reference. Emphasize real squeeze physics, stable hand anatomy, and clean product texture. |
| v1.s1.f4 | 9.0s to 12.0s | CTA | The tube stands beside the sunscreen ribbon on the stone ledge. The final hero frame feels polished and brand-forward. | Close-Up · Eye Level · Static | natural room tone; room settles quiet | Minimal piano, resolved final note | End on @Image1 panel 4. Lock final hero composition, readable exact label, product scale, and no extra claims or overlays. |

## Seedance handoff

- Render unit: this scene only; duration 12.0s, never over 15.0s.
- Visual ref: generated GPT Image 2 storyboard image for this `G2-dtc.md`.
- Prompt handle: `@Image1` = the storyboard image or selected panel crop. Lock only visible attributes the image owns: product/package shape, exact label text, bathroom stone ledge, hand grooming, sunscreen texture, room layout, lighting direction, and start/end composition.
- Execution layer: put camera movement, cuts, physical hand motion, squeeze pressure, texture behavior, SFX/ambient sound, music cue, and failure guardrails in the Seedance call sheet, not in the rendered beat-sheet image.
- Timeline source:
  - 0.0s to 3.0s: Static close product reveal on stone ledge; no overlays; exact label readable.
  - 3.0s to 6.0s: Hand enters and tilts tube toward camera; maintain packaging continuity.
  - 6.0s to 9.0s: Tight squeeze demo; sunscreen ribbon forms on fingertips with believable pressure and texture.
  - 9.0s to 12.0s: Final hero hold; tube and sunscreen ribbon share frame; no extra claims or text.

## Validation summary

- V1 No unset tokens: pass
- V2 Required values resolved: pass
- V3 Time sum = 12.0s: pass
- V4 Scene duration <= 15.0s: pass
- V5 Frame durations <= 5.0s: pass
- V6 4 frames maps to 2x2 grid: pass
- V7 Voiceover skipped; no dialogue column: pass
- V8 Variation lock not applicable for single variation: pass
- V9 Aspect ratio appears in opening clause and Render at line: pass
- V10 Cinematic metadata disabled: pass
- V11 Timestamp ranges explicit and contiguous: pass
- V12 GPT Image 2 prompt is visual-only; no audio, VO, motion commands, or production table rendered into image: pass
