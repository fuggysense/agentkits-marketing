---
description: Scrape Meta Ad Library for an industry, enrich winners, draft Schwartz stage analysis, rebuild SQLite swipe-file DB
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: <industry> [--analyze-only | --no-enrich | --dry-run | --page <page_id>]
---

## Purpose

Pull every active Meta ad for the pages tracked in `swipe-files/<industry>/pages-to-scrape.md`, enrich the winners (>30 days running), classify with Nemotron, rebuild the queryable SQLite layer, and draft a Schwartz 5-stage market sophistication brief for HITL approval.

Output: `swipe-files/<industry>/ads-db.sqlite` + `stage-analysis.md` + per-ad JSON files.

## Input

`$ARGUMENTS` — industry slug (e.g. `property-sg`). Must match a directory in `swipe-files/`.

Optional flags:
- `--analyze-only` — skip scrape + enrich, just regenerate `stage-analysis.md` from existing SQLite
- `--no-enrich` — L1 only (skip transcripts/OCR/classifier)
- `--dry-run` — fetch + parse but don't write files
- `--page <page_id>` — restrict to a single page (debugging)

## Prerequisites

- [ ] `SCRAPECREATORS_API_KEY` in `.env`
- [ ] `swipe-files/<industry>/pages-to-scrape.md` exists with at least one page ID
- [ ] (For L2) `transcribe` skill available + `pytesseract` installed
- [ ] (For L3) `KILO_API_KEY` in `.env` for `scripts/research-llm.sh kilo`

## Execution

Invoke the `ad-library-scraper` skill. The skill runs Phases 0–7:

0. Load `pages-to-scrape.md` → page IDs
1. L1 scrape via `facebook_company_ads(page_id=..., country=..., status="ACTIVE")` (paginate via `cursor`)
2. dev-browser fallback on miss → log to `pages/<id>/scrape-log.jsonl`
3. L2 enrich ads where `days_running > 30` (transcribe video / OCR image)
4. L3 classify with Kilo → Nemotron 3 Super
5. Rebuild `ads-db.sqlite`
6. Auto-draft `stage-analysis.md` → HITL approve before commit
7. Report run summary + append to `swipe-files/<industry>/_index.md` scrape log

## Output

```
swipe-files/<industry>/
├── pages/<page_id>/
│   ├── meta.json
│   ├── ads/<ad_id>.json (+ optional -transcript.txt / -image-ocr.txt / assets/)
│   └── scrape-log.jsonl
├── ads-db.sqlite                   ← rebuilt every run
└── stage-analysis.md               ← HITL gate
```

## Cost estimate

~1 ScrapeCreators credit per page-of-results (paginated). 11-page property-sg full scrape ≈ 15–25 credits. L2 enrichment burns local CPU + Kilo credits proportional to `count(ads where days_running > 30)`.

## See also

- Skill: `skills/ad-library-scraper/SKILL.md`
- Schema mapping: `skills/ad-library-scraper/references/meta-ad-library-schema.md`
- Build plan: `~/.claude/plans/started-prancy-origami.md`
