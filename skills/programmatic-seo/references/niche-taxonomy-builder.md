## Graph Links
- **Parent skill:** [[programmatic-seo]]
- **Sibling references:** [[pseo-2-architecture]], [[pseo-implementation-guide]], [[pseo-quality-gates]], [[pseo-scaling-protocol]]
- **Related skills:** [[seo-mastery]]

# Niche Taxonomy Builder

Framework for building structured niche taxonomies for pSEO 2.0 campaigns. Every pSEO project starts with a taxonomy — it defines what pages exist and how they relate.

> **Important**: We do NOT ship a universal taxonomy. Each business builds its own. This guide teaches how.

---

## What is a Niche Taxonomy?

A structured hierarchy that maps:
- **Niches** (market segments you serve)
- **Audiences** (who searches within each niche)
- **Pain Points** (what problems they have)
- **Content Types** (what page formats answer their queries)
- **Subtopics** (specific variations within each niche)
- **Monetization** (how each niche connects to revenue)

### Why Taxonomy First?

Without a taxonomy:
- You generate random pages with no strategic coherence
- Cannibalization is inevitable (no map = no territory)
- Internal linking has no structure
- You can't measure performance by segment

---

## Taxonomy Structure

### YAML Schema

```yaml
taxonomy:
  name: "[Business] pSEO Taxonomy v1"
  created: "YYYY-MM-DD"
  approved_by: "[Name]"

  niches:
    - id: "niche-slug"
      name: "Niche Name"
      description: "One-line description"
      search_volume_estimate: "high/medium/low"
      competition: "high/medium/low"

      audiences:
        - id: "audience-slug"
          name: "Audience Name"
          role: "Job title or persona"
          intent: "informational/commercial/transactional"

      pain_points:
        - id: "pain-slug"
          description: "The specific problem"
          urgency: "high/medium/low"

      content_types:
        - type: "comparison|location|glossary|resource|tool|directory"
          pattern: "URL pattern template"
          title_template: "Title generation template"
          estimated_pages: 50

      subtopics:
        - id: "subtopic-slug"
          name: "Subtopic Name"
          keywords: ["keyword1", "keyword2"]
          parent: "niche-slug"

      monetization:
        model: "direct|affiliate|lead-gen|brand"
        conversion_path: "How this niche connects to revenue"
```

---

## Building Your Taxonomy: 6-Step Process

### Step 1: Seed Niches from Business Context

**Input**: Product, ICP, existing content, competitors
**Output**: Initial niche list (10-30 niches)

Questions to answer:
1. What categories does your product serve?
2. What industries do your customers come from?
3. What do your competitors rank for?
4. What search patterns have volume in your space?

**MCP integration**: Use Semrush `keyword_ideas` or DataForSEO for seed keyword expansion.

### Step 2: Map Audiences per Niche

For each niche, identify:
- Who searches for this? (role, seniority, industry)
- What's their intent? (learning, comparing, buying)
- What format do they expect? (list, guide, tool, comparison)

### Step 3: Extract Pain Points

For each audience-niche pair:
- What problem are they trying to solve?
- How urgent is it?
- What language do they use to describe it?

**Source**: Customer interviews, support tickets, Reddit/community forums, "People Also Ask" data.

### Step 4: Assign Content Types

Map each niche to the best pSEO playbook(s):

| Niche Characteristic | Best Playbook |
|---------------------|--------------|
| Location-dependent service | Location pages |
| Multiple competing products | Comparison pages |
| Technical concepts | Glossary pages |
| Tool/calculator need | Resource/tool pages |
| Many sub-categories | Directory pages |
| Integration ecosystem | Integration pages |

### Step 5: Generate Subtopics

Expand each niche into specific subtopics:
- Use keyword research tools for long-tail variations
- Map PAA (People Also Ask) questions
- Identify seasonal or trending subtopics
- Cross-reference with competitor content gaps

### Step 6: Validate & Prune

Before approval, check:
- [ ] Every niche has ≥1 content type assigned
- [ ] No two niches target the same keywords
- [ ] Estimated page count is realistic for your DA
- [ ] Each niche has a clear monetization path
- [ ] Total pages align with scaling protocol limits

---

## Example Taxonomies

### Example 1: SaaS Project Management Tool

```yaml
niches:
  - id: "pm-by-industry"
    name: "Project Management by Industry"
    content_types:
      - type: "persona"
        pattern: "/project-management-for-{industry}/"
        title_template: "Project Management for {Industry}: Complete Guide ({year})"
        estimated_pages: 25
    subtopics:
      - { id: "pm-construction", name: "Construction PM", keywords: ["construction project management", "building project tracker"] }
      - { id: "pm-marketing", name: "Marketing PM", keywords: ["marketing project management", "campaign tracker"] }

  - id: "pm-comparisons"
    name: "PM Tool Comparisons"
    content_types:
      - type: "comparison"
        pattern: "/{product}-vs-{competitor}/"
        title_template: "{Product} vs {Competitor}: Honest Comparison ({year})"
        estimated_pages: 40
```

### Example 2: Local Services Marketplace

```yaml
niches:
  - id: "plumbers-by-city"
    name: "Plumbers by City"
    content_types:
      - type: "location"
        pattern: "/plumbers/{city}-{state}/"
        title_template: "Best Plumbers in {City}, {State} — {year} Reviews & Prices"
        estimated_pages: 500
    subtopics:
      - { id: "emergency-plumber", name: "Emergency Plumbers", keywords: ["24 hour plumber", "emergency plumber near me"] }
      - { id: "plumber-cost", name: "Plumber Costs", keywords: ["plumber cost", "how much does a plumber charge"] }
```

### Example 3: B2B Software Directory

```yaml
niches:
  - id: "crm-alternatives"
    name: "CRM Alternatives"
    content_types:
      - type: "comparison"
        pattern: "/{product}-alternatives/"
        title_template: "Best {Product} Alternatives for {use_case} ({year})"
        estimated_pages: 30
      - type: "directory"
        pattern: "/best-{category}-software/"
        title_template: "Best {Category} Software: Top {count} Tools Reviewed ({year})"
        estimated_pages: 15
```

---

## Taxonomy Maintenance

### When to Update
- New product features unlock new niches
- Competitor analysis reveals gaps
- Performance data shows winning/losing niches
- Seasonal keyword trends shift
- New market segments emerge

### Update Process
1. Propose taxonomy changes
2. Check for cannibalization with existing pages
3. Get HITL approval (taxonomy changes = strategy changes)
4. Update schemas if content types change
5. Generate new pages following scaling protocol

---

## Integration with MCP Data Sources

| Step | MCP Server | Use |
|------|-----------|-----|
| Seed niches | Semrush `keyword_ideas` | Find keyword patterns |
| Validate volume | Semrush `keyword_overview` | Check search demand |
| Competitor gaps | Semrush `domain_overview` | See what competitors rank for |
| SERP analysis | DataForSEO `serp_api` | Understand current results |
| Performance tracking | GSC `get_search_analytics` | Monitor after launch |

---

## Taxonomy Approval Checklist

Before the taxonomy is approved for pipeline execution:

- [ ] Every niche has clear business relevance
- [ ] No keyword cannibalization between niches
- [ ] Total page count aligns with DA (see scaling protocol)
- [ ] Content types are realistic for available data
- [ ] Monetization path exists for each niche
- [ ] Taxonomy reviewed by stakeholder (HITL gate)
- [ ] Saved to `clients/<project>/campaigns/pseo-<slug>/taxonomy.yaml`
