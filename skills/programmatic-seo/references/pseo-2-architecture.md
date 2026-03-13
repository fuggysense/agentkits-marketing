# pSEO 2.0 Architecture

Based on schema-driven generation patterns. Case study references include survivorship bias disclaimer — see Guardrails.

> **Survivorship Bias Notice**: Published pSEO case studies (including Ward/Byword's 466% growth) represent best-case outcomes from practitioners selling pSEO tools. Results vary significantly by domain authority, niche competition, and content quality. Never promise specific traffic growth percentages.

---

## Three-Layer Separation

pSEO 2.0 separates concerns into three distinct layers. Mixing layers is the #1 architectural mistake.

### Layer 1: Data (Taxonomy + Variables)
- Structured niche taxonomy (see `niche-taxonomy-builder.md`)
- Variable definitions per content type
- Data sources and refresh schedules
- **Owned by**: researcher agent + content-strategy skill

### Layer 2: Schema (JSON Structure)
- Strict JSON schemas per content type
- Deterministic title templates (NOT AI-generated titles)
- Field validation rules
- Required vs optional sections
- **Owned by**: copywriter agent + programmatic-seo skill

### Layer 3: Renderer (Page Output)
- HTML/Tailwind templates that consume JSON
- Conditional display logic
- Schema markup injection
- Internal linking automation
- **Owned by**: website-design skill (Creation mode)

**Why separate?** When layers are mixed, you can't validate, scale, or debug independently. JSON-first means every page passes schema validation before rendering — catching quality issues at generation, not after publishing.

---

## JSON Schema Design Patterns

### Pattern 1: Location Pages
```json
{
  "$schema": "location-page-v1",
  "title_template": "{service} in {city}, {state} — {year} Guide",
  "fields": {
    "service": { "type": "string", "from": "taxonomy.services" },
    "city": { "type": "string", "from": "taxonomy.locations" },
    "state": { "type": "string", "derived": "city.state" },
    "year": { "type": "number", "auto": "current_year" },
    "local_stats": { "type": "object", "required": true, "min_fields": 3 },
    "providers": { "type": "array", "min_items": 5, "unique_data": true },
    "faq": { "type": "array", "min_items": 3, "max_items": 7 }
  },
  "unique_data_threshold": 0.4
}
```

### Pattern 2: Comparison Pages
```json
{
  "$schema": "comparison-page-v1",
  "title_template": "{product_a} vs {product_b}: Honest Comparison ({year})",
  "fields": {
    "product_a": { "type": "object", "from": "taxonomy.products" },
    "product_b": { "type": "object", "from": "taxonomy.products" },
    "feature_comparison": { "type": "array", "min_items": 8 },
    "pricing_comparison": { "type": "object", "required": true },
    "verdict": { "type": "object", "required": true },
    "use_case_recommendations": { "type": "array", "min_items": 3 }
  },
  "unique_data_threshold": 0.5
}
```

### Pattern 3: Resource/Tool Pages
```json
{
  "$schema": "resource-page-v1",
  "title_template": "Free {tool_type} for {niche}: {specific_use}",
  "fields": {
    "niche": { "type": "string", "from": "taxonomy.niches" },
    "tool_type": { "type": "string", "from": "taxonomy.tool_types" },
    "specific_use": { "type": "string", "deterministic": true },
    "content_sections": { "type": "array", "min_items": 4 },
    "data_points": { "type": "array", "min_items": 5, "unique_data": true },
    "related_resources": { "type": "array", "min_items": 3 }
  },
  "unique_data_threshold": 0.4
}
```

### Pattern 4: Glossary/Definition Pages
```json
{
  "$schema": "glossary-page-v1",
  "title_template": "What is {term}? Definition, Examples & Guide",
  "fields": {
    "term": { "type": "string", "from": "taxonomy.terms" },
    "definition": { "type": "string", "max_length": 160, "required": true },
    "extended_explanation": { "type": "string", "min_length": 200 },
    "examples": { "type": "array", "min_items": 2 },
    "related_terms": { "type": "array", "min_items": 3, "from": "taxonomy.terms" },
    "faq": { "type": "array", "min_items": 3 }
  },
  "unique_data_threshold": 0.6
}
```

---

## Deterministic Title Templates

**Critical rule**: Titles are generated from templates with variables, NOT by AI. This prevents:
- Cannibalization (AI may generate similar titles for different pages)
- Inconsistency (AI titles vary in format and quality)
- Loss of control (can't predict or audit AI-generated titles at scale)

### Title Template Examples

| Content Type | Template | Example Output |
|-------------|----------|----------------|
| Location | `{service} in {city}, {state} — {year} Guide` | "Plumbers in Austin, TX — 2026 Guide" |
| Comparison | `{product_a} vs {product_b}: Honest Comparison ({year})` | "HubSpot vs Salesforce: Honest Comparison (2026)" |
| Alternative | `Best {product} Alternatives for {use_case} ({year})` | "Best Notion Alternatives for Project Management (2026)" |
| Integration | `{product_a} + {product_b} Integration: How to Connect` | "Slack + Asana Integration: How to Connect" |
| Glossary | `What is {term}? Definition, Examples & Guide` | "What is pSEO? Definition, Examples & Guide" |
| Resource | `Free {tool_type} for {niche}: {specific_use}` | "Free ROI Calculator for SaaS: Measure Marketing Spend" |

### Anti-Patterns
- AI-generated titles (unpredictable, may cannibalize)
- Titles without year modifiers (look stale)
- Titles >60 characters (truncated in SERPs)
- Titles without differentiating variable (all look the same)

---

## Concurrent Generation Architecture

For large-scale generation (500+ pages), structure batch processing:

### Batch Processing Model
```
Taxonomy (approved) → Schema Validation → Batch Queue
                                              ↓
                                    ┌─────────────────┐
                                    │  Batch 1 (50)   │→ Quality Gate → Publish Queue
                                    │  Batch 2 (50)   │→ Quality Gate → Publish Queue
                                    │  Batch 3 (50)   │→ Quality Gate → Publish Queue
                                    │  ...             │
                                    └─────────────────┘
                                              ↓
                                    Failed Pages → Regeneration Queue
```

### Batch Size Guidelines
| DA Range | Max Batch Size | Cool-Down Period |
|----------|---------------|-----------------|
| DA 20-30 | 50 pages | 2 weeks between batches |
| DA 30-40 | 100 pages | 1 week between batches |
| DA 40-60 | 200 pages | 3-5 days between batches |
| DA 60+ | 500 pages | Monitor crawl stats |

---

## Generative Engine Optimization (GEO)

pSEO pages must be optimized for both traditional search AND AI search engines (Perplexity, ChatGPT Search, Google AI Overviews).

### GEO Principles for pSEO at Scale

1. **Entity-First Structure**: Each page should clearly define its primary entity with schema.org markup
2. **Concise Answer Blocks**: Include a 40-60 word direct answer near the top of each page (extractable by AI)
3. **Citation-Friendly Formatting**: Use clear headings, numbered lists, and data tables that AI can reference
4. **Unique Data Points**: Pages with proprietary data get cited more by AI engines
5. **Source Attribution**: Cite your data sources — AI engines prefer content with clear provenance

### AEO/GEO Markup Patterns

For detailed AEO/GEO markup implementation on individual pages, see `skills/website-design/SKILL.md` → "AEO / GEO Specific Patterns" section. The patterns above focus on GEO considerations unique to pSEO at scale:

- **Batch-apply entity markup** across all pages via JSON schema (include `@type` field in every schema)
- **Speakable schema** for answer blocks (include in page schema definition)
- **FAQ schema** on every page type (already in JSON patterns above)

---

## Tech Stack Options (Strategy Only)

We provide architecture and schemas. Implementation uses the client's stack. Common patterns:

| Approach | Best For | Complexity |
|----------|----------|-----------|
| Headless CMS + SSG | Most pSEO projects | Medium |
| Database + Next.js/Astro | Custom data-heavy projects | High |
| Spreadsheet + Webflow | Simple, <500 pages | Low |
| Custom script + static HTML | Maximum control | Medium |

**Our deliverable**: JSON schemas, title templates, taxonomy, quality gates, rollout plan. Client's dev team handles rendering and deployment.
