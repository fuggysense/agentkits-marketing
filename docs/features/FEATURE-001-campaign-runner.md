---
number: "001"
name: "Campaign Runner"
status: "shipped"
proposed_date: "260312"
feasibility_date: "260312"
build_date: "260312"
shipped_date: "260312"
satisfaction: ""
usage_frequency: ""
production_ready: "no"
---

# FEATURE-001: Campaign Runner

## Idea

What: Full-stack campaign execution framework with state tracking across sessions
Why: Agent kit could strategize and create content but couldn't execute or remember progress between sessions
Proposed by: Jerel

## Feasibility Assessment

- **Fits current codebase?** Yes — extends existing skills/agents pattern
- **Dependencies:** PyYAML (Python), Postiz MCP (optional, for publishing)
- **Effort estimate:** Large
- **Verdict:** Feasible — built and shipped same session

## Build Log

| Date | What was done |
|------|--------------|
| 260312 | Created full skill: SKILL.md, execution playbook, state manager, 4 campaign templates |
| 260312 | Created 6 slash commands: new, status, next, schedule, metrics, report |
| 260312 | Created Postiz integration (index.md + config.json) |
| 260312 | Wired into CLAUDE.md, skills-registry, dependency-graph, clients README |
| 260312 | All 10 state_manager.py tests passing |

### Files Created/Modified

**New (18):**
- `skills/campaign-runner/SKILL.md`
- `skills/campaign-runner/learnings.md`
- `skills/campaign-runner/references/execution-playbook.md`
- `skills/campaign-runner/templates/state-template.yaml`
- `skills/campaign-runner/templates/campaign-types/product-launch.yaml` (12 tasks)
- `skills/campaign-runner/templates/campaign-types/content-seo.yaml` (8 tasks)
- `skills/campaign-runner/templates/campaign-types/lead-gen.yaml` (10 tasks)
- `skills/campaign-runner/templates/campaign-types/retention.yaml` (8 tasks)
- `skills/campaign-runner/scripts/state_manager.py`
- `skills/integrations/postiz/index.md`
- `skills/integrations/postiz/config.json`
- `clients/_template/campaigns/.gitkeep`
- `.claude/commands/campaign/new.md`
- `.claude/commands/campaign/status.md`
- `.claude/commands/campaign/next.md`
- `.claude/commands/campaign/schedule.md`
- `.claude/commands/campaign/metrics.md`
- `.claude/commands/campaign/report.md`

**Modified (4):**
- `CLAUDE.md`
- `skills/skills-registry.json`
- `skills/dependency-graph.md`
- `clients/README.md`

## Testing

| Test | Result | Notes |
|------|--------|-------|
| state_manager.py --test | PASS | 10/10 tests pass |
| YAML template validation | PASS | All 5 templates valid |
| JSON registry validation | PASS | skills-registry.json valid |
| Create campaign from template | PASS | Correct dir structure + state |

## Ship Notes

- **Shipped date:** 260312
- **How to use:** `/campaign:new`, `/campaign:status`, `/campaign:next`
- **Known limitations:** Postiz MCP not yet configured (needs VPS setup). Publishing defaults to manual until then.

## Usage & Feedback

| Date | Feedback | Action Taken |
|------|----------|-------------|
| | | |

### Satisfaction
**Rating:**
**Would I miss it if removed?**

### Usage Frequency
**Frequency:**

## Fix Log

| Date | Issue | Fix | Status |
|------|-------|-----|--------|
| | | | |
