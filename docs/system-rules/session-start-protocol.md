# Session Start Protocol

At the start of every session (before any work), run these checks **silently** and surface a brief status dashboard:

## 1. Git sync
`git fetch upstream`, check for new commits (every 3 days). `upstream` = `aitytech/agentkits-marketing`.

## 2. Ops freshness
- Look for most recent file in `docs/ops/weekly/` → if >7 days ago, flag `/ops:weekly` as overdue
- Look for most recent file in `docs/ops/monthly/` → if >30 days ago, flag `/ops:monthly` as overdue
- If no files exist yet, note "never run" and suggest first run

## 3. Multi-project check
If multiple projects exist in `clients/`, show per-project status:
```
Project health:
- AURA: weekly overdue (12 days) | monthly OK (18 days)
- Client B: all OK
```

## 4. Active campaigns
Read `.claude/active-work.json` if present, then check `clients/*/campaigns/_campaigns-index.json` for `status: active`. For older clients without `_campaigns-index.json`, fall back to `clients/*/campaigns/*/state.yaml`. Surface the active client, campaign, current gate, live review URL if present, and next action.

## 5. Cron restore
If running with `--channels` (Telegram bot active), read `cron-registry.json` and re-register all `enabled: true` jobs via CronCreate. Crons are session-only and auto-expire after 7 days, so this must happen every session. Log how many were restored.

## 6. Compact dashboard
Max 5 lines. Don't block work, just surface it. If everything is fine, say "All ops current" and move on.

### Format
```
Session check:
  Git: upstream synced (2 days ago)
  Ops: /ops:weekly overdue (9 days) — run now?
  Crons: 4 restored from cron-registry.json
  AURA: 1 active campaign (tiktok-content, execution phase)
```
