# 02_script — Concept And Script Contract

Legacy and non-campaign message work: concepts, hooks, scripts, music directions, captions, email copy, lead-magnet copy, sales-letter drafts. Decides what the message is before production. **All campaign video concept work lives under `../campaigns/<campaign>/video-concepts/<concept-slug>/02_ag1-options/` + `/03_scripts/` — never here.**

## Inputs

- L4 (working): selected input refs and synthesized research from `01_research/output/`.
- L3 (reference): `../_brand/` (voice, offer, buyer, story), `../_config/scope-agreement.md`, and the global copywriting frameworks at `.claude/references/copywriting-os/` (auto-loaded when copy work fires per `routing-overrides.md`).

## Process

Draft the message for non-campaign work: Reel scripts (hook/body/CTA via the global `ig-reel-script-writer`), video concept packs, music-ad lyrics and briefs, captions, email sequences, lead-magnet copy, sales letters, headlines. Long-form YouTube scripts use the global `yt-scriptwriter` (Chasteen retention method). Fire the copywriting-os gates before drafting (`channeling-check`, `coat-of-arms-generator`, `one-person-seed`), then run the reviewers after the first draft (`one-person-enforcement`, `proof-density-audit`, `emotional-sequence-audit`, `objection-coverage-audit`, `teardown-reviewer`). Per-client filled artifacts generate on demand into `../_brand/copy/`.

## Outputs

- `output/<TYPE><id>-<slug>/...` — `R###/script.md` (Reels), `V###/concept-pack.md` + `music-brief.md`, `E###/email.md`, `LM###/copy.md`, `SL<YYMMDD>-v<N>.md` (sales letters).
  - Done: the operator approves the concept direction; approved scripts hand off to `03_production/`. Do not generate production assets before that approval.
