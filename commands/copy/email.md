---
description: Generate an email or email sequence (welcome / nurture / sales / re-engagement) with copywriting-OS gates wrapped around the existing email-sequence skill. Invoke via `/copy email <client-slug> [sequence-type]`.
version: "0.1.0"
brand: AgentKits Marketing by AityTech
argument-hint: <client-slug> [sequence-type: welcome | nurture | sales | re-engage | single]
---

## What this does

Wraps `skills/email-sequence/` + `skills/email-marketing/` with copywriting-OS gates + reviewers. Supports both single emails and sequences.

## Mark Masters's 4-day sales sequence voice rules (from cai #40 — apply as hard constraints)

- **One person to one person** — not a brand talking to a list
- **Short paragraphs** — 1-3 sentences max
- **Reader's language** — "getting more clients" not "scaling your customer acquisition pipeline"
- **Under 2 min on phone screen**
- **No fake urgency** — if no deadline exists, don't invent one; use a different closing angle
- **Subject lines** — short, specific, openable between meetings; not clever for clever's sake

## Step 1 — Shared context

See `commands/copy.md` Step 2.

## Step 2 — Pre-write gates

Same 3 gates as `/copy:sales-letter`:
1. `gates/channeling-check.md` — existing desire + reader's internal conversation
2. `gates/coat-of-arms-generator.md` — Halbert portrait
3. `gates/one-person-seed.md` — writer instruction injection

## Step 3 — Resolve sequence type + emotional progression

If `$2` is a sequence type (welcome / nurture / sales / re-engage), map to the 6 emotional states (cai #37) across the emails:

- **Welcome (4-5 emails):** Email 1 = Indifference→Pain; Email 2 = Pain→Understanding; Email 3 = Hope; Email 4 = Belief; Email 5 = Desire (first offer)
- **Nurture (4-6 emails):** Slower progression; Email 1-2 Pain, Email 3-4 Understanding→Hope, Email 5 Belief, Email 6 Desire
- **Sales (4 emails, cai #40 template):** Day 1 = Indifference→Pain (open conversation); Day 2 = Pain→Understanding→Hope; Day 3 = Belief; Day 4 = Desire (close)
- **Re-engage (3 emails):** Email 1 = acknowledge absence (Pain of what they're missing); Email 2 = Hope + new angle; Email 3 = Belief + Desire (offer to return)
- **Single email:** depends on the purpose; most will cover Indifference→Pain→Hope→Desire in one message

Declare the progression before writing. Each email MUST be tagged with its emotional state.

## Step 4 — Delegate to existing skill

Use `/content:email` or `/sequence:<type>` (existing commands) with shared context + gates injected:

```
/content:email <slug> <sequence-type>
```

OR for specific sequences:
```
/sequence:welcome <slug>
/sequence:nurture <slug>
/sequence:re-engage <slug>
```

Sub-agent execution; main thread only sees final drafts.

## Step 5 — Post-write reviewers (fire in parallel as sub-agents)

5 sub-agents as per `/copy` parent. Email-specific tweaks:

1. **one-person-enforcement** — IMAGINED READER declaration required at end of EACH email (not just the sequence)
2. **proof-density-audit** — usually lower threshold for emails (≥60% density, ≥3/6 types); Mark Masters cai #38 was still strict but email density naturally lower than sales letters
3. **emotional-sequence-audit** — both ACROSS the sequence (Email 1→N in order) AND WITHIN each email (mini-arc)
4. **objection-coverage-audit** — coverage can span the full sequence, not every email; verify by end of sequence
5. **teardown-reviewer** — email element adaptation: Hero = subject line + preview text + first line; Lead = opening paragraph; Body = middle; Proof = any inline proof; CTA = close + PS

## Step 6 — Synthesize + revise

Same as `/copy:sales-letter` Step 5. Revision cycles ≤2.

## Step 7 — Ship + log

- **Output:** `clients/<slug>/copy-system/outputs/emails/<YYMMDD>-<sequence-name>/email-<N>.md` (one file per email)
- **Sequence metadata:** `clients/<slug>/copy-system/outputs/emails/<YYMMDD>-<sequence-name>/_meta.md` (emotional-state map, total word count, estimated read time)
- **Logs:** standard quality-gate logs
- **Learnings:** `skills/email-sequence/learnings.md` + `skills/email-marketing/learnings.md` + `clients/<slug>/learnings.md`

## Prerequisites

All `/copy` prerequisites PLUS:
- Sequence purpose clearly stated (if sequence; else purpose for single email)
- List segment identified (who receives this — must match an avatar)

## Related

- Underlying skills: `skills/email-sequence/`, `skills/email-marketing/`
- Existing commands wrapped: `commands/content/email.md`, `commands/sequence/*.md`
- Parent router: `commands/copy.md`
- Cai #40 voice rules (hard constraints): applied as output validator
