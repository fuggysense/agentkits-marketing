## Graph Links
- **Parent skill:** [[video-director]]
- **Sibling references:** [[character-bible-template]], [[cinematography-reference]], [[client-campaign-audit]], [[realism-tricks]], [[seed-management]], [[video-type-catalog]]
- **Related skills:** [[image-generation]]

# AI Video Model Selection Guide

Decision framework for choosing the right AI video generation model. Written as capability-based decisions, not hard-coded to specific versions.

**Last verified:** 2026-03-13

---

## Model Comparison Matrix

| Capability | Sora 2 Pro | Kling 3.0 | VEO 3.1 | Nano Banana Pro | Kie.ai (API) |
|------------|-----------|-----------|---------|-----------------|-------------|
| **Talking head / dialogue** | Excellent | Limited | Good | N/A (images only) | Routes to Sora/Kling |
| **Complex multi-person scenes** | Excellent | Good | Good | N/A | Routes to best model |
| **Image-to-video conversion** | Good | Excellent | Good (ref images) | N/A | Yes (all models) |
| **Smooth transitions / timelapse** | Good | Excellent | Good | N/A | Yes |
| **Educational / anatomical** | Good | Limited | Excellent | N/A | Routes to VEO |
| **Scientific accuracy** | Good | Limited | Excellent | N/A | Routes to VEO |
| **UGC realism** | Excellent | Good | Limited | Excellent (images) | Yes |
| **Product shots** | Good | Good | Good | Excellent (images) | Yes |
| **Reference image generation** | N/A | N/A | N/A | Excellent | N/A |
| **First/last frame control** | Good | Good | Good | N/A | Yes |
| **Clip extension** | Good (6x, up to 120s) | Good | Good | N/A | Yes |
| **Character consistency** | Excellent (Characters API) | Good | Good | Good | Routes to Sora |
| **Video editing/remixing** | Good (Video Edits endpoint) | Limited | Limited | N/A | Yes |
| **Batch async generation** | Yes (Batch API) | Limited | Limited | N/A | Yes |
| **Cost per generation** | $$$ | $$ | $$ | ~$0.07 | $0.75-$3.15/clip |
| **Availability** | Limited | Generally available | Generally available | Generally available | API access |

### VEO 3.1 Ingredients-to-Video

VEO 3.1 uses an "ingredients" approach — provide detailed scene ingredients (characters, environment, actions, camera, audio) and VEO assembles them. Think of it like giving a chef ingredients vs. a recipe. Stronger for complex scenes where you want the model to make creative choices within your constraints.

### Production Budget Rule

Quick budget decision:
- **Under $10K production budget** → Sora 2 Pro (best quality for talking head / UGC)
- **$10K-$100K** → Mix of Sora + Kling (Sora for dialogue, Kling for product/transitions)
- **Over $100K** → VEO 3.1 for hero content + full post-production pipeline

### Image-to-Video Dominance

~90% of commercial projects use the image-first pipeline (reference image → video model) rather than text-only generation. Image-first gives you:
- Exact control over starting composition
- Consistent product appearance
- Better brand color accuracy
- More predictable results (lower rejection rate)

**Default to image-first** unless the video is purely talking head with no product.

### Two Image Workflows

| Path | Flow | Best For |
|------|------|----------|
| **Objects** | Generate product/scene image → feed as first frame → video model animates around static product | Product commercials, food, real estate, unboxing |
| **Characters** | Generate character reference → use Characters API or text block → video model creates action | UGC, testimonials, talking head, multi-shot sequences |

---

## Decision Framework

### Step 1: Does your video need someone TALKING?

**YES → Sora 2 Pro** (primary) or Kling with voice-over (fallback)
- Sora handles lip-sync, dialogue delivery, and facial expressions best
- If Sora unavailable: Generate video in Kling + add voice-over separately

**NO → Continue to Step 2**

### Step 2: Do you need image-to-video (starting from a reference image)?

