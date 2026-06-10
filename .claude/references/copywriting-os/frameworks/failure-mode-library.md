---
name: AI Copy Failure Mode Library
source: cai #45 (worst-ai-sales-page-teardown.md, Peggy Burnett) + cai #26 (hidden-ai-patterns-emails-revenue.md, Peggy Burnett)
loaded_by: reviewers/teardown-reviewer.md, reviewers/forbidden-content-audit.md
purpose: A complete catalog of AI-copy failure modes a reviewer can check against, organized by location in the asset (hero / lead / body / proof / CTA) and by channel (sales letter, ad, email).
---

# AI Copy Failure Mode Library

## Why this library exists
LLM-generated copy fails in patterned, predictable ways. The same five or six structural tells show up across hundreds of sales pages and email sequences. This library catalogs every named failure mode from cai #45 (the sales-page teardown) and cai #26 (the email pattern analysis) so a reviewer can systematically check a draft against them — element by element, channel by channel — instead of relying on instinct alone.

## Section A — Sales letter failure modes (cai #45)

Peggy's teardown walks the page top to bottom: hero, problem section, benefits, testimonials, plus a root-cause synthesis at the end. Each failure below is named, illustrated with the verbatim bad example from the post, and paired with the prompt-level fix.

### Hero failures

**A1. The "Transform" opener — abstraction without specifics**
- What it looks like: Verbs that signal enormous change without naming any specific change. Words: *transform, empower, streamline, maximize*.
- Verbatim example: *"Transform Your Booking Experience With The Ultimate All-In-One Scheduling Solution"*
- Why it kills conversion: "The reader has no idea what will be different." Floats above the page in a cloud of abstraction.
- Fix: Ban the words. Force the headline to "name a specific person in a specific situation and hint at the outcome."

**A2. Category-speak instead of reader language**
- What it looks like: Phrases a product manager would write in a user story, not how the actual buyer thinks about her week.
- Verbatim example: *"Booking experience"* — "It's not how a massage therapist thinks about her Tuesday morning. She thinks about whether she'll get a text from a client saying they can't make it at 10."
- Why it kills conversion: The reader didn't come looking for the category. She came looking for the specific outcome.
- Fix: Use language a real buyer would use when talking about her own business. If it sounds like a product manager wrote it, rewrite.

**A3. Defensive umbrella claims — "ultimate" and "all-in-one"**
- What it looks like: Generic qualifiers used to preempt objections by promising everything.
- Verbatim example: *"Ultimate All-In-One Scheduling Solution"*
- Why it kills conversion: "Tells the reader nothing and signals that the product is probably mediocre at several things."
- Fix: Ban *ultimate, all-in-one, solution, platform*. Pick one specific thing the product does best.

**A4. Subhead built on Claude's three fallback verbs**
- What it looks like: Subheads that lean on *empower, streamline, maximize* with "cutting-edge technology" filler.
- Verbatim example: *"Empower your business with cutting-edge technology designed to streamline operations and maximize client satisfaction."*
- Why it kills conversion: "This entire sentence could be pasted onto a sales page for any B2B SaaS product made in the last fifteen years."
- Fix: Ban the three verbs and the phrase "cutting-edge technology." Force the subhead to reference a feeling or moment, not a category noun like "client satisfaction."

### Lead failures

**A5. Category-abstraction problem bullets**
- What it looks like: A "Problems You're Facing" section that names problem *shapes* without naming any actual problem.
- Verbatim example:
  - *Lost bookings due to inefficient scheduling*
  - *Time wasted on manual appointment management*
  - *Frustrated clients who can't book at their convenience*
  - *Missed revenue opportunities*
  - *Inability to scale your business*
- Why it kills conversion: Every bullet has the same structural pattern: *[negative state] + [generic cause]*. "Real problems don't all have the same shape. When every bullet in a list has the same grammar, it was written by an LLM pattern-matching on 'list of problems.'"
- Fix: Replace the list of problems with 3–4 specific moments from the reader's actual week — name the day, the time, what she's doing, what goes wrong. No parallel structure across moments.

