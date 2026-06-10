# Objection Coverage Audit — Post-Write Reviewer (sub-agent)

**Source:** Mark Masters, "Your Copy Is Leaking Money" (cai #36, 30-min issue).

**Core principle:** "$997 product vs $297-497 competitors, unhandled price objection → 0.3% conversion, $23K wasted ad spend. Rewrote with systematic objection handling throughout → 3.2%. Same traffic, same offer, same price." Every unhandled objection is a leak.

**Agent model:** Sub-agent. Receives the draft + `clients/<slug>/copy-system/objection-matrix.md` (client-specific objection language if populated).

## The 6 Categories

Categories 1, 2, 3, 5 fully confirmed from cai #36 preview. Categories 4 + 6 marked **[TBD: confirm against full-body read of cai #36 in Phase 4.2]** — placeholders below are sensible defaults; do not trust until verified.

### 1. Price — "This costs too much"
Variations: "too expensive", "can't afford right now", "seen similar for less", "price doesn't match value", "need to wait until I have more money", "vs [competitor]", "can I get a discount", "what if it doesn't work — wasted money", "can't justify to spouse/partner", "payment plan still too much monthly"
**Handlers:** price anchoring vs higher alternatives • ROI calc showing cost vs value gained • cost-of-inaction framing • payment plan positioning • daily/weekly equivalents ("$1.32/day") • investment-vs-expense reframe

### 2. Timing — "Not right now"
Variations: "I'll do this later", "now isn't a good time", "too busy to start something new", "after [event/season/quarter]", "need to finish X first", "let me think about it", "more research first", "not ready yet", "maybe next month/quarter/year", "too much on my plate"
**Handlers:** future pacing cost of delay • "perfect timing" myth destruction • quick-start positioning • implementation timeline clarity • "waiting makes it harder" framing • urgency via scarcity or deadline • immediate small win demonstration

### 3. Trust — "How do I know this works?"
Variations: "who are you", "is this a scam", "sounds too good to be true", "I've been burned before", "don't know this company", "need more reviews", "competitors I know are cheaper/slower"
**Handlers:** founder/origin story • money-back guarantee • proof stacking (see `reviewers/proof-density-audit.md` — all 6 types) • specificity (see same) • third-party validation • case-study detail with names + numbers

### 4. Fit / Need — "This isn't for my situation" **[TBD confirm]**
Variations: "my case is different", "industry-specific requirements", "I tried something similar and it didn't work", "what if my team/product/customer is different", "I'm at a different stage"
**Handlers:** specific case-study with their vertical • "the principle works in X industry because Y" • carve-out ("this isn't for people who...") • mechanism translation to their context

### 5. Authority — "I can't decide alone"
Variations: "need to ask my spouse/partner", "have to run this by my boss", "business partner handles this", "check with my team", "discuss with my accountant/advisor", "affects more than just me", "don't make purchasing decisions", "need approval for this amount", "stakeholder wouldn't approve", "present to the board first"
**Handlers:** shareable summary creation • stakeholder objection anticipation ("here's what your spouse/boss/board will ask") • decision-maker-specific benefits • "how to pitch this to your [stakeholder]" content • money-back guarantee for "permission" safety • testimonials from similar decision dynamics ("a CFO who was skeptical") • ROI documentation for approval processes

### 6. Skepticism / Urgency-mechanism — "Why now? Does this actually work?" **[TBD confirm]**
Variations: "I'll wait to see if it pans out", "why this approach when X has worked for years", "every company says they're different", "prove the mechanism", "industry is changing, why invest"
**Handlers:** mechanism proof (see `reviewers/proof-density-audit.md` Logical type) • why-now argument tied to external catalyst • competitor teardown showing WHY they fail • "this is what everyone will be doing in 18 months"

## Procedure

### Step 1 — Scan the draft for each category
For each of the 6, classify as:
- **ADDRESSED** (pre-emptively handled before reader thinks it OR reactively handled in FAQ/CTA/PS)
- **NOT ADDRESSED** (LEAK)
- **N/A with reason** (e.g., Authority for a $9/mo consumer product — reason required)

### Step 2 — Cross-check client-specific leaks
Load `objection-matrix.md` (if exists). Any verbatim objection listed there that isn't addressed in-copy → LEAK.

## Output schema

```
## OBJECTION COVERAGE AUDIT
Categories addressed: N/6 (+ client-specific matches)

Category by category:
1. Price — ADDRESSED on line X via <handler> / NOT ADDRESSED / N/A (reason: ...)
2. Timing — <status>
3. Trust — <status>
4. Fit/Need — <status>
5. Authority — <status>
6. Skepticism — <status>

Client-specific leaks (from objection-matrix.md):
- "<exact client-phrased objection>" — NOT ADDRESSED / addressed on line X
- ...

Verdict: PASS (6/6 addressed or explicit N/A with reason, AND 0 client-specific leaks) / FAIL

Top 3 revisions (exact inserts):
1. Category <X> — inject near line <Y> — copy: "<exact handler draft>"
2. ...
```

## Explicit N/A rule

A category MAY be marked N/A, but the reviewer MUST state the reason. "N/A because..." is required. "N/A" alone = FAIL.

## Logging

Append to `clients/<slug>/copy-system/quality-gates/objection-coverage-log.md`:
`| YYMMDD-HHMM | output file | addressed N/6 | client-specific leaks N | verdict |`

## Phase 4.2 follow-up

Confirm categories 4 + 6 exact definitions against full-body read of cai #36. Update this file when verified.
