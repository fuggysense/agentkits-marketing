---
name: sales-letter-method
version: "1.0.0"
brand: AgentKits Marketing by AityTech
preferred_invocation: /copy:sales-letter  # wraps this skill with copywriting-OS gates + reviewers (see .claude/references/copywriting-os/)
category: content
difficulty: advanced
description: When the user wants to write a long-form direct-response sales letter for cold paid traffic (FB/IG ads) — 800-2000+ word assets designed to earn 5+ minutes of attention and convert cold scrollers into booked consultations. Industry-agnostic, first-class support for real estate, consulting, coaching, agency, high-ticket service. NOT for short landing pages (use content:landing), pricing/product pages (use copywriting), or email sequences (use email-sequence).
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
  - clients/<slug>/offer.md
  - clients/<slug>/buyer-profile.md
related_skills:
  - copywriting
  - copy-editing
  - page-cro
  - ab-test-setup
  - prompt-contracts
  - verification-loops
  - unslop
  - content-moat
  - avatar-research
  - headline-bank
agents:
  - copywriter
  - brand-voice-guardian
  - conversion-optimizer
  - solopreneur
  - startup-founder
mcp_integrations:
  optional:
    - meta-ads
    - google-analytics
    - semrush
success_metrics:
  - opt_in_rate
  - scroll_depth
  - cta_click_through_rate
  - cost_per_booked_consultation
---

