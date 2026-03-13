---
name: website-design
version: "4.0.0"
brand: AgentKits Marketing by AityTech
category: content
difficulty: intermediate
description: "Dual-mode website skill: Recreation (match reference screenshots pixel-perfect) OR Creation (build distinctive interfaces from scratch with bold aesthetics). Single index.html with Tailwind CDN. Automated screenshot comparison loops. Anti-generic guardrails."
triggers:
  - website design
  - build website
  - create website
  - design website
  - landing page design
  - website from screenshot
  - clone design
  - replicate website
  - web design
  - website redesign
  - HTML website
  - recreate website
  - match this design
  - pixel perfect
  - design from scratch
  - build landing page
  - cinematic website
  - distinctive website
  - bold design
  - creative landing page
  - scroll-driven website
  - animated website
prerequisites: []
related_skills:
  - page-cro
  - copywriting
  - image-generation
  - brand-building
  - schema-markup
agents:
  - copywriter
  - brand-voice-guardian
  - conversion-optimizer
  - tracking-specialist
mcp_integrations:
  optional:
    - google-analytics
    - firecrawl
success_metrics:
  - design_match_percentage
  - mobile_responsive
  - page_load_speed
  - conversion_elements_present
  - aesthetic_distinctiveness
output_schema: website-build
---

# Website Design v4.0 — Dual Mode (Recreate + Create)

Two modes, one skill. Recreate pixel-perfect from references OR create distinctive designs from scratch.

---

## Mode Router

Detect mode automatically from user input:

| Signal | Mode | Workflow |
|--------|------|----------|
| User provides reference screenshot/URL | **A: Recreation** | Match reference exactly |
| User describes what to build (no reference) | **B: Creation** | Design from scratch with bold aesthetics |
| Reference + "make it better" / "redesign" | **C: Hybrid** | Recreate structure, apply creation aesthetics |

---

## Shared Foundation (All Modes)

### Tools

#### browser-tools.py (Primary)
```bash
# Screenshot any URL
python3 skills/website-design/scripts/browser-tools.py screenshot <url> <output> [--full-page] [--mobile] [--width N]

# Side-by-side comparison image
python3 skills/website-design/scripts/browser-tools.py compare <reference> <build> <output>

# Local server for build screenshots
python3 skills/website-design/scripts/browser-tools.py serve <html_dir> [--port 8765]

# Analyze screenshot with Gemini vision → structured design tokens
python3 skills/website-design/scripts/browser-tools.py design-analyze <screenshot> [--output json|markdown] [--focus full|layout|colors|typography|sections] [--model MODEL]
```

#### Fallback Chain
If browser-tools.py fails → Firecrawl MCP → WebFetch → crawl4ai. Switch automatically, don't ask user.

### Technical Defaults (All Modes)

- **CSS framework:** Tailwind CSS via CDN — `<script src="https://cdn.tailwindcss.com"></script>`
- **Placeholder images:** `https://placehold.co/` (e.g., `https://placehold.co/600x400`)
- **Responsive:** Mobile-first responsive design
- **Output:** Single `index.html` unless user requests otherwise
- **Icons:** Inline SVGs or Heroicons via CDN
- **Fonts:** Google Fonts via `<link>` tag
- **Animations:** GSAP via CDN for scroll-driven/cinematic builds

### Screenshot & Comparison Loop (All Modes)

1. Serve the HTML: `browser-tools.py serve ./build`
2. Screenshot: `browser-tools.py screenshot http://127.0.0.1:8765 /tmp/build.png --full-page`
3. View and review the screenshot
4. **Minimum 2 rounds required** — always do at least 2 screenshot passes
5. Kill the serve process when done

### Anti-Generic Guardrails (All Modes)

These apply to **every** build, recreation or creation. See `references/aesthetic-guidelines.md` for full details.

- **BANNED fonts:** Inter, Roboto, Arial, system fonts as primary choice
- **BANNED colors:** Default Tailwind palette (indigo-500, blue-600, etc.) as primary brand color
- **BANNED patterns:** Purple gradients on white, `transition-all`, flat `shadow-md`
- **REQUIRED:** Paired fonts (display + body), layered color-tinted shadows, hover/focus/active states on all clickables, intentional spacing tokens

> Exception for Recreation mode: If the reference *uses* a banned pattern, match it anyway — recreation accuracy overrides guardrails.

### References (load on demand)
- `references/browser-automation.md` — Playwright patterns, troubleshooting
- `references/aesthetic-guidelines.md` — Full anti-generic rules, banned/required patterns
- `references/scroll-driven-design.md` — Typography-as-design, color zones, animation choreography
- `references/cinematic-presets.md` — 4 aesthetic preset systems
- `references/component-sources.md` — Component libraries
- `references/gallery-sources.md` — Design inspiration galleries

---

## Mode A: Recreation

When the user provides a reference image (screenshot) and optionally CSS classes or style notes.

