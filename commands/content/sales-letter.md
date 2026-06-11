---
description: "[DEPRECATED] Write a long-form direct-response sales letter for cold paid traffic (FB/IG ads) — 800-2000+ words. 5-phase pipeline with context-aware 12-component framework."
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [client-slug] [optional: offer focus]
deprecated: true
deprecation-note: "The /content:* family is superseded by /copy:* (see .claude/rules/_index.md). For sales letters use /copy:sales-letter (the sales-letter-method skill)."
---

> **DEPRECATED.** `/content:*` is superseded by `/copy:*` (see `.claude/rules/_index.md`). For long-form sales letters, use `/copy:sales-letter` (routes the `sales-letter-method` skill). Kept for reference only.

## Prerequisites

Before running this command:
- [ ] Client project exists at `clients/<slug>/` with `context-profile.json`, `_brand/offer.md`, `_brand/buyer-profile.md`
- [ ] Brand voice defined (`voice/<person>/` or `clients/<slug>/_brand/brand-voice.md`)
- [ ] If data-driven: Meta Ads + GA baseline metrics accessible (sheets-updater or MCP)
- [ ] Guarantee mechanic decided (or flagged for Phase 0 HITL resolution)

If any critical input is missing, surface before drafting. Do NOT fabricate.

---

## Context Loading (Execute First)

Load in this order:
1. **Skill:** `.claude/skills/sales-letter-method/SKILL.md`
2. **Prompt Template:** `.claude/skills/sales-letter-method/prompt-template.md`
3. **Component Matrix:** `.claude/skills/sales-letter-method/references/component-matrix.md`
4. **Guarantee Variants:** `.claude/skills/sales-letter-method/references/guarantee-variants.md`
5. **Copy Gems:** `.claude/skills/sales-letter-method/references/copy-gems.md`
6. **Frameworks:** `.claude/skills/sales-letter-method/references/frameworks.md`
7. **Client context:** `clients/<slug>/context-profile.json`, `_brand/offer.md`, `_brand/buyer-profile.md`, `_brand/brand-voice.md`, `source-of-truth.md` (if exists), `_brand/avatars/` (if exists)
8. **Voice files:** `voice/<person>/*`
9. **Corrections:** `.claude/skills/sales-letter-method/corrections.md` (hard constraints from past sessions)

---

## When to Use

**YES:**
- Cold FB/IG ad traffic → consultation booking funnel
- High-ticket service, consulting, coaching, agency, real estate
- Long-form letter (800-2,000+ words)
- No price disclosed on page

**NO — route elsewhere:**
- Short landing pages → `/content:landing`
- Pricing/feature/product pages → `copywriting` skill
- Email sequences → `/content:email`
- Ad creative → `/ads:big-angle-spotter`

---

## The 5-Phase Pipeline

### Phase 0 — Context Scan + HITL Gate

Auto-read client files, build component inclusion matrix. Present 1-screen review:

```
PHASE 0 SCAN — [client-slug]

Offer: [audit / consultation / strategy session]
Traffic: Cold FB/IG → Schwartz Level [2-3]
Baseline: [opt-in X%, CTR Y%, CPC $Z] OR [no data — target generic]

COMPONENT INCLUSION:
✓/✗ each of 13 components with reasoning

MISSING INPUTS:
[ ] any gaps flagged

Proceed? [Y/n] Adjust?
```

User confirms → Phase 1. User adjusts → update matrix → re-gate → Phase 1.

### Phase 1 — Parallel Drafting (2 Sonnet subagents)

Single message, 2 Agent calls in parallel:
- **Hook Half:** Components 1-4 (Headline + Sub + Lead + Pain Cycle + Integrity Tie-Down)
- **Commit Half:** Components 5-13 (Mechanism + Proof + Offer + Bonus + Scarcity + Guarantee + CTA + FAQ + PS)

Both agents receive:
- Full client context
- Component inclusion matrix from Phase 0
- `prompt-template.md` + `copy-gems.md` + `guarantee-variants.md`

Output: two half-letter drafts.

### Phase 2 — Stitcher (1 Opus agent) + Cohesion Check

Merges halves, smooths transitions, enforces voice consistency, deletes redundancy.

**Cohesion Check (required before handoff):**
- Run the 11-boundary test per `skills/sales-letter-method/references/cohesion-check.md`
- Score each transition: `continuous` / `bridge` / `jump`
- Auto-fail if any `jump` at critical boundaries: Headline→Sub, Sub→Lead, Lead→Pain, Pain→Mechanism, CTA→PS
- Rewrite all `jump` transitions using Echo / Escalate / Pivot / Answer bridge patterns
- Output: single cohesive draft + COHESION REPORT

