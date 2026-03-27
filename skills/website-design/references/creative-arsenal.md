## Graph Links
- **Parent skill:** [[website-design]]
- **Sibling references:** [[aesthetic-guidelines]], [[cinematic-presets]], [[scroll-driven-design]]
- **Related skills:** [[page-cro]]

# Creative Arsenal — Premium Interaction Patterns

30+ interaction patterns for HTML + Tailwind CSS + GSAP builds. Each pattern includes: name, description, difficulty tag, recommended MOTION_INTENSITY range, and implementation approach.

> **Stack constraint:** All patterns use vanilla HTML + Tailwind CSS + GSAP via CDN only. No React, no Framer Motion, no build tools.

---

## Navigation (6 patterns)

### 1. Floating Pill Nav
Compact nav that detaches from top, becomes a floating pill on scroll with glassmorphism.
- **Difficulty:** CSS + JS
- **MOTION_INTENSITY:** 3+
- **Approach:** Start with `w-full` nav. On scroll past 80px, GSAP morphs to `max-w-fit mx-auto rounded-full px-6 backdrop-blur-2xl bg-white/80 shadow-lg` with a spring ease. Use `position: sticky` + `top: 1rem`.
```html
<nav id="pill-nav" class="sticky top-0 z-50 w-full transition-none">
  <div class="mx-auto flex items-center justify-between px-6 py-3">
    <!-- logo + links + CTA -->
  </div>
</nav>
<script>
gsap.to("#pill-nav", {
  scrollTrigger: { trigger: "body", start: "80px top", toggleActions: "play none none reverse" },
  maxWidth: "720px", marginInline: "auto", borderRadius: "9999px",
  backdropFilter: "blur(24px)", backgroundColor: "rgba(255,255,255,0.85)",
  boxShadow: "0 4px 30px rgba(0,0,0,0.08)", top: "1rem",
  duration: 0.5, ease: "power3.out"
});
</script>
```

### 2. Magnetic Button Hover
Buttons subtly follow the cursor within a proximity radius, like they're attracted to it.
- **Difficulty:** CSS + JS
- **MOTION_INTENSITY:** 5+
- **Approach:** Track mouse position relative to button center. Apply small `transform: translate()` toward cursor. Reset on mouse leave with spring ease.
```html
<script>
document.querySelectorAll('.magnetic-btn').forEach(btn => {
  btn.addEventListener('mousemove', (e) => {
    const rect = btn.getBoundingClientRect();
    const x = (e.clientX - rect.left - rect.width / 2) * 0.3;
    const y = (e.clientY - rect.top - rect.height / 2) * 0.3;
    gsap.to(btn, { x, y, duration: 0.3, ease: "power2.out" });
  });
  btn.addEventListener('mouseleave', () => {
    gsap.to(btn, { x: 0, y: 0, duration: 0.5, ease: "elastic.out(1, 0.3)" });
  });
});
</script>
```

### 3. Mega Menu Reveal
Full-width dropdown that slides/fades down with staggered content columns.
- **Difficulty:** CSS + JS
- **MOTION_INTENSITY:** 3+
- **Approach:** Hidden `div` below nav with `opacity: 0; clipPath: inset(0 0 100% 0)`. On trigger, GSAP animates clipPath to `inset(0)` + staggers child columns.

### 4. Dynamic Island Status
Pill-shaped status bar (like Apple Dynamic Island) that morphs to show notifications, loading states, or CTAs.
- **Difficulty:** GSAP
- **MOTION_INTENSITY:** 6+
- **Approach:** Fixed pill at top center. GSAP morphs width/height/border-radius between compact (dot) → expanded (message) → collapsed states. Use `gsap.timeline()` with labels.

### 5. Contextual Radial Menu
Circular menu that radiates outward from a trigger point (floating action button).
- **Difficulty:** CSS + JS
- **MOTION_INTENSITY:** 5+
- **Approach:** Items positioned absolutely, initially stacked at center with `scale: 0; opacity: 0`. On click, GSAP staggers each item to its final position using `rotation` + `transformOrigin` math.

