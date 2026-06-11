---
description: Cross-client status board (no args) or single-campaign dashboard (with args)
version: "2.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: "[project-name] [campaign-slug] — omit both for the cross-client board"
---

## What this does

Two modes, decided by arguments.

- **No arguments → cross-client status board.** One line per client: where the work sits, what's next, who's blocking, plus a stale-state flag. This is the breadth view you run at the start of a session or when asked "where is every client / what's next / who's blocked".
- **Arguments given → single-campaign dashboard.** The depth view for one campaign: phase progress, last session, next actions, blockers, assets, metrics.

---

## Mode A — Cross-client board (no args)

Run the board and read it back to the operator. Nothing to load first; the script reads disk truth itself.

```bash
python3 scripts/status_board.py
```

Optionally narrow to named clients or get JSON:

```bash
python3 scripts/status_board.py eugene-chieng neezanizam
python3 scripts/status_board.py --json
```

Output format, one line per active campaign:

```
<client>: <campaign/workspace> @ <phase> — next: <action> — blocked on: <operator|client|gate|nothing>
```

A `[stale: ...]` tag means work landed on disk after the index was last bumped. Flag it to the operator and offer to update the index.

Engine and full behavior: `skills/status-board/SKILL.md`. The script is read-only (no network/Meta/sheet/render calls).

---

## Mode B — Single-campaign dashboard (args given)

### Step 1: Load campaign-runner

`skills/campaign-runner/SKILL.md`

### Step 2: Identify the campaign

If both args are present, load directly. Otherwise:

1. Trigger the context gate if no project is selected.
2. List campaigns: `python3 skills/campaign-runner/scripts/state_manager.py list <project>`
3. If multiple, ask the operator to pick.

### Step 3: Load state

```bash
python3 skills/campaign-runner/scripts/state_manager.py load <project> <campaign>
```

### Step 4: Show the dashboard

```markdown
## Campaign: [name] — Phase: [phase] ([done]/[total] tasks)

### Progress by Phase
| Phase | Done | Total | % |
|-------|------|-------|---|
| Planning | X | Y | Z% |
| Creation | X | Y | Z% |
| Execution | X | Y | Z% |
| Optimization | X | Y | Z% |

### Last Session ([date])
[last_action summary]

### Next 3 Actions
1. [task] ([agent] + [skill])
2. [task] ([agent] + [skill])
3. [task] ([agent] + [skill])

### Blockers
[list or "None"]

### Assets Created
- [asset] — [status]

### Recent Metrics
| Date | Metric | Value |
|------|--------|-------|
```

### Step 5: Offer next steps

- `/campaign:next` — execute next priority actions
- `/campaign:schedule` — schedule content via Postiz
- `/campaign:metrics` — pull latest metrics
- `/campaign:report` — generate performance report
