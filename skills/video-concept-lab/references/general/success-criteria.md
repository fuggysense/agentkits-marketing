# Video Concept Lab Success Criteria

Use this checklist before a concept pack is treated as ready for Approval Gate 1.

## Required Pass Criteria

- Five concepts are present unless the user explicitly requested a different count.
- Every concept inherits the same active `big_idea_id` unless the user asked to test multiple big ideas.
- Every concept includes the required taxonomy fields from `concept-taxonomy.json`: `campaign_specific_premise`, `recommended_ad_format`, `presentation_context`, `style_profile`, `angle_family`, `creative_mechanism`, `proof_mode`, `script_mode`, `format_recipe`, and `psychological_engine`.
- No deprecated format labels are saved as `recommended_ad_format`: `ugc_voiceover`, `ugc_direct_to_camera`, `creator_education`, `founder_led`, `product_demo`, `testimonial`, `vsl`, `no_dialogue`, `singing_ad`, or `hybrid`.
- The buyer micro-persona is stable and separate from the on-screen persona or visual character.
- Claim constraints are explicit: allowed claims, avoided claims, and claims needing review.
- Each concept has a scroll-stopping visual hook, verbal hook where relevant, rendered-text plan, and subtitle policy.
- `target_video_frame` is recorded before client concept visuals are created. If it was not inferable, the user was asked once.
- Each concept has two separate client concept visuals: `production-design-guide.md` and `pencil-sequence-sheet.md`.
- Each pencil sequence sheet uses shot number, shot size, angle, subject, description, voiceover/audio, and pencil thumbnail direction.
- Pencil sequence sheets match the target frame and use a flexible shot count rather than a fixed six-shot cap.
- Production design guides are treated as art-direction boards, so they do not need to match the target video frame unless the user explicitly asks for that.
- Each concept states initial character, product, environment, prop/UI, and style-reference needs.
- The recommended winner has script/refinement direction appropriate to `script_mode`.
- `script_mode: "no_dialogue"` uses `subtitle_policy: "none"`.
- `script_mode: "singing"` includes a musical premise and music direction.
- Hard-number, medical, legal, financial, or quantified proof is backed by approved evidence or marked as blocked.
- `approval-1.json` exists with `status: "pending"` when saving a run.
- The output does not create Video Factory handoff files, production beat sheets, render prompts, Higgsfield commands, or API calls.

## Scoring Bar

Score each concept from 1-10 on:

- Scroll-stop velocity.
- Emotional impact.
- Narrative clarity.
- Shareability.
- Conversion potential.
- Video Studio feasibility.

Minimum bar for a production candidate:

- Total score at least 42/60.
- No individual score below 6.
- Recommended winner at least 48/60, or the pack must explain why a lower-scoring concept is strategically preferred.

## Failure Conditions

- The pack uses a wrapper label like UGC, podcast, founder, singing, or no-dialogue as the narrative format.
- The pack confuses buyer micro-persona with on-screen persona or visual character.
- All five concepts reuse the same visual structure with only wording changes.
- The concept depends on an unapproved product reference or claim without flagging it as a blocker.
- The pencil sequence sheet defaults to six shots when the concept clearly needs more beats.
- The concept pack tries to skip Approval Gate 1 and move directly to Video Factory, Beat Sheet Director, or rendering.
- The concept pack labels client pencil sequence sheets as production Beat Sheet Director outputs.
