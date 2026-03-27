# MCP Integrations (Real Data Sources)

Use MCP servers for verified data. See `.claude/skills/integrations/_registry.md` for full details.

| Server | Category | Use For |
|--------|----------|---------|
| `google-search-console` | SEO | Search performance, rankings |
| `google-analytics` | Analytics | Web traffic, user behavior |
| `semrush` | SEO | Keywords, backlinks, domain analysis |
| `dataforseo` | SEO | SERP data, keyword metrics |
| `meta-ads` | Advertising | Facebook/Instagram ads |
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
| `chrome` | Browser | Authenticated browser control, live dashboard inspection |
| `paper` | Design | Visual design editing, JSX/Tailwind export, HTML preview |
| `netlify` | Hosting | Site creation, deploys, env vars, DNS, serverless functions |

**Usage**: `/use-mcp [task]` or delegate to `mcp-manager` agent.

### Research LLM Router

Route research synthesis to cheaper models instead of burning Claude tokens. Script: `scripts/research-llm.sh`

```bash
scripts/research-llm.sh kilo "prompt"                                    # MiniMax M2.5 (default)
scripts/research-llm.sh kilo "prompt" --model "nvidia/nemotron-3-super"  # Nemotron 3 Super
scripts/research-llm.sh gemini "prompt"                                  # Gemini 2.5 Flash
scripts/research-llm.sh auto "prompt"                                    # Kilo first, Gemini fallback
```

Env: `KILO_API_KEY` in `.env`. Gemini CLI must be installed separately.
