# Learnings Template — Wave Conclusion Append

What feedback-router auto-appends after every wave decision. Two files get touched. Both follow the Marketing CLAUDE.md self-annealing rule.

---

## File 1 — `clients/<slug>/learnings.md`

Append a wave-conclusion entry. Format:

```markdown
### Wave [N] conclusion (YYYY-MM-DD)

**Spend:** S$[total] over [N] days · **Routing decision:** [NEW | BETTER | MORE]

**Winning angle:** [Angle name]
- CPA: S$[X] (vs KPI target S$[Y], baseline S$[Z])
- CTR: [X]% · Hold-rate: [X]% · Frequency: [X]

**Underperforming (cut):** [List of cut angles with their CPA]

**What we learned about the buyer:**
- [1-2 sentence pattern observation grounded in metric — not speculation]
- e.g., "Wife-voice UGC outperforms founder explanation 3x on hold-rate. Buyer responds to peer recognition, not authority on this angle."

**What we learned about the angle/execution:**
- [1-2 sentence pattern observation about what worked structurally]
- e.g., "Identification opens (Scene 1 = mirror buyer's exact situation) outperformed claim opens at L4 sophistication. Confirms sophistication-creative-map.md."

**What we changed in the strategy stack:**
- [If NEW: SoT sections refreshed]
- [If BETTER: which angle gets re-ideated]
- [If MORE: which winning combo gets expanded + how]

**Next action:** [exact slash command]

---
```

This format is greppable for cross-wave pattern detection. Future waves read prior wave-conclusion entries to avoid re-learning.

---

## File 2 — `clients/<slug>/angles/iteration-log.md`

Append a wave entry. Format:

```markdown
## YYYY-MM-DD — Wave [N] conclusion + Wave [N+1] kickoff

**Wave [N] outcome:** [route decision in 1 sentence]

**Winners promoted:**
- [Batch ID + angle + winning metric]

**Cuts:**
- [Batch ID + angle + losing metric + why]

**Watch list (warning, hold for now):**
- [Batch ID + angle + warning condition]

**Wave [N+1] direction:**
- Route: [NEW | BETTER | MORE]
- Locked: [what stays the same — angle / format / hook pattern]
- Variable being tested: [what's new in next wave]

**SoT impact:** [either "no impact" OR "if NEW, SoT §X being refreshed"]

---
```

This pairs with the existing iteration-log entries (per `clients/neezanizam/angles/iteration-log.md` 260418) so wave-by-wave evolution is documented in ONE place.

---

## What NOT to append

The router should NOT append to learnings.md/iteration-log.md when:

- Pre-routing gates fail (insufficient spend) — surface the gap, don't pollute the log with "couldn't route"
- The decision is the same as the prior wave (e.g., MORE → MORE → MORE without new signal) — append ONCE per direction change, not every wave that confirms the prior direction. Add a 1-line "Wave N also chose MORE — winning combo still scaling, no new pattern" instead of re-pasting the full template.
- The user manually overrides the router's decision — log the override + reasoning, not the auto-decision

---

## What this enables downstream

After 3+ wave-conclusion entries accumulated:

1. **`source-of-truth` Phase 2 enrichment** — re-running SoT can read these entries and pre-populate §17 Iteration Rules with the client's actual iteration patterns (not generic templates)
2. **`avatar-research` re-runs** — wave-over-wave learnings about what worked per avatar can refine the 16-point breakdown
3. **`ad-concept-engine` Phase 1** — angle generation can pull from "what beat baseline last wave" as a positive prior, not just from the swipe file
4. **Cross-client pattern mining** — accumulated learnings.md across clients with same product_type produce the next layer of the sophistication-creative-map (currently example-based; can become evidence-based)

The compounding only happens if the appends happen. This is the most important step in the pipeline.
