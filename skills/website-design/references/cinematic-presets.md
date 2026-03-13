# Cinematic Landing Page Presets

Adapted from Nick Sareav's cinematic landing page framework. These presets define complete aesthetic systems for premium landing pages built with Tailwind CSS + GSAP 3.

> **Note:** Verify font choices against `aesthetic-guidelines.md` anti-generic guardrails before using. Avoid converging on the same preset across builds.

---

## 4 Aesthetic Presets

### 1. Organic Tech
**Vibe:** Apple meets Notion — warm, approachable, premium but not cold
```json
{
  "palette": {
    "bg": "#FAF8F5",
    "surface": "#FFFFFF",
    "text": "#1A1A1A",
    "muted": "#6B6B6B",
    "accent": "#E85D3A",
    "accentHover": "#D14E2D",
    "border": "#E8E4DF"
  },
  "typography": {
    "heading": "DM Serif Display",
    "body": "Figtree",
    "mono": "JetBrains Mono"
  },
  "imageMood": "soft natural lighting, warm earth tones, editorial photography, organic textures",
  "identity": "Elegant simplicity. Think a ceramics studio that happens to build software."
}
```

### 2. Midnight Luxe
**Vibe:** Dark mode luxury — Vercel meets premium finance
```json
{
  "palette": {
    "bg": "#0A0A0A",
    "surface": "#141414",
    "text": "#FAFAFA",
    "muted": "#888888",
    "accent": "#6C5CE7",
    "accentHover": "#5A4BD5",
    "border": "#2A2A2A"
  },
  "typography": {
    "heading": "Syne",
    "body": "General Sans",
    "mono": "Fira Code"
  },
  "imageMood": "dark moody lighting, neon accents, cinematic depth, high contrast",
  "identity": "Power and precision. Like a control room at mission control."
}
```

### 3. Brutalist Signal
**Vibe:** Bold, raw, high-contrast — Linear meets punk zine
```json
{
  "palette": {
    "bg": "#F5F5F0",
    "surface": "#FFFFFF",
    "text": "#000000",
    "muted": "#555555",
    "accent": "#FF3B00",
    "accentHover": "#E03500",
    "border": "#000000"
  },
  "typography": {
    "heading": "Instrument Serif",
    "body": "IBM Plex Sans",
    "mono": "IBM Plex Mono"
  },
  "imageMood": "high contrast black and white, bold typography as image, raw textures, grain",
  "identity": "No BS. Confident and loud. The brand that doesn't whisper."
}
```

### 4. Vapor Clinic
**Vibe:** Clinical futurism — healthcare tech meets sci-fi
```json
{
  "palette": {
    "bg": "#F0F4F8",
    "surface": "#FFFFFF",
    "text": "#1E293B",
    "muted": "#64748B",
    "accent": "#0EA5E9",
    "accentHover": "#0284C7",
    "border": "#CBD5E1"
  },
  "typography": {
    "heading": "Plus Jakarta Sans",
    "body": "Outfit",
    "mono": "JetBrains Mono"
  },
  "imageMood": "clean clinical lighting, cool blue tones, minimal, floating UI elements",
  "identity": "Trust and clarity. A doctor's precision with a designer's eye."
}
```

---

## Fixed Design System Rules (All Presets)

These rules apply regardless of which preset is chosen:

### Visual Texture
- **Noise overlay:** Subtle grain texture via CSS `background-image` (0.02 opacity)
- **Rounded corners:** `rounded-2xl` (16px) for cards, `rounded-full` for buttons
- **Shadows:** Layered soft shadows — `shadow-sm` + `shadow-lg` for depth
- **Glassmorphism:** For overlays — `backdrop-blur-xl bg-white/80`

### Micro-Interactions
- **Buttons:** Scale 1.02 on hover, 0.98 on press (`transition-transform`)
- **Cards:** Subtle lift + border glow on hover
- **Links:** Color transition 200ms, underline slide-in
- **Scroll reveals:** Fade-up with 30px translate, staggered 100ms per element

### GSAP Animation Lifecycle
```javascript
// Standard scroll-triggered entrance
gsap.from(element, {
  y: 30,
  opacity: 0,
  duration: 0.8,
  ease: "power2.out",
  scrollTrigger: {
    trigger: element,
    start: "top 85%",
    toggleActions: "play none none none",
  }
});

// Staggered children
gsap.from(children, {
  y: 20,
  opacity: 0,
  duration: 0.6,
  stagger: 0.1,
  ease: "power2.out",
  scrollTrigger: { trigger: parent, start: "top 80%" }
});

// Hero entrance (page load)
const tl = gsap.timeline();
tl.from(".hero-title", { y: 40, opacity: 0, duration: 1, ease: "power3.out" })
  .from(".hero-subtitle", { y: 20, opacity: 0, duration: 0.8 }, "-=0.5")
  .from(".hero-cta", { y: 20, opacity: 0, duration: 0.6 }, "-=0.4");
```

---

## 7 Component Architecture

Every cinematic landing page uses these 7 sections in order:

### 1. Navbar
- Logo left, nav links center, CTA button right
- Sticky with glassmorphism on scroll
- Mobile: hamburger → full-screen overlay menu
- GSAP: fade-in on load, background blur on scroll past 50px

### 2. Hero
- Full viewport height (100vh or min-h-screen)
- Large heading (text-5xl md:text-7xl), subheading, primary CTA
- Optional: floating UI mockup, background gradient, or video
- GSAP: staggered entrance — title → subtitle → CTA → visual

### 3. Features
- 3-column grid (md:grid-cols-3)
- Each card: icon/emoji + title + description
- Bento grid variant for premium feel (asymmetric sizes)
- GSAP: staggered card entrance on scroll

### 4. Philosophy / "Why Us"
- Full-width split: text left, visual right (or vice versa)
- Large quote or mission statement
- Counter stats (e.g., "10K+ users", "99.9% uptime")
- GSAP: parallax scroll on the visual, text fade-in

### 5. Protocol / "How It Works"
- 3-step process: numbered cards or timeline
- Each step: number + title + description + optional visual
- Horizontal on desktop, vertical on mobile
- GSAP: sequential step reveals

### 6. Pricing
- 2-3 tier cards, one highlighted as "Popular"
- Each card: plan name, price, feature list, CTA button
- Toggle for monthly/annual pricing
- GSAP: cards slide up on scroll

### 7. Footer
- Logo + tagline, nav columns, social links, legal links
- Newsletter signup (optional)
- Dark variant by default regardless of preset
- GSAP: subtle fade-in

---

## Technical Stack

Default (single-file builds):
```
Tailwind CSS      — via CDN (<script src="https://cdn.tailwindcss.com"></script>)
GSAP 3            — via CDN (ScrollTrigger animations)
Google Fonts      — Typography (loaded via <link>)
Heroicons/SVG     — Icons (inline or CDN)
```

For complex multi-page builds (user must request):
```
React 19 / Next.js — Component framework
Tailwind CSS 3.4   — Utility-first styling
GSAP 3             — ScrollTrigger animations
Lucide React       — Icon library
```

### Build Sequence
1. Set up preset tokens (colors, fonts) in Tailwind config or `<style>` block
2. Load Google Fonts in `<head>`
3. Build components top-to-bottom: Navbar → Hero → Features → Philosophy → Protocol → Pricing → Footer
4. Add GSAP animations after layout is solid
5. Add noise overlay and micro-interactions last
6. Mobile responsive pass
7. Screenshot verification loop

### Noise Overlay CSS
```css
.noise-overlay::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.02;
  pointer-events: none;
  z-index: 50;
}
```
