## Graph Links
- **Parent skill:** [[video-director]]
- **Sibling references:** [[character-bible-template]], [[cinematography-reference]], [[client-campaign-audit]], [[model-selection-guide]], [[seed-management]], [[video-type-catalog]]
- **Related skills:** [[image-generation]], [[script-skill]], [[campaign-runner]]

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

### Two Methods for Character Consistency

**Method 1: Sora Characters API** (Sora 2 Pro only)
- Upload reference image → get `@username` handle → reference in prompts
- Max 2 characters per generation via API
- Best for: multi-clip sequences, 1min+ content, recurring characters
- See: `references/character-bible-template.md` for full API documentation

**Method 2: Text-Based Character Block** (All models)
- Copy the character block verbatim into every prompt
- Works with Sora, Kling, VEO — any model that accepts text
- Best for: one-off sequences, multi-model workflows, more than 2 characters
- See: `references/character-bible-template.md` for facial profile + context templates

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

## Post-Production Pipeline

After generating video clips, enhance with this toolchain:

### Step 1: Grain & Texture (CapCut / DaVinci Resolve)
- Add subtle film grain to fight the "too clean" AI look
- Adjust exposure for slight highlights blow-out (natural phone camera behavior)
- Add subtle lens vignette if not present

### Step 2: Upscale (Topaz Video AI)
- Upscale 1.25x to 1.75x — NOT more (over-upscaling looks artificial)
- Use "natural" mode, not "enhance" (enhance over-sharpens)
- Maintains detail without introducing AI upscaling artifacts

### Step 3: Voice & Audio (11 Labs / ElevenLabs)
- Generate voice-over for talking head clips
- Match voice to character profile (age, gender, energy level)
- Add room tone / ambient noise to match the visual environment
- Layer under the voice: keyboard clicks, traffic hum, café noise (per scene)

### Result
Raw AI clip → grain + texture → upscale → voice/audio = production-ready video that passes as real footage.

---

## Emotional Block Dialogue Cues

Structure dialogue in "emotional blocks" — each block has one dominant emotion and transitions naturally to the next:

```
BLOCK 1 — CURIOSITY (0:00-0:04)
Speaker leans forward, eyes slightly squinted, speaks slowly:
"Have you ever noticed how the best ads don't feel like ads?"
[Beat — slight pause, head tilt]

BLOCK 2 — CONFIDENCE (0:04-0:08)
Speaker straightens up, gestures with open palm, pace increases:
"That's because they're built on one simple principle..."
[Slight smile, eyebrow raise]

BLOCK 3 — CONVICTION (0:08-0:12)
Speaker points at camera, lowers voice slightly:
"Real stories from real people. That's it. That's the secret."
[Nods slowly, maintains eye contact]
```

### Why Emotional Blocks Work
- Models interpret emotional cues as acting direction → more natural facial expressions
- Each block gives the model a clear "beat" to play → better pacing
- Transitions between emotions feel human (curiosity → confidence → conviction is a natural arc)

### Block Transition Patterns
| From → To | Feels Like | Physical Cue |
|-----------|-----------|-------------|
| Curiosity → Confidence | "I figured it out" | Lean back, shoulders drop, slight smile |
| Surprise → Excitement | "Wait, this is amazing" | Eyes widen, lean forward, hands come up |
| Frustration → Resolution | "Here's what finally worked" | Head shake → nod, tension release |
| Calm → Urgency | "But here's the thing..." | Lean in, pace quickens, finger point |

---

## Weak → Strong Prompt Transformations

Turn vague prompts into high-quality outputs by following these transformation patterns:

| Weak Prompt | Problem | Strong Prompt |
|------------|---------|---------------|
| "A woman talking to camera" | No specificity | "A 28-year-old woman with dark wavy hair, wearing a sage green linen shirt, speaking directly to camera from a sunlit kitchen, iPhone selfie-cam at arm's length, slight natural shake" |
| "Product on a table" | No context or action | "Hands slide a matte black subscription box across a wooden dining table, pause, then carefully lift the magnetic lid. Warm window light from the left, shallow depth of field. Sound: satisfying magnetic click, tissue paper rustle" |
| "Someone reacting to something" | No emotion anchor | "Close-up of a 35-year-old man's face shifting from skepticism (furrowed brow, slight head shake) to genuine surprise (eyebrows up, mouth opens slightly, leans back), shot on iPhone 15 Pro, ring light catchlights visible in eyes" |
| "A cooking video" | No sensory detail | "Macro shot of golden-brown garlic sizzling in olive oil in a cast iron pan, camera slowly pulls back to reveal hands adding fresh herbs. Steam rises, oil pops. 45-degree overhead angle, warm kitchen lighting, shallow DOF" |

### Transformation Rules
1. **Add a specific person** — age, appearance, clothing, emotion
2. **Add a specific place** — not "kitchen" but "sunlit Brooklyn apartment kitchen with subway tile and hanging copper pots"
3. **Add a specific action** — not "using product" but "slides open the magnetic lid, lifts out the bottle, reads the label"
4. **Add sensory details** — sounds, textures, temperatures, smells (described for scene comprehension)
5. **Add camera specifics** — not "medium shot" but "35mm lens, eye-level, slight handheld drift, shallow DOF"

---

## Image Input First-Frame Control

When a model supports image input (Sora, Kling, VEO):

### How It Works
1. Generate a high-quality reference image using `image-generation` skill
2. Upload as the "first frame" or "reference image" input
3. The model uses this as the starting composition and animates from there
4. Result: exact visual match to your intended look, with motion added

### Best Practices
- Reference image should match the exact aspect ratio of the video output
- Lighting, composition, and subject appearance in the image = what the video starts with
- For transformation videos: provide both first-frame AND last-frame images
- Image quality matters — higher quality input = better video output

### When to Use
- Product shots where you need exact product appearance
- Character-based content where facial features must match a reference
- Scene compositions that are difficult to describe in text alone
- Before/after sequences where you control both endpoints

---

## Dialogue Formatting Best Practice

How dialogue is formatted in the prompt affects how models interpret and render speech:

### Recommended Format
```
[CHARACTER] speaks [delivery style], [physical action]:
"[Dialogue line]"
[Beat/reaction description]
"[Next line]"
```

### Example
```
Sarah speaks confidently, leaning forward with one hand on the desk:
"Three months ago, I couldn't get a single ad to convert."
[Slight laugh, shakes head, sits back]
"Now? We're spending $50K a month and every dollar comes back 4x."
[Direct eye contact, slight smile]
```

### Rules
- Dialogue ALWAYS in quotation marks — models interpret these as spoken words
- Delivery style as adverb: "confidently," "hesitantly," "excitedly"
- Physical actions between lines as [bracketed beats]
- Keep individual lines short — models handle 1-2 sentences per speech block better than paragraphs
- Specify WHO speaks before each line in multi-character scenes

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
