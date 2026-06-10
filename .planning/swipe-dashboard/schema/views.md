# Schema — Views

Pre-computed query shortcuts. Agents should prefer views over raw joins — less surface area, cleaner intent, easier to evolve the underlying tables.

## `v_winning_ads`
Every winner (running >30 days OR historical winner) joined with transcript + classification + active embedding.
```sql
CREATE VIEW v_winning_ads AS
  SELECT a.*,
         t.text AS transcript,
         c.schwartz_stage AS ad_stage,
         c.angle,
         c.avatar_fit,
         c.blue_box_category,
         e.embedding AS active_embedding,
         e.provider AS embedding_provider
  FROM ads a
  LEFT JOIN transcripts t USING (ad_archive_id)
  LEFT JOIN classifications c USING (ad_archive_id)
  LEFT JOIN ad_embeddings e
    ON e.ad_archive_id = a.ad_archive_id AND e.is_active
  WHERE a.is_winner;
```

## `v_active_embeddings`
Provider-agnostic semantic-search view. Always routes to the currently-active provider.
```sql
CREATE VIEW v_active_embeddings AS
  SELECT ad_archive_id, embedding, provider, model_version
  FROM ad_embeddings
  WHERE is_active;
```

Usage (provider-swap-safe):
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

## `v_untargeted_segments`
Buyer-segment coverage per industry. Cross-references classifications against HITL Schwartz brief's identified avatars.
```sql
CREATE VIEW v_untargeted_segments AS
  SELECT industry_slug, avatar_fit,
         COUNT(*) AS current_ad_count
  FROM classifications c
  JOIN ads a USING (ad_archive_id)
  GROUP BY 1, 2;
```
Agent query: "which property-sg avatars are untargeted?" → rows with low/zero `current_ad_count`.

## `v_new_this_week`
Ads first observed in the last 7 days (our-scraper perspective).
```sql
CREATE VIEW v_new_this_week AS
  SELECT * FROM ads
  WHERE first_seen_date > CURRENT_DATE - INTERVAL '7 days';
```

## `v_page_performance`
Per-advertiser rollup. Powers the sidebar count chips + advertiser picker UX.
```sql
CREATE VIEW v_page_performance AS
  SELECT p.name, p.page_id, p.industry_slug,
         COUNT(a.*) FILTER (WHERE a.is_winner) AS winners,
         AVG(a.days_running)::INT AS avg_days_running,
         MAX(a.days_running) AS longest_running
  FROM pages p
  LEFT JOIN ads a USING (page_id)
  GROUP BY 1, 2, 3;
```

## `v_advertiser_detail`
Powers the `/advertiser/<page_id>` page header stats row.
```sql
CREATE VIEW v_advertiser_detail AS
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
    MAX(a.last_seen_date) AS latest_ad,  -- NB: add ads.last_seen_date column (or coalesce last_seen_active_date for active / stopped_date for inactive)
    AVG(a.days_running)::INT AS avg_days_running
  FROM pages p
  LEFT JOIN ads a USING (page_id)
  GROUP BY 1,2,3,4,5,6,7,8,9,10;
```

Note: `ads` has `last_seen_active_date` and `stopped_date` but no single `last_seen_date` column. For the view, replace `MAX(a.last_seen_date)` with:
```sql
MAX(COALESCE(a.stopped_date, a.last_seen_active_date)) AS latest_ad
```

## Future views
- `v_creative_fatigue` — `recently_stopped` winners grouped by page, for a "who's running out of ideas" dashboard card
- `v_similar_to_winner` — materialized view that pre-computes top-5 similar ads for every winner (nightly refresh)
- `v_cross_industry_angles` — angle distribution across multiple industries, once we scrape 2+

## Materialization strategy
Start all views as regular (non-materialized) views — cheap, always fresh. If query perf degrades once we pass ~10k ads, convert hot views (`v_winning_ads`, `v_advertiser_detail`) to `MATERIALIZED VIEW` with a `REFRESH MATERIALIZED VIEW CONCURRENTLY` step appended to `ghost-sync.py` after every scrape.
