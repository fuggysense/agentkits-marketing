# Concept Input Packet

Use a concept input packet whenever paid video concepts should inherit a proven, testing, or hypothesis angle.

The packet is the bridge between marketing strategy and concept generation. It prevents Video Concept Lab from reading a broad buyer profile and inventing weak structure.

When an audience-insights synthesis exists, use it before the broad buyer profile. The packet should carry the few research facts needed for the concept run, not the full research archive.

## Required Fields

```json
{
  "schema_version": "1.0",
  "client": "",
  "campaign": "",
  "primary_platform": "Meta",
  "big_idea": {
    "big_idea_id": "",
    "display_name": "",
    "status": "hypothesis | testing | proven | retired",
    "active_for_this_run": true,
    "evidence_type": ["our_judgment", "client_approval", "comments", "manual_performance_notes", "research_support"],
    "claim_risk": "low | medium | high",
    "core_tension": "",
    "allowed_expressions": [],
    "forbidden_expressions": []
  },
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
  "research_inputs": {
    "audience_synthesis_path": "",
    "agent_findings_paths": [],
    "raw_research_paths": [],
    "top_pain_points": [],
    "failed_solutions": [],
    "desired_outcomes": [],
    "objections": [],
    "misconceptions": [],
    "golden_nuggets": [],
    "research_gaps": []
  },
  "on_screen_persona": {
    "reuse_preference": "same_across_concepts | new_per_concept | flexible",
    "persona_policy": "same_as_buyer | adapted_buyer | authority | creator | fictional",
    "requires_user_approval": true
  },
  "offer_mechanism": "",
  "proof_hooks": [],
  "objection_map": [],
  "cta": {
    "destination_type": "soft | hard | retargeting | unknown",
    "destination": "",
    "action_text": "",
    "conversion_pressure": "low | medium | high",
    "notes": ""
  },
  "what_the_ad_must_do": "",
  "taxonomy_steering": {
    "allowed_recommended_ad_formats": [],
    "disallowed_recommended_ad_formats": [],
    "allowed_presentation_contexts": [],
    "disallowed_presentation_contexts": [],
    "allowed_style_profiles": [],
    "disallowed_style_profiles": [],
    "allowed_angle_families": [],
    "disallowed_angle_families": [],
    "allowed_creative_mechanism_types": [],
    "disallowed_creative_mechanism_types": [],
    "allowed_proof_modes": [],
    "disallowed_proof_modes": [],
    "allowed_script_modes": [],
    "disallowed_script_modes": []
  },
  "client_pack_visual_policy": {
    "visual_type": "production_design_guide_plus_pencil_sequence_sheet",
    "target_video_frame": "9:16 vertical | 4:5 feed | 1:1 square | 16:9 landscape | custom",
    "pencil_sequence_sheet_shot_count": "flexible; not capped at six shots",
    "one_row_equals": "one first-pass shot or story beat",
    "include_voiceover_or_script_per_frame": true,
    "production_expansion_later": true
  },
  "duration_target_seconds": 60
}
```

## Evidence Status

- `proven` means the market idea, emotional engine, or swipe pattern has enough internal evidence to anchor concepts.
- `proven` does not automatically mean every factual claim inside the angle is approved.
- Keep unsupported claim variants in `forbidden_expressions` or `needs_review`, even when the big idea itself is active.

## Research Input Rule

Use `research_inputs` to preserve where the concept came from. If the user later asks for more research or challenges a concept, open the cited audience synthesis and agent findings first. Do not make Concept Lab reload all `_brand/` documents or every legacy avatar file unless the cited research is insufficient.

## Output Rule

Save the normalized fields into workspace-root `concept-brief.json` so a no-context agent can generate a pack without reading the entire client archive. Existing `concept-input-packet.json` files are legacy aliases only.

## CTA Rule

Capture CTA destination before concept generation. A hard CTA such as buy, book, apply, or checkout requires a sharper premise, earlier proof, and stronger objection handling than a soft CTA such as learn more, watch, save, comment, or DM. If CTA is unknown, mark it as a blocker or keep `conversion_pressure: "medium"` and ask during Approval Gate 1.

## Duration Rule (no default)

`duration_target_seconds` is operator-declared per `concept-brief.json`. There is no default. The seeder + pack-builder MUST honor it as authoritative and route to the matching section in `video-compression-by-duration.md`.

