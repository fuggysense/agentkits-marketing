---
name: youtube-content
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: content
difficulty: intermediate
description: "Generate complete YouTube descriptions from video transcripts. Use when the user wants a YouTube description, video metadata, timestamps, or says 'youtube description', 'describe this video', 'video description', 'youtube metadata'. Handles transcription (via transcribe skill), auto-generates timestamps, researches links for tools mentioned, and outputs paste-ready descriptions."
triggers:
  - youtube description
  - describe this video
  - video description
  - youtube metadata
  - youtube timestamps
prerequisites:
  - transcribe
  - copywriting
related_skills:
  - transcribe
  - copy-editing
  - content-strategy
agents:
  - copywriter
mcp_integrations:
  optional: []
success_metrics:
  - description_completeness
  - timestamp_accuracy
---

## Graph Links
- **Feeds into:** [[social-media]]
- **Draws from:** [[copywriting]], [[video-director]]
- **Used by agents:** [[copywriter]]
- **Related:** [[content-moat]], [[tiktok-slideshows]]

# YouTube Content

Generate complete YouTube descriptions from video transcripts — timestamps, links, and brand-consistent copy.

## When to Use

- After recording a YouTube video and need a full description
- Creating timestamps and metadata for published videos
- Generating descriptions that match your brand voice

## Workflow

1. **Transcribe** — Use the `transcribe` skill to get the video transcript (URL or local file)
2. **Read transcript** — Parse the output for text + timestamps
3. **Generate timestamps** — Identify topic shifts, create YouTube chapter markers (5-10 entries, first always `0:00`)
4. **Research links** — Web search for tools/resources mentioned in the video
5. **Write description** — Fill the template from `references/youtube-description-template.md`, pulling tone from `voice/<person>/brand-voice.md` and CTA from project's `offer.md`
6. **De-AI pass** — Run the written copy through `copy-editing` Sweep 8 (De-AI) to strip AI patterns
7. **Review with user** — Present description, ask for missing links or corrections

## Description Template

See `references/youtube-description-template.md` for the full template structure.

**Sections (in order):**
- **Hook** — ONE punchy sentence. Specific outcome or curiosity gap.
- **Context** — ONE sentence. Who + what problem.
- **What You'll Learn** — 3 short bullets max. Action verb start.
- **Newsletter/Offer CTA** — Pulled from project's `offer.md` or `channels.json`. Must appear before YouTube's "show more" truncation.
- **Links Mentioned** — All tools/resources with URLs from research step.
- **Connect With Me** — Social links pulled from `clients/<project>/channels.json`.
- **Timestamps** — Generated from transcript segments.

## Section Guidelines

### Hook
- ONE sentence max. Conversational, not salesy.
- Lead with the outcome or curiosity gap
- Good: "I automated my entire content pipeline with one Claude prompt."
- Bad: "Stop wasting hours on tasks AI can do in minutes."

### Context
- ONE sentence. Who is this for + what problem it solves. That's it.

### What You'll Learn
- 3 bullets max. Each one line. Action verb start. Conversational.

### Timestamps
- Generated from Whisper transcript segment timestamps
- Identify major topic shifts
- Format: M:SS or MM:SS
- First entry always starts at 0:00
- Aim for 5-10 entries

## Output Format

Generate as **plain text** (not markdown) — ready to paste directly into YouTube.

## Commands

- `/content:youtube-desc` — Generate YouTube description from video

## Related Skills

| If the task is... | Use instead |
|-------------------|-------------|
| Transcribing a video URL | `transcribe` |
| Writing general marketing copy | `copywriting` |
| Editing/polishing copy | `copy-editing` |
| Creating AI video prompts | `video-director` |

---

*Attribution: Adapted from remygaskell/youtube-description skill. Generalized for multi-project use with context layer integration.*
