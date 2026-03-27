---
name: tiktok-slideshows
version: "2.0.0"
brand: AgentKits Marketing by AityTech
category: social-content
difficulty: intermediate
description: "Use this skill for ANY TikTok-related content work: creating slideshows, Photo Mode carousels, planning content calendars, researching trending hooks, reviewing post performance, scanning competitors, or managing batch production cycles. Triggers on: \"TikTok\" combined with slideshows, carousels, Photo Mode, hooks, content pillars, batches, content calendar, performance review, or competitor analysis. Also triggers when the user mentions \"story ledger\", \"batch 01/02\", or continuing narrative threads across TikTok content cycles \u2014 even without explicitly saying \"TikTok\". Covers the full TikTok slideshow lifecycle: hook research, slide prompt construction, image generation, publishing, analytics review, and winner recreation."
triggers:
  - tiktok slideshow
  - tiktok carousel
  - tiktok photo mode
  - tiktok slides
  - photo mode batch
  - slideshow batch
prerequisites:
  - image-generation
related_skills:
  - image-generation
  - campaign-runner
  - social-media
  - content-strategy
  - copy-editing
agents:
  - copywriter
  - planner
---

## Graph Links
- **Feeds into:** [[social-media]]
- **Draws from:** [[image-generation]], [[video-director]], [[content-moat]], [[script-skill]], [[campaign-runner]]
- **Used by agents:** [[copywriter]], [[planner]]
- **Related:** [[content-moat]], [[analytics-attribution]]
- **Templates:** [[hooks-db-template]], [[story-ledger-template]], [[dashboard-template]]

# TikTok Photo Mode Slideshows v2

Story-driven TikTok Photo Mode carousels with cross-slide consistency, brand-aware prompts, and batch generation.

## When to Use This Skill

- Creating TikTok Photo Mode carousels (3-10 image slides)
- Batch-generating slideshow content for 1-2 week cycles
- Any project — loads brand context from `clients/<project>/`

---

## Step 0: Load Client Context (MANDATORY)

Before writing a single prompt, load ALL of these from `clients/<project>/`:

| File                                       | What it gives you                                                       | Required     |
| ------------------------------------------ | ----------------------------------------------------------------------- | ------------ |
| `brand-voice.md`                           | Voice, tone, terminology, anti-patterns                                 | Yes          |
| `offer.md`                                 | What the product actually is/does, value prop, differentiators          | Yes          |
| `visual-style-guide.md`                    | Visual DNA, mood, photography style, color application, narrative flows | Yes          |
| `typography.md`                            | Font hierarchy, color pairings, AI prompt text rendering instructions   | Yes          |
| `assets/brand-colors.md`                   | Hex codes, usage rules                                                  | Yes          |
| `story-bank.md`                            | Real narratives to draw from (not made-up scenarios)                    | Yes          |
| `icp.md`                                   | Who the audience is, what they care about                               | Yes          |
| `campaigns/<campaign>/content-strategy.md` | Content pillars, if they exist                                          | If available |

**If `visual-style-guide.md` or `typography.md` don't exist for a client, create them first.** Use the AURA versions as templates (`clients/aura/visual-style-guide.md`, `clients/aura/typography.md`).

---

## TikTok Photo Mode Design Rules

