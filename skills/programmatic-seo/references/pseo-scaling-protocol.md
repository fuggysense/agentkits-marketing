# pSEO Scaling Protocol

Graduated rollout system for programmatic SEO pages. Designed to protect domain authority while maximizing growth.

> **Core principle**: Scale based on signals, not ambition. Every batch must earn the next batch.

---

## Pre-Scaling Requirements

### Domain Authority Threshold (MANDATORY)

| DA Range | Maximum Total Pages | Max Pages/Week | Recommendation |
|----------|-------------------|----------------|----------------|
| DA < 20 | **STOP** | 0 | Build authority with editorial content first. pSEO is premature. |
| DA 20-30 | 500 | 50 | Proceed cautiously. Monitor aggressively. |
| DA 30-40 | 2,000 | 100 | Standard scaling. Follow 4-phase protocol. |
| DA 40-60 | 5,000 | 200 | Accelerated scaling possible. Still follow phases. |
| DA 60+ | 10,000+ | 500 | Full velocity. Monitor crawl stats. |

**How to check DA**: Use Semrush MCP `domain_overview` or ask user directly.

**Why DA matters**: Low-authority domains publishing thousands of pages trigger Google's quality filters. The pages may get indexed initially but get de-indexed in subsequent algorithm updates.

### Existing Content Audit

Before scaling, verify:
- [ ] No existing pages will cannibalize new pSEO pages
- [ ] Site has at least 50 indexed editorial pages (establishes topical authority)
- [ ] No existing manual actions or penalties in GSC
- [ ] Core Web Vitals passing on current site

---

## 4-Phase Graduated Rollout

### Phase 1: Proof of Concept (50-100 pages)

**Goal**: Validate that Google indexes and ranks this content type.

**Actions**:
1. Publish 50-100 pages from the strongest niche in taxonomy
2. Submit sitemap to GSC
3. Monitor daily for 2 weeks

**Gate criteria to proceed to Phase 2**:
- [ ] ≥80% of pages indexed within 14 days
- [ ] No thin content warnings in GSC
- [ ] ≥10% of pages appearing in SERPs (any position)
- [ ] No negative impact on existing site rankings
- [ ] Average quality score ≥70 (per quality gates)

**If gate fails**:
- <50% indexed → audit content quality, check for crawl issues
- Thin content warnings → strengthen unique data %, revise schemas
- Existing rankings dropped → pause, investigate, possibly remove pages
- Quality score <70 → improve schemas before scaling

### Phase 2: Validation (200-500 pages)

**Goal**: Confirm the pattern works at moderate scale and generates traffic.

**Actions**:
1. Expand to 2-3 more niches from taxonomy
2. Publish 200-500 additional pages (batches of 100)
3. Wait 1 week between batches
4. Monitor for 2 weeks after final batch

**Gate criteria to proceed to Phase 3**:
- [ ] ≥75% of all pages indexed
- [ ] Some pages ranking in top 20 for target keywords
- [ ] Traffic growing week-over-week for pSEO pages
- [ ] No quality warnings from Google
- [ ] Internal linking structure working (pages passing authority)

**If gate fails**:
- <60% indexed → likely cannibalization or quality issues. Pause and audit.
- No ranking movement → check competition level, may need stronger content
- Traffic flat → validate search intent match, check CTR in GSC

### Phase 3: Scale (1,000-5,000 pages)

**Goal**: Maximize coverage of high-value niches.

**Actions**:
1. Expand across all validated niches
2. Publish in batches of 200-500 (per DA limits)
3. 3-5 days between batches
4. Monitor weekly

**Gate criteria to proceed to Phase 4**:
- [ ] ≥70% of all pages indexed (indexation naturally decreases at scale)
- [ ] Traffic from pSEO pages growing MoM
- [ ] Conversions occurring from pSEO pages
- [ ] No crawl budget issues (check crawl stats in GSC)
- [ ] Server performance stable

### Phase 4: Optimize & Expand (5,000+ pages)

