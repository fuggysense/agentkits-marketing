---
description: Execute next priority campaign actions
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [project-name] [campaign-slug]
---

## Context Loading

1. Load campaign-runner skill: `skills/campaign-runner/SKILL.md`
2. Load execution playbook: `skills/campaign-runner/references/execution-playbook.md`
3. Load project context: `clients/<project>/` (icp.md, offer.md, brand-voice.md)
4. Load V.O.I.C.E. files from `voice/<person>/`

---

## Workflow

### Step 1: Load Campaign State

```bash
python3 skills/campaign-runner/scripts/state_manager.py load <project> <campaign>
```

### Step 2: Get Next Actions

```bash
python3 skills/campaign-runner/scripts/state_manager.py next <project> <campaign>
```

### Step 3: Present Options

Show top 3 available actions with details:
```markdown
Next actions for [campaign name]:

1. **[Task description]**
   Agent: [agent] | Skill: [skill] | Phase: [phase]
   Dependencies: [met/list]

2. **[Task description]**
   ...

3. **[Task description]**
   ...
```

**Question:** "Which actions to execute?"
**Options:**
- **#1 only** — Execute first action
- **All 3** — Execute all available actions
- **Pick** — I'll choose specific tasks
- **Skip** — Show me the full task list instead

### Step 4: Execute Selected Tasks

For each selected task:

1. Load the assigned skill's SKILL.md
2. Route to the assigned agent (see execution-playbook.md)
3. Provide full context (project + voice + campaign state)
4. Agent produces output → save to `assets/`
5. **HITL gate**: Present output for approval before publishing
6. If approved and publishable → schedule/publish via MCP
7. Update task status in state.yaml

### Step 5: Save Progress

After all tasks complete:

1. Update `state.yaml`:
   - Mark completed tasks as `done`
   - Register new assets
   - Update `last_session` and `last_action`
   - Set `next_actions` for next session

2. Display summary:
```markdown
Session complete. State saved.
  [completed items with checkmarks]
  Next session: [upcoming actions]
```
