## Graph Links
- **Parent skill:** [[website-design]]
- **Sibling references:** [[aesthetic-guidelines]], [[cinematic-presets]], [[creative-arsenal]], [[scroll-driven-design]]
- **Related skills:** [[brand-building]], [[page-cro]]

# Aesthetic Modes — Soft, Minimalist, Brutalist

Three opinionated aesthetic systems for Mode B/C builds. Each mode defines palette, typography, surface treatment, component rules, motion philosophy, and anti-patterns.

> **Attribution:** Adapted from [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (soft-skill, minimalist-skill, brutalist-skill). Translated from React + Framer Motion to our HTML + Tailwind + GSAP stack.

---

## Mode Selection

| User Signal | Recommended Mode |
|-------------|-----------------|
| "luxury", "agency", "premium", "expensive-feeling" | **Soft** |
| "editorial", "workspace", "clean", "Notion-like", "Linear-like" | **Minimalist** |
| "raw", "industrial", "tactical", "brutalist", "blueprint" | **Brutalist** |
| "portfolio" (creative/design) | Soft or Brutalist (ask user) |
| "dashboard", "data-heavy" | Minimalist or Brutalist (ask user) |
| "SaaS landing page" | Soft (default) or Minimalist |

After selecting a mode, verify choices against `aesthetic-guidelines.md` guardrails before proceeding.

---

## 1. Soft Mode (Luxury / Agency)

**Vibe:** $150k agency build. Apple meets high-end studio — haptic depth, cinematic spatial rhythm, obsessive micro-interactions.

### Palette
Use one of these directions based on context:
- **Dark luxury (SaaS/AI/Tech):** OLED black `#050505`, radial mesh gradient accents (subtle purple/emerald orbs), cards with `backdrop-blur-2xl` + `bg-white/5` hairlines
- **Warm luxury (Lifestyle/Agency):** Warm creams `#FDFBF7`, muted sage, deep espresso. CSS noise overlay at `opacity: 0.03` for paper texture
- **Silver luxury (Consumer/Portfolio):** Silver-grey `#F4F4F5` to white, ultra-diffused ambient shadows, maximum typographic contrast

### Typography
| Role | Fonts | Notes |
|------|-------|-------|
| Display | Clash Display, PP Editorial New, Fraunces, Monument Extended | Tight tracking `-0.03em` to `-0.06em`, line-height `0.9-1.1` |
| Body | Geist Sans, Switzer, Plus Jakarta Sans, Figtree | Line-height `1.6`, off-black `#1A1A1A` not pure black |
| Mono | JetBrains Mono, Geist Mono | For code blocks, metadata |

### Surface Treatment — Double-Bezel Architecture
Premium cards use nested enclosures — an outer shell wrapping an inner core, like machined hardware.

```html
<!-- Outer Shell -->
<div class="p-1.5 rounded-[2rem] bg-black/5 ring-1 ring-black/5">
  <!-- Inner Core -->
  <div class="rounded-[calc(2rem-0.375rem)] bg-white shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)] p-8">
    <!-- Content -->
  </div>
</div>
```

- Outer shell: subtle tinted background, hairline ring, generous radius
- Inner core: own background, inset highlight shadow, mathematically smaller radius for concentric curves
- Never place premium cards flat on the background without this nesting

### Component Rules
- **Navigation:** Floating glass pill detached from top (`mt-6 mx-auto w-max rounded-full`), not edge-to-edge sticky bar
- **CTA buttons:** Fully rounded pills (`rounded-full px-6 py-3`). Trailing arrow icons get their own circular wrapper (`w-8 h-8 rounded-full bg-black/5`) nested flush inside the button
- **Eyebrow tags:** Pill-shaped micro-badges above headings (`rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.2em]`)
- **Section spacing:** Double standard — `py-24` to `py-40`. Let the design breathe

### Motion Philosophy — Spring Physics
All motion simulates real-world mass. No linear or default ease-in-out.

```javascript
// GSAP spring equivalent (replaces Framer Motion spring)
gsap.to(element, {
  y: 0, opacity: 1,
  duration: 0.8,
  ease: "elastic.out(1, 0.3)"
});

// Custom cubic-bezier for general transitions
// CSS: transition: all 700ms cubic-bezier(0.32, 0.72, 0, 1);
gsap.to(button, {
  scale: 0.98,
  duration: 0.15,
  ease: "power2.out"
});

// Scroll entry — heavy fade-up with blur
gsap.from(element, {
  y: 64, opacity: 0, filter: "blur(12px)",
  duration: 0.8,
  ease: "cubic-bezier(0.32, 0.72, 0, 1)",
  scrollTrigger: { trigger: element, start: "top 85%" }
});
```

- Buttons: scale `0.98` on press, inner icon translates diagonally on hover
- Cards: lift with color-tinted shadow transition
- Scroll reveals: `translateY(64px)` + blur + opacity over 800ms+, staggered 100ms per element
- Nav hamburger: morphs to X via rotate, menu expands with `backdrop-blur-3xl`, links stagger in

### Anti-Patterns (Soft Mode)
- Symmetrical 3-column Bootstrap grids without whitespace variation
- Edge-to-edge sticky navbars glued to top
- Standard Lucide/FontAwesome thick-stroke icons (use Phosphor Light or Remix Line weight)
- Flat cards without the Double-Bezel nesting
- Default `linear` or `ease-in-out` transitions

---

## 2. Minimalist Mode (Editorial / Workspace)

**Vibe:** Notion meets premium editorial — warm monochrome, typographic hierarchy as the primary design element, invisible motion.

### Palette — Warm Monochrome + Spot Pastels
Color is scarce. Used only for semantic meaning or subtle accents.

| Role | Value |
|------|-------|
| Canvas | `#FFFFFF` or warm bone `#F7F6F3` |
| Surface (cards) | `#FFFFFF` or `#F9F9F8` |
| Borders | Ultra-light `#EAEAEA` or `rgba(0,0,0,0.06)` |
| Body text | Off-black `#2F3437` (never pure `#000`) |
| Muted text | `#787774` |

**Spot pastels (tags, badges, inline code only):**
- Pale red: bg `#FDEBEC`, text `#9F2F2D`
- Pale blue: bg `#E1F3FE`, text `#1F6C9F`
- Pale green: bg `#EDF3EC`, text `#346538`
- Pale yellow: bg `#FBF3DB`, text `#956400`

### Typography — Serif-First Hierarchy
| Role | Fonts | Notes |
|------|-------|-------|
| Display (heroes, quotes) | Newsreader, Instrument Serif, Playfair Display | Tight tracking `-0.02em` to `-0.04em`, line-height `1.1` |
| Body + UI | Switzer, Geist Sans, Plus Jakarta Sans | Line-height `1.6`, `max-w-4xl` or `max-w-5xl` content width |
| Mono (code, metadata) | Geist Mono, JetBrains Mono | For `<kbd>` tags, technical details |

### Surface Treatment — Ultra-Flat
- **Shadows:** Practically non-existent. Max `box-shadow: 0 2px 8px rgba(0,0,0,0.04)` on hover only
- **Borders:** All cards `border: 1px solid #EAEAEA`. This is the primary structural element
- **Border radius:** Crisp `8px` or `12px` max. No `rounded-full` on containers
- **No gradients, no glassmorphism, no 3D effects** (beyond subtle navbar blur)
- **Sections need depth:** Use subtle full-width bg imagery at low opacity, soft radial light spots (`radial-gradient` warm tones at `opacity: 0.03`), or minimal geometric line patterns

### Component Rules
- **Bento grids:** Asymmetric CSS Grid, cards with `border: 1px solid #EAEAEA`, `rounded-lg` (8-12px), generous `p-6` to `p-10`
- **CTA buttons:** Solid `bg-[#111] text-white`, slight radius `rounded-md` (4-6px), no shadow. Hover: shift to `#333` or `scale(0.98)`
- **Tags/badges:** Pill-shaped, `text-xs uppercase tracking-widest`, muted pastel backgrounds
- **Accordions:** No container boxes. Items separated by `border-bottom: 1px solid #EAEAEA` only. Clean `+`/`-` toggle
- **Keystroke UIs:** Physical key look via `<kbd>` — `border: 1px solid #EAEAEA`, `rounded`, `bg-[#F7F6F3]`, mono font

### Motion Philosophy — Invisible
Motion is present but never noticed. Quiet sophistication, not spectacle.

```javascript
// Scroll entry — gentle, barely perceptible
gsap.from(element, {
  y: 12, opacity: 0,
  duration: 0.6,
  ease: "cubic-bezier(0.16, 1, 0.3, 1)",
  scrollTrigger: { trigger: element, start: "top 85%" }
});

// Staggered grid reveals
gsap.from(gridItems, {
  y: 12, opacity: 0,
  duration: 0.5,
  stagger: 0.08,
  ease: "cubic-bezier(0.16, 1, 0.3, 1)",
  scrollTrigger: { trigger: grid, start: "top 80%" }
});
```

- Cards: ultra-subtle shadow shift on hover (from `0 0 0` to `0 2px 8px rgba(0,0,0,0.04)`) over 200ms
- Buttons: `scale(0.98)` on `:active`
- Optional ambient: single slow-moving gradient blob (`duration: 20s+`, `opacity: 0.02-0.04`) on fixed layer
- Entry distance: `translateY(12px)` max — not dramatic, just a whisper

### Anti-Patterns (Minimalist Mode)
- Heavy drop shadows (`shadow-md`, `shadow-lg`)
- Primary-colored backgrounds on large sections
- Gradients, neon colors, 3D glassmorphism
- `rounded-full` on containers or primary buttons
- Emojis in code, markup, headings, or alt text — use icons or SVG
- Oversaturated stock photography

---

## 3. Brutalist Mode (Industrial / Tactical)

**Vibe:** Declassified blueprints meet punk zine. Raw functionality, mechanical precision, zero decoration.

### Visual Path Selection
Pick ONE per project. Do not mix within the same interface.

| Path | When to Use | Key Trait |
|------|-------------|-----------|
| **Swiss Print** | Light mode, editorial, portfolio | Newsprint substrate, heavy sans-serif, red accent |
| **CRT Terminal** | Dark mode, data-heavy, technical | Phosphor green/white on black, monospace-dominant |

### Palette

**Swiss Print (light):**
| Role | Value |
|------|-------|
| Background | `#F4F4F0` or `#EAE8E3` (unbleached paper) |
| Foreground | `#050505` to `#111111` (carbon ink) |
| Accent | `#E61919` or `#FF2A2A` (aviation red — the ONLY accent) |

**CRT Terminal (dark):**
| Role | Value |
|------|-------|
| Background | `#0A0A0A` or `#121212` (deactivated CRT, avoid pure `#000`) |
| Foreground | `#EAEAEA` (white phosphor) |
| Accent | `#E61919` or `#FF2A2A` (same red, same rules) |
| Terminal green | `#4AF626` — optional, ONE element only (status indicator or data readout) |

**Color rules:** No gradients. No soft shadows. No translucency. Colors simulate physical media or primitive emissive displays.

### Typography — Extreme Scale Contrast
| Role | Fonts | Notes |
|------|-------|-------|
| Macro (structural headers) | Archivo Black, Monument Extended, Neue Haas Grotesk | Fluid `clamp(4rem, 10vw, 15rem)`, tracking `-0.03em` to `-0.06em`, line-height `0.85-0.95`, UPPERCASE only |
| Micro (data, telemetry) | JetBrains Mono, IBM Plex Mono, Space Mono | Fixed `10-14px`, tracking `0.05em-0.1em`, UPPERCASE, all metadata/nav |
| Textural (rare, artistic) | Playfair Display, EB Garamond | Sparingly. Subject to halftone/dither post-processing |

### Surface Treatment — Zero Radius, Visible Structure
- **Border radius:** Absolute zero. All corners 90 degrees. `rounded-none` everywhere
- **Borders:** Solid `1px` or `2px`, extensive use to compartmentalize information zones
- **Grid:** Strict CSS Grid. Use `gap: 1px` with contrasting parent/child backgrounds for razor-thin dividers
- **Density:** Oscillates between extreme data density (packed monospace clusters) and vast negative space framing macro type

### Component Rules
- **ASCII framing:** `[ SECTION TITLE ]`, `< LABEL >`, `>>>`, `///` as structural decoration
- **Industrial markers:** `(R)`, `(C)`, `(TM)` as geometric elements, not legal text
- **Technical assets:** Crosshairs `+` at grid intersections, barcode-like vertical lines, warning stripes, random metadata strings (`REV 2.6`, `UNIT / D-01`)
- **Semantic HTML:** Use `<data>`, `<samp>`, `<kbd>`, `<output>`, `<dl>` for technical content
- **No icons** from standard libraries. ASCII symbols or custom SVG only

### Analog Degradation Effects (CSS/SVG)
- **Halftone:** Dot-matrix patterns via SVG radial dot overlay + `mix-blend-mode: multiply`
- **CRT scanlines (terminal path):** `repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)`
- **Mechanical noise:** Global low-opacity SVG noise filter on root element
- **Image treatment:** Convert to 1-bit dithered or halftone. No smooth photography

### Motion Philosophy — Mechanical Precision
Motion is functional, not decorative. Simulates hardware state changes.

```javascript
// Abrupt state reveal — no soft easing
gsap.from(element, {
  y: 20, opacity: 0,
  duration: 0.3,
  ease: "power1.out",
  scrollTrigger: { trigger: element, start: "top 85%" }
});

// Data ticker / telemetry counter
gsap.to(counter, {
  textContent: targetValue,
  duration: 1.5,
  ease: "none",
  snap: { textContent: 1 },
  scrollTrigger: { trigger: counter, start: "top 80%" }
});
```

- Short durations (200-400ms). No lingering spring physics
- Stagger delays for data rows, not decorative cards
- Optional: CRT flicker effect (`opacity` oscillation at 30fps) on terminal path elements

### Anti-Patterns (Brutalist Mode)
- Any `border-radius` above 0
- Soft shadows, glassmorphism, gradients
- Smooth photography without degradation processing
- Decorative motion (springs, bounces, parallax)
- Standard icon libraries (Lucide, Heroicons, FontAwesome)
- More than one accent color

---

## Integration with Taste Parameters

Aesthetic modes **set strong defaults** for the taste parameters. Users can override, but these are the starting points:

| Parameter | Soft | Minimalist | Brutalist |
|-----------|------|------------|-----------|
| DESIGN_VARIANCE | 7-9 | 4-6 | 6-8 |
| MOTION_INTENSITY | 7-9 | 2-4 | 3-5 |
| VISUAL_DENSITY | 4-6 | 3-5 | 6-9 |

## Integration with Presets

Aesthetic modes and cinematic presets (`cinematic-presets.md`) are complementary. A mode defines the design philosophy; a preset provides specific color/font/mood tokens. You can use both:
- Soft Mode + Midnight Luxe preset = dark luxury agency
- Minimalist Mode + Organic Tech preset = warm editorial workspace
- Brutalist Mode + Brutalist Signal preset = Swiss print with specific palette

Or use a mode alone with its built-in palette recommendations.
