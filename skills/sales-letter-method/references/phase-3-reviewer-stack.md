---
file_type: phase-playbook
load_when: pipeline reaches Phase 3; user asks for a sales-letter review, "kill my babies on this letter", or "is this letter clear enough"; any standalone review of a sales letter
applies_to: 5-phase-pipeline (Phase 3)
last_updated: 2026-05-27
---

# Phase 3 — Conversion Gate (Five-Reviewer Stack)

## What this file teaches

Phase 3 is the make-or-break gate before polish. Five reviewer agents fire in parallel, in clean isolated contexts. None of them sees any other one's notes. If you skip any reviewer, the review is broken. This rule covers the full pipeline and any standalone request — "review this sales letter", "kill my babies on this letter", "is this letter clear enough." The five-reviewer stack is the single source of truth for every sales-letter review this skill handles.

## The five reviewers

- **Buyer Lens** (`reviewers/buyer-lens-reviewer.md`) — plays the real target buyer reading the letter for the first time. Reacts on first impression, relevance, trust, desire, friction, decision. No jargon.

- **Copy Chief** (`reviewers/copy-chief-reviewer.md`) — elite direct-response strategist working in a Schwartz-led lens. Goes section by section, names the diagnosis, lists priority fixes, suggests rewrites. Historically labelled "Schwartz / Ogilvy / Halbert combined" but runs about 80% Schwartz / 15% Ogilvy / 5% Halbert in practice. The Halbert voice critique is now owned by the eval-halbert reviewer below. Confirmed 2026-05-27 in a head-to-head test on `tests/v4-firsttime.md` (the neezanizam first-time letter).

- **Self-Contained Experience** (`reviewers/self-contained-reviewer.md`) — the kill-babies lens. Treats the page as a cold standalone read. Asks two questions: (1) Is the whole letter a complete argument a tired Singaporean reader can follow top to bottom? (2) How simple is the language — never make the reader feel "not okay." Outputs: Complete Argument Check, Structural Simplification, Language Simplification (line by line), "Not Okay" Flags, and The One Question.

- **eval-halbert** (subagent dispatch: `subagent_type=eval-halbert`, lives at `agents/eval-halbert.md`) — Gary Halbert persona voice critique. Returns a KILL IT / FIX IT / MAIL IT verdict in an 8-section format: starving crowd, deal, headline, opening, proof, close, weasel words, what's working, sign-off. Catches voice-level weasels like "properly", "full picture", "structural gap", "plain English" — words the Copy Chief tends to miss. Runs in a clean isolated context.

- **eval-sales-letter** (subagent dispatch: `subagent_type=eval-sales-letter`, lives at `agents/eval-sales-letter.md`) — structural audit that wraps the `skills/sales-letter-audit` skill. Returns SHIP / HOLD / REWRITE plus a 12-component map and ranked blockers. Cross-checks the draft against `_brand/offer.md`, `_brand/buyer-profile.md`, and `_brand/icp.md`. Catches mechanism naming conflicts, audience mismatches, and offer-spec mismatches — clashes that voice and strategy reviewers cannot see.

## The synthesizer

After all five reviewers return, the synthesizer maps:

buyer frictions → self-contained cuts and simplifications → chief diagnoses → eval-halbert voice / weasel flags → eval-sales-letter brand-doc conflicts → one proposed fix.

**Precedence order at the first pass:**

1. Brand-doc conflicts (eval-sales-letter) — these ship-block. Fix before anything else.
2. Structural cuts (self-contained)
3. Voice weasels (eval-halbert)
4. Clever additions (chief)
5. Buyer frictions (buyer-lens, for nuance)

The synthesizer outputs a **Priority Fix Stack** ranked by severity × ease-of-fix × simplification-alignment.

## Contract validation (merged in)

Every Phase 3 pass also checks the letter against the shipping contract:

- **GOAL:** opt-in rate must beat baseline × 1.5.
- **CONSTRAINTS:** voice match, offer accuracy, no AI patterns, no more than 9 movements, no unexplained acronyms or branded titles, no sentence over 25 words, no unresolved "not okay" flags.
- **FORMAT:** 12 components and 5 cross-cutting requirements present, numbers specific.
- **FAILURE:** vague promises, generic headlines, missing guarantee / FAQ / P.S., forced components, any broken argument beat flagged by the self-contained reviewer, any unresolved "not okay" flag.

## Pass or fail

Pass or fail. If fail, loop back to Phase 2 with the Priority Fix Stack. Maximum 2 loops before a human takes over.

## Assertions a reviewer can score

- All five reviewers ran in clean isolated contexts. *(yes / no)*
- None of the reviewers saw another reviewer's output. *(yes / no)*
- The synthesizer applied the precedence order above (brand-doc conflicts first). *(yes / no)*
- Contract validation lists pass or fail against every line in GOAL / CONSTRAINTS / FORMAT / FAILURE. *(yes / no)*
- The loop count is recorded, and any third loop has been escalated to a human. *(yes / no)*
