## Graph Links
- **Parent skill:** [[website-design]]
- **Sibling references:** [[aesthetic-guidelines]], [[browser-automation]], [[cinematic-presets]], [[component-sources]], [[scroll-driven-design]]
- **Related skills:** [[page-cro]], [[brand-building]]

# Gallery Sources Reference

## Gallery Strengths & Usage

| Gallery | Best For | Volume | Curation | URL Pattern |
|---------|----------|--------|----------|-------------|
| godly.website | Modern SaaS, tech startups | Medium | High (hand-picked) | `godly.website` |
| awwwards.com | Creative agencies, premium design | Large | Award-based | `awwwards.com/websites/` |
| landingfolio.com | Landing pages specifically | Large | Medium | `landingfolio.com/inspiration` |
| lapa.ninja | General landing pages, volume | Very large | Low (bulk) | `lapa.ninja` |
| onepagelove.com | Single-page sites, portfolios | Medium | High | `onepagelove.com` |

---

## Per-Gallery Details

### godly.website
- **Strengths:** Curated, modern SaaS aesthetic, excellent filter by category
- **Categories:** SaaS, Agency, Portfolio, E-commerce, Startup, AI
- **URL patterns:**
  - Browse all: `https://godly.website`
  - By category: `https://godly.website/category/saas`
- **DOM selectors:** `a[href*='/website/']` for items, nested `img` for thumbnails
- **Rate limiting:** None observed, but be respectful — 2s between requests
- **Best used when:** User wants modern, clean SaaS inspiration

### awwwards.com
- **Strengths:** Award-winning designs, very high quality
- **Categories:** Filtered by nominees, winners, honorable mentions
- **URL patterns:**
  - Browse: `https://www.awwwards.com/websites/`
  - By tag: `https://www.awwwards.com/websites/corporate/`
- **DOM selectors:** `.js-collectable` for items, `.rollover img` for thumbnails
- **Rate limiting:** May require cookies/login for full access
- **Best used when:** User wants creative, high-end, experimental design

### landingfolio.com
- **Strengths:** Focused on landing pages, organized by section type
- **Categories:** SaaS, App, Agency, Product, by section (hero, pricing, CTA)
- **URL patterns:**
  - Browse: `https://www.landingfolio.com/inspiration`
  - By type: `https://www.landingfolio.com/inspiration/landing-page/saas`
- **DOM selectors:** `.inspiration-card` or `a[href*='/inspiration/']`
- **Rate limiting:** None observed
- **Best used when:** User needs landing page specific inspiration

### lapa.ninja
- **Strengths:** Huge volume, good for finding niche examples
- **Categories:** By color, industry, style
- **URL patterns:**
  - Browse: `https://www.lapa.ninja`
  - By category: `https://www.lapa.ninja/category/saas`
- **DOM selectors:** `.grid-item a` or `a[href*='/post/']`
- **Rate limiting:** None observed
- **Best used when:** Need volume of options, especially for niche industries

### onepagelove.com
- **Strengths:** Single-page focus, great for one-page marketing sites
- **Categories:** By template type, industry
- **URL patterns:**
  - Browse: `https://onepagelove.com`
  - Templates: `https://onepagelove.com/templates`
- **DOM selectors:** `.post-entry a` for items
- **Rate limiting:** None observed
- **Best used when:** Building a single-page site or portfolio

---

## Gallery Selection Strategy

| User Wants | Recommend |
|------------|-----------|
| SaaS landing page | godly.website → landingfolio.com |
| Creative/agency site | awwwards.com → godly.website |
| Simple single-page | onepagelove.com |
| Lots of options to browse | lapa.ninja → landingfolio.com |
| Specific section inspiration (hero, pricing) | landingfolio.com |
| AI/tech startup | godly.website (AI category) |

## Workflow

1. Ask user about industry/vibe → pick 2-3 galleries
2. Run `browser-tools.py gallery <url> --limit 8` on each
3. Screenshot top picks: `browser-tools.py screenshot <site_url> /tmp/inspo-N.png --full-page`
4. Present to user for selection
5. Deep-capture winner (desktop + mobile full-page screenshots)
