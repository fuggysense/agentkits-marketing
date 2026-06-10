# Agent Query Cookbook — Swipe Ads DB

Read this before writing any SQL against the Swipe Ads Ghost Postgres instance (`swipe-ads`).

---

## What this DB is

A running mirror of competitor Meta Ad Library data, stored in Timescale Cloud Postgres. Every ad scraped via ScrapeCreators is upserted here — one row per `ad_archive_id`. The pipeline is:

```
Meta Ad Library → ScrapeCreators API → ingest-advertiser.py → Ghost Postgres
```

Enrichments (video transcripts, Nemotron classifications, Gemini style analysis, embeddings) are stored in satellite tables and joined at query time.

**What it solves:**
- Competitor tracking: who's running what, how long, and when they stopped
- Style reverse-engineering: what hook/angle/awareness-stage mechanics each winning ad uses
- Winner detection: proxy for "this creative is working" = ads running >30 days
- Semantic discovery: find ads similar to a reference ad via embedding distance
- Schwartz stage mapping: what market sophistication level is the industry at

---

## Bootstrap query — always run first in a fresh session

```sql
SELECT content FROM _agent_readme;
```

This returns a self-documenting README with current stats, the temporal model, all views, and a semantic search recipe. Run it before anything else — it may show a newer embedding provider or updated stats snapshot.

---

## Temporal model cheatsheet

**Do not query raw `ads` for time-aware fields. Use `v_ads`.**

| Field | Table | Notes |
|---|---|---|
| `status` | `ads` | `ACTIVE` or `INACTIVE`. Updated every scrape. |
| `start_date` | `ads` | When Meta says the ad first went live. Persistent. |
| `first_seen_date` | `ads` | When our scraper first ingested it. |
| `last_seen_active_date` | `ads` | Last scrape where it was still ACTIVE. |
| `stopped_date` | `ads` | Date we first observed it as INACTIVE. NULL = still running. Approximate. |
| `days_running` | `ads` | Set by sync script. Snapshot — not live. |
| `run_duration_days` | `v_ads` | Computed: ACTIVE → today − start_date. INACTIVE → stopped_date − start_date. |
| `is_winner` | `ads` | Stored: `days_running > 30`. Proxy for "this is working." |
| `is_new` | `v_ads` | ACTIVE and started ≤3 days ago. |
| `is_recently_stopped` | `v_ads` | INACTIVE and stopped ≤14 days ago. |
| `lifecycle_stage` | `v_ads` | Computed bucket: `new / ramping / running / winner / recently_stopped / historical` |

**Prefer `lifecycle_stage` over raw date arithmetic.** It's what every downstream skill uses.

**Lifecycle stage definitions:**

| Stage | Condition | Meaning |
|---|---|---|
| `new` | ACTIVE, ≤3 days | Just launched |
| `ramping` | ACTIVE, 3–14 days | Testing phase |
| `running` | ACTIVE, 14–30 days | Stable run |
| `winner` | ACTIVE, >30 days | Proven — budget behind this |
| `recently_stopped` | INACTIVE, stopped ≤14 days | Potential creative fatigue |
| `historical` | INACTIVE, stopped >14 days | Archive |

---

## Recipes

### Discovery

**All winners in an industry, ranked by longevity**

```sql
SELECT a.ad_archive_id, p.name AS advertiser, a.headline,
       a.days_running, a.meta_library_url
FROM ads a
JOIN pages p USING (page_id)
WHERE a.industry_slug = 'property-sg'
  AND a.is_winner = true
ORDER BY a.days_running DESC
LIMIT 20;
```

**Advertisers with the most winners (competitive ranking)**

```sql
SELECT name, page_id, winners, avg_days_running, longest_running
FROM v_page_performance
WHERE industry_slug = 'property-sg'
ORDER BY winners DESC NULLS LAST
LIMIT 10;
```

**Newest ads this week (what competitors just launched)**

```sql
SELECT ad_archive_id, page_id, headline, first_seen_date, lifecycle_stage
FROM v_ads
WHERE industry_slug = 'property-sg'
  AND first_seen_date > CURRENT_DATE - INTERVAL '7 days'
ORDER BY first_seen_date DESC;
```

---

### Temporal

**Ads that stopped this week (creative fatigue / budget kill signal)**

