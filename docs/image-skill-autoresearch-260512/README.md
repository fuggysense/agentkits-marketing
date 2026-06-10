# Image Skill AutoResearch Experiment - 2026-05-12

## Summary

This package implements the parallel image-skill AutoResearch plan without changing canonical skill files.

Coordinator-owned render sample:

| Candidate | Skill path | Render | Score | Critical failure |
|---|---|---|---:|---|
| A-001 | image-generation | [A-001-image-generation-product-ad.png](renders/A-001-image-generation-product-ad.png) | 87 | Yes - invented bottle logo |
| B-006 | gpt-image-2-director | [B-006-gpt-image-diagram.png](renders/B-006-gpt-image-diagram.png) | 96 | No |
| C-002 | ugc-creator | [C-002-ugc-product-review.png](renders/C-002-ugc-product-review.png) | 96 | No |
| HF-003 | higgsfield-style marketplace | [HF-003-marketplace-card.png](renders/HF-003-marketplace-card.png) | 94 | No |

Round 0 mean score: 93.25.

Final status: prompt-quality loop succeeded, but exact aspect-ratio control hit a renderer limitation. Loop 1 cleared all four samples at 93+ with no critical failures. Loop 2 confirmed the UGC label fix at 96, but exposed product-ad aspect-ratio drift. Loop 3 fixed the product-ad aspect ratio and scored 99, then Loop 4 reproduced the aspect-ratio drift with the same final prompt. The stable scale fix is not more prompt text; it is a deterministic dimension gate after generation.

## Files

- [render-sample-manifest.json](prompts/render-sample-manifest.json) - selected prompts and expected checks.
- [prompt-test-matrix.md](prompts/prompt-test-matrix.md) - prompt-only matrix from the parallel candidate agents.
- [round-0-evaluation.md](reviews/round-0-evaluation.md) - baseline evaluator scores and mutation queue.
- [loop-results.md](reviews/loop-results.md) - targeted loop history and final success decision.
- [thin-stack-recommendation.md](thin-stack-recommendation.md) - keep/archive/remove table and cleanup patch list.

## Decision

Do not mutate canonical skill files automatically. The evidence supports a human-reviewed patch to product-ad prompt guidance: blank/unbranded product-surface rules must be explicit. For aspect ratio, add a workflow rule instead of relying on prompt text alone: check output dimensions after render, then rerender or normalize/export with deterministic tooling.
