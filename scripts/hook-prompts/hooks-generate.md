# hooks-generate

**Activates:** `script-skill` (global, voice-locked).
**Output:** 20 hooks, medium-depth (hook text + reasoning + originality score + voice-fit score), distributed across funnel stages per the client's `funnel-goal.json`.
**Assumes:** the operator is sitting in a client folder OR has provided the `client` slug so the deterministic inputs can be resolved.

---

## DETERMINISTIC INPUTS (HARD-LOAD; FAIL IF MISSING)

The skill must load these BEFORE generating a single hook. If any required file is missing, halt and report which file is missing — do NOT proceed with defaults.

| # | Input | Path | Required? |
|---|---|---|---|
| 1 | Voice + tone | `clients/<client>/_config/voice-and-tone.md` | **Required** |
| 2 | Format patterns | `clients/<client>/_config/format-patterns.md` | **Required** |
| 3 | Constraints (forbidden words / anti-patterns) | `clients/<client>/_config/constraints.md` | **Required** |
| 4 | Buyer profile | `clients/<client>/_config/buyer-profile.md` | **Required** |
| 5 | ICP | `clients/<client>/_config/icp.md` | **Required** |
| 6 | Offer | `clients/<client>/_config/offer.md` | **Required** |
| 7 | Funnel-goal | `clients/<client>/_config/funnel-goal.json` | **Required** |
| 8 | Hook bank (past winners + decompositions) | `clients/<client>/06_learn/hook-bank.md` | Optional |
| 9 | Niche outlier pool (competitor hooks) | `voice/swipe-pools/<niche>/outlier-pool.jsonl` | Optional |
| 10 | Winning ad transcript (if mature client) | `clients/<client>/06_learn/winners/<id>.md` | Optional |

**Voice lock is non-negotiable.** If files 1-3 are missing, the skill cannot enforce the voice match and must refuse. No generic fallback.

---

## VARIABLE INPUT (the only thing the operator types)

```
{{concept}}
```

A 1-3 sentence description of the topic/angle this hook batch should explore.

Example: *"The hidden cost of writing too many 'value posts' on LinkedIn — most coaches lose authority by month 3 because they educate but never sell."*

---

## CONSTRAINTS

### Volume + distribution

- **Generate 20 hooks** in this batch.
- **Distribute by funnel-goal.json** `short_form_split`:
  - default 60 TOFU / 30 MOFU / 10 BOFU → 12 TOFU + 6 MOFU + 2 BOFU
  - Override only if `funnel-goal.json` says otherwise.
- **Pillar distribution** per `funnel-goal.json` `pillar_weights`:
  - default 40 Educate / 30 Sell / 20 Story / 10 Inspire → 8 Edu + 6 Sell + 4 Story + 2 Inspire
  - Pillars rotate within each funnel stage.

### The 4 Commandments (every hook must pass)

1. **Alignment** — spoken hook intent must align with what the visual + on-screen text would show. (Visual/text not in this output, but the hook must support them.)
2. **Speed to Value** — signal value within 3 seconds (≈ first 6 words). No setup before payoff.
3. **Clarity** — 6th grade reading level. Active voice. One concept per sentence. No jargon unless defined.
4. **Curiosity** — open a question the viewer MUST answer. Bigger gap = deeper hook. Never satisfy the curiosity inside the hook itself.

### The 4 Fatal Mistakes (every hook must avoid)

1. **Delay** — no preamble before the payoff. First 3 seconds carry the topic clarity.
2. **Confusion** — no ambiguous referents. The viewer cannot misunderstand.
3. **Irrelevance** — use "you/your" not "I/me". Exception: PERSONAL EXPERIENCE format (rule 8 below) which deliberately uses "I" as a vulnerability/proof signal.
4. **Weak Payoff** — the promised reveal must be worth waiting for. No "the secret to..." that turns out generic.

### Voice constraint (hard filter)

Run every hook through `constraints.md`:
- Reject hooks containing any forbidden word.
- Reject hooks matching any listed anti-pattern.
- Reject hooks that fail the "would they actually say this?" test against `voice-and-tone.md` + `format-patterns.md`.
- Rejected hooks: regenerate, don't ship.

---

## THE 9 FORMAT POOL

Each hook is assigned exactly ONE format. **No format may be used more than 3 times in the batch** (rotation enforced):

