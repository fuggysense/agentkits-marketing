---
name: linkedin-optimization
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: core
difficulty: intermediate
description: LinkedIn organic optimization — profile audit, algorithm deep dive, content type playbooks, creator mode, B2B sales motion, engagement strategy, newsletters, organic-to-paid compounding, plus interactive tools (profile analyzer, banner designer, content idea generator).
triggers:
  - LinkedIn profile
  - LinkedIn optimization
  - LinkedIn content
  - LinkedIn strategy
  - LinkedIn algorithm
  - LinkedIn profile audit
  - LinkedIn banner
  - LinkedIn content ideas
  - LinkedIn newsletter
  - LinkedIn engagement
  - LinkedIn creator mode
  - LinkedIn SSI
  - LinkedIn B2B
  - LinkedIn organic
prerequisites:
  - social-media
related_skills:
  - social-media
  - paid-advertising
  - copywriting
  - content-strategy
  - image-generation
  - linkedin-content
agents:
  - attraction-specialist
  - copywriter
  - brainstormer
mcp_integrations:
  optional:
    - postiz
success_metrics:
  - SSI_score
  - engagement_rate
  - profile_views
  - follower_growth
  - connection_acceptance_rate
---

## Graph Links
- **Feeds into:** (end of LinkedIn pipeline)
- **Draws from:** [[linkedin-content]], [[social-media]]
- **Used by agents:** [[attraction-specialist]]
- **Related:** [[analytics-attribution]]

# LinkedIn Optimization

LinkedIn organic optimization — profile, algorithm, content, creator mode, B2B sales, engagement, newsletters, and organic-to-paid compounding.

## Language & Quality Standards

**CRITICAL**: Respond in the same language the user is using. If Vietnamese, respond in Vietnamese. If Spanish, respond in Spanish.

**Standards**: Token efficiency, sacrifice grammar for concision, list unresolved questions at end.

---

## When to Use This Skill

- Optimizing a LinkedIn personal profile or company page
- Understanding the LinkedIn algorithm for content distribution
- Creating LinkedIn content (text posts, carousels, articles, newsletters, polls, video)
- Building a personal brand / creator mode strategy
- Running B2B sales motions via LinkedIn (SSI, warm outreach, DMs)
- Compounding organic reach into paid (thought leader ads, document ads)
- Improving engagement rates and follower growth
- Auditing a LinkedIn profile (use interactive profile analyzer)
- Designing a LinkedIn banner image (use interactive banner designer)
- Generating LinkedIn content ideas (use interactive content idea prompts)

---

## Profile Optimization Framework

### Headline (220 chars max)

**Formula options:**

| Formula | Example |
|---------|---------|
| `[Outcome] for [Audience] \| [Credibility]` | "Helping B2B SaaS companies 3x pipeline \| Ex-HubSpot" |
| `[Role] → [Result] → [How]` | "CMO → $50M ARR → Content-Led Growth" |
| `[Title] at [Company] \| [Unique angle]` | "Head of Growth at Acme \| LinkedIn Top Voice" |

**Rule:** First 40 characters must state a clear outcome — this is what shows in search results and comment previews.

### About Section (2,600 chars max)

**Structure:**
1. **Hook** (line 1-2): Metric or proof statement. No "I am a passionate..." openers.
2. **Problem** (line 3-4): What pain you solve, who you solve it for.
3. **Proof** (line 5-8): 2-3 specific results with numbers.
4. **Method** (line 9-12): How you do it (your framework/approach).
5. **CTA** (last line): One clear next step — link, DM prompt, or "Follow for [topic]."

**Formatting:** Use line breaks generously. Short paragraphs. Emojis sparingly (max 3). Bullet points for proof/method.

### Featured Section

- **1-3 tiles** (not 4+ which looks cluttered)
- **Dimensions:** 1200×628px per tile
- **Each tile needs a CTA** — link to newsletter, lead magnet, case study, or booking page
- **Order:** Most important conversion asset first

### Banner Image

- **Dimensions:** 1584×396px
- **Content placement:** Concentrate in center — profile photo overlaps bottom-left on desktop, center on mobile
- Use the **Banner Designer** interactive tool (see Interactive Tools section)
- Include: value proposition, CTA, social proof element

### Profile Photo

- Face fills 60%+ of frame
- Solid or simple background
- Eye contact with camera
- Professional lighting (natural or studio)
- Matches brand energy (formal vs approachable)

### Custom URL

- Format: `linkedin.com/in/firstname-lastname`
- Remove random numbers/characters
- Match across all social platforms if possible

### CTA Button

