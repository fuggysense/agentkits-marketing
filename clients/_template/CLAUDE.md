# CLAUDE.md — {{client_name}}

> **Scope:** nested CLAUDE.md for the {{client_name}} client. Parent `/Marketing/CLAUDE.md` global rules apply — this file adds client-specific identity and overrides.
> **Entry reminder:** parent `CLAUDE.md` owns the Agent Entry Contract. Any worker touching this client carries a context receipt covering this file, `CONTEXT.md`, the campaign registry, active workspace state, and loaded paths.
> **Routing law:** this file overrides everything below it. Folder map, stage routing, and campaign/workspace layout live in `CONTEXT.md` (L1) — read it before guessing any path.

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

## Constraints (kill before launch)

- [client-specific never-do rules]
- [tone/voice constraints]
- [audience-specific landmines]
- Keep raw reusable inputs at `00_inputs/` in the client root. Product inputs live under `00_inputs/product/`; market, buyer, persona, category, and competitor context live under `00_inputs/market/`; source research lives under `00_inputs/research/`.
- Do not create broad duplicated `00_inputs/` folders inside campaigns or concept workspaces. Campaigns and concepts select from `00_inputs/input-manifest.json` and record those selections in the campaign brief or concept `concept-brief.json`.
- Keep `_brand/icp.md` and `_brand/buyer-profile.md` separate. `icp.md` is the market boundary and qualification layer. `buyer-profile.md` is buyer psychology plus the 3-7 micro-persona map.
- Do not use `_brand/avatars/` for buyer targeting. Use `_brand/visual-characters/` for generated presenters, mascots, recurring faces, and face-lock references; `_brand/avatars/` is legacy/tooling only.
- Do not promote generated assets to reusable brand assets until they are approved and logged in `_brand/asset-map.md`.
- For Higgsfield/Seedance video work, read `_brand/higgsfield-reference-routing.json` before deriving reference paths from the Higgsfield prompt repo. Client facts and assets come from this client folder; Higgsfield files supply prompt mechanics only.
- Do not guess campaign artifact paths. Follow the discovery chain in `CONTEXT.md` § Campaign Discovery.

## Site & Media — Isolation Contract

> Applies only if this client has a public funnel site. If it has no site, leave the blank
> values blank — this section is RECOMMENDED, not required for conformance.
>
> Every name below is DERIVED from the slug `{{client_slug}}` — never invent or hand-type
> them. Hard rule: this client's site, media, and data are isolated. Never read, embed,
> deploy, or reference another client's files, keys, domains, or projects. The real isolation
> guarantee is one GitHub repo + one Cloudflare Pages project per client — not this list.

**Pinned identity (derived from slug `{{client_slug}}`):**

| Resource | Value |
|---|---|
| Site source (the ONLY build root) | `clients/{{client_slug}}/website/` |
| GitHub repo (source of truth + backup) | `<org>/{{client_slug}}-site` |
| Cloudflare Pages project | `{{client_slug}}-site` |
| Live domain (client-owned, DNS → Cloudflare) | `[fill on provision]` |
| Mux env keys | `MUX_TOKEN_ID_<SLUG_UPPER>` / `MUX_TOKEN_SECRET_<SLUG_UPPER>` (slug uppercased, `-`→`_`) |
| CRM (Google Sheet id) | `[fill on provision]` |

**Slug-scoped commands (copy verbatim — never hand-type the project name or `--client`):**

```bash
npx wrangler pages deploy clients/{{client_slug}}/website/dist --project-name={{client_slug}}-site
mux upload <file> --client {{client_slug}} --name "<title>"
mux embed <asset-id> --client {{client_slug}}
mux list  --client {{client_slug}}
```

**Never:**

- Pass another client's `--client` flag or `--project-name`.
- `import`, copy, or reference anything under `clients/<other>/`.
- Deploy a build whose source root is outside `clients/{{client_slug}}/website/`.
- Reuse another client's Mux key, domain, Pages project, or CRM sheet.

## Stopping Criteria

Ship: [concrete deliverables that mark "engagement complete"].
