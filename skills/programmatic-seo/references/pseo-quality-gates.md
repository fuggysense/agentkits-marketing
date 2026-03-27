## Graph Links
- **Parent skill:** [[programmatic-seo]]
- **Sibling references:** [[niche-taxonomy-builder]], [[pseo-2-architecture]], [[pseo-implementation-guide]], [[pseo-scaling-protocol]]
- **Related skills:** [[analytics-attribution]]

# pSEO Quality Gates

Three-gate validation system for programmatic SEO content. Every page must pass all three gates before publishing.

---

## Gate 1: Unique Answer Test

**Question**: Does this page answer a distinct search query that no other page on the site answers?

### Scoring Rubric

| Score | Criteria | Action |
|-------|----------|--------|
| Pass | Page targets a unique keyword/intent combination | Proceed |
| Conditional | Partial overlap with another page | Merge or differentiate |
| Fail | Another page answers the same query equally well | Remove or consolidate |

### Automated Checks
1. **Title uniqueness**: No two pages share >70% title similarity
2. **H1 uniqueness**: Every H1 must be unique
3. **Primary keyword**: No two pages target the exact same primary keyword
4. **Intent overlap**: Check if searcher would be equally satisfied by another page on the site

### Cannibalization Detection

**Signals of cannibalization**:
- Two pages ranking for the same query (check GSC)
- Pages trading positions in SERPs
- Similar click patterns on similar pages
- Internal search showing multiple results for same query

**Resolution playbook**:
1. Identify the stronger page (more backlinks, better content, older)
2. Options:
   - **Merge**: Combine content, 301 redirect weaker → stronger
   - **Differentiate**: Sharpen each page's unique angle
   - **Noindex**: Keep page for users but remove from index
   - **Delete**: If no unique value, remove entirely
3. After resolution, re-check in 2 weeks via GSC

---

## Gate 2: 40% Unique Data Test

**Question**: Is at least 40% of the page's content unique to THIS specific page (not shared template content)?

### What Counts as Unique Data

| Unique (counts) | Shared (doesn't count) |
|-----------------|----------------------|
| Location-specific statistics | Template intro paragraph |
| Product-specific features | Navigation/header/footer |
| User reviews/ratings | Boilerplate disclaimers |
| Local pricing data | Generic section headings |
| Entity-specific FAQs | Standard CTA blocks |
| Original analysis/commentary | Repeated methodology text |
| Dynamic data (API-sourced) | Static template copy |

### Scoring Method

```
Unique Data % = (unique content words) / (total content words) × 100

Pass: ≥40%
Warning: 30-39% (add more unique data)
Fail: <30% (thin content risk — do not publish)
```

### How to Increase Unique Data %
1. Add more data fields to the JSON schema (more variables per page)
2. Include conditional content blocks (show different sections based on data)
3. Add user-generated content (reviews, comments)
4. Pull real-time data from APIs
5. Include entity-specific FAQs (not generic)
6. Add original analysis per page

---

## Gate 3: Engagement Test

**Question**: Would a user find this page useful even if it never ranked in search engines?

### The "Bookmark Test"
> Would someone bookmark this page to come back to later?

If the answer is no, the page needs more value.

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| Pass | Page provides actionable information, data, or tools that solve a real problem |
| Conditional | Page is informative but lacks a unique hook or actionable takeaway |
| Fail | Page exists only to rank — no genuine utility beyond SEO |

### Value Signals
- Contains data not easily found elsewhere
- Provides a tool, calculator, or interactive element
- Aggregates information that saves user research time
- Offers expert analysis or recommendations
- Includes community contributions (reviews, ratings)

### Anti-Patterns (Auto-Fail)
- Page is just a list of links to other pages
- Content is a rewording of Wikipedia/public knowledge
- No differentiation from the first Google result
- "Doorway page" that immediately funnels to product page
- Missing key information (empty sections, placeholder text)

---

## Quality Scoring Framework

### Per-Page Score

```
Quality Score = (Gate 1 × 0.3) + (Gate 2 × 0.4) + (Gate 3 × 0.3)

Each gate scored 0-100:
- Gate 1: Uniqueness (0 = duplicate, 100 = completely unique query)
- Gate 2: Data % (0 = all template, 100 = all unique)
- Gate 3: Engagement (0 = zero utility, 100 = bookmark-worthy)

Overall:
- 80+: Publish immediately
- 60-79: Publish with improvement notes
- 40-59: Hold — improve before publishing
- <40: Do not publish — regenerate or remove
```

### Batch Quality Report

After running quality gates on a batch, produce:

```markdown
## Quality Report: Batch [N] — [Date]

### Summary
- Total pages: [N]
- Passed (80+): [N] ([%])
- Conditional (60-79): [N] ([%])
- Held (40-59): [N] ([%])
- Failed (<40): [N] ([%])

### Gate Breakdown
| Gate | Avg Score | Lowest | Issues Found |
|------|-----------|--------|-------------|
| Gate 1: Unique Answer | [score] | [page] | [count] cannibalization |
| Gate 2: 40% Data | [score] | [page] | [count] thin pages |
| Gate 3: Engagement | [score] | [page] | [count] low-utility |

### Action Items
1. [Specific pages to fix]
2. [Schema changes needed]
3. [Data gaps to fill]
```

---

## Post-Generation Page Optimization

After pages pass the 3-gate validation, apply the optimization stack from `skills/website-design/SKILL.md` → "Post-Build Optimization Router":

1. **SEO** (meta tags, heading structure) — via seo-specialist
2. **Schema Markup** (JSON-LD) — via seo-specialist
3. **AEO/GEO** (AI search optimization) — via seo-specialist
4. **Tracking** (GA4 events, conversion pixels) — via tracking-specialist

This applies at the template level (optimize once, all pages benefit) rather than per-page.

---

## Ongoing Quality Monitoring

### Weekly Checks (via GSC MCP)
- Index coverage % (target: >80%)
- New crawl errors
- Pages with impressions but 0 clicks (title/meta issues)
- Cannibalization signals (multiple pages ranking for same query)

### Monthly Checks
- Thin content warnings in Search Console
- Average position trends by page type
- Traffic per page distribution (flag pages with 0 traffic after 60 days)
- Content freshness (flag pages with stale data)

### Quarterly Reviews
- Prune pages that never gained traction (>90 days, 0 traffic)
- Refresh data on top-performing pages
- Expand taxonomy based on performance data
- Update JSON schemas based on quality gate trends
