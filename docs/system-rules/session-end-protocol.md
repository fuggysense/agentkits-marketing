# Session End Protocol

Before ending any session:

0. **CLAUDE.md auto-capture:** Run `/ops:claude-md` — auto-scans session for CLAUDE.md-worthy learnings (commands discovered, gotchas, patterns). Surgical edits with prune logic. Apply approved changes.

1. **Log decisions** to `learnings/session-state.md` under `## Confirmed Patterns`

2. **Skill learnings capture:** If any skill or agent was invoked this session and produced a confirmed insight (something worked, something failed, a pattern was validated), append it to that skill's `learnings.md` under the appropriate section. **This is not optional maintenance — it's part of completing the work.**

3. **Corrections triage:** Review corrections.md files appended to this session. If any correction appeared 3+ times across sessions, promote to the appropriate section of that skill's `learnings.md` and remove from `corrections.md`.

4. **Update directives** that were improved during the session

5. **Note unfinished work** in `learnings/open-threads.md`

6. **Changelog:** If any skill/agent was created, updated, amplified, merged, or deleted during this session → append entry to `docs/changelog.md` under today's date. Ask for "inspired by" source + contributor if not clear from conversation. Use verbs: `Created`, `Amplified`, `Updated`, `Merged`, `Deleted`.

7. **Living files update:** Review what you learned about the user this session and update:
   - `USER.md` — new tools, platforms, workflows, preferences, or context about Jerel
   - `SOUL.md` — new communication patterns, writing rules, or formatting preferences observed
   - Only add **confirmed patterns**, not one-off requests. If in doubt, skip.

8. **Persist context** across context window clears — these files are the bridge between sessions.

## Periodic maintenance
During `/ops:monthly`, trigger `claude-md-improver` (plugin skill) to audit all CLAUDE.md files for quality, bloat, and staleness. Target score: B+ (75+/100). If parent CLAUDE.md exceeds 80 lines, extract sections to `docs/system-rules/`.
