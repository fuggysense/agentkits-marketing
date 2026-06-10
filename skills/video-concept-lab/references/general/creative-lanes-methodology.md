# Creative Lanes Methodology

> **Source:** Iman Gadzhi, takekine consultation 2026-05-18 (chat_id `94ce6e7e-d760-4da2-9848-2c19f61a4b63`).
> **Organizing principle:** "One lane for identity, one for mismatch, one for pattern interruption, one for mechanism tease, one for specificity shock — variety without chaos. The ad is not the funnel. The ad is just the doorway."
> **Compressed version (2026-05-19):** 3 of Iman's 5 lanes cross-link to existing copywriting-os files. Only 2 native lane scaffolds live here.

---

## What is a Creative Lane?

A creative lane is a named persuasion doorway — it defines the psychological approach the ad uses to move a persona from their current awareness rung to the SL's opening rung. It is NOT a format. NOT an angle_family. It is the strategic constraint that precedes all format/angle decisions.

**Lane anatomy (5 required fields):**
1. `lane_id` — kebab-case slug (e.g., `lane_2_pattern_recognition`)
2. `hook_archetype` — the 1-sentence hook premise the ad must open on
3. `awareness_open` / `awareness_close` — which rung the ad starts and ends at
4. `sl_handoff_rung` — what rung the SL opens at (must match awareness_close, max 1-2 rung gap for 30s ads)
5. `must_do` / `must_not_do` — lane-specific creative constraints (client-defined in `_brand/funnel.md`)

---

## Where Lane Content Lives

- **Generic methodology:** this file.
- **Native lane scaffolds (Pattern-Recognition, Mechanism Tease):** §"Native Lane Scaffolds" below.
- **Cross-link lane scaffolds (Hidden-Mismatch, Identity Mirror, Specificity Shock):** §"Cross-Link Lane Stubs" below — these point to existing copywriting-os frameworks instead of redefining the lane locally.
- **Client-specific lane definitions:** `clients/<client>/_brand/funnel.md` → §"Strategic Ad Lanes."
- **Persona-to-lane mapping:** `clients/<client>/_brand/funnel.md` → §"Persona → Lane → Handoff Mapping."

---

## Lane Selection Protocol

1. Identify target persona from brief (`chosen_persona_id`).
2. Read `_brand/funnel.md` §"Persona → Lane → Handoff Mapping" → find valid lanes for the persona's awareness rung.
3. Assign one lane per concept. Across a 5-concept pack: default ≥ 3 distinct lanes.
4. Commit via `chosen_lane` block in `concept-brief.json` (legacy schema reference: `concept-input-packet.md`).
5. Hook archetype MUST match the committed lane's `hook_archetype`.
6. If `lane_test_mode: true`, the pack can run a single lane across all 5 concepts.

---

## Ad Length Budget Reality

30s ads can lift at most 1-2 awareness rungs. Lane selection must respect this:

| Rung lift needed | Required ad length |
|---|---|
| 0.5 rung (identity match) | 15s |
| 1 rung | 30s |
| 2 rungs | 60s (tight) |
| 3 rungs | 90-120s |

The SL's opening rung is fixed. Work backward from the SL opener to determine which awareness rung the ad must close at, then select a persona that opens at a rung the ad can actually lift from.

See `video-compression-by-duration.md` for beat-sheet specifics across 15s / 30s / 45s / 60s / 90s. Duration is operator-declared per `concept-brief.json` (`duration_target_seconds`) — no default lock-in.

---

## angle_family Compatibility

Lanes constrain which `angle_family` values are appropriate. Guidelines (not hard locks — override with rationale in `override_log`):

| Lane type | Compatible angle_family | Incompatible |
|---|---|---|
| Awareness-first (Unaware → Problem-Aware) | `symptom_overlap`, `problem_agitation`, `status_quo_contrast` | `offer_led`, `product_demo` |
| Solution-first (Solution-Aware+) | `mechanism_reveal`, `protocol_failure`, `specificity_shock` | broad `problem_agitation` without solution frame |
| Identity-led (any rung) | `identity_validation`, `lifestyle_mismatch` | `authority_explanation` alone |

---

## Pack-Level Diversity Rule

