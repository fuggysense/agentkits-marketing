# Direct-Response Singing / Music Ads Layer

**Purpose:** rules for applying the DR spine inside sung / musical short-form ads. Music does NOT replace DR — it changes the DELIVERY MECHANICS.

**Source:** Iman Gadzhi take 2026-05-18, music addendum (see `iman-take-260518.md` lines 143-209).

---

## Core ruling

> Singing ads use the SAME DR spine: **pain → gap → mechanism → belief shift**. Music is a delivery wrapper, NOT a separate persuasion track.

If the song has no DR structure under it, it becomes a cute brand asset, not a cold-traffic ad. You might get recall, but not response.

---

## Structure rules for sung short-form

| Beat | Job | Recommended delivery |
|---|---|---|
| Line 1 | Hook — sonic interruption or memorable phrase | **SUNG** |
| Lyric body | State pain OR desired state natively in the music | **SUNG** |
| Mechanism / proof / belief shift | DR work after attention is won | **SUNG** in conversational metaphor (see §Format amplifies vs buries mechanism worked examples). **Default = SUNG.** Use spoken only if brief explicitly carries `mechanism_delivery: "spoken_bridge"`. NEVER extract ingredients/pharmacology into a separate spoken VO — translate to singable metaphor or pick a different angle. |

**Best practice (Iman):** don't sing everything. Melody carries the HOOK + emotional carrier. Switch to clearer spoken DR language once attention is secured.

---

## How LF8 translates in music

**STRONGER** than in spoken word. Rhythm delivers desire faster than exposition.

- Comfort, status, freedom, sex, approval — all felt immediately through rhythm
- Use the per-market dialect from `lf8-market-translation.md` for the lyric
- Translated, not literal — sung primal language reads even cornier than spoken primal language

---

## How open loops translate

**Musical, not informational.** Same tension structure, different vehicle:

- Repeated lyric → unanswered question carried by repetition
- Unfinished phrase → resolves at the next beat
- Call-and-response → tension structure baked into the melody

See `concept-stage-mandatory-checks.md` Pillar 1 for the open-loop check. In music, the loop is held via the musical phrase, not the verbal phrase.

---

## Format-market fit for sung ads

| Market type | Music verdict |
|---|---|
| Problem-aware cold traffic | Sung hook can replace verbal hook, but NOT the DR spine |
| Educated / sophisticated audiences | Can **OUTPERFORM** spoken word — cuts through sameness, sticks |
| Technical / trust-heavy / low-desire | **Risk of misfire** — music lowers perceived seriousness |
| High-emotion consumer (wellness, beauty, fitness, DTC) | **LETHAL** if lyric names pain fast and visual proof is obvious |

---

## Where sung ads fail (anti-patterns to reject at seeder stage)

1. Song tries to BE the ad instead of SERVING the ad
2. Hook is memorable but the BUYER is unclear
3. Audience hears entertainment, not relevance
4. Market sophistication too low — lyric never names the problem clearly enough

---

## Iman's warning (mandatory pre-emit check)

> "Singing ads make discipline MORE important, because the vehicle is seductive and it's easy to fool yourself into thinking 'this is creative' when it's actually just ornamental."

The seeder MUST verify the concept passes the standard concept-vs-content test (see `concept-stage-mandatory-checks.md`) BEFORE accepting "but it's a great song" as a justification. If the song doesn't pass the four spine tests, it's ornamental — reject.

---

## Decision rule — when to choose a sung format at all

Apply the standard format-last 4-gate rubric from `concept-stage-mandatory-checks.md`. For sung ads specifically:

| Gate | Sung-ad consideration |
|---|---|
| 2-second legibility | Can the LYRIC name the buyer or problem in the first 2 seconds? If not, music buries it. |
| Proof form (person / process / metaphor) | Music typically pairs with metaphor or person — process proofs usually need spoken word |
| Creator credibility | The voice must be culturally fluent in the target market's music genre, OR the song must be deliberately ironic |
| Format amplifies vs buries mechanism | **Mechanism MUST be translated into singable conversational metaphor — NEVER named as a technical ingredient or pharmacology phrase in lyric.** If you cannot sing the mechanism the way a real person would sing it to a friend, the mechanism is too technical for THIS concept — pick a different angle. Do NOT extract the mechanism into a separate spoken VO unless the brief explicitly requires `mechanism_delivery: "spoken_bridge"`. Default = ALL sung, in real-song register. |