1. **SECRET REVEAL** — "Here's what nobody tells you about [thing]..."
2. **CASE STUDY** — "[Specific person] did [thing] and got [result]..."
3. **COMPARISON** — "[X] vs [Y] — here's the real difference..."
4. **QUESTION** — "Ever wondered why/how [thing]?"
5. **EDUCATION** — "The 3 things you need to know about [thing]..."
6. **LIST** — "[N] ways to [achieve outcome]..."
7. **CONTRARIAN** — "Everything you know about [thing] is wrong..."
8. **PERSONAL EXPERIENCE** — "I tried [thing] for [duration] and..." (only format that uses "I/me")
9. **PROBLEM** — "If you're struggling with [thing]..."

## THE 6 ARCHETYPES

Each hook is assigned exactly ONE archetype. **No archetype may be used more than 4 times** (rotation enforced):

- **Fortune Teller** — predicts an outcome
- **Experimenter** — shows test results / "I tried X and..."
- **Teacher** — educates on a framework or distinction
- **Magician** — before/after transformation
- **Investigator** — uncovers a hidden truth
- **Contrarian** — challenges a widely-held belief

---

## THE 3-STEP FORMULA (every hook must follow)

**Step 1 — Context Lean-in (≈1-2 seconds)**
*"If you [pain or desire from buyer-profile.md]..."*
→ Establishes relevance, makes the viewer think "this is for ME".

**Step 2 — Scroll-Stop Interjection (≈1 second)**
*"But..."* / *"Here's the truth..."* / *"Actually..."* / *"Wait —"*
→ Pattern interrupt, signals something unexpected.

**Step 3 — Contrarian Snapback (≈2-3 seconds)**
*[Shocking premise, counterintuitive reveal, or specific proof element]*
→ Delivers the curiosity gap. Creates the "wait, WHAT?" moment.

Total hook length: **1-3 sentences, ~6-15 words, ≤8 seconds of speaking time.**

---

## OUTPUT SCHEMA (use exactly — one block per hook)

```
Hook #N  [TOFU/MOFU/BOFU · PILLAR · FORMAT · ARCHETYPE]
"[Hook text — 1-3 sentences, voice-locked]"
Why it works: [1-2 line explanation of the psychological mechanism]
Originality: X/100  (X = how distinct vs hook-bank + niche outliers; 100 = nothing similar exists)
Voice fit: X/10    (X = how cleanly it passes constraints.md + matches voice-and-tone.md; 10 = sounds exactly like the operator/client)
```

Example output block:

```
Hook #7  [TOFU · Story · PERSONAL EXPERIENCE · Magician]
"I almost quit financial advising because of one client. What they said changed how I do this whole business."
Why it works: vulnerable open + curiosity gap on "one client" + transformation tease (Magician archetype) without revealing the lesson
Originality: 78/100  (no similar story-led financial-advisor hook in hook-bank; pattern adapted from Brendan Ang outlier)
Voice fit: 9/10      (uses Michelle's "raw" tone, no forbidden words, matches her sentence-length distribution)
```

---

## SELF-CHECK BEFORE EMITTING EACH HOOK

For every generated hook, verify silently:

- [ ] Passes all 4 Commandments
- [ ] Avoids all 4 Fatal Mistakes
- [ ] Uses "you/your" not "I/me" (unless PERSONAL EXPERIENCE format)
- [ ] No forbidden words from `constraints.md`
- [ ] Sounds like the voice files (would the client say this?)
- [ ] Originality > 60/100 (genuinely distinct from hook-bank entries)
- [ ] Funnel-stage tag matches the hook's *actual* job (don't claim TOFU on a sell-heavy hook)
- [ ] Word count ≤ 20 words

Hooks that fail self-check: regenerate. Don't ship them.

---

## OUTPUT ORDER

Emit hooks grouped by funnel stage:

```
==== TOFU hooks (12) — awareness / curiosity ====
Hook #1 ...
Hook #2 ...
...

==== MOFU hooks (6) — consideration / proof ====
Hook #13 ...
...

==== BOFU hooks (2) — decision / direct CTA ====
Hook #19 ...
Hook #20 ...

==== Batch summary ====
- Distinct formats used: [list]
- Distinct archetypes used: [list]
- Average originality: X/100
- Average voice fit: X/10
- Forbidden words triggered (and replaced): [list, or "none"]
- Suggested next: run hooks-select.md on this batch
```

---

## RUN

Generate 20 hooks for the concept above against the loaded deterministic inputs. Follow every rule. Self-check every hook. Emit in the exact output schema.
