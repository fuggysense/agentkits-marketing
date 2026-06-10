# AG1 Card Template — Locked Structure

> **Status:** LOCKED 2026-05-23 by operator. Every AG1 review page rendered via `html-publisher` MUST follow this card structure. Future changes require operator sign-off + version bump.
>
> **Consumed by:** `html-publisher` (as `structure_brief_ref`), `video-prompt-pack-builder` (as the script-drafts.json output contract guide), vid-director orchestrator (when assembling AG1 task envelopes).

## Why this template exists

The pre-lock AG1 surface mixed verbatim voice-over with narrative prose. Operators couldn't tell what the actor literally says vs. what the concept describes. This template separates the two by enforcing a per-scene table where voice-over lives in a dedicated quoted cell.

## Card anatomy (one card per concept)

```
┌─ Concept Header ──────────────────────────────────────────────┐
│ • Concept ID (e.g., c01)                                      │
│ • Title                                                       │
│ • Recommended? (badge if yes)                                 │
│ • Micro-persona ID + one-line description                     │
│ • Awareness × Sophistication (e.g., "Solution-Aware × L3")    │
│ • Format / workflow_flow (e.g., cartoon-flow, ugc-flow)       │
│ • Spine (one sentence — the through-line)                     │
└───────────────────────────────────────────────────────────────┘

┌─ "Why this lands now" block (replaces "Stage 4 Move") ────────┐
│ One paragraph, plain English. Names what the buyer has tried, │
│ why it failed, and how this concept reframes the mechanism.   │
│ This is the discredit-and-reintroduce move, told without      │
│ Schwartz jargon.                                              │
└───────────────────────────────────────────────────────────────┘

┌─ Scene Table (5 columns — LOCKED) ────────────────────────────┐
│ # │ Time   │ Visual / Direction │ Voice-over (quoted) │ Purpose
│ 1 │ 0-3s   │ ...                │ "..."               │ Hook
│ 2 │ 3-7s   │ ...                │ "..."               │ Discredit
│ 3 │ 7-11s  │ ...                │ "..."               │ Proof
│ 4 │ 11-15s │ ...                │ "..."               │ Payoff
└───────────────────────────────────────────────────────────────┘

┌─ Hook Variants block (only if multiple) ──────────────────────┐
│ For concepts with multiple opening hooks (e.g., c02 has 3,    │
│ c03 sung has δ + ε):                                          │
│ • Hook ID                                                     │
│ • Verbal (VO line, quoted)                                    │
│ • Visual (one-line shot description)                          │
│ • Rendered text on screen (if any)                            │
│ • Subtitle policy                                             │
│ • "Pick this hook" chip → records decision to approval-1.json │
└───────────────────────────────────────────────────────────────┘

┌─ Suno Brief Callout (c03 sung concepts ONLY) ─────────────────┐
│ Sidebar (not a table column). Contains:                       │
│ • Genre / vibe target                                         │
│ • Tempo + key                                                 │
│ • Vocal performance note                                      │
│ • Bridge-delivery note (spoken outro handoff if any)          │
│ • Lyric variants list (e.g., δ / ε) with "Pick δ" chip per    │
└───────────────────────────────────────────────────────────────┘

┌─ Approval CTA (always last) ──────────────────────────────────┐
│ Single recommended action button (red, per HazeCraft wrapper):│
│ "Approve c0X" → writes approval-1.json status                 │
│ Secondary actions: "Request revision", "Kill concept"         │
└───────────────────────────────────────────────────────────────┘
```

## Scene Table — column rules (LOCKED)