**Philosophy:** Match the reference exactly — don't improve it, don't add to it.

### Step 1: Analyze Reference
- Run `design-analyze` on the reference screenshot to extract design tokens (colors, typography, layout, sections)
- If no Gemini API key, Claude analyzes the screenshot visually
- Note exact colors (hex), font sizes, spacing, layout structure, border radii, shadows

### Step 2: Generate
- Create a single `index.html` using Tailwind CSS via CDN
- Include all content inline — no external CSS/JS files
- Use placeholder images from `placehold.co` when source images aren't provided
- Match only what's visible in the reference — don't add sections or features not shown

### Step 3: Screenshot & Compare
- Screenshot the build (see Shared Foundation)
- Compare: `browser-tools.py compare /tmp/reference.png /tmp/build.png /tmp/compare.png`
- View the comparison image
- List every mismatch with specific measurements:
  - Spacing/padding (px)
  - Font sizes, weights, line heights
  - Colors (hex values)
  - Alignment and positioning
  - Border radii, shadows, effects
  - Image/icon sizing

### Step 4: Fix
- Edit the HTML/Tailwind code to fix every listed mismatch
- Be precise — change specific values, not broad strokes

### Step 5: Repeat
- Re-screenshot and compare again
- **Minimum 2 comparison rounds required**
- Keep going until within ~2-3px of reference everywhere
- Only stop when user says so or no visible differences remain

### Recreation Rules
- Do not add features, sections, or content not present in the reference
- Match the reference exactly — do not "improve" the design
- If user provides CSS classes or style tokens, use them verbatim
- Keep code clean but don't over-abstract — inline Tailwind classes are fine
- Be specific about mismatches (e.g., "heading is 32px but reference shows ~24px")
- Don't guess content — use exactly what's in the reference or placeholder text

---

## Mode B: Creation

When the user describes what to build but provides no reference image.

**Philosophy:** Design distinctive, memorable interfaces. No AI slop. Every build should feel hand-crafted.

### Step 1: Design Thinking
Before writing any code, establish:
- **Purpose:** What problem does this interface solve? Who uses it?
- **Tone:** Pick a BOLD direction — brutally minimal, maximalist, retro-futuristic, organic/natural, luxury/refined, playful, editorial/magazine, brutalist/raw, art deco, soft/pastel, industrial, etc.
- **Constraints:** Technical requirements, accessibility needs
- **Differentiation:** What's the ONE thing someone will remember about this design?

**CRITICAL:** Choose a clear conceptual direction and execute with precision. Bold maximalism and refined minimalism both work — the key is intentionality, not intensity.

### Step 2: Choose Aesthetic Direction
Options:
1. **Use a preset** from `references/cinematic-presets.md` (Organic Tech, Midnight Luxe, Brutalist Signal, Vapor Clinic)
2. **Custom aesthetic** — define palette, typography pair, image mood, identity statement
3. **Scroll-driven** — load `references/scroll-driven-design.md` for typography-as-design, color zones, animation choreography rules

Whichever path: verify choices against `references/aesthetic-guidelines.md` guardrails before proceeding.

### Step 3: Generate
- Create a single `index.html` with Tailwind CSS via CDN
- Apply the chosen aesthetic system consistently
- Include GSAP animations via CDN for scroll/entrance effects
- Build with depth: layered shadows, noise overlays, gradient atmospheres
- Every interactive element gets hover, focus-visible, and active states

### Step 4: Screenshot & Self-Review
- Screenshot the build
- Review against anti-generic guardrails checklist:
  - [ ] No banned fonts (Inter/Roboto/Arial as primary)?
  - [ ] No default Tailwind palette colors?
  - [ ] Paired fonts (display ≠ body)?
  - [ ] Layered, color-tinted shadows (not flat shadow-md)?
  - [ ] All clickables have hover + focus + active states?
  - [ ] Consistent spacing tokens?
  - [ ] Depth/layering system (not all flat)?
  - [ ] Would a human designer recognize this as AI-generated? If yes → fix.

### Step 5: Iterate
- Fix any guardrail violations found in self-review
- Re-screenshot
- **Minimum 1 self-review round required** (2+ recommended)
- Ask: "Does this feel like it was designed by a creative studio, or generated by AI?"

### Creation Rules
- Never converge on the same aesthetic across builds — vary themes, fonts, palettes
- Match implementation complexity to vision: maximalist = elaborate code; minimalist = precise restraint
- Check `brand_assets/` folder in the project before designing — use real logos/colors if available
- Load client brand-voice and ICP context if available (from `clients/<project>/`)

---

## Mode C: Hybrid

When user provides a reference AND asks to improve/redesign it.

1. Run Mode A Steps 1-2 (analyze reference, generate structure match)
2. Identify the structural skeleton (layout, sections, content flow)
3. Apply Mode B aesthetic direction on top of that skeleton
4. Run Mode B Steps 4-5 (self-review against guardrails)

