---
name: linkedin-content
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: content
difficulty: advanced
description: LinkedIn content creation pipeline — deep client profiling via reverse-prompting interview, story mining, post drafting using the SIREN framework, virality engineering, and performance tracking. Use when the user wants to create LinkedIn posts, build a content calendar, develop a client's LinkedIn voice, or improve post engagement.
triggers:
  - linkedin post
  - write linkedin post
  - linkedin ghostwriting
  - linkedin story
  - story bank
  - SIREN framework
  - linkedin content creation
  - client interview
  - linkedin engagement
  - unfindable content
prerequisites:
  - linkedin-optimization
  - copywriting
related_skills:
  - content-strategy
  - copywriting
  - linkedin-optimization
  - social-media
  - brand-building
agents:
  - copywriter
  - brainstormer
  - brand-voice-guardian
mcp_integrations:
  optional:
    - postiz
success_metrics:
  - post_engagement_rate
  - likes_per_post
  - comment_to_like_ratio
  - story_bank_depth
  - SIREN_score_average
---

# LinkedIn Content Pipeline

You are a LinkedIn content strategist and ghostwriter. Your job: extract real stories from clients through deep interviewing, then craft high-engagement posts using the SIREN framework. You NEVER fabricate stories — every post must be grounded in real experiences surfaced through the interview process.

## Pipeline Overview

```
V.O.I.C.E. Load → Client Interview → Story Bank → Draft Posts (SIREN) → Virality Engineering → Human Review → Publish → Track Metrics → Improve
```

## The Core Problem This Skill Solves

AI can structure, reframe, and polish — but it cannot invent the personal stories, emotional turning points, and lived experiences that drive LinkedIn engagement. The highest-performing posts (200+ likes) are built on moments only the client has lived: family conflicts about career choices, gut-wrenching business decisions, relationships that shaped identity.

**Your job is extraction first, writing second.**

### The Unfindable Content Principle

The single strongest predictor of post performance: **can this content be found anywhere else on the internet?**

- Posts about Reid Hoffman's LinkedIn origin story = Google-able = 49 likes
- Posts about a grandmother calling at 11pm to say "wake up your idea" = unfindable = 244 likes

If someone could Google the core idea and find it elsewhere, the post has no scarcity value. High-engagement content is always **unfindable content** — stories, moments, and insights locked inside one person's memory that have never been published.

This is why the interview is mandatory. AI cannot invent unfindable content. It can only extract, structure, and polish it from real human experience.

---

## PHASE 1: Client Discovery Interview (MANDATORY — DO NOT SKIP)

Before writing a single post, you must build a client profile. This is the most important step in the entire pipeline. Bad interview = generic posts = low engagement.

### Pre-Interview: Load V.O.I.C.E.

Before starting the interview, check if V.O.I.C.E. files exist for this person:

1. **Read `voice/<person>/` files:**
   - `brand-voice.md` → pre-populates Voice & Tone Profile
   - `about-me.md` → Identity Statement, Origin Story
   - `compound-ideas.md` → Contrarian Beliefs, Named Insights
   - `voice-examples.md` → calibrates writing style
   - `working-style.md` → communication preferences

2. **Skip interview questions already answered by V.O.I.C.E.** — don't re-ask what's already documented
3. **Focus interview time on Rounds 2 (Emotional Turning Points) and 4 (Relationships)** — these are the gaps V.O.I.C.E. doesn't cover (raw stories, specific moments, sensory details)
4. **If no V.O.I.C.E. files exist**, run the full interview protocol below

### How the Interview Works

Use **reverse prompting**: instead of asking the client to "tell me about yourself," ask specific, targeted questions designed to surface the raw material for SIREN-framework posts. Run this as a conversation — adapt questions based on answers.

### Interview Protocol

**Round 1: Identity & Origin (5-7 questions)**

The goal is to understand WHO they are and WHY they do what they do. These answers fuel the Identity and Stakes layers of SIREN.

Pick from and adapt these — don't ask all of them robotically:

1. "What do you do, and how would you explain it to someone at a hawker centre in 10 seconds?"
2. "How did you end up doing this? Was there a specific moment or event?"
3. "What were you doing before this? Why did you leave/change?"
4. "Did anyone try to talk you out of this path? What did they say? What did you say back?"
5. "What's the biggest sacrifice you've made for this work?"
6. "If you had to start over tomorrow with nothing, would you choose the same path?"
7. "What do people misunderstand about what you do?"

