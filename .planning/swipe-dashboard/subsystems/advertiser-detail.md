# Subsystem — `/advertiser/<page_id>` page

The Meta-Ad-Library-style per-advertiser browse page. Click "Delvin Goh" from anywhere in the dashboard → see his entire ad library (active + stopped + winners) with the same drawer UX as the main grid.

## Visual structure

```
┌────────────────────────────────────────────────────────────┐
│ ← Back to library                                          │
├────────────────────────────────────────────────────────────┤
│  [Logo]  Delvin Goh · Property Agent                       │
│          ● Verified · Property · facebook.com/delvingoh    │
│          🇸🇬 Singapore · Active since Mar 2024             │
│                                                            │
│  Stats: 47 total · 12 active · 35 stopped · 8 winners     │
│         [Run full-history backfill] [Refresh active]       │
├────────────────────────────────────────────────────────────┤
│  Tabs: [ All (47) ] [ Active (12) ] [ Stopped (35) ] [ Winners (8) ] │
│  Filters: Format · Angle · Date range · Search             │
├────────────────────────────────────────────────────────────┤
│  [Masonry grid of every ad this advertiser ran]            │
└────────────────────────────────────────────────────────────┘
```

## Design language (match main dashboard exactly)
- Same color tokens: `--bg: #0c0d0e`, `--accent: #c6f94d`, `--text: #e8e9ea`
- Same font: Geist + Geist Mono
- Same masonry grid: `columns: 5 220px; column-gap: 14px`
- Same card hover reveal (Higgsfield pattern): corner action stack + bottom info strip + center play button for videos
- Same drawer (right-slide): no hero image, brand line → headline → body → CTA → Copy link button → Run timeline → Placement mix → Tagged angles → Transcript excerpt → Creative variants

## Header (new for this page)
- **Logo:** `pages.profile_pic_url` (Netlify Blobs cached). Fallback: first letter in accent-colored avatar square.
- **Name:** `pages.name`. Subtitle: `pages.category`.
- **Meta chips row:** Verified (if `pages.verified`), category name, clickable Facebook URL (`pages.url`).
- **Flag + active-since:** derived from `pages.meta.country` + `MIN(ads.start_date)`.
- **Stats row:** 4 pill cards showing `v_advertiser_detail.ads_total / ads_active / ads_stopped / ads_winners`.
- **Action buttons:**
  - `[Run full-history backfill]` — calls `POST /api/advertiser/<page_id>/backfill` → queues a deep scrape via ScrapeCreators `status='ALL'`. Disabled + shows "Full history already synced" when `pages.full_history_complete = true`.
  - `[Refresh active]` — calls `POST /api/advertiser/<page_id>/refresh` → runs shallow ACTIVE scrape now.

## Tabs
Controlled state, live counts pulled from `v_advertiser_detail`:
- **All** (`ads_total`) — every ad
- **Active** (`ads_active`) — `WHERE status='ACTIVE'`
- **Stopped** (`ads_stopped`) — `WHERE status='INACTIVE'`
- **Winners** (`ads_winners`) — `WHERE is_winner`

Tab click updates URL query param (`?tab=active`) for shareable links.

## Filters (below tabs)
Same filter bar pattern as main dashboard (chips with active state), but scoped to THIS advertiser's distinct values:
- **Format:** IMAGE / VIDEO / CAROUSEL (with counts from `WHERE page_id=X GROUP BY format`)
- **Angle:** from `classifications.angle` for this page's ads
- **Lifecycle stage:** new / ramping / running / winner / recently_stopped / historical (see `schema/temporal-model.md`)
- **Date range:** start_date within last 7 / 30 / 90 / all days
- **Search:** full-text via `ads.tsv` filtered to this page_id

## Grid
Same `AdCard` component as main dashboard. Renders `asset_url` from Netlify Blobs (not synthetic CSS surfaces). Hover reveals: save / download / copy-link / more. Click → drawer.

## Drawer (reused from main dashboard)
Same component. When opened from this page, the ←/→ nav keys walk through THIS advertiser's ad list (not the global library).

## API routes (Next.js App Router)

### `GET /api/advertiser/[page_id]`
```ts
// app/api/advertiser/[page_id]/route.ts
export async function GET(req, { params }) {
  const row = await db.query('SELECT * FROM v_advertiser_detail WHERE page_id = $1', [params.page_id]);
  if (!row) return new Response('Not found', { status: 404 });
  return Response.json(row);
}
```

### `GET /api/advertiser/[page_id]/ads`
Query params: `tab=all|active|stopped|winners`, `format=IMAGE|VIDEO|CAROUSEL`, `angle=<slug>`, `lifecycle=<stage>`, `from=<ISO>`, `to=<ISO>`, `q=<search>`, `limit=<n>`, `offset=<n>`.

```sql
SELECT ad_archive_id, headline, asset_url, format, platforms, status,
       start_date, stopped_date, run_duration_days, lifecycle_stage
FROM ads
WHERE page_id = $1
  AND ($2::text IS NULL OR status = $2)  -- tab filter
  AND ($3::text IS NULL OR format = $3)
  ...
ORDER BY start_date DESC
LIMIT $n OFFSET $m;
```

### `POST /api/advertiser/[page_id]/backfill`
Writes a row to `scrape_queue` (new table, Phase 3) → picked up by a background worker (Trigger.dev task in Phase 4) that runs `/ads:scrape-advertiser <page_id> --depth full`. Returns `{ queued: true, estimated_credits: N }`.

### `POST /api/advertiser/[page_id]/refresh`
Shallow-scrape NOW (runs inline in the request handler, ~5-10s). Calls `scrape_advertiser(page_id, status='ACTIVE')`, then `ghost_sync(industry)`. Returns the refreshed `v_advertiser_detail` row.

## Entry points (how users get to this page)
1. **Sidebar brand chip** — prototype's brand chips are filter-toggles. Add a small `↗` hover arrow that opens `/advertiser/<page_id>`.
2. **Drawer brand-line click** — clicking the brand avatar + name at the top of any ad's drawer opens that advertiser's page.
3. **Add Competitor form** — after adding a new advertiser, redirect to its `/advertiser/<page_id>` page.
4. **Direct URL** — shareable.

## Empty states
- Page loading: same shimmer pattern as main dashboard (12 skeleton cards)
- No ads match filters: same contextual empty-state from main dashboard ("No video ads from Delvin Goh in the last 30 days")
- Full-history never synced: banner at top — "Showing currently-active ads only. [Run full-history backfill] to see every ad this advertiser has ever run."

## Example interactions
- Claude Code via Ghost MCP: `SELECT * FROM v_advertiser_detail WHERE name ILIKE '%delvin%'` → get page_id → visit URL
- User clicks "Delvin Goh" chip in sidebar → `/advertiser/<delvin_page_id>?tab=winners` → sees his 8 winners
- User clicks "[Run full-history backfill]" → background deep-scrape runs, page auto-refreshes in 30s, now shows all 47 historical ads

## Related Meta Ad Library features we're NOT replicating (scope decisions)
- Political/issue-ad spend + impressions disclosures (Meta exposes these for flagged ads; we ignore for now)
- "Targeted demographics" (Meta exposes for political; not available for commercial)
- "Funded by" field (political; irrelevant)
- EU DSA transparency data (possible future feature once scraper supports it)

The commercial-ad view we're building matches what agents and the user actually need: creative + timing + classification.
