---
name: 6 Proof Types
source: cai #38, raw-newsletters/proof-arsenal-claude-project-skill.md
loaded_by:
  - builders/proof-inventory-builder.md
  - reviewers/proof-density-audit.md
  - reviewers/specificity-audit.md
  - reviewers/claim-verification-audit.md
purpose: Canonical taxonomy of the six proof types every claim in cold-traffic copy must be backed by, with placement strategy and stacking rules used by reviewers to score proof density.
---

# 6 Proof Types

## Canonical definition

Every piece of proof in direct-response copy falls into one of six categories. Each hits a different part of the buyer's brain. Stack them, and skepticism collapses. Most copywriters rely entirely on Type 1 (testimonials) and ignore the other five — that is leaving conversions on the table.

> "Every claim without proof is a leak in your conversion bucket. Most copywriters know they need testimonials. That's amateur hour. Professionals deploy six distinct proof types, strategically layered throughout their copy." — Mark Masters

## The 6 elements

### 1. Social Proof
Other people did this and got results. Testimonials, case studies, user counts, reviews.

- Example: "Over 14,000 copywriters have used this system"
- Example: A direct client quote with name and result attached
- When to use: Headlines (specificity + social), objection handling, close/CTA reinforcement, anywhere the reader needs "people like me succeeded."

### 2. Credentials Proof
Authority markers that establish expertise. Education, experience, publications, media mentions, client logos.

- Example: "After writing for Apple, Nike, and Salesforce..."
- Example: "Featured in Forbes, Entrepreneur, and Inc."
- When to use: Opening (establish authority fast — credential or screenshot in first 3 paragraphs), bio blocks, anywhere a "who is this person" objection arises.

### 3. Demonstration Proof
Show, don't tell. Screenshots, video walkthroughs, before/after comparisons, live examples.

- Example: A screenshot of actual results
- Example: A video of the product in action; side-by-side before/after
- When to use: Opening alongside credentials, mechanism explanations, anywhere a claim can be visually substantiated instead of verbally asserted.

### 4. Logical Proof
Reasoning that makes the claim inevitable. If-then arguments, analogies, mechanisms explained.

- Example: "Because the system automates your follow-up sequence, you're no longer limited by your own memory. Leads that would have slipped through now convert automatically."
- When to use: Objection handling (preempt "why should I believe this?"), mechanism reveals, complex/intangible benefits where no demo is possible.

### 5. Specificity Proof
Concrete details that signal insider knowledge. Specific numbers, exact processes, precise timeframes.

- Example: "2.3 pounds in 28 days" hits harder than "lose weight fast"
- Example: "Average implementation time: 23 minutes"
- When to use: Headlines, claim language throughout body, anywhere round numbers or vague language are leaking credibility. Specificity implies measurement, which implies truth.

### 6. Implied Proof
Proof embedded in how you communicate. Confidence, detail depth, casual mentions of results.

- Example: "When we rolled this out to our beta group last March..." implies a real history without explicitly claiming it.
- When to use: Close/CTA (reinforce results right before the ask), narrative passages, transitions — places where overt proof would interrupt flow.

## Application rules

> "Rule: Every major claim needs proof within 2 sentences. Stack multiple proof types for big claims." — Mark Masters

**Placement strategy (verbatim from the deployment guide):**

| Section | Best proof types |
|---|---|
| Headlines | Specificity, Social Proof |
| Opening | Demonstration, Credentials |
| Body / claims | Any — every major claim ≤2 sentences from proof |
| Objection handling | Social Proof, Logical Proof |
| Close / CTA | Social Proof, Implied Proof |

**Proof stacking:**
- Weak: single proof type per claim
- Strong: 2–3 proof types layered

Example stack from the newsletter:
- Claim: "This system works fast"
- Specificity: "Average implementation time: 23 minutes"
- Social: "James Chen had it running before lunch on day one"
- Demonstration: [Screenshot of setup-complete timestamp]

**Density target:** No major claim should sit naked. Every claim, promise, or assertion gets logged in the audit; "claims with proof / total claims" is the proof density score.

## Diagnostic / scoring

