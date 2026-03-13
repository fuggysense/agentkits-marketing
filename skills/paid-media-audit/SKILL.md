---
name: paid-media-audit
version: "1.0.0"
brand: AgentKits Marketing by AityTech
description: Systematic audit framework for evaluating paid advertising accounts across Google Ads, Meta Ads, LinkedIn Ads, and TikTok Ads. Covers 200+ checkpoints spanning account structure, tracking, bidding, targeting, creative, and landing pages.
triggers:
  - paid media audit
  - ad account audit
  - PPC audit
  - ads review
  - advertising audit
  - account health check
  - ad performance review
  - campaign audit
model: sonnet
---

# Paid Media Audit

## Overview

A 5-phase audit workflow for systematically evaluating paid advertising accounts and surfacing actionable improvements.

1. **Scope** — Define audit goals, platforms, timeframe, and success criteria. Align with stakeholders on what "good" looks like.
2. **Extract** — Pull account structure, performance data, tracking configs, audience settings, and budget/bidding parameters from each platform.
3. **Analyze** — Run 200+ checkpoints across 9 categories. Flag issues by severity. Compare against benchmarks.
4. **Score** — Assign severity ratings (P0–P3) to every finding. Estimate budget impact for top issues.
5. **Report** — Compile executive summary, platform-specific findings, budget projections, and a 30/60/90 day action plan.

## When to Use

- New client onboarding / account takeover
- Quarterly account health reviews
- Performance decline diagnosis
- Pre-scale readiness assessment
- Budget reallocation planning

## Audit Framework

### Phase 1: Scope Definition

- Define audit goals, timeframe, and platforms in scope
- Identify key stakeholders and their KPI targets
- Establish benchmark comparisons (historical, industry, competitor)
- Confirm data access — platform accounts, analytics, CRM
- Agree on deliverable format and presentation date

### Phase 2: Data Extraction

- Account structure export (campaigns, ad groups/sets, ads)
- Performance data by campaign/ad group/ad (last 90 days minimum)
- Conversion tracking verification (pixel fires, event logs)
- Audience/targeting review (custom audiences, lookalikes, exclusions)
- Budget and bidding settings (strategy type, caps, pacing)
- Search term reports (Search campaigns)
- Auction insights / competitive data
- Landing page URLs and load times

### Phase 3: Analysis (Organized by Category)

#### Account Structure (10 checkpoints)

- [ ] Campaign naming conventions — consistent, descriptive, parseable
- [ ] Ad group/ad set organization — clear theme per group
- [ ] Match type segmentation (Search) — separated or intentionally blended
- [ ] Campaign objective alignment — objective matches funnel stage
- [ ] Budget distribution efficiency — spend proportional to opportunity
- [ ] Geographic targeting accuracy — no wasted geo spend
- [ ] Device bid adjustments — reflect device performance data
- [ ] Ad schedule optimization — dayparting matches conversion windows
- [ ] Negative keyword coverage — campaign and account-level negatives
- [ ] Audience segmentation depth — distinct audiences, not overlapping

#### Tracking & Measurement (10 checkpoints)

- [ ] Conversion action configuration — primary vs secondary actions correct
- [ ] Pixel/tag firing verification — all pages, all events, no duplicates
- [ ] Attribution window settings — matches sales cycle length
- [ ] Enhanced conversions setup — hashed first-party data flowing
- [ ] Offline conversion tracking — CRM data feeding back to platforms
- [ ] Cross-domain tracking — no data loss across domains
- [ ] UTM parameter consistency — naming convention across all campaigns
- [ ] Google Analytics 4 integration — events, audiences, attribution synced
- [ ] Server-side tracking (if applicable) — reliability and latency check
- [ ] Consent mode compliance — GDPR/CCPA consent signals passing correctly

#### Bidding & Budget (8 checkpoints)

- [ ] Bid strategy alignment with goals — tCPA for leads, tROAS for revenue, etc.
- [ ] Daily/lifetime budget pacing — not limited, not overspending
- [ ] Target CPA/ROAS accuracy — targets realistic vs actual performance
- [ ] Portfolio bid strategy usage — appropriate grouping of campaigns
- [ ] Bid adjustment rationality — data-backed, not arbitrary
- [ ] Budget cap efficiency — no campaigns consistently budget-capped with strong ROAS
- [ ] Impression share vs budget — identifying lost IS due to budget
- [ ] Wasted spend identification — spend on non-converting terms/audiences

#### Keywords & Targeting (10 checkpoints — Search specific)

- [ ] Keyword relevance scoring — keywords match landing page and offer
- [ ] Quality Score distribution — % of spend on QS 7+ keywords
- [ ] Search term report mining — weekly review cadence, action taken
- [ ] Negative keyword hygiene — regular additions, shared lists
- [ ] Match type balance — broad not cannibalizing exact
- [ ] Competitor keyword strategy — branded vs non-branded separation
- [ ] Long-tail coverage — high-intent, low-competition terms present
- [ ] Landing page relevance — keyword-to-page alignment
- [ ] Ad group keyword theme tightness — <15 keywords per group, single theme
- [ ] Keyword cannibalization check — no internal competition between campaigns

#### Creative & Ad Copy (10 checkpoints)

