# NeezaNizam Reorg — Migration Map & Remnant Report

> Generated 260608. READ-ONLY audit of on-disk state vs `clients/neezanizam/_reorg-spec.md` (locked 260608). No client files were modified. This doc drives Phase 1 (migrate folders) and is a checklist for "did anything get lost."

## 1. Summary + file counts

| Metric | Count |
|--------|-------|
| Total files under `clients/neezanizam/` | 1,869 |
| Total dirs | 470 |
| **Files that are pure NOISE** (`.claude/worktrees/mystifying-wu-249e7d/` — a stray full Marketing-repo clone) | **1,061** |
| Files excl. worktree (1,869 − 1,061) | **808** (verified `find`) |
| **Real signal files** (808 − 34 `.DS_Store`) | **~774** |
| PNG renders (excl. worktree) | 185 |
| MP4 (excl. worktree) | 11 |
| `.DS_Store` cruft (excl. worktree) | 34 (verified) |

**Headline finding:** The single biggest "current file count" distortion is the **1,061-file gitignored worktree** at `clients/neezanizam/.claude/worktrees/mystifying-wu-249e7d/`. It is a full clone of the Marketing repo's `skills/`, `.github/`, integration configs — NOT NeezaNizam work product. It dwarfs the real client tree (~774 files). **Delete it before counting or migrating anything** — it will otherwise get swept into a `cp -r` and double the move. (Post-worktree-delete file count = 808, of which ~774 are real signal and 34 are `.DS_Store` cruft — Step 1's `~808` prediction is exact.)

**Structural verdict:** The current tree is a *flat date-stamped sprawl* (`campaigns/dct-260417/`, `dct-260419/`, `dct-260421/`, `dct-10-5-5-proof-260603/`, `funnel/`, `angles/`, `ad-concepts-260406/`, `metrics/`, `sheet-snapshots/` all siblings under `campaigns/`). The spec wants a *3-campaign-by-offer* tree (`buyer-funnel/`, `asset-progression/`, `thomson-reserve/`), each with an identical `avatars/ · angles/ · dcts/ · _drafts/ · CONTEXT.md` skeleton, plus a `_TEMPLATE/`. Almost every date-stamped folder collapses INTO one of the 3 campaigns as a `dcts/DCTxxx/` or `_drafts/` entry. This is a real restructure, not a rename.

**LIVE-WAVE reality check (correcting the task framing):** The 10-5-5 proof wave (`dct-10-5-5-proof-260603/`) is **NOT live on Meta**. Its `dct-tracker.json` shows all 5 angles `status: DRAFT`, images mostly unrendered (only 1 of 10 rendered: `DCT010-A01-v1`), Canva links empty, and a hard rule that it writes ONLY to *test* sheet tabs. **Note:** inside `dct-tracker.json` the `creatives_test_tab` / `copy_test_tab` fields are literal `TBD_at_phase5` placeholders — the *resolved* test-tab gids (`CREATIVES_10x5x5_TEST` gid 1443650484 / `COPY_10x5x5_TEST` gid 1125162846) live in `_brand/metrics-config.json` (the `buyer-funnel-10-5-5-test` block, label "TEST TABS ONLY — not for live metrics"), NOT in the tracker. The wave writes only to those test tabs — never the live CREATIVES/COPY tabs, never the meta_puller. "LIVE" in `_campaigns-index.json` / CONTEXT.md means **live in the TEST sheet tabs**, i.e. data was written there 260603. The genuinely live-on-Meta wave is **`dct-260417`** (buyer-funnel, Meta campaign `52569405524110`, DCT001–009-B "shipped"). Both still carry breakage risk — see §4.

---

## 2. Migration table (current → target)

Target root = `clients/neezanizam/`. Campaign mapping is driven by `_campaigns-index.json` + CLAUDE.md routing law.

### 2a. Top-level + identity

| Current | Target | Notes |
|---------|--------|-------|
| `CLAUDE.md` | `CLAUDE.md` (rewrite) | Phase 2. Hardcodes OLD paths (`campaigns/dct-260417/`, `dct-260421/`, `dct-260419/`, `campaigns/angles/`, `campaigns/funnel`) — these BREAK on move and must be rewritten. "Two Metrics-Campaigns" → "Three campaigns". |
| `CONTEXT.md` | `CONTEXT.md` (rewrite) | Phase 2. Same hardcoded old paths in File-routing + Active-work + Common-commands. |
| `context-profile.json` | `context-profile.json` | Unchanged (spec §1). |
| `_research-meta-flex-tracking.md` | `_brand/` or keep top-level | Referenced by spec LOCKED §5 as the research basis. Move to `_brand/` or `_swipe/research/`. **UNCLEAR** — operator decision. |
| `_reorg-spec.md` | DELETE after Phase 6 | Spec §8.6 says delete. |
| `_reorg-dataflow.html` | DELETE after Phase 6 | Companion to the spec; same lifecycle. |
| `.herenow/`, `.DS_Store` | (housekeeping) | `.DS_Store` → delete; top-level `.herenow/state.json` → keep (here.now publish state). NOTE a SECOND `.herenow/state.json` lives under `campaigns/thomson-reserve-260530/` — see §2d. |
| `.claude/settings.local.json` | `.claude/settings.local.json` | KEEP. Per-client Claude Code permissions/settings. Not part of the reorg tree but must NOT be dropped. |
| `.claude/scheduled_tasks.lock` | **DECISION: delete or regenerate** | Cron lock for the NeezaNizam Modal/scheduled job (130 bytes, written 260531). Tied to R1/R2 — the freeze pauses that cron. A STALE lock can block or confuse the puller's next run. Recommend **delete** during the freeze (it regenerates on next legit run); do NOT silently carry it across the move. **Operator confirm.** |

