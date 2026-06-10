# SG Property Data Bot: Strategic Decision Document

**Date:** 2026-03-28
**Source:** 5-agent chatroom (3 rounds) + 3 consensus polls (21 agents each)
**Confidence:** High — strong convergence across all phases

---

## Decision 1: Who We Serve First

**HDB homeowners approaching MOP** — as the free acquisition surface.
**Property agents** — as the paying customers from day one.

These are not sequential. They're a flywheel:
- Homeowner runs free simulator → captures intent signal
- Intent signal becomes qualified lead → sold to agent at flat fee
- Agent buying leads → upsold to $149/mo SaaS subscription
- SaaS revenue → funds more homeowner acquisition

**Poll result:** 4/7 voted homeowners first (HDB MOP), 3/7 voted agents first. But the key insight: both sides agreed they're symbiotic, not competing. The simulator generates demand; the agent product monetizes it.

---

## Decision 2: Business Model

**Three revenue streams, sequenced:**

| Priority | Model | Price | Timeline |
|----------|-------|-------|----------|
| 1 | Agent SaaS subscription | $149/mo ($99 founding cohort, first 30 agents) | Month 1 |
| 2 | Lead marketplace (flat fee per qualified lead) | $150-300/lead | Month 4-6 |
| 3 | White-label API for agencies | $2-5K/mo | Month 9-12 |

**Consensus poll ranked B (Lead Marketplace) and A (Agent SaaS) as #1 and #2** — virtually tied. The non-obvious finding: they're not alternatives, they're a compound system.

**Bridge revenue:** Consulting/done-for-you market analysis ($2-5K/engagement) for immediate cash flow in months 1-3 while SaaS and simulator mature.

