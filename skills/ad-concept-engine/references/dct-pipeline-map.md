# DCT Pipeline Map — the orchestrator's runbook

_The map the `ad-concept-engine` skill follows to run a DCT end-to-end. Reached **by intent, not a command** (e.g. "new ad concepts for neezanizam," "continue the DCT") via `.claude/rules/routing-overrides.md` → Conductor Mode. It is resumable: every run starts by reading `pipeline-state.json`, so production can be paused at any phase and any later session picks up exactly where it stopped._

## Resume protocol (DO THIS FIRST, every run)

1. Locate the DCT workspace (`clients/<client>/campaigns/<campaign>/dcts/<dct>/`).
2. Read `pipeline-state.json`. If it doesn't exist, this is a NEW DCT → `pipeline_state.py init`.
3. If it exists and `current_phase` is past `phase_0_context` OR any phase is `complete` → **this is a RESUME**. Do NOT regenerate completed phases. Print the resume card (`pipeline_state.py resume <state>`), then act on `next_action`.
4. After every state-changing step, advance the state (`pipeline_state.py advance …`) and append a line to `event-log.jsonl`. The state file is the single source of truth for "where are we."

```bash
PS=skills/ad-concept-engine/scripts/pipeline_state.py
python3 $PS resume  clients/<c>/campaigns/<camp>/dcts/<dct>/pipeline-state.json   # you-are-here card
python3 $PS next    clients/<c>/.../pipeline-state.json                            # one-line next action
python3 $PS advance clients/<c>/.../pipeline-state.json --phase phase_1_angles --status complete --gate-status approved --output "5 angles"
```

## The map (phases · owner · gate)

Each phase: what it produces, who owns it (skill = dispatch a sub-agent / load the skill; script = shell out), and the HITL gate that must be `approved` before the next phase unblocks.

| # | Phase | Owner | Type | Gate (HITL) |
|---|---|---|---|---|
| 0 | `phase_0_context` | `avatar-research` + client `_brand/` | skill | **gate_0_personas** — operator picks the micro-persona (one DCT = one avatar) |
| 1 | `phase_1_angles` | `big-angle-spotter` (`--top-n 5` for 10-5-5) | skill | **gate_1_angles** — angle approval |
| 2 | `phase_2_assembly` | `headline-bank` → assemble `dct.json` | skill + script | **gate_2_batch** — batch approval |
| 3 | `phase_3_render` | image craft → `scripts/ad-images/render.py` | script | — |
| 3b | `phase_3b_allocate` | `allocate` → `dct.json` image_pool + `_assets.json` | script (Build #10) | — |
| 3c | `phase_3_creative_gate` | operator | gate | **gate_3_creative** — creative approval |
| 3d | Canva push (runs as the `phase_4_sheet` prerequisite; no separate state phase) | `scripts/canva_push.py --dct <workspace>/dct.json` — stitches the approved renders into one lossless PDF (`uvx img2pdf`), Drive-hosts it, fires a Canva URL Import via `one` → ONE design with one image per page (the only programmatic way to get images ONTO pages — Canva's API can't edit existing designs, and library asset uploads hide under Projects, not Uploads). Verifies page count, patches dct.json (`canva_design_id`, stable `canva_link`, `canva_method`). Idempotent, `--dry-run`, `--force` re-imports. Validated live 260610 (Eugene DCT002 → DAHMJ4jWRwo, 10 pages). | script | — |
| 4 | `phase_4_sheet` | `scripts/ad_concept_sheet_writer.py` (reads `dct.json`) — CANVA LINK cell takes dct.json's `canva_link` | script | — |
| 5 | `phase_5_upload` | `meta-ads-uploader` (`dct.json`→`bundle.json`) | skill | **gate_4_preupload** — ads created **PAUSED**, founder enables |

## Contract

- The per-DCT manifest shape is locked in `docs/dct-json-schema.md`. The orchestrator NEVER hand-assembles a DCT in a shape that disagrees with it.
- Image prompts live on `image_pool.images[].image_prompt`; the pool is flat (≤10, Meta mixes), `source` records angle/variant provenance.
- Legacy `dct-tracker.json` → `dct.json` via `scripts/migrate_tracker_to_dct.py` (10-5-5 only; 3-2-2 normalizer pending).

## Mechanical vs judgment (how the orchestrator runs each phase)

- **Shell out** (deterministic, has its own dry-run/HITL): `migrate_tracker_to_dct.py`, `render.py`, `allocate`, `ad_concept_sheet_writer.py`, `canva_push.py` (dct.json shape — Drive links + Canva design + asset uploads via `one`), `create_canva_design.py` (legacy dct-tracker.json — empty design only), `pipeline_state.py`.
- **Dispatch a sub-agent / load the skill** (judgment, creative): `avatar-research`, `big-angle-spotter`, `headline-bank`, image-prompt craft, `meta-ads-uploader` bundle assembly.

## Known gaps (tracked as blockers in pipeline-state.json until closed)

- **G1** ad-concept-engine still emits old `dct-tracker.json` — repoint Phase 2 to `dct.json`.
- **G2** big-angle-spotter angle count not yet votable (`--top-n`) + emits thin output, not typed angles.
- **G3** `allocate` (Build #10) unbuilt — `phase_3b` cannot complete.
- **G4** `ad_concept_sheet_writer.py` reads old format — repoint to `dct.json`.
- **G5** no `dct.json`→`bundle.json` adapter for `meta-ads-uploader`.
- **G6** this skill not yet wired into routing/skill-graph/global client template — until then a fresh/new-client session won't auto-discover the pipeline.
