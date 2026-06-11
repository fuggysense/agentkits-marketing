# APPLY-NOTE — neezanizam _campaigns-index.json (staged M3)

**Date:** 2026-06-11 (rebuild M3.4 — index auto-sync).
**Why staged, not written:** neezanizam is a LIVE client; the rebuild treats live-client folders as read-only. --apply refused and dropped the proposed index here. Operator applies after review.

## What
- Proposed regenerated index: `_campaigns-index.proposed.json` (this folder).

## Where it goes
- Target: `clients/neezanizam/campaigns/_campaigns-index.json`
- Command (operator runs from repo root, AFTER diffing):
  ```bash
  diff clients/neezanizam/campaigns/_campaigns-index.json \
       _handoffs/staged-m3/neezanizam/_campaigns-index.proposed.json
  cp _handoffs/staged-m3/neezanizam/_campaigns-index.proposed.json \
     clients/neezanizam/campaigns/_campaigns-index.json
  ```

## Caution
- The proposal regenerates entries at the TOP-LEVEL campaign-dir granularity (folder truth). If this client's existing index intentionally uses a finer granularity (e.g. neezanizam registers individual DCTs, not the buyer-funnel parent), DO NOT blindly overwrite — reconcile by hand. The script merges prior metadata onto matching slugs but cannot know a slug means something different.

---

# APPLY-NOTE — DCT3 spotter-run `_source.md` (staged M4.5 / B4-sweeps)

**Date:** 2026-06-11 (rebuild M4.5 — orphan/duplicate marker, E-08).
**Why staged, not written:** neezanizam is a LIVE client; treated read-only this session.

## What
- Relocation marker: `_source.md` (this folder) — records that the DCT3 angle-spotter run is canonical in the client tree (newer, 2026-05-31) and has an older duplicate at `~/AI workflows/big-angle-spotter/runs/neezanizam_DCT3_260421-1748/` (no deletion performed).

## Where it goes
- Target: `clients/neezanizam/campaigns/buyer-funnel/angles/_spotter-runs/wave-1/DCT3/_source.md`
- Command (operator runs from repo root):
  ```bash
  cp _handoffs/staged-m3/neezanizam/_source.md \
     clients/neezanizam/campaigns/buyer-funnel/angles/_spotter-runs/wave-1/DCT3/_source.md
  ```

## Caution
- Safe to drop in — it is a new sidecar marker, overwrites nothing. The `~/AI workflows` duplicate is NOT deleted; that needs a separate per-folder operator OK (eugene RELOCATED.md pattern).
