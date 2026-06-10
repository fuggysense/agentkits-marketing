# ad-library-scraper — Learnings

## Confirmed Patterns
- Verified 2026-04-19: `GET /v1/facebook/adLibrary/company/ads?pageId=<id>&country=SG&status=ACTIVE` returns `{success, credits_remaining, results[], searchResultsCount, cursor}`. `snapshot` carries body/title/cta/videos/images. 1 credit per page request.
- For SG ads, `spend` / `reach_estimate` / `total_active_time` are always null (Meta only exposes for EU/political). Use `(end_date - start_date) / 86400` as `days_running`, and use that as the proxy for "winning" ads.

## Mistakes Not to Repeat
- `skills/scrapecreators` `facebook_company_ads()` originally sent param `company` → 400. Always send `pageId` or `companyName`. (Wrapper fixed; see `skills/scrapecreators/corrections.md`.)
- Don't trust handover labels for page names — verify via the live `page_name` field on first scrape. Page #1 in `property-sg/pages-to-scrape.md` was labelled "Damien Tan Properties" but the API returned "Delvin Goh".

## Open Questions
- Does `cursor` reliably empty when results exhausted, or do we need a max-pages safety cap? Verify in Phase F.
- L2 enrichment cost — how often does `transcribe` succeed on Meta CDN URLs (signed, expire fast)? Will we need to download to a local cache first?
- Tesseract install on this machine — confirm `pytesseract` works before Phase D ships.
