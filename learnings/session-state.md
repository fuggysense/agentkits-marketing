# Session State — Confirmed Patterns + Mistakes

Cross-session institutional memory. Loaded on demand via `_index.md`. Append when something is verified or breaks.

## Confirmed Patterns

- **Fork workflow:** `upstream` = `aitytech/agentkits-marketing`, `origin` = `fuggysense/agentkits-marketing`. Push to origin, pull from upstream.
- **Trust-and-ship preference:** Jerel prefers "trust and ship" over PR review for Claude-built changes.
- **Commit cadence:** Commit only after significant changes, not after every small edit. Bundle related work.
- **Telegram bot:** `@jerel` via official Anthropic plugin. Launch with `gumclaw` (preferred) or `claude --channels plugin:telegram@claude-plugins-official`. Bot registry at `~/.claude/channels/telegram/bot-registry.json`.
- **GumClaw:** repo at `~/AI workflows/claudeclaw-seamless/` (GitHub: fuggysense/GumClaw). Multi-bot launcher with auto-pair, lock management, group permissions.
- **ClaudeClaw blueprint:** cloned at `/Users/jerel/AI workflows/claudeclaw/` — reference only, not an installed system. Borrowed patterns: SOUL.md, USER.md, cron-registry.json, deny list.

## Mistakes Not to Repeat

- Must install Telegram plugin (`claude plugin install telegram`) BEFORE launching with `--channels` flag. Otherwise shows "plugin not installed."
- Bun runtime required for Telegram plugin MCP server. Install with `curl -fsSL https://bun.sh/install | bash`.
- Bot token must be at `~/.claude/channels/telegram/.env` (where plugin reads it), not just in `settings.local.json`.
- Cannot launch a second Claude Code instance from inside an existing one via tmux — TTY conflict. User must launch manually in a separate terminal.
- Telegram pairing step is mandatory — bot won't respond until you DM it, get the 6-char code, and run `/telegram:access pair <code>` in the terminal.
- When user says "follow the setup instructions" for a repo, clone it and follow literally. Don't abstract/adapt without asking.
