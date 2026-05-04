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
| `client-onboarding` | Guided project setup — scaffold, Fuggy's Media 6-section intake (~21 questions → context-profile.json), marketing deep dive, agent enrichment, validate, activate |
| `offer-builder` | Interactive offer construction — discovery, viability scoring, identity extraction, micro offer, audit, deployment |
| `skill-builder` | Creates new agents and skills with feedback loops (global: `~/.claude/skills/skill-builder/`) |
| `marketing-fundamentals` | Core marketing concepts, funnel stages |
| `marketing-psychology` | 70+ mental models for marketing |
| `marketing-ideas` | 140+ proven SaaS marketing strategies |
| `seo-mastery` | Search optimization, keyword research, GEO (AI search), parallel audit architecture, DataForSEO command layer |
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
| `sales-letter-method` | Long-form direct-response sales letter for cold paid traffic (800-2000+ words). 12-component framework (Hormozi-inspired, price anchor removed, guarantee stack promoted as primary conversion lever). 5-phase pipeline: Phase 0 Context Scan + HITL → Phase 1 Parallel Drafters (Hook Half + Commit Half) → Phase 2 Stitcher → Phase 3 Conversion Gate (cold-reader + prompt-contracts dual-lens) → Phase 4 Polish (de-AI + unslop + brand-voice). Industry-agnostic, first-class real estate / consulting / agency support. `/content:sales-letter` |
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
| `ad-library-scraper` | **Stage 0.3 industry pool.** Meta Ad Library scraper → filesystem + SQLite swipe DB per industry. Enriches winners (>30d) with transcripts/OCR + Nemotron classifier. Drafts Schwartz 5-stage brief (HITL). One scrape serves every client in the industry. `/ads:scrape-library <industry>` — Single-page ingestion into Ghost Postgres: `/ads:scrape-advertiser <page_id> <industry>` |
| `paid-media-audit` | Systematic 200+ checkpoint ad account audit |
| `meta-ads-uploader` | Upload ad creatives to Meta (images, videos, dynamic creatives) → PAUSED ads |
| `avatar-research` | Build 3+ advertising avatars per project for DCT targeting — 16-point psychological breakdown (Schwartz + Top 5 Deep Fears + Raw Inner Dialogue + Desired Transformation + Relationship Impact), external research prompts, feeds into ad-concept-engine |
| `headline-bank` | Static-ad headline reservoir — 75+ headlines across 5 awareness levels × 10 angle banks, anchored to one mass desire per run. Interactive mass-desire question first. Optional reservoir for ad-concept-engine alternate copy variants. NOT called in the big-angle-spotter path. `/ads:headlines` |
| `big-angle-spotter` | **Stage 1.25 Depth specialist.** 1 run = 1 angle (= 1 DCT = 1 Ad Set). 12-step Opus→Sonnet pipeline (fresh `claude -p` worker per step, no session chaining) produces: 1 top angle + 3 ranked headlines + 3 ad prompts + 3 image-gen prompts. Multi-angle via sequential runs with cross-pollinated `EXISTING_ANGLES`. Symlinked from `~/AI workflows/big-angle-spotter/`. `/ads:big-angle-spotter` |
| `ad-concept-engine` | **Orchestrator** (v3.0 post-integration) — loops big-angle-spotter N times across avatars with EXISTING_ANGLES cross-pollination, wraps outputs into Meta hierarchy (Campaign/Ad Set/Ad) + new naming, retains Phase 2b video briefs, Phase 3 routing to image-generation + video-director, writes tracker + sheet. Does NOT generate angles or static hooks directly — delegates to big-angle-spotter. |
| `feedback-router` | Stage 6 of creative pipeline. Reads wave performance, routes next action to NEW (research refresh) / BETTER (concept refinement) / MORE (variant expansion). Auto-appends learnings. Closes the loop. |
| `campaign-runner` | Full-stack campaign execution, state tracking, Postiz publishing, TikTok slideshow batches |
| `deep-research` | Multi-agent parallel research orchestrator (MECE, 3-6 sub-agents) |
| `verification-loops` | Spawn reviewer + resolver agents for quality assurance |
| `multi-agent-consensus` | Poll N agents for strategic decisions and ranking |
| `prompt-contracts` | Structured GOAL/CONSTRAINTS/FORMAT/FAILURE specs |
| `agent-chatrooms` | Multi-round adversarial debate between agent roles |
| `script-skill` | Video script writing in YOUR voice — voice capture, competitor hook scraping, hooks database, de-AI + humanizer passes, **5-pass ad-VO loop** for paid ads (Diagnose → Contextualize → Draft → De-AI Sweep → Direct). **Phase 3.5 — bespoke hook generation** via 3-element framework (relatability / sensationalism / stakes) + contrast technique + growing case_log of decoded real-world hooks (global: `~/.claude/skills/script-skill/`). Companion: `viral-hooks-content-creator` for template-library batch ideation; this skill for single-brief depth + voice-match. |
| `viral-hooks-content-creator` | **1000+ viral hook templates** across 7 categories (Educational, Comparison, Myth-Bust, Storytelling, Authority, Day-in-Life, Engagement) + **7-factor viral content framework** (Topic / Hooks / Value / Angle / CTA / Format / Editing) + batch/calendar mode (one topic → 7 angles). Use for "give me hooks", "content ideas", "what should I post", weekly batches (global: `~/.claude/skills/viral-hooks-content-creator/`). Companion: `script-skill` for voice-match + de-AI. |
| `video-director` | AI video prompt generation — 14 types, 3 pipelines (Direct, Image-First, Localized), character bibles, seed management, UGC automation, HITL gates. NOT for Seedance UGC ads (→ `seedance-ugc-director`) |
| `seedance-ugc-director` | **Seedance 2.0 UGC ad director (global).** One-shot output from a script/concept: Pinterest creator refs + @Image1/2/3 mapping + Hook→Problem→Benefit→CTA 15s segment prompts + anti-cinematic keyword bans + room-tone matched audio + natural dialogue rules. Single opinionated output format — no clarifying questions. Supersedes Mode 3 of `seedance-prompt`. |
| `seedance-prompt` | Seedance 2.0 T2I (character sheets, scene images, environments) + I2V (animate existing realistic images with sound). **No longer handles UGC ad sequences** — route those to `seedance-ugc-director`. |
| `ugc-creator` | Hyper-realistic Higgsfield UGC studio — persistent actor identities, face-lock, talking-head prompts. For Seedance UGC use `seedance-ugc-director`. |
| `analytics-usage` | Global skill/agent usage tracking, 80/20 pareto analysis, client breakdown |
| `knowledge-hygiene` | Anti-decay system — freshness audit, learnings integration check, registry drift detection |
| `autoresearch` | Autonomous skill optimization — generate → evaluate → mutate → keep/discard loops, per-client (global: `~/.claude/skills/autoresearch/`) |
| `skill-amplifier` | Enhance existing skills/agents, conflict detection, merge suggestions (global: `~/.claude/skills/skill-amplifier/`) |
| `chrome-mcp` | Authenticated Chrome browser control — live dashboards, tracking verification, post-publish QA (global: `~/.claude/skills/chrome-mcp/`) |
| `auto-broll` | Fetches free B-roll footage for video scripts (Pexels / Pixabay / Unsplash). Scene-typed downloader with HEVC→H.264 transcode handling. Symlinked global skill: `~/.claude/skills/auto-broll` → `~/AI workflows/hyperframes-student-kit/.claude/skills/auto-broll`. Edits in either location reflect both — single source of truth. |
| `website-design` | Quad-mode website builds (Recreate, Create, Hybrid, Paper-First) with Paper.design MCP for bidirectional visual editing |
| `design-system` | Extract brand visual system from site URL/screenshot → generates `clients/<slug>/brand/design-system.html` + `brand-book-a4.pdf`. Chrome-mcp devtools pulls logo SVG + colors + fonts. HITL gate before generation. |
| `unslop` | Domain-specific AI pattern detection — generates empirical avoidance profiles (Layer 1 of 4-layer de-AI stack) |

