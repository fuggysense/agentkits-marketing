# Concept Stage Mandatory Checks

**Purpose:** the practical pre-write checklist every video-concept-seeder dispatch MUST run before emitting any concept. This is the operational layer on top of `core-framework.md` (theory) and `lf8-market-translation.md` (substrate-to-dialect).

**Source:** Iman Gadzhi take 2026-05-18 (Q2 minimum-viable directive + Q3 modular order + Q4 format-last rubric + 3 missing pillars). See `iman-take-260518.md`.

---

## The minimum-viable seeder directive (verbatim Iman)

Embed this single sentence into the seeder's system prompt. It is the irreducible core:

> **"Know the level of awareness, hit one sharp pain, widen the gap, sell the mechanism, and only then choose the format that expresses it best."**

If the seeder violates this sentence, the concept is invalid. No exceptions.

---

## Mandatory pre-write order (6 modules — NEVER fuse, NEVER reorder)

The seeder MUST generate concepts as discrete modules, in this exact order. Do NOT produce a "fully fused creative blob" — that's where format invents strategy.

| # | Module | What gets decided | Source file |
|---|---|---|---|
| 1 | **Market Sophistication** | Which of Schwartz's 5 stages the audience sits at. | `core-framework.md` Layer 1 |
| 2 | **Angle** | The ONE belief / pain / desire this concept targets. From `concept-brief.json.angle_family` or operator directive. | brief |
| 3 | **Promise** | What the prospect gets — translated through the market's LF8 dialect. | `lf8-market-translation.md` |
| 4 | **Proof type** | Person / process / metaphor — and which of 3 jobs the proof does (validates mechanism / problem specificity / buyer identity). See pillar 2 below. | this file |
| 5 | **Format recommendation** | Chosen LAST via the 4-gate rubric. NOT inherited from upstream brief. See gate questions below. | this file |
| 6 | **Claim guardrails** | Allowed / forbidden expressions per `concept-brief.json.allowed_expressions` + `forbidden_expressions`. | brief |

**Critical:** **Format is module 5, not module 1.** If the brief locks `workflow_flow` upstream, the seeder should TREAT IT AS A HYPOTHESIS, not a constraint. The seeder may override the upstream format if modules 1-4 + the 4-gate rubric point elsewhere — and must flag the override to the operator at AG0.

---

## Duration-collapse rules (Iman F1 + Q1)

Match the body structure to the target duration. Do not import VSL completeness into short-form.

| Target duration | Body structure (mandatory) |
|---|---|
| **15 seconds** | hook + ONE pain image + ONE mechanism cue. Nothing else. |
| **30-60 seconds** | hook + pain + gap + mechanism + ONE objection touch |
| **60s+ (VSL territory)** | full Joyner 5-step body acceptable (point-pain → gap → plan/mechanism → belief via gradualization/mechanization → harpoon objections) |

**Test:** count the persuasion beats in the concept. If a 15s concept has 5 beats, it's a VSL squeezed into 15s — reject and collapse.

---

## The three Iman pillars (mandatory pre-emit checks)

These are NOT in orthodox DR. Iman flagged them as the biggest gaps in the Schwartz/Whitman/Joyner orthodoxy for short-form video. Run all three on every concept.

### Pillar 1 — Open-loop architecture

**Definition:** each beat must carry an unanswered question into the next beat. The loop is a WITHHELD ANSWER, not a narrative device.

**The cardinal sin:** 3 clips that all resolve simultaneously = zero tension, zero forward motion, just information.

**Per-beat check (run on every multi-clip concept):**
- Clip 1: what question does this clip OPEN that the viewer needs answered?
- Clip 2: does this clip CARRY the tension (gap widens, mechanism still unnamed) or RESOLVE it prematurely?
- Clip 3 (or final): does this clip CLOSE the loop from clip 1? Is the mystery answered, the mechanism named?