| Col | Header | Type | Rules |
|---|---|---|---|
| 1 | `#` | int | Sequential 1..N. Never skip. |
| 2 | `Time` | range | `Xs-Ys` format. Total across all scenes MUST equal `concept-brief.json.duration_target_seconds`. |
| 3 | `Visual / Direction` | prose | What we see: subject, framing, lighting, action. Camera notes optional. **On-screen text is OPTIONAL** — render as parenthetical inside this cell only when the concept actually calls for text overlay (typically hook + payoff only for DTC product ads). Format: `Subject doing thing, framing, lighting. (on-screen text: "Take Kine")`. If no text, omit the parenthetical entirely — do NOT write `(on-screen text: none)`. |
| 4 | `Voice-over (quoted)` | quoted string | The literal words the actor / VO talent says. Must be in double quotes. If a scene is non-verbal, leave the cell as an em-dash (`—`). NEVER put narrative prose, "quote-unquote" phrasing, or VO direction here. Direction goes in column 3. |
| 5 | `Purpose` | enum | One of: `Hook`, `Setup`, `Discredit`, `Mechanism`, `Proof`, `Authority`, `Payoff`, `CTA`. (v1.1 — extended 2026-05-23 per operator + Iman.) Used by evaluators to check beat coverage. **Mechanism** = the how-it-works reveal (distinct from `Discredit` which names the failure). **Authority** = expert/clinician/doctor handoff (distinct from `Proof` which is testimonial/data/before-after). Outro NOT added — per Iman: "Outro is usually just CTA-adjacent coda; unless training people to distinguish rhetorical landing from transactional close, doesn't change the work." Rhetorical/reflective closes remain tagged `CTA` with the understanding that the on-screen card carries the transactional handoff. |

## Why columns are exactly 5

- **Lean:** Fast taste-pass for the operator at AG1. 5 cols fits comfortably on a laptop screen without horizontal scroll.
- **Production-ready:** Voice-over + direction + purpose is enough for the pack-builder to produce model adapters at Phase 6 without re-asking the operator.
- **No empty columns:** On-screen text was rejected as a standalone column because most DTC ads only carry text at hook + payoff. Forcing a column would render empty cells for 60-80% of scenes. Inline parenthetical in column 3 keeps the page dense.

## Voice-over source of truth (LOCKED)

- The scene-table cell is the single source of truth for VO. Never duplicate VO into prose elsewhere on the card.
- For sung concepts (c03), the table cell holds the **lyric line for that scene** (quoted), and the Suno brief callout holds the music/genre direction. Lyrics are not duplicated in the Suno sidebar.

## "Why this lands now" block (replaces "Stage 4 Move")

- One paragraph, plain English, 2-4 sentences.
- Names: (1) what the buyer has tried, (2) why it didn't work, (3) how this concept reframes the mechanism.
- No Schwartz citation, no "Stage 4 sophistication" language. Internal jargon stays internal.
- Read by `eval-buyer-fit` to verify the Stage-3/4 discredit move is doing its job for the declared micro-persona.

## What this template does NOT carry

- Input-image manifests (those live at Phase 6 / `04_input-images/`)
- Canonical prompt packs (Phase 6 / `05_prompt-packs/`)
- Model adapter payloads (Phase 6)
- Suno full-generation prompts (Phase 6 — Suno brief at AG1 is brief-level only)
- Render cost estimates (Phase 6.5+)

## html-publisher integration

When the orchestrator dispatches an AG1 build, the task envelope MUST include:

```json
{
  "structure_brief_ref": "clients/_template/_templates/concept-phases/ag1-card-template.md",
  "data_sources": {
    "packs": [
      {
        "concept_slug": "...",
        "concepts_draft": "<workspace>/02_ag1-options/concepts.json",
        "script_drafts": "<workspace>/02_ag1-options/script-drafts.json",
        "suno_briefs": "<workspace>/02_ag1-options/suno-briefs.json",
        "concept_brief": "<workspace>/concept-brief.json"
      }
    ]
  }
}
```

html-publisher renders one card per concept, in concept-ID order. Recommended concept gets a visible badge + red accent border (per HazeCraft wrapper rules).

## Version

- **v1.0** — 2026-05-23 — Initial lock by operator. Columns: # / Time / Visual+Direction / VO quoted / Purpose. "Why this lands now" replaces "Stage 4 Move".
- **v1.1** — 2026-05-23 — Purpose enum extended from 6 to 8: added `Mechanism` (the how-it-works reveal, distinct from Discredit's failure-naming) and `Authority` (expert/clinician handoff, distinct from Proof's testimonial/data). `Outro` proposed and rejected per Iman's verdict ("CTA-adjacent coda, doesn't change the work"). Eval-buyer-fit axis 6 now treats Mechanism + Authority as distinct proof types for the ≥3-types scoring threshold.
