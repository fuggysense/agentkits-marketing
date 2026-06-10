# Perplexity Research Prompt Template

> Perplexity excels at: factual data, market research, cited sources, competitor analysis, demographics.
> Use for: points 1, 7, 8, 9, 10, 11, 12 of the avatar breakdown.

---

## Template (fill placeholders, then copy-paste to Perplexity)

```
I'm building a detailed advertising avatar for a specific sub-segment of buyers in the {geography} market.

**Product/Service:** {product_description}
**Target market:** {market_description}
**This specific avatar:** {avatar_description}

I need real-world data to build a 12-point avatar profile. For each point, cite your sources.

1. **Demographics** — What are the typical age, gender, income, and location characteristics of {avatar_description} in {geography}? Be specific to this sub-segment, not the general market.

2. **Day-to-day struggles** — What are the concrete daily struggles this person faces related to {problem_domain}? Not abstract pain points. Real daily behaviors, thoughts, and frustrations. Search for forum posts, Reddit threads, or survey data from {geography}.

3. **Image they project** — What public persona does this demographic typically maintain? What do they want colleagues, friends, and family to see?

4. **Status they aspire to** — What concrete status markers (material, social, professional) does this segment aspire to in {geography}? What does "making it" look like to them?

5. **How {product_category} helps them achieve status** — How does solving {problem} specifically help this person achieve the status in point 4?

6. **Beliefs we must overcome** — What are the top 3 beliefs that prevent this person from buying {product_category}? Include evidence for why each belief exists. Search for objections in forums, social media, and review sites.

7. **Other solutions they've tried** — What has this audience in {geography} already tried to solve {problem}? Be specific to the local market. Include both free and paid approaches.

8. **Why those solutions failed** — For each solution in point 7, what specifically went wrong? Search for complaints, negative reviews, and forum discussions in {geography}.

9. **Similar products/services they've considered** — What competing products, services, or approaches exist in {geography} for this audience? Name specific companies or categories.

10. **Why those fell short** — For each product in point 9, what are the common complaints? Search for reviews, forum posts, and social media discussions.

11. **Market awareness (Schwartz framework)** — Is this avatar Unaware, Problem-Aware, Solution-Aware, Product-Aware, or Most Aware? Provide evidence for your assessment based on the search behavior and language they use.

12. **Market sophistication** — On a scale of 1-5, how sophisticated is this audience about marketing claims in {product_category}? How many competing messages have they seen? How cynical are they?

Focus on {geography}-specific data. Cite all sources.
```

## Placeholder Guide

| Placeholder | Fill with | Source |
|------------|-----------|--------|
| `{geography}` | e.g., "Singapore" | icp.md → Geography |
| `{product_description}` | One-line description | offer.md → One-Line Description |
| `{market_description}` | Target market summary | icp.md → Industry + Demographics |
| `{avatar_description}` | Avatar hypothesis name + key differentiator | From Phase 1 hypothesis table |
| `{problem_domain}` | The core problem area | buyer-profile.md → Core Problem |
| `{product_category}` | Category name | offer.md → category or industry |
| `{problem}` | The specific problem this avatar faces | From Phase 1 hypothesis |
