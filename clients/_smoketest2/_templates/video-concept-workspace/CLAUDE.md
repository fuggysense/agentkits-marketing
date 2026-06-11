# CLAUDE.md — {{concept_slug}} concept workspace

> **Scope:** concept-level L0 identity file. Client `CLAUDE.md` at `../../../../CLAUDE.md` is the authoritative routing law — this file adds concept-specific identity only.

## Identity

- **Client:** {{client_slug}}
- **Campaign:** {{campaign_slug}}
- **Concept slug:** {{concept_slug}}
- **Workspace root:** `campaigns/{{campaign_slug}}/video-concepts/{{concept_slug}}/`

## Key paths

| File | Purpose |
|---|---|
| `concept-brief.json` | Selected-input contract for this concept (canonical typed brief) |
| `artifact-manifest.json` | Phase artifact registry + status |
| `pipeline-state.json` | Current phase, approvals, next actions |
| `event-log.jsonl` | Append-only activity log |

## Phase folders

`00_inputs/` → `01_strategy/` → `02_ag1-options/` (AG1 STOP) → `03_scripts/` → `04_input-images/` → `05_prompt-packs/` → `06_generation-runs/` → `07_review/` (AG2 STOP) + `eval/`

Each phase folder contains a `CONTEXT.md` pointer to the canonical stage contract at:
`../../../../_templates/concept-phases/<phase>-CONTEXT.md`

## Client context

- Client root: `../../../../`
- Brand layer: `../../../../_brand/`
- Input bank: `../../../../00_inputs/input-manifest.json`
- Phase template contracts: `../../../../_templates/concept-phases/`

## Routing law

On resume or hand-off: read `pipeline-state.json` → current phase → phase `CONTEXT.md` → proceed. Do NOT re-derive workspace structure from agent files. This CLAUDE.md + `CONTEXT.md` + `pipeline-state.json` are the three sources of truth.
