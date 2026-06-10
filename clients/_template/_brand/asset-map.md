# Asset Map

> **PURPOSE:** Single source of truth for where all marketing assets live for this project.
> Claude MUST read this file first when asked about project assets, status, or "what do we have."
> Update this file whenever new assets are created anywhere.

## Asset Locations

### In-Project (`clients/<project-slug>/`)
| Path | Contents |
|------|----------|
| `_brand/brand-assets/` | Approved reusable creative — logos, product shots, packaging, style sheets, reusable AI-approved assets |
| `_brand/visual-characters/` | Approved generated presenters, mascots, recurring faces, actor references, and face-lock assets |
| `_brand/avatars/` | Legacy/tooling exports only; not buyer targeting |
| `campaigns/<slug>/` | Campaign-specific assets, briefs, results |
| `videos/<slug>/` | Video Studio runs created by `/video:new` |
| `05_handoff/output/` | Final handoff notes and promoted asset logs |

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
| `[external path]` | Original heavy media folders. Link here rather than duplicating multi-GB source material into the repo. |

---

## Asset Registry

<!-- Update this section as assets are created. Format: -->
<!-- | Asset | Location | Date | Status | -->
<!-- | Meta ad copy (9 variations) | docs/content/ads/meta-lead-gen-YYMMDD.md | 260312 | Draft | -->

| Asset | Location | Date | Status |
|-------|----------|------|--------|
| *(fill as assets are created)* | | | |

## External Source Registry

| Source | Location | Contents | Import Policy |
|---|---|---|---|
| *(fill when source folders exist)* | | | Link and summarize first; copy only approved reusable assets into `_brand/brand-assets/` |

---

## Routing Rules (for Claude)

1. **When asked "what assets do we have"** — scan ALL locations above, not just `assets/`
2. **When creating new assets** — add campaign-specific assets to the campaign registry first
3. **When promoting reusable assets** — copy only approved assets into `_brand/brand-assets/` and add an Asset Registry entry
4. **When reporting project status** — always include asset count from this map
5. **Never say "assets folder is empty"** without checking docs/content/ first
