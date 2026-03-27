## Graph Links
- **Parent skill:** [[analytics-attribution]]
- **Sibling references:** [[attribution-models]], [[dashboards]], [[ga4-implementation-guide]], [[google-analytics]], [[reporting-templates]], [[search-console]]
- **Related skills:** [[paid-advertising]], [[ab-test-setup]]

# Analytics & Attribution Frameworks

Comprehensive reference for marketing analytics, attribution modeling, RFM analysis, dashboards, and ROI calculations.

---

## RFM Analysis Framework

RFM (Recency, Frequency, Monetary) segments customers by behavior to prioritize marketing actions.

### Dimensions

| Dimension | Measures | How to Score |
|-----------|----------|-------------|
| **Recency** | Days since last purchase/engagement | Lower = better (recent buyers score higher) |
| **Frequency** | Number of transactions/interactions in period | Higher = better (repeat buyers score higher) |
| **Monetary** | Total revenue/value in period | Higher = better (big spenders score higher) |

### Scoring Methodology (1-5 per Dimension)

Divide customers into quintiles (20% each) for each dimension:

| Score | Recency | Frequency | Monetary |
|-------|---------|-----------|----------|
| 5 | Last 7 days | 10+ orders | Top 20% revenue |
| 4 | 8-30 days | 6-9 orders | 60th-80th percentile |
| 3 | 31-90 days | 3-5 orders | 40th-60th percentile |
| 2 | 91-180 days | 2 orders | 20th-40th percentile |
| 1 | 180+ days | 1 order | Bottom 20% revenue |

*Adjust thresholds to your business cycle. SaaS monthly renewals differ from e-commerce purchase frequency.*

### Customer Segments & Action Plans

| Segment | RFM Score Pattern | % of Base | Priority Action |
|---------|-------------------|-----------|-----------------|
| **Champions** | R:5 F:5 M:5 | 5-10% | Reward loyalty, early access, referral program, upsell premium |
| **Loyal Customers** | R:4-5 F:4-5 M:3-5 | 10-15% | Loyalty program, cross-sell, ask for reviews/testimonials |
| **Potential Loyalists** | R:4-5 F:2-3 M:2-3 | 10-15% | Nurture sequence, membership offers, engagement program |
| **New Customers** | R:5 F:1 M:1-2 | 5-10% | Onboarding sequence, welcome offer, education content |
| **Promising** | R:3-4 F:1-2 M:1-2 | 10-15% | Build relationship, product education, second-purchase incentive |
| **Need Attention** | R:3 F:3 M:3 | 10-15% | Re-engagement campaign, limited-time offer, survey for feedback |
| **At Risk** | R:2 F:3-5 M:3-5 | 5-10% | Win-back urgency, personal outreach, "we miss you" + incentive |
| **Can't Lose** | R:1-2 F:4-5 M:4-5 | 3-5% | Highest priority win-back, executive outreach, premium offer |
| **Hibernating** | R:1-2 F:1-2 M:1-3 | 15-20% | Low-cost reactivation, brand awareness ads, sunset if no response |
| **Lost** | R:1 F:1 M:1 | 10-20% | Last-chance offer, then suppress from active campaigns to save budget |

### RFM Implementation Steps
1. Pull transaction data for 12-month window
2. Calculate R, F, M values per customer
3. Score each dimension 1-5 (quintile method)
4. Concatenate scores (e.g., "553" = R:5, F:5, M:3)
5. Map to segments using pattern table above
6. Build segment-specific campaigns
7. Re-score monthly — track segment migration as a health metric

---

## Executive Dashboard Patterns

### C-Suite Dashboard (5 Metrics Max)
**Purpose:** Board-level view. Answer "Is marketing driving growth?"
**Refresh:** Weekly summary, monthly deep dive

| Metric | Definition | Target Direction |
|--------|-----------|-----------------|
| Revenue from Marketing | Revenue attributed to marketing-sourced leads | Up |
| Customer Acquisition Cost (CAC) | Total marketing spend / new customers acquired | Down |
| Lifetime Value (LTV) | Average revenue per customer over their lifetime | Up |
| LTV:CAC Ratio | LTV / CAC (healthy = 3:1 or better) | Up |
| Marketing-Sourced Pipeline | Total value of deals originated by marketing | Up |

**Design rule:** One number per card, with trend arrow and comparison to prior period. No charts needed — just big numbers.

### Marketing Ops Dashboard
**Purpose:** Channel and campaign performance. Answer "What's working and what's not?"
**Refresh:** Daily check, weekly review

| Section | Metrics |
|---------|---------|
| Channel Performance | Spend, leads, CPA, ROAS per channel |
| Campaign Metrics | Impressions, clicks, CTR, conversions, CPA per campaign |
| Funnel Conversion | Visitor → Lead → MQL → SQL → Opportunity → Customer (with conversion rates) |
| Budget Pacing | Spend vs. budget, projected end-of-month spend |
| Top Performers | Top 5 campaigns by ROAS or volume this period |

