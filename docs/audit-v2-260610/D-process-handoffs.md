# Dimension D — Process & Handoffs Audit

_Audit date: 2026-06-10 (SGT). Repo root: `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing`. All paths repo-relative. Every FACT below = lines I re-read or commands I ran THIS session. JUDGMENT = my interpretation._

Jargon key (one line each): **money path** = the steps that lead to live ad spend (build → sheet → Meta upload → metrics). **HITL gate** = a checkpoint where a human must approve. **dct.json** = the new per-ad-test data file; **dct-tracker.json** = the old one it replaced. **Drift** = a doc/index that says X while the repo does Y. **Gitignored** = git never saves it; one bad cleanup deletes it forever.

---

## Headline

The marketing system is healthy where a human is in the loop and rotten where machines are supposed to carry state across sessions. Four "generic" money-path scripts only work for one client or one data shape; the rest of the live waves run by hand around them, losing the snapshot-safety those scripts were built to provide. Indexes, specs, and the mandated session-memory files all drift because **nothing auto-syncs them and the last git commit was 33 days ago** while ~520 files sit uncommitted. The biggest invented-number risk (an unsourced $214,300 in a shipped creative) reaches the creative approval gate with no machine check — covered in C's trace; I confirm the process gap that lets it through.

---

## 1. Broken / bypassed automation on the money path

Each script verified by reading the cited lines this session.

- **render.py tracker-mode is dead against current data.** `scripts/ad-images/render.py:79-83` reads `data.get("creatives") or data.get("ads")` then matches `c.get("batch")`. Today's `dct.json` has neither key (copy lives in `angles[]`, prompts in `image_pool.images[]`). So `--from-tracker` raises "batch not found" for every batch. Every 10-5-5 render is now hand-pasted via `--prompt` — the exact manual grind the tool exists to kill. (B-04/A2 §1.2)
- **ad_concept_sheet_writer.py refuses the new shape.** `scripts/ad_concept_sheet_writer.py:314-324` hard-requires a `dct-tracker.json` with a `creatives[]` array, errors otherwise. Eugene's live wave is `dct.json` (angles + image_pool), so the sheet write was done by hand via direct `gws` calls — bypassing the script's HITL snapshot. (C §8)
- **tr_10_5_5_sheet_writer.py is hardcoded to one client.** `scripts/tr_10_5_5_sheet_writer.py:37-38` pins `DCT_IDS=["DCT101".."DCT105"]` and `SHEET_ID="1KqWJP08h8B…"`; defaults `--client neezanizam --campaign thomson-reserve` (lines 153-154). The ONLY new-shape sheet writer that exists works for exactly one campaign. Any other 10-5-5 wave has no working writer.
- **Two scripts look for metrics-config.json in the wrong place.** `scripts/source_of_truth_sheet_writer.py:79` and `scripts/patch_angle_cell.py:40` read `clients/<slug>/metrics-config.json` (client root). The two live clients keep it at `_brand/` (verified: `clients/neezanizam/_brand/metrics-config.json`, `clients/eugene-chieng/_brand/metrics-config.json` exist; root copies do NOT). Only idle/internal `hazecraft` still has a root copy. So these writers `FileNotFoundError` for exactly the clients they serve. `ad_concept_sheet_writer.py` already handles both locations — the fix exists in a sibling and was never back-ported.

Consequence (JUDGMENT): the sheet-write stage was designed with a HITL preview/snapshot (`skills/ad-concept-engine/corrections.md`). Because operators route around the broken scripts with manual `gws` writes, **no pre-write snapshot or log artifact exists** — the client-facing dashboard write is unverifiable from disk (C §8 open Q1).

## 2. State / index drift (nothing auto-syncs)

