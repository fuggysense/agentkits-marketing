# PPC Strategy Frameworks

Comprehensive reference for paid search and PPC campaign architecture, budget allocation, and optimization.

---

## Budget Tier Strategies

### Starter: $1K-$5K/mo
- **Focus:** Single platform (usually Google Search), narrow keyword set
- **Bidding:** Manual CPC to learn cost-per-click baselines
- **Structure:** 2-3 tightly themed campaigns, 3-5 ad groups each
- **Priority:** Find 1-2 profitable keywords/audiences before expanding
- **Testing:** Sequential A/B tests (not enough volume for multivariate)
- **Mindset:** Every dollar is a data purchase. Learn fast, cut losers weekly.

### Growth: $5K-$25K/mo
- **Focus:** Primary platform + 1 secondary (e.g., Google + Meta or LinkedIn)
- **Bidding:** Transition to automated — Enhanced CPC or Target CPA once 30+ conversions/mo
- **Structure:** Brand, non-brand, and competitor campaigns separated
- **Priority:** Scale winners from Starter phase; begin retargeting
- **Testing:** Parallel A/B tests across ad copy and landing pages
- **Mindset:** Double down on what works. Spend 70% on proven, 30% on experiments.

### Scale: $25K-$100K/mo
- **Focus:** Full-funnel across 2-3 platforms
- **Bidding:** Portfolio bid strategies, Target ROAS for revenue-focused campaigns
- **Structure:** Segmented by funnel stage (TOFU awareness, MOFU consideration, BOFU conversion)
- **Priority:** Audience expansion via lookalikes, broad match with smart bidding, Display/Video
- **Testing:** Creative testing at volume (3-5 variants per ad group minimum)
- **Mindset:** Optimize the portfolio, not individual campaigns. Manage blended ROAS.

### Enterprise: $100K+/mo
- **Focus:** Diversified across all relevant platforms, including programmatic
- **Bidding:** Max Conversions / Max Conv. Value with portfolio constraints
- **Structure:** Brand + performance separation, incrementality testing, geo holdouts
- **Priority:** Incremental lift measurement, diminishing returns analysis, brand halo effect
- **Testing:** Always-on testing program with dedicated budget (10-15% of spend)
- **Mindset:** Marginal efficiency. Every new dollar should justify itself vs. existing spend.

---

## Account Architecture Patterns

### Campaign Tier Structure
```
Account
├── Brand Campaigns (protect brand terms, lowest CPA)
│   ├── Brand - Exact
│   └── Brand - Broad/Phrase (catch misspellings, modifiers)
├── Non-Brand Campaigns (growth engine, highest volume)
│   ├── Category Terms
│   ├── Problem/Solution Terms
│   └── Long-tail / Question Terms
├── Competitor Campaigns (conquest, higher CPA acceptable)
│   ├── Competitor Names - Exact
│   └── Competitor + Category Terms
└── Remarketing Campaigns (highest ROAS, lowest volume)
    ├── Site Visitors (7/14/30/90 day windows)
    ├── Cart/Form Abandoners
    └── Past Customers (cross-sell/upsell)
```

### Ad Group Structures

**Theme Clusters (Recommended for most accounts)**
- Group 5-15 closely related keywords per ad group
- Ensures ad relevance without management overhead
- Best when: <500 keywords total, automated bidding

**Single Keyword Ad Groups (SKAGs)**
- One keyword per ad group (exact + phrase match)
- Maximum control over ad copy relevance and Quality Score
- Best when: Manual bidding, high-CPA keywords, granular reporting needed
- Drawback: Management complexity, harder to accumulate conversion data for smart bidding

**Alpha/Beta Testing Structure**
- **Beta campaigns:** Broad match keywords, low bids — used to mine search terms
- **Alpha campaigns:** Exact match winners graduated from Beta — high bids, optimized ads
- Flow: Beta discovers terms → review search term report → promote winners to Alpha → negative match in Beta
- Cadence: Mine search terms weekly, graduate monthly

---

## Google Ads Specifics

