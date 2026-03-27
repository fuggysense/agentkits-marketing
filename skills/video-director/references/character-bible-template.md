## Graph Links
- **Parent skill:** [[video-director]]
- **Sibling references:** [[cinematography-reference]], [[client-campaign-audit]], [[model-selection-guide]], [[realism-tricks]], [[seed-management]], [[video-type-catalog]]
- **Related skills:** [[script-skill]]

# Character Bible Template

Maintain consistent characters across shots, videos, and campaigns. Two methods: API-based (Sora Characters API) and text-based (all models).

---

## Method 1: Sora Characters API

For Sora 2 Pro only. Best for long-form projects (1min+ multi-clip sequences).

### How It Works
1. Upload a clear reference image of the character
2. Sora assigns a `@username` handle
3. Reference `@username` in future prompts — Sora maintains appearance automatically
4. **Limit:** Max 2 characters per generation via API

### API Example
```json
{
  "model": "sora-2-pro",
  "prompt": "@sarah walks into a coffee shop and sits down at a corner table...",
  "characters": [
    {
      "name": "@sarah",
      "reference_image": "sarah_reference.png"
    }
  ]
}
```

### When to Use API Method
- Multi-clip sequences featuring the same person
- Character appears in 3+ separate generations
- Long-form content (ads, mini-series, story arcs)
- When you have a clear, well-lit reference photo

### When NOT to Use API Method
- One-off generations (overkill — use text method)
- Multiple characters beyond 2 (API limit)
- Non-Sora models (Kling, VEO don't support this)
- When you don't have a reference image

---

## Method 2: Text-Based Character Block (All Models)

Works with Sora, Kling, VEO — any model that accepts text prompts. Copy this block verbatim into every prompt in a sequence.

### Facial Profile Template

```
FACIAL PROFILE: [CHARACTER NAME]
- Age: [specific age, not range]
- Bone structure: [round / angular / heart-shaped / square jaw]
- Skin tone: [specific: warm olive / light with pink undertones / deep brown / etc.]
- Skin texture: [visible pores, light acne scarring on cheeks, freckles across nose bridge]
- Eyes: [color], [shape: almond / round / hooded], [spacing: close-set / wide-set]
- Eyebrows: [thick natural / thin groomed / bushy / arched], [color]
- Nose: [straight / slightly upturned / wide bridge / narrow / button]
- Mouth: [full lips / thin upper lip / slight overbite / visible laugh lines]
- Hair: [color], [texture: straight / wavy / curly / coily], [length], [style: messy bun / slicked back / loose around shoulders]
- Distinguishing marks: [mole on left cheek, small scar above right eyebrow, birthmark on neck]
- Facial hair (if any): [5 o'clock shadow / clean-shaven / full beard trimmed short]
```

### Character Context Profile

```
CHARACTER CONTEXT: [CHARACTER NAME]
- Build: [slim / athletic / stocky / average], [approximate height impression]
- Personality energy: [calm and measured / bubbly and animated / intense and focused]
- Speaking style: [fast with hand gestures / slow and deliberate / casual with filler words]
- Default posture: [relaxed lean / straight and formal / slouched and comfortable]
- Wardrobe DNA: [always wears earth tones / prefers oversized fits / minimalist black and white]
- Current outfit: [specific: dark charcoal blazer over black crew-neck t-shirt, dark wash slim jeans, white low-top sneakers]
- Accessories: [silver watch on left wrist, thin gold chain, tortoiseshell glasses]
- Backstory cue: [tech founder, 3 years into their startup — shows in slight under-eye circles and confident posture]
```

### Common Scenarios/Expressions Matrix

| Scenario | Expression | Body Language | Voice Cue |
|----------|-----------|---------------|-----------|
| Explaining a concept | Slight squint, one eyebrow raised | Hands palm-up, leaning forward | Measured, slightly faster than normal |
| Reacting to good news | Wide eyes, genuine smile (crow's feet) | Slight head tilt back, open posture | Higher pitch, laugh at end |
| Demonstrating product | Focused, lips slightly pursed | Product held at chest height, rotating | Slower, deliberate, pointing at features |
| Casual conversation | Relaxed, asymmetric smile | Weight shifted to one leg, one hand in pocket | Natural cadence, occasional "um" |
| Surprised/impressed | Eyebrows up, mouth slightly open | Step back, then lean in | Quick inhale, "wait, really?" |

---

## Cross-Video Consistency Checklist

Before generating any new shot in a sequence:

- [ ] Facial profile block copied verbatim (no paraphrasing)
- [ ] Same clothing described in identical terms ("navy crew-neck sweater" not "blue top")
- [ ] At least 2 distinguishing marks included (anchors for the model)
- [ ] Skin tone and texture terms unchanged
- [ ] Hair described identically (style, length, color, texture)
- [ ] Accessories mentioned in same order
- [ ] Build/posture consistent (changes only if plot requires it)
- [ ] Only emotion/expression changes per shot — physical description stays verbatim

---

## Best Practices

### DO
- Be hyper-specific about UNCHANGING features (bone structure, eye color, skin tone, marks)
- Use the same vocabulary across all prompts (don't synonym-swap)
- Include at least 2 distinguishing marks — models anchor on unique features
- Describe clothing with brand-level specificity ("dark charcoal wool blazer" not "jacket")
- Lock hair state ("loose strands framing face" in every prompt)

### DON'T
- Change descriptors between shots ("brown hair" → "dark hair" = inconsistency)
- Forget the marks/scars — they're the strongest consistency anchors
- Over-specify emotion in the character block (emotion varies per shot, put it in the action section)
- Use generic terms ("nice outfit", "pretty face", "average build")

---

## Seedream 4 Alternative (Character-Based Accounts)

For creators building character-based accounts (fictional personas, mascots):
- **Seedream 4** can generate consistent character images from a single reference
- Use for building a character image library → feed to video models
- Workflow: Seedream 4 (character images) → Nano Banana (scene context) → Video model (animation)

---

*Sources: Mikoslab facial engineering framework (Plan A #3), OpenAI Sora Characters API documentation (Plan B #17). Combined for maximum model coverage.*
