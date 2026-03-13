# Paid Media Audit Checklist

> 200+ checkpoint framework for systematic paid advertising account audits.

## How to Use

1. Select relevant platform sections
2. Work through each checkbox systematically
3. Score findings by severity (🔴🟠🟡🟢)
4. Compile into audit report using `SKILL.md` Phase 5 format

**Severity key:**
- 🔴 Critical (P0) — Revenue loss or tracking failure. Fix immediately.
- 🟠 High (P1) — Significant inefficiency. Fix within 1 week.
- 🟡 Medium (P2) — Optimization opportunity. Address within 1 month.
- 🟢 Low (P3) — Nice-to-have improvement. Backlog.

---

## Account Structure (16 checkpoints)

- [ ] Campaign naming follows consistent, parseable convention (platform_objective_audience_geo_date)
- [ ] Campaigns organized by objective (awareness / consideration / conversion)
- [ ] Ad groups/ad sets organized by single theme or audience
- [ ] Match type segmentation strategy is intentional (Search)
- [ ] Campaign objective matches actual funnel stage goal
- [ ] Budget distribution proportional to revenue opportunity
- [ ] Geographic targeting matches serviceable market — no wasted geo spend
- [ ] Device bid adjustments reflect actual device performance data
- [ ] Ad schedule/dayparting aligns with peak conversion windows
- [ ] Negative keyword lists applied at campaign and account level
- [ ] Audience segmentation is distinct — no significant overlap between ad sets
- [ ] Campaign count is manageable — not over-fragmented (consolidation check)
- [ ] Experiments/drafts used for testing rather than duplicating campaigns
- [ ] Labels/tags applied for reporting and filtering
- [ ] Shared budgets used appropriately (or avoided when harmful)
- [ ] Account-level settings reviewed (auto-apply recommendations OFF, correct time zone, currency)

## Tracking & Measurement (16 checkpoints)

- [ ] Conversion actions configured — primary vs secondary correctly assigned
- [ ] Pixel/tag fires on all relevant pages — no missing or duplicate fires
- [ ] Attribution window matches typical sales cycle length
- [ ] Enhanced conversions enabled — hashed first-party data flowing
- [ ] Offline conversion imports set up — CRM closed-won feeding back to platform
- [ ] Cross-domain tracking configured — no data loss between domains
- [ ] UTM parameters consistent across all campaigns and platforms
- [ ] Google Analytics 4 properly integrated — events, audiences, attribution synced
- [ ] Server-side tracking implemented (if applicable) — reliability and latency verified
- [ ] Consent mode compliance — GDPR/CCPA consent signals passing correctly
- [ ] Conversion value assigned correctly (static or dynamic)
- [ ] Micro-conversions tracked (scroll depth, time on site, video views)
- [ ] Phone call tracking configured (if phone is a conversion path)
- [ ] Form submission tracking verified — no double-counting
- [ ] Thank-you page / confirmation event fires only on actual completion
- [ ] Tag Manager container organized — no orphaned or conflicting tags

## Bidding & Budget (12 checkpoints)

- [ ] Bid strategy aligned with business goal (tCPA for leads, tROAS for revenue, maximize conversions for volume)
- [ ] Daily/lifetime budget pacing reviewed — not limited prematurely, not overspending
- [ ] Target CPA/ROAS values realistic based on historical data
- [ ] Portfolio bid strategies used where campaigns share goals
- [ ] Bid adjustments data-backed — not arbitrary percentages
- [ ] No campaigns consistently budget-capped while showing strong ROAS
- [ ] Impression share loss due to budget identified and quantified
- [ ] Wasted spend identified — non-converting search terms, audiences, placements
- [ ] Budget allocation reviewed against funnel stage (prospecting vs retargeting ratio)
- [ ] Seasonal bid/budget adjustments planned and documented
- [ ] Shared budgets not causing one campaign to starve another
- [ ] Bid strategy learning period disruptions minimized (no constant changes)

## Keywords & Targeting (16 checkpoints — Search)

- [ ] Keywords relevant to landing page content and offer
- [ ] Quality Score distribution analyzed — % of spend on QS 7+ keywords
- [ ] Search term report reviewed (last 30, 60, 90 days)
- [ ] Irrelevant search terms added as negatives weekly
- [ ] Negative keyword lists shared across relevant campaigns
- [ ] Match type balance reviewed — broad match not cannibalizing exact match
- [ ] Competitor keyword strategy defined — branded vs non-branded separated
- [ ] Long-tail, high-intent keywords present in account
- [ ] Landing page relevance matches keyword intent
- [ ] Ad group keyword themes tight — <15 keywords per group, single intent
- [ ] No keyword cannibalization between campaigns
- [ ] Low-performing keywords paused or removed (>2x target CPA, zero conversions after significant spend)
- [ ] Keyword bid caps set for high-CPC terms
- [ ] Dynamic search ads (DSA) coverage reviewed for gaps
- [ ] Keyword insertion used appropriately (not in sensitive contexts)
- [ ] Audience layering applied to search campaigns (observation or targeting mode)

