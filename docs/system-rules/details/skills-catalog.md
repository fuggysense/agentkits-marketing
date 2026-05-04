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
- `client-onboarding` - Guided project onboarding — scaffold, Fuggy's Media 6-section intake (~21 questions → context-profile.json), marketing deep dive, agent enrichment, validate, activate. Also runs standalone via `/project:profile` for updates.
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
- `sales-letter-method` - Long-form direct-response sales letter for cold paid traffic (800-2000+ words). 12-component context-gated framework (Hormozi-inspired, price anchor removed, guarantee stack promoted as primary conversion lever). 5-phase pipeline: Phase 0 Context Scan + HITL → Phase 1 Parallel Sonnet Drafters (Hook Half + Commit Half) → Phase 2 Opus Stitcher → Phase 3 Conversion Gate (merged cold-reader + prompt-contracts dual-lens) → Phase 4 Polish (copy-editing Sweep 8 + unslop + brand-voice). Industry-agnostic with first-class real estate / consulting / agency support. Based on 8-page competitor analysis (universal back-half gap = FAQ + PS + Guarantee missing 8/8). `/content:sales-letter`
- `youtube-content` - YouTube description generation from transcripts — timestamps, links, brand-consistent copy
- `email-sequence` - Drip campaigns, nurture sequences
- `content-moat` - Originality-first ideation, layer stacking (10 types), copycat resistance scoring
- `tiktok-slideshows` - TikTok Photo Mode carousels — 3:4 specs, text placement rules, typography system, batch workflow, Canva assembly
- `image-generation` - AI image generation — Nano Banana 2 JSON prompts, carousel slides, marketing assets (~$0.07/image)
- `linkedin-content` - LinkedIn post creation — story mining, SIREN framework, virality engineering
- `script-skill` - Video script writing in YOUR voice — voice capture, competitor hook scraping, hooks database, de-AI + humanizer passes, **5-pass ad-VO loop** (Diagnose → Contextualize → Draft → De-AI Sweep → Direct) for paid ads. **Phase 3.5 — bespoke hook generation** via 3-element framework (relatability / sensationalism / stakes) + contrast technique + growing case_log calibration set. Triggers also on "write me a hook", "scroll-stopper", "first 3 seconds", "fix my opening" (global: `~/.claude/skills/script-skill/`). Companion: `viral-hooks-content-creator` for 1000+ template batch ideation; script-skill for single-brief depth + voice-match.
- `viral-hooks-content-creator` - **1000+ viral hook templates** across 7 categories (Educational / Comparison / Myth-Bust / Storytelling / Authority / Day-in-Life / Engagement) + **7-factor viral content framework** (Topic / Hooks / Value / Angle / CTA / Format / Editing) + batch/calendar mode (one topic → 7 angles via angle multiplication). Triggers: "hooks", "content ideas", "what should I post", "viral", weekly content batches (global: `~/.claude/skills/viral-hooks-content-creator/`). Companion: `script-skill` for voice-matching + de-AI sweep + ad-VO direction.
- `video-director` - AI video prompt generation — 14 types, 3 pipelines (Direct, Image-First, Localized), character bibles, seed management, UGC automation, HITL gates. **NOT for Seedance UGC ads → use `seedance-ugc-director`**
- `seedance-ugc-director` - **Seedance 2.0 UGC ad director (global).** One-shot output from a script: Pinterest creator refs + @Image1/2/3 + Hook→Problem→Benefit→CTA 15s segments + anti-cinematic keyword bans + room-tone matched audio + natural dialogue rules. Replaces Mode 3 of `seedance-prompt`. No clarifying questions — strict format.
- `seedance-prompt` - Seedance 2.0 T2I (character sheets, scene images) + I2V (animate existing images with sound). **Ad Creative mode retired → use `seedance-ugc-director`**
- `seedance-effects` - Multi-shot Seedance with stacked effects + energy arc
- `seedance-loop` - Seamless webpage background video loops
- `seedance-motion` - Motion graphics / liquid glass / app promos (no humans)
- `ugc-creator` - Higgsfield UGC studio with persistent actor identities and face-lock. For Seedance UGC ads use `seedance-ugc-director`.
- `ai-filmmaking` - Narrative / brand films (director profiles + ARQ 7-step pipeline)

## SEO & Growth Skills
- `programmatic-seo` - pSEO 2.0 — JSON-first schema-driven pages at scale, niche taxonomy, quality gates, GEO
- `schema-markup` - Structured data, rich snippets
- `competitor-alternatives` - Comparison and alternative pages
- `launch-strategy` - Product launches, feature announcements
- `pricing-strategy` - Pricing, packaging, monetization
- `referral-program` - Referral, affiliate, word-of-mouth
- `free-tool-strategy` - Engineering-as-marketing tools

