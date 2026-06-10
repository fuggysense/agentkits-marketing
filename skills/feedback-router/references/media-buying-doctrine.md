# Media-Buying Doctrine — Kill, Scale, Rotate, Refresh

The decision rules the feedback-router cites when it routes a wave. Distilled from `_shared-knowledge/ferres/07-media-buying-testing-scaling.md` (Ferres "Media Buying Crash Course" + Cheat Sheet, cross-swept Parts 2/4, Q&A call, Statics Playbook). The router reads this file for the WHY behind a route; `routing-criteria.md` holds the numeric thresholds.

> ⚠️PLATFORM: every numeric threshold below (frequency, learning-phase events, similarity-score, 25–35 unique ads) is Meta-specific. They came from Ferres reading the post-Andromeda Meta algo (mid-2025). Treat them as Meta defaults, not laws of physics. On TikTok, Google, or any other platform, keep the *logic* and re-derive the *numbers*. Cost bands are also ⚠️DATED (his 2025–26 figures).

---

## 1. The kill rule — 3x TCPR before keep/kill

Define a Target Cost Per Result (TCPR) per campaign before launch: the most you will pay for one lead, call, or sale and stay profitable. Every other rule keys off it.

The rule: **let each new ad spend 3x TCPR before a final keep/kill call**, unless it is obviously terrible. A $10 cost-per-lead target means $30 of spend per ad before you judge it; a $100/call target means $300.

- At $30 spent with CPL = $30 → kill.
- At $25 spent with CPL = $8 → keep and scale.
- Ecommerce: $300 spent, CAC at $280+ and no sign of improvement → kill.

Two exceptions:
- **Early kill (learning phase only):** kill a clear disaster early — 5x TCPR with a horrible CTR and no signs of life. Expect volatility for about 3 days. Never nuke the account over one bad day.
- **Early stop (winner):** an obvious winner can end a test early. But then you *keep spending* on it — you do not pause it.

This is the gate that earns a CUT inside any route. The router never cuts a creative that has not cleared 3x TCPR of spend; below that, a bad number is noise, not a verdict.

(Ferres 07 §2; Cheat Sheet.)

---

## 2. Scaling — vertical and horizontal

Once an ad set hits TCPR, there are two ways to add spend. They are not interchangeable.

- **Vertical:** raise the ad set's budget **20–30% once per day**, per ad set. Do not edit the same ad set more than once a day. Slow and steady — large jumps throw the ad set back into a worse learning phase than the climb is worth.
- **Horizontal:** duplicate the winning ad set (same targeting, same winning ads) at **50–100% of the original budget**. Run both, keep whichever holds.

Re-entering the learning phase after a change is fine. The sin is making huge changes too often, not the "learning" label itself.

**The real ceiling is creative volume.** Hook-swap variants on one body are fine at testing budgets. But at scale, Meta's similarity score flags near-duplicates, and each distinct angle exhausts its own slice of responsive audience. Scaling demands **25–35 genuinely unique ads** — different message and angle end to end, not a changed first 5 seconds. (Ferres 07 §4.) ⚠️PLATFORM

The scale gate sits above all of this: **30-day LTV : CAC ≥ 3:1**. If 30-day ROAS is 3x or better, spend more. The 30-day window exists so spend can float on a card and be repaid from profit. ROAS is a function of offer, funnel, upsells, and email — not just the ads. Fix the money model before blaming creative. (Ferres 07 §0.)

---

## 3. Fatigue — detection and rotation

Fatigue is a former winner sliding. It fires only when **ALL THREE** are true on the ad:

1. **Frequency > 3**
2. **7-day CPL/CPA is 30%+ worse** than the prior 30-day figure
3. **Thumbstop, CTR, or watch-time is down** versus the ad's own winning period

Then: pause the ad, and launch **1–3 fresh variations of the same angle** — same core promise, new hook, new opener, new visuals, new first 3 seconds. Judge the new ones by the 3x TCPR rule. (Ferres 07 §5.) ⚠️PLATFORM (frequency is a Meta metric)

Run the check weekly: sort ads by last-7-day spend; for the top spenders, compare 7d vs 30d on CPA, CTR, thumbstop, and frequency; rotate a fresh version in for anything matching the pattern.

**Statics fatigue faster than video** — a static gives its whole message in one glance, so nothing pulls a viewer back for a second pass. Keep feeding fresh statics; hold frequency under 3. (Ferres 06 Statics Playbook; 07 §5.) ⚠️PLATFORM

When all three fatigue conditions hold across *every* variant at once, that is no longer a single-ad rotation — it is a wave-level signal the router reads as a NEW or BETTER trigger (see §6).

---

## 4. The 80/20 next-batch mix (the MORE / BETTER engine)

Every new batch the router proposes should split:

- **80% iterations of proven winners and swipes.** You ride existing data — your own winners and competitor ads that already paid for their own testing. Lower variance, capped ceiling.
- **20% fresh original concepts.** Originals scale further because they are unseen by the audience and the algorithm, but they are a gamble each time.