## Graph Links
- **Pipeline pair:** [[sales-letter-audit]] — audit an existing letter through Schwartz/Halbert lens, then this skill rewrites it. Audit → Method is a closed loop.
- **Feeds into:** [[page-cro]], [[ab-test-setup]], [[copy-editing]], [[conversion-optimizer]], [[website-design]] (Mode E: Cold-Traffic CRO ships the letter as a coded HTML+CSS landing page)
- **Audited by:** [[sales-letter-auditor]] agent (runs as ship-gate before publish; isolated-context fresh-eyes review against `sales-letter-audit` skill — escapes the generator's brain)
- **Draws from:** [[copywriting]], [[headline-bank]], [[marketing-psychology]], [[avatar-research]], [[source-of-truth]], [[content-moat]]
- **Used by agents:** [[copywriter]], [[brand-voice-guardian]], [[conversion-optimizer]]
- **QA layer:** [[verification-loops]], [[prompt-contracts]], [[multi-agent-consensus]]

# Sales Letter Method

You are building a **long-form direct-response sales letter** for cold paid traffic. Target: 800-2,000+ words that stop the scroll, hold 5+ minutes of attention, and convert strangers into booked consultations.

This is NOT a landing page. It is a single-page asset engineered to replace a VSL, webinar, or nurture sequence with one concentrated belief-build → commit flow.

Named methodology: **The Sales Letter Method.**

## When to use this skill

**YES:**
- Cold FB/IG ad traffic → booking/opt-in page
- High-ticket service, consulting, coaching, agency, real estate
- Single-offer funnel (no product catalog)
- Stranger → booked consultation in one reading session

**Verticals this skill handles natively** (with vertical-specific guidance in `references/component-matrix.md` → Industry Tweaks + Vertical-Specific Failure Modes):

- **DTC supplements / wellness / health** — adapt narrator carefully (regulatory; see voice-register guidance)
- **Real estate** (SG and US) — first-time buyers, upgraders, sellers, investors
- **B2B SaaS / agency / consulting** — high-ticket, outcome-led
- **Financial services** — adapt with compliance pass; lean on credentials + outcome guarantees
- **Coaching / info product / online course** — graduated proof ladder, identity-led close

What changes per vertical: register, failure-mode catalog (Pain Cycle scenes), proof types (case studies vs testimonials vs credentials), guarantee variants. What stays constant: the 12-component framework, the 5 cross-cutting requirements, the 5-phase pipeline.

**NO — route elsewhere:**
- Short product landing pages → `/content:landing`
- Pricing/feature/product pages → `copywriting` skill
- Email sequences → `email-sequence`
- Ad creative → `/ads:big-angle-spotter`
- Warm-traffic or branded pages → `page-cro`

**Downstream — once the letter is approved:**
- **Audit before ship:** `sales-letter-auditor` agent (`agents/sales-letter-auditor.md`) — mandatory ship-gate. Pass finished letter + client context files. Agent returns pass/fail with ranked findings. Apply before ship.
- **Ship as a coded landing page:** `website-design` Mode E (Cold-Traffic CRO) — ingests this letter as body content, wraps it in an anti-template HTML+CSS page using one of 8 experience formats. Letter wording preserved where it fits the page section; design layer added on top.
- **Optimize an existing live page:** `page-cro` (after publish, with traffic data)

## The 12-Component Framework + 5 Cross-Cutting Requirements

The 13th Hormozi component (Price Anchor) is intentionally removed — this skill targets lead-gen/consultation funnels where no price is disclosed. The Guarantee Stack replaces it as the primary conversion lever.

**Not every letter uses all 12.** Phase 0 Context Scan decides which components fit the offer. See `references/component-matrix.md`.

**5 Cross-Cutting Requirements (always required — thread through components):**
1. **Objection Architecture** — 10 canonical objections preempted inline or in FAQ (`references/objection-architecture.md`)
2. **Qualification** — at least 1 testable qualification block (`references/qualification-patterns.md`)
3. **Trust Density** — ≥ 5 distinct trust signals distributed across ≥ 3 components (`references/trust-density.md`)
4. **Mechanism Justification** — Component 5 now has 5 jobs, includes cause-and-effect logic (`references/mechanism-justification.md`)
5. **Cohesion** — Stitcher runs boundary-transition check; 0 `jump` at 5 critical boundaries (`references/cohesion-check.md`)

**Default sequence:**

1. **Headline + Subheadline** — Dream Outcome, specific numbers, mechanism tease
2. **Lead** — Dear [avatar] opener, restate offer in new language, tease mechanism
3. **Pain Cycle / Why Most Fail** — Name the broken loop, deconstruct old way
4. **Integrity Tie-Down** — Rhetorical commitment ("if you nodded to any of this…")
5. **Mechanism** — Name the system, describe function (not tools), show speed + ease
6. **Proof Stack** — Living Proof (identical-to-them results). If no proof yet, pivot to credentials/methodology.
7. **Offer Breakdown + Bonus Stack** — Outcome first, then deliverables, then bonuses (if real)
8. **Light Scarcity** — Real capacity limits only. "5 spots this month" / "30 bookings to maintain quality" — NEVER heavy countdowns.
9. **Guarantee Stack** — PRIMARY CONVERSION LEVER. No-pitch, value-pay, or outcome guarantees. See `references/guarantee-variants.md`.
10. **CTA** — Benefit-oriented button + friction reducers (`[risk reversal] + [social proof] + [speed/ease]`)
11. **FAQ** — 5 core objections: Time / Money / Authority / Stall / Preference
12. **PS Line** — Threshold fear handler, personal tone

## The 5-Phase Pipeline

### Phase 0 — Context Scan (auto + HITL gate)
Auto-reads client files → builds component inclusion matrix → 1-screen HITL for confirm/adjust → feeds drafters.

### Phase 0.5 — Claim Audit (creative constraint)

Before any drafting begins, produce a 3-bucket claim inventory the drafters must obey:

- **CAN claim** — settled science, product specs, third-party-tested data, named outcomes from real clients with documented results, credentials/certifications the operator holds.
- **CANNOT claim** — overreaching beyond research, brand-name competitor comparisons that violate ad policies, regulatory red flags (medical / financial / legal), fabricated testimonials or invented proof.
- **REQUIRES CAREFUL FRAMING** — emerging research framed as settled, mechanism hypotheses presented as established, comparative outcomes against the operator's own past selves, claims that depend on context the letter doesn't have room to set up.

**Why this runs before Phase 1, not after:** Drafters write differently when they know what they can't say. Catching overclaim in Phase 3 is expensive — half the draft has to be rewritten. Naming the constraints upfront means Phase 1 produces compliant copy on the first pass.

**This is critical for medical, financial, wellness, and any regulated vertical.** For unregulated verticals (consulting, agency, coaching, B2B SaaS) the audit is lighter — focus on overclaim of guaranteed outcomes and competitor naming.

The Phase 0.5 output is a one-screen creative-constraint document handed to all Phase 1 drafters alongside the component inclusion matrix.

### Phase 1 — Parallel Drafting (2 Opus 4.6 subagents)
- **Hook Half** (components 1-4): Headline + Sub + Lead + Pain Cycle + Integrity
- **Commit Half** (components 5-12): Mechanism + Proof + Offer + Scarcity + Guarantee + CTA + FAQ + PS

Run in parallel (single message, 2 Agent calls). Saves ~40% drafting time. Each agent receives identical Phase 0 output + component matrix + client files.

**Model:** `claude-opus-4-6` for both drafters (global policy: Opus for all copy generation, Sonnet for all review). TODO: migrate to `claude-opus-4-7` by 2026-06-15 (Opus 4.6 deprecation date).

### Phase 2 — Stitcher (1 Opus 4.6 agent)
Merges halves, smooths transitions, enforces voice consistency, deletes redundancy.

**Cohesion check (required):** before handing off to Phase 3, stitcher runs the 11-boundary test per `references/cohesion-check.md`. All `jump` transitions flagged and rewritten using Echo / Escalate / Pivot / Answer bridge patterns. 0 `jump` tolerated at the 5 critical boundaries (H→S, S→L, L→P, P→M, CTA→PS). Output includes a COHESION REPORT.

### Phase 3 — Conversion Gate (3 parallel reviewers + synthesizer) [MANDATORY]

Three subagents fire in parallel, in clean isolated contexts. None may see any other's output. Skipping any one of them = auto-reject the review as incomplete. This applies to the full pipeline AND to any standalone review invocation (e.g. user says "review this sales letter", "kill my babies on this letter", "is this letter clear enough") — the three-reviewer stack is the single source of truth for every sales letter evaluation this skill handles.

- **Buyer Lens** (`reviewers/buyer-lens-reviewer.md`): simulates the actual target prospect reading the letter. Jargon-free. Reacts on first impression, relevance, trust, desire, friction, decision.
- **Copy Chief** (`reviewers/copy-chief-reviewer.md`): elite DR strategist (Schwartz/Ogilvy/Halbert lens). Section-by-section diagnosis, priority fixes, rewrite recommendations.
- **Self-Contained Experience** (`reviewers/self-contained-reviewer.md`): kill-babies lens. Treats the page as a cold standalone read. Two questions: (1) Is it a complete argument a tired native-English SG reader can follow top to bottom? (2) How simple is the language — thorough structural then language simplification, never make the reader feel "not okay." Outputs Complete Argument Check / Structural Simplification / Language Simplification (line-by-line) / "Not Okay" Flags / The One Question.

**Synthesizer** maps buyer frictions → self-contained cuts + simplifications → chief diagnoses → single proposed fix. Structural cuts from the self-contained reviewer take precedence over clever additions from the chief — simpler wins over smarter at the first pass. Outputs **Priority Fix Stack** ranked by severity × ease-of-fix × simplification-alignment.

Plus Contract Validation (merged-in):
- GOAL (opt-in > baseline × 1.5) / CONSTRAINTS (voice, offer accuracy, no AI patterns, markup applied, ≤9 movements, no unexplained acronyms/branded titles, no sentence > 25 words, no unresolved "not okay" flags) / FORMAT (12 components + 5 cross-cutting requirements present, numbers specific) / FAILURE (vague promises, generic headlines, missing guarantee/FAQ/PS, forced components, markup missing, any broken argument beat from self-contained reviewer, any unresolved "not okay" flag)

Pass/fail. If fail → loop back to Phase 2 with Priority Fix Stack. Max 2 loops before HITL escalation.

### Phase 4 — Polish + Pre-Ship Gate

**Polish passes:**
- `copy-editing` Sweep 8 (de-AI pass)
- `unslop` profile for "long-form-sales-letter"
- `brand-voice-guardian` final voice check

**Step 4a — Fresh-eyes audit [MANDATORY ship-gate]**

Spawn the `sales-letter-auditor` agent (`agents/sales-letter-auditor.md`) in an **isolated context window**. Do not run this in the generation session. The agent's value is that it has never seen this letter before. Contaminate it and you've wasted the step.

**Pass to the agent:**
- Path to finished letter: `clients/<slug>/copy/<YYMMDD>-<letter>.md`
- Client context directory paths: `offer.md`, `icp.md`, `buyer-profile.md`, `context-profile.json`
- Purpose of letter (from Phase 0 HITL output — one sentence)
- CTA target (from Phase 0 — one sentence)
- Final goal (from Phase 0 — one sentence)

**Do NOT pass:** generation conversation history, drafter's reasoning, alternative drafts, any "what we were going for" framing. That context defeats the isolation.

**Gate behavior:**
- Agent returns SHIP / HOLD — minor fixes / HOLD — blockers present / DO NOT SHIP.
- If SHIP → proceed to Step 4b.
- If HOLD or DO NOT SHIP → address every blocker listed in the ranked findings, then re-spawn the agent. Do not skip. Do not override. Letter does not ship until the agent returns SHIP or operator explicitly overrides WEAK marks with documented rationale.

**Pre-Ship Gate (`reviewers/pre-ship-checklist-reviewer.md`):** A higher-resolution structural audit that runs as the final gate before the letter ships. Five lenses with explicit pass/fail criteria — UMP clarity, identity-layer depth, headline-body coherence, concentration sharpness, CTA structural completeness. This is sharper than `copy-chief-reviewer` because each lens has named fail patterns and a quantitative pass threshold. Runs on a single artifact (no cross-artifact summary), produces a fix list ranked by impact.

If the pre-ship reviewer marks any lens as FAIL → letter does not ship until the proposed fix is applied. WEAK marks may ship with operator's explicit override.

**Optional 4th Phase 3 reviewer:** `reviewers/coherence-reviewer.md` — runs only when the letter has companion artifacts (other ads pointing to the same LP, an advertorial pair, an email sequence the letter inherits language from). Cross-document emotional + linguistic continuity check.

## Required Inputs

Load in order before drafting:
1. `clients/<slug>/context-profile.json` → identity foundation
2. `clients/<slug>/offer.md` → offer deliverables (verbatim)
3. `clients/<slug>/buyer-profile.md` → persona psychology
4. `clients/<slug>/avatars/` → DCT avatars from `/ads:avatars`
5. `clients/<slug>/source-of-truth.md` → paid ads research
6. `clients/<slug>/brand-voice.md` → voice target
7. `voice/<person>/*` → V.O.I.C.E. files
8. Meta Ads + GA baseline metrics (via `sheets-updater` or MCP) → Phase 3 GOAL threshold

If any critical input is missing, surface to user before drafting. Do NOT fabricate.

## Key References (load on demand)

- `prompt-template.md` — finalized prompt, copy-paste-ready for any LLM
- `references/copy-gems.md` — 11 techniques + verbatim quote library from 8 competitor scrapes
- `references/component-matrix.md` — context-aware inclusion logic + 5 cross-cutting requirements
- `references/guarantee-variants.md` — no-price guarantee patterns
- `references/frameworks.md` — Schwartz / Halbert / Sugarman distilled
- `references/competitor-analysis.md` — 8-page scrape findings (Brendon Luu, Syncom ×4, RoofGrow, Green Industry, Damien Tan)
- `references/objection-architecture.md` — 10 canonical objections × placement map × resolution patterns
- `references/qualification-patterns.md` — who-this-is-for / who-it-isn't-for / readiness-criteria blocks
- `references/trust-density.md` — 10 trust signals, confidence-credibility ratio, density calibration
- `references/mechanism-justification.md` — cause-and-effect logic (4 patterns) extending Component 5
- `references/cohesion-check.md` — stitcher transition test + Echo/Escalate/Pivot/Answer bridge patterns
- `references/markup-convention.md` — `(h)`, `(b)`, `(u)`, `*italics*` inline markup spec
- `reviewers/buyer-lens-reviewer.md` — subagent spec: prospect-lens review (Phase 3, MANDATORY)
- `reviewers/copy-chief-reviewer.md` — subagent spec: DR-strategist diagnostic review (Phase 3, MANDATORY)
- `reviewers/self-contained-reviewer.md` — subagent spec: kill-babies / self-contained experience / structural + language simplification review (Phase 3, MANDATORY — fires on every create AND every review)
- `reviewers/pre-ship-checklist-reviewer.md` — Phase 4 pre-ship gate: 5-lens structural audit (UMP / Identity / Headline-Body / Concentration / CTA) with quantitative pass criteria. Runs after polish, before ship.
- `reviewers/coherence-reviewer.md` — optional Phase 3 4th lens: cross-document emotional + linguistic continuity check. Run only when companion artifacts exist (paired ads + LP, letter + email sequence, etc.).

## Critical Rules

1. **Context-first, framework-second.** Skip components that don't fit. Never force all 12.
2. **Specificity beats cleverness.** Numbers, names, timeframes. "$526K every 4 years" beats "great returns."
3. **Proof-or-credentials.** No results yet? Pivot Proof Stack to credentials/methodology/sample work. Never fake testimonials.
4. **Light scarcity or none.** Heavy countdowns read as manipulation for high-ticket consulting.
5. **Guarantee is the primary conversion lever.** Not optional.
6. **FAQ + PS are non-negotiable.** 8/8 competitor pages scraped missed these — this is your moat.
7. **De-AI pass is mandatory before delivery.** No exceptions.
8. **No price anchoring.** This skill is for no-price lead-gen funnels.
9. **Chat-only output by default.** NEVER write the final letter or any draft artifacts to disk without explicit user approval. Full draft delivers in chat → user reviews → user says `y` / `save` / `ship it` → only then write to `clients/<slug>/sales-letters/<YYMMDD>-v1.md`. If user says `edit`, loop to Phase 2 stitcher. If `n`, discard. See `/content:sales-letter` command for full HITL approval gate spec.

## Common Failure Modes

- Forcing 12 components when 8 fit the offer
- Vague benefit promises with no numbers
- Generic headlines reusable by 10 other businesses
- Proof Stack that's "we're great" instead of identical-to-them results
- CTA that says "Submit" instead of outcome-language
- Heavy urgency that reads as manipulation
- Skipping FAQ because "it seems long" (it's 5 objections × 2 sentences)
- Forgetting to re-inject specific numbers after de-AI pass

## Related

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[sales-letter-auditor]] (agent, 0.14)

<!-- skill-graph:end -->
