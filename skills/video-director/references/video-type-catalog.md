# Video Type Catalog

All 11 AI video ad types organized by pipeline. Each type includes a fill-in-the-blank prompt template, recommended model, and key techniques.

**Important:** This system generates PROMPTS, not videos. Output = ready-to-paste text for external tools.

---

## Pipeline Legend

| Pipeline | Flow | When to Use |
|----------|------|-------------|
| **Direct Video** | Single prompt → video model | Talking head, dialogue, simple action |
| **Image-First** | Generate reference images → feed to video model | Product, food, real estate, unboxing |
| **Localized Recreation** | Analyze source → reconstruct in new language/culture | Scaling winning ads to new markets |

---

# Direct Video Pipeline

## 1. Street Interview

**Pipeline:** Direct Video
**Primary Model:** Sora 2 Pro | **Fallback:** Kling + voice-over
**Duration:** 15-30s | **Aspect Ratio:** 9:16 (TikTok/Reels) or 4:5 (Feed)

### When to Use
- Brand awareness / top-of-funnel engagement
- Making complex products feel approachable
- Social proof through "person on the street" reactions
- Pattern interrupt in feeds (looks like real content, not ads)

### When NOT to Use
- Products that need detailed demo/walkthrough
- B2B with formal brand requirements
- When you need specific, scripted testimonials

### Prompt Template

```
[SCENE SETUP]
A [age]-year-old [gender] [ethnicity descriptor] is being interviewed on a
[specific location: busy city sidewalk / college campus / farmers market / etc.].
They're wearing [casual outfit: hoodie and jeans / sundress / business casual / etc.].

[DIALOGUE]
An off-camera interviewer asks: "[Question about product/problem]"
The person responds naturally: "[Authentic reaction/answer — conversational, not scripted]"
[Optional: follow-up question and surprised/delighted reaction]

[CAMERA]
Handheld smartphone camera, slight shake, shot at chest-to-head level.
Shallow depth of field with blurred [pedestrians / storefronts / trees] in background.
Natural outdoor lighting with [sunlight / overcast / golden hour] conditions.

[REALISM]
Natural skin with visible pores, wind-moved hair, ambient street noise implied.
Compression artifacts consistent with iPhone video.
Subject occasionally breaks eye contact, looks to the side while thinking.

[NEGATIVE]
No cinematic lighting, no studio setup, no teleprompter reading, no perfect framing,
no stock photo aesthetics, no airbrushed skin, no extra fingers.
```

### Key Techniques
- Subject should look slightly away from camera occasionally (thinking, not rehearsed)
- Background pedestrians add authenticity
- Imperfect audio framing (interviewer slightly off-mic) feels real
- Surprise/delight reactions on the "reveal" moment are the hook

---

## 2. Podcast Style

**Pipeline:** Direct Video
**Primary Model:** Sora 2 Pro | **Fallback:** Kling + voice-over
**Duration:** 15-45s | **Aspect Ratio:** 9:16 or 1:1

### When to Use
- Authority/thought leadership positioning
- Explaining complex concepts simply
- Building personal brand alongside product
- Mid-funnel content (viewer already somewhat aware)

### When NOT to Use
- Cold audiences who don't know you yet
- Products that need visual demonstration
- Quick scroll-stopping hooks (podcast format is slower-burn)

### Prompt Template

```
[SCENE SETUP]
A [age]-year-old [gender] sits at a [podcast desk / home office / studio setup] with
[specific mic: Shure SM7B / Blue Yeti / rode podcaster] in front of them.
They're wearing [casual professional: button-up with sleeves rolled / crew neck sweater / etc.].
Background: [bookshelf with varied books / acoustic panels / plant and monitor / etc.].

[DIALOGUE]
The person speaks directly, gesturing naturally:
"[Key insight or hot take about the industry/problem]"
[Beat — slight pause, lean forward]
"[The punchline / surprising stat / counterintuitive truth]"
[Optional: slight head shake or eyebrow raise for emphasis]

[CAMERA]
Slightly above eye level, medium close-up (chest and above).
Subtle rack focus between speaker and background.
[Warm / cool] studio lighting with [ring light catchlights / softbox key light].

[REALISM]
Natural gestures — speaker touches chin, adjusts in chair, uses hands while talking.
Slight lip moisture, natural blink rate, micro-expressions between sentences.
Audio implied: slight room reverb, no echo.

[NEGATIVE]
No teleprompter stare, no robotic delivery, no perfect stillness,
no cinematic color grading, no dramatic shadows, no extra fingers.
```

