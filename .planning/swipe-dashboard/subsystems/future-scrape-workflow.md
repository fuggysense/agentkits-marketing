# Subsystem — Future Scrape Workflow (ad_archive_id as the traceability thread)

Once this system ships, every scrape follows a single pattern. This doc walks through what happens from the user's command to the dashboard showing new ads, with `ad_archive_id` as the primary key stamped on every artifact along the way.

## The traceability principle

**Every artifact that represents or derives from an ad must be tagged with its `ad_archive_id`.** Filenames, sidecar headers, DB rows, Netlify Blobs keys, classification records, embeddings, transcript headers — all carry the same ID. Any agent can trace any piece of data back to the source ad with one query.

ScrapeCreators / Meta's `ad_archive_id` is an opaque 15-16 digit number like `1234567890123456`. It's globally unique across Meta Ad Library and permanent once assigned. We use it verbatim — no re-keying, no hashing, no surrogate keys.

## Three scrape flows

### Flow A — Weekly shallow refresh of an existing industry

```
User: /ads:scrape-library property-sg
```

**What happens (in order):**

1. **Phase 1 — L1 scrape**
   Reads `swipe-files/property-sg/pages-to-scrape.md` → 10 page_ids
   For each page: `c.facebook_company_ads(page_id=..., status='ACTIVE')` paginated
   Per ad returned from API:
   - Extract `ad_archive_id` (the thread we tag everything with)
   - Dedupe vs existing `swipe-files/property-sg/pages/<page_id>/ads/<ad_archive_id>.json`
   - If exists: update `run.last_seen_date` + `is_active` → same filename, same ID
   - If new: write full JSON to `swipe-files/property-sg/pages/<page_id>/ads/<ad_archive_id>.json`
   - Append to `swipe-files/property-sg/pages/<page_id>/scrape-log.jsonl` with `ad_archive_id`

2. **Phase 2 — disappearance detection (NEW)**
   Compare `previously_active` (Ghost `SELECT ad_archive_id FROM ads WHERE industry_slug='property-sg' AND status='ACTIVE'`) vs `currently_seen_active` (set of ad_archive_ids returned this scrape)
   `newly_stopped = previously_active - currently_seen_active`
   These ads disappeared → they just stopped running. Will be marked `status=INACTIVE, stopped_date=today` during ghost-sync.

3. **Phase 3 — L2 enrichment (only for winners + new winners)**
   For each ad where `days_running > 30` AND no transcript sidecar exists:
   - Video: download `snapshot.videos[0].video_hd_url` to `pages/<page_id>/ads/assets/<ad_archive_id>.mp4`
   - Call `transcribe` skill with Groq: `transcribe(assets/<ad_archive_id>.mp4, provider='groq', model='groq/whisper-large-v3')`
   - Write `pages/<page_id>/ads/<ad_archive_id>-transcript.txt` with sidecar header (format below)
   - Image: download → `assets/<ad_archive_id>.jpg` → Tesseract OCR → `<ad_archive_id>-image-ocr.txt`

4. **Phase 4 — L3 classifier (Nemotron)**
   For each L2-enriched ad: bundle `(ad_archive_id, headline, body, transcript_or_ocr)` → Nemotron → classifications.
   Output file: `pages/<page_id>/ads/<ad_archive_id>.json` (existing JSON gets `enrichment.*` + `schwartz_*` keys added — still keyed on ad_archive_id via filename)

5. **Phase 5 — Rebuild SQLite**
   Walk `swipe-files/property-sg/pages/*/ads/*.json` → flatten to `ads-db.sqlite`. `ad_archive_id` is the primary key. Every row traces.

6. **Phase 6 — Auto-draft Schwartz brief** (HITL-approved)
   Nemotron synthesis over the SQLite data → `stage-analysis.draft.md`. Cites specific ad_archive_ids in "winners by duration" and "mechanism inventory" sections.

