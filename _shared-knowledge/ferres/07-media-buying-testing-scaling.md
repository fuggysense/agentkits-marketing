# Ferres — Media Buying: Testing, Kill/Scale Rules, Feedback Loop (operational rulebook, synthesized)
Primary: Lecture 8 "Media Buying Crash Course" PDF + Cheat Sheet; cross-swept Parts 2/4, Q&A call, Roast My Ads call, Statics Playbook.
Last distilled: 2026-06-10. ⚠️PLATFORM: entire file is Meta-specific unless noted.

## 0. Economics gate (before any media buying)
- Define a Target Cost Per Result (TCPR) per campaign before launch — e.g. $10/lead, $100/call, $100 CAC on a $50 front-end if backend covers it. Every rule below keys off TCPR (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).
- Scale gate: 30-day LTV : CAC ≥ 3:1 (30-day LTV = avg cash collected in first 30 days). If 30-day ROAS ≥ 3x → increase spend; the 30-day window exists so spend can float on a credit card and be repaid from profit (text/08_63630360_The_AI_Ads_Lab_Pt_6_-_Media_Buying_Crash_Course.txt).
- ROAS is a function of offer + funnel + upsells + email, not just ads. Fix the money model before blaming creative (text/08_63630360_The_AI_Ads_Lab_Pt_6_-_Media_Buying_Crash_Course.txt).

## 1. Metric hierarchy (what he watches, in order)
**Ultimate:** 1) ROAS — the only thing that finally matters. 2) Cost per result — best overall indicator of ad strength, but only meaningful in ROAS context: great CPR + no sales = wrong/unqualified leads (text/08_63630360_The_AI_Ads_Lab_Pt_6_-_Media_Buying_Crash_Course.txt).
**Diagnosis (leading) metrics + thresholds:**
| Metric | Reads | KPI | If failing |
|---|---|---|---|
| Thumbstop rate | hook | min 25–30%; First-Frame Retention sub-metric ~90% | test new hooks/formats/visual openers + on-screen text |
| Thruplay (past 15s) | hook + body | min 15–20% | stronger 4–15s storyline, value props earlier, pattern interrupts, faster cuts; use the drop-off chart to fix the exact second |
| Avg watch time | hook + body | min 25–30% of length | front-load benefits before avg drop-off; if watch AND CTR both low, change the angle entirely — wrong ICP resonance |
| CTR (link) | body + CTA | min 2%; 3–5% very solid | more compelling copy, preview what's behind the click, urgency |
| Frequency | fatigue | keep < 3 | refresh creatives, widen targeting, lower warm-audience budget |
All from (text/08_63630360_The_AI_Ads_Lab_Pt_6_-_Media_Buying_Crash_Course.txt). Two judgment notes from the same doc: high CTR + low 15s retention is usually GOOD (hook drives early clicks); the ad's job is the click, not full watch-through — don't over-optimize watch time on a working ad.
**Cost-per-result benchmarks** ⚠️DATED: lead $5–50; call $50–200 (to $500 high-ticket); sale 20–30% of AOV (ecom) or $500–2,000 (high-ticket) (text/08_63630360_The_AI_Ads_Lab_Pt_6_-_Media_Buying_Crash_Course.txt).
**Post-click:** track bounce rate + time on site (GA) and the full click-to-action funnel; put effort on the single weakest stage — 10% improvement at the biggest bottleneck beats polishing strong stages (text/08_63630360_The_AI_Ads_Lab_Pt_6_-_Media_Buying_Crash_Course.txt). To raise revenue per customer, pull AOV first (order bumps, upsell/downsell, bundles) — fastest profitability lever, improves ROAS without more traffic (text/08_63630360_The_AI_Ads_Lab_Pt_6_-_Media_Buying_Crash_Course.txt).

