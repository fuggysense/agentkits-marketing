> Consolidated learnings → [[social-learnings]]

# TikTok Slideshows — Learnings

## Confirmed Patterns
- 3:4 (1080x1440) is the correct aspect ratio for TikTok Photo Mode, NOT 9:16
- Gemini 3.1 Flash renders text well — spelling accurate, typography clean
- Font test (260314): Baked-in text approach viable for simple slides
- **Standalone prompts produce inconsistent slides** — each image generated in isolation has no awareness of the others in the same post
- **Brand context must be in the prompt** — without it, outputs look generic regardless of hex colors specified
- **5-layer prompt architecture** (brand context → style anchor → slide narrative → visual → negative) produces dramatically better consistency than flat single-line prompts
- Style anchor (same block cloned across all slides in a post) is the #1 lever for visual consistency
- Slide narrative layer (referencing previous/next slides) makes the sequence feel like a story instead of random images
- 3 API keys with round-robin = 3x throughput for batch generation

## Mistakes (v1 → fixed in v2)
- v1 prompts were standalone text descriptions with no brand context, no style anchor, no narrative flow
- v1 referenced external styles ("SLVR Editorial") instead of the brand's own visual identity
- v1 had no `visual-style-guide.md` or `typography.md` in client profile — now required
- v1 generated only some slides per post (24 of ~55) with no consistency between them

## Batch Workflow Learnings (260314)
- **Ad-hoc scripts cause key exposure + fragmented tooling.** Two scripts were generated in asset folders with hardcoded Gemini API keys as fallback defaults. Always use `scripts/generate_batch.py` with a JSON manifest — never generate standalone Python scripts in asset folders.
- **Post ordering matters.** Origin story ("day 1: building the anti-shopping app") should be Post 1, not buried in the middle. Sequence: origin → introduce pillars one by one → deepen each in week 2 → bookend callback to close.
- **Story continuity tracking prevents repetition across batches.** Without a ledger, batch 2 would unknowingly reuse hooks, repeat angles, or contradict claims from batch 1. Story ledger template added at `skills/tiktok-slideshows/templates/story-ledger-template.md`.
- **Image file mapping > renaming.** When reordering posts, add a mapping table (old filenames → new post numbers) instead of renaming generated images. Avoids broken references and unnecessary churn.

## Integration Learnings (260315)
- Competitor research, metrics review, and winner recreation all exist in adjacent skills (content-moat, script-skill, campaign-runner, postiz MCP) but were NOT wired into the tiktok-slideshows batch workflow. Now integrated as Phase 1.5b (performance review), Phase 1.5c (competitor scan), and Phase 6 (winner recreation).
- ScrapeCreators API (`docs.scrapecreators.com`) gives direct access to TikTok competitor profiles, video metrics, keyword search, trending hashtags/sounds — 1 credit/request, simple REST with `x-api-key` header.
- Key 2 rate-limited during 27-slide generation. For large batches, increase pause to 5s+ or use only 2 keys at a time to avoid quota burns.

## Cross-Platform Carousel Insights (260315 — @sociyell IG analysis)

Source: `clients/aura/research/sociyell-carousel-analysis.md`

### Validated from IG carousel analysis (113K-follower account, 12 posts):
- **9-slide default** is the sweet spot for educational/framework IG carousels — maps to TikTok Photo Mode well
- **6-8 slides for save-bait** (cheat sheets, tip lists) — shorter = more saves per slide
- **10+ slides = engagement cliff** — never exceed 9 for TikTok slideshows
- **Pure black synthesis slide** (penultimate) is a universal pattern — text-only philosophical statement creates a contemplative pause before the CTA, making the ask feel earned. Add this to all patterns.
- **Two-font cover system** (condensed sans-serif all-caps + italic serif accent word) creates magazine-quality stopping power. Map to AURA: Bebas Neue + a Didone-style italic serif.
- **Comment emoji triggers** themed per post (not generic "follow") drive 3-7x higher comment rates than save CTAs
- **Dark→light bg flip** mid-carousel acts as a pattern interrupt — drives save behavior. The alternating light/dark rhythm on content slides prevents visual fatigue.
- **Warm cream backgrounds** (#F5F0E8) for info-dense slides outperform pure white — softer, more editorial
- **Step-number badges** (pill outline or sparkle icon) provide progress signaling that reduces abandonment
- **Bookmark icon** on CTA slide = visual priming before the text ask (pre-verbal persuasion)
- **Story opening captions** ("A friend showed me X last week") outperform declarative captions
- **Per-carousel accent color rotation** — each carousel uses ONE signature accent color. Max 3 active colors per slide.
- **Photo reuse across carousels** is fine — build an asset library, recycle signature images
- **All-caps: cover only** — interior slides use Title Case for section headers, sentence case for body
- **3-column footer strip** on cover/CTA slides ("Topic / Brand / Save") adds magazine masthead professionalism

### New narrative flow patterns added to skill:
- **Pattern E:** Numbered Framework (save-bait, highest save rate)
- **Pattern F:** Confession → Lessons (trust-building, $ specificity)
- **Pattern G:** Alternating Rhythm (best for long sequences, visual pacing)

### API discovery:
- ScrapeCreators Instagram endpoints require `handle` param, NOT `username` — the Python client sends `username` which returns 400. Direct API calls must use `handle`.
- Carousel posts: `media_type == 8` in posts response
- Slide image URLs in `carousel_media[].image_versions2.candidates[0].url`
- IG carousel analysis workflow: scrape posts → filter carousels → download slide images → Claude vision analysis → pattern extraction

## Open Questions
- Seed locking across slides: does fixing the Gemini seed improve within-post consistency? Needs testing.
- How much prompt detail is "too much" for Gemini? Very long prompts may cause the model to ignore parts.
- Image-to-image variation (using slide 1 as reference for slide 2) could be stronger than prompt-only approaches.
- Should we fix the ScrapeCreators Python client to use `handle` param for IG endpoints? Currently must use direct API calls for IG.
