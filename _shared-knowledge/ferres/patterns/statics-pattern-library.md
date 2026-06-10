# Statics Pattern Library — Sean Ferres "AI Ads Lab"

What this is: 49 winning static creatives clustered into named, reusable patterns — each with anatomy + an image-prompt-ready recipe — to ground the image-prompt stage of the pipeline.
Primary lectures: BONUS #1 The Winning Statics Playbook (lecture 24, transcript + `text/24_..._Winning_Statics_Playbook_v4.txt`) and BONUS #3 The Winning Ads Swipe Vault (`text/swipe_vault/STATICS_01–49.md`, `text/25_..._STATICS.csv`).
Last distilled: 2026-06-10.

---

## How to use this file

The library has two layers. Read the **operating axis** first (it decides which pattern to even reach for), then pick a pattern.

Every pattern below maps to one of Ferres' five canonical "lanes" so the image-prompt generator can tag output: **PRODUCT-SHOT · SOCIAL-PROOF · INFOGRAPHIC · NATIVE · TABLOID** (24_bonus-1 [00:05:07]). The swipe vault breaks those five into finer visual sub-types — that finer split is what this file names, because the image generator needs the specific layout, not the lane label.

---

## The operating axis: Direct ⟷ Indirect (read before picking a pattern)

This is the single decision that drives format choice. It is not optional.

- **The whole market is a temperature gradient** — unaware → problem-aware → solution-aware → product-aware → most-aware (`text/24_..._Playbook.txt`). The warmer/more-aware the audience, the more **direct** the static. The colder/more-unaware, the more **indirect** and disguised it must be to earn curiosity (24_bonus-1 [00:02:39]).
- **Direct statics speak to the ~3% ready to buy now.** Product shot + headline + maybe price, "here's the offer, buy it," linked straight to the product page or checkout. Highest ROAS, but you exhaust that 3% fast and the format does not scale huge (24_bonus-1 [00:02:52], [00:15:54]).
- **Indirect statics speak to the other 97% of your TAM.** They do not look like ads — they look like content, a news post, a friend's status. They earn the click on pure curiosity, then long-form copy / an advertorial does the selling. These scale on cold traffic and make the most money long-term. Rule of thumb: the less it looks like an ad, the better it performs (24_bonus-1 [00:03:41], [00:03:54]).
- **Indirect splits two ways:** (1) **BLEND IN** — camouflage as native feed content (candid photo, Notes-app screenshot, meme, confession). (2) **STAND OUT** — interrupt the scroll with something the brain has to stop and process (tabloid headline, weird circled image, ugly graphic) (24_bonus-1 [00:04:08], [00:04:26]; `text/24_..._Playbook.txt`).
- **Click routing is part of the format.** Direct → product page / checkout. Indirect → advertorial article that educates and warms, which then links to the product. Never point an indirect static straight at a product page (24_bonus-1 [00:15:58], [00:16:04]; `text/24_..._Playbook.txt`).

**Two universal facts to bake into every brief:**
- **Statics fatigue faster than video.** A static gives away its whole message in one glance, so once someone's seen it there is nothing left to pull them back. Keep feeding the account fresh statics and keep frequency under 3 (24_bonus-1 [00:01:59], [00:02:16]; `text/24_..._Playbook.txt`).
- **Long run-time = the "this works" stamp.** An ad live for months/years is almost certainly profitable. Liquid Death's comment-style ran 2,037 days, King Kong's native 1,184, Skull Bliss's listicle 911, Zapier's infographic 634, 4Patriots' product shot 619 (`text/25_..._STATICS.csv`). Model the long-runners first.

**The tabloid "stop-the-scroll" test** (apply to any STAND-OUT pattern): (1) pattern interrupt in the image — something weird that physically stops the thumb, often a secondary image in a circle with an arrow; (2) burning intrigue in the headline — an open loop the brain must close; (3) a targeted big benefit so the algorithm knows who to find. Pure intrigue with no benefit pulls everyone and qualifies no one; pure benefit with no intrigue gets ignored. You want the intersection (`text/24_..._Playbook.txt`; 24_bonus-1 [00:10:04], [00:10:12]).

