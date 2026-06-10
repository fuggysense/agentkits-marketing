# Session Handoff — NeezaNizam ICM reorg + DCT/asset structure (content-spine groundwork)

_Date: 2026-06-08 (SGT). Branch: main. Background processes: none._

## Where it started

Combine two prior sessions (10-5-5 angle generation + a NeezaNizam folder reorg) into one comprehensive workflow, then "see how it fits with the sales-letter-method." It expanded into: writing the content-spine spec, executing the NeezaNizam reorg, and designing the DCT/image-asset organization.

Framing that emerged: the reorg is the proving ground for a repeatable, orchestrator-knowable client structure. Two prior-session reads corrected the premise — both were really big-angle-spotter work on the **Eugene** client; "LISM" is no client; the reorg existed only as a locked spec.

## Decisions locked + what shipped

- **Content-spine spec** — `.claude/workflows/content-spine-workflow.md`. Layer 1→2→3, conditional keystone (letter-when-fits / source-of-truth-when-not), letter→downstream cascade contract. Reviewed (strong pass), 11 fixes applied.
- **NeezaNizam reorg EXECUTED** (was spec-only) — 1,869 → ~770 files, 3 offer-campaigns: `buyer-funnel`, `asset-progression`, `thomson-reserve`. All file moves invariant-checked (no loss).
- **Worktree salvage (data-loss near-miss)** — the audit said "delete the worktree, referenced by nothing"; it actually held the ONLY copy of the V4 first-time-buyer sales-letter lineage (8 files) + 3 reverse docs + a letter-critic skill, all gitignored + excluded from the first backup. Salvaged → `clients/neezanizam/output/sales-letters/firsttime-buyers/` (letters) and `clients/neezanizam/_salvaged-from-worktree/letter-critic/` (skill, parked).
- **Authoritative backup** — `~/neezanizam-prereorg-SALVAGED-260608-1525.tar.gz` (793 real files, gzip-verified). Folder is gitignored = this tar is the only undo.
- **DCT model locked** — 5 angles per DCT (operator override of spec's 1-angle); one avatar is the constant (one DCT = one ad set); images = flat pool of ≤10, `DCT<NNN>-img-<NN>`, Meta-mixed, NOT angle-tied; copy+headlines = the 5 angles. Tracking = blended ad-set CPL + per-asset CTR (directional).
- **Canonical rules** — `clients/neezanizam/CLAUDE.md` § "DCT & asset structure". `_TEMPLATE` skeleton + `_inbox` pools + `_assets.json` image ledgers on all 3 campaigns + `campaign_type` CONTEXT.md contracts (dct/dct/launch).
- **DCT010 worked example** — `dct.json` manifest + `copy.md` + `images/` + `_preview.html` (additive; legacy `dct-tracker.json` untouched).
- **Learning logged** — `learnings/reorg-worktree-salvage.md` (never delete a worktree on an audit's say-so).

## Key files for next session

- `docs/neezanizam-reorg-migration-map.md` — full migration record + the ADDENDUM (salvage + audit corrections). **Read first.**
- `.claude/workflows/content-spine-workflow.md` — the spine spec the reorg serves.
- `clients/neezanizam/CLAUDE.md` — canonical DCT/asset law (§ DCT & asset structure).
- `clients/neezanizam/campaigns/buyer-funnel/dcts/dct-10-5-5-proof-260603/dct.json` + `_preview.html` — the worked example of the target shape.
- `learnings/reorg-worktree-salvage.md`
- Memory files touched: none (chat + repo only).

## Running state

- Background processes: none (both workflows — `wswv17her`, `wa5u7ak88` — completed).
- Dev servers / ports: none.
- Open worktrees / branches: none (the stray `clients/neezanizam/.claude/worktrees/mystifying-wu-249e7d` was salvaged + `git worktree remove`d; branch `claude/mystifying-wu-249e7d` deleted). On `main`.

## Verification — how to confirm things still work

> **Verified 2026-06-08: all 7 checks PASS** (sub-agent audit). Two notes: file count is **784**, not exactly ~770 (within tilde); the spec/map/learning files live at repo level (`.claude/workflows/`, `docs/`, `learnings/`), not under `clients/neezanizam/`. Salvage tar is **432 MB** — confirm that scope is intended.

> Pass the repo path via env var — the apostrophe in "Jerel's brain" breaks inline `python3 -c 'open("...")'` (bit me 3× this session).

- `F=".../clients/neezanizam/campaigns/_campaigns-index.json" python3 -c "import json,os; d=json.load(open(os.environ['F'])); print(len(d['campaigns']),'campaigns')"` → 6 entries, all `tracker_paths` resolve.
- `grep -m1 campaign_type ".../campaigns/<c>/CONTEXT.md"` for each of the 3 → dct/dct/launch.
- `find ".../clients/neezanizam" -type f | wc -l` → ~770 (was 1,869; ~1,061 worktree junk removed).
- `tar -tzf ~/neezanizam-prereorg-SALVAGED-260608-1525.tar.gz | grep -c sales-letter-v4-firsttime` → ≥1 (salvage is in the backup).

## Deferred + open questions

- **Deferred #8** — per-DCT tracker split (monolithic `dct-tracker.json` → per-DCT `dct.json`) + rewrite of the 6 coupled ad-creation scripts. Needs the Modal puller paused + tested; it's a code change, not a file move.
- **Deferred #9** — internal-reference cleanup (stale `dct-*/thomson-reserve-260530` mentions inside trackers' `image_prompts_dir`, `source-of-truth.md`, wave docs, meetings), avatar YAML frontmatter, per-campaign `angles/_ledger.json`, delete `_reorg-spec.md`.
- **Deferred #10** — `render.py` append + `allocate <DCT> <image-id>` helper (image-first one-command flow). Operator chose propose-not-build.
- **Deferred #6/#7** — content-spine folder homes + cascade wiring; skill-trim diagnosis (routing-tester). Started conceptually, not built.
- **Open** — letter-critic skill: promote to global `skills/` or discard (parked in `_salvaged-from-worktree/`).
- **Open** — `scripts/modal/ONE_CLICK_ONBOARDING_PLAN.md`: fold into `client-onboarding` as its external-provisioning sub-step, or leave parked. Recommended folding-in + doing one more manual onboarding first; user didn't answer.

## Pick up here

1. **Build #10** — the `render.py` / `allocate` image-first automation (`scripts/ad-images/render.py`).
2. **Eugene (`clients/eugene-chieng/`) — Skill + pipeline.** Skill: `big-angle-spotter` (project skill in Marketing repo, but a **symlink** to `~/AI workflows/big-angle-spotter`, where the real code lives). Pipeline: `scripts/run_pipeline.py` in that repo — the orchestrator that runs all 12 steps; each step spawns its own fresh `claude -p` worker, then passes the relevant prior output forward. When the skill is invoked, its only job is to collect inputs and launch `run_pipeline.py` — the script is the actual engine.

**Constraint:** these must not overlap and clash — the project-repo skill (symlink) and the real `~/AI workflows` code should stay identical. While Eugene dev proceeds, the overlap between NeezaNizam's image tooling (Build #10 render/allocate + DCT image-pool convention) and the big-angle-spotter pipeline's image-gen output needs to be checked.

> **→ Overlap analysis: `docs/ad-image-tooling-overlap-260608.md`** (generated this session — read before building Build #10 or wiring big-angle-spotter into a DCT folder).

**Overlap verdict (2026-06-08):** the two systems are **complementary, not clashing** — BAS emits text image-gen prompts only (verified: zero renders), `render.py` is the only renderer, `allocate` (unbuilt) is the only DCT-namer. Symlink is intact (no divergent copy). Build #10 blockers: (1) ~~missing overlap doc~~ → now written; (2) ~~NeezaNizam internal contradiction~~ → **resolved 260608**: one image = one DCT by default, `allocated_to` array kept for flex, `allocate` = MOVE semantics (fixed in CLAUDE.md §DCT + `dct.json` + `_assets.json`); (3) **decided 260608** — do **Deferred #8** (tracker split + rewrite the 6 ad-creation scripts, pause the Modal puller) FIRST, then Build #10, so `render.py`/`allocate` read canonical `dct.json` not legacy `dct-tracker.json`.

**Decided 260608 (operator grill):** image↔DCT = one-by-default-flexible · `allocate` = MOVE · Eugene adopts `_assets.json` agency-wide · BAS final-angle-count should be **votable** (DCT wants 5, BAS emits top-3 — ship as a `--top-n` param, never a per-client fork). Full record: `docs/ad-image-tooling-overlap-260608.md` §Decisions locked.

**`allocate` guard contract (locked 260608):** signature is now `allocate <DCT> <render-file>` (tool auto-assigns the slot — no image-id arg). Guards: auto-next slot (collision impossible) · fail-closed on any forced collision · check-all-then-move + `--dry-run` (verify pool≤10 + slot-free + both files writable before moving) · **11th image → refuse, suggest a similar DCT with room (same avatar→offer, same campaign), else keep the render in `_inbox` as available — never discard** · two-file (`dct.json`+`_assets.json`) atomic write with rollback. Full spec: overlap doc §`allocate` contract. Biggest invisible risk: a forked copy of the global pipeline `cp`'d into a gitignored client tree — guard the symlink.

**Reality note on the Eugene premise:** `clients/eugene-chieng/` has **no big-angle-spotter output, no DCT folders, no `_assets.json`, no rendered ad-images** on disk (snapshot 2026-06-08). Active Eugene work is the MP1 sales letter + landing page (`campaigns/mp1-upgrader-letter-260603`, stage body-draft-v3-in-review). If BAS-in-Eugene is starting, it's a clean slate — decide Eugene's image source-of-truth (NeezaNizam's campaign `_assets.json` vs Eugene's documented `ad-concepts/` + `input-image-manifest.json`) **before the first run** to avoid a per-client convention fork.
