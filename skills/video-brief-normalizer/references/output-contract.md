# Video Brief Pack Output Contract

Use this contract after Video Concept Lab Approval Gate 1 and script/visual refinement. In Option B, this brief contract is part of the larger AG2 prompt/input package; AG2 is incomplete unless the input-image plan, canonical prompt pack, model adapters, and manual run guide also exist.

## Client-Facing Google Docs Brief

Save as `05_prompt-packs/brief-pack/google-docs-brief.md`.

Required sections:

```markdown
# Video Brief - <client> - <campaign>

## What We Are Producing

## Approved Concept

## Hook

## Final Script

## Visual Direction

## Approved Concept Visuals

## Deliverables

## Style And Format

## Assets Or References Needed From Client

## Approval Notes
```

Rules:

- Show only the approved winner.
- Do not include internal model prompts, CLI flags, render commands, or reference-order mechanics.
- Make it suitable to paste into Google Docs for client review.

## Internal Video Brief Markdown

Save as `05_prompt-packs/brief-pack/video-brief.md`.

Required sections:

```markdown
# Internal AI Video Brief - <client> - <campaign>

## Source Files

## Approved Concept

## Final Hook And Script

## Scene Plan

## Visual Treatment

## Visual Ground Truth Inputs

## Input Asset Requirements

## Style Sheet Requirements

## Reference Order

## Model Assumptions

## Open Blockers

## Video Factory Readiness
```

Rules:

- This is the internal execution contract for Video Factory.
- It may include model assumptions, reference order, and render-segment planning.
- It must not contain final Higgsfield commands or render prompts.

## Internal Video Brief JSON

Save as `05_prompt-packs/brief-pack/video-brief.json`.

```json
{
  "schema_version": "1.0",
  "brief_type": "ai-video-production-brief",
  "client": "",
  "campaign": "",
  "concept_slug": "",
  "selected_concept_id": "",
  "platform_priority": "Meta",
  "production_mode": "ai_video_only",
  "approval": {
    "approval_1_file": "",
    "approval_1_status": "approved",
    "approval_2_file": "07_review/approval-2.json",
    "approval_2_status": "pending"
  },
  "taxonomy": {
    "taxonomy_version": "1.3",
    "taxonomy_reference": "skills/video-concept-lab/references/concept-taxonomy.json",
    "format_recipe_reference": "skills/video-concept-lab/references/general/format-prompt-recipes.md",
    "campaign_specific_premise": {
      "line": "",
      "problem_mechanism": "",
      "solution_mechanism": "",
      "promise": "",
      "proof_mode": ""
    },
    "recommended_ad_format": "",
    "presentation_context": "",
    "style_profile": "",
    "angle_family": "",
    "creative_mechanism": {
      "type": "",
      "descriptor": ""
    },
    "proof_mode": "",
    "script_mode": "",
    "format_recipe": {
      "recipe_id": "",
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
    "psychological_engine": ""
  },
  "format": {
    "recommended_ad_format": "",
    "aspect_ratio": "9:16",
    "duration_seconds_estimate": 45,
    "render_segment_cap_seconds": 15,
    "segments_count": 3
  },
  "hook": {
    "verbal_hook": "",
    "quiet_visual_hook": "",
    "rendered_text_hook": "",
    "subtitle_policy": ""
  },
  "script": {
    "script_mode": "voiceover | direct_to_camera | dialogue | singing | no_dialogue",
    "script_type": "voiceover | avatar-acting | singing | no-dialogue",
    "final_script_markdown_path": "03_scripts/final-script.md",
    "visual_treatment_path": "03_scripts/visual-treatment.md"
  },
  "approved_concept_visuals": {
    "production_design_guide": {
      "path": "",
      "role": "look_and_asset_truth",
      "status": "approved_at_gate_1"
    },
    "pencil_sequence_sheet": {
      "path": "",
      "role": "story_flow_truth",
      "status": "approved_at_gate_1",
      "required_columns": [
        "shot_number",
        "shot_size",
        "angle",
        "subject",
        "description",
        "voiceover_or_audio",
        "pencil_thumbnail"
      ]
    }
  },
  "scene_plan": [],
  "input_asset_requirements": {
    "character_style_sheets": [],
    "product_style_sheets": [],
    "environment_sheets": [],
    "style_reference_sheets": [],
    "props_or_ui_sheets": [],
    "audio_references": [],
    "video_references": []
  },
  "reference_order": [
    {
      "alias": "@Image1",
      "role": "production_design_guide_or_visual_world_reference",
      "source": "generated_from_approved_concept_visuals_after_approval_2",
      "required": true
    },
    {
      "alias": "@Image2",
      "role": "ten_frame_sheet_or_beat_sheet_director_scene_sheet",
      "source": "generated_from_approved_pencil_sequence_sheet_after_approval_2",
      "required": true
    },
    {
      "alias": "@Image3",
      "role": "input_image_hero_start_frame_product_sheet_or_character_sheet",
      "source": "generated_or_user_supplied_after_approval_2",
      "required": false
    }
  ],
  "model_assumptions": {
    "default_renderer": "seedance-2.0",
    "engine_selection_status": "deferred_until_input_assets_are_approved",
    "seedance_first": true,
    "higgsfield_render_allowed": false
  },
  "open_blockers": [],
  "ready_for_video_factory": false
}
```

