# HazeCraft Agency Wrapper

Use this when a skill creates an agency-facing or client-review artifact for Jerel/HazeCraft: concept packs, client briefs, review galleries, prompt packs, strategy reports, dashboards, decks, motion-spec boards, and video-animation references.

Do not use this as a replacement for a client's own brand. Client-owned final ads, product visuals, landing pages, social posts, and render prompts should use the client brand unless the user explicitly asks for a HazeCraft-branded asset.

## Source Of Truth

Read these files before building a HazeCraft-styled artifact:

- `clients/hazecraft/brand/DESIGN/design-system.md`
- `clients/hazecraft/brand/DESIGN/project/ds.css`
- `clients/hazecraft/brand/DESIGN/project/Design Spec.html` when component detail is needed
- `clients/hazecraft/brand/DESIGN/project/assets/logos/` when a logo or lockup is needed

The folder `/Users/jerel/Downloads/Haze Craft Design System` is only an import source. The repo copy above is the working source.

## Routing Rule

Use HazeCraft wrapper for:

- Client-facing concept packs where HazeCraft is presenting strategic options.
- Internal or client-review HTML reports.
- Prompt-pack galleries and input-image approval galleries.
- Video Studio / Video Factory review surfaces.
- Motion graphics that represent HazeCraft, not the client's consumer-facing brand.
- Agency decks, case studies, and status dashboards.

Do not use HazeCraft wrapper for:

- Final client ads that must look like the client's brand.
- Product packaging, product renders, or brand-owned images.
- Client landing pages, client social posts, client marketplace cards, or final creative unless HazeCraft is intentionally the visible publisher.
- Medical, legal, financial, or compliance copy presentation where the design might make unapproved claims look final.

## Visual Rules

- Canvas: white `#FFFFFF`; off-white `#F7F8FB` for banded sections.
- Color system: navy `#0F2A5F` is the workhorse (headlines, fills, structure); blue `#2F6DB5` is the interactive accent (replaces the old hot red — links, current-phase, hover, single interactive focal point per view); gold `#B8945A` is a sparing premium cue (<5%) for dividers and small accents only — never a fill or CTA.
- Type: Cinzel for the hero promise + H1/H2 only (short strings — unreadable on body), Montserrat for everything else (H3 down, body, CTAs, UI, eyebrows), JetBrains Mono for IDs/timestamps/paths/code.
- Display type: serif, positive 0.02em tracking, calm hierarchy. Never negative-track a serif.
- Surfaces: light cards with cool navy-tinted soft shadows, hairline borders, corner marks (navy) used as measured cues.
- Corners: 12px default cards; pills/buttons fully rounded (999px). The old 0-4px sharp default is retired.
- Icons: Lucide outline, 1.5px stroke, no emoji; muted by default; only the glyph turns blue on hover.
- Shadows: use the cool navy-tinted soft shadows (`0 1px 2px / 0 4px 12px / 0 16px 40px rgba(15,42,95,…)`). No accent glow.
- Charts: chart palette is functional only and must not become brand color. **Exception:** when a chart belongs to the single recommended-winner element on a review surface (e.g. compass score bars on the AG1 winner card), the bars may use a brand-navy fill (`rgba(15,42,95,0.6)`) so the winner reads as one cohesive navy focal point. This is the ONLY chart exception — all non-winner charts stay neutral.
- Motion: 240ms hover, 420ms reveal, 420ms data animations, 160ms micro; `cubic-bezier(0.22,1,0.36,1)` only unless a component has a stronger source rule. No bouncy easings.
- Font loading: Cinzel + Montserrat + JetBrains Mono load via Google Fonts `@import` inside an inline `<style>` block. This is permitted on otherwise self-contained single-file HTML deliverables because typography is a presentation primitive, not a layout dependency. If a fully offline deliverable is required, base64-embed the WOFF2 files instead — do not fall back to system-font stacks (the wrapper's hierarchy depends on the specified weights).

## Artifact Contracts

### HTML concept packs and reports

Use HazeCraft as the shell:

- Header chrome with project, client, stage, and approval state.
- Light canvas (white or banded off-white); an optional navy hero block for the masthead.
- Sections with clear numerical Montserrat all-caps labels.
- Cards with hairline borders, soft navy-tinted shadows, and top-left navy corner marks.
- A single blue accent on the recommended action or current gate (danger color for the highest-priority warning).
- Client/product assets displayed inside neutral white containment so the asset itself remains accurate.

### Prompt and image approval galleries

Use HazeCraft as the review frame, but keep generated and client-provided images visually unaltered. Do not apply filters, brand overlays, or color treatments to images that are being approved for reference fidelity.

### Video and motion assets

Use HazeCraft when the animation is an agency deliverable, explainer, dashboard, or review surface:

- Lower-thirds: Montserrat all-caps eyebrow, Cinzel title (short) or Montserrat for longer lines, blue for the key word or current phase, gold as a sparing cue.
- Background: light, or a navy hero block when the moment needs weight.
- Transitions: restrained reveals on `cubic-bezier(0.22,1,0.36,1)`, no bouncy or playful easing.
- Frame language: measured drawing, process map, data board, or operating manual.

For client video renders, HazeCraft can style the review page and prompt pack, but the render prompt must still use the approved client brand or campaign style profile.

## Data Flow

1. The producing skill writes structured content first.
2. The HazeCraft wrapper reads that structured content and renders the review surface.
3. Approval state stays in JSON or Markdown gate files, not only in HTML.
4. Approved reusable HazeCraft assets are logged in `clients/hazecraft/asset-map.md`.
5. Approved reusable client assets are logged in that client's `_brand/asset-map.md`.

## Naming

Use file names that reveal both content and shell:

- `concept-pack.html` for the concept artifact.
- `client-brief.html` only when an HTML brief is explicitly requested.
- `input-image-review.html` for image approval galleries.
- `render-prompt-review.html` for render prompt approval.

Avoid names like `pretty.html`, `final.html`, or `new-design.html`.