### 6. Scroll-Aware Progress Nav
Side or top nav where items highlight as their corresponding section enters viewport.
- **Difficulty:** CSS + JS
- **MOTION_INTENSITY:** 2+
- **Approach:** ScrollTrigger on each section updates active class on nav items. Optional: animated underline or dot indicator slides to active position via GSAP.

---

## Layout (6 patterns)

### 7. Asymmetric Bento Grid
Unequal grid cells — one large hero cell, medium supporting cells, small accent cells. Not a uniform grid.
- **Difficulty:** CSS-only
- **MOTION_INTENSITY:** 1+ (layout only)
- **Approach:** CSS Grid with named areas or `grid-template-columns: 2fr 1fr 1fr` + `grid-row: span 2` on the hero cell. Vary `rounded-2xl` to `rounded-3xl` per cell size.
```html
<div class="grid grid-cols-3 grid-rows-2 gap-4">
  <div class="col-span-2 row-span-2 rounded-3xl bg-slate-100 p-8"><!-- Hero cell --></div>
  <div class="rounded-2xl bg-slate-50 p-6"><!-- Small cell --></div>
  <div class="rounded-2xl bg-slate-50 p-6"><!-- Small cell --></div>
</div>
```

### 8. Split-Screen Scroll
Two columns that scroll independently — left stays fixed while right scrolls, then they swap.
- **Difficulty:** GSAP
- **MOTION_INTENSITY:** 5+
- **Approach:** Left column pinned via ScrollTrigger `pin: true`. Right column scrolls normally. Unpin left and pin right at the transition point.

### 9. Curtain Reveal
Sections stack on top of each other; scrolling peels back the current section to reveal the next one underneath, like turning pages.
- **Difficulty:** GSAP
- **MOTION_INTENSITY:** 6+
- **Approach:** Each section is `position: sticky; top: 0`. ScrollTrigger scales the current section down and reduces opacity as the next section's trigger enters.
```javascript
sections.forEach((section, i) => {
  if (i < sections.length - 1) {
    gsap.to(section, {
      scale: 0.9, opacity: 0.3, borderRadius: "2rem",
      scrollTrigger: { trigger: sections[i + 1], start: "top bottom", end: "top top", scrub: true }
    });
  }
});
```

### 10. Z-Axis Card Cascade
Cards stacked on the z-axis (like a deck) that fan out as user scrolls into view.
- **Difficulty:** GSAP
- **MOTION_INTENSITY:** 6+
- **Approach:** Cards start stacked with increasing `translateZ` and slight rotation. ScrollTrigger fans them into a grid layout.

### 11. Masonry Flow
Pinterest-style variable-height columns that pack efficiently.
- **Difficulty:** CSS-only
- **MOTION_INTENSITY:** 1+
- **Approach:** `columns: 3; column-gap: 1.5rem` on container. Items get `break-inside: avoid; margin-bottom: 1.5rem`. Add GSAP stagger reveals for MOTION_INTENSITY 4+.

### 12. Overlapping Section Layers
Sections that overlap by 40-80px, creating depth via shadows and z-index stacking.
- **Difficulty:** CSS-only
- **MOTION_INTENSITY:** 1+
- **Approach:** Negative margins (`-mt-16`) + `relative z-{n}` on sections. Higher sections cast shadows on lower ones. Combine with rounded top corners (`rounded-t-3xl`) for a card-stack feel.

---

## Cards & Surfaces (6 patterns)

### 13. Parallax Tilt Card
Cards that tilt in 3D following cursor position, with a light reflection effect.
- **Difficulty:** CSS + JS
- **MOTION_INTENSITY:** 5+
- **Approach:** Track mouse on card, calculate rotation angle (max ±15deg). Apply `transform: perspective(1000px) rotateX() rotateY()`. Add a pseudo-element `::before` with radial gradient that follows cursor for the shine effect.
```javascript
card.addEventListener('mousemove', (e) => {
  const rect = card.getBoundingClientRect();
  const x = (e.clientX - rect.left) / rect.width - 0.5;
  const y = (e.clientY - rect.top) / rect.height - 0.5;
  gsap.to(card, {
    rotateY: x * 15, rotateX: y * -15,
    duration: 0.4, ease: "power2.out"
  });
});
```