**Concrete bad → good examples (read these before writing any sung lyric — added 2026-05-22):**

| ❌ BAD (jargon / technical / un-singable) | ✅ GOOD (sung-real, metaphor-led, conversational) |
|---|---|
| *"Ferric saccharate under the trigger"* | *"What was blocking the door, gone"* / *"The kind that slips right through"* |
| *"Hepcidin spike blocks absorption"* | *"Your body locked the gate behind you"* / *"It shut you out, you didn't know"* |
| *"Day 60, ferritin 54"* (number-stamp) | *"Sixty days, and I'm not the one cancelling things anymore"* (carries the number in a lived sentence) |
| *"Storage form of iron"* (clinical) | *"The kind that stays / the kind that lasts"* (sensory) |
| *"Below 50 you'd be in treatment"* (geographic claim) | *(do not sing — keep this for sales letter only)* |

**The naturalness test:** read the line aloud as if you're a tired 35-year-old woman humming to herself in the kitchen. If she'd say "what?" or it sounds like a doctor wrote it, REWRITE. A real songwriter never sings ingredients — they sing what the ingredient DOES to the person, in plain words.

---

## Required outputs for sung ads

> **Absorbed 2026-05-19** from `../general/script-and-music.md` §Singing Ad + `../general/suno-manual-target.md` after a 4-condition methodology A/B test on the TakeKine `dr-foundation-pilot-singing` pack confirmed those two files were ~70% redundant with this one for lyric writing. This file is now the single load-bearing reference the pack-builder reads for singing flows. The other two files remain in the repo for non-singing scripts (VO, avatar acting, no-dialogue) and historical reference.

For any concept with `script_mode: "singing"`, the pack-builder MUST output:

- **Sung lyrics** broken into structure slots (`intro` / `verse` / `pre_chorus` / `chorus_hook` / `bridge` / `outro` as needed). Every slot gets a populated `full_lyric` field — seed lines and locked chorus hooks alone do NOT satisfy this requirement.
- **Spoken bridge** for the mechanism reveal — per the "sing hook + emotion, speak the mechanism" rule above.
- **Music direction:** genre stack, mood, tempo BPM range, vocal style, instrumentation.
- **Hook timing:** where the product/offer line lands.
- **Visual performance direction.**
- **Brand words to include + claim words to avoid.** Sung claims are STRONGER than spoken (rhythm makes them stickier). Lock `forbidden_expressions` out of lyrics — do not paraphrase them either.
- **Rhyme-pressure scan.** Identify words whose obvious rhymes drift into forbidden-claim territory (e.g., rhyming clinical terms forces diagnosis-adjacent pairings). Substitute with allowed paraphrases before writing the full lyric.
- **Negative/exclude list** (sounds, instruments, or production elements to suppress in Suno).
- **Manual Suno paste steps.**
- **Rights and consent notes + commercial-use checklist.**

**Policy boundary:** Suno is a manual creative target, not an automatable backend. No public official Suno API. Third-party "Suno API" wrappers are unofficial and require explicit operator approval before use. Do NOT emit an API request object unless a real integration has been approved.

---

## Sung word budget by duration

> **Why this section exists:** spoken-word budgets (see `../general/video-compression-by-duration.md`) do NOT translate 1:1 to sung lyrics. Sustained vowels stretch syllables 2-4x. Choruses repeat (write once, play 2-3x). Intros/outros eat ~3-6s of setup beats. Vocal style (rap-density vs ballad-stretch) shifts per-beat word density by 3-5x. The pack-builder needs a lookup that accounts for all four.

### Master table (sung lyrics — distinct from spoken)

| Duration | Baseline sung words (mid-tempo pop) | Rap-dense ceiling | Ballad-stretch floor | Chorus repeats (typical) | Setup overhead (intro+outro) |
|---|---|---|---|---|---|
| **15s** | ~18-22 written words | ~40 | ~8-10 | 1 (no repeat — full song is the hook) | ~2s |
| **30s** | ~38-50 written words | ~85 | ~18-22 | 1-2 | ~3s |
| **45s** | ~60-75 written words | ~130 | ~30-35 | 2 | ~4s |
| **60s** | ~80-100 written words | ~180 | ~40-50 | 2-3 | ~5s |
| **90s** | ~130-160 written words | ~280 | ~65-80 | 2-3 (+ bridge) | ~6s |

