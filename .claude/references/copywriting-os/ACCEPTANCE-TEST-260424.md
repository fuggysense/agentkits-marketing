# Phase B Reviewer Acceptance Test — 2026-04-24

**Target:** `clients/neezanizam/sales-letters/260421-v1.md` (329-line draft).
**Model:** Sonnet 4.6 via fresh `claude -p` workers (Ravan pattern, content-cached SP).
**Runner:** `scripts/phase4_acceptance_test.py`.
**Total runtime:** 514 s wall clock (workers parallel).
**Total cost:** $3.09.
**Outputs:** `clients/neezanizam/sales-letters/260421-v1-reviews/b{1,2,3,4}-*.md`.

## Summary

| Reviewer | Verdict | Findings | Ship decision |
|----------|---------|----------|---------------|
| B1 Claim Verification | **FAIL** | 26 claims audited, 34.6% coverage, 1 CRITICAL + 5 HIGH + 7 MEDIUM + 4 LOW unsourced | Ship as-is |
| B2 Forbidden Content | PASS (with flags) | 0 CRITICAL/HIGH, 3 F3 voice drift + 2 F4 AI-tell, density 1.0/1000 | Ship as-is |
| B3 Specificity | PASS | 0 CRITICAL/HIGH/MEDIUM, 9 LOW allowable hedges, density 0.0/1000 | Ship as-is, calibrate in Wave 2 |
| B4 Buyer Language Fidelity | PASS (marginal) | 0 confirmed CRITICAL, 1 conditional HIGH (Riduan testimonial — needs `testimonials/` verification), 2 MEDIUM case-study additions | Ship as-is |

**All 4 reviewers functional. All produced structured audit reports matching their specs' output schemas. All caught real violations.**

## Acceptance criteria check (per plan)

| Plan expected | Actual | Match |
|---------------|--------|-------|
| B1 should flag fabricated case-study numbers | Flagged Emilia & Faizal liquid-savings comparison as CRITICAL (not in any grounding file) + Fahmy "two kids" as MEDIUM + ClearBuy™ umbrella trademark as HIGH | ✅ |
| B1 should flag "22 years" claim | B1 correctly did NOT flag — `context-profile.json` has `years_experience: 22`, claim is sourced | ✅ (correct behaviour) |
| B2 should flag voice violations | Flagged 13 em-dash heading violations (explicit source-of-truth.md §1 ban), dismissive FAQ DIY tone, all-caps hook, not-X-not-Y-but-Z triplet | ✅ |
| B3 should flag weasel words | Flagged "most buyers", "most couples", "a small number" — correctly classified as LOW because no grounding number exists (per spec: weasel without grounding number = LOW allow) | ✅ (correct behaviour) |
| B4 should flag Riduan testimonial | Flagged HIGH conditional CRITICAL pending `testimonials/` folder verification — authenticity markers (Malay honorifics, Singlish orthography) note real-buyer register | ✅ |

## Findings that matter most (operator attention)

**Must-fix before ship (B1 + B2 FAIL-level):**
1. **Emilia & Faizal case study (B1 CRITICAL)** — "preserved more of their liquid savings than the EC route" is fabricated. Remove or source from case records.
2. **13 em-dash headings (B2 MEDIUM, explicit client constraint breach)** — violates source-of-truth.md §1 ban on em-dashes in headlines. Swap to colon / pipe / period.
3. **"Five Questions" CTA (B1 HIGH)** — assessment count not confirmed. Swap to sourced "Two minutes" framing.
4. **"As seen on" [Logo ×28] (B1 HIGH)** — no logo inventory in grounding. Replace with sourced "22 years · 729+ families · $200M transacted" authority bar.
5. **ClearBuy™ umbrella (B1 HIGH)** — RAM™ and SPOT™ are sourced trademarks; ClearBuy™ is not. Remove until legal/brand confirms.

