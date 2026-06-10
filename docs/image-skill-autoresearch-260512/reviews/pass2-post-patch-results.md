# Pass 2 Post-Patch Results

Date: 2026-05-13

Scope: verify the promoted image-skill rules after Pass 1 skill edits. This pass checks routing and prompt-rule coverage. No new render spend or external Higgsfield generation was run.

## Skill Updates Verified

| Rule | Owner | Status |
|---|---|---|
| Thin-stack routing gate for image requests | `skills/image-generation/SKILL.md` | Pass |
| Product/ad blank-surface rule | `higgsfield-product-photoshoot` | Pass |
| Feed-safe post-render dimension gate | `image-generation`, `higgsfield-product-photoshoot` | Pass |
| Marketplace count/label and fake-badge guardrails | `higgsfield-marketplace-cards` | Pass |
| GPT Image 2 diagram relationship/arrow contract | `gpt-image-2-director` | Pass |
| UGC actor seed + product-label cleanliness | `ugc-creator` | Pass |
| Retired `seedance-ugc-director` route-away references removed from tested image/UGC surfaces | `gpt-image-2-director`, `ugc-creator` | Pass |

## Prompt-Only Routing Matrix

| ID | Case | Expected Route | Result |
|---|---|---|---|
| P1 | Product shot for Meta ads, blank matte bottle, brand only as overlay | `image-generation` shim -> `higgsfield-product-photoshoot` | Pass |
| P2 | Marketplace listing images / A+ modules | `higgsfield-marketplace-cards` | Pass |
| P3 | Dense technical diagram with exact node labels | `gpt-image-2-director` Format A | Pass |
| P4 | UGC skincare selfie with fictional recurring actor | `ugc-creator` | Pass |
| P5 | Train my face / digital twin | `higgsfield-soul-id` | Pass |
| P6 | No-people cinematic location still | `higgsfield-generate` | Pass |
| P7 | Character reference sheet with front/side/back labels | `gpt-image-2-director` Format A | Pass |
| P8 | UGC ad video from script | Video stack / `seedance-director`, not still-image render | Pass |
| P9 | Branded ad image with avatar + product | `higgsfield-generate` Marketing Studio Image | Pass |
| P10 | Generic raw stylized illustration, no product | `higgsfield-generate` | Pass |

## Render Gate

The four-render matrix from the AutoResearch plan remains the next optional live test:

1. R1 product ad: blank product surface + true 4:5 dimension check.
2. R2 marketplace card: exactly three callouts, no fake badges.
3. R3 diagram: exactly seven nodes and directed arrows.
4. R4 UGC selfie: exact `DEW SERUM` label, plausible hands, actor lock.

Do not call the render pass clean unless each image scores 90+ with no critical failures and R1 includes an actual saved-dimension check. If R1 drifts ratio, that is acceptable only when marked as renderer-control failure and normalized or rerendered before feed use.