## Copywriting OS (`commands/copy.md` + `.claude/references/copywriting-os/`)

Command-based layer (not a skill — ships as `/copy` + 5 sub-commands to avoid auto-activation system-prompt bloat). Wraps existing copy skills with universal gates + reviewers.

| Component | Path | Purpose |
|-----------|------|---------|
| Router | `commands/copy.md` → `/copy` | Asks "what copy?" → delegates to sub-command; loads shared context once |
| Sub-commands | `commands/copy/*.md` → `/copy:sales-letter`, `/copy:email`, `/copy:landing`, `/copy:ad`, `/copy:headline` | Each wraps the matching existing `/content:*` or `/ads:*` command |
| Pre-write gates | `.claude/references/copywriting-os/gates/{channeling-check,coat-of-arms-generator,one-person-seed}.md` | Schwartz/Collier + Halbert enforcement BEFORE writing |
| Pre-write builders | `.claude/references/copywriting-os/builders/{proof-inventory-builder,objection-matrix-builder}.md` | 2 parallel sub-agents. Populate proof-inventory.md + objection-matrix.md feeding B1 + B4 reviewers + drafter |
| Post-write Phase B reviewers | `.claude/references/copywriting-os/reviewers/{claim-verification-audit,forbidden-content-audit,specificity-audit,buyer-language-fidelity-audit}.md` | 4 anti-hallucination sub-agents — grounding verification. FAIL blocks ship regardless of Phase C. |
| Post-write Phase C reviewers | `.claude/references/copywriting-os/reviewers/{one-person-enforcement,proof-density-audit,emotional-sequence-audit,objection-coverage-audit,teardown-reviewer}.md` | 5 persuasion-craft sub-agents via `verification-loops` pattern |
| Reference index | `.claude/references/copywriting-os/_index.md` | Library map; gates/reviewers/frameworks pointers |
| Client workspace template | `clients/_template/copy-system/` | copy-brief + coat-of-arms + scout-instructions + proof-inventory + objection-matrix + outputs/ + quality-gates/ |
| Sandbox reference library | context-mode KB, sources `cai #35` through `cai #45` + `cai schwartz-awareness` + 35 older slugs | 47 copywriting.ai newsletters indexed — queryable via `ctx_search` |

**Source:** Mark Masters + Peggy Burnett + NOVA articles from copywriting.ai archive (47 newsletters). Key frameworks embedded: 5 Headline Mechanisms (cai #39) • 6 Proof Types (cai #38) • 6 Emotional States (cai #37) • 6 Objection Categories (cai #36) • Halbert A-pile + Coat of Arms + One-Person (cai #44) • Collier enter-the-conversation (cai #42) • Schwartz channeling (Schwartz post) • Scout custom instructions (cai #35) • Failure-mode teardown library (cai #45).

**Preferred invocation:** `/copy:<domain>` over the underlying `/content:*` or `/ads:*` commands, so gates + reviewers fire automatically. Direct invocation of the underlying command bypasses the OS layer.

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
