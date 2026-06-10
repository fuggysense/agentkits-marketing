# Schema — Tables

Full text in source plan lines 91-303. Canonical SQL will live at `skills/ad-library-scraper/references/ghost-schema.sql` once Phase 1 runs.

## Extensions required (Phase 1 verification step)
```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS vectorscale;  -- Tiger Data / pgvectorscale
CREATE EXTENSION IF NOT EXISTS pg_trgm;
-- pg_textsearch if available, else built-in tsvector suffices
```
Before applying schema, run:
```sql
SELECT name, installed_version FROM pg_available_extensions
WHERE name IN ('vector','vectorscale','pg_trgm','pg_textsearch');
```
Log result in `findings.md` under "Ghost.build ⚠️ UNVERIFIED" section.

## Tables (9 total)

### `industries`
Row per scraped industry. Source of truth for stage-analysis.md briefs.
```sql
CREATE TABLE industries (
  slug TEXT PRIMARY KEY,             -- 'property-sg'
  name TEXT NOT NULL,
  emoji TEXT,
  schwartz_stage SMALLINT,           -- 1..5 from stage-analysis.md
  stage_confidence TEXT,             -- 'low'|'medium'|'high'
  stage_analysis_md TEXT,            -- HITL-approved brief full text
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### `pages`
One row per Facebook page ID (advertiser). Tracks both shallow ACTIVE scrape and deep ALL-history scrape timestamps separately.
```sql
CREATE TABLE pages (
  page_id TEXT PRIMARY KEY,
  industry_slug TEXT REFERENCES industries(slug),
  name TEXT NOT NULL,
  url TEXT,
  profile_pic_url TEXT,
  category TEXT,
  verified BOOLEAN DEFAULT false,
  meta JSONB,
  first_scraped_at TIMESTAMPTZ,
  last_scraped_at TIMESTAMPTZ,
  last_active_scrape_at TIMESTAMPTZ,   -- status=ACTIVE run
  last_full_scrape_at TIMESTAMPTZ,     -- status=ALL (historical) run
  full_history_complete BOOLEAN DEFAULT false
);
```

### `ads` (core table)
One row per `ad_archive_id`. Rich temporal model — see `schema/temporal-model.md` for the full status/lifecycle semantics.
```sql
CREATE TABLE ads (
  ad_archive_id TEXT PRIMARY KEY,
  industry_slug TEXT REFERENCES industries(slug),
  page_id TEXT REFERENCES pages(page_id),
  format TEXT,                       -- 'IMAGE'|'VIDEO'|'CAROUSEL'
  platforms TEXT[],                  -- ['Meta','Instagram']
  headline TEXT,
  body_text TEXT,
  cta_text TEXT,
  asset_url TEXT,                    -- signed Netlify Blobs URL
  asset_type TEXT,                   -- 'image'|'video'
  meta_library_url TEXT GENERATED ALWAYS AS
    ('https://www.facebook.com/ads/library/?id=' || ad_archive_id) STORED,
  status TEXT,                       -- 'ACTIVE'|'INACTIVE'
  start_date DATE,                   -- Meta's reported first-live date
  first_seen_date DATE,              -- when OUR scraper first saw it
  last_seen_active_date DATE,
  stopped_date DATE,                 -- NULL while still running
  run_duration_days INT GENERATED ALWAYS AS (...) STORED,
  days_running INT,                  -- backwards-compat
  regions TEXT[],
  is_new BOOLEAN GENERATED ALWAYS AS (...) STORED,
  is_winner BOOLEAN GENERATED ALWAYS AS (days_running > 30) STORED,
  is_active BOOLEAN GENERATED ALWAYS AS (status = 'ACTIVE') STORED,
  is_recently_stopped BOOLEAN GENERATED ALWAYS AS (...) STORED,
  lifecycle_stage TEXT GENERATED ALWAYS AS (...) STORED,
  raw JSONB,                         -- full ScrapeCreators payload
  tsv tsvector GENERATED ALWAYS AS (
    to_tsvector('english', coalesce(headline,'')||' '||coalesce(body_text,''))
  ) STORED
);