### 14. Spotlight Border
Card border that glows/highlights only near the cursor position, like a flashlight sweeping across the edge.
- **Difficulty:** CSS + JS
- **MOTION_INTENSITY:** 4+
- **Approach:** Card has `border: 1px solid transparent`. A CSS `radial-gradient` on `border-image` follows cursor position via CSS custom properties `--x` and `--y` updated by JS.
```css
.spotlight-card {
  border: 1px solid transparent;
  background: linear-gradient(var(--bg), var(--bg)) padding-box,
              radial-gradient(circle 120px at var(--x) var(--y), rgba(255,255,255,0.4), transparent) border-box;
}
```

### 15. Double-Bezel Card
Card with an inset border creating a picture-frame depth effect — border outside + inner shadow.
- **Difficulty:** CSS-only
- **MOTION_INTENSITY:** 1+
- **Approach:** Outer card with border + `ring-1 ring-inset ring-white/10`. Inner content area with `shadow-inner`. Creates a "glass in a frame" look.

### 16. Holographic Foil
Iridescent gradient that shifts based on cursor position, mimicking a holographic trading card.
- **Difficulty:** CSS + JS
- **MOTION_INTENSITY:** 5+
- **Approach:** Multi-stop `background: linear-gradient()` with high saturation hues. Rotate the gradient angle based on cursor position. Overlay with noise texture for realism.

### 17. Glassmorphism with Inner Refraction
Enhanced glassmorphism with colored inner borders that simulate light refraction at glass edges.
- **Difficulty:** CSS-only
- **MOTION_INTENSITY:** 1+
- **Approach:** `backdrop-blur-2xl bg-white/10` + `shadow-[inset_0_0_0_1px_rgba(255,255,255,0.15)]` + a subtle inner gradient from transparent to white/5 at the top edge.

### 18. Floating Depth Card
Card that appears to float above the page with multi-layer shadows that shift on hover.
- **Difficulty:** CSS-only
- **MOTION_INTENSITY:** 2+
- **Approach:** Three shadow layers: close (4px, 0.04), medium (16px, 0.06), far (40px, 0.08). On hover, increase y-offset and blur of the far shadow. Tint shadows to the card's accent color.
```css
.float-card {
  box-shadow: 0 2px 4px rgba(0,0,0,0.04), 0 8px 16px rgba(0,0,0,0.06), 0 20px 40px rgba(0,0,0,0.08);
  transition: box-shadow 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.float-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.04), 0 16px 32px rgba(0,0,0,0.08), 0 32px 64px rgba(0,0,0,0.12);
}
```

---

## Scroll Animations (6 patterns)

### 19. Sticky Scroll Stack
Sections pin to the top and stack, each one covering the previous as user scrolls through a set.
- **Difficulty:** GSAP
- **MOTION_INTENSITY:** 5+
- **Approach:** Each section is `position: sticky; top: 0` with increasing z-index. ScrollTrigger adds subtle scale-down and shadow to covered sections. Works brilliantly for feature showcases.
```javascript
panels.forEach((panel, i) => {
  ScrollTrigger.create({
    trigger: panel, start: "top top", pin: true, pinSpacing: false
  });
  if (i > 0) {
    gsap.from(panel, {
      opacity: 0, scale: 0.95,
      scrollTrigger: { trigger: panel, start: "top bottom", end: "top top", scrub: true }
    });
  }
});
```

### 20. Horizontal Scroll Section
One section hijacks vertical scroll to scroll horizontally through a gallery or feature showcase.
- **Difficulty:** GSAP
- **MOTION_INTENSITY:** 6+
- **Approach:** Container pinned with ScrollTrigger. Inner track translated on x-axis based on scroll progress. Total scroll distance = track width - viewport width.
```javascript
const track = document.querySelector(".h-track");
gsap.to(track, {
  x: () => -(track.scrollWidth - window.innerWidth),
  ease: "none",
  scrollTrigger: {
    trigger: ".h-section", pin: true, scrub: 1,
    end: () => "+=" + (track.scrollWidth - window.innerWidth)
  }
});
```

