# Feature Parking Lot

Ideas that don't fit yet but might later. Check trigger conditions periodically — when they're met, the feature graduates from "parked" to "build it."

**Review cadence:** Check this list during monthly ops reviews (`/ops:monthly`) or when hitting a scaling pain point.

---

## Parked Features

### 1. Embeddings-Based Semantic Search
- **Suggested:** 260312
- **What:** Use Google Gemini Embedding 2 (free tier) to embed skills, assets, campaign content for vector similarity search
- **Why not now:** Claude already does semantic routing natively by reading CLAUDE.md. Adding embeddings is redundant at current scale.
- **Trigger conditions (build when ANY are true):**
  - [ ] 50+ campaigns with hundreds of assets — too many to fit in Claude's context window
  - [ ] Building a standalone web app/dashboard outside Claude Code that needs content matching
  - [ ] Cross-session memory search becomes slow or unreliable across hundreds of files
  - [ ] Need to score voice consistency quantitatively (not just qualitative review)
- **Best first use case when triggered:** Pre-filtering campaign assets before Claude processes them
- **Tech notes:** Gemini Embedding 2 — free tier for text, $0.20/M tokens paid, 8K context, 768-3072 dimensions

### 2. Autonomous Morning Ad Report (Modal.com)
- **Suggested:** 260312
- **What:** Serverless scheduled script on Modal.com that pulls Meta Ads metrics daily, sends to Claude API for analysis, stores learnings, and sends WhatsApp/email summary
- **Why not now:** No live ad campaigns running yet. Need real data flowing before building the pipeline.
- **Trigger conditions (build when ANY are true):**
  - [ ] First Meta ad campaign running for 2+ weeks with real data
  - [ ] Managing 3+ clients with active ad campaigns (manual morning check becomes painful)
  - [ ] Meta Ads API key is configured and working
- **Best first use case when triggered:** Daily pull for 1UP Sales AI Meta campaigns → Claude API audit → WhatsApp summary to Jerel
- **Tech notes:** Modal.com serverless Python, `@modal.Cron("3 8 * * *")`, ~$0.05/day/client (Modal compute + Claude API). Needs: Meta Ads API key, Anthropic API key, WhatsApp/email notification key. Storage: push metrics to GitHub private repo for Claude Code to read locally. Dashboard endpoint possible later on same platform.
- **Build phases:**
  1. Pull + store script (Modal + Meta API)
  2. Add Claude API analysis (autonomous audit)
  3. Add notification (WhatsApp/email summary)
  4. Add dashboard web endpoint (Modal web_endpoint)

### 3. Cloud Automation Layer (Trigger.dev vs Inngest)
- **Suggested:** 260313 | **Updated:** 260314
- **What:** Cloud automation for scheduled ops reviews, metrics pulls, content publishing, lead routing. Claude Code writes code → push to GitHub → platform runs it on their infra. Auto-sends summary to Jerel for approval.
- **Primary use cases:**
  1. Auto-run `/ops:weekly` every Friday → send summary to WhatsApp/email → Jerel approves suggestions
  2. Daily metrics pull (GA4 + Postiz → campaign state)
  3. Scheduled content publishing
  4. Lead routing (24/7)
- **Why not now:** 1 active client, pre-scale. HITL gates block most automation. Session Start Protocol (CLAUDE.md) handles ops freshness checks within Claude Code for now.

#### Platform Comparison

| Factor | Trigger.dev | Inngest |
|--------|-------------|---------|
| **Hosting** | Runs on THEIR servers | Requires YOUR server (Vercel/Railway/etc.) |
| **Timeout** | No limits for long-running tasks | 10s-300s depending on host plan |
| **Pricing** | Free tier: $5/mo credit, 10 concurrent, 10 schedules | Free tier: 500K events/mo, 5 concurrent |
| **SDK** | TypeScript | TypeScript, Python, Go |
| **Long AI agents** | Yes — built for long-running workflows | Limited by host timeout |
| **Self-host** | Open-source, full escape hatch | Open-source, full escape hatch |
| **GitHub deploy** | Auto-deploy from GitHub | Manual or CI/CD |
| **MCP server** | Available | Not available |
| **Event-driven** | Yes (triggers + schedules) | Yes (events + crons — stronger event model) |
| **Fan-out/parallel** | Yes | Yes — stronger (built-in step.run parallelism) |
| **Retries/replay** | Yes | Yes — stronger (automatic retries, replay from any step) |
| **Best for** | Long-running AI agent workflows, cron jobs | Event-driven pipelines, complex multi-step workflows |

#### Recommendation
- **For ops automation (weekly/monthly reviews, metrics pulls):** Trigger.dev — simpler, runs on their servers, no hosting needed
- **For event-driven marketing (new lead → score → route → nurture):** Inngest — stronger event model, better fan-out
- **Both are good.** Start with Trigger.dev (simpler first use case), add Inngest later if event-driven needs grow

- **Trigger conditions (build when ANY are true):**
  - [ ] Running 3+ campaigns simultaneously
  - [ ] 3+ clients needing automated reporting
  - [ ] Same MCP metrics pull done 3+ times/week
  - [ ] Jerel wants ops reviews without opening Claude Code
