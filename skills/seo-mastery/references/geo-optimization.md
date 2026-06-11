## Graph Links
- **Parent skill:** [[seo-mastery]]
- **Related skills:** [[schema-markup]], [[programmatic-seo]], [[website-design]]
- **Used by agents:** [[researcher]]

# Generative Engine Optimization (GEO)

Optimize content for AI search engines — Google AI Overviews, ChatGPT Search, Perplexity, Claude search — in addition to traditional SERP ranking.

## What GEO Is

AI search engines don't just rank pages — they extract, cite, and synthesize content into direct answers. GEO ensures your content gets cited as a source, not buried. A page can rank #1 on Google but never get cited by Perplexity if it lacks the right structure.

**Key difference from traditional SEO:**
- Traditional SEO: Optimize for ranking position
- GEO: Optimize for citation and extraction by AI engines

---

## GEO Audit Checklist (Per Page)

Score each item 0-2 (0 = missing, 1 = partial, 2 = strong). Total /20 = GEO Readiness Score.

| # | Check | What to Look For | Score |
|---|-------|------------------|-------|
| 1 | **Answer block** | 40-60 word direct answer near page top, clearly answering the primary query | /2 |
| 2 | **Entity markup** | Primary entity wrapped in schema.org markup (Organization, Product, Person, etc.) | /2 |
| 3 | **FAQ schema** | JSON-LD FAQ schema for common questions on the page | /2 |
| 4 | **Speakable schema** | `speakable` property on sections suitable for voice/AI extraction | /2 |
| 5 | **Citation-friendly formatting** | Clear headings, numbered lists, data tables — easy for AI to reference | /2 |
| 6 | **Unique data points** | Proprietary stats, original research, or first-party data (not generic claims) | /2 |
| 7 | **Source attribution** | Data sources cited — AI engines prefer content with clear provenance | /2 |
| 8 | **Quotable one-liners** | Clear, self-contained statements that can be extracted as citations | /2 |
| 9 | **Topical authority signals** | Author credentials, org expertise, links to authoritative sources | /2 |
| 10 | **Structured comparisons** | Tables, pros/cons, vs-format content that AI engines love to cite | /2 |

**Scoring:**
- **16-20:** GEO-ready — high citation potential
- **10-15:** Partially optimized — missing key elements
- **0-9:** Not GEO-optimized — AI engines will skip this content

---

## Implementation Patterns

### 1. Answer Block (Top Priority)

Place a concise 40-60 word answer near the top of the page that directly addresses the primary search query. AI engines extract this preferentially.

```html
<div itemscope itemtype="https://schema.org/Answer">
  <p itemprop="text">
    [Direct answer to the page's primary question in 40-60 words.
    Include the key fact, number, or conclusion. Make it self-contained
    — a reader should understand the core answer from this paragraph alone.]
  </p>
</div>
```

### 2. Entity Markup

Wrap brand, product, and person names in schema.org markup so AI engines understand what entities the page is about.

```html
<span itemscope itemtype="https://schema.org/Organization">
  <span itemprop="name">1UP Sales AI</span>
</span>
```

### 3. FAQ Schema (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is [topic]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[40-60 word direct answer]"
      }
    }
  ]
}
```

**Note:** Google restricted FAQ rich results in Aug 2023 to government and health sites. But FAQ schema still helps AI engines (Perplexity, ChatGPT) extract structured Q&A. Include it for GEO even if it won't show rich snippets on Google.

### 4. Speakable Schema

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".answer-block", ".key-takeaway"]
  }
}
```

### 5. Citation-Friendly Structure

**Do:**
- Use numbered lists for processes/steps
- Use data tables for comparisons
- Use clear H2/H3 headings that state the topic (not clever/vague)
- Include specific numbers, percentages, dates
- Write self-contained paragraphs (each makes sense alone)

**Don't:**
- Long unbroken paragraphs
- Vague headings ("Why it matters")
- Claims without data ("industry-leading")
- Content that requires reading the full page to understand any part

### 6. Unique Data Points

AI engines preferentially cite original data. Include:
- First-party statistics from your product/clients
- Original research or surveys
- Calculated benchmarks from proprietary data
- Case study metrics with specific numbers

Example: "Our clients saw a 58% → 100% contact rate improvement over 8 weeks" is citable. "We help businesses improve their contact rates" is not.

---

## GEO Optimization Workflow

When running `/seo:geo` on a page:

1. **Fetch the page** (WebFetch or Chrome MCP snapshot)
2. **Score against the 10-point checklist** above
3. **Identify gaps** — which elements are missing or weak?
4. **Generate fixes:**
   - Write an answer block for the page's primary query
   - Generate FAQ schema JSON-LD for 3-5 relevant questions
   - Suggest where to add entity markup
   - Identify quotable one-liners to add or restructure
   - Flag content that lacks data/specificity
5. **Output:** GEO score + prioritized recommendations + generated code snippets

---

## AI Search Visibility Check

If DataForSEO MCP is available, check:
- `serp_google_organic_live` — look for AI Overview presence in SERP features
- Check for "featured snippet" and "people also ask" positions (precursors to AI citation)
- If DataForSEO has LLM mention tracking, check if the domain is cited by AI engines

If DataForSEO is not available:
- Manual check: search the query on Perplexity and ChatGPT, see if the page is cited
- Flag: "DataForSEO not configured — manual AI visibility check recommended"

---

## GEO by Page Type

| Page Type | Priority GEO Elements | Why |
|-----------|----------------------|-----|
| Homepage | Entity markup, answer block, org schema | AI engines need to understand who you are |
| Product/Service | FAQ schema, comparison tables, pricing data | Most likely to be cited in "best X" queries |
| Blog/Article | Answer block, unique data, source attribution | Content pages are primary citation targets |
| Comparison | Structured tables, pros/cons, verdict | AI engines love structured comparisons |
| Landing Page | Usually low GEO priority | Conversion-focused, not citation-focused |
| pSEO Pages | Entity markup, FAQ schema, data tables (batch-apply) | See `programmatic-seo` skill for scale patterns |

---

## References

- `skills/programmatic-seo/SKILL.md` → GEO section (batch patterns for pages at scale)
- `skills/programmatic-seo/references/pseo-2-architecture.md` → GEO principles
- `skills/website-design/SKILL.md` → AEO/GEO specific HTML patterns
- `skills/schema-markup/SKILL.md` → Schema implementation details
