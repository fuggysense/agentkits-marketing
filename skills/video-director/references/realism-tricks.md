# Realism Tricks for AI Video Generation

Universal realism rules extracted from proven AI video ad prompts. These techniques make AI-generated video look like native UGC content shot on a phone, not polished studio production.

---

## Camera Realism

The #1 giveaway of AI video is "too perfect" camera work. Real UGC has imperfections.

### Handheld & Phone Characteristics
- **Micro-jitters**: Specify "subtle handheld shake" or "natural micro-jitters" — never perfectly stabilized
- **Imperfect framing**: Subject slightly off-center, occasional head cutoff at top of frame
- **iPhone compression artifacts**: Reference "iPhone 15 Pro" or "smartphone camera quality" for authentic digital look
- **Auto-focus hunting**: Brief moments of soft focus, especially on close-ups
- **Rolling shutter**: Slight wobble on fast pans (matches phone cameras)

### Camera Movement
- **Slow natural drift**: Camera drifts slightly even when "still" — mimics hand-held
- **Organic pans**: Not smooth dolly shots — human-speed pans with slight acceleration/deceleration
- **No crane shots**: Avoid anything that screams "production crew" unless deliberately cinematic
- **Selfie-arm distance**: For talking-head, maintain realistic arm's-length distance (~18-24 inches)

### Lens Simulation
- **Slight barrel distortion**: Wide-angle phone lens effect, especially at edges
- **Shallow DoF on portrait mode**: Simulated bokeh with occasional edge artifacts (like real phone portrait mode)
- **Lens flare on bright sources**: Natural, not cinematic — small, subtle

---

## Skin & Body Realism

AI models tend to create "perfect" people. Fight this aggressively.

### Skin
- **Visible pores**: Always specify "natural skin texture with visible pores"
- **Micro-imperfections**: Subtle acne scars, moles, uneven skin tone
- **Natural shine**: Slight oiliness on forehead/nose, not matte-perfect
- **Under-eye shadows**: Real people have them, especially on camera

### Body & Movement
- **Asymmetry**: Slightly uneven eyebrows, one ear slightly higher
- **Natural hair**: Loose strands, flyaways, not salon-perfect
- **Clothing wrinkles**: Fabric creases, slightly untucked edges
- **Weight shift**: Standing people shift weight, adjust posture
- **Micro-expressions**: Eyebrow raises, lip pursing between sentences

### Hands (Critical)
- **Natural positioning**: Hands resting naturally, not perfectly posed
- **Gestural imperfection**: Gestures that don't perfectly sync with speech
- **Finger count**: Always specify "anatomically correct hands with five fingers" in prompt AND negative prompt ("no extra fingers, no missing fingers")

---

## Environmental Realism

Backgrounds make or break the UGC feel.

### Indoor Settings
- **Mixed lighting**: Overhead fluorescent + window light = realistic office/home
- **Background clutter**: Bookshelves, coffee mugs, slightly messy desk
- **Depth blur**: Background slightly out of focus (phone camera behavior)
- **Ambient noise references**: "faint air conditioning hum" or "distant keyboard typing" — helps models understand the environment even if they don't generate audio

### Outdoor Settings
- **Pedestrians**: Background people walking, not frozen
- **Wind effects**: Hair movement, flag flutter, tree sway
- **Traffic sounds**: Referenced for context even in video-only generation
- **Inconsistent lighting**: Clouds passing = light variation on face

### Street/Public Spaces
- **Crowd density**: Specify roughly how busy — "moderately busy sidewalk" vs "quiet residential street"
- **Signage**: Period-appropriate, locale-appropriate background signs
- **Ground texture**: Wet pavement after rain, cracked sidewalk, worn asphalt

---

## Negative Prompt Library

Negative prompts are as important as positive prompts. Organize by category.

### Anti-Cinematic (for UGC-style)
```
cinematic lighting, dramatic shadows, lens flare, anamorphic,
film grain, color grading, teal and orange, movie-like,
professional studio lighting, three-point lighting, rim light,
dolly zoom, crane shot, steadicam, gimbal-smooth
```

### Anti-Polished (for authenticity)
```
airbrushed skin, perfect skin, porcelain skin, smooth skin,
perfect hair, salon-styled, model-perfect, retouched,
professional makeup, studio backdrop, infinite white background,
stock photo, corporate headshot, posed, staged
```

### Anti-AI-Looking (universal)
```
extra fingers, missing fingers, deformed hands, extra limbs,
blurry face, distorted features, uncanny valley, plastic skin,
watermark, signature, text overlay, logo, border,
cartoon, anime, 3D render, CGI, illustration, painting,
oversaturated, HDR, hyper-realistic (paradoxically makes it look more AI)
```

### Anti-Commercial (for native feel)
```
product placement, brand logo visible, commercial lighting,
advertising aesthetic, catalog photo, e-commerce white background,
call to action overlay, promotional text, banner
```

---

## Platform-Specific Realism Notes

