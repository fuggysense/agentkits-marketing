---
name: headline-bank
version: "2.2.0"
brand: AgentKits Marketing by AityTech
preferred_invocation: /copy:headline  # wraps this skill with mandatory 5-mechanism diversity (cai #39) + copywriting-OS gates (see .claude/references/copywriting-os/)
category: content
difficulty: intermediate
description: "Curiosity-led Meta ad copy generator. Per angle: a ~150w PRIMARY on the six-emotional-states sequence (hook -> pain -> agitate -> hope -> loop CTA) + a ~50w compression, with 3-5w headlines. Funnel-aware, brand-conditional emoji. Feeds DCT COPY tab 1:1. Triggers: meta copy, meta headline, halbert copy, ad primary text, ad body copy, headline bank, facebook ad copy."
triggers:
  - meta copy
  - meta headline
  - halbert copy
  - short headline
  - ad primary text
  - ad body copy
  - headline bank
  - direct response ad copy
  - facebook ad copy
prerequisites:
  - copywriting
  - big-angle-spotter
related_skills:
  - big-angle-spotter
  - ad-concept-engine
  - copywriting
  - avatar-research
  - source-of-truth
  - copy-editing
  - unslop
agents:
  - copywriter
  - brand-voice-guardian
success_metrics:
  - headline_ctr
  - primary_text_engagement
  - scroll_stop_rate
output_schema: meta-copy-bank
---

# Meta Ad Copy Bank (Halbert-style)

> Per angle, produces a ~150-word PRIMARY copy (the lock) built on a defined curiosity-led structure, plus a ~50-word compression of it, each paired with ONE short Meta headline (3-5 words). 1:1 match with the COPY tab schema: `HEADLINE 1`, `HEADLINE 2`, `COPY 1`, `COPY 2`. See **Body Copy Structure** below — primary text is built on a sequence, not freestyled.

## Graph Links

- Feeds into: `[[ad-concept-engine]]` (Phase 3 — Meta primary text + headline fields on the COPY tab)
- Runs after: `[[big-angle-spotter]]` (Step 11 ad prompts provide the angle spine + text-overlay spec)
- Draws from: `[[source-of-truth]]`, `[[avatar-research]]`, `[[copywriting]]`, `[[brand-building]]`
- Related: `[[copy-editing]]`, `[[unslop]]`, `[[marketing-psychology]]`

## When to Use This Skill

- After big-angle-spotter produces a locked angle + top-3 image/overlay creatives
- Need Meta primary text (body copy above the image) + Meta headline field (short clickable text below image)
- Per DCT: run once to get 2 headlines + 2 copies — Meta DCT rotates all 4 text combinations against the 3 image creatives = 12 combinations tested
- Command: `/ads:headlines` (or invoked as the copy step inside ad-concept-engine Conductor Mode — intent-routed, see routing-overrides.md)

## What This Skill Does NOT Produce

- **Text overlays on the image** — those are big-angle-spotter step 11's job (long-form mechanism hooks, baked into the image in Canva)
- **Image prompts** — big-angle-spotter step 12's job
- **Angles** — big-angle-spotter steps 1-7's job (or locked upstream)

## Operating Modes

**Mode A — Single-angle run (default)**
- Generate 2 copies + 2 headlines for ONE locked angle
- Used inline after big-angle-spotter for a DCT

