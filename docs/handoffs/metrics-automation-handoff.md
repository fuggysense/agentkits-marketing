# Metrics Automation — Session Handoff

**Last updated:** 2026-04-16 (Phase 4 complete)
**Status:** Phases 1-4 complete. Cron live. Waiting on first auto-fire at 9am SGT tomorrow.
**Branch:** main

## TL;DR

Templatable Google Sheets automation that pulls daily Meta Ads metrics and writes to per-client dashboards. Tested end-to-end on neezanizam (NND@Propnex account). Next: deploy Modal cron for daily auto-runs.

## Current state — what's already working

### Infrastructure built
- [x] 6 Python scripts at `scripts/modal/` (1,506 lines total, all parse cleanly)
- [x] 2 Pentagon skills: `skills/sheets-provisioner/` + `skills/sheets-updater/`
- [x] Template config at `clients/_template/metrics-config.json`
- [x] Ops agent Soul + Purpose updated with new workflows
- [x] `.gitignore` excludes `credentials.json`

### Credentials configured
- [x] Meta long-lived access token (60 days, expires ~2026-06-15) — saved to `.env` as `META_ADS_ACCESS_TOKEN`
- [x] Meta App ID: `1630630598147290`, App Secret in `.env`
- [x] Google Cloud service account: `neezanizam@neezanizam-492212.iam.gserviceaccount.com`
- [x] Service account JSON at `scripts/modal/credentials.json` (gitignored)
- [x] Google Sheets API + Google Drive API enabled in GCP project "Neezanizam"

### Neezanizam test setup
- [x] Sheet created manually (Drive copy of master template)
- [x] Sheet ID: `1D-HrqZHUzvQVmnYO4hR3f9rnznnIprz0CZu8hmUO610`
- [x] Sheet URL: https://docs.google.com/spreadsheets/d/1D-HrqZHUzvQVmnYO4hR3f9rnznnIprz0CZu8hmUO610/edit
- [x] Shared with service account as Editor
- [x] All 7 tabs cleared of old data + one mock row per tab at row 2
- [x] DAILY CALLS row 2 formulas restored (auto-summarize rows 3:1000)
- [x] Config generated at `clients/neezanizam/metrics-config.json`
- [x] Ad account: `act_837789749619954` (NND@Propnex)

### First real data pull completed
- [x] Pulled 7 days of Asset Progression campaign (ID: 6665612766106)
- [x] Written to DAILY CALLS rows 3-9 (spend $211.84, 6 leads, 2 appts)
- [x] Row 2 formulas auto-calculated summaries from the data
- [x] Snapshot saved: `clients/neezanizam/metrics/test_260416_1811.json`

## Phase 2-4 completed 2026-04-16

- Modal CLI already installed (v1.3.5). Workspace: `fuggysense`.
- Secrets created: `meta-ads` (from .env), `google-sheets` (from credentials.json).
- Deployed: 4 functions (`daily_metrics`, `weekly_aggregation`, `monthly_aggregation`, `run_in_modal`).
- Deploy URL: https://modal.com/apps/fuggysense/main/deployed/marketing-metrics
- Dry-run: 12s end-to-end, no writes. Pipeline verified.
- Live run: row 10 appended to DAILY CALLS (Apr 15 data, account-level NND@Propnex).

### Bugs fixed during Phase 2-4

1. **`config_loader.py` path resolution** — `_CLIENTS_DIR` used `parent.parent.parent` which works locally (`scripts/modal/config_loader.py` → repo root) but broke in Modal where scripts are flattened to `/root/`. Now prefers the `/root/clients` mount when present.

2. **CVR double-percentage bug** — `meta_puller.py:285` and `:330` returned `leads/clicks * 100` (e.g. `4.878`), but the sheet's `%`-formatted cell multiplies by 100 again for display → showed `487.80%`. Removed the `* 100`. Now stores raw ratio (`0.04878`), displays as `4.88%`. Row 10 in Neezanizam sheet manually corrected.

## What's left to do

### Phase 5: Wait for cron (24h)

**Goal:** Daily automated writes at 9am SGT without manual intervention.

Tomorrow at 9am SGT (01:00 UTC), the scheduled function `daily_metrics` fires automatically.

**Where to check:**

1. **Dashboard (easiest):** https://modal.com/apps/fuggysense/main/deployed/marketing-metrics
   Functions tab → `daily_metrics` → shows last run timestamp and next scheduled fire.