### TikTok Native
- **Vertical 9:16 mandatory** — anything else screams "repurposed"
- **In-app text overlays**: Reference TikTok's built-in text style if adding captions
- **Stitch/Duet framing**: Can simulate split-screen for reaction-style content
- **Quick cuts**: 2-4 second clips stitched together, not long takes
- **Front-facing camera default**: Most TikTok is selfie-cam, not rear camera

### Instagram Reels
- **9:16 but slightly more polished** than TikTok — Instagram users expect marginally higher production
- **Ring light acceptable**: Instagram creators commonly use ring lights, so subtle ring-light catchlights are fine
- **Color-corrected but not graded**: Light editing, not full cinematic color grade
- **Smooth transitions ok**: Instagram audiences are used to planned transitions

### YouTube Shorts
- **9:16 format** but can have higher production than TikTok
- **Rear camera acceptable**: YouTube shorts are more varied in camera perspective
- **Slightly longer takes**: YouTube audiences tolerate 5-10 second single shots
- **B-roll inserts**: More common on YouTube than TikTok

### Facebook/Meta Feed
- **1:1 or 4:5 aspect ratio** for feed (not 9:16 unless Stories/Reels)
- **Captions critical**: 85% of Facebook video is watched without sound
- **Slightly older demographic**: Adjust subject age/setting accordingly
- **Longer attention span**: Can hold shots 3-5 seconds vs TikTok's 1-2 seconds

---

## Character Consistency Framework

For multi-shot sequences, copy this character block into EVERY prompt to maintain consistent appearance:

```
[NAME/ROLE], a [AGE]-year-old [ETHNICITY] [GENDER] with [HAIR COLOR/STYLE],
[EYE COLOR], [DISTINGUISHING FEATURES like moles, scars, facial hair],
[BUILD/HEIGHT], wearing [SPECIFIC CLOTHING with colors and details],
with [POSTURE DESCRIPTION], expressing [EMOTION/ENERGY LEVEL]
```

### Character Consistency Rules
- Be specific about UNCHANGING features (bone structure, eye color, skin tone) not just clothing
- Describe the same clothing in identical terms across prompts — "navy crew-neck sweater" not "blue top"
- Include at least 2 distinguishing marks (mole on left cheek, scar on chin) for the model to anchor on
- Energy/emotion can change per shot, but physical description stays verbatim

---

## Transition Realism

For transformation, before/after, and timelapse-style videos:

### Physical Actions Over Morphing
- Describe realistic construction/renovation/application actions, not magical transitions
- "Workers install new cabinets, paint walls, lay flooring" beats "room magically transforms"
- The viewer should be able to imagine HOW the change happened physically

### Phased Timing Structure
- **Setup:** Establish the before state (2-3 seconds)
- **Construction/Action:** Show the change happening (5-8 seconds)
- **Reveal:** Show the completed after state (2-3 seconds)

### Lighting Evolution
- As spaces transform, lighting should evolve naturally
- Old state: flat fluorescents, dim, unflattering
- Mid-transition: construction lighting, mixed sources
- New state: warm recessed lighting, natural daylight, designed ambiance

### Sound Design as Comprehension Tool
- Describe sounds to help the model understand what physical actions are occurring
- "Sound of power drill, hammering, paint roller on wall" → model generates construction-like motion
- Works even when the model can't generate actual audio

---

## Negative Prompt Format Guide

### Best Practice: List Unwanted Elements Directly

Instead of using "no" or "don't" language, list unwanted elements as bare terms:

**Do this:**
```
cinematic lighting, studio setup, airbrushed skin, extra fingers, stock photo
```

**Not this:**
```
no cinematic lighting, don't use studio setup, avoid airbrushed skin
```

Some models interpret "no X" as emphasis on X. Listing bare terms in the negative prompt field is more reliable.

### Negative Prompt by Video Type

| Type | Critical Negatives |
|------|-------------------|
| UGC/Talking Head | cinematic, studio, teleprompter, perfect framing, airbrushed |
| Product | floating product, CGI, white void, commercial lighting, stock |
| Food | plastic food, artificial, stock photo, fast food chain |
| Real Estate | CGI, miniature, dollhouse, unrealistic, stock |
| Educational | cartoon, horror, gore, inaccurate anatomy |
| All Types | extra fingers, missing fingers, watermark, text overlay, blurry face |

---

## Quick Realism Checklist

Before finalizing any video prompt:

- [ ] Camera type specified (iPhone, handheld, selfie-cam)?
- [ ] Micro-imperfections included (skin texture, hair, clothing)?
- [ ] Environment has depth and detail (not blank backdrop)?
- [ ] Negative prompts block common AI tells?
- [ ] Aspect ratio matches target platform?
- [ ] Movement is natural, not robotic or perfectly smooth?
- [ ] Hands described carefully with finger count?
- [ ] Lighting matches the claimed environment (not studio-perfect)?

---

*Source: Realism patterns extracted from David Roberts (AI Ad Guys) prompt collection — @recap_david on X/Twitter. Universal across Sora 2 Pro, Kling, VEO, and Nano Banana.*