### Performance Max (PMax) Optimization
1. **Asset groups:** Create separate asset groups per theme/product line (not one catch-all)
2. **Audience signals:** Add your best audiences as signals (not targets) — customer lists, in-market, custom intent
3. **Asset quality:** Provide maximum assets — 20 images, 5 videos, 5 logos, 15 headlines, 5 descriptions
4. **URL expansion:** Turn OFF if you need landing page control; ON for broad discovery
5. **Negative keywords:** Use account-level negatives (PMax doesn't support campaign-level, use brand exclusions list)
6. **Learning period:** Allow 2-3 weeks before judging performance; don't make changes during learning
7. **Cannibalization check:** Monitor if PMax is eating brand traffic — compare brand campaign metrics before/after PMax launch

### Quality Score Targeting
- **Target:** 70%+ of spend on keywords with QS 7+
- **QS 1-3:** Pause or restructure — ad relevance or landing page issue
- **QS 4-6:** Optimize — improve ad copy relevance, test new landing pages
- **QS 7-8:** Good — maintain, minor optimizations
- **QS 9-10:** Excellent — scale spend, use as ad group templates
- **Components to optimize (in order):** Expected CTR → Ad Relevance → Landing Page Experience

### RSA Best Practices
- **Headlines (15 slots):**
  - 5 benefit-focused (what the customer gets)
  - 5 feature/differentiator-focused (what makes you unique)
  - 3 CTA-focused (action-oriented)
  - 2 brand/social proof (company name, reviews, awards)
- **Pin strategy:**
  - Pin brand name to position 1 or 2 if brand consistency required
  - Pin primary CTA to position 3
  - Leave remaining headlines unpinned for Google to optimize
  - Over-pinning kills performance — pin only when necessary
- **Descriptions (4 slots):**
  - Desc 1: Problem → Solution statement
  - Desc 2: Key differentiator + social proof
  - Desc 3: Offer details + urgency
  - Desc 4: Alternative angle / secondary audience
- **Ad strength:** Aim for "Good" or "Excellent" — but don't sacrifice message clarity for the score

### Smart Bidding Ladder
Progress through this sequence as conversion volume grows:

| Stage | Strategy | When to Use | Min. Data Needed |
|-------|----------|-------------|------------------|
| 1 | Manual CPC | New account, <15 conversions/mo | None |
| 2 | Enhanced CPC | Learning phase, 15-30 conversions/mo | 2 weeks of data |
| 3 | Target CPA | Stable CPA goal, 30-50 conversions/mo | 30+ conversions in 30 days |
| 4 | Target ROAS | Revenue optimization, 50+ conversions/mo | 50+ conversions with value data |
| 5 | Max Conversions (with cap) | Scaling phase, high volume | 100+ conversions in 30 days |

**Rule:** Never skip more than one step. Each stage needs 2-4 weeks of stable data before advancing.

### Search Term Mining Cadence
| Budget | Review Frequency | Action |
|--------|-----------------|--------|
| <$5K/mo | Weekly | Add negatives, promote winners |
| $5K-$25K/mo | 2x/week | Above + identify new ad group themes |
| $25K+/mo | Daily (automated alerts for high-spend terms) | Above + feed into Alpha/Beta structure |

---

## Platform Budget Allocation Framework

Recommended starting allocation by business type (adjust based on performance data):

### B2B SaaS
| Platform | Allocation | Rationale |
|----------|-----------|-----------|
| Google Search | 45-55% | High-intent keyword targeting |
| LinkedIn Ads | 20-30% | Professional audience targeting |
| Meta (FB/IG) | 10-15% | Retargeting + lookalike prospecting |
| Microsoft Ads | 5-10% | Lower CPCs, older/professional demographic |
| Other (Reddit, Quora) | 0-5% | Niche community targeting |

### B2C / D2C E-commerce
| Platform | Allocation | Rationale |
|----------|-----------|-----------|
| Meta (FB/IG) | 35-45% | Visual products, broad targeting |
| Google Shopping | 25-35% | Purchase-intent product searches |
| Google Search | 10-15% | Brand + category terms |
| TikTok Ads | 5-15% | Younger demo, viral creative |
| Pinterest | 0-10% | Discovery/inspiration (home, fashion, food) |

### Local / Service Business
| Platform | Allocation | Rationale |
|----------|-----------|-----------|
| Google Search | 50-60% | "Near me" and service-intent queries |
| Google Local Services | 15-25% | Pay-per-lead, Google Guaranteed badge |
| Meta (FB/IG) | 15-20% | Local awareness + retargeting |
| Microsoft Ads | 5-10% | Supplementary search coverage |

### B2B Professional Services
| Platform | Allocation | Rationale |
|----------|-----------|-----------|
| Google Search | 40-50% | Intent-driven lead generation |
| LinkedIn Ads | 25-35% | Account-based marketing, job-title targeting |
| Meta (FB/IG) | 10-15% | Retargeting decision-makers |
| Microsoft Ads | 5-10% | B2B-skewing audience |

---

## Key PPC Metrics & Benchmarks

### Quality Score Distribution Targets
| QS Range | Target % of Spend | Action |
|----------|-------------------|--------|
| 9-10 | 15-25% | Scale aggressively |
| 7-8 | 45-55% | Maintain, minor optimization |
| 5-6 | 15-25% | Active optimization |
| 1-4 | <5% | Pause, restructure, or fix landing page |

### CTR Benchmarks by Position & Match Type
| Metric | Benchmark | Notes |
|--------|-----------|-------|
| Search (Position 1) | 5-8% | Branded terms can exceed 15% |
| Search (Position 2-3) | 3-5% | Target range for most non-brand |
| Search (Position 4+) | 1-3% | Consider bid increase or ad improvement |
| Exact Match | 4-7% | Should outperform phrase/broad |
| Phrase Match | 2-5% | Mid-range, good for discovery |
| Broad Match (with smart bidding) | 1-3% | Acceptable when CPA is on target |
| Display | 0.3-0.8% | Visual creative quality dependent |
| Shopping | 1-3% | Product image and price dependent |

### CPA Efficiency Ratios by Funnel Stage
| Funnel Stage | CPA Multiple | Example (Base CPA = $50) |
|--------------|-------------|-------------------------|
| TOFU (awareness lead) | 0.3-0.5x | $15-$25 |
| MOFU (qualified lead) | 1x | $50 |
| BOFU (sales-ready lead) | 1.5-3x | $75-$150 |
| Customer acquisition | 3-10x | $150-$500 |

### Impression Share Targets by Campaign Type
| Campaign Type | Target IS | Rationale |
|---------------|----------|-----------|
| Brand | 90%+ | Protect brand terms, don't lose to competitors |
| High-intent non-brand | 60-80% | Maximize visibility on best converters |
| Broad non-brand | 30-50% | Budget-constrained discovery |
| Competitor | 20-40% | Cherry-pick, don't overspend |
| Display/Remarketing | N/A | Use frequency targets instead (3-7 per week) |

---

*Attribution: PPC frameworks adapted from msitarzewski/agency-agents PPC Strategist patterns. Enhanced for AgentKits context.*
