# Observation — thomson-reserve pipeline-state.json has no timestamp field (staged, not fixed)

**Date:** 2026-06-11 (rebuild M3.3 — pipeline-state validator).
**Why staged, not fixed:** neezanizam is a LIVE client; the rebuild treats its folders as read-only.

## What the validator caught

`clients/neezanizam/campaigns/thomson-reserve/dcts/pipeline-state.json` is the ONE real
state file that FAILS the permissive schema:

```
[FAIL] no WHEN field — none of: last_updated, updated_at, last_modified, created_date, created
```

It carries `built_260609` and "approved 260609" inside string values, but no top-level
date field, so freshness can't sort it. It also uses `phase` (not `current_phase`) and
omits top-level `client` — those are WARN-level (accepted aliases), not the failure.

## The fix (operator applies)

Add one line to the top-level object:

```json
"last_updated": "2026-06-09",
```

Optionally also add `"client": "neezanizam"` and rename `"phase"` -> `"current_phase"`
to clear the two warnings. None of these change meaning; they make the file sortable and
canonical. The launch state itself (`PARTIAL_UPLOAD__BLOCKED_SG_ADVERTISER_VERIFICATION`)
is a valid SHOUTING phase token and needs no change.

## Verify after applying

```bash
python3 scripts/validate_pipeline_state.py \
  clients/neezanizam/campaigns/thomson-reserve/dcts/pipeline-state.json
```

Expect `OK` (or warn-only if you skip the alias renames).
