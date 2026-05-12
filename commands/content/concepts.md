---
description: Generate organic short-form concepts (the ANGLES upstream of hooks) — Iman-grounded, voice-locked, broader-TAM at TOFU. Wraps content-strategy + content-moat.
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: <one-line topic or "pillar X for week Y"> [--client <slug>]
---

# /content:concepts

**Underlying skills:** `content-strategy` + `content-moat` (originality scoring).
**Job-of-asset:** Discovery + resonance. Make people CARE about the creator/idea so they self-select into the funnel.
**Output:** 10-15 organic concepts per pillar, distributed across funnel stages, originality-scored.

This is the **upstream** of `/hooks:generate`. A concept = an angle (the buyer, the pain, the mechanism, the promise, the proof, the objection). The hook is the first 3 seconds. **Brief the concept fully before generating any hook.**

---

## Iman-grounded surface rules (ORGANIC)

These are LOCKED for organic concepts. Source: Iman Gadzhi via AskIman Whop chatbot, 2026-05-12, 10 isolated queries. Full findings: `/Users/jerel/.claude/jobs/ad9ddcd2/iman_organic_vs_ads_concepts.md`.

| Dimension | Organic rule |
|---|---|
| Asks the question | "What would make someone stop scrolling and care about this person or idea?" |
| Brief starts from | Creator's worldview, human truth, sharp opinion, pattern interrupt, story, lesson |
| Awareness target | Unaware → problem-aware (sometimes solution-aware) |
| Specificity | Broader umbrella at TOFU so the algorithm finds adjacent viewers. Narrow at MOFU/BOFU. **Broader, not unfocused.** |
| Pain framing | Relatable, identity-based, self-diagnostic. **Lead with the tension, not the pain.** Let them self-diagnose. |
| Proof load | Layered — supports the lesson/story. Mid or close. **OK to delay.** Build trust deeper. |
| Risk tolerance | Smaller, more measured. Going too hard too fast distorts brand. |
| Volume per pillar | 5-10 videos before the pillar is tapped |
| Position in loop | Lab — where signal is discovered cheaply, then handed to paid for amplification |

**Cross-surface rule (applies to both organic and paid):**
- Rule 0: capture CTA destination FIRST. Soft CTAs (follow / save / DM keyword) allow broader concepts. Hard CTAs require sharper.
- Rule 4: repurposing direction is asymmetric. Organic discovers → paid validates → organic resharpens.
- Rule 5: concept ≠ hook. Don't write hooks here.
- Rule 6: polarizing ≠ lying. Especially at $5K-$15K offers.

---

## Step 1 — Resolve client + load deterministic inputs

If `--client <slug>` provided, use it. Otherwise infer from cwd. If neither, halt and ask.

| # | Input | Path | Status |
|---|---|---|---|
| 1 | Brand voice | `clients/<client>/brand-voice.md` | **Required** |
| 2 | Buyer profile | `clients/<client>/buyer-profile.md` | **Required** |
| 3 | ICP | `clients/<client>/icp.md` | **Required** |
| 4 | Offer | `clients/<client>/offer.md` | **Required** |
| 5 | Channels + funnel structure | `clients/<client>/channels.json` (or `funnel-goal.json`) | **Required** |
| 6 | Past winners | `clients/<client>/learnings.md` → `## Hook winners` or `## Concept winners` | Optional |
| 7 | Story bank | `clients/<client>/story-bank.md` | Optional |
| 8 | Niche outliers | `voice/swipe-pools/<niche>/outlier-pool.jsonl` | Optional |

Halt if any required file is missing.

## Step 2 — Capture CTA destination (Rule 0, non-negotiable)

Before generating any concept, ask (or infer from offer.md):

- **Primary CTA for this batch:** soft (follow/save/DM keyword) OR hard (book a call / buy / apply)?
- If hard CTA + organic, that's unusual — flag it. Hard CTAs from organic require sharper concepts + tighter proof. Default for organic is SOFT CTA unless explicitly overridden.

Persist the CTA choice in the output so downstream `/hooks:generate` knows.

## Step 3 — Capture pillar + funnel distribution

Read funnel + pillar weights from `channels.json` (or `funnel-goal.json`).

Default if unspecified:
- **Funnel split:** 60 TOFU / 30 MOFU / 10 BOFU
- **Pillar split:** 40 Educate / 30 Sell / 20 Story / 10 Inspire

If the operator's input is "pillar X for week Y" (e.g. "Pillar: Educate, Week 19"), generate ONLY for that pillar. Otherwise generate the full mix.

## Step 4 — Variable input

```
{{topic}}
```

A 1-2 sentence topic anchor. Examples:
- *"The hidden cost of value-only LinkedIn posting"*
- *"MOP timing for HDB upgraders"*
- *"Why every property calculator says yes"*

If empty, generate from the creator's worldview + buyer-profile pain points (no anchor → fully open).

## Step 5 — The organic brief template (apply per concept)

For EVERY concept, fill these 7 fields. This is Iman's organic brief structure:

