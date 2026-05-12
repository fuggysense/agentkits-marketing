# High-Converting Static Ad Brief

> **Load this file in Phase 2a (Hooks) whenever `format ∈ {Static, Carousel}`.**
> **Origin:** 2026-04-18 — Jerel briefed these constraints during neezanizam DCT001 generation. They apply to ALL static/carousel variant generation from this point forward, for every client.
> **Bar:** *"They need to be so good that the persona feels physically ill if they scroll past it."*

---

## Non-negotiable rules (apply to every single image variant in a batch)

1. **Each variant must be completely unique from the others.** Different composition, different concept type, different visual style. No two variants in a batch share the same treatment.
2. **Different formats and styles across the 3 variants.** The spread typically looks like: typographic/editorial, photojournalistic scene, split-screen or narrative diptych, UGC-style selfie, infographic, screenshot aesthetic. Never pick three photos of people in the same setting — that's one creative with three exposures.
3. **Any person in the ad must be demographically correct for the market.** Singapore = Chinese / Malay / Indian / Eurasian. Match the target avatar's ethnicity to the primary variant. Use the other variants to broaden reach across the market's main ethnic groups without adding a test variable.
4. **People must look real — not AI-like.** No plastic skin, no over-symmetrical faces, no impossibly perfect teeth, no seven-fingered hands, no uncanny-valley smiles. Reference real photographers by name in the `style` field (e.g. Geraldine Kang, Sean Lee for SG; Alec Soth, Gregory Crewdson for cinematic). Negative prompt must explicitly reject: AI skin sheen, warped hands, extra fingers, over-symmetry, plastic texture, AI watermark.
5. **The headline must be clear on the ad.** Not a subtle overlay, not a faint watermark — readable in the feed thumbnail. Specify font, colour, placement, size relative to the image, and contrast. Use drop-shadows or scrims behind text over busy imagery.
6. **Add a bridge line or additional info if the hook alone is ambiguous.** If the hook is provocative but unclear (e.g. "3 numbers. Not your salary."), the image can carry a small bridge line that removes confusion ("The 3rd one isn't on any letter.") without turning the image into a wall of text.
7. **Stay away from generic imagery.** No stock-photo smiling couples, no hand-shaking-over-keys clichés, no cartoon dollar signs, no generic house icons, no shutterstock-looking faces. The image must look like it belongs in a *Straits Times* feature, a *Kinfolk* editorial, or a documentary — not in an FB marketplace ad.
8. **The information on the image must be factually correct and make sense to the persona.** No invented stats. No claims the brand can't back. If the image shows a document (CPF, HFE, etc.), it must look like the real Singaporean document. If the image shows a price band, it must match the persona's actual income range.
9. **Scroll-stop bar:** gut-punching, emotion-provoking, curiosity-driving, high-converting. The persona should feel physically ill if they scroll past it — because it names their exact situation, mirrors their inner dialogue, or contradicts the belief they've been living for months.

---

## Concept-type distribution per batch (required)

Across the 3 variants, spread the `visual_concept_type` so each variant tests a different entry framing:

- **Variant A — Picture of the mechanism** (the product / methodology / framework made tangible) — often typographic or editorial infographic, no people
- **Variant B — Picture of the problem** (the before-state scene — the 11pm kitchen table, the 4th bad agent call, the abandoned cart) — photojournalistic, scene-led, person in context
- **Variant C — Picture of the transformation** (the before → after narrative collapsed into one frame — split-screen, diptych, or single subject with a clear state change) — cinematic portraiture

This distribution is the default. Deviate only when an angle genuinely requires a different spread (e.g. founder-video batches use a different logic). When you deviate, document why in the variant's `_meta.visual_concept_type_rationale` field.

---

## Visual-style distribution per batch (required)

No two variants in the same batch share a visual style. Spread across:

- Premium editorial infographic / Bloomberg-Straits Times aesthetic
- Warm documentary photojournalism
- Cinematic diptych portraiture
- UGC selfie / phone-camera first-person
- Text-on-dark WhatsApp screenshot
- Claymation / 3D / Pixar illustration
- Data-overlay-on-photo
- Split-screen before/after

L4 and L5 markets favour UGC + authentic + text-on-dark. L1-L3 markets favour clean demo / infographic / bold-claim. Match to the batch's sophistication level (see `sophistication-creative-map.md`).

---

## Quality self-check before writing to `dct-tracker.json`

Before any variant ships into the tracker, run this 9-point check against the rules above. If any point is weak, regenerate — do not ship.

```
[ ] Variant A, B, C are visibly, structurally different from one another
[ ] Format/style spread hits 3 distinct treatments
[ ] People (if any) match SG ethnic distribution logic
[ ] No AI-uncanny tells (hands, symmetry, skin sheen) — negative prompt explicit
[ ] Headline on image is clear in feed thumbnail (font, size, contrast specified)
[ ] Bridge line present where the hook alone would confuse
[ ] Image doesn't look like a generic Meta ad — it borrows from editorial / documentary / cinema
[ ] All numbers, documents, claims shown are factually correct for the brand + persona
[ ] The "feel physically ill if they scroll past" bar is hit — named situation, mirrored dialogue, contradicted belief
```

---

## Output contract — per variant, in `dct-tracker.json`

```json
{
  "variant": "A|B|C",
  "text_on_image_hook": "[hook, 2-8 words preferred, flexible if emotionally required]",
  "bridge_line": "[optional — only if hook alone is ambiguous]",
  "visual_concept_type": "Picture of mechanism | problem | transformation | product-in-action",
  "visual_style": "[one-line style descriptor]",
  "image_prompt_file": "campaigns/<campaign-slug>/image-prompts/<batch>-<variant>.json"
}
```

The full Nano Banana 2 JSON prompt lives in the file path, not inline in the tracker. The tracker stays readable; the prompts stay searchable/editable per file.