2. **CLI:**
   ```bash
   # See when cron last fired and what it output
   modal app history marketing-metrics | head -20
   modal app logs marketing-metrics              # live tail
   modal container list                          # any running right now?
   ```

**What to look for in logs:**
- `daily_metrics` invocation around 01:00 UTC
- Output: `{clients_processed: 1, successes: ["neezanizam"], failures: []}`
- New row in DAILY CALLS for today's date (target_date = yesterday relative to fire time)

### Phase 6: Anomaly detection wiring (optional, ~30 min)

The scripts already compute anomalies. Next step: wire them to alert you.

**Option A — Telegram** (reuse your existing bot):
- In `marketing_metrics.py`, add a `send_telegram_alert()` function
- Call it when anomalies detected

**Option B — Pentagon Ops agent**:
- Modal writes anomalies to `clients/<slug>/metrics/anomalies.log`
- Ops agent polls this log via routine → DMs Strategist

Decide which based on how often you'd want to be pinged.

### Phase 7: Pentagon integration (optional, ~1 hour)

**Only do this after Modal is proven stable for 3+ days.**

1. Add `sheets-updater` skill to Ops agent in Pentagon
2. Test on-demand pull: DM Ops → "pull neezanizam now"
3. Set up Ops routine: "Every 12h, check `modal app logs marketing-metrics`. DM Strategist if any failures."

See `~/.claude/pentagon-agents/ops/soul.md` — already has the skill references.

## Critical files reference

