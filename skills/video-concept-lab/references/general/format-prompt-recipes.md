# Format Prompt Recipes

Use this bank when the user supplies a reusable prompt shape such as UGC selfie, podcast clip, 2D animation, claymation, crochet, or another style they want to preserve.

A recipe is not a single taxonomy knob. It is a reusable bundle that fills multiple knobs and gives Video Factory a later prompt scaffold. Keep the taxonomy fields separate.

## Recipe Shape

```json
{
  "format_recipe": {
    "recipe_id": "",
    "recipe_label": "",
    "recipe_status": "draft | active | retired",
    "recipe_source": "user_supplied | reverse_engineered | internal",
    "knob_mapping": {
      "recommended_ad_format": "",
      "presentation_context": "",
      "style_profile": "",
      "angle_family": "",
      "creative_mechanism_type": "",
      "proof_mode": "",
      "script_mode": ""
    },
    "best_for": [],
    "avoid_when": [],
    "fill_requirements": [],
    "prompt_scaffold": ""
  }
}
```

## Current Recipes

### `ugc_selfie_talking_head`

Use for raw first-person credibility, buyer confession, direct-to-camera objection handling, and product routine stories.

Default knob mapping:

```json
{
  "recommended_ad_format": "testimony_or_experience",
  "presentation_context": "selfie_cam",
  "style_profile": "ugc_realism",
  "angle_family": "routine_friction",
  "creative_mechanism_type": "product_in_action_sequence",
  "proof_mode": "narrative_plausibility",
  "script_mode": "direct_to_camera"
}
```

Best for:
- Buyer says what changed in plain language.
- Routine-friction products.
- "I tried X and kept quitting" stories.
- Meta-first ads that need trust more than visual spectacle.

Prompt scaffold:

```text
[CHARACTER]: [age] year old [gender], [ethnicity], [hair], wearing [specific outfit], [realistic facial details].
[SETTING]: [specific lived-in location with visible imperfections].
[CAMERA]: selfie style, handheld, slight shake, phone held at arm's length, vertical 9:16.
[ACTION]: character looks into camera and says: "[8-10 seconds of natural speech]".
[LIGHTING]: natural window light, realistic shadows.
[MOOD]: casual, unscripted, like recording a story for a friend.
```

### `two_person_podcast_clip`

Use for authority contrast, expert conversation, belief reframe, and clipped discussion formats.

Default knob mapping:

```json
{
  "recommended_ad_format": "comparison_contrast",
  "presentation_context": "podcast_clip",
  "style_profile": "raw_documentary",
  "angle_family": "authority_gap",
  "creative_mechanism_type": "split_screen_contrast",
  "proof_mode": "authority_explanation",
  "script_mode": "dialogue"
}
```

Best for:
- American Doctor vs Japanese Doctor-style angles when softened into "same symptoms, different interpretation."
- Two-person debate, clinician conversation, or expert reaction formats.
- Ads that need cuts between wide shot, speaker close-up, listener reaction, and B-roll.

Prompt scaffold:

```text
[SCENE]: podcast studio, two people at a wooden table, professional microphones on boom arms.
[CHARACTER A]: [description].
[CHARACTER B]: [description].
[FRAMING]: medium two-shot plus close-ups of each speaker and reactions.
[CAMERA]: cut between wide two-shot, close-up A, close-up B, and over-shoulder.
[LIGHTING]: warm cinematic key lights, soft shadows, slight background bokeh.
[ACTION]: A says "[script]", B reacts naturally with nods, pauses, and micro-expressions.
```

### `flat_2d_motion_graphic`

Use for simple mechanism explanation, abstract belief shifts, educational diagrams, and no-real-person visual hooks.

Default knob mapping:

```json
{
  "recommended_ad_format": "teach_and_explain",
  "presentation_context": "brand_voiceover",
  "style_profile": "clean_motion_graphics",
  "angle_family": "mechanism_reveal",
  "creative_mechanism_type": "framework_reveal",
  "proof_mode": "process_walkthrough",
  "script_mode": "voiceover"
}
```

Best for:
- "Normal range vs how you feel" diagrams.
- Product mechanism simplification.
- Low-risk educational visualizations when real medical footage would imply too much.

Prompt scaffold:

```text
[STYLE]: 2D flat animation, [specific reference], [3-4 color palette].
[CHARACTER/SUBJECT]: [simple shape-based description].
[MOTION]: [animation principle, e.g. squash/stretch, stepped 12fps, ease in/out].
[SCENE]: beat 1..., beat 2..., beat 3...
[CAMERA]: static or defined pan/zoom.
[BACKGROUND]: minimal, [color], simple geometric shapes.
```

### `handcrafted_claymation_scene`

Use for tactile, playful, handmade product metaphors and scroll-stopping style tests.

Default knob mapping:

```json
{
  "recommended_ad_format": "scenario_dramatization",
  "presentation_context": "fictional_scene",
  "style_profile": "handcrafted_claymation",
  "angle_family": "product_format_upgrade",
  "creative_mechanism_type": "prop_metaphor",
  "proof_mode": "visual_comparison",
  "script_mode": "voiceover"
}
```

Best for:
- Turning routine friction into a simple physical metaphor.
- Product format stories where tactile contrast matters.
- Non-photoreal creative tests after product reference approval.

Prompt scaffold:

```text
[STYLE]: stop motion claymation, visible fingerprints, slight frame-to-frame inconsistency, 12fps choppy motion.
[CHARACTER]: clay figure of [description], exaggerated features, rough texture, slight asymmetry.
[SETTING]: miniature handmade set, visible cardboard/fabric/painted wood.
[MOTION]: deliberate jerky movement, slight wobble between frames.
[CAMERA]: locked off or slow dolly, macro lens feel.
[LIGHTING]: warm practical lights, visible shadows.
```

### `handcrafted_crochet_diorama`

Use for fully handmade yarn worlds, crochet product metaphors, and tactile miniature brand films.

Default knob mapping:

```json
{
  "recommended_ad_format": "scenario_dramatization",
  "presentation_context": "fictional_scene",
  "style_profile": "handcrafted_crochet",
  "angle_family": "product_format_upgrade",
  "creative_mechanism_type": "prop_metaphor",
  "proof_mode": "visual_comparison",
  "script_mode": "voiceover"
}
```

Best for:
- Crochet / knitted miniature scenes.
- Products that need memorable style more than literal UGC realism.
- Concepts where product treatment is approved to become a styled prop.

Prompt scaffold:

```text
[STYLE]: fully crocheted and knitted handmade miniature diorama world.
[MATERIAL RULE]: every surface, character, prop, product stand-in, hand, face, and background has visible yarn stitches and fabric loops.
[SCENE]: [specific miniature environment].
[ACTION]: [simple action with low hand complexity].
[LIGHTING]: [single motivated practical light].
[NEGATIVE]: no realistic skin, no smooth surfaces, no clay, no CGI plastic, no Disney/Pixar look.
```

## Rules

- Do not save recipe names as `recommended_ad_format`.
- Save recipe names in `format_recipe.recipe_id`.
- A recipe can suggest defaults, but the concept generator can override individual knobs when the concept requires it.
- If the user gives a new prompt style, first save it as `custom_style_profile` or a draft recipe. Promote it only after reuse or explicit approval.
- Product-inclusive recipes still require the product reference gate before image generation.