---

## Pattern 01 — Product-Shot + Big Promise  · lane: PRODUCT-SHOT (DIRECT)
**Members:** STATICS_01 RYZE (F&B, 458d), STATICS_02 4Patriots (survival, 619d), STATICS_03 Curlified (haircare, 419d), STATICS_04 Bumzzy (men's grooming).
**What it is:** The product is the hero and fills the frame; the single biggest text element is an outcome-level promise — a number, a guarantee, or a discount — not the product name. Looks like a polished ad and links straight to the product page. Your warm-audience and retargeting workhorse (`text/24_..._Playbook.txt`; 24_bonus-1 [00:05:12]).
**When it works:** Product-aware / most-aware buyers; bottom-funnel and retargeting. Use when you have one defensible, quantifiable claim (8-hour sleep, 25-year shelf life, 40% off).
**Anatomy (top→bottom):** brand wordmark (top-center, small, all-caps) · hero product at ≥60% of frame · headline = the big promise (largest, heaviest, all-caps) · 3–5 lines of mechanism/benefit body OR feature bullets with check icons · optional CTA pill restating the offer. Single high-contrast background hue (red=urgency, blue=trust/science, green=natural).
**Replication recipe (prompt-ready):**
1. Pick the ONE measurable outcome — a number or a categorical guarantee. That becomes the headline.
2. Shoot/strip a clean PNG of the real product; place it as hero at ≥60% frame, slight 3/4 or overhead angle. (Background-strip the product first — Adobe Express remover — then drop into the scene, `text/24_..._Playbook.txt`.)
3. One saturated background hue whose emotion matches the promise. Never white (reads as unpaid organic).
4. Layer copy directly on the product/background, white text, no boxes. Body = [mechanism]+[quality signal]→[primary outcome]→[secondary outcome]→[objection killed], under 60 words.
5. Optional: one seasonal prop bled from a corner, sharing the background's color temperature — never centered.
6. Test by swapping the PROMISE, not the photo (servings vs shelf-life vs % off vs guarantee length).

## Pattern 02 — Hard Offer / Red-Hot-Deal  · lane: PRODUCT-SHOT (DIRECT)
**Members:** STATICS_25 RYZE (156d), STATICS_26 True Classic (403d), STATICS_27 Mobile Editing Club; deal-variant of STATICS_03 Curlified, STATICS_11 Adstra's "$27"; bundle play STATICS_12 Nobl.
**What it is:** The offer mechanic IS the creative — an oversized discount %, a "buy 1 get N free" stack, or a price so low it reads as a pattern interrupt. Pure transaction promise (save money now), complexity deferred to the page.
**When it works:** Most-aware / hot traffic, sales events, retargeting carts. Needs a real reason-why (season, launch, "biggest sale of the year") so urgency feels contextual not manufactured (STATICS_03, STATICS_12).
**Anatomy:** discount/offer figure at 30–40% of canvas height, high-contrast (red on light, white on dark) · soft qualifier above it ("UP TO", "FROM") to stay compliant without shrinking the number · one event label ("SUMMER SALE") smaller than the number · product(s) or order-summary screenshot below · brand wordmark small at top. The Nobl variant uses a raw order-summary screenshot where five "FREE" line items under one $699 anchor do the arithmetic for the reader.
**Recipe:** (1) Lead with the single offer figure at oversized scale. (2) Add a qualifier word + a seasonal/event reason. (3) Show 2–4 SKUs as a system, or a screenshot of the stacked free items with exact names/prices (specificity = legitimacy). (4) Strip everything else — no bullets, no testimonials. Landing page closes.

## Pattern 03 — Social-Proof Quote + Face  · lane: SOCIAL-PROOF (DIRECT)
**Members:** STATICS_19 True Classic (359d), STATICS_20 AG1 (26d).
**What it is:** A real-feeling customer face plus a quote in their own words. Sells through borrowed trust; runs in every niche because proof is universal (24_bonus-1 [00:05:39]).
**When it works:** All temperatures, but especially solution-/product-aware where the doubt is "does it actually work for someone like me." The quote demonstrates the benefit instead of claiming it.
**Anatomy:** real (un-model-like) person reacting to the product on a real body · their verbatim quote as the dominant overlay, in curly quotes, one word italicized for texture · small brand monogram in a corner · no CTA, no separate headline.
**Recipe:** (1) Pull a genuine customer line that sounds texted-to-a-friend, not copywritten ("My butt hasn't looked this good since I was 20"). (2) Keep one specific comparative anchor ("since I was 20") — specificity signals it's real. (3) Photograph a joyful, candid reaction; emotion is contagious and lands before the words. (4) Brand stays subordinate.

## Pattern 04 — Verified Review / Comment Card  · lane: SOCIAL-PROOF (INDIRECT-blend)
**Members:** STATICS_31 True Classic review card (403d), STATICS_32 Liquid Death FB-comment (2,037d), STATICS_13 Magic Spoon "You Asked / We Listened" comment, STATICS_28 third-party ("Dermatologists Trust" + 23,000 reviews, Vegamour 31d), STATICS_29 Ballboyz authority.
**What it is:** A real-or-realistic piece of UGC — a star-rated review widget, a Facebook comment, a "verified buyer" card — embedded so it reads as found content, not paid creative. Two sub-flavors: (a) peer review/comment, (b) third-party authority ("the serum dermatologists trust," 300k customers).
**When it works:** Cold-to-warm; drops ad-skepticism in the half-second the brain misreads it as a screenshot. Authority sub-flavor closes efficacy doubt; peer-volume sub-flavor closes risk aversion — stack both when you can (STATICS_28).
**Anatomy:** pixel-matched review/comment UI (avatar, name, "Verified Buyer ✅", timestamp, star row) · body text with the two highest-value claims auto-bolded mid-sentence · specific named pain points ("collar won't curl," "didn't shrink in the wash") not generic praise · for authority flavor: categorical claim ("Dermatologists Trust") + a big round review count.
**Recipe:** (1) Replicate the platform's real review/comment chrome exactly — mismatched UI breaks the illusion. (2) Write the quote with named, verifiable specifics, deliberately casual/lowercased if it's a comment. (3) Bold the sensory claim + the value claim. (4) For authority: keep the endorser categorical (a profession, not a named person) to avoid inviting scrutiny.

## Pattern 05 — Educational / Annotated Infographic  · lane: INFOGRAPHIC (INDIRECT)
**Members:** STATICS_22 Groundingwell annotated diagram (612d), STATICS_24 Zapier workflow UI (634d), STATICS_23 AppsFlyer stat report (192d), STATICS_38/39 us-vs-them comparison (see Pattern 06).
**What it is:** Teaches or proves something inside the image — a labeled how-it-works, a stat, a clean comparison. Earns the click by handing over value upfront, building authority and pre-selling the mechanism (`text/24_..._Playbook.txt`; 24_bonus-1 [00:06:46]).
**When it works:** Problem-/solution-aware audiences who want to understand the mechanism. The visual IS the argument — no body copy needed (STATICS_22, STATICS_24).
**Anatomy:** one product-in-use photo OR a UI mock · 3 benefit labels on leader lines, each hitting a distinct node of the symptom/benefit cluster · a single problem-name headline ("Lymphedema?") or a demystifying tagline ("Automation isn't magic. It's Zapier.") · optional discount starburst at the eye-exit (bottom-right) · brand mark small.
**Recipe:** (1) Pick a real workflow/mechanism and show it, don't describe it (Zapier's three "On" toggles = a live system). (2) Anchor 3 benefit labels spatially to the product with leader lines so each claim feels demonstrated. (3) Headline = the condition/problem name as a question for ruthless self-selection, or a 2-beat "X isn't magic, it's [brand]" demystifier. (4) Keep it spare — clutter signals "trying to persuade"; restraint signals confidence.

