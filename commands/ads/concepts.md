---
description: Generate paid ad concepts (angles upstream of hooks) — Iman-grounded, hyper-specific persona, problem-aware target, proof front-loaded. Composes content-moat + unique-mechanism-* + persuasive-premise.
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: <offer focus or "from-winner: <organic-concept-id>"> [--client <slug>]
---

# /ads:concepts

**Underlying skills (composed):** `content-moat` + `unique-mechanism-problem` + `unique-mechanism-solution` + `persuasive-premise` + `problem-promise` + `usp-generator`.
**Note:** `ad-concept-engine` was referenced in routing-table.md but doesn't exist in the repo. Until it does, this command composes the existing skills above.

**Job-of-asset:** Efficiency + qualification. Make the right buyer self-select and keep moving toward conversion.
**Output:** 5-7 paid ad concepts per batch (each becoming 3-5 hook variations downstream, total 15-35 testable creatives).

This is the **upstream** of `/hooks:generate` (which gets run in `--mode=ads` for each chosen concept). A concept = the angle/buyer/pain/mechanism/promise/proof/objection. The hook is the first 3 seconds. **Brief the concept fully before generating hooks.**

---

## Iman-grounded surface rules (PAID)

These are LOCKED for paid concepts. Source: Iman Gadzhi via AskIman Whop chatbot, 2026-05-12, 10 isolated queries. Full findings: `/Users/jerel/.claude/jobs/ad9ddcd2/iman_organic_vs_ads_concepts.md`.

| Dimension | Paid rule |
|---|---|
| Asks the question | "What angle will make the right buyer self-select and keep moving toward conversion?" |
| Brief starts from | Buyer's pain, desire, mechanism, objection, market angle — closer to a commercial thesis than content |
| Awareness target | Problem-aware → product-aware (cold). Most-aware = retargeting only. |
| Specificity | **Hyper-specific.** One named person, one named pain, one named moment. Broad TAM is a trap at the ad level. |
| Pain framing | Surgical, painfully specific, cost-of-inaction. **Lead with the pain.** Sharper than organic but NOT reckless — polarizing ≠ lying. |
| Proof load | **Baked in early.** Hook or immediately after. The colder the audience, the earlier the proof. |
| Risk tolerance | Bigger creative swing allowed, inside a tight commercial frame |
| Volume per angle | **3-5 variations per angle. Not 12. Not 20.** Vary hook/framing, keep core promise. |
| Position in loop | Scaler — where proven signal gets budget. Winners recycle back into organic. |

**Cross-surface rule (applies to both organic and paid):**
- Rule 0: capture CTA destination FIRST. Hard CTAs are paid's default. Soft CTAs in paid = retargeting only.
- Rule 4: repurposing direction is asymmetric. Organic discovers → paid validates → organic resharpens. **Never port raw organic to paid untouched.**
- Rule 5: concept ≠ hook. Don't write hooks here.
- Rule 6: polarizing ≠ lying. Exaggeration beyond reality kills lead quality at $5K-$15K price points.

---

## Step 1 — Resolve client + load deterministic inputs

| # | Input | Path | Status |
|---|---|---|---|
| 1 | Brand voice | `clients/<client>/brand-voice.md` | **Required** |
| 2 | Buyer profile | `clients/<client>/buyer-profile.md` | **Required** |
| 3 | ICP | `clients/<client>/icp.md` | **Required** |
| 4 | Offer | `clients/<client>/offer.md` | **Required** |
| 5 | Channels | `clients/<client>/channels.json` | **Required** |
| 6 | Past ad winners + losers | `clients/<client>/learnings.md` → `## Ad winners` / `## Ad losers` | Optional |
| 7 | Organic winning concept (if porting from organic) | `clients/<client>/01_ideate/output/<id>.md` | Optional |
| 8 | Competitor ad library data | `clients/<client>/_swipe/competitor-ads/` | Optional |

Halt if any required file is missing.

## Step 2 — Capture CTA destination + offer focus (Rule 0)

Before generating any concept:

- **Primary CTA:** what specific action? Book a call / Apply / Buy now / Free trial / Quiz funnel. Hard CTAs are default for paid.
- **Offer focus:** which product/tier from `offer.md` does this batch target? Lead magnet? T1 paid? T2? Core?
- **Price point:** if $5K-$15K+ offer, Iman's "more embedded proof + concept doing more work" rules apply intensely.

