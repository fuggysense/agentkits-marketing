# Handoff — 10-5-5 Pipeline Consolidation + Eugene SA (260616, ~01:30 SGT)

**For:** Jerel, next session (and a fresh agent).
**How to start tomorrow:** read this file top to bottom, then jump to "§7 Do this first."

---

## 1. TL;DR — where we are

You wanted the ad pipeline **solid enough to run continuously, across multiple clients**: spin creatives + copy → launch 10-5-5 → track results → make/refine angles from what worked → repeat, with competitor copy as a feed-in.

The build is **mostly there on the CREATE side, weak on the LEARN side.** The single most important thing to understand:

> **10-5-5 Meta Flexible Ads cannot tell you which of the 5 angles won.** Meta mixes the pool and reports one blended number per ad set + rough per-image CTR (no per-angle conversions). So "track results → make new angles from what worked" is **broken at the data layer, not the tooling layer.** This is the heart of your vision and it needs a decision (see §5). It is not a bug we can code away — it's how Meta Flex works.

Everything else is normal build/wiring work.

---

## 2. What got DONE this session (all committed, local only, nothing pushed)

On branch `rebuild-v2`; `main` fast-forwarded locally. Commits:

- `6e6355e` — 10-5-5 finalization (dct.json sheet writers + ad-concept-engine/headline-bank)
- `ffaf5ea` — new skills (metrics-wire, offer-validation) + psych-coverage method landed
- `6f91452` — rebuild-v2 skill/agent/routing sweep + meta-publish-gate hook
- `083a43b` — **renamed `tr_10_5_5_sheet_writer.py` → `dct_10_5_5_sheet_writer.py`** (+ 3 live references; dated audit docs left as history)
- `5d351e0` — fixed a **stale docstring** that falsely said the live-write path wasn't built (it is)

Also: psych-coverage P1 cleanup (deleted the WIP breadcrumb, kept the canonical `v2-tag-schema.md`).

