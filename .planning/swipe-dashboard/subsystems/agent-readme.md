# Subsystem — `_agent_readme` seed content

This is the single-row `_agent_readme` table that any fresh agent reads FIRST. It's the bootstrap doc that teaches the domain + schema + conventions in one query: `SELECT content FROM _agent_readme`.

Written to the DB by Phase 2's `scripts/seed-agent-readme.ts` (or updated by `scripts/ghost-sync.py` on every sync to refresh stats).

## Why this matters
- Ghost MCP gives agents raw SQL access to the DB, but raw schemas don't teach intent
- A fresh agent session needs to know: what's an ad, what's a winner, why do we care about Schwartz stage, how do we search semantically
- Without this, agents default to raw queries that miss the views, ignore `lifecycle_stage`, and generate wrong interpretations
- With this, the agent's first query reads the doc → subsequent queries are correct + conventional

## Full seed content (markdown stored as TEXT)

```markdown
# Swipe Ads DB — agent bootstrap

You are querying the Swipe Ads Ghost Postgres DB. It stores competitor ads
scraped from the Meta Ad Library, one row per ad_archive_id.

## Core mental model

- `industries` → `pages` (advertisers) → `ads` (individual creatives)
- Every ad has classifications (Schwartz stage, angle, avatar_fit), optionally
  a transcript (for video), and an embedding (in `ad_embeddings`, one row per
  provider; query through `v_active_embeddings` to be provider-agnostic).

## THE TEMPORAL MODEL — READ THIS BEFORE TIME-AWARE QUERIES

Every ad has a lifecycle. Don't assume "running" means currently live. Use
these fields for time reasoning:

- `status`: 'ACTIVE' (currently running) or 'INACTIVE' (stopped).
- `start_date`: when Meta says the ad first went live.
- `stopped_date`: when our scraper first observed it as no-longer-ACTIVE.
  NULL while still active. Approximate — actual stop could have been any time
  between `last_seen_active_date` and `stopped_date`.
- `run_duration_days`: total days the ad ran.
  For ACTIVE: today − start_date. For INACTIVE: stopped_date − start_date.
- `is_active`, `is_new`, `is_winner`, `is_recently_stopped`: computed booleans.
- `lifecycle_stage`: authoritative bucket — use this over raw date math.
    - `new` — ACTIVE, started ≤3 days ago
    - `ramping` — ACTIVE, 3-14 days in
    - `running` — ACTIVE, 14-30 days in
    - `winner` — ACTIVE, >30 days (proxy for "this is working")
    - `recently_stopped` — INACTIVE, stopped ≤14 days ago (creative fatigue signal)
    - `historical` — INACTIVE, stopped >14 days ago

Prefer `lifecycle_stage` over raw date math when classifying ads.

## Important views (prefer over raw joins)

- `v_winning_ads` — all winners with transcript + classification + active embedding
- `v_advertiser_detail` — one row per page with totals (total/active/stopped/winners)
- `v_new_this_week` — ads first_seen in the last 7 days (our scraper perspective)
- `v_untargeted_segments` — buyer-segment coverage per industry from HITL brief
- `v_page_performance` — per-advertiser rollup for sidebar counts
- `v_active_embeddings` — current-provider-only embeddings for semantic queries

## What fields DO NOT exist (common mistakes)

Meta Ad Library does NOT expose and we do NOT store:
- Estimated spend ($)
- Impressions count
- CTR %
- Placement-mix percentages
- Ad-reach / targeting specifics (except for political/issue ads, which we skip)

If a user asks "how much did this ad spend," the answer is "Meta Ad Library
doesn't expose that for commercial ads." Use `run_duration_days` and
`is_winner` as proxies for "working well."

## Semantic search recipe (provider-agnostic)

```sql
WITH seed AS (
  SELECT embedding FROM v_active_embeddings WHERE ad_archive_id = $1
)
SELECT a.headline, a.body_text,
       e.embedding <=> seed.embedding AS distance
