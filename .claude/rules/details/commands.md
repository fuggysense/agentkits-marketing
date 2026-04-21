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
- `/content:ads` - Create ad copy for paid campaigns
- `/content:good` - Write good creative copy
- `/content:fast` - Write creative copy quickly
- `/content:enhance` - Enhance existing copy
- `/content:cro` - Optimize content for conversion
- `/content:editing` - Edit and polish existing copy
- `/content:video` - Generate AI video prompts (Sora, Kling, VEO)

## SEO Optimization
- `/seo:keywords` - Conduct keyword research
- `/seo:competitor` - Analyze competitor SEO strategy
- `/seo:optimize` - Optimize content for keywords
- `/seo:audit` - Perform comprehensive SEO audit
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
- `/project:profile` - Build or update business context profile (30-question interview → context-profile.json)
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

## Ads Upload
- `/ads:upload` - Upload creative bundle to Meta Ads (full pipeline)
- `/ads:validate` - Validate creative bundle (no API calls)
- `/ads:preview` - Preview what would be created (dry run)

## Testing
- `/test:ab-setup` - Plan and design A/B tests

## Transcription
- `/transcribe` - Transcribe video from any URL (YouTube, Instagram, TikTok, etc.) into text

## Audits & Checklists
- `/audit:paid-media` - Systematic paid media account audit
- `/audit:competitor-ads` - Extract and analyze competitor ads from Meta Ad Library
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