CREATE INDEX ads_industry_idx ON ads(industry_slug);
CREATE INDEX ads_winner_idx ON ads(industry_slug, is_winner) WHERE is_winner;
CREATE INDEX ads_tsv_idx ON ads USING gin(tsv);
```
Full generated-column expressions in `schema/temporal-model.md`. Comments (COMMENT ON TABLE/COLUMN) in source plan lines 184-207.

### `ad_embeddings`
Decoupled from `ads` to enable provider swap. See `subsystems/embedding-provider.md`.
```sql
CREATE TABLE ad_embeddings (
  ad_archive_id TEXT REFERENCES ads(ad_archive_id) ON DELETE CASCADE,
  provider TEXT NOT NULL,
  model_version TEXT,
  dim INT NOT NULL DEFAULT 1024,
  embedding vector(1024) NOT NULL,
  native_dim INT,
  input_hash TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  is_active BOOLEAN DEFAULT true,
  PRIMARY KEY (ad_archive_id, provider)
);

CREATE INDEX ad_emb_active_idx ON ad_embeddings(provider) WHERE is_active;
CREATE INDEX ad_emb_vec_idx ON ad_embeddings USING diskann(embedding vector_cosine_ops);
-- fallback if diskann unavailable:
-- CREATE INDEX ad_emb_vec_idx ON ad_embeddings USING hnsw(embedding vector_cosine_ops);
```

### `embedding_provider_log`
Audit log of every provider swap.
```sql
CREATE TABLE embedding_provider_log (
  id BIGSERIAL PRIMARY KEY,
  provider TEXT NOT NULL,
  model_version TEXT,
  native_dim INT,
  activated_at TIMESTAMPTZ DEFAULT now(),
  deactivated_at TIMESTAMPTZ,
  notes TEXT
);
```

### `transcripts`
Video ad transcripts. Only populated for winners (days_running > 30). Provider-swappable — see `subsystems/transcription-provider.md`.
```sql
CREATE TABLE transcripts (
  ad_archive_id TEXT PRIMARY KEY REFERENCES ads(ad_archive_id) ON DELETE CASCADE,
  text TEXT,
  language TEXT DEFAULT 'en',
  duration_sec NUMERIC,
  provider TEXT,                     -- 'groq:whisper-large-v3'|'faster-whisper:large-v3'|'openai:whisper-1'
  audio_hash TEXT,                   -- sha256 of audio bytes (skip re-transcribe if unchanged)
  confidence NUMERIC,                -- avg whisper logprob, if available
  created_at TIMESTAMPTZ DEFAULT now()
);
COMMENT ON TABLE transcripts IS
  'Video transcripts. Default provider groq:whisper-large-v3 (165x realtime, ~$0.04/hr audio). '
  'Fallback faster-whisper:large-v3 for offline. audio_hash prevents re-transcribing unchanged audio.';
```

### `classifications`
Nemotron output. One row per ad.
```sql
CREATE TABLE classifications (
  ad_archive_id TEXT PRIMARY KEY REFERENCES ads(ad_archive_id) ON DELETE CASCADE,
  schwartz_stage SMALLINT,
  angle TEXT,
  avatar_fit TEXT,
  blue_box_category TEXT,            -- 'saturated'|'untargeted'|'emerging'
  model TEXT DEFAULT 'nemotron-3-super',
  confidence NUMERIC,
  raw_response JSONB
);
```

### `scrape_runs`
Append-only log of every `/ads:scrape-library` invocation. Powers "new this week" diffs and pipeline health.
```sql
CREATE TABLE scrape_runs (
  id BIGSERIAL PRIMARY KEY,
  industry_slug TEXT REFERENCES industries(slug),
  started_at TIMESTAMPTZ DEFAULT now(),
  finished_at TIMESTAMPTZ,
  pages_scraped INT,
  ads_found INT,
  ads_new INT,
  status TEXT,                       -- 'running'|'success'|'error'
  error_text TEXT
);
```

### `_agent_readme`
The agent bootstrap table. An agent's first query is always `SELECT content FROM _agent_readme`. See `subsystems/agent-readme.md` for seed content.
```sql
CREATE TABLE _agent_readme (
  id SMALLINT PRIMARY KEY DEFAULT 1,
  content TEXT NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

## Future tables (added in later phases)
- `user_saves` — dashboard's Save-to-board feature (Phase 3)
- `pages_queue` — Add Competitor page's "queue for scrape" (Phase 3)
- `api_keys` — bearer tokens for external agents hitting /api/ (Phase 4)
