---
description: Scrape one Meta Ad Library advertiser page into the Ghost Postgres DB
version: "1.0.0"
argument-hint: <page_id|meta_url> <industry_slug> [--depth active|full] [--country SG]
---

## Purpose

Ingest a single advertiser's ads from the Meta Ad Library into the Ghost Postgres `swipe-ads` DB. Run this to add a new competitor or refresh an existing one outside of the full industry scrape cycle.

Output: ads upserted into `ads` + `pages` tables. Visible immediately in the Swipe Dashboard.

## Input

`$ARGUMENTS` — one of:

| Form | Example |
|---|---|
| `<page_id> <industry_slug>` | `100852962092831 property-sg` |
| `<meta_url> <industry_slug>` | `https://facebook.com/ads/library/?view_all_page_id=100852962092831 property-sg` |

### Flags

| Flag | Default | Notes |
|---|---|---|
| `--depth active` | `active` | Active ads only — fast, ~2–5 ScrapeCreators credits |
| `--depth full` | — | Full historical library — costs more credits. **HITL gate required.** |
| `--country SG` | `SG` | 2-letter country code passed to ScrapeCreators |

## Prerequisites

- [ ] `SCRAPECREATORS_API_KEY` in `Marketing/.env`
- [ ] `GHOST_DATABASE_URL` in `Marketing/.env` (or environment)
- [ ] Python 3.10+ with `psycopg2` and `requests` installed
- [ ] Industry slug must exist in the `industries` table (run `/ads:scrape-library <industry>` first if new)

## Execution

### Step 1 — Resolve page_id

If the user provided a Meta Ad Library URL, extract `view_all_page_id` from the query string:
```
https://www.facebook.com/ads/library/?view_all_page_id=100852962092831&country=SG
                                                        ^^^^^^^^^^^^^^^^
```

### Step 2 — HITL gate (full depth only)

If `--depth full` was requested, warn before running:

> `--depth full` scrapes the complete ad history for this page, not just active ads. It consumes significantly more ScrapeCreators credits (estimated 5–15×). The DB will grow by potentially hundreds of historical ads. Proceed?

Abort unless user confirms.

### Step 3 — Run scraper

```bash
cd "/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing"

python3 scripts/ingest-advertiser.py \
    <page_id> \
    <industry_slug> \
    --depth <active|full> \
    --country <country>
```

Script outputs a single JSON line on stdout:
```json
{"ok": true, "page_id": "...", "page_name": "...", "industry": "...", "depth": "active", "ads_total": 12, "ads_inserted": 3, "ads_updated": 9, "ad_ids": [...]}
```

Show the result to the user.

### Step 4 (optional) — SQLite re-sync

If the industry also maintains a SQLite swipe-file layer (`swipe-files/<industry>/ads-db.sqlite`) and you want it to reflect the new ads:

```bash
python3 scripts/ghost-sync.py <industry_slug>
```

Only needed if other tools (e.g. the ad-library-scraper offline pipeline) read from SQLite rather than Postgres. The Swipe Dashboard reads from Postgres directly — skip this step if that's all you need.

### Step 5 — Verify

Confirm the new page appears in the DB:

```sql
SELECT p.name, COUNT(a.*) AS ads_total,
       COUNT(a.*) FILTER (WHERE a.is_active) AS active
FROM pages p
LEFT JOIN ads a USING (page_id)
WHERE p.page_id = '<page_id>'
GROUP BY 1;
```

Or open the Swipe Dashboard — the advertiser appears in the sidebar immediately.

## Cost estimate

- `--depth active`: 2–5 ScrapeCreators credits (one per paginated result page of active ads)
- `--depth full`: 10–30+ credits depending on how long the advertiser has been running ads

## Output

```
Advertiser: <page_name>
Page ID: <page_id>
Industry: <industry_slug>
Depth: active
Ads inserted: N  (new to DB)
Ads updated: N   (refreshed status/dates)
Total seen: N
```

## See also

- Full industry scrape: `/ads:scrape-library <industry>` — scrapes ALL tracked pages for an industry
- Schema: `skills/ad-library-scraper/references/ghost-schema.sql`
- Agent query guide: `skills/ad-library-scraper/references/agent-query-cookbook.md`
- ScrapeCreators endpoint: `skills/ad-library-scraper/references/meta-ad-library-schema.md`
- Script source: `scripts/ingest-advertiser.py`