```sql
SELECT ad_archive_id, page_id, headline, days_running,
       stopped_date, last_seen_active_date
FROM v_ads
WHERE industry_slug = 'property-sg'
  AND lifecycle_stage = 'recently_stopped'
ORDER BY stopped_date DESC;
```

**Longest-running ad per advertiser (one winner per page)**

```sql
SELECT DISTINCT ON (a.page_id)
       p.name, a.ad_archive_id, a.headline,
       a.days_running, a.meta_library_url
FROM ads a
JOIN pages p USING (page_id)
WHERE a.industry_slug = 'property-sg'
  AND a.is_winner = true
ORDER BY a.page_id, a.days_running DESC;
```

**Ads that ran exactly 7–30 days then stopped (early creative fatigue)**

```sql
SELECT ad_archive_id, page_id, headline,
       run_duration_days, stopped_date
FROM v_ads
WHERE industry_slug = 'property-sg'
  AND lifecycle_stage = 'historical'
  AND run_duration_days BETWEEN 7 AND 30
ORDER BY run_duration_days DESC
LIMIT 20;
```

---

### Classification (Nemotron-enriched ads only)

**Winners by Schwartz awareness stage**

```sql
SELECT c.schwartz_stage, COUNT(*) AS ad_count,
       AVG(a.days_running)::INT AS avg_days_running
FROM classifications c
JOIN ads a USING (ad_archive_id)
WHERE a.industry_slug = 'property-sg'
  AND a.is_winner = true
GROUP BY c.schwartz_stage
ORDER BY c.schwartz_stage;
```

**Winners grouped by creative angle**

```sql
SELECT c.angle, COUNT(*) AS count, AVG(a.days_running)::INT AS avg_run
FROM classifications c
JOIN ads a USING (ad_archive_id)
WHERE a.industry_slug = 'property-sg'
  AND a.is_winner = true
GROUP BY c.angle
ORDER BY count DESC;
```

**Avatar-fit coverage (untargeted segments)**

```sql
SELECT avatar_fit, current_ad_count
FROM v_untargeted_segments
WHERE industry_slug = 'property-sg'
ORDER BY current_ad_count DESC;
```

---

### Semantic search via `v_active_embeddings`

The embedding layer is provider-agnostic. Always go through `v_active_embeddings` — it auto-selects the current active provider (check `_agent_readme` to see which one).

**Find ads semantically similar to a reference ad**

```sql
WITH seed AS (
  SELECT embedding
  FROM v_active_embeddings
  WHERE ad_archive_id = '753407127406583'   -- replace with your reference ad_archive_id
)
SELECT a.ad_archive_id, a.headline, p.name AS advertiser,
       a.days_running, a.meta_library_url,
       e.embedding <=> seed.embedding AS distance
FROM ads a
JOIN v_active_embeddings e USING (ad_archive_id), seed
JOIN pages p USING (page_id)
WHERE a.industry_slug = 'property-sg'
  AND a.ad_archive_id != '753407127406583'
ORDER BY distance
LIMIT 10;
```

Lower `distance` = more similar. Distance > 0.4 is usually not relevant.

**Full-text search (fast, no embeddings needed)**

```sql
SELECT ad_archive_id, headline, body_text, days_running, meta_library_url
FROM ads
WHERE industry_slug = 'property-sg'
  AND tsv @@ plainto_tsquery('english', 'upgrade property free ebook')
ORDER BY days_running DESC
LIMIT 10;
```

---

### Style analysis via `ad_styles`

`ad_styles` is populated by the dashboard's reverse-engineer endpoint (Gemini 2.5). Each row has an `analysis` JSONB field with mechanics extracted by a direct-response strategist prompt.

**Key fields inside `analysis` JSONB:**

| Key | What it contains |
|---|---|
| `hook_type` | Pattern name (e.g. "calling-out segment", "contrarian warning") |
| `angle_family` | One of 8 families (problem-aware fear, mechanism-led proof, etc.) |
| `visual_style` | One-sentence visual description |
| `tone` | 2–3 adjectives |
| `awareness_stage` | Schwartz 1–5 (unaware → most-aware) |
| `sophistication_stage` | Schwartz sophistication level description |
| `desire_lever` | Cashvertising LF8 lever (survival, fear-of-loss, etc.) |
| `headline_formula` | Reusable template with `[brackets]` |
| `cta_psychology` | Why the CTA feels low-friction |
| `audience_hint` | Who it's targeting |
| `copycat_recipe` | 3–5 steps to clone the mechanics for a different product |

