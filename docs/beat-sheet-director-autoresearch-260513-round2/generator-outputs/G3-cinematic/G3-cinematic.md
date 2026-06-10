# Scene 1 - First Sign of Pursuit · v1

> Variation 1 of 1. Time range: 0.0s to 12.0s. Duration: 12.0s. 6 frames in 2x3 grid. Tag: [SETUP] to [ESCALATION].

## GPT Image 2 prompt (visual reference)

Paste this single prompt into GPT Image 2 to render the full scene as a 2x3 grid:

> Create a 16:9 live-action cinematic photoreal storyboard grid for Scene 1 of "Neon Memory Courier" - 2x3 layout, 6 panels on a clean black canvas, panels separated by thin black gutters only.
>
> Overarching scene theme: A tense cyberpunk noir alley at Neon Night during heavy rain, pavement glossy with reflected magenta and cyan signage. The same courier appears in every panel: young adult, androgynous build, wet black hooded raincoat, dark utility sling bag, fingerless gloves, alert expression. The courier carries one small transparent hard-shell memory chip case glowing electric blue from within. Keep the case, wardrobe, alley geometry, wet reflections, and neon palette consistent across all panels. Show the first sign of pursuit building from quiet suspicion to visible threat.
>
> Panels, left-to-right, top-to-bottom:
>
> Panel 1: The courier steps into a narrow rain-slick service alley, shoulders hunched beneath neon spill.
> Panel 2: A gloved hand opens the sling bag just enough to reveal the glowing memory chip case.
> Panel 3: The courier pauses beside a puddle, noticing a second silhouette reflected far behind.
> Panel 4: The blue case lights the courier's tense face as rain beads on the transparent shell.
> Panel 5: A red scanner beam sweeps across wet brick behind the courier's shoulder.
> Panel 6: The courier snaps the case shut and turns toward the alley exit as two pursuers emerge in haze.
>
> Character: one courier with wet black hooded raincoat, dark utility sling bag, fingerless gloves, rain-darkened hair partly hidden by hood, sharp anxious eyes; two distant pursuers only as indistinct dark silhouettes with red visor glints.
>
> Environment: rain-slick alley, Neon Night, Heavy Rain. Mood: Tense. Visual style: live-action cinematic photorealism, shot on ARRI Alexa 65 with IMAX 70mm lenses, prestige cyberpunk noir, naturalistic volumetric lighting, deep cinematic shadows, subtle film grain, muted color grading, readable faces and silhouettes.
>
> Camera/lens feel: ARRI Alexa 65, Anamorphic Primo, 50mm Standard, Natural Flares.
>
> Below each panel: no captions, no timestamps, no action text; optional tiny white panel number in one corner only if needed for sequence clarity.
>
> Forbidden: no title banner, no footer, no colored gridlines, no director's note, no VO/dialogue text, no SFX/BGM/music cue, no camera-movement commands, no production tables. Plain black canvas with 6 visual panels arranged in 2x3.
>
> Render at 16:9 aspect ratio.

---

## Production breakdown

Each row is one panel inside the scene. Use this as the shot-list source when generating downstream video clips. Time ranges are explicit and contiguous.

