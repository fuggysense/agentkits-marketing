# Big Angle Spotter — Run Summary (hardened mode, EMULATED)

> FICTIONAL SMOKE-TEST DATA - not a real client. Client: Meridian Property Advisory (fictional).
> Run: 260611. Mode: hardened (threshold 4, min_pass_count 5). EMULATED — see `_run.log` for why the
> live 18-worker pipeline was not executed (no-spend rule) and proof the script CAN run headless
> (clean `--dry-run`, single live worker probe returned valid JSON).

## Gate log

| step | gate | verdict | note |
|------|------|---------|------|
| 02 | resonance (scored, code-decided) | **PASS** | 8/10 angles banked on loop 1 (need >=5). A07, A09 failed; held for audit. No regenerate loop. |
| 05 | top-angle confirm | **PASS** | A01 confirmed rank-1 (clean YES). |
| 06 | novelty / not-saturated | **PASS (note)** | Keep execution concrete; the abstract "no conflict of interest" slogan is saturated. Satisfied in top-3. |
| 10 | four-check on top-3 headlines | **PASS** | All 3 finalists clear pain / buyer-words / concrete / chills. |

No warning on any shipped finalist. The only note is the step-06 execution note, which downstream copy honours.

## Top angle

**A01 — The incentive flip** (MP-01 Repeat-Mistake Upgrader, Solution-Aware). The same agent who sold
the flat fast goes cold on the buy, because buy-side commission is lower. Name the flip; the flat fee
is the obvious fix. Spine of the whole set.

## Top-3 headlines (with provenance)

```yaml
- headline: "Your agent sold your flat in three weeks. Notice how quiet they went when you started buying?"
  provenance:
    source_phrase_id: null   # add to research-pool.json
    source_quote: "Sold our flat in 3 weeks, great. Now buying side and suddenly the same agent is much less helpful lol. Makes sense, less money for them on the buy."
    source_url: "00_inputs/research/voc-reddit-dump-260611.md#quote-3 (FICTIONAL)"
    competitor_weakness_addressed: "No commission agent names the buy-side incentive drop; this makes the felt experience explicit and offers the structural fix."

- headline: "On the buy side, your agent earns more when you spend more. That's the whole problem."
  provenance:
    source_phrase_id: null
    source_quote: "The whole game is rigged on the incentive. Fix the incentive and I'm in."
    source_url: "00_inputs/research/voc-reddit-dump-260611.md#quote-26 (FICTIONAL)"
    competitor_weakness_addressed: "No competitor (incl. 'honest agent' brands) can claim a fee identical regardless of price; this owns the only structure that removes the incentive."

- headline: "The 'free' property agent isn't free. The cost is just hidden in the price."
  provenance:
    source_phrase_id: null
    source_quote: "The 'free' agent isn't free. The commission is baked into the price. You're paying, you just can't see it."
    source_url: "00_inputs/research/voc-reddit-dump-260611.md#quote-16 (FICTIONAL)"
    competitor_weakness_addressed: "Commission agents trade on 'free'; this makes the hidden cost visible and reframes the flat fee as the cheaper, honest line item."
```

## Ad-prompt files

- `11_ad_prompts.md` — 3 ads (headline + ~150w primary + ~50w short + provenance), one per top-3 headline.
- `12_image_prompts.md` — 3 image-gen prompts (Midjourney / DALL-E 3 / Flux / Ideogram strings), one per ad.

## Step artifacts (open in order)

01_angles.md -> 02_gate_resonance.json -> 03_pruned.md -> 04_ranked_angles.md ->
05_gate_top_angle.md -> 06_gate_novelty.md -> 07_expansion.md -> 08_headlines.md ->
09_ranked_headlines.md -> 10_gate_four_check.md -> 11_ad_prompts.md -> 12_image_prompts.md.

## Hard reminders before any live use

- Every quote, stat, and proof point is FICTIONAL — must clear the claim gate first.
- Never imply Meridian is a licensed CEA agent or promise guaranteed gains. Contrast the model, not the people.
- source_phrase_id is null on all three — operator populates research-pool.json in /ads:source-of-truth Phase 5.
