## Graph Links
- **Parent skill:** [[image-generation]]
- **Sibling references:** [[nano-banana-full-guide]]
- **Related skills:** [[video-director]], [[tiktok-slideshows]]

# Nano Banana 2 — JSON Prompt Examples

> Source: fearless-offer-231.notion.site — Nano Banana 2 with Claude Code
> Cost: ~$0.07 per generated image
> Use these as templates — customize subject, product, and scene details for your needs.

---

## 1. UGC Skincare Selfie

**Style:** ugc-selfie | **Ratio:** 4:5 | **Resolution:** 2K

Best for: Social proof ads, authentic product testimonials, Instagram feed

```json
{"meta":{"aspect_ratio":"4:5","resolution":"2K","thinking_level":"high"},"subject":[{"type":"person","appearance":{"age":"late 20s","gender":"female","skin":"visible pores, natural texture, subtle redness on cheeks, light freckles across nose bridge","hair":{"style":"messy bun, loose strands framing face","color":"dark brown"},"expression":"genuine smile, relaxed, morning freshness"},"clothing":[{"item":"oversized white cotton t-shirt","fit":"relaxed, slightly off-shoulder"}],"action":"holding a 1oz glass dropper bottle of vitamin C serum close to face, other hand touching cheek","position":"center frame"},{"type":"product","name":"Vitamin C Brightening Serum","details":"1oz amber glass dropper bottle, white label with gold text reading 'VITAMIN C SERUM', dropper cap slightly open, golden liquid visible"}],"scene":{"location":"modern bathroom, marble countertop partially visible","details":"small potted succulent and cotton rounds visible on counter edge, mirror slightly out of focus behind","time_of_day":"morning","lighting":{"type":"ring-light","direction":"frontal, slightly above eye level","quality":"soft, even, bright catchlight in both eyes, slight overexposure at edges"}},"camera":{"lens":"28mm","angle":"selfie angle — slightly above eye level, 15 degrees","framing":"close-up, face and product prominent","height":"above eye level","depth_of_field":"shallow","focus":"eyes and product","style":"shot on iPhone 15, slight wide-angle distortion, casual imperfect framing"},"style":{"aesthetic":"ugc-selfie","color_grading":"warm, slightly overexposed highlights","mood":"authentic morning routine, casual, real person not a model","post_processing":"minimal — slight warmth increase only"},"negative_prompt":"professional model, studio lighting, airbrushed skin, perfect hair, magazine quality, plastic skin, overly posed, stock photo, cartoon, watermark, extra fingers, oversaturated, heavy makeup"}
```

**Key techniques:** Ring-light frontal lighting, iPhone selfie style, warm color grading, natural skin imperfections, casual imperfect framing.

---

## 2. Product Hero Clean

**Style:** studio-product-hero | **Ratio:** 1:1 | **Resolution:** 2K

Best for: E-commerce listings, landing page hero images, product catalogs

```json
{"meta":{"aspect_ratio":"1:1","resolution":"2K","thinking_level":"minimal"},"subject":[{"type":"product","name":"Premium Protein Powder","details":"Matte black cylindrical tub, 2lb size, silver metallic label reading 'PURE WHEY ISOLATE' in clean sans-serif font, nutrition facts panel visible on side, sealed lid","position":"centered, angled 15 degrees to the right to show label and side simultaneously"}],"scene":{"location":"infinite white studio background","surface":"white seamless paper, soft circular shadow beneath product","lighting":{"type":"studio-softbox","direction":"main key light from upper-left at 45 degrees, fill light from right at 25% intensity, subtle hair light from behind for edge definition","quality":"soft, even, product edges clearly defined with subtle rim highlight, no harsh shadows"}},"camera":{"model":"Phase One IQ4","lens":"105mm","aperture":"f/11","angle":"eye-level with product center","framing":"product fills 65% of frame, breathing room on all sides","depth_of_field":"deep — entire product tack sharp from front label to back edge"},"style":{"aesthetic":"studio-product-hero","color_grading":"neutral, true-to-life colors, whites are pure white","mood":"clean, premium, trustworthy, e-commerce ready"},"negative_prompt":"busy background, distorted proportions, misspelled text on label, blurry label, floating product, harsh shadows, colored background, lifestyle elements, hands, person"}
```

