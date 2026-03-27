---
type: learnings
domain: social
---
# Social Media Learnings

Consolidated from [[social-media]], [[linkedin-content]], [[linkedin-optimization]], and [[tiktok-slideshows]].

## LinkedIn Content

### Confirmed Patterns

- Unfindable content outperforms findable content by 3-5x (based on analysis of 35 posts across two Singapore-based creators)
- Posts activating 4-5 SIREN elements consistently hit 200+ likes (breakout tier)
- Vulnerability narratives have the highest ceiling but can't be stacked back-to-back
- Third-person stories (writing about someone else) drop engagement 50-70%
- Framework-first posts are useful but underperform story-first posts

### Diagnostic Rules

- Post underperforming? Check: (1) Is the author IN the story? (2) Are stakes concrete? (3) Do first 2 lines trigger emotion?
- Low comment-to-like ratio (<30%)? Post is agreeable but not provocative enough — add rebellion element
- High comments but low likes? Strong community activation — good sign, story resonates deeply with niche

### Reference Data

- SIREN framework derived from: 35 LinkedIn posts, 2 creators (Kelvin Kuok 9.6K followers, Michelle Koh 5K followers), March 2026
- Breakout threshold: 200+ likes
- Strong threshold: 100-200 likes
- Average threshold: 50-100 likes
- Engagement pod detection: comment-to-like ratio >60%

### Open Questions

- How does SIREN performance vary by industry/niche?
- Optimal posting frequency before audience fatigue?
- Does the unfindable content principle hold for larger accounts (50K+ followers)?

## TikTok Slideshows

### Confirmed Patterns

- 3:4 (1080x1440) is the correct aspect ratio for TikTok Photo Mode, NOT 9:16
- Gemini 3.1 Flash renders text well — spelling accurate, typography clean
- Font test (260314): Baked-in text approach viable for simple slides
- **Standalone prompts produce inconsistent slides** — each image generated in isolation has no awareness of the others in the same post
- **Brand context must be in the prompt** — without it, outputs look generic regardless of hex colors specified
- **5-layer prompt architecture** (brand context -> style anchor -> slide narrative -> visual -> negative) produces dramatically better consistency than flat single-line prompts
- Style anchor (same block cloned across all slides in a post) is the #1 lever for visual consistency
- Slide narrative layer (referencing previous/next slides) makes the sequence feel like a story instead of random images
- 3 API keys with round-robin = 3x throughput for batch generation

### Mistakes (v1 -> fixed in v2)

- v1 prompts were standalone text descriptions with no brand context, no style anchor, no narrative flow
- v1 referenced external styles ("SLVR Editorial") instead of the brand's own visual identity
- v1 had no `visual-style-guide.md` or `typography.md` in client profile — now required
- v1 generated only some slides per post (24 of ~55) with no consistency between them

### Batch Workflow Learnings (260314)

- **Ad-hoc scripts cause key exposure + fragmented tooling.** Two scripts were generated in asset folders with hardcoded Gemini API keys as fallback defaults. Always use `scripts/generate_batch.py` with a JSON manifest — never generate standalone Python scripts in asset folders.
- **Post ordering matters.** Origin story ("day 1: building the anti-shopping app") should be Post 1, not buried in the middle. Sequence: origin -> introduce pillars one by one -> deepen each in week 2 -> bookend callback to close.
- **Story continuity tracking prevents repetition across batches.** Without a ledger, batch 2 would unknowingly reuse hooks, repeat angles, or contradict claims from batch 1.
- **Image file mapping > renaming.** When reordering posts, add a mapping table (old filenames -> new post numbers) instead of renaming generated images.

### Open Questions

- Seed locking across slides: does fixing the Gemini seed improve within-post consistency? Needs testing.
- How much prompt detail is "too much" for Gemini? Very long prompts may cause the model to ignore parts.
- Image-to-image variation (using slide 1 as reference for slide 2) could be stronger than prompt-only approaches.

## Social Media (General)

> No confirmed learnings captured yet in [[social-media]]. Will populate as social campaigns produce insights.

## LinkedIn Optimization

> No confirmed learnings captured yet in [[linkedin-optimization]]. Will populate as profile audits produce insights.
