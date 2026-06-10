# Forbidden Content Audit — Post-Write Reviewer (sub-agent)

**Source:** Phase B anti-hallucination layer (internal). Integrates unslop/overused-ai-patterns Layer 2, client learnings, brand-voice files, and angle iteration logs.

**Core principle:** Every client has language, angles, and framings that are off-limits — spent angles, voice violations, legal tripwires, and hard-sell phrases the client has explicitly rejected. Generic AI-tell patterns compound the problem by flattening voice even when no client-specific rule is broken. A single compliance slip or a re-used burned angle can collapse trust or waste a DCT wave.

**Agent model:** Sub-agent. Fires as Phase B reviewer (alongside `claim-verification-audit`, `specificity-audit`, `buyer-language-fidelity-audit`). A FAIL here blocks shipment regardless of Phase C scores.

## Inputs

| Source | Required | Used for |
|--------|----------|---------|
| Draft under review | Yes | Primary scan target |
| `clients/<slug>/learnings.md` | If exists | F1 banned phrases, F6 hard-sell flags |
| `clients/<slug>/CLAUDE.md` | If exists | F5 legal/compliance constraints |
| `clients/<slug>/angles/iteration-log.md` | If exists | F2 saturated angle detection |
| `clients/<slug>/brand-voice.md` | If exists | F3 voice-rule extraction |
| `voice/<person>/brand-voice.md` | If applicable | F3 personal voice rules (Jerel-specific if copy is authored in his voice) |
| `skills/unslop/profiles/<content-type>.md` | If exists | F4 domain-specific AI-tell patterns |

## The 6 Forbidden Categories

**F1 — Client-specific banned phrases.** Exact strings or near-matches pulled from `learnings.md` entries tagged "do not use", "avoid", or "banned". Examples: a client who burned "pain points" across every email; a phrase rejected after user feedback.

**F2 — Saturated angles.** Angle names or thematic cores already deployed in prior DCT waves (read from `iteration-log.md`). Re-using a saturated angle as a *primary* theme wastes ad spend and signals creative fatigue to the algorithm.

**F3 — Brand-voice violations.** Tone or register mismatches against `brand-voice.md` rules. Examples: using "investment" for a client who sells consulting (not finance); "rockstar" for a brand with formal register; "revolutionary" for a client who codes humility as a brand pillar.

**F4 — AI-tell patterns.** Generic LLM defaults that flatten voice. Minimum detection list (augment with unslop profile if available):
1. "not X, not Y, but Z" triplet structure
2. "in today's fast-paced world"
3. "in the world of [noun]"
4. "at the end of the day"
5. "whether you're X or Y" structure
6. "game-changer" / "game changer"
7. "unlock your [noun]"
8. "seamlessly"
9. "leverage" (as generic verb, not technical)
10. "it's not just about X, it's about Y"
11. Em-dash count > 3 per 1000 words
12. "dive into" / "delve into"
13. "journey" as metaphor for product use
14. Consecutive sentences starting with "And" or "But" (≥ 3 instances)
15. Emoji placed as section headers (🔥 **Section Title**)

**F5 — Legal/compliance words.** Terms flagged in `clients/<slug>/CLAUDE.md` for regulated verticals. Examples: "guaranteed returns" for financial services; "cure" or "treat" for wellness/supplement brands; "no risk" without qualifying language.

**F6 — Hard-sell language the client has rejected.** Phrases the client has explicitly flagged as off-brand pressure tactics. Examples: "act now", "don't miss out", "limited time offer", "spots are filling fast" — if the client's learnings.md or CLAUDE.md records an objection to high-pressure tactics.

## Severity Rules

| Severity | Trigger | Consequence |
|----------|---------|-------------|
| CRITICAL | F1 banned phrase match OR F5 compliance violation | Auto-FAIL. No operator override. Rewrite required before re-review. |
| HIGH | F2 saturated angle re-used as primary theme | FAIL pending operator confirm. Operator may override with explicit note if deliberate re-test. |
| MEDIUM | F3 voice drift OR F6 hard-sell drift | Flag with rewrite suggestion. Does not auto-fail alone; accumulation fails (see thresholds). |
| LOW | F4 AI-tell pattern | Flag, must be resolved before ship but not independently blocking. |

## Procedure

### Step 1 — Load and categorise all forbidden-content sources

Read each input file in the order listed above. Extract:
- F1: every "do not use" / "avoid" / "banned" phrase from `learnings.md`
- F2: every angle name/theme from `iteration-log.md` (column: angle, status: used/winner/loser)
- F3: voice rules from `brand-voice.md` (register constraints, banned adjectives, tone mandates)
- F4: the 15-pattern list above, plus any additions from the unslop profile
- F5: legal flags from `clients/<slug>/CLAUDE.md` (look for "compliance", "legal", "do not claim")
- F6: hard-sell flags from `learnings.md` (look for "pressure", "urgency", "avoid hard-sell")

