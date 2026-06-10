# Meta Ad Library Schema — ScrapeCreators → Swipe File JSON

Reference for mapping `GET /v1/facebook/adLibrary/company/ads` response → `swipe-files/schema/ad.schema.json`.

Verified 2026-04-19 against `https://docs.scrapecreators.com/openapi.json` + live test call on page `100852962092831` (Delvin Goh, SG property).

---

## Endpoint

`GET https://api.scrapecreators.com/v1/facebook/adLibrary/company/ads`

Auth: `x-api-key` header (loaded from `.env` → `SCRAPECREATORS_API_KEY` by `skills/scrapecreators/scripts/api.py`).

### Query params (after Phase A wrapper fix)

| Param | Required | Notes |
|---|---|---|
| `pageId` | one of | The companies ad library page id. From FB Ad Library URL `view_all_page_id` query param. |
| `companyName` | one of | Alternative to `pageId`. |
| `country` | no | 2-letter code, e.g. `SG`. Defaults to ALL. |
| `status` | no | `ACTIVE` (default per Q&A) / `INACTIVE` / `ALL`. |
| `media_type` | no | `ALL` (default) / `VIDEO` / `IMAGE` / `MEME` (image+text). |
| `language` | no | 2-letter, e.g. `EN`. |
| `sort_by` | no | impressions (default) / `relevancy_monthly_grouped` (most recent). |
| `start_date` / `end_date` | no | YYYY-MM-DD impressions window. |
| `cursor` | no | Pagination — pass back `r["cursor"]` from previous response. |
| `trim` | no | `true` for trimmed response. |

### Wrapper signature

```python
from api import ScrapeCreatorsClient
c = ScrapeCreatorsClient()
r = c.facebook_company_ads(
    page_id="100852962092831",
    country="SG",
    status="ACTIVE",
)
```

**Bug history:** wrapper originally sent `company` as the param name → 400 errors. Fixed in `skills/scrapecreators/scripts/api.py` 2026-04-19. See `skills/scrapecreators/corrections.md`.

---

## Response shape

```jsonc
{
  "success": true,
  "credits_remaining": 2,
  "results": [ /* array of ads */ ],
  "searchResultsCount": 4,
  "cursor": ""        // empty when no more pages
}
```

### Per-ad object — top-level keys

| Field | Type | → swipe-file path |
|---|---|---|
| `ad_archive_id` | str | `ad_archive_id` |
| `page_id` | str | `page_id` |
| `page_name` | str | `page_name` |
| `is_active` | bool | `run.is_active` |
| `start_date` | int (unix s) | `run.first_seen_date` (convert YYYY-MM-DD) |
| `end_date` | int (unix s) | `run.last_seen_date` (convert YYYY-MM-DD) |
| `publisher_platform` | list[str] | `creative.publisher_platform` |
| `targeted_or_reached_countries` | list[str] | `targeting_hints.countries` |
| `total_active_time` | int | **NULL for SG** (EU/political only) |
| `spend` | obj | **NULL for SG** |
| `reach_estimate` | obj | **NULL for SG** |
| `currency` | str | optional |
| `snapshot` | obj | see below |

`days_running` = `(end_date - start_date) // 86400`. Compute manually since `total_active_time` is null for SG.

### `snapshot.*` — the actual creative

| Field | Type | → swipe-file path |
|---|---|---|
| `body.text` | str | `copy.primary_text` |
| `title` | str | `copy.headline` |
| `link_description` | str | `copy.description` |
| `cta_text` | str | `copy.cta_button_text` |
| `cta_type` | str (e.g. `LEARN_MORE`) | `copy.cta_type` |
| `link_url` | str | `copy.cta_link` |
| `caption` | str (e.g. `fb.me`) | `copy.caption` |
| `display_format` | str (`VIDEO`/`IMAGE`) | `creative.format` + derive `creative.media_type` |
| `videos[].video_hd_url` | str | `creative.asset_remote_url` (download → `asset_local_path`) |
| `videos[].video_sd_url` | str | fallback if HD fails |
| `videos[].video_preview_image_url` | str | thumbnail |
| `images[].original_image_url` | str | for image ads |
| `page_profile_uri` | str | page meta |
| `page_profile_picture_url` | str | page meta |
| `page_categories` | list[str] | `targeting_hints.page_categories` + `page.page_categories` |
| `page_like_count` | int | `page.page_like_count` |
| `cards` | list | carousel slides |

### Media-type derivation

```python
fmt = ad["snapshot"].get("display_format", "").upper()
if fmt == "VIDEO": media_type = "video"
elif fmt == "IMAGE": media_type = "image"
elif ad["snapshot"].get("cards"): media_type = "carousel"
else: media_type = "unknown"
```

---

## Pagination

Loop: `while r.get("cursor"):` re-call with `cursor=r["cursor"]`. Each call = 1 credit.

## Costs

1 credit per page request. With 11 pages × ~2 pages-of-ads (estimate), expect ~22 credits per full `property-sg` scrape. Verify in Phase F first run.

## Known gaps (SG-specific)

- `spend`, `reach_estimate`, `total_active_time` always null. Schwartz analysis cannot rely on impressions/spend — must use `days_running` as the proxy for "winners."
- `targeted_or_reached_countries` available but not granular demo (age/gender hidden outside EU).

## Related endpoints (for reference, not used by this skill yet)

- `GET /v1/facebook/adLibrary/ad?ad_id=...` — single ad lookup. Used to resolve ad-only URLs (page #2 in `property-sg/pages-to-scrape.md`).
- `GET /v1/facebook/adLibrary/search/companies?query=...` — find page IDs by company name.
- `GET /v1/facebook/adLibrary/search/ads?query=...` — keyword search across all ads.
