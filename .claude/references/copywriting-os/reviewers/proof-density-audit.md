# Proof Density Audit — Post-Write Reviewer (sub-agent)

**Source:** Mark Masters, "Add Undeniable & Convincing Proof In Your Copy (with AI)" (cai #38).

**Core principle:** "Every claim without proof is a leak in your conversion bucket." Amateur copy = 1-2 testimonials and done. Professional copy = 6 distinct proof types, strategically layered.

**Agent model:** Sub-agent. Receives the draft + `clients/<slug>/copy-system/proof-inventory.md` (if exists).

## The 6 Proof Types

1. **Social** — testimonials, case studies, user counts, reviews, logos of users
2. **Credentials** — authority markers (degrees, years in industry, media mentions, awards, featured-in)
3. **Demonstration** — screenshots, video walkthroughs, before/after, live examples, product shots that show the actual experience
4. **Logical** — if-then reasoning, mechanism explained, analogy that makes the claim inevitable ("Because X, therefore Y")
5. **Specificity** — concrete numbers, exact processes, precise timeframes. *"14.3 hours per week"* beats *"a lot of hours"*. *"$297"* beats *"affordable"*. *"Week 3"* beats *"quickly"*. Specificity implies measurement implies truth.
6. **Implied** — proof embedded in HOW you communicate: confidence, detail depth, calm refusal to oversell. Tone as proof.

## Procedure

### Step 1 — Extract major claims

A "major claim" is anything that asks the reader to believe something non-obvious about: outcome, speed, capability, differentiation, risk-elimination, or mechanism.

Parse the draft and list every major claim with line reference.

### Step 2 — Tag proof type(s) for each claim

For each claim, identify which of the 6 proof types support it IN-COPY (not just in the operator's head — it must actually appear near the claim in the draft).

### Step 3 — Compute metrics

- **Density:** (claims with ≥1 proof) / (total major claims) × 100%
- **Type coverage:** which of 6 proof types appear anywhere in the draft
- **Leaks:** claims with ZERO proof types attached

### Step 4 — Cross-check against proof inventory

If `clients/<slug>/copy-system/proof-inventory.md` exists, check: is there available proof for any of the leaking claims that wasn't used? List those.

## Output schema

```
## PROOF DENSITY AUDIT
Total major claims in draft: N
Claims with ≥1 proof: M
Density: M/N × 100 = X%
Claims without proof (LEAKS): N-M

Leaks:
1. "<claim>" — line X — NO PROOF. Suggested proof type: <type>. Available from inventory: <yes/no, what>
2. ...

Proof type coverage (of 6):
- [ ] Social — used <N> times
- [ ] Credentials — used <N> times
- [ ] Demonstration — used <N> times
- [ ] Logical — used <N> times
- [ ] Specificity — used <N> times
- [ ] Implied — used <N> times

Types present: <N>/6

Verdict: PASS (density ≥ 80% AND types ≥ 4/6) / FAIL

Top 3 specific revisions (exact rewrites, not abstract):
1. Line X — current: "<copy>" → suggested: "<copy with specific proof>"
2. ...
3. ...
```

## Failure thresholds

- Density < 80% → FAIL
- Fewer than 4 of 6 proof types present → FAIL
- Any claim about outcome / guarantee / mechanism without proof → auto-FAIL regardless of density

## The two cheap wins to look for first

1. **Specificity wins** — any round number in the draft ("10x", "2x", "5 ways", "thousands") is a red flag. Push to exact number.
2. **Logical wins** — any outcome claim without a stated mechanism ("saves time" without saying HOW it saves time) needs the mechanism.

## Logging

Append to `clients/<slug>/copy-system/quality-gates/proof-density-log.md`:
`| YYMMDD-HHMM | output file | claims N | with-proof M | density % | types present N/6 | verdict |`
