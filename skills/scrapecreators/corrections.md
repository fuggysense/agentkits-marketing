# scrapecreators — Corrections Log

- 260419 | facebook_company_ads(company=...) sent param `company` → API rejects with 400; correct param is `pageId` (digits) or `companyName`. Fixed wrapper to accept page_id, company_name, country, status, media_type, language, sort_by, start_date, end_date, cursor, trim. CLI scrape.py also updated. | discovered while building ad-library-scraper skill, verified against https://docs.scrapecreators.com/openapi.json
