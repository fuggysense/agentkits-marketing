---
name: ad-library-scraper
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: paid-media
difficulty: intermediate
description: "Build industry-level Meta Ad Library swipe-file database + Schwartz 5-stage market brief. One scrape per industry, reusable for all clients. Triggers: scrape ad library, competitor ads database, market sophistication, blue ocean angles, winners by duration, industry ad pool, stage analysis."
triggers:
  - scrape ad library
  - meta ad library scrape
  - competitor ads database
  - swipe file refresh
  - schwartz stage analysis
  - market sophistication
  - industry ad pool
  - winners by duration
  - blue ocean angles
  - blue boxes
  - mechanism inventory
  - ads-db
  - stage-analysis
prerequisites:
  - scrapecreators
related_skills:
  - scrapecreators
  - source-of-truth
  - avatar-research
  - ad-concept-engine
  - paid-media-audit
  - feedback-router
  - transcribe
agents:
  - researcher
  - attraction-specialist
mcp_integrations:
  optional:
    - kilo-gateway
success_metrics:
  - pages_scraped_vs_targeted
  - new_ads_per_run
  - l2_enrichment_rate
  - stage_analysis_hitl_approval
---

## Graph Links
- **Reads from:** [[scrapecreators]] (Meta Ad Library endpoint), [[transcribe]] (video → text), [[dev-browser]] (fallback)
- **Writes to:** `swipe-files/<industry>/` (canonical industry pool)
- **Feeds into:** [[source-of-truth]] Phase 0.5, [[ad-concept-engine]] Phase 0.5, [[paid-media-audit]], [[feedback-router]]
- **Classifier:** Kilo gateway → Nemotron 3 Super (`scripts/research-llm.sh kilo "..." --model "nvidia/nemotron-3-super"`)

---

## When to Use

| Intent | Command |
|---|---|
| Build / refresh a full industry swipe pool | `/ads:scrape-library <industry>` |
| Add / refresh a single competitor page | `/ads:scrape-advertiser <page_id> <industry>` |
| Just regenerate the Schwartz brief | `/ads:scrape-library <industry> --analyze-only` |
| Dry-run one page (verify before full scrape) | `/ads:scrape-library <industry> --page <page_id> --dry-run` |
| Skip L2 enrichment this run (L1 only) | `/ads:scrape-library <industry> --no-enrich` |
| Query the DB from a Claude session | `mcp__ghost__ghost_sql` with `id: "swipe-ads"` — see `references/agent-query-cookbook.md` |

Industries scaffolded: see `swipe-files/_index.md`. First active industry: `property-sg`.

## When NOT to Use

- **Per-client competitors** that aren't industry-wide → keep in `clients/<slug>/swipe-file-buyers.md`.
- **Single-ad lookup** → use `scrapecreators` directly (`facebook_ad`).
- **Live-account audit of YOUR ads** → use `paid-media-audit`.

---

## Pipeline (7 phases)

### Phase 0 — Load inputs
Read `swipe-files/<industry>/pages-to-scrape.md`. Parse page IDs (digits) + ad-only URLs (resolve via `/v1/facebook/adLibrary/ad?ad_id=...` to get the page).

### Phase 1 — L1 scrape
For each page: `c.facebook_company_ads(page_id=..., country=..., status="ACTIVE")`. Paginate via `cursor` until exhausted. Per ad:
- Compute `days_running = (end_date - start_date) / 86400` (unix ts → integer days). Convert to `YYYY-MM-DD`.
- Dedupe vs `swipe-files/<industry>/pages/<page_id>/ads/<ad_archive_id>.json`. If exists: update `run.last_seen_date` + `is_active` only. If new: write full JSON per `swipe-files/schema/ad.schema.json`.
- Update `swipe-files/<industry>/pages/<page_id>/meta.json` per `page.schema.json`.

### Phase 2 — Fallback
On any ScrapeCreators error (4xx/5xx, missing `snapshot`, empty `body.text`), invoke dev-browser per `~/.claude/skills/dev-browser/reference.md`. Capture from the public Ad Library page UI. Append to `pages/<page_id>/scrape-log.jsonl`:
```json
{"ts": "ISO-8601", "page_id": "...", "ad_id": "...", "event": "fallback", "error": "...", "fallback_used": "dev-browser"}
```

### Phase 3 — L2 enrichment (conditional)
For ads where `run.days_running > 30` AND no transcript/OCR sidecar exists:
- **Video** (`creative.media_type == "video"`): download `snapshot.videos[0].video_hd_url` → invoke `transcribe` skill → write `<ad_id>-transcript.txt` + set `enrichment.video_transcript_path`.
- **Image** (`creative.media_type == "image"`): download `snapshot.images[0].original_image_url` → OCR (Tesseract via `pytesseract`) → write `<ad_id>-image-ocr.txt` + set `enrichment.image_ocr_path`.

### Phase 4 — L3 classifier
For L2-enriched ads: bundle `(copy.primary_text + headline + transcript_or_ocr)` → call `scripts/research-llm.sh kilo "<prompt>" --model "nvidia/nemotron-3-super"` → fill `enrichment.detected_*` + `schwartz_*`. Set `classifier_model` + `classified_at`.

