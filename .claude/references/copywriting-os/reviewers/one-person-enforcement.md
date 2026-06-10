# One-Person Enforcement — Post-Write Reviewer (sub-agent)

**Source:** Gary Halbert One-Person Rule (cai #44).

**Purpose:** Verify the writer actually wrote to a SPECIFIC person (not a persona or segment) by grading the IMAGINED READER declaration block.

**Agent model:** Runs as a sub-agent via verification-loops pattern. Main thread never loads this reviewer's body.

## Input to the sub-agent

- The final draft (including the required IMAGINED READER block)
- `clients/<slug>/copy-system/coat-of-arms-<avatar>.md` (for cross-checking specifics)

## Procedure

### Step 1 — Parse the IMAGINED READER block

If the block is MISSING from the draft → AUTO-FAIL. Return to writer with: "IMAGINED READER block missing. Cannot ship without declaration."

### Step 2 — Grade each field

Score each of 4 fields as SPECIFIC / GENERIC:

**Name** — SPECIFIC if a real first name that doesn't smell like a stock placeholder. Any of {Sarah, John, Mike, Jane, Bob, Alice} with no other distinguishing context → GENERIC. A less-common name (Priya, Fahmy, Devante, Mei) OR a common name with a distinguishing context (e.g. "Sarah, who still keeps her first business card pinned to the corkboard over her monitor") → SPECIFIC.

**Job / role** — SPECIFIC if it includes ≥2 of: (a) company-stage ("Series A", "12 employees", "family business 2nd generation"), (b) team position ("2nd marketing hire reporting to founder"), (c) seniority AND context ("Head of Growth" + who they report to), (d) industry AND sub-segment ("B2B SaaS selling to legal teams"). Plain titles ("marketing director", "copywriter", "founder", "business owner") → GENERIC.

**Moment** — SPECIFIC if it includes ≥3 of: (a) time of day, (b) physical location or setting, (c) what they're doing, (d) what they're feeling, (e) named external trigger (what app, what just happened). "Busy afternoon", "scrolling social", "in a meeting" → GENERIC.

**Coat-of-arms specifics** — SPECIFIC if ≥3 of the listed specifics actually appear in (or are cross-checkable against) `coat-of-arms-<avatar>.md`. Fabricated specifics → AUTO-FAIL.

### Step 3 — Verdict

- All 4 fields SPECIFIC → PASS
- Any 1 GENERIC → FAIL, return to writer

## Output schema (sub-agent returns to orchestrator)

```
## ONE-PERSON ENFORCEMENT VERDICT
Block present: YES / NO (if NO, auto-fail)
Field scores:
- Name: SPECIFIC / GENERIC — <quote the field>
- Job: SPECIFIC / GENERIC — <quote>
- Moment: SPECIFIC / GENERIC — <quote>
- Coat-of-arms specifics: SPECIFIC / GENERIC / FABRICATED — <list which specifics matched the coat, which didn't>

Verdict: PASS / FAIL

If FAIL, specific instruction back to writer:
- <name, job, moment, or specifics — which one(s) need fixing — plus example of what SPECIFIC looks like for this avatar>
```

## Logging

Append to `clients/<slug>/copy-system/quality-gates/one-person-log.md`:
`| YYMMDD-HHMM | output file | imagined name | job (SPECIFIC/GENERIC) | moment (SPECIFIC/GENERIC) | specifics N/5 matched coat | verdict |`

## Examples

**FAIL example:**
> Name: Sarah. Job: marketing manager. Moment: busy afternoon at her desk. Coat specifics I used: "frustrated with growth", "needs better ROI", "busy".

Reject: Name is stock, job is plain title, moment is vague, specifics are generic (and don't appear in the coat).

**PASS example:**
> Name: Priya. Job: Head of Growth at a 40-person Series A SaaS reporting to a founder who built the product and doesn't quite understand what she does. Moment: 7:45pm Tuesday, laptop open on the kitchen island, dinner warming in the microwave, second tab is a McKinsey report her founder just Slacked her with the message "thoughts?" Coat specifics I used: "reporting-to-non-marketing-founder anxiety", "2nd marketing hire", "reads First Round Review", "rolls eyes at 'scaling customer acquisition pipeline'", "won't admit wanting a clearer title".
