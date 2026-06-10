# Output Schema

Return both Markdown and JSON when saving a run. Markdown is for human review; JSON is for downstream parsing.

## Markdown Sections

```markdown
# Video Concept Pack - <client> - <campaign>

## Context Summary

## Active Big Idea

## User Direction

## Five Concepts

## Client Concept Visuals

## V2V Scoring

## Recommended Winner

## Script / Visual Refinement Direction

## Avatar Approval Needed

## Initial Image / Style-Sheet Requirements

## Client Approval Questions

## Approval Gate 1

## Downstream Recommendation
```

## JSON Shape

```json
{
  "schema_version": "0.1",
  "client": "",
  "campaign": "",
  "platform_priority": "Meta",
  "concept_count": 5,
  "concept_taxonomy": {
    "taxonomy_version": "1.3",
    "taxonomy_reference": "skills/video-concept-lab/references/general/concept-taxonomy.json",
    "format_recipe_reference": "skills/video-concept-lab/references/general/format-prompt-recipes.md",
    "required_per_concept": [
      "campaign_specific_premise",
      "recommended_ad_format",
      "presentation_context",
      "style_profile",
      "angle_family",
      "creative_mechanism",
      "proof_mode",
      "script_mode",
      "format_recipe",
      "psychological_engine"
    ]
  },
  "source": {
    "existing_hook": "",
    "existing_user_idea": "",
    "context_files": [],
    "concept_brief": ""
  },
  "big_idea": {
    "big_idea_id": "",
    "status": "hypothesis | testing | proven | retired",
    "evidence_type": [],
    "claim_risk": "",
    "active_for_this_pack": true
  },
  "concepts": [
    {
      "concept_id": "",
      "title": "",
      "campaign_specific_premise": {
        "line": "",
        "problem_mechanism": "",
        "solution_mechanism": "",
        "promise": "",
        "proof_mode": ""
      },
      "recommended_ad_format": "problem_agitation | teach_and_explain | demo_walkthrough | proof_case_study | comparison_contrast | offer_invitation | origin_story | scenario_dramatization | testimony_or_experience | vsl_direct_response",
      "presentation_context": "ugc_creator | founder_direct_address | selfie_cam | studio_direct_address | podcast_clip | webinar_clip | interview_clip | screen_recording | product_demo_capture | performance_capture | brand_voiceover | fictional_scene | mixed_media_montage",
      "style_profile": "ugc_realism | clean_educational | premium_brand_realism | cinematic_realism | raw_documentary | clean_motion_graphics | playful_3d_animation | mascot_character | handcrafted_crochet | handcrafted_claymation | mixed_media_collage | custom_style_profile",
      "custom_style_profile_label": "",
      "custom_style_profile_definition": "",
      "angle_family": "status_quo_contrast | routine_friction | symptom_overlap | mechanism_reveal | belief_reframe | authority_gap | identity_validation | objection_reversal | product_format_upgrade | hidden_cost | risk_reframe | category_misconception | social_norm_shift",
      "creative_mechanism": {
        "type": "quote_to_broll_visualization | search_spiral | split_screen_contrast | before_after_reveal | checklist_countdown | teardown_overlay | diagnostic_quiz | framework_reveal | myth_bust_sequence | product_in_action_sequence | social_proof_montage | benchmark_line_shift | challenge_experiment | transformation_map | objection_flip_scene | receipt_cost_reveal | screen_audit | prop_metaphor | silent_visual_sequence | musical_hook_performance | roleplay_scene",
        "descriptor": "campaign-specific visible storytelling device"
      },
      "proof_mode": "product_demonstration | authority_explanation | customer_story | quantified_result | visual_comparison | screen_evidence | before_after_evidence | social_proof | process_walkthrough | third_party_validation | guarantee_or_risk_reversal | research_or_data_reference | narrative_plausibility",
      "script_mode": "voiceover | direct_to_camera | dialogue | singing | no_dialogue",
      "format_recipe": {
        "recipe_id": "ugc_selfie_talking_head | two_person_podcast_clip | flat_2d_motion_graphic | handcrafted_claymation_scene | handcrafted_crochet_diorama | custom_recipe | none",
        "recipe_label": "",
        "recipe_source": "user_supplied | reverse_engineered | internal | none",
        "knob_mapping": {
          "recommended_ad_format": "",
          "presentation_context": "",
          "style_profile": "",
          "angle_family": "",
          "creative_mechanism_type": "",
          "proof_mode": "",
          "script_mode": ""
        },
        "prompt_fill_notes": []
      },
      "psychological_engine": "One plain-English sentence explaining why the ad should work on the buyer."
    }
  ],
  "scores": [],
  "recommended_winner": {
    "concept_id": "",
    "reason": "",
    "required_edits_before_production": []
  },
  "script_direction": {
    "selected_concept_id": "",
    "script_mode": "voiceover | direct_to_camera | dialogue | singing | no_dialogue",
    "hook_direction": "",
    "voiceover_or_line_shape": "",
    "performance_notes": "",
    "music_or_sound_direction": "",
    "rendered_text_policy": "",
    "subtitle_policy": ""
  },
  "avatar_approvals": [],
  "target_video_frame": "9:16 vertical | 4:5 feed | 1:1 square | 16:9 landscape | custom",
  "pencil_sequence_sheet_policy": "flexible shot count; not capped at six shots",
  "client_concept_visuals": [
    {
      "concept_id": "",
      "production_design_guide_path": "",
      "pencil_sequence_sheet_path": ""
    }
  ],
  "client_approval_questions": [],
  "image_handoff": {
    "character_style_sheets": [],
    "product_style_sheets": [],
    "environment_sheets": [],
    "props_or_ui_sheets": [],
    "reference_image_policy": {
      "client_pack_visual": "production_design_guide_plus_pencil_sequence_sheet",
      "production_design_guide_frame": "art-direction board; may be landscape",
      "pencil_sheet_rows_equal": "first-pass shots or story beats",
      "pencil_sheet_frame": "must match target_video_frame",
      "pencil_sheet_shot_count": "flexible",
      "production_expansion_later": true
    }
  },
  "approval_gate_1": {
    "approval_file": "",
    "status": "pending",
    "required_before_brief_pack": true
  },
  "downstream": {
    "next_skill": "script-skill | video-brief-normalizer | ad-concept-engine",
    "notes": ""
  }
}
```

