---
name: transcribe
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: utility
difficulty: beginner
description: "Transcribe video from any URL (YouTube, Instagram, X/Twitter, TikTok, Facebook, Vimeo, etc.) into text. Use when the user says transcribe this video, transcribe [url], get the transcript, what does this video say, or pastes a social media / video URL with transcription intent. Supports 1000+ sites via yt-dlp. No API keys required."
triggers:
  - transcribe
  - transcribe video
  - transcribe url
  - get transcript
  - video to text
  - what does this video say
prerequisites: []
related_skills:
  - youtube-content
  - content-strategy
agents:
  - researcher
  - copywriter
mcp_integrations:
  optional: []
success_metrics:
  - transcript_accuracy
  - segment_count
---

## Graph Links
- **Feeds into:** [[youtube-content]], [[video-director]]
- **Draws from:** (independent -- utility)
- **Used by agents:** (utility)
- **Related:** [[deep-research]]

# Video Transcriber

Transcribe any video URL into text using yt-dlp (download) + faster-whisper (transcription).

## When to Use

- Transcribing competitor videos for analysis
- Extracting content from social media videos for repurposing
- Creating transcripts for YouTube descriptions (pairs with `youtube-content` skill)
- Research — turning video content into searchable text

## Dependencies

- Python 3.8+
- `faster-whisper` (pip3 install faster-whisper)
- `yt-dlp` (pip3 install yt-dlp)
- `ffmpeg` (brew install ffmpeg on macOS)

## Invocation

`/transcribe <url>` — the URL is passed as the skill argument.

If no URL is provided, ask the user for it.

## Workflow

1. Ask the user: "Include timestamps?" (Yes / No)
2. Run the transcription script:

```bash
python3 <skill_path>/scripts/transcribe_url.py "<url>" [--timestamps]
```

Add `--timestamps` if the user chose yes.

3. Present the transcript output to the user — the script prints the transcript directly to stdout.

## Options

- `--model <size>` — Whisper model size (default: `medium`). Use `small` for faster but less accurate results, `large-v3` for maximum accuracy.
- `--timestamps` — Prefix each segment with `[M:SS]` timestamp.

## Dependency Errors

If the script exits with missing dependency errors, relay the install instructions it prints:

```bash
pip3 install yt-dlp faster-whisper
brew install ffmpeg  # macOS
```

## Output

The script prints:
- Metadata header (platform, title, uploader, duration)
- Transcript text (grouped into ~30-second paragraphs, or timestamped segments if `--timestamps` flag used)
- Completion summary to stderr (segment count, language)

## Related Skills

| If the task is... | Use instead |
|-------------------|-------------|
| Writing YouTube descriptions from transcripts | `youtube-content` |
| Creating content from video research | `content-strategy` + this skill |
| Analyzing competitor video ads | `paid-media-audit` Phase 6 + this skill |

---

*Attribution: Adapted from remygaskell/transcribe skill. Enhanced with AgentKits integration and agent mappings.*