**YES → Kling 2.5/2.6** (primary) or VEO (fallback)
- Kling excels at animating still images into motion
- Best for: product reveals, food shots, real estate walkthroughs, unboxing
- Workflow: Generate reference images with Nano Banana → Feed to Kling

**NO → Continue to Step 3**

### Step 3: Is the content educational, scientific, or anatomical?

**YES → VEO 3.1** (primary)
- Strongest at accurate anatomical cross-sections, scientific visualizations
- Smooth animation for explainer-style content
- Good at maintaining scientific accuracy across frames

**NO → Continue to Step 4**

### Step 4: Is it a simple UGC-style video (one person, one action)?

**YES → Sora 2 Pro** (primary) — best at natural human movement and environment interaction

**NO (complex scene) → Sora 2 Pro** for dialogue-heavy, **Kling** for transition-heavy, **VEO** for educational

---

## Pipeline Routing

### Direct Video Pipeline
Single prompt → video model. No intermediate image generation needed.

| Video Type | Primary Model | Fallback |
|------------|--------------|----------|
| Street Interview | Sora 2 Pro | Kling + voice-over |
| Podcast Style | Sora 2 Pro | Kling + voice-over |
| Try-On | Sora 2 Pro | Kling |
| Shock Hook | Sora 2 Pro | Kling |
| Product Commercial | Sora 2 Pro | Kling |
| POV Adventure | Sora 2 Pro | Kling |

### Image-First Pipeline
Generate 2-3 reference images → feed to video model.

| Video Type | Image Model | Video Model | Fallback Video |
|------------|------------|-------------|----------------|
| Viral Food | Nano Banana | Kling 2.5 | VEO |
| Anatomical Animation | Nano Banana | VEO 3.1 | Kling |
| Real Estate Transformation | Nano Banana | Kling 2.6 | VEO |
| Unboxing | Nano Banana | Kling 2.6 | VEO |

### Localized Recreation Pipeline
Analyze existing ad → reconstruct in new language/culture.

| Video Type | Analysis Model | Reconstruction Model | Fallback |
|------------|---------------|---------------------|----------|
| Ad Localization | Gemini (analysis) | Sora 2 Pro | Kling + voice-over |

---

## Model-Specific Prompt Tips

### Sora 2 Pro
- **Strength**: Describe dialogue in quotation marks — Sora interprets spoken words
- **Strength**: Detailed environment descriptions improve scene coherence
- **Strength**: Characters API (`@username`) maintains appearance across clips — max 2 characters per generation
- **Strength**: Video Edits endpoint for remixing/modifying existing clips
- **Strength**: Clip extension with full clip context — extend up to 6x (120s from a 20s base)
- **Strength**: Batch API for async generation of multiple clips
- **Strength**: Storyboard Mode (Pro) — multi-shot storyboards with per-shot prompts
- **Weakness**: Can struggle with hands — always include hand positioning in negative prompts
- **Tip**: Specify camera type (e.g., "shot on iPhone 15 Pro") for UGC realism
- **Tip**: Include timing cues ("in the first 2 seconds..." / "then at the 5 second mark...")
- **Tip**: Shorter clips (4-8s) produce more reliable results — extend for longer content
- **Tip**: API vs Prompt — put character/style info in API parameters, put scene/action in the prompt text
- **Tip**: Creativity tradeoff — shorter prompts = more creative freedom, longer prompts = more control

### Kling 2.5/2.6
- **Strength**: Image-to-video — provide high-quality reference images
- **Strength**: Smooth motion, transitions, and timelapse effects
- **Weakness**: Less control over dialogue/lip-sync
- **Tip**: For best results, generate reference images at the exact aspect ratio you want the video
- **Tip**: Describe the desired MOTION, not just the scene — "camera slowly pulls back to reveal..."

