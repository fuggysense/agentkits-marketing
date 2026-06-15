# Campaign Setup Checklist (pre-launch)

> **HITL publish gate (V4 repo rule):** `.claude/hooks/meta-publish-gate.sh` — Meta DELETEs require operator approval; creates/updates auto-approve. Review happens upstream: write the full spec to `clients/<client>/campaigns/<slug>/campaign-draft.md` first and create everything PAUSED so Jerel can edit before launch. Reads are ungated.

Source: georgeten.com/materials/checklist-campaign-setup.html
Every rule removes a variable that would make test data unreadable.

## The 3 setup rules — no exceptions

**Purchase objective. Always.**
Not Traffic, Reach, or Engagement. Purchase tells Meta what to optimize for inside the broad audience. Ad set: conversion location = website, performance goal = maximize number of conversions, all devices, highest volume, no bid caps. Decline every Meta AI suggestion.

**Minimum $15/day. Minimum 48 hours.**
Below $15/day Meta can't find buyers. Below 48 hours you're reading Day 1 noise.
Exception: low CTR after 24h AND zero ATCs/sales → close early, analyze, re-run.

**Broad. Tier 1. Feeds only.**
No interests. No lookalikes. No stories. No reels. US, UK, CA, AU only.
- Why broad: Meta finds buyers inside the broad pool faster than interest targeting.
- Why feeds only: mixed placements blend CTRs and make data unreadable (e.g. 8.5% feeds + 2.1% stories + 1.3% reels averages to 3.9% — looks like a bad ad, it's just placements).
- Why T1: all English-speaking, all have money for low-ticket. Most expensive inventory = highest-intent eyeballs. Meta shows the warmest buyers first in the first 48h.
- Placements: Facebook feed, Facebook profile feed, Instagram feed, Instagram profile feed.
- Single-country business: top 3–5 cities of that country instead.

## The sales page — 4 rules

1. **Button NOT in the first scroll.** Below the fold (~85% depth works). People reach it only after understanding the offer.
2. **No video.** Too many unknown variables (watched? skipped? disliked voice?).
3. **Price near the button.** An ATC without a visible price is not real intent.
4. **Buy-word on the button.** "Buy Now", "Unlock Now – $47", "Get Access – $47". NEVER "Learn More". The word creates a psychological barrier so only real intent clicks.

## The ad

- **Image does not reveal the offer.** Tease the problem or the result. NO TEXT on the image. The image's job is to make them read the copy, not click the link. If they can decide from the image alone, a funnel step is skipped and CTR data is worthless.
- **Copy is direct, but withhold the price and the full pitch while testing.** No clever angles — the first 48h audience is already looking for this, so name what it is plainly and open a curiosity gap that forces a Learn More click. The price and the money-back guarantee go on the sales PAGE, not the ad. Putting both on the ad means a buyer can decide straight from the feed: don't want it → scroll past → you never learn why; do want it → click without ever needing the page. Either path skips the link click, and that click is the data point you're testing for. Withholding the price is what keeps it readable (George Ten voice note, 260613).
- **When NOT testing — i.e. scaling a proven offer — put everything on the ad.** Once Meta knows who to show it to, full info up front shortens the path to purchase and that's correct. The withhold rule is testing-phase-only: during validation you're analyzing the funnel, so you can't afford to jump over data points (George Ten voice note, 260613).
- **One image, one primary text, one headline, one description per ad.** No flex ads — Meta mixing combinations means you can't tell which part broke. Run 1 ad, or throw 3–5 ads into one ad set and let Meta decide; keep one variable per ad either way.
- **CTA button: Learn More** (Meta default — don't change).

## Tracking — two sources minimum

- **Meta Pixel** firing: PageView, AddToCart, Purchase. Verify with Meta Pixel Helper before launch.
- **Platform checkout tracking** (Shopify/ClickFunnels/Kajabi/etc.) logging checkout views — second source.
- **Microsoft Clarity** installed (free) — required for the heatmap diagnosis if metrics break.
- Never trust one source; if two disagree significantly, one is wrong (usually the pixel).
- Buy from yourself before launch — confirm the whole checkout works. Add PayPal: it measurably lifts cold-traffic conversion.

## API-creation gotchas (learned 260612, 1UP song-ad test)

- **Always set `start_time` ~7 days in the future when creating ad sets via API.** If omitted, Meta stamps creation time, it instantly "starts" (even paused, zero spend), and the schedule field locks forever in UI + API (error 1487057). Locked? Duplicate or recreate the ad set. Update `start_time` to now just before activating.
- **Dayparting needs `lifetime_budget` + `end_time`** — daily budget greys out the scheduling section.
- **Meta may auto-enable Advantage campaign budget (CBO)** and override your ad-set budget with its own default at campaign level. After creating, verify where the budget actually sits (`campaign{daily_budget}` vs adset) and fix at campaign level if needed.
- **Business-owned pixels must be shared to the ad account** (`POST /<pixel_id>/shared_accounts` with `account_id` + `business`) or every ad shows WITH_ISSUES "no access to pixel". Re-save ads to clear the stale flag.

## Running the test

- Run the full 48 hours. Don't pause, edit, restart. Day 1 can look terrible — normal.
- ~33 link clicks = complete test (statistically solid). 15 clicks = directional only.
- Ignore CPC and CPM completely — this is deliberately the most expensive setup on Meta.
