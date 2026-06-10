-- Ghost.build (Timescale Cloud Postgres) — swipe-ads schema
-- Source of truth for the Swipe Ads DB. Applied via `ghost sql swipe-ads < ghost-schema.sql`
-- or psycopg. Matches the design in /Users/jerel/.claude/plans/for-this-what-we-jiggly-pearl.md
--
-- One schema, one file, one pass. All statements idempotent (IF NOT EXISTS / OR REPLACE).

-- ============================================================================
-- Extensions
-- ============================================================================
CREATE EXTENSION IF NOT EXISTS vector;        -- pgvector (0.8.2)
CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;   -- pgvectorscale (0.9.0) — diskann index
CREATE EXTENSION IF NOT EXISTS pg_trgm;       -- trigram fuzzy text

-- ============================================================================
-- Core tables
-- ============================================================================

CREATE TABLE IF NOT EXISTS industries (
  slug TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  emoji TEXT,
  schwartz_stage SMALLINT,
  stage_confidence TEXT,
  stage_analysis_md TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);
COMMENT ON TABLE industries IS
  'One row per scraped industry. Source of truth for stage-analysis.md briefs.';

CREATE TABLE IF NOT EXISTS pages (
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
  last_active_scrape_at TIMESTAMPTZ,
  last_full_scrape_at TIMESTAMPTZ,
  full_history_complete BOOLEAN DEFAULT false
);
COMMENT ON TABLE pages IS
  'Meta Ad Library pages we track. One row per Facebook page ID. '
  'Tracks both "latest active scrape" and "full-history backfill" separately so '
  'an advertiser can be shallow-scraped (active-only, cheap) OR deep-scraped '
  '(full historical library, matches Meta Ad Library UI).';

-- ads: raw facts only. Time-dependent derived fields live in v_ads view below.
-- Postgres requires STORED generated columns to be IMMUTABLE, which CURRENT_DATE
-- is not. So `is_new`, `is_recently_stopped`, `lifecycle_stage`, `run_duration_days`
-- are computed at query time via v_ads. `is_winner` and `is_active` are OK STORED
-- because they derive from plain columns (days_running, status).
CREATE TABLE IF NOT EXISTS ads (
  ad_archive_id TEXT PRIMARY KEY,
  industry_slug TEXT REFERENCES industries(slug),
  page_id TEXT REFERENCES pages(page_id),
  format TEXT,
  platforms TEXT[],
  headline TEXT,
  body_text TEXT,
  cta_text TEXT,
  asset_url TEXT,
  asset_type TEXT,
  meta_library_url TEXT GENERATED ALWAYS AS
    ('https://www.facebook.com/ads/library/?id=' || ad_archive_id) STORED,
  status TEXT,
  start_date DATE,
  first_seen_date DATE,
  last_seen_active_date DATE,
  stopped_date DATE,
  days_running INT,                 -- set by sync script each run
  regions TEXT[],
  is_winner BOOLEAN GENERATED ALWAYS AS (days_running > 30) STORED,
  is_active BOOLEAN GENERATED ALWAYS AS (status = 'ACTIVE') STORED,
  ocr_text TEXT,                      -- Gemini 2.5 Flash vision OCR for IMAGE ads
  ocr_extracted_at TIMESTAMPTZ,       -- when OCR was last run
  ocr_model TEXT,                     -- model used (e.g. "gemini-2.5-flash")
  raw JSONB,
  tsv tsvector GENERATED ALWAYS AS
    (to_tsvector('english', coalesce(headline,'')||' '||coalesce(body_text,''))) STORED
);
COMMENT ON TABLE ads IS
  'Canonical ad record. One row per Meta Ad Library ad_archive_id. '
  'meta_library_url is the clickable Meta Ad Library link. '
  'is_winner flags ads running >30 days — our proxy for "this is working." '
  'Embeddings live in ad_embeddings (decoupled for provider-swap support). '
  'TEMPORAL MODEL: start_date = when Meta says the ad first ran. stopped_date = '
  'when our scraper first observed it as INACTIVE (NULL while still running). '
  'lifecycle_stage is the computed bucket (new/ramping/running/winner/'
  'recently_stopped/historical) agents should use for time-aware queries.';
COMMENT ON COLUMN ads.status IS
  'ACTIVE or INACTIVE. Source: ScrapeCreators facebook_company_ads endpoint. '
  'Updated every scrape. When a previously-ACTIVE ad disappears from the '
  'latest scrape list, the scraper sets status=INACTIVE and stopped_date=today.';
COMMENT ON COLUMN ads.start_date IS
  'The date Meta reports the ad first went live. Persistent across scrapes.';
