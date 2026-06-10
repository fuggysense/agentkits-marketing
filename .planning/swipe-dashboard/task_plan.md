# Task Plan: Ghost.build + Swipe Dashboard + ad-library-scraper integration

Source of truth (full-text reference): `/Users/jerel/.claude/plans/for-this-what-we-jiggly-pearl.md`
Working memory: the files in this directory. Re-read this file before major decisions.

## Goal
Ship a single system where `/ads:scrape-library` → Ghost Postgres stores ads (with temporal + classification + embeddings) → Claude Code + AI agents query via Ghost MCP → a real-media Swipe dashboard renders the library and an advertiser detail page mirrors Meta Ad Library's per-advertiser browse UX.

## Current Phase
Phase 1 (Ghost install + schema) — ready to start

## Phases

### Phase 0: Install planning-with-files + scaffold structure
- [x] Install `planning-with-files` plugin
- [x] Read source plan from `/Users/jerel/.claude/plans/for-this-what-we-jiggly-pearl.md`
- [x] Create `.planning/swipe-dashboard/` directory tree
- [x] Seed `task_plan.md`, `progress.md`, `findings.md`, `decisions.md`, schema/*, subsystems/*, verification.md
- **Status:** complete

### Phase 1: Ghost install + schema (1 hr)
- [ ] `curl -fsSL https://install.ghost.build | sh`
- [ ] `ghost login`
- [ ] `ghost mcp install` — register `mcp__ghost__*` tools in Claude
- [ ] `ghost create swipe-ads`
- [ ] Verify extensions: `SELECT name, installed_version FROM pg_available_extensions WHERE name IN ('vector','vectorscale','pg_trgm','pg_textsearch')` → append result to findings.md
- [ ] `CREATE EXTENSION IF NOT EXISTS ...` for any that report available-but-not-installed
- [ ] Apply full schema from `schema/tables.md` + `schema/views.md`
- [ ] Populate `_agent_readme` with seed content from `subsystems/agent-readme.md`
- [ ] Smoke test: Claude queries `SELECT content FROM _agent_readme` via MCP
- **Status:** pending

### Phase 2: Sync pipeline (2 hr)
- [ ] Write `scripts/ghost-sync.py` per `subsystems/scraper-sync.md` contract
- [ ] Write `scripts/seed-netlify-blobs.py` (uploads existing property-sg assets)
- [ ] Set `EMBEDDING_PROVIDER=ollama`, `EMBEDDING_MODEL=ollama/nomic-embed-text` in env
- [ ] Verify Ollama running locally, model pulled: `ollama pull nomic-embed-text`
- [ ] Set `TRANSCRIPTION_PROVIDER=groq`, `TRANSCRIPTION_MODEL=groq/whisper-large-v3`, `GROQ_API_KEY=...` in env (see `subsystems/transcription-provider.md`)
- [ ] Extend `skills/transcribe/` to accept `--provider` flag + read `TRANSCRIPTION_PROVIDER` env
- [ ] Update `skills/ad-library-scraper/scripts/ad_library/enrich_scraped_ads.py` Phase 3 call to pass provider
- [ ] Add `provider`, `audio_hash`, `confidence` columns to `transcripts` table
- [ ] Run end-to-end on property-sg (60 ads, 10 pages) — verify transcripts now produced via Groq (check sidecar file `# provider:` header)
- [ ] Verify row counts match SQLite
- [ ] Run embedding backfill pass
- [ ] Verify semantic query: `WITH seed AS (SELECT embedding FROM v_active_embeddings LIMIT 1) SELECT headline FROM ads a JOIN v_active_embeddings e USING(ad_archive_id), seed ORDER BY e.embedding <=> seed.embedding LIMIT 5`
- [ ] Log `scrape_runs` row
- [ ] Update `_agent_readme` with active-provider + row-count snapshot
- **Status:** pending

### Phase 3: Dashboard port (4–6 hr)
- [ ] Scaffold Next.js 15 App Router app at `~/AI workflows/swipe-dashboard/`
- [ ] Copy CSS tokens + global styles verbatim from prototype `dashboard.html`
- [ ] Drizzle schema mirroring `schema/tables.md`
- [ ] Build API routes: `/api/ads`, `/api/ads/[id]`, `/api/search`, `/api/industries`, `/api/advertiser/[page_id]`, `/api/advertiser/[page_id]/ads`, `/api/advertiser/[page_id]/backfill`
- [ ] Port `AdCard` — real `<img>`/`<video>` instead of `renderSurf()`, preserve Higgsfield hover-reveal
- [ ] Port `AdDrawer` — swap fake metrics (spend/impressions/CTR/variants) for real (days_running / last_seen / Schwartz stage / blue_box_category), add Transcript section
- [ ] Port `FilterSidebar` — brand / platform (Meta-only) / format / angle filters with live counts
- [ ] Port `TopBar` — industry picker driven by `SELECT slug, name, emoji FROM industries`
- [ ] Port `saved.html` page
- [ ] Port `add-competitor.html` page + add "Pull full history now" toggle
- [ ] Port `settings.html` page — API-key management for external agents
- [ ] Build NEW `/advertiser/<page_id>` page per `subsystems/advertiser-detail.md`
- [ ] Sidebar brand chips → linkable to advertiser page
- [ ] Run locally against Ghost, verify golden-path flow
- **Status:** pending

### Phase 4: Deploy + agent MCP polish (1–2 hr)
- [ ] Deploy dashboard to Netlify with Ghost env vars
- [ ] Verify dashboard loads real property-sg ads from deployed instance
- [ ] Full agent loop test: scrape → sync → query via MCP → see results in dashboard
- [ ] Write `skills/ad-library-scraper/references/agent-query-cookbook.md` with all recipes
- [ ] Update `.claude/rules/mcp-integrations.md` — add `ghost` row
- [ ] Update `skills/ad-library-scraper/SKILL.md` — add Query pattern section + Ghost sync step
- **Status:** pending

### Phase 5: Future (deferred)
- [ ] `scripts/swipe` CLI wrapper
- [ ] Real-time sync via Postgres LISTEN/NOTIFY + Next.js revalidate
- [ ] Multi-industry scale test (add fitness-sg or similar)
- [ ] External-agent API with bearer tokens
- [ ] Provider-swap test (flip to Jina v3, reembed, verify query quality)
- **Status:** pending

## Future scrape workflow

See `subsystems/future-scrape-workflow.md` for the full end-to-end map of what happens when you run any of:
- `/ads:scrape-library <industry>` (weekly shallow refresh)
- `/ads:scrape-library <new-industry>` (industry bootstrap)
- `/ads:scrape-advertiser <page_id> --depth full` (historical backfill per advertiser)

Core principle: `ad_archive_id` is tagged on every artifact (filename, sidecar header, DB PK/FK, Netlify Blobs key, log line, UI chip). Any agent can trace any piece of data back to its source ad with one query.

## Key Questions
1. Does Ghost ship pgvectorscale's `diskann` index enabled, or do we fall back to `hnsw`? → verify in Phase 1, log to findings.md
2. Is Ollama already installed on the build machine? → check in Phase 2
3. Will the property-sg `swipe-files/*.sqlite` schema cleanly map to the Ghost schema, or do we need a migration shim? → discover in Phase 2 first run
4. Does Netlify Blobs or R2/Supabase Storage give cheaper/simpler asset hosting? → decide in Phase 3 before assets upload (both are fine, Netlify Blobs is default per decisions.md)

## Decisions Made
See `decisions.md` for the full list with rationale. Top 6:

| Decision | Rationale |
|----------|-----------|
| Single Ghost DB with `industry` column | Simpler connection, cross-industry queries free, forks still available |
| Next.js 15 App Router + Netlify hosting | Server components query Ghost direct; prototype HTML ports cleanly; auto-deploy |
| LiteLLM + 1024-dim Matryoshka-truncated embeddings | Swap OpenAI/Ollama/Jina/Qwen3 by env var; cross-provider comparable |
| Default provider: Ollama + nomic-embed-text | Free, local, zero API bills — fits Ghost's hard-cap pricing |
| Netlify Blobs for assets | Signed URLs; dashboard-friendly; stays inside Netlify stack |
| Dashboard repo at `~/AI workflows/swipe-dashboard/`, sync script in Marketing | Keeps Marketing focused; dashboard is its own project |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
|       | 1       |            |

## Notes
- Re-read this plan before each phase; re-read `findings.md` before decisions that depend on external research
- Update phase status as you progress
- Log ALL errors here or in progress.md — track attempts to avoid repeats
- Security boundary: external web/API content goes in `findings.md`, NOT task_plan.md (hooks re-read task_plan.md on every tool call)
