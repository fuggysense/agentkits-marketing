---
type: learnings
domain: video
---
# Video & Visual Learnings

Consolidated from [[video-director]], [[youtube-content]], and [[image-generation]].

## Video Director

### Confirmed Patterns

- **UGC realism constraints are the #1 differentiator** — The negative prompts (what NOT to generate) matter as much as the positive prompts. Anti-cinematic, anti-polished, anti-AI directives are what make AI video look native to social feeds.
- **Image-first pipeline produces more consistent results** for product/food/real estate — Generating reference images first gives the video model a concrete visual anchor.
- **Shock hooks can be ultra-simple** — A one-sentence prompt can outperform a detailed paragraph. Complexity does not equal quality for short-form hooks.
- **Negative prompts are as important as positive prompts** — Every video model tends toward "cinematic" by default. You must actively fight this.
- **Platform dictates everything** — Same product needs different video approaches: TikTok (raw, quick-cut, front-camera) vs Instagram (slightly polished, ring-light ok) vs YouTube (can be longer, rear-camera acceptable).
- **Prompt length constraints vary by model** — Always check model-selection-guide before drafting. Exceeding limits silently truncates or degrades output.
- **Multi-phase animation structure works better** — For transformations: setup -> construction/action -> reveal rather than a single continuous description.
- **Preserving geometry/perspective is critical for transformation types** — Before and after images must share exact same camera angle, lens, and framing.
- **Describe realistic physical transitions, not fantasy effects** — "Construction-style renovation" beats "magical morphing."
- **Sound design cues improve scene comprehension** — Describing sounds (sizzle, footsteps) helps models generate more contextually accurate video even when they can't generate audio.
- **Character consistency template is essential for multi-shot sequences** — Without exact same character description in every prompt, subjects drift across shots.
- **8K shot prompting** — Specifying camera body (RED Komodo, ARRI Alexa) triggers higher-fidelity rendering.
- **Seed bracketing reduces cost ~60%** — Test seeds 1000-1010, score, pick 2-3 winners. Platform-specific ranges (TikTok 1000-2000, IG 3000-4000).
- **Emotional blocks improve dialogue delivery** — Structure dialogue in emotional blocks (curiosity -> confidence -> conviction) with physical cues between each.
- **Image-to-video is the default (~90% of projects)** — Text-only generation is the exception.
- **Characters API best for 1min+ multi-clip** — Sora's @username handles maintain appearance across clips. Max 2 characters per generation.
- **UGC automation viable via Kie.ai** — API access to Sora 2 Pro at $0.75-$3.15/clip.
- **Full-clip extension > last-frame extension** — Sora reads full previous clip context. Up to 6x extension (120s from 20s base). Shorter base clips (4-8s) extend more reliably.
- **3 UGC archetypes cover most use cases** — Walk-and-talk (testimonials), driver's seat (reviews), at-home demo (product demos).
- **Timestamp prompting gives meaningful pacing control** — [00:00-00:02] format lets you assign specific actions to time segments.

### Troubleshooting Matrix

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Subject looks different across shots | Missing character consistency block | Use the full character template in every prompt |
| Video looks "too cinematic" | Missing negative prompts | Add anti-cinematic negative prompts |
| Hands have wrong finger count | Hands not explicitly described | Add "anatomically correct hands with five fingers" + negative |
| Motion feels robotic | Over-specified movement | Reduce precision, add "natural" and "organic" qualifiers |
| Transformation looks like morphing | Described as magical, not physical | Rewrite to describe realistic construction/application |
| Face looks plastic/uncanny | Missing skin realism cues | Add "visible pores, natural skin texture, micro-imperfections" |
| Video feels like stock footage | Missing environmental detail | Add background clutter, ambient noise refs, imperfect lighting |
| Prompt gets truncated | Exceeds model limit | Check model-selection-guide for limits; condense or split |
| Lighting doesn't match setting | Conflicting lighting descriptions | Ensure lighting type matches claimed environment |
| Output doesn't match platform feel | Missing platform-specific constraints | Add platform realism notes |

### Patterns to Validate

- Does specifying exact camera model (e.g., "iPhone 15 Pro") consistently improve realism vs generic "smartphone camera"?
- How much do timing cues in prompts actually affect output quality?
- Are multi-shot prompts better than single continuous prompts?
- Does the 5-Part Formula ordering produce better results than other orderings?

## YouTube Content

### Tips

- Keep hook and context extremely short — 1 sentence each, max
- Newsletter/offer CTA must appear before YouTube's "show more" fold
- Always run De-AI sweep on generated descriptions

## Image Generation

### Confirmed Patterns

- Nano Banana 2 + Claude Code generates marketing images at ~$0.07 each
- UGC-style images (selfie, authentic) outperform polished studio shots for Meta ad creatives
- Specifying camera model + lens + aperture produces more photorealistic results
- Natural skin imperfections (pores, freckles, stubble) are critical for realistic people shots
- "thinking_level": "high" for complex scenes with people, "minimal" for simple product shots
- Negative prompts are essential — always exclude: stock photo, airbrushed, cartoon, watermark, extra fingers
- Before/after images MUST use identical lighting on both sides for trust
- Nano Banana Pro features (style saving, annotation) improve batch consistency
- Annotation workflow bridges image -> video pipeline — mark motion zones, static zones, add notes for video model direction
- Seedream 4 is a viable alternative for character consistency — better facial feature preservation across 10+ images than Nano Banana
- Two image workflows: Objects path (product -> animate around) vs Characters path (character reference -> action)

### Diagnostic Rules

- Image looks too polished/fake -> Add natural imperfections, specify "casual imperfect framing"
- Text on image unreadable -> Use text_rendering with high contrast colors + dark shadow
- Product shot looks flat -> Add three-point lighting (key + fill + hair light)
- Person looks like stock photo -> Add specific details: visible pores, loose strands, slight off-shoulder clothing
- Wrong aspect ratio for platform -> 4:5 feed, 1:1 product, 16:9 comparison, 9:16 stories

### Mistakes Not to Repeat

- Forgetting negative_prompt — get extra fingers, cartoon-style, or stock photo look
- Using "minimal" thinking_level for complex people shots — use "high"
- Not specifying lighting direction — makes or breaks realism
- Generic descriptions instead of specific details (e.g., "nice outfit" vs "dark charcoal blazer over black crew neck t-shirt, wool blend, modern slim fit")

### Reference Data

- Cost: ~$0.07 per image (Nano Banana 2)
- 5 template types: UGC Selfie, Product Hero, LinkedIn Headshot, Carousel Cover, Before/After
