# Linkup Integration

> Web search API with sourced answers, inline citations, date/domain filtering, and async deep research.

## What Linkup Adds Over WebSearch

| Capability | WebSearch | Linkup |
|-----------|-----------|--------|
| Sourced answers with inline citations | ❌ | ✅ |
| Date-filtered results (from/to) | ❌ | ✅ |
| Domain inclusion/exclusion filters | ❌ | ✅ |
| Async deep research tasks | ❌ | ✅ |
| JS-rendered URL fetch | ❌ | ✅ |
| Structured output (JSON schema) | ❌ | ✅ |
| Quick general search | ✅ | ✅ |

Linkup **augments** WebSearch — it doesn't replace it. Use both in parallel for best coverage.

## Setup

1. Get API key from [linkup.so](https://linkup.so)
2. Add to your project `.env` file:
   ```
   LINKUP_API_KEY=your-api-key-here
   ```
   (The script auto-loads from `.env` at project root. `.env` is gitignored.)
3. Verify: `scripts/linkup.sh balance`

## Commands

### Search
```bash
scripts/linkup.sh search "query" [options]
```

**Options:**
| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--depth` | fast, standard, deep | standard | Search thoroughness |
| `--output` | searchResults, sourcedAnswer | sourcedAnswer | Response format |
| `--citations` | (flag) | off | Include inline citations |
| `--from` | YYYY-MM-DD | — | Results from this date |
| `--to` | YYYY-MM-DD | — | Results until this date |
| `--include-domains` | "d1.com,d2.com" | — | Only these domains |
| `--exclude-domains` | "d1.com,d2.com" | — | Exclude these domains |
| `--max-results` | N | 5 | Max results returned |

**Examples:**
```bash
# Sourced answer with citations
scripts/linkup.sh search "best AI tools for real estate 2026" --output sourcedAnswer --citations

# Date-filtered search
scripts/linkup.sh search "AI marketing trends" --from 2026-01-01 --to 2026-03-12

# Domain-restricted search
scripts/linkup.sh search "lead generation strategies" --include-domains "hubspot.com,semrush.com"

# Fast fact check
scripts/linkup.sh search "Singapore GDP 2025" --depth fast

# Deep research search
scripts/linkup.sh search "competitor analysis AI CRM tools" --depth deep --citations
```

### Async Research (Beta)
```bash
# Start research task
scripts/linkup.sh research "AI lead recovery tools market Singapore" --citations

# Poll for results
scripts/linkup.sh research-status <task-id>
```
Returns a task ID immediately. Poll with `research-status` until complete. Best for complex, multi-faceted queries where you can do other work while waiting.

### URL Fetch
```bash
# Basic fetch
scripts/linkup.sh fetch "https://example.com"

# With JavaScript rendering
scripts/linkup.sh fetch "https://spa-site.com" --js
```
Fallback option when WebFetch fails. `--js` flag handles SPAs and JS-rendered pages.

### Credit Balance
```bash
scripts/linkup.sh balance
```

## Routing Logic: When Linkup vs WebSearch

```
RESEARCH TASK
├─ Quick fact check → WebSearch
├─ Need citations/sources → Linkup (sourcedAnswer, --citations)
├─ Date-filtered → Linkup (--from/--to)
├─ Domain-restricted → Linkup (--include-domains)
├─ Deep multi-angle (/research:deep) → Both in parallel per sub-agent
├─ Fetch specific URL → WebFetch → Linkup fetch → Firecrawl → crawl4ai
└─ General broad → WebSearch + Linkup (parallel, merge)
```

## Cost Awareness

- Each API call uses credits — check balance periodically with `linkup.sh balance`
- Use `--depth fast` for simple lookups to conserve credits
- Use `--depth deep` only when thoroughness matters
- Async research tasks (`research`) use more credits than regular searches
- Domain filtering reduces result count but not credit usage

## Auth

- **Env var:** `LINKUP_API_KEY`
- **Base URL:** `https://api.linkup.so`
- **Auth method:** Bearer token
