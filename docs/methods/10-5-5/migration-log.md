# 10-5-5 Migration Log

Running record of what changed each phase + verification results. Spec: `./SPEC.md`.

---

## Phase 1 — Spec + data model · 2026-06-03 · DONE
- Wrote `docs/methods/10-5-5/SPEC.md` (contract, 4 locked decisions, 5×2 data model, sheet row model, open items O1–O4, navigation map).
- Confirmed gitignore reality: `clients/*/` gitignored but **writable** from this background session (bgIsolation:none honored at startup, verified live). Corrected stale memory note.
- Key modeling insight: 5 angles × 2 variations means copy+headline are angle-scoped (1 each) → sheet adds ROWS (5/wave), not 5+5 columns. Maps onto the old "one row per creative" writer path.

---

## Phase 3 — Tracker schema + writer · 2026-06-03 · DONE (ran ahead of Phase 2 — cheapest high-value check)
- Wrote `skills/ad-concept-engine/references/dct-tracker-10-5-5.schema.json` (JSON Schema, draft-07).
- Wrote `skills/ad-concept-engine/references/sample-10-5-5-tracker.json` (5-angle reference fixture).
- **Key proof:** `ad_concept_sheet_writer.py` emits 5 CREATIVES + 5 COPY rows from a 5-angle tracker with **zero write-logic change** (it already iterates `creatives[]` one-row-per-entry). 10-5-5 = 5 `creatives[]` entries (one per angle), `copy_1`+`headline_1` filled, `copy_2`/`headline_2` empty.
- Writer changes (all backward-compatible, verified):
  1. **Lazy `gspread` import** — `from modal.sheets_writer import SheetsWriter` moved into the `if not dry_run` branch. `--mode dry-run` now runs with zero network deps (was a latent bug — dry-run promised "no sheet read/write" but couldn't import offline).
  2. **`_load_config` `_brand/` fallback** — checks `clients/<slug>/metrics-config.json` then `clients/<slug>/_brand/metrics-config.json`. Fixes a latent break: the 260504 reorg moved neezanizam/eugene-chieng/harmony-wellness configs to `_brand/` but the writer only looked at root. hazecraft (root) still works.
  3. **Method-aware preview** — when `dct_structure.method == "10-5-5"`, the COPY preview hides empty H2/Copy2 + shows a `**Method:**` line. 3-2-2 write payload byte-identical; preview gains one info line.
- Verified: 10-5-5 fixture → 5 clean rows; real 3-2-2 `dct-260421` → H1/H2/Copy1/Copy2 all still shown, `**Method:** 3-2-2` defaulted correctly. `py_compile` clean.
- Discovery: `clients/eugene-chieng/` already exists with `_brand/` — "Eugene" is partially onboarded (relevant to D4 Eugene-ready track).

## Phase 2 — Parametrize engines · 2026-06-03 · DONE (skills) / GLOBAL pipeline GATED
- Added an opt-in **"10-5-5 Mode"** section to each generator skill (parallel sub-agents, verified additive-only):
  - `skills/ad-concept-engine/SKILL.md` (+42, section at L660) — 5×2 data model, tracker schema pointer, 5-row sheet behavior, HITL gate changes.
  - `skills/headline-bank/SKILL.md` (+47, section at L255) — per-wave 5 angles × (1 copy + 1 headline), over-draft~5→narrow-to-1, aligns the 260418 corrections note.
  - `skills/big-angle-spotter/SKILL.md` (+27, section at L172) — top-5 angles + 2 image prompts/angle; manual fallback (does NOT touch the global pipeline).
- **Verified additive-only WITHOUT git** (skill files are untracked — no baseline): original 3-2-2 markers all still present (9/8/10 matches), new sections sit at the tail before the auto-gen footer, each opens with a "default is 3-2-2/unchanged" blockquote. `existing_content_modified=false` confirmed by content inspection.
- **GLOBAL pipeline (`~/AI workflows/big-angle-spotter/scripts/run_pipeline.py`) — GATED, NOT applied.** Designed change: add `--top-n` (default 3 = current behavior) driving `TOP3_SCHEMA` minItems/maxItems/rank-max (L191-209) + the "top-3"/"other two" prose in STEP_11 (L211-233) + the step-11/12 fan-out + `max_workers`; validate `top_n ≤ headline_count`. `--headline-count` already exists. ~5 edit sites, fully backward-compatible. Awaiting operator nod before applying (shared by other clients).
- Follow-up: run `link-skills.py` (skill-graph regen) — deferred to Phase 6; descriptions unchanged so low priority.

## Phase 4 — NeezaNizam proof wave · 2026-06-03 · DONE (authored + reviewed)
- Authored 5 angles × 2 for avatar-1 (The Hesitant Calculator) → `clients/neezanizam/campaigns/dct-10-5-5-proof-260603/dct-tracker.json` (+ folder CONTEXT.md). canva_link empty (production gate).
- Angles: A01 Closed Loop (decision-fatigue) · A02 She's Ready He's Not (wife tie-breaker) · A03 Full Waterfall (radical cost-transparency) · A04 Not Every Family (qualification filter) · A05 Solution Architects Not Salespeople (anti-sell pledge). Distinct mechanisms.
- **Mechanical: 19/19 PASS** (schema constants, 5 unique angle rows, naming contract, no em-dash/curly/alias).
- **Fresh-eyes review (2 cold reviewers, neither saw the drafting):**
  - Compliance → **PASS-WITH-FIXES.** 10/10 every hard rule; only soft gap = anti-hard-sell pledge in para 5 of A01-A04 (A05 leads with it). No kill.
  - Copy-quality → **REVISE.** Strong buyer-fit (A02 strongest, A04 weakest). Polish: dedup boilerplate (4/5 ads share it), re-lock A01+A05 headlines, differentiate A04 onto premium-tier, add a cost-of-inaction/regret beat, simplify A03 CPF line.
- Findings recorded: `clients/neezanizam/campaigns/dct-10-5-5-proof-260603/review-findings.md`. Shape VALIDATED; copy-polish = operator taste calls (open).

## Phase 5 — Sheets (LIVE) · 2026-06-03 · DONE (operator chose "test-tab write, canva blank")
- Env: installed gspread 6.2.1 into venv `~/.claude/venvs/sheets` (PEP 668 blocked system install; did NOT --break-system-packages). Service account `neezanizam@neezanizam-492212...` confirmed Editor access via read-only connection test.
- Created 2 NEW test tabs in the buyer-funnel workbook (14bh8k6S...): **CREATIVES_10x5x5_TEST** (gid 1443650484) + **COPY_10x5x5_TEST** (gid 1125162846), headers mirrored from live tabs. Live CREATIVES (1164222857) / COPY (1695031878) untouched.
- Writer: added `--allow-missing-canva` — a TEST-TAB-ONLY canva-gate bypass, structurally guarded (refuses unless BOTH target tab names contain "TEST"). Keeps the 260421 no-TBD rule ironclad on live tabs. py_compile clean.
- metrics-config: added `buyer-funnel-10-5-5-test` campaigns[] entry → test tabs. Backed up (`metrics-config.json.bak-260603-pre-10-5-5`); asserted the existing 2 campaigns survive byte-equal in data (meta_puller depends on them).
- Wrote the proof wave: 5 CREATIVES + 5 COPY rows landed. Read-back verified — DCT010-A01..A05, avatar-1 persona, 5 locked headlines present, canva blank, copy_2/headline_2 empty. Snapshots in `clients/neezanizam/sheet-snapshots/260603-1746-*`.
- **End-to-end proven in the live sheet: schema → tracker → writer → 5 angle-rows.**

## Phase 6 — Nav + recording · 2026-06-03 · DONE (recording) / a few manual follow-ups
- Created `clients/neezanizam/campaigns/_campaigns-index.json` (was MISSING) — generated from a real on-disk scan of all 6 dct-tracker.json files + the 3 metrics-campaign → workbook/gid map + a `method_reference` to the 10-5-5 spec. The orchestrator-navigation deliverable.
- Added 2 rows to `clients/neezanizam/CONTEXT.md` File-routing table → the campaign registry + the 10-5-5 method/spec/proof wave.
- Gated pipeline diff written up in full: `docs/methods/10-5-5/pipeline-diff-proposal.md` (operator chose "show me the diff first" — NOT applied; ready on his go).

### Manual follow-ups (not blocking; operator-owned)
- **Apply the gated `--top-n` pipeline diff** once reviewed (see pipeline-diff-proposal.md). Verify with the pipeline's `--dry-run`.
- **`link-skills.py`** skill-graph regen (3 skills edited; descriptions unchanged so low priority).
- **Commit** the untracked `skills/*/SKILL.md` + new `docs/methods/10-5-5/*` + the writer changes (I don't push without your say).
- **Copy polish backlog** (operator accepted proof as shape-proof): dedup boilerplate, re-lock A01/A05 headlines, differentiate A04, add regret beat — in `review-findings.md`. Apply only if these test-tab angles graduate to a real wave.
- **Open items O1-O4** in SPEC.md (Meta Flex attribution / meta_puller, asset-progression routing bug, DCT-ID collisions, Meta live-limit verification).
- Minor: in the sheet, the ANGLE column shows the full `angle_rationale` (3-paragraph). That's existing writer behavior (prefers angle_rationale over the short title) — fine for 3-2-2, but you may want a shorter ANGLE for 10-5-5 readability. Not changed.
- 260612 — Build #10 shipped: `scripts/ad-images/allocate.py` (allocate + --reconcile, dry-run default, two-file lockstep per locked contract). Sheet writer repointed: `ad_concept_sheet_writer.py` now reads `dct.json` natively (angles[] → 5 angle-rows adapter); legacy `dct-tracker.json` path unchanged. DCT010 img-01 ledger drift reconciled. Verified: dct.json dry-run (5 rows), legacy 3-2-2 dry-run (behavior identical), allocate dry-run (source-match slot pick).
- 260614 — Opus-workflow verification (6 agents) on the allocate + sheet-writer fixes: 4 PASS (neeza dct.json sheet write, legacy 3-2-2 back-compat, allocate reconcile+dry-run, allocate edge cases), 1 WARN (eugene DCT002 canva gate — operator-side, angles[] lack per-angle canva_link; same remediation as 3-2-2), 1 FAIL fixed. **Bug autopsy:** `allocate.py do_allocate` rollback only reversed the file move, not the already-saved `dct.json` — a ledger-write failure left dct.json `rendered` + ledger empty (out of lockstep), and the retry then refused 'pool full', orphaning the render until `--reconcile`. Violated the locked "nothing changed" contract. **Fix:** (1) `save_json` now atomic (temp + `os.replace`) — crash-safe; (2) `do_allocate` snapshots dct.json + ledger bytes pre-mutation and restores BOTH on any post-move failure; (3) honest error message; (4) `consistency_check` hardened with a reverse ledger-orphan scan + rendered-invariant check + target-driven cap. Reproduced the exact failure (read-only ledger dir) → confirmed full rollback (dct.json/ledger/render all restored, retry proceeds). Happy path + reconcile show no false positives.
