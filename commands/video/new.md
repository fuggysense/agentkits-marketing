---
description: Scaffold a schema-1.0 video project without spending render credits
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [client] [video-slug]
---

## Contract

`/video:new <client> <slug>` initializes `clients/<client>/videos/<slug>-YYMMDD/` from the video project schema.

`/video:new-from-concept <client> <campaign> <concept-slug>` initializes a lightweight clip-run from an approved post-Video-Concept-Lab brief pack and stores it inside the source concept workspace at `clients/<client>/campaigns/<campaign>/video-concepts/<concept-slug>/06_generation-runs/<run-id>/`.

Standalone `/video:new` must:

- require an existing `clients/<client>/` folder
- write `lock.json` with `schema_version: "1.0"`
- seed `00-concept.md` from client research priority order
- scaffold `clips/`, `payloads/`, `review/`, and `stitch/`; create `stills/`, `beat-sheets/`, `motion-prompts/`, or `rerenders/` only when the selected workflow actually uses them
- intentionally leave the reserved `03-` slot empty
- rebuild `INDEX.md` with run status, clip list, review decisions, and stitch status

When importing from Video Concept Lab, `/video:new-from-concept` must:

- read `clients/<client>/campaigns/<campaign>/video-concepts/<concept-slug>/07_review/approval-2.json`
- refuse to create the video project unless Approval Gate 2 status is `approved`
- read `05_prompt-packs/video-factory-handoff.json`
- require the handoff to include `04_input-images/input-image-plan.json`, `05_prompt-packs/canonical-prompt-pack.json`, `05_prompt-packs/manual-run-guide.md`, and `05_prompt-packs/model-adapters/higgsfield-seedance.json`
- create the derived Video Factory run under `06_generation-runs/<run-id>/`, not `clients/<client>/videos/`
- write `lock.json.concept_source`
- write `00-concept.md` from the approved selected concept and reference the source workspace's `03_scripts/` and `05_prompt-packs/brief-pack/` files instead of duplicating them into the run
- write `run-manifest.json`, placeholder clip payloads, `review/review.json`, and `stitch/ffmpeg-command.sh`
- validate `video-brief.json.format.render_segment_cap_seconds <= 15`
- compute `lock.json.segments_count` and `lock.json.render_units` from the approved duration
- defer engine/style binding unless explicitly selected

It must not accept `approval-1.json` alone. Approval Gate 1 only approves the concept; Approval Gate 2 approves the client-facing brief and internal AI production brief.

## Local Runner

```bash
python3 scripts/video_pipeline.py new <client> <slug>
```

```bash
python3 scripts/video_pipeline.py validate-handoff <client> <campaign> <concept-slug>
python3 scripts/video_pipeline.py new-from-concept <client> <campaign> <concept-slug> --selected-concept <concept-id>
```

Example:

```bash
python3 scripts/video_pipeline.py new fuggysmedia test-dry-run-001
python3 scripts/video_pipeline.py validate-handoff takekine test_2 ferritin-normal-range-gap
python3 scripts/video_pipeline.py new-from-concept takekine test_2 ferritin-normal-range-gap --selected-concept c1
```
