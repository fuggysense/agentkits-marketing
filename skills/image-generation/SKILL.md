---
name: image-generation
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: content
difficulty: intermediate
description: "Generate AI images and photos. Use this skill when the user wants to produce any still visual \u2014 product hero shots, ad creatives, UGC-style photos, selfie-style content, lifestyle shots, headshots, before/after comparisons, carousel slides, or video first-frame references. Key trigger: the user says they NEED, WANT, or asks you to GENERATE/CREATE/MAKE an image, photo, picture, or shot. This includes \"I need images for my campaign\", \"make me a product shot\", \"generate a selfie photo for an ad\", or \"create a before/after image\". This is the ONLY skill that produces still image files. Do NOT use for video creation, copywriting, scripting, analytics, or code."
triggers:
  - generate image
  - create image
  - ad creative
  - product shot
  - UGC
  - headshot
  - carousel image
  - before after
  - marketing image
  - visual content
prerequisites: []
related_skills:
  - copywriting
  - social-media
  - paid-advertising
  - video-director
agents:
  - copywriter
  - attraction-specialist
---

## Graph Links
- **Feeds into:** [[video-director]], [[tiktok-slideshows]]
- **Draws from:** (independent — visual pipeline entry point)
- **Used by agents:** [[copywriter]]
- **Related:** [[content-moat]], [[social-media]]

# Image Generation for Marketing

Generate high-quality marketing images using structured JSON prompts with AI image generation models. ~$0.07 per image via Nano Banana 2 + Claude Code.

## Vertex AI Direct Generation

This skill can generate images directly via API (no external tool needed). See `../video-director/references/vertex-ai-api.md` for full setup.

| Model | Cost | Best For |
|-------|------|----------|
| Imagen 4 Fast | $0.02/img | Quick text-to-image, no reference needed |
| Nano Banana 2 (Flash) | $0.067/img | Reference-based gen, character consistency — **default** |
| Nano Banana Pro | $0.134/img | Higher fidelity when NB2 isn't enough |

NB2 uses Generative Language API with API key. Imagen uses Vertex AI with gcloud auth. Both are configured on project `lexical-tide-491204-b4` (jerel@1upsalesai.com).

## Language & Quality Standards

**CRITICAL**: Respond in the same language the user is using.

---

## When to Use This Skill

- Creating ad creatives (Meta, LinkedIn, TikTok)
- Product hero shots for e-commerce or landing pages
- UGC-style content for social proof
- Professional headshots for LinkedIn or team pages
- Carousel cover slides for social media
- Before/after transformation visuals
- Any marketing visual that needs to look professional without a photographer

## How It Works

1. Define what you need (style, subject, scene, mood)
2. Build a structured JSON prompt following the templates below
3. Send to Nano Banana 2 image generation API
4. Get production-ready marketing image
5. Give feedback — Claude updates preferences, each batch gets better (compounding loop)

## Prompt Review Gate (HITL)

Before generating any image, Claude presents the prompt for human review:

1. **Draft** — Claude builds the JSON prompt based on user request
2. **Present** — Show prompt in formatted code block with plain-English explanation of key choices (why this lighting, why this angle, why this aspect ratio)
3. **Review** — User reviews: **Approve** / **Request Changes** / **Reject**
4. **Generate** — Only after approval, proceed to generation
5. **Feedback Loop** — User corrections update preferences for future prompts. Each batch gets better.

### What to Explain in the Review

- **Aspect ratio choice** — Why 4:5 vs 1:1 vs 9:16
- **Lighting setup** — How it affects mood and realism
- **Style aesthetic** — Why UGC vs studio vs editorial
- **Negative prompts** — What common AI artifacts are being blocked

---

## Video Reference Image Mode

When invoked as part of the `video-director` pipeline (image-first video types):

### How It Works
1. Claude generates 2-3 image prompts as reference frames for video generation
2. **Cross-image consistency is critical** — same subject, lighting, camera angle, color temperature across all images
3. **Batch review** — All image prompts presented simultaneously for a single HITL approval (not 3 separate gates)
4. After approval, generate all images, then feed to video model

