# AGENTS.md

Project guidance for coding agents working on the Marketing repository.

## Role
Analyze marketing requirements -> delegate to marketing agents -> deliver campaigns that drive leads, conversions, and revenue.

## Startup files (read every session)
- `SOUL.md` - communication tone, writing rules, mobile formatting
- `USER.md` - operator context (Jerel)
- `cron-registry.json` - scheduled tasks (if running with scheduled channels)
- `CHANNELS.md` - Telegram bot setup (read on demand)

## Critical workflow rules (mandatory, every session)

- **DATA RELIABILITY:** NEVER fabricate metrics. Use MCP integrations. If unavailable, show "NOT AVAILABLE" with setup instructions. -> `./.claude/workflows/data-reliability-rules.md`
- **CONTEXT DISCIPLINE:** Heavy operations (research, DB queries, scrapes, URL fetches) route through subagents or `ctx_execute`. NEVER directly into session context. The `smart-ctx-guard.sh` PreToolUse hook nudges. -> `./.claude/workflows/context-discipline.md`
- **MARKETING RULES:** mandatory, non-negotiable -> `./.claude/workflows/marketing-rules.md`
- **README CONTEXT:** Before planning a campaign, read `./README.md`.
- **Concision:** Sacrifice grammar for concision in reports. List unresolved questions at end.
- **Dates:** `bash -c 'date +%y%m%d'`. Never use model knowledge for dates.

## CONTEXT GATE (before invoking ANY skill or agent)

Establish WHO and WHAT PROJECT. If not set:
1. List `clients/` (excl. `_template/`) + `voice/` profiles (excl. templates).
2. Ask: "Who is this session for?"
3. Once picked, **lean-load only**:
   - **Always:** `clients/<project>/context-profile.json` (~2KB) + `clients/<project>/CONTEXT.md` if present.
   - **On demand via `ctx_search`:** voice files + Jake-style `_brand/` files (`_brand/icp.md`, `_brand/offer.md`, `_brand/brand-voice.md`, `_brand/channels.json`, `_brand/learnings.md`, `_brand/buyer-profile.md`). For legacy clients only, fall back to flat root files.
   - **Full load required:** copywriting sessions (`_brand/brand-voice.md` verbatim), offer pages (`_brand/offer.md` verbatim). For legacy clients only, fall back to flat root files.
4. Keep loaded files active for the session.
5. If no project: offer to scaffold from `clients/_template/`.
6. **Exception:** pure research tasks (`/research:trend`, `/marketing:ideas`) skip this gate.

## Workflows
- Marketing: `./.claude/workflows/primary-workflow.md`
- Sales: `./.claude/workflows/sales-workflow.md`
- CRM: `./.claude/workflows/crm-workflow.md`
- Marketing rules: `./.claude/workflows/marketing-rules.md`
- Orchestration: `./.claude/workflows/orchestration-protocol.md`
- Documentation mgmt: `./.claude/workflows/documentation-management.md`

## Reference files (load on demand - do NOT preload)

**Index (start here):** `.claude/rules/_index.md`

| Need | Where |
|------|-------|
| Routing keyword -> skill | `.claude/rules/routing-table.md` (auto-generated, hot) + `routing-overrides.md` |
| Detailed catalogs (commands, skills, agents) | `docs/system-rules/details/{commands,routing-table,skills-catalog}.md` |
| System rules (HITL, owner model, self-annealing, etc.) | `docs/system-rules/*.md` (see `_index.md`) |
| Learnings + session state | `learnings/*.md` (see `_index.md`) |
| Skill graph (semantic edges) | `.claude/skill-graph.json` - see `docs/system-rules/skill-graph-rule.md` |
| MCP integrations | `.claude/rules/mcp-integrations.md` |

## Hard pointers (mandatory triggers - load these files when condition fires)

- **End of session?** -> `docs/system-rules/session-end-protocol.md`
- **Start of session?** -> `docs/system-rules/session-start-protocol.md` (silent dashboard, max 5 lines)
- **HITL decision?** -> `docs/system-rules/hitl-gates.md`
- **Tool/strategy choice?** -> `docs/system-rules/analysis-framework.md` (4-factor scoring)
- **Process failed?** -> `docs/system-rules/self-annealing.md` (fix -> log -> update -> test -> strengthen)
- **User corrected output?** -> `docs/system-rules/correction-capture.md`
- **Replying via Telegram?** -> `docs/system-rules/telegram-messaging.md` (multi-message format)
- **Telegram broken?** -> **`learnings/telegram-debugging.md` BEFORE touching files.** Process check first.
- **Creating/editing skill or agent?** -> `docs/system-rules/skill-graph-rule.md` (must run `link-skills.py`)

## Token budget rule
**Net-zero growth.** Any new line auto-loaded into `AGENTS.md` requires deleting an equivalent line elsewhere. Do NOT preload `docs/system-rules/details/*` or `docs/system-rules/*` - fetch via `_index.md` recipes only when triggered.

## Operating model (one-liner)
Owner: Jerel - non-technical, taste/strategy. 80/20 HITL: agent does 80% (research, drafting, analysis), Jerel does 20% (taste, approvals). Full rules: `docs/system-rules/operating-model.md`.

## Obsidian context (one-liner)
Repo lives inside Obsidian vault at `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/`. Voice: `voice/jerel/`. Personal profile: `../../Personal and professional profile/`. Master map: `../../index.md`. Full context: `docs/system-rules/obsidian-context.md`.

## Documentation
All docs in `./docs/`. Ops reports in `./docs/ops/{weekly,monthly}/`. System rules in `./docs/system-rules/`. Architecture reviews in `./docs/`.

---

**MUST READ + MUST COMPLY** all instructions above. **WORKFLOWS** + **CONTEXT GATE** + **CONTEXT DISCIPLINE** + **DATA RELIABILITY** are the load-bearing four. Everything else is reference.