**Killed permanently:**
- Transaction % (illegal without CEA license)
- Homeowner subscription ($29-49/mo — low ARPU, high churn, weak in SG)
- Advertising model (needs traffic volume we won't have in Y1)

---

## Decision 3: Product Scope (MVP)

### What ships first (Week 1-6): Agent Intelligence Bot
- MOP window alerts by HDB block/postcode (URA/HDB data)
- Last 3 comparable transactions per block
- Basic competitor activity feed (which agents closed in your district)
- Delivered via Telegram bot
- Price: $99/mo founding cohort (30 seats), then $149/mo

### What ships second (Week 6-10): Free HDB Upgrade Simulator
- 6 inputs: current flat estimate (URA data), outstanding loan, CPF OA proxy, combined income, target condo budget, timeline
- Output: financial readiness score + specific gap ("you're $87K short — here's what changes that")
- Single-run, non-iterative (avoids MAS financial advisory territory)
- Heavy disclaimer: "estimates only, not financial advice"
- Separate brand surface, no Fuggy's Media branding
- Opt-in agent directory at output screen (post-legal-opinion, ~Month 5)

### What's explicitly OUT for Year 1:
- Native mobile app
- Agent performance rankings (PDPA risk without opt-in)
- Iterative financial scenario planning (MAS risk)
- Transaction-contingent fees of any kind
- Homeowner subscription/paywall
- Commercial/industrial property data

---

## Decision 4: Competitive Positioning

> "We are the financial clarity layer for HDB upgraders and the intelligence layer for the agents who serve them — unlike PropertyGuru which sells visibility, 99.co which sells listings, and MAIA which acts as your agent."

**Differentiation matrix:**

| Us | PropertyGuru | 99.co | MAIA |
|----|-------------|-------|------|
| Helps you decide IF you should transact | Assumes you're already transacting | Assumes you're already searching | Acts as your agent in the transaction |
| Free for homeowners, agents pay for intelligence | Agents pay for visibility | Agents pay for listings | Free for buyers, 0.2% commission |
| No commission motive | Commission-driven ecosystem | Commission-driven ecosystem | Commission-dependent revenue |
| MOP-specific targeting | General property search | General property search | General property search |

---

## Decision 5: Platform Strategy

**Telegram first, WhatsApp at month 3-4.**

Consensus poll: 4/7 voted Option C (Telegram first, WhatsApp later). Key reasoning:

**Why Telegram first:**
- $0 API (WhatsApp charges $0.004-0.14/msg after 24hr)
- Rich bot UI — inline keyboards, web apps, custom menus (WhatsApp has none)
- Instant launch (WhatsApp needs 2-3 week approval + business verification)
- Meta banned general-purpose AI chatbots on WhatsApp Jan 2026
- Amble Project (SG dating app) validated Telegram-first → 6K users → native app
- HDB upgraders approaching MOP skew 25-34 — Telegram's core SG demographic (30.1% penetration)
- Avoids head-to-head with MAIA on WhatsApp from day one

**Why WhatsApp at month 3-4 (not never):**
- 84.4% SG penetration vs Telegram's 30.1%
- Agents LIVE on WhatsApp — it's their primary work tool
- 98% open rate for business messages
- Submit WhatsApp Business API application on day 1 (runs in parallel during Telegram validation)

**Dual-platform architecture:**
- Month 1-3: Telegram only (homeowner simulator + agent SaaS)
- Month 3-4: WhatsApp goes live for agent-facing SaaS tier specifically
- Use BotSailor or Ainisa for multi-channel sync (single conversation flow, dual delivery)
- Homeowner simulator stays Telegram-native (rich UI needed)
- Agent alerts/leads delivered on WhatsApp (where they already are)

**Annual cost:** ~$1,000-1,800 for both platforms combined

---

## Decision 6: Regulatory Boundary

### Safe (no license needed)
- Agent SaaS subscription (MOP alerts, market intelligence, competitor tracking)
- Free homeowner simulator with disclaimers ("not financial advice")
- Opt-in agent directory (agents submit their own profile data)
- Block-level data aggregation (no named individuals)
- Flat lead gen fee (paid upfront per lead, NOT tied to transaction outcome)

### Grey zone (get legal opinion first)
- Agent performance comparisons using derived transaction data
- "Recommended agent" features (implies endorsement)
- Named agent rankings without explicit opt-in

### Red zone (CEA license required)
- Any fee calculated as % of transaction value
- Matching buyers to agents with a success fee
- Acting as buyer/seller representative
- Holding deposits or reviewing transaction documents

### MAS/Financial Advisory
- Single-run calculator with disclaimer = safe
- Never say "you should" — only show numbers
- No bank/mortgage product comparisons
- Direct users to licensed financial adviser for actual advice

**Action item:** $3-5K legal opinion from SG-qualified solicitor before launching agent directory feature (~Month 5). Simulator can launch before legal opinion if it carries robust disclaimers and no agent matching.

---

## Decision 7: Relationship to Fuggy's Media

**Separate entities. Separate brands. Separate domains.**

| | Fuggy's Media | New Product |
|---|---|---|
| Model | B2B lead gen agency | B2B SaaS + free consumer tool |
| Price | $5-6K setup + $100-150/lead | $149/mo subscription |
| Delivery | Meta Ads + AI WhatsApp Setter | Telegram/WhatsApp bot |
| Target | Agents wanting appointments | Agents wanting intelligence |
| Brand | Fuggy's Media | TBD (new brand) |

**How they interact:**
- Fuggy's warm agent list seeds first 30 SaaS subscribers (intro, not co-branding)
- New product's simulator eventually generates leads that could also feed Fuggy's clients
- No cross-branding. If agents see Fuggy's name on the homeowner simulator, trust dies.
- Long-term: the new product may cannibalize Fuggy's lead gen if agents can self-serve via the simulator. That's OK — it means the product is working.

---

## Decision 8: The Long-Term Moat

Not the public data. Not the bot. Not the brand.

**The outcome correlation dataset** (Priya's key insight, 8/10 confidence):

1. Homeowner runs simulator → captures intent + financial profile
2. Homeowner opts into agent match → agent receives lead
3. Agent works lead → transaction happens (or doesn't)
4. Outcome data feeds back into matching quality

After 18 months: "Which agent is most likely to close for a 4-room HDB upgrader in Tampines with an $800K budget?" No public data answers that. No competitor has it. PropertyGuru can't build it because their business model incentivizes volume (more leads sold = more revenue), not quality matching.

**Red line:** This dataset stays proprietary forever. Never license it. Never expose via API to portals.

---

## Go-to-Market: First 90 Days

### Week 1-2: Foundation
- [ ] Register new brand (domain, Telegram bot, social handles)
- [ ] Submit WhatsApp Business API application (runs in parallel)
- [ ] Set up URA/HDB API data pipeline
- [ ] Begin $3-5K legal opinion engagement
- [ ] Build agent SaaS MVP — MOP alerts + block-level comps

### Week 3-4: Agent Validation
- [ ] Deploy Telegram bot (agent-facing features only)
- [ ] Reach out to 10 agents from Fuggy's warm list for beta
- [ ] $99/mo founding cohort offer (30 seats, 60-day expiry on pricing)
- [ ] Collect feedback: what's useful, what's missing, what's wrong

### Week 5-6: Agent Launch
- [ ] Incorporate beta feedback
- [ ] Launch to broader agent audience (PropNex/ERA/Huttons contacts)
- [ ] Target: 15-20 paying agents by Week 6
- [ ] Start building homeowner simulator

### Week 7-10: Simulator Build
- [ ] 6-question financial reality check (URA data + CPF rules + ABSD rates)
- [ ] Single-run output with shareable PDF summary
- [ ] Heavy disclaimer baked into UX
- [ ] No agent matching yet — just data value
- [ ] SEO-index for "HDB upgrade calculator Singapore"

### Week 10-12: Simulator Launch
- [ ] Deploy on separate brand surface (Telegram bot, landing page)
- [ ] Seed distribution: share in HDB Facebook groups, Reddit r/singaporefi
- [ ] Track: completion rates, sharing rates, email capture rates
- [ ] Begin routing simulator completions as intent signals to agent dashboard

### Revenue targets:
- Month 1: $0-990 (consulting bridge + first beta agents)
- Month 2: $1,500-3,000 (15-20 agents at $99-149)
- Month 3: $3,000-5,000 (30+ agents + first lead sales)

---

## Tech Stack (High-Level)

| Component | Tool | Monthly Cost |
|-----------|------|-------------|
| Telegram Bot | Telegram Bot API (python-telegram-bot or grammy) | $0 |
| WhatsApp Bot (Month 3+) | WhatsApp Business API via BSP | $50-150 |
| Data pipeline | URA/HDB APIs → PostgreSQL/SQLite | $0-20 (Supabase free tier) |
| Hosting | Railway or Fly.io | $5-20 |
| AI layer | Claude API (for natural language queries) | $20-50 |
| Multi-channel sync | BotSailor or custom | $0-30 |
| Landing page | Simple static site (Netlify) | $0 |
| **Total** | | **$75-270/month** |

Infrastructure cost is negligible. The investment is Jerel's time + the legal opinion ($3-5K one-time).

---

## Kill Criteria

Stop and pivot if:
- [ ] Can't get 15 paying agents in 90 days via warm outreach
- [ ] Agent churn exceeds 40% in first 3 months (product isn't sticky)
- [ ] Simulator completion rate below 20% (tool isn't useful enough)
- [ ] CEA issues a directive specifically targeting PropTech data platforms
- [ ] URA/HDB APIs become restricted or rate-limited beyond usability
- [ ] A funded competitor launches identical positioning within 6 months

---

## Open Questions Needing More Research

1. **URA/HDB API documentation** — What exact data fields are available? Rate limits? Data freshness? Need a technical spike before committing to simulator accuracy.

2. **MAIA product teardown** — Sign up, interact with the WhatsApp bot, document every feature and limitation. Know exactly what you're differentiating against.

3. **CPF calculation accuracy** — The simulator needs correct accrued interest rules, resale levy, income ceiling. Get a PropTech engineer to scope this before committing timeline.

4. **WhatsApp AI bot ban specifics** — What exactly did Meta ban? Does a "specific-use property intelligence tool" qualify for exemption? Research before WhatsApp launch.

5. **Brand naming** — The new brand needs to signal trust, data, and SG property. Not "Fuggy's" anything. Research available .sg domains and Telegram bot handles.

6. **Amble's monetization learnings** — They charge $10/mo on Telegram. How's conversion? What's the SG willingness to pay inside a Telegram bot? Worth a deeper teardown or founder outreach.
