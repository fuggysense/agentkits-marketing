## Graph Links
- **Parent skill:** [[website-design]]
- **Sibling references:** [[browser-automation]], [[cinematic-presets]], [[component-sources]], [[gallery-sources]], [[scroll-driven-design]]
- **Related skills:** [[page-cro]], [[brand-building]]

# Aesthetic Guidelines — Anti-Generic Guardrails

Merged from frontend-design skill + CLAUDE.md universal rules. Apply to ALL website builds.

---

## Banned Patterns

These patterns produce "AI slop" — generic, recognizable-as-AI output. Never use as primary/default choice.

### Typography
- **Inter, Roboto, Arial, system fonts** as heading or primary body font
- **Space Grotesk** as heading font (overused in AI-generated designs)
- **Serif fonts in dashboard/software UI contexts** — serif headings belong in editorial/marketing pages, not app interfaces
- Same font for headings AND body — always pair a display/serif with a clean sans
- Default browser font stack without intentional choice

### Color
- **Default Tailwind palette** (indigo-500, blue-600, etc.) as primary brand color
- **Purple gradients on white backgrounds** — the #1 AI design cliché
- Evenly-distributed, timid palettes — commit to a dominant color with sharp accents
- Pure black (#000000) text on pure white (#FFFFFF) without contrast adjustment

### Effects
- **`transition-all`** — always specify exact properties (`transition-transform`, `transition-opacity`)
- **Flat `shadow-md`** — use layered, color-tinted shadows instead
- **Uncustomized `shadcn/ui` defaults** — if using shadcn components, customize radii, colors, and shadows to match the aesthetic direction
- Cookie-cutter glassmorphism without purpose
- Uniform border-radius on everything

### Layout
- Identical card grids repeated throughout the page
- Default component patterns without context-specific character
- Same layout for consecutive sections
- Centered hero when DESIGN_VARIANCE > 6 (use split-screen, left-aligned, or asymmetric instead). Centered heroes are fine at ≤ 6 for conversion-focused pages.
- 3-column equal card grids as the primary feature section (use 2-column zig-zag, asymmetric bento, or horizontal scroll). Cards-in-grid is acceptable when VISUAL_DENSITY > 7 or when showing 6+ items.

### Content
- Generic placeholder names (John Doe, Jane Smith) — use realistic, diverse names
- Round placeholder numbers (99.99%, $100) — use organic-feeling data (47.2%, $97)
- AI cliches in headlines or body: Elevate, Seamless, Unleash, Next-Gen, Game-changer, Cutting-edge, Revolutionary, Empower, Leverage, Unlock
- **Emojis in code, markup, or body text** — use proper icons or SVG primitives instead
- Accent color saturation above 80% — desaturate to blend naturally with the neutral palette
- Mixing warm and cool grays in the same build — pick one temperature

---

## Required Patterns

Every build MUST include these. Check before declaring done.

### Typography
- **Paired fonts:** Display/serif for headings + clean sans for body (or vice versa)
- **Tight tracking** on large headings: `letter-spacing: -0.03em` or tighter
- **Generous line-height** on body text: `1.6-1.7`
- Intentional font size scale — not random Tailwind text-{size} steps

### Color & Shadows
- **Custom palette** derived from brand or aesthetic direction — not default Tailwind
- **Layered, color-tinted shadows:** Multiple shadow layers with low-opacity brand/accent tint
  ```css
  box-shadow: 0 4px 6px rgba(accent, 0.08), 0 12px 24px rgba(accent, 0.12);
  ```
- **Dominant + accent** color relationship — one color leads, others support
- CSS variables for color consistency

### Gradients & Backgrounds
- **Multi-gradient + noise** for atmospheric backgrounds
- Noise overlay via SVG filter (0.02-0.04 opacity) for texture/depth
- Image overlays: `bg-gradient-to-t from-black/60` + `mix-blend-multiply` color treatment
- Background variety between sections — not all the same solid color

### Interaction States
- **Every clickable element** needs: hover, focus-visible, AND active states
- Animate only `transform` and `opacity` — never `transition-all`
- Spring-style or power easing (not linear)
- Buttons: subtle scale (1.02 hover, 0.98 press)

### Layout
- **Max-width container** (1200-1440px) with auto margins for all text content
- **`min-h-[100dvh]`** instead of `h-screen` for full-height sections (avoids mobile address bar bug)
- **CSS Grid** over Flex percentage math for multi-column layouts
- Tint shadows to background hue — no pure black shadows at low opacity

### Spacing & Depth
- **Consistent spacing tokens** — pick a scale (4, 8, 16, 24, 32, 48, 64, 96) and stick to it
- **Layering system:** base → elevated → floating surfaces at different z-planes
- Not all elements sit on the same visual plane

---

## Typography Recommendations

Distinctive alternatives to banned fonts:

### Display / Heading Fonts
- **Syne** — geometric, bold, distinctive
- **Clash Display** — modern, sharp, premium
- **Cabinet Grotesk** — clean but characterful
- **Instrument Serif** — elegant editorial
- **DM Serif Display** — warm, approachable serif
- **Plus Jakarta Sans** — modern geometric sans (used well at heavier weights)
- **Satoshi** — clean, distinctive geometric
- **Fraunces** — variable optical-size serif, luxury/editorial feel
- **Monument Extended** — ultra-wide brutalist display, high impact at large scales

### Body Fonts
- **IBM Plex Sans** — professional, readable
- **General Sans** — modern, clean
- **Outfit** — friendly, geometric
- **Figtree** — humanist, warm
- **Manrope** — modern, readable
- **Switzer** — clean geometric sans with character

### Mono Fonts
- **JetBrains Mono** — developer favorite
- **Fira Code** — ligature support
- **IBM Plex Mono** — professional

---

## Self-Review Checklist

Run this after every build (creation mode) or when modifying aesthetics (hybrid mode):

1. [ ] No banned fonts as primary choice?
2. [ ] No default Tailwind palette as brand color?
3. [ ] No purple-gradient-on-white?
4. [ ] Fonts are paired (heading ≠ body)?
5. [ ] Shadows are layered + color-tinted?
6. [ ] All clickables have hover + focus + active states?
7. [ ] No `transition-all` anywhere?
8. [ ] Spacing follows a consistent token scale?
9. [ ] Surfaces have depth/layering (not all flat)?
10. [ ] Background varies between sections?
11. [ ] Would a designer call this "obviously AI"? → If yes, fix it.
12. [ ] Is the aesthetic direction INTENTIONAL and BOLD (not safe/generic)?

---

## Design Quality Score

Rate every build on these 5 dimensions. Use during screenshot review (Mode B Step 4, Mode C post-audit).

| Dimension | 1 (Weak) | 3 (Acceptable) | 5 (Exceptional) |
|-----------|----------|-----------------|------------------|
| **Typography Intent** | Default fonts, no hierarchy | Paired fonts, basic scale | Editorial-grade hierarchy, optical sizing, tight tracking on display |
| **Color Confidence** | Default palette, timid accents | Custom palette, clear dominant | Bold palette with emotional resonance, decisive accent usage |
| **Layout Distinctiveness** | Standard centered sections | Some variety, 2+ layout types | Memorable composition, would screenshot for inspiration |
| **Interaction Polish** | No hover states | Basic hover + opacity transitions | Delightful micro-interactions, spring easing, state awareness |
| **Overall Memorability** | Generic, forgettable | Competent, professional | Someone would share this as design inspiration |

**Minimum passing: 3.0 average across all 5 dimensions. Below 3.0 = must iterate before declaring done.**

Scoring formula: Sum all 5 scores, divide by 5. Report as "DQS: X.X/5" in screenshot review notes.
