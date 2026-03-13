# Scroll-Driven Website Design Guidelines

For cinematic, scroll-driven animated websites. Load this reference when building scroll-heavy or animation-rich pages.

---

## Typography as Design

Text hierarchy replaces card containers. Size, weight, and color ARE the structure.

| Element | Size | Weight | Line-Height | Notes |
|---------|------|--------|-------------|-------|
| Hero headings | **6rem minimum** | 700-800 | 0.9-1.0 (tight) | Impact through scale |
| Section headings | **3rem minimum** | 600-700 | 1.0-1.1 | Confident, bold |
| Horizontal marquee | **10-15vw** | 700+ | 1.0 | Uppercase, letterspaced |
| Section labels | 0.7rem | 400-500 | 1.2 | Uppercase, letterspaced (0.15em+), muted — like "001 / Features" |
| Body text | 1-1.125rem | 400 | 1.6-1.7 | Readable, generous spacing |

---

## No Cards, No Boxes

On scroll-driven sites, avoid containers around text:

- **NEVER** use glassmorphism cards, frosted glass, or visible containers around text
- Text sits directly on the background — clean, confident, editorial
- Readability comes from: font weight (600+), text-shadow if needed, clean backgrounds at text scroll points
- The only acceptable "container" is generous padding on the section itself

---

## Color Zones

Background color must shift between sections to create visual rhythm:

```css
:root {
  --bg-light: #FAF8F5;
  --bg-dark: #0A0A0A;
  --bg-accent: #1A1A2E;
  --text-on-light: #1A1A1A;
  --text-on-dark: #FAFAFA;
}
```

- Background transitions: light → dark → accent → light (minimum 3 zone changes)
- Text color inverts automatically per zone
- Transitions happen via GSAP ScrollTrigger, not CSS transitions
- Each zone should feel like entering a new "room"

---

## Layout Variety

Every scroll-driven page needs at least **3 different layout patterns** from:

1. **Centered** — hero sections, CTAs, statements
2. **Left-aligned** — feature descriptions with product visual on right
3. **Right-aligned** — alternate features (mirror of #2)
4. **Full-width** — horizontal marquee text, stats rows, image bleeds
5. **Split** — text on one side, supporting visual on the other

**Rule:** Never use the same layout for consecutive sections.

---

## Animation Choreography

### Entrance Animations (vary per section)
- Fade-up (translateY + opacity)
- Slide-left / Slide-right (translateX + opacity)
- Scale-up (scale 0.95 → 1 + opacity)
- Clip-path reveal (inset or circle)
- Rotate-in (subtle, 2-5deg)

**Rule:** Every section must use a DIFFERENT entrance animation from its neighbor.

### Stagger Rules
- Elements within a section: stagger 0.08-0.12s between items
- Entrance sequence: label first → heading → body text → CTA/button
- Children of a group (e.g., feature cards): stagger 0.1s

### Required Animation Features
- At least **one section must pin** (stay fixed) while its contents animate internally
- At least **one oversized text element** must move horizontally on scroll
- Hero should have a staggered timeline entrance (title → subtitle → CTA → visual)

### GSAP Patterns
```javascript
// Pinned section with internal animation
ScrollTrigger.create({
  trigger: ".pinned-section",
  start: "top top",
  end: "+=200%",
  pin: true,
  scrub: 1
});

// Horizontal text scroll
gsap.to(".marquee-text", {
  xPercent: -50,
  ease: "none",
  scrollTrigger: {
    trigger: ".marquee-section",
    start: "top bottom",
    end: "bottom top",
    scrub: 0.5
  }
});

// Color zone transition
ScrollTrigger.create({
  trigger: ".dark-section",
  start: "top 80%",
  end: "top 20%",
  onEnter: () => gsap.to("body", { backgroundColor: "#0A0A0A", color: "#FAFAFA", duration: 0.6 }),
  onLeaveBack: () => gsap.to("body", { backgroundColor: "#FAF8F5", color: "#1A1A1A", duration: 0.6 })
});
```

---

## Stats & Numbers

When displaying metrics, stats, or social proof numbers:

- Font size: **4rem+** (make them impossible to miss)
- Numbers MUST count up via GSAP (never appear statically)
- Suffix element (x, M, %, etc.) at a smaller size, slightly offset
- Labels below in small caps or uppercase muted text

```javascript
// Count-up animation
gsap.from(".stat-number", {
  textContent: 0,
  duration: 2,
  ease: "power1.out",
  snap: { textContent: 1 },
  scrollTrigger: {
    trigger: ".stats-section",
    start: "top 80%"
  }
});
```

---

## Performance Notes

- Load GSAP + ScrollTrigger via CDN (not bundled)
- Use `will-change: transform` on animated elements
- Debounce scroll handlers
- Test on mobile — reduce animation complexity if needed (prefer `prefers-reduced-motion` media query)
- Keep total DOM elements reasonable — scroll-driven sites can get heavy
