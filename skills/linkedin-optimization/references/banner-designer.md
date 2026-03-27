## Graph Links
- **Parent skill:** [[linkedin-optimization]]
- **Sibling references:** [[content-ideas]], [[linkedin-algorithm]], [[profile-analyzer]]
- **Related skills:** [[image-generation]], [[brand-building]]

# LinkedIn Banner Designer — Interactive Image Generation Tool

> **Trigger:** User says "design my LinkedIn banner" or "create LinkedIn banner"

## Instructions for Claude

When triggered, follow this exact workflow:

---

## Step 1: Ask 6 Questions

Present these questions to the user (all required before generating):

> I'll design your LinkedIn banner (1584×396px). Answer these 6 questions:
>
> 1. **Headline** — What's the main text? (e.g., "Helping B2B companies scale with content") Keep under 8 words.
> 2. **Tagline** — Supporting text below headline? (e.g., "Speaker | Author | Growth Consultant") Keep under 10 words. Leave blank to skip.
> 3. **CTA text** — What action should people take? (e.g., "Book a free strategy call" or "Subscribe to my newsletter")
> 4. **Social proof** — One credibility line? (e.g., "500+ companies helped" or "Featured in Forbes") Leave blank to skip.
> 5. **Brand colors** — Provide 2-3 hex codes (e.g., #2563EB, #1E293B, #F8FAFC). If unsure, I'll use professional defaults.
> 6. **Photo inclusion** — Do you want a subject/person on the banner? If yes, describe their appearance or upload a photo. If no, text-only layout.

Wait for all answers before proceeding.

---

## Step 2: Generate Image

Use the `image-generation` skill to generate the banner.

### Image Specifications

- **Final dimensions:** 1584×396px
- **Generation approach:** Generate a wide 16:9 image (wider than tall), then instruct that all content is concentrated in the **middle 30% horizontal strip** — the top 35% and bottom 35% should be solid background color only (safe zones for LinkedIn's cropping on different devices)

### Layout Rules

Within the middle content strip:

```
┌──────────────────────────────────────────────────────┐
│                   (empty - bg color)                  │  ← Top 35%: safe crop zone
│                                                      │
├──────────────────────────────────────────────────────┤
│  [CTA button/text]              [Headline]           │  ← Middle 30%: content zone
│        [Subject/photo]     [Tagline]                 │
│                            [Social proof]            │
├──────────────────────────────────────────────────────┤
│                   (empty - bg color)                  │  ← Bottom 35%: safe crop zone
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Placement details:**
- **CTA:** Top-left area of content strip (catches the eye first in left-to-right reading)
- **Subject/person:** Center-left (if included; leaves right side for text)
- **Headline + tagline:** Right half, vertically centered
- **Social proof:** Bottom-right of content strip (subtle, smaller text)

**If no subject/person:**
- Center the headline text
- CTA top-left, social proof bottom-right

### Background

- **Vibrant geometric or gradient** using the user's brand colors
- Not flat/solid — use subtle patterns, angular shapes, or color gradients
- Ensure text contrast: light text on dark areas, dark text on light areas

### Typography Rules
- Headline: Bold, large (visually dominant)
- Tagline: Medium weight, slightly smaller
- CTA: Contrasting color block/button shape or underline
- Social proof: Smaller, lighter weight
- **All text must be readable at 50% zoom** (simulates how LinkedIn displays on feed)

---

## Step 3: Review & Iterate

After generating, ask:
> Here's your LinkedIn banner. Check these before uploading:
> - [ ] Text readable when the image is small?
> - [ ] Nothing important in top/bottom 35% (LinkedIn crops differently on mobile)?
> - [ ] Profile photo won't overlap any critical text (bottom-left on desktop)?
> - [ ] Colors match your brand?
>
> Want me to adjust anything?

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Text unreadable | Increase contrast, add semi-transparent overlay behind text |
| Content cut off on mobile | Move everything to center — mobile crops more aggressively |
| Profile photo overlaps text | Keep bottom-left quadrant clear of text (desktop) and center (mobile) |
| Looks cluttered | Remove tagline or social proof — less is more on banners |
| Colors clash | Stick to 2 colors max + white for text |

---

## Integration Note

This tool uses the `image-generation` skill for actual image generation. If the skill isn't available, provide the user with a detailed design brief they can hand to a designer or use in Canva/Figma, including:
- Exact dimensions (1584×396px)
- Content placement map
- Color codes
- Font size recommendations (headline 48-60pt, tagline 24-32pt, CTA 20-28pt, social proof 16-20pt)