**Iman's annotated 15s example (wellness, Problem-Aware):**
- Clip 1: *"If you wake up tired no matter how much you sleep, this is usually not a motivation problem."* — LOOP OPENS ("if it's not motivation, what is it?")
- Clip 2: *"Most women keep treating it like a willpower issue, but the real cost is creeping into your focus, mood, and patience by 2 p.m."* — TENSION CARRIES (mechanism still unnamed, "what fixes it?" still unresolved)
- Clip 3: *"That's why we built a simple energy reset protocol that helps your body recover before the crash starts."* — LOOP CLOSES (mystery answered, mechanism named)

### Pillar 2 — Proof placement discipline

**Definition:** every proof element in the concept must do ONE of three jobs. If it does none, it is decorative — strip it.

| Proof job | What it does | Example |
|---|---|---|
| (a) **Validate mechanism** | Shows WHY the new mechanism works | "Mucosa-absorption bypasses the stomach lining" |
| (b) **Validate problem specificity** | Confirms the buyer's pain is real and distinct | "73% of women with normal ferritin still report fatigue" |
| (c) **Validate buyer identity** | Confirms the buyer is the right person for this | "I'm a 38yo mom of 2 who tried iron pills for 6 months" |

**Per-concept check:** for every proof element, tag which of (a)(b)(c) it serves. Untagged = decorative = strip.

### Pillar 3 — Compression discipline (anti-intellectually-complete)

**Definition:** short-form REWARDS precision, compression, and selective omission. It PUNISHES completeness. The best concepts make the right person feel the next sentence before you say it.

**Per-concept check:**
- Could I cut 30% of the body beats and still land the punch? If yes, cut.
- Does the concept "tell the whole truth" or does it set up the next sentence?
- Is every beat charged (forward motion) or complete (closed)?

**Iman's warning:** *"The biggest gap is that it still sounds a little too intellectually complete. That's dangerous."*

---

## Hook archetype decision (Iman F2)

Two viable hook archetypes for short-form. Decision variable = **AWARENESS STAGE**, not format.