```
1. WHO this is for          (specific persona slice from buyer-profile.md; broader than paid would allow)
2. TENSION named            (the felt-thing, not the pain — what's uncomfortable but unspoken)
3. BELIEF challenged        (the contrarian element — what assumption gets flipped)
4. STORY / INSIGHT          (the hook into the worldview — creator's lens, lived experience, observation)
5. PROOF (layered, not front-loaded)  (what evidence supports it — can land mid or close)
6. PILLAR + FUNNEL STAGE    (Educate/Sell/Story/Inspire + TOFU/MOFU/BOFU)
7. CTA ALIGNMENT            (what soft action does this push toward — save? follow? DM?)
```

**Tension ≠ pain.** Tension is what the buyer FEELS but doesn't name. Pain is what they'd name when asked. Organic concepts open on tension.

**Belief challenged is the differentiator.** If a concept doesn't challenge a belief, it's reportage, not content. Boring concepts have no belief-flip.

## Step 6 — Apply originality scoring

For every concept generated, score 0-100 against:
- The client's `learnings.md` past winners (no remix)
- The niche outlier pool (if loaded) — adapt patterns, don't copy
- Other concepts in this same batch (no two near-identical concepts)

**Floor:** originality ≥ 60. Below = regenerate or drop.

## Step 7 — Self-check before emitting each concept

For every generated concept, verify silently:

- [ ] Has all 7 fields filled (no blanks)
- [ ] Tension named (felt-but-unspoken), not raw pain
- [ ] Belief challenged is concrete (not "be more authentic")
- [ ] Passes brand-voice.md voice filter
- [ ] Awareness level = unaware → problem-aware (sometimes solution-aware). Flag if it drifts to product-aware (that's paid territory)
- [ ] Specificity is broader-umbrella appropriate (not paid's hyper-specific)
- [ ] Originality ≥ 60
- [ ] CTA destination aligned (soft, unless override)

Concepts that fail self-check: regenerate. Don't ship.

## Step 8 — Output schema (use exactly)

Per concept, one block:

```
Concept #N  [Pillar · Funnel-Stage · Awareness-Level · CTA-Type]
Title: [3-7 word descriptive title]

WHO       : [persona slice]
TENSION   : [the felt-but-unspoken thing]
BELIEF    : [the assumption flipped]
STORY     : [the worldview lens / lived experience / observation]
PROOF     : [evidence — can be delayed]
CTA       : [soft action this pushes toward]

Why this works (organic): [1-2 lines on the resonance mechanism]
Originality: X/100  (vs learnings.md + niche outliers)
Voice fit: X/10    (passes brand-voice.md)
Maps to N hooks: [estimate, typically 5-10 per pillar]
```

Example:

```
Concept #3  [Educate · TOFU · Problem-aware · Soft CTA: save]
Title: "Why your bank's number isn't on any calculator"

WHO       : MOP-clearing couple, 28-35, BTO in mature estate, looking at condos
TENSION   : They've run the numbers three times and gotten three different answers. Nobody trusts each other's math.
BELIEF    : "More calculators = more confidence." Actually more calculators = more disagreement.
STORY     : I keep finding new numbers when I run my own check vs whatever portal they used. There's a number the bank subtracts that public tools don't.
PROOF     : URA report screenshot showing the line item (delayed to mid).
CTA       : Save this so you have a checklist when you sit with the next agent.

Why this works (organic): names the tension (silent disagreement between spouses about which calculator is right), challenges a belief (more tools = more clarity), self-diagnostic (let them run it themselves), no aggressive sell.
Originality: 78/100
Voice fit: 9/10
Maps to N hooks: 6-8 (question hooks, secret reveal, case study)
```

## Step 9 — Output order

Generate in groups by pillar. If a topic was provided, ground all concepts in that topic. Otherwise span all 4 pillars.

```
==== EDUCATE (40%) ====
Concept #1 ...

==== SELL (30%) ====
Concept #N ...

==== STORY (20%) ====
Concept #N ...

==== INSPIRE (10%) ====
Concept #N ...

==== Batch summary ====
- Distinct beliefs challenged: [list]
- Pillar coverage: [counts]
- Funnel stages: [counts]
- Average originality: X/100
- Suggested next: pick 3 → /content:concepts-select → /hooks:generate per pick
```

## Step 10 — Persist

Write to `clients/<client>/01_ideate/output/<YYYY-WW>-concepts-organic.md` (matching the v0.5.2 plan's stage 01 folder).

Append to `clients/<client>/learnings.md` under `## Concept generations`:
```
- YYYY-MM-DD · organic · topic: <first 60 chars> · 12 concepts · avg originality X/100
```

## RUN

Generate 10-15 organic concepts against the loaded deterministic inputs. Apply the Iman organic rules. Self-check every concept. Emit in the exact schema. Persist.

---

## When to use vs `/ads:concepts`

Use `/content:concepts` when:
- Building organic short-form (IG Reels / TikTok / YouTube Shorts) content week
- Creator-led content (founder on camera, voice-locked to a person)
- Soft CTAs (follow / save / DM keyword)
- Discovery mode — finding which angles resonate before scaling

Use `/ads:concepts` when:
- Running paid Meta / TikTok / YouTube ads
- Hard CTAs (book call / buy / apply)
- Already have proven organic angles to validate at scale
- The audience needs to be PRE-FRAMED into a buyer

**Cross-surface translation rule:** when an organic concept hits, don't port the execution. Keep the angle/pain/transformation. Rewrite the hook/CTA/pacing/first-3-seconds for paid. See `/ads:concepts` Rule "Repurposing direction."
