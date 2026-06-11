# CLAUDE.md — VitalKit Labs

> **FICTIONAL SMOKE-TEST CLIENT** — M3.8 repeatability baseline, not a real client. All facts invented.
> **Scope:** nested CLAUDE.md for the VitalKit Labs client. Parent `/Marketing/CLAUDE.md` global rules apply — this file adds client-specific context and overrides.
> **Entry reminder:** parent `CLAUDE.md` owns the Agent Entry Contract. Any worker touching this client must carry a context receipt covering this file, `CONTEXT.md`, campaign registry, active workspace state, and loaded paths.

## Who This Client Is

VitalKit Labs — a US DTC supplement brand selling curated starter kits in three categories (sleep, stress, energy). Founder Priya Sharma formulated the kits after a decade of supplement confusion post-burnout; the brand's core position is "the first stack, done right."

**Sells:**
- **T3 (back-end):** $129/mo Foundation Stack subscription — curated 3-category bundle (sleep + stress + energy), cancel anytime.
- **T2 (mid-funnel):** $49 single-category Starter Kit — 30-day sampler in sleep, stress, or energy. Entry point for the skeptical buyer.
- **T1 (front-end):** Free "Sleep Stack Guide" — 7 common supplement mistakes that waste money and extend the problem.

**Links:**
- Website: https://vitalkit-labs.example.com
- Instagram: https://instagram.com/vitalkitlabs.fictional
- Other: (none)

**Status:** demo / smoke-test (fictional). No deadline.

## Current Funnel State

- Email list: no
- Lead magnet: no (Sleep Stack Guide is planned, not built)
- Funnel today: strangers -> Instagram DM -> Shopify product page -> one-time purchase
- Known fragility: 100% impulse/social-traffic dependent, no nurture, no subscription conversion path, no email capture.

## What We Are Solving

- Build the first paid-acquisition funnel so VitalKit stops depending on organic Instagram traffic.
- Make the "starter kit before you subscribe" logic legible to a skeptical, supplement-fatigued buyer.
- Seed a research pack the downstream marketing pipeline can consume end to end (this M3.8 smoke-test run).

## Idea & Angle Capture (always-on)

Whenever the founder shares a new angle, idea, story, or piece of intel — on a call, in a message, in a video, anywhere — **append it to `_brand/idea-bank.md`** (dated, tagged persona × channel × awareness × status). That file is the single cross-channel idea ledger; it feeds sales letters, emails, and ads. Raw capture (`meetings/`, transcripts, DMs) flows in; durable mechanisms graduate out to `_brand/big-ideas/`. Do not let founder intel die in a chat log — route it to the bank.

## Constraints (kill before launch)

- All data is FICTIONAL. Never present any VitalKit metric, testimonial, or stat as real client data.
- No absolute health claims ("cures," "treats," "prevents") — FTC/FDA. Phrases like "supports sleep quality" are safe; "fixes insomnia" is not.
- No income/ROI claims. No weight-loss percentage claims. No before/after framing for supplements.
- No fear-mongering about health outcomes. Lead with transformation and agency, not disease risk.
- Tone: warm, direct, science-adjacent but not clinical. Priya sounds like a smart friend who did the research, not a pharma rep or wellness influencer.
- Audience landmine: supplement-fatigued US women have tried 5+ things that didn't work. Acknowledge the graveyard of past purchases before making any promise.
- No "natural" or "clean" without specific evidence — those words are meaningless to the target buyer.
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
> Every name below is DERIVED from the slug `_smoketest2` — never invent or hand-type
> them. Hard rule: this client's site, media, and data are isolated. Never read, embed,
> deploy, or reference another client's files, keys, domains, or projects. The real isolation
> guarantee is one GitHub repo + one Cloudflare Pages project per client — not this list.

**Pinned identity (derived from slug `_smoketest2`):**

| Resource | Value |
|---|---|
| Site source (the ONLY build root) | `clients/_smoketest2/website/` |
| GitHub repo (source of truth + backup) | `<org>/_smoketest2-site` |
| Cloudflare Pages project | `_smoketest2-site` |
| Live domain (client-owned, DNS → Cloudflare) | `[fill on provision]` |
| Mux env keys | `MUX_TOKEN_ID_<SLUG_UPPER>` / `MUX_TOKEN_SECRET_<SLUG_UPPER>` (slug uppercased, `-`→`_`) |
| CRM (Google Sheet id) | `[fill on provision]` |

**Slug-scoped commands (copy verbatim — never hand-type the project name or `--client`):**

```bash
npx wrangler pages deploy clients/_smoketest2/website/dist --project-name=_smoketest2-site
mux upload <file> --client _smoketest2 --name "<title>"
mux embed <asset-id> --client _smoketest2
mux list  --client _smoketest2
```

**Never:**

- Pass another client's `--client` flag or `--project-name`.
- `import`, copy, or reference anything under `clients/<other>/`.
- Deploy a build whose source root is outside `clients/_smoketest2/website/`.
- Reuse another client's Mux key, domain, Pages project, or CRM sheet.

## Stopping Criteria

Ship: smoke-test baseline complete — `_smoketest2/` scaffolded from `_template/`, identity files adapted, fictional research pack written to `00_inputs/research/`, thin `_brand/offer.md` + `_brand/buyer-profile.md` seeds in place, all gates run and recorded.
