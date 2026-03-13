---
description: Pull latest campaign metrics from MCP integrations
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [project-name] [campaign-slug]
---

## Context Loading

1. Load campaign-runner skill: `skills/campaign-runner/SKILL.md`
2. Load analytics-attribution skill: `skills/analytics-attribution/SKILL.md`
3. Load campaign state

---

## Workflow

### Step 0: Get Date
```bash
CURRENT_DATE=$(date +%y%m%d)
```

### Step 1: Identify Available Data Sources

Check which MCPs are configured:
- Google Analytics → traffic, conversions, behavior
- Postiz → social engagement, reach, impressions per post
- HubSpot → email opens, clicks, form submissions
- Meta Ads → ROAS, CPC, CPL, conversions

List available vs. not-configured sources.

### Step 2: Pull Metrics

For each configured source, pull relevant data:

**Google Analytics:**
- Visitors, sessions, bounce rate
- Goal completions / conversions
- Traffic sources breakdown
- Top landing pages

**Postiz:**
- Per-post: impressions, engagement, clicks
- Platform-level: followers, reach, engagement rate
- Only for posts tracked in campaign state (by post_id)

**HubSpot:**
- Email sequence metrics: opens, clicks, replies
- Form submissions
- Contact lifecycle stage changes

**Meta Ads:**
- Campaign-level: spend, impressions, clicks, conversions
- ROAS, CPC, CPL, CTR

### Step 3: Save Snapshot

```bash
python3 skills/campaign-runner/scripts/state_manager.py metrics <project> <campaign> --add '{"source": "<source>", "data": {<metrics>}}'
```

### Step 4: Display Dashboard

```markdown
## Metrics Snapshot — [date]

### Traffic (Google Analytics)
| Metric | Value | vs. Last |
|--------|-------|----------|
| Visitors | X | +Y% |
| Signups | X | +Y% |
| Conversion | X% | +Y% |

### Social (Postiz)
| Post | Impressions | Engagement | Clicks |
|------|------------|------------|--------|
| [post] | X | X | X |

### Email (HubSpot)
| Sequence | Opens | Clicks | Replies |
|----------|-------|--------|---------|
| [seq] | X% | X% | X |

### Ads (Meta)
| Metric | Value |
|--------|-------|
| Spend | $X |
| ROAS | X.Xx |
| CPC | $X.XX |
```

### Step 5: Trend Analysis

If previous snapshots exist, show trends:
- Week-over-week changes
- Best/worst performing content
- Recommendations for optimization

**Data unavailable?** Show "NOT AVAILABLE" with setup instructions per data-reliability-rules.md.

---

## Output

Metrics saved to campaign state and displayed in dashboard.
Suggest `/campaign:report` for full performance report.
