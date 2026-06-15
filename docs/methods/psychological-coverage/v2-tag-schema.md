# Psychological Coverage — v2 Tag Schema (canonical field reference)

**Status:** LIVE (P1, 2026-06-14). This is the single source of truth for the `psych_coverage` tag shape and the coverage tally. It supersedes the appendix schema in `INTEGRATION-PROPOSAL.md` (the v1 4-room grid `valence_zone` / `self_concept_anchor` / `coverage_tag`, which the 260614 re-cut killed).
**Locks in:** `VOCABULARY.md` v2 (the "real-loud test lane" re-cut).
**Applies to:** the `dct.json` per-angle manifest. One `psych_coverage` object per angle. Optional — absent/`null` on untagged DCTs, never `required[]`.

---

## Why v2 ≠ v1

The retro-tag proof (260614, NeezaNizam DCT010 + Eugene DCT002) killed two v1 assumptions against real cold waves:

1. **"Loud vs quiet" never moved** — brand contracts forbid loud. So a 2×2 valence×arousal grid (`valence_zone`) wastes two cells on every cold wave. **v2 replaces it with the valence *arc* + a single opt-in real-loud lane.**
2. **Ought/duty is kill-listed cold** — avatars say "too tender for cold," and Eugene's files hard-ban "for the kids / legacy" framing (L4 rage trigger). So Ought is not a coverage target. **v2 drops it as a `self_image` value and turns it into a tripwire.**

Net cold check = **two spread questions + one opt-in test lane + two tripwires.**

---

## The fields

Each angle carries:

```jsonc
"psych_coverage": {
  "valence_arc": "worry->relief",   // see Field 1
  "self_image": "mirror",           // see Field 2
  "real_loud": false,               // see Field 3 (opt-in test lane)
  "tripwire": null,                 // see Field 4 (auto-flag)
  "evidence": "cited line ..."      // see Provenance gate
}
```

### Field 1 — `valence_arc` (the move, not a frozen room)

The reader's emotional movement through the ad. Tokens: `worry` | `relief` | `neutral`.

- **Static (single room):** one token. e.g. `"worry"` — the ad names the problem and leaves the resolution off-ad (in the letter).
- **Arc (it walks):** `"<from>-><to>"`. e.g. `"worry->relief"` — opens on a named worry, hands over relief inside the same ad.
- **Lead valence** (what drives the coverage spread) = the **`<from>` token**. An ad that leads `worry` reaches different people than one that leads `relief`.

