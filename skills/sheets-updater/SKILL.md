---
name: sheets-updater
description: "Pull Meta Ads metrics → client Google Sheet. HITL preview, protected columns. Daily/weekly/monthly/on-demand updates via metrics-config.json."
---

# Sheets Updater — Pull Metrics, HITL Preview, Write

Pulls metrics from Meta Ads API (and other sources), presents a HITL preview, then writes to the client's Google Sheet based on their `metrics-config.json`.

**Input:** `$ARGUMENTS` — client slug + frequency (`daily` / `weekly` / `monthly` / `on-demand`) + optional `--dry-run` flag

## Prerequisites

- `clients/<slug>/metrics-config.json` exists (created by sheets-provisioner)
- Meta API token set: `META_ADS_ACCESS_TOKEN` in `.env` or Modal secret
- Google Sheets service account credentials
- Client's ad account ID set in `metrics-config.json`

## Workflow

### 1. Load config
```python
config = json.load("clients/<slug>/metrics-config.json")
ad_account = config["ad_platforms"]["meta"]["ad_account_id"]
tabs = config["tabs"]
```

### 2. Pull metrics from Meta

For each tab with `source: "meta_insights"` or `"meta_insights_per_ad"`:

**For DAILY CALLS** (account-level aggregation):
```
GET https://graph.facebook.com/v22.0/{ad_account}/insights
  ?fields=spend,impressions,clicks,ctr,cpm,actions,cost_per_action_type
  &time_range={"since":"YYYY-MM-DD","until":"YYYY-MM-DD"}
  &level=account
```

Parse response into row:
- LEAD = actions where type = "lead"
- CPL = cost_per_action_type where type = "lead"
- APPT = actions where type = "schedule" or "onsite_conversion"
- REVENUE = actions_values where type = "purchase" (if tracked)
- AMOUNT SPENT = spend
- CVR = (leads / clicks) * 100
- CPM = cpm
- OCTR = ctr
- CPOC = spend / appointments

**For CREATIVES** (per-ad level):
```
GET https://graph.facebook.com/v22.0/{ad_account}/ads
  ?fields=name,status,insights{ctr,cpc,spend,actions,impressions,clicks}
  &time_range={"since":"launch_date","until":"today"}
```

Match each ad to its DCT batch number (regex on ad name: `DCT\d+`).

### 3. Build preview table

For frequency = daily, preview shape:
```
## Daily Metrics Preview — [Client] — [Date]

### DAILY CALLS (row will be appended)
| DATE | LEAD | CPL | APPT | CAPPT | REVENUE | AMOUNT SPENT | CVR | CPM | CPOC | OCTR | NOTES |
|------|------|------|------|--------|---------|--------------|-----|------|------|------|-------|
| 16/04/26 | 3 | $45.20 | 1 | $135.60 | $0 | $135.60 | 1.2% | $28.45 | $0.89 | 4.2% | (auto) |

### CREATIVES (metric columns will update, strategy columns preserved)
| BATCH | STATUS | CTR | CVR | CPA | CALLS | SPEND | DURATION |
|-------|--------|-----|-----|-----|-------|-------|----------|
| DCT001 | ACTIVE | 3.20% | 1.80% | $89.40 | 2 | $178.80 | 8 days |
| ...

### Anomalies detected
- ⚠️ DCT003 CPA $195 (1.5x baseline $130) — CRITICAL
- (none other)

Proceed? (yes / skip / edit / dry-run-only)
```

### 4. HITL gate

Based on `config.hitl.daily_write`:
- `preview_then_approve`: stop and wait for user
- `auto_write_with_dm_summary`: write immediately, DM summary after
- `dry_run_always`: never write, only preview (for testing)

When Modal cron runs, default is `auto_write_with_dm_summary`. When Ops agent runs interactively, default is `preview_then_approve`.

### 5. Write to sheet

Use `gspread`:
```python
sheet = gc.open_by_key(config["sheet_id"])
tab = sheet.get_worksheet_by_id(int(tab_config["gid"]))

if tab_config["write_mode"] == "append":
    tab.append_row(row_values, value_input_option="USER_ENTERED")
elif tab_config["write_mode"] == "update_metric_columns":
    # For each batch row, only update metric columns, leave protected untouched
    for batch_row in metrics:
        row_num = find_row_by_batch_id(tab, batch_row["BATCH"])
        for col in tab_config["metric_columns"]:
            col_letter = column_name_to_letter(tab, col)
            tab.update(f"{col_letter}{row_num}", batch_row[col])
```

**Critical:** Never write to columns in `protected_columns`. Use `tab.update()` with specific ranges, never `tab.update_values()` on the whole row.

### 6. Log snapshot

Save full metrics to `clients/<slug>/metrics/YYMMDD.json`:
```json
{
  "date": "2026-04-16",
  "frequency": "daily",
  "source": "meta_insights",
  "tabs_updated": ["daily_calls", "creatives"],
  "metrics": { ... full response ... },
  "anomalies": [ ... ],
  "modal_run_id": "run_xxx" (if from Modal)
}
```

### 7. Anomaly handling

If any metric breaches thresholds in `config.anomaly_thresholds`:
- Warning: include in DM summary
- Critical: immediate DM to Strategist via Pentagon MCP
- Ad disapproved: immediate DM to Jerel

## Dry-run mode

With `--dry-run`:
1. Pull metrics
2. Build preview table
3. Show what WOULD be written
4. Do NOT call `tab.append_row` or `tab.update`
5. Save snapshot to `clients/<slug>/metrics/dryrun-YYMMDD.json`

Use for testing new configs or after sheet structure changes.

## Rules

1. **Never fabricate metrics.** If Meta API returns null, write empty (don't estimate).
2. **Protected columns are sacred.** Never touch MARKET AWARENESS, SOPHISTICATION, ANGLE, PERSONA in CREATIVES tab.
3. **HITL required for interactive runs.** Modal cron auto-writes with DM summary.
4. **Log every run** even dry-runs.
5. **Fail loudly** — if Meta API fails, DM Strategist with the error, don't silently skip.

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[sheets-provisioner]] (skill, 0.13)
- [[feedback-router]] (skill, 0.12)

<!-- skill-graph:end -->