Persist all three in the output.

## Step 3 — Pick the input mode

This command has 3 input modes — declare which:

### Mode A: Fresh paid concepts (cold)
Variable input = `{{offer_focus}}` or a market thesis. Example:
> *"Property agents losing money to PropertyGuru's $1,200/mo lead pricing"*

Generates 5-7 fresh concepts from scratch targeting the offer.

### Mode B: Port from winning organic concept
Variable input = `--from-winner: 2026-W19-concept-3`. Reads that organic concept and translates it into paid using the cross-surface translation rule.

### Mode C: Beat existing winning ad
Variable input = `--beat-winner: <winning-ad-transcript-or-id>`. Generates 5-7 angle variations that share the same body/CTA/offer but reframe the angle. This is your previously-pasted Prompt A pattern.

## Step 4 — The paid brief template (apply per concept)

For EVERY concept, fill these 8 fields. This is Iman's paid brief structure:

```
1. NAMED PERSON          (the ONE specific buyer — name, age, situation, current channel. NOT a segment.)
2. NAMED PAIN            (the ONE urgent pain — specific, time-bound, expensive)
3. NAMED MOMENT          (the trigger moment when the pain becomes intolerable — "Tuesday at 11pm", "after the third agent called", "the week MOP clears")
4. DESIRED OUTCOME       (the specific transformation they're buying — not a vibe, a state change)
5. MECHANISM TO BELIEVE  (the thing they have to accept is true for the offer to make sense — unique mechanism, proprietary method, contrarian framework)
6. PROOF FRONT-LOADED    (the credibility element baked into the FIRST 5 seconds — number, screenshot, named person, result. Not "trust me.")
7. OBJECTION NEUTRALIZED (the ONE objection this concept defuses — "I've tried other things", "agents are sleazy", "I can't afford it now")
8. CTA + AWARENESS LEVEL (the hard ask + the awareness level this targets — problem-aware / solution-aware / product-aware)
```

**Hyper-specific from the start.** If you can't name the person + pain + moment within 30 seconds of brainstorming, the concept is too broad. Go narrower.

**Mechanism is load-bearing.** "Better content" is not a mechanism. "The 4-pillar trust ladder that lets coaches charge $5K+ without case studies" is a mechanism. Differentiated. Named. Believable.

## Step 5 — Apply originality + voice scoring

