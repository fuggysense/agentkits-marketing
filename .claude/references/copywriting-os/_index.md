# Copywriting OS — Reference Library Index

Load on demand. Never preloaded. Called by `/copy` and sub-commands.

## Gates (pre-write; run in order)

| File | Purpose | Source |
|------|---------|--------|
| `gates/channeling-check.md` | Name existing desire + reader's internal conversation. Reject if copy is creating desire instead of channeling. | Schwartz 1966 + Collier 1937 + Peggy Burnett audit post |
| `gates/coat-of-arms-generator.md` | Generate or load prompt-ready audience portrait from `buyer-profile.md` + avatar. | Halbert (cai #44) |
| `gates/one-person-seed.md` | Inject "write to one real person + declare who at end" instruction into writer prompt. | Halbert (cai #44) |

## Builders (pre-write; fire as parallel sub-agents)

| File | Produces | Source |
|------|----------|--------|
| `builders/proof-inventory-builder.md` | `clients/<slug>/copy-system/proof-inventory.md` — every citable claim tagged by 6 proof types. Feeds B1 claim-verification-audit. | Mark Masters (cai #38) proof framework |
| `builders/objection-matrix-builder.md` | `clients/<slug>/copy-system/objection-matrix.md` — every heard objection mapped to 6 categories with grounded handlers. Feeds drafter + objection-coverage-audit. | Mark Masters (cai #36) objection categories |

## Reviewers — Phase B Anti-Hallucination (post-write; fire as parallel sub-agents BEFORE Phase C)

| File | Checks | Source |
|------|--------|--------|
| `reviewers/claim-verification-audit.md` | Every factual claim traces to a grounding-file source line. Coverage ≥ 95%, zero CRITICAL unsourced. | Phase B layer; cross-refs proof-inventory-builder output |
| `reviewers/forbidden-content-audit.md` | No banned phrases / saturated angles / voice violations / AI-tell patterns (F1-F6). | Phase B layer; integrates unslop + client learnings.md |
| `reviewers/specificity-audit.md` | No weasel words where grounding has concrete numbers. Density < 4 per 1000 words. | Phase B layer; complements cai #38 Specificity proof type |
| `reviewers/buyer-language-fidelity-audit.md` | Quoted buyer language verbatim-matches research. Paraphrases preserve register (no upshift drift). | Phase B layer; Schwartz/Collier (cai #42) + buyer-language-dossier |

## Reviewers — Phase C Quality (post-write; fire in parallel with Phase B)

| File | Checks | Source |
|------|--------|--------|
| `reviewers/one-person-enforcement.md` | Writer declared specific reader (name / job / moment / coat-of-arms specifics). Reject generic. | Halbert (cai #44) |
| `reviewers/proof-density-audit.md` | Every major claim has ≥1 of 6 proof types. ≥80% density, ≥4/6 types. | Mark Masters (cai #38) |
| `reviewers/emotional-sequence-audit.md` | 6 states covered in order. No skips, no reversals. | Mark Masters (cai #37) |
| `reviewers/objection-coverage-audit.md` | All 6 objection categories addressed or explicitly N/A with reason. | Mark Masters (cai #36) |
| `reviewers/teardown-reviewer.md` | Element-by-element failure-mode check (hero / lead / body / proof / CTA). | Peggy Burnett (cai #45) + Mark Masters (cai #26 hidden AI patterns) |

## Frameworks (canonical reference docs — POPULATED 2026-04-25)

| File | Purpose |
|------|---------|
| `frameworks/five-headline-mechanisms.md` | Curiosity / Specific-Benefit / Contrarian / Fear-Risk / Identity-Call (cai #39) |
| `frameworks/six-proof-types.md` | Expanded definitions + examples (cai #38) |
| `frameworks/six-emotional-states.md` | Definitions + sales-letter-method component mapping (cai #37) |
| `frameworks/six-objection-categories.md` | All categories + ≥10 variations each + pre-emptive handlers (cai #36) |
| `frameworks/halbert-trio.md` | A-pile + Coat of Arms + One-Person Rule (cai #44) |
| `frameworks/collier-principle.md` | Enter the conversation + good/bad prompt examples (cai #42) |
| `frameworks/schwartz-channeling.md` | Channel vs create + diagnostic (schwartz post + cai #41 workflow nuance) |
| `frameworks/scout-mode-instructions.md` | Research Command Center custom instructions (cai #35) |
| `frameworks/failure-mode-library.md` | LLM copy failure modes (cai #45 + cai #26) |
| `frameworks/hormozi-offer.md` | $100M offer framework applied to copy (cai #18) |
| `frameworks/framework-arsenal.md` | Canonical copy frameworks inventory (cai #14) |
| `frameworks/legend-architecture.md` | Origin story for clients (cai #29) |

## Raw newsletters (47 issues, on disk)

All 47 copywriting.ai newsletters scraped to `raw-newsletters/<slug>.md` (full body + frontmatter).
- Index: `_newsletter-index.md` — cai# → slug → cited-by-skill mapping
- Read a newsletter directly with the `Read` tool when a sub-agent needs primary-source quotes
- 14 newsletters are currently cited by skills (cai #14, 18, 26, 29, 35-42, 44, 45); 33 unsourced

## How to use

- Human: don't read these files top-down; they're for the `/copy` command and sub-commands.
- `/copy` command loads each file at the exact step it's needed.
- Reviewer files are loaded by **sub-agents**, not main thread.
- Framework files are loaded only when a gate or reviewer needs a specific fact.