- Choose "Visit my website" or "Subscribe to newsletter" — direct to highest-value conversion
- Don't waste on generic company homepage

---

## Company Page Optimization

**Checklist:**

- [ ] Logo: 300×300px, clear on dark/light backgrounds
- [ ] Banner: 1128×191px, updated quarterly with current campaign/message
- [ ] Tagline: 120 chars max, outcome-focused (not "We are a leading...")
- [ ] About: First 2 lines = hook (visible before "See more"), include keywords for LinkedIn search
- [ ] Custom button: Link to highest-converting page
- [ ] Featured: Pin 1-3 posts that showcase best content/results
- [ ] Hashtags: 3 community hashtags relevant to your space
- [ ] Showcase pages: Only if genuinely different audiences (don't fragment engagement)
- [ ] Employee advocacy: Ensure top 5 employees have optimized profiles linking back

---

## Algorithm Deep Dive

LinkedIn's algorithm classifies content through a multi-phase pipeline:

| Phase | Timeframe | What Happens |
|-------|-----------|--------------|
| 1. Classification | 0-15 min | Spam check → low/high quality scoring |
| 2. Test audience | 15-60 min | Shown to ~8-10% of network |
| 3. Scoring | 1-8 hr | Engagement rate evaluated vs baseline |
| 4. Broader distribution | 8-24 hr | If passing, shown to 2nd/3rd degree |
| 5. Long tail | 1-7 days | Top content continues in feed |

**Key signals (ranked by weight):**
1. Dwell time (time spent reading)
2. Comments (especially 5+ words)
3. Shares/reposts
4. Reactions
5. Click-throughs

**For full algorithm breakdown** → see `references/linkedin-algorithm.md`

---

## Content Type Playbooks

> **For story-driven post creation**, use the `linkedin-content` skill — it provides the SIREN framework, interview pipeline, story banking, and virality engineering for high-engagement LinkedIn posts.

### Text Posts (Highest organic reach)

**Hook patterns (first 2 lines, before "See more"):**

| Pattern | Example |
|---------|---------|
| Contrarian | "Most LinkedIn advice is wrong. Here's why." |
| Metric | "I went from 500 to 50,000 followers in 6 months." |
| Question | "What's the one skill nobody taught you in school?" |
| Story | "I got fired on a Tuesday. By Friday, I had 3 offers." |
| List tease | "7 things I'd do differently if starting over:" |

**Structure:** Hook → Story/Insight → Takeaway → CTA or question. Use line breaks every 1-2 sentences. 1,200-1,500 chars optimal.

### Carousels (Document posts)

- **Slide 1:** Hook headline + visual (this is the thumbnail)
- **Slide 2:** Problem/context
- **Slides 3-8:** One idea per slide, numbered
- **Last slide:** Summary + CTA + "Follow for more [topic]"
- **Format:** PDF upload, 1080×1350px (4:5 ratio) or 1080×1080px (1:1)
- **Design:** Large text (40pt+), brand colors, minimal graphics

### Articles vs Newsletters

| Factor | Articles | Newsletters |
|--------|----------|-------------|
| Distribution | Low (algorithm-dependent) | High (direct subscriber notification) |
| SEO | Indexed by Google | Indexed by Google |
| Subscriber growth | None | Built-in subscribe CTA |
| Recommendation | Avoid unless long-form SEO play | **Preferred** — build subscriber base |

### Polls

- **Best for:** Quick engagement boost, audience research
- **Duration:** 1 week (maximizes exposure)
- **Options:** 3-4 max, make one slightly provocative
- **Add context** in post body — don't let poll stand alone
- **Caution:** Algorithm has deprioritized polls; use sparingly

### Video

- **Native upload only** (never paste YouTube links — algorithm penalizes external links)
- **Hook in first 3 seconds** — text overlay with the point
- **Subtitles mandatory** — 80%+ watch without sound
- **Optimal length:** 30-90 seconds for feed, 3-10 min for deep content
- **Vertical (9:16):** Growing in importance, appears in mobile-first placements

---

## Creator Mode & Personal Brand

### Creator Mode Benefits
- Follow button replaces Connect (builds audience faster)
- Featured and Activity sections move up
- LinkedIn Live and Newsletter tools unlock
- Profile appears in creator-specific recommendations

### Topic Hashtags
- Choose 5 hashtags that define your content territory
- Mix: 2 broad (#Marketing, #Leadership) + 3 niche (#B2BSaaS, #ContentStrategy, #GrowthHacking)
- These appear on your profile and influence who sees your content

### Building Creator Authority
1. **Consistency:** Post 3-5x/week minimum (daily optimal)
2. **Engagement:** Spend 15-30 min daily commenting on others' posts BEFORE posting
3. **Niche down:** Be known for 1-2 topics, not 10
4. **Series:** Create recurring formats ("Monday Marketing Breakdown", "Weekly Win")
5. **Collaboration:** Tag relevant people, co-create content, go Live with others

---

## B2B Sales Motion

### Profile-to-DM Funnel

```
Optimized Profile → Content → Engagement → Connection → DM → Call
```

1. **Profile = landing page** — Every section sells your expertise
2. **Content = ads** — Prove value before asking for anything
3. **Engagement = warming** — Comment on prospects' posts for 2+ weeks
4. **Connection = opt-in** — Send with personalized note referencing their content
5. **DM = conversation** — Never pitch in first message
6. **Call = conversion** — Move off LinkedIn when rapport established

### SSI (Social Selling Index) Breakdown

LinkedIn scores 0-100 across 4 pillars (25 points each):

| Pillar | What It Measures | How to Improve |
|--------|-----------------|----------------|
| Establish brand | Profile completeness + content | Complete all sections, post 3x/week |
| Find the right people | Search + profile view patterns | Use Sales Navigator, view ICP profiles daily |
| Engage with insights | Content interaction + sharing | Comment on 10+ posts/day, share with insights |
| Build relationships | Connection acceptance + messaging | Personalize requests, follow up within 48hr |

**Target:** 70+ SSI = top 5% in your industry. Check at linkedin.com/sales/ssi

### Warm Outreach 5-Touch Framework

| Touch | Action | Timing |
|-------|--------|--------|
| 1 | Like + thoughtful comment on their post | Day 1 |
| 2 | Share their post with added insight | Day 3-5 |
| 3 | Comment on another post | Day 7-10 |
| 4 | Send connection request with personal note | Day 12-14 |
| 5 | DM with value (no pitch) — share relevant resource | Day 16-20 |

**Rule:** Never pitch before Touch 5. The sequence builds familiarity so your DM isn't cold.

---

## Organic-to-Paid Compounding

### Thought Leader Ads
- Sponsor your best-performing organic posts as ads
- Shows as "[Your Name]'s post" (not company page) — higher trust
- **When to promote:** Post hits 2x your average engagement organically
- Targeting: Layer your company page audience + lookalikes

### Document Ads
- Turn top carousels into sponsored document ads
- Built-in lead gen form (name/email to unlock full document)
- Great for gated lead magnets disguised as carousels

### Retargeting Stack
1. **Video viewers** (watched 25%+) → retarget with carousel/document ad
2. **Engagement audience** (liked/commented on company posts) → retarget with direct CTA
3. **Website visitors** (LinkedIn Insight Tag) → retarget with case study/testimonial

**For full paid LinkedIn details** → see `paid-advertising/references/linkedin-ads.md`

---

## Engagement Strategy

### Comment-First Growth

Commenting on others' posts is the #1 underused growth lever:
- **Your comment appears in YOUR network's feed** (free distribution)
- **Builds relationship** with the poster (reciprocity)
- **Positions you as expert** if comments add genuine value

### Strategic Commenting Formula

```
[Agree/Disagree] + [Add a new angle or data point] + [Ask a follow-up question]
```

**Examples:**
- "Strong point on X. One thing I'd add: [insight from experience]. Have you seen this work in [adjacent context]?"
- "Disagree on Y — in my experience [counter-example]. Curious what others think?"

**Rules:**
- 5+ words minimum (algorithm ignores short comments)
- No "Great post!" or emoji-only replies
- Comment within first 60 min of post for maximum visibility
- Target 10-20 strategic comments/day on ICP and peer accounts

### Timing

| Day | Best Times (user's timezone) |
|-----|------------------------------|
| Tue-Thu | 7:30-8:30 AM, 12:00-1:00 PM |
| Mon, Fri | 8:00-9:00 AM |
| Sat-Sun | Low activity — use for scheduling, not posting |

**Note:** Test your specific audience. Use LinkedIn analytics to find when YOUR followers are online.

---

## LinkedIn Newsletter

### Growth Tactics
- **Launch announcement:** Post about newsletter + pin to Featured
- **Every issue:** Share key takeaway as standalone post linking to full newsletter
- **Cross-promote:** Add newsletter link to email signature, website, other socials
- **Collaborate:** Feature guests/experts → they share with their audience
- **Consistency:** Same day/time every week or every 2 weeks

### Subscriber Benchmarks

| Followers | Expected Subscribers (6 months) | Good Open Rate |
|-----------|--------------------------------|----------------|
| <1,000 | 100-300 | 40-50% |
| 1,000-5,000 | 300-1,500 | 35-45% |
| 5,000-20,000 | 1,500-8,000 | 30-40% |
| 20,000+ | 8,000-30,000+ | 25-35% |

### Monetization Paths
1. **Sponsorships:** Charge per issue once 2,000+ subscribers
2. **Lead gen:** Newsletter → lead magnet → email list → funnel
3. **Authority building:** Newsletter → speaking invites, partnerships, consulting leads

---

## Anti-Patterns

| Anti-Pattern | Why It Hurts | Do Instead |
|--------------|-------------|------------|
| External links in post body | Algorithm suppresses by 40-50% | Put link in first comment |
| Posting and ghosting | No engagement = no distribution | Reply to every comment within 2hr |
| Engagement pods | LinkedIn detects and penalizes | Build genuine relationships |
| Over-hashtagging | 5+ hashtags looks spammy, dilutes reach | Use 3-5 relevant hashtags max |
| Pitch in connection request | <10% acceptance rate | Use warm outreach 5-touch framework |
| Reposting without insight | No dwell time, algorithm skips | Share with 2-3 lines of added perspective |

---

## Metrics & Benchmarks

| Metric | Poor | Average | Good | Excellent |
|--------|------|---------|------|-----------|
| SSI Score | <30 | 30-50 | 50-70 | 70+ |
| Post engagement rate | <1% | 1-3% | 3-5% | 5%+ |
| Profile views/week | <50 | 50-150 | 150-500 | 500+ |
| Follower growth/month | <100 | 100-500 | 500-2,000 | 2,000+ |
| Connection acceptance rate | <20% | 20-40% | 40-60% | 60%+ |
| Newsletter open rate | <25% | 25-35% | 35-45% | 45%+ |
| DM response rate (cold) | <5% | 5-15% | 15-30% | 30%+ |
| DM response rate (warm) | <20% | 20-40% | 40-60% | 60%+ |

---

## Interactive Tools

### 1. Profile Analyzer (Vision-based Audit)

**Trigger:** User uploads a LinkedIn profile screenshot or says "audit my LinkedIn profile"

**Instructions:** Load and follow `references/profile-analyzer.md`. Scores profile 0-60 across 6 dimensions with automatic fail conditions, 3-second test, 30-second test, and specific fix recommendations.

### 2. Banner Designer

**Trigger:** User says "design my LinkedIn banner" or "create LinkedIn banner"

**Instructions:** Load and follow `references/banner-designer.md`. Asks 6 questions, then generates a 1584×396px banner using the `image-generation` skill.

### 3. Content Idea Generator

**Trigger:** User says "LinkedIn content ideas" or "generate LinkedIn hooks"

**Instructions:** Load and follow `references/content-ideas.md`. 4-prompt system: Content Themes → Expert Hooks → Story Hooks → Broad/Narrow/Niche variations.

---

## Agent Integration

| Agent | Role in LinkedIn Optimization |
|-------|-------------------------------|
| `attraction-specialist` | Profile optimization, algorithm strategy, growth tactics |
| `copywriter` | Headline formulas, about section copy, post hooks, CTA copy |
| `brainstormer` | Content ideation, theme development, creative angles |
| `brand-voice-guardian` | Ensures LinkedIn content matches brand voice |
| `conversion-optimizer` | Profile-as-landing-page CRO, CTA optimization |

---

## Related Commands

- `/content:social` — Create platform-specific social content (use with LinkedIn context)
- `/social:engage` — Develop engagement strategy
- `/social:schedule` — Create posting schedule
- `/brand:voice` — Ensure LinkedIn content matches brand voice

---

## Quality Checklist

Before publishing any LinkedIn deliverable:

- [ ] Profile changes: headline first 40 chars = clear outcome?
- [ ] Post hook: compelling in 2 lines (before "See more")?
- [ ] No external links in post body (moved to first comment)?
- [ ] CTA present and specific?
- [ ] Content matches brand voice (run through `brand-voice-guardian`)?
- [ ] Formatting: short paragraphs, line breaks, scannable?
- [ ] Hashtags: 3-5, relevant, not over-tagged?
- [ ] Timing: scheduled for Tue-Thu 7:30-8:30 AM or tested optimal time?

---

## Feedback Loop

After each LinkedIn optimization task:
1. Log what worked/didn't in `learnings.md`
2. Update benchmarks with real performance data
3. Note which hook patterns performed best for this specific audience
4. Track SSI score changes over time