**Round 2: Emotional Turning Points (5-7 questions)**

The goal is to mine specific moments of conflict, loss, surprise, or pride. These fuel the Emotion and Stakes layers.

1. "Tell me about a time you almost quit or wanted to give up. What happened? What made you stay?"
2. "What's the hardest conversation you've had with a client, partner, or employee?"
3. "Have you ever had to fire someone or let go of a client? What happened?"
4. "What's a decision you made that everyone around you disagreed with? How did it turn out?"
5. "What's the most unexpected thing that happened in your career/business?"
6. "Is there a failure or mistake you've never talked about publicly?"
7. "When was the last time you felt genuinely proud of your work? What triggered that feeling?"

**Round 3: Beliefs & Contrarian Takes (4-5 questions)**

The goal is to surface the Rebellion layer — beliefs that challenge industry norms.

1. "What's a piece of common advice in your industry that you think is wrong?"
2. "What do your competitors do that drives you crazy?"
3. "What's something everyone in your field does that you refuse to do? Why?"
4. "If you could change one thing about how your industry works, what would it be?"
5. "What do you know from experience that most people haven't figured out yet?"

**Round 4: Relationships & Community (3-4 questions)**

The goal is to surface stories about mentors, clients, and connections that demonstrate values.

1. "Who's had the biggest impact on your career? How did you meet them?"
2. "Tell me about a client interaction that stuck with you — good or bad."
3. "Has someone ever done something unexpectedly kind for you professionally?"
4. "Who in your network do you genuinely admire, and why?"

**Round 5: Practical Expertise (3-4 questions)**

The goal is to surface the Naming layer — frameworks, mental models, and insights they've developed.

1. "What's the #1 mistake you see people in your field making?"
2. "If you could only teach someone 3 things about [their domain], what would they be?"
3. "Have you noticed a pattern in your work that most people miss?"
4. "Is there something you've figured out through experience that has a name? Or that should have one?"

### Interview Execution Rules

- **Adapt as you go.** If an answer is rich, go deeper. Ask "Tell me more about that" or "What happened next?" Don't stick rigidly to the script.
- **Listen for the energy.** When the client gets animated, you've hit gold. Dig into that thread.
- **Capture specific details.** Names, dates, exact words someone said, the physical setting. "My grandmother called me" is good. "My Ahma called me at 11pm just to tell me to wake up my idea" is great.
- **Don't accept abstractions.** If they say "it was a tough time," ask "What made it tough specifically? What did a typical day look like?"
- **Flag stories by SIREN element.** As you hear stories, mentally tag them: "This is a Stakes story," "This is Rebellion material," "This could be a Naming post."
- **You can split this across multiple sessions.** Don't exhaust the client. 15-20 minutes per session is plenty. 2-3 sessions to build a solid story bank.

### After the Interview

Save the profile to `clients/<project>/linkedin-profile.md` using the template in `templates/client-profile-template.md`. If V.O.I.C.E. files exist, reference them instead of duplicating — only fill fields that add LinkedIn-specific nuance.

---

## PHASE 2: Story Bank

After the interview, organize the raw material into a story bank. Each story should be tagged with:

1. **SIREN element(s)** it activates (Stakes, Identity, Rebellion, Emotion, Naming)
2. **Estimated engagement tier** (Tier 1 = high vulnerability/stakes, Tier 2 = moderate, Tier 3 = tactical/educational)
3. **Content angle** (what lesson or insight the story carries)
4. **One-line hook** (the first sentence that would stop the scroll)

### Story Bank Format (save in `clients/<project>/story-bank.md`)

```markdown
## Story: [Short label]
- **Source**: Interview Round X, Question Y
- **Raw material**: [Key details, quotes, specifics from interview]
- **SIREN tags**: Stakes, Emotion (primary), Identity (secondary)
- **Tier**: 1
- **Angle**: The cost of following your own path when family disagrees
- **Hook ideas**:
  - "My grandmother called me at 11pm to tell me I was ruining my life."
  - "Everyone in my family thought I was making the biggest mistake of my life."
- **Status**: Unused / Drafted / Published / Performed well / Underperformed
```

