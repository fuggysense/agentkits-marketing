---
name: video-brief-normalizer
version: "0.1.0"
brand: AgentKits Marketing by AityTech
category: content
difficulty: advanced
description: "Bridge component: approved Video Concept Lab winner → client Google Docs brief + internal AI production brief. In Option B it feeds video-prompt-pack-builder, which owns the full AG2 prompt/input package. NOT for upstream ideation, parsing, images, beat sheets, or Meta copy."
triggers:
  - video brief normalizer
  - normalize video brief
  - google docs video brief
  - client-facing video brief
  - AI video production brief
  - video factory handoff
  - approval gate 2
related_skills:
  - video-concept-lab
  - script-skill
  - video-factory
output_schema: video-brief-pack
---

# Video Brief Normalizer

Video Brief Normalizer converts an approved Video Concept Lab winner plus refined script and visual treatment into two production-ready briefs used by the full AG2 prompt/input package:

1. A client-facing `google-docs-brief.md`.
2. An internal AI production contract, `video-brief.md` and `video-brief.json`.

It is not an intake parser. Do not use it before Video Concept Lab. It runs only after Approval Gate 1 and script/visual refinement.

In the unified Option B system, this skill is a subroutine of `video-prompt-pack-builder`. A complete AG2 package is not approved until these also exist: `04_input-images/input-image-plan.{json,md}`, `05_prompt-packs/canonical-prompt-pack.{json,md}`, `05_prompt-packs/model-adapters/`, `05_prompt-packs/manual-run-guide.md`, and `07_review/approval-2.json`.

## Inputs

Required:

- `02_ag1-options/concept-pack.md`
- `02_ag1-options/concept-pack.json`
- `02_ag1-options/approval-1.json` with `status: approved`
- `03_scripts/final-script.md`
- `03_scripts/visual-treatment.md`

Useful:

- `image-handoff.md` from Video Concept Lab
- approved concept visual docs: `client-concept-visuals/concept-XX/production-design-guide.md` and `client-concept-visuals/concept-XX/pencil-sequence-sheet.md`
- client context and approved assets
- selected style profile notes
- product URLs or source references already approved for this concept

## Workflow

1. Verify Approval Gate 1 is approved.
2. Load only the selected winning concept from `02_ag1-options/concept-pack.json`.
3. Read `03_scripts/final-script.md`, `03_scripts/visual-treatment.md`, and the selected concept's production design guide + pencil sequence sheet as the production source of truth.
4. Create `05_prompt-packs/brief-pack/google-docs-brief.md` for client review. Do not include CLI flags, model internals, or render commands.
5. Create `05_prompt-packs/brief-pack/video-brief.md` and `05_prompt-packs/brief-pack/video-brief.json` for AI execution. Include hooks, script, scene timing, visual-ground-truth inputs, asset requirements, style-sheet requirements, model assumptions, reference order, and blockers.
6. Hand off to `video-prompt-pack-builder` or continue under that agent to create `04_input-images/input-image-plan.{json,md}`, `05_prompt-packs/canonical-prompt-pack.{json,md}`, `05_prompt-packs/model-adapters/`, and `05_prompt-packs/manual-run-guide.md`.
7. Create `07_review/approval-2.json` with `status: pending` only after the full prompt/input package exists.
8. Do not create `05_prompt-packs/video-factory-handoff.json` until Approval Gate 2 is approved.
9. After Approval Gate 2 is approved, write `05_prompt-packs/video-factory-handoff.json` from the approved video brief and prompt pack.

See `references/output-contract.md`.

## Audience Split

The client-facing brief answers:

- What are we making?
- What is the hook and script?
- What will the viewer see?
- What style, format, and deliverables are approved?
- What does the client need to approve?

The internal normalized brief answers:

- What input images are required?
- Which production design guide and pencil sequence sheet are approved?
- Which style sheets are required?
- Which scenes and timing blocks exist?
- Which references map to `@Image1`, `@Image2`, `@Image3`, `@VideoN`, or `@AudioN`?
- Which assumptions are deferred to Video Factory?
- What blocks input-image prompt generation?

## Boundaries

Owns:

- Client-facing Google Docs source brief.
- Internal AI production brief.
- Brief sections of the AG2 package.

Does not own alone:

- The complete AG2 package. `video-prompt-pack-builder` owns scripts, input-image plan, canonical prompt pack, model adapters, manual run guide, Approval Gate 2, and Video Factory handoff.

Optional HTML presentation: when the user asks for a designed client brief or review page, use `skills/common/templates/hazecraft-agency-wrapper.md` as the default HazeCraft agency shell. Keep `05_prompt-packs/brief-pack/google-docs-brief.md`, `05_prompt-packs/brief-pack/video-brief.md`, `05_prompt-packs/brief-pack/video-brief.json`, and `07_review/approval-2.json` as the source of truth; HTML is a presentation layer only.

Does not own:

- Concept generation.
- Meta primary text or headlines.
- Final image prompts.
- Beat sheets.
- Render prompts.
- Higgsfield CLI calls.

## Output Location

Use the same Video Concept Lab output folder:

```text
clients/<project>/campaigns/<campaign>/video-concepts/<slug>/
+-- 03_scripts/
|   +-- final-script.md
|   +-- visual-treatment.md
+-- 04_input-images/
|   +-- input-image-plan.json
|   +-- input-image-plan.md
+-- 05_prompt-packs/
|   +-- brief-pack/
|   |   +-- google-docs-brief.md
|   |   +-- video-brief.md
|   |   +-- video-brief.json
|   +-- canonical-prompt-pack.json
|   +-- canonical-prompt-pack.md
|   +-- manual-run-guide.md
|   +-- model-adapters/
|   |   +-- manual-any-model.md
|   |   +-- higgsfield-seedance.json
|   +-- video-factory-handoff.json   # only after approval-2 is approved
+-- 07_review/
    +-- approval-2.json
```

## Validation

Before writing a Video Factory handoff, verify:

- Approval Gate 1 is approved.
- Approval Gate 2 is approved.
- `03_scripts/final-script.md`, `03_scripts/visual-treatment.md`, `04_input-images/input-image-plan.json`, `05_prompt-packs/brief-pack/google-docs-brief.md`, `05_prompt-packs/brief-pack/video-brief.md`, `05_prompt-packs/brief-pack/video-brief.json`, `05_prompt-packs/canonical-prompt-pack.json`, `05_prompt-packs/model-adapters/higgsfield-seedance.json`, and `05_prompt-packs/manual-run-guide.md` exist.
- `video-brief.json.duration_seconds_estimate < 60` uses max 15s render segments.
- Seedance-first references are ordered with no sparse image aliases.
- No Higgsfield render prompt or command exists yet.

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[video-concept-lab]] (skill, 0.21)

<!-- skill-graph:end -->
