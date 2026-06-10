# Planted Defects — Smoke-Test Baseline

> Deliberate, documented defects seeded into the smoke-test artifacts so future quality gates
> can be tested against a known-bad input. Each defect is a single, traceable plant — NOT an
> accident, NOT real client data. The point of the regression baseline is to confirm the future
> gate CATCHES these. Every plant lives in a FICTIONAL artifact.
> FICTIONAL SMOKE-TEST DATA — client "Meridian Property Advisory" is not a real client.

---

## 260611 — Stage: IMAGE-PROMPT (ad-concept-engine, static brief)

### PD-IMG-01 — Unsourced statistic baked into an image prompt

- **Where:** `campaigns/wave-smoke-260611/dct.json` → `DCT-SMOKE-01` → `image_pool.images[2]`
  (`id: "DCT-SMOKE-01-img-03"`), inside the `image_prompt` text AND its `text_on_image_hook`.
- **The planted claim (verbatim):** *"73% of Singapore buyers overpay on their second home."*
- **Why it is a defect:** The number is invented. It has no source in `00_inputs/research/market-stats-260611.md`,
  no VoC quote behind it, no URA/HDB citation, and it is rendered as a hard percentage stat ON the
  creative itself — the highest-risk place for an unsourced number, because it ships baked into a
  pixel where no reviewer re-reads the body copy. It also violates the `high-converting-static-brief.md`
  rule 8 ("The information on the image must be factually correct... No invented stats") and the client
  CLAUDE.md constraint ("Never present any Meridian metric, testimonial, or stat as real client data").
- **How it is marked in-artifact:** the image entry carries `"claim_status": "UNSOURCED_PLANTED_DEFECT"`
  and a `"_planted_defect"` note string pointing back to this file. The hook text itself is left
  defect-y (a bare 73% stat) on purpose — the marking lives in the metadata, not in the rendered text,
  so a gate that only reads metadata vs one that reads the actual hook copy are tested differently.
- **What the future claim gate MUST do:** flag `DCT-SMOKE-01-img-03` as containing an unverifiable
  statistic, refuse to pass it to render, and demand either a real source (none exists) or removal.
  A PASS verdict on this image = the gate failed.

### Not a plant (for contrast — real working content)

- Every OTHER number in the manifest (S$4,500 flat fee, S$290 teardown, S$900k/S$1.6m price band,
  "three weeks", S$30k overpay-saving) traces to the offer file or the angle/copy stage and is
  labelled FICTIONAL at the file header. They are in-world consistent and source-linked within the
  fictional pack — they are NOT the planted defect. Only the bare `73%` stat in img-03 is the plant.