**A6. Symmetry as a tell**
- What it looks like: Five bullets, all the same length, all the same grammar.
- Why it kills conversion: Uniformity is a structural fingerprint of "list of problems" prompts. Real lived problems are jagged.
- Fix: Force asymmetry. Different lengths, different sentence shapes, different opening words.

### Body failures

**A7. Parallel-structure benefit blocks**
- What it looks like: Eight benefits, all in the shape *Bold benefit headline — one-sentence explanation*, all using the words *intelligent, advanced, premium, effortlessly, seamlessly*.
- Verbatim example:
  - *Save Hours Every Week — Our intelligent scheduling system automatically handles appointment booking so you can focus on what matters most: your clients.*
  - *Boost Your Revenue — With advanced features that optimize your calendar, you'll maximize every available slot and grow your business effortlessly.*
  - *Enhance Client Satisfaction — Deliver a premium booking experience that keeps clients coming back and referring their friends.*
- Why it kills conversion: "Soothing to write and exhausting to read. The reader's eyes start skipping after the third one."
- Fix: "Do not write in parallel structure. Each benefit should have a different sentence shape, a different length, and a different rhythm."

**A8. Category-level promises ("Save hours every week")**
- What it looks like: Benefits stated at category level, true of every automation tool ever sold.
- Verbatim example: *"Save Hours Every Week"*
- Why it kills conversion: Communicates no specific value. "'Save hours' is what the product claims to do. 'Stop scrambling every Sunday night to figure out if Monday is actually going to work' is what the reader experiences. One of those sells. The other decorates the page."
- Fix: Each benefit must describe a specific change in the reader's actual life, not a capability the product has.

**A9. "You" as a rhythm stabilizer**
- What it looks like: The word *you* in the same syntactic position across every bullet — "so you can focus," "you'll maximize," "that keeps clients coming back."
- Why it kills conversion: "A common LLM tell. Claude reaches for 'you' as a rhythm stabilizer when it runs out of specifics."
- Fix: Vary openings. Don't start more than one benefit with a verb. Don't put *you* in the same position twice in a row.

**A10. Capability promises instead of life-change promises**
- What it looks like: Every benefit is "a promise the product makes, not a change in the reader's life."
- Why it kills conversion: Decorates the page; doesn't sell.
- Fix: Reframe every benefit as a specific moment in the reader's life that gets better.

### Proof failures

**A11. Superlative-then-stat testimonial pattern**
- What it looks like: Three testimonials all opening with a superlative, then an interchangeable stat, then a generic endorsement.
- Verbatim examples:
  - *"This is the best scheduling tool I've ever used. It saved me 10 hours a week and my clients love it." — Sarah M., Personal Trainer*
  - *"I can't imagine running my business without it. The automated reminders alone have cut my no-shows by 30%." — Michael R., Massage Therapist*
  - *"Absolutely life-changing for my practice. Everything just works." — Jennifer L., Yoga Instructor*
- Why it kills conversion: "Real testimonials usually have one specific detail the writer didn't plan for — a brand name, a family member, a moment of frustration that resolved. These have none of that."
- Fix: Never ask an LLM to write testimonials. The only legitimate use is editing real customer quotes down — that's editing, not generation.

**A12. Round-number stats**
- What it looks like: *"10 hours a week"*, *"30% fewer no-shows"* — even, round numbers.
- Why it kills conversion: "The kind of round, even numbers LLMs produce when asked for believable statistics. Real testimonials have odd numbers. 'It saved me about six hours most weeks, maybe seven on a good week.'"
- Fix: If the number is even and tidy, it's suspect. Real numbers are *six-ish, maybe seven; about three a week down to about one*.

**A13. Generic endorsements ("life-changing", "everything just works")**
- What it looks like: Closing lines that could attach to any product.
- Why it kills conversion: No specificity = no proof.
- Fix: Pull verbatim from real customer interviews. If you don't have them, don't publish testimonials.

### CTA failures
The post does not contain a dedicated CTA teardown section. The implicit CTA failure pattern, derived from the rest of the teardown, is:

