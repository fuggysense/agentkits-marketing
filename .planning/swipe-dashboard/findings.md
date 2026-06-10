# Findings & Research — Swipe Dashboard + Ghost integration

## Requirements (from user)
- Ghost.build as the backing DB for scraped ads
- Dashboard to browse/search the swipe file (design from claude.ai/design)
- Dashboard must support Meta-Ad-Library-style per-advertiser browse (click an advertiser → see all their ads, active + inactive)
- Meta-only for now; other platforms greyed out as "Soon"
- AI agents (primarily Claude Code via Ghost MCP) must be able to query the DB — understand temporal state, status, lifecycle
- Embedding provider must be swappable (future-proof for Qwen3, Jina v3/v4, etc.)
- Default to zero-API-bill setup: local Ollama embeddings, stay within Ghost's hard-cap free tier
- Plan to be organized using `planning-with-files` file structure before Phase 1

## Verified Facts (confirmed via docs + code inspection)

### Ghost.build (Tiger Data)
- Ghost is "the first database designed for agents" — on-demand Postgres per DB
- Free tier: **100 hours/month, 1TB storage, hard spending caps** (suitable for internal use)
- Unlimited databases, forks, deletes
- Native Claude Code MCP integration: `ghost mcp install` → `mcp__ghost__*` tools callable
- Ghost's own docs market three potential limitations (web dashboard / usage-based pricing / Postgres-only) — all three **do not apply** to this use case:
  - "No web dashboard" → irrelevant; Ghost is Postgres underneath, any Postgres-speaking UI (Metabase / Retool / Grafana / our Next.js) connects
  - "No usage-based pricing" → irrelevant for internal use; 100 hrs/mo covers scraper + dashboard reads
  - "Postgres only" → Postgres is the right choice (JSONB + FTS + pgvector)
- Tiger Data is the company behind pgvectorscale; Tiger Cloud explicitly markets "Vector and keyword search on Postgres"
- **⚠️ UNVERIFIED (verify in Phase 1):** whether `pgvector`, `pgvectorscale`, `pg_textsearch` are enabled by default in every Ghost DB, or whether we need `CREATE EXTENSION`. Phase 1 step: `SELECT name, installed_version FROM pg_available_extensions WHERE name IN ('vector','vectorscale','pg_trgm','pg_textsearch')` — log results here.

### ScrapeCreators (via skills/scrapecreators/scripts/api.py + references/api-reference.md)
- `facebook_company_ads(page_id=..., status=...)` endpoint at `/v1/facebook/adLibrary/company/ads`
- **Status options:** `ACTIVE` (currently running), `INACTIVE` (stopped), `ALL` (full historical library — matches Meta Ad Library UI per-advertiser view)
- Cursor-paginated (1 credit per page fetch)
- `facebook_ad(ad_id)` → full detail per ad
- `facebook_ads_companies(query)` → search advertisers by name when page_id unknown
- Our current `/ads:scrape-library` uses `status='ACTIVE'` only — needs extension to `status='ALL'` for historical backfill per advertiser

