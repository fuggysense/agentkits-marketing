## Graph Links
- **Parent skill:** [[copywriting]]
- **Sibling references:** [[direct-response-copy]], [[frameworks-library]], [[video-ad-scripts]]
- **Related skills:** [[paid-advertising]], [[image-generation]]

# Ad Creative Frameworks

Comprehensive reference for ad creative strategy across Google, Meta, LinkedIn, and TikTok. Covers copy architecture, testing methodology, and message alignment.

---

## RSA (Responsive Search Ad) Architecture

### 15-Headline Strategy

Organize headlines into four categories to give Google maximum mix-and-match flexibility:

**Benefit-Focused (5 headlines)**
Focus on what the customer gets — outcomes, results, transformations.
- "Cut Your [Pain Point] by 50%"
- "Get [Desired Result] in [Timeframe]"
- "Save [X Hours/Dollars] Every [Period]"
- "Finally, [Aspirational Outcome]"
- "[Specific Metric] Improvement Guaranteed"

**Feature/Differentiator-Focused (5 headlines)**
What makes you unique — capabilities, proof points, competitive edges.
- "[Unique Feature] Built for [Audience]"
- "The Only [Category] That [Differentiator]"
- "[X] Integrations | [Y] Features"
- "Rated #1 by [Authority/Review Site]"
- "Trusted by [Number]+ [Customer Type]"

**CTA-Focused (3 headlines)**
Direct action language — tell them exactly what to do next.
- "Start Your Free Trial Today"
- "Get Your Custom Quote — Free"
- "Book a [X]-Minute Demo Now"

**Brand/Social Proof (2 headlines)**
Reinforce trust and recognition.
- "[Brand Name] — [Tagline or Descriptor]"
- "[X] Stars on [Review Platform] | [Y]+ Reviews"

### Description Line Strategy

| Slot | Structure | Purpose |
|------|-----------|---------|
| Desc 1 | Problem → Solution → CTA | Primary message — should work standalone |
| Desc 2 | Differentiator + proof point | Why you over competitors |
| Desc 3 | Offer details + urgency element | Drive immediate action |
| Desc 4 | Alternative angle for secondary audience | Catch different intent |

**Format:** Each description = 90 chars max. Lead with the strongest word. End with action.

### Pin Strategy

| Scenario | Pin Recommendation |
|----------|-------------------|
| Brand compliance required | Pin brand name to H1 or H2 |
| Regulated industry (finance, health) | Pin required disclaimers |
| Strong CTA performer identified | Pin CTA headline to H3 |
| Testing phase | Pin nothing — let Google optimize |
| Mature account with data | Pin only proven winners |

**Rule of thumb:** Fewer pins = better performance. Only pin when you have a business reason. Every pin reduces Google's optimization flexibility by ~30%.

### Headline Testing Velocity
- **Low volume (<100 clicks/week):** Test 2 RSAs per ad group, swap every 4-6 weeks
- **Medium volume (100-500 clicks/week):** Test 3 RSAs, rotate every 2-4 weeks
- **High volume (500+ clicks/week):** Test 3-4 RSAs, review weekly, swap underperformers bi-weekly

---

## Meta Creative Structure

### Hook-Body-CTA Framework (Static Images)

Every static ad image + copy combination follows this three-part structure:

**Hook (stops the scroll)**
The first thing they see — must earn attention in <1 second for image, <2 seconds for primary text.

| Hook Type | Example | Best For |
|-----------|---------|----------|
| Pattern interrupt | Unexpected visual, bold color, unusual layout | Cold audiences, awareness |
| Bold claim | "We 3x'd revenue in 90 days" | Proof-heavy offers |
| Question | "Still doing [painful thing] manually?" | Problem-aware audiences |
| Statistic | "87% of marketers waste budget on..." | Data-driven buyers |
| Before/After | Visual transformation or metric comparison | Results-based offers |

**Body (builds the case)**

| Body Type | Structure | Best For |
|-----------|-----------|----------|
| Story | Character → Struggle → Discovery → Result | Emotional products, founder-led brands |
| Proof | Claim → Evidence → Evidence → Evidence | High-skepticism audiences |
| Education | Insight → Why it matters → How we solve it | Complex or new-category products |
| Comparison | Old way vs. New way (you) | Competitive displacement |

**CTA (drives action)**