### Key Techniques
- Lean-in moment creates intimacy and emphasis
- Specific mic model adds visual authenticity
- Background details (specific books, personal items) make it feel like a real space
- Natural pause before the punchline builds tension

---

## 3. Try-On / Product Demonstration

**Pipeline:** Direct Video
**Primary Model:** Sora 2 Pro | **Fallback:** Kling
**Duration:** 10-20s | **Aspect Ratio:** 9:16

### When to Use
- Fashion, beauty, accessories, wearable products
- Before/after comparisons on a person
- UGC-style product reviews
- "Get ready with me" format

### When NOT to Use
- Products that can't be worn/applied to a person
- Technical/SaaS products
- Products where the visual difference is subtle

### Prompt Template

```
[SCENE SETUP]
A [age]-year-old [gender] stands in front of a [bathroom mirror / bedroom full-length mirror /
ring light setup]. Room has [natural daylight from window / warm bedroom lighting / bathroom fluorescents].
They're initially wearing [plain outfit / no makeup / before-state description].

[ACTION SEQUENCE]
1. Person holds up [product] to camera, showing packaging/label briefly
2. [Application action: puts on / applies / unboxes / tries on]
3. Reaction shot — [genuine surprise / satisfaction / checking different angles]
4. Final pose or spin showing the result

[CAMERA]
Front-facing smartphone camera (selfie mode), mounted or hand-held.
Mirror reflection visible for context. Natural room lighting.
Slight perspective distortion from wide-angle front camera.

[REALISM]
Real bathroom/bedroom clutter visible at edges. Natural skin texture.
Product packaging has realistic printing (not blank/generic).
Movement is casual, not choreographed — slight fumbling is authentic.

[NEGATIVE]
No studio lighting, no professional photography, no perfect posing,
no stock photo aesthetics, no CGI product, no extra fingers.
```

---

## 4. Shock Hook

**Pipeline:** Direct Video
**Primary Model:** Sora 2 Pro | **Fallback:** Kling
**Duration:** 3-8s | **Aspect Ratio:** 9:16

### When to Use
- First 3 seconds of any ad (can splice with longer video)
- Scroll-stopping pattern interrupt
- A/B testing multiple hooks for the same ad body
- Controversial or surprising claims

### When NOT to Use
- Luxury/premium brands that need elegance
- Sensitive topics where shock feels exploitative
- When the product doesn't deliver on the shocking claim

### Prompt Template

```
[SCENE — KEEP IT SIMPLE]
A [age]-year-old [gender] looks directly at camera, [in their kitchen / at their desk / outside].
Expression: [wide eyes / leaning in / pointing at camera / shaking head].

[DIALOGUE — ONE LINE]
"[Shocking statement or question that creates immediate curiosity]"

[CAMERA]
Close-up, handheld, slightly tilted. 2-3 second shot maximum.
Abrupt start — no fade-in. Feels like mid-conversation.

[NEGATIVE]
No setup, no intro, no music, no transitions. Raw and immediate.
```

### Key Techniques
- **Less is more** — One sentence. One person. One emotion.
- Start mid-action (no "hey guys" intro)
- Expression must match the claim (genuine shock, not performed)
- Works best as the opening splice before a longer video

### Example Hooks
- "I spent $50,000 on ads before I learned THIS..."
- "Stop. If you're using [product category], watch this first."
- "My doctor told me to stop doing [common thing]. Here's why."
- "This $12 product replaced my $200 [competitor]."

---

## 5. Product Commercial

**Pipeline:** Direct Video
**Primary Model:** Sora 2 Pro | **Fallback:** Kling
**Duration:** 15-30s | **Aspect Ratio:** 9:16 or 1:1

### When to Use
- Product launches and hero content
- Mid-funnel consideration stage
- When the product's visual appeal IS the selling point
- E-commerce and DTC brands

### When NOT to Use
- Services or SaaS (nothing physical to show)
- When price/offer is the main driver (use direct response instead)

### Prompt Template

