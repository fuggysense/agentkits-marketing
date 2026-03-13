# Image Generation — Learnings & Patterns

> This file updates continuously. Add confirmed patterns, insights, and fixes discovered during use.

## Confirmed Patterns
- Nano Banana 2 + Claude Code generates marketing images at ~$0.07 each
- UGC-style images (selfie, authentic) outperform polished studio shots for Meta ad creatives
- Specifying camera model + lens + aperture produces more photorealistic results
- Natural skin imperfections (pores, freckles, stubble) are critical for realistic people shots
- "thinking_level": "high" for complex scenes with people, "minimal" for simple product shots
- Negative prompts are essential — always exclude: stock photo, airbrushed, cartoon, watermark, extra fingers
- Before/after images MUST use identical lighting on both sides for trust

## Diagnostic Rules
- Image looks too polished/fake → Add natural imperfections, specify "casual imperfect framing"
- Text on image unreadable → Use text_rendering with high contrast colors + dark shadow
- Product shot looks flat → Add three-point lighting (key + fill + hair light for edge definition)
- Person looks like stock photo → Add specific details: visible pores, loose strands, slight off-shoulder clothing
- Wrong aspect ratio for platform → 4:5 feed, 1:1 product, 16:9 comparison, 9:16 stories

## Mistakes Not to Repeat
- Forgetting negative_prompt — get extra fingers, cartoon-style, or stock photo look
- Using "minimal" thinking_level for complex people shots — use "high"
- Not specifying lighting direction — makes or breaks realism
- Generic descriptions instead of specific details (e.g., "nice outfit" vs "dark charcoal blazer over black crew neck t-shirt, wool blend, modern slim fit")

## Reference Data
- Cost: ~$0.07 per image (Nano Banana 2)
- 5 template types: UGC Selfie, Product Hero, LinkedIn Headshot, Carousel Cover, Before/After
- Full templates: `references/nano-banana-examples.md`

## Open Questions
- (Add unresolved questions to investigate)
