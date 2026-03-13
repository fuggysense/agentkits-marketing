---
description: Show current campaign progress dashboard
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [project-name] [campaign-slug]
---

## Context Loading

1. Load campaign-runner skill: `skills/campaign-runner/SKILL.md`

---

## Workflow

### Step 1: Identify Campaign

If arguments provided, load directly. Otherwise:

1. Trigger context gate if no project selected
2. List campaigns: `python3 skills/campaign-runner/scripts/state_manager.py list <project>`
3. If multiple campaigns, ask user to pick

### Step 2: Load State

```bash
python3 skills/campaign-runner/scripts/state_manager.py load <project> <campaign>
```

### Step 3: Display Full Dashboard

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

### Step 4: Offer Next Steps

**Options:**
- `/campaign:next` — Execute next priority actions
- `/campaign:schedule` — Schedule content via Postiz
- `/campaign:metrics` — Pull latest metrics
- `/campaign:report` — Generate performance report