```
[SCENE SETUP]
[Product] sits on [surface: marble counter / wooden table / minimalist shelf].
A hand reaches in from [right/left] and picks it up.

[ACTION SEQUENCE]
1. Hero shot — product centered, clean background, [warm / cool] lighting
2. Human interaction — person [uses / opens / demonstrates] the product
3. Detail shot — close-up of [key feature / texture / label]
4. Lifestyle context — product in natural use environment
5. End frame — product centered with [tagline / website]

[CAMERA]
Smooth slow-motion for hero shot (120fps feel).
Handheld for lifestyle shots.
Macro lens for detail close-ups.

[LIGHTING]
[Soft natural window light / warm studio key light / bright and airy].
Product should be the brightest element in frame.

[NEGATIVE]
No floating product, no CGI effects, no lens flare, no dramatic shadows,
no white void background (unless specifically e-commerce style).
```

---

## 6. POV Adventure

**Pipeline:** Direct Video
**Primary Model:** Sora 2 Pro | **Fallback:** Kling
**Duration:** 10-30s | **Aspect Ratio:** 9:16

### When to Use
- Travel, outdoor, lifestyle brands
- Experience-based products (classes, events, destinations)
- "Day in the life" content
- Aspiration-driven marketing

### When NOT to Use
- Products that need explanation/education
- B2B or technical products
- When the user experience isn't visually interesting

### Prompt Template

```
[POV SETUP]
First-person perspective. Camera is the viewer's eyes.
Location: [specific environment with rich visual detail].

[ACTION SEQUENCE]
1. POV walking through [environment] — ground visible, arms occasionally in frame
2. Discover [product / place / experience] — camera looks down/around
3. Interaction — hands reach out to [touch / pick up / open / use]
4. Reveal — pull back to show the full [scene / result / transformation]

[CAMERA]
GoPro / action camera perspective. Wide angle, slight barrel distortion.
Natural movement — walking bounce, head turns, occasional stumble.
No stabilization — raw adventure footage feel.

[ENVIRONMENT]
[Detailed description of location, weather, time of day, ambient sounds].
Background detail: [people, animals, vehicles, nature sounds].

[NEGATIVE]
No drone shots, no cinematic framing, no smooth dolly moves,
no perfect composition, no stock footage aesthetics.
```

---

# Image-First Pipeline

For these types, generate 2-3 reference images FIRST using the `image-generation` skill (Nano Banana), then feed them to the video model.

## 7. Viral Food

**Pipeline:** Image-First
**Image Model:** Nano Banana | **Video Model:** Kling 2.5 | **Fallback Video:** VEO
**Duration:** 8-15s | **Aspect Ratio:** 9:16 or 1:1

### When to Use
- Food/beverage products
- Recipe-based marketing
- Restaurant/delivery service promotion
- Satisfying/ASMR-style content

### When NOT to Use
- Products unrelated to food
- When the food doesn't look visually impressive
- Health products where food might send wrong message

### Image Prompts (Generate First)

**Image 1 — Hero ingredient/product shot:**
```json
{
  "meta": { "aspect_ratio": "1:1", "resolution": "2K", "thinking_level": "high" },
  "subject": [{ "type": "food", "description": "[Product/ingredient in pristine state]" }],
  "scene": { "location": "[Kitchen counter / cutting board / restaurant table]",
    "lighting": { "type": "natural window", "direction": "side", "quality": "soft warm" }},
  "camera": { "lens": "85mm equivalent", "angle": "45-degree overhead", "framing": "tight", "depth_of_field": "shallow" },
  "style": { "aesthetic": "food-photography", "color_grading": "warm appetizing", "mood": "inviting" },
  "negative_prompt": "stock photo, artificial lighting, plastic food, fast food chain, cartoon"
}
```

**Image 2 — Action/preparation shot:**
```json
{
  "meta": { "aspect_ratio": "1:1", "resolution": "2K", "thinking_level": "high" },
  "subject": [{ "type": "food-action", "description": "[Pouring / slicing / sizzling / plating action]" }],
  "scene": { "location": "[Same kitchen/setting as Image 1]",
    "lighting": { "type": "natural window", "direction": "side", "quality": "soft warm" }},
  "camera": { "lens": "50mm equivalent", "angle": "eye-level", "framing": "medium", "depth_of_field": "moderate" },
  "style": { "aesthetic": "food-photography", "color_grading": "warm appetizing", "mood": "dynamic" },
  "negative_prompt": "stock photo, artificial lighting, plastic food, cartoon, blurry"
}
```

### Video Prompt (Feed Images to Kling)