## Approval 2 JSON

Save as `07_review/approval-2.json`.

```json
{
  "schema_version": "1.0",
  "approval_stage": "brief-pack",
  "client": "",
  "campaign": "",
  "concept_slug": "",
  "status": "pending | approved | rejected | needs_revision",
  "selected_concept_id": "",
  "approved_concept_ids": [],
  "approved_at": null,
  "approved_by": null,
  "approved_files": {
    "google_docs_brief": "05_prompt-packs/brief-pack/google-docs-brief.md",
    "video_brief_markdown": "05_prompt-packs/brief-pack/video-brief.md",
    "video_brief_json": "05_prompt-packs/brief-pack/video-brief.json",
    "final_script": "03_scripts/final-script.md",
    "visual_treatment": "03_scripts/visual-treatment.md",
    "input_image_plan": "04_input-images/input-image-plan.json",
    "canonical_prompt_pack": "05_prompt-packs/canonical-prompt-pack.json",
    "manual_run_guide": "05_prompt-packs/manual-run-guide.md",
    "higgsfield_seedance_adapter": "05_prompt-packs/model-adapters/higgsfield-seedance.json"
  },
  "blocking_questions": [],
  "next_action_if_pending": "review scripts, input-image plan, canonical prompt pack, model adapters, manual run guide, google-docs-brief.md, video-brief.md, and video-brief.json",
  "next_action_if_approved": "write 05_prompt-packs/video-factory-handoff.json and run /video:new-from-concept"
}
```

## Video Factory Handoff

Write `05_prompt-packs/video-factory-handoff.json` only after Approval 2 is approved.

```json
{
  "schema_version": "1.0",
  "handoff_type": "video-brief-normalizer-to-video-factory",
  "client": "",
  "campaign": "",
  "concept_slug": "",
  "approval": {
    "status": "approved",
    "approval_file": "07_review/approval-2.json",
    "required_before_video_project": true
  },
  "source_files": {
    "concept_pack_markdown": "02_ag1-options/concept-pack.md",
    "concept_pack_json": "02_ag1-options/concept-pack.json",
    "final_script": "03_scripts/final-script.md",
    "visual_treatment": "03_scripts/visual-treatment.md",
    "google_docs_brief": "05_prompt-packs/brief-pack/google-docs-brief.md",
    "video_brief_markdown": "05_prompt-packs/brief-pack/video-brief.md",
    "video_brief_json": "05_prompt-packs/brief-pack/video-brief.json",
    "input_image_plan": "04_input-images/input-image-plan.json",
    "input_image_plan_markdown": "04_input-images/input-image-plan.md",
    "canonical_prompt_pack_json": "05_prompt-packs/canonical-prompt-pack.json",
    "canonical_prompt_pack_markdown": "05_prompt-packs/canonical-prompt-pack.md",
    "manual_run_guide": "05_prompt-packs/manual-run-guide.md",
    "manual_any_model_adapter": "05_prompt-packs/model-adapters/manual-any-model.md",
    "higgsfield_seedance_adapter": "05_prompt-packs/model-adapters/higgsfield-seedance.json",
    "production_design_guide": "02_ag1-options/client-concept-visuals/<selected-concept>/production-design-guide.md",
    "pencil_sequence_sheet": "02_ag1-options/client-concept-visuals/<selected-concept>/pencil-sequence-sheet.md"
  },
  "selected_concepts": [],
  "model_agnostic_render_intent": {
    "platform_priority": "Meta",
    "aspect_ratio": "9:16",
    "duration_seconds_estimate": 45,
    "recommended_ad_format": "",
    "presentation_context": "",
    "style_profile": null,
    "angle_family": "",
    "creative_mechanism": {
      "type": "",
      "descriptor": ""
    },
    "proof_mode": "",
    "script_mode": "",
    "use_case": "ugc-ad",
    "truth_source": "UGC PHONE",
    "mode": "cut-montage",
    "style_reference_mode": "derive_from_approved_input_assets_and_concept_notes"
  },
  "input_asset_requirements": {},
  "engine_selection": {
    "status": "deferred_until_input_assets_and_beat_sheet_are_approved",
    "candidate_engines": ["seedance-2.0"],
    "do_not_bind_to_engine_yet": true
  },
  "gates": [
    "input-image-prompt-review",
    "input-image-approval",
    "beat-sheet-approval",
    "render-prompt-approval",
    "higgsfield-render-approval"
  ],
  "resume_instructions": []
}
```

## Reference Order Rules

- Seedance-first default after Approval 2: `@Image1` is the production design guide or visual-world reference, `@Image2` is the 10-frame look-and-story-flow sheet or Beat Sheet Director scene sheet, and `@Image3` is the optional hero/start frame, product sheet, character sheet, or style sheet needed for that render.
- Kling 3.0 and SeedDance 1.5 primarily use input images as start-frame and optional end-frame anchors; Video Factory decides those image roles after Approval 2.
- Do not create sparse image aliases. If `@Image2` is omitted, do not jump to `@Image3`; renumber or require the missing asset.
- Start/end frames are Video Factory decisions for models that require them, not fields in this normalizer's schema.
- No Higgsfield render prompt or CLI command is created in this stage.
- Render prompts must explicitly state how every uploaded reference should be followed. If a prompt mentions `@ImageN` without defining what that reference controls, it fails the handoff.