### 21. Zoom Parallax
Elements at different depths zoom at different rates on scroll, creating a parallax depth field.
- **Difficulty:** GSAP
- **MOTION_INTENSITY:** 7+
- **Approach:** Layered elements with different `data-speed` attributes. ScrollTrigger drives `scale` and `y` at varying rates. Background layer barely moves, foreground zooms dramatically.

### 22. Scroll Progress Indicator
Fixed progress bar (top or side) that fills as the user scrolls through the page.
- **Difficulty:** CSS + JS
- **MOTION_INTENSITY:** 2+
- **Approach:** Fixed `div` at top, `width` or `scaleX` driven by scroll percentage. Can use pure CSS `animation-timeline: scroll()` in modern browsers, or GSAP ScrollTrigger for wider support.

### 23. Text Line Reveal
Text appears line by line, word by word, or character by character as it enters the viewport.
- **Difficulty:** GSAP
- **MOTION_INTENSITY:** 4+
- **Approach:** Split text into `<span>` per word/line. Each span starts at `opacity: 0; y: 20px`. ScrollTrigger staggers them in with `stagger: 0.05`.

### 24. Liquid Swipe Transition
Sections transition with a curved/wave clip-path that sweeps across, like liquid flowing.
- **Difficulty:** GSAP
- **MOTION_INTENSITY:** 7+
- **Approach:** Animated `clip-path: polygon()` or `clip-path: ellipse()` with GSAP. Start at one corner, expand to full viewport. Coordinate with section background color for smooth blending.

---

## Typography (5 patterns)

### 25. Kinetic Marquee
Infinite-scrolling text strip, like a stock ticker, for social proof or brand messaging.
- **Difficulty:** CSS-only
- **MOTION_INTENSITY:** 3+
- **Approach:** Duplicate text content in a flex row. CSS `@keyframes` translates the entire row by -50%. `animation: marquee 20s linear infinite`. Reverse direction on alternate rows.
```html
<div class="overflow-hidden">
  <div class="flex animate-marquee whitespace-nowrap">
    <span class="mx-8 text-6xl font-bold opacity-20">BRAND NAME</span>
    <!-- repeat 8+ times -->
  </div>
</div>
<style>
@keyframes marquee { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.animate-marquee { animation: marquee 30s linear infinite; }
</style>
```

### 26. Text Mask Reveal
Large text revealed through a clip/mask as the user scrolls, like wiping fog from glass.
- **Difficulty:** GSAP
- **MOTION_INTENSITY:** 5+
- **Approach:** Text has a gradient mask (`-webkit-mask-image`) that moves from left to right on scroll. Or use `clip-path: inset(0 100% 0 0)` animated to `inset(0)`.

### 27. Text Scramble Effect
Characters scramble randomly before settling into the final text, like a cipher decoding.
- **Difficulty:** JS
- **MOTION_INTENSITY:** 5+
- **Approach:** Replace each character with random chars at 30ms intervals, progressively locking in the correct character from left to right. Good for hero headlines on page load.

### 28. Gradient Stroke Animation
Text with animated gradient outline (no fill), where the gradient rotates or shifts over time.
- **Difficulty:** CSS-only
- **MOTION_INTENSITY:** 3+
- **Approach:** `-webkit-text-stroke: 2px transparent` + `background: linear-gradient()` + `background-clip: text` + CSS animation rotating the gradient angle.

### 29. Split Heading Entrance
Heading splits into two halves (top/bottom or left/right) that slide apart from center on scroll entry.
- **Difficulty:** GSAP
- **MOTION_INTENSITY:** 5+
- **Approach:** Duplicate heading in two containers with `overflow: hidden`. First shows top half (clip bottom), second shows bottom half (clip top). GSAP animates them from offset to aligned position.

---

## Micro-Interactions (5 patterns)

