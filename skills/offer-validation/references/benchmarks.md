# Benchmarks Cheatsheet (reading results)

Source: georgeten.com/materials/cheatsheet-benchmarks.html
Read after 48 hours, in this order. Stop at the first level that answers the question.

## Reading order

1. **Purchases** — 3+ sales = validated. Scale it. Stop reading metrics. (3 → 30 → 300 → 3,000 as long as the market is big enough.)
2. **ATCs** — only if 0–2 purchases. ATCs without sales = problem between ATC and checkout (technical, too many checkout fields, missing payment options, price not near button). ~50% of intent ATCs convert to sale at scale → 2 ATCs ≈ 1 expected purchase.
3. **CTRs** — only if zero ATCs. Diagnoses ad vs page failure.

## CTR All (any click on the ad)

| CTR All | Signal | Action |
|---|---|---|
| <7% | Bad hook | Fix image + first line of copy before judging anything downstream |
| 7% | Minimum | Keep watching |
| 8%+ | Strong demand | Hook works. Move down the funnel |

## CTR Link — the 40% rule

CTR Link ÷ CTR All should be ≈40%. Example: 3.77 ÷ 9.3 = 40.5%.

| Ratio | Signal | Action |
|---|---|---|
| Way under 40% (e.g. <30%) | Hook worked, offer didn't | CTA/offer presentation isn't pulling |
| ~40% (35%+ OK) | Offer landing | Real qualified traffic flowing |
| Way over 40% | Confusion/curiosity clicks, NOT intent | They don't understand what's being sold. These clicks never convert. Make copy clearer |

Wait for ~33 link clicks before firm conclusions.

## Click-to-ATC rate (Microsoft Clarity, mobile only)

Visitors who clicked ATC ÷ visitors who REACHED the button.

| Rate | Signal |
|---|---|
| <10% | Offer or price problem |
| 10–15% | Page working |
| 15–20%+ | Converting hard |

Day 1: 15%+ possible and good. Day 2–3: aim 10%+ (warm audience exhausts). Click→ATC of ~15% on day 1 with ~50% ATC→purchase ≈ 7% purchase rate day 1.

## Quick diagnosis table

| Symptom | Likely cause |
|---|---|
| ATCs, no sales | Technical/checkout problem (fields, payments, broken flow) |
| Good CTRs, no ATCs | Page problem → run heatmap-analytics checklist |
| CTR All good, CTR Link <30% of All | Offer/CTA presentation problem |
| CTR Link ≫40% of All | Confusion clicks — clarify the ad copy |

## Confirm across two sources

Meta Pixel (ATC + IC events) vs platform checkout views vs Clarity button clicks. Two sources minimum; big disagreement = one is wrong (usually pixel).