COMMENT ON COLUMN ads.stopped_date IS
  'Date our scraper first observed the ad as no-longer-ACTIVE. NULL = still running. '
  'Approximate — actual stop could have been any time since last_seen_active_date.';
COMMENT ON COLUMN ads.raw IS
  'Full Meta payload as received. Query via JSONB operators when new fields needed.';

CREATE INDEX IF NOT EXISTS ads_industry_idx ON ads(industry_slug);
CREATE INDEX IF NOT EXISTS ads_winner_idx ON ads(industry_slug, is_winner) WHERE is_winner;
CREATE INDEX IF NOT EXISTS ads_tsv_idx ON ads USING gin(tsv);
CREATE INDEX IF NOT EXISTS ads_page_idx ON ads(page_id);
CREATE INDEX IF NOT EXISTS ads_status_start_idx ON ads(industry_slug, status, start_date);

-- ============================================================================
-- Embeddings (decoupled, provider-agnostic, Matryoshka 1024-dim)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ad_embeddings (
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
COMMENT ON TABLE ad_embeddings IS
  'Embeddings decoupled from ads table. Each ad can have multiple embedding '
  'rows (one per provider). Semantic queries should filter to the active provider '
  'via the v_active_embeddings view.';
COMMENT ON COLUMN ad_embeddings.embedding IS
  'Matryoshka-truncated to 1024 dim. Native model output may be 768/1024/1536/4096; '
  'first 1024 components are kept. Works because modern embedding models are '
  'trained with Matryoshka Representation Learning.';

CREATE INDEX IF NOT EXISTS ad_emb_active_idx ON ad_embeddings(provider) WHERE is_active;
-- diskann from pgvectorscale (preferred). If the extension isn't available the
-- CREATE EXTENSION above will have failed; swap to HNSW as fallback:
CREATE INDEX IF NOT EXISTS ad_emb_vec_idx ON ad_embeddings
  USING diskann(embedding vector_cosine_ops);

CREATE TABLE IF NOT EXISTS embedding_provider_log (
  id BIGSERIAL PRIMARY KEY,
  provider TEXT NOT NULL,
  model_version TEXT,
  native_dim INT,
  activated_at TIMESTAMPTZ DEFAULT now(),
  deactivated_at TIMESTAMPTZ,
  notes TEXT
);
COMMENT ON TABLE embedding_provider_log IS
  'Audit log of embedding-provider swaps. When we migrate from openai-3-small '
  'to jina-v3, the old row gets deactivated_at set; the new row is current.';

-- ============================================================================
-- Enrichment tables
-- ============================================================================
CREATE TABLE IF NOT EXISTS transcripts (
  ad_archive_id TEXT PRIMARY KEY REFERENCES ads(ad_archive_id) ON DELETE CASCADE,
  text TEXT,
  language TEXT DEFAULT 'en',
  duration_sec NUMERIC,
  created_at TIMESTAMPTZ DEFAULT now()
);
COMMENT ON TABLE transcripts IS
  'Groq whisper-large-v3 transcripts for video ads. Only populated for winners (days_running > 30). '
  'Fall back to faster-whisper when Groq rate-limited.';

CREATE TABLE IF NOT EXISTS classifications (
  ad_archive_id TEXT PRIMARY KEY REFERENCES ads(ad_archive_id) ON DELETE CASCADE,
  schwartz_stage SMALLINT,
  angle TEXT,
  avatar_fit TEXT,
  blue_box_category TEXT,
  model TEXT DEFAULT 'nemotron-3-super',
  confidence NUMERIC,
  raw_response JSONB
);
COMMENT ON TABLE classifications IS
  'Nemotron classification. One row per ad. blue_box_category maps ads to '
  'the saturated/untargeted framework from the HITL Schwartz brief.';

CREATE TABLE IF NOT EXISTS scrape_runs (
  id BIGSERIAL PRIMARY KEY,
  industry_slug TEXT REFERENCES industries(slug),
  started_at TIMESTAMPTZ DEFAULT now(),
  finished_at TIMESTAMPTZ,
  pages_scraped INT,
  ads_found INT,
  ads_new INT,
  status TEXT,
  error_text TEXT
);
COMMENT ON TABLE scrape_runs IS
  'Append-only log of every /ads:scrape-library invocation. '
  'Used for "new this week" diffs and pipeline health.';

-- ============================================================================
-- Agent bootstrap table — first query for any fresh agent
-- ============================================================================
CREATE TABLE IF NOT EXISTS _agent_readme (
  id SMALLINT PRIMARY KEY DEFAULT 1,
  content TEXT NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT now()
);
COMMENT ON TABLE _agent_readme IS
  'Self-documenting bootstrap. An agent with zero context should SELECT content '
  'FROM _agent_readme and get enough to answer common questions.';

-- ============================================================================
-- Views
-- ============================================================================
-- v_ads: raw ads + time-dependent derived columns. Use this instead of the ads
-- table whenever you need is_new / is_recently_stopped / lifecycle_stage /
-- run_duration_days. Recomputed at every query — always reflects CURRENT_DATE.
CREATE OR REPLACE VIEW v_ads AS
  SELECT
    a.*,
    CASE
      WHEN a.status = 'ACTIVE' THEN GREATEST(0, (CURRENT_DATE - a.start_date))
      WHEN a.stopped_date IS NOT NULL AND a.start_date IS NOT NULL
        THEN GREATEST(0, (a.stopped_date - a.start_date))
      ELSE NULL
    END AS run_duration_days,
    (a.status = 'ACTIVE' AND (CURRENT_DATE - a.start_date) <= 3) AS is_new,
    (a.status = 'INACTIVE' AND a.stopped_date IS NOT NULL
      AND (CURRENT_DATE - a.stopped_date) <= 14) AS is_recently_stopped,
    CASE
      WHEN a.status = 'ACTIVE' AND (CURRENT_DATE - a.start_date) <= 3 THEN 'new'
      WHEN a.status = 'ACTIVE' AND (CURRENT_DATE - a.start_date) <= 14 THEN 'ramping'
      WHEN a.status = 'ACTIVE' AND (CURRENT_DATE - a.start_date) <= 30 THEN 'running'
      WHEN a.status = 'ACTIVE' AND (CURRENT_DATE - a.start_date) > 30 THEN 'winner'
      WHEN a.status = 'INACTIVE' AND (CURRENT_DATE - a.stopped_date) <= 14 THEN 'recently_stopped'
      WHEN a.status = 'INACTIVE' THEN 'historical'
      ELSE 'unknown'
    END AS lifecycle_stage
  FROM ads a;
COMMENT ON VIEW v_ads IS
  'Ads with time-aware derived columns (run_duration_days, is_new, is_recently_stopped, '
  'lifecycle_stage). Use this view — never the raw ads table — when you need those fields.';

CREATE OR REPLACE VIEW v_active_embeddings AS
  SELECT ad_archive_id, embedding, provider, model_version
  FROM ad_embeddings
  WHERE is_active;

CREATE OR REPLACE VIEW v_winning_ads AS
  SELECT a.*, t.text AS transcript, c.schwartz_stage AS ad_stage,
         c.angle, c.avatar_fit, c.blue_box_category,
         e.embedding AS active_embedding, e.provider AS embedding_provider
  FROM ads a
  LEFT JOIN transcripts t USING (ad_archive_id)
  LEFT JOIN classifications c USING (ad_archive_id)
  LEFT JOIN ad_embeddings e
    ON e.ad_archive_id = a.ad_archive_id AND e.is_active
  WHERE a.is_winner;

CREATE OR REPLACE VIEW v_untargeted_segments AS
  SELECT a.industry_slug, c.avatar_fit, COUNT(*) AS current_ad_count
  FROM classifications c
  JOIN ads a USING (ad_archive_id)
  GROUP BY 1, 2;

CREATE OR REPLACE VIEW v_new_this_week AS
  SELECT * FROM ads WHERE first_seen_date > CURRENT_DATE - INTERVAL '7 days';

CREATE OR REPLACE VIEW v_page_performance AS
  SELECT p.name, p.page_id, p.industry_slug,
         COUNT(a.*) FILTER (WHERE a.is_winner) AS winners,
         AVG(a.days_running)::INT AS avg_days_running,
         MAX(a.days_running) AS longest_running
  FROM pages p
  LEFT JOIN ads a USING (page_id)
  GROUP BY 1, 2, 3;

CREATE OR REPLACE VIEW v_advertiser_detail AS
  SELECT
    p.page_id,
    p.name,
    p.url,
    p.profile_pic_url,
    p.category,
    p.verified,
    p.industry_slug,
    p.full_history_complete,
    p.last_active_scrape_at,
    p.last_full_scrape_at,
    COUNT(a.*) AS ads_total,
    COUNT(a.*) FILTER (WHERE a.is_active) AS ads_active,
    COUNT(a.*) FILTER (WHERE NOT a.is_active) AS ads_stopped,
    COUNT(a.*) FILTER (WHERE a.is_winner) AS ads_winners,
    MIN(a.first_seen_date) AS earliest_ad,
    MAX(a.last_seen_active_date) AS latest_seen_active,
    AVG(a.days_running)::INT AS avg_days_running
  FROM pages p
  LEFT JOIN ads a USING (page_id)
  GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10;
