# Step 11 — ad prompts (3 parallel, one per top-3 headline)

> FICTIONAL SMOKE-TEST DATA - not a real client. EMULATED. Each block = locked headline + primary
> body (~150w) + short variant (~50w) + a `provenance` block per SKILL.md §6. UK English, grade 4-6,
> calm/numbers-first tone, straight quotes, contrast the model not the people. Every claim that would
> touch live media is FICTIONAL and must clear the claim gate first.

---

## Ad 1 — Recognition hook (MP-01 Repeat-Mistake Upgrader)

**Headline:** Your agent sold your flat in three weeks. Notice how quiet they went when you started buying?

**Primary (~150w):**
You felt it before you could name it. On the sell side they were everywhere. Calls, viewings, a deal
closed fast. Then you started buying, and the same person went a little quiet.

Here's why. On the buy side, the better the price they get you, the less they earn. The incentive
quietly flipped, right when your 7-figure, decade-long decision needed someone fully on your side.

We fixed that by being paid differently. One flat fee. The same whether you buy at S$900k or S$1.6m.
No commission. We don't earn a cent more if you spend more, so the only thing we're optimising is
whether the unit is right.

Want to test it before you commit? For S$290 we'll tear down your current shortlist and show you the
numbers on each unit. You decide. No pressure.

**Short (~50w):**
On the sell side your agent moved fast. On the buy side, notice the silence? It's the maths: they
earn more when you spend more. We charge one flat fee instead. See the analysis on your shortlist for
S$290 before you commit to anything.

**provenance:**
```yaml
source_phrase_id: null   # add to research-pool.json
source_quote: "Sold our flat in 3 weeks, great. Now buying side and suddenly the same agent is much less helpful lol. Makes sense, less money for them on the buy."
source_url: "00_inputs/research/voc-reddit-dump-260611.md#quote-3 (FICTIONAL r/HDB)"
competitor_weakness_addressed: "Commission agents (and the dual sell+buy agent in particular) never name the buy-side incentive drop; this ad makes the felt experience explicit and offers the structural fix."
```

---

## Ad 2 — Mechanism hook (MP-03 Fee-Allergic Convertible / MP-01)

**Headline:** On the buy side, your agent earns more when you spend more. That's the whole problem.

**Primary (~150w):**
Read that again. The person advising you on the biggest purchase of your life is paid a slice of how
much you spend. Spend more, they earn more. Nobody in that room loses money if you overpay.

That's not a character flaw. It's the structure. And it's why "trust your agent" never quite settles
the knot in your stomach.

So we changed the structure. Meridian charges one flat fee, paid the same regardless of the unit you
buy or the price you pay. We don't take a commission and we don't take a referral split. The only
outcome we're paid to care about is that the numbers hold up.

Start small. The S$290 Shortlist Teardown puts a data-backed verdict on each unit you're considering,
with the analysis on the table. If it's useful, the fee credits toward the full advisory.

**Short (~50w):**
The maths is simple: your agent earns more when you spend more. So who in the room loses if you
overpay? We took commission out of it. One flat fee, same price whatever you buy. See your shortlist
torn down for S$290 first.

**provenance:**
```yaml
source_phrase_id: null   # add to research-pool.json
source_quote: "The whole game is rigged on the incentive. Fix the incentive and I'm in."
source_url: "00_inputs/research/voc-reddit-dump-260611.md#quote-26 (FICTIONAL r/singaporefi)"
competitor_weakness_addressed: "Both commissioned agents and 'honest agent' brands still earn from the transaction; none can claim a flat fee that is identical regardless of purchase price. This ad owns the one structure that removes the incentive entirely."
```

---

## Ad 3 — Fee-flip hook (MP-03 Fee-Allergic Convertible)

**Headline:** The "free" property agent isn't free. The cost is just hidden in the price.

**Primary (~150w):**
S$4,500 for advice, when agents are free? That's the reflex. It's also the trap.

The "free" agent isn't free. Their commission is built into the price you pay, you just never see it
itemised. One quiet purchase later, most buyers work that out the hard way.

Here's the maths laid bare. A flat S$4,500, paid once, with the full analysis shown to you. Against a
commission you can't see and an incentive that rewards a higher price. If a clear set of eyes stops
you overpaying by even S$30k, the flat fee isn't the cost. It's the saving.

And you don't take it on faith. The S$290 Shortlist Teardown shows you the method first: a verdict on
each unit, the numbers behind it, no sales pitch about how experienced anyone is. Then you decide.

**Short (~50w):**
"Free" agents aren't free, the commission is hidden in the price. We charge one visible flat fee
instead. If it stops you overpaying by S$30k, the maths is obvious. See the method for S$290 before
you pay the full fee.

**provenance:**
```yaml
source_phrase_id: null   # add to research-pool.json
source_quote: "The 'free' agent isn't free. The commission is baked into the price. You're paying, you just can't see it."
source_url: "00_inputs/research/voc-reddit-dump-260611.md#quote-16 (FICTIONAL r/singaporefi)"
competitor_weakness_addressed: "Commission agents trade on the word 'free'; this ad makes the hidden cost visible and reframes a flat fee as the cheaper, honest line item — the exact frame that converts the fee-allergic skeptic."
```

---

> Phrase-exclusivity check (SKILL.md §6): `research-pool.json` does not exist for this fictional
> client, so no `claimed_by_client` collisions are possible. All three source phrases are unclaimed.
> Operator should populate `research-pool.json` during the `/ads:source-of-truth` Phase 5 pool update.
