# APPLY-NOTE — neezanizam locale-rules.md (staged M2.4)

**Date:** 2026-06-11 (rebuild M2.4 — Statics Lane).
**Why staged, not written:** neezanizam is a LIVE client; the rebuild treats live-client folders as read-only. Operator applies.

## What
- One new file: `locale-rules.md` (this folder's sibling).

## Where it goes
- Copy to: `clients/neezanizam/_brand/locale-rules.md`
- Command (operator runs from repo root):
  ```bash
  cp "_handoffs/staged-m2/neezanizam/_brand/locale-rules.md" "clients/neezanizam/_brand/locale-rules.md"
  ```

## Why
The new client-agnostic static image method (`skills/ad-concept-engine/references/static-image-method.md`) and the copy pre-launch rubric carry ZERO locale content — they load `clients/<slug>/_brand/locale-rules.md` IF PRESENT. Without this file, NeezaNizam's static batches lose the SG casting rule, the CPF/HFE/MOP document-fidelity rule, and the locale-layer kill-list cross-check (no smiles / no "dream home" / no "break-the-bank" / no fake urgency). That locale content used to live Singapore-hardcoded inside the old `high-converting-static-brief.md`, now archived; relocating it per-client is the fix.

## Verify before/after applying
- Source pointers (e.g. `_brand/buyer-profile.md:7`, `:11`, `_brand/brand-voice.md:52`) reflect file state as of 260611. Re-anchor if those files shifted lines.
- The kill-list includes both the file's stated rules AND project-memory rules (smiles / upbeat tone / "investment" / "dream home" / "break-the-bank"). Confirm these still hold before applying; the canonical CTA word **consult** is locked.
- NeezaNizam carries an open M1 quote-provenance flag (`_handoffs/neezanizam-quote-flag-260611.md`) — image proof cues should respect it. This locale file does not resolve that flag; it only references it so proof cues inherit the scrutiny.
- ADDITIVE — creates a new file, touches nothing existing.
