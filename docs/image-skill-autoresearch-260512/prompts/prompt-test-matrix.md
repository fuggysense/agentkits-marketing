# Prompt Test Matrix

The prompt agents generated broad prompt-only coverage first. The coordinator selected four render samples from this matrix to keep render cost bounded.

Status meanings:

- Rendered: sent through Codex image generation and scored by fresh-context evaluator.
- Prompt-only pass: structurally valid prompt candidate, not rendered in this loop.
- Route-away: negative boundary case; correct behavior is not to render as a still image.

## image-generation Candidates

| Candidate | Use case | Status | Notes |
|---|---|---|---|
| A-001 | Product ad creative | Rendered | Initially failed due invented product logo; fixed in Loop 1 and Loop 3. |
| A-002 | UGC-style still | Prompt-only pass | Good people/skin/hand stress case. |
| A-003 | Before/after comparison | Prompt-only pass | Good split-panel consistency case. |
| A-004 | Video first-frame reference | Prompt-only pass | Good still-vs-video boundary case. |
| A-005 | Carousel cover | Prompt-only pass | Good text-heavy social cover case. |
| A-006 | Lifestyle product shot | Prompt-only pass | Good hand/product realism case. |
| A-007 | Headshot/team image | Prompt-only pass | Good multi-person realism case. |
| A-008 | Negative routing boundary | Prompt-only pass | Correctly expects still keyframe route, not video route. |

## gpt-image-2-director Candidates

| Candidate | Use case | Status | Notes |
|---|---|---|---|
| B-001 | Infographic poster | Prompt-only pass | Dense six-section text/layout case. |
| B-002 | Landing page mockup | Prompt-only pass | Browser UI and product-preview labels. |
| B-003 | Character reference sheet | Prompt-only pass | Layout-heavy character sheet. |
| B-004 | Social media mockup | Prompt-only pass | Mobile UI and split comparison card. |
| B-005 | Editorial document layout | Prompt-only pass | Long text/table stress case. |
| B-006 | Diagram with exact labels | Rendered | Scored 96 baseline, 99 regression. |
| B-007 | Dense poster with 3 sections | Prompt-only pass | Three-section educational poster. |
| B-008 | Face-lock realism boundary | Route-away | Correct route is Higgsfield Soul/Nano Banana, not GPT Image 2 prose. |

## ugc-creator Candidates

| Candidate | Use case | Status | Notes |
|---|---|---|---|
| C-001 | Actor reference sheet | Prompt-only pass | Multi-view identity consistency stress case. |
| C-002 | Product review still | Rendered | Scored 96 baseline, 93 regression, 96 final label confirmation. |
| C-003 | GRWM still | Prompt-only pass | Mirror/reflection hand stress case. |
| C-004 | Unboxing still | Prompt-only pass | Product/box/hand interaction case. |
| C-005 | Routine/lifestyle still | Prompt-only pass | Kitchen routine realism case. |
| C-006 | Creator headshot | Prompt-only pass | Actor identity baseline. |
| C-007 | Persistent actor consistency | Prompt-only pass | Four-panel identity drift stress case. |
| C-008 | Seedance/video boundary | Route-away | Correct route is video/Seedance, not still rendering. |

## Higgsfield-Style Candidates

| Candidate | Use case | Status | Notes |
|---|---|---|---|
| HF-001 | Generic raw image | Prompt-only pass | Environment/architecture realism. |
| HF-002 | Product photoshoot | Prompt-only pass | Fictional skincare product label case. |
| HF-003 | Marketplace card | Rendered | Scored 94 baseline, 98 regression. |
| HF-004 | Branded ad image | Prompt-only pass | Marketing Studio-style static ad. |
| HF-005 | Soul-like fictional portrait | Prompt-only pass | Portrait realism without identity claim. |
| HF-006 | Cinematic still | Prompt-only pass | Widescreen/film-still style. |
| HF-007 | Location still | Prompt-only pass | People-exclusion environment case. |
| HF-008 | Seedance/video boundary | Prompt-only pass | Correctly treats as static keyframe only in Codex test. |

## Render Selection Rationale

The four rendered samples covered:

1. Generic product ad with text and brand-logo risk.
2. Exact-label diagram for layout/text fidelity.
3. UGC person/product still for face, skin, hand, and label fidelity.
4. Marketplace card for compliance-style product infographic structure.

This gave one sample per major skill family while leaving the rest as prompt-only coverage for future loops.
