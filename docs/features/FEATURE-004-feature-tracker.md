---
number: "004"
name: "Feature Tracker"
status: "shipped"
proposed_date: "260312"
feasibility_date: "260312"
build_date: "260312"
shipped_date: "260312"
satisfaction: ""
usage_frequency: ""
production_ready: "yes"
---

# FEATURE-004: Feature Tracker

## Idea

What: Folder tracking all features through their lifecycle — idea → build → test → ship → feedback
Why: Need visibility into what's been added, whether it works, usage frequency, and production readiness
Proposed by: Jerel

## Feasibility Assessment

- **Fits current codebase?** Yes — markdown files + Python dashboard
- **Dependencies:** None
- **Effort estimate:** Small
- **Verdict:** Feasible

## Build Log

| Date | What was done |
|------|--------------|
| 260312 | Created `docs/features/` folder with README, template, tracker script |
| 260312 | Backfilled features 001-004 from this session |

### Files Created/Modified

- `docs/features/README.md`
- `docs/features/TEMPLATE.md`
- `docs/features/feature_tracker.py`
- `docs/features/FEATURE-001-campaign-runner.md`
- `docs/features/FEATURE-002-feature-parking-lot.md`
- `docs/features/FEATURE-003-help-commands.md`
- `docs/features/FEATURE-004-feature-tracker.md` (this file)

## Testing

| Test | Result | Notes |
|------|--------|-------|
| Dashboard display | | |
| Status filter | | |
| JSON output | | |

## Ship Notes

- **Shipped date:** 260312
- **How to use:** `python3 docs/features/feature_tracker.py` for dashboard
- **Known limitations:** Satisfaction + usage fields need manual updates by Jerel

## Usage & Feedback

| Date | Feedback | Action Taken |
|------|----------|-------------|
| | | |

### Satisfaction
**Rating:**
**Would I miss it if removed?**

### Usage Frequency
**Frequency:**