Build a flat lookup table per category before scanning begins.

### Step 2 — Scan the draft line by line against each category

Process F1 first (exact string match, case-insensitive). Then F5 (exact + proximity — flag the sentence, not just the word). Then F2 (thematic scan — identify the primary angle of the draft's hook and mechanism, compare against burned angle names). Then F3, F6 (register/tone read, paragraph-level). Then F4 (pattern matching across full draft).

### Step 3 — F4 AI-tell pass

Apply all 15 patterns. For em-dash (pattern 11): count total em-dashes, divide by word count × 1000. Flag if rate exceeds 3 per 1000 words.

If a domain-specific unslop profile exists, append its pattern list to the F4 check and run both sets.

### Step 4 — Record each hit

For every match: category (F1–F6), severity (CRITICAL / HIGH / MEDIUM / LOW), draft line number, offending phrase (quoted exactly), rewrite suggestion (one sentence, concrete).

### Step 5 — Compute violation counts

Total violations per category. Total CRITICAL count. Total HIGH count. Total MEDIUM count. Total LOW count. AI-tell density = (F4 violations) / (total word count) × 1000.

### Step 6 — Emit output schema

Produce the structured report below.

## Output Schema

```
## FORBIDDEN CONTENT AUDIT

Violation counts:
F1 Client-banned phrases:     N
F2 Saturated angles:          N
F3 Brand-voice violations:    N
F4 AI-tell patterns:          N
F5 Legal/compliance:          N
F6 Hard-sell flags:           N
Total:                        N

Violations (ordered by severity):

CRITICAL
1. F1 | Line X — "<offending phrase>" — matches learnings.md entry: "<exact ban record>"
   Rewrite: "<suggested replacement>"

2. F5 | Line X — "<offending phrase>" — compliance flag: "<source in CLAUDE.md>"
   Rewrite: "<suggested replacement>"

HIGH
3. F2 | Primary angle "<angle name>" — matches burned angle from iteration-log.md wave N (status: <winner/loser>)
   Operator override required to proceed. Confirm intentional re-test or select new angle.

MEDIUM
4. F3 | Line X — "<phrase>" — voice violation: brand-voice.md rule: "<rule>"
   Rewrite: "<suggested replacement>"

LOW
5. F4 | Line X — "<pattern name>" — "<offending phrase>"
   Rewrite: "<suggested replacement>"

Saturated-angle check:
Burned angles on file: ["angle A (wave 1, loser)", "angle B (wave 2, winner)", ...]
Draft primary angle: "<detected angle>"
Verdict: NEW ANGLE / RE-USE (operator confirm required) / COLLISION (auto-block)

AI-tell density:
F4 violations: N
Draft word count: N
Density: N per 1000 words (threshold: < 2.0)

Verdict: PASS / FAIL
Reason: <one line — e.g., "1 CRITICAL (F5 compliance), AI-tell density 3.2/1000">

Blocking revisions required before re-review:
1. Line X — current: "<copy>" → required: "<clean version>"
2. ...
```

## Failure Thresholds

- Any CRITICAL violation → auto-FAIL (no override)
- Any HIGH violation without documented operator override flag → FAIL
- AI-tell density ≥ 2.0 per 1000 words → FAIL
- More than 3 MEDIUM violations → FAIL
- Any F5 hit in a regulated vertical → auto-FAIL regardless of other scores

## The Four Cheap Wins to Check First

1. **"Investment" scan** — if `brand-voice.md` or `context-profile.json` shows the client is not in finance or property, flag every instance of "investment", "portfolio", or "returns" as F3.
2. **Em-dash frequency** — count before full scan. If already > 3 per 1000 words, surface immediately and resolve before other F4 checks compound.
3. **Stock LinkedIn openers** — grep for "in today's", "in the world of", "at the end of the day" as first-pass F4 sweep. These appear in nearly every LLM first draft and are instant LOW flags.
4. **Triplet structure** — search for "whether you're X or Y" and "not X, not Y, but Z". One instance is borderline; two is a pattern; three is a template leak.

## Logging

Append to `clients/<slug>/copy-system/quality-gates/forbidden-content-log.md`:
`| YYMMDD-HHMM | output file | F1 N | F2 N | F3 N | F4 N | F5 N | F6 N | CRITICAL N | HIGH N | ai-tell density X.X/1000 | verdict |`