### 2b. `_brand/` — mostly stays, gains structure

| Current | Target | Notes |
|---------|--------|-------|
| `_brand/offer.md`, `buyer-profile.md`, `brand-voice.md`, `source-of-truth.md`, `CONTEXT.md`, `_index.md`, `icp.md`, `learnings.md`, `story-bank.md`, `channels.json`, `notebooklm.json`, `asset-map.md` | same paths | Stable factory. `learnings.md` becomes the cross-campaign memory (spec §0/§5). |
| `_brand/metrics-config.json` | `_brand/metrics-config.json` | KEEP. Add `thomson-reserve` block (spec §1 comment). **LIVE — see §4 risk.** |
| `_brand/avatars/avatar-{1,2,3,4}.md` | same paths | **GAP: no YAML frontmatter.** Spec §2 requires `id / name / mass_desire / awareness / sophistication / used_by_campaigns[] / status` + an `<!-- AUTO: angle-performance -->` rollup block. Phase 3 adds these. Not data loss — a schema upgrade. |
| `_brand/avatars/_index.md` | same | Already canonical-names SSOT. Spec wants it to also carry `used_by_campaigns[]` per avatar. |
| `_brand/avatars/first-time-buyers/ftb-{1,2}.md` + `_index.md` | `_brand/avatars/first-time-buyers/` | Unchanged (spec §1 keeps `first-time-buyers/`). |
| `_brand/avatars/avatar-backlog.md`, `avatar-coverage-map.md`, `first-time-buyer-research.md`, `research-prompts.md`, `sophistication-map.md` | `_brand/avatars/` | Keep. Supporting docs. |
| `_brand/brand-assets/DESIGN/**` | `_brand/brand-assets/DESIGN/` | Unchanged (spec §1). Read-before-render asset. |
| `_brand/source-of-truth-draft.json` | `_brand/` | Keep (in-flight SoT). |
| `_brand/metrics-config.json.bak-260420`, `.bak-260603-pre-10-5-5`, `source-of-truth-draft.json.bak-260419` | **STALE → archive/delete** | Superseded backups. See §3 STALE. |

### 2c. `_swipe/` — stays as L3 factory (spec §1 keeps `_swipe/`)

| Current | Target | Notes |
|---------|--------|-------|
| `_swipe/research/**` (dossiers, big-ideas, raw/, testimonials/) | `_swipe/research/` | Unchanged. The spotter's raw inputs. |
| `_swipe/headline-banks/wave-{1,2}-headline-bank.md` | `_swipe/headline-banks/` | Unchanged. |
| `_swipe/competitor-ads/*-raw.md` | `_swipe/swipe-files/` (spec §1 names it `swipe-files/`) | Folder rename `competitor-ads/` → `swipe-files/` OR keep; reconcile with existing `_swipe/swipe-file*.md` loose files. **Minor UNCLEAR.** |
| `_swipe/swipe-file.md`, `swipe-file-buyers.md`, `swipe-file-sellers.md`, `wave-reserved-angles.md`, `hook-library.md` | `_swipe/` | Keep at root or fold into subfolders. `hook-library.md` is named in spec §1. |

### 2d. `campaigns/` — the heart of the restructure

