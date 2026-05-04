# Self-Annealing Rule

When an error occurs or a process fails:

1. **Fix** — Resolve the immediate issue
2. **Log** — Append the correction to the relevant skill's `corrections.md`: `- YYMMDD | what was wrong → what was right | context`
3. **Update** — Modify the directive/skill/agent that caused the failure
4. **Test** — Verify the fix works
5. **Strengthen** — The system is now more resilient than before the error

Every failure makes the system stronger. **Never fix the same error twice — always update the source.**

## Where corrections go

- Skill-level: `skills/<skill>/corrections.md`
- Agent-level: `agents/<agent>-learnings.md`
- Client-level: `clients/<slug>/learnings.md`
- Cross-cutting: `learnings/<domain>-learnings.md`

## When a correction appears 3+ times across sessions
Promote it from `corrections.md` to the appropriate section of `learnings.md`. Do this during `/ops:weekly` (corrections triage step).