**A14. Category-noun CTA verbs**
- What it looks like: CTAs that reuse the abstract verbs from the hero (*Transform*, *Empower*) or generic action ("Get Started", "Learn More") with no specific outcome attached.
- Why it kills conversion: Same root cause as the hero failure — no specific moment, no specific promise, the reader can't picture what happens after the click.
- Fix: The CTA should reference the same specific moment the hero promised to fix. If the hero named a Sunday-night problem, the CTA should reference Sunday.

### Section A root cause (verbatim from cai #45)
> "The writer gave Claude the product and asked it to sell the product. Claude sold the product — in the smoothest, most category-standard way it knew how. Every section was symmetrical, every sentence was inoffensive, every word was the word the training data expected. The missing ingredient was the reader."

> "The problem isn't Claude. The problem is that Claude lets you skip the thinking that used to happen before you wrote."

## Section B — Email failure modes (cai #26)

cai #26 is structured as four working email patterns (Random Observation, Blind Tease, Anniversary Hook, Authentic Rant) plus the calibration rules each one requires. The failure modes below are extracted from those rules: each one is what happens when an LLM generates the pattern *without* the calibration. Verbatim phrasing from the post is preserved where it names the failure.

### Subject line failures

**B1. Subject lines that signal "promotional"**
- What it looks like: Direct-pitch subject lines that violate the patterns' core principle: these emails work *because* "they don't follow conventional copywriting wisdom" and feel "casual, too indirect, too... human."
- Why it kills conversion: Triggers the resistance the four patterns are specifically designed to bypass.
- Fix: Subject lines for observation/rant/anniversary/tease emails should mirror the email's pattern — curiosity, temporal landmark, contrarian declaration, or incomplete loop. Never lead with the offer.

### Preview text failures

**B2. Preview text that completes the loop**
- What it looks like: Preview text that gives away the resolution the email body is designed to withhold (especially fatal for blind teases).
- Why it kills conversion: Kills the Zeigarnik effect the email is engineered around.
- Fix: Preview text should extend the curiosity gap, not close it.

### Opening line traps

**B3. Skipping the pattern interrupt**
- What it looks like: Opening with "Hi [name], today I want to tell you about…" — the expected email cadence the Random Observation pattern is designed to break.
- Verbatim principle: Random observations require a "Pattern Interrupt: Breaks expected email cadence."
- Fix: Open with a customer interaction, a specific off-topic detail, or a present-tense moment of genuine surprise.

**B4. Missing the "permission & setup" line on a rant**
- What it looks like: Rant emails that launch straight into the contrarian declaration without the *"I'm about to go on a rant…"* setup that primes the reader.
- Verbatim principle: "Acknowledge intensity. Create anticipation. Skip pleasantries."
- Fix: Always include the one-paragraph permission-to-rant opener before the declaration.

**B5. Anniversary opener without a specific date or sensory detail**
- What it looks like: "It's been a while since…" with no actual date, no generational marker, no sensory hook.
- Verbatim principle: "'Did you know…' or 'Can you believe…' Specific date/time reference. Express genuine surprise at time passage. Include generational marker."
- Fix: Research the actual date. Anchor the opening to it.

### Body / mid-email failures

**B6. The blind tease that feels manipulative (under-reveal)**
- What it looks like: A tease that withholds more than 30–40% of the value.
- Verbatim rule: "Blind teases that reveal less than 60% feel manipulative. More than 70% removes incentive to act."
- Why it kills: Reader senses bait-and-switch and disengages.
- Fix: Reveal 60–70% of the method. Withhold only the crucial implementation detail.

**B7. The blind tease that over-reveals**
- What it looks like: The email essentially gives the answer; no reason to click through to the webinar/course/call.
- Verbatim rule (same as B6): "More than 70% removes incentive to act."
- Fix: Audit the email — would a reader still want the next step? If no, pull a key implementation detail back into the next-step asset.