**Mode B — Multi-angle batch**
- Given N locked angles (e.g. 3 DCTs in a wave), generate per-angle outputs in one call
- Each angle stays independent — no cross-pollination (unlike big-angle-spotter's EXISTING_ANGLES logic)

## Inputs (checklist — MUST all be present before running)

| Input | Example | Source |
|-------|---------|--------|
| Brand/Client name | "NeezaNizam (Propnex Realty SG)" | `context-profile.json` brand.brand_name |
| Angle | "Why Most Late-Life Divorces Leave Both Parties Priced Out" | `04_ranked_angles.md` (from big-angle-spotter) or `angles/iteration-log.md` |
| Market Awareness | "Problem-Aware → Solution-Aware" | `_brand/buyer-profile.md` Micro-Persona Map |
| Market Sophistication | "L3 (drowning, not cynical)" | `_brand/buyer-profile.md` Micro-Persona Map |
| Persona | selected micro-persona row + supporting buyer-language notes, or ~200 word summary | `clients/<slug>/_brand/buyer-profile.md` |
| Landing page URL | https://swopyourhome.com | `context-profile.json` brand.social_links.website OR offer.entry_offer landing URL |
| Angle spine (cause-effect) | From big-angle-spotter `07_expansion.md` §1 | DCT folder |

If any are missing, halt and request them. No improvisation on inputs.

## Research-completeness precondition (rebuild M2.1)
Before generating for any client, run: python3 scripts/research_gate.py --client clients/<slug>
PASS is required. On FAIL: stop and surface the scorecard to the operator — never generate from thin research. Override only via an operator-recorded research_gate_override (with reason) in the campaign's pipeline-state.json.

---

## Body Copy Structure (the format — not "Halbert vibes")

Primary text is BUILT on a structure, not freestyled to a word count. The structure is the front of the Skeptic→Buyer sequence in `.claude/references/copywriting-os/frameworks/six-emotional-states.md` (Pain → Problem → Hope → Belief → Desire → Urgency), where **curiosity is the fuel between states**. A Meta ad runs the FRONT of that sequence and hands off — it never tries to close.

**Beat order (the ~150w primary):**
1. **Curiosity hook** (line 1) — open a loop or name a hidden thing without resolving it. Scroll-stop. No warm-up, no "are you tired of".
2. **Pain** — mirror the reader's lived experience in their own words (verbatim avatar voice).
3. **Problem / agitate** — name the specific cost or mechanism behind the pain. Concrete: a number, a named consequence, not a vague worry.
4. **Hope (the turn)** — one line that the cost is reversible, or that someone found the answer. A flash, not the full solution.
5. **Loop-opener CTA** — hand the click to the next step. Do NOT resolve the loop in the ad.

**Funnel-aware rule (decides where the copy STOPS):**
- **Ad → sales letter / long-form page:** the ad runs states 0–3 only (Curiosity → Pain → Problem → a flash of Hope) and STOPS. The letter finishes Belief → Desire → Urgency. CTA is a read-cue ("read how", "see the number"), never a transactional verb. Carry the page's exact claims so the scent matches and the click doesn't bounce.
- **Ad → lead form / DM:** may add one belief + one proof + a transactional CTA, but still opens on curiosity, not the offer.

**Length:** the **~150w piece is the PRIMARY lock.** Generate a ~50w compression as a secondary variant (same beats, fewer words) for brevity-first placements. In 10-5-5 mode the ~150w piece is the single locked copy per angle.

**Emoji:** brand-conditional, OFF by default. Only include emoji if the client's `brand-voice.md` permits them. Many brands (e.g. senior/advisory registers) ban them outright — then the CTA is plain text, no arrow glyph.

## Insight tags (every hook and headline carries one — non-negotiable)

A hook has two jobs: scroll-stop AND speak to the avatar's real situation in their own words (Ferres `03-angles-hooks-copy.md` §Hook rules #4 — build hooks from the prospect's problems, circumstances, outcomes; §Copy rules #3 — exact customer language everywhere). The second job is the one that decays silently when copy is freestyled from model memory. So we make it checkable.

**Every hook and every headline you generate MUST carry an insight tag.** The format is exact:

```
insight: <research-file>#<line-or-anchor> — <≤8-word paraphrase>
```

- `<research-file>` — a path that exists on disk (e.g. `clients/<slug>/00_inputs/research/voc-reddit-dump.md` or `_brand/buyer-profile.md`).
- `#<line-or-anchor>` — either `#L<n>` (1-based line) or `#<markdown-heading>` text (e.g. `#THE CORE PROBLEM`).
- `— <paraphrase>` — eight words or fewer, what the line tells you.

**An untagged hook or headline is invalid output.** It is not a stylistic nicety — it is the gate the `hook_gate.py` script (below) enforces. A tag that points at a missing file or a non-existent line/anchor fails the build too.

**Worked example** (smoke-test client `_smoketest`, against its real research pack):

| Hook / headline | Insight tag |
|---|---|
| "We overpaid 40-50k on our first flat. Not doing it twice." | `insight: clients/_smoketest/00_inputs/research/voc-reddit-dump-260611.md#L30 — upgrader overpaid 40-50k, won't repeat` |
| "28 saved listings. Zero decisions. Sound familiar?" | `insight: clients/_smoketest/00_inputs/research/voc-reddit-dump-260611.md#L38 — first-timer, 28 saved, zero decisions` |
| Headline: "The fee that saves 50k" | `insight: clients/_smoketest/_brand/buyer-profile.md#THE CORE PROBLEM — advice never feels on their side` |

Each tag points at a line a reviewer can open and read. The hook is only as good as the research line under it.

## VOC injection slots (fixed-slot discipline, per Ferres)

Ferres treats voice-of-customer not as flavour but as fixed structural slots — the agitation beat runs on verbatim mined phrases, and the top objection is answered in-line with proof (`03-angles-hooks-copy.md` §Copy rules #3, #6, #5 proof hierarchy). Two slots are mandatory in the ~150w PRIMARY:

1. **Problem/agitate beat = EXACT customer language.** Do not paraphrase the pain into marketer-speak. Pull a verbatim phrase from the VOC dump (or buyer-profile `Language` rows) and use the buyer's own words. Carry a source pointer for the phrase you lifted: `voc: <research-file>#<line> — "<the lifted phrase>"`. If comments say "scam," the copy opens near "scam" — not "you may have concerns about legitimacy." (Ferres: *if comments say "scam," open with "you probably think this is a bullshit scam…"*).
2. **Top objection, answered in-line with proof.** Identify the single biggest objection for this avatar from research (the buyer-profile `Beliefs to overcome` / `Messages rejected` rows are the source). Answer it inside the body with one concrete proof, not a separate FAQ. Max ~3 objections per ad; lead with the one research ranks highest. The proof must follow the proof hierarchy (demonstration > stat > testimonial) and clear the Claim Gate before it ships.

Both slots feed the insight-tag requirement above — the verbatim phrase and the objection each name the research line they came from.

## THE CORE PROMPT (curiosity-led, structured)

This is the single source of truth for generating Meta ad copy. Fill in all CAPS placeholders before sending to a copywriter agent or Sonnet worker.

```
You're the world's best marketer. Renowned for your short form, direct response copywriting skills.

You are Eugene Schwartz. You are an expert in market awareness, market sophistication, desire, personas, mechanisms etc.

The first line of BOTH copies NEEDS to be ultra scroll stopping. Needs to grab eyes like your life depends on it.

Your Client / Brand Name is: <BRAND>

Angle: <ANGLE — one sentence cause-effect claim>

Market Awareness: <MARKET AWARENESS STAGE>

Market Sophistication: <MARKET SOPHISTICATION LEVEL>

Persona: <PERSONA — full avatar doc or ~200-word summary covering demographics, emotional state, primary fear, buying trigger, tonal contract rules>

Their landing page says: <LDP URL>

Funnel target (where this ad sends the click): <FUNNEL TARGET — "sales letter / long-form page" OR "lead form / DM". This decides where the copy STOPS — see Body Copy Structure above.>

Brand emoji rule: <"EMOJI OK (sparingly)" OR "NO EMOJI" — read from the client's brand-voice.md. Default NO EMOJI.>

Write the body on the curiosity-led structure (Curiosity hook → Pain → Problem/agitate → Hope → loop-opener CTA). Do not freestyle. Each beat earns the next line.

- If FUNNEL TARGET is a sales letter / long-form page: run Curiosity → Pain → Problem → a flash of Hope, then STOP and hand off. The page closes the sale, not the ad. CTA is a read-cue ("see the number on your flat", "read how"), never "Sign Up / Book / Submit". Carry the page's exact claims (numbers, mechanism, named case) so the scent matches.
- Mirror the reader's pain in THEIR words — pull verbatim avatar voice, do not paraphrase into marketer-speak. The problem/agitate beat MUST use an exact phrase lifted from the research (VOC dump or buyer-profile Language rows) — quote it, do not summarise it. Record the source as `voc: <research-file>#<line> — "<lifted phrase>"`.
- Answer the avatar's single biggest objection IN-LINE with one concrete proof (from the buyer-profile "Beliefs to overcome" / "Messages rejected" rows). Not a separate FAQ. The proof must clear the Claim Gate before it ships.
- Agitate with one concrete cost (a figure, a named consequence), not a vague worry.
- Every hook AND every headline you write MUST carry an insight tag: `insight: <research-file>#<line-or-anchor> — <≤8-word paraphrase>`. The file must exist and the line/anchor must resolve. Untagged hooks/headlines are invalid output — they fail the hook gate (see "Hook gate" below).

Take brand messaging and tone into account. Use plain verbs. Lay it out for the eye: short lines, one idea per line, white space between beats, each line pulling the next.

Do NOT use: life changer, breakthrough, game changer, unlock, dream home, game-changer. No corny influencer cadence. No manufactured urgency unless it is the reader's own real deadline.

CTA format: if NO EMOJI — `<read-cue text>` then the URL on its own. If EMOJI OK — `<read-cue text>` then the URL (one arrow glyph max, only if brand permits). Remove any "<>" from the final output.

Give me 2 versions of the SAME structured piece:
  - Copy A: PRIMARY (~150 words) — the full curiosity-led sequence, all five beats.
  - Copy B: COMPRESSION (~50 words) — same beats, same hook, fewer words, for brevity-first placements.

Copy A is the lock. Copy B is the short variant of A — same concept, not a different angle.

With the copy, give me 1 headline per version (3-5 words max each).

Output format (exact):

## COPY A — PRIMARY (~150 words)
**HEADLINE 1:** <3-5 word headline>
insight (headline 1): <research-file>#<line-or-anchor> — <≤8-word paraphrase>

<body copy: curiosity hook → pain → problem → hope → loop-opener CTA. Emoji only if brand permits.>

insight (hook): <research-file>#<line-or-anchor> — <≤8-word paraphrase>
voc (agitate phrase): <research-file>#<line> — "<verbatim phrase lifted into the body>"

---

## COPY B — COMPRESSION (~50 words)
**HEADLINE 2:** <3-5 word headline>
insight (headline 2): <research-file>#<line-or-anchor> — <≤8-word paraphrase>

<same five beats, compressed. Emoji only if brand permits.>

insight (hook): <research-file>#<line-or-anchor> — <≤8-word paraphrase>
voc (agitate phrase): <research-file>#<line> — "<verbatim phrase lifted into the body>"
```

---

## Hard Rules (all copies must pass)

1. **First line of both copies must scroll-stop.** No warm-ups. No "hey" / "imagine if" / "are you tired of". Rip attention immediately.
2. **No banned words:** life changer / breakthrough / game changer. Add avatar-specific banned words from the persona's tonal contract (for Avatar 2 life-transition: no "investment," "dream home," "build wealth," "maximize returns," upbeat/celebratory language).
3. **CTA = read-cue, brand-conditional.** Ad → letter/page: a read-cue ("see the number", "read how") + the URL, never "Sign Up / Submit / Book Now". No emoji or arrow glyph unless the client's `brand-voice.md` permits emoji.
4. **No corny/cringey.** If it reads like a LinkedIn influencer, rewrite.
5. **Emoji OFF by default.** Include emoji ONLY if `brand-voice.md` permits; then 2-4 max, never decorative, each carrying weight. Senior / advisory brands: zero emoji, zero exclamation marks.
6. **Built on the curiosity-led structure** (Body Copy Structure section). Curiosity hook → pain → problem/agitate → hope → loop-opener CTA. Copy B is the compression of Copy A (same beats), not a different angle.
7. **Headlines 3-5 words MAX.** These populate Meta's headline field (the short text below the image, not the overlay). If you're writing 6+ words, you're writing a text overlay, not a headline.
8. **Paragraph rhythm:** short lines, one idea per line. White space between paragraphs. Each line should make the reader want the next.
9. **Every hook and headline carries a resolving insight tag** (Insight tags section). The agitate beat carries a `voc:` source pointer. Untagged output is invalid and fails the hook gate.

---

## Hook gate (run before output is final — rebuild M2.2)

Hooks/headlines are the highest-leverage, easiest-to-fake part of the copy, so they pass through a code-decided gate before the copy bank is considered final. The gate is not advisory — it fail-closes the build.

**Step 1 — emit a hooks JSON.** Collect every hook (the first line of each copy) and every headline into a flat JSON array. Score each on five 1-5 dimensions and attach its insight tag:

```json
[
  {
    "hook": "We overpaid 40-50k on our first flat. Not doing it twice.",
    "scores": { "clarity": 5, "avatar_match": 5, "flow": 4, "insight_tag_resolves": 5, "native_feel": 4 },
    "insight": "clients/_smoketest/00_inputs/research/voc-reddit-dump-260611.md#L30 — upgrader overpaid 40-50k, won't repeat"
  }
]
```

- `clarity` — a cold reader gets it in one pass.
- `avatar_match` — would THIS avatar think "that's me".
- `flow` — reads aloud clean, no stumble.
- `insight_tag_resolves` — your confidence the tag is real (the gate re-checks it anyway).
- `native_feel` — feed-native, not salesy, no AI tell.

**Step 2 — run the gate:**

```
python3 scripts/hook_gate.py <hooks.json> --root clients/<slug>
```

The gate code-decides: average score ≥ 4.0 for every hook AND every insight tag must resolve to a real file at a real line/anchor. On any failure it exits 1 and names what broke. PASS (exit 0) is required before you finalise the copy bank. Use `--audit` to see the per-hook table without fail-closing. Full input shape + format in `python3 scripts/hook_gate.py --help`.

This is the hook-side sibling of the Claim Gate (`scripts/claim_gate.py`), which guards the body's numeric claims. Run both: hook gate on the hooks JSON, claim gate on the finished copy `.md`.

## Additional hook sources (input candidates — operator extension point)

The default hook source is the avatar's research (VOC dump, buyer-profile, big-angle-spotter angle spine). When that runs thin, or for breadth before you narrow, the global `script-skill` carries a large hook library and a query flow you can mine for candidates — by reference, not by duplication:

- `~/.claude/skills/script-skill/references/viral-hooks-library.md` — 1000+ hook templates across 7 categories (educational, comparison, myth-busting, storytelling, authority, day-in-the-life, engagement). Use for batch ideation when the research-native hooks are thin.
- `~/.claude/skills/script-skill/references/hook-bank.md` — example library by element + reusable structural templates.
- `~/.claude/skills/script-skill` Phase 3.5 (the 3-element framework: Relatability / Sensationalism / Stakes) + `cases/case_log.md` — for single-brief depth calibrated against decoded real-world hooks.

Rules when mining script-skill:
- A borrowed template is a STARTING shape, not a finished hook. It still has to pass every Hard Rule, carry a resolving insight tag back to THIS client's research, and clear the hook gate. A template with no client research line behind it is invalid output.
- Do not edit script-skill — it is read-only here. Fold its assets in by reference only.

**Operator extension point:** to add a future hook source (a new swipe file, a competitor scrape, a client's own winning ads), append it as a bullet to the list above with a one-line "use when X" trigger. Keep each entry a pointer + trigger — never copy the source's contents into this skill.

---

## Output File Location

Save the output to (adjacent to big-angle-spotter outputs for the same DCT):

```
clients/<slug>/angles/big-angle-spotter/wave-<N>/DCT<N>/halbert-copy.md
```

Inside that file, structure:

```markdown
# Meta Copy Bank — <BRAND> — DCT<N> — <YYMMDD>

**Angle:** <angle text>
**Avatar:** <avatar ref>
**Awareness / Sophistication:** <AW / SOPH>
**Landing page:** <URL>

---

## COPY 1 — PRIMARY (~150 words)
**HEADLINE 1:** <3-5 words>
insight (headline 1): <research-file>#<line-or-anchor> — <≤8-word paraphrase>

<body copy: the full curiosity-led sequence — this is the lock>

insight (hook): <research-file>#<line-or-anchor> — <≤8-word paraphrase>
voc (agitate phrase): <research-file>#<line> — "<verbatim phrase>"

---

## COPY 2 — COMPRESSION (~50 words)
**HEADLINE 2:** <3-5 words>
insight (headline 2): <research-file>#<line-or-anchor> — <≤8-word paraphrase>

<body copy: same five beats as COPY 1, fewer words>

insight (hook): <research-file>#<line-or-anchor> — <≤8-word paraphrase>
voc (agitate phrase): <research-file>#<line> — "<verbatim phrase>"

---

## Sheet Mapping

| Sheet Column | Value |
|---|---|
| HEADLINE 1 | <headline 1 verbatim> |
| HEADLINE 2 | <headline 2 verbatim> |
| COPY 1 | <body copy 1 verbatim, with emojis + CTA> |
| COPY 2 | <body copy 2 verbatim, with emojis + CTA> |

> The `insight:` and `voc:` lines are the audit trail — they stay in this `.md`, NOT in the sheet (the sheet only carries the four shippable text fields). They are what `scripts/hook_gate.py` checks before this file is final.
```

---

## Integration in the DCT Pipeline

**Position:** Step 13 of big-angle-spotter's conceptual flow (post-step 12). Runs after image prompts are written.

**Sequencing per DCT:**

```
big-angle-spotter:
  Step 7  → angle expansion
  Step 8-9 → 25 ranked text-overlay headlines (long-form, for image overlay)
  Step 10-10b → top 3 text-overlay headlines extracted
  Step 11 → 3 ad prompts (per overlay headline, with visual spec)
  Step 12 → 3 image prompts (paste-ready for Nano Banana / Midjourney)
THEN:
  Step 13 (this skill) → 2 short Meta headlines + 2 primary-text copies for the SAME angle
  → feeds COPY tab via ad_concept_sheet_writer.py
```

**Why one Halbert run per DCT (not per top-3 overlay headline):** Meta DCT rotates all text variants across all image variants. 2 headlines × 2 copies × 3 images = 12 combinations. One run suffices; more would cause diminishing returns and bloat the COPY tab.

## Quality Standards

- UK English (`realise`, `colour`, `optimise`, `centre`) — matches big-angle-spotter convention
- Voice matches brand tone from `context-profile.json` + `clients/<slug>/brand-voice.md`
- Passes `skills/copy-editing/references/overused-ai-patterns.md` (no AI-slop patterns)
- Passes avatar tonal contract (avatar-*.md "Language to Avoid")
- Passes `clients/<slug>/learnings.md` saturated-angle check (don't echo tried-and-killed hooks)
- Passes `scripts/hook_gate.py` (every hook/headline scores ≥4 avg AND resolves its insight tag) before the bank is final
- Passes the research-completeness precondition (`scripts/research_gate.py`) before any generation starts

## Known Limitations

- Headlines capped at 5 words — some avatars benefit from 6-8 word headlines (e.g. curiosity-loop specific). If a specific angle genuinely needs longer, split: keep 3-5 word "grabber" for the headline field, extend into primary-text opener.
- Does NOT generate ad overlay text. That's big-angle-spotter's step 8-10b territory.
- Does NOT generate angle ideation. Upstream work.

## References

- `references/SKILL-v1-75-matrix-LEGACY.md` — archived v1 approach (5 awareness × 10 angles × 75+ headlines matrix). Replaced because v1 output was too broad: a DCT only needs 2 headlines + 2 copies, not 75. v1 remains available if future strategy needs the full matrix.
- `references/awareness-angle-matrix.md` — Schwartz awareness × angle matrix reference (still useful for angle ideation in upstream skills)
- `references/mass-desires-catalog.md` — LF8 mass desire reference

---

## 10-5-5 Mode (opt-in — Meta Flex)

> **Default is unchanged.** Everything above stays the law: 2 copies + 2 headlines per angle, one Halbert run per DCT. This mode fires ONLY when the operator passes the 10-5-5 flag or names the method explicitly (e.g. `/ads:headlines --method 10-5-5`, or a tracker with `dct_structure.method == "10-5-5"`). Absent that, behave exactly as today. Do not auto-switch.

Meta retired the old DCT toggle (capped 3 images / 2 primary texts / 2 headlines) and replaced it with the **Flex** format (up to 10 media / 5 primary texts / 5 headlines). "10-5-5" is Flex's ceiling. Operator decision D1 (2026-06-03) locks the shape to **5 angles × 2 variations**. Full spec: `docs/methods/10-5-5/SPEC.md`.

### What this skill emits in 10-5-5 mode

The unit shifts from per-DCT (2+2) to **per-wave across 5 angles**, with each angle locked to ONE shipped pair:

| | 3-2-2 default (per angle) | 10-5-5 mode (per wave = 5 angles) |
|---|---|---|
| Copies | 2 (~50w + ~150w) | **1 locked copy per angle** → 5 copies/wave |
| Headlines | 2 (3-5 words) | **1 locked headline per angle** → 5 headlines/wave |
| Sheet rows | 1 row per DCT | 1 row per angle → **5 rows/wave** |

The "one row per angle, not per visual variant" rule from corrections.md (260420) carries straight over — the 2 image variations of an angle share the SAME locked copy + headline. The row tracks the strategic bet; visuals live in the tracker.

### The over-draft → narrow move (this is the headline craft)

For each of the 5 angles, draft **~5 headlines**, then narrow to the single best. This is the 2→5-7 expansion the 260418 corrections note already planned, now formalised by the method:

1. Generate ~5 headline candidates per angle (3-5 words each, all passing the Hard Rules above).
2. Pick the ONE that scroll-stops hardest for that angle's awareness/sophistication — that becomes `headline_1`.
3. **Keep the losers.** Write all candidates to the tracker's `headline_drafts[]` for that angle. They are the audit trail and the next-wave reservoir — never discarded.

For over-draft *breadth* (more candidate angles per awareness level before you narrow), the archived `references/SKILL-v1-75-matrix-LEGACY.md` (5 awareness × 10 angle banks × 75+ headlines) is a useful generator. You are not shipping 75 — you are mining that width to find 5 strong angle-headlines.

Copy stays a single locked piece per angle: the **~150w curiosity-led PRIMARY** (Copy A) from the Body Copy Structure. Ask for the one ~150w primary; the over-draft discipline applies to headlines, not body copy. The ~50w compression is optional in 10-5-5 (the COPY tab holds one locked copy per angle).

### Tracker + sheet contract

Each angle is one `creatives[]` entry: `copy_1` + `headline_1` filled, `copy_2` / `headline_2` left **empty** (kept only for 3-2-2 back-compat). Batch ids are unique per angle — `DCT010-A01` through `DCT010-A05`. The writer emits one CREATIVES row + one COPY row per entry = 5 rows/wave.

- Schema: `skills/ad-concept-engine/references/dct-tracker-10-5-5.schema.json`
- Sample tracker: `skills/ad-concept-engine/references/sample-10-5-5-tracker.json`

Do not duplicate the schema here — read those two files before writing a tracker.

### Caveats (recorded, not hidden)

- 10-5-5 has **zero proven results** for our clients yet — it is a platform-ceiling fit, validated by a proof wave (SPEC §4). Treat it as experimental.
- Verify Meta's live Flex limits against the actual ad account before the first upload (SPEC Open Item O4). If Meta's caps differ, the 5/5 counts change.

---

## Skill Graph

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[ad-concept-engine]] (skill, 0.14)

<!-- skill-graph:end -->