- [ ] RSA headline diversity — 15-headline strategy with varied angles
- [ ] Ad copy A/B testing velocity — at least 2 active variants per group
- [ ] Extension/asset utilization — sitelinks, callouts, structured snippets, images
- [ ] Creative fatigue monitoring — frequency thresholds (Meta: >3/week, Display: >5)
- [ ] Hook-body-CTA structure (Meta) — first 3 seconds, value prop, clear action
- [ ] Video completion rates — benchmarking against platform norms
- [ ] Image/video quality standards — resolution, aspect ratios, text overlay limits
- [ ] Ad-to-landing-page message match — headline and offer continuity
- [ ] Dynamic creative optimization — DCO enabled where appropriate
- [ ] Creative testing statistical rigor — sufficient sample size before declaring winners

#### Shopping / E-commerce (6 checkpoints — if applicable)

- [ ] Product feed quality — titles, descriptions, images, GTINs complete
- [ ] Title/description optimization — keywords in titles, benefit-driven descriptions
- [ ] Performance Max asset groups — segmented by product category/margin
- [ ] Product segmentation — hero products vs long tail separated
- [ ] Pricing competitiveness — price benchmarking vs competitors
- [ ] Shopping campaign structure — branded vs non-branded, margin tiers

#### Landing Pages (8 checkpoints)

- [ ] Page load speed — <3 seconds on mobile and desktop
- [ ] Mobile responsiveness — no layout breaks, tap targets sized correctly
- [ ] Message match with ad copy — headline mirrors ad promise
- [ ] CTA visibility and clarity — above the fold, action-oriented, single focus
- [ ] Trust signals present — logos, testimonials, security badges, guarantees
- [ ] Form friction analysis — minimum fields, progressive profiling
- [ ] Above-the-fold value prop — benefit-first, not feature-first
- [ ] Conversion path clarity — one primary action, minimal distractions

#### Competitive Positioning (5 checkpoints)

- [ ] Auction insight analysis — impression share, overlap rate, outranking share
- [ ] Share of voice assessment — brand vs category coverage
- [ ] Competitor ad copy review — messaging gaps and differentiation
- [ ] Competitive gap opportunities — keywords/audiences competitors miss
- [ ] Market positioning strength — unique angles not being exploited

### Phase 4: Severity Scoring

Rate every finding using this system:

| Severity | Label | Action | Examples |
|----------|-------|--------|----------|
| :red_circle: Critical (P0) | Revenue loss or tracking failure | Fix immediately | Broken pixel, wrong conversion action, budget hemorrhage |
| :orange_circle: High (P1) | Significant inefficiency | Fix within 1 week | Poor bid strategy, missing negatives causing 20%+ waste |
| :yellow_circle: Medium (P2) | Optimization opportunity | Address within 1 month | Low QS keywords, underutilized extensions, creative fatigue |
| :green_circle: Low (P3) | Nice-to-have improvement | Backlog | Naming conventions, minor geo refinements |

**Scoring heuristic:** If fixing this finding would recover/save >5% of monthly spend, it's at least P1.

### Phase 5: Report Generation

Structure the audit report as follows:

1. **Executive Summary** — 1-page overview: platforms audited, total spend reviewed, top 3 wins, top 3 critical issues, estimated monthly savings/gain
2. **Key Findings** — All findings severity-scored, grouped by category, with specific evidence
3. **Platform-Specific Findings** — Detailed breakdown per platform (Google, Meta, LinkedIn, TikTok)
4. **Budget Impact Projections** — Estimated $ impact of fixing P0 and P1 issues
5. **30/60/90 Day Action Plan**
   - **30 days:** Fix all P0 and P1 issues
   - **60 days:** Address P2 optimizations
   - **90 days:** Implement P3 improvements and establish ongoing monitoring

## Workflow

1. **Kick-off:** Confirm platforms, access, goals, and timeframe with stakeholder
2. **Access check:** Verify admin/read access to all ad accounts, analytics, and tag managers
3. **Data pull:** Export last 90 days of performance data, structure, and settings
4. **Checklist run:** Work through `references/audit-checklist.md` for each platform in scope
5. **Score findings:** Assign P0–P3 severity to each issue found
6. **Estimate impact:** Calculate wasted spend and projected savings for top findings
7. **Draft report:** Compile into standard report format (Phase 5 structure)
8. **Review:** Internal QA — does the report tell a clear story?
9. **Deliver:** Present findings with action plan. Get sign-off on priorities.
10. **Track:** Create task list from action plan. Schedule follow-up audit in 90 days.

## Commands

- `/audit:paid-media` — Run full paid media audit (all phases, all categories)
- `/audit:paid-media:quick` — Rapid health check (top 20 checkpoints only — tracking, bidding, top waste)

## Resources

- **Reference:** `./references/audit-checklist.md` — Detailed 200+ checkpoint checklist
- **Skill:** `paid-advertising/SKILL.md` — Platform strategies and campaign management
- **Skill:** `analytics-attribution/SKILL.md` — Measurement framework and attribution models

## Related Skills

| If the task is... | Use instead |
|-------------------|-------------|
| Creating new ad campaigns | `paid-advertising` |
| Optimizing landing page conversions | `page-cro` |
| Setting up tracking | Use `tracking-specialist` agent |
| A/B testing ad variations | `ab-test-setup` |
| Analyzing overall marketing ROI | `analytics-attribution` |

## Self-Annealing

When an audit reveals patterns not covered by the current checklist:
1. Document the new finding with evidence
2. Add checkpoint(s) to `references/audit-checklist.md` under the appropriate category
3. If the finding is platform-specific, add to the platform section
4. Update severity scoring heuristics if the new pattern reveals a gap
5. Log the pattern in `learnings.md` for future audits

---

*Attribution: Audit framework adapted from msitarzewski/agency-agents paid-media auditor patterns. Enhanced with severity scoring and AgentKits integration.*
