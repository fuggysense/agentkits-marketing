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
| `persona-builder` | Deep buyer profile & persona (3 modes: extract from copy, interactive discovery, project enrichment) + Schwartz awareness mapping |
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
| `client-onboarding` | Guided project setup — scaffold, 30-question business context profile (→ context-profile.json), marketing deep dive, agent enrichment, validate, activate |
| `offer-builder` | Interactive offer construction — discovery, viability scoring, identity extraction, micro offer, audit, deployment |
| `skill-builder` | Creates new agents and skills with feedback loops (global: `~/.claude/skills/skill-builder/`) |
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
| `copy-editing` | Edit and polish existing marketing copy (includes Sweep 8: De-AI) |
| `transcribe` | Video URL transcription via yt-dlp + faster-whisper, supports 1000+ sites |
| `scrapecreators` | Universal social intelligence API — 25+ platforms, profiles, videos, posts, ads, trending |
| `youtube-content` | YouTube description generation — timestamps, links, brand-consistent copy from transcripts |
| `email-sequence` | Drip campaigns, nurture sequences |
| `content-moat` | Originality-first ideation, layer stacking, copycat resistance scoring |
| `tiktok-slideshows` | TikTok Photo Mode carousels — 3:4 specs, text placement, typography, batch workflow, Canva assembly |
| `image-generation` | AI image generation — Nano Banana 2, JSON prompts, carousel slides, ~$0.07/image |
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
| `meta-ads-uploader` | Upload ad creatives to Meta (images, videos, dynamic creatives) → PAUSED ads |
| `campaign-runner` | Full-stack campaign execution, state tracking, Postiz publishing, TikTok slideshow batches |
| `deep-research` | Multi-agent parallel research orchestrator (MECE, 3-6 sub-agents) |
| `verification-loops` | Spawn reviewer + resolver agents for quality assurance |
| `multi-agent-consensus` | Poll N agents for strategic decisions and ranking |
| `prompt-contracts` | Structured GOAL/CONSTRAINTS/FORMAT/FAILURE specs |
| `agent-chatrooms` | Multi-round adversarial debate between agent roles |
| `script-skill` | Video script writing in YOUR voice — voice capture, competitor hook scraping, hooks database, de-AI + humanizer passes (global: `~/.claude/skills/script-skill/`) |
| `video-director` | AI video prompt generation — 14 types, 3 pipelines (Direct, Image-First, Localized), character bibles, seed management, UGC automation, HITL gates |
| `analytics-usage` | Global skill/agent usage tracking, 80/20 pareto analysis, client breakdown |
| `knowledge-hygiene` | Anti-decay system — freshness audit, learnings integration check, registry drift detection |
| `autoresearch` | Autonomous skill optimization — generate → evaluate → mutate → keep/discard loops, per-client (global: `~/.claude/skills/autoresearch/`) |
| `skill-amplifier` | Enhance existing skills/agents, conflict detection, merge suggestions (global: `~/.claude/skills/skill-amplifier/`) |
| `chrome-mcp` | Authenticated Chrome browser control — live dashboards, tracking verification, post-publish QA (global: `~/.claude/skills/chrome-mcp/`) |
| `website-design` | Quad-mode website builds (Recreate, Create, Hybrid, Paper-First) with Paper.design MCP for bidirectional visual editing |
| `unslop` | Domain-specific AI pattern detection — generates empirical avoidance profiles (Layer 1 of 4-layer de-AI stack) |

## Context Layers
| Path | Purpose |
|------|---------|
| `context/clief-notes/` | Foundation layer — curated repos, skills, MCP servers, tools |
| `context/writing/` | Writing frameworks — copywriting masters, marketing genius, anti-AI patterns |
| `voice/<person>/` | V.O.I.C.E. system — 5 files per person (shared across all projects) |
| `clients/<project>/context-profile.json` | Business identity foundation — structured JSON, read FIRST by all skills |
| `clients/<project>/` | Per-project configs — ICP, offer, tone tweaks, channels |

**Context load order (all downstream skills):**
1. `context-profile.json` → business identity (WHO)
2. `voice/<person>/` → writing voice (HOW)
3. `icp.md`, `offer.md`, `brand-voice.md`, `channels.json` → marketing specifics (WHAT)
4. `buyer-profile.md` → buyer psychology (TO WHOM)
5. `learnings.md` → accumulated intelligence (WHAT WORKS)

**Two-layer context model:**
- **Voice = the person** (how you write) — stays the same across projects
- **Project = the business** (who you serve, what you sell) — changes per project

V.O.I.C.E. files: `brand-voice.md` (V), `about-me.md` (O), `working-style.md` (I), `compound-ideas.md` (C), `voice-examples.md` (E)

## Agent-Skill Mappings (Quick Reference)

| Agent | Primary Skills |
|-------|----------------|
| `pseo-architect` | programmatic-seo, seo-mastery, schema-markup, content-strategy, analytics-attribution |
| `copywriter` | copywriting, copy-editing, email-sequence, linkedin-content, video-director, content-moat, script-skill |
| `brainstormer` | content-moat, content-strategy, marketing-ideas |
| `researcher` | deep-research, content-moat (research-fueled mode), competitor-alternatives |