## Saved Folder Contract

```text
clients/<project>/campaigns/<campaign>/video-concepts/<slug>/
+-- pipeline-state.json
+-- artifact-manifest.json
+-- event-log.jsonl
+-- concept-brief.json
+-- 02_ag1-options/
|   +-- concept-pack.md
|   +-- concept-pack.html
|   +-- concept-pack.json
|   +-- approval-1.json
|   +-- script-direction.md
|   +-- client-concept-visuals/
|       +-- concept-01/
|       |   +-- production-design-guide.md
|       |   +-- pencil-sequence-sheet.md
|       +-- concept-02/
|       |   +-- production-design-guide.md
|       |   +-- pencil-sequence-sheet.md
|       +-- concept-03/
|           +-- production-design-guide.md
|           +-- pencil-sequence-sheet.md
+-- 04_input-images/
|   +-- input-references/
|   +-- image-handoff.md
```

Do not write `video-factory-handoff.json` in this stage. That file belongs to `video-brief-normalizer` after Approval Gate 2.

`concept-pack.html` is client-facing. It may show the five concepts, script/refinement direction, production design guides, pencil sequence sheets, reference-image implications, and approval questions. It must not expose CLI commands, render internals, or model-routing implementation details.

Default visual shell: `skills/common/templates/hazecraft-agency-wrapper.md`. Use it for HazeCraft agency/client-review artifacts unless the user explicitly requests a client-branded shell. The wrapper must not alter client/product reference assets or imply final client ad styling.

Client concept visuals are not Seedance production beat sheets. For the client pack, the production design guide defines the visual world and the pencil sequence sheet defines the first-pass shot/story flow. A later production beat sheet can expand an approved scene into many frames.

Every concept must keep premise, format, presentation, style, angle, mechanism, proof, script mode, and psychology separate:

- `campaign_specific_premise`: generated one-sentence ad hypothesis object.
- `recommended_ad_format`: hardcoded narrative-job enum from `references/general/concept-taxonomy.json`.
- `presentation_context`: hardcoded delivery-wrapper enum from `references/general/concept-taxonomy.json`.
- `style_profile`: hardcoded visual/tone enum from `references/general/concept-taxonomy.json`; `custom_style_profile` requires label and definition.
- `angle_family`: hardcoded reusable strategic-persuasion enum from `references/general/concept-taxonomy.json`.
- `creative_mechanism`: object with hardcoded type plus generated descriptor.
- `proof_mode`: hardcoded credibility-source enum from `references/general/concept-taxonomy.json`.
- `script_mode`: hardcoded script-execution enum from `references/general/concept-taxonomy.json`.
- `format_recipe`: optional reusable prompt scaffold from `references/general/format-prompt-recipes.md`; never use this as the ad format.
- `psychological_engine`: generated sentence explaining why the concept should work.

## Approval 1 JSON Shape

```json
{
  "schema_version": "1.0",
  "approval_stage": "concept",
  "client": "",
  "campaign": "",
  "concept_slug": "",
  "status": "pending | approved | rejected | needs_revision",
  "recommended_concept_id": "",
  "approved_concept_ids": [],
  "approved_at": null,
  "approved_by": null,
  "blocking_questions": [],
  "next_action_if_pending": "review concept-pack.html and client-concept-visuals/",
  "next_action_if_approved": "run script/visual refinement, then video-brief-normalizer"
}
```

## Downstream Brief-Pack Shape

After Approval Gate 1, the downstream stage should create:

```text
clients/<project>/campaigns/<campaign>/video-concepts/<slug>/
+-- 03_scripts/
|   +-- final-script.md
|   +-- visual-treatment.md
+-- 05_prompt-packs/
|   +-- brief-pack/
|   |   +-- google-docs-brief.md
|   |   +-- video-brief.md
|   |   +-- video-brief.json
|   +-- video-factory-handoff.json   # only after approval-2 is approved
+-- 07_review/
    +-- approval-2.json
```

See `skills/video-brief-normalizer/references/output-contract.md` for the Approval 2 and Video Factory handoff schema.
