# Correction Capture Rule

**When the user corrects any output during a session:**

1. Apply the correction immediately to the current work
2. Append to the relevant skill's `corrections.md`: `- YYMMDD | what was wrong → what was right | context`
3. If client-specific, ALSO append to `clients/<project>/learnings.md`

## What counts as a correction

- "Don't use that word/phrase" → log in the skill that produced it
- "The tone should be more X" → log in copywriting or brand-building
- "Always do X for this client" → log in client learnings AND the skill
- "That's not how we format this" → log in the skill that formatted it
- Rewriting/heavily editing Claude's output → diff key changes and log

## What does NOT count (skip)

- Clarifying a vague request ("I meant the pricing page")
- Choosing between options Claude presented
- Factual corrections ("the price is $49, not $39")

## Compounding loop

Per `skill-activation.md`: when a skill is activated, READ its `corrections.md` first. This is what makes the loop close — last session's corrections become this session's first-draft constraints.