**B8. Random observation with no surprise element**
- What it looks like: A "story" that builds curiosity but never delivers the unexpected connection.
- Verbatim principle: The pattern requires a "Surprise Element: Reveal the unexpected connection. Make it feel discovered, not planned."
- Fix: If you can't name the specific surprise that made you "think twice," the email isn't ready. Don't ship a random observation that has no observation.

**B9. Rant without logical thread**
- What it looks like: Pure venting — no logical deconstruction of the common belief, no irrefutable build.
- Verbatim rule: "Maintain logical thread throughout. Never rant without purpose."
- Fix: A rant must walk through *why* the common belief is wrong, with analogies and "Think about it…" moments. Emotion alone reads as unhinged.

**B10. Anniversary email that romanticizes without delivering present value**
- What it looks like: Pure nostalgia, no bridge to the product, no time-bound offer.
- Verbatim rule: "Balance past romanticism with present value."
- Fix: Anniversary content must include the cultural bridge (past → present) and a time-bound, anniversary-specific reason to act now.

**B11. Missing authenticity markers**
- What it looks like: Body copy that reads as smooth, edited, formula-perfect prose. None of the small human signals.
- Verbatim required markers: "Include 1–2 parenthetical asides. Use conversational transitions ('anyway,' 'so,' 'but here's the thing'). Reference specific names, places, or brands. Include one self-interruption."
- Fix: Every observation/rant email must include at least three of those four markers. If a draft has none, it reads as AI-generated.

**B12. Calibration drift — missing structural element**
- What it looks like: A pattern email that drops one of the calibration steps (e.g. a tease with no value stack; a rant with no rallying cry).
- Verbatim warning: "They only work when the psychology is precisely calibrated… Miss one element, and performance drops by up to 71%."
- Fix: Walk every pattern email against its checklist before sending. Missing structure = missing revenue.

## Section C — Cross-cutting AI tells (both sources)

Patterns that show up across both newsletters, regardless of asset type:

**C1. Parallel structure as a fingerprint**
- cai #45 names this on every body section: "every bullet has the same structural pattern… that uniformity is a tell."
- cai #26 designs every pattern around *breaking* expected cadence — "Pattern Interrupt: Breaks expected email cadence."
- Reviewer rule: If five consecutive elements (bullets, benefits, opening lines) share the same grammar or rhythm, flag it.

**C2. Saturated AI vocabulary (banned word list)**
Drawn directly from cai #45's two prompt-level bans:
- *transform, empower, streamline, maximize, ultimate, all-in-one, solution, platform, cutting-edge, seamless, effortless* (hero ban)
- *seamlessly, effortlessly, intelligent, advanced, premium, streamline, empower, maximize* (benefits ban)
- Reviewer rule: Any of these words in a draft is an automatic flag.

**C3. Category-level abstraction over reader specifics**
- cai #45: "category abstraction… names a problem shape without naming any actual problem."
- cai #26: every pattern requires "specific, unusual details," "actual quotes or messages," "specific names, places, or brands."
- Reviewer rule: Strip every claim and ask, "could this attach to any product in this category?" If yes, it's abstraction.

**C4. Capability framing instead of life-change framing**
- cai #45: "Every benefit is stated as a promise the product makes, not as a change in the reader's life."
- cai #26: every pattern bridges to a *specific change in the reader's situation*, never to a feature.
- Reviewer rule: Rewrite any sentence that describes what the product does into a sentence about what the reader stops or starts doing.

**C5. Round, tidy numbers**
- cai #45: "Real testimonials have odd numbers."
- cai #26 implies the same when it demands "specific, memorable details" over "abstractions."
- Reviewer rule: 10 hours, 30%, 50%, 100% — all suspect. Real numbers are messy.

**C6. Formula leakage**
- cai #45: "The same verbs in the same positions… eight benefit statements all in the same shape."
- cai #26: warns that pattern emails must include authenticity markers (parentheticals, self-interruptions, conversational transitions) precisely because the underlying frame is structural.
- Reviewer rule: If the structural skeleton (*verb — explanation*, *Bold — sentence*, *problem — fix*) is visible to the reader, the formula has leaked. Break it.

