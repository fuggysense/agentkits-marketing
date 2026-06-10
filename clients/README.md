# Clients

This folder holds per-client marketing workspaces.

New clients must use the Jake Full Toolkit marketing structure. Do not create new flat client folders with root-level `icp.md`, `offer.md`, `brand-voice.md`, or `channels.json`.

## Current Rule

Use one of these entrypoints:

```bash
/project:new <client-slug>
```

or:

```bash
./scripts/scaffold-client.sh <client-slug> "<Client Name>"
```

Both paths copy `clients/_template/` into `clients/<client-slug>/`. The template is the source of truth.

New clients also inherit the Option B discovery layer:

- `campaigns/_campaigns-index.json` — client-level campaign registry
- `campaigns/README.md` — campaign workspace rules
- `00_inputs/input-manifest.json` — client-level reusable input bank for product, market/buyer, competitors, and research
- `_templates/video-concept-workspace/` — reusable concept workspace scaffold, including `concept-brief.json` plus `01_strategy/` through `07_review/`

## Jake-Style Client Structure

```text
clients/<client-slug>/
├── CLAUDE.md                 # L0: client-specific agent guidance
├── CONTEXT.md                # L1: folder map and stage routing
├── context-profile.json      # L0: structured business identity, always loaded first
├── 00_inputs/                # L2: reusable client input bank
│   ├── input-manifest.json   # Product, market/buyer, competitor, and research index
│   ├── product/
│   ├── market/               # Buyer/persona, category, competitor, and market context
│   └── research/
├── 01_research/              # L2: research stage
│   └── output/
├── 02_script/                # L2: concepts, hooks, copy, scripts
│   └── output/
├── 03_production/            # L2: prompts, assets, beat sheets, render prep
│   └── output/
├── 04_review/                # L2: QA, revision notes, compliance checks
│   └── output/
├── 05_handoff/               # L2: final delivery and lessons
│   └── output/
├── _brand/                   # L3: stable brand, buyer, offer, voice, approved assets
│   ├── icp.md
│   ├── offer.md
│   ├── brand-voice.md
│   ├── buyer-profile.md
│   ├── channels.json
│   ├── learnings.md
│   ├── asset-map.md
│   └── video-style.md
├── _config/                  # L3: engagement terms, brief, scope, active priorities
├── _references/              # L3: reusable frameworks and source material
├── _swipe/                   # L3: research reservoir, competitor examples, swipe files
│   └── research/
├── campaigns/                # L4: campaign workspaces
│   ├── _campaigns-index.json # Client-level campaign registry
│   ├── README.md             # Campaign discovery rules
│   └── feedback/
├── videos/                   # L4: Video Studio runs
├── _templates/
│   └── video-concept-workspace/
│       ├── pipeline-state.json
│       ├── artifact-manifest.json
│       ├── event-log.jsonl
│       ├── concept-brief.json
│       ├── 01_strategy/
│       ├── 02_ag1-options/
│       ├── 03_scripts/
│       ├── 04_input-images/
│       ├── 05_prompt-packs/
│       ├── 06_generation-runs/
│       └── 07_review/
└── output/
    └── deliverables/         # L4: approved final handoff assets
```

## Option B Campaign Structure

For AI-video campaigns, `/campaign:new <project> video-content` must create:

```text
clients/<client-slug>/campaigns/<campaign-slug>/
├── campaign-index.json       # Per-campaign discovery contract
├── state.yaml
├── event-log.jsonl
└── video-concepts/
    └── README.md
```

Actual concept workspaces use this layout:

```text
clients/<client-slug>/campaigns/<campaign-slug>/video-concepts/<concept-slug>/
├── pipeline-state.json
├── artifact-manifest.json
├── event-log.jsonl
├── concept-brief.json        # Selected refs from client-root 00_inputs/input-manifest.json
├── 01_strategy/
├── 02_ag1-options/
├── 03_scripts/
├── 04_input-images/
│   └── input-image-manifest.json
├── 05_prompt-packs/
├── 06_generation-runs/
└── 07_review/
```

Agents must read `campaign-index.json` first, then the concept workspace `artifact-manifest.json`, then `pipeline-state.json`, then `concept-brief.json`. For uploads, adapters must read `04_input-images/input-image-manifest.json`. Do not infer paths from an orchestrator prompt when these files exist.

Concept workspaces must not duplicate broad client input folders. `concept-brief.json` records the selected product, market/buyer, competitor, and research entries from `clients/<client-slug>/00_inputs/input-manifest.json`; the source files stay in the client-level `00_inputs/` bank.

## Onboarding Paths

`/project:new` loads `skills/client-onboarding/SKILL.md` and chooses one path:

- **Path A: research-first** for clients with public footprint. Scrapes public pages, stores evidence in `_swipe/research/`, then produces a brainstorm-agent prompt in `output/deliverables/`.
- **Path B: interview-first** for cold-start or formal paid intake. Runs `business-profile`, writes `context-profile.json`, then optionally fills `_brand/icp.md`, `_brand/offer.md`, and `_brand/brand-voice.md`.
- **Hybrid:** Path A first, Path B only for missing fields.

## Context Loading

When a session starts and a skill/agent needs client context:

1. Read `clients/<client-slug>/CLAUDE.md`.
2. Read `clients/<client-slug>/context-profile.json`.
3. Use `clients/<client-slug>/CONTEXT.md` to route to the right layer.
4. Read `clients/<client-slug>/00_inputs/input-manifest.json` when the task needs product, market/buyer, competitor, or research inputs.
5. Load `_brand/` selectively for stable identity, offer, buyer, voice, and approved assets.
6. Load `_config/` for engagement-specific scope and priorities.
7. Load `_references/` and `_swipe/research/` only when the task needs supporting evidence or reusable frameworks.
8. Write active work into the relevant numbered stage, `campaigns/`, `videos/`, or `output/deliverables/`.

## Deprecated Flat Structure

Older clients may still contain files like:

```text
clients/<slug>/icp.md
clients/<slug>/offer.md
clients/<slug>/brand-voice.md
clients/<slug>/channels.json
```

Those are legacy. Do not use that pattern for new clients.

If an old client must be migrated, do it deliberately:

```text
icp.md          -> _brand/icp.md
offer.md        -> _brand/offer.md
brand-voice.md  -> _brand/brand-voice.md
channels.json   -> _brand/channels.json
learnings.md    -> _brand/learnings.md
assets/         -> _brand/brand-assets/ or campaign-specific assets, depending on approval status
```

## Guardrail

`scripts/scaffold-client.sh` validates that `clients/_template/` contains the required Jake folders before it creates a new client. If `00_inputs/input-manifest.json`, `00_inputs/product/`, `00_inputs/market/`, `00_inputs/research/`, `_brand/`, `_config/`, `_references/`, `_swipe/`, the numbered stages, `output/deliverables/`, `campaigns/_campaigns-index.json`, or the video concept workspace template are missing, scaffold should fail instead of creating a broken client workspace.