**Flag-to-verify:**
6. **Riduan & Nadiah testimonial (B4 HIGH-conditional)** — pull `testimonials/` folder, fuzzy-match ≥ 90%. If absent, escalates to CRITICAL.
7. **12–18 month MOP timing (B1 HIGH)** — no source. Reframe without the specific window.

## Calibration notes for future runs

**B3 specificity — slightly lenient by design.** 0.0/1000 density looks suspicious at first glance, but B3's spec treats weasels without grounding numbers as LOW-allow. This is intentional — the reviewer cannot fabricate a specific number when none exists. What it WILL catch:
- Vague headline/hero with an available number → CRITICAL
- Round multipliers ("10x") without anchor → MEDIUM if index has better figure

To tighten B3 in future: populate `proof-inventory.md` via `proof-inventory-builder.md` (planned for Phase C integration) with all numeric claims from `context-profile.json` + `source-of-truth.md`. Then B3 will upgrade LOW → HIGH when grounding numbers exist for flagged phrases.

**B1 missing `proof-inventory.md`.** B1's spec lists `proof-inventory.md` as primary cross-reference. The file doesn't exist yet for NeezaNizam. B1 cascaded to other grounding files (per its own fallback logic) and still achieved strong findings. Run `proof-inventory-builder.md` for NeezaNizam before next B1 run to close the gap.

**B2 caught client-specific rules correctly.** source-of-truth.md §1 "Words/tones to avoid" was honoured — reviewer knew to look for em-dashes in headlines specifically. This validates the F3 category wiring to client `brand-voice.md` / `source-of-truth.md`.

**B4 register-attenuation judgment.** B4 correctly noted Singlish presence in raw research (*lah*, *leh*, *anot*, *bo bian*) versus standard English in draft, but classified as "format-appropriate attenuation" for a long-form letter. This is the right call — the draft is a formal letter, not ad copy. B4's register-drift detection is calibrated correctly.

## Ship decision

**All 4 reviewers ship as-is.** No reviewer iteration needed before wiring into `/copy:*` flows. Integration work (commands/copy.md router Step 3b + Step 5, `_index.md`, `routing-table.md`, `changelog.md`) already complete.

## What this unlocks

- `/copy:sales-letter` (and the other 4 `/copy:*` commands via the router) now gate on grounding verification before shipping copy.
- Phase B failures block ship regardless of Phase C verdicts (existing persuasion-craft reviewers — one-person, proof-density, emotional-sequence, objection-coverage, teardown).
- Pre-write builders (`proof-inventory-builder` + `objection-matrix-builder`) populate the reference files B1/B4/objection-coverage depend on before the drafter runs.
- Sales-letter-method drafters now run on Opus 4.6 (global policy: copy=Opus, review=Sonnet).
- Big-angle-spotter pipeline now routes copy-generating steps (01/07/07b/08/11/12) to Opus 4.6, review/ranking/gating steps to Sonnet 4.6.

## What's deferred

- 4 sub-commands (`copy/email.md`, `landing.md`, `ad.md`, `headline.md`) not yet updated with Phase B block. Router owns the wiring so they inherit — surgical updates optional.
- 47 copywriting.ai newsletters framework references (deferred per original plan decision).
- NeezaNizam v1.5 rewrite applying B1/B2 fixes — operator decision, not in this test.

## Next steps (operator decision)

1. **Apply B1/B2 findings to NeezaNizam v1.5** — produces a v1.6 with grounded claims + stripped em-dashes.
2. **Run `proof-inventory-builder` for NeezaNizam** — populates `copy-system/proof-inventory.md` so future B1 runs hit the primary cross-reference.
3. **Test on a second client** — e.g., a non-property client to verify reviewers generalise beyond NeezaNizam's register patterns.
4. **Wire Phase B into `/copy:email`, `/copy:landing`, `/copy:ad`, `/copy:headline` sub-commands** — currently inherits from router, explicit wiring is optional polish.
