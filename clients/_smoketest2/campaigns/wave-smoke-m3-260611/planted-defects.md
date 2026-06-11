# Planted Defect Registry — VitalKit Labs — wave-smoke-m3-260611

> **FICTIONAL SMOKE-TEST DATA.** M3.8 repeatability proof.

| ID | Stage | Location | Planted claim | What the gate MUST do |
|---|---|---|---|---|
| PD2-STAT-01 | IMAGE-PROMPT | `campaigns/wave-smoke-m3-260611/dct.json` -> `DCT-SM3-01` -> `image_pool.images[2]` (`DCT-SM3-01-img-03`), both `text_on_image_hook` and `image_prompt` body | "91% of VitalKit buyers sleep better within 14 days" — no source exists | Flag both occurrences as UNSOURCED, exit 1. A PASS = gate failed. |

All other claims in this DCT are source-linked:
- $49 (×4) — ledger -> offer.md
- $79 — auto-traced to competitor-notes-260611.md (AG1 price)
- 200 and 400 (dose range) — ledger -> market-stats-260611.md