**Goal**: Refine what works, prune what doesn't, expand to new content types.

**Actions**:
1. Analyze performance by niche — double down on winners
2. Prune pages with 0 impressions after 90 days
3. Refresh data on top-performing pages
4. Expand taxonomy based on performance insights
5. Test new content types

---

## Indexation Kill Switch

**MANDATORY PROTOCOL**

### Trigger: Indexation Rate Drops Below 40%

If at any point the indexation rate of pSEO pages drops below 40%:

1. **STOP** all new page publishing immediately
2. **Alert** Jerel / project stakeholder
3. **Diagnose**:
   - Check GSC for manual actions
   - Check for crawl errors
   - Review recent algorithm updates
   - Audit content quality of newest batch
   - Check for cannibalization
4. **Do NOT resume** until:
   - Root cause identified
   - Fix implemented
   - Indexation trending upward for 2+ weeks

### Other Kill Switch Triggers

| Signal | Action |
|--------|--------|
| Manual action in GSC | Stop immediately. Address violation. |
| Existing site traffic drops >20% | Pause pSEO. Investigate correlation. |
| Crawl budget exhaustion | Reduce page velocity by 50%. |
| Thin content warning | Stop. Audit last batch. Strengthen before resuming. |
| Core update ranking drop | Pause 2 weeks. Assess if pSEO pages affected. |

---

## Page Velocity Limits

**Never exceed these publishing rates** regardless of DA:

| Timeframe | Maximum New Pages |
|-----------|------------------|
| Per day | 100 (even for DA 60+) |
| Per week | See DA table above |
| First month of pSEO | 100 total (Phase 1) |

**Why velocity limits?** Sudden spikes in published pages trigger Google's spam detection. Even high-quality pages can get flagged if published too fast.

---

## Content Decay Management

pSEO pages are especially vulnerable to content decay because:
- Data goes stale (prices change, businesses close, stats update)
- Year modifiers in titles become outdated
- Competitor pages get refreshed while yours stay static

### Decay Prevention Schedule

| Content Type | Refresh Frequency | What to Update |
|-------------|-------------------|----------------|
| Location pages | Quarterly | Local data, provider lists, pricing |
| Comparison pages | Monthly | Features, pricing, ratings |
| Glossary pages | Semi-annually | Definitions, examples, related terms |
| Tool/resource pages | Quarterly | Data points, benchmarks |
| Directory pages | Monthly | Listings, ratings, new entries |

### Automated Freshness Signals
- Update `dateModified` in schema markup on every refresh
- Year in title templates: auto-update with current year
- "Last updated" visible on page
- Dynamic data fields refresh from APIs where possible

---

## Monitoring Dashboard

### Weekly Metrics (via GSC MCP)

```markdown
## pSEO Monitoring: Week of [Date]

### Indexation
- Total pages published: [N]
- Indexed: [N] ([%])
- Trend: [↑/↓/→]

### Performance
- Total impressions: [N]
- Total clicks: [N]
- Avg CTR: [%]
- Avg position: [N]

### Health
- Crawl errors: [N]
- Thin content warnings: [N]
- Manual actions: [None/Details]

### Kill Switch Status: [GREEN/YELLOW/RED]
- Indexation rate: [%] (threshold: 40%)
- Existing site impact: [None/Details]
```

### Monthly Report Additions
- Traffic by niche (which taxonomy segments perform best)
- Conversion tracking by page type
- Pages to prune (0 impressions after 90 days)
- Taxonomy expansion recommendations

---

## Rollback Protocol

If a batch of pages needs to be removed:

1. **Noindex first** (don't delete immediately)
2. Wait for Google to process (1-2 crawl cycles)
3. Monitor impact on remaining pages
4. If no negative impact: delete noindexed pages
5. If negative impact: investigate before deleting
6. Update sitemap to remove references
7. Log decision in `decisions.md`

**Never** mass-delete pages without noindexing first. Sudden page removal can confuse Google's understanding of your site structure.
