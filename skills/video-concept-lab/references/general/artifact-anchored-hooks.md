# Artifact-Anchored Hooks

**Purpose:** raise `first_frame_thumbstop` scores on mechanism-tease and pattern-recognition lanes by anchoring the hook in a physical object the buyer has already touched, hoarded, or thrown away.

**Source:** empirical, derived from the Phase 2 head-to-head against external `creative-director-skill` on the Takekine `dr-foundation-pilot` brief — see `_audit/creative-director-comparison-260520.md`. External's artifact-anchored concepts (Quit Jar, Receipt) scored 9 and 8 on `first_frame_thumbstop`; our mechanism-reveal concepts (c03 owl-and-clipboard, c04 bank-metaphor) scored 6–7 on the same axis. The finding is portable; the methodology that produced it is not.

---

## The pattern

A hook is **artifact-anchored** when the opening 0–1.5s frame shows an object that:

1. Already exists in the buyer's home / phone / inbox / body
2. Carries embedded buyer-history (it represents a specific past failure, decision, or moment)
3. Is loaded with implicit narrative before any word is spoken
4. The buyer can identify by sight alone, without explanation

The object is doing the work of an entire copy line. The first frame says "this is about you" before the voiceover has to.

---

## Worked examples (from the empirical baseline)

| Artifact | Buyer history embedded | Why it scored 9 |
|---|---|---|
| **The Quit Jar** — bathroom-shelf graveyard of half-finished iron-supplement bottles | Every bottle is a previous failure; the jar is the buyer's own quitting pattern made visible | Buyer recognizes their own bathroom in frame 1. Self-recognition before any voiceover. |
| **The Receipt** — foot-long CVS receipt listing every iron product the buyer has tried, last line finally different | The receipt IS the tried-and-discounted alternatives list, made physical | One scrollable visual carries 18 months of buyer history. The "last line different" is the whole sales argument compressed into typography. |

Compare against mechanism-tease hooks that scored 6:

| Artifact | Why it underperformed |
|---|---|
| Owl with clipboard ticking off symptoms | Owl is a stand-in, not the buyer's. No embedded history. The clipboard *describes* the buyer's symptoms instead of *showing* the buyer's evidence. |
| Bank-account metaphor (depleted iron stores) | The metaphor is intellectually correct but visually generic. A bank account is not in the buyer's hand at 7am crashing through cortisol. |

The pattern: **artifact-anchored hooks show the buyer's own object; mechanism-reveal hooks describe what the object would mean.** The first stops thumbs. The second educates a viewer who already scrolled past.

---

## When to use this

**Use artifact-anchoring on these lanes:**
- Pattern-Recognition (L2) — the artifact IS the pattern the buyer keeps repeating
- Hidden-Mismatch (L1) — the artifact shows the gap between what the buyer did and what they thought they were doing
- Specificity Shock (L5) — the artifact is the specific receipt / shelf / drawer that wouldn't exist if the buyer hadn't tried everything

**Avoid artifact-anchoring on:**
- Mechanism-Tease (L4) when the mechanism is invisible (cellular absorption, microbiome action) — forcing an artifact here usually produces a literal organ diagram, which fails on `first_frame_thumbstop`. Use mechanism-tease the other way: anchor the artifact in the buyer's hand FIRST, then reveal the invisible mechanism second.
- Identity Mirror (L3) when the buyer-identity is the visual hook — the face IS the artifact.

---

## The Buyer-Object Test (run before locking the hook)

For every hook you draft, answer:

1. **Does the buyer already own / has owned / has thrown away the object in frame 1?**
   - Yes → artifact-anchored candidate.
   - No → not artifact-anchored. Either swap to one they own, OR accept this is a mechanism-tease hook and score it differently.

2. **Could the buyer identify the object in 0.5s with no caption?**
   - Yes → frame 1 works as a stopping signal.
   - No → the artifact is too generic. Specify it. ("Bottle" → "the brown amber Slow Fe bottle." "Receipt" → "CVS pharmacy receipt with red letterhead.")

3. **Does the object carry buyer-history without narration?**
   - Yes → the object earns its frame.
   - No → it's a prop, not an artifact. The hook will lean on voiceover to do work the visual should be doing.

4. **Specificity Test:** could a competitor's ad use the same artifact?
   - Yes → the artifact is generic to the category, not specific to this brand's offer. The hook will score originality ≤ 5. Find a more specific artifact OR change lane.

---

## Production handoff implications

For the `image_handoff_only` loadout and prompt-pack builder downstream:

- Frame-1 input image MUST show the artifact in the buyer's hand / shelf / pocket — not on a clean studio background.
- Lighting should match the buyer's actual environment (bathroom fluorescent / kitchen morning light / car interior at 7am) — NOT cinematic product-shot lighting.
- The artifact must be the visual subject of the first 1.5s. Avoid pull-back reveals that hide the artifact behind a person's face for the first 2s — that burns the thumbstop window.

---

## Scoring effect

When the artifact-anchored pattern is applied and passes all 4 Buyer-Object questions:

| Compass axis | Expected lift vs mechanism-reveal hook on same brief |
|---|---|
| `first_frame_thumbstop` | +2 to +3 |
| `spine_clarity` | +0 to +1 (artifact carries narrative load) |
| `flow_renderability` | 0 (artifacts are usually easier to render than allegorical visuals) |
| `claim_safety` | 0 (orthogonal — the artifact carries no claim by itself) |

Net: +2 to +4 on total compass. Highest-leverage hook upgrade available without changing the spine or the mechanism.

---

## See also

- `hook-and-format-rules.md` — base hook schema (verbal / visual / rendered_text / subtitle_policy)
- `creative-lanes-methodology.md` — lane → archetype mapping; the Buyer-Object Test refines lane assignment for hooks specifically
- `scoring-and-analysis.md` — Specificity Test + emotion-tier resolution
- `_audit/creative-director-comparison-260520.md` — full empirical baseline this pattern was derived from
