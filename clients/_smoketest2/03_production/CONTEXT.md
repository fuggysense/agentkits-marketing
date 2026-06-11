# 03_production — Production Prep Contract

Production assets: input-image plans, reference images, storyboards, beat sheets, Higgsfield/Video Studio render prompts, footage refs, motion graphics, finished Reels, lead-magnet PDFs, sales-page HTML.

## Inputs

- L4 (working): approved scripts/concepts from `02_script/output/` (legacy) or the campaign concept workspace.
- L3 (reference): selected product assets, `../_brand/visual-characters/` (if presenters/mascots are needed), `../_brand/asset-map.md`, `../_brand/higgsfield-reference-routing.json` for render-reference routing.

## Process

Build the assets the approved concept needs, reusing the storyboard skill contract per scene: a GPT Image 2 prompt + frame breakdown, a Seedance/Kling/Veo call sheet, a `renderRequest.json`, a VO script + voice ID, and motion notes. HITL gate: the operator must approve input images, reference images, beat sheets, render prompts, and `renderRequest.json` before anything moves to render or final assembly. Only approved assets advance.

## Outputs

- `output/<TYPE><id>-<slug>/...` — per scene `scene-N/v{V}/{scene-N.md, video-prompt.md, renderRequest.json, voiceover.md, motion.md}`; per deliverable `final.mp4` + `captions.srt` (Reels), `LM###/final.pdf` (lead magnets), `SL<YYMMDD>-final.html` (sales pages).
  - Done: only operator-approved assets exist in render-ready form; finished assets hand off to `04_review/` or `../campaigns/<campaign>/` for review, scheduling, or paid-media upload.
