# Verification — 10-point end-to-end checklist

Run these AFTER Phase 4 (deploy + agent MCP polish) is complete. Every check must pass before calling the project shipped.

## V1 — Ghost infrastructure live
- `ghost --version` returns a version string
- `ghost list` shows a database named `swipe-ads`
- `mcp__ghost__*` tools visible to Claude Code in a fresh session (run `/help` or inspect tool list)
- Can query: `mcp__ghost__query "SELECT name, installed_version FROM pg_available_extensions WHERE name IN ('vector','vectorscale','pg_trgm','pg_textsearch')"` → returns rows confirming all 4 extensions available (or 3/4 if pg_textsearch absent, documented in findings.md)

## V2 — Agent bootstrap works
- `SELECT content FROM _agent_readme` returns non-empty markdown
- Content includes the TEMPORAL MODEL section, view list, current active provider, and stats snapshot with real numbers (not `{POPULATED AT SYNC TIME}` placeholders)
- A fresh Claude Code session reads this row as its first DB query automatically (via MCP hint) or on explicit prompt

## V3 — Row counts match SQLite after sync
After `python scripts/ghost-sync.py property-sg`:
```sql
SELECT
  (SELECT COUNT(*) FROM ads WHERE industry_slug='property-sg') AS ghost_ads,
  (SELECT COUNT(*) FROM pages WHERE industry_slug='property-sg') AS ghost_pages,
  (SELECT COUNT(*) FROM transcripts t JOIN ads a USING(ad_archive_id) WHERE a.industry_slug='property-sg') AS ghost_transcripts,
  (SELECT COUNT(*) FROM classifications c JOIN ads a USING(ad_archive_id) WHERE a.industry_slug='property-sg') AS ghost_classifications,
  (SELECT COUNT(*) FROM ad_embeddings e JOIN ads a USING(ad_archive_id) WHERE a.industry_slug='property-sg' AND e.is_active) AS ghost_active_embeddings;
```

Compare against SQLite counts (`sqlite3 swipe-files/property-sg/ads-db.sqlite 'SELECT COUNT(*) FROM ads;'` etc.). Ads + pages should match exactly. Transcripts/classifications should match what's in the filesystem.

## V4 — Semantic search returns sensible matches
```sql
WITH seed AS (
  SELECT embedding FROM v_active_embeddings
  WHERE ad_archive_id = (SELECT ad_archive_id FROM ads WHERE is_winner LIMIT 1)
)
SELECT a.headline, e.embedding <=> seed.embedding AS distance
FROM ads a
JOIN v_active_embeddings e USING (ad_archive_id), seed
ORDER BY distance
LIMIT 5;
```
Top 5 results should be thematically related (same angle, similar hook, same avatar). Manually eyeball: distance values should be monotonically increasing and reasonable (typically 0.0 to 0.6 range for cosine-similar ads).

## V5 — Dashboard renders real property-sg ads
Visit the deployed dashboard URL:
- Grid shows ~60 real ad creatives (actual mp4/jpg from Netlify Blobs, not CSS surfaces)
- Videos play on hover (center play button)
- Brand chip (top-left of card) shows real page name
- Days-running + first-seen date in bottom strip matches Meta Ad Library when cross-checked

## V6 — Filters work correctly
On the dashboard:
- Click a brand chip in sidebar → grid filters to that advertiser's ads
- Click "VIDEO" format chip → only video ads remain
- Click "Running 30d+" → only winners remain
- Click "New only" → only ads with `is_new=true` remain
- Active filters visible in top subbar; results-count updates live
- Empty states show contextual message (e.g., "No video ads from Delvin Goh in the last 7 days")

## V7 — Drawer shows REAL metrics (no fake $/CTR)
Click any ad → drawer opens → performance snapshot shows:
- Days running: real number
- Last seen: real date
- Schwartz stage: 1-5 with confidence label
- Blue-box category: saturated/untargeted/emerging
- Transcript excerpt (if video + winner)
- Tagged angles from classifications
- Run timeline with start → today/stopped
- Runs on: platform chips (Meta binary, others greyed)

Explicitly verify: the drawer does NOT show fake "Est. spend $Xk" or "Impressions 1.2M" or "CTR 2.3%".