### Content Dashboard
**Purpose:** Content marketing effectiveness. Answer "Is our content attracting and converting?"
**Refresh:** Weekly

| Section | Metrics |
|---------|---------|
| Traffic | Sessions, unique visitors, traffic by source |
| Engagement | Avg. time on page, bounce rate, pages per session |
| SEO | Keyword rankings (movement), organic traffic, new backlinks |
| Content ROI | Leads generated per content piece, assisted conversions |
| Pipeline | Top 10 content pieces by lead generation or revenue influence |

### Email Dashboard
**Purpose:** Email program health. Answer "Are our emails driving engagement and revenue?"
**Refresh:** Per-send for campaigns, weekly for program health

| Section | Metrics |
|---------|---------|
| Deliverability | Delivery rate, bounce rate, spam complaint rate |
| Engagement | Open rate, click rate, click-to-open rate |
| Revenue | Revenue per email, revenue per subscriber |
| List Health | List growth rate, unsubscribe rate, active subscriber % |
| Automation | Sequence completion rate, drop-off points |

### Recommended Refresh Cadence

| Dashboard | Real-time | Daily | Weekly | Monthly |
|-----------|-----------|-------|--------|---------|
| C-Suite | - | - | Summary | Deep dive |
| Marketing Ops | Ad spend alerts | Full review | Team review | Strategy adjust |
| Content | - | Traffic check | Full review | Content planning |
| Email | Deliverability alerts | Campaign results | Program review | List strategy |

---

## Multi-Touch Attribution Models

### Model Comparison

| Model | Credit Distribution | Best For | Limitation |
|-------|-------------------|----------|------------|
| **First-Touch** | 100% to first interaction | Measuring awareness/discovery effectiveness | Ignores everything after first touch |
| **Last-Touch** | 100% to last interaction before conversion | Direct response, short sales cycles | Ignores awareness and nurture |
| **Linear** | Equal credit to all touchpoints | Understanding full journey, no strong hypothesis | Over-credits low-impact touches |
| **Time-Decay** | More credit to recent touches (exponential decay) | Long sales cycles, nurture-heavy funnels | Undervalues early awareness |
| **Position-Based (U-shaped)** | 40% first, 40% last, 20% split across middle | Balanced view of discovery + conversion | Arbitrary weight split |
| **W-shaped** | 30% first, 30% lead creation, 30% opportunity creation, 10% middle | B2B with clear stage transitions | Requires stage tracking |
| **Data-Driven** | ML algorithm assigns credit based on patterns | High-volume accounts with 600+ conversions/mo | Needs significant data, black-box logic |

### Decision Framework: Which Model to Use

```
Start here:
│
├── Sales cycle < 7 days?
│   ├── YES → Last-Touch (simple, actionable)
│   └── NO ↓
│
├── Sales cycle 7-30 days?
│   ├── Content/nurture heavy? → Linear or Time-Decay
│   └── Ad-driven? → Position-Based (U-shaped)
│
├── Sales cycle 30+ days (B2B)?
│   ├── Clear funnel stages? → W-shaped
│   └── No clear stages? → Time-Decay
│
└── 600+ conversions/month?
    └── YES → Data-Driven (supplement with position-based for comparison)
```

### Practical Recommendations
- **Run two models simultaneously** — compare results to identify blind spots
- **Last-touch for optimization** — use for daily bid/budget decisions
- **Position-based for strategy** — use for channel investment planning
- **Data-driven for validation** — use to confirm or challenge your assumptions
- **Report multiple models** to stakeholders with explanation of what each reveals

---

## Four-Phase Analytical Workflow

### Phase 1: Collect
**Goal:** Gather clean, reliable data

| Task | Details |
|------|---------|
| Define data sources | GA4, CRM, ad platforms, email, social, sales data |
| Set up tracking | UTM parameters, conversion pixels, event tracking |
| QA checks | Cross-platform data reconciliation (spend, leads, revenue should match within 5%) |
| Data cleaning | Deduplicate, remove test data, handle missing values |
| Documentation | Data dictionary — define every metric, its source, and calculation method |

**Common pitfalls:**
- UTM parameters inconsistent across team members (use a UTM builder template)
- Conversion tracking firing on wrong pages (test with Tag Assistant)
- Timezone mismatches between platforms (standardize to one timezone)

### Phase 2: Analyze
**Goal:** Find patterns and segment data for insights

| Technique | When to Use | Example |
|-----------|------------|---------|
| Trend analysis | Track changes over time | "Organic traffic grew 15% MoM for 3 months" |
| Segmentation | Break data into meaningful groups | "Mobile users convert 40% less than desktop" |
| Cohort analysis | Compare groups over same timeframe | "Jan signups retained 20% better than Feb signups" |
| Correlation analysis | Find relationships between metrics | "Blog posts >2,000 words generate 3x more backlinks" |
| Funnel analysis | Identify drop-off points | "60% of leads drop between MQL and SQL stage" |
| Comparative analysis | Benchmark against prior period or industry | "Our CTR is 2x industry average on branded terms" |

