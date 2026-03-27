## Graph Links
- **Parent skill:** [[video-director]]
- **Sibling references:** [[character-bible-template]], [[cinematography-reference]], [[client-campaign-audit]], [[model-selection-guide]], [[realism-tricks]], [[video-type-catalog]]
- **Related skills:** [[image-generation]], [[script-skill]], [[campaign-runner]]

# Seed Management & Bracketing

Reduce AI video generation costs by ~60% through systematic seed testing instead of random generation.

---

## What Is Seed Bracketing?

Instead of generating 10 random videos and hoping for a good one, test a narrow range of seeds (e.g., 1000-1010), score the results, and reuse the 2-3 winning seeds for all future generations in that style.

**Without bracketing:** 15% hit rate → ~7 wasted generations per good output
**With bracketing:** 70% hit rate → ~1.4 generations per good output
**Cost reduction:** ~60% fewer generations needed

---

## Seed Bracketing Technique

### Step 1: Initial Bracket Test
```
Generate the same prompt with seeds 1000 through 1010 (11 generations)
```

### Step 2: Score Each Result
Rate each output 1-10 on:
- Subject accuracy (does it match the prompt?)
- Motion quality (smooth, natural, no artifacts?)
- Composition (framing, lighting, overall look?)
- Platform fit (would this stop the scroll on TikTok/IG?)

### Step 3: Pick Winners
Select the 2-3 seeds that scored 7+ across all criteria. These are your "golden seeds" for this prompt style.

### Step 4: Reuse
Apply winning seeds to variations of the same prompt type:
- Same style, different product → same seed
- Same character, different scene → same seed
- Same camera setup, different subject → same seed

---

## Platform-Specific Seed Ranges

Organize seeds by platform to maintain visual consistency within each channel:

| Platform | Seed Range | Rationale |
|----------|-----------|-----------|
| **TikTok** | 1000-2000 | Raw, energetic, front-camera feel |
| **YouTube** | 2000-3000 | Slightly polished, rear-camera acceptable |
| **Instagram** | 3000-4000 | Aesthetic, ring-light friendly, curated |
| **Facebook/Meta** | 4000-5000 | Broader demographic, 4:5 optimized |
| **LinkedIn** | 5000-6000 | Professional, authority positioning |

### Why Separate Ranges?
- Each platform has a different "native look" — seeds that produce great TikTok content may look wrong on LinkedIn
- Separating ranges prevents cross-contamination of visual styles
- Makes it easy to track which seeds belong to which channel

---

## Seed Library Tracking Template

Track your winning seeds in a simple table:

```markdown
## Seed Library — [Project Name]

### TikTok Winners
| Seed | Style | Score | Notes | Date Found |
|------|-------|-------|-------|------------|
| 1003 | UGC talking head | 9/10 | Natural movement, great micro-expressions | 2026-03-14 |
| 1007 | Shock hook | 8/10 | High energy, abrupt feel | 2026-03-14 |
| 1012 | Try-on | 8/10 | Good mirror reflection, natural lighting | 2026-03-14 |

### Instagram Winners
| Seed | Style | Score | Notes | Date Found |
|------|-------|-------|-------|------------|
| 3002 | Product commercial | 9/10 | Clean composition, warm tones | 2026-03-14 |
| 3008 | Food | 8/10 | Great color saturation, appetizing | 2026-03-14 |

### YouTube Winners
| Seed | Style | Score | Notes | Date Found |
|------|-------|-------|-------|------------|
| 2005 | Podcast style | 9/10 | Natural studio feel, good depth | 2026-03-14 |
```

### Where to Store
- Per-project: `clients/<project>/assets/video/seed-library.md`
- Global defaults: can be shared across projects if visual style is consistent

---

## Cost Impact Example

### Without Seed Bracketing
- 10 videos needed for a campaign
- 15% hit rate → need ~67 generations to get 10 good ones
- At $1-3 per generation → $67-$201 total

### With Seed Bracketing
- 11 bracket tests upfront → pick 3 winners
- 70% hit rate → need ~14 generations to get 10 good ones
- Total: 11 (bracket) + 14 (production) = 25 generations
- At $1-3 per generation → $25-$75 total
- **Savings: 60-63%**

---

## Integration with Video Director

When using the video-director skill:

1. **First time using a new prompt type?** → Run a bracket test (seeds 1000-1010)
2. **Have winning seeds for this style?** → Specify seed in the prompt meta block
3. **Changing platforms?** → Switch to that platform's seed range
4. **New campaign, same style?** → Reuse seeds from the seed library

### Adding Seed to Prompts

```
META
- Type: street-interview
- Duration: 15s
- Aspect Ratio: 9:16
- Model: Sora 2 Pro
- Seed: 1003  ← from seed library
```

---

*Source: Mikoslab seed bracketing methodology (Plan A #6, #7). Validated cost reduction of ~60% across 50+ generation sessions.*