- **Best first use case when triggered:** Auto `/ops:weekly` on Friday → WhatsApp summary
- **Build phases:**
  1. Weekly ops auto-review (~2 hrs to build on Trigger.dev)
  2. Daily metrics collector
  3. Scheduled content publishing
  4. Lead routing (24/7) — consider Inngest here
  5. Full campaign orchestration
- **Tech notes:** Trigger.dev free = $5/mo credit. Inngest free = 500K events/mo. Both TypeScript. Both open-source self-host. Stack: Claude Code → TypeScript → GitHub → Trigger.dev/Inngest.
- **Supersedes:** Entry #2 (Modal.com) for the automation runtime. Modal remains an option for pure Python serverless (heavy compute like batch transcription).

### 4. External Database for Client/Asset Data
- **Suggested:** 260313
- **What:** Migrate structured data (channels, campaigns, asset metadata) to a queryable database. Strategy docs (ICP, offer, brand-voice) stay as markdown files — only structured/relational data moves.
- **Why not now:** 1 active client. File system + git = versioned, Claude-native, zero-cost database. Adding a real DB adds infrastructure, API layers, and schema maintenance with no benefit at current scale.
- **Trigger conditions (build when ANY are true):**
  - [ ] 10+ active clients (cross-client search via grep becomes weekly pain)
  - [ ] 50+ campaigns (asset deduplication needed)
  - [ ] Need cross-client analytics ("which video types convert best across all clients?")
  - [ ] Time-series campaign metrics need querying (markdown can't do this well)
- **Best first use case when triggered:** `clients/INDEX.json` auto-maintained index mapping clients -> campaigns -> assets. Graduate to SQLite/Supabase only if index outgrows JSON.
- **Migration path (already architected):**
  1. `channels.json` -> Channels table (already structured)
  2. Campaign metadata -> Campaigns table + file refs (markdown stays as files)
  3. Asset metadata -> Assets table with file paths
  4. `learnings.md` -> Learnings table (enables cross-client pattern search)
  5. Strategy docs (icp, offer, brand-voice) -> **Stay as files forever** (rich text doesn't belong in a DB)
- **Interim step:** Add `clients/INDEX.json` as a lightweight queryable index before any real database. Claude can auto-maintain this during `/project:new` and `/campaign:new`.
- **Tech notes:** SQLite (simplest, file-based, no server) or Supabase (if need remote access/dashboard). Pairs with Entry #1 (embeddings) for semantic search over the database.

### 5. Lead Magnet Funnel Deployment Skill
- **Suggested:** 260314
- **What:** Unified lead magnet funnel deployment — Notion doc → landing page → email automation → deploy. End-to-end from content asset to live funnel.
- **Why not now:** Original implementation is stack-specific (Vercel + n8n + Beehiiv) and brand-specific (Remy's templates). Core patterns already extracted to `skills/launch-strategy/references/lead-magnet-funnel-pattern.md` and `skills/email-sequence/templates/lead-magnet-delivery-email.html`.
- **Trigger conditions (build when ANY are true):**
  - [ ] A client uses Vercel + n8n stack and needs automated lead magnet deployment
  - [ ] Kit gets a general-purpose deployment/hosting skill
  - [ ] 3+ lead magnets deployed manually, justifying automation
- **Best first use case when triggered:** Single-command lead magnet deployment for a client with known hosting stack
- **Tech notes:** Source: remygaskell/lead-magnet-launcher skill. Patterns extracted, full skill parked. Would need stack abstraction layer (Vercel/Netlify/Cloudflare) and email provider abstraction (n8n/Zapier/SendGrid).

---

<!-- TEMPLATE for new entries:

### N. Feature Name
- **Suggested:** YYMMDD
- **What:** One-line description
- **Why not now:** Why it doesn't fit current needs
- **Trigger conditions (build when ANY are true):**
  - [ ] Condition 1
  - [ ] Condition 2
- **Best first use case when triggered:** Where to start
- **Tech notes:** Key specs, links, pricing

-->

### 5. Niche Selection System (Video)
- **Suggested:** 260314
- **What:** Systematic framework for identifying which niches produce the best ROI from AI video content. Combines audience sizing, competition analysis, hook pattern density, and monetization potential into a scoring system.
- **Why not now:** Belongs in deep-research or as a standalone skill, not inside video-director. Current focus is upgrading video-director's core production capabilities. Niche selection is upstream strategy, not production tooling.
- **Trigger conditions (build when ANY are true):**
  - [ ] Running video campaigns for 3+ different niches simultaneously — need to compare which niches produce best results
  - [ ] Building a content agency that needs to evaluate new client niches before committing
  - [ ] Script-skill hooks database has 100+ hooks across 5+ niches — enough data to score niche potential
- **Best first use case when triggered:** Score niche potential before starting a new video campaign for a new client/project
- **Tech notes:** Source: Mikoslab niche selection framework (Plan A #16). Would combine with deep-research skill for competitive analysis and campaign-runner for performance data. Scoring: audience size × engagement rate × competition gap × monetization potential.
