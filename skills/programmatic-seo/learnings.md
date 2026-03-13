# Programmatic SEO — Learnings & Patterns

> This file updates continuously. Add confirmed patterns, insights, and fixes discovered during use.

## Confirmed Patterns
- JSON-first architecture > freeform AI for consistency at scale — validate before render, catch quality issues at generation not after publishing
- Deterministic titles > AI-generated titles for cannibalization avoidance — AI may generate similar titles for different pages, losing control at scale
- 40% unique data threshold = minimum for thin content safety — below 30% is high-risk for Google quality filters
- Indexation <80% → check cannibalization before assuming technical issues — often the cause is content overlap, not crawl errors
- DA <20 domains should NOT attempt large-scale pSEO — build authority with editorial content first
- 60 days is insufficient to declare Google safety — monitor 6+ months before scaling aggressively
- Ward's results have survivorship bias (Byword.ai founder marketing his product) — always disclaim when referencing
- Three-layer separation (data/schema/renderer) prevents the most common pSEO failures — mixing layers makes debugging impossible at scale
- Niche taxonomy before schema design — without a taxonomy, you generate random pages with no strategic coherence

## Diagnostic Rules
- When indexation drops suddenly → check for cannibalization first, then crawl errors, then algorithm updates
- When pages rank briefly then disappear → likely thin content issue, audit Gate 2 (unique data %)
- When traffic per page is very low despite good indexation → check search intent match (Gate 3)

## Mistakes Not to Repeat
- Publishing 1000+ pages before validating with a 50-100 page proof of concept
- Using AI-generated titles at scale (creates cannibalization)
- Scaling without DA check (low-authority domains get filtered)
- Not setting up indexation monitoring before rollout

## Reference Data
- Quality score thresholds: 80+ publish, 60-79 publish with notes, 40-59 hold, <40 reject
- Batch size by DA: DA 20-30 = 50 pages, DA 30-40 = 100, DA 40-60 = 200, DA 60+ = 500
- Content decay refresh cycles: comparisons monthly, locations quarterly, glossary semi-annually

## Open Questions
- Optimal unique data % for different content types (is 40% universal or should it vary?)
- GEO impact on pSEO traffic — how much traffic is shifting to AI search engines?
- Long-term indexation trends for large-scale pSEO sites (2+ years of data needed)
