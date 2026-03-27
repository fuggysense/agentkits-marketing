---
name: website-design
version: "5.0.0"
brand: AgentKits Marketing by AityTech
category: content
difficulty: intermediate
description: "Quad-mode website skill: Recreation (pixel-perfect from reference), Creation (bold aesthetics from scratch), Hybrid (recreate + improve), Paper-First (import from Paper.design). Paper.design MCP for bidirectional visual editing — push HTML to Paper, read back JSX/Tailwind, extract precise design tokens. Single index.html with Tailwind CDN. Automated screenshot comparison loops. Anti-generic guardrails."
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
  - paper design
  - design from paper
  - paper to code
  - import from paper
  - paper file
prerequisites: []
related_skills:
  - page-cro
  - copywriting
  - image-generation
  - brand-building
  - schema-markup
  - userinterface-wiki
agents:
  - copywriter
  - brand-voice-guardian
  - conversion-optimizer
  - tracking-specialist
mcp_integrations:
  optional:
    - google-analytics
    - firecrawl
    - paper
success_metrics:
  - design_match_percentage
  - mobile_responsive
  - page_load_speed
  - conversion_elements_present
  - aesthetic_distinctiveness
output_schema: website-build
---

## Graph Links
- **Feeds into:** [[page-cro]]
- **Draws from:** [[copywriting]], [[brand-building]]
- **Post-build audit:** [[userinterface-wiki]] (UX quality pass — animation, timing, typography, visual design, UX laws)
- **Used by agents:** [[conversion-optimizer]]
- **Related:** [[image-generation]]

# Website Design v5.0 — Quad Mode (Recreate + Create + Hybrid + Paper-First)

Four modes, one skill. Recreate pixel-perfect, create from scratch, hybrid redesign, or import from Paper.design.

---

## Mode Router

Detect mode automatically from user input:

| Signal | Mode | Workflow |
|--------|------|----------|
| User provides reference screenshot/URL | **A: Recreation** | Match reference exactly |
| User describes what to build (no reference) | **B: Creation** | Design from scratch with bold aesthetics |
| Reference + "make it better" / "redesign" | **C: Hybrid** | Recreate structure, apply creation aesthetics |
| User says "from Paper" / has Paper file open | **D: Paper-First** | Read design from Paper, generate code, iterate bidirectionally |

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

#### Paper.design MCP (Optional — Bidirectional Design)

At the start of any website-design session, probe Paper availability by calling `get_basic_info` with a 3-second timeout. If it responds, note Paper is available and enhance the workflow. If it fails (connection refused / timeout), continue the standard workflow silently. **Paper is always optional — never blocks.**

**Read tools:** `get_basic_info`, `get_tree_summary`, `get_selection`, `get_node_info`, `get_children`, `get_jsx` (Tailwind mode), `get_computed_styles`, `get_screenshot`, `get_fill_image`, `get_font_family_info`, `get_guide`

**Write tools:** `create_artboard`, `write_html`, `set_text_content`, `update_styles`, `rename_nodes`, `duplicate_nodes`, `delete_nodes`, `find_placement`, `start_working_on_nodes`, `finish_working_on_nodes`, `group_nodes`, `ungroup_nodes`, `set_fill_image`

**Key pattern — bidirectional loop:**
```
Generate HTML → push to Paper (write_html) → user edits in canvas
→ read back (get_jsx) → refine code → push again → repeat
```

See `references/paper-integration.md` for full tool reference, JSX→HTML conversion, and workflow patterns.

### Technical Defaults (All Modes)

- **CSS framework:** Tailwind CSS via CDN — `<script src="https://cdn.tailwindcss.com"></script>`
- **Placeholder images:** `https://placehold.co/` (e.g., `https://placehold.co/600x400`)
- **Responsive:** Mobile-first responsive design
- **Output:** Single `index.html` unless user requests otherwise
- **Icons:** Inline SVGs or Heroicons via CDN
- **Fonts:** Google Fonts via `<link>` tag
- **Animations:** GSAP via CDN for scroll-driven/cinematic builds

### Taste Parameters (All Modes)

