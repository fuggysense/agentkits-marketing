# CLAUDE.md — {{client_name}}

> **Scope:** nested CLAUDE.md for the {{client_name}} client. Parent `/Marketing/CLAUDE.md` global rules apply — this file adds client-specific context and overrides.
> **Entry reminder:** parent `CLAUDE.md` owns the Agent Entry Contract. Any worker touching this client must carry a context receipt covering this file, `CONTEXT.md`, campaign registry, active workspace state, and loaded paths.

## Who This Client Is

{{client_name}} — [one-line description: who they are, what they do, geo].

**Sells:**
- **T3 (back-end):** [main paid offer]
- **T2 (mid-funnel):** [intermediate container — workshop / bootcamp / community]
- **T1 (front-end):** [lead magnet — audit / checklist / prompt set]

**Links:**
- Website: [URL]
- LinkedIn: [URL]
- Instagram: [URL]
- Other: [URL]

**Status:** [paid / pro-bono / friend / demo]. [deadline or "no deadline"].

## Current Funnel State

- Email list: [yes/no — provider if yes]
- Lead magnet: [yes/no — name if yes]
- Funnel today: [strangers → ??? → ??? → paid]
- Known fragility: [where leakage happens]

## What We Are Solving

[1-3 bullet points — the actual job to be done this engagement]

## Idea & Angle Capture (always-on)

Whenever the founder shares a new angle, idea, story, or piece of intel — on a call, in a message, in a video, anywhere — **append it to `_brand/idea-bank.md`** (dated, tagged persona × channel × awareness × status). That file is the single cross-channel idea ledger; it feeds sales letters, emails, and ads. Raw capture (`meetings/`, transcripts, DMs) flows in; durable mechanisms graduate out to `_brand/big-ideas/`. Do not let founder intel die in a chat log — route it to the bank.

## Folder Map (Jake Full Toolkit pattern)

| Folder | Purpose | Loaded |
|---|---|---|
| `CLAUDE.md`, `context-profile.json` | Always-on client identity and routing | L0 |
| `CONTEXT.md` | Client workflow map and stage routing | L1 |
| `00_inputs/input-manifest.json` | Client-level source-of-truth input bank: product, market/buyer, competitors, research | L2 |
| `01_research/`, `02_script/`, `03_production/`, `04_review/`, `05_handoff/`, `06_measure/` | Stage contracts for active work | L2 |
| `_brand/` | Stable brand, product, ICP, buyer psychology, visual characters, voice, video, approved reusable assets, and client-confirmed video reference routing | L3 |
| `_config/` | Engagement-specific operating context: brief, terms, scope, active priorities | L3 |
| `_references/` | Reusable frameworks, external research, market/category notes | L3 |
| `_swipe/research/` | Research reservoir, scrape outputs, audits, benchmark notes | L3 |
| `campaigns/` | Campaign workspaces with `campaign-index.json`, selected-input contracts, typed deliverable workspaces, and review gates | L4 |
| `videos/` | Video Studio (Video Factory) render-projects created by `/video:new` | L4 |
| `campaigns/<campaign>/video-concepts/<concept>/` | AG1/AG2 ideation workspaces scaffolded by `/video:new-concept <campaign> <concept-slug>` (NOT `/video:new`) | L4 |
| `output/deliverables/` | Finished handoff assets | L4 |

## Constraints (kill before launch)

- [client-specific never-do rules]
- [tone/voice constraints]
- [audience-specific landmines]
- Keep raw reusable inputs at `00_inputs/` in the client root. Product inputs live under `00_inputs/product/`; market, buyer, persona, category, and competitor context live under `00_inputs/market/`; source research lives under `00_inputs/research/`.
- Do not create broad duplicated `00_inputs/` folders inside campaigns or concept workspaces. Campaigns and concepts must select from `00_inputs/input-manifest.json` and record those selections in the campaign brief or concept workspace `concept-brief.json`.
- Keep `_brand/icp.md` and `_brand/buyer-profile.md` separate. `icp.md` is the market boundary and qualification layer. `buyer-profile.md` is buyer psychology plus the 3-7 micro-persona map.
- Do not use `_brand/avatars/` as buyer targeting. Use `_brand/visual-characters/` for generated presenters, mascots, recurring faces, and face-lock references; `_brand/avatars/` is legacy/tooling only.
- Do not promote generated assets to reusable brand assets until they are approved and logged in `_brand/asset-map.md`.
- For Higgsfield/Seedance video work, read `_brand/higgsfield-reference-routing.json` before deriving reference paths from the Higgsfield prompt repo. Client facts and assets come from this client folder; Higgsfield files supply prompt mechanics only.
- Do not guess campaign artifact paths. Read `campaigns/_campaigns-index.json`, then `campaigns/<campaign>/campaign-index.json`, then `campaign-selection.json`, then the deliverable workspace `artifact-manifest.json` and `pipeline-state.json`.

## Site & Media — Isolation Contract

