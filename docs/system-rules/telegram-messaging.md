# Telegram Messaging Rule

When replying via Telegram (`mcp__plugin_telegram_telegram__reply`), send **multiple short messages** instead of one big block.

- One thought per message, like a real chat
- Break long responses into 3-5 short messages
- Keep each under 500 chars when possible
- Use emoji reactions (`react`) for quick acknowledgements
- Use `edit_message` for interim progress updates (no push notification)
- New `reply` for completion (triggers ping on user's device)

## When NOT to send a wall of text
Almost never. If you have a long technical answer, send a 1-line summary as the first message, then break the detail into 2-4 follow-ups.

## See also
- `learnings/telegram-debugging.md` — when Telegram stops working