**Corrections to earlier wrong assumptions (verified this session):**
- The 10-5-5 sheet writer's live-write path **is fully built** (writes via `gws`). Earlier "not implemented" was a stale comment.
- **Eugene uses `ad_concept_sheet_writer.py`** (per-angle rows); the renamed `dct_10_5_5_sheet_writer.py` is the **Thomson** per-DCT writer. Two writers, two jobs — not one.
- The **Meta "bundle" is dead weight.** The `meta` CLI already does 10-5-5 (`--images ×10 --titles ×5 --bodies ×5`). The Thomson upload bypassed the bundle and went straight to Graph. **Don't build a bundle adapter — use the `meta` CLI directly.**
- The `--top-n 5` change to big-angle-spotter **is applied + dry-run-verified** but **uncommitted** (it's a separate repo; its hardening edits are still pending your review).

---

## 3. Eugene service account — STARTED, blocked on 2 things you must do

I created it under `jerel@genflos.com` (your `gcloud` login worked):
- **Project:** `eugene-chieng-ads` (ACTIVE) — Sheets + Drive APIs enabled
- **Service account:** `eugene-sheets@eugene-chieng-ads.iam.gserviceaccount.com`
- Deleted the stray `eugene-chieng-mktg` project I'd made earlier under jinoxlr8 (wrong identity).

**Two blockers, both need YOU:**

1. **The SA key is blocked by a genflos org policy** (`iam.disableServiceAccountKeyCreation`), and your genflos account lacks `orgpolicy.policyAdmin` to override it. Without a key, the SA can't authenticate. Options:
   - **(A, fastest — recommended interim)** Don't make a per-client key at all. Reuse the **existing NeezaNizam SA** (`neezanizam@neezanizam-492212.iam.gserviceaccount.com`, key already in `scripts/modal/credentials.json`) as a shared agency writer — grant it Editor on every client sheet. One key, every client tracked. Sidesteps the org policy entirely.
   - **(B, cleaner, slower)** Get a genflos Workspace **org-admin** to allow key creation for the `eugene-chieng-ads` project (relax `iam.disableServiceAccountKeyCreation`) or grant you `orgpolicy.policyAdmin`. Then I mint the dedicated key.
   - **(C)** Keyless impersonation — more code, still needs a live human token, defeats "validate once." Not recommended.

2. **gws is NOT actually authed** — your login refreshed `gcloud` but `gws` returns `invalid_rapt` (a reauth challenge it didn't finish). So I couldn't grant the SA on Eugene's sheet. **Fix:** run `! gws auth login` and complete the browser reauth fully (it may force a fresh consent / 2FA "reauth" step — that's the RAPT challenge).

**Net:** once (2) is fixed I can grant whichever SA you pick on the sheet in one command; once the key question (1) is settled, Eugene writes work.

---

## 4. The two writers + auth, plain version

| Writer | Used by | Writes via | Status |
|---|---|---|---|
| `ad_concept_sheet_writer.py` | Eugene, NeezaNizam buyer-funnel (per-angle rows) | service account (gspread) | live path works |
| `dct_10_5_5_sheet_writer.py` | Thomson (per-DCT rows) | **`gws` (human login, expires)** | live path works, but should be repointed to the SA |

**Keystone fix still to do (task §7.3):** repoint `dct_10_5_5_sheet_writer.py` from `gws` → the service account, like `ad_concept_sheet_writer.py` already does. Then **no sheet write ever needs a human login again** ("validate once, never again" = "never needed"). Testable against NeezaNizam's existing SA key without gws.

---

## 5. Your vision vs. the pipeline (the scorecard)

Your loop: **(1) spin creatives+copy → (2) track results across clients → (3) results → new/refined angles → (4) new creatives+copy → repeat; + (5) competitor copy → angles.**

| Step | State | The gap |
|---|---|---|
| 1. Create (avatar→angle→copy→creative→assemble) | **Partial — works** | Phase-2 still emits the legacy `dct-tracker.json` not `dct.json` (G1); `--top-n 5` uncommitted (G2); ad-concept-engine not auto-wired into new-client template (G6). All mechanical. |
| 2. Track across clients | **Gap** | Only **NeezaNizam** is live. Eugene SA blocked (§3). **6 clients have no metrics-config at all** (1up, aura, fuggysmedia, michelle-koh, propwise-sg, stackworks). **No cross-client dashboard** — you check each sheet by hand. |
| 3. Results → new/refined angles | **GAP (the big one)** | **10-5-5 Flex gives no per-angle conversions.** `feedback-router` exists and works, but it has no per-angle truth to route on. Fix = promote a winning angle to its **own ad set** (1 ad set = 1 angle = clean data) — documented in `neezanizam/CLAUDE.md` but **not wired** into the workflow. |
| 4. New creatives+copy | Same as step 1 | — |
| 5. Competitor copy → angles | **Partial** | Tools exist (`ad-library-scraper`, `big-angle-spotter` accepts `EXISTING_ANGLES`, `source-of-truth` §28 competitor matrix) but **no wired route** from "competitor X is winning with this copy" → angle generation input. |

**The honest strategic read:** 10-5-5 Flex is a **delivery/volume** vehicle, not a **learning** vehicle. If you want to *learn which angle wins* (your step 3), you need either (a) a winner-isolation structure (own ad set per tested angle), or (b) accept directional CTR + your own judgment. Decide this before scaling — it shapes everything downstream.

---

## 6. Open questions (need your answer)

1. **Who is "Lisa"?** You said track results "for Eugene but also for Lisa." **There is no `lisa` client folder.** Closest is `michelle-koh`. Did you mean a new client to onboard, or someone else? (Clients on disk: 1up-sales-ai, aura, eugene-chieng, fuggysmedia, harmony-wellness, hazecraft, michelle-koh, neezanizam, propwise-sg, stackworks, takekine.)
2. **SA architecture:** per-client SAs (needs org-admin per key) **or** one shared agency SA (reuse NeezaNizam's, grant on all sheets)? (§3 option A vs B.)
3. **Proof-wave folder** `dct-10-5-5-proof-260603` (DCT010): keep as historical (recommended) or archive? It has real reviewed copy; I left it untouched, only flagged its stale TEST-tab wiring.
4. **Per-angle attribution (§5 step 3):** isolate winners into own ad sets, or live with directional CTR?

---

## 7. Do this first (tomorrow, prioritized)

**You (5 min, unblocks me):**
1. `! gws auth login` — finish the browser reauth (fixes `invalid_rapt`).
2. Answer the 4 open questions in §6 (esp. "who is Lisa" + SA architecture).

**Then me, in order:**
3. **[P1] Repoint `dct_10_5_5_sheet_writer.py` → service account** (kills the gws dependency for writes). Test against NeezaNizam's SA in dry-run + one scratch-tab write **with you watching**.
4. **[P1] Grant the chosen SA on Eugene's sheet** (once gws is live) + wire `eugene-chieng/_brand/metrics-config.json`.
5. **[P1] Eugene DCT002 live sheet write** — ready (Canva `DAHMJ4jWRwo` on all 5 rows, 5/5 approved copy, dry-run passes). **Gated on your 2 permission calls:** Derek+Cheryl quote permission, v10 case scope. Command:
   `python3 scripts/ad_concept_sheet_writer.py --client eugene-chieng --campaign-path "upgrader-ads/dcts/dct-002-math-blind" --metrics-campaign upgrader-ads --mode write`
6. **[P1] Fix G1** — make ad-concept-engine Phase 2 emit `dct.json` as canonical (not the legacy `dct-tracker.json`). Removes the `migrate_tracker_to_dct.py` extra step.
7. **[P2] Commit the big-angle-spotter `--top-n` + hardening** (separate repo) once you've reviewed it — then it stops defaulting to 3 angles.
8. **[P2] Decide + wire the learn loop** (§5 step 3) — the winner-to-own-ad-set workflow + competitor-insight → big-angle-spotter input route.
9. **[P2] Multi-client tracking** — a "client readiness" matrix + a cross-client dashboard; onboard whichever clients you actually want tracked (not all 11).

**Do NOT** (without you): any live Meta upload, any billable action, any live write to a client's real (non-test) tab.

---

## 8. State pointers

- Git: branch `rebuild-v2`, `main` == `rebuild-v2` (local, **unpushed**). Uncommitted: auto-regenerated `skill-graph.json` + 7 `agents/*-attribution.md` (a hook re-dirties these — harmless churn) + `propwise-sg` (dirty submodule, separate question).
- Eugene SA: `eugene-sheets@eugene-chieng-ads.iam.gserviceaccount.com` (project `eugene-chieng-ads`, no key yet).
- gcloud: `jerel@genflos.com` valid; `jinoxlr8@gmail.com` valid; `jerel@1upsalesai.com` expired. gws: **needs reauth.**
- Eugene's sheet: `1SDLzn4ceWoLUoWEagrmPFtWA7ZlTZAV_ShRqrD557mw`. NeezaNizam workbook: `14bh8k6S…`.
- Full consolidation evidence: this session's workflow outputs (4-reader pipeline-vs-vision run).
- Proof-wave folder: `clients/neezanizam/campaigns/buyer-funnel/dcts/dct-10-5-5-proof-260603/` (DCT010, all DRAFT, never live).

---

## 9. SESSION 2 UPDATE (260616 ~11:00 SGT) — decisions locked + Eugene SA unblocked

**Operator decisions (this session):**
1. **SA architecture = per-client SAs** (not shared agency SA).
2. **Attribution = isolate winners → own ad sets**, PLUS two added must-haves: (a) track whether a 10-5-5 *set as a whole* is working, (b) a live registry of *which angles are currently running*. (Sharper than §6 — this is the learn-loop spec.)
3. **Proof-wave folder (DCT010) = keep** as historical.
4. **"Lisa" = does not exist** — dropped. No phantom client.
5. **Eugene sheet layout = Layout A** — one row per DCT, 5 angles across `ANGLE1…ANGLE5` columns (the shape already in the sheet; matches the "which angles are running + is the set working" goal).

**DONE + verified this session (local only, see commit):**
- **§7.3 keystone — `dct_10_5_5_sheet_writer.py` repointed off `gws` → service account** (gspread `values_update`). Dry-run + read-only SA auth both pass.
- **Fixed a hidden env blocker:** gspread was not installed in ANY local Python → installed `gspread`+`google-auth` into `.venv`. The SA write path for BOTH writers was unrunnable locally before this.
- **Eugene per-client SA fully unblocked:** relaxed `iam.disableServiceAccountKeyCreation` **project-scoped** on `eugene-chieng-ads` (Jerel is org `roles/owner` → self-granted org-level `policyAdmin`); minted + **gitignored** the Eugene SA key (`scripts/modal/eugene-credentials.json`, glob added); granted the SA Editor on Eugene's sheet via `gws`; wired `provisioning.service_account`+`credentials_path`; fixed a `{{GOOGLE_SHEET_ID}}` placeholder bug that blocked campaign-flatten. **Eugene SA opened Eugene's live sheet read-only — zero human login. Auth proven 3×.**
- **Made `ad_concept_sheet_writer.py` credentials-aware** (was hardcoding the agency-default SA → would 403 on a per-client sheet).

**CORRECTION to §4:** the handoff said "Eugene uses `ad_concept_sheet_writer.py` (per-angle rows)". **Wrong against the live sheet.** Eugene's sheet is **Layout A** (per-DCT row, `ANGLE1…5` + `COPY1…5` columns) — neither canonical writer emits it. DCT002 was hand-populated (~260610) and already sits in the sheet correctly. `ad_concept_sheet_writer.py` (per-angle rows) **fails header validation** on Eugene's sheet.

**STILL OPEN (next session):**
- ~~[P1 build] Layout-A writer for Eugene~~ **DONE 260617 — see §10.**
- **[operator] Eugene DCT002 Meta upload** — still gated on Derek+Cheryl quote permission + v10 case scope.
- **[P2] Learn-loop wiring** — per decision #2: set-level performance + active-angles registry + winner→own-ad-set promotion + competitor-insight→big-angle-spotter route.
- **[P2] Other 6 clients** — still no metrics-config (1up, aura, fuggysmedia, michelle-koh, propwise-sg, stackworks); each now needs its own per-client SA + key + `provisioning.credentials_path` (the per-client cost decision #1 accepted).

---

## 10. SESSION 3 UPDATE (260617) — Layout-A writer built + verified

**Built:** `scripts/dct_layout_a_sheet_writer.py` — the canonical Layout-A writer (closes decision #5 / the §9 P1 gap). Imports all shared config/auth/COPY logic from `dct_10_5_5_sheet_writer.py` (one source of truth); the base writer was NOT modified, so NeezaNizam's full-wave path is untouched.

**What's different from the base 10-5-5 writer** (verified against Eugene's live sheet, not the config — the config's column defs were stale 3-2-2 / single-ANGLE):
- **CREATIVES = 20 cols, Layout A.** Col A header is a literal SPACE (the BATCH key). Angles are split into **`ANGLE1…ANGLE5`** (cols G:K), each cell `<id> - <name> ("<headline>")` — vs the base writer's single joined `ANGLE` cell.
- **COPY = 12 cols, byte-identical** to the base 10-5-5 COPY tab (reused verbatim).
- **Write strategy = per-DCT UPSERT**, not full-wave rewrite. Finds-or-appends each DCT's row by `dct_id` in col A; writes ONLY `A + C:N` (CREATIVES) and `A + C:L` (COPY). **Never** touches STATUS (col B) or the meta_puller metric cols (O:T). So a new DCT joins without disturbing DCT002.
- **DCT discovery is folder-name agnostic** (any subdir with a `dct.json`) — Eugene names folders `dct-002-math-blind`, which the base writer's `^DCT\d+$` regex would miss.

**Verified:** py_compile (both writers); dry-run against DCT002 reproduces the live row's ANGLE/COPY/HEADLINE cells exactly; read-only live-path sim against the real sheet → header passes `validate_layout_a`, DCT002 resolves to row 2 (UPDATE), a future DCT003 appends at row 3. Fresh-eyes sub-agent review applied: hardened the append target (true last-used row, not `len(col_values)+1`), anchored the header left-edge (cols C:F), added write-width asserts.

**NOT done (gated):** no live write performed — DCT002 already stands and any write to Eugene's real tab needs operator go. The writer is ready for the next DCT:
`./.venv/bin/python scripts/dct_layout_a_sheet_writer.py --client eugene-chieng --campaign upgrader-ads --mode dry-run` (then `--mode live` on operator go).
- Note: re-running `--mode live` on DCT002 would UPDATE its row in place — replacing the hand-tuned FORMAT/AWARENESS/PERSONA/ANGLE prose with the writer's computed (cleaner, deterministic) versions, STATUS+metrics untouched. Only do that if you want the machine version on DCT002; otherwise target new DCTs only (`--dct <folder>`).

---

## 11. SESSION 3 cont. (260617) — cross-client consistency sweep + 3-2-2 kill + buyer-funnel live migration

**Operator directive (standing): NEVER the 3-2-2 format again.** 10-5-5 is canonical (COPY 1..5 / HEADLINE 1..5). Captured to memory `feedback_no_322_format.md`.

**Consistency audit (3 sub-agents, live sheets read as ground truth):**
| Sheet | CREATIVES | COPY | Writer | Was consistent? |
|---|---|---|---|---|
| neez **thomson-reserve-buyers** (`1KqWJP08…`) | single `ANGLE` | 10-5-5 | `dct_10_5_5` | ✅ reference sheet |
| neez **buyer-funnel** (`14bh8k6S…`) | single `ANGLE` | **3-2-2** (old DCT1/DCT2 wave) | `dct_10_5_5` | ❌ COPY was 3-2-2; DCT010 10-5-5 wave never written |
| **eugene** upgrader-ads (`1SDLzn4…`) | `ANGLE1…5` | 10-5-5 | `dct_layout_a` | ✅ |

**DONE this session (all verified):**
- **Killed 3-2-2 at the root:** `_template/_brand/metrics-config.json` COPY → 10-5-5. Eugene config → true Layout A (ANGLE1…5 + "Why am I testing this?") + 10-5-5 COPY.
- **buyer-funnel MIGRATED LIVE → Layout A** (operator chose: overwrite old wave + "do it like eugene"). Sequence: snapshot (`campaigns/_sheet-snapshots/buyer-funnel-pre-migration-260617-1219.json`) → cleared old DCT1/DCT2/DCT003/DCT3 → stamped Layout-A headers → upserted DCT010. **Fresh sub-agent validated PASS** (header byte-identical to Eugene; DCT010 copy verbatim; STATUS+metrics blank; old wave gone).
- **New writer mode:** `dct_layout_a_sheet_writer.py --init-headers` (stamps the 20-col CREATIVES + 12-col COPY Layout-A headers; one-time, header row only) — used for the buyer-funnel conversion, reusable for any future Layout-A client.
- **neez config synced to live truth:** buyer-funnel block → Layout A; thomson block → declared single-ANGLE 10-5-5 (was silent). Region-scoped edit (buyer-funnel block only) because buyer-funnel + asset-progression blocks were byte-identical.
- **credentials.json relabel + guard:** it is NeezaNizam's SA, not "agency-default". `resolve_credentials` now HARD-ABORTS if a client's `provisioning.service_account` ≠ the fallback creds' `client_email` (unit-tested: neez passes, a mismatched client aborts).

**FLAGGED (not touched — need a separate decision/audit):**
- **neez `asset-progression` block** — STILL 3-2-2 AND its `creatives`/`copy` gids (`1164222857`/`1695031878`) are stale copy-paste pointing at buyer-funnel's tabs, while its real `sheet_id` is `1D-HrqZ…`. Needs a live audit of `1D-HrqZ…` before any config fix (don't repeat the config-≠-sheet drift).
- **Legacy `CREATIVES_10x5x5_TEST` / `COPY_10x5x5_TEST` tabs** still on the buyer-funnel sheet (`14bh8k6S…`) — retire if unused.
- **Other clients' configs still 3-2-2** (harmony-wellness, hazecraft, takekine, `_template.old`, smoketests, archive) — un-audited, scoped out; fix per-client only after confirming their live sheet shape.