**Rules:**
- "Written words" = unique words the pack-builder must author. A repeated 8-word chorus played 3x = 8 written, ~24 played.
- Spoken bridges (mechanism reveal per the core ruling) follow `video-compression-by-duration.md` word budgets, NOT this table. Subtract the spoken-bridge seconds from the sung total before sizing.
- Sustained-note math: a 4-second sustained vowel ("freeeeeeee") = 1 written word but eats the same airtime as ~10 mid-tempo words. Budget accordingly.

### Style modifiers

| Vocal style | Density multiplier on baseline | Notes |
|---|---|---|
| Trap / rap / drill | 2.0-2.5x | Cap at the "rap-dense ceiling" column. |
| Pop-punk / uptempo indie | 1.3-1.5x | Choruses still repeat; verses are denser. |
| Mid-tempo pop / R&B | 1.0x (baseline) | Default reference column. |
| Ballad / slow R&B / acoustic | 0.4-0.6x | Sustained notes dominate; use ballad-stretch floor. |
| Children's jingle / chant | 0.6-0.8x | Repetition heavy; written-word count drops further. |
| Spoken-word over beat | Use `video-compression-by-duration.md` rate | Treat as spoken with rhythmic delivery. |

### Worked examples

**Example 1 — TakeKine c02 (30s, mid-tempo pop, 5 character voices, 2 chorus repeats):**
- Baseline 30s = ~38-50 written words.
- 2 chorus repeats means ~10-14 of those words are the chorus hook (written once).
- Remaining ~28-36 words distribute across intro (~4) + verse (~14-18 per character beat) + outro (~4).
- With 5 characters trading lines, each character carries ~6-8 words. Tight — borderline needs 45s.

**Example 2 — 60s ballad, single vocalist, mechanism spoken bridge:**
- 60s total = ~80-100 baseline. Ballad multiplier 0.5 → ~40-50 written words sung.
- Reserve 12s for spoken mechanism bridge (~30 spoken words from `video-compression-by-duration.md`).
- Sung sections fit ~40-50 words across intro / verse / chorus (repeated 2x) / outro.

**Example 3 — 15s rap hook, product chant:**
- 15s baseline ~18-22. Rap multiplier 2.0 → ~36-44 written words.
- No chorus repeat at 15s. Setup overhead ~2s. Effective sung window ~13s.
- All 36-44 words deliver in one continuous flow. Dense — only works if cadence is locked tight.

---

## Multi-character Suno label spec

> **Why this section exists:** Suno's structural tags are documented and reliable. Arbitrary character names are NOT — Suno often interprets `[Owl]` as a vocal-style cue ("owl-like voice") rather than a character-switch instruction. Producers running multi-voice concepts (TakeKine c02 with 5 animal voices, ensemble pieces, call-and-response) need a labeling convention that Suno actually respects.

### What is reliably documented (Suno-side)

- `[Verse]`, `[Verse 1]`, `[Verse 2]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Intro]`, `[Outro]`, `[Hook]`, `[Refrain]` → reliable structural anchors. Suno respects these.
- `[Instrumental]`, `[Break]`, `[Drop]`, `[Solo]` → reliable production-section tags.
- Square-bracket production cues like `[soft]`, `[whispered]`, `[shouted]`, `[harmonies]`, `[ad-libs]` → influence delivery on the LINE that follows. Reliable for delivery shaping, NOT for character switching.

### What is ambiguous (EMPIRICAL TODO)

- Arbitrary names: `[Owl]`, `[Fox]`, `[Narrator]`, `[Customer]`, `[Doctor]` → Suno's behavior is inconsistent. Sometimes interpreted as character switch, often interpreted as vocal-style cue ("owl-sounding voice"), sometimes ignored.
- Dialogue notation: `Owl: "line"` vs `[Owl] line` vs `(Owl) line` → no consistent Suno behavior documented.
- Voice-model assignment per character → not natively supported in standard Suno custom mode as of last verified usage. Voice-model feature applies to ONE voice per generation.

