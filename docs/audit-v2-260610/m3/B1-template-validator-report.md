# M3 B1 — Template Rebuild + Validator v2

Task: rebuild `clients/_template/` to pass its own validator, then upgrade `validate-icm.sh` to a content-aware v2. Branch `rebuild-v2`. Date 2026-06-11 (SGT).

Owned scope: `clients/_template/**` + `~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh` (outside repo). Findings driven from `docs/audit-v2-260610/A-icm-compliance.md` (A-01..A-12).

## Result in one line

`_template` went from 3/7 PARTIAL to **10/10 PASS — ICM Compliant**. The validator now catches the three blind spots the audit named (L2 contract, L3→L4 grounding, persona-quote provenance), stops mangling numeric path prefixes, ignores `_archive/`, and reports empty skeletons as UNONBOARDED instead of letting them outrank live clients.

---

## Part 1 — Template changes

| File | Change | Before → After |
|---|---|---|
| `clients/_template/CLAUDE.md` | Cut to L0 identity + constraints + isolation contract. Relocated Folder Map, Campaign/Workspace/Concept routing to root CONTEXT.md (the canonical owner). Dropped booking/tracking row. | 197 → **91 lines** (R1 max 100) |
| `clients/_template/CONTEXT.md` | Absorbed the relocated routing as a tightened Campaign Discovery section incl. the Simple-concept route; trimmed Stage/Brand tables. | 127 → **73 lines** (R4 max 100) |
| `clients/_template/_brand/CONTEXT.md` | **New.** L3 factory contract in the exact 3-section form (Inputs/Process/Outputs), states the one-way L3→L4 rule. | absent → **26 lines** (satisfies R3 + R9) |
| `clients/_template/0{1..6}_*/CONTEXT.md` | Rewrote all 6 Jake stage contracts to the 3-section form, folding "skills available / out-of-scope / hand-off" into Process and "Done" conditions into Outputs. No content lost — relocated. | multi-section → **Inputs/Process/Outputs** (R9) |
| `clients/_template/_brand/booking.json`, `tracking.json` | **Removed** (`git rm`). | — |

### booking.json / tracking.json — justification for removal

No real client carries them (`grep` across `clients/` minus template/smoketest = only `_smoketest` mirrors them). No script or skill reads them (`grep -rl` over `*.sh,*.py,*.js` = zero). Both ship with empty values and a `_notes` field calling themselves "RECOMMENDED, not required." Dead scaffold. Git is the archive if a future site-bearing client wants them back. The CLAUDE.md isolation table lost its booking/tracking row to match.

### Broken pointers

After the rewrite, every relative ref in CLAUDE.md and root CONTEXT.md resolves (R6 PASS). The two that the old validator flagged as broken (`01_strategy/creative-diversity-map.json`, `02_ag1-options/concepts-draft.json`) are workspace-relative refs to runtime-generated outputs — real locations, files generated later. The v2 R6 resolves them (see Part 2).

---

## Part 2 — Validator v2

File: `~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh` (197→416 lines). Backup: `validate-icm.sh.bak-260611-m3` (confirmed present, same dir). `--json` contract kept and extended with an `onboarded` boolean; the per-rule output array now carries 10 rules instead of 7, same shape.

### (a) R6 pointer resolution — fixed two bugs

- **Numeric-prefix mangling (A-05).** Old regex `_[a-z]` started a match mid-token, so `00_inputs/...` became `_inputs/...` and got reported broken though the real file exists. New regex anchors on a path boundary (`[0-9]{2}_` as its own alternative) so `00_inputs/...` is captured whole. *(validate-icm.sh:~300, the `grep -oE` in the R6 loop.)*
- **Workspace-relative refs (A-05).** `ref_resolves()` now tries the anchor dir, the client root, and every concept-workspace base (template skeletons + any dir holding a `concept-brief.json`). For refs whose leaf is a runtime artifact, it accepts when the parent **phase folder** exists — R6 verifies the location is real, not that a not-yet-generated file already sits on disk. *(validate-icm.sh:~175-200.)*