### Consistency Checklist
- [ ] Same subject description (verbatim character block) across all prompts
- [ ] Matching `scene.lighting` settings (type, direction, quality)
- [ ] Same or complementary `camera.angle` and `camera.lens`
- [ ] Matching `style.color_grading` for consistent look
- [ ] Same aspect ratio across all images (must match final video output)

### Output to Video Pipeline
After generating reference images, hand off to `video-director` skill with:
- Generated image files (for upload to video model)
- The image prompts used (for the video prompt to reference)
- Recommended video model and prompt template

---

## JSON Prompt Structure

Every image prompt follows this schema:

```json
{
  "meta": {
    "aspect_ratio": "4:5 | 1:1 | 16:9 | 9:16",
    "resolution": "1K | 2K",
    "thinking_level": "minimal | high"
  },
  "subject": [{ ... }],
  "scene": {
    "location": "...",
    "lighting": { "type": "...", "direction": "...", "quality": "..." }
  },
  "camera": {
    "lens": "...",
    "angle": "...",
    "framing": "...",
    "depth_of_field": "..."
  },
  "style": {
    "aesthetic": "...",
    "color_grading": "...",
    "mood": "..."
  },
  "text_rendering": { ... },
  "negative_prompt": "..."
}
```

### Key Fields

| Field | Purpose | Tips |
|-------|---------|------|
| `meta.aspect_ratio` | Image dimensions | 4:5 for social, 1:1 for product/headshot, 16:9 for before/after, 3:4 for TikTok Photo Mode, 9:16 for stories/reels |
| `meta.thinking_level` | Generation complexity | "high" for people/complex scenes, "minimal" for simple product shots |
| `subject` | What's in the image | Be extremely specific about appearance, clothing, position |
| `scene.lighting` | Light setup | Specify type, direction, quality — this makes or breaks realism |
| `camera` | Shot style | Lens, angle, depth of field control professional look |
| `style.aesthetic` | Overall feel | ugc-selfie, studio-product-hero, editorial-portrait, before-after, clean-bold-cover |
| `negative_prompt` | What to avoid | Always include: stock photo, cartoon, watermark, extra fingers |

## Marketing Image Templates

See `references/nano-banana-examples.md` for complete JSON templates:

1. **UGC Skincare Selfie** — Authentic selfie-style, ring light, iPhone look
2. **Product Hero Clean** — Studio product shot, infinite white, e-commerce ready
3. **LinkedIn Authority Headshot** — Professional portrait, Rembrandt lighting
4. **Carousel Cover Slide** — Bold text, gradient background, scroll-stopping
5. **Before/After Transformation** — Split comparison, identical lighting both sides

## Best Practices

### For Ad Creatives
- Use 4:5 aspect ratio (Facebook/Instagram feed)
- UGC-style outperforms polished studio shots for Meta ads
- Include product in frame — don't just show lifestyle
- Match the image style to your CTR goals: authentic > polished for lead gen

### For Social Media
- Carousel covers: bold text, dark backgrounds, curiosity-driving headlines
- 9:16 for stories/reels
- 1:1 for feed posts

### For Realism
- Always specify "natural skin texture, visible pores" for people
- Add negative_prompt to exclude: airbrushed skin, stock photo, cartoon, watermark
- Specify camera model and lens for photographic realism
- Include imperfections: "slightly off-shoulder", "loose strands", "casual imperfect framing"

### Cost Optimization
- ~$0.07 per image with Nano Banana 2
- Use "thinking_level": "minimal" for simple product shots
- Use "thinking_level": "high" for complex scenes with people
- Batch generate variations — cheap enough to test multiple creatives

## Setup for Image Generation

### Prerequisites
- Google AI Studio API key(s) in `.env`:
  - `GEMINI_API_KEY` (required) — primary key
  - `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3` (optional) — for round-robin rotation (3 keys = 3x daily quota, ~150 free images/day)
  - Get keys at: https://aistudio.google.com/apikey (one per Google AI Studio project)
- Python with `requests` package
- Generation script: see `references/nano-banana-full-guide.md`

### Standard Key Rotation Pattern

