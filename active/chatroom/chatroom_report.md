# Agent Chatroom Report: SG Property Data Bot

**Problem**: Should Jerel build a Singapore property data monetization business via AI bot? Who to serve, what to charge, how to position?
**Agents**: 5 | **Rounds**: 3
**Date**: 2026-03-28

## Participants

| Agent | Role | Final Confidence |
|-------|------|-----------------|
| Marcus | SG Property Agent (top 10%, $50K/mo) | 8/10 |
| Sarah | HDB Upgrader (35yo couple, hitting MOP) | 7/10 |
| Wei | Marketplace Strategist (2-sided marketplace builder) | 7/10 |
| Priya | PropTech Competitor Analyst (works at MAIA/MOGUL.sg) | 8/10 |
| Daniel | CEA Compliance Advisor (15 years regulation) | 8/10 |

---

## Consensus (All 5 Agreed)

### Strategic Direction
1. **Agent SaaS revenue first.** Homeowner tools second. Agents pay, homeowners get free tools.
2. **New brand, separate from Fuggy's Media.** Not "eventually separate" — separate at launch. Fuggy's agent relationships seed the first 30 subscribers, but the product stands independently.
3. **No transaction % in year 1.** Flat SaaS subscription only. Daniel killed referral fees definitively — transaction-contingent income = unlicensed estate agent activity under CEA Section 28.
4. **Free HDB Upgrade Simulator as lead gen**, not homeowner subscription. Sarah conceded the $29-49/mo tier. The simulator is a surface for capturing intent, not a revenue line.
5. **Build on URA/HDB APIs as primary data source.** OpenAgent.sg scraping is fragile (no API, can be blocked). Use it as enrichment, not foundation.
6. **Get a $3-5K legal opinion from SG-qualified solicitor before launching agent matching.** CEA enforcement on PropTech is evolving. Documented legal review is insurance.

### Pricing
- **$149/month** (all converged here)
- Wei's addition: $99 founding cohort for first 30 agents (60-day hard expiry, then $149)
- 14-day free trial, no freemium tier

### Sequencing
| Timeline | Milestone |
|----------|-----------|
| Week 1-6 | Agent SaaS MVP live (MOP alerts, block-level comps) |
| Week 6-10 | Build homeowner simulator |
| Week 10 | Simulator goes live (free, separate brand surface) |
| Month 5 | Agent directory added to simulator (post-legal-opinion) |
| Month 8+ | Outcome correlation layer activates |

---

## Key Disagreements (Resolved)

| Question | Round 1 Split | Round 3 Resolution |
|----------|--------------|-------------------|
| Homeowner-first or agent-first? | 4:1 (Sarah alone on homeowner-first) | All 5: agent-first, simulator at Week 10 |
| Parallel or sequential launch? | Priya/Sarah: parallel. Marcus/Wei/Daniel: sequential | All 5: sequential (agent SaaS → simulator) |
| Homeowner subscription? | Sarah: $29-49/mo. Everyone else: free | All 5: free forever |
| Transaction referral fee? | Priya: 0.1-0.2%. Daniel: illegal without license | All 5: no transaction % in year 1 |
| Fuggy's Media 2.0 or separate? | Wei: Fuggy's 2.0. Everyone else: separate | All 5: separate brand |
| Pricing | $99 (Marcus) to $499 (Wei) | All 5: $149/mo ($99 founding cohort) |

---

## Red Lines (Non-Negotiable Per Agent)

| Agent | Red Line |
|-------|----------|
| Marcus | Agent revenue before any homeowner monetization. Simulator is lead gen, not revenue. |
| Sarah | Simulator must be genuinely useful — not a glorified lead capture form. Real financial value or the trust angle collapses. |
| Wei | New brand fully separate from Fuggy's before anything ships publicly. No association = no poison. |
| Priya | Outcome correlation data (which agent-lead pairings close) stays proprietary forever. Never license, never expose via API. This is the moat. |
| Daniel | No ranking by performance metrics unless every agent opts in AND methodology is disclosed. Randomize or let agents self-sequence via paid tiers. |

---

## The Long-Term Moat (Priya's Key Insight)

The real defensible asset isn't the public data. It's the **outcome correlation layer** built over 12-18 months:

