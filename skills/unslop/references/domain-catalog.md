# Unslop Domain Catalog

Tracks all profiled domains, generation metadata, and freshness.

| Domain | Slug | Type | Samples | Model | Generated | Status |
|--------|------|------|---------|-------|-----------|--------|
| LinkedIn posts | linkedin-posts | text | 50 | Claude (default) | 260319 | Active |
| SaaS landing pages | saas-landing-pages | text | 50 | Claude (default) | 260319 | Active |
| Email sequences | email-sequences | text | 50 | Claude (default) | 260319 | Active |
| Blog writing | blog-writing | text | 50 | Claude (default) | 260319 | Active |
| Video scripts | video-scripts | text | 50 | Claude (default) | 260319 | Active |
| TikTok hooks | tiktok-hooks | text | 50 | Claude (default) | 260319 | Active |
| pSEO templates | pseo-templates | text | 50 | Claude (default) | 260319 | Active |

## Freshness Rules

- Profiles >90 days old: flag for regeneration (expires ~260618)
- After major model update: regenerate all profiles
- Track which model version was used for each profile

## Dedup Log

| Domain | Patterns Removed | Date |
|--------|-----------------|------|
| LinkedIn posts | 6 (em-dash rule, "landscape", "dive in", "It's not X/it's Y", revelation hooks, "in today's world/era") | 260319 |
| SaaS landing pages | 5 (em-dash rule, "seamless/robust/innovative", "It's not X/it's Y", "leverage/streamline", business jargon) | 260319 |
| Email sequences | 4 (em-dash rule, "here's the thing", "It's not X/it's Y" variant, formal transitions) | 260319 |
| Blog writing | 5 (em-dash rule, "here's the thing", "It's not X/it's Y", revelation hooks, "in today's world") | 260319 |
| Video scripts | 4 (em-dash rule, "here's the thing/why", "It's not X/it's Y", revelation hooks) | 260319 |
| TikTok hooks | 3 (em-dash rule, "here's the thing", revelation hooks) | 260319 |
| pSEO templates | 3 (em-dash overuse, "Not X, Y" contrast, "here's the/what") | 260319 |

## Future Domains

| Domain | Type | Notes |
|--------|------|-------|
| Landing page design | visual | Requires Playwright install |
