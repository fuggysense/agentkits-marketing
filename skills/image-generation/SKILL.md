---
name: image-generation
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: content
difficulty: intermediate
description: AI image generation for marketing assets — ad creatives, social posts, product shots, headshots, before/after comparisons. Uses structured JSON prompts with Nano Banana 2 via Claude Code (~$0.07/image).
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

# Image Generation for Marketing

Generate high-quality marketing images using structured JSON prompts with AI image generation models. ~$0.07 per image via Nano Banana 2 + Claude Code.

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
| `meta.aspect_ratio` | Image dimensions | 4:5 for social, 1:1 for product/headshot, 16:9 for before/after, 9:16 for stories |
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
- Google AI Studio API key (set as `GOOGLE_AI_KEY` env var)
- Python with `requests` package
- Generation script: see `references/nano-banana-full-guide.md`

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

## Related Commands

- `/content:ads` — Write ad copy (pair with generated images)
- `/content:social` — Social content (pair with generated visuals)
- `/social:viral` — Viral content strategy
