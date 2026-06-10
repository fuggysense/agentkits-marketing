# CONTEXT — Phase 04: Input Images

Canonical stage contract. Per-concept `04_input-images/CONTEXT.md` points here.

## Inputs

- Layer 4 (working): `../03_scripts/script-pack.md`
- Layer 3 (reference): `clients/takekine/_brand/brand-assets/ferrovia/product-reference-manifest.md` (reference gate — pack + strip references required)
- Layer 3 (reference): `clients/takekine/_brand/visual-characters/<id>.md` if concept declares `visual_character_id`
- Layer 3 (reference): `clients/takekine/_brand/higgsfield-reference-routing.json` — REQUIRED before any Higgsfield path derivation
- Layer 3 (reference): `clients/takekine/_brand/video-style.md` (locked visual choices)

## Process

`video-prompt-pack-builder` (vid-director.md §2 phase 4) resolves every reference image the script needs: face-lock identity, product references, scene references. Honors the product reference gate — stop if pack or strip reference is missing. All Higgsfield workflow_flow → reference path mappings come from `higgsfield-reference-routing.json`, never from Higgsfield repo defaults.

## Outputs

- `input-image-manifest.json` — every reference resolved to a concrete path with `use_for` tag and `claim_copy_status`
  - **Done:** manifest passes the reference gate, no `claim_copy_status: unapproved_do_not_reproduce` assets are slated for text reproduction, ready for prompt-pack assembly
