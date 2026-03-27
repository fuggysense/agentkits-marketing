---
name: verification-loops
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: quality-assurance
difficulty: intermediate
description: >
  After completing a task, spawn reviewer agents to check the output for correctness, edge cases,
  and simplification. If issues are found, spawn a resolver agent to fix conflicts. Produces 2-3x
  quality improvement via agent-reviews-agent architecture. Chain: Implement → Review → Resolve.
triggers:
  - verify this
  - review loop
  - verification loop
  - self-review
  - agent review agent
  - double-check with a subagent
  - have another agent review this
  - get a second opinion
  - review and resolve
prerequisites: []
related_skills:
  - prompt-contracts
  - multi-agent-consensus
  - deep-research
agents:
  - brand-voice-guardian
  - conversion-optimizer
  - seo-specialist
---

## Graph Links
- **Feeds into:** (meta-skill -- quality gate)
- **Draws from:** (any skill output)
- **Used by agents:** (system-level)
- **Related:** [[multi-agent-consensus]]

# Subagent Verification Loops

After completing a task, spawn a reviewer agent with fresh context to audit the output. If the reviewer finds issues, spawn a resolver agent to reconcile. Chain: **Implement → Review → Resolve**. Repeat until clean or max iterations reached.

**Why this works:** Same reason human code review works — fresh eyes catch things the implementer misses. The reviewer agent has no sunk-cost bias from the implementation. It didn't write the content, so it doesn't defend the content. The resolver agent sees both perspectives (original + critique) and produces a synthesis that's better than either.

## Language & Quality Standards

**CRITICAL**: Respond in the same language the user is using.

## When to Use This Skill

- After writing campaign copy, ad creative, or landing page content
- After building a strategy doc or campaign plan
- When creating high-stakes deliverables (client-facing, paid media)
- After any complex multi-step output where quality matters
- User says "double-check that" or "verify this"

**NOT for:** Trivial edits, quick lookups, brainstorming drafts the user explicitly called "rough".

## Execution

### 1. Identify what to verify

Determine what output needs verification:
- **Copy just written** — ad creative, landing page, email sequence
- **Strategy/plan** — campaign plan, content calendar, pricing strategy
- **User-provided content** — user asks you to review their work
- **Any prior output** — user says "double-check that" or "verify this"

Gather the full artifact to review:
- The content/output itself
- The original requirements or brief that produced it
- Any relevant context (brand voice, ICP, offer docs, competitor examples)

### 2. Spawn the Reviewer

Spawn a single reviewer agent with fresh context. The reviewer has NO access to the implementation reasoning — only the output and the requirements. This is intentional: fresh eyes, no bias.

Config:
- `subagent_type: "general-purpose"`
- `model: "sonnet"` (default — use opus if the content is high-stakes or complex)

#### Reviewer prompt:

```
You are a senior marketing reviewer with fresh eyes. You did NOT create this content. Your job is to find problems.

ORIGINAL BRIEF/REQUIREMENTS:
{what the content was supposed to achieve}

CONTENT TO REVIEW:
{the full artifact}

CONTEXT:
{brand voice guidelines, ICP, offer, competitor examples, or other relevant files}

Review for:
1. **Effectiveness** — Does it actually achieve the brief? Will it convert/engage the target audience?
2. **Edge cases** — What audiences or scenarios would this fail for? Missing objections? Unclear CTAs?
3. **Simplification** — Is anything over-engineered or bloated? Can copy be tighter without losing impact?
4. **Brand consistency** — Does it match the brand voice, tone, and positioning guidelines?
5. **Accuracy** — Any factual claims that need verification? Misleading statistics? Compliance issues?

Respond in this exact format:

VERDICT: PASS | ISSUES_FOUND | CRITICAL

ISSUES (if any):
For each issue:
- SEVERITY: critical | major | minor | nit
- LOCATION: {section or line}
- PROBLEM: {what's wrong}
- FIX: {concrete fix — show the corrected version, not just "fix this"}

SIMPLIFICATIONS (if any):
- {what can be tightened or removed, with the simpler version}

SUMMARY: {one paragraph — overall assessment}

Be ruthless. Better to flag a false positive than miss a real problem. But don't invent issues that don't exist — if the content is strong, say PASS.

Write your response directly — do not write to any files.
```

### 3. Evaluate the review

Read the reviewer's output. Three possible paths:

#### Path A: PASS (no issues)
The reviewer found nothing wrong. Report to the user:
- "Verified by independent reviewer — no issues found."
- Include the reviewer's summary as confirmation.

#### Path B: ISSUES_FOUND (non-critical)
The reviewer found real issues but nothing catastrophic. Proceed to the Resolve step.