```
Using reference images as starting and ending frames:
Smooth transition from [ingredient/product hero shot] to [preparation action].
[Specific motion: pour / sizzle / steam rising / cheese pull / sauce drizzle].
Camera slowly pulls in during the action.
Warm, appetizing lighting consistent across the sequence.
Sound design implied: [sizzle / crunch / pour / ambient kitchen].
Duration: 8-12 seconds. Smooth, satisfying motion.
```

---

## 8. Anatomical Animation

**Pipeline:** Image-First
**Image Model:** Nano Banana | **Video Model:** VEO 3.1 | **Fallback Video:** Kling
**Duration:** 10-20s | **Aspect Ratio:** 9:16 or 1:1

### When to Use
- Health/wellness/supplement products
- Medical device marketing
- Fitness/body transformation content
- Educational health content for social

### When NOT to Use
- Non-health products
- When scientific accuracy isn't needed
- Audiences that would find anatomical imagery off-putting

### Image Prompts (Generate First)

**Image 1 — External view:**
```json
{
  "meta": { "aspect_ratio": "1:1", "resolution": "2K", "thinking_level": "high" },
  "subject": [{ "type": "anatomical", "description": "[Body part / system in external view — e.g., person's torso, knee joint, skin surface]" }],
  "scene": { "location": "clean medical illustration background",
    "lighting": { "type": "even studio", "direction": "front", "quality": "clinical" }},
  "camera": { "lens": "macro equivalent", "angle": "straight-on", "framing": "tight", "depth_of_field": "deep" },
  "style": { "aesthetic": "medical-illustration", "color_grading": "neutral clinical", "mood": "educational" },
  "negative_prompt": "cartoon, anime, gross, bloody, horror, low quality"
}
```

**Image 2 — Cross-section / internal view:**
```json
{
  "meta": { "aspect_ratio": "1:1", "resolution": "2K", "thinking_level": "high" },
  "subject": [{ "type": "anatomical-cross-section", "description": "[Internal view showing mechanism — e.g., muscle fibers, joint cartilage, skin layers]" }],
  "scene": { "location": "clean medical illustration background",
    "lighting": { "type": "even studio", "direction": "front", "quality": "clinical" }},
  "camera": { "lens": "macro equivalent", "angle": "straight-on", "framing": "tight", "depth_of_field": "deep" },
  "style": { "aesthetic": "medical-illustration", "color_grading": "neutral clinical", "mood": "educational" },
  "negative_prompt": "cartoon, anime, gross, bloody, horror, low quality, inaccurate anatomy"
}
```

### Video Prompt (Feed Images to VEO)

```
Smooth animated transition from [external body view] to [anatomical cross-section].
Camera zooms into [body area], layers peel away to reveal internal structure.
[Product/ingredient/mechanism] is highlighted with subtle glow as it [interacts with / repairs / strengthens] the [target tissue/organ].
Clean, educational animation style. Scientifically accurate anatomy.
Duration: 10-15 seconds. Smooth, precise motion.
No gore, no blood, no horror elements. Clinical and reassuring.
```

---

## 9. Real Estate Transformation

**Pipeline:** Image-First
**Image Model:** Nano Banana | **Video Model:** Kling 2.6 | **Fallback Video:** VEO
**Duration:** 10-20s | **Aspect Ratio:** 9:16 or 16:9

### When to Use
- Real estate listings and virtual tours
- Home renovation / interior design services
- Before/after property transformations
- Architecture and construction marketing

### When NOT to Use
- Properties that look the same before/after
- When photos alone would suffice
- Budget too tight for multiple image + video generation

### Image Prompts (Generate First)

**Image 1 — Before state:**
```json
{
  "meta": { "aspect_ratio": "16:9", "resolution": "2K", "thinking_level": "high" },
  "subject": [{ "type": "interior", "description": "[Room in before state: dated cabinets, old carpet, dim lighting, worn walls]" }],
  "scene": { "location": "[specific room: kitchen / living room / bathroom]",
    "lighting": { "type": "existing room light", "direction": "overhead", "quality": "flat unflattering" }},
  "camera": { "lens": "wide angle 16mm", "angle": "eye-level corner", "framing": "full room", "depth_of_field": "deep" },
  "style": { "aesthetic": "real-estate-photo", "color_grading": "slightly desaturated", "mood": "dated" },
  "negative_prompt": "luxury, modern, perfect, staged, stock photo"
}
```

