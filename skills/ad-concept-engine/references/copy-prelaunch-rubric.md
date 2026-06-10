# Meta-Copy Pre-Launch Rubric (fresh-context reviewer gate)

> **Runs on every batch BEFORE the human creative gate (HITL Gate 3), after the Claim Gate.** A FRESH-context reviewer (no anchoring from the drafting context) scores each ad's copy against this rubric. **Code decides** pass/fail from a fixed threshold — the reviewer JUDGES, it does not get to wave its own work through.
>
> **Grounding:** distilled from `_shared-knowledge/ferres/05-quality-bar-critique-rubric.md` (Sean Ferres' live ad critiques). Open that file for the primary-source line cites when a dimension is unclear.
>
> **Scoring convention** mirrors the big-angle-spotter resonance gate (`skills/big-angle-spotter/scripts/run_pipeline.py`, `RESONANCE_GATE` + `compute_gate_verdicts`): per-dimension integer 1-5, no half-points, anchored bars; an ad PASSES only if EVERY dimension ≥ threshold; missing/malformed scores fail closed. The task brief named `scripts/hook_gate.py` as the scoring source — that script does not exist in the repo; the resonance gate is the live, canonical implementation of the same "model judges, code decides" pattern, so this rubric reuses it.

---

## Why a fresh-context reviewer

The drafting agent is anchored — it wrote the copy and will under-rate its own flaws. A fresh sub-agent reads the batch cold and scores it against worded anchors. The reviewer supplies SCORES; a deterministic check (threshold 4) computes the verdict. This is the same shape as the eval-buyer-fit agent and the BAS resonance gate.

**Dispatch envelope** (orchestrator → reviewer sub-agent):
- The assembled batch FILE PATH (the `dct.json` — never paste copy inline; pasting loads the drafter's anchoring into the reviewer).
- The persona file path + the offer file path, so the reviewer can check call-out and proof against source.
- This rubric.
- Instruction: score every ad on all six dimensions 1-5 using the anchors below; quote the exact copy line that justifies the LOWEST score; return the JSON contract verbatim. Do not rewrite the copy.

---

## The six dimensions (score each 1-5, no half-points)

The PASS bar is **4** on every dimension, so 4 means "strong, no hedge" — not "good enough."

### 1. `hook_effort_two_jobs` — does the hook earn its 80% and do both jobs?

Ferres cites Ogilvy's ~80%-of-effort-on-the-headline ratio; the hook must (a) stop the scroll AND (b) tell the algorithm who to show it to — the words steer delivery, not just persuasion (05 §1).

- 5 = pattern-interrupt opener that ALSO carries avatar-specific language so Meta can target; no name-drop wallpaper.
- 4 = strong scroll-stop and clearly signals the avatar, one notch short of perfect.
- 3 = stops the scroll OR signals the avatar, not both.
- 2 = generic opener; a name-drop in line 1, or a template call-out ("If you're a coach doing $30k/mo…").
- 1 = no hook — opens on throat-clearing or founder credentials nobody outside the brand knows.

### 2. `call_out_and_who_not` — who it's for AND who it's NOT for

If the offer isn't for the masses, the ad must say who it's for and who it's NOT for — ideally in the hook; a single disqualifier sentence is enough (05 §2). Includes the brokie-bait and hidden-assumption scans.

- 5 = explicit call-out + a disqualifier (or "even if…" qualifier) drawn from researched disqualifying beliefs; no hidden assumptions; no "made $X fast/easily" brokie-bait.
- 4 = clear call-out, disqualifier present but soft.
- 3 = calls out who it's for but never who it's not — lets unqualified leads in.
- 2 = a hidden assumption the reader lacks ("your book") makes them self-disqualify, OR brokie-bait framing.
- 1 = no call-out; reads as for-everyone when the offer is niche.

### 3. `copyboarding` — every claim → objection → proof, handled in real time

Every claim raises an objection; crush each with proof and/or handling the moment it forms (the Agora copyboarding discipline). Objections come from research docs + ad comments, never the writer's guesses. Proof is "your god in copywriting" (05 §3).

- 5 = each major claim is paired with proof or an objection handled at the point it arises; proof is specific (numbers, named results, testimonials sourced).
- 4 = claims mostly handled; one minor claim leans on assertion.
- 3 = a real claim sits unhandled — the reader hears later lines through "yeah but…".
- 2 = multiple unhandled claims, or proof is vague ("trusted by many").
- 1 = pure assertion, no proof, no objection handling.

### 4. `native_feel` — reads as content, not as an ad

The best ads don't look like ads until late; very direct "obviously an ad" copy only converts the small now-buyer slice and won't scale (05 §4). A structurally trivial top performer still works: extended avatar call-out → their pains in their words → problem-solution → CTA.

- 5 = reads as organic content / a peer voice ("I am one of you") until the offer lands late.
- 4 = mostly native, one line tips into ad-voice.
- 3 = recognisably an ad early, but not pushy.
- 2 = salesy throughout; the reader's ad-filter is up from line 1.
- 1 = hard-sell wallpaper.

### 5. `word_economy` — every word earns its place

Word economy is the mastery test: fit everything required into the fewest words; cut all fluff. Body length is flexible, but every second/line must earn its place (05 §4).

- 5 = nothing cuttable; each line advances hook → problem → proof → CTA.
- 4 = tight, one or two trimmable phrases.
- 3 = noticeable padding or a repeated beat.
- 2 = bloated; the point arrives late.
- 1 = rambling; the reader scrolls before the point.

### 6. `compliance` — Meta-safe (⚠️ all platform-specific)

No income/money-amount claims; no personal-attribute call-outs ("you're morbidly obese…"); no graphic before/after; claims that survive disapproval (05 §6).

- 5 = clean: no income claims, no personal-attribute call-outs, no graphic before/after, no disallowed superlatives.
- 4 = clean but one phrase sits close to the line and should be softened.
- 3 = one likely-disapproval phrase present.
- 2 = a clear income/money-amount claim or personal-attribute call-out.
- 1 = multiple disapproval triggers — would get the ad (or account) actioned.

For each ad also return: `weakest` (lowest-scoring dimension name), `evidence` (the exact copy line that justifies the lowest score), `fix` (a concrete one-line repair).

---

## JSON contract (reviewer emits; code decides)

```json
{
  "gate": "copy_prelaunch",
  "dct_id": "<dct slug>",
  "threshold": 4,
  "ads": [
    {
      "id": "<ad/angle id>",
      "scores": {
        "hook_effort_two_jobs": 4,
        "call_out_and_who_not": 5,
        "copyboarding": 3,
        "native_feel": 4,
        "word_economy": 5,
        "compliance": 5
      },
      "weakest": "copyboarding",
      "evidence": "\"buyers overpay by tens of thousands\" — claim with no proof line behind it",
      "fix": "Add the sourced cost-of-mistake figure from the offer's lead-magnet claim, or reword to remove the number."
    }
  ]
}
```

### Decision rule (deterministic — code, not the reviewer)

Mirror `compute_gate_verdicts`:

- Per-ad: `min_score = min(all six dimension scores)`. `verdict = PASS if min_score >= 4 else FAIL`. Any non-integer or missing dimension fails closed (min_score 0). A JSON bool does not count as an int.
- Set: the batch passes when at least `min_pass_count` ads PASS (default = all ads in the batch; lower it per wave spec if a batch only needs a handful of strong winners). Otherwise `set_verdict = REVISE`.
- On REVISE: the orchestrator routes the FAILED ads back to the copywriter with their scores + `weakest` + `evidence` + `fix` — keep the passing ads verbatim, regenerate only the failures (same loop as `REGEN_ANGLES`). Re-run the gate. Do not advance to HITL Gate 3 until `set_verdict = PASS` or a recorded operator override.

Never trust the reviewer's own pass/fail opinion — recompute from the scores. The reviewer scores honestly because it does not control the verdict.

---

## Where this sits in the gate sequence

```
Phase 2 assembly → dct.json
  → Claim Gate (machine: every number sourced or cut)            [scripts/claim_gate.py --gate]
  → Copy Pre-Launch Rubric (fresh reviewer scores; code decides) [this file]
  → HITL Gate 3: human creative approval
  → Phase 3 render / allocate
```

Both machine gates run before the human ever sees the batch, so the human reviews only copy that is already sourced and already clears the Ferres quality bar.