7. **Phase 7 — Ghost sync (NEW — auto-appended after Phase 6)**
   `python scripts/ghost-sync.py property-sg`
   See `subsystems/scraper-sync.md` for the pseudocode. Net effect:
   - Upsert `pages` rows
   - Upsert `ads` rows (keyed on ad_archive_id, preserves temporal fields)
   - UPDATE ads SET status='INACTIVE', stopped_date=CURRENT_DATE WHERE ad_archive_id IN newly_stopped
   - Upload each `assets/<ad_archive_id>.(mp4|jpg)` → Netlify Blobs with key `swipe-ads/<industry>/<ad_archive_id>.<ext>` → store signed URL in `ads.asset_url`
   - Upsert `transcripts` rows (ad_archive_id FK + provider + audio_hash from sidecar header)
   - Upsert `classifications` rows (ad_archive_id FK + Nemotron output)
   - Run embeddings pass — for each ad needing one, compute embedding, upsert `ad_embeddings(ad_archive_id, provider=...)` 
   - Append `scrape_runs` row
   - Rewrite `_agent_readme` content with fresh stats

8. **Dashboard visibility**
   Next page load fetches from Ghost. New ads appear in the grid. `v_new_this_week` shows this scrape's additions. Any "stopped" ads now have the `recently_stopped` lifecycle badge on the card.

### Flow B — New industry bootstrap

```
User: Let's onboard fitness-sg. Here are 15 gym/fitness pages to watch.
Claude: /ads:scrape-library fitness-sg  (first-time)
```

**What's different from Flow A:**

1. **Pre-Phase:** Scaffold `swipe-files/fitness-sg/` with:
   - `pages-to-scrape.md` (user-provided list)
   - `_index.md` (registry entry)
   - `schema/` symlinks to the global ad/page schemas
2. Ghost `INSERT INTO industries (slug, name, emoji, ...) VALUES ('fitness-sg', 'Fitness — Singapore', '🏋', ...)` on first ghost-sync
3. Phase 6 Schwartz brief runs on FRESH data (no prior stage-analysis.md) → full 5-stage analysis, HITL approval
4. Every ad carries the new `industry_slug='fitness-sg'` tag; queries filter by industry when needed
5. Dashboard industry picker now shows 2 options (property-sg, fitness-sg)

`ad_archive_id` remains globally unique across industries — a single ad_archive_id cannot appear in two industries (each Meta ad has one page, each page belongs to one industry per our mapping). If a page later moves industry, we update `pages.industry_slug` and cascade; the ad's ID stays put.

### Flow C — Per-advertiser deep backfill (historical library)

```
User: Show me Delvin Goh's entire ad history, not just active ads.
Claude: /ads:scrape-advertiser 1234567890 --depth full
```

Or via dashboard UI: click `[Run full-history backfill]` on the `/advertiser/<page_id>` page.

**What's different:**