| Frame | Time Range | Tag | Visible Action | Motion / Camera Intent | SFX / Ambient Sound | Music Cue | Seedance Notes | Cinematic Metadata |
|---|---|---|---|---|---|---|---|---|
| v1.s1.f1 | 0.0s to 2.0s | [SETUP] | The courier enters a narrow wet alley. Neon reflections ripple under each step. | Wide Establishing · Eye Level · Slow Dolly In | heavy rain on metal vents and pavement | dark ambient drone begins low | Use @Image1 as visual reference. Lock alley layout, wet neon palette, courier wardrobe, and case location in bag. | transition: cut in from black · motion: controlled forward drift · rhythm: slow tense setup · motif: blue case glow hidden |
| v1.s1.f2 | 2.0s to 4.0s | [SETUP] | The sling bag opens slightly. The blue memory chip case glows inside. | Close-Up · Low Angle · Static | rain patter with faint electrical hum | drone adds thin synth pulse | Use @Image1 for prop continuity. Keep case small, transparent, hard-shell, electric blue glow; no readable labels. | transition: hard cut · motion: held detail · rhythm: quiet reveal · motif: blue light against black fabric |
| v1.s1.f3 | 4.0s to 6.0s | [ESCALATION] | The courier stops at a puddle. A distant second silhouette appears in reflection. | Medium Close · High Angle · Push In | rain splashes into puddle; distant footstep implied | pulse grows slightly | Convert reflection beat into Seedance action: courier notices the reflected shape before looking back. | transition: match cut on blue reflection · motion: subtle push toward puddle · rhythm: suspicion beat · motif: doubled silhouettes |
| v1.s1.f4 | 6.0s to 8.0s | [ESCALATION] | Blue case light washes over the courier's tense face. Rain beads on the transparent shell. | Close-Up · Eye Level · Handheld | breath, rain, soft case latch movement | drone tightens | Lock face readability and prop glow. The courier's expression shifts from focus to alarm. | transition: cut to face · motion: slight handheld tension · rhythm: held reaction · motif: blue glow on skin |
| v1.s1.f5 | 8.0s to 10.0s | [PEAK] | A red scanner beam crosses wet brick behind the courier. The courier freezes mid-turn. | Over Shoulder · Dutch 15° · Whip Pan | rain plus scanner sweep tone | pulse spikes briefly | Use red beam as first unmistakable pursuit sign. Keep pursuers mostly offscreen until final frame. | transition: snap pan · motion: fast lateral sweep · rhythm: alarm spike · motif: red threat crossing blue world |
| v1.s1.f6 | 10.0s to 12.0s | [FINAL] | The courier snaps the case shut and pivots toward the alley exit. Two pursuers emerge through haze. | Medium Wide · Low Angle · Tracking | rain intensifies; boots hit puddles | drone drops to unresolved hit | End frame should be a Seedance handoff endpoint: courier ready to run, pursuers newly visible, case secured. | transition: cut on case snap · motion: tracking retreat · rhythm: launch point · motif: blue case hidden, red visors appear |

## Seedance handoff

- **Render unit:** Scene 1 only; duration 12.0s, never over 15.0s.
- **Visual ref:** generated GPT Image 2 storyboard image for this `G3-cinematic.md`.
- **Prompt handle:** `@Image1` = the storyboard image or selected panel crop. Lock only visible attributes the image owns: courier wardrobe, glowing blue memory chip case, rain-slick alley geometry, neon color palette, wet reflections, red pursuit signal, and final pursuer silhouettes.
- **Execution layer:** Put camera movement, cuts, physical motion, ambient sound, music cue, and failure guardrails in the Seedance call sheet, not in the rendered beat-sheet image.
- **Timeline source:** Convert the production breakdown rows into Seedance ranges:
  - `0.0s to 2.0s`: Slow forward alley entry; courier cautious, blue case still concealed.
  - `2.0s to 4.0s`: Close detail reveal of the glowing case inside the bag.
  - `4.0s to 6.0s`: Reflection reveals the first shadow behind the courier.
  - `6.0s to 8.0s`: Courier face reaction lit by the case glow.
  - `8.0s to 10.0s`: Red scanner beam announces pursuit.
  - `10.0s to 12.0s`: Courier pivots to escape as pursuers emerge.

## Validation summary

- V1 No `[unset]` tokens pass
- V2 All required variables resolved pass
- V3 Time sum = 12.0s pass
- V4 Scene duration <= 15.0s pass
- V5 All frames <= 5.0s pass
- V6 6 frames maps to 2x3 grid pass
- V7 Voiceover skipped; no dialogue or VO column pass
- V8 Variation lock N/A for one variation pass
- V9 Aspect ratio appears in opening clause and render line pass
- V10 Cinematic metadata uniform pass
- V11 Timestamp ranges explicit pass
- V12 Image prompt visual-only pass
