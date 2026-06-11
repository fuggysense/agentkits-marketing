# 06_measure — Analytics And Feedback Loop Contract

Weekly analytics snapshot that closes the loop: scorecards inform what to make next and feed back into `01_research/`.

## Inputs

- L4 (working): live platform data (YouTube Studio, Instagram Insights) via browser; `05_handoff/output/` promoted deliverables to compare against benchmarks.
- L3 (reference): campaign brief assumptions and `../_brand/learnings.md` (where content-direction updates land).

## Process

Run the platform scorecards weekly, then decide if findings trigger a `01_research` revisit (no gate is required first). The global `yt-scorecard` and `ig-scorecard` skills collect data by browser and output a 5-tab .xlsx (Full Scorecard / Winners / Losers / Takeaways / Strategy). Supporting skills: `analytics-attribution` (measurement, attribution, ROI), `sheets-updater` (pull Meta Ads metrics into an existing sheet, HITL preview), `sheets-provisioner` (provision a new campaign/LP sheet). After each campaign, compare the scorecard to the brief's assumptions. Out of scope: paid-ads analytics (`analytics-attribution` / `sheets-updater`) and new-campaign planning (back to `01_research/`).

## Outputs

- `output/weekly.md` (narrative summary) and `output/scorecard-{platform}-{YYYY-MM-DD}.xlsx` (5-tab).
  - Done: the weekly summary is current, an insight brief is fed back to `01_research/output/<YYMMDD>-scorecard-findings.md`, and content-direction notes are promoted to `../_brand/learnings.md`.
