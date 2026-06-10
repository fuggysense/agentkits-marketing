# Lego Bricks — Three-Layer Alignment

**The rule:** all three hook layers (Visual + Text + Verbal) must reinforce ONE idea per variant. Misaligned layers produce confusion. Confused viewers churn.

## The Three Layers

1. **Visual layer** — what's on screen. High motion, high color, high contrast where possible. The scroll-stopper.
2. **Text layer** — 3–5 bold rendered words on-frame within 0:00–0:02. Establishes context visually before VO catches up.
3. **Verbal layer** — the VO or dialogue line. Active voice, ≤14 words, hard down-tone ending.

## Alignment Examples

**Aligned (pass):**
> Visual: open cabinet, full pill bottle untouched.
> Text: "You didn't fail iron."
> VO: "The bottle hasn't moved in six months."
> → All three point at format-failure reframe. One idea.

**Misaligned (reject):**
> Visual: two clinics side by side.
> Text: "Same test, different lab."
> VO: "Your results depend on who you ask."
> → Visual says geography, text says lab comparison, VO says provider trust. Three ideas. Confused viewer.

## Alignment Audit

For every variant, write a one-line `lego_brick_alignment` statement:
> "Visual: [X]. Text: '[Y].' VO: '[Z].' — all three point at [one idea]."

If you cannot write a single coherent one-idea statement, the layers are misaligned. Redraft before proceeding.

## The Visual-Supplement-Verbal Trick

If the VO line is solid but not viral on its own, compensate with a dominant visual or text layer.

- "400 slices of bread" → absurd visual so extreme that a plain VO works.
- "dream car" reference ad → needed a cash stack in frame 1 to supplement the okay VO (it didn't — that's why it underperformed).

Rule of thumb: ONE layer carrying the hook strongly is sufficient if the others stay aligned. Do not force three equally strong layers — that often produces three medium layers and a confused viewer.

## Output Field

In `hook-variants-draft.json`, record per variant:
```json
"lego_brick_alignment": "Visual: [shot]. Text: '[words].' VO: '[line].' — all three point at [one idea]."
```
