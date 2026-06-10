# Step 12 — image-gen prompts (3 parallel, one per top-3 ad)

> FICTIONAL SMOKE-TEST DATA - not a real client. EMULATED. Paste-ready prompts with model-specific
> parameter strings (Midjourney / DALL-E 3 / Flux / Ideogram), per SKILL.md step-12 contract. Visual
> tone per CLAUDE.md: calm, plain, numbers-first, no hype, no drone-shot aspiration (that's
> kill-listed). Static ad creative for Meta feed (1:1 and 4:5). NO generation was run — prompts only.

---

## Image 1 — for Ad 1 (recognition hook)

**Concept:** Split-frame. Left: a phone showing a flurry of "SOLD" notifications and missed calls.
Right: the same phone, screen quiet, one unread message. Cool, calm, documentary lighting. The
contrast IS the message (loud on sell, silent on buy). Headline text overlaid top.

- **Midjourney v6:** `split-screen smartphone, left side crowded with SOLD property notifications and calls, right side silent single unread chat, calm Singapore HDB interior background, soft natural window light, muted blues and warm neutrals, editorial documentary style, no text --ar 4:5 --style raw --v 6`
- **DALL-E 3:** "A clean split-screen of one smartphone shown twice. Left: busy with property SOLD alerts and many missed calls. Right: quiet, a single unread message. Calm Singapore flat interior, soft daylight, muted palette. Editorial, restrained, room for a headline at the top."
- **Flux:** `split-frame phone, left busy with sold-property alerts, right silent, calm SG apartment, soft daylight, muted blue/neutral, photographic, leave top third clear for overlay text, 4:5`
- **Ideogram:** `Split-screen smartphone composition, sold-property alerts vs silence, calm muted tones, top banner space for headline text, photographic, 4:5`

---

## Image 2 — for Ad 2 (mechanism hook)

**Concept:** A plain see-saw / balance diagram, hand-drawn marker style on white. One side: a small
fixed coin labelled "flat fee". Other side: a rising stack of coins tied to a rising house price
arrow. The fixed coin doesn't move. Calm infographic, not aggressive. Reads in one glance: their pay
rises with your price, ours doesn't.

- **Midjourney v6:** `minimalist hand-drawn infographic on white, a balance scale, one side a single fixed coin, other side a growing stack of coins linked to a rising house-price arrow, calm marker illustration, two flat colours plus black ink, lots of negative space --ar 1:1 --style raw --v 6`
- **DALL-E 3:** "A calm, minimalist hand-drawn infographic on a white background. A simple balance: one side a single fixed coin labelled with a flat amount; the other side a growing stack of coins rising with a house-price arrow. Two-colour marker style, plenty of white space, clear and unhurried."
- **Flux:** `minimal marker-style infographic, white background, fixed single coin vs rising coin stack with price arrow, two-tone, large negative space for headline, 1:1`
- **Ideogram:** `Minimalist balance infographic, fixed flat-fee coin vs commission stack rising with price, clean two-colour marker, white space for text, 1:1`

---

## Image 3 — for Ad 3 (fee-flip hook)

**Concept:** A single clean receipt / line-item on white. Top line struck through: "Agent commission
(hidden in price): S$??,???". Below, crisp and clear: "Advisory fee: S$4,500 (flat, visible)". Calm,
honest, almost boring on purpose — boring reads as trustworthy to this skeptic. No red, no alarm.

- **Midjourney v6:** `clean minimalist receipt graphic on white, top line a struck-through hidden commission with question marks, bottom line a clear flat fee, calm neutral palette, crisp typography mock, no clutter, trustworthy and plain --ar 4:5 --style raw --v 6`
- **DALL-E 3:** "A clean, plain receipt-style graphic on white. One line struck through, labelled as a hidden agent commission with blurred or question-mark digits. Below it, a single clear line: a flat advisory fee. Calm neutral colours, crisp and honest, no alarm colours, deliberately plain."
- **Flux:** `minimal receipt graphic, struck-through hidden commission line vs clear flat-fee line, white background, neutral palette, plain trustworthy typography, space for headline, 4:5`
- **Ideogram:** `Plain receipt graphic, hidden commission struck out vs visible flat fee, calm neutral tones, crisp legible type, 4:5`

---

> All visuals avoid the kill-listed drone-shot/dream-home aesthetic. Each maps 1:1 to its ad's
> mechanism. Generate via the project image-gen route (`gpt-image-2` executor or `image-generation`
> skill) only after copy + claim-gate approval — none generated here (no spend).
