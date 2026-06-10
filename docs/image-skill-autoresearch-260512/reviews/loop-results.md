# Loop Results

## Loop 1 - Product Logo Fix + Regression

| Candidate | Score | Critical | Decision |
|---|---:|---|---|
| L1-A-001 product ad mutated | 98 | No | Keep mutation |
| L1-B-006 diagram regression | 99 | No | Keep baseline pattern |
| L1-C-002 UGC regression | 93 | No | Keep with label-cleanliness note |
| L1-HF-003 marketplace regression | 98 | No | Keep baseline pattern |

Loop 1 decision: clean loop. The product-ad mutation fixed the invented-logo failure.

Kept mutation:

> Product-ad surfaces must stay blank/unbranded unless the user explicitly asks for a product label. If a brand name is needed, place it only in overlay text or on a separate removable tag, never as an invented logo on the product.

## Loop 2 - Confirmation

| Candidate | Score | Critical | Decision |
|---|---:|---|---|
| L2-A-001 product ad confirmation | 91 | Yes | Do not count as clean loop |
| L2-C-002 UGC label confirmation | 96 | No | Keep label rule |

Loop 2 decision: not clean. The bottle stayed blank and text was correct, but the product-ad render drifted into a taller portrait crop instead of true 4:5.

New mutation:

> For feed-safe social ad renders, include true canvas wording: "TRUE 4:5 vertical social-feed canvas, exactly Meta-feed-safe 4:5 crop, not 2:3, not 9:16, not poster-tall."

## Loop 3 - Aspect Ratio Confirmation

| Candidate | Score | Critical | Decision |
|---|---:|---|---|
| L3-A-001 product ad 4:5 confirmation | 99 | No | Keep final product-ad rule |

Loop 3 decision: clean confirmation for this render.

## Loop 4 - Reproducibility Check

| Candidate | Score | Critical | Decision |
|---|---:|---|---|
| L4-A-001 product ad confirmation | 91 | Yes | Aspect ratio drift reproduced |
| L4-C-002 UGC label confirmation | 93 | No | UGC pattern remains acceptable |

Loop 4 decision: not clean. The same final product-ad prompt produced a taller crop again. This means exact 4:5 is not reliably prompt-controllable through the built-in image renderer.

Dimension check:

| Render | Dimensions | Ratio | Expected |
|---|---:|---:|---:|
| Round 0 A-001 | 1122x1402 | 0.8003 | 0.8 |
| Loop 1 A-001 | 1122x1402 | 0.8003 | 0.8 |
| Loop 2 A-001 | 947x1660 | 0.5705 | 0.8 |
| Loop 3 A-001 | 1122x1402 | 0.8003 | 0.8 |
| Loop 4 A-001 | 1003x1568 | 0.6397 | 0.8 |

An exact 4:5 normalized copy was created at:

`/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/docs/image-skill-autoresearch-260512/renders/normalized/L4-A-001-product-ad-confirmation-4x5-normalized.png`

That proves deterministic normalization is possible, but the side-padding result is not ideal enough to count as a pure prompt win.

## Final Decision

Prompt-quality success met for structure, text, subject, routing, and visual quality. Exact aspect-ratio reliability did not meet the original stop condition through prompt text alone.

Keep these prompt patterns:

1. GPT Image 2-style diagrams: count-and-label prompts with exact node names and arrow contracts.
2. UGC stills: persistent fictional actor seed + everyday clutter + explicit label cleanliness.
3. Marketplace cards: exact feature-count callouts + marketplace-badge exclusions.
4. Product ads: blank/unbranded product surface + explicit true aspect-ratio canvas, plus post-render dimension check.

Do not apply cleanup automatically. Use [thin-stack-recommendation.md](../thin-stack-recommendation.md) as the human-review patch queue.

## Required Workflow Rule

For any production asset with a required aspect ratio:

1. Generate with explicit aspect-ratio wording.
2. Check actual saved dimensions.
3. If ratio is wrong, do not score it as a prompt failure only. Mark it as renderer control failure.
4. Either rerender with a hard cap or normalize/export through deterministic image tooling.
5. Only final normalized assets can be called feed-safe.
