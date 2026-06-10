# Three-Element Pre-flight Check

Agent-facing checklist for applying the Three Elements (Relatability / Sensationalism / Stakes) with claim_risk guardrails.

## Pre-flight Steps

1. Identify which elements the hook hits. Record in `elements_hit[]`.
2. If Sensationalism is present, validate every claim against `allowed_expressions` in concept-brief.json.
3. If claim_risk = high → treat Sensationalism as guarded. Prefer Relatability + Stakes combination instead.
4. Confirm differentiation axis: Hook A and Hook B must differ on ANGLE, not word choice.

## Element Definitions

### Relatability
- Universal experience the avatar lives: sensation, scenario, identity.
- Viewer's reaction: "that's me."
- Use "you/your" framing.
- Not "I/me" framing unless the creator's story is the anchor (then it must resolve into "you" within 3 seconds).

### Sensationalism
- Pattern interrupt, extreme contrast, status reversal.
- Huge numbers, extreme outcomes, impossible contrasts.
- CLAIM RISK WARNING: validate every sensational claim against `allowed_expressions`. A weaker hook beats a flagged one. Claim safety wins.
- When claim_risk = high: treat Sensationalism as guarded. Default to Relatability + Stakes.

### Stakes
- What's at risk if the viewer doesn't act or watch.
- Identity threat, loss frame, urgency, failure consequence.
- Stakes convert passive interest into active engagement.

## Differentiation Rule

Hook A and Hook B must differ on HOOK ANGLE — not just word choice.

| Acceptable differentiation | Same angle (reject) |
|---|---|
| A = stakes-led (identity threat); B = sensationalism-led (mechanism reveal) | A = "your hair is thinning"; B = "is your hair thinning" |
| A = relatability-led (avatar mirror); B = stakes-led (loss frame) | A = "you keep quitting"; B = "why do you keep quitting" |

## Output

```json
"elements_hit": ["relatability", "stakes"],
"contrast_axis": "Point A (she keeps failing iron) → Point B (the format failed her)"
```

Record `differentiation_axis` at the concept level:
```json
"differentiation_axis": "stakes-led identity-threat (A) vs sensationalism-led mechanism-reveal (B)"
```