Three global variables that calibrate every build. Set at the start of Mode B/C. Mode A ignores them (recreation matches reference).

| Parameter | Range | Default | Low (1-3) | High (7-10) |
|-----------|-------|---------|-----------|-------------|
| **DESIGN_VARIANCE** | 1-10 | 6 | Clean grids, centered heroes, safe layouts | Asymmetric bento, split-screen, zig-zag, editorial |
| **MOTION_INTENSITY** | 1-10 | 5 | Hover opacity + subtle scale only | Scroll-triggered reveals, parallax, spring physics, kinetic type |
| **VISUAL_DENSITY** | 1-10 | 5 | Generous whitespace, hero-centric | Compact grids, dense feature rows, dashboard-like |

**Mapping to implementation:**

| Parameter | 1-3 | 4-6 | 7-10 |
|-----------|-----|-----|------|
| DESIGN_VARIANCE | `text-center`, symmetric grid, standard hero | 2-column zig-zag, some overlap | Asymmetric bento, split-screen, z-axis layering, masonry |
| MOTION_INTENSITY | `hover:opacity-80`, `transition-transform duration-200` | GSAP scroll fade-in, stagger reveals | ScrollTrigger pin, horizontal scroll, parallax layers, spring easing |
| VISUAL_DENSITY | `py-24` to `py-32` sections, 1-2 items per row | `py-16` to `py-20`, 2-3 items per row | `py-8` to `py-12`, 3-4+ items per row, bento grids |

**V.O.I.C.E. integration:** If a voice profile exists, read `voice/<person>/brand-voice.md` to calibrate:
- "Bold, direct, provocative" → higher DESIGN_VARIANCE (7-8)
- "Warm, approachable, friendly" → lower VISUAL_DENSITY (3-4)
- "Premium, refined, luxury" → moderate all (5-6), emphasize texture profiles

**Conversion override:** Landing pages focused on conversion should cap DESIGN_VARIANCE at 6 — experimental layouts reduce conversion rates.

**Pattern reference:** See `references/creative-arsenal.md` for patterns organized by MOTION_INTENSITY range.

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

### Completeness Protocol (All Modes)

**Banned output patterns — never produce these:**
- `<!-- rest of sections -->`, `<!-- similar to above -->`, `<!-- etc -->`
- Placeholder comments replacing real content (`<!-- add more features here -->`)
- Incomplete sections with "add more here" or "TODO" notes
- Skeleton HTML without real copy or images (unless user explicitly asks for wireframe)

**Token-limit protocol:** If a build is too large for a single response:
```
[PAUSED — X of Y sections complete. Send "continue" to resume from: [section name]]
```
Never pause mid-HTML-element. Pause only between complete sections or between workflow phases (generate → screenshot → fix).

**Scope-count-verify:** At the start of a build, count the sections to generate. After generating, verify all sections are present before declaring done. If any are missing, generate them before moving to screenshot review.

### References (load on demand)
- `references/browser-automation.md` — Playwright patterns, troubleshooting
- `references/aesthetic-guidelines.md` — Full anti-generic rules, banned/required patterns, Design Quality Score rubric
- `references/scroll-driven-design.md` — Typography-as-design, color zones, animation choreography
- `references/cinematic-presets.md` — 5 aesthetic presets + 3 texture profiles
- `references/aesthetic-modes.md` — 3 opinionated aesthetic systems: Soft (luxury/agency), Minimalist (editorial/workspace), Brutalist (industrial/tactical)
- `references/creative-arsenal.md` — 34 premium interaction patterns (nav, layout, cards, scroll, type, micro-interactions) with GSAP/Tailwind snippets
- `references/redesign-audit.md` — 7-category structured audit checklist for Mode C and site reviews
- `references/component-sources.md` — Component libraries
- `references/gallery-sources.md` — Design inspiration galleries
- `references/paper-integration.md` — Paper.design MCP tool reference, JSX→HTML conversion, bidirectional workflow patterns

---

## Design System Lookup (Data-Driven)

Before building in **Mode B (Creation)** or **Mode C (Hybrid)**, run the design system lookup to get data-backed recommendations for style, colors, typography, and layout.

