---
description: OPTIONAL deep-dive on one hook — diagnose 4 fatal mistakes, generate 7 rewrite variations. Wraps script-skill.
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: <hook-text or hook-id> [--client <client-slug>]
---

# /hooks:analyze

**Underlying skill: `script-skill`**. **Optional** step — use ONLY when:

- A selected hook from `/hooks:select` feels close but not quite landing
- You want before/after rewrites of one hook for testing
- You're diagnosing why a shipped hook underperformed
- Routine generate → select feels predictable and you want a 7-direction stretch

**Skip this command for normal flow.** Don't auto-run it after `/hooks:select` — only invoke when something tells you to.

---

## Step 1 — Resolve input

| Input | Source | Required? |
|---|---|---|
| The hook to analyze | First positional arg: either raw text OR a hook ID like `#7` from a generate batch | **Required** |
| Client context (voice, buyer, offer) | `clients/<client>/brand-voice.md` + `buyer-profile.md` + `icp.md` + `offer.md` | **Required** |
| Past performance data (if shipped) | `clients/<client>/learnings.md` analytics section | Optional |
| Visual + text overlay (if known) | Operator pastes during run | Optional |

## Step 2 — Diagnose against the 4 Fatal Mistakes

For each fatal mistake, score the hook 0-10 (10 = fully avoids the mistake; 0 = completely guilty):

### 1. Delay
- **Time to topic clarity**: how many seconds until a 6th grader knows what the video is about?
- 0-3 sec = good · 4-7 sec = warning · 8+ sec = fatal
- **Quote the exact words** that delay (if any).

### 2. Confusion
- Can the hook be misunderstood?
- Are referents ambiguous? Is there comprehension loss?
- **Identify the specific word/phrase** that creates confusion.

### 3. Irrelevance
- Counts of "I/me" vs "you/your"
- Does the audience hear "this is FOR ME" by second 3?
- Exception: PERSONAL EXPERIENCE format uses "I" deliberately as a proof signal

### 4. Weak Payoff
- Is the promised reveal actually valuable enough?
- Or is it a generic "the secret to..." that turns out unremarkable?
- Test: would a buyer-profile reader genuinely want to know the answer?

## Step 3 — Diagnose against the 4 Commandments

Same 1-10 scoring:

1. **Alignment** — does the spoken hook imply a clear, consistent visual + text overlay?
2. **Speed to Value** — value signal by ≤3 seconds?
3. **Clarity** — 6th grade reading level? Active voice?
4. **Curiosity** — gap size A→B; is the gap large?

## Step 4 — Identify what's working + what's broken

Output 2-4 strengths + 2-5 critical flaws:

```
### Strengths
1. [Element] — works because [psychological principle]. Evidence: "[quote]"
2. [...]

### Critical flaws
1. [Problem] — fails because [why]. Bounce moment: [exact second]. Fix direction: [what to change]
2. [...]
```

## Step 5 — Generate 7 rewrite variations

Each variation REWRITES the hook fully (not describes changes). Each targets a different psychological lever:

### Variation A: Maximum Clarity (Delay Elimination)
Strip all fluff. Front-load the "what". Topic clarity in first 3 seconds.

```
[REWRITTEN HOOK — 1-3 sentences]
```

**Psychological shift:** [what changed and why]
**Best for:** [audience / platform]

---

### Variation B: Pain Amplification (Twist the Knife)
Surface the pain immediately. Visceral language. Make them FEEL the frustration.

```
[REWRITTEN HOOK]
```

**Psychological shift:** [...]
**Best for:** [...]

---

### Variation C: Curiosity Gap Maximization
Largest possible before→after gap. Tease the transformation without revealing the how.

```
[REWRITTEN HOOK]
```

**Psychological shift:** [...]
**Best for:** [...]

---

### Variation D: You-Centric Relevance Boost
Replace all "I/me" with "you/your". Audience-of-one technique. Pronoun audit pass.

```
[REWRITTEN HOOK]
```

**Psychological shift:** [...]
**Best for:** [...]

---

### Variation E: Proof-Seeded Trust Building
Immediate credibility — stat, screenshot, authority. Proof in first 5 seconds.

```
[REWRITTEN HOOK]
```

**Psychological shift:** [...]
**Best for:** [...]

---

### Variation F: Controversy / Strong Stance
Take a position that sparks debate. Impossible not to have an opinion.

```
[REWRITTEN HOOK]
```

**Psychological shift:** [...]
**Best for:** [...]

---

### Variation G: Pattern Interrupt (Unexpected Format)
Question format, challenge, direct address. Break the typical hook shape entirely.

```
[REWRITTEN HOOK]
```

**Psychological shift:** [...]
**Best for:** [...]

## Step 6 — Final recommendation

```
Should you use the original?  [Yes — as is / Yes — with tweaks / No — use Variation X / No — abandon]

Champion variation: [A-G]

Reasoning: [2-3 sentences on why this variation wins for THIS buyer profile]

Execution notes (if champion is filmed):
- Opening visual: [description]
- On-screen text: [exact text]
- Delivery tone: [direction]
- Pacing: [fast / measured / dramatic]
- First 3 seconds must include: [critical element]

Split test plan:
- Primary version: [original or champion]
- Test version: [different variation letter]
- Hypothesis: [what we're testing]
- Success metric: [hook rate / dwell / saves / etc.]
```

## Step 7 — Voice-check the 7 variations

For each variation, run the SAME voice constraint check as `/hooks:generate`:
- Does it pass `brand-voice.md` filter?
- Voice fit ≥ 8/10?
- Any forbidden words?

Drop or rewrite any variation that fails. The user should never see a voice-fit-failing rewrite as a recommendation.

## Step 8 — Persist

Append to `clients/<client>/02_script/output/<YYYY-WW>-hooks-analyze.md`:
- Original hook
- 4 Fatal Mistake scores + 4 Commandment scores
- All 7 variations
- Champion + reasoning

Also append to `clients/<client>/learnings.md` under `## Hook analyses`:
```
- YYYY-MM-DD · analyzed Hook #X · champion = Variation [Y] · key flaw fixed: [delay / confusion / irrelevance / weak payoff]
```

## Brutal honesty note

Analyzer's job is surgical truth-telling. Never sugarcoat. The creator needs to know WHERE viewers bounce and WHY. If the original hook is structurally broken, say so. If a variation is just the original with synonyms, mark it as such.

## RUN

Analyze the hook above. Diagnose against 4 fatal mistakes + 4 commandments. Surface strengths + flaws. Generate 7 voice-checked rewrite variations. Pick a champion. Output split-test plan. Persist.
