# CLAUDE.md

Project guidance for Claude Code on the Marketing repository.

## Role
Analyze marketing requirements → delegate to marketing agents → deliver campaigns that drive leads, conversions, revenue.

## Startup files (read every session)
- `SOUL.md` — communication tone, writing rules, mobile formatting
- `USER.md` — operator context (Jerel)
- `cron-registry.json` — scheduled tasks (if running with `--channels`)
- `CHANNELS.md` — Telegram bot setup (read on demand)
- **Where is every client / what's next?** → `/campaign:status` (no args = cross-client board, `scripts/status_board.py`). Session memory lives in `_handoffs/<date>-<topic>.md` (see `session-end-protocol.md`).

## Critical workflow rules (mandatory, every session)

- **DATA RELIABILITY:** NEVER fabricate metrics. Use MCP integrations. If unavailable, show "⚠️ NOT AVAILABLE" with setup instructions. → `./.claude/workflows/data-reliability-rules.md`
- **CONTEXT DISCIPLINE:** Heavy operations (research, DB queries, scrapes, URL fetches) route through subagents or `ctx_execute`. NEVER directly into session context. The `smart-ctx-guard.sh` PreToolUse hook nudges. → `./.claude/workflows/context-discipline.md`
- **MARKETING RULES:** mandatory, non-negotiable → `./.claude/workflows/marketing-rules.md`
- **CAMPAIGN CONTEXT:** Before planning a campaign, read `./clients/README.md` plus the active client's campaign index/state files.
- **Concision:** Sacrifice grammar for concision in reports. List unresolved questions at end.
- **Dates:** `bash -c 'date +%y%m%d'`. Never use model knowledge for dates.

## AGENT ENTRY CONTRACT (before invoking ANY skill or agent)

For client/campaign/workspace work, establish a context receipt before delegation or writes. Receipt = agent can name WHO, active campaign, workspace, current phase, and next action after reading:
1. `CLAUDE.md` — repo rules.
2. `clients/<project>/CLAUDE.md` — client law.
3. `clients/<project>/CONTEXT.md` + `context-profile.json` — folder map + business facts.
4. `clients/<project>/campaigns/_campaigns-index.json` — active campaign.
5. Workspace chain: `campaign-index.json` -> `campaign-selection.json` -> workspace `artifact-manifest.json` -> `pipeline-state.json` -> workspace-root `concept-brief.json` (canonical typed brief). Treat `concept-input-packet.json` only as a legacy alias in older workspaces, or use the typed brief named by the artifact manifest.

If WHO/WHAT is unset: read `.claude/active-work.json` first. If it resolves to existing client/campaign state, use it as the default context receipt and mention it briefly. If missing/stale or the user asks for different work, list `clients/` (excl. `_template/`) and `voice/` profiles if any exist (excl. templates), ask "Who is this session for?", then lean-load only `context-profile.json` + `CONTEXT.md`; load `_brand/*` on demand via `ctx_search` except copywriting/offer-page sessions, which REQUIRE `_brand/offer.md` + `_brand/buyer-profile.md` loaded verbatim into `loaded_paths[]` — a copy session with an active client and no offer file loaded must STOP and load it (or flag if absent on disk), never interview around it.
Every subagent/worker touching `clients/*` must receive `context_receipt: {client, campaign, workspace, phase, loaded_paths[]}`. No receipt = stop and read/ask first. Pure research tasks (`/research:trend`, `/marketing:ideas`) skip this gate.

## Workflows
- Marketing: `./.claude/workflows/primary-workflow.md`
- Sales: `./.claude/workflows/sales-workflow.md`
- CRM: `./.claude/workflows/crm-workflow.md`
- Marketing rules: `./.claude/workflows/marketing-rules.md`
- Orchestration: `./.claude/workflows/orchestration-protocol.md`
- Documentation mgmt: `./.claude/workflows/documentation-management.md`

## Reference files (load on demand — do NOT preload)

**Index (start here):** `.claude/rules/_index.md`

| Need | Where |
|------|-------|
| Routing keyword → skill | `.claude/rules/routing-table.md` (auto-generated, hot) + `routing-overrides.md` |
| Detailed catalogs (commands, skills, agents) | `docs/system-rules/details/{commands,routing-table,skills-catalog}.md` |
| System rules (HITL, owner model, self-annealing, etc.) | `docs/system-rules/*.md` (see `_index.md`) |
| Skill graph (semantic edges) | `.claude/skill-graph.json` — see `docs/system-rules/skill-graph-rule.md` |
| MCP integrations | `.claude/rules/mcp-integrations.md` |

## Hard pointers (mandatory triggers — load these files when condition fires)

- **End of session?** → `docs/system-rules/session-end-protocol.md`
- **Start of session?** → `docs/system-rules/session-start-protocol.md` (silent dashboard, max 5 lines)
- **HITL decision?** → `docs/system-rules/hitl-gates.md`
- **Tool/strategy choice?** → `docs/system-rules/analysis-framework.md` (4-factor scoring)
- **Process failed?** → `docs/system-rules/self-annealing.md` (fix → log → update → test → strengthen)
- **User corrected output?** → `docs/system-rules/correction-capture.md`
- **Replying via Telegram?** → `docs/system-rules/telegram-messaging.md` (multi-message format)
- **Telegram broken?** → **`learnings/telegram-debugging.md` BEFORE touching files.** Process check first.
- **Creating/editing skill or agent?** → `docs/system-rules/skill-graph-rule.md` (must run `link-skills.py`)

## Token budget rule
**Net-zero growth.** Any new line auto-loaded into CLAUDE.md requires deleting an equivalent line elsewhere. Do NOT preload `docs/system-rules/details/*` or `docs/system-rules/*` — fetch via `_index.md` recipes only when triggered.

## Operating model (one-liner)
Owner: Jerel — non-technical, taste/strategy. 80/20 HITL: Claude does 80% (research, drafting, analysis), Jerel does 20% (taste, approvals). Full rules: `docs/system-rules/operating-model.md`.

## Obsidian context (one-liner)
Repo lives inside Obsidian vault at `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/`. Voice folder: `voice/` (read `voice/README.md` first; no personal voice profile is guaranteed). Personal profile: `../../Personal and professional profile/`. Master map: `../../index.md`. Full context: `docs/system-rules/obsidian-context.md`.

## Documentation
All docs in `./docs/`. Ops reports in `./docs/ops/{weekly,monthly}/`. System rules in `./docs/system-rules/`. Architecture reviews in `./docs/`.

---

**MUST READ + MUST COMPLY** all instructions above. **WORKFLOWS** + **AGENT ENTRY CONTRACT** + **CONTEXT DISCIPLINE** + **DATA RELIABILITY** are the load-bearing four. Everything else is reference.
