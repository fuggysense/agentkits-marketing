# Swiped.co → Jerel's Three Niches: Taxonomy Map

**Built:** 2026-05-27 | **Stream:** Phase 0b stream B | **Source:** swiped.co (Mike Schauer's "Swipe Studies" archive)

---

## How swiped.co organizes itself

swiped.co tags every swipe by **Niche** (~90 categories) and **Type** (~80 format/element labels: Long Copy, Direct Mail, Advertorial, Sales Letter, Landing Page, Facebook Ad, etc.). Niches and Types overlap freely — a single swipe can carry 2-3 niches + 4-6 types.

## Mapping to Jerel's three priority buckets

| Jerel's bucket | swiped.co niches pulled from | Rationale |
|---|---|---|
| **Info products / coaching / courses** | Info Marketing (24), Self-Improvement (10), Education (11), Business Opportunity (25), Online Business (25), Entrepreneurship (5) | All sell knowledge, transformation, or a "make money / get results" outcome to a consumer end-buyer. Business Opportunity is a borderline case (often MLM-adjacent or get-rich-quick) — flagged where it shades into pure hype. |
| **Agency services** | Consulting (5), Services (4), Marketing (50 — filtered), Copywriting (5) | Done-for-you or done-with-you offers targeting business owners. Marketing niche is dominated by Frank Kern / Ryan Deiss / Dan Kennedy — many entries are info products *about* marketing, but the sales letters themselves promote agency-style offers (consulting, funnel build-outs, fixed fees). |
| **B2B services / SaaS** | SAAS (19), Software (5) | swiped.co under-represents B2B sales letters. SaaS marketing is dominated by **landing pages**, homepage tests, and free-trial funnels — not 5,000-word direct-response letters. To get 10 entries I had to relax the "must be a sales letter" filter and include landing pages + homepage breakdowns. |

## Categories I did NOT pull from (and why)

- **Financial (43), Fashion (20), Food (21), Politics (21), Automotive (20)** — high volume but not in Jerel's verticals. Patterns may transfer but signal-to-noise is low.
- **Health & Wellness (16), Fitness (5), Weight Loss (9)** — consumer health niche, transferable hooks but not directly Jerel's buyer.
- **Fundraising, Dating, Religion, Gambling, Survival** — outside priority verticals.

## Categories that don't fit cleanly

- **Business Opportunity vs Info Marketing** — heavily overlapping. Halbert's "Make Money With Your Credit Cards" is both. Mapped to **info-products** because the buyer-end is the same (an individual aspirational consumer, not a business buying agency services).
- **Marketing niche** — 50 entries but only ~10 are actual sales letters; the rest are FB ads, retargeting, checkout pages, pop-outs, opt-in forms. Filtered hard.
- **SaaS landing pages** — these are **NOT** comparable to the 8 STRONG long-form letters Jerel hand-picked. Treat patterns from this niche as **landing-page-conversion** patterns rather than sales-letter patterns. Flagged in each annotation.

---

## What is publicly visible on each swipe page (CRITICAL — affects schema)

I scraped one swipe before committing the corpus. Findings:

- **The full sales letter body is NOT text-scrapable.** Original letters are served as images, PDF scans, or screenshots embedded in the swipe page.
- **"Download As PDF" is gated** — appears to require login (paywall flag for full reproductions, but commentary itself is free).
- **What IS public on every swipe page:**
  - Headline (quoted in the body of the commentary)
  - Source URL + era / date swiped
  - **Mike Schauer's analyst commentary** — typically 200-1,500 words explaining what makes the swipe work, who the buyer is, the offer mechanic, and any notable techniques
  - "Key Takeaways" section on some entries (additional analyst breakdown)
  - Tags (Long Copy, Direct Mail, Tested, Control, Exclusivity, Call to Action, etc.)

## What this means for the schema

Every annotation in this corpus is built from:
1. **The headline** (verbatim from commentary)
2. **Tags** swiped.co attached (these populate the Components Present checklist with high confidence)
3. **Schauer's analysis** (the source of truth for hook type, lead type, mechanism, standout pattern)
4. **Era/date** (every entry has one)

Fields where data is **NOT available** are explicitly marked `[NOT VISIBLE — image-only original]` rather than guessed. The most common missing fields:
- Exact opening two sentences (after the headline)
- Word count (image originals = no count)
- Exact P.S. text
- Full guarantee wording

## Paywall behavior

Free content used in this corpus:
- All page bodies (commentary, headlines, tags, source URLs)
- Embedded image thumbnails

Gated content I did NOT attempt to bypass:
- "Download As PDF" full reproductions
- "Become a Member" deep-dive videos (only one swipe, the Deiss/Kern consulting letter, has a free video breakdown — referenced in annotation)

Login was never required to read a swipe study. Zero paywall hits encountered for the in-corpus URLs.

---

## Final volume per bucket

| Bucket | Letters | Reasoning |
|---|---|---|
| info-products | 20 | High supply on swiped. Mix of modern (Kern, Kennedy, Brunson, Pagan, Deiss, Roeder) + classic (Halbert, Schwartz, Ogilvy). |
| agency | 10 | Limited supply. Consulting category only has 5 entries; expanded with Marketing-niche entries that are clearly agency-offer sales letters (Jay Abraham, Yodle, Conversion Rate Experts, Scott Haines copywriting). |
| b2b-services | 10 | Swiped under-represents B2B. Relaxed criteria to include landing pages, homepage tests, and free-trial conversion strategies. Flagged in each annotation that these are NOT comparable to long-form sales letters. |

Total: 40 letters (Jerel's lower bound was 15, upper was 60 — 40 hits the sweet spot where signal is dense and the analyst commentary alone provides defensible annotations).