Across a 5-concept pack:
- ≥ 3 distinct `lane_id` values (unless `lane_test_mode: true`)
- No two concepts may share the same `lane_id` AND the same `persona_id`
- Lane spread should mirror awareness spread: include at least one Unaware-entry lane and one Solution-Aware-entry lane per pack (where both exist in the client's lane menu)

---

## Native Lane Scaffolds

The 2 lanes below have no upstream framework in copywriting-os — defined fully here.

### Lane 2 — Pattern-Recognition

**Hook archetype:** "Most [persona-noun] are doing this wrong / chasing the wrong fix."

**Must do:**
- Open with a behavior pattern the persona recognizes themselves in
- The recognition is the conversion — buyer thinks "that's me" within 5 seconds
- Pair with mechanism or specificity in the body (recognition alone isn't enough)

**Must not do:**
- Generalize so broadly it could apply to anyone ("most people are tired")
- Pattern-match without offering the corrected pattern
- Use accusatory framing ("you're stupid for trying X")

**Awareness fit:** Problem-Aware → Solution-Aware (1-rung lift)
**SL handoff:** Solution-Aware opener (clean handoff)
**Compatible angle_family:** `symptom_overlap`, `status_quo_contrast`

### Lane 4 — Mechanism Tease

**Hook archetype:** "The problem isn't [obvious thing]. It's [hidden mechanism]."

**Must do:**
- Reveal mechanism in ad but NOT the full protocol (that's SL territory)
- Lead with the false-mechanism the buyer believes, contrast with the real one
- Pair with one specificity hook (numbers, ingredients, timelines)

**Must not do:**
- Reveal complete mechanism — leaves nothing for SL
- Use unfamiliar jargon without translation
- Stack 3+ mechanism statements in ad (kills pacing)

**Awareness fit:** Solution-Aware → Solution-Aware (no lift, sharpens)
**SL handoff:** Solution-Aware opener (cleanest possible handoff)
**Compatible angle_family:** `mechanism_reveal`, `protocol_failure`

---

## Cross-Link Lane Stubs

The 3 lanes below cross-link to existing copywriting-os frameworks. Use those frameworks directly; this section is a routing convenience only.

### Lane 1 — Hidden-Mismatch
**→ Load `stage-4-discrediting.md` (NEW-1) Moves 1+2 (Anger Recruitment + Validation Flattery).**
The Hidden-Mismatch lane IS the Schwartz-Stage-4 validation-flattery pattern. Same psychological move, same hook archetype, same awareness-fit. Don't redefine — use NEW-1.

### Lane 3 — Identity Mirror
**→ Load `.claude/references/copywriting-os/frameworks/schwartz-channeling.md`.**
The Identity Mirror lane IS Schwartz's channeling principle: match the audience's existing self-image, don't manufacture one. Hook archetype: "If you're the kind of [persona-identity] who [behavior], this is for you." Awareness fit: any rung. SL handoff: matches whatever rung the SL opens at, since identity holds across rungs.

### Lane 5 — Specificity Shock
**→ Load `.claude/references/copywriting-os/frameworks/six-proof-types.md` (Type 5: Specificity Proof) + `scout-mode-instructions.md` (mining concrete details).**
The Specificity Shock lane IS the layered application of Schwartz/Halbert specificity proof. Hook archetype: a single concrete number, ingredient, or timeline that lands as undeniable. Awareness fit: Problem-Aware → Solution-Aware OR Solution-Aware → Solution-Aware. SL handoff: clean.

---

## Clients Without Defined Lanes

If `_brand/funnel.md` contains no §"Strategic Ad Lanes" section:
- Skip lane selection entirely.
- Proceed with standard `spine_angle_family` from the concept-brief.
- Flag gap: "No creative lanes defined for [client]. Operator may populate `_brand/funnel.md` §Strategic Ad Lanes using the template below."

---

## Template: 5-Lane Scaffold (for new client `_brand/funnel.md` population)

```
## Strategic Ad Lanes (LOCKED creative menu)

### Lane 1 — Hidden-Mismatch
- Cross-link: `skills/video-concept-lab/references/general/stage-4-discrediting.md`
- **Client-specific must do/must not do:** [client fills in]
- **Awareness fit:** [rung → rung]
- **SL handoff strength:** [Weak | Medium | High | CLEANEST]

### Lane 2 — Pattern-Recognition
- Methodology: this file §Native Lane Scaffolds
- **Client-specific must do/must not do:** [client fills in]
- **Awareness fit:** [rung → rung]

### Lane 3 — Identity Mirror
- Cross-link: `.claude/references/copywriting-os/frameworks/schwartz-channeling.md`
- **Client-specific identity statement:** [client fills in]

### Lane 4 — Mechanism Tease
- Methodology: this file §Native Lane Scaffolds
- **Client-specific reveal vs withhold split:** [client fills in]

### Lane 5 — Specificity Shock
- Cross-link: `.claude/references/copywriting-os/frameworks/six-proof-types.md` + `scout-mode-instructions.md`
- **Client-specific specificity bank:** [client fills in — at least 10 concrete details]

## Persona → Lane → Handoff Mapping

| Micro-persona | Awareness rung | Best lane(s) | SL handoff |
|---|---|---|---|
| [persona_id] | [rung] | [lane N, lane N] | [Soft | Medium | Strong | CLEANEST] |
```

Use any N lanes. The 5-lane structure is Iman's recommended starting menu, not a mandate.

---

## See Also

- `_brand/funnel.md` (per client) — actual lane definitions and persona mapping
- `skills/video-concept-lab/references/general/stage-4-discrediting.md` (NEW-1) — Hidden-Mismatch lane content
- `skills/video-concept-lab/references/general/common-enemy-bridge.md` (NEW-2) — pairs with Lane 1 + Lane 4
- `skills/video-concept-lab/references/general/video-compression-by-duration.md` — beat-sheet templates per duration (15s / 30s / 45s / 60s / 90s); operator picks duration per `concept-brief.json`
- `.claude/references/copywriting-os/frameworks/schwartz-channeling.md` — Lane 3 (Identity Mirror) cross-link
- `.claude/references/copywriting-os/frameworks/six-proof-types.md` — Lane 5 (Specificity Shock) cross-link
- `.claude/references/copywriting-os/frameworks/scout-mode-instructions.md` — Lane 5 mining
- `skills/video-concept-lab/references/general/scoring-and-analysis.md` — V2V scorer (lane choice affects spine_clarity)