## Pattern 06 — Us-vs-Them Comparison  · lane: INFOGRAPHIC (INDIRECT)
**Members:** STATICS_38 MS Meats jerky split (439d), STATICS_39 Intake Breathing vs nasal strips (72d).
**What it is:** A split frame — OUR side vs THEIR side — that triggers the comparison reflex before a word is read. Warm/artisan palette vs cold/industrial palette does half the selling.
**When it works:** Solution-/product-aware markets where a category alternative is the real competitor; positions your product against the whole mass-market category.
**Anatomy:** vertical split · matching headline pair ("OUR JERKY" / "THEIR JERKY") · a color-coded badge per side (amber=trustworthy, grey=inferior) · 3 parallel bullets per side using **negative specificity** on the "them" side ("Fat and Meat Trimmings," "Multinational") so the reader concludes "poor quality" themselves.
**Recipe:** (1) Build the two columns with identical structure. (2) Warm palette + irregular/premium product shape on your side; cool palette + thin/uniform on theirs. (3) Replace every "vs cheap alternatives" with a concrete attack (an ingredient reality, an ownership reality). (4) End each side with one verifiable provenance noun ("Made in Montana").

## Pattern 07 — Native Article-Thumbnail Advertorial  · lane: NATIVE (INDIRECT-blend, most indirect)
**Members:** STATICS_05 King Kong "Keeping Up With The Kash" (1,184d), STATICS_06 Klyra candid parking-lot photo (63d), STATICS_07 Stansberry editorial headline (48d).
**What it is:** The creative is indistinguishable from a real editorial article thumbnail. Zero ad-signals on the image — no logo, no product, no CTA, no brand color. All copy lives in Facebook's caption + link-bar fields, where a real article link would put it (24_bonus-1 [00:07:35], [00:07:50]).
**When it works:** Cold/unaware traffic. Pairs with a long advertorial ("57-year-old from Norway reveals…") that does the persuading; never links straight to product (`text/24_..._Playbook.txt`).
**Anatomy:** a photojournalistic image only — slight angle, available light, warm bokeh, serious authority face OR a candid "caught through a car window" moment that raises a question · NO text on image · link-bar styled as a media outlet (publication-style domain, editorial headline, "Learn More" — never "Buy") · brand appears only in the page avatar.
**Recipe:** (1) Invent a wealth/outcome-coded fake publication ("Keeping Up With The Kash") + matching media-style domain. (2) Source an editorial press portrait (Getty/Unsplash "executive portrait documentary") or shoot a deliberately imperfect candid that begs a question. (3) Put ALL persuasion in the link-bar headline: "[specific person] [achieved] [number] [in timeframe] using [oddly-named mechanism]." (4) Set the display URL to the publication domain, CTA to "Learn More" only. (5) QA: show it cold and ask "what is this?" — if they say "an article about X," it holds; if "an ad for X," a signal leaked.

