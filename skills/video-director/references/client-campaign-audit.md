## Graph Links
- **Parent skill:** [[video-director]]
- **Sibling references:** [[character-bible-template]], [[cinematography-reference]], [[model-selection-guide]], [[realism-tricks]], [[seed-management]], [[video-type-catalog]]
- **Related skills:** [[image-generation]], [[script-skill]], [[campaign-runner]]

# Client Campaign Audit Framework

7-step audit for evaluating AI video ad campaigns. Focus metric: **unique outbound clicks** — the most reliable proxy for actual purchase intent.

---

## The Key Metric: Unique Outbound Clicks

Most vanity metrics (views, impressions, CPM) don't predict revenue. The metric that matters:

| Metric | What It Means | Action Threshold |
|--------|---------------|-----------------|
| **Unique outbound click rate** | % of viewers who clicked through to your site/offer | Below 1% = kill the ad. Above 3% = scale aggressively. |
| Cost per unique outbound click | How much each real click costs | Compare to your target CPA / ROAS |

**Why unique outbound clicks?**
- Filters out repeat clickers (bots, curious but not buyers)
- Directly ties to purchase funnel entry
- Platform-agnostic (works on Meta, TikTok, YouTube)

---

## 7-Step Audit Framework

### Step 1: Pull Raw Data (Metrics Snapshot)

Gather per-ad metrics for the audit period (minimum 7 days, ideally 14):

```
Per ad creative:
- Spend
- Impressions
- Reach
- Video views (3s, ThruPlay/50%, 100%)
- Unique outbound clicks
- Unique outbound click rate
- Cost per unique outbound click
- Frequency
- CTR (all)
- CPM
```

**Data source:** Meta Ads Manager export, or via `meta-ads` MCP integration.

### Step 2: Sort by Performance

Rank all creatives by unique outbound click rate, descending:

| Rank | Creative | Spend | Unique OB Clicks | OB Click Rate | Cost/Click |
|------|----------|-------|-------------------|---------------|------------|
| 1 | Video A | $500 | 45 | 4.2% | $11.11 |
| 2 | Video B | $300 | 18 | 2.8% | $16.67 |
| 3 | Video C | $400 | 8 | 0.7% | $50.00 |

### Step 3: Classify Each Ad

| Click Rate | Classification | Action |
|-----------|----------------|--------|
| > 3% | Winner | Scale spend, create variations |
| 1-3% | Potential | Optimize hook/CTA, test seed variants |
| < 1% | Underperformer | Kill immediately, analyze why |

### Step 4: Analyze the Offer (Not Just the Creative)

Poor click rates often stem from the offer, not the video:

**Value vs Homework Test:**
- Does the offer give VALUE (savings, knowledge, access) or assign HOMEWORK (fill forms, schedule calls, complete steps)?
- High-homework offers kill click rates regardless of creative quality
- Fix: Lead with value, hide the homework

**Offer Audit Questions:**
- [ ] Is the offer clear in the first 3 seconds?
- [ ] Does the viewer know what they GET, not just what they DO?
- [ ] Is the CTA a single, specific action?
- [ ] Is there urgency or scarcity (real, not fake)?
- [ ] Does the offer match the audience temperature (cold vs warm)?

### Step 5: Hook Analysis

Audit the first 3 seconds of each ad:

| Element | Winner Pattern | Loser Pattern |
|---------|---------------|---------------|
| First frame | Unexpected visual, person mid-action | Logo, title card, slow fade-in |
| First words | Question or shocking claim | "Hey guys, welcome to..." |
| Camera | Close-up, slightly off-center | Wide shot, perfectly framed |
| Energy | High — leans in, eyes wide | Low — sitting back, neutral |
| Sound | Starts mid-conversation | Starts with silence or music |

### Step 6: Visual/Technical Audit

Check each ad against realism standards:

- [ ] Does it look like native UGC or like a commercial?
- [ ] Camera movement: handheld or gimbal-smooth?
- [ ] Lighting: natural or studio?
- [ ] Skin: real texture or airbrushed?
- [ ] Aspect ratio: platform-native (9:16 for TikTok, 4:5 for feed)?
- [ ] Any AI tells visible? (extra fingers, uncanny skin, morphing)
- [ ] Text overlays: platform-native or grafted on?

### Step 7: Generate Action Items

For each ad, produce one of three outputs:

**SCALE (> 3% OB click rate):**
```
- Increase daily budget by 20-30%
- Create 3-5 hook variations (same body, different first 3 seconds)
- Test on additional platforms
- Run seed bracket test to find optimal seeds for this style
- Create character bible for the talent (for future consistency)
```

**OPTIMIZE (1-3% OB click rate):**
```
- Test new hook (first 3 seconds only)
- Test different CTA
- Check if offer framing can emphasize VALUE over HOMEWORK
- Try different model/seed for visual improvement
- Narrow audience targeting
```

**KILL (< 1% OB click rate):**
```
- Pause immediately
- Document what didn't work (hook? offer? creative? audience?)
- Log in learnings.md so pattern doesn't repeat
- Reallocate budget to winners
```

---

## Audit Frequency

| Campaign Stage | Audit Frequency |
|---------------|----------------|
| First 7 days (learning) | Daily monitoring, no changes |
| Day 7-14 | First full audit — classify all ads |
| Ongoing | Weekly audit, kill losers fast |
| Monthly | Full creative refresh audit |

---

## Integration with Campaign Runner

When using the `campaign-runner` skill for video campaigns:

1. **Optimization phase** tasks should include this 7-step audit
2. Feed audit results into `clients/<project>/learnings.md`
3. Winner patterns inform next batch of video-director prompts
4. Loser patterns feed into negative examples (what to avoid)

---

*Source: Mikoslab client campaign audit framework (Plan A #15). Metric focus validated across Meta Ads campaigns — unique outbound clicks most predictive of downstream revenue.*