### 30. Particle Button
Button that emits particles (dots, confetti, sparkles) on click.
- **Difficulty:** JS
- **MOTION_INTENSITY:** 5+
- **Approach:** On click, create 12-20 absolutely-positioned small circles. GSAP animates each with random angle, distance, opacity fade, and scale. Remove from DOM after animation.

### 31. Directional Hover Fill
Button/card background fills from the direction the cursor enters.
- **Difficulty:** CSS + JS
- **MOTION_INTENSITY:** 4+
- **Approach:** Detect entry edge (top/right/bottom/left) on `mouseenter`. Set `::before` pseudo-element's `transform-origin` to that edge. Animate `scaleX` or `scaleY` from 0 to 1.

### 32. Ripple Click
Material Design-style ripple that emanates from the click point.
- **Difficulty:** CSS + JS
- **MOTION_INTENSITY:** 3+
- **Approach:** On click, create a circle `div` at click coordinates inside the button. Animate `scale` from 0 to 2.5 + `opacity` from 0.4 to 0. Remove after 600ms.

### 33. Animated SVG Line Draw
SVG illustrations that draw themselves on scroll entry.
- **Difficulty:** CSS + JS
- **MOTION_INTENSITY:** 4+
- **Approach:** Set `stroke-dasharray` and `stroke-dashoffset` to the path's total length. On scroll entry, animate `stroke-dashoffset` to 0 with GSAP. Pair with a fill fade-in after the stroke completes.

### 34. Mesh Gradient Background
Animated multi-point gradient that slowly shifts colors, creating an organic living background.
- **Difficulty:** CSS-only
- **MOTION_INTENSITY:** 2+
- **Approach:** Multiple overlapping `radial-gradient` layers with CSS `@keyframes` that shift `background-position` slowly (60-120s cycle). Subtle — the movement should be barely perceptible.
```css
.mesh-bg {
  background:
    radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3), transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 115, 0.3), transparent 50%),
    radial-gradient(circle at 40% 80%, rgba(78, 205, 196, 0.2), transparent 50%);
  animation: mesh-shift 60s ease-in-out infinite alternate;
}
@keyframes mesh-shift {
  0% { background-position: 0% 0%, 100% 0%, 0% 100%; }
  100% { background-position: 100% 100%, 0% 100%, 100% 0%; }
}
```

---

## Pattern Selection Guide

### By MOTION_INTENSITY Level

| Level | Recommended Patterns |
|-------|---------------------|
| 1-3 | Scroll Progress (#22), Kinetic Marquee (#25), Gradient Stroke (#28), Mesh Gradient (#34), Floating Depth Card (#18), Double-Bezel (#15), Glassmorphism (#17), Masonry (#11), Overlapping Sections (#12) |
| 4-6 | Magnetic Button (#2), Spotlight Border (#14), Parallax Tilt (#13), Text Line Reveal (#23), Directional Hover (#31), Ripple Click (#32), SVG Line Draw (#33), Split-Screen Scroll (#8), Floating Pill Nav (#1), Sticky Scroll Stack (#19) |
| 7-10 | Horizontal Scroll (#20), Curtain Reveal (#9), Z-Axis Cascade (#10), Zoom Parallax (#21), Liquid Swipe (#24), Text Scramble (#27), Dynamic Island (#4), Holographic Foil (#16), Particle Button (#30) |

### By Use Case

| Use Case | Best Patterns |
|----------|--------------|
| SaaS landing page | Floating Pill Nav, Sticky Scroll Stack, Text Line Reveal, Floating Depth Cards |
| Portfolio / Agency | Parallax Tilt Cards, Horizontal Scroll, Curtain Reveal, Kinetic Marquee |
| E-commerce / Product | Holographic Foil, Spotlight Border, Directional Hover, Asymmetric Bento |
| Dashboard / App marketing | Glassmorphism, Double-Bezel, Dynamic Island, Split-Screen Scroll |
| Editorial / Magazine | Text Mask Reveal, Split Heading, Overlapping Sections, Masonry Flow |