Reviewer protocol from the Proof Auditor SKILL.md:

1. **Identify Claims** — scan copy. List every claim, promise, or assertion.
2. **Audit each claim** — for each: Is it currently supported by proof? (Yes/No) If yes, what type? If no, flag as gap.
3. **Check inventory** — for each gap, identify available proof from `proof-inventory.md` that could fill it.
4. **Recommend fixes** — for each unproven claim suggest: which proof type to add, specific proof from inventory (if available), placement, whether stacking would strengthen it.
5. **Output**: Proof Audit Report.

Output format reviewers should produce:

```
## Proof Audit Report

### Summary
- Total claims found: X
- Claims with proof: X
- Claims without proof: X
- Proof density score: X%

### Claim-by-Claim Analysis
**Claim 1:** "[Exact claim from copy]"
- Current proof: None / [Type]
- Recommendation: Add [Type] — [Specific suggestion]
- Inventory match: [Yes/No] — [Specific proof asset if yes]

### Priority Fixes
1. [Most important gap] — [Why it matters]
2. [Second priority] — [Why it matters]
3. [Third priority] — [Why it matters]

### Missing Inventory
Proof you need to gather:
- [Type] for [claim] — Suggestion: [How to get it]
```

## Common failures

1. **Testimonial monoculture** — relying entirely on Type 1 and ignoring the other five. Amateur hour.
2. **Claim-without-proof gaps** — making claims with no supporting proof within 2 sentences. Each gap is a "leak in your conversion bucket."
3. **Single-type stacking on big claims** — one weak proof point on a load-bearing claim instead of 2–3 stacked types.
4. **Round-number vagueness** — using vague claims ("save time," "lose weight fast") when specificity proof ("14.3 hours per week within 60 days," "2.3 pounds in 28 days") is available.

## Exact prompts (verbatim from the newsletter)

**Custom Instructions for the Proof Arsenal Project:**

```
You are a direct response proof strategist. When auditing copy:
- Identify every claim that lacks supporting proof
- Reference proof-inventory.md for available proof assets
- Suggest specific proof placements using proof-deployment-guide.md
- Recommend proof stacking for major claims
- Flag proof gaps where no inventory exists (client needs to gather more)
```

**Proof Auditor SKILL.md frontmatter and process:**

```
---
name: Proof Auditor
description: Audits copy for proof gaps and recommends specific fixes
version: 1.0
author: Mark Masters
---

# Proof Auditor Skill

## Purpose
Analyze copy for unproven claims and recommend specific proof deployments.

## Process
### Step 1: Identify Claims
Scan the copy in current-copy.md. List every claim, promise, or assertion.

### Step 2: Audit Each Claim
For each claim, note:
- Is it currently supported by proof? (Yes/No)
- If yes, what type?
- If no, flag as gap

### Step 3: Check Inventory
Reference proof-inventory.md. For each gap, identify available proof that could fill it.

### Step 4: Recommend Fixes
For each unproven claim, suggest:
- Which proof type to add
- Specific proof from inventory (if available)
- Placement recommendation
- Whether proof stacking would strengthen it
```

**Inventory file structure (`proof-inventory.md`) writers should populate before auditing:**

```
# Proof Inventory

## Social Proof
- [Client name] — [Result] — [Quote if available]
- [User count, review stats, etc.]

## Credentials Proof
- [Background, publications, media mentions]
- [Client logos you can reference]
- [Awards, certifications, years of experience]

## Demonstration Proof
- [Screenshots available — describe each]
- [Videos available — describe each]
- [Before/after examples — describe each]

## Logical Proof
- [Key mechanisms you can explain]
- [Analogies that work well]
- [If-then arguments you've used]

## Specificity Proof
- [Specific numbers from real results]
- [Exact timeframes from case studies]
- [Precise process details]

## Implied Proof
- [Real events you can reference casually]
- [Beta groups, founding customers, etc.]
- [Historical details that signal legitimacy]
```

> "Claims are free. Anyone can make them. Proof is expensive. It requires real results, real customers, real data. That's exactly why it works." — Mark Masters
