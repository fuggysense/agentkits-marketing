---
description: Generate 20 voice-locked hooks for a concept (medium-depth output, funnel-stage tagged). Wraps script-skill.
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: <one-sentence concept> [--client <client-slug>]
---

# /hooks:generate

**Underlying skill: `script-skill`** (global, voice-locked). This command locks the skill into a specific workflow: voice-first, funnel-aware, medium-depth output, with self-checks.

---

## Step 1 — Resolve the client

If `--client <slug>` is provided, use that. Otherwise infer from cwd (`clients/<slug>/...`). If neither resolves, halt and ask.

## Step 2 — Load deterministic inputs (HARD-FAIL if required files missing)

Load these from `clients/<client>/`. If any **Required** file is missing, halt and report which one — do NOT proceed with defaults.

| # | Input | Path | Status |
|---|---|---|---|
| 1 | Brand voice (tone + patterns + constraints) | `brand-voice.md` | **Required** |
| 2 | Buyer profile | `buyer-profile.md` | **Required** |
| 3 | ICP | `icp.md` | **Required** |
| 4 | Offer | `offer.md` | **Required** |
| 5 | Channels + funnel structure | `channels.json` | **Required** |
| 6 | Funnel-goal override (v0.5.2 plan format) | `funnel-goal.json` or `_config/funnel-goal.json` | Optional — overrides 5 |
| 7 | Past winners + hook-bank | `learnings.md` | Optional |
| 8 | Story / proof bank | `story-bank.md` | Optional |
| 9 | Niche outlier pool | `voice/swipe-pools/<niche>/outlier-pool.jsonl` | Optional |
| 10 | Winning ad transcript (if mature client) | `learnings.md` → "winners" section | Optional |

**Voice lock is non-negotiable.** If `brand-voice.md` is missing or empty, refuse to run. No generic fallback.

## Step 3 — Resolve funnel split + pillar split

Read funnel structure from (in priority order):
1. `funnel-goal.json` → `short_form_split` + `pillar_weights`
2. `channels.json` → channels with `funnel_stage` and `pillar` weights
3. **Default** if neither has the data: 60 TOFU / 30 MOFU / 10 BOFU + 40 Educate / 30 Sell / 20 Story / 10 Inspire

Compute the distribution for 20 hooks:
- Default split → 12 TOFU + 6 MOFU + 2 BOFU
- Pillars rotate within each funnel stage

## Step 4 — Variable input (the only thing the operator types)

```
{{concept}}
```

A 1-3 sentence description of the topic/angle this hook batch should explore. Example:

> *"The hidden cost of writing too many 'value posts' on LinkedIn — most coaches lose authority by month 3 because they educate but never sell."*

## Step 5 — Apply constraints

### The 4 Commandments (every hook must pass)

1. **Alignment** — spoken hook intent must align with the visual + on-screen text it implies (we focus on spoken here; visual/text generation is downstream).
2. **Speed to Value** — signal value within 3 seconds (≈ first 6 words). No setup before payoff.
3. **Clarity** — 6th grade reading level. Active voice. One concept per sentence. No jargon unless defined.
4. **Curiosity** — open a question the viewer MUST answer. Never satisfy the curiosity inside the hook itself.

### The 4 Fatal Mistakes (every hook must avoid)

