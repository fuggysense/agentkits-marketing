# Video-Director v2.0.0 Upgrade — Session Context

## Date: 2026-03-14

## What This Is
Crash-safe context file preserving all research and planning for the unified video-director upgrade. If the session crashes, a new session can read this file + the plan file + the PDF extraction to continue without re-reading anything.

## Source Material

### 11 PDFs (all read, extraction saved to `active/pdf-extraction-report.md`)
1. VEO 3.1 VS SORA 2 (5p) — Model selection rule, ingredients-to-video, voice workflow
2. THE COMPLETE AI INFLUENCER SYSTEM GUIDE (9p) — Character consistency (80% of success), facial engineering, enhancor.ai, character context profile, 8K shot prompting, emotional block cues, batch generation, post-production
3. The Complete AI Influencer Niche Selection System (7p) — Whop leaderboard, Reddit mining, NotebookLM, customer journey mapping
4. THE AI CONTENT AGENCY BLUEPRINT (8p) — Premium positioning, value ladder, B-roll + AI voiceover, UTM tracking, 7-step client audit, outbound clicks metric (<1% kill, >3% scale)
5. Sora Video Prompt Structure System Guide (6p) — Header→Shot-by-shot→Tech specs→Audio mix structure
6. nanobanana, gemini 3, sora 2 (5p) — Cross-platform workflows, Gemini 3 image gen
7. Nano banana pro full guide (4p) — JSON method, style prompt saving, annotation for frame-to-video
8. HOW TO BUILD AN AI PERSONAL BRAND (6p) — Sora 2 storyboard mode, 25s clips, character cameos
9. How I Cut AI Video Costs By 60% (4p) — Seed bracketing (1000-1010), platform-specific ranges, cost reduction from 15%→70% hit rate
10. Full guide on making ai ugc that converts (5p) — UGC ad creative rules, hook formulas, authenticity signals
11. Full ai slideshow workflow (3p) — TikTok slideshow scripting, hook→storytelling→soft sell→visual cues

### Sora 2 Prompting Guide (OpenAI, March 2026)
- Characters API (@username, up to 2 chars, objects/animals too)
- API vs Prompt structure (resolution/duration/model in API, everything else in prompt)
- Clip extension (full clip context, 6x=120s)
- Video edits endpoint (POST /v1/videos/{id}/edits)
- Discrete durations: 4, 8, 12, 16, 20s
- Resolutions: sora-2 (720p), sora-2-pro (up to 1080p)
- Prompt creativity tradeoff (short=creative, long=control)
- Ultra-detailed cinematic format (10 sections)
- Weak→strong prompt transformations
- Image input for first-frame control
- Dialogue formatting best practice

### Lucas Walter UGC Automation
- n8n workflow: form trigger → Firecrawl brand scrape → context engineering → Gemini 2.5 Pro script → Kai.ai video gen → Google Drive upload
- 3 UGC archetypes: On-the-Go Testimonial, Driver's Seat Review, At-Home Demo
- Creative Director system prompt pattern
- Kai.ai pricing: Sora 2 Pro Standard (10s=$0.75, 15s=$1.35), High (10s=$1.65, 15s=$3.15)
- Characters API for consistent character reuse across videos

## Current Skill State (as of session start)

### video-director v1.0.0
- SKILL.md: 5-Part Prompt Schema, 3 pipelines, 11 types, HITL, Production SOP
- video-type-catalog.md: 11 types with fill-in templates (697 lines)
- cinematography-reference.md: Shots, angles, movements, lens effects (186 lines)
- realism-tricks.md: Camera/skin/environment realism, negative prompts (238 lines)
- model-selection-guide.md: Sora 2 Pro, Kling 3.0, VEO 3.1, NB Pro comparison (178 lines)
- learnings.md: 11 confirmed, 11 troubleshooting, 5 open questions

### image-generation v1.0.0
- SKILL.md: JSON prompts, HITL, 5 templates, carousel mode
- nano-banana-examples.md: 5 marketing templates
- nano-banana-full-guide.md: Complete schema, 100+ categories (300 lines)
- learnings.md: 13 confirmed patterns

### campaign-runner
- tiktok-content.yaml: 15-task template, 4 phases, 2 HITL gates

## Plans

### Plan A: goofy-seeking-firefly.md
- Location: `/Users/jerel/.claude/plans/goofy-seeking-firefly.md`
- Scope: 11 PDFs → consensus → integrate 10 files + create 3 new → verify
- 16 knowledge areas

### Plan B: shiny-napping-scone.md
- Location: `/Users/jerel/.claude/plans/shiny-napping-scone.md`
- Scope: Sora 2 Guide + Lucas Walter → 7-file sequential edit → verify
- 14 knowledge areas

### Unified Plan: virtual-spinning-taco.md
- Location: `/Users/jerel/.claude/plans/virtual-spinning-taco.md`
- Scope: Merges both plans into 3-step execution (consensus → integrate 13 files + create 3 → verify)
- 30 knowledge areas combined

## Status
- [x] All 11 PDFs read and extracted
- [x] Both existing plans analyzed
- [x] Current skill state explored
- [x] Unified plan written
- [ ] Consensus not yet run
- [ ] Integration not yet started
- [ ] Verification not yet done
