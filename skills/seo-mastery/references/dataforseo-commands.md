## Graph Links
- **Parent skill:** [[seo-mastery]]
- **Related:** [[programmatic-seo]], [[competitor-alternatives]]
- **MCP integration:** DataForSEO (`skills/integrations/dataforseo/`)

# DataForSEO Command Reference

Structured reference for agents to know which DataForSEO API to call and when. Always check if DataForSEO MCP is available before calling — if not, fall back to manual analysis and flag "DataForSEO not configured."

---

## Quick Reference Table

| Use Case | DataForSEO Tool | When to Use | Cost |
|----------|----------------|-------------|------|
| Check Google rankings | `serp_google_organic_live` | `/seo:audit`, `/seo:keywords` | ~$0.002/req |
| Get search volume | `keywords_google_ads_search_volume` | `/seo:keywords`, content planning | ~$0.001/kw |
| Find keyword ideas | `labs_google_keyword_ideas` | `/seo:keywords`, topic research | ~$0.001/kw |
| Keyword difficulty | `labs_google_keyword_difficulty` | Keyword prioritization | ~$0.001/kw |
| Related keywords | `labs_google_related_keywords` | Content cluster planning | ~$0.001/kw |
| Analyze backlink profile | `backlinks_summary` | `/seo:audit` off-page, `/competitor:deep` | ~$0.004/req |
| List backlinks | `backlinks_backlinks` | Link audit, toxic link detection | ~$0.004/req |
| New/lost backlinks | `backlinks_new_lost` | Link velocity tracking | ~$0.004/req |
| On-page audit | `onpage_task_post` | `/seo:audit` technical | varies |
| SERP features | `serp_google_organic_live` (parse features field) | `/seo:geo`, featured snippet research | ~$0.002/req |
| Competitor SERP overlap | `labs_google_competitor_domain` | `/competitor:deep` | ~$0.002/req |
| Domain metrics | `labs_google_domain_metrics` | Quick authority check | ~$0.001/req |

---

## Authentication

Requires environment variables:
```bash
export DATAFORSEO_LOGIN="your-login-email"
export DATAFORSEO_PASSWORD="your-api-password"
```

Get credentials at: https://app.dataforseo.com/register

---

## Cost Estimation by Task

| Task | Typical API Calls | Estimated Cost |
|------|------------------|----------------|
| Basic keyword check (1 keyword) | 1 SERP + 1 volume | ~$0.003 |
| Keyword research (10 seeds) | 10 ideas + 10 volume + 10 difficulty | ~$0.030 |
| Backlink audit (1 domain) | 1 summary + 1 backlinks list | ~$0.008 |
| Full SEO audit (1 site) | 5-10 SERP + 1 on-page + 1 backlink | ~$0.05-0.10 |
| Competitor analysis (3 competitors) | 3 domain metrics + 3 backlink summaries + SERP overlaps | ~$0.05 |

**Monthly budget guidance:** Light usage ~$5-10/mo. Heavy agency use ~$50-100/mo.

---

## Usage Rules

1. **Always check availability** — before calling DataForSEO tools, verify the MCP is connected. If not: flag and continue with manual analysis.
2. **Batch when possible** — `keywords_google_ads_search_volume` accepts arrays. Send 10 keywords in one call, not 10 separate calls.
3. **Cache results mentally** — if you already fetched SERP data for a keyword this session, don't re-fetch.
4. **Location matters** — always pass `location_name` (e.g., "Singapore", "United States") for accurate local data.
5. **Language code** — pass `language_code` (e.g., "en") for keyword data accuracy.
6. **Cost awareness** — tell the user approximate cost before running large batches. "This keyword research will make ~30 API calls, costing approximately $0.03."

---

## Common Patterns

### Pattern 1: Keyword Research Sprint
```
1. labs_google_keyword_ideas(keywords=["seed1", "seed2"], location="Singapore")
   → Get 50-100 keyword ideas

2. keywords_google_ads_search_volume(keywords=[top 20 from step 1], location="Singapore")
   → Get volume + CPC for best candidates

3. labs_google_keyword_difficulty(keywords=[top 10 from step 2])
   → Check difficulty to prioritize

Output: Ranked keyword list with volume, difficulty, CPC
```

### Pattern 2: Quick Competitive Check
```
1. serp_google_organic_live(keyword="target keyword", location="Singapore")
   → See who ranks, what SERP features exist

2. backlinks_summary(target="competitor.com")
   → Check their link authority

Output: Who's ranking, how strong they are, what features to target
```

### Pattern 3: Backlink Audit
```
1. backlinks_summary(target="client-site.com")
   → Overall profile metrics

2. backlinks_backlinks(target="client-site.com", order_by="page_from_rank,desc")
   → List strongest backlinks

3. backlinks_new_lost(target="client-site.com", date_from="2025-01-01")
   → Recent link changes

Output: Link health assessment, strongest links, recent gains/losses
```

### Pattern 4: GEO Visibility Check
```
1. serp_google_organic_live(keyword="target query", location="Singapore")
   → Check for AI Overview, featured snippet, PAA in SERP features

2. Parse response for:
   - "ai_overview" in features → Google is showing AI answer
   - "featured_snippet" → Current citation source
   - "people_also_ask" → Related questions to target

Output: AI search visibility assessment
```

---

## Fallback When DataForSEO Is Unavailable

| Data Needed | Fallback Method |
|-------------|----------------|
| Rankings | Google Search Console MCP (own site only) |
| Search volume | Estimate from industry knowledge, flag as estimate |
| Backlinks | Semrush MCP (if available) |
| SERP features | Manual Google search via WebFetch |
| Keyword ideas | Content-based brainstorming + Google autocomplete via WebFetch |

Always flag: "⚠️ DataForSEO not configured — data is estimated/manual. Install DataForSEO MCP for verified metrics."

---

## Related

- `skills/integrations/dataforseo/index.md` — MCP setup and endpoint list
- `skills/integrations/_registry.md` — MCP registry
- `.claude/rules/mcp-integrations.md` — Integration overview