1. **Delay** — no preamble before the payoff.
2. **Confusion** — no ambiguous referents.
3. **Irrelevance** — use "you/your" not "I/me". Exception: PERSONAL EXPERIENCE format (#8 below).
4. **Weak Payoff** — the promised reveal must be worth waiting for.

### Voice constraint (hard filter)

Run every hook through `brand-voice.md`:
- Reject hooks containing any forbidden word.
- Reject hooks matching any listed anti-pattern.
- Reject hooks that fail the "would the client actually say this?" test against the voice doc's tone + patterns sections.
- Rejected hooks: regenerate, don't ship.

## Step 6 — Format + archetype rotation

### The 9 Formats (each hook assigned exactly one; no format used > 3× per batch)

1. **SECRET REVEAL** — "Here's what nobody tells you about [thing]..."
2. **CASE STUDY** — "[Specific person] did [thing] and got [result]..."
3. **COMPARISON** — "[X] vs [Y] — here's the real difference..."
4. **QUESTION** — "Ever wondered why/how [thing]?"
5. **EDUCATION** — "The 3 things you need to know about [thing]..."
6. **LIST** — "[N] ways to [outcome]..."
7. **CONTRARIAN** — "Everything you know about [thing] is wrong..."
8. **PERSONAL EXPERIENCE** — "I tried [thing] for [duration] and..." (only format that uses "I/me")
9. **PROBLEM** — "If you're struggling with [thing]..."

### The 6 Archetypes (each hook assigned exactly one; no archetype used > 4× per batch)

- **Fortune Teller** — predicts an outcome
- **Experimenter** — shows test results
- **Teacher** — educates on a framework or distinction
- **Magician** — before/after transformation
- **Investigator** — uncovers a hidden truth
- **Contrarian** — challenges a widely-held belief

## Step 7 — The 3-Step Formula (every hook follows this shape)

**Step A — Context Lean-in (≈1-2 sec)**
*"If you [pain or desire from buyer-profile.md]..."*
→ Establishes relevance.

**Step B — Scroll-Stop Interjection (≈1 sec)**
*"But..."* / *"Here's the truth..."* / *"Actually..."* / *"Wait —"*
→ Pattern interrupt.

**Step C — Contrarian Snapback (≈2-3 sec)**
*[Shocking premise, counterintuitive reveal, or specific proof element]*
→ Delivers the curiosity gap.

Total hook length: **1-3 sentences, ~6-15 words, ≤8 seconds of speaking time.**

## Step 8 — Self-check before emitting each hook

For every generated hook, verify silently:

- [ ] Passes all 4 Commandments
- [ ] Avoids all 4 Fatal Mistakes
- [ ] Uses "you/your" not "I/me" (unless PERSONAL EXPERIENCE format)
- [ ] No forbidden words from `brand-voice.md`
- [ ] Sounds like the voice doc (would the client say this?)
- [ ] Originality > 60/100 (distinct from `learnings.md` hook-bank entries)
- [ ] Funnel-stage tag matches the hook's *actual* job
- [ ] Word count ≤ 20 words

Hooks that fail self-check: regenerate. Don't ship them.

## Step 9 — Output schema (use exactly)

Per hook, one block:

```
Hook #N  [TOFU/MOFU/BOFU · PILLAR · FORMAT · ARCHETYPE]
"[Hook text — 1-3 sentences, voice-locked]"
Why it works: [1-2 line explanation of the psychological mechanism]
Originality: X/100  (X = distinct vs learnings.md hook-bank + niche outliers)
Voice fit: X/10    (X = passes brand-voice.md filter + matches tone)
```

Example:

```
Hook #7  [TOFU · Story · PERSONAL EXPERIENCE · Magician]
"I almost quit financial advising because of one client. What they said changed how I do this whole business."
Why it works: vulnerable open + curiosity gap on "one client" + transformation tease (Magician archetype)
Originality: 78/100  (no similar story-led financial-advisor hook in hook-bank)
Voice fit: 9/10      (matches client's "raw" tone, no forbidden words)
```

## Step 10 — Output order

```
==== TOFU hooks (12) ====
Hook #1 ...
...

==== MOFU hooks (6) ====
Hook #13 ...
...

==== BOFU hooks (2) ====
Hook #19 ...
Hook #20 ...

==== Batch summary ====
- Distinct formats used: [list]
- Distinct archetypes used: [list]
- Average originality: X/100
- Average voice fit: X/10
- Forbidden words triggered (and replaced): [list, or "none"]
- Next: run /hooks:select against this batch
```

## Step 11 — Persist

Write the batch to `clients/<client>/02_script/output/<YYYY-WW>-hooks-generate.md` (matching the v0.5.2 plan's stage 02 folder structure). If that folder doesn't exist yet, create it.

Also append a one-liner to `clients/<client>/learnings.md` under a `## Hook generations` section:
```
- YYYY-MM-DD · concept: <first 60 chars> · 20 hooks · avg originality X/100 · avg voice-fit X/10
```

## RUN

Generate 20 hooks for the concept above against the loaded deterministic inputs. Follow every rule. Self-check every hook. Emit in the exact output schema. Persist the output.
