# Context Pack

Build a compact context pack before generating concepts. Do not paste full client documents into every worker if a short extract is enough.

## Load Order

1. `context-profile.json`
   - Business name, offer, vertical, competitors, target audience, objections, benefits, assets link, brand constraints.
2. Latest `01_research/output/*audience-insights-synthesis.md`
   - Priority buyer-language synthesis: pain points, failed solutions, desired outcomes, objections, misconceptions, Reddit/forum quotes, key personas, claim-sensitive language, research gaps.
3. `source-of-truth.md`
   - Core message, priority angles, hook library, pain/objection/proof, buyer language, Golden Nuggets, misconceptions.
4. `_brand/big-ideas/`
   - Active hypotheses, testing angles, proven angles, retired angles, evidence type, claim risk, and allowed/forbidden expressions.
5. Selected micro-persona from `_brand/buyer-profile.md#micro-persona-map`
   - Awareness level, sophistication level, primary emotion, buying trigger, raw inner dialogue, desired transformation, relationship impact, and market behavior. Load one selected micro-persona. Load `_brand/visual-characters/` only when the work needs a generated presenter, mascot, recurring face, or actor reference.
6. Workspace-root `concept-brief.json`; older `campaigns/<campaign>/01_research/output/concept-input-packet*.json` files are legacy migration inputs only
   - Tight execution packet for the current concept run.
7. `angles/`
   - Current wave angles, prior winners, saturated angles, kill list, hook library, iteration log.
8. `learnings.md`
   - Client-specific mistakes, winning creative patterns, forbidden claims, tone corrections.
9. `_swipe/winning-ads/`
   - Proven hooks, scripts, creative structures, emotional engines, compliance risks, and reuse notes.
10. Brand assets and proof assets
   - Product shots, founder/customer proof, testimonials, screenshots, case studies, approved claims.

If the user asks for more research, first open the latest audience synthesis and the exact `01_research/output/agent-findings/` files it cites. Only launch new research when those files do not answer the question.

## Context Pack Shape

```json
{
  "client": "",
  "campaign": "",
  "offer": "",
  "primary_platform": "Meta",
  "objective": "",
  "big_idea": {
    "big_idea_id": "",
    "status": "hypothesis | testing | proven | retired",
    "evidence_type": [],
    "core_tension": "",
    "allowed_expressions": [],
    "forbidden_expressions": [],
    "claim_risk": ""
  },
  "audience_synthesis": {
    "path": "",
    "research_density": "",
    "top_pain_points": [],
    "failed_solutions": [],
    "desired_outcomes": [],
    "objections": [],
    "misconceptions": [],
    "golden_nuggets": [],
    "research_gaps": []
  },
  "concept_brief_path": "",
  "target_micro_persona": {
    "micro_persona_id": "",
    "buyer_profile_path": "_brand/buyer-profile.md",
    "name": "",
    "awareness": "",
    "sophistication": "",
    "primary_emotion": "",
    "raw_inner_dialogue": [],
    "desired_transformation": ""
  },
  "approved_claims": [],
  "forbidden_claims": [],
  "proof_assets": [],
  "priority_angles": [],
  "existing_hooks": [],
  "winning_swipes": [],
  "saturated_patterns": [],
  "brand_voice": "",
  "visual_constraints": [],
  "existing_user_idea": ""
}
```

## Concept Input Packet

Build this before concepts when the user wants paid video concepts anchored to a known angle.

Required fields:

```json
{
  "big_idea_id": "",
  "big_idea_status": "hypothesis | testing | proven | retired",
  "evidence_type": ["our_judgment", "client_approval", "comments", "manual_performance_notes"],
  "target_micro_persona": {
    "micro_persona_id": "",
    "buyer_profile_path": "_brand/buyer-profile.md",
    "job_to_be_done": "",
    "desired_outcome": "",
    "pain_state": "",
    "current_workaround": "",
    "why_now": "",
    "awareness_stage": "",
    "sophistication_level": ""
  },
  "on_screen_persona": {
    "persona_type": "same_as_buyer | adapted_buyer | authority | creator | fictional",
    "reuse_preference": "same_across_concepts | new_per_concept | flexible",
    "approval_required": true
  },
  "offer_mechanism": "",
  "proof_hooks": [],
  "objection_map": [],
  "angle_constraints": {
    "allowed": [],
    "avoid": [],
    "claim_risk": []
  },
  "what_the_ad_must_do": "",
  "reference_image_policy": {
    "client_pack_visual": "client_scene_beat_sheet",
    "one_frame_equals": "one scene",
    "production_expansion_later": true
  }
}
```

## Missing Context Rule

Ask only for missing fields that block concept quality:
- What is the offer?
- Which active big idea should all five concepts inherit?
- Which buyer micro-persona is this for?
- Should the on-screen visual character stay the same across concepts, change per concept, or stay flexible?
- What action should the viewer take?
- What proof can we safely show?
- Which format direction do you want to explore?