> Applies only if this client has a public funnel site. If it has no site, leave the
> blank values blank — these files (`_brand/booking.json`, `_brand/tracking.json`) and
> this section are RECOMMENDED, not required for conformance.
>
> Every name below is DERIVED from the slug `{{client_slug}}` — never invent or hand-type
> them. Hard rule: this client's site, media, and data are isolated. Never read, embed,
> deploy, or reference another client's files, keys, domains, or projects. The real
> isolation guarantee is one GitHub repo + one Cloudflare Pages project per client — not
> this list. This list just keeps the names honest.

**Pinned identity (derived from slug `{{client_slug}}`):**

| Resource | Value |
|---|---|
| Site source (the ONLY build root) | `clients/{{client_slug}}/website/` |
| GitHub repo (source of truth + backup) | `<org>/{{client_slug}}-site` |
| Cloudflare Pages project | `{{client_slug}}-site` |
| Live domain (client-owned, DNS → Cloudflare) | `[fill on provision]` |
| Mux env keys | `MUX_TOKEN_ID_<SLUG_UPPER>` / `MUX_TOKEN_SECRET_<SLUG_UPPER>` (slug uppercased, `-`→`_`) |
| CRM (Google Sheet id) | `[fill on provision]` |
| Booking + tracking config | `_brand/booking.json`, `_brand/tracking.json` |

**Slug-scoped commands (copy verbatim — never hand-type the project name or `--client`):**

```bash
# Deploy site (build root is scoped to THIS client only)
npx wrangler pages deploy clients/{{client_slug}}/website/dist --project-name={{client_slug}}-site
# Media (per-client Mux environment)
mux upload <file> --client {{client_slug}} --name "<title>"
mux embed <asset-id> --client {{client_slug}}
mux list  --client {{client_slug}}
```

**Never:**

- Pass another client's `--client` flag or `--project-name`.
- `import`, copy, or reference anything under `clients/<other>/`.
- Deploy a build whose source root is outside `clients/{{client_slug}}/website/`.
- Reuse another client's Mux key, domain, Pages project, or CRM sheet.

## Campaign Workspace Layout

Use the same high-level pattern for every output type:

```text
campaigns/<campaign>/<artifact-family>/<artifact-slug>/
```

Examples:

```text
campaigns/<campaign>/video-concepts/<concept-slug>/
campaigns/<campaign>/email-sequences/<sequence-slug>/
campaigns/<campaign>/funnel-pages/<page-slug>/
campaigns/<campaign>/ad-concepts/<batch-slug>/
campaigns/<campaign>/lead-magnets/<asset-slug>/
```

Each workspace owns `pipeline-state.json`, `artifact-manifest.json`, `event-log.jsonl`, and a typed workspace brief. The campaign root owns `campaign-index.json` and `campaign-selection.json`.

## AI-Video Specialized Layout

New AI-video concept workspaces use:

```text
campaigns/<campaign>/video-concepts/<concept-slug>/
```

The concept workspace owns video-specific phase folders. It is a specialization of the generic campaign workspace contract above.

Each concept workspace owns only a selected-input contract:

```text
campaigns/<campaign>/video-concepts/<concept-slug>/concept-brief.json
```

That file should reference the client input bank entries used for the concept. It must not duplicate the full client-level product, market/buyer, competitor, or research folders.

Specialized video phase folders:

```text
campaigns/<campaign>/video-concepts/<concept-slug>/
├── CLAUDE.md               ← concept identity (ICM L0)
├── CONTEXT.md              ← concept routing (ICM L1)
├── concept-brief.json      ← canonical typed brief (selected inputs)
├── artifact-manifest.json
├── pipeline-state.json
├── event-log.jsonl
├── 00_inputs/              ← input pinning + manifest
├── 01_strategy/
├── 02_ag1-options/         ← AG1 HARD STOP
├── 03_scripts/
├── 04_input-images/
├── 05_prompt-packs/
├── 06_generation-runs/
├── 07_review/              ← AG2 HARD STOP
└── eval/                   ← buyer-fit + compliance gate
```

Each phase folder contains a `CONTEXT.md` pointer to the canonical stage contract at `_templates/concept-phases/<phase>-CONTEXT.md`. Do not write stage contracts directly in phase folders.

`02_ag1-options/` holds candidate directions, concept packs, and Approval Gate 1 artifacts. It is not a second concept root.

`concept-brief.json` is the canonical name. Legacy alias `concept-input-packet.json` is accepted in older workspaces only — do not use for new concepts.

## Simple Concept Generation Route

If an operator gives a short instruction such as "generate concepts", "make concept options", "run the concept stage", or "create AG1 options" from inside a video concept workspace, route it through the one concept generator:

```text
concept-brief.json
+ 01_strategy/creative-diversity-map.json
+ selected workflow flow SKILL.md
+ /Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/skills/video-concept-lab/SKILL.md
  ↓
/Users/jerel/.claude/agents/video-concept-seeder.md
  ↓
02_ag1-options/concepts-draft.json
  ↓
Phase 4 synthesis creates 02_ag1-options/concept-pack.{md,json,html}
+ 02_ag1-options/approval-1.json
```

`video-concept-lab` is methodology/rubric only. Do not invoke it as a second concept generator. If `concept-brief.json` or `creative-diversity-map.json` is missing, stop and create/approve those first.

## Stopping Criteria

Ship: [concrete deliverables that mark "engagement complete"].
