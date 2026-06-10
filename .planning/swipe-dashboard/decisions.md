# Decisions (settled tradeoffs)

Each decision below was proposed, debated, and locked. Push back only if new information changes the tradeoff.

## D1 — Database layout: single Ghost DB with `industry` column
**Not** per-industry databases.

- **Why:** one connection string simplifies ops; cross-industry queries are trivial (`WHERE industry_slug='...'`); Ghost forks are still available per-industry via filtered dumps when a client needs a private snapshot.
- **Cost:** slightly larger DB over time (mitigated by indexes + views); forking a single industry requires `pg_dump --where=...` rather than a native `ghost fork swipe-property-sg`.

## D2 — Embedding architecture: decoupled `ad_embeddings` table, LiteLLM abstraction, 1024-dim Matryoshka-truncated vectors
- **Why swap-ability:** User wants future-proofing for Qwen3-Embedding, Jina v3/v4, etc. Locking to one provider's native dim (OpenAI 1536, Nomic 768) forces painful re-embed + schema change on every swap.
- **Solution:**
  - Embeddings live in `ad_embeddings` keyed on `(ad_archive_id, provider)` — one ad can have multiple provider rows; only one is `is_active=true`
  - Column pinned to `vector(1024)`; LiteLLM fetches native vector, script truncates to first 1024 dims (Matryoshka)
  - `embedding_provider_log` audit table records every swap; `v_active_embeddings` view routes queries to current provider automatically
- **Swap cost:** flip two env vars, re-run `scripts/ghost-sync.py --reembed-all` → old rows get `is_active=false` but stay for rollback

## D3 — Default embedding provider: Ollama + nomic-embed-text
- **Why:** User explicitly requested zero-API-bill setup that stays inside Ghost hard-cap pricing. Local Ollama is free, offline, private; nomic-embed-text natively outputs 768 dims (truncated to 1024 per D2 — padding zeros acceptable since it never exceeds the limit; we skip truncation when native < target).
- **Alternative providers, ready to switch to:** OpenAI text-embedding-3-small (paid, $0.02/1M tokens, strongest quality), Jina embeddings v3 (strong multilingual), Qwen3-Embedding 0.6B (newer, competitive)

