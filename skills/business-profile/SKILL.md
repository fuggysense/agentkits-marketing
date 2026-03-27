---
name: business-profile
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: core
difficulty: beginner
description: "Interactive business context profile builder. Walks through 30 questions via AskUserQuestion, outputs structured JSON to clients/<project>/context-profile.json. Foundation layer for all downstream skills — every agent reads this first."
triggers:
  - business profile
  - context profile
  - project profile
  - build profile
  - onboard business
prerequisites: []
related_skills:
  - client-onboarding
  - offer-builder
  - brand-building
  - persona-builder
agents: []
mcp_integrations:
  optional: []
success_metrics:
  - fields_completed
  - json_validity
output_schema: context-profile
---

## Graph Links
- **Feeds into:** [[client-onboarding]], [[offer-builder]], [[copywriting]], [[campaign-runner]], [[brand-building]]
- **Draws from:** (independent — interview flow)
- **Related:** [[persona-builder]]

# Business Context Profile Builder

You build a structured JSON context profile for a business. This profile is the foundation layer — every skill, agent, and campaign reads it to understand WHO this business is before producing anything.

## Core Philosophy

Without context, AI gives generic answers. With it, the AI can say: "Given that you're a $8k/month SaaS agency with 4 clients targeting e-commerce brands, here's what I'd do next." This profile enables that personalization.

**Principles:**
- Ask in sections, not all 30 at once — one section per AskUserQuestion
- Accept partial answers — mark unknowns as `null` in JSON, never invent
- Works for new projects (create) AND existing projects (update)
- Output is ONLY the JSON file — no extra markdown or commentary files

---

## Mode Detection

On invocation:

1. **Check for existing profile:** Read `clients/<project>/context-profile.json`
   - If exists → **Update mode**: Show current profile summary, ask which sections to update
   - If not → **Create mode**: Run full interview from Section 1

2. **Check for existing project files:** If `clients/<project>/icp.md`, `offer.md`, etc. have content (not just template defaults), pre-populate what you can from those files and SKIP those questions. Tell the user: "I pulled X fields from your existing project files. I'll only ask what's missing."

---

## Interview Flow

Ask one section at a time using AskUserQuestion. Present all questions in the section as a numbered list. User answers in plain text — numbers don't need to match, just answer in order.

### Section 1: Business Identity
1. What is the name of your business?
2. Do you have a slogan or tagline?
3. When was it founded?
4. Where is your business headquartered? Do you operate in other regions?
5. Do you serve clients internationally?
6. In 1-2 sentences, what does your business do?
7. What is your mission or big picture goal?

### Section 2: Products & Services
8. What services or products do you offer? (Include deliverables and value for each)
9. What are your current offers, products, or programs? (Include pricing if comfortable)
10. What is your business model? (e.g., SaaS, service-based, info product, agency, marketplace, e-commerce)

### Section 3: People
11. Who are the founders? What are their roles and brief bios?
12. How is your team structured? Do you use contractors or employees? Where are they based?

### Section 4: Market & Customers
13. Who are your ideal clients? (Industry, company size, monthly revenue, problems they have)
14. Who are your top 2-3 competitors? What do they do differently?
15. How do customers currently find you? (Referrals, ads, organic, cold outreach, partnerships, etc.)
16. What does your sales process look like? (Self-serve, demo call, consultation, proposal, etc.)

### Section 5: Operations
17. What tools or platforms are core to your operations? (CRM, email tool, project management, etc.)
18. What are your current goals and KPIs?

### Section 6: Growth & Status
19. Are you pre-launch or launched? When is/was the launch? How ready are you?
20. What's your current monthly revenue range? (Even a rough bracket helps: <$5K, $5-20K, $20-50K, $50K+)
21. What growth stage are you in? (Bootstrapping, seed, scaling, established)
22. What is your biggest current challenge or bottleneck?

### Section 7: Brand & Content
23. What tone best describes your brand? (Formal, casual, witty, authoritative, friendly, provocative, etc.)
24. What content do you already produce? (Blog, video, podcast, newsletter, social posts)
25. Do you have existing brand assets? (Logo, brand colors, style guide, photography)

### Section 8: Proof & Differentiation
26. What makes your business unique from others in your space?
27. What measurable results do your clients get? (Specific numbers, percentages, timeframes)
28. What have some past clients said about your business? (Testimonials, reviews, quotes)

