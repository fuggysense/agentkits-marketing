---
description: Generate a landing page (hero / lead / features / benefits / proof / objections / CTA) with copywriting-OS gates wrapped around the existing copywriting skill. Invoke via `/copy landing <client-slug> [page-type]`.
version: "0.1.0"
brand: AgentKits Marketing by AityTech
argument-hint: <client-slug> [page-type: lead-magnet | product | feature | pricing | homepage]
---

## What this does

Wraps `skills/copywriting/` + `skills/page-cro/` with copywriting-OS gates + reviewers. Produces a complete landing page draft.

**3-input principle from Mark Masters cai #40:** landing pages work from 3 inputs — product (what + core promise), buyer (frustrations + what tried), offer (price + guarantee + bonuses + deadline). Don't overwhelm with more questions.

## Step 1 — Shared context

See `commands/copy.md` Step 2.

Extract the 3 core inputs from loaded context:
- **Product:** from `offer.md` + `context-profile.json`
- **Buyer:** from `buyer-profile.md` + chosen `avatars/<avatar>.md`
- **Offer:** from `offer.md` (price, guarantee, bonuses, deadline if any)

If any of the 3 is missing from the client files, ask the operator ONCE before writing (don't overwhelm). Then write.

## Step 2 — Pre-write gates

Same 3 gates as `/copy:sales-letter`:
1. `gates/channeling-check.md` — existing desire + reader's internal conversation
2. `gates/coat-of-arms-generator.md` — Halbert portrait
3. `gates/one-person-seed.md` — writer instruction injection

## Step 3 — Resolve page type + structure

- **Lead-magnet** — opt-in page; Indifference→Pain→Desire-for-the-lead-magnet (skip Belief for product; Belief for the free resource is implicit)
- **Product** — full page; all 6 emotional states + all 6 objection categories
- **Feature** — feature-specific page; Pain→Understanding→Belief (customer already trusts the brand)
- **Pricing** — Price + Authority + Trust objections front-loaded; Desire in CTA
- **Homepage** — shorter; Indifference→Pain→Hope→Belief (many paths to Desire via CTAs to sub-pages)

Declare the structure before writing.

## Step 4 — Delegate to existing `/content:landing`

```
/content:landing <slug> <page-type>
```

Sub-agent execution. All shared context + gates injected into Phase 0.

## Step 5 — Post-write reviewers

Same 5 sub-agents. Landing-page-specific tweaks:
1. **one-person-enforcement** — required
2. **proof-density-audit** — ≥70% density, ≥4/6 types (higher bar than emails since landing pages carry the full conversion load)
3. **emotional-sequence-audit** — 6 states for product pages; adapted per page type (see Step 3)
4. **objection-coverage-audit** — front-load Price + Trust + Authority for pricing pages; full coverage for product pages
5. **teardown-reviewer** — full element check, critical failures at Hero H1 (transform class) and CTA C3 (fake urgency) auto-FAIL

## Step 6 — Synthesize + revise

Same as `/copy:sales-letter`.

## Step 7 — Ship + log

- **Output:** `clients/<slug>/copy-system/outputs/landing-pages/<YYMMDD>-<page-name>.md` (copy text)
- **Rendered HTML (optional):** `clients/<slug>/copy-system/outputs/landing-pages/<YYMMDD>-<page-name>-rendered/index.html`
- **Design handoff:** if `website-design` skill is next in chain, the draft's element structure is already compatible
- **Logs + learnings:** standard

## Prerequisites

All `/copy` prerequisites PLUS:
- Offer + pricing known (or explicitly marked "TBD — request via form")
- Page type identified

## Related

- Underlying skills: `skills/copywriting/`, `skills/page-cro/`
- Existing command wrapped: `commands/content/landing.md`
- Downstream handoff: `skills/website-design/` for actual HTML/JSX build
- Parent router: `commands/copy.md`
- Cai #40 3-input principle enforced