1. Homeowner runs simulator → captures intent signal
2. Homeowner opts into agent match → agent receives lead
3. Agent works the lead → transaction happens (or doesn't)
4. That outcome data feeds back into matching quality

After 18 months, you have a proprietary dataset that answers: "Which agent is most likely to close a deal for a 4-room HDB upgrader in Tampines with a $800K budget?" No public data can tell you that. No competitor has it. That's the moat.

---

## Regulatory Map (Daniel's Framework)

### Safe (No CEA License)
- Agent SaaS subscription (MOP alerts, market intelligence, competitor tracking)
- Free homeowner calculator/simulator with disclaimers
- Opt-in agent directory (agents submit their own profile data)
- Block-level data aggregation and publishing
- Flat lead gen fee (paid upfront per lead passed, NOT contingent on transaction)

### Grey Zone (Get Legal Opinion First)
- Agent performance comparisons using derived transaction data
- "Recommended agent" features (implies endorsement)
- Iterative financial scenario planning (approaches financial advisory)

### Red Zone (CEA License Required)
- Any fee calculated as % of transaction value
- Matching buyers to agents with a success fee
- Acting as buyer/seller agent (what MAIA does at 0.2%)
- Holding deposits, reviewing OTP terms

### MAS/Financial Advisory
- Single-run calculator with disclaimer = safe
- Iterative scenario planning with recommendations = approaches FAA territory
- Never say "you should" — only show numbers

---

## Relationship to Fuggy's Media

**Separate entities.** Not a pivot, not a rename, not an extension.

- Fuggy's Media: B2B lead gen agency. High-touch. $5-6K + pay-per-lead. Meta Ads + AI Setter.
- New product: B2B SaaS. Self-serve. $149/mo subscription. Data intelligence + homeowner lead gen.

**How they interact:**
- Fuggy's agent relationships seed the first 30 SaaS subscribers (warm intros)
- The new product's homeowner simulator eventually generates leads that could feed Fuggy's clients too
- But they must have different brands, different domains, different positioning
- Why: if agents see "Fuggy's Media" on the homeowner simulator, they'll assume it's a sales funnel for Fuggy's clients. Trust dies.

---

## Debate Highlights

**Mind changes:**
- Sarah (Round 1 → Round 3): Moved from "homeowners first, $29-49/mo sub" to "agents first, simulator free forever, wire for agent revenue from day one." Key driver: acknowledged that homeowner subscription has regulatory risk and agent revenue funds better homeowner tools.
- Wei (Round 1 → Round 3): Moved from "agents only, $199-499/mo, don't touch homeowners until $150K MRR" to "parallel-ish launch at $149, simulator as lead gen surface." Key driver: Sarah's simulator-as-distribution insight and Priya's outcome correlation argument.
- Priya (Round 2 → Round 3): Dropped 0.1-0.2% referral fee after Daniel's definitive CEA analysis. Conceded parallel launch → sequential.

**Sharpest exchange:**
Daniel (Round 2) systematically dismantled every transaction-contingent revenue model with specific CEA section references. Priya's response: "I concede the transaction percentage model entirely for year 1. Flat SaaS fees are defensible, auditable, and remove the conflict-of-interest question before it gets asked."

**Most valuable insight:**
Marcus (Round 2): "Agents have databases of past clients who bought from them 5-7 years ago and are approaching MOP. This is warm pipeline, not cold." → Led to the white-label MOP alert feature idea (agents use the tool to re-engage their own past buyers).

---

---

## Phase 2: Consensus Poll Results

### Poll 1: Launch Persona Priority (7 agents)

| Option | Votes | Strategists |
|--------|-------|-------------|
| A — HDB sellers approaching MOP | **4** | Risk-Averse, Growth Hacker, Customer Empathy, Data-Driven |
| B — Property agents | 3 | Bootstrap, Long-Term, Contrarian |

**Winner: A (HDB MOP homeowners)** — moderate-high confidence. MOP timelines are structural and predictable, simulator has built-in virality in HDB estate communities, and the pain is the most emotionally intense.

**Key dissent:** Bootstrap strategist argues homeowners are "information seekers, not payers" — agents have proven subscription psychology. Resolution: both sides are right. Homeowners are the acquisition surface, agents are the revenue engine.

### Poll 2: Revenue Model Ranking (7 analysts)

| Rank | Model | Avg Position |
|------|-------|-------------|
| 1 | B — Lead Marketplace ($150-300/lead) | 1.57 |
| 2 | A — Agent SaaS ($149/mo) | 1.86 |
| 3 | C — White-label API ($2-5K/mo) | 3.29 |
| 4 | F — Consulting bridge ($2-5K/engagement) | 3.57 |
| 5 | D — Homeowner subscription ($29-49/mo) | 4.71 |
| 6 | E — Advertising | 6.00 (unanimous last) |

**Key insight:** B and A are not competing — they're a flywheel. Simulator generates leads (B), agents buying leads become SaaS subscribers (A), SaaS revenue funds more homeowner acquisition.

### Poll 3: Platform Choice (7 strategists)

| Option | Votes |
|--------|-------|
| C — Telegram first, WhatsApp later | **4** |
| B — WhatsApp only | 2 |
| A — Telegram only | 1 |
| D — Both simultaneously | 0 |

**Winner: C (Telegram first, WhatsApp at month 3-4)** — moderate-high confidence.

Reasoning: Telegram's $0 API, rich UI (inline keyboards, web apps), instant setup, and avoidance of Meta's AI bot ban make it the right validation platform. WhatsApp (84.4% SG penetration) is where agents live, so submit the Business API application on day 1 and port the validated flow at month 3-4.

Amble Project (SG dating app) validated this exact playbook: Telegram bot → 6K users → native app expansion.

---

## Unresolved Risks

1. **Data engineering complexity.** Priya warned repeatedly: "Data engineering harder than it looks." CPF accrued interest calculations, resale levy rules, income ceiling checks — the simulator needs PropTech-specific engineering. Scope with an experienced dev before committing timeline.

2. **Agent adoption speed.** 30 agents in 90 days is achievable via Fuggy's warm list, but depends on demo quality. Without a tight 60-second product demo, agents won't convert.

3. **PropertyGuru response.** 12-18 month window before they notice and respond. Their DataSense product already does market intelligence. The differentiation must be MOP-specific targeting + outcome correlation — not general market data.

4. **CEA enforcement trajectory.** 2023 advisory flagged PropTech platforms aggregating data for agent prospecting. The regulatory environment is tightening. Legal opinion isn't optional.

5. **Simulator accuracy risk.** If financial outputs are wrong, a homeowner makes a bad decision, and the entire trust proposition collapses. Must have correct ABSD rates, stamp duties, CPF rules, current loan limits. These change with government policy — needs maintenance.
