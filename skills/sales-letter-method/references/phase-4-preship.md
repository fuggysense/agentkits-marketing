---
file_type: phase-playbook
load_when: pipeline reaches Phase 4 polish; agent is about to ship the letter to disk; final pre-ship gate fires
applies_to: 5-phase-pipeline (Phase 4)
last_updated: 2026-05-27
---

# Phase 4 — Polish and Pre-Ship Gate

## What this file teaches

Phase 4 is the final scrub before the letter ships. Three polish passes, then an isolated fresh-eyes audit, then a structural pre-ship checklist. Any FAIL on the pre-ship lenses stops the ship.

## Polish passes (run in order)

- **`copy-editing` skill, Sweep 8** — the de-AI pass. Strips AI-shaped patterns.
- **`unslop` skill, profile `long-form-sales-letter`** — strips slop language.
- **`brand-voice-guardian`** — final check that the voice matches the brand.

## Step 4a — Fresh-eyes audit (mandatory ship-gate)

Spawn the `sales-letter-auditor` agent (`agents/sales-letter-auditor.md`) in an **isolated context window**. Do not run this in the same session that wrote the letter. The whole point of this step is that the agent has never seen the letter before. If you let it see the generation history, you have wasted the step.

**Pass to the agent:**

- Path to finished letter: `clients/<slug>/copy/<YYMMDD>-<letter>.md`
- Client context directory paths: `offer.md`, `icp.md`, `buyer-profile.md`, `context-profile.json`
- Purpose of letter (one sentence, from Phase 0 HITL output)
- CTA target (one sentence, from Phase 0)
- Final goal (one sentence, from Phase 0)

**Do NOT pass:** generation conversation history, drafter's reasoning, alternative drafts, or any "what we were going for" framing. That context kills the isolation.

**Gate behavior:**

- Agent returns one of four verdicts: SHIP, HOLD — minor fixes, HOLD — blockers present, or DO NOT SHIP.
- If SHIP → proceed to the pre-ship checklist below.
- If HOLD or DO NOT SHIP → fix every blocker in the ranked findings, then spawn the agent again. Do not skip. Do not override. The letter does not ship until the agent returns SHIP, or the operator explicitly overrides a WEAK mark with a written reason.

## Pre-ship checklist (`reviewers/pre-ship-checklist-reviewer.md`)

A sharper structural audit than the Copy Chief. Five lenses, each with named fail patterns and a clear pass threshold:

1. UMP clarity
2. Identity-layer depth
3. Headline-body coherence
4. Concentration sharpness
5. CTA structural completeness

Runs on a single artifact. Produces a fix list ranked by impact.

**Gate rule:** any lens marked FAIL → the letter does not ship until the proposed fix is applied. WEAK marks may ship if the operator gives an explicit override.

## Optional 4th Phase 3 reviewer (used in Phase 4 if applicable)

`reviewers/coherence-reviewer.md` — runs only when the letter has companion pieces (other ads pointing to the same landing page, a paired advertorial, an email sequence the letter inherits language from). Cross-document emotional and language continuity check.

## Assertions a reviewer can score

- The three polish passes ran in the order above. *(yes / no)*
- The `sales-letter-auditor` agent ran in an isolated context window with no generation history. *(yes / no)*
- The agent's verdict is one of SHIP / HOLD-minor / HOLD-blockers / DO NOT SHIP. *(yes / no)*
- Every blocker from a HOLD or DO NOT SHIP verdict has been fixed before the next spawn. *(yes / no)*
- All five pre-ship lenses are PASS, or any FAIL has a documented fix applied, or the operator has logged an override reason on any WEAK marks. *(yes / no)*
