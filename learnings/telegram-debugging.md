# Telegram Debugging Rules — MANDATORY

When Telegram stops working (can't send, can't receive, "not allowlisted"), follow this exact order. **Process check first. Never reverse this order.**

## Step 1 ALWAYS: Check for competing bot processes

```bash
pgrep -af "bun.*telegram"
# Then for each PID, check parent:
ps -p <PID> -o ppid=,command=
```

- If multiple bot processes exist with **DIFFERENT parent PIDs** → competing sessions
- Kill ONLY the ones NOT from this session (check parent PID matches current Claude session)
- This is the cause **90% of the time**. Do this BEFORE touching access.json files.

## NEVER DO

- **Never kill this session's own bot processes** (check parent PID first). Killing them disconnects the MCP server permanently — session must be restarted.
- **Never debug access.json files before checking for competing processes.** The files are almost always fine — the problem is process-level.
- **Never spend more than 30 seconds on file-level debugging** if process check wasn't done first.

## Step 2 ONLY IF Step 1 found no competing processes

- Find real state dir: `ps eww $(pgrep -f "bun.*telegram" | head -1) | tr ' ' '\n' | grep TELEGRAM_STATE_DIR`
- Check access.json at the resolved path
- Run `bash ~/.claude/channels/telegram/auto-pair.sh`

## Diagnostic order (memorize)
**processes → state dir → access file**

Never reverse.