### Recommended pattern (structural-anchor-first)

Lead with a documented structural tag, append the character role as a parenthetical guide:

```
[Verse 1] (Owl voice — wise, low, slow)
Lyric line for owl character here...

[Pre-Chorus] (Fox voice — sly, mid-tempo, smirking)
Lyric line for fox character here...

[Chorus] (all characters together — harmonies)
Shared chorus hook here...

[Bridge] (Narrator voice — spoken, intimate)
Mechanism reveal spoken here...
```

**Why this pattern:**
- The structural anchor (`[Verse 1]`) is the documented, respected tag — Suno follows it.
- The parenthetical character note shapes delivery on that section without confusing Suno's section parser.
- Putting the character cue INSIDE the structural tag (as a delivery instruction) is more reliable than expecting Suno to switch voices on a bare `[Owl]` tag.

### Fallback when single-voice generation is mandatory

If Suno generates one voice for the whole track regardless of structural cues (common in default custom mode):
- Treat the multi-character concept as a **single-narrator-doing-impressions** brief. The vocal direction field should explicitly request character-voicing within one performance.
- OR: generate per-character stems in separate Suno runs (one per character), then stitch in post. Document this in `manual_suno_steps`.
- OR: use Suno's voice-model feature for the lead character + run separate generations for other characters and layer.

### EMPIRICAL TODO (flagged for Suno-side testing)

1. Confirm whether `[Verse 1] (Owl voice)` reliably shifts delivery vs `[Verse 1]` alone.
2. Test whether `[Owl - Verse 1]` (character-first) vs `[Verse 1 - Owl]` (structural-first) produces different parsing.
3. Test whether dialogue-style notation (`Owl: line`) inside a structural tag forces character separation.
4. Verify behavior when 3+ characters are referenced in one generation (current recommendation assumes degraded reliability above 2-3 distinct voices in a single run).
5. Document current Suno version + mode (Simple / Custom / Voice Model) under which each test was run — behavior has shifted across Suno releases.

Future operators: log results into this section. Replace EMPIRICAL TODO entries with confirmed patterns + version numbers as testing completes.

---

## Suno-ready output schema (YAML)

Use this canonical shape for the pack-builder's singing-concept output. Field names are stable — downstream tools (HTML publisher, AG1 review surfaces, post-AG1 manual run guide) parse against this schema.

```yaml
music_ad_type: singing_ad | jingle | music_bed | hook_song | product_chant
generation_access: manual_suno_only
suno_mode: simple | custom | instrumental | add_vocals | voice_model
title:
duration_target_sec:
platform_use: paid_social
simple_prompt:
style_prompt:
genre_stack:
mood:
tempo_bpm_or_feel:
vocal_direction:
instrumentation:
instrumental: false
lyrics_brief:
lyrics:
  intro:
  verse:
  pre_chorus:
  chorus_hook:
  bridge:
  outro:
structure_timeline:
negative_exclude:
brand_offer:
cta_line:
must_say:
must_not_say:
voice_or_persona_requirement:
rights_and_consent_notes:
commercial_use_checklist:
video_beat_map:
variant_prompts:
manual_suno_steps:
```

Each `lyrics.<slot>` field MUST contain the FULL line(s) for that slot, not a seed or topic. Empty slots are only acceptable when the concept's structure explicitly omits that slot.

---

## See also

- `core-framework.md` — the DR spine that singing ads must respect
- `lf8-market-translation.md` — dialect translation for the sung lyric
- `concept-stage-mandatory-checks.md` — the standard concept-vs-content test (mandatory before any sung-ad concept is approved)
- `../general/script-and-music.md` — general script methodology for **non-singing** flows (VO, avatar acting, no-dialogue). Singing-flow content was absorbed into this file 2026-05-19; do NOT load `script-and-music.md` for singing concepts.
- `../general/suno-manual-target.md` — historical Suno research reference. Singing-flow output schema + policy were absorbed into this file 2026-05-19; do NOT load `suno-manual-target.md` for singing concepts.
- `iman-take-260518.md` — full Iman transcript including music addendum (lines 143-209)
