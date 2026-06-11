# B2 — Canonical pipeline-state schema + index/state auto-sync

**Task:** M3.3 (canonical pipeline-state schema) + M3.4 (index/state auto-sync).
**Date:** 2026-06-11 (SGT) · Branch: rebuild-v2.
**Outcome:** all acceptance criteria met. One real state file fails the schema for a legit
pre-existing data gap (documented, read-only client, can't fix here).

## Changes (file:line)

### New — `scripts/pipeline_state_schema.json` (65 lines)
Permissive JSON-Schema-style spec doc. Three required identity families with accepted
aliases (WHERE = client/campaign or workspace path; PHASE = current_phase/phase/current_stage;
WHEN = last_updated/updated_at/last_modified/created_date/created). Known-phase enum is OPEN:
known tokens listed per lane (dct / video-concept / sales-letter), plus three structural
patterns accepted (`^phase_...`, `^x-...` custom, `^[A-Z_]+$` SHOUTING). Optional blocks
passthrough — extra keys never rejected. The `validator_contract` block names exactly which
conditions hard-fail vs warn.

Design note: I did NOT use the `jsonschema` library (not installed; install would need
network — forbidden). The validator implements the contract in plain Python so it runs with
zero deps. The schema file is the human-readable spec the validator follows.

### New — `scripts/validate_pipeline_state.py` (279 lines, executable)
- `validate_pipeline_state.py <file> ...` or `--all` (scans `clients/*/campaigns/**/pipeline-state.json`, skips `_archive`).
- HARD FAIL (exit 1): unparseable JSON · not an object · no WHERE field · no PHASE field · no WHEN field · null/empty phase.
- WARN (exit 0, or 1 under `--strict`): alias used instead of canonical · unrecognized non-x- phase value · `phases` not an object · non-ISO date string.
- Never auto-repairs. Every finding prints what's wrong + a `->` one-line fix + which file.
- `--strict` promotes warns to failures (for CI gating).

### New — `scripts/sync_campaign_indexes.py` (301 lines, executable)
- Regenerates `clients/<slug>/campaigns/_campaigns-index.json` from folder truth (a campaign dir = a direct child of `campaigns/` carrying real work: `campaign-index.json`, a state file, or a nested `pipeline-state.json`/`dct-tracker.json`/`dct.json`; denylist excludes `_example-campaign`, `_TEMPLATE`, `feedback`, `_sheet-snapshots`, dot-dirs).
- DEFAULT = dry-run diff (writes nothing). `--apply` writes. `--drift` = plain-language state-vs-folder report.
- Merges prior hand-authored metadata onto matching slugs (notes survive). `build_regenerated()` also RETAINS deliberately-archived index entries whose folder is gone (`is_archived_entry()` checks `status:archived` / `archived_at` / `archived_to`) so `--apply` never drops them — and `diff_lines()` excludes them from STALE noise.
- LIVE-client guard: `LIVE_CLIENTS = {eugene-chieng, neezanizam}`. `--apply` REFUSES to write their index; instead `write_or_stage()` drops `_campaigns-index.proposed.json` + an `APPLY-NOTE.md` (with a diff/cp command and a granularity-mismatch caution) under `_handoffs/staged-m3/<client>/`.
- Scope one client with `--client <slug>` or sweep all.

### Migrated — `clients/takekine/campaigns/test_2/`
- `state.yaml` -> `state.yaml.pre-m3` (archived in place, plain `mv` — client files are gitignored so `git mv` n/a).
- New `pipeline-state.json` (campaign-level, schema_version 1.0), equivalent content, zero data loss. PyYAML not installed; converted by hand. Validates `OK`.

### Edited — `commands/ops/daily.md:147` (Workflow section)
Added step 0 "State hygiene (run first)" — one line: run `sync_campaign_indexes.py --drift`, read-only, fix with `--apply`.

### New — `_handoffs/staged-m3/neezanizam/thomson-reserve-state-gap.md`
Documents the one legit schema failure + the one-line operator fix (read-only client).

## Tests (real output)

**1. Schema validates all real files OR documents failure** — `validate_pipeline_state.py --all`:
```
summary: 9 clean, 6 warn-only, 1 failed (16 checked)
failed files:
  - clients/neezanizam/campaigns/thomson-reserve/dcts/pipeline-state.json
```
The 6 warn-only files are real heterogeneous shapes (alias date fields, custom phase tokens,
`{{today}}` template placeholders) — all accepted by design. The 1 FAIL is thomson-reserve,
which genuinely has no top-level timestamp field (pre-existing gap; fix staged).

**2. Planted-invalid files fail loud + helpful** (3 cases, all exit 1):
- missing WHERE+WHEN: `[FAIL] no WHERE identity field — none of: client, campaign, ... -> add `client` + `campaign`, or a `workspace` path string`
- truncated JSON: `[FAIL] invalid JSON: Expecting property name ... at line 2 col 1 -> fix the JSON syntax (trailing comma? ...)`
- top-level array: `[FAIL] top-level value is a list, not a JSON object -> a pipeline-state file must be a single JSON object {...}`

**3. takekine migration** — `validate_pipeline_state.py clients/takekine/campaigns/test_2/pipeline-state.json` -> `OK`. Content parity spot-check: every yaml scalar (ag1_review, dr-foundation-pilot, 260519, video-brief-normalizer, blocked_until_ag2, both superseded slugs) present in the JSON. `state.yaml.pre-m3` archived alongside.

**4. Dry-run regenerates indexes incl. the two known-missing campaigns** — `sync_campaign_indexes.py` (dry-run):
```
=== eugene-chieng ===
  + MISSING from index: 'upgrader-ads' exists on disk (2 workspace(s) ...)
=== neezanizam ===
  + MISSING from index: 'thomson-reserve' exists on disk (1 workspace(s) ...)
```
Both known-missing campaigns surfaced. Writes nothing in dry-run.

**5. Live-client --apply refusal** — `--apply --client eugene-chieng`:
```
  STAGED -> _handoffs/staged-m3/eugene-chieng/_campaigns-index.proposed.json (live client, not written)
```
Same for neezanizam. Writable `_smoketest --apply` WROTE the index, registered all 3 missing
campaigns, and is idempotent (second run: "nothing to write — already in sync"). Eugene
proposal preserves the prior `primary_persona: avatar-1` metadata on the existing campaign.

**6. Compile/parse** — `py_compile` clean on both scripts; schema JSON parses.

## Acceptance status

| Criterion | Status |
|---|---|
| Schema validates all real state files OR documents each legit failure | PASS — 15/16 pass (clean+warn); 1 documented gap (thomson-reserve, staged) |
| Planted-invalid file fails with helpful message | PASS — 3 planted cases, all FAIL + `->` fix |
| takekine migrated + archived | PASS — pipeline-state.json validates OK, state.yaml.pre-m3 archived in place |
| Dry-run regenerates indexes incl. two known-missing campaigns | PASS — upgrader-ads + thomson-reserve surfaced |
| Live-client --apply refusal works | PASS — eugene + neezanizam staged, not written |

## Out-of-scope observations (logged, not fixed)

1. **thomson-reserve state file has no timestamp** — the one schema FAIL. Read-only client; one-line fix staged at `_handoffs/staged-m3/neezanizam/thomson-reserve-state-gap.md`.
2. **neezanizam index granularity mismatch** — the existing `_campaigns-index.json` registers individual DCTs (`dct-260417`, `W1_DCT1_...`) rather than the top-level campaign dirs (`buyer-funnel`, `asset-progression`). The sync script regenerates at campaign-dir granularity, so it flags all 6 DCT entries STALE and the 3 parent dirs MISSING. This is a real structural decision, not a bug — the staged APPLY-NOTE warns the operator NOT to blindly overwrite, and reconcile by hand. Not fixed (read-only + needs a human call on granularity).
3. **Two sibling untracked scripts** (`scripts/mirror_handoffs.sh`, `scripts/status_board.py`) appeared from a parallel M3 task — left untouched.
4. **Template state files carry `{{today}}` placeholders** — they warn on the non-ISO date. Correct behaviour (templates aren't live files); no action.