### Aspect Ratio
- **Always 3:4** (1080x1440) — TikTok Photo Mode native
- Do NOT use 9:16 (that's for Stories/Reels video, not Photo Mode)
- Do NOT use 1:1 or 4:5

### Text Placement
- **Upper 1/3 of frame only** — rule of thirds
- Bottom is blocked by TikTok's caption bar, buttons, profile icon
- Never place text in bottom 40%

### Consistency Rules
- Same text size, style, and placement on every slide within a post
- Same color palette across all slides in a set
- Same layout grid (margins, padding, alignment)
- Every post needs a CTA on the final slide
- **Clean > clever** — professional consistency beats creative chaos

---

## Prompt Architecture (the core upgrade)

Every image prompt is built from 4 layers, assembled in order:

### Layer 1: Brand Context (same for entire batch)

Loaded from client files. Tells the AI what brand it's creating for.

```
BRAND CONTEXT: [1-2 sentence brand identity from offer.md]. Visual personality: [from visual-style-guide.md]. Audience: [from icp.md]. Voice: [key traits from brand-voice.md].
```

Example:
```
BRAND CONTEXT: AURA is a premium fashion discovery app that rejects 95% of brands — only the 5% worth wearing. AI try-on in 4 seconds. Visual personality: warm editorial, indie magazine, quiet luxury. Audience: women 25-35 Singapore, fashion-conscious, tired of scrolling. Voice: Gen Z creator energy, confident not pretentious, anti-noise.
```

### Layer 2: Style Anchor (same for all slides in ONE post)

Defines the visual system. Written once per post, cloned to every slide.

```
STYLE ANCHOR: Background: [hex + description]. Photography: [style]. Color grading: [warm/cool/neutral + specifics]. Lighting: [type]. Text treatment: [font style, placement, color]. Negative space: [how much]. All slides in this post use this exact same visual system.
```

Example:
```
STYLE ANCHOR: Background: #170F0B warm black. Photography: B&W with warm undertones, soft film grain, editorial motion blur. Color grading: warm muted. Lighting: soft directional, dramatic rim. Text: bold condensed sans-serif (Bebas Neue), #F8F7F6 cream, upper-left, wide letter-spacing. Generous negative space. All slides in this post use this exact same visual system.
```

### Layer 3: Slide Narrative (unique per slide)

Each slide knows its role in the story and what came before/after.

```
SLIDE [N] of [total] — Role: [hook/build/tension/reveal/CTA].
Story so far: [what previous slides established].
This slide: [what happens here, how it advances the narrative].
Next slide will: [what comes after, so this slide sets it up].
```

Example:
```
SLIDE 2 of 6 — Role: reveal (the number).
Story so far: Slide 1 hooked with "we looked at 50 brands this week."
This slide: The dramatic payoff — the number "2" takes over the frame. The contrast between 50 and 2 IS the story. Stark, minimal.
Next slide will: Show the rejection reasons, so this slide should end on confident simplicity.
```

### Layer 4: Visual Description (the actual image)

The specific visual elements, built on top of the style anchor.

```
VISUAL: [Detailed description of what appears in the image — composition, subjects, text overlays, colors, textures]. Aspect: 3:4 portrait (1080x1440).

TEXT OVERLAY: "[exact words — 3-7 words max, lowercase preferred, no exclamation marks]"
TEXT RULES: Text in upper 1/3 only. One message per slide. Period at end for emphasis.

TYPOGRAPHY: [Load from client typography.md — font style reference, weight, size description, color hex per background]. Example:
  Title: bold condensed sans-serif (Bebas Neue), [color hex], large fills width, wide letter-spacing
  Body: clean sans-serif (Inter), [color hex], medium, regular weight
  Placement: upper-left / center / upper-right [must match style anchor]
```

### Layer 4b: CTA Slide Template (same for all posts in batch)

The final slide of every post uses this identical template. Build once per batch, reuse verbatim.

```
CTA TEMPLATE: [light background hex] background. "[CTA text]" in [dark text hex], centered, [font style]. Brand wordmark in [grey hex] below. Thin [accent hex] horizontal line between text and wordmark. Clean, minimal, generous white space. This slide is visually identical across all posts in this batch.
```

This ensures every post ends with the same look — brand recognition through repetition.

### Layer 5: Negative Prompt (same for entire batch)

Loaded from `visual-style-guide.md`.

```
NEGATIVE: [project-specific negative prompt from visual style guide]
```

### Assembled Prompt (what gets sent to the API)

```
[Layer 1: Brand Context]

[Layer 2: Style Anchor]

[Layer 3: Slide Narrative]

[Layer 4: Visual Description]

[Layer 5: Negative Prompt]
```

---

## Slide Narrative Flow Patterns

Every post follows one of these story structures. Pick the pattern before writing prompts.

### Pattern A: Hook → Tension → Reveal → CTA
Best for: Filter posts, comparison posts, "we rejected X" posts
1. **Hook:** Bold claim/question. Dark bg. Curiosity.
2. **Build (1-3 slides):** Evidence, details, tension. Same visual system.
3. **Reveal:** The payoff. Strongest visual moment.
4. **CTA:** Light bg switch. Clean. Brand wordmark.

### Pattern B: Timeline
Best for: Try-on demos, "then vs now", building in public
1. **Past:** Problem state. Desaturated, cold tone.
2. **Present:** Current frustration. Slightly warmer.
3. **Future:** Product solution. Warm, glowing. Contrast IS the story.
4. **CTA:** Clean light bg.

### Pattern C: Mood Board / Style DNA
Best for: Archetype reveals, style quizzes, aesthetic posts
1. **Title:** Archetype name + single teaser image
2. **Mood board (1-2 slides):** Collage of textures, items, colors
3. **Personality:** Text about what this style means
4. **Brand list:** Names (not logos) that match
5. **CTA:** Quiz link with all archetypes listed

### Pattern D: Progression
Best for: Try-on sequences, outfit comparisons, "nah → this one" posts
1. **Setup:** Context frame (where/when)
2. **Options (2-3 slides):** Sequential reveals, each building momentum
3. **Winner:** The chosen one. Decisive moment.
4. **CTA:** Clean payoff.

### Pattern E: Numbered Framework (IG-inspired, highest save rate)
Best for: Tip lists, cheat sheets, save-bait educational content
1. **Cover:** "0X [Topic] Tips" — numbered promise, tool/brand icon, creator selfie bg
2. **Steps (3-5 slides):** Pill-badge slide number, 3-column icon grid, dark bg first → white flip at midpoint
3. **Reference card:** One ultra-dense cheat-sheet slide (drives saves)
4. **CTA:** "Save this + follow" dual-action, share icon + vertical divider

### Pattern F: Confession → Lessons (IG-inspired, high trust)
Best for: Building credibility, myth-busting, insider knowledge
1. **Cover:** Confession hook — "We [mistake] with [specific $]" on red/dramatic bg
2. **Reality check:** Before/after contrast (Month 1 vs Month 6)
3. **Lessons (3-5 slides):** Each with unique photo + accent color, lesson label in small caps
4. **Synthesis:** Pure black, single aphorism ("X is a multiplier, not a substitute")
5. **CTA:** Comment emoji trigger

### Pattern G: Alternating Rhythm (IG-inspired, best for long sequences)
Best for: Multi-step systems, workflow reveals, "our stack" posts
1. **Cover:** Two-font headline (condensed sans + italic serif)
2. **Problem:** Dark diagnostic slide
3. **Steps (alternating):** Light bg → dark bg → light bg → dark bg (visual pacing)
4. **Synthesis:** Pure black text-only slide
5. **CTA:** Bookmark icon + themed emoji comment trigger

---

## Batch Generation Workflow

### Phase 1: Context Loading
1. Load ALL client files from Step 0
2. Build the Brand Context block (Layer 1)
3. Build the batch-wide Negative Prompt (Layer 5)
4. Load content pillars + story bank

### Phase 1.5: Pre-Batch Intelligence (MANDATORY for batch 2+)

Before writing a single hook, run all three sub-steps. If this is batch 1, skip to Phase 2.

#### 1.5a: Story Continuity Check

Read the project's story ledger at `clients/<project>/campaigns/tiktok-slideshows/story-ledger.md`.

1. **Check exhausted angles** — any angle used 2+ times must rest for 2 batches
2. **Check pillar balance** — no pillar >40% or <15% across all batches combined
3. **Check open threads** — previous batch may have set up promises ("the 3 yeses come later this week") that this batch should pay off
4. **Check hooks used** — never repeat a hook within 3 batches
5. **Check archetypes covered** — for Style DNA, use uncovered archetypes first
6. **Check key claims** — new content must not contradict previous claims
7. **Present constraints to user** before proceeding

If no story ledger exists, create one from the template at `skills/tiktok-slideshows/templates/story-ledger-template.md`.

#### 1.5b: Performance Review

Pull analytics for the previous batch to know what worked.

1. Pull Postiz `analytics:post` for all posts from previous batch
2. Rank posts by engagement (views, saves, engagement%)
3. Identify top 3 winners and bottom 3 underperformers
4. Log metrics to story ledger "Performance by Batch" section
5. Present to user: "Post 2 got 2.3K views (Filter pillar, Hook-Tension-Reveal pattern). Post 8 got 450 views. Recommendation: lean into Filter hooks, reduce interactive format."
6. If Postiz analytics not available (e.g., haven't posted yet), skip gracefully — note "no metrics yet" and move on

#### 1.5c: Competitor Scan

Scan competitor TikTok accounts for hooks, trends, and angles to inform this batch.

1. **Primary method: ScrapeCreators API** (requires `SCRAPECREATORS_API_KEY` in `.env`)
   - **TikTok:** Run: `python3 skills/tiktok-slideshows/scripts/competitor_scan.py <project> --profiles @handle1 @handle2 --keywords "keyword1" "keyword2" --scan-trending`
   - Script calls ScrapeCreators endpoints: `/v3/tiktok/profile/videos`, `/v1/tiktok/search/keyword`, `/v1/tiktok/hashtags/popular`, `/v1/tiktok/songs/popular`
   - **Instagram (cross-platform):** Use ScrapeCreators directly for IG carousel inspiration:
     ```bash
     # Profile overview (NOTE: use 'handle' param, not 'username' — API quirk)
     python3 skills/scrapecreators/scripts/scrape.py instagram profile <handle>
     # Posts with engagement data
     python3 skills/scrapecreators/scripts/scrape.py instagram posts <handle>
     # Individual post detail (slide-level image URLs)
     python3 skills/scrapecreators/scripts/scrape.py instagram post <shortcode>
     ```
   - Filter carousels: `media_type == 8` in the posts response
   - Slide images in `carousel_media[].image_versions2.candidates[0].url`
   - Download slides → analyze with Claude vision for typography, color, composition patterns
   - Outputs scan report to `clients/<project>/campaigns/tiktok-slideshows/competitor-scan-YYMMDD.md`
   - Appends outlier hooks to `clients/<project>/assets/video/hooks-db.md` (auto-deduped by video ID)
2. **Post-scan analysis** (Claude does this, not the script):
   - Read the scan report + updated hooks-db
   - Categorize new hooks (type: Question/Shocking claim/Contrarian/Story open/Challenge/Authority/Curiosity gap)
   - Score power level (High/Medium/Low)
   - Write "why it works" and "adapted for [PROJECT]" fields
   - For IG carousels: note structural patterns (slide count, bg rhythm, CTA format, typography system)
3. **Fallback: hooks-db.md** if script-skill has already scraped competitors
4. **Fallback: researcher agent** for manual competitive scan if no API key
5. Present to user: "Competitors are doing X, Y, Z. We haven't tried Y yet. Trending sound: [name]. Angle Z aligns with our open thread from batch-01."
6. Flag any competitor hooks that overlap with our exhausted angles

**Hooks-db location:** `clients/<project>/assets/video/hooks-db.md` (create from template at `skills/tiktok-slideshows/templates/hooks-db-template.md` if missing)

### Phase 2: Calendar + Copy
1. Build 2-week calendar: pillar, hook, slide count, story pattern per post
2. **HITL gate:** Present calendar for review
3. Write slide-by-slide text + captions (load brand voice first)
4. Map each post to a narrative flow pattern (A/B/C/D)

### Phase 3: Prompt Construction
1. For each post: write the Style Anchor (Layer 2) — one per post
2. For each slide: write the Slide Narrative (Layer 3) referencing previous/next slides
3. For each slide: write the Visual Description (Layer 4) with typography from `typography.md`
4. Assemble all 4 layers into complete prompts
5. **HITL gate:** Present all prompts grouped by post for review

### Phase 4: Image Generation

**ANTI-AD-HOC RULE:** NEVER generate standalone Python scripts in asset folders. Always use `scripts/generate_batch.py` with a JSON manifest. Ad-hoc scripts cause API key exposure, fragmented tooling, and inconsistent prompt formatting.

1. Export prompts to JSON manifest
2. Run: `python skills/tiktok-slideshows/scripts/generate_batch.py manifest.json -o <output-dir>`
3. Review outputs grouped by post (not individually)
4. Re-run failures: `--retry-failed`

### Phase 5: Assembly & Publishing
1. Review images in post groups — does each post flow as a story?
2. If text needs adjustment, handle in Canva using `typography.md`
3. Select trending music in TikTok app
4. Upload as Photo Mode, schedule via Postiz

### Phase 5.5: Ledger Update (MANDATORY)

After batch is approved, update the story ledger at `clients/<project>/campaigns/tiktok-slideshows/story-ledger.md`:

1. **Batch Log** — add entry with batch name, date, post count, arc summary, status
2. **Pillar Usage** — update counts and percentages
3. **Hooks Used** — log every hook with batch/post/pillar/pattern
4. **Angles Exhausted** — flag any angles used 2+ times, set rest period
5. **Key Claims Made** — log any new factual claims
6. **CTAs Used** — update CTA type distribution
7. **Narrative Arc Tracker** — note where the story left off, open threads for next batch
8. **Archetypes Covered** — check off any new archetypes featured

This step is not optional. Skipping it means the next batch has no continuity data.

### Phase 6: Winner Recreation (optional, after 7+ days of data)

After a batch has been live for 7+ days, analyze performance and recreate winners.

1. Pull analytics for all posts via Postiz MCP
2. Rank by engagement + saves
3. For top 3 winners:
   - Analyze what made it work (hook pattern? pillar? visual style? caption?)
   - Generate 1-2 variation ideas (new angle on same pillar, different archetype, deeper cut)
   - **Option A:** Repost exact same content (TikTok rewards reposts of winners)
   - **Option B:** Create variation post for next batch
   - **Option C:** Repurpose to IG carousel (resize from 3:4 to 4:5)
4. Log to story ledger "Winners to Recreate" section
5. **HITL gate:** Present winner analysis + recreation options to user before executing

---

## Manifest Format v2

```json
{
  "batch_name": "batch-02",
  "project": "aura",
  "model": "gemini-3.1-flash-image-preview",
  "aspect_ratio": "3:4",
  "brand_context": "AURA is a premium fashion discovery app that rejects 95% of brands...",
  "negative_prompt": "stock photo, corporate, clip art, ...",
  "posts": [
    {
      "post_id": "post01",
      "pillar": "The Filter",
      "hook": "we looked at 50 brands this week. accepted 2.",
      "pattern": "hook-tension-reveal-cta",
      "style_anchor": "Background: #170F0B warm black. Photography: B&W warm undertones...",
      "slides": [
        {
          "filename": "post01_slide1.png",
          "role": "hook",
          "narrative": "Slide 1 of 6. Hook. Bold claim...",
          "visual": "#170F0B background. Large bold text..."
        }
      ]
    }
  ]
}
```

### Script Usage

```bash
# Full batch with key rotation
python skills/tiktok-slideshows/scripts/generate_batch.py manifest.json -o clients/aura/assets/tiktok-batch-02/

# Dry run
python scripts/generate_batch.py manifest.json --dry-run

# Retry failures only
python scripts/generate_batch.py manifest.json -o output/ --retry-failed
```

Script: `scripts/generate_batch.py` — supports round-robin across `GEMINI_API_KEY`, `_2`, `_3` for 3x throughput.

---

## Cross-Slide Consistency Checklist

### Within a post (mandatory):
- [ ] Same background tone across all story slides
- [ ] Same text position (upper-left, center, etc.) on every slide
- [ ] Same font treatment (size, weight, spacing)
- [ ] Same photography style (B&W/color, grain, blur)
- [ ] Same border/margin/padding
- [ ] Narrative flows — each slide builds on the previous
- [ ] CTA slide uses light bg (consistent across all posts)

### Across posts in a batch:
- [ ] Posts in same pillar share the same visual system
- [ ] All CTA slides are visually identical (brand consistency)
- [ ] Same negative prompt across entire batch
- [ ] Brand context block unchanged across all prompts

---

## Quality Checklist

### Per Slide
- [ ] 3:4 (1080x1440)
- [ ] Text in upper 1/3
- [ ] Colors from brand palette only
- [ ] No pure black or pure white
- [ ] Text legible at phone screen size
- [ ] Matches style anchor of its post
- [ ] Advances the narrative (not standalone)

### Per Post
- [ ] 6-9 slides (sweet spot; 9 for frameworks, 6-8 for save-bait; never exceed 9)
- [ ] Tells a complete micro-story
- [ ] Slide 1 = strong hook (two-font cover system: condensed sans + italic serif accent)
- [ ] Penultimate slide = pure black synthesis (text-only, philosophical — makes CTA feel earned)
- [ ] Final slide = CTA with bookmark icon + themed comment emoji trigger
- [ ] Visual consistency across all slides
- [ ] Caption ≤ 2200 chars + 3-5 hashtags
- [ ] At least 1 background pattern interrupt (dark→light flip or colored bg)

### Per Batch
- [ ] All client context files loaded before prompting
- [ ] Brand context block consistent
- [ ] Style anchors reference visual-style-guide.md
- [ ] Typography follows typography.md
- [ ] Negative prompt from visual-style-guide.md

---

## Client Setup Checklist

For any new project, ensure these exist before generating:

```
clients/<project>/
├── brand-voice.md          # How the brand speaks
├── offer.md                # What the product is
├── icp.md                  # Who the audience is
├── story-bank.md           # Real narratives to draw from
├── visual-style-guide.md   # How it looks (create from AURA template if missing)
├── typography.md           # Font system for slides (create from AURA template if missing)
├── assets/
│   └── brand-colors.md     # Hex codes + usage rules
└── campaigns/
    └── tiktok-slideshows/
        └── story-ledger.md # Narrative continuity tracker (create from template if missing)
```

**Story ledger template:** `skills/tiktok-slideshows/templates/story-ledger-template.md`

**Templates:** Use `clients/aura/visual-style-guide.md` and `clients/aura/typography.md` as starting points for new projects.

---

## What This Skill Does NOT Cover

- **Content strategy** — stays in `clients/<project>/campaigns/`
- **Image generation internals** — stays in `image-generation` skill
- **Campaign state management** — stays in `campaign-runner` skill
- **Postiz publishing API** — stays in `skills/integrations/postiz/`

---

## Learnings

- Gemini 3.1 Flash renders text well at 3:4 — spelling accurate, typography clean
- 3:4 is the correct TikTok Photo Mode ratio; 9:16 causes cropping
- Standalone prompts (no context) produce inconsistent slides — multi-layer prompts fix this
- Style anchor + slide narrative layers are the key to cross-slide consistency
- Brand context in every prompt prevents generic/stock-looking output
- 3 API keys with round-robin = 3x throughput for batch generation
