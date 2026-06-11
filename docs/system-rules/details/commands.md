# Command Categories

## Campaign Management
- `/campaign:new` - Start new campaign from template
- `/campaign:status` - Show current campaign progress
- `/campaign:next` - Execute next priority actions
- `/campaign:schedule` - Schedule social content via Postiz
- `/campaign:metrics` - Pull latest metrics from MCPs
- `/campaign:report` - Generate campaign performance report
- `/campaign:plan` - Create comprehensive campaign plan
- `/campaign:brief` - Generate creative brief
- `/campaign:analyze` - Analyze campaign performance
- `/campaign:calendar` - Generate content calendar

## Content Creation
- `/content:humanize` - Run De-AI sweep (copy-editing Sweep 8) to remove AI patterns from text
- `/content:youtube-desc` - Generate complete YouTube description from video transcript
- `/content:blog` - Create SEO-optimized blog post
- `/content:social` - Create platform-specific social content
- `/content:email` - Create email copy with sequences
- `/content:landing` - Create landing page copy
- `/content:sales-letter` - Write long-form direct-response sales letter for cold paid traffic (800-2000+ words, 12-component Hormozi-inspired framework, 5-phase pipeline: Context Scan → parallel drafters → stitcher → Conversion Gate → polish)
- `/content:ads` - Create ad copy for paid campaigns
- `/content:good` - Write good creative copy
- `/content:fast` - Write creative copy quickly
- `/content:enhance` - Enhance existing copy
- `/content:cro` - Optimize content for conversion
- `/content:editing` - Edit and polish existing copy
- `/content:video` - Generate AI video prompts (Sora, Kling, VEO)

## Copywriting OS (unified copy pipeline — command-based layer wrapping existing skills with universal gates + reviewers)