| Current | Target | Notes |
|---------|--------|-------|
| `campaigns/_campaigns-index.json` | `campaigns/_campaigns-index.json` (regenerate) | Spec Phase 2. Must list the 3 NEW campaigns, not the 6 current date-stamped slugs. **LIVE registry — see §4.** |
| `campaigns/dct-260417/` (live wave, DCT001-009-B, buyer-funnel) | `campaigns/buyer-funnel/dcts/DCT001…/` (split per-DCT) + `_drafts/dct-260417` | The shipped Avatar-1 wave. 10 creatives in one tracker → spec wants per-DCT folders each with `dct.json + copy.md + prompts/ + renders/ + metrics.json`. **HIGHEST-RISK move (live on Meta).** |
| `campaigns/dct-260417/dct-tracker.json` | `…/dcts/DCTxxx/dct.json` (schema migrate) | Old `dct-tracker.json` schema → new `dct.json` schema (spec §4). Field rename + per-DCT split. |
| `campaigns/dct-260417/dct-tracker.json.bak-260420` | **STALE → delete** | Superseded backup. |
| `campaigns/dct-260417/image-prompts/DCT001-{A,B,C}.json` | `…/dcts/DCT001/prompts/` | Renders NOT yet generated (no `renders/`); matches DRAFT. |
| `campaigns/dct-260419/` (asset-progression, Avatar-2 sell-side) | `campaigns/asset-progression/dcts/DCT002…/` + `_drafts/` | Spec §1 explicitly: "asset-progression … dcts ← dct-260419". Copy UNCHANGED (260529 lock). |
| `campaigns/dct-260419/image-prompts/{DCT002,DCT003-*}.json + PROMPTS.md` | `…/dcts/DCTxxx/prompts/` | Per-DCT prompts. |
| `campaigns/dct-260421/dct-tracker.json` (buyer-funnel, Spousal Deadlock DCT3) | `campaigns/buyer-funnel/dcts/DCT003/` | 1 angle × 3 visual variants, DRAFT. |
| `campaigns/dct-10-5-5-proof-260603/` (proof wave, avatar-1, TEST tabs) | `campaigns/buyer-funnel/dcts/DCT010/` | **Live in TEST tabs — see §4.** 5 angles × 2 variants; only `DCT010-A01-v1` rendered. Keep its `CONTEXT.md` + `review-findings.md` alongside. |
| `campaigns/dct-10-5-5-proof-260603/image-prompts/renders/DCT010-A01-v1*.png (+ .meta.json)` | `…/dcts/DCT010/renders/` | The one rendered proof asset. Do NOT lose. |
| `campaigns/dct-260408/chatgpt-talking-head-scripts-prompt.md` | `campaigns/buyer-funnel/_drafts/` | Orphan one-file folder; referenceable draft. |
| `campaigns/ad-concepts-260406/` (12 prompts, headlines-all-40, generate.py, assets/) | `campaigns/buyer-funnel/_drafts/ad-concepts-260406/` | Spec §1 lists `ad-concepts-260406` as a `_drafts/` item. |
| `campaigns/angles/` (wave-1.md, wave-2.md, iteration-log.md, big-angle-spotter/, README.md, wave-1-vs-stage-analysis.md) | split: per-campaign `angles/` + `_spotter-runs/` | Spec §1: angles live PER-CAMPAIGN (`campaigns/<c>/angles/`). Current `campaigns/angles/` is a wave-level rollup that must be DECOMPOSED by avatar/campaign. **Biggest judgment call — see §5 UNCLEAR.** |
| `campaigns/angles/big-angle-spotter/wave-1/DCT{1,2,3}/`, `wave-2/comfort-upgrader/` | `campaigns/<c>/angles/_spotter-runs/` | Provenance. wave-1 DCT1/DCT2 → buyer-funnel; DCT3 → buyer-funnel (spousal); wave-2 comfort-upgrader → asset-progression (Avatar-2). |
| `campaigns/big-angle-spotter-runs/20260420-152524/` | `campaigns/<c>/angles/_spotter-runs/` | Duplicate-ish of `angles/big-angle-spotter/` provenance. See §3 DUPLICATE. |
| `big-angle-spotter-runs/20260529-225558/` (CLIENT-ROOT, 9 files: `01_angles.md`, `02_gate_resonance.md`, `03_pruned.md`, `04_ranked_angles.md`, `05_gate_top_angle.md`, `06_gate_novelty.md`, `07_expansion.md`, `inputs.json`, `system_prompt.txt`) | `campaigns/<c>/angles/_spotter-runs/20260529-225558/` | **Third spotter-run tree, at CLIENT ROOT (not under `campaigns/`).** 260529 run. Route by the avatar in `inputs.json` (the 260529 angles lock = Avatar-2 asset-progression). Easy to miss in a `campaigns/`-only sweep — give it its own move. See §3 DUPLICATE #2. |
| `campaigns/funnel/ghl-setup-notes.md`, `qualification-form-copy.md` | `_brand/funnel-setup.md` | Spec §1 explicit: "`funnel-setup.md` ← was `campaigns/funnel/`". Promotes to `_brand/` (stable). |
| `campaigns/metrics/test_260416_1811.json` | `campaigns/buyer-funnel/dcts/<DCT>/metrics.json` OR delete | Single stale test pull. Likely STALE — see §3. |
| `campaigns/sheet-snapshots/*.json` (21 files, verified) | `campaigns/_sheet-snapshots/` | Spec §1: `campaigns/_sheet-snapshots/`. Audit trail — keep all. Note `_` prefix added. |
| `campaigns/sheet-snapshots/` (21) vs top-level `sheet-snapshots/` (2 proof-wave files) → 23 total | merge → `campaigns/_sheet-snapshots/` | **TWO snapshot dirs exist** (split trap). Merged dir must end with 23 files. See §3 DUPLICATE. |
| `campaigns/dashboard.html` | `campaigns/` or `output/` | Standalone dashboard (Apr-20). Keep; reattach to new tree. |
| `campaigns/feedback/` (empty dir) | drop | No files. |
| `campaigns/buyer-funnel/` (ALREADY EXISTS — partial) | `campaigns/buyer-funnel/` | **Half-migrated already.** Holds `cartoon-ads-260606/`, `CBO_Test_BuyerFunnel_Apr26/`, `image-prompts/` (40 renders), `landing-pages/`. Reconcile with incoming dct-260417/421/proof. See §4. |
| `campaigns/buyer-funnel/CBO_Test_BuyerFunnel_Apr26/W1_DCT{1,2}_*/dct-tracker.json` | `campaigns/buyer-funnel/dcts/` | 3-2-2 trackers registered in `_campaigns-index.json`. |
| `campaigns/buyer-funnel/cartoon-ads-260606/` (40 renders + refs + scripts) | `campaigns/buyer-funnel/_drafts/cartoon-ads-260606/` | Spec §1 lists `cartoon-ads` as a `_drafts/` item. |
| `campaigns/buyer-funnel/image-prompts/` (40 renders, batch json, zip) | `campaigns/buyer-funnel/dcts/<DCT>/prompts|renders/` | Static batch 260606 (BF01–BF05). Map to whichever DCT they back. |
| `campaigns/buyer-funnel/landing-pages/*.html` | `campaigns/buyer-funnel/landing-pages/` | Spec §1 keeps `landing-pages/` per campaign. |
| `campaigns/firsttime-letter-260512/` (foundation-packet/ + v4-revision-brief) | `output/` OR `campaigns/buyer-funnel/_drafts/` | First-time-buyer sales letter work. Foundation-packet is a copywriting artifact, not a DCT. **UNCLEAR routing** (ftb avatars are DRAFT/founder-gated) — operator decision. |
| `campaigns/thomson-reserve-260530/` (large: refs, swipe, creatives, ugc, 60+ tr_* renders) | `campaigns/thomson-reserve/` | Spec §1: third campaign = launch (`thomson-reserve`), "same skeleton + reference/ creatives/". Folder rename drops the date stamp. Its internal `01_reference/`, `02_creatives/`, `_refs/`, `_swipe/` largely preserved. |
| `campaigns/thomson-reserve-260530/.herenow/state.json` | `campaigns/thomson-reserve/.herenow/state.json` | **NESTED here.now publish-state — carries 2 LIVE publish slugs** (`flint-tundra-whwk` → https://flint-tundra-whwk.here.now/, `silver-zephyr-83pf` → https://silver-zephyr-83pf.here.now/). The date-stamp-drop rename MUST carry this file with the folder, or those here.now publish targets orphan (a re-publish would mint a NEW slug instead of updating these). Distinct from the top-level `.herenow/` in §2a. |
| `campaigns/thomson-reserve-260530/02_creatives/.../prompts/_superseded/**` | **STALE → archive** | Already self-marked `_superseded`. See §3. |
| `campaigns/thomson-reserve-260530/02_creatives/.../renders-v4-archive/**` | **STALE → archive** | Self-marked `-archive`; v5/v6/v7 supersede. See §3. |

### 2e. `output/`, `meetings/`, `website/`, `assets/`

| Current | Target | Notes |
|---------|--------|-------|
| `output/sales-letters/**` (260421-v1 → 260425-v1.7, reviews/, build-logs/) | `output/sales-letters/` | Spec §1 keeps `output/` + sales-letters. Multiple versioned drafts — newest is `260425-v1.7.md`; older = STALE-ish but versioned history, keep. |
| `output/deliverables/onboarding-strategy-report-260411.pdf` | `output/deliverables/` | Keep. |
| `meetings/` (3 files) | `meetings/` | Unchanged (spec §1). |
| `website/` (16 files, propnex-listings-widget + .wrangler) | `website/` (do NOT move without verifying deploy) | **LIVE CLOUDFLARE WORKER — not inert site work.** `website/propnex-listings-widget/` holds `worker.js` (46KB, edited 260604) + `wrangler.toml` + a `.wrangler/state/v3/kv/…/*.sqlite` miniflare local KV store, plus `DEPLOY.md` and `squarespace-embed.html` / `squarespace-iframe-personal-plan.html`. A path move can break (a) the Worker's relative `.wrangler` local state and (b) the deploy if `wrangler.toml`/CI assumes this path. If the widget is embedded on a live PropNex/Squarespace page, moving it is a **breakage risk, not an org question**. **Verify embed status + deploy config BEFORE any move; prefer keep-in-place.** See §4 R9. |
| `assets/` (0 files) | drop | Empty dir. |
| `.claude/worktrees/mystifying-wu-249e7d/` (1,061 files) | **DELETE — ORPHAN NOISE** | See §3 ORPHAN #1. |

### 2f. NEW folders the spec requires that DON'T exist yet (net-new, Phase 1/3)

- `campaigns/_TEMPLATE/` (empty campaign skeleton: `CONTEXT.md`, `avatars/_index.md`, `angles/_ledger.json + _index.md`, `dcts/.gitkeep`)
- `campaigns/CONTEXT.md` (campaign room map — does not exist at `campaigns/` level)
- Per-campaign `avatars/_index.md` (bidirectional avatar anchor) — none exist
- Per-campaign `angles/_ledger.json` (machine angle rollup) — **none exist anywhere**
- Per-DCT `dct.json` (new schema), `copy.md`, `metrics.json` — none exist (current = monolithic `dct-tracker.json`)
- `_brand/funnel-setup.md` (← from `campaigns/funnel/`)

---

## 3. REMNANT / LOST REPORT

### LOST (referenced by an index/state file but MISSING on disk)
*No hard data-loss found.* Every `tracker_path` in `_campaigns-index.json` resolves to a real file on disk (all 6 dct-tracker.json verified present). The references that look "missing" are forward-looking placeholders, not lost files:
- `dct-tracker.json` blockers reference renders that were never generated (e.g. dct-260417 has only 3 prompt JSONs, no `renders/`; proof wave references 10 renders but only 1 exists: `DCT010-A01-v1`). These are **un-produced**, not **lost** — DRAFT state, expected.
- `_campaigns-index.json` notes `review: campaigns/dct-10-5-5-proof-260603/review-findings.md` → EXISTS. Good.
- CONTEXT.md references `_swipe/research/big-ideas/FINAL_ROLLUP.md` + `ROLLUP_AUDIT.md` → **BOTH EXIST on disk** (verified) — they are SYMLINKS into the source repo `/Users/jerel/AI workflows/nn-ads-big-ideas/rollup/`. The big-ideas dir actually holds **8 entries**, not the 2 an earlier listing implied: `avatar-2-scored.jsonl`, `avatar-2-top-candidates.md`, `avatar-2-buyer-scored.jsonl`, `avatar-2-buyer-top-candidates.md`, `avatar-3-scored.jsonl`, `avatar-3-top-candidates.md`, plus symlinks `FINAL_ROLLUP.md`, `ROLLUP_AUDIT.md`, `all_ideas.jsonl`, `ideas_by_chills.md` (→ `~/AI workflows/nn-ads-big-ideas/`). No data loss. **Symlink caveat:** they resolve only while that source repo is intact and reachable; the reorg must not break the relative-to-absolute symlink targets, but the rollups are NOT missing.
- CONTEXT.md references `../../swipe-files/property-sg/` (industry pool, outside the client folder) → **dir EXISTS on disk** (verified: `avatar-registry.json`, `research-pool.json`, `pages/`). However the specific file `swipe-files/property-sg/stage-analysis.md` that CONTEXT.md also names is **NOT present** (the pool is all-JSON, no `.md`) — that one path is a dangling pointer (renamed/never-built), but it lives OUTSIDE the client folder so the reorg does not touch it. Low stakes — fix the CONTEXT.md ref during the Phase-2 rewrite. The pool itself is not lost.

### ORPHAN (on disk, nothing references it — at risk of being dropped in a move)
1. **`.claude/worktrees/mystifying-wu-249e7d/` (1,061 files)** — stray full Marketing-repo clone (skills/, .github/, integration configs). Referenced by nothing. **Delete, do not migrate.** Gitignored, so it is invisible to git and easy to `cp -r` by accident.
2. `_reorg-dataflow.html` — companion to `_reorg-spec.md`; delete with the spec at Phase 6.
3. `campaigns/dashboard.html` — standalone HTML dashboard (Apr-20), referenced by no index. Keep but re-anchor.
4. `campaigns/dct-260408/` — one loose file (`chatgpt-talking-head-scripts-prompt.md`), in NO `_campaigns-index.json` entry. Orphan draft → `_drafts/`.
5. `campaigns/metrics/test_260416_1811.json` — single test pull, no tracker references it. Likely throwaway.
6. `campaigns/feedback/` — empty dir.
7. `assets/` — empty dir.
8. `website/` — 16 files, absent from the spec tree entirely. Orphaned relative to the reorg, but **NOT inert** — it is a live Cloudflare Worker (`worker.js` + `wrangler.toml` + `.wrangler` KV state). Real work, unrouted, and move-sensitive. See §2e + §4 R9.
9. `campaigns/firsttime-letter-260512/` — present, but ftb avatars are DRAFT/founder-gated and it is in no `_campaigns-index.json` entry. Orphan relative to the 3-campaign model.
10. `big-angle-spotter-runs/20260529-225558/` (CLIENT-ROOT, 9 files) — third spotter-run provenance tree, sitting at the client root (not under `campaigns/`). Referenced by no index. Easy to miss in a `campaigns/`-scoped sweep. Route to `campaigns/<c>/angles/_spotter-runs/` — see §2d row + §3 DUPLICATE #2.
11. `campaigns/thomson-reserve-260530/.herenow/state.json` — nested here.now publish state holding 2 live slugs. Travels with the thomson-reserve rename; orphaning it disconnects the here.now publish targets. See §2d.
12. `.claude/settings.local.json` + `.claude/scheduled_tasks.lock` — the `.claude/` dir's own contents (outside the deleted worktree). `settings.local.json` = KEEP (per-client CC settings); `scheduled_tasks.lock` = cron lock, decide delete/regenerate during the R1/R2 freeze. Neither is in any index. See §2a.

### STALE (superseded snapshots / backups — safe to archive or delete)
1. `_brand/metrics-config.json.bak-260420`
2. `_brand/metrics-config.json.bak-260603-pre-10-5-5`
3. `_brand/source-of-truth-draft.json.bak-260419`
4. `campaigns/dct-260417/dct-tracker.json.bak-260420`
5. `campaigns/thomson-reserve-260530/02_creatives/sales-letter-mockups-260603/prompts/_superseded/**` (~20 files, self-marked superseded)
6. `campaigns/thomson-reserve-260530/02_creatives/sales-letter-mockups-260603/renders-v4-archive/**` (self-marked archive; v5/v6/v7 supersede)
7. `campaigns/metrics/test_260416_1811.json` (also orphan)
8. `34 .DS_Store` files throughout (macOS cruft — strip during move)

### DUPLICATE (same role, two locations — split trap)
1. **Two sheet-snapshot dirs:** `campaigns/sheet-snapshots/` (21 files, verified) AND top-level `sheet-snapshots/` (2 proof-wave files). Spec wants ONE: `campaigns/_sheet-snapshots/` (23 files total). Merge both, watch for the 260603 proof-wave pair living in the top-level one.
2. **THREE big-angle-spotter provenance trees:** (a) `campaigns/angles/big-angle-spotter/wave-N/`, (b) `campaigns/big-angle-spotter-runs/20260420-152524/`, and (c) the CLIENT-ROOT `big-angle-spotter-runs/20260529-225558/` (9 files — has its own §2d migration row). Same artifact family (01_angles, 04_ranked_angles, gate files, ad-prompts). The third one lives at the client root, NOT under `campaigns/`, so a `campaigns/`-only sweep misses it. Consolidate all three into per-campaign `angles/_spotter-runs/`.
3. **`buyer-funnel/` partially pre-exists** while `dct-260417/421/proof` (also buyer-funnel) still sit as siblings — the campaign is half-migrated. Reconcile so each DCT lands once.
4. Avatar story-name "Hafiz & Siti" / "The Striving Upgraders" — deprecated aliases that must NOT re-appear as tags (already governed by `_brand/avatars/_index.md`; watch during any frontmatter add).

### UNCLEAR — needs operator decision (do not guess)
1. `campaigns/angles/` wave-level rollup (`wave-1.md`, `wave-2.md`, `iteration-log.md`, `wave-1-vs-stage-analysis.md`, `README.md`) → must be DECOMPOSED into per-campaign `angles/`. Which angles belong to buyer-funnel vs asset-progression is a judgment call (wave-1 = Avatar-1 buyer; wave-2 comfort-upgrader = Avatar-2 seller). Confirm split before moving.
2. `campaigns/firsttime-letter-260512/` (+ foundation-packet) → `output/` or `buyer-funnel/_drafts/`? ftb avatars are DRAFT/founder-gated.
3. `website/` (live Cloudflare Worker, 16 files) → keep in place is the SAFE default (path move risks the deploy + `.wrangler` local KV state — see §2e/§4 R9). Only fold into `_brand/brand-assets/` if confirmed NOT embedded live. Operator must confirm embed/deploy status before any move.
4. `_research-meta-flex-tracking.md` → `_brand/`, `_swipe/research/`, or keep top-level?
5. `_swipe/competitor-ads/` vs spec's `_swipe/swipe-files/` naming, and the loose `_swipe/swipe-file*.md` — reconcile into one convention.
6. `.claude/scheduled_tasks.lock` → delete or regenerate during the R1/R2 cron freeze? (A stale lock can block the puller's next run — recommend delete; confirm before the move.)

---

## 4. Risks if executed (esp. live-wave breakage)

**R1 — `_brand/metrics-config.json` is LIVE plumbing.** The Modal `meta_puller` + `ad_concept_sheet_writer.py` read `sheet_id`, `gid`s, `campaign_filter.campaign_ids`, and `--metrics-campaign` routing from it. The reorg renames campaigns (`dct-260417` → `buyer-funnel/`) and adds a `thomson-reserve` block. **If the puller's `metrics_campaign` keys or gids drift, daily metric writes hit the wrong tab or fail silently.** Freeze the puller (pause the cron) during the move; verify gids unchanged after.

**R2 — The genuinely live-on-Meta wave is `dct-260417`, not the proof wave.** Meta campaign `52569405524110` (buyer-funnel) is pulling. Splitting its monolithic `dct-tracker.json` into per-DCT `dct.json` files risks: (a) breaking the `BATCH`-name ↔ sheet-row ↔ Meta-ad-name thread the metric writer relies on; (b) losing the `_revision_history` / `_headline_source` provenance fields during schema migration. Migrate the schema in a worktree, diff old→new field-by-field, keep the old `dct-tracker.json` as `.bak` until a clean metric pull confirms the thread holds.

**R3 — Proof wave (`dct-10-5-5-proof-260603`) writes ONLY to TEST sheet tabs.** Its hard rule is "NEVER touch live CREATIVES (gid 1164222857) / COPY (gid 1695031878)". A careless move that re-points the test-tab routing at the wrong gid, or merges its test-tab snapshot into the live snapshot history, could leak proof data into live tabs on the next write. **Where the guard actually applies:** the proof tracker's own `creatives_test_tab` / `copy_test_tab` fields are unresolved placeholders (`"TBD_at_phase5"`) — there is nothing concrete to preserve there. The REAL test-tab gids (1443650484 / 1125162846) live in `_brand/metrics-config.json` under the `buyer-funnel-10-5-5-test` block. **Point the verbatim-preserve guard at that metrics-config block** (keep its `gid`s + the `_10x5x5_TEST` tab names + the `_note` "Live CREATIVES/COPY untouched" intact), not at the tracker placeholders. This is also why the concern is **forward-looking**: the wave is all-DRAFT (5 angles, only `DCT010-A01-v1` rendered, not live on Meta), so no proof data is flowing yet — the guard protects the FUTURE Phase-5 write, not an active one. The one rendered asset (`DCT010-A01-v1.png` + `-chumbox.png` + their `.meta.json`) must travel with the DCT.

**R4 — CLIENT FOLDER IS GITIGNORED → no recovery.** Confirmed: `git check-ignore` matches `clients/neezanizam/*`. There is NO git history to restore a lost file. Every move is irreversible without a manual backup. This elevates every ORPHAN above from "low risk" to "gone forever if dropped."

**R5 — Hardcoded paths in CLAUDE.md + CONTEXT.md break on move.** Both files name old paths (`campaigns/dct-260417/`, `dct-260421/`, `dct-260419/`, `campaigns/funnel`, `campaigns/angles/`). After the folder move, every one of these is a dangling pointer until Phase 2 rewrites them. Agents reading the stale CLAUDE.md mid-migration will route writes to non-existent folders. Do the path rewrite in the SAME phase as the move, not after.

**R6 — The 1,061-file worktree gets swept into a `cp -r`.** If migration uses a recursive copy of `campaigns/` or the client root, the gitignored worktree rides along, doubling the tree and burying real files. Delete it FIRST.

**R7 — Avatar frontmatter add (Phase 3) could break the canonical-name contract.** Adding `used_by_campaigns[]` etc. to `avatar-{1..4}.md` must not introduce a deprecated alias as a tag. The `_brand/avatars/_index.md` SSOT table governs this; honor it.

**R8 — Two snapshot dirs + three spotter-run dirs invite a half-merge** that silently drops the 260603 proof-wave snapshot pair (only in the top-level `sheet-snapshots/`). Inventory both before merging. (The 21 `campaigns/sheet-snapshots/` + 2 top-level = 23 snapshot files total — verify the merged `campaigns/_sheet-snapshots/` ends with all 23.)

**R9 — `website/propnex-listings-widget/` is a LIVE Cloudflare Worker, not inert files.** It contains `worker.js` (46KB, edited 260604), `wrangler.toml`, a `.wrangler/state/v3/kv/…/*.sqlite` miniflare local KV store, and a `DEPLOY.md` + two `squarespace-*.html` embed snippets. **A path move can break: (a)** the Worker's relative `.wrangler` local state, and **(b)** the deploy if `wrangler.toml` / any CI step assumes this directory. If the widget is embedded on a live PropNex/Squarespace page (the `squarespace-embed.html` strongly implies it is), moving it can take the live embed down. **Before any move: confirm whether it is embedded live and how it deploys. Default = leave `website/` in place** (it is outside the spec tree anyway — §2e). This is a deploy/wave risk the org-placement framing missed.

---

## 5. Recommended pre-move safeguards

### Step 0 — TAR BACKUP (mandatory; folder is gitignored, no other recovery)
```bash
cd "/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing"
# Exclude the 1,061-file worktree noise and .DS_Store from the backup
tar --exclude='clients/neezanizam/.claude/worktrees' \
    --exclude='.DS_Store' \
    -czf ~/neezanizam-prereorg-backup-$(date +%y%m%d-%H%M).tar.gz \
    clients/neezanizam
# Verify it is non-trivial and listable
ls -lh ~/neezanizam-prereorg-backup-*.tar.gz
tar -tzf ~/neezanizam-prereorg-backup-*.tar.gz | wc -l   # expect ~774 (808 − 34 .DS_Store), NOT ~1800
```

### Step 1 — Delete the worktree noise BEFORE anything else
```bash
rm -rf "clients/neezanizam/.claude/worktrees/mystifying-wu-249e7d"
# Re-count to confirm: from 1,869 → 808 files (verified exact: 808 real, of which 34 are .DS_Store → ~774 signal)
find clients/neezanizam -type f | wc -l
```
NOTE: only the `worktrees/` SUBdir is noise. The `.claude/` dir's other two files — `settings.local.json` (keep) and `scheduled_tasks.lock` (cron lock — decide delete/regenerate in Step 2's freeze) — must survive this delete. The `rm -rf` above targets only `worktrees/`, so they are safe; just don't widen it to `rm -rf .claude`.

### Step 2 — Freeze the live plumbing
- Pause the NeezaNizam Modal cron / `meta_puller` job (it writes to live + test tabs daily). Confirm no scheduled write fires mid-move.
- During the freeze, decide `.claude/scheduled_tasks.lock`: delete it (recommended — regenerates on next legit run) so a stale lock can't block the puller's resume. Do NOT carry the lock across the move silently.
- Confirm `website/propnex-listings-widget/` is NOT mid-deploy and check whether its Worker is embedded live (DEPLOY.md + squarespace-embed.html). If embedded, leave `website/` in place — do not move it (§4 R9).
- Snapshot the current live sheet state once more (`scripts/...sheet-snapshots`) so post-move you can diff.

### Step 3 — Dry-run order (lowest-risk → highest)
1. **STALE/ORPHAN cleanup first** (reversible via the tar): delete `.DS_Store`, `feedback/`, `assets/`, `*.bak-*`, `_superseded/`, `renders-v4-archive/`. Re-count.
2. **Stable factory next** (`_brand/`, `_swipe/`): low blast radius — promote `campaigns/funnel/` → `_brand/funnel-setup.md`, fix any path refs.
3. **`thomson-reserve` (NOT live on Meta):** rename `thomson-reserve-260530/` → `thomson-reserve/`. Safe — no metric plumbing.
4. **Proof wave (test tabs):** `dct-10-5-5-proof-260603/` → `buyer-funnel/dcts/DCT010/`. Preserve test-tab refs + the rendered asset.
5. **`asset-progression` (live filter `6665612766106`):** `dct-260419/` → `asset-progression/dcts/`. Verify metrics-config gids after.
6. **LIVE buyer-funnel wave LAST** (`dct-260417`, Meta `52569405524110`): split monolithic tracker → per-DCT `dct.json`, keep `.bak`, diff the BATCH-name thread, run one test metric pull, confirm clean BEFORE deleting the `.bak`.
7. **Rewrite CLAUDE.md + CONTEXT.md paths in the same commit as the move** (R5).
8. **Net-new scaffolds** (`_TEMPLATE/`, `_ledger.json`, per-campaign `avatars/_index.md`, avatar frontmatter) — additive, do last.

### Step 4 — Per-campaign worktree isolation (spec Phase 1 says so)
Run each campaign's migration in its own git worktree/branch so a botched split is isolated. After each, verify: (a) every `tracker_path` in the regenerated `_campaigns-index.json` resolves; (b) no `dct.json` references a missing prompt/render; (c) metrics-config gids unchanged; (d) grep the moved tree for old path strings.

### Step 5 — Post-move integrity gate
```bash
# Nothing should still point at the OLD paths after Phase 2:
grep -rn "dct-260417\|dct-260419\|dct-260421\|dct-10-5-5-proof\|campaigns/funnel\|campaigns/angles" \
  clients/neezanizam --include="*.md" --include="*.json" | grep -v _drafts | grep -v _spotter-runs
# Expect: empty (or only intentional _drafts/ provenance mentions).

# Account for every previously-unmapped item — all should be present, none orphaned:
ls clients/neezanizam/.claude/settings.local.json                         # KEEP — must exist
ls clients/neezanizam/campaigns/*/angles/_spotter-runs/20260529-225558/   # client-root run rehomed
find clients/neezanizam -path '*thomson-reserve*/.herenow/state.json'      # nested here.now state carried
# Snapshot count: 21 (campaigns) + 2 (top-level) = 23 should all land in _sheet-snapshots/:
ls clients/neezanizam/campaigns/_sheet-snapshots/*.json | wc -l           # expect 23
# website/ Worker still in place (NOT moved unless deploy verified):
ls clients/neezanizam/website/propnex-listings-widget/worker.js
```

---

## ADDENDUM — worktree salvage (discovered DURING execution, 260608-1520)

**§3 ORPHAN #1 / §2e / R6 were WRONG about the worktree.** They called `.claude/worktrees/mystifying-wu-249e7d/` "pure noise, referenced by nothing, DELETE." On execution this proved false and nearly cost a real deliverable:

- It was a **git-registered worktree** (branch `claude/mystifying-wu-249e7d`, 0 unmerged commits, working tree dated 2026-04-21), not an orphan clone — removed with `git worktree remove --force`, not `rm -rf`.
- **Two real files referenced its path** — `_brand/learnings.md:178` and `campaigns/firsttime-letter-260512/v4-revision-brief.md`, which warned verbatim: *"If the worktree is ever cleaned up, the letter path breaks entirely."*
- Its working dir held the **only copy** of 11 gitignored NeezaNizam deliverables (absent from main AND from the first backup, which excluded the worktree path):
  - `copy/` (8): `sales-letter-v4-firsttime.md` (147 lines, real) + `-skeleton.json`/`-skeleton-summary.md`/`-audit.md`, `sales-letter-v3-firsttime.md`, `sales-letter-v2-strategic.md`, `headline-experiments.md`, `sales-letter-deai-pass.md`
  - `reverse/` (3): `customer-avatar-inferred.md`, `mass-desires-inferred.md`, `purple-ocean-inferred.md`
  - plus untracked global skill `skills/letter-critic/` (4 files)

**Action taken (all verified byte-identical via `diff -rq`):**
- `copy/` + `reverse/` salvaged to `clients/neezanizam/copy/` + `clients/neezanizam/reverse/` (worktree-relative path). These are NEW inputs the original map didn't know about — final placement decided in the firsttime-letter tier (§5 UNCLEAR #2).
- `letter-critic/` parked at `clients/neezanizam/_salvaged-from-worktree/letter-critic/` — **OPERATOR DECISION PENDING:** promote to global `skills/` or discard.
- Authoritative backup re-taken WITH salvage: `~/neezanizam-prereorg-SALVAGED-260608-1525.tar.gz` (793 real files, gzip-verified).
- Worktree removed; merged branch `claude/mystifying-wu-249e7d` deleted; tree **1,869 → 823 files**.

**Correction to §3 LOST (line ~132 was already right, flagging here for the record):** `FINAL_ROLLUP.md` / `ROLLUP_AUDIT.md` are NOT lost or never-built — they are **symlinks** into `~/AI workflows/nn-ads-big-ideas/` and resolve. The reorg must preserve the symlink targets; there is no dangling reference to fix.

**Lesson:** never delete a worktree on an audit's say-so. A worktree working dir can hold gitignored client deliverables that exist nowhere else. Always (1) check who references its path, (2) inventory files unique to it vs main, (3) salvage + back up, THEN remove. Logged to `learnings/reorg-worktree-salvage.md`.
