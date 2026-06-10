# Ad-Image Tooling Overlap — NeezaNizam render/allocate vs big-angle-spotter

_Generated 2026-06-08. Pre-build gate for Build #10 (`scripts/ad-images/render.py` + `allocate`) and for wiring big-angle-spotter into any client DCT folder. Referenced from `clients/neezanizam/SESSION-HANDOFF-260608.md` line 62._

_Method: 4 parallel sub-agent deep-reads (NeezaNizam image tooling, the big-angle-spotter pipeline, Eugene's on-disk state, handoff verification) → synthesis. Every claim below traces to a file/line a reader can re-check._

---

## TL;DR

The two systems **do not clash today.** They are sequential stages of one pipeline, not two tools fighting for the same job:

```
big-angle-spotter            render.py                 allocate (UNBUILT)
─────────────────            ─────────                 ──────────────────
angles → headlines           prompt → PNG              PNG → DCT pool slot
→ image-gen PROMPTS    →      (Azure gpt-image-2)  →    + dct.json/_assets.json
(text only, own run dir)      writes flat-named PNG     strips angle identity
```

Verified non-overlap: big-angle-spotter **never renders** (the only subprocess in its 1,493 lines is `claude -p` — zero Azure/diffusion/PNG calls), **never writes** to `scripts/ad-images/` or any client DCT folder, and is **unaware** of `DCT<NNN>-img-<NN>` or `_assets.json`. `render.py` is the only renderer; `allocate` (not yet built) is the only thing that mints DCT image IDs. So the worst fear — two tools rendering the same PNG or writing the same file — is **not present.**

The real risks are narrower and all sit at the **handoff seam** or are **internal to NeezaNizam**. None is a territory war. Don't build Build #10 until the three blockers below are cleared.

---

## Decisions locked (2026-06-08, operator grill)

1. **Image ↔ DCT:** one image = one DCT **by default**, kept flexible. `allocated_to` stays an array for forward-compat but holds exactly one DCT today; cross-DCT sharing is opt-in, never default. Per-image CTR assumes single ownership. → fixed in `CLAUDE.md` §DCT, `dct.json` format string, `_assets.json` schema string.
2. **`allocate` semantics:** **MOVE**, not copy. One canonical file in `images/`, pre-move filename recorded as `source` in `dct.json`. (Legacy DCT010 has a copy-dupe from before the rule — reconcile when `allocate` is built.)
3. **Eugene convention:** adopt the `_assets.json` ledger model **agency-wide** so `render.py`/`allocate` run unmodified everywhere. Eugene's `input-image-manifest.json` is for INPUT refs (a different stage) — coexists. Update Eugene `CONTEXT.md` when ad work starts.
4. **Sequencing (#8 vs #10):** **#8 first, then #10.** Split the monolithic `dct-tracker.json` into per-DCT `dct.json` + rewrite the 6 ad-creation scripts (pause the Modal puller, test) BEFORE coding `render.py`/`allocate`, so `allocate` reads the canonical schema — no rework.
5. **big-angle-spotter enhancement (operator idea):** make the **final angle count votable**, not hard-locked at 10→top-3. The DCT model wants **5** angles (A01–A05); BAS today emits top-3 — a real seam gap. Ship as a global pipeline **parameter** (`--top-n` / `inputs.json`), never a per-client pipeline fork.
6. **`allocate` guard contract:** locked — see the dedicated section below.

---

## `allocate` contract (locked 2026-06-08 — build spec for Build #10)

Signature changes from the original sketch: **`allocate <DCT> <render-file>`** — the operator no longer types an image id; the tool assigns it (decision 1).

1. **Slot assignment — AUTO-NEXT.** `allocate` scans the DCT's `images/` pool and assigns the next free `DCT<NNN>-img-<NN>`. The operator never picks a number → slot collision is impossible by construction. (If a `--slot NN` override is ever added later, rule 2 governs it.)
2. **Collision — FAIL-CLOSED.** If a specific slot is ever targeted (override path) and already occupied, refuse with a clear message and change nothing. No overwrite without an explicit future `--force` (which would park the displaced file in a recoverable trash, never hard-delete).
3. **Move safety — CHECK-ALL-THEN-MOVE (atomic) + `--dry-run`.** Before touching the file, verify in order: (a) pool not full (≤10), (b) target slot free, (c) both `dct.json` and `_assets.json` writable. Only if all pass: move the render from `_inbox/` → `dcts/DCT<NNN>/images/DCT<NNN>-img-<NN>.png`, record the pre-move filename as `source` in `dct.json`, flip `_assets.json` status `available`→`allocated`, set `allocated_to: ["<DCT>"]`. Any check fails → abort, nothing changed. `--dry-run` prints the full plan (target slot + both file diffs) and spends/moves nothing.
4. **Pool full (the 11th) — REFUSE → REROUTE → NEVER DISCARD.** If the DCT is already at 10:
   - **Refuse** the allocation into this DCT.
   - **Suggest siblings:** scan the campaign for *similar* DCTs with a free slot and print them as alternatives — e.g. `DCT010 full (10/10). DCT012 (same avatar, 6/10) and DCT014 (4/10) have room → re-run: allocate DCT012 <render>`. "Similar" precedence: same `avatar` first, then same `offer`, within the same campaign. _(Confirm precedence at build time.)_
   - **Keep the render:** if no similar DCT has room, leave the file in `_inbox/` as `available` — never delete or reject it. Operator decides later.
5. **Two-file integrity.** `dct.json` (per-DCT manifest) and `_assets.json` (campaign ledger) update together. On any write failure after the move, roll the file back to `_inbox/`. A cheap post-write consistency check (image present in both, statuses agree) is the insurance.

---

## Honest premise check — read this first

The task assumed big-angle-spotter is "being developed in Eugene's folder right now." **On disk, it isn't.** `clients/eugene-chieng/` has zero spotter output, zero DCT folders, zero `_assets.json`, zero rendered ad-images. The newest files there (dated 5 Jun) are all the **MP1 sales letter + its landing page** — not ad-image work. The whole tree is gitignored, but uncommitted work still lands as files, and there are none.

So either the BAS-in-Eugene work hasn't started, is happening in a scratch dir outside the client tree, or "Eugene" is shorthand for the big-angle-spotter repo itself (`~/AI workflows/big-angle-spotter`, edited today). **There is nothing in Eugene to clash with yet** — which is the good news: Eugene is a clean slate, so the convention decision (below) can be made right, before the first run, instead of retrofitted.

---

## "Both should be the same" — symlink check: PASS (with one real risk)

Both `skills/big-angle-spotter` and `.claude/skills/big-angle-spotter` are symlinks resolving to the identical target `~/AI workflows/big-angle-spotter`. The real `run_pipeline.py` (1,493 lines, edited today) exists in exactly one place. Editing through either symlink edits the one file. **Your "both should be the same" expectation holds today — no divergent copy exists.**

**The one way this breaks (HIGH risk):** a well-meaning fork. If, while wiring BAS into a client, someone `cp`s `run_pipeline.py` into a client folder "to customize it," or a tool replaces the symlink with a real dir, or someone patches the pipeline to emit `DCT<NNN>-img-<NN>` names — you get two copies that silently drift. Because client trees are **gitignored**, a forked copy would be **invisible to `git status`** and could rot for weeks. SKILL.md already warns the pipeline is global/shared and that 10-5-5 mode must be done *manually*, not by patching.

> **Guard:** never edit the pipeline for one client — all client-specific behavior lives in `inputs.json` + `--run-dir` + downstream glue. Add a pre-commit check that `skills/big-angle-spotter` stays a symlink, and `grep` for stray `run_pipeline.py` copies under `clients/`.

---

## Overlap matrix

| Area | NeezaNizam side | big-angle-spotter side | Severity | Keep-them-apart rule |
|---|---|---|---|---|
| **Render vs prompt** | `render.py` is the *only* renderer (Azure gpt-image-2 → PNG + `.meta.json`) | Emits **text prompts only**; step 12 literally says "Do NOT produce an actual image" | **LOW** | Clean handoff seam, not an overlap. Glue = thin adapter: read `12_image_prompt_rankN.md` → `render.py --prompt` → `allocate`. Never merge the tools. |
| **Image naming** | Flat pool `DCT<NNN>-img-<NN>`, ≤10, Meta-mixed, **angle-decoupled** (A01–A05 label text+headline only) | Angle-**tied**: `rankN` = a specific top-3 angle. No image files named (none produced). | **MED** | `allocate` is the seam that drops rank identity. `rankN` becomes provenance metadata only — it must **not** survive into the filename or `_assets.json`. |
| **Output location** | `render.py` → `<tracker>/image-prompts/renders/`; canonical → `dcts/DCT<NNN>/images/` via `allocate`; pool at `_assets/renders/` + `_inbox/` | Writes **only** to `$PWD/big-angle-spotter-runs/<timestamp>/` (override `--run-dir`). Never touches DCT folders. | **LOW** | Disjoint paths today. Pin BAS `--run-dir` (don't let it default to `$PWD`). `render.py`/`allocate` own `dcts/.../images/` + `_assets/`; BAS never writes there. |
| **Angle generation** | `render.py` does none; `dct.json` *holds* 5 angles authored upstream | BAS's core job (steps 1–9, hardened gate) — the one place it's authoritative | **LOW** | One direction only: BAS → (human pick) → `dct.json`. Never hand-author angles that contradict BAS output. |
| **Executor** | Azure gpt-image-2 (only registered engine); Higgsfield/nano-banana are commented placeholders | None. Names Midjourney/DALL-E/Flux as *target strings* inside prompt text (`--ar 1:1 --v 6`, `quality: hd`) | **LOW** | Adapter must **strip** model-specific param strings before `render.py --prompt` (it controls `--size`/`--quality`). Or tell BAS to target `gpt-image`. |
| **Manifest/ledger ownership** | `dct.json` + `_assets.json`, written by `allocate` | Reads/writes neither (zero matches) | **MED** | No BAS clash — the conflict here is **internal to NeezaNizam** (see Blocker 2). |

---

## Three blockers — clear these before coding Build #10

**1. This doc was missing (now fixed).** The handoff's own pre-build gate (line 62) pointed at `docs/ad-image-tooling-overlap-260608.md`, which did not exist on disk or in git — likely lost in the session's worktree near-miss. Anyone following the handoff hit a dead reference. **This file is the regeneration.** ✅

**2. ~~NeezaNizam contradicts itself on image sharing.~~ ✅ RESOLVED 260608** — reconciled to one-image-one-DCT-by-default + flexible array; schema strings fixed in all three sites. _(Rationale kept below for the record.)_ `clients/neezanizam/CLAUDE.md` said *"one image = exactly one DCT … never shared across DCTs."* But the `_assets.json` schema string and `dct.json` format string say *"SHARED POOL / allocated_to may be ≥1 DCT"* — and `allocated_to` is an **array**. Two source-of-truth statements in direct conflict. On top of that, the same image is described with **two different shapes**: `{status, source}` in `dct.json` vs `{status, allocated_to, rendered_at, prompt_source, notes}` in `_assets.json`. `allocate` has to keep both in lockstep, so this must be resolved **in writing first** — pick one model, fix the losing schema strings, then code `allocate` as the *sole synchronized writer* of both files (atomic two-file update + consistency check).

**3. `render.py` reads the legacy tracker, not the canonical manifest.** `render.py --from-tracker` reads the monolithic `dct-tracker.json`; the canonical shape is per-DCT `dct.json`. The per-DCT split is **Deferred #8** (unbuilt). Coding `allocate` against the legacy schema bakes in debt. **Sequence: #8 (tracker split) → then #10 (render/allocate).**

---

## Eugene: decide the convention before the first run

Eugene is a clean slate, but its documented convention **diverges** from NeezaNizam's, and silently forking per-client is how `render.py`/`allocate` end up needing client branches:

| | NeezaNizam (live) | Eugene (documented, not instantiated) |
|---|---|---|
| BAS output home | `campaigns/<c>/angles/_spotter-runs/wave-N/` | `campaigns/<c>/ad-concepts/<batch>/` (per CONTEXT.md) |
| Image source-of-truth | campaign `_assets/_assets.json` ledger | per-workspace `04_input-images/input-image-manifest.json` |

Pick **one** before BAS runs for Eugene: either adopt NeezaNizam's `_assets.json` model (and update Eugene's CONTEXT.md to document `angles/_spotter-runs` + `dcts/`), or keep Eugene's `ad-concepts/` + `input-image-manifest.json` model and pin BAS `--run-dir` + `allocate` to match. Don't let the two conventions fork.

---

## Recommendations (ranked)

1. **Use this doc as the regenerated gate** and confirm the handoff pointer resolves. ✅ (done — file now exists)
2. **Sequence Build #10 after Deferred #8** (tracker split) so `render.py` reads canonical `dct.json`.
3. **Resolve the one-image-one-DCT contradiction in writing** before coding `allocate`. Pick one model, fix the losing schema strings.
4. **Make `allocate` the single seam** that strips angle/rank identity and is the *only* minter of `DCT<NNN>-img-<NN>` IDs and the *only* writer of `dct.json` + `_assets.json`.
5. **Add a symlink-integrity guard** (pre-commit check + grep for stray `run_pipeline.py` under `clients/`). Highest-leverage failure mode is an invisible gitignored fork.
6. **Decide Eugene's image source-of-truth** before the first BAS run.
7. **Strip Midjourney/DALL-E param strings** from BAS step-12 prompts in the adapter before rendering.
8. **Never patch `run_pipeline.py` per-client.** Client-specifics live in `inputs.json` + `--run-dir` + glue.

---

## Bottom line

big-angle-spotter and `render.py`/`allocate` are **complementary with a clean handoff seam**, not competitors — and the disk backs that up. The operator's clash fear is largely unfounded *as long as* no one merges the tools, points BAS's run-dir into the DCT tree, or forks the global pipeline into a client folder. The work that actually remains is **convention reconciliation at the seam** (angle-tied → angle-free naming, owned by `allocate`) plus **fixing a NeezaNizam internal contradiction** that blocks `allocate` regardless of BAS. Eugene has no BAS work on disk yet, so the convention call can be made cleanly now.

---

## Appendix — handoff verification (2026-06-08): PASS (7/7)

All seven verification checks in `SESSION-HANDOFF-260608.md` verify against disk:

| Check | Expected | Actual | ✓ |
|---|---|---|---|
| Campaigns index | 6 entries, tracker_paths resolve | 6, all resolve | ✅ |
| campaign_type ×3 | dct / dct / launch | dct / dct / launch | ✅ |
| File count | ~770 (was 1,869) | **784** (within ~tolerance; big drop real) | ✅ |
| Salvage tar | exists, ≥1 v4-firsttime | exists (**432 MB**), grep = 4 | ✅ |
| Salvaged worktree files | both dirs non-empty | firsttime-buyers/ = 18, letter-critic/ = 4 | ✅ |
| Spec/map/learning files | all present | all present (repo-level, not under clients/) | ✅ |
| No stray worktree | none for neezanizam | none | ✅ |

Two notes (not failures): (a) file count is **784**, not exactly ~770 — within the tilde; (b) the content-spine / migration-map / learning files live at **repo level** (`.claude/workflows/`, `docs/`, `learnings/`), not under `clients/neezanizam/` — a `find` scoped only to the client folder would miss them. The salvage tar is **432 MB** — large; confirm it's the intended scope and not accidentally bundling renders.