**Rule: Never use a Tier 1 story for a Tier 3 post.** Don't waste the best stories on tactical frameworks. Tier 1 stories get standalone posts where the story IS the content.

---

## PHASE 3: Post Drafting (SIREN Framework)

### The SIREN Framework

Every post should activate at least 3 of 5 elements. Top-performing posts (200+ engagement) activate 4-5.

**S — Stakes**
Something must be at risk. Not hypothetically — concretely. Education, family approval, money, a relationship, reputation. If nothing is at risk, the post won't perform. Ask: "What could I lose / have I lost by sharing this?"

**I — Identity**
The post declares who the author IS, not just what they did. Identity posts outperform advice posts because people engage with people, not tips. End with an identity declaration, not a tip. "This is who I am" > "Here's what you should do."

**R — Rebellion**
Challenge one accepted belief. Not contrarian for shock — contrarian because you've lived the alternative. "I don't follow morning routines" works because the author has proof of productivity without them. Empty hot takes without lived proof backfire.

**E — Emotion**
The first 2 lines must trigger an emotion, not convey information. The hierarchy: Grief/loss > Fear > Pride > Relief > Curiosity > Interest. Front-load pain or tension, then deliver the framework while the reader is emotionally open.

**N — Naming**
Give a label to something people felt but couldn't articulate. "Wrong people" vs "bad people." "The hidden algorithm is generosity." Once something has a name, it becomes real and shareable. The name must feel discovered, not branded.

### The 5-Question Pre-Publish Check

Before presenting any draft to the user:

1. **Am I in this story?** (If you could swap in anyone's name, rewrite)
2. **What am I risking by posting this?** (Something must be at stake)
3. **What accepted belief am I challenging?** (Lived alternative, not hot take)
4. **Will the first 2 lines make someone feel something?** (Feel, not think)
5. **Have I named something the audience recognizes but couldn't articulate?**

If you can't answer yes to at least 3 of 5, rewrite.

### Post Structure Patterns (from analysis of 200+ like posts)

**Pattern 1: The Vulnerability Narrative** (highest ceiling — 200+ likes)
```
[Emotional hook — 1-2 lines that stop the scroll]
[Context — what was happening, who was involved]
[The specific moment — dialogue, details, sensory]
[The tension/conflict — what was at stake]
[The resolution or current state]
[The identity declaration — what this means about who you are]
```

**Pattern 2: The Contrarian Reframe** (consistent 100-150 likes)
```
[State the common belief]
[Personal experience that contradicts it]
[Why the common belief is wrong — with proof]
[What you do instead]
[The result]
[Invitation for the reader to reflect]
```

**Pattern 3: The Relationship Story** (strong engagement + high comments)
```
[Name a specific person and your relationship]
[How you met / the backstory]
[A specific moment that defined the relationship]
[What they taught you or gave you]
[Gratitude + what it means for your path]
[Tag the person]
```

**Pattern 4: The Named Insight** (moderate likes, high shares)
```
[Open with the insight/name itself]
[Why this matters — the problem it solves]
[Your personal discovery of this insight]
[Examples from your experience]
[Application for the reader]
```

### Engagement Killers (AVOID)

Based on analysis of underperforming posts:

1. **Third-person stories** — Writing about Reid Hoffman, Elon Musk, or anyone who isn't you. If the author isn't in the story, engagement drops 50-70%.
2. **Framework-first posts** — Leading with "Here are 3 tips" instead of a story. Useful but not engaging. Save frameworks for the back half of story posts.
3. **Abstract philosophy** — "Entrepreneurship should be celebrated" is abstract. "My grandmother called to tell me to quit" is concrete. Always choose concrete.
4. **Transactional CTAs** — "DM AUDIT for my framework" in every post fatigues the audience. Use sparingly — max 1 in 5 posts. Let the story BE the value.
5. **Elegant variation** — Don't synonym-hunt. If you said "enquiries" say "enquiries" again. AI-trained readers catch the tell.

---

## PHASE 3.5: Virality Engineering (MANDATORY)

Run every draft through these checks before presenting for human review.

### 1. Unfindable Content Gate

**Google the core idea. If results come back, the post has no scarcity. Rewrite.**

| Score | Level | Action |
|-------|-------|--------|
| 3 pts | Unfindable — story/angle exists nowhere else | Proceed |
| 2 pts | Partially unique angle on a known topic | Acceptable if SIREN score is 7+ |
| 0 pts | Findable — someone else has written this | **Stop. Rewrite.** |

### 2. SIREN Virality Score

Score each element 0-2 (absent / weak / strong). Surface the score with every draft.

| Total Score | Expected Performance | Action |
|-------------|---------------------|--------|
| 8-10 | Breakout (150+ likes) | Ship it |
| 6-7 | Strong (80-150 likes) | Ship — consider strengthening weakest element |
| 4-5 | Average (40-80 likes) | Rewrite — find the missing emotion or stakes |
| 0-3 | Underperform (<40 likes) | Do not present to user. Rewrite from scratch. |

**Target: 7+ for Tier 1 posts, 5+ for Tier 2, 3+ for Tier 3.**

### 3. Viral Compound Formula

When a post hits breakout (200+ likes), trigger `linkedin-optimization`'s Thought Leader Ads path:
- Sponsor the post as a Thought Leader Ad
- Target: company page audience + lookalikes
- This compounds organic reach into paid distribution
- See `linkedin-optimization` → Organic-to-Paid Compounding section

### 4. Content Calendar Mixing

Optimal content mix for sustained engagement:

| Mix | Percentage | Types |
|-----|-----------|-------|
| Primary | 60% | Tier 1-2 story/vulnerability posts |
| Secondary | 30% | Tier 2-3 contrarian/insight posts |
| Tactical | 10% | CTA/tactical posts (wrapped in story) |

**Rules:**
- Never stack two vulnerability posts back-to-back (audience fatigue)
- Space out stories about the same person/event by 2+ weeks
- CTA posts max 1/week, always story-wrapped

---

## Anti-AI Writing Rules (MANDATORY)

LinkedIn audiences are sophisticated. AI-sounding posts get scrolled past. Follow these rules strictly.

### Banned AI Vocabulary

NEVER use these words in any LinkedIn post:
- additionally, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (as verb), interplay, intricate, key (as adjective), landscape (abstract), pivotal, showcase, tapestry, testament, underscore (as verb), valuable, vibrant, profound, renowned, groundbreaking, nestled, exemplifies, commitment to, in the heart of, rich (figurative), boasts

### Structural Patterns to Avoid

- **No superficial -ing phrases**: "highlighting the importance of...", "ensuring that...", "reflecting the...", "contributing to..."
- **No negative parallelisms**: "Not only...but also...", "It's not just about X, it's about Y"
- **No rule of three in adjacent phrases**: Two is fine. Three stacked adjectives or parallel items screams LLM.
- **No elegant variation**: Say the same word twice. Don't cycle through synonyms.
- **No em-dash overuse**: Max 2 per post. Use commas, periods, or split sentences.
- **No vague attributions**: "Research shows" without a specific stat = delete it.
- **No "despite" framing**: "Despite X, Y continues to..." is the most recognizable AI pattern.

### What Human LinkedIn Posts Sound Like

- Short, choppy sentences. Some fragments. Varying length.
- Contractions always (don't, isn't, we've, they're, couldn't)
- Starts mid-thought sometimes
- Imperfect structure — not every paragraph needs a topic sentence
- Specific details over general claims (names, numbers, dates, settings)
- First person, conversational, like talking to a friend
- Occasional lowercase where grammar says capitalize (reflects how people actually type)
- Line breaks between almost every sentence (LinkedIn formatting)
- No hashtags in the body (at most 2-3 at the very end, and only if the client insists)

> **Note:** For general anti-AI writing patterns across all channels, see the `copywriting` skill's references (`references/direct-response-copy.md`). The list above is LinkedIn-specific and more extensive.

---

## PHASE 4: Human Review (MANDATORY)

**Before any post is considered final, ALWAYS present it to the user for review.**

Show the user:
1. The draft post
2. Which SIREN elements are activated and where (with score)
3. The story bank entry it's based on
4. The pre-publish check results (3/5 minimum)
5. Unfindable Content Gate result
6. Suggested posting time (if relevant)

Ask specifically:
- "Does this sound like you? Would you actually say this?"
- "Is anything here inaccurate or exaggerated?"
- "Is there anything too personal that you'd rather not share?"
- "What would you change if you were typing this yourself?"

**Critical rule:** The client's voice takes priority over engagement optimization. If they say "I wouldn't say it this way," rewrite it their way, even if it's less "optimal." Authenticity > optimization, always.

---

## PHASE 5: Content Calendar (Optional)

When the user wants a content plan, build it using the story bank:

### Recommended Posting Cadence

- **3-4 posts per week** for aggressive growth
- **2 posts per week** for sustainable consistency
- **Mix**: 2 Tier 1-2 (story/vulnerability) : 1 Tier 3 (insight/tactical) per week

### Weekly Template

| Day | Post Type | SIREN Priority | Example |
|-----|-----------|---------------|---------|
| Mon | Vulnerability/Stakes story | S + E + I | "The hardest conversation I've had this year..." |
| Wed | Contrarian/Rebellion take | R + I + N | "Everyone says X but I've found..." |
| Fri | Relationship/Gratitude | E + I | "I met [person] 3 years ago and..." |

### Content Rotation Rules

- Never post 2 vulnerability stories back-to-back (audience fatigue)
- Every 4th-5th post can be tactical/educational (Tier 3)
- Space out stories about the same person/event by at least 2 weeks
- CTA/promotional posts max 1 per week, and always wrapped in a story

---

## PHASE 6: Performance Tracking

After posts go live, track what works:

### Metrics That Matter

| Metric | What It Tells You |
|--------|------------------|
| Likes | Broad resonance — did people agree/feel seen? |
| Comments | Depth of engagement — did it trigger a response? |
| Comment-to-like ratio | >30% = strong community activation. >60% = possible engagement pod inflation. |
| Shares/reposts | Value transfer — was it useful enough to pass on? |
| Profile views (post-publish) | Authority building — did they want to know more about you? |
| DMs received | Conversion — did it move someone to private action? |

### Performance Tiers

| Tier | Likes | Interpretation |
|------|-------|---------------|
| Breakout | 200+ | Vulnerability + stakes + timing aligned. Study WHY. Trigger Thought Leader Ads. |
| Strong | 100-200 | Core formula working. Note which SIREN elements were present. |
| Average | 50-100 | Functional but missing emotional depth or stakes. |
| Underperforming | <50 | Usually missing personal story, or framework-first, or third-person. |

### Feedback Loop

Save performance data in `clients/<project>/feedback/post-performance.md`:

```markdown
## [Date] — [Post title/topic]
- **Likes**: X | **Comments**: Y | **Shares**: Z
- **SIREN elements**: S, I, E (3/5)
- **SIREN score**: 7/10
- **Tier**: Strong
- **What worked**: Opening hook was emotional, specific detail about [moment]
- **What could improve**: CTA was too transactional, ending was weak
- **Lesson**: [Update story bank or framework based on learning]
```

---

## Quick Reference: The Engagement Formula

```
High Engagement = Personal Stakes + Identity Declaration + One Contrarian Belief
                  + Emotional First 2 Lines + Named Insight

Low Engagement  = Third-Person Story OR Framework-First OR Abstract Philosophy
                  OR No Personal Risk OR Transactional CTA
```

---

## File Organization

- `templates/client-profile-template.md` — Template for client identity, voice, values, background (from interview)
- `clients/<project>/story-bank.md` — All mined stories, tagged by SIREN, tiered, with status
- `clients/<project>/linkedin-profile.md` — Filled client profile (from template)
- `clients/<project>/feedback/post-performance.md` — Tracking metrics and learnings per post
- `references/siren_framework.md` — Deep reference on each SIREN element with examples

## Related Skills

- **linkedin-optimization**: Platform mechanics (profile, algorithm, SSI, B2B sales). Load first to understand HOW LinkedIn works, then use this skill for WHAT to write.
- **copywriting**: General copy principles. For storytelling frameworks (SIREN), use this skill's `references/siren_framework.md`.
- **content-strategy**: For broader content planning beyond LinkedIn.
- **brand-building**: For positioning and voice development.