The reference defines WHAT content and layout to use. Creation mode defines HOW it looks.

---

## File Structure

```
build/
├── index.html              # The build
├── screenshots/
│   ├── reference.png       # Original reference (Mode A/C)
│   ├── build-pass-1.png    # First build screenshot
│   ├── compare-1.png       # First comparison (Mode A)
│   ├── build-pass-2.png    # Second build screenshot
│   ├── compare-2.png       # Second comparison (Mode A)
│   └── final.png           # Final result
└── assets/                 # Any local images/icons if needed
```

---

## Integration with Other Skills (During Build)

| Need | Route To |
|------|----------|
| Marketing copy | `copywriting` skill + `copywriter` agent |
| Brand voice check | `brand-building` skill + `brand-voice-guardian` agent |
| Image generation | `image-generation` skill |

---

## Post-Build Optimization Router

**MANDATORY.** After the build is complete and screenshots pass review, present the user with this optimization menu. The website is only half-done after design — optimization is what makes it perform.

Present as a numbered checklist the user can pick from:

> **Your website is built. Want to optimize it?**
>
> Pick any combination (recommended: all of them):
>
> 1. **CRO Audit** — Conversion rate optimization review
> 2. **SEO Optimization** — On-page SEO, meta tags, heading structure, keyword placement
> 3. **AEO / GEO** — AI Engine Optimization & Generative Engine Optimization (structured data for AI answers)
> 4. **Schema Markup** — JSON-LD structured data for rich snippets
> 5. **Analytics & Tracking** — GA4 events, conversion pixels, UTM setup
> 6. **Performance Audit** — Page speed, Core Web Vitals, image optimization
> 7. **Accessibility Check** — WCAG compliance, screen reader, contrast
>
> Or say "all" to run the full optimization stack.

### Optimization Routing Table

| # | Optimization | Skill | Agent | What It Does |
|---|-------------|-------|-------|-------------|
| 1 | CRO Audit | `page-cro` | `conversion-optimizer` | Reviews CTAs, above-fold content, social proof placement, friction points, form optimization, trust signals. Outputs specific HTML/copy changes. |
| 2 | SEO | `seo-mastery` | `seo-specialist` | Adds/fixes meta title & description, heading hierarchy (H1-H6), alt text, internal linking structure, keyword placement, canonical tags, Open Graph & Twitter cards. |
| 3 | AEO / GEO | `schema-markup` + `seo-mastery` | `seo-specialist` | Adds FAQ schema, HowTo schema, speakable markup, and structures content for AI-generated answers (Google AI Overviews, ChatGPT search, Perplexity). Focuses on concise answer-format blocks, entity markup, and citation-friendly structure. |
| 4 | Schema Markup | `schema-markup` | `seo-specialist` | Adds JSON-LD: Organization, WebPage, Product, FAQ, BreadcrumbList, LocalBusiness (as relevant). Validates with Google Rich Results guidelines. |
| 5 | Analytics & Tracking | `analytics-attribution` | `tracking-specialist` | Sets up GA4 gtag.js, defines key events (page_view, scroll, click, form_submit, cta_click), adds conversion pixels (Meta, Google Ads), UTM parameter capture, data layer. |
| 6 | Performance | (built-in) | — | Checks: image format (WebP/AVIF), lazy loading, font-display: swap, minified CSS/JS, preconnect hints, defer/async scripts, CLS prevention. |
| 7 | Accessibility | (built-in) | — | Checks: color contrast (4.5:1 minimum), focus indicators, ARIA labels, skip-to-content link, semantic HTML, alt text, keyboard navigation, reduced-motion support. |

### Execution Flow

When user picks optimizations:

1. **Run them sequentially** — each optimization may change the HTML, so later ones build on earlier changes
2. **Recommended order:** SEO → Schema → AEO/GEO → CRO → Tracking → Performance → Accessibility
3. **After each optimization:** briefly list what changed (3-5 bullet points)
4. **After all optimizations:** take a final screenshot to confirm nothing broke visually
5. **Final output:** updated `index.html` with all optimizations applied inline

### AEO / GEO Specific Patterns

Since this is newer and not yet a standalone skill, here are the key patterns to apply:

- **Concise answer blocks:** Add `<div itemscope itemtype="https://schema.org/Answer">` around FAQ-style content
- **Entity markup:** Wrap brand/product/person names in `<span itemprop="name">` within appropriate schema
- **Speakable:** Add `speakable` schema property to sections suitable for voice search
- **Question-answer format:** Structure "How it works" / "Why us" sections as implicit Q&A pairs
- **Citation-friendly:** Include clear, quotable one-sentence descriptions near the top of the page
- **Topical authority signals:** Link to authoritative sources, include author/org credentials

---

## Learnings

(Updated as patterns are confirmed during website builds — see `learnings.md`)