| File | Purpose |
|---|---|
| `scripts/modal/marketing_metrics.py` | Modal app — 3 cron functions (daily, weekly, monthly) + manual entrypoint |
| `scripts/modal/config_loader.py` | Loads `clients/<slug>/metrics-config.json` + env vars |
| `scripts/modal/meta_puller.py` | Meta Marketing API client (account-level + per-ad) |
| `scripts/modal/sheets_writer.py` | gspread wrapper, respects protected columns |
| `scripts/modal/sheets_creator.py` | Creates new sheets (NOTE: won't work until Workspace Shared Drive set up — currently requires manual copy) |
| `scripts/modal/aggregator.py` | Weekly/monthly rollups |
| `scripts/modal/credentials.json` | Google service account (gitignored) |
| `clients/neezanizam/metrics-config.json` | First client config — working reference |
| `clients/_template/metrics-config.json` | Template for new clients (placeholders) |
| `skills/sheets-provisioner/SKILL.md` | Pentagon skill for creating new sheets |
| `skills/sheets-updater/SKILL.md` | Pentagon skill for writing metrics on demand |
| `.env` | Meta credentials (gitignored) |

## Known issues / follow-ups

### Minor fixes needed before scaling to multiple clients

1. **CREATIVES.CTR hardcoded to 0** — `meta_puller.py:get_per_ad_insights` doesn't request `impressions` field, so CTR can't be recomputed. Fix: add `impressions` to the fields param.

2. **APPT/CAPPT columns hardcoded to 0 in account-level daily** — currently using `schedule` + `messaging_conversation_started_7d` Meta action types as heuristic. For NeezaNizam's real ops, appointments likely come from a custom conversion event or manual tracking. Confirm the right Meta event with Jerel.

3. **sheets-provisioner can't auto-create sheets** — service accounts have no Drive quota, so `drive.files.copy` fails with `storageQuotaExceeded`. Workaround: Jerel manually copies the master template in Drive UI (~10 sec), then runs the sheet inspection step. Permanent fix would require Google Workspace Shared Drive.

4. **Appointment mapping per client** — each client may use different Meta events for "appointments." Add a `meta_event_mapping` section to each `metrics-config.json` so the mapping is configurable, not hardcoded.

5. **`transfer_ownership` is implemented but fails silently** — Google Workspace-to-Workspace transfer restrictions. Not critical since we're using the manual copy approach.

6. **Scope mismatch between manual test rows and Modal rows** — DAILY CALLS rows 3-9 were pulled campaign-scoped (Asset Progression only) during manual testing. Row 10 onwards is account-scoped (all campaigns on NND@Propnex). This creates duplicate-date rows where the scope differs. Decide: reconcile historical rows to account-level, OR add a `campaign_id` filter to `metrics-config.json` to keep Modal campaign-scoped. Row 9 notes column flags this ("Asset Progression (campaign test)").

7. **CTR in `_parse_daily_row` may double-percentage** — Meta returns `ctr` as a percentage number (e.g. `2.056`). Code stores as-is. If any sheet column using `ctr` is `%`-formatted, it will show `205.6%` instead of `2.06%`. Not currently written to DAILY CALLS (only OCTR is), but watch for this if `ctr` gets plumbed to a sheet later. Same pattern as the CVR bug that was already fixed.

### Architectural decisions to revisit

- Modal cron runs for ALL clients in sequence. At scale (5+ clients), consider parallelizing with `map`. Currently 1 client ≈ 10 seconds, so 10 clients = 100 seconds. Still under Modal free tier (30 hrs/month).
- Snapshots pile up in `clients/<slug>/metrics/`. Add a cleanup job that archives snapshots older than 90 days.
- No retry on transient Meta API failures beyond the built-in backoff. Consider dead-letter queue if critical.

## Reference — first real test results (for comparison)

**Campaign:** Asset Progression (ID: 6665612766106)
**Period:** Apr 9–15, 2026
**Account:** NND@Propnex (act_837789749619954)

| Metric | Value |
|---|---|
| Total spend | $211.84 |
| Total leads | 6 |
| Total appointments | 2 |
| Best day | Apr 13 (1 lead → 1 appt, 100% CVR) |
| Avg CPM | $14.61 |
| Avg OCTR | 1.78% |

Snapshot: `clients/neezanizam/metrics/test_260416_1811.json`

## Commands cheatsheet

```bash
# Check Meta token still valid
curl -s "https://graph.facebook.com/v22.0/me/adaccounts?access_token=$META_ADS_ACCESS_TOKEN" | python3 -m json.tool | head

# Manual sheet write test (from project root)
python3 -c "
import gspread
from google.oauth2.service_account import Credentials
creds = Credentials.from_service_account_file('scripts/modal/credentials.json', 
    scopes=['https://www.googleapis.com/auth/spreadsheets'])
sheet = gspread.authorize(creds).open_by_key('1D-HrqZHUzvQVmnYO4hR3f9rnznnIprz0CZu8hmUO610')
print([ws.title for ws in sheet.worksheets()])
"

# Modal deployment
cd scripts/modal && modal deploy marketing_metrics.py

# Check Modal cron logs (streams live; Ctrl+C to exit)
modal app logs marketing-metrics

# For historical runs, use the dashboard:
# https://modal.com/apps/fuggysense/main/deployed/marketing-metrics

# Manual Modal trigger (for testing)
modal run marketing_metrics.py::run_for_client --client-slug neezanizam --dry-run

# Onboard a new client
# 1. Manually copy master template sheet in Drive
# 2. Share new sheet with neezanizam@neezanizam-492212.iam.gserviceaccount.com
# 3. Create clients/<new-slug>/metrics-config.json from template
# 4. Replace sheet_id, sheet_url, tab gids, ad_account_id
# 5. Redeploy: modal deploy marketing_metrics.py
```

## How to check Modal sessions / cron runs

**Dashboard:** https://modal.com/apps/fuggysense/main/deployed/marketing-metrics — bookmark it. Shows live runs, scheduled function history, container status, next cron fire time.

**CLI reference:**

| Question | Command |
|---|---|
| All my deployed apps? | `modal app list` |
| Did today's cron fire? What output? | `modal app history marketing-metrics \| head -20` |
| Live tail of running logs | `modal app logs marketing-metrics` |
| Logs for a specific past run | `modal app logs ap-<id>` (ID shown after `modal run` or in dashboard) |
| Is anything running right now? | `modal container list` |
| Shell into a running container | `modal container exec <container-id> bash` |
| Stop a runaway app | `modal app stop marketing-metrics` |
| Confirm auth / workspace | `modal secret list` (shows workspace in output) |

**Quirks noted:**
- `modal app logs` has no `--since` flag. For time-filtered history, use the dashboard.
- `modal token current` does not exist. `modal token new` re-auths.
- When you run `modal run`, streamed output is from the local entrypoint, not the container function. Container logs need `modal app logs <run-id>` or dashboard.

## To resume this work in a new session

1. Open Claude Code in `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/`
2. Say: "Continue metrics automation from `docs/handoffs/metrics-automation-handoff.md` — we're at Phase 5 (cron wait)"
3. Claude reads this doc and picks up where we left off