**Key techniques:** Three-point softbox lighting, infinite white background, deep DOF (f/11), product fills 65% of frame, thinking_level "minimal" for simple shot.

---

## 3. LinkedIn Authority Headshot

**Style:** editorial-portrait | **Ratio:** 1:1 | **Resolution:** 2K

Best for: LinkedIn profiles, team pages, speaker bios, author photos

```json
{"meta":{"aspect_ratio":"1:1","resolution":"2K","thinking_level":"high"},"subject":[{"type":"person","appearance":{"age":"mid-30s","gender":"male","ethnicity":"South Asian","build":"athletic, broad shoulders","skin":"visible pores, natural skin texture, light stubble along jawline, subtle smile lines","hair":{"style":"short, neatly styled, slight texture on top","color":"black"},"expression":"confident, relaxed smile with closed lips, direct eye contact, slight head tilt to the right"},"clothing":[{"item":"dark charcoal blazer over black crew neck t-shirt","fabric":"wool blend blazer, cotton tee","fit":"modern slim fit, shoulders sharp"}],"accessories":[{"item":"minimal watch","material":"brushed silver, dark face","placement":"left wrist, barely visible"}],"action":"facing camera, shoulders angled 30 degrees to the left, chin slightly forward","position":"center frame, rule of thirds with eyes on upper third line"}],"scene":{"location":"modern minimalist office, completely out of focus","lighting":{"type":"studio-softbox","direction":"Rembrandt lighting — key light from upper left at 45 degrees, creating triangle of light on right cheek","quality":"soft, directional, subtle fill from right side to prevent deep shadows","secondary":"hair light from behind-right for edge separation from background"},"background_blur":"completely blown out — solid soft gray gradient, no identifiable elements"},"camera":{"model":"Sony A7RV","lens":"85mm","aperture":"f/2.0","shutter_speed":"1/200","iso":200,"angle":"eye-level, camera at exact same height as subject's eyes","framing":"head and shoulders, top of head has small breathing room, bottom crops at mid-chest","depth_of_field":"shallow — eyes tack sharp, ears slightly soft","focus":"locked on nearest eye"},"style":{"aesthetic":"editorial-portrait","color_grading":"neutral with subtle warmth, skin tones true to life","mood":"trustworthy, competent, executive presence without being stiff","film_stock":"digital clean, minimal post-processing"},"negative_prompt":"plastic skin, airbrushed, stock photo, toothy grin, harsh shadows, flat lighting, busy background, visible office furniture, cartoon, watermark, overly saturated, heavy retouching, glamour lighting"}
```

**Key techniques:** Rembrandt lighting (triangle of light on cheek), 85mm f/2.0 shallow DOF, eyes on upper third, blown-out background, hair light for edge separation.

---

## 4. Carousel Cover Slide

**Style:** clean-bold-cover | **Ratio:** 4:5 | **Resolution:** 1K

Best for: Instagram/LinkedIn carousel first slides, social media hooks, educational content

```json
{"meta":{"aspect_ratio":"4:5","resolution":"1K","thinking_level":"high"},"subject":[],"scene":{"details":"Deep navy (#1a1a2e) to purple (#7b5ad9) diagonal gradient background, subtle geometric pattern of thin lines at 10% opacity, clean and modern"},"text_rendering":{"elements":[{"text":"7 Mistakes","placement":"center-upper, large and dominant","font_style":"sans-serif, extra bold, very large, uppercase","color":"white"},{"text":"Killing Your","placement":"center, directly below first line","font_style":"sans-serif, regular weight, large","color":"white at 80% opacity"},{"text":"Ad Conversions","placement":"center, directly below second line","font_style":"sans-serif, extra bold, very large, uppercase","color":"#7b5ad9"},{"text":"Swipe to fix them →","placement":"bottom-center, with comfortable margin","font_style":"sans-serif, regular, small, lowercase","color":"white at 50% opacity"}]},"style":{"aesthetic":"clean-bold-cover","color_grading":"high contrast, dark theme","mood":"curiosity-driving, authoritative, must-read, professional"},"negative_prompt":"stock photo, too many words, cluttered, light background, decorative flourishes, clip art, emoji, childish, rounded bubbly fonts, busy pattern"}
```