- **eugene campaigns-index misses the hottest workspace.** `clients/eugene-chieng/campaigns/_campaigns-index.json` lists only `mp1-upgrader-letter-260603`. The `upgrader-ads/` DCT folder (edited today, nearest to live spend) exists on disk but is absent from the index. An agent obeying the AGENT ENTRY CONTRACT ("use the index to discover campaigns") would miss it.
- **SPEC.md says all phases unstarted; migration-log says all done.** `docs/methods/10-5-5/SPEC.md:140-145` shows every phase `[ ]` "in progress", while `docs/methods/10-5-5/migration-log.md:7-51` marks Phases 1-6 DONE (2026-06-03). SPEC also calls itself "single source of truth" (header).
- **SPEC sheet model contradicts the live sheet.** `SPEC.md:80-84` mandates "one row per angle (5 rows per wave)… we do NOT widen the COPY tab." The shipped Thomson + eugene sheets are the wide one-row-per-wave layout (C §5; `SESSION-HANDOFF-260609.md:11`). The 260608 handoff explicitly forbade letting sheet and spec silently disagree; they now do.
- **No regeneration script exists.** Grepping `scripts/` + `skills/` for `_campaigns-index.json` / `pipeline-state.json` writers returns only `scaffold-client.sh` (one-time create) and `campaign-runner/scripts/state_manager.py` (the V3 lifecycle path the DCT pipeline routes around). Confirmed: **no tool keeps these indexes/specs in sync** — they only drift.

## 3. Missing human gates where money moves

- **Citation audit is advisory, not blocking.** `clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/angle-run-260609/_run.log:13` (re-read): `[WARN] citation audit (advisory): 2 passing angle(s) cite evidence not found verbatim in profile: ['A01','A03']` — it warned and the angles shipped. The one machine check on claim-grounding cannot stop a wave.
- **Sheet-write stage has no gate at all.** C §4 gate inventory: dct.json → sheet = "NONE — script HITL bypassed, direct manual write." The stage that pushes copy to the client dashboard is mechanical and ungated once the operator runs it by hand.
- **Claim/number injection is ungated by design.** The copy-assembly and image-prompt stages pull figures from research/avatar files into ad text; the only checks are the writer's own in-file checklist and operator eyeballs. An invented `$214,300` reached shipped creatives img-03/04 and passed the creative gate (C §3). No machine compares copy numerals to a source manifest. This is the highest-stakes gap: an unsourced number can ride to paid media.

## 4. Dead stages & manual grind

