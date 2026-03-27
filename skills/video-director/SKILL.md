---
name: video-director
version: "2.0.0"
brand: AgentKits Marketing by AityTech
category: content
difficulty: intermediate
description: AI video prompt generation for marketing ads — 11 video types across 3 pipelines (Direct, Image-First, Localized). Generates ready-to-paste prompts for Sora, Kling, VEO. Includes HITL review gates and full production SOP.
triggers:
  - video ad
  - AI video
  - video prompt
  - sora prompt
  - kling prompt
  - veo prompt
  - talking head video
  - UGC video
  - unboxing video
  - product video
  - street interview
  - podcast video
  - shock hook
  - video commercial
  - food video
  - real estate video
  - anatomical animation
  - ad localization
  - video generation
  - consistent character
  - UGC automation
  - sora character
  - video edit
  - character bible
  - seed bracketing
  - 8K video
  - post production
prerequisites:
  - image-generation
related_skills:
  - copywriting
  - paid-advertising
  - image-generation
  - social-media
agents:
  - copywriter
  - attraction-specialist
  - brainstormer
---

## Graph Links
- **Feeds into:** [[tiktok-slideshows]], [[social-media]]
- **Draws from:** [[image-generation]], [[copywriting]]
- **Used by agents:** [[copywriter]]
- **Related:** [[content-moat]], [[youtube-content]]

# AI Video Director

Generate ready-to-paste prompts for AI video tools (Sora 2 Pro, Kling, VEO). This skill produces PROMPTS, not actual videos — EXCEPT when using Vertex AI direct API, which can generate videos and images end-to-end from Claude Code. Every prompt goes through a HITL review gate before the user takes it to the external tool.

## Vertex AI Direct Generation (Optional)

When the user says "generate with Vertex", "use Veo directly", or "generate the video/image for me" — use the Vertex AI API to produce actual media files instead of just prompts. See `references/vertex-ai-api.md` for full config, API templates, and gotchas.

- **Imagen 4 Fast** — $0.02/img, text-to-image via Vertex AI
- **Nano Banana 2** — $0.067/img, reference-based image gen via Generative Language API
- **Nano Banana Pro** — $0.134/img, higher fidelity reference-based gen
- **Veo 3.1 Fast** — $0.15/s, text-to-video and I2V
- **Veo 3.1 Quality** — $0.40/s, higher quality, stricter safety filters

Default to NB2 for images, Veo 3.1 Fast for video unless user requests quality.

## Language & Quality Standards

**CRITICAL**: Respond in the same language the user is using.

---

## When to Use This Skill

- Creating video ads for Meta, TikTok, YouTube, Instagram
- UGC-style talking head content
- Product demonstrations, unboxings, food content
- Before/after transformations (real estate, fitness, beauty)
- Scaling winning ads to new markets (localization)
- Educational/anatomical animations for health products
- Any marketing video that needs AI generation prompts

## The Framework: 3 Pipelines, 14 Types

### Pipeline Overview

| Pipeline | Video Types | Flow |
|----------|-------------|------|
| **Direct Video** | Street Interview, Podcast, Try-On, Shock Hook, Product Commercial, POV Adventure, Walk-and-Talk, Driver's Seat, At-Home Demo | Single prompt -> video model |
| **Image-First** | Viral Food, Anatomical Animation, Real Estate Transformation, Unboxing | Generate 2-3 reference images -> feed to video model |
| **Localized Recreation** | Ad Localization at Scale | Analyze source -> reconstruct in new language/culture |

### Video Type Quick Reference

| # | Type | Pipeline | Primary Model | Best For |
|---|------|----------|--------------|----------|
| 1 | Street Interview | Direct | Sora 2 Pro | Brand awareness, social proof |
| 2 | Podcast Style | Direct | Sora 2 Pro | Authority, thought leadership |
| 3 | Try-On | Direct | Sora 2 Pro | Fashion, beauty, wearables |
| 4 | Shock Hook | Direct | Sora 2 Pro | Scroll-stopping 3s hooks |
| 5 | Product Commercial | Direct | Sora 2 Pro | Product launches, DTC |
| 6 | POV Adventure | Direct | Sora 2 Pro | Travel, lifestyle, experiences |
| 7 | Viral Food | Image-First | Nano Banana + Kling | Food/beverage, ASMR |
| 8 | Anatomical Animation | Image-First | Nano Banana + VEO | Health, wellness, supplements |
| 9 | Real Estate Transform | Image-First | Nano Banana + Kling | Renovation, interior design |
| 10 | Unboxing | Image-First | Nano Banana + Kling | E-commerce, subscription boxes |
| 11 | Ad Localization | Localized | Gemini + Sora 2 Pro | International scaling |
| 12 | On-the-Go Testimonial | Direct | Sora 2 Pro | Authentic testimonials, social proof |
| 13 | Driver's Seat Review | Direct | Sora 2 Pro | Product reviews, immediate reactions |
| 14 | At-Home Demo | Direct | Sora 2 Pro | Home products, beauty routines |

