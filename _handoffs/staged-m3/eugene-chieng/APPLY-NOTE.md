# APPLY-NOTE — eugene-chieng _campaigns-index.json (staged M3)

**Date:** 2026-06-11 (rebuild M3.4 — index auto-sync).
**Why staged, not written:** eugene-chieng is a LIVE client; the rebuild treats live-client folders as read-only. --apply refused and dropped the proposed index here. Operator applies after review.

## What
- Proposed regenerated index: `_campaigns-index.proposed.json` (this folder).

## Where it goes
- Target: `clients/eugene-chieng/campaigns/_campaigns-index.json`
- Command (operator runs from repo root, AFTER diffing):
  ```bash
  diff clients/eugene-chieng/campaigns/_campaigns-index.json \
       _handoffs/staged-m3/eugene-chieng/_campaigns-index.proposed.json
  cp _handoffs/staged-m3/eugene-chieng/_campaigns-index.proposed.json \
     clients/eugene-chieng/campaigns/_campaigns-index.json
  ```

## Caution
- The proposal regenerates entries at the TOP-LEVEL campaign-dir granularity (folder truth). If this client's existing index intentionally uses a finer granularity (e.g. neezanizam registers individual DCTs, not the buyer-funnel parent), DO NOT blindly overwrite — reconcile by hand. The script merges prior metadata onto matching slugs but cannot know a slug means something different.