- `/copy` - **Router.** Entry point that asks "what copy?" and delegates to the matching sub-command. Injects 3 pre-write gates (Channeling / Coat-of-Arms / One-Person) + 5 post-write sub-agent reviewers (One-Person-Enforcement / Proof-Density / Emotional-Sequence / Objection-Coverage / Teardown) around every domain module. **Zero system-prompt weight when not invoked.** Reference library: `.claude/references/copywriting-os/`. Client workspace: `clients/<slug>/copy-system/`.
- `/copy:sales-letter` - Long-form direct-response sales letter. Wraps `/content:sales-letter` (sales-letter-method) with all 8 OS gates + reviewers (3 pre + 5 post). **Prefer this over `/content:sales-letter` for automatic gate enforcement.**
- `/copy:email` - Email sequences (welcome / nurture / sales / re-engage / single). Wraps `/content:email` + `/sequence:*`. Enforces cai #40 voice rules + 6-state emotional progression across the sequence.
- `/copy:landing` - Landing page (lead-magnet / product / feature / pricing / homepage). Wraps `/content:landing` with cai #40 3-input principle enforced.
- `/copy:ad` - Ad copy (primary text + headlines + descriptions). Wraps `/content:ads` or a DCT wave (intent: "new ad concepts for <project>"). Mechanism diversity enforced on headline variants.
- `/copy:headline` - Static-ad headline bank with mandatory 5-mechanism diversity (Curiosity / Specific / Contrarian / Fear / Identity — cai #39). Wraps `/ads:headlines` with mechanism-diversity reviewer.

## SEO Optimization
- `/seo:keywords` - Conduct keyword research
- `/seo:competitor` - Analyze competitor SEO strategy
- `/seo:optimize` - Optimize content for keywords
- `/seo:audit` - Perform comprehensive SEO audit (parallel subagent architecture)
- `/seo:geo` - Optimize content for AI search engines (AI Overviews, ChatGPT, Perplexity)
- `/seo:programmatic` - Build SEO pages at scale
- `/seo:schema` - Add/optimize schema markup

## Social Media
- `/social:engage` - Develop engagement strategy
- `/social:viral` - Create viral-potential content
- `/social:schedule` - Create posting schedule
- `/tiktok:batch` - Create, approve, and schedule a 2-week batch of TikTok Photo Mode slideshows

## Email & Sequences
- `/sequence:welcome` - Create welcome sequence
- `/sequence:nurture` - Create lead nurture sequence
- `/sequence:re-engage` - Create re-engagement sequence

## Analytics & Reporting
- `/analytics:usage` - Show skill/agent usage analytics (pareto, clients, trend, unused, productivity, raw)
- `/analytics:roi` - Calculate campaign ROI
- `/analytics:funnel` - Analyze conversion funnel
- `/analytics:report` - Generate performance report
- `/report:weekly` - Generate weekly report
- `/report:monthly` - Generate monthly report
- `/analytics:cross-client` - Cross-client analytics report (Postiz data grouped by project)

## Sales & Leads
- `/sales:outreach` - Generate outreach sequence
- `/sales:pitch` - Generate sales pitch
- `/sales:battlecard` - Create competitive battlecard
- `/sales:qualify` - Qualify leads
- `/leads:score` - Design lead scoring model
- `/leads:nurture` - Design lead nurture sequence
- `/leads:qualify` - Create qualification criteria

## CRM & Lifecycle
- `/crm:sequence` - Create automated sequence
- `/crm:segment` - Create customer segment
- `/crm:score` - Calculate lead score
- `/crm:lifecycle` - Manage lifecycle transitions

## Video Scripts
- `/script` - Write video script in your voice (voice analysis, hook selection, de-AI, humanizer)
- `/hooks` - Scrape competitor profile for outlier video hooks, add to hooks database

## Brand Management
- `/brand:voice` - Create brand voice guidelines
- `/brand:book` - Generate comprehensive brand book
- `/brand:assets` - Manage brand assets

## CRO (Conversion Rate Optimization)
- `/cro:page` - Optimize marketing pages (homepage, landing, pricing)
- `/cro:form` - Optimize lead capture, contact, demo forms
- `/cro:popup` - Create/optimize popups, modals, overlays
- `/cro:signup` - Optimize signup/registration flows
- `/cro:onboarding` - Optimize post-signup onboarding
- `/cro:paywall` - Optimize in-app paywalls, upgrade screens

## Project Onboarding
- `/project:new` - Guided new client/project onboarding (scaffold, interview, enrich, validate, activate)
- `/project:profile` - Build or update business context profile (Fuggy's Media 6-section intake, ~21 questions → context-profile.json)
- `/project:validate` - Run readiness check on existing project

## Offer Building
- `/offer:build` - Full 15-step interactive offer construction
- `/offer:validate` - Run audit passes on existing offer
- `/offer:micro` - Build micro offer only (Steps 1-7)
- `/offer:score` - Quick Vending Machine Score diagnostic

## Operations & Planning
- `/ops:daily` - Daily marketing tasks
- `/ops:weekly` - Weekly marketing review
- `/ops:monthly` - Monthly performance review
- `/ops:claude-md` - Create, update, or fix CLAUDE.md files
- `/plan:cro` - Create CRO plan

## Research & Competitive Analysis
- `/research:market` - Conduct market research
- `/research:persona` - Create buyer persona
- `/research:trend` - Analyze industry trends
- `/research:deep` - Multi-agent deep research (MECE decomposition, parallel agents)
- `/competitor:deep` - Deep competitor analysis
- `/competitor:alternatives` - Create competitor comparison pages

## Growth & Launch
- `/growth:launch` - Plan product launch, feature announcement
- `/growth:referral` - Design referral/affiliate program
- `/growth:free-tool` - Plan free tool for marketing
- `/pricing:strategy` - Design pricing and packaging

## Marketing Strategy
- `/marketing:psychology` - Apply psychological principles
- `/marketing:ideas` - Get 140+ marketing ideas

## De-AI / Unslop
- `/unslop:profile <domain>` - Generate domain-specific avoidance profile (e.g., "linkedin posts", "saas landing pages")
- `/unslop:refresh` - Re-run all existing profiles with current model
- `/unslop:list` - Show all generated profiles with metadata

## Amplification (via global skill-amplifier)
- `/amplify:skill` - Enhance an existing skill
- `/amplify:agent` - Enhance an existing agent
- `/amplify:scan` - Scan all for conflicts and overlaps
- `/amplify:merge` - Suggest merges for coupled artifacts

## Autoresearch (Autonomous Skill Optimization)
- `/autoresearch:init` - Scaffold autoresearch data for a client project
- `/autoresearch:bootstrap <skill>` - Auto-generate rubric + scenarios for a skill
- `/autoresearch:run <skill>` - Run the optimization loop (default: 3 iterations)
- `/autoresearch:results [skill]` - Show experiment history + score progression
- `/autoresearch:batch <skills...>` - Run across multiple skills (Phase 2)
- `/autoresearch:continuous [N]` - Run next N skills from priority queue (Phase 3)
- `/autoresearch:schedule` - Show priority queue + next scheduled (Phase 3)
- `/autoresearch:trust [skill] [level]` - View/set trust levels (Phase 3)
- `/autoresearch:budget` - Show spend vs caps (Phase 3)
- `/autoresearch:stop` - Kill switch — halt all runs (Phase 3)
- `/autoresearch:calibrate <skill>` - Force rubric recalibration from campaign data (Phase 4)
- `/autoresearch:feedback <campaign>` - Record campaign outcomes for a skill (Phase 4)

## Ads (6-stage creative pipeline — see `.claude/workflows/creative-pipeline.md`)
- `/ads:source-of-truth` - **Stage 1 Research.** Generate the 26-section paid ads strategic doc for any client/URL/idea. Parallel research (scrapecreators + buyer-language-researcher + deep-research + paid-media-audit) → HITL (4 strategic decisions) → writes source-of-truth.md + derivative files + angles/ folder + optionally populates AVATARS sheet tab. Multi-product (ecom/SaaS/service/info/agency/property).
- **Build avatars** (intent, no slash command — say "build avatars for <project>"; routes to `avatar-research`) - **Stage 1 Research (avatar deepening).** Build 3+ DCT avatars per project (16-point psychological breakdown including Top 5 Deep Fears, Raw Inner Dialogue, Desired Transformation, Relationship Impact).
- `/ads:headlines` - **Stage 1.5 Headline Reservoir (optional, legacy path).** Generate a static-ad headline bank anchored to one mass desire: 75+ headlines across 5 awareness levels × 10 angle banks. Interactive. Used when you want breadth for alternate copy variants. NOT called in the big-angle-spotter path.
- `/ads:big-angle-spotter` - **Stage 1.25 Depth specialist (1 angle = 1 DCT = 1 Ad Set).** 12-step Opus→Sonnet pipeline (fresh `claude -p` per step, no session chaining). Input: OFFER / COMPANY / PERSONA / INDUSTRY / EXISTING_ANGLES. Output: 1 top angle + 3 ranked headlines + 3 ad prompts + 3 image-gen prompts. Called directly for single-angle runs OR looped by the DCT wave (intent: "new ad concepts for <project>", `ad-concept-engine` Conductor Mode) for multi-angle waves with cross-pollinated EXISTING_ANGLES. Outputs land at `clients/<slug>/angles/big-angle-spotter/wave-<N>/angle-<i>/`.
- **New ad concepts / DCT wave** (intent, no slash command — say "new ad concepts for <project>"; routes to `ad-concept-engine` Conductor Mode) - **Stages 2 + 3 Orchestrator (v3.0).** Loops `/ads:big-angle-spotter` N times across avatars (sequential, EXISTING_ANGLES cross-pollinated — run N sees runs 1..N-1 winners). Wraps outputs into Meta hierarchy per new naming: Campaign `[Obj]_[Test|Scale]_[Theme]_[MonYY]` -> Ad Set `[Aud]_[Targ]_[Angle]_[Budget]` (1 per angle) -> Ad `[YYMMDD]_[Angle]_[Format+Hook#]` (3 per Ad Set). Retains Phase 2b video briefs (UGC/Founder/VSL/Demo 6-scene). Phase 3 routes image prompts to image-generation, video briefs to video-director. Writes dct-tracker + sheet.
- `/ads:scrape-library` - **Stage 0.3 Industry Pool.** Scrape Meta Ad Library for an industry (e.g. `property-sg`), enrich winners (>30 days running) with transcripts/OCR + Nemotron classifier, rebuild SQLite swipe-file DB, auto-draft Schwartz 5-stage market sophistication brief for HITL approval. Writes to `swipe-files/<industry>/`. Read by `/ads:source-of-truth`, the DCT wave (intent: "new ad concepts for <project>"), `/ads:feedback` as canonical industry strategic brief.
- `/ads:upload` - **Stage 5 Test.** Upload creative bundle to Meta Ads (ads created PAUSED).
- `/ads:validate` - Validate creative bundle (no API calls).
- `/ads:preview` - Preview what would be created (dry run).
- `/ads:feedback` - **Stage 6 Feedback.** Read DCT wave performance + route next action to NEW (research refresh) / BETTER (concept refinement within winning angle) / MORE (variant expansion in winning direction). Closes the loop. Auto-appends learnings.
- `/ads:scrape-advertiser` - **Single-page ingestion.** Scrape one Meta Ad Library page into Ghost Postgres (`swipe-ads`) via `ingest-advertiser.py`. Accepts page_id or Meta URL + industry slug. `--depth active` (default, fast) or `--depth full` (HITL gate — costs more credits). Visible in Swipe Dashboard immediately.

## Testing
- `/test:ab-setup` - Plan and design A/B tests

## Transcription
- `/transcribe` - Transcribe video from any URL (YouTube, Instagram, TikTok, etc.) into text

## Audits & Checklists
- `/audit:paid-media` - Systematic paid media account audit
- `/audit:competitor-ads` - **Superseded by `/ads:scrape-library`** (industry-pool scraper with Schwartz brief). Old placeholder, no command file ever shipped under this name.
- `/audit:full` - Comprehensive marketing audit
- `/checklist:campaign-launch` - Pre-launch checklist
- `/checklist:social-daily` - Daily social media checklist
- `/checklist:seo-weekly` - Weekly SEO checklist
- `/checklist:analytics-monthly` - Monthly analytics review
- `/checklist:ab-testing` - A/B testing framework
- `/checklist:content-approval` - Content approval workflow

## Utilities
- `/brainstorm` - Brainstorm marketing strategies
- `/use-mcp` - Use MCP server tools
- `/skills:select` - Intelligent skill selection
