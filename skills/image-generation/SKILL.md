---
name: image-generation
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: content
difficulty: intermediate
description: "Tier-1 image-gen orchestrator: routes intent + Vertex/NB2 direct backend + HITL prompt review + carousel mode + video reference frames. Routes to `higgsfield` skill (sub-areas: product-photoshoot, marketplace-cards, soul-id, generate) or `gpt-image-2-director` peer. NOT for: video, copywriting, scripting."
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
  - video-factory
agents:
  - copywriter
  - attraction-specialist
---

## Graph Links
- **Feeds into:** [[video-factory]], [[tiktok-slideshows]]
- **Draws from:** (independent — visual pipeline entry point)
- **Used by agents:** [[copywriter]]
- **Related:** [[content-moat]], [[social-media]]

# Image Generation for Marketing

Generate high-quality marketing images using structured JSON prompts with AI image generation models. ~$0.07 per image via Nano Banana 2 + Claude Code.

## Tier-1 Architecture Note

This skill is **Tier 1** in the image-generation pipeline:
- **Tier 1 (this skill):** Intent routing + HITL prompt review + Vertex API direct backend + carousel templates + video reference frame mode
- **Tier 2 (`higgsfield` skill at `~/.claude/skills/higgsfield/`):** CLI router with sub-areas in `references/<area>/`
- **Tier 3 (`higgsfield-prompts/skills/media/image-generation/`):** Higgsfield CLI payload formatter, IMAGE_HANDOFF schema receiver
- **Peer (`gpt-image-2-director`):** Independent GPT Image 2.0 prompt engineer

Never format `higgsfield_generate` payloads here — that's Tier 3's job. Never invent storyboards — that's the workflow-generation flows in higgsfield-prompts.

## Thin-Stack Routing Gate

Before drafting a prompt or asking for a backend, route by intent. Sub-areas below are **reference packages inside the global `higgsfield` skill** at `~/.claude/skills/higgsfield/references/<area>/`, NOT standalone skills. Invoke the `higgsfield` skill with intent context; the router dispatches the sub-area.

| User intent | Route |
|---|---|
| Product photos, studio shots, lifestyle product images, product ad creatives, Meta/TikTok/Pinterest static ads, hero banners, product carousels, virtual try-on | `higgsfield` skill → sub-area `product-photoshoot` |
| Marketplace listing images, A+ modules, secondary product cards, marketplace infographics, listing compliance visuals | `higgsfield` skill → sub-area `marketplace-cards` |
| Train a face/Soul Character, digital twin, identity model, persistent face-lock setup | `higgsfield` skill → sub-area `soul-id` |
| Dense layouts, diagrams, UI mockups, posters with exact text, infographics, character sheets, labeled grids | `gpt-image-2-director` skill (peer) |
| Generic Higgsfield image generation, image edits/remixes, cinematic stills, no-product illustrations, Marketing Studio image/video with avatar + product | `higgsfield` skill → sub-area `generate` |
| Full video, UGC ad video, image-to-video, animation, Seedance/Kling/Veo prompts | Route to the video skill stack; use this skill only for deliberate still keyframes/reference frames. |

Stay in this skill only when the user explicitly wants Vertex/Nano Banana, a quick batch prompt engine, or a still-image job that does not fit a narrower owner above.

## Vertex AI Direct Generation

This skill can generate images directly via API (no external tool needed). See `references/vertex-ai-api.md` for full setup (local copy maintained; identical file also exists at `../video-director/references/vertex-ai-api.md` for the video-director skill).

| Model | Cost | Best For |
|-------|------|----------|
| Imagen 4 Fast | $0.02/img | Quick text-to-image, no reference needed |
| Nano Banana 2 (Flash) | $0.067/img | Reference-based gen, character consistency — **default** |
| Nano Banana Pro | $0.134/img | Higher fidelity when NB2 isn't enough |

NB2 uses Generative Language API with API key. Imagen uses Vertex AI with gcloud auth. Both are configured on project `lexical-tide-491204-b4` (jerel@1upsalesai.com).

## Backend selection (MANDATORY gate - after routing gate)

If the Thin-Stack Routing Gate keeps the work in this skill, ask before calling any generator when cost or backend choice is ambiguous. Do not silently route to the retired browser Higgsfield flow.

### Vertex API (this file, above tables)
- Fast (seconds per image), small per-image cost
- Best for: quick iteration, batch runs, script-driven pipelines
- Models: Imagen 4 Fast, Nano Banana 2, Nano Banana Pro
- Cost is real: $0.02–$0.13 per image

### Higgsfield CLI routes

Do not use the retired project-local browser skill `skills/higgsfield/`.

