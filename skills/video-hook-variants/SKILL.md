---
name: video-hook-variants
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: content
difficulty: advanced
description: "Hook engineering for multi-clip paid video ads. Produces 2 paired hook variants per concept (clip_1A + clip_1B) — each variant is verbal (VO line) + visual (shot description) + rendered_text + subtitle_policy. Single-clip flows are refused. Dispatched by vid-director at Phase 2 via video-hook-variant-generator agent."
triggers:
  - hook
  - hooks
  - video hook
  - hook variants
  - hook audit
  - thumbstop
  - scroll-stopper
  - opening seconds
  - first frame
  - hook engineering
  - six-second hook
  - hook checklist
  - hook writing
related_skills:
  - video-concept-lab
  - script-skill
  - headline-bank
  - ad-concept-engine
output_schema: hook-variants-draft.json
---

# Video Hook Variants

Methodology for `video-hook-variant-generator` agent. In the v0.5+ pipeline this skill is the rubric/reference the agent reads — not a standalone hook writer. Dispatch `video-hook-variant-generator`; it reads this skill and writes `hook-variants-draft.json`.

## Boundary

**Owns:** hook engineering methodology; Visual / Text / Verbal layer alignment; Three-Element Checklist (Relatability / Sensationalism / Stakes); Four Horsemen audit; Modern W Order; Forbidden Openers; Six-Question Checklist; example bank by type and by element; A/B differentiation rules; Lego Brick Alignment.

**Does not own:** concept strategy (→ `video-concept-lab`); Meta primary text / headlines (→ `headline-bank`); beat sheets beyond clip_1 (→ `video-brief-normalizer`); rendering or production (→ `video-factory`).

## One-Line Summary

A hook is the first 1–5 seconds (ideally 3) of a video. Its only job: grab attention instantly and remove all friction so the viewer opts in and keeps watching. It does this by delivering crystal-clear **topic clarity** + **on-target curiosity** that makes the brain ask "what happens next?"

## Core Requirements (non-negotiable)

1. Grab attention — visual, text, or verbal/audio.
2. So simple a 6–7-year-old understands it in one second.
3. Zero friction — viewer immediately knows "this is for me and worth my time."

Both Topic Clarity AND On-Target Curiosity must pass. If either fails, nothing else about the hook matters.

## Three Hook Types — use ≥1, can combine all three

| Type | What it is | Example |
|---|---|---|
| **Visual** | What the eye sees first — scroll-stopper even with sound off | 400 slices of bread piled wall-to-wall |
| **Text** | On-screen text overlay (3–5 bold words, 0:00–0:02) — NOT subtitles | "POV: your mom's live reaction to you making $150k/month at 19" |
| **Verbal/Audio** | First words spoken — active voice, ≤14 words, hard down-tone | "This is how my bosses left their stable jobs to start a cereal company." |

Full framework: `references/frameworks/three-hook-types.md`
Examples: `references/examples/by-type/`

## Three Elements — hit ≥1, ideally 2–3

| Element | What it does |
|---|---|
| **Relatability** | Mass-audience mirror. Viewer thinks "that's me / that could be me." |
| **Sensationalism** | Huge contrast or extreme. Pattern interrupt. |
| **Stakes** | High risk, what's on the line. |

Pro move: all three together = nuclear hook. See `references/examples/combined/nuclear-hooks.md`.
Full framework: `references/frameworks/three-elements.md`

## Six-Question Checklist (run on every hook)

1. Is the topic crystal clear in ≤3 seconds?
2. Does it open an immediate curiosity gap?
3. Does it contain ≥1 of: Relatability / Sensationalism / Stakes?
4. Can a 6–7-year-old understand it?
5. Is value (visual/text/verbal) delivered in the first 1–2 seconds?
6. Does it create contrast (what people believe vs. what you're showing)?

Scoring: yes to 1–4 + ≥1 in #3 → strong. All three elements in #3 → elite.
Full checklist: `references/checks/six-question-checklist.md`

## Runtime Routing — load exactly one loadout

Read **two files only** before loading references:

1. `REFERENCE_GRAPH.json` — machine-readable loadout contract (single source of truth).
2. `INDEX.md` — human-readable loadout table.

Pick exactly one `methodology_loadout_id`. Load only that loadout's `required_nodes` plus triggered `conditional_nodes`. Do not bulk-load `references/`.

## Loadout Selection (quick reference)

| Intent | Loadout ID |
|---|---|
| Standard A/B hook pair | `standard_hook_variant` |
| All 3 elements required (elite bar) | `elite_hook_variant` |
| Multi-clip A/B paired production | `multi_clip_hook_pair` |
| Audit existing hooks, no generation | `hook_audit_only` |

## Context Load (dispatch)

The orchestrator must pass:
- `concepts-draft.json` path (from video-concept-seeder)
- `creative-diversity-map.json` path
- `concept-brief.json` (allowed_expressions, forbidden_expressions, claim_risk, language constraints)
- `multi_clip_flow: true` (refuse if false)
- Enumerated `_brand/*.md` files and `_swipe/winning-ads/*.marketing.md` files

## Output Contract

Write to `<concept-folder>/02_ag1-options/hook-variants-draft.json`. Return `methodology_receipt` with `methodology_loadout_id`, loaded files, skipped files, routing reason.

See `references/frameworks/` for all methodology files. See agent at `~/.claude/agents/video-hook-variant-generator.md` for dispatch rules.
