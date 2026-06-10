# Step 10 — gate: the four-check on the top-3 headlines + top-3 extraction

> FICTIONAL SMOKE-TEST DATA - not a real client. EMULATED. Logged gate. The four-check asks of each
> finalist: (1) does it hit a TOP-3 pain, (2) is it in the buyer's own words, (3) is it concrete (not
> a saturated slogan), (4) does it pass the chills test for this persona.

## Top-3 extracted (structured_output equivalent)

```json
{
  "top_3": [
    "Your agent sold your flat in three weeks. Notice how quiet they went when you started buying?",
    "On the buy side, your agent earns more when you spend more. That's the whole problem.",
    "The 'free' property agent isn't free. The cost is just hidden in the price."
  ]
}
```

## Four-check

| headline | TOP-3 pain? | buyer's words? | concrete (not slogan)? | chills test? | verdict |
|----------|-------------|----------------|------------------------|--------------|---------|
| H1 (incentive flip, recognition) | Yes — TRUST, the dominant wound | Yes — VoC quote 3 near-verbatim | Yes — specific lived moment | Yes — MP-01 has felt this exactly | PASS |
| H2 (earns more when you spend more) | Yes — TRUST + OVERPAY-FEAR | Yes — buyer-truth line | Yes — names the mechanism | Yes for MP-03/MP-01 | PASS |
| H3 (free isn't free) | Yes — the fee illusion blocking MP-03 | Yes — VoC quote 16 | Yes — hidden-cost specific | Yes for MP-03 | PASS |

All three clear the four-check. No ⚠️ on the finalists. The step-06 caveat (stay concrete, avoid the
"no conflict of interest" slogan) is satisfied — none of the top 3 retreat to the abstract claim.

Gate: **PASS.**
