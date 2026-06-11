# Session End Protocol

Before ending any session:

0. **CLAUDE.md auto-capture:** Run `/ops:claude-md` — auto-scans the session for CLAUDE.md-worthy learnings (commands discovered, gotchas, patterns). Surgical edits with prune logic. Apply approved changes.

1. **Write ONE session handoff** to `_handoffs/<date>-<topic>.md`. This is the single session-memory convention. It replaces the old split across `session-state.md` + `open-threads.md` — one file per session, named by date and topic, so the next session reads one thing.

   - Date is `bash -c 'date +%y%m%d'` (never model knowledge). Topic is a short slug, e.g. `_handoffs/260611-rebuild-m2.md`.
   - Match the format of the existing `_handoffs/260611-rebuild-*.md` files: a `# Session Handoff — <title>` heading with date/branch/commit line, then `## Done` (what shipped, with file paths), `## Pending operator` (decisions waiting on Jerel, each pointing at its own file), and `## Next` (what the following session picks up).
   - Capture both confirmed patterns AND unfinished work in this one file. Do not reopen `session-state.md` / `open-threads.md` for new entries — they are legacy; this handoff is the bridge between sessions now.

2. **Mirror client handoffs:** Run `bash scripts/mirror_handoffs.sh`. It copies any `clients/*/SESSION-HANDOFF*.md` and campaign `_audit/session-handoff*` into `_handoffs/mirror/`, idempotently, so every client's latest handoff is findable from one folder. Read-only toward client folders; never deletes.

3. **Skill learnings capture:** If any skill or agent ran this session and produced a confirmed insight (something worked, something failed, a pattern was validated), append it to that skill's `learnings.md` under the right section. This is part of completing the work, not optional cleanup.

4. **Corrections triage:** Review `corrections.md` files appended this session. If a correction appeared 3+ times across sessions, promote it to the right section of that skill's `learnings.md` and remove it from `corrections.md`.

5. **Changelog:** If any skill/agent was created, updated, amplified, merged, or deleted → append an entry to `docs/changelog.md` under today's date. Ask for the "inspired by" source + contributor if the conversation doesn't make it clear. Verbs: `Created`, `Amplified`, `Updated`, `Merged`, `Deleted`.

6. **Living files update:** Review what you learned about the user and update:
   - `USER.md` — new tools, platforms, workflows, preferences, or context about Jerel.
   - `SOUL.md` — new communication patterns, writing rules, or formatting preferences observed.
   - Only add **confirmed patterns**, not one-off requests. If in doubt, skip.

## Periodic maintenance

During `/ops:monthly`, trigger `claude-md-improver` (plugin skill) to audit all CLAUDE.md files for quality, bloat, and staleness. Target score: B+ (75+/100). If the parent CLAUDE.md exceeds 80 lines, extract sections into `docs/system-rules/`.