### Phase 3: Interpret
**Goal:** Turn data into business-meaningful insights

| Principle | Application |
|-----------|-------------|
| Correlation ≠ Causation | "Revenue went up when we launched ads AND hired 2 SDRs — which caused it?" |
| Business context first | "CPA increased 30% but we also moved upmarket — higher CPA is expected for enterprise" |
| Statistical significance | "Don't act on 3 days of data. Wait for 95% confidence or 2+ weeks minimum." |
| Segment before averaging | "Average CPA is $50 but brand is $10 and non-brand is $90 — very different stories" |
| Ask 'So what?' three times | Data → Insight → Action. "Traffic is down" → "Organic is down because rankings dropped" → "Refresh top 10 declining pages this week" |

### Phase 4: Act
**Goal:** Turn insights into measurable improvements

| Action Type | Framework | Example |
|-------------|-----------|---------|
| Quick win | <1 week to implement, >10% expected impact | Fix broken landing page, pause wasted ad spend |
| Optimization | 1-4 weeks, iterative improvement | A/B test new headline, adjust bid strategy |
| Strategic shift | 1-3 months, requires planning | Reallocate 30% of budget from Display to Search |
| Experiment | Test a hypothesis with controlled conditions | "If we add video to landing pages, will conversion rate improve?" |

**Feedback loop:** Every action generates new data → return to Phase 1. The cycle never stops.

---

## Marketing ROI Calculations

### Core Formulas

| Metric | Formula | Healthy Benchmark |
|--------|---------|-------------------|
| **ROAS** | Revenue / Ad Spend | 3:1+ (varies by industry) |
| **CAC** | Total Marketing Spend / New Customers | Depends on LTV (target LTV:CAC ≥ 3:1) |
| **LTV** | Avg Revenue per Customer × Avg Customer Lifespan | Higher = more room for CAC |
| **Marketing Efficiency Ratio (MER)** | Total Revenue / Total Marketing Spend | 5:1+ for mature businesses |
| **Payback Period** | CAC / Monthly Revenue per Customer | <12 months for SaaS, <3 months for e-commerce |
| **Contribution Margin** | (Revenue - Variable Costs) / Revenue | 60-80% for SaaS, 30-50% for e-commerce |

### Extended Formulas

**Blended CAC vs. Paid CAC**
- Blended CAC = Total Marketing Spend / All New Customers
- Paid CAC = Paid Ad Spend / Paid-Attributed New Customers
- Track both — blended shows overall efficiency, paid shows ad efficiency

**LTV Calculation Methods**

| Method | Formula | Best For |
|--------|---------|----------|
| Simple | Avg Order Value × Purchase Frequency × Customer Lifespan | E-commerce with consistent AOV |
| Subscription | ARPU × (1 / Monthly Churn Rate) | SaaS with monthly billing |
| Cohort-based | Sum of revenue per cohort / cohort size over time | Most accurate, requires 12+ months of data |
| Predictive | ML model using RFM + behavioral signals | High-volume businesses with rich data |

**Channel-Level ROI**
```
Channel ROI = (Channel Revenue - Channel Spend) / Channel Spend × 100
```

Example: Google Ads generated $50K revenue on $10K spend → ROI = ($50K - $10K) / $10K × 100 = 400%

**Incremental ROAS (iROAS)**
```
iROAS = (Revenue with Ads - Revenue without Ads) / Ad Spend
```
Measures the TRUE lift from advertising, not just attributed revenue. Requires holdout/geo-lift testing.

### Benchmark Ranges by Business Type

| Metric | B2B SaaS | E-commerce | Local Services | Agency |
|--------|----------|-----------|---------------|--------|
| CAC | $200-$2,000 | $10-$100 | $50-$500 | $500-$5,000 |
| LTV | $1,000-$50,000 | $100-$1,000 | $500-$10,000 | $5,000-$100,000 |
| LTV:CAC | 3:1 - 8:1 | 3:1 - 5:1 | 3:1 - 10:1 | 4:1 - 10:1 |
| Payback Period | 6-18 months | 1-3 months | 1-6 months | 3-12 months |
| Blended ROAS | 3:1 - 10:1 | 4:1 - 8:1 | 5:1 - 15:1 | 5:1 - 20:1 |

### ROI Reporting Tips
- Always report **blended AND channel-level** — blended for executives, channel-level for optimization
- Include **time lag** — B2B conversions often take 30-90 days after first click
- Show **trend, not snapshot** — a single month's ROI is noise; 3-month rolling average is signal
- Account for **attribution window** — Meta defaults to 7-day click / 1-day view; Google defaults to 30-day click
- **Never compare ROAS across platforms** without normalizing attribution windows first

---

*Attribution: Analytics frameworks adapted from msitarzewski/agency-agents Analytics Reporter patterns. Enhanced for AgentKits context.*
