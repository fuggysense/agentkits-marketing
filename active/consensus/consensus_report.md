# Multi-Agent Consensus Report

**Problem**: Should we build a GTM Navigator skill? What should it cover? What problem does it solve?
**Agents**: 10
**Date**: 2026-03-13

---

## Consensus (agreed by 10/10 agents)

### 1. Build it — the gap is real
**Unanimous YES.** Confidence range: 85-95% across all 10 agents. No dissent, including the contrarian and risk-averse framings.

The gap is specific: no existing skill takes GTM history as primary input, diagnoses failure modes, filters by business model constraints, and routes to the next path through conversational iteration.

### 2. The core problem it solves
**"I've tried things and they didn't work — what should I try next, and does the answer change because I'm a SaaS/agency/coach?"**

Existing skills are either pre-GTM (offer-builder), execution-assuming (launch-strategy), menu-based (marketing-ideas), or technique-oriented (problem-solving). None are diagnostic + model-aware + iterative.

### 3. Framework: 5 phases (strong convergence)

| Phase | Agents | Core function |
|-------|--------|---------------|
| Model Identification | 10/10 | Classify business type + ACV + sales motion FIRST |
| GTM History Audit | 10/10 | Structured inventory of what's been tried + failure classification |
| Constraint Mapping | 8/10 | Time, budget, audience, proof assets, unfair advantages |
| Path Recommendation | 10/10 | 2-3 ranked paths (not a list), model-aware, with kill criteria |
| Iteration Loop | 10/10 | 30-day return protocol, re-diagnose with new data |

### 4. Business model knowledge — consensus rules

**SaaS:**
- ACV gates everything: <$500/yr = self-serve/PLG; $1K-$10K = sales-assisted; $10K+ = full sales (10/10)
- PLG only works if time-to-value < 10 min without human help (8/10)
- SEO has 6-18 month lag — wrong for "need revenue in 90 days" (10/10)
- Paid ads before PMF = burning money on leaky bucket (9/10)
- Diagnose churn/retention before investing in acquisition (7/10)

**Agency:**
- Referrals are THE primary channel at every stage (10/10)
- Paid ads almost never work until sharp positioning + case studies (10/10)
- Niche > generalist, always (9/10)
- Capacity ceiling: more leads without delivery capacity = churn (8/10)
- Founder personal brand (LinkedIn, speaking) has outsized ROI (8/10)

**Coaching/Consulting:**
- Personal brand IS the distribution — founder is the product (10/10)
- Audience before offer (inverted from SaaS) (9/10)
- DMs + warm outreach + speaking > ads/SEO at early stage (10/10)
- High-ticket ($5K+) requires sales call, not checkout page (8/10)
- One strong transformation story beats 50 generic testimonials (7/10)

### 5. Failure taxonomy — 6 root causes (converged independently)

| Failure Mode | Description |
|-------------|-------------|
| Economics mismatch | Channel cost vs ACV doesn't math (e.g., paid ads for $49/mo SaaS) |
| Channel-model mismatch | Right tactic, wrong business type (e.g., PLG for coaching) |
| Insufficient volume/duration | Abandoned before signal — most common (~"tried content" = 4 posts) |
| Offer problem disguised as GTM | Distribution isn't broken, the offer is (~40% of cases) |
| Execution failure | Right channel, poor implementation |
| Trust/proof gap | Deployed acquisition before building credibility assets |

---

## Divergences (split opinions)

### Phase count: 4 vs 5
- **4 phases** (3 agents): Merge constraint mapping into model ID for speed
- **5 phases** (7 agents): Structural vs situational constraints are different inputs
- **Rec**: 5 phases. Extra phase prevents misdiagnosis.

### Constraint mapping depth
- **Light** (3 agents): 2-3 questions (time, money, audience)
- **Deep** (7 agents): 4-6 questions incl. unfair advantage + proof inventory
- **Rec**: Deep. Proof/audience inventory is what personalizes recommendations.

### "Why do you think it failed?" question
- **Ask it** (6 agents): Founder hypothesis is useful signal even if biased
- **Skip it, ask for metrics** (4 agents): Founders rationalize; collect data, derive diagnosis
- **Rec**: Ask both. Collect quantified outcomes AND hypothesis. Flag discrepancies.

---

## Outliers (unique high-value ideas)

| Idea | Source | Value |
|------|--------|-------|
| "Fast lane" for first-timers — skip history intake if nothing tried | Bootstrap | Prevents skill feeling irrelevant to pre-attempt founders |
| "Offer exit ramp" as hard rule — 40% of cases are offer problems, not GTM | Risk-Averse + 4 others | Route to `/offer:validate`, don't fix GTM on broken offer |
| Micro-payoffs during diagnosis — "here's what I'm noticing" between questions | Customer Empathy | Prevents question fatigue and abandonment |
| Reference marketing-ideas by tactic # instead of encoding 140 tactics inline | Systems Thinker | Keeps skill lean, avoids duplication |
| Chain output to campaign-runner for execution handoff | Systems Thinker | Navigator sets motion, Runner executes sprint |
| Encode disqualifying rules per model, not just positive recommendations | Contrarian | "X is off the table because..." is higher-value than "try X" |
| Sequencing logic: "do X first because it funds/enables Y" | First Principles | Most founders run 3 channels simultaneously and get noise |

---

## Top Risk (8/10 agents flagged)

**Founders can't accurately self-report why things failed.** "Content didn't work" = 4 posts in 2 months or 18 months of committed effort. Skill diagnoses based on user input; user input is systematically biased.

**Mitigation**: Force quantification. Don't accept "X didn't work." Ask: how many, over how many weeks, what measurable result? If can't quantify → flag as "insufficient data" not "confirmed failure." Build skepticism into Phase 2.

**Secondary risk (6/10)**: Scope creep into offer-builder. Build the offer exit ramp from day one.

---

## Individual Agent Framings

| # | Framing | Unique contribution |
|---|---------|-------------------|
| 1 | Neutral | Clean 5-phase framework, 6 failure modes taxonomy |
| 2 | Risk-averse CMO | "Diagnosis theater" risk — sounds smart but confidently wrong on bad inputs |
| 3 | Growth hacker | Fast lane for pre-attempt founders, 4-phase lean version |
| 4 | Contrarian | Don't default to 5 phases. Disqualifying rules > positive recs |
| 5 | First-principles | Sequencing logic — do X first because it funds Y |
| 6 | Customer-empathy | Micro-payoffs during diagnosis prevent abandonment |
| 7 | Bootstrap | Reference marketing-ideas, don't duplicate. Solo operators need speed |
| 8 | Long-term brand | Positions kit as "thinks in business models" — moat vs generic AI tools |
| 9 | Data-driven | Force quantified outcomes, don't trust self-reported failure reasons |
| 10 | Systems thinker | Chain: Navigator -> campaign-runner. Exit ramp: Navigator -> offer-builder |