## V8 — Copy-link generates working Meta Ad Library URL
Click "Copy link" in drawer or card action stack → clipboard contains `https://www.facebook.com/ads/library/?id=<ad_archive_id>`. Paste into browser → Meta Ad Library opens the exact same ad.

## V9 — Companion pages work
- `/saved` — ads you've saved appear in boards grid, with notes/tags; bulk-select works
- `/add-competitor` — paste a Meta Ad Library URL → preview card appears → "Pull full history now" toggle visible → "Start watching" succeeds → page added to pages_queue (or directly scraped)
- `/settings` — API-key management UI renders; can create/rotate/revoke a key
- `/advertiser/<page_id>` — header + stats + tabs + masonry grid all load for a known page_id (e.g., the Delvin Goh page); "Run full-history backfill" button queues a scrape

## V9.5 — ad_archive_id tagging is consistent end-to-end
Random-sample audit: pick 3 ads at random, trace them through every artifact layer.

```bash
# Pick 3 ad_archive_ids
SAMPLE=$(sqlite3 swipe-files/property-sg/ads-db.sqlite "SELECT ad_archive_id FROM ads ORDER BY RANDOM() LIMIT 3")

for AD in $SAMPLE; do
  echo "=== $AD ==="
  # Filesystem
  find swipe-files/property-sg -name "*${AD}*"     # should list: 1 JSON, maybe transcript, maybe asset
  # Sidecar header check (if transcript exists)
  head -10 swipe-files/property-sg/pages/*/ads/${AD}-transcript.txt 2>/dev/null | grep "ad_archive_id: ${AD}"
  # Ghost row
  psql $GHOST_URL -c "SELECT ad_archive_id, status, page_id FROM ads WHERE ad_archive_id='${AD}'"
  # Netlify Blobs key (indirectly, via asset_url)
  psql $GHOST_URL -c "SELECT asset_url FROM ads WHERE ad_archive_id='${AD}'"   # URL should contain the ID
done
```
Every artifact must embed the same ad_archive_id. If any layer is missing it or has a different value → sync is broken.

## V10 — Fresh agent can answer lifecycle-aware question without help
In a brand-new Claude Code session (no prior context), connect to Ghost MCP and ask:
> "Which property-sg ads target the life-transition avatar and are winners?"

Expected agent flow:
1. `SELECT content FROM _agent_readme` — learns schema
2. `SELECT * FROM v_winning_ads WHERE industry_slug='property-sg' AND avatar_fit='life-transition'` — direct answer
3. Presents headline + page_name + days_running + lifecycle_stage for each result

The agent should NOT try to compute `days_running` manually, should NOT fabricate spend data, should correctly use `v_winning_ads` view.

## Bonus verification (not blocking, nice-to-have)

### B1 — Provider swap works end-to-end
1. `export EMBEDDING_PROVIDER=jina EMBEDDING_MODEL=jina-embeddings-v3 JINA_API_KEY=...`
2. `python scripts/ghost-sync.py property-sg --reembed-all`
3. Verify `embedding_provider_log` has a new row with old provider deactivated
4. Verify `v_active_embeddings` returns Jina provider
5. Re-run V4 semantic search → quality should be comparable or better

### B2 — Temporal reconciliation catches a disappeared ad
1. Note a currently-ACTIVE ad in Ghost (pick one with recent `last_seen_active_date`)
2. Manually DELETE that ad from the SQLite source (simulate Meta removing the ad)
3. Run `python scripts/ghost-sync.py property-sg`
4. Verify the Ghost row now has `status='INACTIVE'`, `stopped_date=today`, `lifecycle_stage='recently_stopped'`

### B3 — Full-history backfill works
1. Pick an advertiser with `pages.full_history_complete=false`
2. `POST /api/advertiser/<page_id>/backfill` or manually: `/ads:scrape-advertiser <page_id> --depth full`
3. Verify Ghost row count for that page jumps (typically from 5-10 ACTIVE → 20-100 total with historical INACTIVE)
4. Verify `pages.full_history_complete=true`, `pages.last_full_scrape_at` updated
5. Visit `/advertiser/<page_id>` — all tabs populate with correct counts

## Sign-off
Once V1-V10 pass: project is shipped. Move Phase 5 (CLI, real-time sync, multi-industry) to a new planning cycle (`.planning/swipe-dashboard-v2/`).
