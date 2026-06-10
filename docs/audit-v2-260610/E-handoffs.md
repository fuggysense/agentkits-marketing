# E — Handoffs Comparator Report
_Audit date: 2026-06-10 (SGT). Repo root: `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing`. All paths relative to repo root unless absolute._

Jargon key (one line each): **handoff** = end-of-session note telling the next session where work stopped. **Loose end** = a promised/deferred task inside a handoff. **PERSISTENT-DRIFT** = a loose end that shows up 2+ times (or survives 2+ weeks) with no recorded resolution. **Untracked** = the file exists on disk but git has never saved it — one bad cleanup away from gone.

---

## 1. Handoff inventory (what exists, where)

| # | File | Date | Scope | In git? |
|---|------|------|-------|---------|
| 1 | `docs/handoffs/metrics-automation-handoff.md` | 2026-04-16 | Modal metrics cron | yes |
| 2 | `docs/handoff/2026-04-24-copywriting-os-phase-1.md` | 2026-04-24 | Copywriting OS | yes |
| 3 | `docs/council/CODEX-HANDOFF-video-pipeline.md` | ~2026-05-12 | Video pipeline restructure | **NO — `docs/council/` is untracked** |
| 4 | `clients/takekine/campaigns/test_2/_audit/session-handoff-260519-ag1.md` | 2026-05-19 | TakeKine AG1 review | NO (`clients/*/` gitignored, `.gitignore:83`) |
| 5 | `clients/neezanizam/SESSION-HANDOFF-260608.md` | 2026-06-08 | NeezaNizam reorg + DCT structure | NO (gitignored) |
| 6 | `clients/neezanizam/SESSION-HANDOFF-thomson-sheet-260608.md` | 2026-06-08 | Thomson sheet rebuild | NO (gitignored) |
| 7 | `clients/neezanizam/SESSION-HANDOFF-260609.md` | 2026-06-09 | Thomson upload | NO (gitignored) |

Supporting "living" files the session-end protocol says should carry this load: `learnings/open-threads.md`, `learnings/session-state.md`, `docs/changelog.md` — all assessed in §4.

FACT — Two near-duplicate folders exist: `docs/handoffs/` (1 file) and `docs/handoff/` (1 file). Singular vs plural; nothing reconciles them.

FACT — The client Jake-structure ships a `clients/_template/05_handoff/` contract (`clients/_template/05_handoff/CONTEXT.md:1-23`, output convention `output/<YYMMDD>-handoff-note.md`), but it is for packaged campaign deliverables, and no client uses it: `clients/eugene-chieng/05_handoff/output/` is empty, `clients/harmony-wellness/05_handoff/` holds only the CONTEXT.md.

JUDGMENT — Handoffs live in at least 5 locations (docs/handoffs, docs/handoff, docs/council, client roots, campaign `_audit/`), and the 4 most recent + highest-stakes ones (items 3-7) are NOT version-controlled. Given this repo already had a data-loss near-miss with gitignored content (`clients/neezanizam/SESSION-HANDOFF-260608.md:15` — worktree salvage), the handoff files themselves now sit in the same fragility class.

---

## 2. Loose-end ledger

Legend: OPEN = no evidence of resolution. RESOLVED = verified closed. RESOLVED-UNLOGGED = closed in repo but the handoff/tracker never updated. P-DRIFT = persistent drift.

### A. Metrics automation (first: 2026-04-16, `docs/handoffs/metrics-automation-handoff.md`)