**Image 2 — After state:**
```json
{
  "meta": { "aspect_ratio": "16:9", "resolution": "2K", "thinking_level": "high" },
  "subject": [{ "type": "interior", "description": "[Same room transformed: modern finishes, fresh paint, new fixtures, styled decor]" }],
  "scene": { "location": "[same room as Image 1]",
    "lighting": { "type": "natural daylight + recessed", "direction": "window side", "quality": "bright warm" }},
  "camera": { "lens": "wide angle 16mm", "angle": "same corner as Image 1", "framing": "full room", "depth_of_field": "deep" },
  "style": { "aesthetic": "real-estate-photo", "color_grading": "bright airy", "mood": "aspirational" },
  "negative_prompt": "CGI, unrealistic, miniature, dollhouse, stock photo"
}
```

### Video Prompt (Feed Images to Kling)

```
Smooth timelapse-style transition from [before room state] to [after room state].
Same camera angle throughout. Elements transform:
- Walls change color/texture
- Fixtures morph from old to new
- Lighting shifts from flat to warm and inviting
- Furniture and decor appear/transform
Duration: 10-15 seconds. Satisfying, smooth transformation.
No jump cuts — continuous morphing transition.
```

---

## 10. Unboxing

**Pipeline:** Image-First
**Image Model:** Nano Banana | **Video Model:** Kling 2.6 | **Fallback Video:** VEO
**Duration:** 15-30s | **Aspect Ratio:** 9:16

### When to Use
- E-commerce product launches
- Subscription box reveals
- Premium/luxury product presentation
- Gift-oriented marketing (holidays, occasions)

### When NOT to Use
- Digital/SaaS products
- Products with underwhelming packaging
- When the product experience is more important than the reveal

### Image Prompts (Generate First)

**Image 1 — Sealed package:**
```json
{
  "meta": { "aspect_ratio": "4:5", "resolution": "2K", "thinking_level": "high" },
  "subject": [{ "type": "product-box", "description": "[Sealed product box/package on table, hands approaching]" }],
  "scene": { "location": "[desk / kitchen table / bed]",
    "lighting": { "type": "natural window + overhead", "direction": "side-front", "quality": "warm natural" }},
  "camera": { "lens": "35mm equivalent", "angle": "overhead 45-degrees", "framing": "tight on package", "depth_of_field": "moderate" },
  "style": { "aesthetic": "ugc-unboxing", "color_grading": "natural warm", "mood": "anticipation" },
  "negative_prompt": "stock photo, commercial, studio, perfect lighting, catalog"
}
```

**Image 2 — Revealed product:**
```json
{
  "meta": { "aspect_ratio": "4:5", "resolution": "2K", "thinking_level": "high" },
  "subject": [{ "type": "product-reveal", "description": "[Product removed from box, held up or displayed, packaging tissue/inserts visible]" }],
  "scene": { "location": "[same setting as Image 1]",
    "lighting": { "type": "natural window + overhead", "direction": "side-front", "quality": "warm natural" }},
  "camera": { "lens": "50mm equivalent", "angle": "eye-level", "framing": "medium", "depth_of_field": "shallow" },
  "style": { "aesthetic": "ugc-unboxing", "color_grading": "natural warm", "mood": "excitement" },
  "negative_prompt": "stock photo, commercial, studio, perfect lighting, catalog, floating product"
}
```

### Video Prompt (Feed Images to Kling)

```
Using reference images as key frames:
Hands slide box across table, pause, then open the packaging.
Tissue paper rustles as hands pull back layers.
Product is lifted out and held up for inspection.
Camera follows the product upward.
Natural room lighting, casual pace, slight hand tremor (not robotic).
Duration: 15-20 seconds. Satisfying reveal pacing.
ASMR-adjacent: implied sounds of cardboard, tissue, product click.
```

---

# Localized Recreation Pipeline

## 11. Ad Localization at Scale

**Pipeline:** Localized Recreation
**Analysis Model:** Gemini | **Reconstruction Model:** Sora 2 Pro | **Fallback:** Kling + voice-over
**Duration:** Matches original | **Aspect Ratio:** Matches original

### When to Use
- Scaling proven ads to new markets/languages
- International campaign rollouts
- Cultural adaptation (not just translation)
- When a winning ad exists and you want to replicate its success in other regions

