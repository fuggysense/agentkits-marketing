---
name: programmatic-seo
version: "2.0.0"
updated: "260313"
brand: AgentKits Marketing by AityTech
category: seo-growth
difficulty: advanced
description: When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions "programmatic SEO," "pSEO 2.0," "JSON-first pages," "niche taxonomy," "schema-driven content," "template pages," "pages at scale," "directory pages," "location pages," "[keyword] + [city] pages," "comparison pages," "integration pages," "GEO," "generative engine optimization," or "building many pages for SEO." For auditing existing SEO issues, see seo-audit.
triggers:
  - programmatic SEO
  - pSEO 2.0
  - JSON-first pages
  - niche taxonomy
  - schema-driven content
  - template pages
  - pages at scale
  - directory pages
  - location pages
  - comparison pages
  - integration pages
  - GEO
  - generative engine optimization
prerequisites:
  - seo-mastery
related_skills:
  - seo-mastery
  - schema-markup
  - competitor-alternatives
  - analytics-attribution
  - content-strategy
  - website-design
agents:
  - pseo-architect
  - attraction-specialist
  - seo-specialist
mcp_integrations:
  optional:
    - google-search-console
    - semrush
    - dataforseo
success_metrics:
  - indexed_pages
  - organic_traffic
  - keyword_coverage
---

## Graph Links
- **Feeds into:** [[schema-markup]]
- **Draws from:** [[seo-mastery]], [[content-strategy]]
- **Used by agents:** [[pseo-architect]], [[seo-specialist]]
- **Related:** [[competitor-alternatives]]

# Programmatic SEO (v2.0)

You are an expert in programmatic SEO—building SEO-optimized pages at scale using templates and data. Your goal is to create pages that rank, provide value, and avoid thin content penalties.

## pSEO 2.0: The Paradigm Shift

pSEO 2.0 separates content generation into three distinct layers:

1. **Data Layer** — Structured niche taxonomy defining what pages exist
2. **Schema Layer** — Strict JSON schemas defining page structure per content type
3. **Renderer Layer** — Templates that consume JSON to produce HTML pages

**Key innovations over v1.0**:
- JSON-first architecture (validate before render, not after publish)
- Deterministic title templates (no AI-generated titles — prevents cannibalization)
- Niche taxonomy system (strategic page planning, not random generation)
- Three-gate quality validation (unique answer, 40% data, engagement)
- Graduated scaling protocol with DA-based velocity limits
- Indexation kill switch (<40% indexed = stop and audit)

> **Survivorship bias notice**: Published pSEO case studies represent best-case outcomes. Results vary significantly by domain authority, niche competition, and content quality. Never promise specific traffic growth percentages.

**Deep dive**: `references/pseo-2-architecture.md`

---

## Three-Gate Quality Validation

Every pSEO page must pass all three gates before publishing:

| Gate | Test | Threshold |
|------|------|-----------|
| Gate 1: Unique Answer | Does this page answer a distinct query no other page answers? | Pass/fail — no overlap allowed |
| Gate 2: 40% Unique Data | Is ≥40% of content unique to THIS page (not template)? | ≥40% unique content words |
| Gate 3: Engagement | Would a user bookmark this page? Useful without search engines? | Pass = actionable value |

Pages scoring <40 on the quality framework should NOT be published. Hold, improve, or remove.

**Deep dive**: `references/pseo-quality-gates.md`

---

## Niche Taxonomy System

Every pSEO project starts with a structured taxonomy:

```
Niches → Audiences → Pain Points → Content Types → Subtopics → Monetization
```

The taxonomy defines the universe of pages. Build it BEFORE designing schemas or generating content. Each business builds its own taxonomy — we teach the framework, not a universal list.

**Deep dive**: `references/niche-taxonomy-builder.md`

---

## Graduated Scaling Protocol

Scale based on signals, not ambition. DA thresholds are non-negotiable:

| DA Range | Max Total Pages | Max Pages/Week | Status |
|----------|----------------|----------------|--------|
| DA < 20 | **0** | **0** | STOP — build authority first |
| DA 20-30 | 500 | 50 | Cautious |
| DA 30-40 | 2,000 | 100 | Standard |
| DA 40-60 | 5,000 | 200 | Accelerated |
| DA 60+ | 10,000+ | 500 | Full velocity |

**Indexation kill switch**: If indexation drops below 40%, STOP all publishing, alert stakeholder, audit content.

**Deep dive**: `references/pseo-scaling-protocol.md`

---

## Risk Assessment & Guardrails

### Non-Negotiable Guardrails

1. **DA threshold check** before any pSEO campaign starts
2. **Page velocity limits** enforced per DA range (see Scaling Protocol)
3. **Indexation kill switch** at <40% — automatic stop
4. **Survivorship bias disclaimer** on all case study references
5. **Content decay monitoring** — pSEO pages go stale faster than editorial
6. **Cannibalization detection** — check before publishing every batch

### Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Thin content penalty | Medium (if no quality gates) | High | Three-gate validation, 40% unique data minimum |
| Keyword cannibalization | High (at scale) | Medium | Deterministic titles, Gate 1 uniqueness check |
| Content decay | High (especially location/pricing data) | Medium | Quarterly refresh schedule, dynamic data where possible |
| Algorithm update vulnerability | Medium | High | Graduated rollout, kill switch, don't over-index on pSEO |
| Crawl budget exhaustion | Medium (at scale) | Medium | Velocity limits, sitemap management |
| Index bloat (many low-quality pages) | Medium | High | Prune pages with 0 impressions after 90 days |

### When NOT to Use pSEO

- DA < 20 (build authority with editorial content first)
- No proprietary or differentiated data available
- Niche has <100 realistic keyword variations
- No conversion path for the generated pages
- Site already has thin content issues

---

## Generative Engine Optimization (GEO)

pSEO pages must be optimized for both traditional search AND AI search engines (Perplexity, ChatGPT Search, Google AI Overviews).

**Key GEO principles for pSEO at scale**:
- Entity-first structure with schema.org markup on every page
- Concise 40-60 word answer blocks near page top (AI-extractable)
- Citation-friendly formatting (clear headings, numbered lists, data tables)
- Unique data points (AI engines prefer citing original data)
- Source attribution (clear provenance for all data)

For detailed AEO/GEO markup patterns on individual pages, see `skills/website-design/SKILL.md` → "AEO / GEO Specific Patterns" section. The patterns above focus on GEO considerations unique to pSEO at scale.

**Deep dive**: `references/pseo-2-architecture.md` → GEO section

---

## Initial Assessment

Before designing a programmatic SEO strategy, understand:

1. **Business Context**
   - What's the product/service?
   - Who is the target audience?
   - What's the conversion goal for these pages?

2. **Opportunity Assessment**
   - What search patterns exist?
   - How many potential pages?
   - What's the search volume distribution?

3. **Competitive Landscape**
   - Who ranks for these terms now?
   - What do their pages look like?
   - What would it take to beat them?

---

## Core Principles

### 1. Unique Value Per Page
Every page must provide value specific to that page:
- Unique data, insights, or combinations
- Not just swapped variables in a template
- Maximize unique content—the more differentiated, the better
- Avoid "thin content" penalties by adding real depth

### 2. Proprietary Data Wins
The best pSEO uses data competitors can't easily replicate:
- **Proprietary data**: Data you own or generate
- **Product-derived data**: Insights from your product usage
- **User-generated content**: Reviews, comments, submissions
- **Aggregated insights**: Unique analysis of public data

Hierarchy of data defensibility:
1. Proprietary (you created it)
2. Product-derived (from your users)
3. User-generated (your community)
4. Licensed (exclusive access)
5. Public (anyone can use—weakest)

### 3. Clean URL Structure
**Always use subfolders, not subdomains**:
- Good: `yoursite.com/templates/resume/`
- Bad: `templates.yoursite.com/resume/`

### 4. Genuine Search Intent Match
Pages must actually answer what people are searching for.

### 5. Scalable Quality, Not Just Quantity
Quality standards must be maintained at scale. Better to have 100 great pages than 10,000 thin ones.

### 6. Avoid Google Penalties
No doorway pages, keyword stuffing, or duplicate content across pages.

---

## The 12 Programmatic SEO Playbooks

These define **WHAT** types of pages to build. pSEO 2.0 (above) defines **HOW** to build them at scale with quality.

### 1. Templates
**Pattern**: "[Type] template" — Downloadable or interactive templates.

### 2. Curation
**Pattern**: "best [category]" — Curated lists ranking options.

### 3. Conversions
**Pattern**: "[X] to [Y]" — Format, unit, or currency converters.

### 4. Comparisons
**Pattern**: "[X] vs [Y]" — Head-to-head product comparisons.
*See also: competitor-alternatives skill*

### 5. Examples
**Pattern**: "[type] examples" — Galleries of real-world examples.

### 6. Locations
**Pattern**: "[service] in [location]" — Location-specific pages.

### 7. Personas
**Pattern**: "[product] for [audience]" — Audience-specific landing pages.

### 8. Integrations
**Pattern**: "[product] [integration]" — Integration detail pages.

### 9. Glossary
**Pattern**: "what is [term]" — Educational definitions.

### 10. Translations
Multi-language content with hreflang tags.

### 11. Directory
**Pattern**: "[category] tools" — Comprehensive category directories.

### 12. Profiles
**Pattern**: "[entity] info" — Profile pages about people/companies.

### Additional Playbooks (v2.0)

### 13. Resources
**Pattern**: "[type] for [niche]" — Idea lists, checklists, guides.

### 14. Free Tools
**Pattern**: "[niche] [tool type]" — Calculators, generators, analyzers.

### Choosing Your Playbook