Score every concept 0-100:
- **Originality:** vs competitor ads (if `_swipe/competitor-ads/` loaded) + past learnings.md ad winners
- **Voice fit (lower bar than organic):** still must pass brand-voice.md but paid allows sharper edges than organic. **Floor: 7/10** (vs organic's 8/10).

Why lower voice fit floor for paid: paid intentionally takes bigger creative swings inside the commercial frame. The trade-off is loss of voice nuance in service of conversion.

## Step 6 — Self-check before emitting each concept

For every paid concept, verify silently:

- [ ] All 8 fields filled (no blanks). NAMED PERSON / PAIN / MOMENT are concrete (not "young entrepreneurs")
- [ ] Awareness level = problem-aware → product-aware (cold). Flag if you drift to unaware (organic territory) or most-aware (retargeting only).
- [ ] Pain framing is surgical, not vague. "Cost of inaction" stated.
- [ ] Proof element is FRONT-LOADED (in the first 5 sec when this becomes a hook)
- [ ] Mechanism is NAMED, not generic
- [ ] Objection neutralized is the RIGHT objection (not a strawman)
- [ ] Hard CTA assumed unless retargeting
- [ ] Polarizing ≠ lying — claim is defensible
- [ ] Originality ≥ 60 vs competitor ads + past winners
- [ ] Voice fit ≥ 7/10

Concepts that fail self-check: regenerate.

## Step 7 — Volume rule

**Generate 5-7 concepts per batch. NOT 20.** Iman: "Not 12, not 20."

Each concept gets 3-5 hook variations downstream via `/hooks:generate --mode=ads`. Total testable creatives per batch = 15-35.

This is intentional. Paid testing economics break above 5-7 concepts per cycle.

## Step 8 — Output schema (use exactly)

Per concept, one block:

```
Ad Concept #N  [Offer-Focus · Awareness-Level · CTA-Type · Mode-A/B/C]
Title: [3-7 word commercial thesis]

NAMED PERSON       : [specific persona — name, age, situation]
NAMED PAIN         : [urgent, time-bound, expensive]
NAMED MOMENT       : [the trigger moment]
DESIRED OUTCOME    : [specific state change]
MECHANISM          : [the proprietary thing they have to believe]
PROOF (front)      : [the first-5-sec credibility element]
OBJECTION KILLED   : [the one objection this defuses]
CTA + AWARENESS    : [hard ask + awareness level]

Why this works (paid): [1-2 lines on the conversion mechanism]
Cost of inaction: [if they don't act, what specifically happens / costs / persists]
Originality: X/100  (vs competitor ads + past winners)
Voice fit: X/10    (passes brand-voice.md; lower floor of 7 vs organic 8)
Hook variations to generate: [3, 4, or 5 — operator picks via /hooks:generate --mode=ads]
```

Example (CB Agent / propwise-sg):

```
Ad Concept #2  [Agent SaaS · Problem-aware → Product-aware · Hard CTA: book demo · Mode A]
Title: "Stop paying $1,200/mo for tire-kickers"

NAMED PERSON       : Marcus, 38, 5-year mid-tier SG property agent doing 8-12 deals/year, spends $1,200/mo on PropertyGuru subscription
NAMED PAIN         : 70% of PG leads ghost or aren't financially qualified — wastes 15 hours/week on first calls that go nowhere
NAMED MOMENT       : Tuesday morning when he opens his PG lead inbox and sees the same garbage from last week
DESIRED OUTCOME    : Spend 3 hours/week on 5 leads that close at 60%+, not 15 hours on 30 that close at 5%
MECHANISM          : CB Agent's free bot pre-qualifies upgraders with a 6-question financial readiness check BEFORE they're sold as leads — flat fee, no transaction kickback
PROOF (front)      : "Last month, 47 of our 200 quiz-takers were verdict=Ready. 38 of those took a call. 22 closed." (real numbers from learnings.md)
OBJECTION KILLED   : "Another lead source promising quality" — answered by the verdict-distribution proof + the bot occasionally saying NOT to buy (alignment with agent's interest)
CTA + AWARENESS    : "DM AGENT to see this month's verdict distribution" → Problem-aware → Product-aware progression

Why this works (paid): hyper-specific persona (Marcus, the named cost of $1,200/mo), surgical pain (the 70% ghost rate), proof front-loaded (47-of-200 stat), CEA-compliant (flat fee), differentiation through the "we sometimes say no" mechanism.
Cost of inaction: 15 hours/week × 4 weeks = 60 hours/month wasted = $6,000/month in foregone deal-time.
Originality: 81/100 (no SG property tech leads with verdict-distribution as proof; CB Agent's "sometimes says no" is differentiating)
Voice fit: 8/10 (sharper than CB Agent's organic homeowner voice but stays compliance-safe)
Hook variations to generate: 5 (cost framing, time framing, identity framing, mechanism reveal, results-led)
```

## Step 9 — Persist

Write to `clients/<client>/01_ideate/output/<YYYY-WW>-concepts-ads.md`.

Append to `clients/<client>/learnings.md` under `## Ad concept generations`:
```
- YYYY-MM-DD · paid · offer: <focus> · 6 concepts · avg originality X/100 · CTA: <hard ask>
```

## RUN

Generate 5-7 paid concepts against the loaded deterministic inputs. Apply the Iman paid rules. Self-check every concept. Emit in the exact schema. Persist.

---

## Cross-surface translation (when porting from organic)

Iman: *"If you're talking about raw, untouched organic posts being ported straight into paid, I'd expect most of them to miss... Test the same core idea, not the exact same execution."*

**Keep:** angle, pain, mechanism, transformation, proof element
**Rewrite:** hook (sharper), CTA (harder), pacing (faster reveal), first-3-seconds (proof up-front), landing alignment (concept must match the LP it points at)

**Mode B input pulls the organic concept and runs this translation automatically.**