Full templates and examples: `references/video-type-catalog.md`

---

## Universal Prompt Schema (5-Part Formula)

Every video prompt follows this structure. Based on the canonical format: **[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]**.

```
1. CINEMATOGRAPHY (Camera + Lighting)
   - Shot type (close-up, medium, wide, POV)
   - Camera mount (handheld, tripod, selfie-arm, GoPro)
   - Movement (static, slow pan, follow, drift, locked)
   - Lens equivalent (16mm wide, 35mm normal, 85mm portrait)
   - Lighting type, direction, quality

2. SUBJECT (Who/What)
   - Age, gender, appearance descriptors
   - Wardrobe and accessories
   - Energy level and emotional state
   - Character consistency: [NAME/ROLE], [AGE] [ETHNICITY] [GENDER] with [HAIR], [EYES], [FEATURES], [BUILD], wearing [CLOTHING], with [POSTURE], [EMOTION]
   - Specific imperfections for realism

3. ACTION / DIALOGUE (What Happens)
   - Sequence of events with timing
   - Dialogue in quotes with delivery notes
   - Emotional beats and transitions
   - Physical actions and gestures
   - Timestamp structure for precision: [00:00-00:02] Setup, [00:02-00:04] Main action, [00:04-00:06] Reveal

4. CONTEXT (Environment + Audio)
   - Specific location with details
   - Background elements (people, objects, signs)
   - Ambient conditions (weather, noise, time of day)
   - Sound design cues (sizzle, footsteps, crowd murmur)
   - Dialogue delivery style

5. STYLE & AMBIANCE (Constraints + Mood)
   - Negative prompts (list unwanted elements without "no" or "don't")
   - Platform-specific rules
   - Overall vibe (1-2 sentence mood)
   - Anti-cinematic / anti-polished / anti-AI rules as needed
```

### Meta Block (prepend to every prompt)

```
Type: [video type from catalog]
Duration: [seconds]
Aspect Ratio: [9:16 / 4:5 / 1:1 / 16:9]
Model: [Sora 2 Pro / Kling / VEO]
```

---

## HITL Prompt Generation Pipeline

This is what Claude handles — generating the prompt and getting approval.

### Step 1: BRIEF

User describes what they need. Claude asks clarifying questions:

- What product/service is the video for?
- Who's the target audience?
- Which platform(s)? (TikTok, Instagram, YouTube, Facebook)
- What's the goal? (awareness, consideration, conversion)
- Any existing creative assets or brand guidelines?
- Budget constraints? (affects model selection)
- Do you have reference images, or do we need to generate them?

### Step 2: RECOMMEND

Claude picks the best video type + model pairing and explains why.

Present as:

```
RECOMMENDATION
- Video Type: [type] ([pipeline] pipeline)
- Model: [primary] (fallback: [fallback])
- Why: [1-2 sentence rationale]
- Duration: [range]
- Aspect Ratio: [ratio] (optimized for [platform])

Confirm? Or would you like to explore a different approach?
```

### Step 3: DRAFT

Claude generates the full prompt(s) using the Universal Prompt Schema.

**For Direct Video types:** One complete video prompt.

**For Image-First types:**
1. Generate image prompts first using `image-generation` skill
2. Present image prompts for batch review (single approval, not 3 separate gates)
3. After image approval, generate the video prompt that references those images

**For Localized Recreation:**
1. Generate analysis prompt for the source ad
2. Generate cultural adaptation checklist
3. Generate reconstruction prompt

### Step 4: REVIEW GATE

Present the complete prompt in a formatted code block with:

```
PROMPT REVIEW
==============

[Full prompt in code block]

KEY CHOICES:
- Camera: [why this camera setup]
- Subject: [why these characteristics]
- Environment: [why this setting]
- Realism: [what anti-AI measures are included]

PRE-GENERATION CHECKLIST:
- [ ] Character description is specific enough for consistency
- [ ] Camera/movement matches platform expectations
- [ ] Negative prompts block common AI artifacts
- [ ] Timing cues are clear and actionable
- [ ] Audio/ambience cues help model understand the scene
- [ ] Aspect ratio matches target platform

Approve / Edit / Reject?
```

**Nothing proceeds until approval.** After approval, output the final prompt in a clean copy-paste block.

---

## Production SOP (End-to-End Workflow)

After the HITL pipeline generates approved prompts, the user follows this SOP to produce the final video. This is the full workflow from "I have a product" to "finished video."

### Phase 1: PREPARE

Transform/generate source assets.