**Disambiguation rules (added 260615 from proof #2 — the two lead types where independent raters split):**

1. **Lead = the opening MOVE's register, not the worry it implicitly resolves.** If the ad OPENS by offering safety / removing a fear — a pledge or reassurance, e.g. *"No hard sell. No spam. No pressure."* — that is **`relief`-led**, even though a worry sits underneath. Do not back-infer `worry` from the fear a reassurance addresses; tag what the first move *does*.
2. **A lead that opens on positioning / qualification / identity (not an emotion) is `neutral`-led.** e.g. *"This isn't for every family,"* premium-tier framing (*"Toyota vs Lexus"*), *"find out which type you are."* It usually arcs to `relief` or pairs with `self_image: aspiration`.

**Do NOT add a 4th valence token (e.g. "confidence").** The "confident / premium" quality of a positioning lead is already captured by `valence: neutral` + `self_image: aspiration` — two axes each doing their job. A 4th token would muddy the single question this axis exists to answer: worry-led vs relief-led spread.

> **Coverage question 1 (worry/relief spread):** *does the wave carry both worry-led and relief-led ads, or is everything piled on one?* A wave that is 100% worry-led is a collapse signal — but worry-heavy is **correct and expected for L1–L2 (unaware → problem-aware)** audiences, where you must name the problem before they care. Read the spread against the wave's awareness stage, not against a 50/50 ideal.

### Field 2 — `self_image` (who the ad casts the reader as)

Tokens: `mirror` | `aspiration`.

- `mirror` = who-they-are-now ("the owner who didn't look," their exact current belief spoken back).
- `aspiration` = who-they-want-to-be ("the couple who unlocked the upgrade," the prudent winner).
- **Duty / Ought ("do it for the kids") is NOT a value here** — it's a `tripwire` (see Field 4). On cold traffic it's a contract breach, not a coverage cell.

> **Coverage question 2 (mirror/aspiration spread):** *does the wave span both who-they-are-now AND who-they-want-to-be?* A wave that collapses to near-pure `mirror` (the NeezaNizam DCT010 result) is a real, usable signal — it's leaving the aspiration door shut.

### Field 3 — `real_loud` (the opt-in test lane)

Boolean. `true` ONLY when the angle leads with **genuine** urgency: a real deadline, a quantified runway, a quantified loss left on the table. NOT manufactured ("limited units," "act now").

This is the **test lane**, not a tripwire — real-loud is *allowed* and usually *absent*. When `0/N` angles carry it, that's white space worth a deliberate test **if the offer permits it.**

> **Client gate:** only surface real-loud as white space when the offer contract permits life-trigger urgency. Eugene's `offer.md` does: *"life-trigger urgency, not artificial scarcity… anchor to the prospect's own runway"* (MOP / family / retirement-runway windows). NeezaNizam's: *"MOP timing · mortgage-rate window."* If a client's contract forbids all urgency, real-loud is not white space for them — it's off-limits, and the tally should say so.

### Field 4 — `tripwire` (auto-flag = likely cold-traffic breach)

`null` | `"fake_loud"` | `"guilt_duty"`.

- `fake_loud` = manufactured scarcity / hype / exclamation CTAs / "act now." A brand-contract breach for every client whose files ban it.
- `guilt_duty` = a guilt / "do it for them" / social-obligation appeal on cold traffic.

Tripwires are **surfaced, never rewarded as coverage.** A wave with zero tripwires is a useful *on-contract confirmation*, not just an absence.

### Provenance gate — `evidence`

Every tag set carries a cited `evidence` line: the specific phrase in the copy that justifies the tags. Same rule the avatars enforce ("no source → it's only a hypothesis"). No vibes. A `psych_coverage` block with empty `evidence` is incomplete, not done.

---

## The coverage tally (what the operator sees)

Computed from the N tagged angles. Read in five seconds at angle-approval time. Advisory — the human decides whether a gap is worth filling.

```
DCT0NN — "<avatar/wave>" (N angles)

Valence (lead → in-ad arc):
  worry-led ........ A.., A..   (k)   ← read against the wave's awareness stage
  relief-led ....... A..        (k)
  resolves in-ad ... A.., A..         (which worry-led ads hand over relief vs leave it to the letter)

Self-image:
  mirror ........... A.., A..   (k)
  aspiration ....... A.., A..   (k)   ← collapse to one = door left shut

Test lane (real-loud, opt-in):
  count            (k)   ← if 0 AND offer permits life-trigger urgency: WHITE SPACE
                          if offer forbids urgency: "off-contract, n/a"

Tripwires (auto-flag):
  fake-loud ........ none / A..  ⚠
  guilt-duty ....... none / A..  ⚠
```

---

## What this does NOT do

- Does **not** re-encode awareness / sophistication — `market_awareness` + `market_sophistication` already exist per angle.
- Does **not** gate the wave. Advisory only — surfaced at HITL Gate 1, the human decides.
- Does **not** chase a filled grid. "Cover white space only where the territory is worth occupying." Forcing all rooms when two don't fit the buyer makes creative worse.

## Build status

- **P1 Phase 1 (260614):** schema locked; DCT002 (Eugene) tagged as the worked example; this doc + `docs/dct-json-schema.md` document the field.
- **P1 Phase 2 (260615):** shared engine `scripts/psych_coverage_tally.py` (`compute_tally` / `format_tally` / `summarize_tally` / `project_angle` + CLI). Both sheet writers patched to call it, additive + guarded (byte-identical when no psych tags exist): `ad_concept_sheet_writer.py` (per-ANGLE `PSYCH COVERAGE` cell via `project_angle` — serves Eugene + NeezaNizam buyer-funnel) and `dct_10_5_5_sheet_writer.py` (per-DCT aggregate via `summarize_tally`, column appended only when tagged — serves the Thomson-Reserve `DCT101–105` batch; renamed from `tr_10_5_5_sheet_writer.py` 260616, no longer TR-specific). HITL Gate-1 coverage-tally print added to `ad-concept-engine/SKILL.md`. `big-angle-spotter` is a global symlink — not edited. Validated via dry-runs (no live writes).
- **P2 (deferred):** creation-time `hypothesis` field + feedback-router predicted-vs-observed.
