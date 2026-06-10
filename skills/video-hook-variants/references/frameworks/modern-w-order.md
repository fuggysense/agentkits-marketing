# Modern W Order

Lead with **What + Why** the viewer should care. Defer **Who + How** to beat 2. Drop **Where + When** entirely (or save for end-card).

## The Rule

The traditional journalism W's (Who, What, When, Where, Why, How) are ordered for comprehension. For hook writing, that order is wrong. Viewers make opt-in decisions in ~0.5 seconds.

**Modern W Order for hooks:**
1. **What** — the topic. What is this video about?
2. **Why** — why should this viewer care? Stakes, relevance, curiosity.
3. **Who** — deferred to beat 2. Credentials, context, actor framing.
4. **How** — deferred to beat 2 or 3. Mechanism, process.
5. **Where + When** — dropped or end-card only. Geographic and temporal anchors are irrelevance signals.

## Pass / Fail Examples

| Hook | Verdict | Reason |
|---|---|---|
| "Same body, same number, two different answers." | Pass | What (same result) + Why (something's wrong) first |
| "In a clinic in San Francisco last March, a woman…" | Fail | Where + When first = immediate scroll |
| "This is how my bosses left their stable jobs." | Pass | What (leaving jobs) + implied Why (it's a surprise) |
| "A year-three media student who interned at…" | Fail | Who (credentials) first = delayed topic, irrelevance risk |

## W-Order Compliance Check

Before locking a variant:
- Does the first word or phrase establish WHAT the video is about?
- Is there a Why signal (contrast, stakes, curiosity gap) in the first 2 seconds?
- Have you deferred geographic/temporal anchors?

Record in output:
```json
"w_order_compliant": true
```

If false → redraft the verbal layer before proceeding.