- **Direct Video:** No preparation needed — go straight to Phase 2
- **Image-First:** Generate reference images using `image-generation` skill
  - Match aspect ratio to final video output
  - Ensure cross-image consistency (same subject, lighting, angle)
  - For transformation types: match exact geometry/perspective between before/after
- **Localized:** Analyze source ad, complete cultural adaptation checklist

**HITL Gate:** Review and approve all source assets before proceeding.

### Phase 2: ANIMATE

Feed prompts/images to the video model.

- Paste the approved prompt into the chosen model
- For image-first: upload reference images as specified (start/end frames, reference, or single input)
- Note: prompt length limits vary by model — check `references/model-selection-guide.md`
- Use phased prompt structure for complex sequences (setup -> main action -> reveal)
- Describe realistic physical transitions, not fantasy morphing effects

**Key constraints by type:**
- Transformation videos: locked tripod, same angle throughout
- POV/adventure: handheld, natural movement
- Talking head: slight drift, selfie-arm distance
- Shock hook: close-up, abrupt start, no intro

### Phase 3: ENHANCE

Add supplementary shots and polish.

- Generate B-roll, hero shots, or CTA end cards as separate clips
- Use clip extension workflow for longer sequences: generate base clip -> extend
- First/last frame control: provide start and end images for precise transitions
- Generate multiple takes and select the best

### Phase 4: ASSEMBLE

Edit clips together + add audio.

- Combine clips in video editor (CapCut, DaVinci, Premiere, etc.)
- Add music/sound effects
- Add captions/subtitles (critical for feed video — 85% watched without sound)
- Add CTA end card
- Export at platform-native specs

**HITL Gate:** Review final assembled video before publishing.

---

## Model Selection Decision Tree

Quick decision flow — full details in `references/model-selection-guide.md`.

```
Does the video need someone TALKING?
├── YES -> Sora 2 Pro (Characters API for 1min+ multi-clip)
└── NO
    ├── Need image-to-video? -> Kling (default to image-first — 90% of projects)
    ├── Educational/scientific? -> VEO (ingredients-to-video approach)
    └── Simple UGC action? -> Sora 2 Pro
```

---

## Advanced Techniques

### Timestamp Prompting

Assign specific actions to time segments within a single generation:

```
[00:00-00:02] Medium shot: person sits at desk, looks up at camera
[00:02-00:04] Reverse shot: screen shows [product interface]
[00:04-00:06] Close-up: person's reaction, slight smile, nods
[00:06-00:08] Wide shot: pulls back to reveal full workspace
```

Works best with models that support longer generations. Useful for controlling pacing and multi-beat sequences.

### First/Last Frame Anchoring

Generate precise transitions by providing start and end images:

1. Generate "before" image with `image-generation` skill
2. Generate "after" image with matching composition
3. Feed both as first/last frames to video model
4. Model interpolates the transition between them

Best for: transformations, reveals, before/after comparisons.

### Character Consistency Across Shots

For multi-shot sequences featuring the same character, use this template:

```
[CHARACTER NAME], a [AGE]-year-old [ETHNICITY] [GENDER] with [HAIR COLOR/STYLE],
[EYE COLOR], [DISTINGUISHING FEATURES], [BUILD/HEIGHT], wearing [SPECIFIC CLOTHING],
with [POSTURE DESCRIPTION], expressing [EMOTION/ENERGY]
```

Copy this character block into every prompt in the sequence to maintain consistency.

### Clip Extension Workflow

Build longer videos from shorter generations:

1. Generate a base clip (4-8 seconds)
2. Use the last frame as input for the next generation
3. Describe continuation of the action in the next prompt
4. Repeat until desired length
5. Assemble in editor

---

## Platform-Specific Features (Sora 2 Pro)

### Characters API
Maintain consistent character appearance across clips using `@username` handles. Upload a reference image, get a handle, reference in future prompts. Max 2 characters per generation. Full details: `references/character-bible-template.md`

### Video Edits Endpoint
Remix or modify existing video clips — change backgrounds, alter actions, adjust timing without regenerating from scratch.

### Clip Extension
Extend clips with full context — the model sees the entire previous clip, not just the last frame. Extend up to 6x original length (20s base → 120s). Shorter base clips (4-8s) produce more reliable extensions.

### Batch API
Submit multiple generation jobs asynchronously. Useful for batch campaign creation — submit all prompts, collect results later.

### API vs Prompt Structure
- **API parameters:** Character references, style presets, model version, resolution, duration
- **Prompt text:** Scene description, actions, dialogue, camera, environment
- Rule: Put stable/reusable info in API params, put per-video unique info in the prompt

### Storyboard Mode (Pro)
Multi-shot storyboards with per-shot prompts. Define shots individually, Sora maintains continuity across the sequence. Best for longer narratives and multi-beat ad stories.

---

## Production Techniques