## Pattern 08 — Breaking-News / Tabloid  · lane: TABLOID (INDIRECT-standout) — Ferres' favorite
**Members:** STATICS_08 Sabri Suby "58 Millionaires" (BULLSEYE example), STATICS_09 YouTube-To-Skool, STATICS_10 InvestorKit "REVEALED…1992" (222d), STATICS_37 Matt Leitz "Over 30?" webclass (34.4K likes).
**What it is:** The format every big Facebook page runs. A slightly odd primary image, usually a smaller circled/arrowed inset, a bold news-style headline bar with red accents. Two competing images stop the scroll because the brain tries to process both at once (`text/24_..._Playbook.txt`; 24_bonus-1 [00:08:37], [00:09:00]). Ferres: don't feel "above" it — you won't undo thousands of years of psychology; people crave news and drama (`text/24_..._Playbook.txt`).
**When it works:** Cold/unaware at scale; "rips harder than literally anything else" per Ferres (24_bonus-1 [00:14:06], [00:15:47]). Goes ham on a news angle to win clicks, then the advertorial qualifies (24_bonus-1 [00:11:17]).
**Anatomy:** pattern-interrupt primary photo · a secondary image in a red circle with a hand-drawn arrow pointing at it (the signature device, 24_bonus-1 [00:10:12]) · red "BREAKING NEWS" bar + a news-chyron lower-third subhead · specific number in the headline ("58 Millionaires" — counted, not rounded) · optional press-clipping collage (real-paper printouts) for borrowed authority · book/credential prop in scene.
**Recipe:** (1) Stage a weird-but-relevant primary image. (2) Add the red-circle + arrow inset highlighting one curious object. (3) White heavy condensed sans on a red/black bar: "BREAKING:" red tag + an open-loop headline carrying ONE hyper-specific number and a targeted benefit. (4) Mystique label the hero ("Mysterious 'Millionaire Maker' Breaks His Silence") — framed as press-given, in quotes. (5) Slightly punchy high-contrast tabloid grade; keep face + text inside the safe area. Inspiration source: Meta's Widely-Viewed Content Report + big IG shoutout pages (24_bonus-1 [00:13:46]).

