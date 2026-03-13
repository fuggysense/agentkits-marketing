# Aesthetic Guidelines — Anti-Generic Guardrails

Merged from frontend-design skill + CLAUDE.md universal rules. Apply to ALL website builds.

---

## Banned Patterns

These patterns produce "AI slop" — generic, recognizable-as-AI output. Never use as primary/default choice.

### Typography
- **Inter, Roboto, Arial, system fonts** as heading or primary body font
- **Space Grotesk** as heading font (overused in AI-generated designs)
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
- Cookie-cutter glassmorphism without purpose
- Uniform border-radius on everything

### Layout
- Identical card grids repeated throughout the page
- Default component patterns without context-specific character
- Same layout for consecutive sections

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

### Body Fonts
- **IBM Plex Sans** — professional, readable
- **General Sans** — modern, clean
- **Outfit** — friendly, geometric
- **Figtree** — humanist, warm
- **Manrope** — modern, readable

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