| CTA Type | Example | Best For |
|----------|---------|----------|
| Direct | "Start free trial" | Bottom-funnel, high intent |
| Urgency | "Only 12 spots left this month" | Limited offers, events |
| Curiosity | "See how it works →" | Top-funnel, education-first |
| Value-based | "Get your free [resource]" | Lead magnets, gated content |

### Video Ad Structure

| Segment | Timing | Purpose | Tip |
|---------|--------|---------|-----|
| Hook | 0-3s | Stop the scroll | Movement in first frame. Text overlay. Face close-up. |
| Problem | 3-8s | Build relatability | Name the pain specifically. "You know that feeling when..." |
| Solution | 8-20s | Introduce your product | Show, don't just tell. Demo or walkthrough. |
| Proof | 20-30s | Build credibility | Testimonial clip, metric, screenshot, before/after |
| CTA | 30-35s | Drive action | Clear next step. Repeat the offer. End card with URL. |

**Critical:** 65% of viewers who watch past 3 seconds will watch to 15 seconds. The hook IS the ad.

> **For full talking-head video ad scripts**, see [`video-ad-scripts.md`](./video-ad-scripts.md) — 3 complete A-to-Z frameworks (Straight-For-The-Kill, Personal Story, Don't Do That) with step-by-step breakdowns and fill-in templates.

> **For AI-generated video ads**, see the `video-director` skill (11 video types, 3 pipelines). Use script frameworks here for dialogue and copy; use video-director for visual generation prompts that you paste into Sora, Kling, or VEO.

### UGC-Style Creative Guidelines
- Film vertically (9:16) for Reels/Stories, square (1:1) for Feed
- Use natural lighting — avoid studio-perfect aesthetics
- Start with the person talking directly to camera (builds trust faster)
- Include captions/subtitles (85% of feed video is watched without sound)
- Authentic > polished. "iPhone quality" outperforms "production quality" for most offers.
- Brief the creator on the hook — that's the only non-negotiable. Let them be natural for the rest.

---

## Ad-to-Landing-Page Message Alignment

### Headline Echo Technique
The visitor's brain is pattern-matching. If the landing page headline doesn't echo the ad, they bounce.

| Ad Headline | Landing Page Headline | Alignment Score |
|-------------|----------------------|----------------|
| "Cut Onboarding Time by 60%" | "Cut Onboarding Time by 60%" | Perfect (exact match) |
| "Cut Onboarding Time by 60%" | "Faster Employee Onboarding" | Good (concept match) |
| "Cut Onboarding Time by 60%" | "Welcome to Our Platform" | Bad (no connection) |

**Rule:** Landing page headline should be an exact or near-exact echo of the ad headline that drove the click.

### Visual Continuity
- Same hero image or color palette on ad and landing page
- If the ad shows a person, the landing page should show the same person (or same style)
- Consistent brand elements (logo placement, font, color)
- Jarring visual transitions = bounce rate spike

### Offer Consistency
- If the ad says "Free trial" → landing page says "Free trial" (not "Request a demo")
- If the ad says "50% off" → landing page shows the 50% off price immediately
- If the ad promises a specific resource → the form delivers that exact resource

### Scent Trail Verification Checklist
Run this check for every ad → landing page combination:

- [ ] Ad headline echoed in landing page H1
- [ ] Same primary value proposition visible above the fold
- [ ] CTA text matches the ad's promise (free trial, demo, download, etc.)
- [ ] Visual style is consistent (colors, imagery, tone)
- [ ] Offer terms match exactly (price, discount, duration)
- [ ] No unexpected steps between click and conversion (extra pages, surprise requirements)
- [ ] Mobile experience matches desktop (same message, not truncated)

---

## Creative Testing Methodology

### Statistical Significance Requirements
- **Minimum confidence level:** 95%
- **Minimum conversions per variant:** 100 (for reliable CPA/ROAS conclusions)
- **Minimum impressions per variant:** 1,000 (for reliable CTR conclusions)
- **Test duration:** Minimum 7 days (captures day-of-week variation), maximum 30 days (avoids fatigue contamination)
- **Budget rule:** Allocate enough budget to reach statistical significance within 14 days

### Testing Hierarchy
Test in this order — each level has more impact than the next:

| Priority | Test Element | Impact Level | Example |
|----------|-------------|-------------|---------|
| 1 | Concept | Highest | Testimonial ad vs. product demo ad vs. lifestyle ad |
| 2 | Format | High | Static image vs. video vs. carousel vs. UGC |
| 3 | Hook | High | Different opening lines, different lead images |
| 4 | Body | Medium | Story-based vs. feature list vs. comparison |
| 5 | CTA | Lower | "Start free trial" vs. "See pricing" vs. "Learn more" |

**Rule:** Never test CTA variants until you've found winning concepts and hooks. Optimizing a CTA on a losing concept is wasted spend.

### Creative Fatigue Signals
| Signal | Threshold | Action |
|--------|-----------|--------|
| Frequency | >3 (7-day average) | Rotate in new creative |
| CTR declining | >20% drop from peak | Replace or refresh hook |
| CPA rising | >15% above target for 5+ days | Test new concept |
| Relevance score dropping | Below 5 (Meta) | Audience or creative mismatch |
| Engagement rate flat | No improvement in 14 days | Full creative refresh |

### Winner Graduation & Scaling Process
1. **Identify winner:** Variant beats control by 20%+ on primary metric with 95% confidence
2. **Validate:** Run for 3 more days to confirm stability
3. **Graduate:** Move winner to "evergreen" creative set
4. **Scale:** Increase budget by 20-30% every 3-5 days (not overnight — avoids re-entering learning phase on Meta)
5. **Iterate:** Create 2-3 variations of the winner (same concept, different hooks/visuals) for the next test round

### Portfolio Approach
- **Always maintain 3-5 active creatives per ad set** (Meta) or ad group (Google)
- Mix of formats: at least 1 static, 1 video, 1 UGC or carousel
- Stagger launch dates so all creatives don't fatigue simultaneously
- Retire creatives that have been live >60 days (even if still performing — they'll decline soon)
- Keep a "creative backlog" of 5-10 ready-to-launch assets at all times

---

## Platform-Specific Creative Specs

### Quick Reference Table

| Platform | Format | Dimensions | Max File Size | Text Limits |
|----------|--------|-----------|---------------|-------------|
| **Google Search** | RSA Text | N/A | N/A | 30 char headlines (15), 90 char descriptions (4) |
| **Google Display** | Static Image | 300x250, 728x90, 160x600, 336x280, 320x50 | 150 KB | Overlay text <20% of image |
| **Google PMax** | Mixed | 1200x628 (landscape), 960x960 (square), 480x600 (portrait) | 5 MB | 30 char headlines (5), 90 char descriptions (5) |
| **Meta Feed** | Static Image | 1080x1080 (1:1) or 1200x628 (1.91:1) | 30 MB | 125 char primary, 40 char headline, 25 char desc |
| **Meta Stories/Reels** | Vertical | 1080x1920 (9:16) | 30 MB (img), 4 GB (vid) | Keep text in center 1080x1420 safe zone |
| **Meta Video** | MP4/MOV | 1:1 or 4:5 (feed), 9:16 (stories) | 4 GB | Same as static; captions recommended |
| **Meta Carousel** | Multi-image | 1080x1080 per card | 30 MB per card | 2-10 cards; each with unique headline |
| **LinkedIn Single** | Static Image | 1200x627 (1.91:1) or 1080x1080 (1:1) | 5 MB | 150 char intro, 70 char headline |
| **LinkedIn Video** | MP4 | 1:1, 16:9, or 9:16 | 200 MB | 3 sec - 30 min; recommend <90 sec |
| **LinkedIn Carousel** | PDF document | 1080x1080 or 1920x1080 | 100 MB | 2-10 slides |
| **TikTok In-Feed** | Vertical Video | 1080x1920 (9:16) | 500 MB | 5-60 sec; 100 char ad text |
| **TikTok Spark Ads** | Organic post boost | Same as In-Feed | Same | Uses original post caption |

### Platform-Specific Tips
- **Google:** Provide ALL possible asset sizes. Google rewards asset coverage with more impressions.
- **Meta:** 1:1 for Feed, 9:16 for Stories/Reels. Always design both. Text overlay should be minimal and high-contrast.
- **LinkedIn:** Professional tone even in casual formats. Company page followers convert 2x better than cold audience — use follower campaigns.
- **TikTok:** First 2 seconds determine everything. No logos in opening frame. Native-looking content outperforms polished ads 3:1.

---

*Attribution: Ad creative frameworks adapted from msitarzewski/agency-agents Creative Strategist patterns. Enhanced for AgentKits context.*