### Section 9: Vision & Values
29. What core values guide your work?
30. What inspired you to start this business? (Origin story — 2-3 sentences)

---

## Post-Interview Processing

After all sections are answered:

1. **Parse answers** into the JSON schema below
2. **Cross-reference** with existing project files (icp.md, offer.md) — if the profile reveals info that enriches those files, note it but do NOT auto-update them
3. **Write** the JSON to `clients/<project>/context-profile.json`
4. **Show summary** — compact table of what was captured vs what's still null
5. **Suggest next steps** — which null fields matter most and how to fill them

---

## JSON Output Schema

```json
{
  "business_name": "",
  "tagline": "",
  "founded": "",
  "headquarters": "",
  "operational_locations": [],
  "serves_clients_internationally": false,
  "description": "",
  "mission": "",
  "business_model": "",
  "core_services": [
    {
      "name": "",
      "description": "",
      "deliverables": [],
      "value_proposition": ""
    }
  ],
  "current_offers": [
    {
      "name": "",
      "price": "",
      "description": ""
    }
  ],
  "ideal_clients": {
    "industries": [],
    "company_size": "",
    "revenue_threshold": "",
    "pain_points": []
  },
  "competitors": [
    {
      "name": "",
      "differentiator": ""
    }
  ],
  "founders": [
    {
      "name": "",
      "role": "",
      "bio": ""
    }
  ],
  "team": {
    "structure": "",
    "type": "",
    "size": "",
    "locations": []
  },
  "tools_and_platforms": [],
  "goals_and_kpis": {
    "primary_goal": "",
    "kpis": [],
    "timeline": ""
  },
  "launch_status": {
    "stage": "",
    "launch_date": "",
    "readiness": ""
  },
  "revenue": {
    "range": "",
    "growth_stage": "",
    "primary_source": ""
  },
  "sales_process": {
    "acquisition_channels": [],
    "sales_model": "",
    "avg_deal_size": "",
    "sales_cycle": ""
  },
  "biggest_challenge": "",
  "brand_identity": {
    "tone": "",
    "content_types": [],
    "existing_assets": []
  },
  "unique_differentiator": "",
  "measurable_results": [],
  "testimonials": [
    {
      "quote": "",
      "attribution": ""
    }
  ],
  "core_values": [],
  "origin_story": "",
  "profile_version": "1.0",
  "last_updated": ""
}
```

### Field Rules
- **Strings:** Use `""` for unanswered, never invent content
- **Arrays:** Use `[]` for unanswered, populate with as many entries as the user provides
- **Booleans:** Use `false` as default, only set `true` if explicitly confirmed
- **Nested objects:** Include the object structure even if all fields are empty
- **`last_updated`:** Set to current date in ISO format (YYYY-MM-DD)
- **`profile_version`:** Increment minor version on updates (1.0 → 1.1 → 1.2)

---

## Update Mode

When `context-profile.json` already exists:

1. Read the existing JSON
2. Show a summary: "Here's your current profile (30 fields, X populated, Y empty)"
3. Ask: "Which sections do you want to update? (1-9, or 'all', or 'gaps' to fill empty fields only)"
4. Only ask questions for selected sections
5. Merge new answers into existing JSON (don't wipe fields the user didn't update)
6. Bump `profile_version` and `last_updated`

---

## Integration with Other Skills

This profile is the FIRST file any skill should read when loading project context. The context gate in CLAUDE.md should be updated to include:

```
Load order:
1. context-profile.json (business identity — WHO)
2. voice/<person>/ (writing voice — HOW)
3. icp.md, offer.md, brand-voice.md (marketing specifics — WHAT)
```

Skills that benefit most from this profile:
- **copywriting** — knows the business model, tone, and proof points
- **campaign-runner** — knows channels, goals, and budget range
- **offer-builder** — knows existing offers, pricing, and market position
- **persona-builder** — knows ideal clients, pain points, and competitors
- **content-strategy** — knows content types, brand tone, and growth stage

---

## Error Handling

- If user says "skip" for a section → leave those fields as defaults, move to next section
- If user says "I'll come back to this" → save what's collected so far, note incomplete sections
- If JSON already exists and user runs create mode → warn and offer: overwrite, update, or cancel
- If no project folder exists → create it first (scaffold from template) or error with instructions