## Creative & Ad Copy (16 checkpoints)

- [ ] RSAs have 15 unique headlines with diverse angles (not variations of same message)
- [ ] At least 2 active ad variants per ad group for testing
- [ ] All available extensions/assets utilized (sitelinks, callouts, structured snippets, images, price)
- [ ] Creative fatigue monitored — frequency thresholds respected (Meta: <3/week, Display: <5)
- [ ] Hook in first 3 seconds of video (Meta/TikTok) — grabs attention immediately
- [ ] Body communicates value prop clearly — benefit-first messaging
- [ ] CTA is clear, specific, and action-oriented
- [ ] Video completion rates benchmarked against platform norms
- [ ] Image/video meets platform quality standards (resolution, aspect ratios, text overlay limits)
- [ ] Ad headline matches landing page headline (message match)
- [ ] Dynamic creative optimization (DCO) enabled where data volume supports it
- [ ] Creative testing reaches statistical significance before declaring winners
- [ ] Pin strategy intentional for RSAs — not over-pinning
- [ ] Ad copy includes differentiators (price, speed, guarantee, social proof)
- [ ] Emotional and rational appeals balanced across ad variations
- [ ] UGC-style creative tested alongside polished creative (Meta/TikTok)

## Shopping / E-commerce (11 checkpoints)

- [ ] Product feed complete — titles, descriptions, images, GTINs, prices all populated
- [ ] Product titles optimized — primary keyword + brand + key attribute
- [ ] Product descriptions benefit-driven with relevant keywords
- [ ] Product images high quality — white background, multiple angles where supported
- [ ] Performance Max asset groups segmented by product category or margin tier
- [ ] Hero/best-seller products separated from long-tail SKUs
- [ ] Pricing competitive vs top auction competitors
- [ ] Shopping campaign structure separates branded vs non-branded traffic
- [ ] Supplemental feed used for custom labels and additional attributes
- [ ] Merchant Center diagnostics clean — no disapproved products
- [ ] Product ratings and seller ratings enabled (if eligible)

## Landing Pages (13 checkpoints)

- [ ] Page load speed <3 seconds on mobile (test via PageSpeed Insights)
- [ ] Page load speed <3 seconds on desktop
- [ ] Mobile layout responsive — no horizontal scroll, proper tap targets
- [ ] Headline matches ad promise (message match score)
- [ ] Primary CTA visible above the fold without scrolling
- [ ] CTA text is action-oriented and specific (not "Submit" or "Click Here")
- [ ] Single primary conversion goal — minimal competing CTAs
- [ ] Trust signals present — customer logos, testimonials, security badges, guarantees
- [ ] Form friction minimized — fewest fields possible, progressive profiling for longer forms
- [ ] Above-the-fold section communicates value prop (benefit-first, not feature-first)
- [ ] Social proof near CTA (testimonials, user count, ratings)
- [ ] Exit intent or engagement triggers present (if appropriate)
- [ ] Thank-you page / confirmation has clear next step (not a dead end)

## Competitive Positioning (9 checkpoints)

- [ ] Auction insights reviewed — impression share, overlap rate, outranking share tracked
- [ ] Top 3-5 competitors identified and monitored
- [ ] Share of voice calculated — brand coverage vs category coverage
- [ ] Competitor ad copy analyzed — messaging gaps and differentiation opportunities documented
- [ ] Competitive keyword gaps identified — terms competitors rank for that we don't
- [ ] Competitor landing pages reviewed for CRO ideas
- [ ] Market positioning strength assessed — unique angles not yet exploited
- [ ] Competitor spending trends noted (if available via third-party tools)
- [ ] Defensive branded campaigns running to protect brand terms from competitors

---

## Platform-Specific: Google Ads (17 checkpoints)

- [ ] Account-level automated recommendations reviewed and declined where inappropriate
- [ ] Auto-applied suggestions turned OFF (or reviewed weekly)
- [ ] Search Partners performance evaluated — enabled only if ROAS positive
- [ ] Display Network excluded from Search campaigns (unless intentional)
- [ ] Performance Max campaigns have complete asset groups (text, images, video)
- [ ] Performance Max audience signals configured with first-party data
- [ ] Demand Gen campaigns tested for mid-funnel
- [ ] Discovery/Demand Gen placements reviewed for quality
- [ ] Responsive Search Ads have ad strength "Good" or "Excellent"
- [ ] Broad match keywords paired with Smart Bidding and audience signals
- [ ] Keyword-level final URLs used where appropriate
- [ ] IP exclusions set for known bots/competitors (if applicable)
- [ ] Placement exclusions applied for Display/Video — remove low-quality sites/apps
- [ ] YouTube targeting refined — topics, channels, custom segments
- [ ] Remarketing lists active and properly segmented (RLSA, display, video)
- [ ] Customer Match lists uploaded and refreshed regularly
- [ ] Conversion action sets assigned correctly per campaign

