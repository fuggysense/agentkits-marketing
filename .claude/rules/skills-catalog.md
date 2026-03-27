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
- `client-onboarding` - Guided project onboarding — scaffold, 30-question business context profile (→ context-profile.json), marketing deep dive, agent enrichment, validate, activate. Also runs standalone via `/project:profile` for updates.
- `offer-builder` - Interactive offer construction — deep discovery, viability scoring (OV Gate + Vending Machine), identity extraction, micro offers, audit passes, deployment scripts
- `document-skills` - DOCX, PDF, PPTX, XLSX document creation

## CRO Skills
- `page-cro` - Homepage, landing page, pricing page optimization
- `form-cro` - Lead capture, contact, demo request forms
- `popup-cro` - Modals, overlays, exit intent popups
- `signup-flow-cro` - Registration, trial signup optimization
- `onboarding-cro` - Post-signup activation, first-run experience
- `paywall-upgrade-cro` - In-app paywalls, upgrade screens
- `ab-test-setup` - A/B test planning and experiment design

## Utility Skills
- `transcribe` - Video URL transcription via yt-dlp + faster-whisper (YouTube, Instagram, TikTok, 1000+ sites)
- `scrapecreators` - Universal social intelligence API client for 25+ platforms (TikTok, Instagram, YouTube, LinkedIn, Facebook, Twitter/X, Reddit, Threads, Pinterest, Bluesky, and more)
- `unslop` - Domain-specific AI pattern detection — generates empirical avoidance profiles by sampling model defaults. Layer 1 of 4-layer de-AI stack (unslop → overused-ai-patterns → corrections.md → V.O.I.C.E.)

## Content & Copy Skills
- `copywriting` - Marketing page copy, headlines, CTAs
- `copy-editing` - Edit and polish existing marketing copy (includes Sweep 8: De-AI pattern removal)
- `youtube-content` - YouTube description generation from transcripts — timestamps, links, brand-consistent copy
- `email-sequence` - Drip campaigns, nurture sequences
- `content-moat` - Originality-first ideation, layer stacking (10 types), copycat resistance scoring
- `tiktok-slideshows` - TikTok Photo Mode carousels — 3:4 specs, text placement rules, typography system, batch workflow, Canva assembly
- `image-generation` - AI image generation — Nano Banana 2 JSON prompts, carousel slides, marketing assets (~$0.07/image)
- `linkedin-content` - LinkedIn post creation — story mining, SIREN framework, virality engineering
- `script-skill` - Video script writing in YOUR voice — voice capture, competitor hook scraping, hooks database, de-AI + humanizer passes (global: `~/.claude/skills/script-skill/`)
- `video-director` - AI video prompt generation — 14 types, 3 pipelines (Direct, Image-First, Localized), character bibles, seed management, UGC automation, HITL gates

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
- `meta-ads-uploader` - Upload ad creatives to Meta (images, videos, dynamic creatives) → ads created PAUSED

## Knowledge Hygiene
- `knowledge-hygiene` - Anti-decay system: freshness audit, learnings integration check, registry drift detection. Wired into `/ops:weekly` and `/ops:monthly`, not standalone.

## System Tools (Global Skills)
- `skill-builder` - Creates new agents and skills with feedback loops (global: `~/.claude/skills/skill-builder/`)
- `skill-amplifier` - Enhance existing skills/agents, conflict detection, merge suggestions (global: `~/.claude/skills/skill-amplifier/`)
- `autoresearch` - Autonomous skill optimization via generate → evaluate → mutate → keep/discard loops. Wraps any skill in a self-improving loop per client (global: `~/.claude/skills/autoresearch/`)
- `chrome-mcp` - Chrome DevTools browser control — authenticated dashboard access, tracking verification, live page inspection (global: `~/.claude/skills/chrome-mcp/`)

## Design & Build Skills
- `website-design` - Quad-mode website builds (Recreate, Create, Hybrid, Paper-First) with Paper.design MCP for bidirectional visual editing, design token extraction, JSX/Tailwind export

## Usage Analytics
- `analytics-usage` - Global skill/agent usage tracking, 80/20 pareto analysis, trend reports, unused detection

## Research Skills
- `deep-research` - Multi-agent parallel research orchestrator (MECE decomposition, 90.2% better than single-agent)

## Campaign Execution
- `campaign-runner` - Full-stack campaign execution with state tracking, agent routing, and Postiz publishing

## Quality Assurance Skills
- `verification-loops` - Spawn reviewer + resolver agents for 2-3x quality improvement (Implement → Review → Resolve)
- `multi-agent-consensus` - Poll N agents with framing variations, aggregate by consensus/divergence/outlier
- `prompt-contracts` - Define GOAL/CONSTRAINTS/FORMAT/FAILURE before execution for zero-ambiguity deliverables
- `agent-chatrooms` - Multi-round adversarial debate between agents with distinct roles (brand strategist vs performance marketer vs customer advocate)
