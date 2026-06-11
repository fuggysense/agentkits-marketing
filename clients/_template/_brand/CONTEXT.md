# CONTEXT — _brand/ (L3 Factory)

The stable brand factory for {{client_name}}: configure once, read often, agents almost never write here. Data flows one way — `_brand/` never references `campaigns/` or `output/` (L4). The full per-file map lives in `_index.md`; this is the load contract.

## Inputs

- L3 (reference): `_index.md` — the full file map (what each `_brand/` file answers, load when).
- L3 (reference): the brand files themselves, loaded on demand by job:
  - `buyer-profile.md` — buyer psychology + 3-7 micro-personas (the canonical targeting source).
  - `icp.md` — market boundary (demographics, geography, eligibility).
  - `brand-voice.md`, `offer.md`, `story-bank.md`, `idea-bank.md`, `video-style.md` — copy, offer, proof, ideation, visual context.
  - `research-brief.md` — the niche "research complete" contract read by the research gate.
  - `channels.json`, `metrics-config.json`, `higgsfield-reference-routing.json`, `asset-map.md` — channel, KPI, render-reference, and asset routing.
  - subfolders: `visual-characters/`, `avatars/` (legacy), `big-ideas/` (optional), `brand-assets/`, `funnel-research/` (optional).
- Upstream (read-only): `00_inputs/` raw research and intake feed the build of these files; they are not re-read at load time.

## Process

A worker reads `_index.md` first, then loads only the brand files its task needs (never the whole folder). Buyer targeting always resolves to `buyer-profile.md` § Micro-Persona Map. New `_brand/` files get registered in `_index.md` in the same session they are created. No file here may cite a `campaigns/` or `output/` path — those are L4 product, not L3 factory.

## Outputs

- Loaded brand context: the specific files a downstream stage or campaign needs, by job.
  - Done: the task has the buyer, voice, offer, and asset facts it needs, sourced from `_brand/` and not duplicated into a campaign folder.
- Registered additions: any new `_brand/` file appears in `_index.md`.
  - Done: `_index.md` lists every file present in `_brand/`.
