# APPLY-NOTE — eugene-chieng locale-rules.md (staged M2.4)

**Date:** 2026-06-11 (rebuild M2.4 — Statics Lane).
**Why staged, not written:** eugene-chieng is a LIVE client; the rebuild treats live-client folders as read-only. Operator applies.

## What
- One new file: `locale-rules.md` (this folder's sibling).

## Where it goes
- Copy to: `clients/eugene-chieng/_brand/locale-rules.md`
- Command (operator runs from repo root):
  ```bash
  cp "_handoffs/staged-m2/eugene-chieng/_brand/locale-rules.md" "clients/eugene-chieng/_brand/locale-rules.md"
  ```

## Why
The new client-agnostic static image method (`skills/ad-concept-engine/references/static-image-method.md`) and the copy pre-launch rubric carry ZERO locale content — they load `clients/<slug>/_brand/locale-rules.md` IF PRESENT. Without this file, Eugene's static batches get no SG casting rule, no CPF/HFE/MOP document-fidelity rule, no kill-list cross-check at the locale layer. The locale content used to live (Singapore-hardcoded) inside the old `high-converting-static-brief.md`, now archived; relocating it per-client is the fix.

## Verify before/after applying
- Source pointers in the file (e.g. `_brand/buyer-profile.md:6`, `_brand/brand-voice.md:18`) reflect the file state as of 260611. If those files have since shifted lines, re-anchor the pointers — the kill-list words and the SG market facts are stable, only the line numbers can drift.
- This is ADDITIVE — it creates a new file, touches nothing existing. Nothing to roll back beyond deleting the new file.