## 2. Test budgets & kill criteria — the 3x TCPR rule
- **Default rule:** let each new ad spend 3x TCPR before a final keep/kill call, unless it's obviously terrible. $10 CPL target → $30 per ad; $100/call target → $300 per ad (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).
- **Keep/kill examples:** at $30 spent with CPL = $30 → kill; at $25 spent with CPL = $8 → keep/scale. Ecom: $300 spent, CAC $280+ and no sign of improvement → kill (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).
- **Early-kill exception:** in learning phase only kill "clear disasters" — e.g. 5x TCPR with horrible CTR and no signs of life. Expect volatility for ~3 days; never nuke the account over one bad day (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).
- **Early-stop inverse:** an obvious winner can end a test early — but then you keep spending on it, not pause it (09_bonus-q-a-call-for-first-20-buyers [00:36:20]).

## 3. Campaign / ad-set structure ⚠️DATED (post-"Andromeda" Meta algo, mid-2025)
- Andromeda-era structure assumes **25–50 ads per ad set** (high-volume creative testing). Meta will concentrate spend into your top 1–3 and starve the rest — that's normal; don't micro-kill every non-spender (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).
- **Budget must feed the ads:** daily budget ÷ TCPR = results/day. Each active ad needs a realistic shot at 3x TCPR spend over 7–14 days; if not, raise budget or cut active-ad count until reads are clean. ($100/day at $10 CPL feeds ~5 test ads; 25 ads on $100/day = no data) (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).
- **Reference build: same ~25 ads across 3 ad sets — Broad, Lookalike, Warm.** Week 1 = launch & learn: run all 3–7 days, ignore daily noise. Then: cold ad sets keep top 3–5 by CPR/ROAS (with a few conversions each), pause the rest; warm ad set can hold 5–10 but watch frequency "like a hawk" — warm frequency > 4 with falling performance → pause + refresh (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).
- **Targeting stance:** no interest-stack micromanagement appears anywhere — targeting is done by (a) the words in the ad: Meta transcribes your video + landing page and matches the message to people, so "creative diversity" means diversity of MESSAGING, not backgrounds (03_part-2-what-makes-a-winning-ad [00:26:17]); and (b) pixel conditioning — whoever reports into the results column teaches Meta who to find next, so guard which event/who converts (22_roast-my-ads-call-for-daniel-throssell-promo-buy [00:28:43]).
- **Learning phase:** pixel wants ~50 optimization events per ad set per week to stabilize (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt; same rule of thumb at 22_roast-my-ads-call-for-daniel-throssell-promo-buy [00:28:24]). If your event is too expensive to hit 50/week (e.g. $100+ booked calls), move the optimization event up-funnel to something cheaper — he put an opt-in before the VSL to feed the pixel volume (22_roast-my-ads-call-for-daniel-throssell-promo-buy [00:29:08]).
- **Spend-concentration diagnosis:** when results crater, check ad-level spend distribution — one "bad-lead magnet" ad can hoover all spend and poison the pixel; he found this by sorting ads by spend, killed the ad, then re-conditioned targeting (22_roast-my-ads-call-for-daniel-throssell-promo-buy [00:27:42]).

## 4. Scaling rules
- **Vertical:** once an ad set hits TCPR, raise budget 20–30% once per day per ad set; don't edit the same ad set multiple times a day (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).
- **Horizontal:** duplicate the winning ad set (same targeting/winners) at 50–100% of original budget; run both, keep what holds (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).
- Re-entering learning after changes is fine — the sin is huge changes too often, not the "learning" label (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).
- **Creative volume is the scaling ceiling:** hook-swap variants on one body are fine at testing budgets, but at scale Meta's "similarity score" flags near-duplicates and each angle exhausts its responsive audience — scaling demands 25–35 completely unique ads (different message/angle end-to-end, not a changed first 5 seconds) (22_roast-my-ads-call-for-daniel-throssell-promo-buy [01:05:48]–[01:07:14]; 03_part-2-what-makes-a-winning-ad [00:27:02]; 05_part-4-how-to-get-paid [00:43:58]). ⚠️DATED — this is his read of the July-2025 algo rebuild (03_part-2-what-makes-a-winning-ad [00:23:17]). "Minority hooks" (fringe motives/benefit-of-the-benefit) can now carry whole ads because the algo matches micro-motives to people (03_part-2-what-makes-a-winning-ad [00:25:48]).

