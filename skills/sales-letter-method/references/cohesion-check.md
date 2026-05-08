# Cohesion Check

The teardown flagged: "each section must answer the question created by the prior section." The current pipeline's Stitcher (Phase 2) smooths transitions but doesn't test them. This adds an explicit cohesion test.

**Where it runs:** Phase 2 Stitcher, before handoff to Phase 3 Conversion Gate.

---

## The Cohesion Principle

A long sales letter is an argument in sequence. Every component plants a question; the next component resolves it and plants the next.

If the reader finishes a section thinking *"…and so what?"* and the next section doesn't answer, you've lost them.

---

## The Expected Question Chain

Each component creates a specific question the next component must earn the right to answer.

| After reading... | Reader's next question | Next component answers... |
|------------------|------------------------|---------------------------|
| 1. Headline | "Is this actually real? Who says?" | 2. Subheadline (qualifying + intensifying) |
| 2. Subheadline | "Okay, who is this for — is it me?" | 3. Lead (restates offer in reader's language) |
| 3. Lead | "Why hasn't this worked for me before?" | 4. Pain Cycle (dismantles old way) |
| 4. Pain Cycle | "So what's the alternative?" | 5. Integrity Tie-Down → 6. Mechanism |
| 5. Mechanism | "Does this actually work for people like me?" | 7. Proof Stack |
| 6. Proof | "What exactly do I get if I move forward?" | 8. Offer Breakdown |
| 7. Offer | "What's the risk if it doesn't work?" | 9. Guarantee Stack |
| 8. Guarantee | "What if I'm not ready / not sure / have concerns?" | 10. FAQ |
| 9. FAQ | "Alright — what do I do now?" | 11. CTA |
| 10. CTA | "Am I going to regret this?" | 12. PS Line |

(Numbering reflects sequence, not component IDs.)

---

## The Cohesion Test (run in Stitcher)

For each section boundary in the draft:

1. **Extract the last sentence of section N.**
2. **Extract the first sentence of section N+1.**
3. **Ask:** Does the first sentence of N+1 feel like a natural continuation of the argument N just made, OR does it feel like a topic jump?
4. **Score:**
   - `continuous` — reads like one voice continuing
   - `bridge` — acknowledges the prior section before pivoting
   - `jump` — starts a new topic with no acknowledgment
5. **Flag all `jump` transitions.**

---

## Transition Rewrite Heuristics

When a transition scores `jump`, rewrite using one of these 4 bridge patterns:

### Bridge 1 — Echo
Repeat a key phrase from the prior section.
```
[End of section N: "...the 17-Day Method was built to close that gap."]
[Jump: "Here's how the process works..."]
[Echo rewrite: "Here's how the 17-Day Method actually works — step by step."]
```

### Bridge 2 — Escalate
Raise the stakes the prior section established.
```
[End of section N: "...which is why most agents plateau at 8 deals a year."]
[Jump: "Our system uses AI-powered lead scoring..."]
[Escalate rewrite: "And plateauing at 8 deals a year isn't a skill problem — it's a system problem. Here's the system that breaks the ceiling."]
```

### Bridge 3 — Pivot
Name the pivot explicitly.
```
[End of section N: "...so that's what's broken about the old way."]
[Jump: "We work with clients who..."]
[Pivot rewrite: "So what does the fixed version look like? Start here."]
```

### Bridge 4 — Answer
Treat N+1 as the answer to N's implied question.
```
[End of section N: "...and most methods just don't work at this scale."]
[Jump: "The guarantee is simple..."]
[Answer rewrite: "You might be wondering what happens if this doesn't work for you either. The guarantee is simple..."]
```

---

## Cohesion Metrics

Run the check across all section boundaries. Target:

| Letter quality | `continuous` + `bridge` ratio | `jump` tolerance |
|----------------|-------------------------------|------------------|
| Passing | ≥ 85% of boundaries | ≤ 15% |
| Strong | ≥ 95% | ≤ 5% |
| Premium | 100% | 0% |

Any `jump` at Headline→Sub, Sub→Lead, Lead→Pain, Pain→Mechanism, or CTA→PS is an auto-fail — these are the 5 highest-friction boundaries and must be airtight.

---

## Stitcher Output Format

After cohesion check, Stitcher outputs:

```
COHESION REPORT
Boundaries tested: 11
  continuous: 7
  bridge: 3
  jump: 1

FLAGGED TRANSITION:
  Section 4 (Pain Cycle) → Section 5 (Mechanism)
  Last sentence: "...and that's why prospecting feels like shouting into the void."
  First sentence: "Our system is called the Appointment Engine."
  Score: jump
  Rewrite using: Bridge 3 (Pivot)
  Proposed fix: "So what breaks the void? A system that puts prospects in front of you, not the other way around. It's called the Appointment Engine."

APPLY REWRITE? [Y/n/manual]
```

Auto-apply on `Y`, skip on `n`, or hand to user for manual rewrite.

---

## Anti-Patterns

- **Restating the whole prior section in the transition** — creates redundancy, not cohesion
- **Transitional filler** ("Now let's talk about...", "Moving on...", "Next up...") — breaks the conversational register
- **Cliffhanger transitions that don't resolve** — creates friction, not flow
- **Over-bridging** — every section starts with a 2-sentence recap

---

## Diagnostic Test

Before Phase 2 Stitcher hands off to Phase 3 Conversion Gate:

- [ ] All 11 section boundaries tested
- [ ] No `jump` at the 5 critical boundaries (H→S, S→L, L→P, P→M, CTA→PS)
- [ ] Overall `jump` count ≤ 15% of total boundaries
- [ ] Transitional filler phrases flagged and removed
- [ ] Each section begins by either echoing, escalating, pivoting, or answering the prior section