### (b) `_archive/` + `_template.old/` excluded from all scans

`PRUNE_DIRS=( "_archive" "_template.old" )` feeds a shared `find_context_md()` and the R8/R10 finds. Fixes A-06: takekine's R4/R5 now PASS (its only "fails" were dead-folder `_archive/.../CONTEXT.md` files).

### (c) NEW R8 — L3 never references L4 by grounding

Greps `_brand/` for references to a **file** (path with extension) under a `campaigns/` or `output/` tree, skipping lines that are ownership/location disclaimers ("owned by", "does not write", "lives in/at", "do not duplicate"). This matches the audit's own severity split (A-04): it fires on takekine's `product-claim-context.md` sourcing claims from `campaigns/.../output/concept-input-packet-*.json` (the real circular-dependency violation) and passes harmony's benign asset-map table that merely names `campaigns/` as a location.

### (d) NEW R9 — L2 3-section contract

Every stage/room CONTEXT.md (numbered stage dirs, `_brand/`, `eval/`, concept-phase templates) must carry exactly `## Inputs` / `## Process` / `## Outputs`. Root CONTEXT.md (L1) and one-line phase-pointer stubs are exempt. Enforces SKILL.md:32 + checklist:222, the contract the audit (A-01) said was load-bearing and universally unmet.

### (e) NEW R10 — persona-quote provenance