## 5. Ad fatigue — detection + rotation
Fatigue = a former winner sliding. Trigger when ALL of: (1) frequency > 3 on the ad, (2) 7-day CPL/CPA is 30%+ worse than the prior 30-day, (3) thumbstop/CTR/watch-time down vs its winning period. Then: pause the ad → launch 1–3 fresh variations of the SAME angle (same core promise; new hook/opener, new visuals, new first 3 seconds) → judge the new ones by the 3x TCPR rule (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).
Weekly fatigue check: sort by last-7-day spend; for top spenders compare 7d vs 30d CPA/CTR/thumbstop/frequency; rotate a fresh version in for anything matching the pattern (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).
Statics fatigue faster than video (whole message in one glance) — keep feeding fresh statics, frequency under 3 (24_bonus-1-the-winning-statics-playbook [00:01:59]–[00:02:16]).

## 6. Iteration cadence & the creative feedback loop
- **Weekly cycle per ad set:** keep top 3–5 winners → add 2–3 new test ads → pause 2–3 worst, so the set stays "winners + fresh tests," not months of dead ads (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).
- **80/20 next-batch mix:** 80% of tests = iterations of proven winners and swipes (riding existing data), 20% = fresh original concepts — original bangers scale further because they're unseen (24_bonus-1-the-winning-statics-playbook [00:18:14]).
- **Cheap angle pre-test:** before committing an angle to video production, "spin up five statics, spend 100 bucks" and let data answer whether the hook/claim has legs (24_bonus-1-the-winning-statics-playbook [00:01:01]).
- **Recombination play (Motion app)** ⚠️DATED pricing ~$250/mo: per-section performance shows Ad A = strong hook/weak CTA, Ad B = weak hook/strong body → splice A's hook onto B's body for a likely winner. Optional, client-billable (text/08_63630360_The_AI_Ads_Lab_Pt_6_-_Media_Buying_Crash_Course.txt).

## 7. Daily checklist (his literal operating loop)
1. Account-level ROAS/CAC vs target — still economically sound? 2. Tag each ad set WINNER / STABLE / TEST / LOSER. 3. Scale winners slowly (20–30%/day) or duplicate horizontally. 4. Kill losers that hit 3x-TCPR thresholds or show fatigue. 5. Keep ad sets loaded (25–50 ads) but clear obvious losers weekly. 6. Once a week, run the fatigue check and rotate fresh versions of top angles (text/08_63630360_AI_Ads_Lab_-_Media_Buying_Cheat_Sheet.txt).

## 8. The head-to-head "Control Challenge" test (client-acquisition flavor of testing)
His standard new-client proof test — also a clean generic A/B recipe:
1. **Find the control:** view-only access → 30-day window → the ad with the best cost per result is the one to beat (05_part-4-how-to-get-paid [00:41:02]).
2. **Pick a low-CPR funnel** to test on (lead magnet/webinar reg at ~$5–10/lead, not $100–200 booked calls) — at small budgets only cheap conversions reach statistical significance; a 6-vs-5 conversion "win" proves nothing (05_part-4-how-to-get-paid [00:42:06]; 09_bonus-q-a-call-for-first-20-buyers [00:38:02]).
3. **Structure:** duplicate the existing winning campaign; strip to ONE ad set containing the control; keep every setting incl. headlines/primary text; budget $25/day at AD SET level; duplicate that ad set 3x and swap in each challenger — one campaign, 4 identical ad sets, one ad each, for a fair test (text/17_63673992_The_AI_Ads_Lab_Control_Challenge_Checklist.txt).
4. **Budget/duration:** $100/day total for 7 days = $700 — his stated minimum for "enough data to come to a conclusion" (05_part-4-how-to-get-paid [00:41:32]).
5. **Afterwards:** review winners, articulate WHY they won (hook resonance, visual), and feed that into the pitch for the 25–35-unique-ad batch (05_part-4-how-to-get-paid [00:43:34]).

## Unresolved / watch-outs
- Crash-course PDF and its deck disagree on call benchmark upper bound ($200 vs $300) — treat the band as ~$50–300, niche-dependent.
- No stance found on CBO-vs-ABO or bid strategies; his system is creative-led, structure-light. Don't invent precision he doesn't give.