| Hook archetype | When to use | When to AVOID | Example (fatigue / women's wellness) |
|---|---|---|---|
| **Problem-aware hook** | Audience already feels the pain. Default for cold traffic. | Never wrong, but feels generic to saturated/sophisticated audiences. | *"Still crashing at 2 p.m. even after sleeping eight hours? That's because most women are chasing energy the wrong way."* |
| **Mechanism-first hook** | Audience is colder/saturated/educated. Already feels pain. Needs a NEW LENS to believe THIS offer is different. | Fails on audiences who haven't felt the pain strongly enough — sounds vague, abstract, fake science. | *"The reason this works is because it targets the recovery layer your body is ignoring, not just the symptom you feel by afternoon."* |

**Mechanism-first is NOT a 2026 replacement for problem-aware.** It is a sophistication-tier upgrade applied selectively. Default to problem-aware for cold; upgrade to mechanism-first when the audience is Stage 3-5 sophisticated AND already pain-aware.

**Hook archetype is awareness-dependent first, NOT format-dependent first.** UGC and cartoon can both carry mechanism-first if the mechanism is grounded and visually legible.

---

## Format-last selection rubric (Iman F4)

Format is module 5 — chosen LAST, not first. NOT a deterministic lookup table. Heuristic with hard constraints.

### Practical selection rules

Match angle character to format:

| Angle character | Recommended format |
|---|---|
| Emotionally immediate + easily dramatized + creator-led | UGC or founder piece-to-camera |
| Depends on visual transformation, process clarity, or mechanism that benefits from motion | cartoon-flow or motion-design |
| Novelty, curiosity, or pattern interruption | viral preset clones |
| Trust-heavy + identity-driven | talking-head (human face carries belief) |

### The 4 gate questions (mandatory)

Before locking format, the seeder MUST answer all 4:

1. **Can this be understood in 2 seconds?** (If no, the format is wrong.)
2. **Does the proof look stronger as a person, a process, or a visual metaphor?** (This determines person-led vs motion vs animated.)
3. **Does the creator have enough credibility to hold the format?** (If UGC/talking-head, the creator must carry it; if not, choose a non-human format.)
4. **Will the format amplify the mechanism, or bury it?** (If buries → wrong format. Mechanism MUST be physically legible in the format chosen.)

**Failure mode:** if 1+2 are yes but 4 is no → format is wrong, even if it "feels right."

### Multi-format output

If multiple formats pass all 4 gates, the seeder outputs the **top 2 with reasons**. The operator picks only when there's a genuine tradeoff. Single winner = no operator decision needed.

### Verdict on upstream format-locking

> Useful for production, dangerous for strategy. Locks creative bias before the real problem is diagnosed. Format is a rendering choice, not the starting assumption.

If `concept-brief.json` declared a `workflow_flow` upstream and the 4-gate rubric points elsewhere, the seeder must:
1. Flag the conflict at AG0 in the chat-only compass
2. Emit concepts in BOTH the declared format AND the 4-gate-recommended format
3. Let the operator choose at AG1

---

## Concept-vs-content test (final gate before emit)

Run all 6 BEFORE writing the concept JSON:

1. ✅ Does it reduce cleanly to **pain → gap → mechanism → belief shift**?
2. ✅ Does it follow the **6-module order** (sophistication → angle → promise → proof → format → guardrails)?
3. ✅ Does it pass the **duration-collapse rule** for target length?
4. ✅ Does it have a **clear open loop** that carries beat-to-beat?
5. ✅ Does every proof element have a **tagged job** (mechanism / problem specificity / buyer identity)?
6. ✅ Does the hook match the **awareness stage** (problem-aware default; mechanism-first only when warm)?
7. ✅ Does it pass the **Specificity Test** — swap the brand name for a direct competitor's. If the hook, spine, proof, and close all still land → concept is generic, cap `originality` at 5/10, flag `specificity_fail: true`, regenerate. (Source: external creative-director-skill, MIT, smixs.)

Any NO = not a concept. Reject. Regenerate.

---

## Output schema additions (for concepts.json per concept)

The seeder must emit these new fields per concept (additive to existing schema):

```json
{
  "dr_framework_compliance": {
    "module_order_followed": true,
    "duration_target_seconds": 15,
    "body_structure_per_duration_rule": "hook + pain + mechanism_cue",
    "spine_reduction_check": "pain → gap → mechanism → belief_shift",
    "open_loop": {
      "clip_1_opens": "<question opened>",
      "clip_2_carries": "<tension element>",
      "clip_3_closes": "<answer / mechanism named>"
    },
    "proof_elements_tagged": [
      {"element": "...", "job": "validate_mechanism | validate_problem_specificity | validate_buyer_identity"}
    ],
    "hook_archetype": "problem_aware | mechanism_first",
    "hook_archetype_rationale": "<awareness-stage justification>",
    "lf8_substrate": ["<which LF8 drives>"],
    "lf8_market_dialect_applied": "<which market row from lf8-market-translation.md>",
    "format_4_gate": {
      "legibility_2s": true,
      "proof_form": "person | process | metaphor",
      "creator_credibility": true,
      "format_amplifies_mechanism": true
    },
    "format_chosen": "cartoon-flow | ugc-flow | motion-design | tv-ad | talking-head | viral-preset",
    "format_alternates_considered": ["..."],
    "upstream_format_override_flag": false
  }
}
```

---

## See also

- `core-framework.md` — the theory layer (Schwartz/Whitman/Joyner + Iman corrections)
- `lf8-market-translation.md` — the substrate-to-dialect translation table
- `growthhub-creative-diversity-2026.md` — pack-level Entity ID diversification check (run AFTER per-concept compliance)
- `iman-take-260518.md` — full verbatim Iman transcript (both turns + music addendum)
