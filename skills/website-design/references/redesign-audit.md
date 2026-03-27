## Graph Links
- **Parent skill:** [[website-design]]
- **Sibling references:** [[aesthetic-guidelines]], [[cinematic-presets]], [[creative-arsenal]]
- **Used by:** Mode C (Hybrid), standalone site reviews

# Redesign Audit — 7-Category Structured Checklist

Systematic design quality audit for Mode C (Hybrid) redesigns and standalone site reviews. Run this between analysis and redesign to identify exactly what to preserve vs improve.

> **Adapted from** [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) redesign-skill, filtered for HTML + Tailwind + GSAP stack.

---

## How to Use

1. **Screenshot the reference** or existing site
2. **Score each category** (1-5): 1 = critical issues, 3 = acceptable, 5 = excellent
3. **Mark items** as KEEP (preserve in redesign) or FIX (change in redesign)
4. **Apply fixes in priority order** (see bottom of this doc)
5. **Re-screenshot and re-score** after changes

---

## 1. Typography (8 checks)

- [ ] **T1 — No browser defaults:** No Times New Roman, system serif, or unstyled headings
- [ ] **T2 — Headline presence:** At least one heading is large enough (48px+) to anchor the page
- [ ] **T3 — Body width:** Body text stays within 60-75ch per line (not spanning full viewport)
- [ ] **T4 — Weight variety:** Uses at least 3 font weights (e.g., 400, 600, 800) for clear hierarchy
- [ ] **T5 — Number formatting:** Stats, prices, and data use tabular figures, not default proportional
- [ ] **T6 — Letter-spacing:** Large headings have tightened tracking (≤ -0.02em); small labels have normal or slightly open tracking
- [ ] **T7 — No orphaned words:** Headlines don't leave a single word dangling on the last line (use `text-wrap: balance` or manual `<br>`)
- [ ] **T8 — Font pairing:** Heading and body fonts are intentionally different families (not the same font at different weights)

**Category score:** __ / 5

---

## 2. Color & Surfaces (11 checks)