In `_brand/buyer-profile.md` and `avatars/*`, any quoted phrase of 4+ words must have a source pointer on the line or within 2 lines (filename, citation marker, or source word). `[HYPOTHESIS]`-tagged lines and `{{...}}`/`[fill...]` template placeholders are exempt. Surfaces exactly the kind of invented-quote-on-money-path the audit reserved Critical for (open question #4).

### (f) Scoring v2 — UNONBOARDED

A client missing all three of CLAUDE.md + root CONTEXT.md + `_brand/` reports `onboarded:false`, score `-/N`, verdict UNONBOARDED — no numeric score. Fixes the inversion (A-02): the five empty skeletons no longer pass rules vacuously and outrank eugene.

---

## Tests (real output)

**Template, before:** `3/7 — PARTIAL` (R1 197 lines, R3 missing `_brand/CONTEXT.md`, R4 127 lines, R6 5 mangled/layered false positives).
**Template, after:** `10/10 — PASS — ICM Compliant`, exit 0. All ten rules green.

**R6 negative test** (fixture in `/tmp`): `00_inputs/input-manifest.json` (exists) NOT flagged and NOT mangled; `./_brand/does-not-exist.md` (genuinely missing) correctly flagged. Proves R6 was fixed, not disabled.

**R8 fires on takekine:** flags `_brand/funnel-research/voc/product-claim-context.md:35,37,98,135,...` citing `campaigns/test_2/01_research/output/concept-input-packet-*.json` — the A-04 headline violation the old validator was blind to. Passes harmony's `asset-map.md` ownership table.

**R9 fires:** the 6 legacy-format stage CONTEXTs in harmony (and the template, pre-rewrite) report their actual section sets vs the required three.

**R10 fires:** harmony `buyer-profile.md` → 5 unsourced quotes (objection lines like `"Is $89 really all I pay..."` with no source, no `[HYPOTHESIS]`). eugene avatars/ → 14+26+15+... unsourced.

**`_archive` exclusion:** takekine R4 + R5 now PASS despite many `_archive/.../CONTEXT.md` files present.

**JSON contract:** all 13 client JSONs in `docs/audit-v2-260610/baseline/post-m3/` parse with `jq -e .`. `onboarded` field present.

### Before → After (all clients, 7-rule → 10-rule)

| Client | Before | After |
|---|---|---|
| _template | 3/7 PARTIAL | **10/10 PASS — ICM Compliant** |
| harmony-wellness | 7/7 PASS | **8/10 PASS — Minor Issues** |
| takekine | 6/7 PASS-Minor | 7/10 PARTIAL |
| michelle-koh | 6/7 PASS-Minor | 8/10 PASS-Minor |
| hazecraft | 5/7 PASS-Minor | 8/10 PASS-Minor |
| neezanizam | 5/7 PASS-Minor | 5/10 FAIL |
| eugene-chieng | 3/7 PARTIAL | 5/10 FAIL |
| _smoketest | 3/7 PARTIAL | 5/10 FAIL |
| 1up-sales-ai | 4/7 PARTIAL | **UNONBOARDED** |
| aura | 4/7 PARTIAL | **UNONBOARDED** |
| fuggysmedia | 4/7 PARTIAL | **UNONBOARDED** |
| propwise-sg | 4/7 PARTIAL | **UNONBOARDED** |
| stackworks | 4/7 PARTIAL | **UNONBOARDED** |

The drops to FAIL/PARTIAL on live clients are the new content rules surfacing real debt (legacy stage contracts, unsourced quotes, takekine's L3→L4 grounding). Those clients are READ-ONLY in this task; their content was not touched. The lower scores are correct, not regressions.

---

## Acceptance

| Criterion | Status | Evidence |
|---|---|---|
| `_template` 7/7 (or 10/10 with new rules) | PASS | 10/10, exit 0 |
| validator `.bak` exists | PASS | `validate-icm.sh.bak-260611-m3` in same dir |
| new rules demonstrably fire | PASS | R8 on takekine, R9 on legacy stages, R10 on harmony/eugene quotes, R6 negative test |
| harmony-wellness still passes | PASS | 8/10 PASS — Minor Issues; all 7 original structural rules green; only the new content rules fire on its pre-existing debt |
| UNONBOARDED reporting works | PASS | 5 empty skeletons report `onboarded:false`, `-/N`, UNONBOARDED |

### Note on "harmony still passes"

harmony was the only 7/7 client. On the 10-rule scale it cannot hit 10/10 without editing harmony's own files (legacy stage CONTEXTs, unsourced quotes) — out of scope. It stays in the PASS family (8/10 PASS — Minor Issues) and passes all 7 original structural rules with no regression. That is the honest ceiling given the scope boundary. If the intent was a literal 10/10 for harmony, that requires a separate task to migrate harmony's content (the same rewrite this task did to the template).

---

## Out-of-scope observations (logged, not fixed)

1. **`research-brief.md` line 11** points at `_shared-knowledge/ferres/02-research-flow.md`. That file exists at the **repo root**, not under the client folder — so the reference is repo-root-relative, ambiguous inside a client. R6 doesn't scan research-brief.md so it isn't flagged. Left untouched (M2 file to preserve); fixing it would change the M2 contract.
2. **eugene-chieng + neezanizam** carry the same legacy debt the template had (197-line CLAUDE.md, multi-section stage CONTEXTs, unsourced avatar quotes). They are the next migration candidates — the template rewrite here is the template for that work.
3. **`_smoketest`** still mirrors the old template (booking/tracking present, no `_brand/CONTEXT.md`, oversized files). It scored 5/10 FAIL. It's a writable fixture; re-scaffolding it from the new template would be a clean follow-up but wasn't required here.
4. **R9 strictness vs spec budget.** R9 enforces the 3 sections but not the 200–500 token budget (SKILL.md:57); R4 still caps at 100 lines, which the audit (A-01 blind spot 2) flags as ~2× the token budget. Token-based budgeting was not in the B1 rule list — left for a later pass.
5. **SKILL.md terminology drift (A-06 §6).** The ICM SKILL.md names the factory `_shared-knowledge/` in its generic example while practice + the validator use `_brand/`. Doc-level fix, outside the validator.

## Files changed

- `clients/_template/CLAUDE.md` (197→91)
- `clients/_template/CONTEXT.md` (127→73)
- `clients/_template/_brand/CONTEXT.md` (new, 26)
- `clients/_template/01_research/CONTEXT.md` … `06_measure/CONTEXT.md` (6 files, rewritten to 3-section)
- `clients/_template/_brand/booking.json`, `tracking.json` (removed)
- `~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh` (197→416) + `.bak-260611-m3`
- `docs/audit-v2-260610/baseline/post-m3/*.json` (13 client validator outputs)
