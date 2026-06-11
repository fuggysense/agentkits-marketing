# MCP Integrations (Real Data Sources)

Use MCP servers for verified data. See `.claude/skills/integrations/_registry.md` for full details.

| Server | Category | Use For |
|--------|----------|---------|
| `google-search-console` | SEO | Search performance, rankings |
| `google-analytics` | Analytics | Web traffic, user behavior |
| `semrush` | SEO | Keywords, backlinks, domain analysis |
| `dataforseo` | SEO | SERP data, keyword metrics. See `skills/seo-mastery/references/dataforseo-commands.md` for command reference |
| `hubspot` | CRM | Contacts, deals, marketing automation |
| `slack` | Communication | Team notifications |
| `notion` | Project Mgmt | Pages, databases |
| `asana` | Project Mgmt | Tasks, projects |
| `twitter` | Social | Tweets, search |
| `tiktok` | Social | Video trends |
| `line` | Regional (JP) | Japan messaging |
| `postiz` | Social Publishing | Multi-platform scheduling, media upload, analytics |
| `linkup` | Web Search | Sourced answers, citations, date/domain filtering, async research |
| `kilo-gateway` | Research LLM | Cheap model routing for research synthesis (MiniMax M2.5, Nemotron 3 Super) |
| `gemini-cli` | Research LLM | Gemini 2.5 Flash for research synthesis via CLI |
| `ollama` | Local LLM | Local models via Ollama (Qwen3, etc.) — free, private, offline |
| `chrome` | Browser | Authenticated browser control, live dashboard inspection |
| `paper` | Design | Visual design editing, JSX/Tailwind export, HTML preview |
| `netlify` | Hosting | Site creation, deploys, env vars, DNS, serverless functions |

**Usage**: `/use-mcp [task]`.

> **Meta / Facebook Ads = CLI, not MCP.** All Meta Marketing API work (campaigns, ad sets, ads, creatives, insights, datasets/pixels, catalogs) goes through the `meta` CLI (`~/.local/bin/meta`) — there is no meta-ads MCP server. Auth: `source ~/.claude/.env && export ACCESS_TOKEN="$META_ACCESS_TOKEN"`, then `meta auth status`. Read verbs (`meta ads campaign list`, `meta ads insights get`, `meta ads adaccount get`) are safe; `create`/`update`/`delete` are LIVE + billable — show the command and confirm before running. Scope every call with `--ad-account-id act_…` or `--business-id …`; add `-o json` for downstream processing. Do NOT use a meta-ads MCP, pipeboard, or raw Graph `curl`. Known accounts: NND@Propnex `act_837789749619954` (biz `837781629620766`), Fuggy's Media #1 `act_936198302709669` (biz `2334231630425342`).

### Research LLM Router

Route research synthesis to cheaper models instead of burning Claude tokens. Script: `scripts/research-llm.sh`

```bash
scripts/research-llm.sh kilo "prompt"                                    # MiniMax M2.5 (default)
scripts/research-llm.sh kilo "prompt" --model "nvidia/nemotron-3-super"  # Nemotron 3 Super
scripts/research-llm.sh gemini "prompt"                                  # Gemini 2.5 Flash
scripts/research-llm.sh ollama "prompt"                                  # Qwen3 local (default)
scripts/research-llm.sh ollama "prompt" --model "qwen3:latest"           # Explicit model
scripts/research-llm.sh ollama "prompt" --no-think                       # Skip Qwen3 thinking (faster)
scripts/research-llm.sh local "prompt"                                   # Alias for ollama
scripts/research-llm.sh list                                             # Show installed Ollama models
scripts/research-llm.sh auto "prompt"                                    # Kilo → Gemini → Ollama fallback
```

Env: `KILO_API_KEY` in `.env`. Gemini CLI must be installed separately. Ollama: `ollama serve` must be running (override host with `OLLAMA_HOST` env var).