## Paid Media Skills (6-stage creative pipeline — see `.claude/workflows/creative-pipeline.md`)
- `source-of-truth` - **Stage 1 Research.** 26-section paid ads SoT for any client/URL/idea. Multi-product (ecom/SaaS/service/info/agency/property) with product_type-driven branching. Includes §5.5 Golden Nuggets, §5.7 ICP Language Analysis, §7.5 Misconceptions. Phase 0.5 raw-doc upload supported. Upstream of avatar-research. `/ads:source-of-truth`
- `avatar-research` - **Stage 1 Research (avatar deepening).** 16-point psychological breakdown per avatar (Schwartz awareness/sophistication PLUS Top 5 Deep Fears, Raw Inner Dialogue, Desired Transformation, Relationship Impact). External research prompts (Perplexity/Grok/ChatGPT). Feeds ad-concept-engine. `/ads:avatars`
- `headline-bank` - **Stage 1.5 Reservoir (optional, legacy path).** Static-ad headline bank anchored to one mass desire per run. 75+ headlines across 5 awareness levels × 10 angle banks (Cashvertising LF8 + Schwartz + Halbert). Interactive — first response asks which mass desire to focus on. Outputs `clients/<slug>/angles/wave-<N>-headline-bank.md`. Used when you want breadth for alternate copy variants. **NOT called in the big-angle-spotter path** — big-angle-spotter produces its own ranked top-3. `/ads:headlines`
- `big-angle-spotter` - **Stage 1.25 Depth specialist.** One run = one angle = one DCT = one Ad Set. 12-step Opus→Sonnet pipeline (fresh `claude -p` worker per step, no session chaining, content-addressable SP cache). Input: OFFER / COMPANY / PERSONA / INDUSTRY / EXISTING_ANGLES. Output: 1 top angle + 3 ranked headlines + 3 ad prompts + 3 image-gen prompts. **Multi-angle via sequential runs with cross-pollinated EXISTING_ANGLES** (run N sees runs 1..N-1 winners). Symlinked skill at `skills/big-angle-spotter/` → `~/AI workflows/big-angle-spotter/`. `/ads:big-angle-spotter`
- `ad-concept-engine` - **Orchestrator** (v3.0 post-integration) — Stages 2+3. Loops big-angle-spotter N times across avatars with EXISTING_ANGLES cross-pollination, wraps outputs into Meta hierarchy per `/ads/` naming spec (`CBO_Test_Theme_MonYY` → `Broad_None_Angle_$budget` → `YYMMDD_Angle_F#`). Retains Phase 2b Briefs (UGC/Founder/VSL/Demo 6-scene breakdown) for video creatives. Phase 3 routes image-gen prompts to image-generation (3a) and video briefs to video-director (3b). Writes dct-tracker + sheet. **Does NOT generate angles or static hooks directly** — delegates to big-angle-spotter. `/ads:concepts`
- `ad-library-scraper` - **Stage 0.3 Industry Pool.** Meta Ad Library scraper → `swipe-files/<industry>/` filesystem + SQLite. Hybrid enrichment (L1 always; L2 transcripts/OCR for ads with `days_running > 30`; L3 Kilo→Nemotron classifier). Auto-drafts Schwartz 5-stage brief for HITL approval. Industry-level pool serves every client in the industry. `/ads:scrape-library <industry>`
- `paid-media-audit` - Systematic 200+ checkpoint ad account audit
- `meta-ads-uploader` - **Stage 5 Test.** Upload ad creatives to Meta (images, videos, dynamic creatives) → ads created PAUSED
- `feedback-router` - **Stage 6 Feedback.** After wave concludes, reads CREATIVES + COPY sheet metrics + dct-tracker.json Performance table, routes next action: NEW (research refresh) / BETTER (concept refinement within winning angle) / MORE (variant expansion in winning direction). Auto-appends learnings to clients/<slug>/learnings.md + angles/iteration-log.md. Closes the 6-stage loop. `/ads:feedback`

## Knowledge Hygiene
- `knowledge-hygiene` - Anti-decay system: freshness audit, learnings integration check, registry drift detection. Wired into `/ops:weekly` and `/ops:monthly`, not standalone.

## System Tools (Global Skills)
- `skill-builder` - Creates new agents and skills with feedback loops (global: `~/.claude/skills/skill-builder/`)
- `skill-amplifier` - Enhance existing skills/agents, conflict detection, merge suggestions (global: `~/.claude/skills/skill-amplifier/`)
- `autoresearch` - Autonomous skill optimization via generate → evaluate → mutate → keep/discard loops. Wraps any skill in a self-improving loop per client (global: `~/.claude/skills/autoresearch/`)
- `chrome-mcp` - Chrome DevTools browser control — authenticated dashboard access, tracking verification, live page inspection (global: `~/.claude/skills/chrome-mcp/`)
- `auto-broll` - Fetches free B-roll footage for video scripts (Pexels / Pixabay / Unsplash) with scene typing + HEVC→H.264 transcode. Symlinked global skill: `~/.claude/skills/auto-broll` → `~/AI workflows/hyperframes-student-kit/.claude/skills/auto-broll`. Edits in either location reflect both — single source of truth.

## Design & Build Skills
- `website-design` - Quad-mode website builds (Recreate, Create, Hybrid, Paper-First) with Paper.design MCP for bidirectional visual editing, design token extraction, JSX/Tailwind export
- `design-system` - Brand visual extraction + artifact generator. Pulls logo SVG/colors/fonts from any reference (URL via chrome-mcp, screenshot, or existing assets), cross-references `source-of-truth.md` + `brand-voice.md`, HITL gate, then outputs `clients/<slug>/brand/design-system.html` (scrollable reference) + `brand-book-a4.html/.pdf` (printable one-pager). Upstream of website-design, image-generation, ad-concept-engine.

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
