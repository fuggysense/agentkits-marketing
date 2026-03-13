---
name: video-director
version: "1.0.0"
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

# AI Video Director

Generate ready-to-paste prompts for AI video tools (Sora 2 Pro, Kling, VEO). This skill produces PROMPTS, not actual videos. Every prompt goes through a HITL review gate before the user takes it to the external tool.

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

## The Framework: 3 Pipelines, 11 Types

### Pipeline Overview

| Pipeline | Video Types | Flow |
|----------|-------------|------|
| **Direct Video** | Street Interview, Podcast, Try-On, Shock Hook, Product Commercial, POV Adventure | Single prompt -> video model |
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
├── YES -> Sora 2 Pro
└── NO
    ├── Need image-to-video? -> Kling
    ├── Educational/scientific? -> VEO
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

---

*Source: Framework extracted from David Roberts (AI Ad Guys) — @recap_david on X/Twitter. Enhanced with patterns from snubroot (Veo 3.1 Meta Framework) — GitHub snubroot/Veo-3-Meta-Framework.*
