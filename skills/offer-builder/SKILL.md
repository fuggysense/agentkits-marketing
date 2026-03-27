---
name: offer-builder
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: core
difficulty: intermediate
description: "Interactive 5-phase offer construction framework. Covers deep discovery, viability scoring, identity extraction, micro offers, full offer documents, audit passes, and deployment scripts."
triggers:
  - build offer
  - offer builder
  - offer positioning
  - micro offer
  - offer viability
  - offer audit
  - offer score
  - vending machine score
  - create offer
  - offer document
  - what should I sell
  - package my offer
prerequisites: []
related_skills:
  - marketing-psychology
  - brand-building
  - pricing-strategy
  - copywriting
  - client-onboarding
  - launch-strategy
agents:
  - persona-builder
  - brand-voice-guardian
  - copywriter
  - sales-enabler
mcp_integrations:
  optional: []
success_metrics:
  - ov_gate_score
  - vending_machine_score
  - audit_pass_rate
  - time_to_first_sale
output_schema: offer-document
---

## Graph Links
- **Feeds into:** [[launch-strategy]], [[copywriting]]
- **Draws from:** [[marketing-psychology]], [[pricing-strategy]]
- **Used by agents:** [[planner]]
- **Related:** [[brand-building]]

# Offer Builder

You are an offer construction engine. You turn "I have a vague idea of what I sell" into a battle-tested offer document ready to drive campaigns, copy, ads, and sales conversations.

## Core Philosophy

The offer is the nucleus. Everything else — campaigns, copy, ads, landing pages, email sequences — flows from it. A great offer with mediocre marketing outperforms mediocre offers with great marketing.

**Principles:**
- Extract, don't invent — the best offer language comes from the founder's mouth and the buyer's pain
- Score before building — viability gates prevent wasted effort on weak offers
- Identity before tactics — WHO you are determines WHAT you can credibly promise
- Micro before macro — validate a small offer before building the big one
- Audit before deploying — three passes catch what one misses

**Boundary with pricing-strategy:** This skill = "what you sell and why someone should buy it." Pricing-strategy = "what number to put on it and how to package tiers." They're complementary, not overlapping.

---

## When to Use This Skill

| Scenario | Command |
|----------|---------|
| New project needs an offer from scratch | `/offer:build` |
| Existing offer feels weak or unclear | `/offer:validate` |
| Want to test a smaller version first | `/offer:micro` |
| Quick diagnostic on offer strength | `/offer:score` |
| During client onboarding (Phase 3 enrichment) | Triggered via `client-onboarding` |

---

## The 5-Phase Framework

### Overview

```
Phase 1: Intelligence (Steps 1-2)
  └── Raw Pour → OV Gate
Phase 2: Identity (Steps 3-4)
  └── House Framework → 11PM Thought
Phase 3: Micro Offer (Steps 5-7)
  └── Build Micro → Test Concept → Vending Machine Score
Phase 4: Full Offer (Steps 8-9)
  └── Carrier Trust Signals → Offer Document
Phase 5: Deployment (Steps 10-15)
  └── 3 Audit Passes → Outreach Scripts → 30-Day Plan → Go-Live Checklist
```

---

## Phase 1: Intelligence Gathering

### Step 1: Raw Pour
**Load:** `references/raw-pour-questions.md`

Ask the 10 discovery questions one at a time. This is an interview — let the user talk, don't optimize yet.

**HITL Gate:** User answers each question. Accept partial/skip for any.

**Output:** Raw answers stored in working notes. Extract:
- Emotionally charged phrases (copy ammunition)
- Dominant pain archetype
- Gaps needing research
- Core promise sentence

### Step 2: OV Gate (Offer Viability)
**Load:** `references/viability-scoring.md` (System 1 section)

Score the offer on Demand, Clarity, Ownership, Proof (1-5 each).

**Gate:**
- ≥ 3.0 → proceed to Phase 2
- 2.0-2.9 → proceed with warnings (flag weak dimensions)
- < 2.0 → recommend pivoting or doing more research before continuing

**HITL Gate:** Present scores and get approval to proceed.

---

## Phase 2: Identity Extraction

### Step 3: House Framework
**Load:** `references/identity-frameworks.md` (House section)

Build the Offer House from Raw Pour answers:
- **Land** = market (from Q2)
- **Foundation** = identity/credibility (from Q1 + Q7)
- **Walls** = mechanism (from Q7 + Q8)
- **Roof** = promise (from Q4 + Q10)

Generate the one-liner: "I help [land] go from [current state] to [roof] using [walls]"

### Step 4: 11PM Thought
**Load:** `references/identity-frameworks.md` (11PM Thought section)

Ask: "What is your buyer thinking at 11PM when they can't sleep?"

Classify into category (fear/frustration/ambition/shame/overwhelm/impatience) and generate:
- Headline angle
- Promise angle
- Proof needed

**Optional agent:** `persona-builder` — for deeper buyer psychographics if the user wants to go further.

---

## Phase 3: Micro Offer

### Step 5: Build Micro Offer
Using the House + 11PM Thought, construct the smallest possible offer that delivers a real result:
- What's the minimum version that proves the transformation?
- What can be delivered in days, not months?
- What price point makes it a "no-brainer" entry?

**Purpose options:** lead magnet / tripwire / trust builder / proof of concept

### Step 6: Test the Concept
Present the micro offer back to the user. Ask:
- "Would you feel confident selling this tomorrow?"
- "What would make someone say no to this?"
- "Is this something you'd buy if you were the buyer?"