## Pattern 09 — Native-Organic: Notes / Handwritten / UI-Mimic  · lane: NATIVE (INDIRECT-blend)
**Members:** STATICS_15 Happy Mammoth fake iOS "Reminder" (30d), STATICS_16 PeakForm sticky note "TSH: 2.8 — Normal Range?" (195d), STATICS_17 Skool cardboard sign, STATICS_18 Grant Cardone whiteboard checklist (153d); chat-UI cousins STATICS_33/34 Rocket Money fake X-thread + spreadsheet (51d).
**What it is:** The copy IS the ad. A handwritten sticky note, a marker checklist, a fake iOS notification, or a fake X reply thread — text on a human-feeling surface, no graphic design, no banner. Reads as something a person authored, not a marketing department (24_bonus-1 [00:04:17]; STATICS_15, STATICS_16).
**When it works:** Cold (blend-in) and warm retargeting (the whiteboard "Still Thinking About It?" mirrors a hesitating visitor). Jargon in the note ("TSH") self-selects the exact sufferer and repels everyone else.
**Anatomy:** an authentic surface (sticky note, medicine-cabinet shelf, iOS alert card, X thread) shot like a real photo/screenshot · short hand-lettered or system-font copy · for the data-mirror variant, a clinical value undercut by a "?" that names the "normal but not well" wound · for the chat variant, an engineered absurd line item ($3,200 red-light therapy) that forces a re-read, then a peer reply naming the product · product visible only as soft background context.
**Recipe:** (1) Choose the surface that matches the niche's native habitat. (2) Write copy as the customer's own note/thought, not a claim — mirror the wound or the question. (3) Plant one jargon term or one absurd detail to self-select and to create the pause. (4) Let the product sit in the background, never overlaid. (5) Pair with long emotional advertorial copy for the click.

## Pattern 10 — Before / After Transformation  · lane: SOCIAL-PROOF / INFOGRAPHIC (DIRECT-ish)
**Members:** STATICS_21 Vernal "Crêpe-less" Week 0 vs Week 4 (244d).
**What it is:** A split-screen timeline (Week 0 / Week 4) with the product, plus an outcome-story headline framing the result as a "discovery."
**When it works:** Problem-aware beauty/health/fitness where the before-state is a visible insecurity. A specific timeline (4 weeks) reads as a real protocol, not magic.
**Anatomy:** two photo panels with WEEK 0 / WEEK 4 labels · unflinching before-state for self-recognition · outcome-narrative headline ("She Wore Short Sleeves to Her Reunion Thanks to This Discovery") that names a specific high-stakes social moment · ingredient-transparent product label for clinical credibility · panel color matched to the product hue.
**Recipe:** (1) Label a believable timeline, not just before/after. (2) Show the real before-state honestly. (3) Headline = a specific emotional scenario + "discovery" framing; don't name the brand. ⚠️PLATFORM: literal weight-loss before/afters get ads rejected and can kill the whole ad account — **animate or imply the transformation** rather than showing graphic real-photo weight-loss before/afters (`text/24_..._Playbook.txt`).

