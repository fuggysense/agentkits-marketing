# Beat Sheet Director Render Evaluation

Date: 2026-05-13

Model: `gpt_image_2`, `resolution=1k`, `quality=medium`.

All four renders were generated through Higgsfield CLI and saved locally.

## Render Results

| ID | File | Dimensions | Score | Critical fail? | Decision |
|---|---|---:|---:|---|---|
| R1-ugc-calm-c12 | `renders/R1-ugc-calm-c12.png` | 752x1344 | 83 | Soft fail | Keep grid/label pattern; patch UGC anti-polish + label lock. |
| R2-dtc-solara-label | `renders/R2-dtc-solara-label.png` | 1024x1024 | 81 | Yes | Patch no-extra-copy/no-claims rule for DTC product storyboards. |
| R3-cinematic-neon-courier | `renders/R3-cinematic-neon-courier.png` | 1344x752 | 87 | No | Keep cinematic pattern; patch caption readability + identity continuity. |
| R4-ugc-gripflow-12-panel | `renders/R4-ugc-gripflow-12-panel.png` | 752x1344 | 87 | No | Keep 12-panel 3x4 pattern; patch action-proof weighting + anti-polish. |

Note: R4 looked slightly wider than ideal to one evaluator, but saved dimensions are exact `752x1344`, matching 9:16.

## Logged Errors

### E1 — Caption overlays can violate UGC/DTC output intent

Observed in: R1, R2.

The default beat-sheet prompt asks for black caption bands below each panel. This works for cinematic storyboard review, but it polluted UGC/DTC renders where the image itself should look like raw phone footage or clean product photography. In R2, the captions invented marketing copy and implied claims.

Change:

- Add a mode-aware caption policy:
  - Cinematic storyboards: caption bands allowed, but text must be large and high-contrast.
  - UGC/DTC validation renders: no captions, subtitles, timestamps, VO text, bottom text bars, or explanatory overlay text unless the user explicitly asks for storyboard annotations.

### E2 — Product-label lock needs stronger per-panel rules

Observed in: R1, R2, R4.

Labels were mostly readable, but fragile. R1 panel 9 was soft; R2 preserved SOLARA but the captions added unsanctioned copy; R4 did well on package label but sock text warped.

Change:

- Add `PRODUCT LABEL LOCK` block when a label is specified:
  - exact required text
  - label must be large, straight, flat to camera, and readable in each product-facing panel
  - no extra words, badges, claims, certification seals, or marketing copy
  - if the text is not central to the panel, describe the product without forcing tiny label text

### E3 — DTC product storyboards need claim hygiene

Observed in: R2.

R2 added “Water beads,” “Form meets function,” and “Simple. Essential. Yours.” These violate the exact copy/no extra claims brief. The water-bead visual can also imply water resistance.

Change:

- Add `DTC CLAIM HYGIENE`:
  - the only readable text may be the approved label/copy list
  - avoid visual or written performance claims unless explicitly supplied
  - ban fake dermatology, reef-safe, clinical, award, rating, or performance cues

### E4 — UGC rawness decays into polished ad framing

Observed in: R1, R4.

R1 and R4 started raw, then later panels became planned product holds or influencer-polished. Existing corrections already warn about this, but the scene prompt needs panel-level anti-polish constraints.

Change:

- Add `UGC RAWNESS LOCK`:
  - awkward crop, handheld framing, uneven light, mirror/sink/apartment clutter, imperfect posture
  - avoid product-hero staging, commercial symmetry, shallow-depth polish, beauty posing, and catalog-style CTA frames
  - maintain lived-in background through CTA/result panels

### E5 — Action proof is underweighted in product-use sequences

Observed in: R4.

R4 got the package and grip texture, but several panels became unboxing/product display rather than proof of workout use.

Change:

- Add action-evidence weighting:
  - for demo/proof scenes, require at least 40% of panels to show active use, not static product display
  - for grip socks specifically: grip dots contacting floor in at least three panels
  - for consumables/topicals: two-stage product action when the product can disappear

### E6 — Cinematic captions and identity continuity need tightening

Observed in: R3.

The cinematic grid passed, but captions were small and character continuity softened across panels. The final panel was underlit.

Change:

- Add cinematic storyboard refinements:
  - large, high-contrast captions readable at thumbnail size
  - one or two short caption lines only
  - explicit recurring identity lock for the main character across all panels
  - every panel must show a distinct story action, not only atmosphere
  - preserve action/facial clarity in noir or low-light scenes

## Proposed Skill Patch

Patch `/Users/jerel/.claude/skills/beat-sheet-director/SKILL.md` in three places:

1. Add a `Mode-aware caption policy` after `## Caption rules`.
2. Add `Product label / claim hygiene` after `## Reference image handling`.
3. Add `Mode fidelity locks` under the three style modes.

Do not change the core folder-tree contract. It held up.

## What Passed

- Exact aspect ratios were honored in the saved files.
- 2x2, 3x3, and 3x4 grids rendered correctly.
- Cinematic mode produced a usable storyboard.
- GPT Image 2 handled multi-panel storyboard layouts well at 1K medium.
- The skill's separation from `ai-filmmaking` remains correct: this is a pre-production storyboard tool, not a narrative writing engine.
