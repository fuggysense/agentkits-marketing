# 03_production — Production Prep Contract

Production assets: input image plans, reference images, storyboards, beat sheets, Higgsfield/Video Studio render prompts, filmed footage refs, motion graphics, finished Reel files, lead-magnet PDFs, sales-page HTML.

## Output convention (reuses storyboard skill contract)

- `output/R<###>-<slug>/scene-N/v{V}/scene-N.md` — storyboard contract (one GPT Image 2 prompt + frame breakdown)
- `output/R<###>-<slug>/scene-N/v{V}/video-prompt.md` — Seedance / Kling / Veo call sheet
- `output/R<###>-<slug>/scene-N/v{V}/renderRequest.json` — future renderer/CLI request schema
- `output/R<###>-<slug>/scene-N/v{V}/voiceover.md` — VO script + ElevenLabs voice ID
- `output/R<###>-<slug>/scene-N/v{V}/motion.md` — motion graphics notes
- `output/R<###>-<slug>/final.mp4` — rendered Reel
- `output/R<###>-<slug>/captions.srt` — subtitles
- `output/LM<###>-<slug>/final.pdf` — lead-magnet PDF
- `output/SL<YYMMDD>-final.html` — sales page HTML

## HITL rule

User approval is required for:
- input images and reference images
- beat sheets
- render prompts
- `renderRequest.json`

Only approved assets move to render or final assembly.

## Hand-off rule

Finished assets → `04_review/` or `../campaigns/<campaign-name>/` when ready for review, scheduling, or paid-media upload.