1. Single page scope (not industry-wide)
2. ScrapeCreators call: `c.facebook_company_ads(page_id=..., status='ALL', cursor=...)` — returns ACTIVE + INACTIVE, paginated until cursor empty
3. For INACTIVE ads returned by Meta:
   - `ads.status='INACTIVE'`
   - `ads.stopped_date = payload['end_date']` (Meta's authoritative date, not our inferred scrape date)
   - `ads.start_date = payload['start_date']`
4. L2 enrichment runs same as before — winners get transcripts regardless of active/inactive status
5. After sync: `pages.full_history_complete=true`, `pages.last_full_scrape_at = now()`
6. Dashboard `/advertiser/<page_id>` now shows all tabs populated (All / Active / Stopped / Winners)

**Cost signal:** a deep scrape on a big advertiser (100+ historical ads) might run 50+ ScrapeCreators credits + embedding compute + transcription. The `[Run full-history backfill]` button should display estimated credits before firing.

## ad_archive_id tagging in every artifact

### Filesystem (canonical, git-tracked)

| Path pattern | ad_archive_id location |
|---|---|
| `swipe-files/<industry>/pages/<page_id>/ads/<ad_archive_id>.json` | filename stem |
| `swipe-files/<industry>/pages/<page_id>/ads/<ad_archive_id>-transcript.txt` | filename prefix + sidecar header |
| `swipe-files/<industry>/pages/<page_id>/ads/<ad_archive_id>-image-ocr.txt` | filename prefix + sidecar header |
| `swipe-files/<industry>/pages/<page_id>/ads/assets/<ad_archive_id>.mp4` | filename stem |
| `swipe-files/<industry>/pages/<page_id>/ads/assets/<ad_archive_id>.jpg` | filename stem |
| `swipe-files/<industry>/pages/<page_id>/scrape-log.jsonl` | one line per event carries `ad_archive_id` field |
| `swipe-files/<industry>/ads-db.sqlite` | PRIMARY KEY on `ad_archive_id` |
| `swipe-files/<industry>/stage-analysis.md` | cites ad_archive_ids inline in winners list |

### Sidecar headers (make every file self-describing)

Every transcript/OCR sidecar file starts with a YAML-ish comment block:

```
# ad_archive_id: 1234567890123456
# page_id: 987654321
# industry: property-sg
# provider: groq:whisper-large-v3
# audio_hash: sha256-abc123def456...
# duration_sec: 47.2
# transcribed_at: 2026-04-20T09:42:13+08:00
# source_asset: assets/1234567890123456.mp4

[full transcript text begins here]
```

If someone finds a stray transcript file 6 months from now, they can identify exactly which ad it belongs to without grepping the DB.

Same pattern for OCR output:
```
# ad_archive_id: 1234567890123456
# page_id: 987654321
# industry: property-sg
# ocr_engine: tesseract-5.3
# source_asset: assets/1234567890123456.jpg
# ocr_at: 2026-04-20T09:42:45+08:00

[OCR text begins here]
```

### Ghost Postgres (queryable mirror)

Every table has `ad_archive_id` as PK or FK:

| Table | ad_archive_id role |
|---|---|
| `ads` | PRIMARY KEY |
| `transcripts` | PRIMARY KEY, FK to ads |
| `classifications` | PRIMARY KEY, FK to ads |
| `ad_embeddings` | part of composite PRIMARY KEY (ad_archive_id, provider), FK to ads |
| `scrape_runs` | no direct FK (industry-scoped) — but `scrape_runs.ads_found` count + JSONB array of touched ad_archive_ids |
| `_agent_readme` | no FK (singleton) — but stats snapshot cites counts per industry |

Every view joins on `ad_archive_id`. Every agent query can filter, group, or follow the ID.

### Netlify Blobs (asset storage)

Blob key pattern: `swipe-ads/<industry>/<ad_archive_id>.<ext>`

Example: `swipe-ads/property-sg/1234567890123456.mp4`

Result: asset URL in `ads.asset_url` is directly readable — you can tell which ad it belongs to from the URL alone. Deletion, migration, and auditing are trivial.

### Dashboard UI (visible to the user)

Every ad card shows the ad_archive_id in a subtle monospace corner tag (hover-reveal or always-visible small chip). The drawer explicitly shows:
- ad_archive_id: `1234567890123456` (monospace)
- Meta Ad Library URL: `https://www.facebook.com/ads/library/?id=1234567890123456` (clickable)
- Copy-link button: copies the Meta URL with the ID embedded

### Logs + errors

Every log line, every error row in `scrape_runs.error_text`, every Postgres NOTICE should include the relevant `ad_archive_id` when applicable:

```
2026-04-20 09:42:13 INFO  scraped ad=1234567890123456 page=987654321 days_running=47
2026-04-20 09:42:18 ERROR transcription failed ad=1234567890123456 reason="audio decode error"
2026-04-20 09:42:22 INFO  embedded ad=1234567890123456 provider=ollama native_dim=768 truncated_to=1024
```

## Agent trace example (how to use the tagging)

> "Why does ad 1234567890123456 have no transcript?"

Single-ID trace using Ghost MCP:

```sql
-- Step 1: is it in ads at all?
SELECT ad_archive_id, status, format, run_duration_days, lifecycle_stage
FROM ads
WHERE ad_archive_id = '1234567890123456';
-- → row returned, format=VIDEO, run_duration_days=18

-- Step 2: is it a winner (only winners get transcripts)?
SELECT is_winner FROM ads WHERE ad_archive_id = '1234567890123456';
-- → false (only 18 days, threshold is 30)

-- Answer: "Not transcribed because it hasn't run long enough yet. Will be L2-enriched once days_running > 30."
```

Or: "Why are Delvin Goh's ads missing classifications?"

```sql
SELECT a.ad_archive_id, a.headline, c.ad_archive_id IS NOT NULL AS has_classification
FROM ads a
LEFT JOIN classifications c USING (ad_archive_id)
WHERE a.page_id = '987654321'
ORDER BY a.ad_archive_id;
-- → 12 of 47 missing — these are the ones where days_running < 30 (not yet enriched)
```

## Common pitfalls to avoid

1. **Don't hash or re-key ad_archive_id.** Use verbatim as it comes from ScrapeCreators. Anything else breaks cross-reference to Meta Ad Library.
2. **Don't embed ad_archive_id in asset filenames as a truncated or transformed string.** Full ID always.
3. **Don't collapse across pages.** A single `ad_archive_id` maps to exactly one `page_id` (Meta guarantee). If two scrapes disagree on page_id, something is broken.
4. **Don't let a transcript land without the header comment block.** An unheadered transcript is an orphan and will be ignored by ghost-sync.
5. **Don't use surrogate keys in Ghost.** Don't add a `BIGSERIAL id` to `ads`. `ad_archive_id` IS the key.

## Verification touchpoint

Added to `verification.md` V9 check:
> Random-sample a filesystem artifact (a transcript file, an asset mp4, a classification JSON) and verify the embedded ad_archive_id matches the filename and the Ghost DB row.

## What the user actually sees in the terminal (next scrape)

```
$ /ads:scrape-library property-sg

▸ Phase 1: L1 scrape (10 pages)
  page=Delvin_Goh    ads_active=12  new=3  updated=9
  page=Property_Matters  ads_active=8  new=1  updated=7
  ...
  Total: 60 active ads across 10 pages (61 total, 1 new since last scrape)

▸ Phase 2: Disappearance detection
  Previously active but not in this scrape: 2 ads
    ad=1111111111111111 last_seen=2026-04-13 → marking INACTIVE
    ad=2222222222222222 last_seen=2026-04-13 → marking INACTIVE

▸ Phase 3: L2 enrichment (winners only, days_running > 30)
  ad=3333333333333333 format=VIDEO → groq transcribe (0.42s) → transcript written
  ad=4444444444444444 format=VIDEO → groq transcribe (0.38s) → transcript written
  ad=5555555555555555 format=IMAGE → tesseract OCR → ocr text written
  ...
  8 winners enriched

▸ Phase 4: L3 Nemotron classification
  8 ads classified (schwartz_stage, angle, avatar_fit, blue_box_category)

▸ Phase 5: SQLite rebuild
  ads-db.sqlite: 61 ads (up from 60)

▸ Phase 6: Schwartz stage-analysis draft
  stage-analysis.draft.md written → review + approve by renaming to stage-analysis.md

▸ Phase 7: Ghost sync
  Industries upserted: 1
  Pages upserted: 10
  Ads upserted: 61 (1 new, 2 newly-stopped)
  Assets uploaded to Netlify Blobs: 3 new
  Transcripts upserted: 2 new (groq:whisper-large-v3)
  Classifications upserted: 8
  Embeddings upserted: 3 (ollama/nomic-embed-text, input_hash unchanged for 58)
  _agent_readme refreshed

✓ Scrape complete. Dashboard will reflect changes on next load.
  New ads (3): 1234567890123456, 2345678901234567, 3456789012345678
  Newly stopped (2): 1111111111111111, 2222222222222222
  Winners that stopped (creative fatigue): 1111111111111111 (ran 47 days)
```

Everything traceable. Every artifact tagged. Agents can answer "what happened to ad X" with a single query.
