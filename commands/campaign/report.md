---
description: Generate campaign performance report
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [project-name] [campaign-slug]
---

## Context Loading

1. Load campaign-runner skill: `skills/campaign-runner/SKILL.md`
2. Load analytics-attribution skill: `skills/analytics-attribution/SKILL.md`
3. Load campaign state + all metric snapshots

---

## Workflow

### Step 0: Get Date
```bash
CURRENT_DATE=$(date +%y%m%d)
```

### Step 1: Load All Campaign Data

- Campaign state (tasks, assets, status)
- All metric snapshots from `metrics/`
- Published content list (post_ids, dates)

### Step 2: Ask Report Scope

**Question:** "What type of report?"
**Options:**
- **Quick** — One-page summary with key metrics
- **Weekly** — This week's progress and metrics
- **Full** — Comprehensive campaign performance report
- **Custom** — I'll specify what to include

### Step 3: Generate Report

#### Quick Report
```markdown
# [Campaign Name] — Quick Report ([date])

**Phase:** [phase] | **Progress:** [done]/[total] tasks ([%])
**Duration:** [start] → [current] ([N] days)

## Key Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| [metric] | [value] | [target] | [on/off track] |

## Highlights
- [top achievement]
- [top achievement]

## Next Steps
1. [action]
2. [action]
```

#### Weekly Report
Includes Quick + this week's completed tasks, content published, metric changes.

#### Full Report
Includes Weekly + full metric history, per-asset performance, ROI analysis, recommendations, risk assessment.

### Step 4: Save Report

Save to: `clients/<project>/campaigns/<campaign>/assets/reports/report-[date].md`
Register as asset in state.yaml.

### Step 5: Recommendations

Based on data, suggest:
- Tasks to prioritize next
- Content to double down on (top performers)
- Areas to optimize (underperformers)
- Budget reallocation (if paid media involved)

---

## Output Location

Report saved to campaign assets folder and displayed inline.
