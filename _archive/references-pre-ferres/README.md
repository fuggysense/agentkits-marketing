# Pre-Ferres static references (archived, switchable)

Retired 2026-06-11 during the rebuild (M2.4 — Statics Lane rebuild). These were the static-ad creative-direction files in use BEFORE the Ferres "AI Ads Lab" distilled references landed in `_shared-knowledge/ferres/`. They are archived, not deleted — the operator may request reactivation at any time.

## What is here

| File | Was loaded by | Replaced by |
|------|---------------|-------------|
| `high-converting-static-brief.md` | `skills/ad-concept-engine/SKILL.md` Phase 2a (the "9-point scroll-stop bar", MANDATORY on every static batch) | `skills/ad-concept-engine/references/static-image-method.md` |
| `gut-wrenching-ad-format.md` | `skills/image-generation/SKILL.md` ("Gut-Wrenching FORMAT" 9-rule standard for ad-image prompt sets) | `skills/ad-concept-engine/references/static-image-method.md` (image-generation now points there) |
| `sg-cultural-guidelines.md` | `skills/ad-concept-engine/SKILL.md` (Phase 2a/2b "Skills loaded" + Language Standards + References — skill-global Singapore cultural-sensitivity rules) | `clients/<slug>/_brand/locale-rules.md` §6 "Cultural sensitivity" (the SG example in `clients/_template/_brand/locale-rules.md` carries the distilled Malay-Muslim / Islamic-finance / register rules) |

## Why retired

Both files carried hard-coded Singapore/CPF/HFE/ethnicity locale content baked into a client-agnostic skill, and predated the Ferres method (5 canonical formats + 11-pattern library + 3-pass teardown-rebuild + post-render image QA gate). The rebuild:

1. Moved all locale content out to per-client `clients/<slug>/_brand/locale-rules.md` (template at `clients/_template/_brand/locale-rules.md`).
2. Grounded the new method in the citation-verified Ferres distillation (`_shared-knowledge/ferres/06-statics-playbook.md` + `patterns/statics-pattern-library.md` + `05-quality-bar-critique-rubric.md`).
3. Wired the claim gate (M1) + a fresh-context copy pre-launch rubric in front of the human creative gate.

## How to reactivate (if the operator asks)

The switch is a one-line repoint per skill — the files are intact:

1. `git mv _archive/references-pre-ferres/high-converting-static-brief.md skills/ad-concept-engine/references/` and re-point ACE SKILL.md Phase 2a back at it (the old "Skills loaded" + "MANDATORY: Load `references/high-converting-static-brief.md`" lines).
2. `git mv _archive/references-pre-ferres/gut-wrenching-ad-format.md skills/image-generation/references/` and re-point image-generation SKILL.md's "Ad-creative quality bar" callout back at it.
3. `git mv _archive/references-pre-ferres/sg-cultural-guidelines.md skills/ad-concept-engine/references/` only if you deliberately want skill-global SG rules again — but prefer NOT to: the SG cultural-sensitivity content now lives in the per-client `locale-rules.md` SG example, where it belongs. Reactivating the skill-global copy reintroduces the leak the rebuild fixed.

Reactivating any of these does NOT undo the locale move — the SG/CPF/HFE/ethnicity + Malay-Muslim/Islamic-finance rules now live in `clients/<slug>/_brand/locale-rules.md` and should stay there. If you reactivate brief #1 or #2, strip the locale lines from the reactivated brief or you reintroduce the leak.