**Winners with style analysis — headline formulas in use**

```sql
SELECT a.ad_archive_id, a.headline, a.days_running,
       s.analysis->>'hook_type' AS hook_type,
       s.analysis->>'angle_family' AS angle_family,
       s.analysis->>'headline_formula' AS headline_formula,
       s.analysis->>'desire_lever' AS desire_lever
FROM ads a
JOIN ad_styles s USING (ad_archive_id)
WHERE a.industry_slug = 'property-sg'
  AND a.is_winner = true
ORDER BY a.days_running DESC;
```

**Group winners by hook type (what's dominating the market)**

```sql
SELECT s.analysis->>'hook_type' AS hook_type,
       COUNT(*) AS winner_count,
       AVG(a.days_running)::INT AS avg_run
FROM ad_styles s
JOIN ads a USING (ad_archive_id)
WHERE a.industry_slug = 'property-sg'
  AND a.is_winner = true
GROUP BY 1
ORDER BY winner_count DESC;
```

**Get copycat recipe for a specific winning ad**

```sql
SELECT a.headline, a.days_running,
       jsonb_array_elements_text(s.analysis->'copycat_recipe') AS step
FROM ad_styles s
JOIN ads a USING (ad_archive_id)
WHERE a.ad_archive_id = '753407127406583';   -- replace with target ad
```

---

## Write-path — how new ads get into the DB

**Do not write to `ads`, `pages`, `transcripts`, or `classifications` directly** unless you fully understand the temporal reconciliation logic. The scraper maintains `first_seen_date`, `last_seen_active_date`, and `stopped_date` with specific upsert semantics — blind INSERTs will corrupt the lifecycle model.

**The correct write path:**

```bash
# From Marketing repo root:
python3 scripts/ingest-advertiser.py <page_id> <industry_slug> \
    --depth active \     # active = current ads only (fast, cheap)
    --country SG

# After scraping, if the SQLite swipe-file layer is also in use:
python3 scripts/ghost-sync.py <industry_slug>
```

The only table safe to write directly is `ad_styles` (the dashboard does this via the reverse-engineer endpoint — it's a pure upsert with no temporal logic).

---

## MCP vs HTTP — when to use which

| Need | Use |
|---|---|
| Query the DB from inside a Claude session | `mcp__ghost__ghost_sql` with `id: "swipe-ads"` |
| Load ads for the dashboard UI | `GET /api/ads?industry=property-sg` (REST) |
| Stream a video/image asset from local disk | `GET /api/asset?p=<path>` (local only) |
| Trigger a Gemini reverse-engineer | `POST /api/reverse-engineer/<ad_archive_id>` |
| Trigger a scrape from the UI | `POST /api/scrape-advertiser` (local only — not on Netlify) |

For agent queries (research, analysis, cookbook recipes), always use `mcp__ghost__ghost_sql`. It's direct, no HTTP overhead, and supports multi-statement queries.

---

## Quick reference — all tables and views

| Object | Type | Purpose |
|---|---|---|
| `industries` | table | One row per industry slug |
| `pages` | table | One row per Facebook page (advertiser) |
| `ads` | table | One row per ad_archive_id — raw facts + immutable derived |
| `ad_embeddings` | table | Embeddings, decoupled by provider |
| `transcripts` | table | Groq Whisper transcripts for video winners |
| `classifications` | table | Nemotron Schwartz/angle/avatar classification |
| `ad_styles` | table | Gemini reverse-engineer output (JSONB analysis) |
| `scrape_runs` | table | Append-only log of every scrape run |
| `_agent_readme` | table | Self-documenting bootstrap (query this first) |
| `v_ads` | view | ads + time-aware derived columns — use this over raw `ads` |
| `v_winning_ads` | view | Winners + transcript + classification + active embedding |
| `v_advertiser_detail` | view | Per-page totals (total/active/stopped/winners) |
| `v_new_this_week` | view | Ads first_seen in last 7 days |
| `v_untargeted_segments` | view | Buyer-segment coverage from Schwartz classification |
| `v_page_performance` | view | Per-advertiser rollup (winners, avg/max days_running) |
| `v_active_embeddings` | view | Current-provider-only embeddings — use for semantic queries |
