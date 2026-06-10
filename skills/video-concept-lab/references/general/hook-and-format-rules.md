# Hook And Format Rules

Meta-first paid video concepts must define how the first second works visually and verbally.

## Hook Types

Every concept separates these fields:

```json
{
  "verbal_hook": "",
  "quiet_visual_hook": "",
  "rendered_text_hook": "",
  "subtitle_policy": "none | open-captions | platform-captions | rendered-text-only"
}
```

## Definitions

- `verbal_hook`: the spoken first line. Used for UGC, founder, VO, demo, and singing ads.
- `quiet_visual_hook`: a wordless visual interruption: impossible action, unusual setting, before/after reveal, product mechanism, gesture, facial reaction, prop transformation.
- `rendered_text_hook`: text that is intentionally part of the video image, such as a Snapchat-style strip, label, handwritten note, UI overlay, or bold center-frame caption.
- `subtitle_policy`: subtitles are accessibility/transcription captions. Rendered text is creative text. Do not confuse them.

## No-Dialogue Ads

No-dialogue ads must not include subtitles in the final version.

Allowed:
- Rendered text strips.
- UI overlays.
- Labels on props or screens.
- Single phrase cards.
- Sound design and music cues.

Required:
- State whether rendered text appears.
- State exact text if it appears.
- Ensure the visual narrative still makes sense without spoken words.

## Knob Separation

Use `references/general/concept-taxonomy.json` as the source of truth. The old one-word labels are not stable enough for an agency-wide API because they mix the ad's job, wrapper, style, proof, and script mode.

Use `references/general/format-prompt-recipes.md` when the user supplies a reusable prompt pattern. A recipe is a bundle of knobs plus a fillable prompt scaffold; it is not itself a `recommended_ad_format`.

| User Says | Store As |
|---|---|
| UGC | optional `format_recipe.recipe_id: "ugc_selfie_talking_head"`; `presentation_context: "ugc_creator"` or `"selfie_cam"`; choose `recommended_ad_format` by the narrative job |
| Podcast with B-roll | optional `format_recipe.recipe_id: "two_person_podcast_clip"`; `presentation_context: "podcast_clip"`, `creative_mechanism.type: "quote_to_broll_visualization"`, plus the right narrative format |
| Founder-led | `presentation_context: "founder_direct_address"` plus the right narrative format, often `"origin_story"`, `"teach_and_explain"`, or `"offer_invitation"` |
| Demo | usually `recommended_ad_format: "demo_walkthrough"`, `presentation_context: "product_demo_capture"`, and `proof_mode: "product_demonstration"` |
| Singing ad | `presentation_context: "performance_capture"`, `script_mode: "singing"`, and usually `creative_mechanism.type: "musical_hook_performance"` |
| No-dialogue ad | `script_mode: "no_dialogue"` and `subtitle_policy: "none"` |
| 2D animation / motion graphic | optional `format_recipe.recipe_id: "flat_2d_motion_graphic"`; usually `style_profile: "clean_motion_graphics"` |
| Claymation | optional `format_recipe.recipe_id: "handcrafted_claymation_scene"`; `style_profile: "handcrafted_claymation"` |
| Crochet style | optional `format_recipe.recipe_id: "handcrafted_crochet_diorama"`; `style_profile: "handcrafted_crochet"` |
| Testimonial | `recommended_ad_format: "testimony_or_experience"` or `"proof_case_study"` and `proof_mode: "customer_story"` or `"social_proof"` |
| VSL | usually `recommended_ad_format: "vsl_direct_response"`; use `"offer_invitation"`, `"teach_and_explain"`, or `"problem_agitation"` only when the direct-response arc is not the dominant structure |

Hard rule: do not save `ugc_voiceover`, `ugc_direct_to_camera`, `creator_education`, `founder_led`, `product_demo`, `testimonial`, `vsl`, `no_dialogue`, `singing_ad`, or `hybrid` as `recommended_ad_format`.

## Current Format Enum

Use only these `recommended_ad_format` ids:

- `problem_agitation`
- `teach_and_explain`
- `demo_walkthrough`
- `proof_case_study`
- `comparison_contrast`
- `offer_invitation`
- `origin_story`
- `scenario_dramatization`
- `testimony_or_experience`
- `vsl_direct_response`

## Hook Quality Bar

Score hooks on:
- Topic clarity in 3 seconds.
- Avatar match.
- Curiosity gap.
- Emotional pain or desire.
- Proof required.
- BS-detector risk.
- Visual support.