| Item | First | Status | Evidence |
|---|---|---|---|
| Phase 5: cron first auto-fire | 04-16 (:60-64) | RESOLVED-UNLOGGED | Cron ran daily 3 Apr→6 Jun per `clients/neezanizam/SESSION-HANDOFF-thomson-sheet-260608.md:93`. Handoff header still frozen at "Waiting on first auto-fire" (:4) — 8 weeks stale. |
| Phase 6: anomaly alert wiring (Telegram) | 04-16 (:84-96) | OPEN (dormant) | No `telegram` reference in `scripts/modal/marketing_metrics.py` (grep empty). Never re-mentioned. |
| Phase 7: Pentagon Ops integration | 04-16 (:98-104) | OPEN (dormant) | unverified — no later mention anywhere. |
| Known issue 1: CREATIVES CTR hardcoded 0 (missing `impressions`) | 04-16 (:129) | RESOLVED-UNLOGGED | `scripts/modal/meta_puller.py:99,145,186` now request `impressions`. Handoff never closed the item. |
| Known issue 2: APPT columns heuristic — "confirm the right Meta event with Jerel" | 04-16 (:131) | **P-DRIFT** | Re-deferred 8 weeks later: appointment optimisation "deferred — needs pixel + offline event; OPERATOR handles pixel manually" (`clients/neezanizam/SESSION-HANDOFF-260609.md:15,18`). Same unanswered question, two handoffs, no resolution. |
| Known issue 3: service account can't create sheets | 04-16 (:133) | RESOLVED | Two-identity model + `skills/sheets-provisioner/references/sheet-auth.md` + `find_or_create_sheet.sh` (built ~260608, `...thomson-sheet-260608.md:68,98`). ~7.5 weeks open, then properly documented. |
| Known issue 4: per-client `meta_event_mapping` config | 04-16 (:135) | OPEN (dormant) | No later mention; unverified in config. |
| Known issue 6: scope mismatch rows 3-9 (campaign) vs 10+ (account) | 04-16 (:139) | OPEN (dormant) | Never mentioned again in any later handoff. |
| Meta token expires ~2026-06-15 | 04-16 (:21) | RESOLVED | Swapped to never-expiring system token 260608 (`...thomson-sheet-260608.md:94`) — closed ~1 week before expiry. |
| Snapshot cleanup job (90-day archive) | 04-16 (:146) | OPEN (dormant) | Premise partly changed (snapshots go to ephemeral Modal storage, `...thomson-sheet-260608.md:93`); nobody updated the item. |

### B. Copywriting OS (first: 2026-04-24, `docs/handoff/2026-04-24-copywriting-os-phase-1.md`)

