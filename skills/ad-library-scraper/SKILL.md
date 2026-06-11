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

## Proven-winner curation defaults (Ferres Path A)

The scrape pulls every active ad on a page, but the swipe file is only worth modelling if it surfaces the *proven* winners. Apply Ferres' Path A filters as the DEFAULT view whenever a human or a downstream skill reads the pool (`_shared-knowledge/ferres/06-statics-playbook.md` §5 Path A; `patterns/statics-pattern-library.md` §build-stack). Long run-time is the closest thing the Ad Library gives to a "this works" stamp — there is no impression sort, so duration stands in for spend-backed proof.

Default filter set (override only with a stated reason):
- **Media type: image OR video still live** — `creative.media_type IN ('image','video')` AND `is_active = 1`. A dead ad proves nothing.
- **30+ days running** — `run.days_running >= 30`. This already matches the L2-enrichment trigger (Phase 3 enriches `days_running > 30`), so the curated view and the enriched view line up.
- **Sort by longest-running, descending** — `ORDER BY run.days_running DESC`. The top of this list is the model-first set; the multi-year runners (Liquid Death's comment-style at 2,037 days, King Kong's native at 1,184) are near-certain profit.

SQL shape against the Ghost pool (read-only):
```sql
SELECT page_id, ad_archive_id, media_type, days_running, primary_text, headline
FROM ads
WHERE industry_slug = '<industry>' AND is_active = true AND days_running >= 30
  AND media_type IN ('IMAGE','VIDEO')
ORDER BY days_running DESC;
```

This is curation, not a scrape filter — the scrape still stores everything (so duration can keep accruing run-by-run). The filters apply at read/model time. `stage-analysis.md` Phase 6 "Winners by duration (top 10)" already honours this ordering; the defaults above make it the standard lens for `source-of-truth` and `ad-concept-engine` reads too.

## Pattern-naming discipline (11 named static patterns)

When a saved STATIC ad clearly matches one of the named patterns in `_shared-knowledge/ferres/patterns/statics-pattern-library.md`, tag it with the pattern name so downstream skills can model by recipe, not just by lane. The pattern names are a finer split UNDER the five canonical lanes (PRODUCT-SHOT · SOCIAL-PROOF · INFOGRAPHIC · NATIVE · TABLOID) — record both.

| # | Pattern name | Lane | One-line tell |
|---|---|---|---|
| 01 | Product-Shot + Big Promise | PRODUCT-SHOT | product fills frame, the big text is an outcome promise/number, not the product name |
| 02 | Hard Offer / Red-Hot-Deal | PRODUCT-SHOT | the discount/offer figure IS the creative |
| 03 | Social-Proof Quote + Face | SOCIAL-PROOF | real-feeling customer face + verbatim quote, no separate headline |
| 04 | Verified Review / Comment Card | SOCIAL-PROOF | star-rated review widget or FB comment embedded as found content |
| 05 | Educational / Annotated Infographic | INFOGRAPHIC | labelled how-it-works, stat, or leader-line benefit diagram |
| 06 | Us-vs-Them Comparison | INFOGRAPHIC | split frame, OUR side vs THEIR side |
| 07 | Native Article-Thumbnail Advertorial | NATIVE | reads as an editorial article thumbnail, zero ad-signals on the image |
| 08 | Breaking-News / Tabloid | TABLOID | odd primary image + red-circle inset + news-style headline bar |
| 09 | Native-Organic: Notes / Handwritten / UI-Mimic | NATIVE | sticky note, fake iOS alert, fake X thread — copy IS the ad |
| 10 | Before / After Transformation | SOCIAL-PROOF / INFOGRAPHIC | split-screen timeline (Week 0 / Week 4) |
| 11 | Pattern-Interrupt Oddballs | (varies, STAND-OUT) | wanted poster, ugly-pain close-up, surreal-AI, meme, apology, listicle cover, spokesperson, UGC selfie, quiz, countdown |

Tagging rules:
- Only tag where the match is clear — a forced tag is worse than no tag. If an ad fits none, leave the pattern field empty (it is still a valid swipe).
- Pattern 11 is a tail of single-trick formats; record the specific sub-name in a note (e.g. `pattern: 11 / wanted-poster`) rather than just "11".
- Tags belong in the per-ad JSON (`enrichment` block) so `ghost-sync.py` carries them into the Ghost classification rows. Do not invent a new top-level schema field without updating `swipe-files/schema/ad.schema.json` first — flagged here, not changed in this pass.
- These 11 patterns are for STATICS. Video ads keep lane + format tags from the existing L3 classifier; the named-pattern library does not apply to video.

---

## Canonical store: Ghost Postgres (the SQLite is a transient build artifact)

`swipe-files/<industry>/ads-db.sqlite` **no longer exists on disk** — it is regenerated on demand by `scripts/ad_library/rebuild_ads_db.py` (Phase 5) from the per-ad JSON files, then consumed by `scripts/ghost-sync.py` and discarded. **The canonical store is Ghost Postgres** (`GHOST_DATABASE_URL`, accessed via `mcp__ghost__ghost_sql` with `id: "swipe-ads"`). The SQLite is a flat intermediate, not the source of truth.

Source-of-truth hierarchy (most → least canonical):
1. **Ghost Postgres** — the live, queryable, embedding-backed store. Query here for any read.
2. **Per-ad JSON** (`swipe-files/<industry>/pages/<page_id>/ads/<ad_id>.json`) — the durable on-disk record; what `rebuild_ads_db.py` walks. These are the regeneration seed.
3. **`ads-db.sqlite`** — transient. Built from (2), synced into (1), then expendable.

Regeneration path (if SQLite or Ghost rows are missing or stale):
```bash
# Rebuild the transient SQLite from the durable per-ad JSON files
python3 scripts/ad_library/rebuild_ads_db.py --industry <industry>
# Sync the rebuilt SQLite into Ghost Postgres (canonical)
python3 scripts/ghost-sync.py <industry>
```
The first command is local-only (no network). The second writes to Ghost — that IS the canonical write, gated by normal data-reliability rules. Earlier doc text that called the SQLite "canonical source" is superseded by this note.

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
| `swipe-files/<industry>/ads-db.sqlite` | Transient build artifact — rebuilt from per-ad JSON, synced into Ghost Postgres (canonical), then expendable. See §"Canonical store". |
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

- [[scrapecreators]] (skill, 0.22)
- [[feedback-router]] (skill, 0.21)
- [[meta-ads-uploader]] (skill, 0.20)
- [[source-of-truth]] (skill, 0.18)
- [[onboarding-strategy-pdf]] (skill, 0.18)

<!-- skill-graph:end -->
