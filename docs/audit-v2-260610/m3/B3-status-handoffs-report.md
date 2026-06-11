# B3 — /status capability + handoff system v2

Date: 2026-06-11 (SGT) · Branch: rebuild-v2 · Task: M3.5 + M3.6

## Summary

Built a cross-client status board (skill + script), upgraded `/campaign:status` to carry it, rewrote the session-end memory steps onto the single `_handoffs/` convention, merged the two handoff doc folders, and shipped an idempotent mirror script. Net-zero on root CLAUDE.md. No live-client writes, no network/Meta/sheet/render calls.

## Changes (file:line)

### New: scripts/status_board.py
Read-only, stdlib-only. One line per active campaign per client:
`<client>: <campaign/workspace> @ <phase> — next: <action> — blocked on: <operator|client|gate|nothing>`, capped under 40 lines.
- Truth precedence per campaign (`resolve_campaign`, line ~196): campaign-index.json → state.yaml → active workspace pipeline-state.json → folder mtimes.
- DCT-tracker shape handled separately (`resolve_tracker`, line ~163) — neezanizam's `dct-tracker.json` carries no phase string, so phase is synthesized from `metrics_campaign` + render/blocker signals; clients collapse to newest DCT per funnel (`scan_client`, line ~310) so a 2-funnel client shows 2 lines not 12.
- Stale flag (`resolve_campaign`, line ~258): fires when `last_updated` lags newest artifact mtime by >3 days.
- Blocker classification (`classify_block`, line ~131): gate > operator > client > nothing, heuristic from phase/next/blocker text.
- `--json` and per-client-name args supported.

### New: skills/status-board/SKILL.md
Triggers (`where is every client` / `what's next` / `status board` / `who is blocked`), runs the script, interprets the four blocker states, points to `/campaign:status` for the depth view. Registered in `.claude/skill-graph.json` via `scripts/link-skills.py` (2 references confirmed).

### New: scripts/mirror_handoffs.sh
Idempotent (content-compare via `cmp -s`, never deletes). Copies `clients/*/SESSION-HANDOFF*.md` → `_handoffs/mirror/<basename>` and campaign `_audit/session-handoff*` → `_handoffs/mirror/<client>-<basename>`. Naming matches the established mirror state exactly. Prunes `_archive` / `_template*`.

### Upgraded: commands/campaign/status.md (v1.0.0 → v2.0.0)
Replaced the body in place (no duplicate command). Two modes: no args = cross-client board (runs `status_board.py`); args = the original single-campaign deep dashboard (campaign-runner state_manager, progress table, next-3-actions, blockers, assets, metrics — preserved verbatim as Mode B).

### Rewritten: docs/system-rules/session-end-protocol.md
Memory steps collapsed to ONE convention: step 1 now writes `_handoffs/<date>-<topic>.md` (format anchored to existing `260611-rebuild-*.md` files), step 2 runs `mirror_handoffs.sh`. `session-state.md` + `open-threads.md` marked legacy (new entries go to the handoff). Non-memory steps preserved: claude-md auto-capture (0), skill-learnings (3), corrections triage (4), changelog (5), living files (6), periodic maintenance.

### Merge: docs/handoff/ → docs/handoffs/
`git mv docs/handoff/2026-04-24-copywriting-os-phase-1.md docs/handoffs/` (rename tracked, history preserved). Both folders' files now live in `docs/handoffs/` (plural, canonical, 2 files). Pointer left at `docs/handoff/README-MOVED.md`. No name collisions.

### Root CLAUDE.md (net-zero)
- ADDED under Startup files: `Where is every client / what's next? → /campaign:status (no args = cross-client board, scripts/status_board.py). Session memory lives in _handoffs/<date>-<topic>.md`.
- REMOVED from Reference-files table: `| Learnings + session state | learnings/*.md (see _index.md) |`.
- Justification: the removed row is redundant — `.claude/rules/_index.md` (already the "start here" pointer on the line above the table) carries a full `## On-demand learnings` section registering `session-state.md` / `open-threads.md` / `telegram-debugging.md`. The protocol rewrite also demotes session-state/open-threads to legacy. Removing the row orphans nothing; learnings stay discoverable via `_index.md`.
- `git diff --numstat CLAUDE.md` → `1  1` (one added, one removed).

## Tests (real output)

