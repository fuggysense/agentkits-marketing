# CONTEXT — Phase 05: Prompt Packs

Canonical stage contract. Per-concept `05_prompt-packs/CONTEXT.md` points here.

## Inputs

- Layer 4 (working): `../03_scripts/script-pack.md`
- Layer 4 (working): `../04_input-images/input-image-manifest.json`
- Layer 3 (reference): `clients/takekine/_brand/video-style.md`
- Layer 3 (reference): `clients/takekine/_brand/higgsfield-reference-routing.json`
- Layer 3 (reference): `~/.claude/skills/higgsfield/` reference docs for active model adapters (Seedance 2.0, Kling, GPT Image 2, etc.)

## Process

`video-prompt-pack-builder` (vid-director.md §2 phase 5) assembles the canonical prompt pack (model-agnostic shot list with truth-source / legend / timeline / boosters) plus per-model adapters in `model-adapters/`. `manual-run-guide.md` documents how a human operator runs the pack if the autonomous executor is unavailable.

## Outputs

- `canonical-prompt-pack.json` — model-agnostic shot list (one entry per shot/clip)
- `model-adapters/<model>.json` — Seedance / Kling / VEO / etc. formatted prompts
- `manual-run-guide.md` — copy-pasteable instructions for human-driven render
  - **Done:** canonical pack covers every script beat, every adapter exists for the executor target, manual guide is reproducible end-to-end
