---
description: Generate a long-form direct-response sales letter for cold paid traffic with all copywriting-OS gates + reviewers wrapped around the existing sales-letter-method pipeline. Invoke via `/copy sales-letter <client-slug>` or `/copy:sales-letter <client-slug>`.
version: "0.1.0"
brand: AgentKits Marketing by AityTech
argument-hint: <client-slug> [optional: avatar name if >1]
---

## What this does

Wraps the existing `skills/sales-letter-method/` pipeline (5 phases, 12-component framework) with copywriting-OS pre-write gates and post-write reviewers. Delegates the heavy writing to the domain skill; this command owns only the gate + reviewer orchestration.

## Step 1 — Shared context (from `/copy` parent)

Already loaded if this came from `/copy sales-letter`. If invoked directly, run `/copy` shared-context loader (see `commands/copy.md` Step 2). Required:
- `clients/<slug>/context-profile.json`
- `clients/<slug>/copy-system/copy-brief.md` (generate if missing)
- `clients/<slug>/_brand/offer.md`, `_brand/buyer-profile.md`, `_brand/avatars/<avatar>.md`
- `voice/<person>/brand-voice.md` OR `clients/<slug>/_brand/brand-voice.md`

## Step 2 — Pre-write gates (run in order; HITL on fail)

1. **Channeling Check** — load `.claude/references/copywriting-os/gates/channeling-check.md`. Require the writer to declare the existing desire + evidence + reader's internal conversation before any copy is generated.
2. **Coat of Arms** — load `.claude/references/copywriting-os/gates/coat-of-arms-generator.md`. Load or generate `clients/<slug>/copy-system/coat-of-arms-<avatar>.md`.
3. **One-Person Seed** — load `.claude/references/copywriting-os/gates/one-person-seed.md`. Inject the "think of specific person + declare at end" instruction into the writer prompt.

## Step 3 — Delegate to existing `/content:sales-letter`

Invoke the existing command (all its internal phases — Context Scan, Parallel Drafters, Stitcher, Conversion Gate, Polish — run as before):

```
/content:sales-letter <slug> <optional offer focus>
```

Pass through the context-profile, offer, buyer-profile, avatars, voice as usual. **Inject the 3 pre-write gate specifications into Phase 0 Context Scan** so the drafters produce the required CHANNELING CHECK + IMAGINED READER blocks.

**Delegation target:** runs as sub-agent. Main thread only sees the completed draft.

## Step 2b — Pre-write grounding builders (fire in parallel as sub-agents)

Spawn 2 sub-agents before Step 3 delegates to the drafter. Each populates one grounding file that B1 / B4 reviewers depend on:

1. `builders/proof-inventory-builder.md` → writes `clients/<slug>/copy-system/proof-inventory.md`
2. `builders/objection-matrix-builder.md` → writes `clients/<slug>/copy-system/objection-matrix.md`

Skip if both files exist and are < 14 days old (unless operator requests refresh).

## Step 4 — Post-write reviewers (fire in parallel as sub-agents)

Spawn 9 sub-agents using `verification-loops` skill pattern, in two banks. Each receives the draft + one reviewer spec. Phase B failures strictly gate — resolve before Phase C.

**Phase B (anti-hallucination):**
1. `reviewers/claim-verification-audit.md` — every claim sourced to a grounding file; zero CRITICAL unsourced
2. `reviewers/forbidden-content-audit.md` — F1-F6 (banned phrases / saturated angles / voice drift / AI-tell / compliance / hard-sell)
3. `reviewers/specificity-audit.md` — weasel density < 4 per 1000 words; CRITICAL on vague headlines with available numbers
4. `reviewers/buyer-language-fidelity-audit.md` — verbatim-match quotes, register-drift scoring on paraphrases

**Phase C (persuasion craft):**
5. `reviewers/one-person-enforcement.md` — verify IMAGINED READER block is specific
6. `reviewers/proof-density-audit.md` — ≥80% density, ≥4/6 proof types
7. `reviewers/emotional-sequence-audit.md` — 6 states in order, no skips
8. `reviewers/objection-coverage-audit.md` — 6 categories addressed or explicit N/A
9. `reviewers/teardown-reviewer.md` — element-by-element (hero / lead / body / proof / CTA)

Existing `sales-letter-method` Phase 3 reviewers (buyer-lens + copy-chief + self-contained) ALSO fire. Total 12-reviewer stack.

## Step 5 — Synthesize + revise

Consolidate all reviewer verdicts into a single Priority Fix Stack:
- Criticals (any auto-FAIL from any reviewer) first
- Then high-impact (proof-density gaps, emotional skips, element-level failures)
- Then nice-to-haves

Run ≤2 revision cycles. After each revision, re-fire the relevant reviewer sub-agents. Escalate to operator (HITL) if still failing after 2 cycles.

## Step 6 — Ship + log

- **Output:** `clients/<slug>/sales-letters/<YYMMDD>-v<n>.md` (inherited from the `/content:sales-letter` engine — revisions auto-increment the version; do NOT re-declare a separate `copy-system/outputs/` path or the letter lands in two places)
- **Rendered HTML (optional):** `clients/<slug>/sales-letters/<YYMMDD>-v<n>-rendered/index.html` (if the sales-letter-method renderer is invoked)
- **Quality gate logs:** append one row each to the 5 reviewer log files in `clients/<slug>/copy-system/quality-gates/`
- **Run manifest:** append to `clients/<slug>/copy-system/quality-gates/runs.md`
- **Learnings:** append to `skills/sales-letter-method/learnings.md` + `clients/<slug>/learnings.md`

## Prerequisites

All `/copy` prerequisites (see `commands/copy.md`) PLUS:
- Offer has a guarantee mechanic defined (or flagged for HITL in Phase 0)
- Mass desire + Schwartz awareness level identified in `context-profile.json` or `source-of-truth.md`

## Related

- Underlying skill: `skills/sales-letter-method/`
- Existing command being wrapped: `commands/content/sales-letter.md`
- Gates + reviewers: `.claude/references/copywriting-os/`
- Parent router: `commands/copy.md`