### Data Files (`data/`)

8 CSV datasets (cherry-picked from [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)):

| File | Records | What It Contains |
|------|---------|-----------------|
| `styles.csv` | 67 | UI styles with properties, compatibility scores, anti-patterns |
| `colors.csv` | 161 | Industry-aligned color palettes (WCAG-compliant) |
| `typography.csv` | 57 | Font pairings with Google Fonts URLs + Tailwind config |
| `ui-reasoning.csv` | 161 | Product-type reasoning rules with JSON decision logic |
| `landing.csv` | 19 | Conversion-optimized landing page patterns |
| `ux-guidelines.csv` | 99 | UX best practices with code examples |
| `charts.csv` | 25 | Chart types with library recs + accessibility grades |
| `app-interface.csv` | 30 | UI component design guidance |

### Scripts (`scripts/`)

```bash
# Generate full design system recommendation for a product type
python3 skills/website-design/scripts/design-search.py "SaaS dashboard" --design-system

# Search a specific domain (style, color, typography, landing, ux, chart, web)
python3 skills/website-design/scripts/design-search.py "fintech" -d color

# Persist design system to files (Master + page overrides)
python3 skills/website-design/scripts/design-search.py "e-commerce" --design-system --persist -p "MyProject"
python3 skills/website-design/scripts/design-search.py "e-commerce" --design-system --persist -p "MyProject" --page "checkout"
```

### When to Use

1. **Mode B (Creation):** Run `--design-system` with the product type/industry BEFORE Step 2 (Choose Aesthetic Direction). Feed the output into your style, color, typography, and layout decisions.
2. **Mode C (Hybrid):** Run after analyzing the reference to get data-backed alternatives for the redesign direction.
3. **Mode A (Recreation):** Skip — recreation matches the reference exactly, no design decisions needed.

### Override Priority

Anti-generic guardrails from `references/aesthetic-guidelines.md` **always override** CSV suggestions:
- If CSV suggests Inter or Roboto → reject, pick the next best pairing
- If CSV suggests default Tailwind palette colors → adjust to custom variants
- The data informs; the guardrails enforce

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