| Item | First | Status | Evidence |
|---|---|---|---|
| Phase 2 build (HITL approval + 10 subphases) | 04-24 (:75-83) | RESOLVED | `skills/copywriting-os/` + `.claude/references/copywriting-os/` exist; `task_plan.md:55-60` shows 2.1-2.4 ✅, 2.11 COMPLETE 2026-04-24. |
| Phase 2.5 framework library — marked DEFERRED | 04-24 (`task_plan.md:59`) | RESOLVED-UNLOGGED | 12 framework files exist at `.claude/references/copywriting-os/frameworks/` (and routing-overrides auto-loads them), but `task_plan.md` (last commit 2026-05-04) still says "DEFERRED". Tracker is stale relative to reality. |
| Phase 4 gap-fills (#41 verdict, #36 categories 4+6) | 04-24 (:119-120) | **P-DRIFT** (parked) | Listed in handoff Open threads AND `task_plan.md:113,137` ("FUTURE sessions / CAN RUN ANYTIME"); no completion evidence ~6.5 weeks later. Explicitly parked, but never re-triaged. |
| NeezaNizam 3-reviewer dogfood (parked, resume in 2.10) | 04-24 (:6) | RESOLVED-BY-REDEFINITION | Dogfood material swapped to "Jerel-uploaded sales letter" (`task_plan.md:48-51`). The original NeezaNizam letter test was never run as promised; superseded. |
| `ripgrep` not on PATH (Glob ENOENT) | 04-24 (:113) | unverified | Flagged as "system-level thing to address"; never re-mentioned. |

### C. Codex video-pipeline handoff (~2026-05-12, `docs/council/CODEX-HANDOFF-video-pipeline.md`)

| Item | Status | Evidence |
|---|---|---|
| Pre-step: merge `worktree-video-pipeline-council-20260512` to main | **NOT DONE / P-DRIFT** | Branch still exists unmerged (`git branch --merged main` excludes it; branch list shows `+ worktree-video-pipeline-council-20260512` = still checked out in a worktree). `docs/council/` is untracked (`git status` → `?? docs/council/`). The handoff's own first instruction (:5-9) never executed — 4 weeks. |
| TASK 0+1: `docs/video-studio.md` (3-sentence doc + ground truth) | NOT DONE | File does not exist (`ls docs/video-studio.md` → no such file). |
| TASK 2: `docs/video-runs/_frozen-skills.md` | NOT DONE | `docs/video-runs/` does not exist. |
| TASK 3: deprecate `video-director`, route to `video-factory --engine=...` | RESOLVED DIFFERENTLY | `skills/video-director/SKILL.md:8` is now a "REDIRECT / signpost (consolidated 2026-05-30)" pointing to the higgsfield-prompts infra — a different architecture than the handoff prescribed. Nothing marks the handoff superseded. |
| TASK 5: ship one real client video, log `docs/video-runs/run-001.md` | NOT DONE | Folder/file absent. The W1 "success criteria" (:79-86) are unmet on every checkable line except the deprecation. |
| 4 open questions Jerel must answer before W3 (:70-75) | OPEN | No recorded answers anywhere found. |

JUDGMENT — This handoff is effectively abandoned: its target (a Codex-executed week-1 plan) was overtaken by the 2026-05-30 video consolidation, but no note says so. A fresh agent finding this file would start executing stale instructions, including merging a 4-week-old worktree branch into today's main.

### D. TakeKine AG1 (2026-05-19, `clients/takekine/campaigns/test_2/_audit/session-handoff-260519-ag1.md`)

| Item | Status | Evidence |
|---|---|---|
| Operator taste pass on live AG1 page (:58) | **P-DRIFT (operator-side)** | `clients/takekine/CLAUDE.md:45` auto-block (refreshed as of 2026-06-10) still shows `ag1_review_pending_operator_taste_pass`; `campaigns/test_2/STATUS.md` last updated 2026-05-19. Campaign frozen 3 weeks waiting on one human decision. |
| "Produce all 10 vs winner-only" decision (:53) | OPEN | "Will resolve after AG1 taste pass" — gated on the item above, so equally stuck. |
| AG1 vault back-link to workspace (:54) | OPEN (minor) | unverified; never re-mentioned. |
| Stale wayfinding files reconciliation | RESOLVED | Self-documented: superseded-note at :4 says wayfinding reconciled — this handoff is the ONLY one that closes its own loop. |

### E. NeezaNizam ICM reorg (2026-06-08, `clients/neezanizam/SESSION-HANDOFF-260608.md`)

| Item | Status | Evidence |
|---|---|---|
| Deferred #8: per-DCT tracker split + rewrite 6 ad-creation scripts (:50) — decided 260608 to do FIRST before Build #10 (:66) | OPEN | Legacy `dct-tracker.json` still in 6 non-archive locations (e.g. `clients/neezanizam/campaigns/buyer-funnel/dcts/dct-260417/dct-tracker.json`). Mentioned twice within the handoff (deferred list + sequencing decision). Recent (2 days), but it gates Build #10. |
| Deferred #9: stale internal refs (`thomson-reserve-260530` etc.) (:51) | OPEN | Stale refs still present: `clients/neezanizam/meetings/260530-thomson-reserve-kickoff.md`, `campaigns/thomson-reserve/02_creatives/gpt-image-2-260531/_pitch-source-brief.md`, `_copy-matrix.md` (grep hits). |
| Deferred #10 / Build #10: `allocate <DCT> <render-file>` helper (:52,59) with full guard contract locked (:70) | OPEN — and the cost already showed | `scripts/ad-images/` holds only `render.py` + styles; no `allocate` anywhere (`grep -rln allocate scripts/` empty). Next session (260609) allocated 44 Thomson images BY HAND (`SESSION-HANDOFF-260609.md:9`) — exactly the manual grind the tool was specced to remove. Spec written, contract locked, tool unbuilt. |
| letter-critic skill: promote or discard (:54) | OPEN | Still parked at `clients/neezanizam/_salvaged-from-worktree/letter-critic/`. |
| `ONE_CLICK_ONBOARDING_PLAN.md` fold-in ("user didn't answer") (:55) | OPEN | Still at `scripts/modal/ONE_CLICK_ONBOARDING_PLAN.md`; question never answered. |
| Locked decision: "Eugene adopts `_assets.json` agency-wide" (:68) | **CONTRADICTED BY REPO** | Eugene DCT work proceeded after the decision (`clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/` with `angle-run-260609`, `wave-1-copy-260610.md`) and there is NO `_assets.json` anywhere under `clients/eugene-chieng/` (find empty). Decision locked 260608, violated by 260609-10 work. |
| "Decide Eugene's image source-of-truth BEFORE the first run" (:72) | OPEN/SKIPPED | First run happened (angle-run-260609 + `images/` exists); no ledger file = the convention question was bypassed, not decided. JUDGMENT: the per-client fork this warning was written to prevent is now live. |

### F. Thomson sheet rebuild (2026-06-08, `clients/neezanizam/SESSION-HANDOFF-thomson-sheet-260608.md`)

| Item | Status | Evidence |
|---|---|---|
| Q1-Q4 wide-layout questions for Jerel (:28-33) | RESOLVED | 260609 handoff: tabs rebuilt, "COPY widened to 10-5-5" (`SESSION-HANDOFF-260609.md:11`). |
| SPEC tension: "Do NOT silently let the sheet and the spec disagree" (:23) | **P-DRIFT — the forbidden state now exists** | `docs/methods/10-5-5/SPEC.md:80-81` still says "we do NOT widen the COPY tab to 5+5 columns crammed on one row. We add rows" while the live Thomson sheet IS the wide 5+5 layout. The handoff demanded an explicit resolve (diverge or update spec); neither was recorded. SPEC.md calls itself "the single source of truth" (header) and is now wrong about the live sheet. |
| Fix wrong "one sheet" note in client CLAUDE.md (:102) | OPEN — live contradiction | `clients/neezanizam/CLAUDE.md:28` still reads "One workbook, separate tabs per metrics-campaign" citing only `14bh8k6S…`. Reality: 3 workbooks (buyer-funnel `14bh8k6S`, asset-progression `1D-Hrq…`, thomson `1KqWJP…` — all in `_brand/metrics-config.json`). A fresh agent obeying client law would write Thomson data to the wrong workbook's assumptions. |
| Tighten provisioner `--into` footgun (:83,103) | OPEN | `skills/sheets-provisioner/scripts/provision_from_template.py:97,121-122` — `--into` still collects ALL destination tab ids and `deleteSheet`s every one. The "nuke all tabs" behavior flagged with a ⚠️ TODO is unchanged. |
| `modal deploy` of fixed config_loader (:101) | OPEN (unverifiable from repo) | No deploy record; handoff itself said "not urgent". Cron still runs the April image per :95. |
| "New skill files + config edits SAVED but NOT committed to git" (:104) | **P-DRIFT** | `skills/sheets-provisioner/` still fully untracked (`?? skills/sheets-provisioner/`) on 2026-06-10. Broader: last commit to the repo is `353612f` dated 2026-05-08; `docs/methods/` (10-5-5 SPEC), `docs/council/`, `.claude/workflows/content-spine-workflow.md`, `docs/ad-image-tooling-overlap-260608.md` are ALL untracked. A month of system-level work has no git safety net. |

### G. Thomson upload (2026-06-09, `clients/neezanizam/SESSION-HANDOFF-260609.md`)

| Item | Status | Evidence |
|---|---|---|
| Paste Tally questions (:23) | RESOLVED | `campaigns/thomson-reserve/instant-form-questions.md:3` — "STATUS: PASTED 260609". |
| Run the upload (:24) | PARTIAL — new hard blocker | `campaigns/thomson-reserve/dcts/pipeline-state.json:7-8`: phase `PARTIAL_UPLOAD__BLOCKED_SG_ADVERTISER_VERIFICATION`. Done: lead form + paused campaign + 8 DCT101 images. Not done: 5 ad sets, 5 creatives, 5 ads. Blocker is operator-only (Meta SG advertiser verification, error_subcode 3858548). |
| Flip `meta.enabled=true` + add campaign_id (:26) | OPEN (correctly gated) | `_brand/metrics-config.json` thomson block `_note` still "meta.enabled=false until a Thomson Reserve Meta campaign exists" — though a paused campaign id `52620225866910` NOW exists per pipeline-state. JUDGMENT: config note is now half-stale (campaign exists, ads don't). |
| 3 provisional avatars founder sign-off (:29) | OPEN (recent) | Flagged "fine while PAUSED"; no sign-off recorded. |
| Proximity claims fact-check before enabling (:30) | OPEN (recent) | No verification artifact found. |
| DCT104 thin — bench top-up decision (:31) | OPEN | `dcts/DCT104/images/` still holds exactly 1 image (`DCT104-img-01.png`). |
| Confirm `thomson.swopyourhome.com/landing` live (:32) | OPEN (unverified) | Not checkable from repo; no check recorded. |

---

## 3. Contradiction spot-checks (handoff says X, repo says Y)

1. **FACT — Client law vs reality (workbooks).** Handoff `...thomson-sheet-260608.md:102` flagged `clients/neezanizam/CLAUDE.md` as wrong; `CLAUDE.md:28` is STILL wrong ("One workbook") while `_brand/metrics-config.json` registers 3 workbooks. Flagged → never fixed → now misleads every session that loads client law.
2. **FACT — Spec vs live sheet (10-5-5 layout).** `docs/methods/10-5-5/SPEC.md:80-81` mandates row-based COPY; the Thomson sheet was rebuilt column-wide per `SESSION-HANDOFF-260609.md:11`. The 260608 handoff (:23) explicitly ordered "do NOT silently let the sheet and the spec disagree" — they now silently disagree.
3. **FACT — Locked decision vs next-day execution (Eugene `_assets.json`).** Decision "Eugene adopts `_assets.json` agency-wide" (`SESSION-HANDOFF-260608.md:68`); Eugene DCT folders built 260609-10 contain no `_assets.json`.
4. **FACT — Tracker vs tracker (Phase 5.2).** `learnings/open-threads.md:14` says "5.2/5.4-5.7 pending"; `task_plan.md:151` says "5.2 ... **COMPLETE 2026-05-04**" — both last committed the SAME day (`3cf78c7`, 2026-05-04). The two designated cross-session memory files contradicted each other at the moment of writing and were never reconciled.
5. **FACT — Codex handoff vs git.** `docs/council/CODEX-HANDOFF-video-pipeline.md:5-9` instructs merging the council worktree to main "so the council artifacts ship with the work"; branch unmerged, `docs/council/` untracked, 4 weeks on.
6. **FACT — Frozen status header.** `docs/handoffs/metrics-automation-handoff.md:3-4` still says "Waiting on first auto-fire at 9am SGT tomorrow" (2026-04-16); the cron has been firing daily for ~2 months (`...thomson-sheet-260608.md:93`). No close-out edit ever made.

---

## 4. Handoff hygiene census

**Is there a convention?** Partially, and it's inverted.

- FACT — The mandated channel is dead. `docs/system-rules/session-end-protocol.md:14-17` requires: log decisions to `learnings/session-state.md` (step 1), note unfinished work in `learnings/open-threads.md` (step 5), append skill changes to `docs/changelog.md` (step 6). Current state: `session-state.md` and `open-threads.md` last committed 2026-05-04 (`3cf78c7`); neither contains a single item from the 5 handoffs dated 260519-260609. `docs/changelog.md`'s newest entry is `## 260424` while skills were created/updated since (sheets-provisioner capability 260608, ship-gate agent, content-spine workflow, copy audit v0.4 — all in git log/handoffs). Three protocol steps, ~6 weeks of non-compliance each.
- FACT — The un-mandated channel is alive but scattered. Real continuity now travels through ad-hoc `SESSION-HANDOFF-*.md` files in 5 different locations (see §1 table), 4 of which are outside version control. The session-end protocol never mentions writing a handoff file at all; the global `session-handoff` skill exists (`~/.claude/skills/`) but no rule routes session-end to it or names a canonical path/filename.
- FACT — Format is half-converged. Items 4-5 (takekine 260519, neezanizam 260608) share an identical section skeleton (Where it started / Decisions locked + what shipped / Key files / Running state / Verification / Deferred + open questions / Pick up here) matching the `session-handoff` skill. Items 1, 2, 6, 7 each use their own ad-hoc structure.
- FACT — One good pattern worth keeping: the takekine handoff carries a "Superseded state note" (`session-handoff-260519-ag1.md:4`) telling future readers which parts are historical. No other handoff self-expires; the metrics and Codex handoffs actively mislead because they don't.
- JUDGMENT — Root CLAUDE.md hard-pointer ("End of session? → session-end-protocol.md") fires, but the protocol it points to optimizes for learnings capture, not state transfer. Sessions that DID write excellent state-transfer handoffs (260608/09) skipped the protocol's own steps (open-threads, changelog, session-state) — so the system has two competing memories and both are partially stale. The fix is one rule: handoffs get ONE canonical, git-tracked location + an index, and session-end-protocol step 5 points there.
- JUDGMENT — Gitignoring `clients/*/` (`.gitignore:83`) makes client handoffs structurally unversioned. The repo already paid for this pattern once (worktree salvage near-miss, `SESSION-HANDOFF-260608.md:15`; learning logged at `learnings/reorg-worktree-salvage.md`). The handoff files now have the same single-copy exposure the learning warns about.

---

## 5. PERSISTENT-DRIFT shortlist (the items to actually chase)

1. **Appointment-event mapping for NeezaNizam** — open since 2026-04-16 (`docs/handoffs/metrics-automation-handoff.md:131`), re-deferred 2026-06-09 (`SESSION-HANDOFF-260609.md:15`). 8 weeks. Blocks appointment-optimised Meta campaigns.
2. **A month of uncommitted system work** — last commit 2026-05-08; `skills/sheets-provisioner/`, `docs/methods/` (10-5-5 SPEC), `docs/council/`, `content-spine-workflow.md`, overlap doc all untracked; explicitly flagged "not committed" in the 260608 handoff (:104) and still true.
3. **Codex video handoff abandoned, never marked superseded** — `docs/council/CODEX-HANDOFF-video-pipeline.md` tasks 0/1/2/5 unexecuted, worktree branch unmerged, 4 open Jerel questions unanswered, 4 weeks.
4. **TakeKine AG1 operator taste pass** — pending since 2026-05-19, campaign frozen (`clients/takekine/CLAUDE.md:45`, STATUS.md dated 05-19). Gates the all-10-vs-winner decision and all downstream production.
5. **SPEC.md vs Thomson sheet silent disagreement** — the exact failure the 260608 handoff forbade (`...thomson-sheet-260608.md:23` vs `docs/methods/10-5-5/SPEC.md:80-81`).
6. **`clients/neezanizam/CLAUDE.md:28` "One workbook" falsehood** — flagged 260608, still live in the client's always-loaded law file.
7. **`allocate` helper unbuilt while its absence already cost a manual 44-image session** — contract locked 260608 (`SESSION-HANDOFF-260608.md:70`), no code (`scripts/ad-images/`), sequencing dependency (Deferred #8 tracker split) also unstarted.
8. **Eugene `_assets.json` agency-wide decision ignored on first use** — locked 260608 (:68), absent in all Eugene DCT folders built 260609-10.
9. **Living-memory files dead** — `open-threads.md` / `session-state.md` / `changelog.md` all frozen ~2026-05-04/04-24 while 5 handoffs accumulated elsewhere; protocol steps 1/5/6 systematically skipped.
10. **Copywriting-OS Phase 4 gap-fills** — parked 2026-04-24 (`docs/handoff/2026-04-24-...md:119-120`), still "FUTURE" in `task_plan.md:113`; mild, but it is the oldest still-listed open thread in any tracker.

## 6. What is genuinely healthy

- FACT — Closure DOES happen when the next session touches the same client: Thomson Q1-Q4 (asked 260608, answered+built 260609), Tally questions (PENDING 260609 morning → PASTED same day), Meta token swap (flagged April, fixed June 8 before the June 15 expiry), SA-can't-create-sheets (April issue → documented two-identity model + script by June).
- JUDGMENT — The drift pattern is specific: loose ends die when they cross a BOUNDARY — client→repo (CLAUDE.md fix, SPEC update, git commits), session→protocol (open-threads/changelog), or owner→owner (Jerel-side decisions: AG1 taste pass, Codex questions, avatar sign-offs). Within a single client lane, the handoffs work well.

## Unresolved questions for the orchestrator

- Was the fixed `config_loader.py` ever `modal deploy`ed? (Not checkable from repo files.)
- Did Jerel ever answer the Codex handoff's 4 W3 questions out-of-band (e.g., the 2026-05-30 video consolidation may embody answers)?
- Is the Eugene image-convention divergence deliberate (BAS pipeline owns its own manifest) or an oversight?
- Are `docs/handoff/` vs `docs/handoffs/` meant to be different things, or a typo that stuck?