**Key techniques:** No subject (text only), gradient background with subtle geometry, text hierarchy (bold headline + lighter subtext + accent color keyword + faded CTA), dark theme for scroll-stopping.

---

## 5. Before/After Transformation

**Style:** before-after | **Ratio:** 16:9 | **Resolution:** 2K

Best for: Testimonials, product results, skincare/fitness/coaching transformations

```json
{"meta":{"aspect_ratio":"16:9","resolution":"2K","thinking_level":"high"},"subject":[{"type":"comparison","left_side":{"label":"BEFORE","description":"Dull, tired-looking skin with visible dark circles, uneven texture, slightly dehydrated appearance, no makeup, harsh bathroom lighting"},"right_side":{"label":"AFTER — 30 DAYS","description":"Same person, same angle, same lighting setup. Skin looks hydrated, more even tone, healthy glow, dark circles reduced, visible improvement but still natural — not airbrushed perfection"},"consistency_note":"CRITICAL: Same person, same camera angle, same expression (neutral, looking at camera), same hair style, same clothing (white t-shirt). Only the skin condition changes."}],"scene":{"location":"bathroom, neutral background","lighting":{"type":"identical on both sides — overhead bathroom vanity light","quality":"even, slightly warm, no tricks to make one side look better through lighting alone"}},"camera":{"lens":"50mm","angle":"eye-level, straight on","framing":"clean vertical split down the exact middle, equal visual weight to both sides","depth_of_field":"moderate"},"text_rendering":{"elements":[{"text":"BEFORE","placement":"top-left corner of left half","font_style":"sans-serif, bold, medium","color":"white with dark shadow for readability"},{"text":"AFTER — 30 DAYS","placement":"top-right corner of right half","font_style":"sans-serif, bold, medium","color":"white with dark shadow for readability"},{"text":"Real results. No filter.","placement":"bottom-center spanning both halves","font_style":"sans-serif, regular, small","color":"white at 70% opacity"}]},"style":{"aesthetic":"before-after","color_grading":"neutral on both sides — identical grading, let the transformation speak for itself","mood":"honest, dramatic improvement, trustworthy"},"negative_prompt":"different lighting between sides, different person, unfair comparison, blurry, misspelled labels, airbrushed after photo, too dramatic difference, cartoon, stock photo"}
```

**Key techniques:** Identical lighting on both sides (critical for trust), same person/angle/expression, clean vertical split, text labels with dark shadow for readability, "Real results. No filter." trust badge.

---

## Customization Guide

To adapt any template:

1. **Change the product** — Update subject name, details, and label text
2. **Change the person** — Update appearance (age, gender, ethnicity, hair, expression)
3. **Change the style** — Swap aesthetic, color_grading, and mood
4. **Change the aspect ratio** — 4:5 (social feed), 1:1 (product/headshot), 16:9 (comparison/banner), 9:16 (stories/reels)
5. **Always update negative_prompt** — Include category-specific exclusions

### Aspect Ratio Guide for Marketing

| Ratio | Use For |
|-------|---------|
| 4:5 | Facebook/Instagram feed ads, social posts |
| 1:1 | Product shots, headshots, square ads |
| 16:9 | Before/after, blog headers, YouTube thumbnails |
| 9:16 | Instagram/TikTok stories and reels |
| 3:4 | Pinterest pins |
