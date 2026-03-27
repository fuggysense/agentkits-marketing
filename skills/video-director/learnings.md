> Consolidated learnings → [[video-learnings]]

# Video Director — Learnings

## Confirmed Patterns

- **UGC realism constraints are the #1 differentiator** — The negative prompts (what NOT to generate) matter as much as the positive prompts. Anti-cinematic, anti-polished, anti-AI directives are what make AI video look native to social feeds.

- **Image-first pipeline produces more consistent results** for product/food/real estate — Generating reference images first gives the video model a concrete visual anchor. Without reference images, product appearance varies between frames.

- **Shock hooks can be ultra-simple** — A one-sentence prompt can outperform a detailed paragraph. Complexity ≠ quality for short-form hooks. The visual simplicity IS the pattern interrupt.

- **Negative prompts are as important as positive prompts** — Every video model tends toward "cinematic" by default. You must actively fight this with negative prompts to get UGC-authentic output.

- **Platform dictates everything** — The same product needs fundamentally different video approaches for TikTok (raw, quick-cut, front-camera) vs Instagram (slightly polished, ring-light ok) vs YouTube (can be longer, rear-camera acceptable).

- **Prompt length constraints vary by model** — Always check the model-selection-guide before drafting. Exceeding a model's prompt limit silently truncates or degrades output.

- **Multi-phase animation structure works better** — For transformation types, structure as setup -> construction/action -> reveal rather than a single continuous description. Gives the model clear timing anchors.

- **Preserving geometry/perspective is critical for transformation types** — Before and after images must share the exact same camera angle, lens, and framing. Any mismatch breaks the transformation illusion.

- **Describe realistic physical transitions, not fantasy effects** — "Construction-style renovation" beats "magical morphing." Models produce more believable output when you describe physically plausible actions.

- **Sound design cues improve scene comprehension** — Even when models can't generate audio, describing sounds (sizzle, footsteps, crowd murmur) helps them understand what physical actions are occurring and generates more contextually accurate video.

- **Character consistency template is essential for multi-shot sequences** — Without copying the exact same character description block into every prompt, subjects drift in appearance across shots.

- **8K shot prompting** — Specifying camera body (RED Komodo, ARRI Alexa) in prompts triggers higher-fidelity rendering. Quality enhancement trick, not a replacement for realism cues.

- **Seed bracketing reduces cost ~60%** — Test seeds 1000-1010, score, pick 2-3 winners. Reuse winners for all variations of that style. Platform-specific ranges (TikTok 1000-2000, IG 3000-4000) maintain channel-appropriate visual consistency.

- **Emotional blocks improve dialogue delivery** — Structure dialogue in emotional blocks (curiosity → confidence → conviction) with physical cues between each. Models interpret emotional cues as acting direction.

- **Image-to-video is the default (~90% of projects)** — Text-only generation is the exception. Image-first gives exact control over starting composition, product appearance, and brand colors.

- **Characters API best for 1min+ multi-clip** — Sora's @username handles maintain appearance automatically across clips. Max 2 characters per generation. For shorter/one-off, text-based character blocks work fine.

- **UGC automation viable via Kie.ai** — API access to Sora 2 Pro at $0.75-$3.15/clip. Enables batch generation for campaign scale.

- **Full-clip extension > last-frame extension** — Sora's clip extension reads the full previous clip context, not just the last frame. Up to 6x extension (120s from 20s base). Shorter base clips (4-8s) extend more reliably.

- **3 UGC archetypes cover most use cases** — Walk-and-talk (testimonials), driver's seat (reviews), at-home demo (product demos). Each has a distinct energy and setting.

- **Timestamp prompting gives meaningful pacing control** — [00:00-00:02] format lets you assign specific actions to time segments. Works best with models supporting longer generations.

## Troubleshooting Matrix

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Subject looks different across shots | Missing character consistency block | Use the full character template in every prompt |
| Video looks "too cinematic" | Missing negative prompts | Add anti-cinematic negative prompts (no dolly zoom, no three-point lighting, etc.) |
| Hands have wrong finger count | Hands not explicitly described | Add "anatomically correct hands with five fingers" + negative "extra fingers, missing fingers" |
| Motion feels robotic | Over-specified movement | Reduce precision, add "natural" and "organic" qualifiers, describe handheld shake |
| Transformation looks like morphing | Described as magical, not physical | Rewrite to describe realistic construction/application/renovation actions |
| Face looks plastic/uncanny | Missing skin realism cues | Add "visible pores, natural skin texture, micro-imperfections, natural shine" |
| Video feels like stock footage | Missing environmental detail | Add background clutter, ambient noise refs, imperfect lighting, pedestrians |
| Prompt gets truncated | Exceeds model limit | Check model-selection-guide for prompt length limits; condense or split into phases |
| Lighting doesn't match setting | Conflicting lighting descriptions | Ensure lighting type matches the claimed environment (no studio light in a kitchen) |
| Output doesn't match platform feel | Missing platform-specific constraints | Add platform realism notes (TikTok = front-cam, quick cuts; Instagram = slightly polished) |

## Patterns to Validate

- Does specifying exact camera model (e.g., "iPhone 15 Pro") consistently improve realism vs generic "smartphone camera"?
- How much do timing cues in prompts actually affect output quality?
- Are multi-shot prompts (describing a sequence of shots) better than single continuous prompts?
- Does the 5-Part Formula ordering (Cinematography + Subject + Action + Context + Style) produce better results than other orderings?

## Mistakes to Avoid

- (grows over time as campaigns use this skill)
