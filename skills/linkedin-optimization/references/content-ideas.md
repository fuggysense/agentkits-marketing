## Graph Links
- **Parent skill:** [[linkedin-optimization]]
- **Sibling references:** [[banner-designer]], [[linkedin-algorithm]], [[profile-analyzer]]
- **Related skills:** [[linkedin-content]], [[content-moat]]

# LinkedIn Content Idea Generator — 4-Prompt System

> **Trigger:** User says "LinkedIn content ideas" or "generate LinkedIn hooks"

## Instructions for Claude

Run these 4 prompts in sequence. Each builds on the previous. Present output after each prompt and confirm before moving to the next.

---

## Prompt 1 — Content Themes

### Input Needed
Ask the user:
> Tell me about your business in 2-3 sentences: What do you do, who do you serve, and what result do you help them achieve?

### Process
Generate **5 content themes/pillars** based on the user's business. Each theme should:
- Be broad enough for 20+ posts
- Be specific enough to establish expertise
- Map to a stage of the buyer's journey

### Output Format

```
## Your 5 LinkedIn Content Themes

### Theme 1: [Theme Name]
What it covers: [1 sentence]
Example topics: [3 bullet points]
Buyer journey stage: [Awareness / Consideration / Decision]

### Theme 2: [Theme Name]
...

### Theme 3: [Theme Name]
...

### Theme 4: [Theme Name]
...

### Theme 5: [Theme Name]
...
```

**Confirm with user** before proceeding to Prompt 2.

---

## Prompt 2 — Expert Content Hooks

### Process
For each of the 5 themes, generate **5 winning hooks** for educational/expert content.

### Rules
- **Short and concise: 8-10 words max per hook**
- No emojis
- Each hook must promise a specific outcome or insight
- Include a **rehook** (curiosity loop at end that makes them want to read more)
- Hook should work in the first 2 lines of a LinkedIn post (before "See more")

### Output Format

```
## Expert Content Hooks

### Theme 1: [Theme Name]

1. Hook: [8-10 word hook]
   Rehook: [curiosity loop / cliffhanger sentence]

2. Hook: [8-10 word hook]
   Rehook: [curiosity loop / cliffhanger sentence]

3. Hook: [8-10 word hook]
   Rehook: [curiosity loop / cliffhanger sentence]

4. Hook: [8-10 word hook]
   Rehook: [curiosity loop / cliffhanger sentence]

5. Hook: [8-10 word hook]
   Rehook: [curiosity loop / cliffhanger sentence]

### Theme 2: [Theme Name]
...
```

**Total:** 25 expert hooks (5 per theme)

---

## Prompt 3 — Storytelling Content Hooks

### Process
For each of the 5 themes, generate **5 winning hooks** for storytelling content that ties back to the theme's lesson.

### Rules
- **Short and concise: 8-10 words max per hook**
- No emojis
- Stories must feel personal, specific, and real (not generic "I once knew a guy...")
- Include a **rehook** (what makes them keep reading after the story setup)
- Stories should lead to a takeaway connected to the theme

### Output Format

```
## Storytelling Hooks

### Theme 1: [Theme Name]

1. Hook: [8-10 word hook]
   Rehook: [curiosity loop / what happened next]

2. Hook: [8-10 word hook]
   Rehook: [curiosity loop / what happened next]

3. Hook: [8-10 word hook]
   Rehook: [curiosity loop / what happened next]

4. Hook: [8-10 word hook]
   Rehook: [curiosity loop / what happened next]

5. Hook: [8-10 word hook]
   Rehook: [curiosity loop / what happened next]

### Theme 2: [Theme Name]
...
```

**Total:** 25 storytelling hooks (5 per theme)

---

## Prompt 4 — Broad / Narrow / Niche Variations

### Process
For each of the 5 themes, generate hooks at **3 audience levels**.

### Definitions

| Level | Audience | Hook Style |
|-------|----------|------------|
| **Broad** | Anyone on LinkedIn | Easy-to-understand hook, universal appeal, big emotion or surprise |
| **Narrow** | Someone aware of the problem/product category | Hook assumes context, references the problem directly |
| **Niche** | Specific practitioner in the field | Punchy, insider language, targets a very specific subtopic |

### Rules
- 1 hook + 1 rehook per level per theme
- **8-10 words max per hook**
- No emojis
- Broad hooks should be shareable by anyone
- Niche hooks should make the target audience feel "this is for me"

### Output Format

```
## Broad / Narrow / Niche Hooks

### Theme 1: [Theme Name]

**Broad:**
Hook: [8-10 words — universal appeal]
Rehook: [curiosity loop]

**Narrow:**
Hook: [8-10 words — problem-aware audience]
Rehook: [curiosity loop]

**Niche:**
Hook: [8-10 words — insider/specific]
Rehook: [curiosity loop]

### Theme 2: [Theme Name]
...
```

**Total:** 15 hooks (3 per theme × 5 themes)

---

## Summary

After all 4 prompts, present:

```
## Content Idea Bank Summary

- 5 content themes
- 25 expert hooks (Prompt 2)
- 25 storytelling hooks (Prompt 3)
- 15 broad/narrow/niche hooks (Prompt 4)
- **Total: 65 LinkedIn content ideas**

Recommended posting cadence: 5x/week = ~13 weeks of content
```

---

## Tips for the User

- **Mix formats:** Use expert hooks for carousels, storytelling for text posts, broad hooks for polls
- **Repurpose:** Every hook can become a text post, carousel, video script, or newsletter topic
- **Test:** Post the broad hooks first to see which themes resonate, then go narrow/niche
- **Refresh:** Run this system quarterly with updated business context
