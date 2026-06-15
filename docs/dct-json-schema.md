# `dct.json` schema — the 10-5-5 per-DCT manifest (Deferred #8)

_Locked 2026-06-08. The per-DCT manifest for **10-5-5 (Meta Flexible Ad) DCTs**. Every script that reads or writes a 10-5-5 DCT targets THIS shape. Proven + verified against `clients/neezanizam/campaigns/buyer-funnel/dcts/dct-10-5-5-proof-260603/` (DCT010)._

## Scope — 10-5-5 ONLY (read this first)

This schema models the **10-5-5 method only** (5 angles, one copy + one headline per angle, a flat ≤10 image pool Meta mixes). It does **not** model the legacy **3-2-2** method (3 angles, two copies + two headlines per creative, images bound per-creative). Confirmed by a 5-lens schema review 2026-06-08.

- **Legacy 3-2-2 DCTs stay on `dct-tracker.json`** until they retire or are rebuilt as 10-5-5. They are NOT migrated to `dct.json`, so their 3-2-2-only fields (`copy_2`/`headline_2`, `_revision_history`, `canva_*`, `asset_gap_flag`, `creative_direction_notes`, `angle_layer`) are out of scope here by design — not lost, just not converted.
- The converter (`migrate_tracker_to_dct.py`) **fails loud** on any non-10-5-5 tracker, enforcing this scope mechanically.
- "Lossless" in this doc and the migration report means **lossless within 10-5-5** — every key of a 10-5-5 tracker is accounted for. It is not a claim about 3-2-2.

## Why the split exists

`dct-tracker.json` bundled three different concerns in one file: per-DCT creative content, campaign-wide config (ad account, sheet ids, KPI targets), and ephemeral working notes. That made every reader couple to the whole monolith. `dct.json` holds **only per-DCT facts**; campaign-level data moves to its real home; ephemera is dropped.

## Shape

```jsonc
{
  "dct_id": "DCT010",                 // DCT + zero-padded number
  "campaign": "buyer-funnel",         // = metrics_campaign
  "campaign_type": "dct",             // dct | launch
  "metrics_campaign": "buyer-funnel", // sheet-routing key (buyer-funnel vs asset-progression)
  "avatar": "avatar-1 (The Hesitant Calculator)", // canonical avatar-<N> (Display); one DCT = one avatar
  "offer": "buyer-funnel",
  "meta_adset": "W1_DCT010_Flex_5angles_avatar-1",
  "status": "draft",
  "dct_method": "10-5-5",             // always "10-5-5" in this schema (3-2-2 stays on dct-tracker.json)

  "format": "...explainer...",        // 10-5-5 mixing-rule explainer; SAME boilerplate for every 10-5-5 DCT. Distinct from the per-ANGLE `format` (Static/Video) below.
  "constant": "avatar + offer/destination (one ad set)",
  "tracking": "...explainer...",

  "angles": [                         // exactly 5 (A01-A05); one per angle, NOT per image. Carries ALL per-angle metadata
    { "id": "A01", "name": "The Closed Loop",
      "headline": "...", "primary_text": "...",
      "format": "Static", "ad_name": "DCT010-A01_avatar-1_closed-loop",
      "market_awareness": "Problem-Aware", "market_sophistication": "Stage 4",
      "angle_rationale": "...", "why_am_i_testing_this": "...",
      "headline_drafts": ["...", "..."], "status": "DRAFT",
      "psych_coverage": {              // OPTIONAL — v2 psychological-coverage tags. Absent on untagged DCTs. Full ref: docs/methods/psychological-coverage/v2-tag-schema.md
        "valence_arc": "worry->relief", // "<from>" (static) or "<from>-><to>" (arc); tokens: worry|relief|neutral. Lead valence = the <from> token.
        "self_image": "mirror",         // mirror | aspiration  (cold target; duty is a tripwire, NOT a value here)
        "real_loud": false,             // opt-in test lane: true ONLY for genuine deadline/runway/quantified-loss urgency
        "tripwire": null,               // null | "fake_loud" | "guilt_duty"  (auto-flag = likely cold-traffic breach)
        "evidence": "cited line from the copy that justifies the tags (provenance gate — no vibes)"
      } }
  ],

  "image_pool": {                     // FLAT pool, ≤10, NOT angle-tied (Meta mixes the pool)
    "target": 10,                     // free int, cap ≤10. The 5-angles×2-variants→10 seeding is a convention, NOT binding; `source` lineage is provenance only.
    "rendered": 1,                    // INVARIANT: must equal count(images where status=="rendered"). render.py/allocate recompute it on every write, never increment blindly.
    "id_format": "DCT010-img-<NN>",
    "images": [
      { "id": "DCT010-img-01",
        "file": "images/DCT010-img-01.png",   // null until rendered
        "status": "rendered",                  // pending | rendered
        "source": "DCT010-A01-v1.png",         // provenance: which angle/variant the prompt came from
        "visual_style": "...",
        "image_prompt": "..." }                // DECISION 2026-06-08: prompt lives on the slot
    ]
  },

  "_provenance": { "migrated_from": "dct-tracker.json", "owner_skill": "ad-concept-engine",
                   "wave": 1, "dct_number": 10, "method": "10-5-5" }
                   // OPEN object — source-lineage keys vary (a freshly-emitted DCT may carry
                   // generated_from / angles_source / messaging_source / buyer_language_source instead).
}
```

