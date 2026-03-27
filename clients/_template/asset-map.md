# Asset Map

> **PURPOSE:** Single source of truth for where all marketing assets live for this project.
> Claude MUST read this file first when asked about project assets, status, or "what do we have."
> Update this file whenever new assets are created anywhere.

## Asset Locations

### In-Project (`clients/<project-slug>/`)
| Path | Contents |
|------|----------|
| `assets/` | Reusable creative — logos, images, templates |
| `campaigns/<slug>/` | Campaign-specific assets, briefs, results |
| `case-studies.md` | Client case studies and proof points |
| `feedback/` | Client quotes, post-mortems, A/B test results |

### In Docs (`docs/content/`)
| Path | Contents |
|------|----------|
| `docs/content/ads/` | Ad copy and image prompts |
| `docs/content/emails/` | Email copy and sequences |
| `docs/content/landing-pages/` | Landing page copy |
| `docs/content/social/` | Social media posts |
| `docs/content/blog/` | Blog posts and articles |

### Other Locations
| Path | Contents |
|------|----------|
| `docs/content/` | Any other content subdirectories |
| `voice/<person>/` | Voice profile files (shared across projects) |

---

## Asset Registry

<!-- Update this section as assets are created. Format: -->
<!-- | Asset | Location | Date | Status | -->
<!-- | Meta ad copy (9 variations) | docs/content/ads/meta-lead-gen-YYMMDD.md | 260312 | Draft | -->

| Asset | Location | Date | Status |
|-------|----------|------|--------|
| *(fill as assets are created)* | | | |

---

## Routing Rules (for Claude)

1. **When asked "what assets do we have"** — scan ALL locations above, not just `assets/`
2. **When creating new assets** — add an entry to the Asset Registry above
3. **When reporting project status** — always include asset count from this map
4. **Never say "assets folder is empty"** without checking docs/content/ first