### When NOT to Use
- Original ad hasn't been proven (test first, then scale)
- Target culture has fundamentally different product perception
- Legal/regulatory differences make the claims invalid in new market

### Step 1: Analyze Original Ad (Use Gemini or Claude)

```
Analyze this video ad and extract:

1. STRUCTURE: Shot-by-shot breakdown with timing
2. SUBJECT: Age, gender, appearance, wardrobe, energy level
3. DIALOGUE: Exact script with emotional beats and timing
4. ENVIRONMENT: Setting, background details, time of day
5. CAMERA: Angles, movements, transitions, lens style
6. LIGHTING: Type, direction, quality
7. AUDIO: Music, SFX, ambient sounds, dialogue delivery style
8. HOOK: What makes the first 3 seconds work?
9. CTA: What's the call to action and how is it delivered?
10. CULTURAL ELEMENTS: What's culturally specific vs universal?
```

### Step 2: Cultural Adaptation Checklist

Before reconstruction, adapt for target market:

- [ ] Translate dialogue (not literal — localize idioms, humor, references)
- [ ] Replace culturally-specific elements (food brands, locations, holidays)
- [ ] Adjust subject appearance to match target demographic
- [ ] Modify wardrobe for cultural norms
- [ ] Update background signage/text to target language
- [ ] Verify claims are legal in target market
- [ ] Adjust humor style (what's funny varies by culture)
- [ ] Check color symbolism (white = purity in West, mourning in some Asian cultures)

### Step 3: Reconstruction Prompt Template

```
Recreate the following ad structure in [TARGET LANGUAGE/CULTURE]:

[ORIGINAL STRUCTURE — paste analysis from Step 1]

CULTURAL ADAPTATIONS:
- Subject: [Adapted age/gender/appearance for target market]
- Setting: [Equivalent local setting — e.g., Tokyo convenience store vs NYC bodega]
- Dialogue: [Localized script — culturally adapted, not literally translated]
- Wardrobe: [Culturally appropriate clothing]
- Background: [Local signage, architecture, pedestrians matching target locale]

MAINTAIN FROM ORIGINAL:
- Same emotional arc and timing
- Same camera angles and movements
- Same hook structure (first 3 seconds)
- Same CTA positioning and urgency level

[Include all standard realism and negative prompts from original type]
```

### Key Techniques
- The STRUCTURE stays the same — that's what made the original work
- The CULTURE changes — that's what makes it feel native
- Localize, don't translate — idioms, humor, and references must feel local
- Test the localized version separately — what works in English may not convert in Japanese

---

## Universal Prompt Schema

All 11 types share this underlying structure. Use it as a checklist when building custom prompts:

```
META
- Type: [street-interview / podcast / try-on / shock-hook / commercial / pov / food / anatomical / real-estate / unboxing / localization]
- Duration: [seconds]
- Aspect Ratio: [9:16 / 4:5 / 1:1 / 16:9]
- Model: [Sora 2 Pro / Kling 2.5 / Kling 2.6 / VEO 3.1]

SUBJECT
- Age, gender, appearance descriptors
- Wardrobe and accessories
- Energy level and emotional state
- Specific imperfections for realism

ACTION / DIALOGUE
- What happens (sequence of events with timing)
- What's said (exact dialogue in quotes)
- Emotional beats and transitions
- Physical actions and gestures

ENVIRONMENT
- Specific location with details
- Background elements (people, objects, signs)
- Ambient conditions (weather, noise, time of day)

CAMERA
- Mount (handheld / tripod / selfie / GoPro)
- Movement (static / slow pan / follow / drift)
- Angle (eye-level / low / high / overhead)
- Lens equivalent (wide 16mm / normal 35mm / portrait 85mm)

LIGHTING
- Type (natural / studio / mixed / available light)
- Direction (front / side / back / overhead)
- Quality (soft / hard / diffused / direct)

STYLE CONSTRAINTS (Negative Prompts)
- Anti-cinematic rules
- Anti-polished rules
- Anti-AI rules
- Platform-specific rules

AUDIO / AMBIENCE (implied — helps model understand the scene)
- Dialogue delivery style
- Background sounds
- Music (if any)

OVERALL VIBE
- 1-2 sentence mood summary
```

---

*Source: Framework extracted from David Roberts (AI Ad Guys) — @recap_david on X/Twitter. 11 AI video ad types adapted into reusable templates for AgentKits.*
