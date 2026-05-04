# Open Threads — Cross-Session Work-in-Progress

Living list. Surface during session start protocol if relevant.

## Recurring scheduled checks

- **Upstream sync (every 3 days):** Run `git fetch upstream`. If new commits, show diff and ask before merging.
- **Weekly reference repo scan:** Once per week, run multi-repo sync check (see `docs/repo-sync-guide.md`). Fetch all reference remotes, summarize useful changes for Jerel to decide.
- **Ops review freshness:** Check `docs/ops/weekly/` and `docs/ops/monthly/` timestamps. Flag overdue.
- **Telegram bot maintenance:** Bot dies on Mac restart, context overflow, or power loss. Relaunch via `CHANNELS.md` quick launch. Re-register crons every session (auto-expire after 7 days).

## Phase work in progress

- **Phase 5 (Re-architecture):** see `task_plan.md`. 5.1 review complete. 5.3 (rules-index slim) in progress 2026-05-04. 5.2/5.4-5.7 pending.