## D4 — Hosting: Next.js 15 App Router on Netlify
- **Why Next.js:** server components query Ghost Postgres directly via connection string, no CORS; the 4 prototype HTML files port cleanly to React pages; API routes give external-agent access via bearer tokens (see settings page).
- **Why Netlify:** user already has Netlify MCP; Netlify Blobs for asset storage lives in the same stack; auto-deploy from git.
- **Rejected:** local-only Python http server (too primitive for advertiser detail page + pgvector queries), Vercel (not user's existing stack), Cloudflare Pages (Workers Postgres pool fiddly).

## D5 — Asset storage: Netlify Blobs
- **Why:** signed URLs the dashboard references directly via `ads.asset_url`; same provider as hosting (one vendor, one auth); reasonable pricing for mp4/jpg volume.
- **Alternatives considered:** R2 (cheaper at scale but adds a vendor), Supabase Storage (good but also adds a vendor), filesystem-only (dashboard can't serve mp4 from `swipe-files/` without a local proxy — doesn't survive Netlify deploy).

## D6 — Repository layout: dashboard separate from Marketing
- Dashboard app: `~/AI workflows/swipe-dashboard/` (its own git repo)
- Marketing repo keeps:
  - `scripts/ghost-sync.py` (called by `/ads:scrape-library`)
  - `skills/ad-library-scraper/references/ghost-schema.sql` (canonical schema source)
  - `skills/ad-library-scraper/references/agent-query-cookbook.md` (agent query recipes)
  - `.planning/swipe-dashboard/` (this planning dir)
- **Why:** Marketing is for strategy + skills + agent workflows; dashboard is a standalone app with its own deploy target, build pipeline, and lifecycle.

## D7 — Dashboard drawer metrics: cut fake, add real
Prototype drawer shows fake Est. spend / Impressions / CTR / Variants live / Placement mix %. Meta Ad Library exposes none of this.

Replacement stat grid (confirmed):
| Prototype (fake) | Real replacement |
|---|---|
| Est. spend $Xk | Days running |
| Impressions (M) | Last seen date |
| CTR % | Schwartz stage (1–5) + confidence |
| Variants live | Blue-box category (saturated / untargeted / emerging) |

Prototype sections to keep: Run timeline, Placement mix (as binary platform chips, not %), Tagged angles (from classifications.angle), Creative variants (only if scraper captures them). Add new section: Transcript excerpt with "View full" expander.

## D8 — Industries in dashboard: real from DB, not prototype's 6 fakes
- Prototype ships 6 synthetic industries (ecom/real-estate/software/finance/health/automotive)
- Replace with `SELECT slug, name, emoji, schwartz_stage FROM industries ORDER BY name`
- Start with 1 row: `property-sg`. Industry picker still renders even with one option so it's ready for fitness-sg etc. later.

## D9 — Meta-only now, platform filter shows others greyed
- Prototype already marks TikTok/YouTube/LinkedIn/etc. as "Soon" — matches reality
- Keep the greyed-out rows for discoverability without pretending we support them

## D10 — Advertiser-centric browse page (new)
- Add `/advertiser/<page_id>` page that mirrors Meta Ad Library's per-advertiser UX
- Shows header (logo/name/category/verified/location/active-since), stats row (total/active/stopped/winners), two CTAs (full-history backfill + refresh active), tabs (All/Active/Stopped/Winners), filters, masonry grid
- Powered by `v_advertiser_detail` view; click any ad opens the same drawer as main dashboard
- Extends the prototype's 4 pages to 5

## D11 — Two scrape depths
- Shallow (current): `facebook_company_ads(page_id, status='ACTIVE')` for weekly monitoring — ~1-3 credits per page
- Deep (new): `facebook_company_ads(page_id, status='ALL', cursor=...)` paginated for historical backfill — 5-50 credits per page
- `/ads:scrape-library` stays shallow (industry-wide). Add `/ads:scrape-advertiser <page_id> [--depth full|active]` for per-advertiser backfill.

## D12 — Temporal model: authoritative lifecycle_stage
- Schema computes `lifecycle_stage` from status + start_date + stopped_date: new / ramping / running / winner / recently_stopped / historical
- Agents should query `lifecycle_stage` rather than doing raw date math
- Scraper reconciles disappearances: ads that were ACTIVE last time but missing now get `status=INACTIVE, stopped_date=today`

## D14 — Transcription provider: Groq whisper-large-v3 default, faster-whisper fallback
- **Why Groq default:** 165x realtime vs faster-whisper's 0.3-1x on CPU; ~$0.04/hr audio (effectively free for ad volumes — ~$1/year per industry at weekly scrape); same Whisper large-v3 model, same accuracy
- **Why keep faster-whisper:** offline fallback, zero-API-cost option, privacy for sensitive content, rate-limit safety net
- **Architecture:** same pattern as embedding provider — LiteLLM abstraction, env-var flip (`TRANSCRIPTION_PROVIDER` / `TRANSCRIPTION_MODEL`), provider stored in `transcripts.provider` column + sidecar file header comment
- **Extends** existing `transcribe` skill (adds `--provider` flag); existing invocations keep working with new default

## D13 — Plan organization: planning-with-files plugin, not manual split
- User chose to install plugin (`/plugin install planning-with-files@planning-with-files`)
- Structure: `task_plan.md` / `findings.md` / `progress.md` at root + `decisions.md` + `schema/` + `subsystems/` + `verification.md` in the same dir
- Source plan at `/Users/jerel/.claude/plans/for-this-what-we-jiggly-pearl.md` stays as canonical full-text reference; split files are working memory
