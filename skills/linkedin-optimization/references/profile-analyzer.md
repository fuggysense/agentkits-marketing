# LinkedIn Profile Analyzer — Vision-Based Audit Tool

> **Trigger:** User uploads a LinkedIn profile screenshot or says "audit my LinkedIn profile"

## Instructions for Claude

When triggered, follow this exact protocol:

### Step 1: Request Screenshot

If user hasn't provided one:
> "Upload a screenshot of your LinkedIn profile (full page, desktop view preferred). I'll score it across 6 dimensions and give you the exact fixes to make."

### Step 2: Analyze & Score

Read the screenshot and score each dimension below. Be brutally honest — vague feedback wastes the user's time.

---

## Scoring System (0-60 points)

### Automatic Fail Conditions

These override all scoring — if ANY are true, total score = 0:

| Condition | Result |
|-----------|--------|
| No profile photo | **Score = 0** — "Fix this before anything else. Profiles without photos get 21x fewer views." |
| No headline (or default "Title at Company") | **Score = 0** — "Your headline is the most-read line on LinkedIn. Default = invisible." |
| Under 50 connections | **Score = 0** — "You need minimum 50 connections for the algorithm to distribute your content." |

If none of the automatic fails apply, score each section:

---

### 1. Photo (0 or 10 — pass/fail, no partial credit)

**ALL must pass for 10 points:**
- [ ] Face fills 60%+ of frame
- [ ] Solid or simple background (not busy/cluttered)
- [ ] Eye contact with camera
- [ ] Professional lighting (natural or studio, no harsh shadows)

**Score:** 10 if all pass, 0 if any fail.

**If 0:** Specify exactly which criterion failed and what to fix.

---

### 2. Headline (0 / 5 / 10)

| Score | Criteria |
|-------|----------|
| **10** | First 40 characters state a clear outcome or value proposition |
| **5** | States role/title but no value or outcome |
| **0** | Generic ("Experienced professional"), truncated, or default "Title at Company" |

**Evaluate:** Read only the first 40 characters (what shows in search/comments). Does it answer "What do you do for whom?"

---

### 3. Featured Section (0 / 5 / 10)

| Score | Criteria |
|-------|----------|
| **10** | 1-3 tiles, proper dimensions (1200×628px visible), each has a clear CTA |
| **5** | Has featured items but wrong dimensions, no CTA, or cluttered (4+) |
| **0** | Missing entirely or auto-populated with random activity |

---

### 4. About Section (0 / 5 / 10)

| Score | Criteria |
|-------|----------|
| **10** | Opens with metric/proof, includes CTA, formatted with line breaks |
| **5** | Has story/narrative but no proof points or CTA |
| **0** | Missing, under 3 lines, or starts with "I am a passionate/dedicated..." |

**Check first 2 lines carefully** — this is what shows before "See more."

---

### 5. Experience Section (0 / 5 / 10)

| Score | Criteria |
|-------|----------|
| **10** | Bullet points with numbers/results (e.g., "Grew revenue 3x", "Managed $2M budget") |
| **5** | Has descriptions but no metrics or measurable results |
| **0** | Title only, no description at all |

**Evaluate:** Look at at least the top 2 positions.

---

### 6. Connections (0 / 5 / 10)

| Score | Criteria |
|-------|----------|
| **10** | 200-499 connections (shows exact number = trust signal) |
| **5** | 500+ (shows "500+" which is fine but loses specificity) OR 100-199 |
| **0** | Under 100 (low credibility) OR 5,000+ showing "500+" (can't tell, but massive networks dilute relevance) |

**Note:** 200-499 scores highest because the exact number is visible, which signals authenticity.

---

## Decision Score Output

Present results in this exact format:

```
## LinkedIn Profile Score: [X]/60

### Instant Click Factors (do people click your profile?)
- Photo: [X]/10
- Headline: [X]/10
- Connections: [X]/10
- **Subtotal: [X]/30**

### Stay-and-Read Factors (do they stick around?)
- Featured: [X]/10
- About: [X]/10
- Experience: [X]/10
- **Subtotal: [X]/30**

### The 3-Second Test: [PASS/FAIL]
> When someone sees your profile in search results or a comment thread,
> they see your photo, headline, and connection count.
> Need 15+ on Instant Click to pass.

### The 30-Second Test: [PASS/FAIL]
> When someone lands on your profile, they scan Featured, About, and Experience.
> Need 15+ on Stay-and-Read to pass.
```

---

## Fixes Section

For each section that scored below 10, provide **ONE specific fix**:

**Format per section:**
```
### Fix: [Section Name] ([current score] → [expected score after fix])

**The problem:** [1 sentence describing exactly what's wrong]

**The fix:** [Exact, actionable recommendation — not vague. Include specific wording if applicable.]

**Expected impact:** [Estimated % improvement in relevant metric]
```

**Examples of GOOD fixes:**
- "Change your headline from 'Marketing Manager at Acme Corp' to 'Helping B2B SaaS companies 3x their pipeline through content | Ex-Acme'. This puts the outcome first and adds credibility."
- "Your About section starts with 'I am a dedicated marketing professional.' Replace the first line with your best metric: 'Built a content engine that drove $2M in pipeline in 12 months.' Numbers stop the scroll."

**Examples of BAD fixes (do not do this):**
- "Improve your headline" (too vague)
- "Add more detail to your experience" (not actionable)
- "Consider updating your photo" (no specific guidance)

---

## Closing

End every profile audit with:

> **The one LinkedIn algorithm secret nobody talks about but changes everything:**
>
> Your profile is not a resume. It's a landing page. Every section either converts a visitor into a follower, a connection, or a lead — or it doesn't. Score yourself honestly every 90 days and fix the weakest link first.