Rung-lift budget per duration (from `video-compression-by-duration.md` master table):

| Duration | Rung-lift max | Best for |
|---|---|---|
| 15s | 0.5 (identity match) | Already at SL opening rung |
| 30s | 1 rung | 1 enemy + 1 reframe + simple mechanism |
| 45s | 1-2 rungs | 1 enemy + breathing room |
| 60s | 2 rungs (tight) | Solution-Aware × Stage-3 default — full 4 discrediting moves |
| 90s | 3 rungs | Unaware-lifting cold traffic |

**Decision rule:** if the concept needs 2+ enemies, 2+ reframes, or 2+ rung-lifts → minimum 60s. Forcing into 30s mutes Stage-4 moves. The brief's `duration_target_seconds` must reflect the actual concept demands, not Meta-convention defaults.

## Taxonomy Steering Rule

Only use `taxonomy_steering` to narrow or exclude enum choices from `references/general/concept-taxonomy.json`. Do not create campaign-specific enum values here. Put campaign-specific language in the persuasive premise, hook, creative mechanism descriptor, script, or claim constraints.

## Solution-Aware × Stage-3 Extension

**Mandatory when** `target_micro_persona.awareness_stage == "solution-aware"` AND `target_micro_persona.sophistication_level >= 3`.

When this gate fires, the existing `big_idea` block extends with 2 new fields, and a new top-level `credibility_stack` block appears as a peer to `proof_hooks`:

```json
{
  "big_idea": {
    "...existing fields": "...",
    "reframe_mechanism": "",
    "named_enemy": [
      {
        "tier": "category | institution | mechanism",
        "name": "",
        "schwartz_authenticity_verified": false,
        "role": "primary | secondary"
      }
    ]
  },
  "credibility_stack": [
    {
      "proof_type": "credentials | logical | implied | social | specificity | demonstration",
      "source": "",
      "strength": "high | medium | low"
    }
  ]
}
```

**Field definitions:**

- `big_idea.reframe_mechanism` — 1-sentence HOW it works, paired to the `big_idea.display_name`. Example for takekine Iron-Pill-Quitter: *"Bloodwork measures circulating iron; ferritin is the storage form. Most women run out of stores 8-12 weeks before labs catch it."* Source skills: `unique-mechanism-problem` and/or `unique-mechanism-solution`.
- `big_idea.named_enemy` — array (1-N items) of Common Enemy frames composed via `common-enemy-bridge.md`. Each item: `tier` ∈ {category, institution, mechanism}, `name`, `schwartz_authenticity_verified`, `role` ∈ {primary, secondary}. Exactly one item MUST have `role: "primary"`. Secondary enemies are optional and used to stack a second discrediting frame (e.g., primary attacks the mechanism, secondary attacks the category/format). For each item, `schwartz_authenticity_verified` should be `true` before the seeder accepts the packet (set true only after ≥10 spontaneous buyer mentions confirmed via Scout Mode). **Verification process options** (operator-declared per packet): (a) manual operator verification — paste evidence links into `schwartz_authenticity_evidence: [...]`; (b) auto-dispatch `scout-mode` skill on packet finalization; (c) trust-and-flag — operator declares boolean, AG1 surfaces it as a risk line. Process choice goes in `schwartz_authenticity_process: "manual | auto_scout | trust_and_flag"`.
- `credibility_stack` — array of 2-4 proof items, sourced from `.claude/references/copywriting-os/frameworks/six-proof-types.md` (6 named types) and built via `.claude/references/copywriting-os/builders/proof-inventory-builder.md`. This is structurally distinct from `proof_hooks` (free-form text) — credibility_stack enforces ≥2 different proof types layered on the same big_idea.

**Validation gate:** if `awareness_stage == "solution-aware"` AND `sophistication_level >= 3` AND any of {`big_idea.reframe_mechanism`, `big_idea.named_enemy` (array empty or no item has `role: "primary"`), `big_idea.named_enemy[primary].name`, `credibility_stack`} is missing or empty, the seeder MUST refuse the packet and surface the gap to the operator.

**Cross-loads** (auto-fired by routing-overrides V2-1):
- `skills/video-concept-lab/references/general/stage-4-discrediting.md`
- `skills/video-concept-lab/references/general/common-enemy-bridge.md`
- `.claude/references/copywriting-os/frameworks/six-proof-types.md` + `.claude/references/copywriting-os/reviewers/proof-density-audit.md`
