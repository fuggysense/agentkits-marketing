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

### 3. Cloud Automation Layer (Trigger.dev)
- **Suggested:** 260313
- **What:** Use Trigger.dev to run cloud automations — scheduled metrics pulls, content publishing, lead routing, research agents. Claude Code writes TypeScript → push to GitHub → Trigger.dev runs it on their infra.
- **Why Trigger.dev over Inngest:** Runs on THEIR servers (no need for your own Vercel/server), no timeout limits for long-running AI agents, cheaper ($10/mo vs $75/mo first paid tier), proven with Claude Code workflow, fully open-source self-host escape hatch.
- **Why not now:** 1 active client, pre-scale. HITL gates block most automation. Adding infrastructure before volume = premature optimization.
- **Trigger conditions (build when ANY are true):**
  - [ ] Running 3+ campaigns simultaneously
  - [ ] 3+ clients needing automated reporting
  - [ ] 1UP hits $10K MRR, needs 24/7 lead routing
  - [ ] Same MCP metrics pull done 3+ times/week
- **Best first use case when triggered:** Daily metrics collector (GA4 + Postiz → state.yaml)
- **Build phases:**
  1. Daily metrics collector (~1-2 hrs to build)
  2. Scheduled content publishing
  3. Lead routing (24/7)
  4. Full campaign orchestration
- **Tech notes:** Trigger.dev free tier = $5/mo credit, 10 concurrent runs, 10 schedules. TypeScript SDK. GitHub auto-deploy. MCP server available. Stack: Claude Code → TypeScript → GitHub → Trigger.dev. $0 to start.
- **Supersedes:** Entry #2 (Modal.com) for the automation runtime — Trigger.dev handles scheduled tasks, long-running agents, and cron jobs that Modal was planned for. Modal remains an option for pure Python serverless if needed.

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
