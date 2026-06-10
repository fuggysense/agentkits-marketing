# 00_inputs — Client Input Bank

This is the reusable source-material layer for the client. Agents should look here before campaign work begins.

Use this folder for raw or lightly organized facts that can feed many services: video ads, image ads, email, landing pages, sales pages, SEO, and future campaign types.

Do not treat this folder as approved brand truth. Distilled, reusable claims and positioning belong in `_brand/`.

## Routing

- `input-manifest.json` is the top-level index.
- `product/` holds product images, features, proof, offers, and FAQs.
- `market/` holds buyer language, awareness, sophistication, competitors, and micro-persona evidence.
- `research/` holds raw dumps, summaries, and winning-ad examples.

Campaigns and concept workspaces should select from this bank through `campaign-selection.json` and `concept-brief.json`; they should not duplicate the whole input bank.
