# CLAUDE.md — Meridian Property Advisory

> **FICTIONAL SMOKE-TEST CLIENT** — regression baseline, not a real client. All facts invented.
> **Scope:** nested CLAUDE.md for the Meridian Property Advisory client. Parent `/Marketing/CLAUDE.md` global rules apply — this file adds client-specific context and overrides.
> **Entry reminder:** parent `CLAUDE.md` owns the Agent Entry Contract. Any worker touching this client must carry a context receipt covering this file, `CONTEXT.md`, campaign registry, active workspace state, and loaded paths.

## Who This Client Is

Meridian Property Advisory — a flat-fee, buyer-side property advisory in Singapore. Founder Daniel Tay runs data-backed unit selection for residential buyers (HDB resale, ECs, private condos), charging one fixed fee instead of taking a commission tied to the purchase.

**Sells:**
- **T3 (back-end):** S$4,500 flat-fee end-to-end Property Purchase Advisory — data-backed unit selection from shortlist through to signing the OTP.
- **T2 (mid-funnel):** S$290 90-minute "Shortlist Teardown" call — one shortlist, a data-backed verdict on each unit.
- **T1 (front-end):** Free "Overpaying Checklist" — 9 unit red flags that cost Singapore buyers S$30k or more.

**Links:**
- Website: https://meridianpropertyadvisory.example.sg
- LinkedIn: https://www.linkedin.com/company/meridian-property-advisory-fictional
- Instagram: https://instagram.com/meridian.advisory.fictional
- Other: (none)

**Status:** demo / smoke-test (fictional). No deadline.

## Current Funnel State

- Email list: no
- Lead magnet: no (the "Overpaying Checklist" is planned, not built)
- Funnel today: strangers → word-of-mouth referral → WhatsApp enquiry → S$4,500 advisory
- Known fragility: 100% referral-dependent, no paid acquisition, no first-touch capture. One slow referral month and the pipeline is empty.

## What We Are Solving

- Build the first paid-acquisition funnel so Meridian stops depending on referrals.
- Make the flat-fee model (vs commission agents) legible to skeptical, fee-shy buyers.
- Seed a research pack the downstream marketing machine can consume end to end (this baseline run).

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

- All data is FICTIONAL. Never present any Meridian metric, testimonial, or stat as real client data.
- Never imply Meridian is a licensed CEA estate agent or that the fee includes agent representation — it is buyer-side advisory only. Do not promise specific resale gains or "guaranteed" appreciation.
- Tone: plain, numbers-first, calm. No hype, no "secret," no fear-baiting about the property market. Daniel sounds like a careful analyst, not a salesperson.
- Audience landmine: SG buyers are fee-allergic and skeptical of anyone "selling" property advice. Lead with what the fee saves them, not with the fee. Never punch down at commission agents by name — contrast the model, not the people.
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
> Every name below is DERIVED from the slug `_smoketest` — never invent or hand-type
> them. Hard rule: this client's site, media, and data are isolated. Never read, embed,
> deploy, or reference another client's files, keys, domains, or projects. The real
> isolation guarantee is one GitHub repo + one Cloudflare Pages project per client — not
> this list. This list just keeps the names honest.

**Pinned identity (derived from slug `_smoketest`):**

| Resource | Value |
|---|---|
| Site source (the ONLY build root) | `clients/_smoketest/website/` |
| GitHub repo (source of truth + backup) | `<org>/_smoketest-site` |
| Cloudflare Pages project | `_smoketest-site` |
| Live domain (client-owned, DNS → Cloudflare) | `[fill on provision]` |
| Mux env keys | `MUX_TOKEN_ID_<SLUG_UPPER>` / `MUX_TOKEN_SECRET_<SLUG_UPPER>` (slug uppercased, `-`→`_`) |
| CRM (Google Sheet id) | `[fill on provision]` |
| Booking + tracking config | `_brand/booking.json`, `_brand/tracking.json` |

**Slug-scoped commands (copy verbatim — never hand-type the project name or `--client`):**

```bash
# Deploy site (build root is scoped to THIS client only)
npx wrangler pages deploy clients/_smoketest/website/dist --project-name=_smoketest-site
# Media (per-client Mux environment)
mux upload <file> --client _smoketest --name "<title>"
mux embed <asset-id> --client _smoketest
mux list  --client _smoketest
```

**Never:**

- Pass another client's `--client` flag or `--project-name`.
- `import`, copy, or reference anything under `clients/<other>/`.
- Deploy a build whose source root is outside `clients/_smoketest/website/`.
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

Ship: smoke-test baseline complete — `_smoketest/` scaffolded from `_template/`, identity files adapted, fictional research pack written to `00_inputs/research/`, thin `_brand/offer.md` + `_brand/buyer-profile.md` seeds in place, and `_baseline/invocations.md` + `_baseline/friction-log.md` logged. Downstream stages (avatar-research, copy, ads) can run against this material in later baseline passes.