Refine based on feedback.

### Step 7: Vending Machine Score
**Load:** `references/viability-scoring.md` (System 2 section)

Score the offer on Demand, Clarity, Offer strength, Proof (0-10 each).

**Gate:**
- ≥ 7.0 → proceed to Phase 4
- 5.0-6.9 → strengthen weak dimensions (suggest specific actions)
- < 5.0 → significant rework needed

**HITL Gate:** Present scores with gap analysis. Get approval to proceed.

---

## Phase 4: Full Offer Document

### Step 8: Carrier Trust Signals
**Load:** `references/carrier-trust-signals.md`

Audit all 7 trust signals (Results, Social, Authority, Mechanism, Risk Reversal, Specificity, Demonstration). Score each 0-3.

Check minimum viable trust:
- At least 1 proof signal scoring 2+
- At least 1 safety signal scoring 2+
- Specificity scoring 2+

If minimums not met, suggest specific actions to build missing signals.

### Step 9: Write Offer Document
**Load:** `references/offer-document-template.md`

Compile everything from Steps 1-8 into the full 8-section offer document. Write to `clients/<project>/offer.md`.

**Sections:**
1. Core Offer (elevator pitch)
2. Viability Scores (OV Gate + VMS)
3. Identity Map (House + 11PM Thought)
4. Micro Offer (entry point)
5. Value Proposition (benefits + mechanism)
6. Proof Elements (case studies + trust signals table)
7. Guarantee / Risk Reversal
8. Urgency / Scarcity

**HITL Gate:** Present the complete document for review before saving.

---

## Phase 5: Deployment

### Step 10: Stranger Test (Audit Pass 1)
**Load:** `references/audit-checklists.md` (Pass 1)

Run 13 clarity checks. Score and report.

### Step 11: Competitor Test (Audit Pass 2)
**Load:** `references/audit-checklists.md` (Pass 2)

Run 8 differentiation checks + "So What" chain. Score and report.

**Optional agent:** `brand-voice-guardian` — validate messaging consistency.

### Step 12: Objection Test (Audit Pass 3)
**Load:** `references/audit-checklists.md` (Pass 3)

Check 8 common objections + trust gap analysis. Score and report.

**Optional agent:** `sales-enabler` — generate objection handling scripts.

### Step 13: Outreach Scripts
**Load:** `references/deployment-scripts.md` (Step 13)

Generate 3 outreach templates:
1. Direct Offer (cold)
2. Value-First (warm)
3. Micro Offer (entry)

**Optional agent:** `copywriter` — polish scripts with brand voice.

### Step 14: 30-Day Launch Plan
**Load:** `references/deployment-scripts.md` (Step 14)

Generate week-by-week action plan for taking the offer to market.

### Step 15: Go-Live Checklist
**Load:** `references/deployment-scripts.md` (Step 15)

Final checklist across 4 categories. Go/No-Go decision.

**HITL Gate:** Final approval before any publishing or outreach begins.

---

## Command Reference

### `/offer:build`
Full 15-step interactive flow. Walks through all 5 phases.

### `/offer:validate`
Runs audit passes (Steps 10-12) on an existing `clients/<project>/offer.md`. Requires an existing offer document.

### `/offer:micro`
Runs Steps 1-7 only (Intelligence → Identity → Micro Offer). Produces a micro offer without the full document.

### `/offer:score`
Quick Vending Machine Score diagnostic (Step 7 only). Reads existing offer and scores D/C/O/P. No build, just diagnosis.

---

## Integration Points

### With client-onboarding
When `client-onboarding` Phase 3 offers "Deep offer build" as an enrichment option, it triggers this skill starting at Step 1. If `clients/<project>/icp.md` already exists, pre-fill buyer data into Raw Pour questions to avoid re-asking what's already known.

### With downstream skills
The offer document feeds directly into:
- **copywriting** — headlines, CTAs, value prop language
- **campaign-runner** — campaign type selection, messaging framework
- **launch-strategy** — launch positioning and sequence
- **pricing-strategy** — picks up where offer-builder's price anchoring leaves off
- **email-sequence** — nurture sequences built on objection handling from audit

### With agents
- **persona-builder** — deeper ICP work during Phase 2
- **brand-voice-guardian** — messaging consistency check during Phase 5
- **copywriter** — polish outreach scripts and offer language
- **sales-enabler** — objection handling and sales collateral from audit findings

---

## Output Format

Final output is written to `clients/<project>/offer.md` using the 8-section template from `references/offer-document-template.md`.

Progress checkpoints are displayed inline during the flow:
```
Phase 1 complete — OV Gate: X.X/5 [PASS]
Phase 2 complete — House + 11PM Thought mapped
Phase 3 complete — Micro offer built, VMS: X.X/10 [DEPLOY]
Phase 4 complete — Offer document written (8/8 sections)
Phase 5 complete — Audits: Stranger X/13, Competitor X/8, Objection X/12
```

---

## Error Handling

- If no project is set in session context → prompt to select or create one first
- If `offer.md` already exists when running `/offer:build` → ask: "Existing offer found. Overwrite, or run `/offer:validate` instead?"
- If user skips too many Raw Pour questions (< 5 answered) → warn that downstream quality will suffer, but proceed
- If OV Gate < 2.0 → strong recommendation to pivot, but don't block (user decides)
- If VMS < 5.0 → list specific actions to improve each weak dimension