### Phase 3 — Conversion Gate (3 parallel reviewers + synthesizer) [MANDATORY — no skips]

Fire 3 subagents in parallel via single message with 3 Agent tool calls. CRITICAL: all three receive the letter + context, but must NOT see each other's output. Independent diagnosis is the value. Skipping any reviewer = auto-reject the review as incomplete. This also applies when the user invokes `sales-letter-method` to review an existing letter outside the full pipeline — the three reviewers still fire together.

**Subagent A — Buyer Lens** (`skills/sales-letter-method/reviewers/buyer-lens-reviewer.md`):
- Simulates actual target prospect reading letter for first time
- No marketing jargon — plain-human reaction
- Outputs: First impression / Relevance / Trust / Desire / Friction / Decision / Suggestions / Final Yes-No
- Input: letter + persona file ONLY (no component matrix, no stitcher notes, no other reviewer output)

**Subagent B — Copy Chief** (`skills/sales-letter-method/reviewers/copy-chief-reviewer.md`):
- Elite DR strategist diagnosis (Schwartz/Ogilvy/Halbert/Hopkins lens)
- 10-point structural checklist (promise, audience, hook, clarity, structure, emotional progression, proof, mechanism, objections, CTA)
- Outputs: Overall verdict / Section-by-section / Priority fixes / Rewritten recommendations / Strategic takeaway
- Input: letter + full context + matrix + cohesion report (NO other reviewer output)

**Subagent C — Self-Contained Experience** (`skills/sales-letter-method/reviewers/self-contained-reviewer.md`) — **ALWAYS FIRES, NO EXCEPTIONS:**
- Treats the page as a cold, standalone read. Kills babies. Forgets "best practices."
- Two core questions: (1) Is it a complete argument a tired native-English SG reader can follow top to bottom? (2) How simple is the language — structural simplification then language simplification, thorough, so the reader never feels "not okay."
- Outputs: Complete Argument Check / Structural Simplification / Language Simplification (line-by-line) / "Not Okay" Flags / The One Question
- Input: letter + client context ONLY (no matrix, no cohesion report, no other reviewer output — keeps the lens clean of framework bias)

**Synthesizer step** (orchestrator runs this after all three return):
- Maps each buyer friction → self-contained cut or simplification → chief's strategic cause → single proposed fix
- Structural cuts + language simplifications from Subagent C take precedence over clever additions from Subagent B — simpler wins over smarter at the first pass
- Outputs **Priority Fix Stack**, ranked by: severity of buyer friction × ease of self-contained cut × alignment with chief diagnosis
- Adds Contract Validation overlay:
  - GOAL: opt-in > baseline × 1.5 (or target if no baseline)
  - CONSTRAINTS: voice verbatim, offer accuracy, no AI patterns, markup `(h)/(b)/(u)` present, proof numbers real, movement count ≤ 9, no unexplained acronyms/branded titles, no sentence > 25 words
  - FORMAT: 12 components + 5 cross-cutting requirements (objections / qualification / trust density / mechanism justification / cohesion) all present
  - FAILURE: vague promises, generic headlines, missing guarantee/FAQ/PS, forced components, markup missing, objections unhandled, no qualification block, any unresolved "Not Okay" flags from Subagent C, any broken argument beats from Subagent C

Pass/fail. If fail → loop back to Phase 2 with Priority Fix Stack. Max 2 loops before HITL escalation.

### Phase 4 — Polish

Sequential:
1. `copy-editing` skill Sweep 8 — de-AI pass (hard constraints from `overused-ai-patterns.md` + `corrections.md`)
2. `unslop` profile for "long-form-sales-letter" (if exists) OR generic AI-patterns profile
3. `brand-voice-guardian` agent — final voice consistency check

Output: final delivery draft.

---

## Interactive Parameter Collection

### Step 1: Confirm Client

**Question:** "Which client project is this for?"
**Options:** auto-populate from `clients/` directories (exclude `_template/`)

### Step 2: Offer Focus

**Question:** "What's the primary offer this letter drives to?"
**Examples:**
- Free consultation / audit / strategy session
- Discovery call
- Property valuation
- Lead magnet download (book funnel)
- Other (specify)

### Step 3: Scarcity Reality