## Key decisions baked in

- **Image prompts live on the image slot** (`image_pool.images[].image_prompt`), not on the angle. The pool is flat; `source` records the angle/variant lineage so prompts aren't angle-tied but provenance survives. (Operator decision 2026-06-08.)
- **One image = one DCT by default.** Cross-DCT sharing is opt-in via `_assets.json` `allocated_to[]`, never the default. `dct.json` records only the post-allocation image (with `source`); the campaign-wide pool/ledger lives in `_assets.json`.
- **Per-angle metadata stays per-angle.** `market_awareness`, `market_sophistication`, `angle_rationale`, `why_am_i_testing_this`, `headline_drafts`, `ad_name`, `format`, `status` ride on each angle — the sheet writer reads them per row.
- **`psych_coverage` is OPTIONAL and v2 (added 2026-06-14).** A namespaced per-angle object carrying the psychological-coverage tags: `valence_arc`, `self_image`, `real_loud`, `tripwire`, `evidence`. Absent/`null` on untagged DCTs — never `required`. It does NOT re-encode `market_awareness`/`market_sophistication` (those already exist). It supersedes the dead `valence_zone`/`self_concept_anchor`/`coverage_tag` design in `docs/methods/psychological-coverage/INTEGRATION-PROPOSAL.md` (the v1 4-room grid the re-cut trimmed). Canonical field/value reference: `docs/methods/psychological-coverage/v2-tag-schema.md`. Same Quote-Provenance gate as the avatars — every tag carries a cited `evidence` line.
- **canva fields are NOT yet in the schema.** Whether canva attaches per-angle or per-image is a Phase-3 sheet-writer decision (the 10-5-5 model splits one "creative row" into pools, so the canva→row mapping needs resolving first). The sheet writer's canva gate hard-fails on a live tab without it — so this MUST be decided before `phase_4_sheet` writes to a non-test tab.
- **`dct.json` and `_assets.json` are two views of the same image and MUST stay in lockstep.** They use different shapes on purpose: `dct.json image_pool` is the per-DCT post-allocation record (`id` = `DCT<NNN>-img-<NN>`, `status` ∈ {pending, rendered}, `source` = pre-move filename); `_assets.json` is the campaign-wide pool ledger (`status` ∈ {available, allocated, published, reference, retired}, `allocated_to[]`). **`allocate` (Build #10) must be the SOLE writer of both**, in one atomic op, with an explicit id-map (`_assets.json` `source` id ↔ `dct.json` slot id) and a post-write consistency check (same image present in both, file path agrees, statuses correspond). Any other writer = silent drift. _(DCT010 already shows minor drift between the two — reconcile when allocate is built.)_

## What leaves `dct.json` (relocated, not dropped)

| Tracker key | Goes to |
|---|---|
| `meta_ad_account_id` | `_brand/metrics-config.json` |
| `meta_campaign_name` | campaign `CONTEXT.md` frontmatter / metrics-config |
| `sheet_write_plan` (sheet_id, tab gids) | `_brand/metrics-config.json` (already lives there — scripts read it from there, not the tracker) |
| `kpi_targets`, `kill_rules` | campaign-level `_targets.json` or `CONTEXT.md` (wave-level, not per-DCT) |
| `wave`, `_owner_skill` | kept in `dct.json._provenance` |

Dropped (recorded in the migration report, intentional): `known_blockers`, `next_commands` (ephemeral), `_method`/`dct_structure` (duplicate of `dct_method` / derivable counts), `client_slug` (the folder path is the client).

## Converter

`scripts/migrate_tracker_to_dct.py` — 10-5-5 only (the 3-2-2 normalizer is a separate, deferred job; the converter fails loud on a non-10-5-5 tracker). Lossless by construction: a closing set-difference audit aborts the run if any source key is unaccounted (`--allow-unaccounted` to override). Dry-run by default; refuses to overwrite a live `dct.json` without `--write`. Merges existing render state by `source`; warns (does not silently revert) on an orphaned rendered image.

```bash
# inspect a candidate without touching the live file:
python3 scripts/migrate_tracker_to_dct.py --tracker <path/dct-tracker.json> --out /tmp/cand.json
# commit:
python3 scripts/migrate_tracker_to_dct.py --tracker <path/dct-tracker.json> --write
```

## Status (2026-06-08)

- DCT010 (proof, draft, not live) migrated + verified. Backup at `dct.json.pre-migrate-260608.bak`.
- **Schema validated** by a 5-lens fresh-eyes review (2026-06-08): contract fidelity PASS; scope locked to **10-5-5-only** (operator decision); doc made honest about scope; ledger-reconciliation rule added.
- **No 3-2-2 normalizer is planned** — legacy 3-2-2 DCTs stay on `dct-tracker.json` until they retire or are rebuilt as 10-5-5 (operator decision 2026-06-08).
- **Not yet done:** the 6-script repoint (render.py, create_canva_design.py, ad_concept_sheet_writer.py, backfill_angle_rationale.py, patch_angle_cell.py, source_of_truth_sheet_writer.py — all need a `dct.json` reader + a `creatives[]`→`angles[]` remap), the `ad-concept-engine` emitter repoint, the canva-home decision (blocks live sheet writes), and Build #10 (`allocate`). See `docs/ad-image-tooling-overlap-260608.md` + `clients/neezanizam/SESSION-HANDOFF-260608.md`.
```
