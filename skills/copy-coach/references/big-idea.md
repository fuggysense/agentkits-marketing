# Big Idea — find one, test it, expand it into the spine of a whole page

Load this reference when invoked for Big Idea help: finding one, testing one the user already has, or mapping the expansion across a page.

## PART 1 — What a Big Idea is

The single most important concept in copywriting. Everything else is execution. If the idea isn't there, no prose saves the page. If the idea is there, even clumsy writing can convert.

**Ogilvy:** *"A big idea is an idea that is instantly comprehended as important, exciting, and beneficial. It also leads to an inevitable conclusion, a conclusion that makes it easy to sell your product."*

**Stefan Georgi** adds shareability — a great Big Idea is almost a meme. The hearer grasps it instantly, and when they pass it to someone else, that person grasps it too.

The Georgi distinction: a **USP** is about the product (*"I've done 300 transactions in District 10"*). A **Big Idea** is about the promise of the copy itself (*"The reason your agent keeps pushing new launches is the commission is 3x higher than resale"*). Only the second makes the prospect stop scrolling.

**The structural form is cause and effect.** Neil Gordon's observation: the most-quoted lines across 2,500 years share one form.

> *"All of warfare is based on deception."* — Sun Tzu
> *"Philosophy begins in wonder."* — Socrates

## PART 2 — Four tests every candidate runs

Run every Big Idea candidate against all four. All four pass — or it's not a Big Idea yet.

1. **Cause and effect.** Can you phrase it as *"When X, Y follows,"* *"It's not X, it's Y,"* or *"Most do A, but the real move is B"*? If you can't get it into one of these forms, it's a theme, not an idea.
2. **Instant comprehension.** Could a busy person reading on their phone get it on one read? No footnotes, no *"let me explain."* If you have to set it up, the setup is the idea — and you haven't found it yet.
3. **Inevitable conclusion.** If the listener accepts the claim as true, does the offer become the obvious next step? If they can accept the claim and still walk away undecided, the idea isn't doing the work the offer needs.
4. **The chills test.** Would the target reader, scrolling at midnight, physically react? Pause? Raise an eyebrow? Lean in? If not, it's not big enough yet. Test 4 is the most expensive to fix — if it fails, you usually need a new candidate, not a polish.

## PART 3 — Hunting Big Ideas

When the contrast exercise doesn't crack it, go where Halbert went — real source material the user has access to:

- Real client video transcripts or testimonials (V4: `clients/<slug>/_brand/voice-of-customer/` or `research/`)
- Customer support tickets (the actual language people use about their pain)
- Subreddit threads where the audience complains
- Sales call recordings
- The founder's offhand explanations to friends
- Articles in trade publications

**Stand for something.** Ogilvy: when you clearly stand for something, you never stand alone. The strongest Big Ideas come from copywriters who let the brand stake a position and lose the customers who don't fit. A Big Idea palatable to everyone is a theme, not an idea.

**Vertical specificity beats general scope.** Bencivenga: don't sell "a stock market newsletter" — sell "three oil service stocks that may soar in the next 12 months." When a candidate feels weak, the fix is often *get more specific*, not broader.

## PART 4 — Expanding the Big Idea into a whole page

A Big Idea that lives only in the hero is decoration. A Big Idea that becomes the spine appears 5–7 times across the page, each time in a different costume. The same idea, restated through different sections, different proof types, different rhetorical moves. Throssell's three pillars:

### Pillar 1 — The chorus

The Big Idea is the chorus of the page. Every section restates it in a section-appropriate costume.

Example:
- *Hero — Big Idea stated as the named authority's professional rule.*
- *Loop section — Big Idea shown as the trap couples are in when they don't follow it.*
- *Method section — Big Idea named as our operating process.*
- *Proof section — Big Idea illustrated through a named client's outcome.*
- *P.S. — Big Idea future-paced as the two-paths choice.*

If a section can't be described this way, it doesn't belong on the page. Cut it or reframe it.

The failure mode is **stacking** — repeating the chorus four times in one section. Spread, don't stack.

### Pillar 2 — The belief chain

The reader starts with current beliefs and needs to reach the buy belief. Every section moves them one notch closer. No section loops back to ground already covered. No section advances if the previous one hasn't earned its claim.

Map it: write where the reader is at the start of each section and where they should be at the end. If two adjacent sections leave the reader in the same place, one is wasted.

**Context kills templates.** There is no universal sales page structure. A cold low-ticket Facebook ad needs a different shape than a warm $2,000 seminar email. The belief-chain *framework* is universal; the specific chain is bespoke.

### Pillar 3 — Proof architecture for every chorus restate

Each chorus appearance needs proof attached. If a restate has no proof, it's hype. Add proof or cut the restate.

Six proof types live at `.claude/references/copywriting-os/frameworks/six-proof-types.md` — load that file when designing proof architecture for a chorus.

### The monkey's fist (Bencivenga)

Sailors throw a small iron ball — the monkey's fist — before hauling the massive hawser rope. Before you can sell anything, you must first sell the prospect on giving you their attention. The first ask must be irresistibly easy — a free sample, a piece of genuinely valuable information, a quiz, a small commitment. Copy that lunges at the sale is throwing the hawser. Copy that offers something genuinely valuable first throws the monkey's fist.

## PART 5 — Testing the expansion

Three checks after expansion. Run all three.

1. **Trace the chorus.** Find every appearance of the Big Idea on the page. Is it spread across 5–7 distinct sections, each in a different costume?
2. **Belief chain audit.** Note the reader's belief state at start and end of each section. Are there gaps? Does any section leave them in the same place as the previous one? If yes, cut or merge.
3. **Proof attachment.** For every chorus restate, name the proof type that earns it. Any restate without proof gets cut or has proof added.

## Output — what to save to disk

When you finish Big Idea work, write `clients/<slug>/copy-system/big-idea.md` with:

- The Big Idea (in cause-and-effect form, one sentence)
- 4-test verdicts (cause-and-effect, instant comprehension, inevitable conclusion, chills) with named reasoning
- Expansion plan (5–7 sections, each with chorus-in-costume description + reader belief state in/out + proof type)
- The monkey's-fist first ask
- Source material drawn from (transcripts, tickets, calls, etc.) — for audit trail

Downstream `/copy` gates load this file. Don't skip the write — without it the drafter re-derives the spine on every run.