When the user wants Higgsfield specifically, invoke the global `higgsfield` skill at `~/.claude/skills/higgsfield/` with the appropriate intent — the router dispatches to the right sub-area in `references/<area>/`. Conceptual map:
- Generic image/video generation, image edits/remixes, cinematic stills, Marketing Studio image/video → sub-area `generate`
- Product photos, product ad creatives, lifestyle product shots, virtual try-on → sub-area `product-photoshoot`
- Marketplace listing cards and A+ modules → sub-area `marketplace-cards`
- Soul/face-lock/identity training → sub-area `soul-id`

These are NOT standalone skill names — do not write `Skill("higgsfield-product-photoshoot")`; write `Skill("higgsfield")` with intent context.

### Ask-the-user prompt template

When invoked, unless the user already specified a backend in the request, ask:

```
Which backend for this image?
  1) Vertex API (fast, ~$0.02–$0.13/img, good for batch)
  2) Higgsfield CLI stack (model-specific route; may use credits)

And briefly: what's the intent — photoreal ad, cartoon/stylized, text-heavy, product shot, headshot, something else?
```

Route on the answer:
- Vertex → continue in this file
- Higgsfield → delegate to the matching global CLI-backed Higgsfield skill above.

**Never silently pick a backend.** Even experienced users forget their credit balance; the ask is fast and the cost of getting it wrong is higher.

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

> **Ad-creative quality bar:** when generating ad-image prompt SETS (DCT variants / statics), apply `references/gut-wrenching-ad-format.md` — the 9-rule "Gut-Wrenching FORMAT" standard (unique formats, real-not-AI Singaporean/locale casting, headline on the ad, scroll-stopping gut-punch). Always reconcile against the active client's brand kill-list.

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

### For Character Consistency (Face-Lock)

When generating multiple images of the same person (campaign, carousel, UGC sequence, thumbnail set), prepend this block to every prompt:

> **CRITICAL CHARACTER LIKENESS:** Same person as the reference image(s). Same face, same eye colour, same jawline, same skin tone, same hair colour and texture. Do not reinterpret or idealise. Match the reference exactly.

Pair with:
- Reference images tagged `@Image1` (and `@Image2` for a secondary angle)
- Specify exact hair/clothing if they stay the same across shots
- If face drifts anyway, strengthen with named features: "same slightly crooked smile", "same gap between front teeth", "same beauty mark on left cheek"

Used by: video-director image-first pipelines, avatar-research → ad handoffs, big-angle-spotter step 11-12, any multi-image campaign with a single talent.

### Cost Optimization
- ~$0.07 per image with Nano Banana 2
- Use "thinking_level": "minimal" for simple product shots
- Use "thinking_level": "high" for complex scenes with people
- Batch generate variations — cheap enough to test multiple creatives

## Iteration Protocol

When generation misses, don't infinitely regenerate. Protocol:

### Post-render dimension gate

For any asset with a required aspect ratio or platform placement:

1. Generate with explicit canvas wording in the prompt (`TRUE 4:5 social-feed canvas`, `square 1:1 canvas`, etc.).
2. Check the saved output dimensions after render.
3. If the ratio is wrong, mark it as a renderer-control failure, not a prompt-quality success.
4. Rerender within the hard cap or normalize/export deterministically before calling it feed-safe.

Do not rely on prompt text alone for exact ratios. The AutoResearch loop showed that the same prompt can alternate between correct 4:5 and taller portrait crops.

**Hard cap:** 2 regeneration attempts per prompt. On the third failure, show the user the best of the batch and ask what to change. Cost control is non-negotiable — regen loops are how $0.07 images become $7 campaigns.

**Failure diagnostics (if-then):**

| Symptom | Root cause | Prompt mutation |
|---|---|---|
| Face drifts from reference | Character Likeness block weak or missing | Add/strengthen the block with named features |
| Composition wrong despite good subject | Layer order in prompt is off | Move camera/framing block higher |
| Tone feels off (too polished for UGC, too casual for premium) | Vibe keywords clashing | Strip aesthetic keywords back to one anchor word |
| Text/overlay garbled | Typography block missing explicit font + size | Re-add typography block from `clients/<slug>/typography.md` |
| Generated people look AI-slick | Realism block too thin | Add "natural skin texture, visible pores, slight asymmetry, casual imperfect framing" |
| Props appear that you didn't ask for | Prompt too sparse — model fills gaps | Specify what's NOT on the surface ("nothing else on the counter, no phone, no mug") |

Log recurring failures for a client to `clients/<slug>/image-generation-gotchas.md` so future batches inherit the learnings.

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

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[video-director]] (skill, 0.13)

<!-- skill-graph:end -->