### Meta Ad Library data availability (from reviewing our scraper output)
- **Available:** ad_archive_id, page_id/name, format (IMAGE/VIDEO/CAROUSEL), headline/body/CTA, start_date, status (ACTIVE/INACTIVE), regions, platforms array, creative asset (mp4/jpg URL)
- **NOT available (prototype shows but data doesn't exist):** estimated spend $, impressions count, CTR %, wk/wk trends, placement-mix percentages — Meta Ad Library exposes NONE of these for non-political/non-issue ads
- **Implication:** dashboard's stat grid must be swapped from fake prototype metrics → real ones (days_running / last_seen / Schwartz stage / blue_box_category / transcript excerpt)

### Claude Design prototype (`KUSp-UyiBjzOAEng5Q9hZg`)
- 4 HTML files: dashboard.html (1408 lines), saved.html (484), add-competitor.html (818), settings.html (644)
- Stack: vanilla HTML/CSS/JS, Geist font, lime accent (`#c6f94d`), dark palette, Pinterest masonry
- Ad creatives are **synthetic CSS surfaces** (`renderSurf()`) keyed to brand color + headline — NOT real media. Port must swap for `<img>` / `<video>`
- Industries in prototype are 6 synthetic ones (ecom/real-estate/software/finance/health/automotive). Real industries come from `SELECT slug, name, emoji FROM industries`
- Platform filter already marks TikTok/YouTube/LinkedIn/etc. as "Soon" (disabled) — matches our Meta-only stance
- Companion pages already built: saved (with boards/notes), add-competitor (wizard with preview), settings (with API-key mgmt section ready for external-agent tokens)
- Collapsible sidebar with `⌘\` shortcut persisted via localStorage
- Drawer supports ←/→ navigation between ads, Esc to close, `/` to focus search
- "Copy link" buttons generate `facebook.com/ads/library/?id=<ad_archive_id>` URLs

### Transcription model landscape (relevant to swap-ability)
- **Current (`skills/transcribe/`):** yt-dlp + faster-whisper (local CPU/GPU). Whisper large-v3 model. Quality excellent, speed poor on CPU (~0.3-1x realtime).
- **Groq whisper-large-v3:** hosted API, ~165x realtime, ~$0.04/hr audio. Same model as faster-whisper, same accuracy. Network dependency.
- **Groq whisper-large-v3-turbo:** slightly lower accuracy (~5% WER delta), ~$0.02/hr audio, even faster.
- **OpenAI whisper-1:** $0.36/hr (9x more expensive than Groq), no speed advantage over Groq.
- **Deepgram Nova-3:** $0.43/hr, ~1s per clip, excellent for real-time speech but overkill for ad transcription.
- **LiteLLM supports `litellm.transcription(model=..., file=...)`** across Groq, OpenAI, Azure, and local endpoints — same abstraction pattern as embeddings.
- **Ad-scraper workload cost with Groq default:** ~$1/year per industry at weekly scrape cadence. Never a reason NOT to use Groq.

### Embedding model landscape (relevant to swap-ability)
- Native dimensions vary widely: OpenAI text-embedding-3-small 1536, Jina v3 1024, Nomic 768, Qwen3-Embedding 0.6B 1024, Cohere v3 1024, text-embedding-3-large 3072
- **Matryoshka Representation Learning:** modern embedding models (OpenAI v3, Jina v3/v4, Nomic, Qwen3) are trained so the first N components of the full vector are a valid embedding on their own. Truncating the native output to 1024 dims preserves quality (~95-98% retention based on published benchmarks).
- LiteLLM provides a unified Python interface across OpenAI, Ollama, HuggingFace, Jina, Cohere → `litellm.embedding(model=..., input=...)` works identically regardless of provider

## Research Findings
- `planning-with-files` plugin (v2.34.0) installed; skill files at `/Users/jerel/.claude/plugins/cache/planning-with-files/planning-with-files/2.34.0/`
- 9.2k GitHub stars, 2B acquisition context (Manus pattern), widely adopted for multi-step coding tasks
- Security note: plugin registers a PreToolUse hook that re-reads `task_plan.md` before every tool call → keep external web content in this findings.md file, not task_plan.md (prompt-injection surface)

## Technical Decisions
See `decisions.md` for the full list. Copied here for quick reference:

| Decision | Rationale |
|----------|-----------|
| Single Ghost DB, `industry` column | One connection string; cross-industry queries free; forks still per-industry via filtered dumps |
| Next.js 15 App Router | Server components query Ghost direct; prototype ports cleanly; Netlify deploy |
| Drizzle ORM | Type-safe, close to SQL, schema file doubles as migration source |
| LiteLLM + 1024-dim Matryoshka | Swap providers by env var; cross-provider compatible; future-proof |
| Ollama + nomic-embed-text default | Free, local, zero API bills — fits Ghost hard-cap requirement |
| Netlify Blobs for assets | Signed URLs; same stack as dashboard hosting |
| SQLite kept as canonical | Git-trackable; repo self-contained for anyone without Ghost account |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| User's initial `cp` command pointed to non-existent cache path | Installed via `/plugin install planning-with-files@planning-with-files` instead |
| Design bundle from claude.ai/design returned as 3MB gzip | Extracted to `/tmp/dashboard-design/`, parsed README + all 4 HTML files |

## Resources
- **Source plan (canonical):** `/Users/jerel/.claude/plans/for-this-what-we-jiggly-pearl.md`
- **Claude Design bundle extracted:** `/tmp/dashboard-design/ad-library-swipe-file-dashboard/`
- **Existing scraper skill:** `skills/ad-library-scraper/SKILL.md`
- **Existing scrapecreators wrapper:** `skills/scrapecreators/scripts/api.py` (facebook_company_ads at L539)
- **ScrapeCreators API reference:** `skills/scrapecreators/references/api-reference.md` (Facebook Ad Library section)
- **Current property-sg data:** `swipe-files/property-sg/` (10 pages, 60 ads, 8 transcripts, stage-analysis.md HITL-approved)
- **Ghost install:** `curl -fsSL https://install.ghost.build | sh`
- **LiteLLM docs:** https://docs.litellm.ai/docs/embedding/supported_embedding
- **pgvectorscale docs:** https://github.com/timescale/pgvectorscale
- **Matryoshka paper:** https://arxiv.org/abs/2205.13147

## Visual/Browser Findings
Captured from reading design bundle HTML/CSS (no screenshots needed — source dimensions/colors are explicit in CSS tokens):
- Color palette: `--bg: #0c0d0e; --bg-1: #121315; --accent: #c6f94d; --accent-ink: #0c0d0e`
- Font stack: `Geist, Geist Mono` via Google Fonts
- Grid: CSS masonry `columns: 5 220px; column-gap: 14px;`
- Card hover pattern: Higgsfield-style — clean image at rest, gradient gloss + corner action stack + bottom info strip reveals on hover (opacity 0 → 1, 180ms cubic-bezier)
- Drawer width: `min(620px, 100%)`; slides from right with `translateX(100%)` → `0`
- Sidebar grid-template transition: `244px 1fr` → `0px 1fr` on collapse, 220ms cubic-bezier(.4,0,.2,1)

---
*Update this file after every 2 view/browser/search operations*
*External web content goes here, NOT task_plan.md (hook re-reads task_plan.md repeatedly → injection surface)*