**All skills that do Gemini image generation MUST use this pattern.** It collects all `GEMINI_API_KEY*` env vars and cycles through them round-robin, automatically rotating on rate limit errors. This multiplies the daily free quota (50/key/day) by the number of keys.

```python
import os
import itertools

def get_gemini_keys():
    """Collect all GEMINI_API_KEY* env vars for round-robin rotation."""
    keys = []
    primary = os.environ.get("GEMINI_API_KEY")
    if primary:
        keys.append(primary)
    i = 2
    while True:
        key = os.environ.get(f"GEMINI_API_KEY_{i}")
        if not key:
            break
        keys.append(key)
        i += 1
    return keys

# Create a cycle iterator at module/script level
key_cycle = itertools.cycle(get_gemini_keys())

# For each generation call: api_key = next(key_cycle)
# On 429/rate-limit error: rotate to next key and retry
```

**Skills using this pattern:**
- `claude-thumbnails` (youtube-thumbnail `generate_thumbnail.py`)
- `tiktok-slideshows` (`generate_batch.py`)
- `image-generation` (any future scripts)

### Project Structure
```
prompts/              # JSON prompt library
├── product-shots/
├── lifestyle/
├── ugc-style/
├── portraits/
├── social-graphics/
├── ad-creative/
images/               # Generated output (mirrors prompts structure)
brand/                # Brand guidelines for consistent style
├── colors.json
├── style-guide.md
```

### 8 Prompt Categories (100+ Templates)
Full guide with all templates: `references/nano-banana-full-guide.md`

1. Professional Portraits (15 templates)
2. Product Photography (15 templates)
3. Social Media Graphics (20 templates)
4. Ad Creative (15 templates)
5. Brand Assets (15 templates)
6. Infographics & Data Viz (10 templates)
7. Image Editing (15 templates)
8. Advanced & Creative (10 templates)

## Carousel Slide Set Mode (TikTok Photo Mode)

Generate 3-10 cohesive images for TikTok Photo Mode carousels. All slides in a set share consistent visual style — same color palette, typography placement, layout grid, and mood.

**Connected skill:** `tiktok-slideshows` owns the full workflow (client context loading, narrative flow, batch generation). This skill provides the image generation engine.

### How It Works

1. **Load client context** — brand voice, visual style guide, typography, brand colors, story bank from `clients/<project>/`
2. **Build prompt layers** — every prompt has 5 layers (see `tiktok-slideshows` SKILL.md for full spec):
   - **Brand Context** (same for entire batch) — what the brand is, visual personality, audience
   - **Style Anchor** (same for all slides in one post) — background, photography, color grading, text treatment
   - **Slide Narrative** (unique per slide) — role in the story, what came before, what comes next
   - **Visual Description** (unique per slide) — composition, subjects, text overlays
   - **Negative Prompt** (same for entire batch) — from visual style guide
3. **Style anchor locks consistency** — written once per post, cloned verbatim to every slide
4. **Slide narrative ensures flow** — each slide references previous/next slides so the AI generates contextually
5. **Batch review** — all slide prompts presented together grouped by post
6. Generate all slides. Output: numbered files per post (e.g., `post-01-slide-01.png` through `post-01-slide-07.png`)

### Typography in AI Prompts

When text is baked into images, include the typography block from `clients/<project>/typography.md`:
- Font style reference (Bebas Neue for titles, Inter for body)
- Text color per background (from color pairing table)
- Placement: upper 1/3 only
- Size descriptions ("large, fills width" / "medium" / "small, readable")

Load the client's typography file — do not hardcode font specs.

### Aspect Ratio

- **Always 3:4** (1080x1440) — TikTok Photo Mode native
- Do NOT use 9:16, 1:1, or 4:5 for TikTok carousels

### Carousel Template Variants

#### 1. Comparison / Curation (5-7 slides)
- **Style:** Side-by-side comparison layout, clean split
- **Slide 1:** Bold hook text on dark/gradient background
- **Slides 2-5:** Product comparison — left vs right with verdict overlay
- **Final slide:** Brand statement + CTA text
- **Mood:** Confident, editorial, slightly provocative
- **Color:** Dark backgrounds, high contrast text, accent color pops
- **Use for:** Product reviews, curation reveals, "X vs Y" content

