# G4 Motion — Liquid Glass Finance App Onboarding

> Compact motion/app promo beat-sheet scene. Time range: 0.0s to 15.0s. Duration: 15.0s. 4 frames in 2x2 grid. Aspect ratio: 9:16. Tag: APP_PROMO.

## GPT Image 2 Prompt

Use this single visual-only prompt for the rendered storyboard reference:

> Create a 9:16 clean DTC motion-design storyboard grid for a premium finance app onboarding sequence: 2x2 layout, 4 panels on a plain black canvas, thin black gutters only, no panel labels, no captions, no timestamps, no title banner, no footer, no visible words.
>
> Overarching scene theme: a liquid-glass mobile finance interface evolves from an empty dashboard into clear spending insight cards. The same tall smartphone screen is centered in every panel, floating against a soft graphite background with subtle reflections, translucent frosted-glass cards, gentle cyan and mint highlights, precise rounded rectangles, and polished app-store promo quality. Use abstract interface blocks only: simple bars, circles, charts, cards, and icon-like shapes. Avoid tiny unreadable UI text and avoid any legible typography.
>
> Panels, read left-to-right, top-to-bottom:
>
> Panel 1: an empty onboarding dashboard shows a frosted glass phone screen with only soft placeholder blocks and a calm blank state.
>
> Panel 2: translucent liquid-glass cards begin rising from the lower screen area, with simple abstract spending blocks forming in layers.
>
> Panel 3: the dashboard morphs into organized insight cards, including smooth rounded graph shapes, category dots, and clean budget tiles without text.
>
> Panel 4: the final app screen feels complete and reassuring, with balanced spending insight cards, one highlighted savings tile, and a subtle glow around the active card.
>
> Environment: premium studio product render, soft graphite background, clear weather equivalent, midday studio light. Mood: hopeful, focused, clean. Visual style: polished app promo, photorealistic glass material, sharp interface geometry, restrained cyan and mint accent colors, high-end fintech aesthetic.
>
> Camera/lens feel: Sony FX3-inspired product render, spherical 50mm standard lens feel, natural reflections, crisp depth, no motion blur.
>
> Forbidden: no readable UI text, no numbers, no logo, no brand name, no captions, no overlays, no subtitles, no timestamps, no panel numbers, no hands, no people, no director notes, no sound cues, no music cues, no camera movement commands, no production table. Plain black canvas with 4 visual panels arranged in a 2x2 grid.
>
> Render at 9:16 aspect ratio.

## Production Breakdown

Each row is one panel inside the scene. Use this as the shot-list source when generating downstream video clips. Time ranges are explicit, contiguous, and sum to 15.0s.

| Frame | Time Range | Tag | Visible Action | Motion / Camera Intent | SFX / Ambient Sound | Music Cue | Seedance Notes |
|---|---|---|---|---|---|---|---|
| v1.s1.f1 | 0.0s to 3.5s | SETUP | The phone opens on an empty liquid-glass dashboard. Placeholder blocks breathe softly in a calm blank state. | Medium Close · Eye Level · Static with very slow push-in | soft glass hum, quiet room tone | minimal warm synth pad begins | Use @Image1 as visual reference. Start with the Panel 1 composition; lock phone position, graphite background, and glass material. |
| v1.s1.f2 | 3.5s to 7.0s | BUILD | Frosted cards rise from the bottom of the screen. Abstract spending blocks begin forming in stacked translucent layers. | Close-Up · Eye Level · Slow Dolly In | gentle liquid swipe, soft card lift | synth pad adds light pulse | Morph from Panel 1 toward Panel 2. Animate cards as fluid glass sheets; no text or numbers appear. |
| v1.s1.f3 | 7.0s to 11.0s | REVEAL | The interface organizes into insight cards. Rounded graph shapes, category dots, and budget tiles align cleanly. | Close-Up · High Angle · Tracking micro-shift | precise UI ticks, soft glass settling | subtle beat enters under synth | Continue morph into Panel 3. Prioritize clean alignment, legible abstract shapes, and no readable typography. |
| v1.s1.f4 | 11.0s to 15.0s | RESOLUTION | The final dashboard feels complete and reassuring. One savings tile glows while the remaining insight cards sit balanced and clear. | Medium Close · Eye Level · Static hold | soft confirmation chime, ambient glass shimmer | music resolves with soft uplift | End on Panel 4. Hold a polished completed-screen composition suitable for a final frame or product hero. |

## Seedance Handoff

- Render unit: this scene only; duration 15.0s, never over 15.0s.
- Visual ref: `G4-motion.png` generated from the GPT Image 2 storyboard prompt above.
- Prompt handle: `@Image1` = the 2x2 storyboard image. Lock only visible attributes the image owns: centered phone silhouette, liquid-glass material, graphite background, cyan/mint accent palette, abstract card hierarchy, and final highlighted insight tile.
- Execution layer: put camera movement, card morphing, timing, SFX, and music in the Seedance call sheet, not in the rendered beat-sheet image.
- Timeline source:
  - 0.0s to 3.5s: Begin on empty frosted dashboard; near-static phone with subtle breathing placeholders.
  - 3.5s to 7.0s: Cards rise and stretch like liquid glass; spending blocks form without text.
  - 7.0s to 11.0s: Interface snaps into clean insight cards; graph shapes and category dots align.
  - 11.0s to 15.0s: Final dashboard holds; one savings tile glows softly as the app feels resolved.

## Validation Summary

- V1 No unset tokens: pass
- V2 Required variables resolved: pass
- V3 Time sum = 15.0s: pass
- V4 Scene duration <= 15.0s: pass
- V5 All frames <= 5.0s: pass
- V6 4 frames map to 2x2 grid: pass
- V7 Voiceover skipped with no dialogue column: pass
- V8 Variation lock not applicable: pass
- V9 Aspect ratio appears in opening and render line: pass
- V10 Cinematic metadata disabled: pass
- V11 Timestamp ranges explicit: pass
- V12 Image prompt is visual-only: pass
