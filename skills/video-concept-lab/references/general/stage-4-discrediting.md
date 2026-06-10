# Stage-4 Discrediting — Solution-Aware Buyer Framework

> **Source pattern:** Flakes (dandruff), Nirvara (iron/ferritin), Primal Queen (women's hormones), zinc7-teardown (raw newsletter).
> **Mark Schwartz, Stage 4 (Solution-Aware):** the buyer knows solutions exist, has tried some, and failed. The job is no longer to introduce the problem — it's to discredit the false solutions they already tried and earn permission to be the next attempt.

---

## When to load

Auto-loads when `concept-brief.json` has:
- `awareness_stage == "solution-aware"` AND
- `sophistication_stage >= 3` (saturated market — competitors all promise the same outcome)

Manual triggers (from `routing-overrides.md` V2-1): `solution-aware`, `jaded buyer`, `tried and failed`, `discredit competitor`.

If the brief is Unaware or Problem-Aware, do NOT load this file — it will mis-target. Use standard `concept-generation.md` instead.

---

## The 4 Moves (in order)

### Move 1 — Anger Recruitment

Convert the buyer's distrust of institutions (drugstore, mainstream medicine, "the industry") into purchase fuel. They are already angry. Don't manufacture it. Channel it.

**Halbert/Schwartz rule:** The anger must ALREADY live in the buyer's mind. If you have to argue them into it, you've manufactured the enemy and Schwartz's channeling principle will reject the ad as fake.

**Do:**
- Name the institution they already distrust ("drugstore iron," "Big Pharma," "dismissive doctors")
- Validate the distrust as correct ("your suspicion was right")
- Position the brand as the insider who escaped the system

**Don't:**
- Invent enemies the buyer doesn't already feel
- Use generic "the industry doesn't want you to know" without naming a specific actor
- Lecture or moralize — anger is a sword, not a sermon

**Flakes example:** *"Most shampoos don't kill the fungus. They just piss it off and make it worse."* Anger pre-existed (buyers were furious dandruff kept coming back). Ad named the enemy (drugstore shampoos) and validated the rage.

---

### Move 2 — Validation Flattery

Name the buyer's suspicion BEFORE they articulate it. The line lands as "this brand finally gets it" — but only because the line was inevitable. The buyer was already 80% of the way to the conclusion.

**Do:**
- Lead with a sentence the buyer has thought but never said out loud
- Match their interior monologue's exact level of frustration
- Pair the validation with mechanism (next move) to prevent it from being empty validation

**Don't:**
- Flatter the buyer's intelligence in a generic way ("smart shoppers like you")
- Validate something they DON'T actually believe — Schwartz violation
- Drag the validation into >2 sentences (it stales fast)

**Nirvara example:** *"Turns out I was using products that couldn't fix the problem even if I was using them correctly."* The buyer was already wondering why they failed. The ad answered before the question.

**takekine Iron-Pill-Quitter angle:** *"You did everything the doctor said. The labs came back 'normal.' You still feel like trash."* Names the suspicion (the system missed something) without the buyer having to defend it.

---

### Move 3 — Mechanism-as-Foreclose

Educate the buyer on the new mechanism in a way that simultaneously discredits the false solution they already tried. The mechanism IS the discrediting move — you don't need a separate "competitor is bad" sentence.

**The Flakes pattern:** "Dandruff isn't dry skin — it's a fungus called malassezia. Drugstore shampoo isn't designed to kill fungus; it's designed to wash flakes away. That's why it makes it worse over time."

The mechanism (fungus, not dry skin) **automatically forecloses** the false solution (moisturizing shampoos). No competitor was attacked by name — the mechanism did it.

**Do:**
- Frame the new mechanism so the false solution becomes obviously wrong in light of it
- Keep mechanism 1-2 sentences (full education comes later in the SL, not the ad)
- Pair with NEW-2 `common-enemy-bridge.md` for named-enemy frames when appropriate

**Don't:**
- Stack 3+ mechanism sentences in the ad — kills pacing
- Discredit the competitor without offering the replacement mechanism (creates anger with no resolution)

**Nirvara Big Idea:** *"Your hair runs on ferritin, not iron."* One sentence. Forecloses every iron supplement the buyer already tried.

**takekine Iron-Pill-Quitter mechanism:** *"Bloodwork measures circulating iron. Ferritin is the storage form. Most women run out of stores 8-12 weeks before bloodwork catches it."* Forecloses both drugstore iron AND the doctor who said "labs are normal."

---

### Move 4 — Pain Stacking via Specificity

Concrete symptom checklist where each item multiplies the previous. The buyer reads 3 items in a row, recognizes themselves, and the recognition compounds.

**Rules:**
- Each symptom must be specific enough to NOT apply to everyone (excludes "tired all the time" alone)
- Mix physical + emotional + relational symptoms (broadens recognition)
- 3-5 items maximum — more dilutes
- Pair with NEW-2 named enemy OR Move 3 mechanism for resolution

**Primal Queen example:** *"Buffalo hump. Itchy ear canals. Rage that came from nowhere. Anxiety so bad she developed a stutter."* — 4 hyper-specific symptoms. Average buyer recognizes 2-3, which feels like a diagnosis.

**takekine Iron-Pill-Quitter stack:** *"Tired by 2pm even on 8 hours sleep. Hair clogging the shower drain. Brain fog that makes you re-read emails 3 times. Heart racing when you climb one flight of stairs."* — 4 specifics, mix of physical + cognitive.

---

## Forbidden Patterns (auto-reject by seeder)

- **Manufactured outrage** — anger the buyer doesn't already feel. Schwartz channeling rule violation.
- **Generic competitor bashing** — "other brands suck" without named mechanism or institution.
- **Mechanism without proof** — the new mechanism must pair with ≥1 Specificity Shock element (load `.claude/references/copywriting-os/frameworks/six-proof-types.md` Type 5) and ≥1 Credibility layer (load `.claude/references/copywriting-os/frameworks/six-proof-types.md` + `.claude/references/copywriting-os/reviewers/proof-density-audit.md`).
- **Pain stacking without resolution** — 4 symptoms with no mechanism reveal = anxiety ad, not a Solution-Aware DR ad.
- **Validation flattery without mechanism follow-through** — empty pandering. Schwartz will reject.

---

## Worked Example — takekine Iron-Pill-Quitter (30s ad)

| Beat | Move | Copy |
|---|---|---|
| 0-3s | Validation Flattery | "You did everything the doctor said. Labs came back 'normal.' You still feel like trash." |
| 3-10s | Pain Stacking | "Tired by 2pm. Hair clogging the drain. Brain fog re-reading emails 3 times. Heart racing climbing one flight." |
| 10-15s | Anger Recruitment | "Here's the thing nobody told you. Drugstore iron doesn't fix this." |
| 15-25s | Mechanism-as-Foreclose | "Your hair, energy, and brain run on ferritin — the storage form. Bloodwork measures the wrong thing. Most women run out of stores 8-12 weeks before labs catch it." |
| 25-30s | CTA | "Find out what your real ferritin level is." |

---

## Cross-links

- `.claude/references/copywriting-os/frameworks/schwartz-channeling.md` — Stage 4 (Solution-Aware) channeling discipline
- `.claude/references/copywriting-os/case-studies/zinc7-teardown.md` — full primary-source breakdown of these 4 moves on a women's-supplement case
- `.claude/references/copywriting-os/frameworks/six-proof-types.md` — Type 5 (Specificity Proof) pairs with Move 4
- `skills/unique-mechanism-problem/SKILL.md` + `skills/unique-mechanism-solution/SKILL.md` — Move 3 mechanism construction
- `skills/video-concept-lab/references/general/common-enemy-bridge.md` (NEW-2) — Move 1 + Move 3 enemy composition
- `skills/video-concept-lab/references/general/video-compression-by-duration.md` — beat-sheet templates for 15s / 30s / 45s / 60s / 90s. **For Solution-Aware × Stage-3, 60s is the default** (all 4 discrediting moves get breathing room; 30s mutes Move 1 and Move 3).