So the MORE route is not "spawn five clones of the winner." It is "spawn the next batch at 80/20." The bulk iterates the structural winner; a fifth of it plants something genuinely new so the angle pool keeps refilling. (Ferres 06 Statics Playbook §Strategy split.)

**Cheap angle pre-test before committing to production:** before spending real production budget (especially video), spin up five statics and spend about $100. Let the data answer whether the hook or claim has legs. A static at $100 is the cheapest possible read on an unproven angle. (Ferres 06; 07 §6.) ⚠️DATED ($100 figure)

---

## 5. Comment-mining — a standing objection-research input

Comment sections are free objection research in the customer's own words. People say "scam," "too hard," "too expensive" in the comments under the client's ads and competitor ads. Save those comments, then reuse the *exact* wording in the next batch — the ad that says "I know what you're thinking, this looks like a bullshit scam" is quoting a real commenter back to the market. (Ferres 02 Research Flow; 04 Part 3.)

For the feedback loop this is not a one-time research step. It is a **standing input that feeds every wave's next batch.** When the router proposes a batch (BETTER or MORE), the brief that goes to `ad-concept-engine` / `headline-bank` should carry the freshest comment-mined objections from the wave that just ran:

- New objections that surfaced in the comments since the last batch → new copy beats to answer them.
- Objections that *kept* showing up despite being answered → the answer is not landing; rework that beat, do not just repeat it.
- An objection that appears across many comments → promote it to a standalone angle, not just a body line.

Pull comments via the `reddit` skill (Reddit VoC), `scrapecreators` / `pp-scrape-creators` (IG/TikTok/FB ad-library comments), or the `research` orchestrator in buyer-language mode. Route the heavy scrape through a subagent — never dump raw comment threads into the router's context. The router only needs the distilled objection deltas, not the raw threads.

---

## 6. Diagnosis map — symptom to route

The router translates a wave's metrics into one of NEW / BETTER / MORE. The doctrine behind each:

| Symptom in the wave | Diagnosis | Route |
|---|---|---|
| Rising cost on a single hyper-specific angle; that angle's CPA climbs while others hold | **TAM exhaustion** — the angle scooped its addressable audience, the copy isn't broken | **BETTER** (broaden the angle / new sibling angles in the same theme) or **NEW** if every angle is maxed |
| One angle wins clearly, but hook/copy variance inside it is wide | Execution gap inside a proven angle | **BETTER** |
| One specific creative beats baseline with headroom (frequency low, CTR holding) | Proven winner with room to scale | **MORE** (80/20 batch) |
| Every angle underperforms; or all variants fatigued at once; or a genuine buyer/market shift | The map is wrong, not the execution | **NEW** (research refresh) |

### TAM exhaustion — the BETTER-route diagnosis to name explicitly

Ferres's metaphor: stop hitting one piano note when there are 87 others. An angle that is too niche maxes out its TAM, and **rising costs on a single hyper-specific angle is the symptom** — not a broken hook. (Ferres 03 Angles/Hooks/Copy.)

This matters because the naive read of "this winning angle's CPA is creeping up" is "the creative fatigued, make new creative." Sometimes true. But if frequency is still moderate and the *angle itself* is narrow, the creative is fine — the angle simply ran out of people. The fix is not a fresher execution of the same narrow angle (that re-exhausts the same small pool). The fix is to **widen the angle or open sibling angles in the same theme** — which is a BETTER route (re-ideate within/around the winning theme), or a NEW route if the whole angle pool is scooped. The router should say "TAM-exhaustion suspected: angle pool scooped, not copy broken" in its rationale so the next batch widens reach instead of polishing a maxed-out note.

---

## 7. What the router does NOT decide

This doctrine is creative-led and structure-light, by design. Ferres gives no stance on CBO vs ABO or bid strategies. The router does not invent precision he never gave. It routes the *creative direction* (NEW / BETTER / MORE) and the *kill/scale calls* the rules above support. Budget-structure mechanics stay with the human media buyer.

The router also never *executes* a route. It outputs the diagnosis, the kill/keep list, and the recommended next intent (see SKILL.md Phase 4). The operator approves and runs it. HITL holds at every loop boundary.

---

## Source map

| Rule | Ferres source |
|---|---|
| TCPR + 3x kill rule | 07 §0, §2 (Cheat Sheet) |
| Vertical / horizontal scaling | 07 §4 (Cheat Sheet) |
| 25–35 unique ads ceiling | 07 §4 (Roast My Ads call; Part 2) |
| Fatigue 3-condition trigger | 07 §5 (Cheat Sheet) |
| Statics fatigue faster | 06 Statics Playbook; 07 §5 |
| 80/20 next-batch mix | 06 Statics Playbook §Strategy split (07 §6) |
| Cheap angle pre-test ($100 / 5 statics) | 06; 07 §6 |
| Comment-mining objection research | 02 Research Flow; 04 Part 3 |
| TAM exhaustion symptom | 03 Angles/Hooks/Copy |
| 30-day LTV:CAC ≥ 3:1 scale gate | 07 §0 |