#### 2. Mood Board / Personality (5-6 slides)
- **Style:** Collage/mood board aesthetic, soft editorial
- **Slide 1:** Category/archetype name in elegant typography
- **Slides 2-4:** Mood board images (textures, items, color swatches, details)
- **Slide 5:** Key traits text on matching background
- **Final slide:** Quiz or engagement CTA
- **Mood:** Aspirational, curated, warm
- **Color:** Palette derived from the subject's personality
- **Use for:** Style quizzes, personality types, aesthetic reveals, "what type are you"

#### 3. Feature Spotlight (5 slides)
- **Style:** Magazine editorial, clean layout
- **Slide 1:** Hero shot with name/title overlay
- **Slide 2:** Origin/story context (text-heavy, minimal)
- **Slide 3:** Detail close-up
- **Slide 4:** Key differentiator or reasoning
- **Slide 5:** CTA
- **Mood:** Premium, trustworthy, sophisticated
- **Color:** Neutral tones, brand-consistent accents
- **Use for:** Product launches, brand spotlights, feature reveals

#### 4. Building in Public / Metrics (3-4 slides)
- **Style:** Text-heavy, minimal background, newsletter aesthetic
- **Slide 1:** Metric/milestone callout (large number)
- **Slide 2-3:** Insight or decision explained simply
- **Final slide:** Engagement question + CTA
- **Mood:** Transparent, authentic, raw
- **Color:** Black/white with single accent, clean sans-serif
- **Use for:** Growth updates, behind-the-scenes, milestone shares

### Consistency Checklist (Carousel)

- [ ] Same `style.color_grading` across all slides in set
- [ ] Matching typography style (font weight, placement, size ratio)
- [ ] Consistent border/padding/layout grid
- [ ] Same `scene.lighting` settings if using photo-style slides
- [ ] Matching negative_prompt across all slides
- [ ] All slides exactly 3:4 (1080x1440)

### Output Structure

```
assets/tiktok/slideshows/
├── post-01/
│   ├── slide-01.png  (hook)
│   ├── slide-02.png
│   ├── ...
│   └── slide-07.png  (CTA)
├── post-02/
│   └── ...
```

---

## Nano Banana Pro Advanced Features

### Style Prompt Saving
Save a style prompt as a reusable template. Lock visual settings (lighting, color grading, composition) and swap only the subject per image. Useful for maintaining brand consistency across a campaign.

```json
{
  "meta": { "style_preset": "saved:brand-hero-style" },
  "subject": [{ "type": "product", "description": "[swap this per image]" }]
}
```

### Annotation Feature
Draw annotations (arrows, circles, highlights) on generated images to mark areas for:
- **Frame-to-video workflow:** Annotate which part of the image should move, expand, or change in the video model
- **Feedback to Claude:** Circle what works, X what doesn't, for the feedback loop
- **Client review:** Mark areas that need revision before final approval

### Two Image Workflows

**Objects Path (Products, Food, Interiors):**
1. Generate product/scene reference image → high quality, exact look
2. Feed to video model as first-frame anchor
3. Video model animates the scene around the static product
4. Best models: Kling (image-to-video), VEO (reference images)

**Characters Path (People, UGC, Testimonials):**
1. Generate character reference using character-bible-template
2. Multiple angles/expressions of same character for consistency
3. Feed to video model with character API or text block
4. Best models: Sora (Characters API), Kling (image-to-video)

### Seedream 4 Alternative
For character-based accounts needing maximum consistency:
- Seedream 4 specializes in consistent character generation from a single reference
- Better than Nano Banana for maintaining exact facial features across many images
- Use when building a character image library for video campaigns

---

## Related Commands

- `/content:ads` — Write ad copy (pair with generated images)
- `/content:social` — Social content (pair with generated visuals)
- `/social:viral` — Viral content strategy
- `/tiktok:batch` — TikTok slideshow batch pipeline (uses carousel slide set mode)