- **`allocate` helper: contract locked, tool never built.** `clients/neezanizam/SESSION-HANDOFF-260608.md:70` (re-read) locks the full `allocate <DCT> <render-file>` guard contract (auto-slot, fail-closed, dry-run, 11th-image refuse, atomic two-file write). `scripts/ad-images/` contains only `render.py` + `styles/` — no allocate. The very next session (260609) hand-allocated 44 Thomson images (`SESSION-HANDOFF-260609.md:9`) — exactly the grind the spec was written to remove.
- **05_handoff packaged-deliverable convention is unused.** `clients/_template/05_handoff/` ships a CONTEXT.md + `output/<YYMMDD>-handoff-note.md` convention; `find clients -path "*/05_handoff/output/*"` (excluding template) returns nothing. The convention exists on paper only.
- (Correction to prior discovery: eugene's six stage folders are NOT empty — each holds 1-20 files, mostly CONTEXT.md scaffolding. Dropped as a finding.)

## 5. Handoff system — the mandated channel is dead, the real one is unversioned

- **Session-end protocol's living files are frozen.** `docs/system-rules/session-end-protocol.md` mandates logging to `learnings/session-state.md` (step 1), `learnings/open-threads.md` (step 5), `docs/changelog.md` (step 6). Last commits (re-verified): session-state.md + open-threads.md = **2026-05-04**; changelog.md = **2026-03-27**, newest in-file entry `## 260424`. Five real handoffs dated 260519-260609 left zero trace in any of them. ~6 weeks of protocol non-compliance.
- **Real continuity rides ad-hoc files in 5 locations; the 4 freshest are gitignored.** `docs/handoffs/`, `docs/handoff/` (singular+plural, nothing reconciles them), `docs/council/` (untracked), client roots, campaign `_audit/`. The 4 highest-stakes recent handoffs (`docs/council/CODEX-HANDOFF-*`, the 3 neezanizam `SESSION-HANDOFF-*.md`) are outside version control — single-copy, one bad cleanup from gone. The repo already had a gitignored-content near-miss (worktree salvage, `SESSION-HANDOFF-260608.md:15`).
- **A month of system work is uncommitted.** Re-verified myself: `git log -1` = `353612f 2026-05-08`; `git status --porcelain | wc -l` = **523**. Untracked include `skills/sheets-provisioner/`, `docs/methods/` (the 10-5-5 SPEC), `docs/council/`, `.claude/references/` (the whole copywriting-OS), `.claude/skill-graph.json`, the eval-halbert/eval-sales-letter agents. No git safety net for any of it.

## 6. link-skills.py — mandated tool fails under the default interpreter

`scripts/link-skills.py:30-35` hard-exits if sklearn is missing. `docs/system-rules/skill-graph-rule.md` mandates running it on EVERY skill/agent edit, and every SKILL.md footer cites it. Default PATH `python3` (homebrew) has no sklearn — the documented invocation dies. The graph IS fresh (mtime 10 Jun) so SOMETHING ran it with a different interpreter, but nothing in-repo documents the sklearn dependency or the working interpreter path. (A2 §5; I re-read lines 30-35.) JUDGMENT: a fresh agent following the mandate runs the command, hits the error, and either gives up or skips the graph update — the graph silently rots on the next edit.

## 7. Deleted-agent references — load-bearing, not cosmetic

17 agents were deleted this cycle. Re-counted myself: **52 SKILL.md + auto-loaded rule files** still name a deleted agent (grep over `skills/*/SKILL.md` + `.claude/rules/*.md`, excluding `_archive`). Two of those auto-load EVERY session:
- `.claude/rules/mcp-integrations.md:27` — "delegate to `mcp-manager` agent" (mcp-manager deleted; `ls agents/mcp-manager.md` → absent).
- `.claude/rules/skill-activation.md:28,30` — routes "research/competitive intel" to `attraction-specialist` and "multi-perspective review" to `solopreneur, startup-founder` (all three deleted). This is the gate that tells agents to USE named agents, so the rot causes failed dispatches.
- Spot-checked skill frontmatter: `campaign-runner/SKILL.md:32-39` lists 7 agents, 6 deleted (only copywriter survives); `prompt-contracts/SKILL.md:29-30` = planner + project-manager (both deleted); `knowledge-hygiene/SKILL.md:20` = docs-manager (deleted) — and knowledge-hygiene is wired into `/ops:weekly`, so its dispatch target is a ghost.

(Repo-wide the count balloons to 164 files including commands/ and training/ — those are lower-stakes; the 52 SKILL.md+rules figure is the load-bearing subset.)

## 8. The campaign-check cron — the one that would catch this — is off

`cron-registry.json` (parsed this session): `campaign-check` (daily 09:00 health scan) `enabled=False`; all four others true. JUDGMENT: the single automated sweep that would flag a stalled money-adjacent campaign is disabled while two clients (neezanizam Thomson, eugene upgrader-ads) have pipelines mid-flight behind operator/client gates.

## 9. Shared service-account identity under multi-client scripts

`scripts/modal/credentials.json` `client_email` = `neezanizam@neezanizam-492212.iam.gserviceaccount.com` (read this session). Three "generic" sheet writers (`ad_concept_sheet_writer.py`, `source_of_truth_sheet_writer.py`, `patch_angle_cell.py`) all hardcode that path. Multi-client tooling rides on one client's GCP identity; the template prescribes per-client SAs. (Security-positive note: the key IS gitignored — `git check-ignore` matches, `git ls-files` empty — so it is not leaking to the remote.)

---

## What is genuinely healthy (so fixes don't break it)

- The angle-generation gate is real machinery: scored 1-5 JSON, threshold 4, set-min 5, regen loop, fail-closed (C §2). Money-spending moments (render, upload) DO have hard human gates; ads are created PAUSED and only a human un-pauses.
- vid-director's REFERENCE_GRAPH chain resolves: I checked 8/8 referenced node files in `skills/video-concept-lab/REFERENCE_GRAPH.json` — all exist. The video routing layer's graph is not rotted.
- Closure happens reliably WITHIN a client lane across consecutive sessions (Thomson Q1-Q4, Tally paste, Meta token swap). Drift only appears when a loose end must cross a boundary (client→repo, session→protocol, owner→owner).

## Unresolved questions for the orchestrator

- Did `.env` re-save (7 Jun) rotate the Meta token flagged to expire ~2026-06-15? Not checkable from files; if not, the metrics cron dies this week.
- Is the wide one-row-per-wave sheet the new intended 10-5-5 shape, or a one-off? Whichever, SPEC.md or the live sheet must change.
- Who owns repointing the four broken scripts to the `dct.json` shape, and is it scheduled before wave 2 (where hand-feeding won't scale)?
