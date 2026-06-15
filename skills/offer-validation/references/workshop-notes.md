# Workshop Notes — rationale, edge cases, Q&A

Source: George Ten Meta-ads validation workshop (live, May 2026). Supplements the checklists with the WHY and the edge cases.

## Why the system works at all

- Meta shows ads to the **warmest, highest-intent buyers in the first 48 hours** (people who effectively just searched "buy weight-loss product"). That's why copy is direct with no angles — the audience is already in-market.
- Consequence: a successful test will often produce ZERO sales when re-run later — the warm pool was exhausted. Testing setup ≠ scaling setup. Scaling needs angles, all placements, more countries.
- You can validate before the product exists; one case study's validation profit ($250+) paid a Fiverr creator to build the course — zero out of pocket.

## Why each constraint exists

- **No text on the ad image / don't show the offer:** image's only job is to force a read of the copy. Text on image lets people skip the copy → skipped funnel step → unreadable data.
- **Direct copy, price withheld while testing:** angles are for cold/scaling. The ad names the product plainly and opens a curiosity gap — (a) "Here's the product, here's what it does, [no price]…" or (b) "Do you have X problem? Here's the product…" — so the only way to learn the price and guarantee is to click Learn More onto the page. Listing price + guarantee on the ad lets people decide from the feed and skip the link click, which is the exact data point the test reads. When NOT testing (scaling a proven offer), the reverse is correct: full info up front shortens the path to purchase, because Meta already knows who to show it to and there are no data points left to analyze (George Ten voice note, 260613).
- **Feeds only:** most expensive, most attention-dense inventory; mixing placements averages CTRs into mush.
- **T1 countries (US/UK/CA/AU):** English + money + most expensive inventory = highest intent. After validation: T1+ (add IE, NZ, Western Europe, MX) → then worldwide broad.
- **Buy-word on the button:** psychological barrier filters curiosity clicks; ATC then means real intent, which is what makes "2 ATCs ≈ 1 sale" hold.
- **No flex ads, 1 text/headline/image per ad:** if Meta mixes combinations you can't isolate which element broke. Run 1 ad, or put 3–5 single-variable ads in one ad set and let Meta decide between them (George Ten voice note, 260613).

## Scaling protocol (post-validation)

1. Never kill a selling campaign — let it run until it dies. Create NEW campaigns alongside.
2. T1 winner → T1+ campaign → worldwide broad (all countries, ages, genders).
3. Angle testing structure: 1 campaign → ad sets named per angle → 3–5 ads per angle inside.
4. Angles live at the AD level, not the sales page. Page stays neutral (speaks to everyone); each ad speaks to one specific person-type and Meta routes it. Only build an angle-specific page once an angle proves crazy-good at high spend.
5. Scale with images first; add video when scaling further.

## Q&A edge cases

- **Physical/premium product >$100 (e.g. $157 leather bags):** $100 is a hard psychological barrier on Meta — anything at or above it is outside impulse-buy range, so impulse direct-response won't carry it. Go as cheap as the offer allows (ideally $17–27); if you can't, stay under $100 charm-priced (97/99), the way retail stacks items just below the line (George Ten voice note, 260613). For genuinely premium goods: bait product <$99 + upsell at checkout/post-purchase (advertise the iPhone case, land on a collection/bundle with the bag), or content-based campaign + retargeting.
- **Service with "nothing to sell" (e.g. auto broker):** productize a slice — paid PDF/guide on the buyer's pain ("17 tips to get a cheaper car in LA"), congruently bridge to the service. Test a PAID item, not a free lead magnet — free downloads don't validate purchase intent.
- **Ultra-niche offers (e.g. "open a Muay Thai gym"):** audience too small for Meta broad; use Google search intent instead.
- **High-ticket call funnels (book a call as the conversion):** a call is a multi-thousand-dollar psychological commitment; this low-ticket validation method doesn't map.
- **Cash-on-delivery markets:** exclude regions where buyers lack cards; target top cities.
- **Custom-input products (personalized books etc.):** take payment FIRST, collect inputs after — paid customers will fill any questionnaire.
- **Waitlist / fake sold-out instead of charging:** never. Checkout reach ≠ validation; only completed payment validates. If squeamish, charge then instantly refund with an apology email.
- **Selling before the product exists:** charge as-is; email buyers "didn't expect sales so fast — refund or wait for delivery in X weeks." ~80% don't open the email, ~19% wait, ~1% refund.
- **Stopping early to save money:** allowed only when CTR All is very low AND zero ATCs/sales after 24h. Otherwise run the full 48h / ~33 link clicks.
- **SaaS free-trial-style front-ends:** avoid time-gap funnels (use product → maybe subscribe later). Sell the low-ticket, then immediately convert: "you already paid for month 1 — first month free" on the thank-you page.