| If you have... | Consider... |
|----------------|-------------|
| Proprietary data | Stats, Directories, Profiles |
| Product with integrations | Integrations |
| Design/creative product | Templates, Examples |
| Multi-segment audience | Personas |
| Local presence | Locations |
| Tool or utility product | Conversions, Free Tools |
| Content/expertise | Glossary, Curation, Resources |
| International potential | Translations |
| Competitor landscape | Comparisons |

---

## Implementation Framework

### 1. Keyword Pattern Research

**Identify the pattern** → **Validate demand** → **Assess competition**

### 2. Data Requirements

**Identify data sources** and design data schema. See `references/niche-taxonomy-builder.md` for structured taxonomy approach.

### 2.5. pSEO 2.0 Architecture (NEW)

For projects using the pSEO 2.0 approach:
1. Build niche taxonomy (see Niche Taxonomy System above)
2. Design strict JSON schemas per content type (see `references/pseo-2-architecture.md`)
3. Design deterministic title templates (NOT AI-generated)
4. Set up three-gate quality validation
5. Follow graduated scaling protocol

**Pipeline orchestration**: Use `pseo-architect` agent for end-to-end pipeline management.

### 3. Template Design

**Page structure**: Header with target keyword → Unique intro → Data-driven sections → Related pages → CTAs

**Ensuring uniqueness**: Each page needs unique value. Conditional content based on data. Use JSON schema `unique_data_threshold` field (minimum 0.4 = 40%).

### 4. Internal Linking Architecture

Hub and spoke model. No orphan pages. XML sitemap for all pages. Breadcrumbs with structured data.

### 5. Indexation Strategy

Prioritize important pages. Manage crawl budget. Separate sitemaps by page type. Monitor indexation rate against kill switch threshold (40%).

---

## Quality Checks

### Three-Gate Validation (v2.0)

All pSEO pages must pass:
1. **Gate 1: Unique Answer** — distinct query answered
2. **Gate 2: 40% Unique Data** — sufficient differentiation
3. **Gate 3: Engagement** — genuinely useful without search engines

See `references/pseo-quality-gates.md` for scoring rubrics and automated checks.

### Pre-Launch Checklist

**Content quality**:
- [ ] Each page provides unique value (Gate 1 passed)
- [ ] ≥40% unique content per page (Gate 2 passed)
- [ ] Useful standalone (Gate 3 passed)

**Technical SEO**:
- [ ] Unique titles (deterministic templates, not AI-generated)
- [ ] Proper heading structure
- [ ] Schema markup implemented
- [ ] Canonical tags correct
- [ ] Page speed acceptable

**Internal linking**:
- [ ] Connected to site architecture
- [ ] No orphan pages
- [ ] Breadcrumbs implemented

**Indexation**:
- [ ] In XML sitemap
- [ ] Crawlable
- [ ] Kill switch monitoring configured

### Monitoring Post-Launch

**Track**: Indexation rate, rankings by pattern, traffic by pattern, engagement, conversions

**Watch for**: Thin content warnings, ranking drops, manual actions, crawl errors, indexation rate < 40%

---

## Common Mistakes to Avoid

### Classic Mistakes (v1.0)
- **Thin Content**: Just swapping variables in identical content
- **Keyword Cannibalization**: Multiple pages targeting same keyword
- **Over-Generation**: Creating pages with no search demand
- **Poor Data Quality**: Outdated, incorrect, or missing data
- **Ignoring User Experience**: Pages exist for Google, not users

### New Mistakes (v2.0)
- **Mixing layers**: Combining data, schema, and rendering in one step
- **AI-generated titles**: Causes cannibalization at scale — use deterministic templates
- **Scaling too fast**: Publishing thousands of pages before proving concept works
- **Ignoring cannibalization**: Not checking for overlap before each batch
- **No kill switch**: Publishing without indexation monitoring = flying blind
- **Content decay neglect**: pSEO pages go stale faster than editorial content

---

## Output Format

### Strategy Document

**Opportunity Analysis** → **Implementation Plan** → **Content Guidelines**

### Page Template

**URL structure** → **Title template** (deterministic) → **Meta description template** → **JSON schema** → **Content outline** → **Schema markup**

### Launch Checklist

Specific pre-launch checks including all three quality gates.

---

## Questions to Ask

If you need more context:
1. What keyword patterns are you targeting?
2. What data do you have (or can acquire)?
3. How many pages are you planning to create?
4. What does your site authority look like? (DA score)
5. Who currently ranks for these terms?
6. What's your technical stack for generating pages?

---

## Related Skills

- **seo-mastery**: Foundation SEO knowledge (prerequisite)
- **schema-markup**: Structured data for pSEO templates
- **copywriting**: Non-templated copy portions
- **analytics-attribution**: Performance measurement and indexation tracking
- **content-strategy**: Niche taxonomy design and content planning
- **website-design**: HTML/Tailwind template rendering for pSEO pages
- **competitor-alternatives**: Comparison page frameworks

## References

- `references/pseo-implementation-guide.md` - Step-by-step pSEO implementation guide
