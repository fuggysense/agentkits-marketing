# Schema — Temporal Model

The piece that makes the DB actually useful for agents: rich time-aware fields on every ad so queries like "which winners just stopped" or "Delvin Goh's longest-running ad ever" are one SELECT away.

## Core date fields on `ads`

| Field | Source | Semantics |
|---|---|---|
| `start_date` | Meta's reported first-live date (persistent across scrapes — never overwritten) | When the ad went live, according to Meta |
| `first_seen_date` | MIN(existing, today) during sync | When OUR scraper first observed the ad |
| `last_seen_active_date` | today IF status=ACTIVE, else unchanged | Last scrape we saw it as ACTIVE |
| `stopped_date` | today, set the moment scraper detects ad no longer ACTIVE | When we first observed it stopped. NULL while still running. |
| `status` | ScrapeCreators `facebook_company_ads` | 'ACTIVE' or 'INACTIVE' |

**stopped_date semantics:** approximate — actual stop could have been any time between `last_seen_active_date` and `stopped_date` (the gap is our scrape cadence).

## Generated columns (all `STORED`, no runtime compute cost)

### `run_duration_days INT`
```sql
run_duration_days INT GENERATED ALWAYS AS (
  CASE
    WHEN status = 'ACTIVE'
      THEN GREATEST(0, (CURRENT_DATE - start_date))
    WHEN stopped_date IS NOT NULL AND start_date IS NOT NULL
      THEN GREATEST(0, (stopped_date - start_date))
    ELSE NULL
  END
) STORED
```
Total days the ad ran. Active: today − start. Inactive: stopped − start.

### `is_new BOOLEAN`
```sql
is_new BOOLEAN GENERATED ALWAYS AS (
  status = 'ACTIVE' AND (CURRENT_DATE - start_date) <= 3
) STORED
```

### `is_winner BOOLEAN`
```sql
is_winner BOOLEAN GENERATED ALWAYS AS (days_running > 30) STORED
```
Proxy for "this is working." Used everywhere: `v_winning_ads`, `v_advertiser_detail` stats, enrichment gating (transcripts only pulled for winners).

### `is_active BOOLEAN`
```sql
is_active BOOLEAN GENERATED ALWAYS AS (status = 'ACTIVE') STORED
```

### `is_recently_stopped BOOLEAN`
```sql
is_recently_stopped BOOLEAN GENERATED ALWAYS AS (
  status = 'INACTIVE' AND stopped_date IS NOT NULL
    AND (CURRENT_DATE - stopped_date) <= 14
) STORED
```
Creative fatigue signal. A winner that just stopped = "this was working until it wasn't."

### `lifecycle_stage TEXT` — THE authoritative bucket
```sql
lifecycle_stage TEXT GENERATED ALWAYS AS (
  CASE
    WHEN status = 'ACTIVE' AND (CURRENT_DATE - start_date) <= 3 THEN 'new'
    WHEN status = 'ACTIVE' AND (CURRENT_DATE - start_date) <= 14 THEN 'ramping'
    WHEN status = 'ACTIVE' AND (CURRENT_DATE - start_date) <= 30 THEN 'running'
    WHEN status = 'ACTIVE' AND (CURRENT_DATE - start_date) > 30 THEN 'winner'
    WHEN status = 'INACTIVE' AND (CURRENT_DATE - stopped_date) <= 14 THEN 'recently_stopped'
    WHEN status = 'INACTIVE' THEN 'historical'
    ELSE 'unknown'
  END
) STORED
```

| Stage | Meaning |
|---|---|
| `new` | ACTIVE, started ≤3 days ago |
| `ramping` | ACTIVE, 3-14 days in |
| `running` | ACTIVE, 14-30 days in |
| `winner` | ACTIVE, >30 days (proxy for "this is working") |
| `recently_stopped` | INACTIVE, stopped ≤14 days ago (creative fatigue signal) |
| `historical` | INACTIVE, stopped >14 days ago |

**Agents: prefer `lifecycle_stage` over raw date math when classifying ads.**

## Scraper disappearance-detection logic

The trick for `stopped_date`: shallow (ACTIVE-only) scrapes don't return INACTIVE ads, so we infer a stop by diffing what was ACTIVE last time vs what's ACTIVE now.

```python
# Before upserting from the new scrape
previously_active = set of ad_archive_ids WHERE industry_slug=$I AND status='ACTIVE'
currently_seen_active = set of ad_archive_ids in the new scrape with status=ACTIVE

# Ads that were ACTIVE but aren't in the new scrape = they just stopped
newly_stopped = previously_active - currently_seen_active
```

After upserting every scraped row (which may overwrite status but NOT stopped_date for still-active), mark the disappeared ones:

```sql
UPDATE ads
SET status = 'INACTIVE',
    stopped_date = CURRENT_DATE
WHERE ad_archive_id = ANY(%(newly_stopped)s)
  AND stopped_date IS NULL;
```

## Deep scrape (status=ALL) is authoritative for INACTIVE ads
When `/ads:scrape-advertiser <page_id> --depth full` runs, ScrapeCreators returns both ACTIVE and INACTIVE ads with Meta's authoritative `end_date` / stopped marker. That scrape:
- Sets `status`, `start_date` directly from Meta's payload
- If INACTIVE and payload includes a stop date, populate `stopped_date` from it (preferred over our inferred value)
- Flags `pages.full_history_complete = true` on success

## Query examples (lifecycle-aware)

```sql
-- Which ads just stopped this week?
SELECT page_id, headline, run_duration_days
FROM ads
WHERE industry_slug='property-sg'
  AND stopped_date > CURRENT_DATE - INTERVAL '7 days'
ORDER BY run_duration_days DESC;

-- Delvin Goh's longest-running ad ever (active or historical)
SELECT headline, status, start_date, stopped_date, run_duration_days
FROM ads
WHERE page_id = '<delvin_page_id>'
ORDER BY run_duration_days DESC NULLS LAST
LIMIT 1;

-- Creative-fatigue list: winners that just stopped
SELECT page_id, headline, run_duration_days, stopped_date
FROM ads
WHERE is_recently_stopped
  AND run_duration_days > 30
ORDER BY run_duration_days DESC;

-- Lifecycle distribution per advertiser
SELECT p.name, a.lifecycle_stage, COUNT(*)
FROM ads a JOIN pages p USING (page_id)
WHERE a.industry_slug='property-sg'
GROUP BY 1, 2
ORDER BY 1, 2;

-- Single-ad temporal snapshot
SELECT status, lifecycle_stage, start_date, stopped_date, run_duration_days
FROM ads WHERE ad_archive_id=$1;

-- Creative lifespan by Schwartz stage (do higher-stage ads last longer?)
SELECT c.schwartz_stage,
       AVG(a.run_duration_days)::int AS avg_days,
       COUNT(*) AS n
FROM ads a JOIN classifications c USING (ad_archive_id)
WHERE a.status='INACTIVE'
GROUP BY 1
ORDER BY 1;
```

## Agent usage rule
When an agent answers time-aware questions, it MUST:
1. Filter on `lifecycle_stage` or the generated booleans (`is_winner`, `is_recently_stopped`, `is_active`)
2. Use `run_duration_days` (not the legacy `days_running`) for duration reasoning
3. Never assume "days_running" means "currently running" — the ad may be INACTIVE
4. When reporting dates to the user, show `start_date` + `stopped_date` (or "still running") explicitly

The `_agent_readme` bootstrap doc restates this so fresh agent sessions pick it up automatically.
