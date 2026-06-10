# DataForSEO Integration

> Enterprise SEO data API with 750+ SEO tools

## Overview

DataForSEO provides comprehensive SEO data including SERP results, keyword data, backlinks, and on-page analysis. Pay-as-you-go pricing model.

## Key Endpoints

### SERP APIs
| Tool | Description | Cost | Use When |
|------|-------------|------|----------|
| `serp_google_organic_live` | Live Google SERP results + features | ~$0.002/req | Checking rankings, SERP features, AI Overview presence |
| `serp_google_organic_task_post` | Async SERP (cheaper for bulk) | ~$0.001/req | Batch keyword position checks |

### Keyword APIs
| Tool | Description | Cost | Use When |
|------|-------------|------|----------|
| `keywords_google_ads_search_volume` | Search volume + CPC | ~$0.001/kw | Validating keyword targets |
| `labs_google_keyword_ideas` | Keyword suggestions from seeds | ~$0.001/kw | Discovering new keywords |
| `labs_google_keyword_difficulty` | Keyword difficulty score | ~$0.001/kw | Prioritizing keywords by feasibility |
| `labs_google_related_keywords` | Semantically related terms | ~$0.001/kw | Content cluster planning |

### Backlink APIs
| Tool | Description | Cost | Use When |
|------|-------------|------|----------|
| `backlinks_summary` | Domain backlink profile overview | ~$0.004/req | Quick authority check, audit off-page |
| `backlinks_backlinks` | List individual backlinks | ~$0.004/req | Link audit, finding toxic links |
| `backlinks_new_lost` | Recently gained/lost links | ~$0.004/req | Tracking link velocity |
| `backlinks_referring_domains` | Unique referring domains | ~$0.004/req | Domain diversity analysis |

### On-Page APIs
| Tool | Description | Cost | Use When |
|------|-------------|------|----------|
| `onpage_task_post` | Full on-page SEO audit | varies | `/seo:audit` technical analysis |

### Competitive APIs
| Tool | Description | Cost | Use When |
|------|-------------|------|----------|
| `labs_google_competitor_domain` | Domains competing for same keywords | ~$0.002/req | `/competitor:deep` |
| `labs_google_domain_metrics` | Quick domain authority metrics | ~$0.001/req | Competitor strength check |

## Authentication

```bash
export DATAFORSEO_LOGIN="your-login-email"
export DATAFORSEO_PASSWORD="your-api-password"
```

Get credentials at: https://app.dataforseo.com/register

## Pricing

Pay-per-request model:
- SERP API: ~$0.002/request
- Keywords API: ~$0.001/keyword
- Backlinks API: ~$0.004/request
- Full audit estimate: ~$0.05-0.50 depending on scope

## Integration with Marketing Commands

| Command | DataForSEO Tools Used |
|---------|----------------------|
| `/seo:audit` | `onpage_task_post`, `backlinks_summary`, `serp_google_organic_live` |
| `/seo:keywords` | `labs_google_keyword_ideas`, `keywords_google_ads_search_volume`, `labs_google_keyword_difficulty` |
| `/seo:geo` | `serp_google_organic_live` (check for AI Overview in SERP features) |
| `/seo:competitor` | `labs_google_competitor_domain`, `backlinks_summary` |
| `/competitor:deep` | `labs_google_domain_metrics`, `backlinks_summary` |

## Detailed Command Reference

See `skills/seo-mastery/references/dataforseo-commands.md` for:
- Full command-to-use-case mapping
- Cost estimation by task type
- Usage rules and batching patterns
- Fallback strategies when DataForSEO is unavailable

## Related
- [Semrush](../semrush/) - Alternative SEO platform
- [Google Search Console](../google-search-console/) - Own site data