### Status board matches disk truth for the 4 named clients
```
eugene-chieng: mp1-upgrader-letter-260603 @ body-draft-v3-in-review — next: Re-run eval gate on body v3; resolve Eugene-side ops flags... — blocked on: gate
neezanizam: dct-10-5-5-proof-260603 @ buyer-funnel / images-pending (10-5-5) — next: Render the 10 image_prompts -> image-generation (Nano Banan... — blocked on: gate  (+4 more campaign folders)
neezanizam: dct-260419 @ asset-progression / images-pending (3-2-2) — next: # 1. Preview Wave 2 sheet write... — blocked on: gate
takekine: test_2 @ ag1_review_pending_operator_taste_pass — 3-conc... — next: Operator reviews the AG1 page... — blocked on: gate  [stale: index 2026-05-21 < artifact 2026-06-11]
```
Cross-checked each surfaced field against source files:
- eugene: index `current_stage: body-draft-v3-in-review`, `next_action` = "Re-run eval gate on body v3...", `operator_review_required: true` → matches.
- neezanizam buyer-funnel: `dct-tracker.json next_commands[0]` = "Render the 10 image_prompts...", `metrics_campaign: buyer-funnel`, method 10-5-5 → matches.
- neezanizam asset-progression: `dct-260419` `metrics_campaign: asset-progression` → matches (2nd funnel correctly split).
- takekine: index `current_stage: ag1_review_pending_operator_taste_pass`, `next_action` = "Operator reviews the AG1 page...", `last_updated: 2026-05-21` < 2026-05-29 artifacts → stale TRUE POSITIVE.

Full board: 16 lines (cap 40). `--json` mode and per-client filtering verified.

### Mirror idempotency (run twice, same result)
```
mirror hash before runs: a53a6fada70d4b4c0831f9a76dbd5670
mirror hash after 2 runs:  a53a6fada70d4b4c0831f9a76dbd5670
IDEMPOTENT: identical ✓
second-run output: mirror_handoffs: 0 copied, 4 unchanged. (orphaned mirror files preserved.)
```
Copy path separately proven with a temp source in writable `clients/_smoketest/`: RUN 1 copied 1 (content matched by `cmp`), RUN 2 copied 0; temp source + mirror copy cleaned up, mirror restored to its original 5 files (orphan `CODEX-HANDOFF-video-pipeline.md` preserved).

### Static checks
- `python3 -m py_compile scripts/status_board.py` → OK.
- `bash -n scripts/mirror_handoffs.sh` → OK. (shellcheck not installed on box — stated, not claimed.)

### Net-zero + no live writes
- `git diff --numstat CLAUDE.md` → `1 1`.
- `git status --porcelain | grep clients/(eugene-chieng|neezanizam|takekine)/` → NONE. Live clients untouched.

## Acceptance status

| Criterion | Status | Evidence |
|---|---|---|
| Status output matches disk truth for 4 named clients | PASS | Field-by-field cross-check above (eugene, neezanizam ×2 funnels, takekine) |
| Net-zero diff shown | PASS | `git diff --numstat CLAUDE.md` = `1 1`; added/removed lines justified |
| Protocol rewritten to ONE convention | PASS | session-end-protocol.md step 1 = `_handoffs/<date>-<topic>.md`, step 2 = mirror script |
| Merge done with pointer | PASS | `git mv` rename + `docs/handoff/README-MOVED.md`; both files in `docs/handoffs/` |
| Mirror script idempotent (run twice, same result) | PASS | Identical hash before/after 2 runs; copy path also proven + reverted |
| `/campaign:status` upgraded not duplicated | PASS | Edited in place to v2.0.0; Mode A (board) + Mode B (original dashboard preserved) |

## Out-of-scope observations (logged, not fixed)

1. **takekine pipeline-state.json mtime 2026-06-11 11:36** — the test_2 root `pipeline-state.json` was touched today by a sibling task (likely B2's Gate-2 state.yaml migration). Not mine; I made zero writes to takekine. The stale flag's displayed artifact date reflects this, but the flag itself is a true positive (index 2026-05-21 genuinely lags the 2026-05-29 video-concept artifacts).
2. **neezanizam index data-quality** — `dct-260417` carries `metrics_campaign: "buyer-funnel (inferred from CLAUDE.md)"` (parenthetical noise). The board normalizes this for the funnel-collapse, but the index entry itself should be cleaned to a bare `buyer-funnel` so downstream tooling doesn't have to strip it.
3. **aura / 1up-sales-ai / others have campaign folders but no `_campaigns-index.json`** — aura has 3 (`brand-outreach`, `reddit-seeding`, `tiktok-slideshows`). The board surfaces this as "unindexed — register campaign in _campaigns-index.json". A registry backfill for these clients would make the board fully accurate for them (currently folder-truth only).
4. **`_smoketest` campaigns** (`tr-smoketest`, `wave-smoke-*`) carry only `path` + `workspace_count`, no campaign-index/state — they show "unknown / none recorded". Correct behavior for stub test fixtures; noting in case the smoke harness wants real state files.
5. **`docs/handoffs/metrics-automation-handoff.md` and the copywriting-os file** are engineering handoffs; `_handoffs/` at root is session memory. The README-MOVED pointer documents this split, but the two namespaces ("docs handoffs" vs "root handoffs") could still confuse a fresh agent. Left as-is per scope.
