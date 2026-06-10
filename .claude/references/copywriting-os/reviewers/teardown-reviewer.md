# Teardown Reviewer — Post-Write Reviewer (sub-agent)

**Source:** Peggy Burnett, "The Worst AI Sales Page I Read This Month" (cai #45) + Mark Masters "Hidden AI Patterns in Emails, Revenue" (cai #26 — to be fully integrated in Phase 4.3).

**Core principle:** Walk the copy element by element (hero → lead → body → proof → CTA) and pattern-match against a named library of LLM-generated-copy failure modes. Most shipped LLM copy has ≥2 failures stacked.

**Agent model:** Sub-agent. Receives the draft. The failure-mode library is inlined below in this file (no external dependency). Phase 4.3 will expand it with email-specific patterns from cai #26.

## Element structure expected in the draft

The reviewer parses the draft into 5 elements:
- **Hero** — headline + subhead (first visual unit)
- **Lead** — opening 2-4 paragraphs that sets up the problem
- **Body** — mechanism / solution / benefit section
- **Proof** — testimonials, case studies, credentials, demonstrations block
- **CTA** — the ask (button + surrounding copy + PS)

If the draft doesn't have clear element breaks (e.g., a short email), adapt: Hero = subject line + opening line, Lead = body start, Body = middle, Proof = any proof element inline, CTA = closing ask.

## Failure Mode Library (seed — expand in Phase 4.3)

### Hero section failures

- **H1 — "Transform class" filler verb** — "transform", "elevate", "unlock", "revolutionize", "empower" used without a specific named measurable outcome attached. Claude reaches for these when it doesn't know what the product actually does. ❌ *"Transform Your Booking Experience"* ✅ *"Cut your Friday hours spent on invoice follow-ups from 3 to zero"*
- **H2 — Category-speak** — how a PM writes in a user story, not how the buyer thinks. ❌ *"Scheduling Solution"* ✅ (whatever the buyer actually calls it when they complain about it at 10pm)
- **H3 — Uncommitted superlative stack** — "ultimate all-in-one", "best-in-class premier", "world's leading". Skepticism magnet.
- **H4 — Abstract benefit promise** — "Scale your business", "Grow faster", "Drive results". No named mechanism, no named outcome.

### Lead section failures

- **L1 — Product-first opening** — describes the tool / company / offer before the reader's world. Violates channeling-check.
- **L2 — "Imagine" opening** — *"Imagine if you could..."*, *"Picture a world where..."*. Creating desire, not channeling.
- **L3 — Generic empathy** — *"You're tired of..."*, *"You've tried everything..."* without specific evidence. Reader sees stock template.

### Body failures

- **B1 — Feature list disguised as benefits** — each "benefit" starts with a feature noun rather than a buyer outcome.
- **B2 — Round numbers everywhere** — "10x faster", "2x more leads", "5 ways to win". Round numbers signal no measurement.
- **B3 — "Imagine how much time you'd save"** — no specific number, no specific activity named.
- **B4 — Corporate verbs** — "leverage", "optimize", "streamline", "synergize". Stock LLM defaults.

### Proof failures

- **P1 — Single stock testimonial** — *"This changed my life. — Sarah M."* No role, no result, no mechanism.
- **P2 — Credentials without context** — *"15 years experience"* or *"Featured in major publications"*. No specific publication, no specific claim earned.
- **P3 — Generic user count** — *"Thousands of happy customers"*. No named company, no industry, no outcome.
- **P4 — Testimonial that doesn't address any objection** — proof exists but doesn't refute a specific doubt the reader has.

### CTA failures

- **C1 — Generic button copy** — "Get Started", "Learn More", "Click Here", "Sign Up Now". No implied outcome.
- **C2 — CTA that describes the action, not the reward** — "Subscribe to Newsletter" vs "Get tomorrow's idea in your inbox".
- **C3 — Fake urgency** — "Only 3 spots left" when there aren't, "Ends tonight" when it doesn't. Violates cai #40 voice rule ("No fake urgency. If there's no deadline, don't invent one.").
- **C4 — CTA buried or single** — no secondary CTA near bottom, or only 1 CTA in long-form copy.

## Procedure

### Step 1 — Parse elements
Split draft into Hero / Lead / Body / Proof / CTA.

### Step 2 — Test each element against its sub-library
For each element, iterate through its failure modes. Flag every hit with line + mode ID + exact offending phrase.

### Step 3 — Mark criticals
Some failures auto-FAIL regardless of count:
- H1 "transform" without specific outcome
- L2 "imagine" opening
- P1 stock testimonial
- C3 fake urgency
Any of these = critical FAIL.

## Output schema

```
## TEARDOWN REPORT
Element pass/fail:
- Hero: PASS / FAIL — failure modes hit: <list IDs>
- Lead: <status>
- Body: <status>
- Proof: <status>
- CTA: <status>

Detailed failures (one per hit):
1. HERO H1 — line <X> — "<offending phrase>"
   Suggested rewrite: "<specific replacement>"
2. ...

Critical failures: <N> (any = auto-FAIL regardless of count)
Total failure modes hit: <N>

Verdict: PASS (0 criticals AND ≤1 failure per element) / FAIL

Top 3 critical revisions:
1. Element <X> — current: "<copy>" → suggested: "<specific rewrite>"
2. ...
3. ...
```

## Failure thresholds

- Any element with > 1 failure mode → FAIL
- Any critical failure (H1 / L2 / P1 / C3) → auto-FAIL
- 0 criticals AND all elements ≤1 failure → PASS

## Logging

Append to `clients/<slug>/copy-system/quality-gates/teardown-log.md`:
`| YYMMDD-HHMM | output file | Hero pass Y/N | Lead Y/N | Body Y/N | Proof Y/N | CTA Y/N | criticals N | verdict |`

## Phase 4.3 follow-up

Full-read cai #26 "Hidden AI Patterns in Emails, Revenue" to expand the failure-mode library with email-specific patterns (subject line failures, preview-text failures, opening-line traps).