**C7. Skipping the reader description**
- cai #45's root-cause fix: "Before you write this section, describe the reader to me… A specific person (name, situation, one sentence on their business). What their Sunday night looks like when things are going badly…"
- cai #26 builds the same requirement into every prompt: customer type, unusual use case, surprising element must be filled before writing.
- Reviewer rule: If the draft can't be traced back to a specific named reader and a specific moment, it was generated without the reader.

## Reviewer checklist (one-page summary)

Hero
- Banned hero words present? (transform, empower, streamline, maximize, ultimate, all-in-one, solution, platform, cutting-edge, seamless, effortless) → A1, A3, A4
- Category-speak instead of reader language? → A2
- Headline could attach to any product in this category? → A2, C3

Lead / problem section
- Bullets share the same grammar? → A5, A6, C1
- Names a *moment* in the reader's week, or a category abstraction? → A5, C3, C7

Body / benefits
- Parallel structure across benefits? → A7, C1
- Banned benefit words present? (seamlessly, effortlessly, intelligent, advanced, premium, streamline, empower, maximize) → C2
- "Save hours" / "boost revenue" capability framing instead of life-change? → A8, A10, C4
- *You* in the same position across multiple sentences? → A9
- Every benefit starts with a verb? → A9

Proof / testimonials
- Superlative → stat → generic endorsement pattern? → A11
- Round numbers? (10, 30%, 50%) → A12, C5
- Generic closers ("life-changing", "everything just works")? → A13
- Verifiable origin (real customer interview)? → A11

CTA
- CTA verb references the same specific moment as the hero, or a generic action? → A14

Email subject + preview
- Subject signals "promotional" instead of mirroring the email's pattern? → B1
- Preview text completes the loop the email is designed to withhold? → B2

Email opening
- Pattern interrupt present (random observation)? → B3
- Permission-to-rant line present (rant)? → B4
- Specific date + generational marker (anniversary)? → B5

Email body
- Blind tease reveal between 60–70%? → B6, B7
- Random observation has an actual surprise element? → B8
- Rant has logical deconstruction, not pure venting? → B9
- Anniversary balances nostalgia with present-value offer? → B10
- Authenticity markers present (parentheticals, self-interruptions, conversational transitions, specific names)? → B11
- Every structural element of the pattern present? → B12

Cross-cutting
- Parallel structure across 5+ elements? → C1
- Banned vocabulary anywhere in draft? → C2
- Could the claim attach to any product in the category? → C3
- Capability framing instead of life-change? → C4
- Round numbers? → C5
- Structural skeleton visible to the reader? → C6
- Can the draft be traced to a specific named reader and a specific moment? → C7

## Exact phrases to flag (verbatim ban list)

From cai #45, hero ban (verbatim):
- transform
- empower
- streamline
- maximize
- ultimate
- all-in-one
- solution
- platform
- cutting-edge
- seamless
- effortless

From cai #45, benefits ban (verbatim):
- seamlessly
- effortlessly
- intelligent
- advanced
- premium
- streamline
- empower
- maximize

Phrases flagged in the cai #45 teardown as category-speak / AI tells:
- "Booking experience"
- "Ultimate All-In-One"
- "Cutting-edge technology"
- "Client satisfaction" (used as a category noun)
- "Save hours every week"
- "Boost your revenue"
- "Enhance client satisfaction"
- "What matters most: your clients"
- "Grow your business effortlessly"
- "Everything just works"
- "Absolutely life-changing"
- "I can't imagine running my business without it"
- "This is the best [X] I've ever used"

Round-number stats flagged as suspect:
- "10 hours a week"
- "30% fewer no-shows"
- Any clean multiple of 5 or 10 used as a testimonial figure

Email-channel structural omissions flagged in cai #26:
- Tease that reveals <60% (manipulative) or >70% (no incentive to act)
- Rant without logical thread / "rant without purpose"
- Random observation with no surprise element
- Anniversary email with no specific date or generational marker
- Pattern email missing any one of its calibration steps (drops performance up to 71%)
