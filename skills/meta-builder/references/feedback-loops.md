# Feedback Loops

How to build feedback loops into any agent or skill so it improves through use.

## 1. Self-Annealing Pattern

The artifact detects its own failures and updates its behavior.

### How It Works

```
Error occurs → Identify root cause → Update directive → Test fix → Confirm improvement
```

### Implementation

Add this to any agent or skill:

```markdown
## Self-Annealing

When output fails to meet quality criteria:
1. Identify which checklist item failed
2. Diagnose why (missing context? wrong format? bad assumption?)
3. Adjust approach for this session
4. Log the pattern: "When [trigger], do [adjusted behavior] instead of [original behavior]"
5. Apply the adjustment and re-generate
```

### Example

An SEO agent generates a meta description that's 200 characters (over the 160 limit):
1. Quality check catches: meta description too long
2. Root cause: didn't enforce character limit
3. Adjustment: "Always count characters before finalizing meta descriptions. Hard limit: 160."
4. Re-generates at 155 characters
5. Passes quality check

### For Skill Authors

Embed self-annealing in the skill's workflow:

```markdown
## Validation

After generating output:
1. Run quality checks (see Quality Checklist)
2. If any check fails, re-run the failed step with the error as context
3. Maximum 2 self-correction attempts before escalating to human
```

## 2. Performance Tracking

Track what works and what doesn't across uses.

### Implementation

Add to agent/skill output format:

```markdown
## Performance Notes

**What worked:**
- [Specific thing that produced good results]

**What didn't:**
- [Specific thing that fell short and why]

**Suggested improvements:**
- [Concrete change to make next time]
```

### For Agents

Agents should maintain an internal model of what succeeds:

```markdown
## Learning

After each interaction:
- Note which approaches the user approved vs. revised
- Adjust confidence levels: high-approval approaches get used first
- Flag patterns: "User always prefers X over Y for this type of request"
```

### For Skills

Skills track performance through success metrics in the registry:

```json
{
  "successMetrics": [
    "Output passes quality checklist on first attempt",
    "User accepts result without major revisions",
    "Execution completes without script errors"
  ]
}
```

## 3. HITL Gate (Human-in-the-Loop)

Critical decision points where a human must approve before proceeding.

### When to Use HITL Gates

- Before publishing or sending external communications
- Before making irreversible changes (deleting files, pushing to production)
- When confidence is below threshold (subjective quality, ambiguous requirements)
- When the output will be seen by external stakeholders

### Implementation

```markdown
## HITL Gate

Before finalizing:
1. Present the complete output to the user
2. Summarize key decisions made and alternatives considered
3. Ask: "Should I proceed, adjust anything, or take a different approach?"
4. Do NOT proceed until explicit approval
```

### Gate Levels

**Hard Gate** — Must get explicit "yes" before proceeding:
```markdown
STOP. Present output and wait for approval before:
- Sending emails
- Publishing content
- Modifying production systems
```

**Soft Gate** — Present output, proceed unless told to stop:
```markdown
Here's the draft. I'll finalize in this format unless you want changes.
```

**Informational Gate** — Notify, don't wait:
```markdown
FYI: I used approach X because of Y. Output follows.
```

## 4. Iteration Prompt

Every created artifact ends with an invitation to improve.

### The Standard Prompt

End every agent or skill output with:

> "Use this, then tell me what to improve."

This single line does three things:
1. Encourages actual use (not just theoretical review)
2. Generates real-world feedback (not hypothetical edge cases)
3. Creates a natural improvement cycle

### Variations by Context

**For agents:**
> "Try this agent on your next [task type]. Note where it helps and where it falls short, then we'll tune it."

**For skills:**
> "Run this skill on a real [input type]. If the output needs adjustment, tell me what to change."

**For templates:**
> "Use this template for your next [artifact]. Tell me which sections were useful and which felt like overhead."

## Wiring It All Together

When building a new agent or skill with meta-builder, include all four:

```markdown
## Feedback Loop

### Self-Annealing
[Specific self-correction rules for this artifact]

### Performance Tracking
[What metrics to track]

### HITL Gate
[Where human approval is required]

### Iteration
Use this, then tell me what to improve.
```

This creates artifacts that get better with every use instead of staying static.
