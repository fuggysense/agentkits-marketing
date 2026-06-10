# G5-property - Singapore Condo Walkthrough Scene

> Bright Singapore condo living room walkthrough - 15.0s, 1 scene, cinematic property mode. One render unit, 4 frames in a 2x2 grid, 16:9.

## GPT Image 2 prompt (visual reference)

Paste this single prompt into GPT Image 2 to render the full scene as a 2x2 grid:

> Create a 16:9 photorealistic cinematic real-estate walkthrough storyboard grid, 2x2 layout, four panels on a clean black canvas with thin black gutters only.
>
> Overarching scene theme: a bright modern Singapore condominium living room in midday tropical daylight, high-floor city view, warm neutral interiors, polished stone floor, pale wood accents, indoor plants, clean staging, one confident property agent in smart casual beige blazer and dark trousers. Keep the same room layout, agent identity, wardrobe, lighting direction, and upscale condo finish across all panels.
>
> Panels, left-to-right, top-to-bottom:
>
> Panel 1: the living room opens wide and airy, sofa and coffee table foreground, floor-to-ceiling windows glowing behind.
> Panel 2: the balcony doors are open, revealing a high-floor Singapore skyline view and lush balcony greenery.
> Panel 3: the kitchen island appears crisp and functional, pendant lights, integrated appliances, breakfast stools, tidy countertop.
> Panel 4: the property agent stands near the balcony threshold, arm extended in a welcoming gesture toward the view.
>
> Character: one Singapore property agent, early 30s, professional and approachable, neat dark hair, beige blazer, white shirt, dark trousers, natural expression.
>
> Environment: modern Singapore condo living room connected to balcony and open kitchen, Midday, Clear. Mood: Hopeful and premium. Visual style: clean property-commercial photorealism, bright natural daylight, accurate interior scale, realistic glass reflections, real fabrics, real surfaces, no exaggerated luxury fantasy.
>
> Camera/lens feel: shot on Sony FX3, Spherical Cooke lens, 24mm Wide, natural lens effects.
>
> Below each panel: no caption bands, no panel labels, no subtitles, no timestamps, no explanatory overlays.
>
> Forbidden: no title banner, no footer, no colored gridlines, no written labels, no visible UI, no captions, no timestamps, no dialogue text, no SFX or music text, no camera notes, no production table. Plain black canvas with four visual panels arranged in a 2x2 grid.
>
> Render at 16:9 aspect ratio.

---

## Production breakdown

Each row is one panel inside the scene. Use this as the shot-list source when generating downstream video clips. Time ranges are explicit, contiguous, and sum to 15.0s.

| Frame | Time Range | Tag | Visible Action | Motion / Camera Intent | Dialogue / Voiceover | SFX / Ambient Sound | Music Cue | Seedance Notes |
|---|---|---|---|---|---|---|---|---|
| v1.s1.f1 | 0.0s to 3.5s | SETUP | A bright condo living room fills the frame. The sofa, coffee table, windows, and balcony line establish the space. | Wide Establishing · Eye Level · Slow Dolly In | - | natural room tone, faint city ambience | minimal piano bed begins softly | Use @Image1 as room-layout lock. Start on living room width; preserve window wall, sofa placement, daylight direction, and polished-floor reflections. |
| v1.s1.f2 | 3.5s to 7.0s | REVEAL | Balcony doors open to a high-floor Singapore skyline. Greenery frames the view without blocking the city. | Medium Wide · Eye Level · Tracking | - | balcony door slide, soft outdoor ambience | minimal piano continues, slightly brighter | Continue from living room into balcony threshold. Lock skyline reveal and greenery placement; avoid text, signboards, and fake building logos. |
| v1.s1.f3 | 7.0s to 10.8s | FEATURE | The kitchen island is clean, bright, and ready for hosting. Pendant lights and stools show scale and function. | Medium Wide · High Angle · Static | - | gentle indoor ambience, subtle countertop touch | minimal piano holds steady | Shift attention to kitchen island. Preserve open-plan continuity from living room; keep island usable, uncluttered, and accurately proportioned. |
| v1.s1.f4 | 10.8s to 15.0s | CTA | The agent stands near the balcony and gestures warmly toward the view. The living room and skyline remain visible together. | Medium · Eye Level · Push In | Agent: "This is the view buyers remember." | natural room tone, faint city ambience | minimal piano resolves cleanly | End with agent gesture to view. Lock agent face, beige blazer, dark trousers, welcoming pose, balcony threshold, and skyline direction from @Image1. |

## Seedance handoff

- Render unit: this scene only; duration 15.0s, never over 15.0s.
- Visual ref: `docs/beat-sheet-director-autoresearch-260513-round2/renders/G5-property.png`.
- Prompt handle: `@Image1` = GPT Image 2 storyboard image. Lock only visible attributes owned by the image: agent identity and wardrobe, condo layout, balcony position, kitchen island placement, daylight direction, skyline reveal, interior material palette.
- Execution layer: put camera movement, cuts, physical motion, dialogue, SFX/ambient sound, music cue, and failure guardrails in the Seedance call sheet, not in the rendered beat-sheet image.
- Timeline source:
  - 0.0s to 3.5s: Slow dolly into the bright living room; establish layout, windows, balcony line, and premium staging.
  - 3.5s to 7.0s: Track toward the open balcony; reveal high-floor Singapore skyline and balcony greenery.
  - 7.0s to 10.8s: Cut to kitchen island; hold a clean feature shot with pendant lights, stools, and integrated appliances.
  - 10.8s to 15.0s: Push in on agent at balcony threshold; agent gestures to the view and delivers the single spoken line.
- Guardrails: no visible captions, no subtitles, no timestamps, no UI overlays, no invented real-estate claims, no readable fake signage, no warped kitchen geometry, no duplicated agent.

## Validation summary

- V1 No placeholder tokens: pass.
- V2 Required values resolved: pass.
- V3 Time sum = 15.0s: pass.
- V4 Scene duration <= 15.0s: pass.
- V5 Each frame duration <= 5.0s: pass.
- V6 4 frames maps to 2x2 grid: pass.
- V7 Voiceover skipped; one agent dialogue line only in production breakdown: pass.
- V8 Variation lock not applicable for single variation: pass.
- V9 Aspect ratio appears in opening clause and render line: pass.
- V10 Cinematic metadata disabled: pass.
- V11 Timestamp ranges are explicit: pass.
- V12 GPT Image 2 prompt is visual-only and forbids rendered text overlays: pass.