**Question:** "Is there a real capacity limit?"
**Options:**
- Yes — specify number (e.g., "5 consultations/month")
- Yes — quality-gated (e.g., "30 bookings/month to maintain quality")
- No — skip scarcity component entirely

### Step 4: Guarantee Variant

**Question:** "Which guarantee mechanic fits this offer?"
**Options (from guarantee-variants.md):**
- No-pitch guarantee ("we'll end the call if not a fit")
- Value-pay guarantee ("$X if we waste your time")
- Outcome guarantee ("leave with 3 insights or we pay")
- Integrity layer ("I will NEVER…" triple-negative)
- Stack 2-3 of the above (recommended)

### Step 5: Proof Status

**Question:** "What proof assets does the client have?"
**Options:**
- Testimonials + case studies with specific numbers
- Testimonials but vague (need to tighten)
- Credentials only (no client results yet)
- Founder story only (new business)

If "credentials only" → Proof Stack pivots to methodology/credentials per `component-matrix.md`.

---

## Output Delivery — CHAT-ONLY BY DEFAULT

**Default mode: ALL output stays in chat. NO files are written until user explicitly approves.**

Deliver in this structure (all in chat):

1. **Phase 0 Summary** — component inclusion decision + reasoning
2. **Final Sales Letter** — ready-to-paste, 800-2,000+ words, formatted for readability
3. **Headline Variants** — 10-15 tested during drafting
4. **Conversion Gate Report** — Lens A friction heatmap + Lens B pass/fail log
5. **Steal-Reference Log** — which gems from `copy-gems.md` were used
6. **Flags** — missing inputs, unresolved questions, recommended next steps
7. **Pipeline Metadata** — which phases looped, total runtime, agents invoked

---

## HITL Approval Gate (MANDATORY before any file writes)

After delivering the full draft in chat, prompt:

```
Save draft? [y/n/edit]
  y     → write to clients/<slug>/sales-letters/<YYMMDD>-v1.md + metadata.json
  n     → discard, log session insights only
  edit  → specify changes, loop back to Phase 2 (stitcher)
```

**DO NOT write any files before this approval.** If user says "save," "ship it," "write it," or "looks good" unambiguously, treat as `y`. If unclear, ask again — never assume.

### On approval (y):
Write these files ONLY:
- `clients/<slug>/sales-letters/<YYMMDD>-v1.md` — final letter (auto-increment version if v1 exists: v2, v3, etc.)
- `clients/<slug>/sales-letters/<YYMMDD>-v1.metadata.json` — inclusion matrix, gems used, guarantee variant chosen, Meta Ads baseline at time of draft, pipeline runtime

### On edit:
- Capture user's specific change requests
- Route back to Phase 2 stitcher (not full re-draft)
- Return updated chat output
- Re-gate: "Save draft? [y/n/edit]"

### On reject (n):
- Discard the draft entirely
- Log any structural insights to `skills/sales-letter-method/learnings.md` (not the letter itself)
- Session ends

### Flags mode (--flags-only):
If user runs `/content:sales-letter <client> --flags-only`, return ONLY Phase 0 scan + flagged missing inputs. No drafting. Useful for pre-flight check.

---

## Critical Rules (enforce)

1. Context-first, framework-second. Never force components that don't fit.
2. Specificity beats cleverness. Numbers or nothing.
3. Proof-or-credentials. Never fake testimonials.
4. Light scarcity or none. No heavy countdowns.
5. Guarantee Stack is the primary conversion lever.
6. FAQ + PS are non-negotiable (8/8 competitor pages missed these).
7. De-AI pass is mandatory before delivery.
8. No price anchoring — this is a no-price lead-gen funnel.

---

## Failure Conditions (auto-reject)

- Any vague promise with no number
- Generic headline reusable by 10 other businesses
- Missing Guarantee component
- Missing FAQ or PS line
- CTA that commands action ("Submit") vs describes benefit
- Fake scarcity or testimonials
- AI-pattern language (detected by Sweep 8)
- Forced components that don't fit the offer

---

## Post-Delivery

1. Log session to `skills/sales-letter-method/learnings.md` if any confirmed insight emerged
2. Capture user corrections to `skills/sales-letter-method/corrections.md`
3. If letter performs in production (data-driven feedback), append wins to `clients/<slug>/learnings.md`
4. Optional: route to `/ads:feedback` after 1-2 weeks of deployed metrics for NEW/BETTER/MORE routing
