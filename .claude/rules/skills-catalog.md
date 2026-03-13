# Skills Catalog

Activate relevant skills during tasks.

## Enterprise Skill System (v2.0)

### Skill Selection
- **Registry:** `.claude/skills/skills-registry.json` - Central skill catalog with semantic metadata
- **Dependencies:** `.claude/skills/dependency-graph.md` - Skill prerequisite relationships
- **Selector:** `/skills:select [task]` - Intelligent skill matching

### Reference Data
- **Benchmarks:** `.claude/skills/common/data/benchmark-metrics.yaml` - Industry standards
- **Formulas:** `.claude/skills/common/data/conversion-formulas.yaml` - Metric calculations
- **MCP Matrix:** `.claude/skills/common/data/mcp-mapping-matrix.yaml` - Data source mappings

### Copy Templates
- **Headlines:** `.claude/skills/common/templates/headline-formulas.md`
- **CTAs:** `.claude/skills/common/templates/cta-library.md`
- **Subject Lines:** `.claude/skills/common/templates/email-subject-lines.md`

### Output Schemas
Standardized outputs: `.claude/skills/schemas/output-schemas.yaml`
- `cro-analysis` - CRO recommendations
- `content-plan` - Content strategy
- `campaign-brief` - Campaign planning
- `seo-audit` - SEO analysis
- `email-sequence` - Email design
- `ab-test-plan` - Test design

## Core Skills
- `marketing-fundamentals` - Core marketing concepts, funnel stages
- `marketing-psychology` - 70+ mental models for marketing
- `marketing-ideas` - 140+ proven SaaS marketing strategies
- `seo-mastery` - Search optimization, keyword research
- `social-media` - Social strategies, platform best practices
- `linkedin-optimization` - LinkedIn profile audit, algorithm, content types, creator mode, B2B sales, engagement, newsletters, banner design
- `email-marketing` - Email automation, deliverability
- `paid-advertising` - Ad platform strategies, ROAS optimization
- `content-strategy` - Content planning, editorial calendars
- `analytics-attribution` - Performance measurement, attribution models
- `brand-building` - Brand strategy, voice, positioning
- `problem-solving` - Marketing problem-solving techniques
- `client-onboarding` - Guided project onboarding (scaffold, interview, enrich, validate, activate)
- `document-skills` - DOCX, PDF, PPTX, XLSX document creation

## CRO Skills
- `page-cro` - Homepage, landing page, pricing page optimization
- `form-cro` - Lead capture, contact, demo request forms
- `popup-cro` - Modals, overlays, exit intent popups
- `signup-flow-cro` - Registration, trial signup optimization
- `onboarding-cro` - Post-signup activation, first-run experience
- `paywall-upgrade-cro` - In-app paywalls, upgrade screens
- `ab-test-setup` - A/B test planning and experiment design

## Content & Copy Skills
- `copywriting` - Marketing page copy, headlines, CTAs
- `copy-editing` - Edit and polish existing marketing copy
- `email-sequence` - Drip campaigns, nurture sequences
- `linkedin-content` - LinkedIn post creation — story mining, SIREN framework, virality engineering
- `video-director` - AI video prompt generation — 11 types, 3 pipelines (Direct, Image-First, Localized), HITL gates, production SOP

## SEO & Growth Skills
- `programmatic-seo` - pSEO 2.0 — JSON-first schema-driven pages at scale, niche taxonomy, quality gates, GEO
- `schema-markup` - Structured data, rich snippets
- `competitor-alternatives` - Comparison and alternative pages
- `launch-strategy` - Product launches, feature announcements
- `pricing-strategy` - Pricing, packaging, monetization
- `referral-program` - Referral, affiliate, word-of-mouth
- `free-tool-strategy` - Engineering-as-marketing tools

## Paid Media Skills
- `paid-media-audit` - Systematic 200+ checkpoint ad account audit

## Research Skills
- `deep-research` - Multi-agent parallel research orchestrator (MECE decomposition, 90.2% better than single-agent)

## Campaign Execution
- `campaign-runner` - Full-stack campaign execution with state tracking, agent routing, and Postiz publishing

## Quality Assurance Skills
- `verification-loops` - Spawn reviewer + resolver agents for 2-3x quality improvement (Implement → Review → Resolve)
- `multi-agent-consensus` - Poll N agents with framing variations, aggregate by consensus/divergence/outlier
- `prompt-contracts` - Define GOAL/CONSTRAINTS/FORMAT/FAILURE before execution for zero-ambiguity deliverables
- `agent-chatrooms` - Multi-round adversarial debate between agents with distinct roles (brand strategist vs performance marketer vs customer advocate)