## Pattern 11 — Pattern-Interrupt Oddballs (Wanted Poster · Ugly Pain · Surreal-AI · Meme · Apology · Listicle-cover · Spokesperson · UGC-selfie · Podcast-clip · Quiz · Countdown)
A tail of single-or-double-member STAND-OUT and direct formats. Each is a one-trick scroll-stop; reach for them as test variety, not as your spine. Common thread: a pattern interrupt + a curiosity gap or a targeted benefit.
- **Wanted Poster** — STATICS_11 Adstra AI. Aged-parchment western broadside; "[NICHE] FOUNDERS:" call-out + transformation headline + "OR IT'S FREE" performance bounty + shockingly low price in a starburst. Aesthetic = confidence signal.
- **Ugly Ad / pain close-up** — STATICS_42 FungalFix (233d). Raw, text-free disgust/pain photo (toenail fungus) that fires threat/disgust circuits; problem-first, product implied; all copy in the ad fields so it reads as UGC.
- **Unhinged / Surreal AI** — STATICS_43 Olipop candyland (22d), STATICS_44 Stefan AI-twin. Spectacle or incongruent prop the brain must stop to process; for AI-course offers the creative doubles as proof of concept.
- **Meme** — STATICS_14 Foreplay car-drift ("FB Ad Library vs Foreplay," car labeled "me"). Instant-decode template; lo-fi reads as peer-shared, not brand.
- **Apology / Open Letter** — STATICS_41 Blume "We're Sorry." Inverts a social script — apologizes for the product working too well; every "sorry" is a boast the reader concludes themselves.
- **Listicle Advertorial cover** — STATICS_40 Skull Bliss "5 REASONS WHY… THE ULTIMATE HOME DECOR" (911d). Curiosity-gap cover card; the list lives in body/page. Big superlative + aspirational room shot.
- **Spokesperson / Celebrity** — STATICS_45 Grant Cardone playbook (369d), STATICS_46 Tony Robbins×Bartlett BOGO. The face IS the guarantee; outcome named to the exact tier ("7-FIGURE COACHES").
- **UGC Selfie / Podcast clip** — STATICS_47 Jarem "Loom Before Zoom" (1-min selfie, hyper-specific promise), STATICS_48 "Meet My AI Twin" podcast-desk. Caption carries the hook; "…See more" truncation forces the micro-commitment.
- **Quiz-Funnel** — STATICS_49 Gundry MD. A personal question + tappable answer bubbles that look clickable; every answer funnels into a "you'd benefit" path. Self-qualifies without shame.
- **Countdown / Vanishing** — STATICS_35 Happy Mammoth "VANISHING!" (36d), STATICS_36 Pocket AI. One loss-aversion word + layered urgency (script "Last Call" + starburst "Only Hours Remaining"); ⚠️PLATFORM the swipe lists these as "animated countdown" — as a static, lean on the verbal scarcity word, not a fake live timer.

---

## The build stack & workflow (Ferres' pipeline — for the orchestrator)

- **Tools:** Claude for the thinking + the prompts; Higgsfield (Plus plan), Nano Banana Pro model, for generating the images. Use Higgsfield for images only — it's "a ripoff for videos" (`text/24_..._Playbook.txt`).
- **80/20 rule:** 80% of tests are re-skins of proven swipe winners (ride someone else's data); 20% are from-scratch concepts (`text/24_..._Playbook.txt`).
- **Path A — Swipe:** find long-runners in Foreplay (filter: image format, still live, 30+ days, English, FB+IG; sort by longest-running), then run the Swipe-Teardown-+-Rebuild prompt (3 passes: why it wins → how we rebuild → the image-gen prompt). Free fallbacks: GetHookd, Meta/TikTok Ad Library.
- **Path B — From scratch:** the 3-part concept engine — FORMAT (one of the five lanes) · THE HOOK (exact on-image words, concrete + specific) · THE PROMPT (copy-paste Nano Banana, 4:5 portrait, text inside center so a square crop survives, end `--ar 4:5`).
- **Generate:** Nano Banana Pro in Higgsfield, 4:5 canvas, 2K, 4 generations at a time; upload a background-stripped product PNG for product shots. If text glitches, regenerate or ask Claude/Gemini "fix the text to read exactly: …".
- **QA before launch:** text legible + correctly spelled; on-brand, product looks right; ⚠️PLATFORM no graphic weight-loss before/afters (account-kill risk).

(Pipeline stages reported in the JSON summary's `stage_map_fragments`.)