- [ ] **C1 — No pure black text:** Body text uses off-black (#1a1a1a, #111827) instead of #000000
- [ ] **C2 — No oversaturated accents:** Accent colors have saturation below 80% — desaturated enough to blend with neutrals
- [ ] **C3 — Accent count:** Max 1-2 accent colors (not a rainbow)
- [ ] **C4 — Gray temperature:** All grays are either warm OR cool — never mixing warm and cool grays
- [ ] **C5 — No AI gradient fingerprint:** No purple-to-blue gradient on white background (the #1 AI cliche)
- [ ] **C6 — Shadow quality:** Shadows are multi-layered AND tinted to the background hue — not flat `shadow-md` or pure-black low-opacity
- [ ] **C7 — Texture presence:** At least one section has depth beyond flat color (grain, gradient, pattern, image)
- [ ] **C8 — Background variety:** Sections alternate between at least 2 surface treatments (not all same bg color)
- [ ] **C9 — Contrast compliance:** Text passes WCAG AA contrast (4.5:1 for body, 3:1 for large text)
- [ ] **C10 — Muted text legibility:** Any text with reduced opacity or muted color is still comfortably readable at a glance
- [ ] **C11 — Color confidence:** The palette feels decisive — one dominant color leads, others clearly support

**Category score:** __ / 5

---

## 3. Layout (12 checks)

- [ ] **L1 — No center bias:** At high DESIGN_VARIANCE (7+), hero is NOT centered-text-over-image (use split-screen, left-aligned, or asymmetric). Centered heroes are fine at DESIGN_VARIANCE ≤ 6 for conversion pages.
- [ ] **L2 — No card wall:** Features are NOT presented as 3 identical equal-width cards unless VISUAL_DENSITY > 7. Use 2-column zig-zag, asymmetric bento, or horizontal scroll instead.
- [ ] **L3 — Viewport height:** Uses `min-h-[100dvh]` instead of `h-screen` for full-height sections (avoids mobile address bar bug)
- [ ] **L4 — Max-width container:** Content is constrained to 1200-1440px with auto margins — not full-bleed text
- [ ] **L5 — Overlap/depth:** At least one element overlaps section boundaries or sits on a different visual plane
- [ ] **L6 — Whitespace balance:** Spacing between sections is deliberate — tighter for related groups, generous for major transitions
- [ ] **L7 — Visual rhythm:** Sections have varied layouts — not the same left-right pattern repeated 4 times
- [ ] **L8 — Mobile stacking:** Multi-column layouts stack cleanly on mobile without broken proportions
- [ ] **L9 — Grid over flex math:** Multi-column layouts use CSS Grid (not flex with percentage widths)
- [ ] **L10 — Section transitions:** Sections don't just butt against each other — there's a visual transition (spacing, color change, divider, or overlap)
- [ ] **L11 — Content density:** Amount of content per section feels proportional to its importance
- [ ] **L12 — Scroll length:** Total page length is proportional to content depth — no padding a thin page with empty space

**Category score:** __ / 5

---

## 4. Interactivity (11 checks)

- [ ] **I1 — Hover states:** Every clickable element has a visible hover state
- [ ] **I2 — Active/pressed:** Buttons have a pressed state (subtle scale down to 0.98)
- [ ] **I3 — Transition duration:** Hover transitions are 150-300ms — not instant, not sluggish
- [ ] **I4 — Transition specificity:** Uses `transition-transform`, `transition-opacity`, etc. — never `transition-all`
- [ ] **I5 — Focus ring:** Keyboard-focusable elements have visible `focus-visible` styles
- [ ] **I6 — Loading states:** Forms and async actions show loading feedback (spinner, disabled state)
- [ ] **I7 — Empty states:** Lists and grids have designed empty states (not just blank space or raw "No items")
- [ ] **I8 — Error states:** Forms show inline validation errors with helpful messages
- [ ] **I9 — Scroll behavior:** Page uses `scroll-behavior: smooth` for anchor links
- [ ] **I10 — Easing quality:** Animations use power/cubic-bezier easing — not linear
- [ ] **I11 — Reduced motion:** `@media (prefers-reduced-motion)` disables parallax, auto-play, and complex animations

**Category score:** __ / 5

---

## 5. Content (11 checks)

- [ ] **N1 — No generic names:** No "John Doe" or "Jane Smith" — use realistic, diverse names if placeholder
- [ ] **N2 — No round numbers:** No "99.99%" or "$100" — use organic data ("47.2%", "$97")
- [ ] **N3 — No AI cliches:** None of: Elevate, Seamless, Unleash, Next-Gen, Game-changer, Cutting-edge, Revolutionary, Empower, Transform, Leverage, Unlock
- [ ] **N4 — No Lorem Ipsum:** All text is real copy or realistic placeholder copy
- [ ] **N5 — Active voice:** Headlines and CTAs use active voice, not passive
- [ ] **N6 — Unique avatars:** Testimonial/team avatars are all different (not same stock photo repeated)
- [ ] **N7 — Specific claims:** Benefits are specific ("Saves 4.2 hours/week") not vague ("Saves time")
- [ ] **N8 — Social proof variety:** Social proof includes mix of formats (quotes, logos, stats, case studies) — not just 3 identical quote cards
- [ ] **N9 — CTA variety:** Multiple CTAs vary in intensity (primary button, text link, soft prompt) — not all the same big button
- [ ] **N10 — Microcopy:** Form labels, button text, and helper text are thoughtful (not generic "Submit")
- [ ] **N11 — Content hierarchy:** Most important message is above the fold with clear visual priority

**Category score:** __ / 5

---

## 6. Components (10 checks)

- [ ] **P1 — No generic cards:** Feature cards have personality beyond "icon + title + description in a box"
- [ ] **P2 — Button variations:** At least 2 button styles (primary filled + secondary outline/ghost)
- [ ] **P3 — Badge/tag patterns:** If categories or labels exist, they have styled badge/tag components
- [ ] **P4 — No FAQ accordion wall:** FAQ sections have visual design beyond plain accordion (grouped categories, illustrations, or search)
- [ ] **P5 — No modal overuse:** Modals are used for confirmations/forms only — not for content that belongs on-page
- [ ] **P6 — Footer substance:** Footer has structured content (nav columns, newsletter, social) — not just a copyright line
- [ ] **P7 — Nav completeness:** Navigation includes logo, links, and CTA — not just text links
- [ ] **P8 — Image treatment:** Images have consistent treatment (rounded corners, aspect ratios, color grading)
- [ ] **P9 — Icon consistency:** Icons are from one family/style (all outline OR all solid, same weight)
- [ ] **P10 — Divider design:** If section dividers exist, they're styled (not plain `<hr>`)

**Category score:** __ / 5

---

## 7. Strategic Omissions (6 checks)

Things often forgotten that signal a complete, professional build:

- [ ] **S1 — Legal links:** Privacy policy / Terms of Service links exist (at least in footer)
- [ ] **S2 — 404 page:** If multi-page, a custom 404 exists (or note: "single-page, N/A")
- [ ] **S3 — Form validation:** All forms have client-side validation with helpful error messages
- [ ] **S4 — Skip-to-content:** Accessibility: `<a href="#main" class="sr-only focus:not-sr-only">` exists
- [ ] **S5 — Cookie/consent:** If tracking pixels are present, a consent banner exists
- [ ] **S6 — Favicon/OG image:** `<link rel="icon">` and Open Graph meta tags are set

**Category score:** __ / 5

---

## Scoring Summary

| Category | Score | Verdict |
|----------|-------|---------|
| 1. Typography | /5 | |
| 2. Color & Surfaces | /5 | |
| 3. Layout | /5 | |
| 4. Interactivity | /5 | |
| 5. Content | /5 | |
| 6. Components | /5 | |
| 7. Strategic Omissions | /5 | |
| **Average** | **/5** | |

**Minimum passing: 3.0 average. Below 3.0 = must iterate before declaring done.**

---

## Fix Priority Order

When the audit reveals multiple issues, fix in this order (highest impact first):

1. **Font swap** — Replace browser defaults or banned fonts with intentional pairings
2. **Color cleanup** — Fix pure black text, oversaturated accents, mixed gray temperatures
3. **Hover states** — Add hover/focus/active to all clickable elements
4. **Layout & spacing** — Fix center bias, card walls, viewport height, container max-width
5. **Component replacement** — Redesign generic cards, buttons, FAQ, footer
6. **State design** — Add loading, empty, error states to interactive elements
7. **Typography polish** — Tighten tracking, fix line widths, balance text wrapping

> This order maximizes visual transformation per unit of effort. Font + color changes are instant wins; state design is important but invisible until triggered.
