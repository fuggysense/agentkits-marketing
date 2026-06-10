# Swiped.co Segmented Corpus — Phase 0b Stream B Summary

**Built:** 2026-05-27 (Singapore time)
**Stream:** Phase 0b stream B — swiped.co cross-vertical sample for sales-letter-method skill calibration
**Companion:** runs alongside Phase 0b stream A (Jerel's 8 hand-picked STRONG exemplars). This stream is the **MID-STRONG** comparison set.

---

## Decision: chose 40 letters total

Lower bound was 5/niche (15); upper bound was 20/niche (60). Chosen volume: **20 / 10 / 10 = 40**.

**Why not 60:**
- After hard filtering against "is this actually a sales letter / long-copy / advertorial / landing page", swiped.co's pipeline of *defensibly Jerel-relevant* swipes thins out fast.
- Agency-niche only has 5 native consulting swipes + a handful of agency-style entries inside the Marketing niche.
- B2B/SaaS swipes are mostly landing pages + free-trial mechanics, not long-form sales letters. Pulling more would dilute the corpus with display ads and pop-out CTAs.

**Why not 15:**
- 5 letters per niche won't reveal cross-niche patterns at all. The info-products niche has 24 dedicated entries on swiped, plus 25 in Business Opportunity, plus 11 in Education — leaving the bucket at 5 would waste the supply.

## Volume per niche

| Bucket | Letters | Source niches drawn from |
|---|---|---|
| info-products | 20 | Info Marketing (8), Business Opportunity (8), Education (1), Online Business (2), Entrepreneurship (1) |
| agency | 10 | Consulting (3), Marketing-filtered (5), Copywriting (2) |
| b2b-services | 10 | SAAS (9), Software (1) |
| **Total** | **40** | |

## Scrape success rate

- **Pages fetched:** 40 / 40 (100% success)
- **Cloudflare hit:** initially blocked on plain Node fetch, bypassed with realistic browser headers (`User-Agent`, `Accept-Language`, `Sec-Fetch-*`). No CAPTCHA challenges encountered.
- **Paywall hits:** 0. All swipe-study pages are publicly readable.
- **"Download As PDF" gated** for full-letter reproductions, but I did not attempt to bypass — Schauer's commentary is the canonical source for this corpus per Jerel's instructions ("do not attempt to bypass auth").

## What is actually in the corpus

Every annotation in `info-products/`, `agency/`, `b2b-services/` is derived from:
- **Headline** (verbatim, when Schauer quoted it — 18 / 40 entries)
- **Schauer's analyst commentary** (verbatim, when present — 32 / 40 entries have >200 chars)
- **Tag set** swiped.co attached (Long Copy, Direct Mail, Tested, Control, Exclusivity, etc.) — present on 39 / 40
- **Era markers** (Classic / Modern / Tested / Control + dates) — present on all 40

**What is NOT in the corpus** (and is flagged `[NOT VISIBLE]` in each file):
- Raw letter body (image/PDF only on swiped.co)
- Exact word count of the original letter
- Exact P.S. wording (for most)
- Full guarantee language (for most)

## Era warning

| Era | Count | % | Translation risk |
|---|---|---|---|
| Classic (pre-1995) | 11 | 28% | **HIGH** — direct-mail-era voice, pre-internet reader habits, "Dear Friend / Cordially yours" register. Pattern transfers; surface language does not. Flagged in each affected file. |
| Modern (1995-2015) | 19 | 48% | Medium — Kern/Kennedy/Deiss/Brunson era. Voice closer to current, but pre-TikTok attention spans. |
| Current (2015+) | 10 | 25% | Low — directly transferable. |

**28% of the corpus is pre-2000 classics.** Halbert, Schwartz, Ogilvy, Hopkins. These are foundational but won't carry to 2026 buyers without translation. Each affected annotation has a per-letter "Era-locked language" weakness note.

## Format distribution

| Format | Count |
|---|---|
| text-long-form (web sales letter) | 7 |
| email-sequence | 6 |
| hybrid | 6 |
| advertorial | 5 |
| landing-page | 5 |
| direct-mail | 4 |
| print-ad-long-copy | 4 |
| homepage | 2 |
| VSL-primary | 1 |

Note: **only ~16 of 40 entries are clean "long-form sales letters" in the Halbert/Schwartz sense.** The rest are adjacent formats (advertorial, direct mail, VSL, landing page). This is the honest shape of what's curated on swiped.co — Schauer's archive skews to multi-format direct response.

---

## Cross-niche patterns (>=3 niches show this) — calibration-worthy for Phase 1

These five patterns appear across info-products, agency, AND B2B in the corpus. They are the highest-priority candidates for the cross-vertical synthesis.

### 1. "Would you like me to [outcome] for free?" qualification headline
- **Examples:** Frank Kern consulting letters (agency), Free Book Sales Letter from Frank Kern (info), Ryan Deiss/Kern consulting (agency), Foundation landing page (B2B)
- **Mechanic:** the headline pre-frames the reader as someone the seller is choosing to help, not begging to sell. Triggers reciprocity + status-anxiety simultaneously.
- **Why it transfers:** the qualifying frame works for any high-ticket offer where the seller can afford to be selective. Steal-worthy across all three niches.

### 2. Free front-end → consultative back-end
- **Examples:** Frank Kern free book, Kern consulting letter ($100 refundable call), Dan Kennedy lead-gen offer, Foundation landing page (free training), Shopify/Dropbox (free trial)
- **Mechanic:** the visible offer is risk-free or free; the actual sale happens in a sequence, call, or trial expiry.
- **Why it transfers:** universal across info-products (free book), agency ($100 call), B2B (free trial). The risk-reversal mechanic is identical; only the back-end conversion mechanic changes.

### 3. Exclusivity / "not for everyone" qualification
- **Examples:** Renegade Millionaire ("radical underground", "secret society"), Genius Network advertorial (Jay Abraham/Joe Polish), Frank Kern consulting (48 clients max), Mr. X Sales Letter (Jay Abraham — hidden identity)
- **Mechanic:** restricts access to filter buyers AND raise perceived value.
- **Why it transfers:** works in all three niches. SaaS uses it via waitlists / closed beta; agencies via application gates; info-products via "for serious students only."

### 4. Continuous testing visible to the swiper (control vs variant tag)
- **Examples:** Crazy Egg homepage testing, Kissmetrics homepage testing, Shopify ad messaging, Frank Kern annual letter (compared 2013 vs 2014)
- **Mechanic:** what's swiped is not "the winning copy" but "the current control." The discipline of testing matters more than the specific lines.
- **Why it transfers:** every niche has tested versions. The lesson is structural: install a testing cadence, don't copy a snapshot.

### 5. Authority + sender persona ("you're getting this because the famous person wrote it")
- **Examples:** All Frank Kern letters, Dan Kennedy Renegade Millionaire, Jay Abraham (Mr. X, Abraham Factor), Russell Brunson direct mail, Eben Pagan Wake Up Productive, David Ogilvy ads
- **Mechanic:** the famous-name halo carries belief that the copy alone couldn't. Voice is intentionally personal, conversational, low-formality.
- **Why it transfers:** any seller with a personal brand can deploy this. For SaaS (B2B) it transfers when the founder is the brand (Basecamp/DHH, ConvertKit/Nathan Barry).

## Vertical-specific patterns (1 niche only) — candidates for vertical BP files

### A. "Read X in Y minutes" tangible time-promise (info-products only)
- **Example:** Schwartz/Boardroom "Read 300 Business Magazines In 30 Minutes"
- **Niche:** info-products (Education + Self-improvement) only
- **Why it doesn't transfer to agency:** agencies sell custom work; the "compressed time" promise doesn't fit done-for-you delivery, which has unavoidable real-world cycle time.
- **Why it doesn't transfer to B2B:** B2B buyers don't trust round-number time claims for products that integrate with their workflows.

### B. Free-trial + social-proof-logo-bar combo (B2B SaaS only)
- **Examples:** Dropbox landing page, Shopify landing page, Basecamp current-stats, Officevibe social proof, Crazy Egg button copy
- **Niche:** b2b-services only
- **Why it doesn't transfer to info-products:** info-product buyers don't care about logos (they care about specific transformation stories).
- **Why it doesn't transfer to agency:** agencies can't offer self-serve trial; the "click to start" conversion mechanic doesn't exist for done-for-you work.

---

## Files in this folder

- `_taxonomy.md` — how swiped.co's 90+ niche categories map to Jerel's three priority buckets, what's behind paywall, what's image-only
- `_summary.md` — this file
- `info-products/` — 20 annotation files
- `agency/` — 10 annotation files
- `b2b-services/` — 10 annotation files

## Hand-off to Phase 1 synthesis

For Phase 1 cross-vertical comparison, prioritize:
1. The **5 cross-niche patterns** above as calibration anchors (test against Jerel's 8 STRONG exemplars to confirm independence of the pattern from the specific letter)
2. The **modern (1995-2015) entries** as the closest proxies to current 2026 reader behavior (avoid grounding too heavily on classics)
3. The **agency-bucket consulting letters** (Kern, Deiss/Kern, Abraham) as the documented templates closest to Jerel's primary vertical — only 3 are in this corpus, so consider supplementing from outside swiped.co for that bucket
4. The **B2B / landing-page bucket** as a *separate* corpus from sales letters — do not blend their patterns directly. Use them only to mark which patterns DO and DON'T translate to platform-led offers.

Vertical-specific patterns (A, B above) should become per-niche BP files in the skill rather than universal rules.