#### Path C: CRITICAL
The reviewer found a critical problem (brand violation, misleading claim, fundamentally wrong strategy). Flag immediately to the user before resolving — they may want to change approach entirely.

### 4. Spawn the Resolver (if issues found)

The resolver sees BOTH the original content AND the review. Its job is to produce a corrected version that addresses the review feedback while preserving the original intent.

Config:
- `subagent_type: "general-purpose"`
- `model: "sonnet"` (match the reviewer's model)

#### Resolver prompt:

```
You are a senior marketing editor resolving review feedback. You have two inputs:

1. ORIGINAL CONTENT:
{the original implementation}

2. REVIEW FEEDBACK:
{the reviewer's full response}

Your job:
- Fix every issue marked "critical" or "major"
- Fix "minor" issues unless the fix would add complexity disproportionate to the benefit
- Apply simplifications where the reviewer's suggestion is genuinely tighter
- Ignore "nit" level feedback unless trivial to address
- Do NOT introduce new sections or features beyond what the review requested

For each issue, either:
- FIXED: {show the fix}
- DECLINED: {explain why the reviewer's suggestion doesn't apply or would make things worse}

Then output the COMPLETE corrected content — not a diff, the full thing. The orchestrator will use this to replace the original.

Write your response directly — do not write to any files.
```

### 5. Apply the resolution

Read the resolver's output. You (the orchestrator) apply the corrected content.

Before applying, sanity-check:
- Did the resolver address all critical/major issues?
- Did the resolver break anything the original got right?
- Are any "DECLINED" decisions reasonable?

If the resolver's output looks good, apply it.

### 6. Optional: Loop (for high-stakes content)

For high-stakes deliverables (paid ads with budget, client-facing decks, email to large lists), run a second verification loop on the resolver's output.

**Max loops: 2.** If the content isn't clean after 2 review cycles, stop and flag to the user — there may be a deeper strategic problem that review can't fix.

Loop structure:
```
Round 1: Create → Review → Resolve
Round 2: Resolve output → Review → Resolve (if needed)
Done.
```

### 7. Write the verification report

Write to `active/verification/verification_report.md`:

```markdown
# Verification Report

**Artifact**: {what was reviewed}
**Date**: {date}
**Rounds**: {how many review cycles}

## Review Verdict: {PASS | FIXED | CRITICAL}

## Issues Found
| # | Severity | Location | Problem | Status |
|---|----------|----------|---------|--------|
| 1 | major | Hero headline | Weak value prop | Fixed |
| 2 | minor | CTA button | Generic "Learn More" | Fixed |
| 3 | nit | Footer | Spacing | Declined |

## Simplifications Applied
{What was tightened and why}

## Changes Made
{Summary of what changed between original and final version}

## Reviewer's Summary
{The reviewer's overall assessment}

## Resolver's Notes
{Any "DECLINED" decisions and reasoning}
```

### 8. Deliver results

Present to the user:
- **Verdict** — PASS (clean) or FIXED (issues found and resolved) or CRITICAL (flagged for user)
- **Issue count** — X issues found, Y fixed, Z declined
- **Key fix** — the most important thing that was caught
- **Confidence** — higher after verification than before
- File path to report

## When to trigger automatically

Use verification loops proactively (without the user asking) when:
- Writing ad creative that will have budget behind it
- Creating client-facing deliverables
- Writing email copy for large list sends
- Building strategy docs that will guide spending decisions

Do NOT auto-trigger for:
- Brainstorming and ideation (rough drafts by nature)
- Internal notes and documentation
- Quick iterations user explicitly said "just do it fast"

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| model | sonnet | Model for reviewer and resolver |
| max_loops | 1 | Review cycles (set to 2 for high-stakes) |
| severity_threshold | minor | Minimum severity to fix (minor, major, critical) |
| auto_apply | true | Apply fixes automatically or show diff first |

User can override: "review this with opus" or "do 2 rounds of verification".

## Cost considerations

- 1 round (reviewer + resolver) with sonnet: ~$0.10-0.20
- 1 round with opus: ~$0.50-1.00
- 2 rounds doubles the cost
- Very cheap relative to the quality improvement

## Edge cases

- **Reviewer finds no issues**: Great — PASS. Don't force a resolve step.
- **Reviewer hallucinates issues**: The resolver will catch this — if the "fix" doesn't make sense, the resolver should DECLINE it.
- **Resolver introduces new problems**: This is why round 2 exists for high-stakes content.
- **Reviewer and resolver disagree**: You (the orchestrator) break the tie.
- **Content is too large**: Split into logical sections and review each separately.
- **Existing report**: Overwrite `active/verification/` — these are ephemeral.
