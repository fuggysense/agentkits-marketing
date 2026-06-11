# _brand/ Index — {{client_name}}

Stable brand context for this client. Load files on demand based on the job below — do not preload everything.

**Canonical buyer source of truth:** `buyer-profile.md` (§ MICRO-PERSONA MAP). All campaigns reference `micro_persona_id` from this file.

## File map

| File | Job (what it answers) | Load when |
|---|---|---|
| `buyer-profile.md` | Buyer psychology + 3-7 micro-personas (motivation, pain, outcome, trigger, awareness, sophistication) | ANY campaign, concept, ad, script, or page touching audience targeting |
| `icp.md` | Market boundary: demographics, firmographics, geography, eligibility, exclusions | Ad targeting, lead qualification, market sizing — NOT buyer psychology |
| `brand-voice.md` | Tone, vocabulary, prohibited phrases, rhythm rules | Any copywriting, scripting, or VO work |
| `offer.md` | What's sold: package, price, guarantee, stack, bonuses, deliverables | Offer-building, sales letters, pricing pages, ad headlines |
| `video-style.md` | Visual/edit conventions: pacing, cuts, color, captions, B-roll rules | Video concepts, prompt packs, beat sheets, edits |
| `story-bank.md` | Founder/origin stories, case studies, testimonials, anecdotes | Hooks, sales letters, about pages, social proof modules |
| `idea-bank.md` | **Living cross-channel capture** of fresh angles, founder intel, and campaign ideas (persona × channel × status). Append on any new founder intel; feeds letters, emails, ads. Durable ideas graduate to `big-ideas/`. | ANY copy/email/ad ideation — check before writing, append after any founder conversation |
| `learnings.md` | Cumulative wins, losses, killed hypotheses, what works for this client | Concept ideation, campaign planning — avoid re-running failed experiments |
| `channels.json` | Active distribution channels + handles + accounts | Multi-channel publishing, scheduling, channel-specific creative |
| `higgsfield-reference-routing.json` | Approved Higgsfield reference IDs + character/product/scene routing | Video prompt building, Higgsfield render dispatch |
| `metrics-config.json` | Per-funnel KPI definitions + sheet mapping | Reporting, dashboards, sheets-updater |
| `asset-map.md` | Inventory of brand assets (logos, fonts, product shots, b-roll) and where they live | Production prep, image/video generation, asset hunts |
| `research-brief.md` | Niche-parameterized definition of "research complete" (YAML floor + builder interview). Read by `scripts/research_gate.py`. | Before any avatar/angle/ad work — the gate checks research against this contract |

## Subfolders

| Folder | Job | See |
|---|---|---|
| `visual-characters/` | Generated presenters, mascots, recurring faces, face-lock assets | `visual-characters/README.md` |
| `avatars/` (legacy) | One-file-per-avatar exports for legacy tooling only — NOT canonical buyer targeting | `avatars/_index.md` |
| `big-ideas/` (optional) | Persistent big-idea/angle library (Schwartz Stage 3-4 mechanisms) when client has long-running ad program | folder README if present |
| `brand-assets/` | Raw brand asset files (logos, fonts, palettes) | inspect folder |
| `funnel-research/` (optional) | Research backing the client's `funnel.md` if present | inspect folder |

## Hard rules

- Buyer targeting source of truth = `buyer-profile.md`. Do NOT fork it into campaign folders.
- `icp.md` ≠ `buyer-profile.md`. ICP is market boundary; buyer-profile is psychology.
- `avatars/` is legacy-only. Do not create new avatar files for buyer targeting.
- Campaigns reference brand context by reading this index first, then loading only the files needed.
- When adding a new `_brand/` file, register it here in the same session.
