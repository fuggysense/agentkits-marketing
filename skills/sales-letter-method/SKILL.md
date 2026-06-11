---
name: sales-letter-method
version: "1.1.0"
brand: AgentKits Marketing by AityTech
preferred_invocation: /copy:sales-letter  # wraps this skill with copywriting-OS gates + reviewers (see .claude/references/copywriting-os/)
category: content
difficulty: advanced
description: "Write 800-2000+ word direct-response sales letters for cold paid traffic. 5+ min engagement → booked consultations. Real estate, consulting, coaching, agency, high-ticket. NOT: landing pages, pricing pages, email sequences."
triggers:
  - sales letter
  - long form sales letter
  - long-form sales letter
  - cold traffic sales page
  - VSL alternative
  - hormozi sales letter
  - direct response letter
  - lead gen sales page
  - sales letter method
prerequisites:
  - clients/<slug>/context-profile.json
  - clients/<slug>/_brand/offer.md
  - clients/<slug>/_brand/buyer-profile.md
related_skills:
  - copywriting
  - copy-editing
  - page-cro
  - ab-test-setup
  - headline-bank
agents:
  - copywriter
  - brand-voice-guardian
  - conversion-optimizer
mcp_integrations:
  optional:
    - meta-ads
    - google-analytics
---

# Sales Letter Method

Build a **long-form direct-response sales letter** for cold paid traffic. Target: 800-2,000+ words that stop the scroll, hold 5+ minutes of attention, and turn strangers into booked consultations. This is not a landing page. It is a single-page asset that replaces a VSL, webinar, or nurture sequence with one belief-build → commit flow.

**Model:** claude-opus-4-8 (Phase 1 drafters).

## When to use this skill

**YES:**
- Cold FB/IG ad traffic → booking or opt-in page
- High-ticket service, consulting, coaching, agency, real estate
- Single-offer funnel (no product catalog)
- Stranger → booked consultation in one reading session

**NO — route elsewhere:**
- Short product landing pages → `/content:landing`
- Pricing or feature pages → `copywriting` skill
- Email sequences → `email-sequence`
- Ad creative → `/ads:big-angle-spotter`
- Warm-traffic or branded pages → `page-cro`
- B2B SaaS sales — product-led growth + sales calls do the work; long letters are the wrong tool

Vertical-specific guidance (DTC supplements, real estate, financial services, coaching, agency) lives in `references/component-matrix.md` → Industry Tweaks.

## The 12-component framework

Not every letter uses all 12 components. Phase 0 picks which ones fit the offer. The framework also has 5 cross-cutting requirements that run through every letter. Full matrix and default sequence → `references/component-matrix.md`.

## The 5-phase pipeline

### Phase 0 — Context Scan (auto + HITL gate)
Auto-reads client files → builds component inclusion matrix → one-screen HITL for confirm or adjust → feeds the drafters.

### Phase 0.5 — Claim Audit
Sort every claim into CAN / CANNOT / NEEDS CAREFUL WORDING before any drafting starts. Critical for health, money, legal verticals. Full playbook → `references/phase-0-5-claim-audit.md`.

### Phase 0.7 — Mechanism + Offer Architecture (HITL gate)
Architect the mechanism, offer stack, brand-association ladder, and scene assignments before drafters touch a component. Output is a required Phase 1 input. Full playbook → `references/mechanism-architecture.md`.

### Phase 1 — Parallel Drafting (2 Opus drafters)
- **Hook Half** (components 1-4): Headline + Sub + Lead + Pain Cycle + Integrity
- **Commit Half** (components 5-12): Mechanism + Proof + Offer + Scarcity + Guarantee + CTA + FAQ + P.S.

Run in parallel (single message, 2 Agent calls) for about 40% time saving. Each drafter gets identical Phase 0 output + Phase 0.5 claim inventory + Phase 0.7 architecture document + component matrix + client files. Drafters running without the Phase 0.7 document is a hard error.

### Phase 2 — Stitcher (1 Opus agent)
Merges the two halves, smooths transitions, enforces one voice, deletes redundancy. Runs the 11-boundary cohesion check before handing to Phase 3. Full transition spec → `references/cohesion-check.md`.

### Phase 3 — Conversion Gate (mandatory)
Five reviewers fire in parallel in isolated contexts. Skip any one and the review is broken. Synthesizer maps all five into one Priority Fix Stack with brand-doc conflicts taking ship-block precedence. Full roster, precedence order, and contract validation → `references/phase-3-reviewer-stack.md`.

### Phase 4 — Polish + Pre-Ship Gate
Three polish passes (de-AI, unslop, voice). Then the `sales-letter-auditor` agent runs in an isolated context as a fresh-eyes ship-gate. Then the pre-ship checklist scores five lenses with quantitative pass criteria. Any FAIL stops the ship. Full spec → `references/phase-4-preship.md`.

## Required inputs

Load in order before drafting:
1. `clients/<slug>/context-profile.json` → identity foundation
2. `clients/<slug>/_brand/offer.md` → offer deliverables (verbatim)
3. `clients/<slug>/_brand/buyer-profile.md` → persona psychology
4. `clients/<slug>/avatars/` → DCT avatars from the avatar-research skill
5. `clients/<slug>/source-of-truth.md` → paid ads research
6. `clients/<slug>/_brand/brand-voice.md` → voice target
7. `voice/<person>/*` → V.O.I.C.E. files
8. Meta Ads + GA baseline metrics → Phase 3 GOAL threshold

> `_brand/` is canonical for offer / buyer-profile / brand-voice (per the AGENT ENTRY CONTRACT). If a client still keeps these at the flat `clients/<slug>/` root (pre-`_brand/` legacy), read those instead and flag the client for migration.

If any critical input is missing, surface to the user before drafting. Do not fabricate.

## On-demand references

- Best-practice catalogue: `best-practices/_index.md` (full reference index coming in Phase 2 as `references/_index.md`).
- Master prompt for any LLM: `prompt-template.md` (skill root).
- Hard rules every letter must obey: `best-practices/_critical-rules.md`.
- Named failure patterns: `best-practices/_failure-modes.md`.

## Related
<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[eval-sales-letter]] (agent, 0.21)
- [[sales-letter-audit]] (skill, 0.15)
- [[sales-letter-auditor]] (agent, 0.14)
- [[headline-bank]] (skill, 0.14)
- [[big-angle-spotter]] (skill, 0.14)

<!-- skill-graph:end -->