## Platform-Specific: Meta Ads (16 checkpoints)

- [ ] Campaign budget optimization (CBO) vs ad set budget — intentional choice documented
- [ ] Advantage+ audience tested alongside manual targeting
- [ ] Custom Audiences created from website, CRM, engagement sources
- [ ] Lookalike Audiences built from highest-value seed lists
- [ ] Audience exclusions set — existing customers excluded from acquisition campaigns
- [ ] Placement optimization reviewed — Advantage+ placements vs manual selection
- [ ] Creative format mix tested (single image, carousel, video, collection)
- [ ] Ad creative refreshed before frequency exceeds 3.0 per week
- [ ] Advantage+ Creative enabled for dynamic optimization
- [ ] Catalog/dynamic product ads set up for retargeting (e-commerce)
- [ ] Conversions API (CAPI) implemented alongside browser pixel
- [ ] Event match quality score reviewed (aim for >6.0)
- [ ] Account spending limit set as safety net
- [ ] Ad account structure avoids audience fragmentation (consolidation principle)
- [ ] Special ad categories correctly applied (housing, credit, employment, politics)
- [ ] Cost cap or bid cap tested for scaling control

## Platform-Specific: LinkedIn Ads (11 checkpoints)

- [ ] Campaign objective matches funnel stage (awareness, consideration, conversion)
- [ ] Audience targeting uses job title + seniority + company size layering
- [ ] Matched Audiences created from website visitors, CRM contacts, account lists
- [ ] Audience expansion turned OFF (unless deliberately testing)
- [ ] LinkedIn Audience Network enabled only if quality placements confirmed
- [ ] Ad format mix tested (single image, carousel, video, document, conversation, message)
- [ ] Lead Gen Forms used for in-platform conversion (vs landing page — test both)
- [ ] Lead Gen Form fields minimized — use pre-filled LinkedIn data
- [ ] Frequency cap set to avoid audience fatigue (small B2B audiences saturate fast)
- [ ] Retargeting audiences segmented (video viewers, page visitors, form openers)
- [ ] Conversion tracking via LinkedIn Insight Tag verified and firing

## Platform-Specific: TikTok Ads (11 checkpoints)

- [ ] Campaign objective aligned with funnel stage
- [ ] Smart Performance Campaign (SPC) tested for automated optimization
- [ ] Custom Audiences built from pixel data, CRM, engagement
- [ ] Lookalike Audiences tested at multiple percentage ranges
- [ ] Creative is native-feeling — not repurposed polished ads from other platforms
- [ ] Hook in first 1-2 seconds — text overlay, movement, or pattern interrupt
- [ ] Video length optimized for objective (6-15s for awareness, 15-60s for consideration)
- [ ] TikTok Pixel and Events API both implemented
- [ ] Spark Ads tested — boosting organic creator content
- [ ] Automated Creative Optimization (ACO) tested
- [ ] Placement: TikTok-only vs Pangle/Global App Bundle — performance compared

---

## Quick Audit: Top 20 Checkpoints

Use these for a rapid health check (`/audit:paid-media:quick`):

1. [ ] Conversion tracking firing correctly — no missing or duplicate events
2. [ ] Primary vs secondary conversion actions correctly assigned
3. [ ] Attribution window matches sales cycle
4. [ ] Bid strategy aligned with business goal
5. [ ] No campaigns budget-capped while ROAS-positive
6. [ ] Wasted spend >10% of total — search terms, placements, audiences
7. [ ] Quality Score: >50% of spend on QS 7+ keywords (Search)
8. [ ] Negative keyword coverage adequate — top irrelevant terms blocked
9. [ ] Creative fatigue: frequency below thresholds
10. [ ] At least 2 active ad variants per ad group/ad set
11. [ ] Landing page load speed <3 seconds mobile
12. [ ] Ad-to-landing-page message match
13. [ ] CTA visible above the fold
14. [ ] Audience overlap/cannibalization between campaigns
15. [ ] Remarketing lists active and segmented
16. [ ] Device performance reviewed — bid adjustments applied
17. [ ] Geographic targeting accurate — no wasted geo spend
18. [ ] UTM parameters consistent across all campaigns
19. [ ] Top 3 competitors identified in auction insights
20. [ ] 30-day trend: CPA increasing or ROAS declining? Root cause identified?

---

*Total checkpoints: 200+. Update this checklist via self-annealing when audits reveal new patterns.*