### Paper Enhancement (if Paper is available)
After generating HTML in Step 2, push to Paper via `write_html` for visual side-by-side comparison. Use `get_computed_styles` on the reference (if it's a Paper file) for precise design token extraction — more accurate than Gemini vision for exact hex colors, spacing, and font sizes.

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

### Step 1.5: Design System Lookup (Data-Driven)
Run the design system search to get data-backed recommendations:
```bash
python3 skills/website-design/scripts/design-search.py "<product type / industry>" --design-system
```
This returns recommended style, color palette, typography pairing, layout pattern, and anti-patterns — all from structured CSV data (67 styles, 161 color palettes, 57 font pairings, 161 reasoning rules).

Use the output to **inform** Step 2 choices. If any recommendation conflicts with anti-generic guardrails, the guardrails win.

### Step 2: Choose Aesthetic Direction
Options:
1. **Use a preset** from `references/cinematic-presets.md` (Organic Tech, Midnight Luxe, Brutalist Signal, Vapor Clinic)
2. **Custom aesthetic** — define palette, typography pair, image mood, identity statement
3. **Data-driven** — use the design system lookup output from Step 1.5 as your foundation
4. **Scroll-driven** — load `references/scroll-driven-design.md` for typography-as-design, color zones, animation choreography rules
5. **Aesthetic mode** — load `references/aesthetic-modes.md`: Soft (luxury/agency), Minimalist (editorial/workspace), or Brutalist (industrial/tactical). Each mode defines complete palette, typography, surface treatment, component rules, and motion philosophy

Whichever path: verify choices against `references/aesthetic-guidelines.md` guardrails before proceeding.

### Step 3: Generate
- Create a single `index.html` with Tailwind CSS via CDN
- Apply the chosen aesthetic system consistently
- Include GSAP animations via CDN for scroll/entrance effects
- Build with depth: layered shadows, noise overlays, gradient atmospheres
- Every interactive element gets hover, focus-visible, and active states

### Step 4: Screenshot & Self-Review
- Screenshot the build
- **Score with Design Quality Score** (from `references/aesthetic-guidelines.md`):
  - Typography Intent: __/5
  - Color Confidence: __/5
  - Layout Distinctiveness: __/5
  - Interaction Polish: __/5
  - Overall Memorability: __/5
  - **DQS: __/5** (must be ≥ 3.0 to pass)
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

### Paper Enhancement (if Paper is available)
After generating HTML in Step 3, push to Paper via `write_html` for visual editing. User can adjust layout, colors, typography directly in the Paper canvas. Read changes back via `get_jsx`, integrate into `index.html`, and push again. This creates a rapid bidirectional iteration loop.

### Creation Rules
- Never converge on the same aesthetic across builds — vary themes, fonts, palettes
- Match implementation complexity to vision: maximalist = elaborate code; minimalist = precise restraint
- Check `brand_assets/` folder in the project before designing — use real logos/colors if available
- Load client brand-voice and ICP context if available (from `clients/<project>/`)

---

## Mode C: Hybrid

When user provides a reference AND asks to improve/redesign it.

**Philosophy:** Preserve what works (structure, content, flow). Transform what doesn't (aesthetics, interaction, polish).

### Step 1: Analyze Reference
- Run Mode A Step 1 (screenshot + design token extraction)
- Capture the structural skeleton: section order, content flow, layout grid

### Step 2: Run Design Audit
- Load `references/redesign-audit.md`
- Score each of the 7 categories (Typography, Color, Layout, Interactivity, Content, Components, Strategic Omissions)
- For each check, mark as **KEEP** (preserve in redesign) or **FIX** (change in redesign)
- Calculate overall Design Quality Score from `references/aesthetic-guidelines.md`

### Step 3: Plan the Redesign
- Identify what to preserve: structural skeleton, content, conversion flow
- Identify what to improve: the lowest-scoring audit categories
- Apply fixes in the priority order from the audit (Font swap → Color cleanup → Hover states → Layout → Components → States → Typography polish)
- Choose aesthetic direction (preset, texture profile, or custom) for the visual transformation

### Step 4: Generate
- Create the build using the preserved skeleton + new aesthetic direction
- Apply taste parameters (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY)
- Follow the fix priority order — don't try to change everything at once

### Step 5: Screenshot & Score
- Screenshot the build
- Re-run the Design Quality Score — compare before vs after
- Run the self-review checklist from `references/aesthetic-guidelines.md`
- **Minimum 1 comparison round required** (2+ recommended)
- Present before/after scores to the user

The reference defines WHAT content and layout to use. The audit defines WHAT to fix. Creation mode defines HOW to fix it.

---

## Mode D: Paper-First

When user has an existing Paper.design file to convert to code, or says "from Paper."

**Requires:** Paper.app running with the target file open.

**Philosophy:** The Paper file is the design authority. Faithfully convert the visual design to code, then iterate bidirectionally.

### Step 1: Read the Design
- `get_basic_info` → confirm file is loaded, get canvas dimensions
- `get_tree_summary` → map the full node tree structure
- `get_font_family_info` → identify all fonts used
- `get_screenshot` → capture the full design for visual reference
- For each top-level section: `get_jsx` → export Tailwind code

### Step 2: Analyze
- Map the node tree to HTML sections (header, hero, features, footer, etc.)
- Extract design tokens via `get_computed_styles` on key elements (colors, spacing, typography, shadows)
- Check tokens against anti-generic guardrails — note any violations but **do not change them** (Paper file is authority, same exception as Mode A)
- Name HTML sections to match Paper layer names for traceability

### Step 3: Generate
- Build `index.html` using Tailwind CSS via CDN
- Convert JSX output to plain HTML (`className` → `class`, self-closing tags, etc.)
- Include Google Fonts `<link>` tags based on `get_font_family_info` results
- Match design tokens precisely — use custom Tailwind config in `<script>` tag if needed

### Step 4: Push Back & Compare
- `create_artboard` → create "Code Output" artboard in Paper
- `write_html` → push the generated HTML to the new artboard
- `get_screenshot` of both the original design and the code output
- Compare visually, list mismatches with specific measurements

### Step 5: Iterate
- Fix mismatches in the HTML code
- Re-push via `write_html`
- OR: user edits the code output in Paper canvas → `get_jsx` → update `index.html`
- **Minimum 1 comparison round required**
- Keep going until visual parity achieved

### Paper-First Rules
- Paper file is the design authority — if the design uses "banned" patterns, keep them (same as Mode A exception)
- Name HTML sections to match Paper layer names
- Use `get_computed_styles` for exact values — don't approximate
- If the design has responsive variants in Paper, generate responsive Tailwind classes accordingly
- Export sections individually via `get_jsx` if the full-page export is too large

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
│   ├── final.png           # Final result
│   ├── paper-source.png    # Paper design screenshot (Mode D)
│   └── paper-render.png    # Paper HTML render screenshot (Mode D)
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
> 8. **UX Audit** — Animation timing, easing, typography, visual design, UX psychology laws
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
| 8 | UX Audit | `userinterface-wiki` | — | Reviews animations, timing, easing, typography, visual design, and UX psychology laws against 152 curated rules. Outputs file:line findings with fixes. |

### Execution Flow

When user picks optimizations:

1. **Run them sequentially** — each optimization may change the HTML, so later ones build on earlier changes
2. **Recommended order:** SEO → Schema → AEO/GEO → CRO → Tracking → Performance → Accessibility → UX Audit
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

### UX Audit Execution (Step 8)

Reads the built HTML against `userinterface-wiki` rules (`.agents/skills/userinterface-wiki/rules/`). Focus on the 6 categories most relevant to marketing sites — skip React/Framer Motion-specific rules.

**Audit categories (in priority order):**

| Priority | Category | What to Check | Key Rules |
|----------|----------|---------------|-----------|
| 1 | Animation Principles | All transitions < 300ms, one focal animation at a time, stagger < 50ms/item | `timing-*`, `physics-*`, `staging-*` |
| 2 | Laws of UX | CTA targets ≥ 32px, choices minimized, response < 400ms, progressive disclosure | `ux-*` |
| 3 | Visual Design | Concentric border radius, layered shadows, consistent spacing scale, no pure-black shadows | `visual-*` |
| 4 | Typography | Tabular nums for pricing, font-display: swap, text-wrap: balance on headings, underline offset | `type-*` |
| 5 | Timing Functions | Entrances ease-out, exits ease-in, no linear motion (except progress bars), duration ranges correct | `easing-*`, `duration-*`, `none-*` |
| 6 | CSS & Prefetch | Pseudo-elements over extra DOM nodes, view transition names, hit-slop prefetch | `pseudo-*`, `prefetch-*` |

**Skip categories:** Exit Animations (AnimatePresence), Morphing Icons, Container Animation, Audio Feedback, Sound Synthesis — these are React/Framer Motion-specific or not applicable to marketing sites.

**Execution steps:**
1. Read the built `index.html`
2. For each category above, load the relevant rule files from `.agents/skills/userinterface-wiki/rules/`
3. Scan the HTML for violations — output as `file:line` findings
4. Group findings by severity: **MUST FIX** (animation > 300ms, tiny CTA targets, no font-display) vs **SHOULD FIX** (missing text-wrap balance, shadow improvements)
5. Apply MUST FIX items automatically, present SHOULD FIX for user approval

**Output format:**
```
UX Audit — 12 findings (4 must-fix, 8 should-fix)

MUST FIX:
- index.html:142 — transition duration 500ms exceeds 300ms max (timing-under-300ms)
- index.html:89 — CTA button 24px wide, below 32px minimum (ux-fitts-target-size)
- index.html:3 — missing font-display: swap on Google Fonts link (type-font-display-swap)
- index.html:201 — linear easing on card hover, should be ease-out (easing-no-linear-motion)

SHOULD FIX:
- index.html:45 — h2 missing text-wrap: balance (type-text-wrap-balance-headings)
- index.html:78 — shadow uses pure black, prefer neutral (visual-no-pure-black-shadow)
...
```

---

## Learnings

(Updated as patterns are confirmed during website builds — see `learnings.md`)