### Phase 5 — Rebuild SQLite
Walk `swipe-files/<industry>/pages/*/ads/*.json` → flatten into `ads-db.sqlite`. One row per ad with all `run.*`, `creative.*`, `copy.*`, `enrichment.*` flattened to columns. Indexed on `page_id`, `days_running`, `is_active`, `schwartz_sophistication_stage`.

### Phase 6 — Stage analysis (auto-draft, HITL approve)
Per Q6: after every scrape, draft `stage-analysis.md`. Synthesis prompt to Nemotron over the SQLite data:
- Executive summary — stage assessment + confidence
- Winners by duration (top 10)
- Mechanism inventory + Claim inventory
- Blue boxes (claims ALL competitors make)
- Blue ocean gaps (claims/mechanisms NO competitor makes)
- Strategic recommendation

Display draft inline → HITL gate → on approval, write to `swipe-files/<industry>/stage-analysis.md`.

### Phase 7 — Report
- N pages scraped / N targeted
- N new ads / N updated / N failed
- N L2-enriched (matches `days_running > 30`)
- Path to `stage-analysis.md` + `ads-db.sqlite`
- Append summary row to `swipe-files/<industry>/_index.md` scrape log

---

## Execution recipe (what `/ads:scrape-library <industry>` actually runs)

```bash
INDUSTRY="$1"

# Phase 1+2 — L1 scrape (paginated) with dev-browser fallback logged to scrape-log.jsonl
python3 scripts/ad_library/scrape_meta_ad_library.py --industry "$INDUSTRY"

# Phase 3+4 — L2 transcripts/OCR for ads with days_running > 30, then L3 Nemotron classify
python3 scripts/ad_library/enrich_scraped_ads.py --industry "$INDUSTRY"

# Phase 5 — drop + recreate ads-db.sqlite from JSON files
python3 scripts/ad_library/rebuild_ads_db.py --industry "$INDUSTRY"

# Phase 6 — auto-draft Schwartz brief → swipe-files/<industry>/stage-analysis.draft.md
python3 scripts/ad_library/generate_stage_analysis.py --industry "$INDUSTRY"

# Phase 6 HITL — review the draft, edit, then approve by renaming:
#   mv swipe-files/$INDUSTRY/stage-analysis.draft.md swipe-files/$INDUSTRY/stage-analysis.md
```

Flag passthrough:
- `--dry-run` → step 1 only (`scrape_meta_ad_library.py --dry-run`)
- `--no-enrich` → skip steps 2 (and consequently L3)
- `--analyze-only` → run only step 4 (no scrape, no enrich, no rebuild — assumes db exists)
- `--page <id>` → restrict step 1 to one page

## Files this skill writes

| Path | Purpose |
|---|---|
| `swipe-files/<industry>/pages/<page_id>/meta.json` | Page metadata |
| `swipe-files/<industry>/pages/<page_id>/ads/<ad_id>.json` | One ad |
| `swipe-files/<industry>/pages/<page_id>/ads/<ad_id>-transcript.txt` | L2 video |
| `swipe-files/<industry>/pages/<page_id>/ads/<ad_id>-image-ocr.txt` | L2 image |
| `swipe-files/<industry>/pages/<page_id>/ads/assets/<ad_id>.(mp4\|jpg\|png)` | Asset cache |
| `swipe-files/<industry>/pages/<page_id>/scrape-log.jsonl` | Append-only log |
| `swipe-files/<industry>/ads-db.sqlite` | Queryable layer |
| `swipe-files/<industry>/stage-analysis.md` | HITL-approved Schwartz brief |

## Files this skill reads

| Path | Purpose |
|---|---|
| `swipe-files/<industry>/pages-to-scrape.md` | Source URLs |
| `swipe-files/schema/ad.schema.json` + `page.schema.json` | Validation |
| `skills/scrapecreators/scripts/api.py` (`facebook_company_ads`) | API client |
| `skills/transcribe/` | Video transcription |

## Locked decisions

See `~/.claude/plans/started-prancy-origami.md` § "Locked decisions" — Q1–Q10 + Phase A wrapper-fix verification.

## Related downstream skills

- `source-of-truth` Phase 0.5 reads `stage-analysis.md` before fresh competitor research.
- `ad-concept-engine` Phase 0.5 loads industry stage analysis on top of per-client swipe files.
- `paid-media-audit` cross-references client ads against the industry pool.
- `feedback-router` scans the pool for post-wave pattern drift.

## See also
- Original handover: `~/.claude/plans/ad-library-scraper-handover.md`
- Build plan + decisions: `~/.claude/plans/started-prancy-origami.md`
- Endpoint schema mapping: `references/meta-ad-library-schema.md`

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[onboarding-strategy-pdf]] (skill, 0.09)
- [[scrapecreators]] (skill, 0.08)
- [[source-of-truth]] (skill, 0.07)
- [[feedback-router]] (skill, 0.07)
- [[sheets-updater]] (skill, 0.06)

<!-- skill-graph:end -->