### Character Bible
Create detailed facial profiles + context profiles for recurring characters. Two methods: Sora Characters API (automatic) and text-based blocks (all models). Full template: `references/character-bible-template.md`

### Seed Management
Reduce generation costs by ~60% through systematic seed bracketing. Test seeds 1000-1010, score results, reuse winners. Platform-specific ranges for visual consistency. Full guide: `references/seed-management.md`

### Post-Production Pipeline
Enhance raw AI output: grain/texture (CapCut) → upscale 1.25-1.75x (Topaz) → voice/audio (11 Labs). Full details in `references/realism-tricks.md`

### 8K Shot Prompting
Specify professional camera bodies (RED Komodo 6K, ARRI Alexa LF, Sony FX6) in prompts to trigger higher-fidelity rendering. Full camera list: `references/cinematography-reference.md`

---

## Automation & Scale

### UGC Pipeline (Kie.ai)
API access to Sora 2 Pro, Kling, and other models. $0.75-$3.15 per clip. Single API for batch generation across models. Best for production-scale campaigns.

### 3 UGC Archetypes
| Archetype | Setting | Energy | Template |
|-----------|---------|--------|----------|
| Walk-and-Talk | Street/park, moving | High, slightly breathless | Type 12 |
| Driver's Seat | Parked car, stationary | Calm, intimate | Type 13 |
| At-Home Demo | Kitchen/bathroom/living room | Casual, real | Type 14 |

### Creative Director Pattern
System prompt for maintaining consistent creative direction across batch UGC generation. Ensures all videos feel authentic, not branded. Template in `references/video-type-catalog.md` (Type 14).

---

## Prompting Mastery

### Creativity Tradeoff
- **Short prompts** (1-2 sentences) = more creative freedom, model fills gaps artistically
- **Long prompts** (detailed 5-part schema) = more precise control, less surprise
- Use short for exploration/ideation, long for production

### Ultra-Detailed Cinematic Format
10-section prompt structure for maximum control (Sora-specific):
1. Opening shot description
2. Camera movement
3. Subject details
4. Action/performance
5. Dialogue (if any)
6. Environment detail
7. Lighting specification
8. Sound design
9. Technical specs (resolution, FPS, aspect ratio)
10. Style/mood constraints

### Weak → Strong Prompts
Transform vague prompts into production-quality outputs. Pattern: add specific person + specific place + specific action + sensory details + camera specifics. Full transformation table: `references/realism-tricks.md`

### OpenAI Recommended Prompt Structure (Alternative Format)
For Sora specifically, an alternative to the 5-Part Schema:
```
HEADER: [concept + duration + aspect ratio]
SHOT: [camera position + movement + subject framing]
TECH: [model + resolution + style constraints]
AUDIO: [dialogue + ambient + music direction]
```

---

## Transition Realism

For transformation and before/after types:

- **Physical actions over morphing:** Describe realistic construction, renovation, application — not magical transformation
- **Phased timing:** Setup (establish the before) -> Construction/action (the change happens) -> Reveal (show the after)
- **Lighting evolution:** As a space transforms, lighting should change naturally (old fluorescents -> new warm recessed)
- **Sound design as comprehension tool:** Even if the model can't generate audio, describing sounds helps it understand what physical actions are occurring

---

## Related Skills & Commands

- `/content:video` — Trigger this skill
- `image-generation` — Generate reference images for image-first pipeline
- `copywriting` — Write dialogue/script (what the person SAYS)
- `paid-advertising` — Ad strategy and platform optimization
- `social-media` — Platform-specific best practices

### Workflow Pairing

| Need | Workflow |
|------|---------|
| Write the script/dialogue | Use `copywriting` skill (video-ad-scripts.md) |
| Generate the visual prompt | Use `video-director` skill (this skill) |
| Generate reference images | Use `image-generation` skill |
| Optimize for platform | Use `paid-advertising` or `social-media` skill |

---

## References

- `references/video-type-catalog.md` — All 11 types with fill-in templates
- `references/realism-tricks.md` — Universal realism rules and negative prompt library
- `references/model-selection-guide.md` — Model comparison and decision framework
- `references/cinematography-reference.md` — Camera angles, movements, shot types, lenses
- `references/character-bible-template.md` — Character profiles, facial engineering, consistency methods
- `references/seed-management.md` — Seed bracketing, platform ranges, cost optimization
- `references/client-campaign-audit.md` — 7-step audit framework, outbound click analysis

---

*Sources: Framework extracted from David Roberts (AI Ad Guys) — @recap_david on X/Twitter. Enhanced with patterns from snubroot (Veo 3.1 Meta Framework), Mikoslab (character bibles, 8K shot prompting, seed bracketing, post-production, campaign audit), OpenAI Sora 2 Prompting Guide, and Lucas Walter UGC automation workflow.*
