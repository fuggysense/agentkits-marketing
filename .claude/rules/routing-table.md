# Routing Table

## Agents (`agents/`)
| Agent | Purpose |
|-------|---------|
| `attraction-specialist` | Lead gen, TOFU, SEO, competitor intel, landing pages |
| `brainstormer` | Campaign ideation, creative concepts, messaging angles |
| `brand-voice-guardian` | Brand consistency, voice validation, tone review |
| `command-helper` | Command discovery and usage guidance |
| `continuity-specialist` | Retention, engagement, customer success |
| `conversion-optimizer` | CRO, conversion rate optimization |
| `copywriter` | Content creation, headlines, CTAs, marketing copy |
| `docs-manager` | Documentation, brand guidelines, style guides |
| `email-wizard` | Email campaigns, sequences, automation |
| `lead-qualifier` | Intent detection, lead scoring, audience analysis |
| `mcp-manager` | MCP server integrations, tool orchestration |
| `persona-builder` | Buyer persona creation and refinement |
| `planner` | Campaign planning, content calendars |
| `project-manager` | Campaign management, coordination |
| `pseo-architect` | Programmatic SEO 2.0 pipeline orchestrator — taxonomy, schema, generation, validation, rollout, monitoring |
| `researcher` | Market research, competitive analysis |
| `sales-enabler` | Sales collateral, case studies, presentations |
| `seo-specialist` | SEO optimization, technical review |
| `solopreneur` | Solopreneur perspective reviewer |
| `startup-founder` | Startup founder perspective reviewer |
| `tracking-specialist` | Pixel tracking, GTM, GA4, conversion actions, attribution setup |
| `upsell-maximizer` | Revenue expansion, cross-sell, upsell |

## Skills (`skills/`)
| Skill | Purpose |
|-------|---------|
| `client-onboarding` | Guided project setup — scaffold, interview, validate, activate |
| `meta-builder` | Creates new agents and skills with feedback loops |
| `marketing-fundamentals` | Core marketing concepts, funnel stages |
| `marketing-psychology` | 70+ mental models for marketing |
| `marketing-ideas` | 140+ proven SaaS marketing strategies |
| `seo-mastery` | Search optimization, keyword research |
| `social-media` | Social strategies, platform best practices |
| `linkedin-content` | LinkedIn content creation — story mining, SIREN framework, virality engineering, post drafting |
| `linkedin-optimization` | LinkedIn organic — profile audit, algorithm, content, creator mode, B2B sales, banner design |
| `email-marketing` | Email automation, deliverability |
| `paid-advertising` | Ad platform strategies, ROAS optimization |
| `content-strategy` | Content planning, editorial calendars |
| `analytics-attribution` | Performance measurement, attribution models |
| `brand-building` | Brand strategy, voice, positioning |
| `problem-solving` | Marketing problem-solving techniques |
| `copywriting` | Marketing page copy, headlines, CTAs |
| `copy-editing` | Edit and polish existing marketing copy |
| `email-sequence` | Drip campaigns, nurture sequences |
| `page-cro` | Homepage, landing page, pricing page optimization |
| `form-cro` | Lead capture, contact, demo request forms |
| `popup-cro` | Modals, overlays, exit intent popups |
| `signup-flow-cro` | Registration, trial signup optimization |
| `onboarding-cro` | Post-signup activation, first-run experience |
| `paywall-upgrade-cro` | In-app paywalls, upgrade screens |
| `ab-test-setup` | A/B test planning and experiment design |
| `programmatic-seo` | pSEO 2.0 — JSON-first schema-driven pages at scale, niche taxonomy, quality gates, GEO |
| `schema-markup` | Structured data, rich snippets |
| `competitor-alternatives` | Comparison and alternative pages |
| `launch-strategy` | Product launches, feature announcements |
| `pricing-strategy` | Pricing, packaging, monetization |
| `referral-program` | Referral, affiliate, word-of-mouth |
| `free-tool-strategy` | Engineering-as-marketing tools |
| `document-skills` | DOCX, PDF, PPTX, XLSX document creation |
| `paid-media-audit` | Systematic 200+ checkpoint ad account audit |
| `campaign-runner` | Full-stack campaign execution, state tracking, Postiz publishing |
| `deep-research` | Multi-agent parallel research orchestrator (MECE, 3-6 sub-agents) |
| `verification-loops` | Spawn reviewer + resolver agents for quality assurance |
| `multi-agent-consensus` | Poll N agents for strategic decisions and ranking |
| `prompt-contracts` | Structured GOAL/CONSTRAINTS/FORMAT/FAILURE specs |
| `agent-chatrooms` | Multi-round adversarial debate between agent roles |
| `video-director` | AI video prompt generation — 11 types, 3 pipelines (Direct, Image-First, Localized), HITL gates |
| `amplifier` | Enhance existing skills/agents, conflict detection, merge suggestions |

## Context Layers
| Path | Purpose |
|------|---------|
| `context/clief-notes/` | Foundation layer — curated repos, skills, MCP servers, tools |
| `context/writing/` | Writing frameworks — copywriting masters, marketing genius, anti-AI patterns |
| `voice/<person>/` | V.O.I.C.E. system — 5 files per person (shared across all projects) |
| `clients/<project>/` | Per-project configs — ICP, offer, tone tweaks, channels |

**Two-layer context model:**
- **Voice = the person** (how you write) — stays the same across projects
- **Project = the business** (who you serve, what you sell) — changes per project

V.O.I.C.E. files: `brand-voice.md` (V), `about-me.md` (O), `working-style.md` (I), `compound-ideas.md` (C), `voice-examples.md` (E)

## Agent-Skill Mappings (Quick Reference)

| Agent | Primary Skills |
|-------|----------------|
| `pseo-architect` | programmatic-seo, seo-mastery, schema-markup, content-strategy, analytics-attribution |
| `copywriter` | copywriting, copy-editing, email-sequence, linkedin-content, video-director |
