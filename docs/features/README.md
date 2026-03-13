# Feature Tracker

Every feature gets its own file in this folder. Each file tracks the full lifecycle: idea → feasibility → build → test → ship → usage feedback.

## Feature Statuses

| Status | Meaning |
|--------|---------|
| `idea` | Just proposed, not yet assessed |
| `feasible` | Assessed, fits the codebase, ready to build |
| `parked` | Doesn't fit yet — moved to `feature-parking-lot.md` with trigger conditions |
| `building` | Currently being built |
| `testing` | Built, being tested for issues |
| `shipped` | Live and working |
| `needs-fix` | Shipped but has issues — fix details inside |
| `retired` | Removed or replaced |

## How It Works

1. **Jerel drops an idea** → Claude creates a feature file with `idea` status
2. **Feasibility check** → Claude honestly assesses fit, updates to `feasible` or `parked`
3. **Build** → Claude builds it, updates to `building`, logs what was created
4. **Test** → Run tests, update to `testing`, log results
5. **Ship** → Mark `shipped` with date
6. **Feedback loop** → Jerel uses it, updates satisfaction + usage frequency
7. **Fix cycle** → If issues, mark `needs-fix`, Claude fixes, back to `testing`

## Quick View

Run this to see all features and their status:
```bash
python3 docs/features/feature_tracker.py
```

## Files

- `README.md` — This file
- `feature_tracker.py` — Script to display status dashboard
- `FEATURE-NNN-slug.md` — One file per feature