FROM ads a
JOIN v_active_embeddings e USING (ad_archive_id), seed
ORDER BY distance
LIMIT 5;
```

## Full-text search recipe

```sql
SELECT headline, body_text,
       ts_rank(tsv, to_tsquery('english', $1)) AS rank
FROM ads
WHERE tsv @@ to_tsquery('english', $1)
ORDER BY rank DESC
LIMIT 20;
```

## Common query patterns

-- Which ads stopped this week?
SELECT page_id, headline, run_duration_days
FROM ads
WHERE stopped_date > CURRENT_DATE - INTERVAL '7 days';

-- Delvin Goh's longest-running ad ever
SELECT headline, status, start_date, stopped_date, run_duration_days
FROM ads
WHERE page_id = (SELECT page_id FROM pages WHERE name ILIKE '%delvin%' LIMIT 1)
ORDER BY run_duration_days DESC NULLS LAST
LIMIT 1;

-- Creative fatigue list: winners that just stopped
SELECT page_id, headline, run_duration_days, stopped_date
FROM ads
WHERE is_recently_stopped AND run_duration_days > 30;

-- Untargeted buyer segments (from HITL Schwartz brief)
SELECT industry_slug, avatar_fit, current_ad_count
FROM v_untargeted_segments
WHERE industry_slug = 'property-sg'
ORDER BY current_ad_count ASC;

-- Blue-box category distribution
SELECT blue_box_category, COUNT(*)
FROM classifications c
JOIN ads a USING (ad_archive_id)
WHERE a.industry_slug = 'property-sg'
GROUP BY 1;

## Current active embedding provider

{POPULATED AT SYNC TIME — e.g. "ollama:ollama/nomic-embed-text (768 native → 1024 padded to target)"}

## Stats snapshot (as of last sync)

{POPULATED AT SYNC TIME — e.g.
- 1 industry (property-sg, Schwartz stage 4, HIGH confidence)
- 10 pages (advertisers)
- 60 ads total (60 active, 0 inactive)
- 8 winners (running >30 days)
- 8 transcripts (video winners)
- 60 classifications (Nemotron)
- 60 active embeddings (ollama/nomic-embed-text)
- Last sync: 2026-04-20 09:42 SGT
}

## Agent conventions

1. Always prefer `v_*` views over raw joins
2. Use `lifecycle_stage` for time-aware queries
3. Use `v_active_embeddings` for semantic search (provider-agnostic)
4. Never fabricate spend/impressions/CTR data — it doesn't exist
5. When the user asks for "winning" ads, filter on `is_winner` (>30 days)
6. When the user asks about "new" or "recent" ads, check whether they mean
   first_seen (our scraper) or start_date (Meta's record) — they can differ by days
7. To find an advertiser by name, use ILIKE on `pages.name`
8. To open an ad in Meta Ad Library UI, use the generated `ads.meta_library_url` column
```

## Update cadence
The `_agent_readme` row gets rewritten at the end of every `scripts/ghost-sync.py` run:
- `{POPULATED AT SYNC TIME}` sections filled with current stats
- `activated_at` timestamp of the current embedding provider
- Row counts per industry, status, classification coverage
- List of pages + their ad counts (top 10 for brevity)

## Testing the seed
Phase 1 verification step:
```sql
SELECT length(content), updated_at FROM _agent_readme;  -- should return non-zero length + recent timestamp
SELECT substring(content from 1 for 500) FROM _agent_readme;  -- read the first 500 chars to eyeball
```

Then via Ghost MCP from Claude Code:
```
query: SELECT content FROM _agent_readme
```
Response should be the full markdown above with stats populated.

## Security note (per `planning-with-files` security boundary)
`_agent_readme` contents ARE injected into every MCP query response and are included when the agent starts a session. Therefore:
- Never include user-generated or externally-scraped content in `_agent_readme`
- Only include schema docs, query recipes, and computed stats (all trusted sources)
- Prompt-injection risk: agents reading this doc will follow its "conventions" section — keep it tight and true
