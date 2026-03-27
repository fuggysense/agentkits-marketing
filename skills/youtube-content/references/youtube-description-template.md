## Graph Links
- **Parent skill:** [[youtube-content]]
- **Related skills:** [[content-strategy]], [[seo-mastery]], [[video-director]]

# YouTube Description Template

## Output Format

Generate as plain text (not markdown) ready to paste into YouTube. Use the structure below, filling sections from the transcript.

```
[HOOK — One punchy sentence. Specific outcome or curiosity gap.]

[CONTEXT — One sentence. Who + what problem.]

In this video, you'll learn:
• [Short takeaway 1]
• [Short takeaway 2]
• [Short takeaway 3]

---

[CTA — Pull from project offer.md or channels.json. Include link.]

---

Links Mentioned
• [Tool/Resource Name]: [URL]
• [Tool/Resource Name]: [URL]

---

Connect With Me
• [Pull from clients/<project>/channels.json]

---

Timestamps
0:00 - [Intro topic]
[TIME] - [Section 1]
[TIME] - [Section 2]
[TIME] - [Section 3]
```

## Dynamic Values

These are pulled from the project's context layer at runtime:
- **CTA text + link** — from `clients/<project>/offer.md` or `channels.json`
- **Social links** — from `clients/<project>/channels.json`
- **Tone** — from `voice/<person>/brand-voice.md`
- **Subscriber count** — ask user if not in project files

## Section Guidelines

### Hook
- ONE sentence max
- Lead with outcome or curiosity gap
- Never start with "In this video..."

### Context
- ONE sentence. Who is this for + what problem.

### What You'll Learn
- 3 bullets max (4 only if absolutely necessary)
- Short — each is one line
- Each starts with action verb (Build, Automate, Set up, Deploy)
- Conversational tone

### CTA
- Must appear early — before YouTube's "show more" truncation (~150 chars on mobile)

### Links Mentioned
- Research and find public URLs for tools mentioned in video
- Ask user for any links that can't be found via web search

### Timestamps
- Generated from Whisper transcript segments
- M:SS or MM:SS format
- First entry always 0:00
- 5-10 entries depending on video length