### VEO 3.1
- **Strength**: Scientific accuracy and smooth educational animations
- **Strength**: Cross-section visualizations, anatomical accuracy
- **Weakness**: Less natural UGC feel
- **Tip**: Use clinical/scientific language for accuracy ("sagittal cross-section", "anterior view")
- **Tip**: Specify animation style explicitly ("smooth 2D animation" vs "3D rendered")

### Nano Banana Pro (Images Only)
- **Strength**: Fast, cheap (~$0.07), consistent quality for reference images
- **Strength**: JSON prompt structure gives precise control
- **Tip**: Generate multiple angles of the same subject for image-first pipeline
- **Tip**: Match lighting and color temperature across reference images for video consistency
- **See**: `image-generation` skill for full JSON prompt templates

---

## Cost Optimization

### Budget-Conscious Approach
1. **Script + storyboard first** — don't generate until the concept is approved
2. **Use Nano Banana for reference images** (~$0.07 each) before committing to video generation
3. **Start with the cheapest model** that meets your needs — upgrade only if quality insufficient
4. **Batch similar generations** — reuse prompt structures across variations

### When to Invest in Premium Models
- Talking head ads (Sora) — dialogue quality directly impacts conversion
- Hero product videos — quality difference visible and worth the cost
- Localized campaigns — one good prompt template × multiple languages = high ROI per generation

---

### Kie.ai (API Gateway)

Access Sora 2 Pro, Kling, and other models through a single API:
- **Pricing:** $0.75-$3.15 per clip (varies by model and duration)
- **Advantage:** Single API for multiple models — no need for separate accounts
- **Advantage:** Async generation — submit batch, get results later
- **Best for:** Production-scale generation, automation pipelines
- **Integration:** Used in the Script-to-Video campaign pipeline (see `campaign-runner`)

---

## Prompt Length & Technical Constraints

| Model | Max Prompt Length | Duration Options | Resolution | Input Formats |
|-------|------------------|-----------------|------------|---------------|
| Sora 2 Pro | ~1500 chars effective | 4, 8, 12, 16, 20s (discrete) | 480p, 720p, 1080p (sora-2-pro) | Text, image, Characters API |
| Kling 3.0 | ~800 chars effective | 5-10s | Up to 1080p | Text, image, image pair |
| VEO 3.1 | ~1200 chars effective | 4/6/8s | 720p, 1080p | Text, reference images |
| Nano Banana | JSON structured | N/A (images) | 1K, 2K | JSON prompt |

**Note:** "Effective" prompt length means the point beyond which additional detail degrades output. Models may accept longer prompts but ignore or misinterpret the excess.

### Tips for Prompt Length Limits
- Lead with the most important details (subject, action) — if truncated, these survive
- Move negative prompts to dedicated negative prompt fields when available
- For Kling: describe MOTION, not static scene details (those come from the reference image)
- For VEO: timestamp prompting can compress multi-beat sequences into shorter text

---

## Version Notes

Model capabilities change rapidly. This guide documents capabilities at time of writing.

- **Sora 2 Pro**: OpenAI's video generation model. Check availability and pricing at time of use.
- **Kling 3.0**: Kuaishou's video model (previously 2.5/2.6). Versions may have been superseded.
- **VEO 3.1**: Google DeepMind's video model. Supports reference images for consistency. May have newer versions available.
- **Nano Banana Pro**: Google AI Studio image generation. Integrated via `image-generation` skill.

**When a model version is outdated:** Update the version number in this guide and the video-type-catalog templates. The capability framework and pipeline routing remain stable across versions.

### Seed Bracketing Cross-Reference

Use seed management to reduce generation costs by ~60%. Test seeds 1000-1010, pick 2-3 winners, reuse for all variations. Full methodology: `references/seed-management.md`

---

*Sources: Model pairing recommendations from David Roberts (AI Ad Guys) — @recap_david on X/Twitter. Sora 2 API features from OpenAI Sora 2 Prompting Guide. Kie.ai pricing from platform documentation. VEO 3.1 ingredients approach from Mikoslab.*
