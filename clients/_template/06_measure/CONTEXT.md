# 06_measure — Analytics And Feedback Loop Contract

Weekly analytics snapshot that feeds back into `01_research/` for the next content cycle. This stage closes the loop — scorecards inform what to make next.

## Consumes

- Live platform data (YouTube Studio, Instagram Insights) via browser
- `05_handoff/output/` — promoted deliverables to compare against benchmarks

## Owns

- `output/weekly.md` — weekly performance summary (written narrative)
- `output/scorecard-{platform}-{YYYY-MM-DD}.xlsx` — 5-tab platform scorecard

## Produces

- Insight brief → fed back into `01_research/output/<YYMMDD>-scorecard-findings.md`
- Updated content direction notes → `_brand/learnings.md`

## Skills available for this phase

**`yt-scorecard`** (global) — Analyzes 10 most recent YouTube videos, outputs 5-tab .xlsx: Full Scorecard / Winners / Losers / Key Takeaways / Content Strategy. Browser-driven data collection. Trigger phrases: "youtube scorecard", "yt scorecard", "score my youtube", "youtube analytics report", "which videos performed", "youtube content review".

**`ig-scorecard`** (global) — Analyzes 10 most recent Instagram posts, outputs 5-tab .xlsx with engagement-rate rankings and content strategy recommendations. Browser-driven. Trigger phrases: "instagram scorecard", "ig scorecard", "score my instagram", "ig analytics report", "which posts performed", "instagram content review".

**Supporting skills:**
- `analytics-attribution` — performance measurement, attribution modeling, ROI
- `sheets-updater` — pull Meta Ads metrics into an existing Google Sheet (HITL preview before write)
- `sheets-provisioner` — provision a new Google Sheet with campaign/LP funnel tabs

## Gates fired

- None required. Run scorecard first, then decide if findings trigger a `01_research` revisit.

## Cadence

- Weekly: run scorecard for active platforms, update `output/weekly.md`
- After each campaign: compare scorecard to campaign brief assumptions; promote learnings to `_brand/learnings.md`

## Out of scope

- Paid ads analytics → `analytics-attribution` skill or `sheets-updater`
- New campaign planning → back to `01_research/`
