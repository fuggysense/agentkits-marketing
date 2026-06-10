# 02_script — Concept And Script Contract

Concepts, hooks, scripts, music directions, captions, email copy, lead-magnet copy, and sales-letter drafts. This stage decides what the message is before production assets are generated.

## In scope

- Reel scripts (hook / body / CTA)
- Video concept packs and campaign briefs
- Music ad lyrics, music direction, and manual generation briefs
- Caption drafts
- Email sequences
- Lead-magnet copy (audit checklist, etc.)
- Sales-letter drafts
- Headlines / hooks

## Output convention

- `output/R<###>-<slug>/script.md` for Reels
- `output/V<###>-<slug>/concept-pack.md` for video concept packs
- `output/V<###>-<slug>/music-brief.md` for music ads
- `output/E<###>-<slug>/email.md` for emails
- `output/LM<###>-<slug>/copy.md` for lead-magnet content
- `output/SL<YYMMDD>-v<N>.md` for sales letters

## Copywriting framework

Frameworks (coat-of-arms, objection-matrix, proof-inventory, scout-mode, etc.) live globally at `.claude/references/copywriting-os/`. Auto-loaded when copy work fires per routing-overrides.md.

Per-client FILLED artifacts (filled coat-of-arms, filled objection-matrix) are generated on-demand into `_brand/copy/` when copy work begins.

## Skills available for this phase

**`yt-scriptwriter`** (global) — Long-form YouTube scripts using the Linden Chasteen method. Retention-optimized structure, pre-script questions, and pattern interrupts. Trigger phrases: "write youtube script", "yt script", "long-form script", "scriptwriter", "youtube video script".

**`ig-reel-script-writer`** (global) — Short-form Reel scripts (hook / body / CTA). Platform-native structure for IG and TikTok short video. Trigger phrases: "reel script", "ig script", "short-form script", "tiktok script", "write a reel".

### Pre-write gates (fire before drafting)

From `.claude/references/copywriting-os/gates/`:
- `channeling-check.md` — confirm you're channeling the right reader, not writing to a crowd
- `coat-of-arms-generator.md` — buyer identity lock before writing
- `one-person-seed.md` — write to the one person, not a persona category

### Post-write reviewers (run after first draft)

From `.claude/references/copywriting-os/reviewers/`:
- `one-person-enforcement.md` — did it stay one-person throughout?
- `proof-density-audit.md` — are claims backed?
- `emotional-sequence-audit.md` — does the emotional arc hold?
- `objection-coverage-audit.md` — are the real objections addressed?
- `teardown-reviewer.md` — final structural teardown before handoff

## Hand-off rule

Approved scripts and concepts → `03_production/` for input assets, image prompts, beat sheets, Video Studio render prompts, and motion prep. Do not generate production assets before the user approves the concept direction.
