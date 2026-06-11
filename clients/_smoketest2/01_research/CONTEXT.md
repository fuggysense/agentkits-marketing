# 01_research — Research Contract

Turn raw client, website, product, market, competitor, and existing-asset material into research downstream concept and script work can trust.

## Inputs

- L4 (working): client brief, website, existing assets, scrape outputs awaiting synthesis.
- L2 (upstream): `../00_inputs/input-manifest.json` — the indexed source bank.
- L3 (reference): `../_references/`, `../_swipe/research/`, `../_brand/research-brief.md` (the "research complete" contract).

## Process

Research the market: competitor deep-dives, audience surveys/interviews, awareness and sophistication, buyer language, objections, category and compliance-sensitive claims, and existing-asset audits (videos, product shots, transcripts, prior prompts). When the target is YouTube long-form, the global `yt-ideator` skill (Chasteen TAM-first method) generates and scores concepts before scripting. Stable, settled research gets promoted out — to `../_swipe/research/` for reusable swipe, or distilled into `../_brand/`. Out of scope: brand-identity decisions (`../_brand/`), concept generation (`02_script/`), and production prep (`03_production/`).

## Outputs

- `output/<YYMMDD>-<topic>.md` — one file per research artifact. A new paid-video campaign requires `market-awareness`, `buyer-language`, `existing-asset-audit`, and `claims-and-compliance-notes`. YouTube concepts land in `output/<YYMMDD>-youtube-concepts.md`.
  - Done: research is synthesized (not raw dumps), reusable findings are promoted to `_swipe/research/` or `_brand/`, and `02_script/` can consume a compact summary rather than source material.
