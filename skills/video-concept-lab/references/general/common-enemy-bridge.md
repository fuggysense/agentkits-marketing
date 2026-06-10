# Common Enemy Bridge — "Us vs. Them" Composition

> **Why this file exists:** The routing-overlap audit (2026-05-19) confirmed copywriting-os has no dedicated framework for **composing** an "us vs. them" line. Scout Mode finds the enemy. Coat of Arms maps what was tried. Legend Architecture frames brand authority. But no file teaches how to assemble them into a single, ad-ready Common Enemy frame.
> This file is the composition bridge. ~120 lines. Small on purpose.

---

## When to load

Auto-loads when `concept-brief.json` has:
- `awareness_stage == "solution-aware"` AND `sophistication_stage >= 3`, OR
- The brief explicitly requests "us vs. them," "competitor positioning," or "villain frame."

Manual triggers (from `routing-overrides.md` V2-1): `common enemy`, `us vs them`, `competitor positioning`, `villain frame`.

---

## The Schwartz Authenticity Gate (READ FIRST)

> **Schwartz, *Breakthrough Advertising*:** "The job of copy is not to create desire — that is the role of biology, environment, and time. The job of copy is to channel desire that already exists into the product."

Applied to Common Enemy: **the enemy must already live in the buyer's mind.** If you have to argue them into hating it, the frame is manufactured and the ad will read as fake.

**Test:** can you find ≥10 verbatim buyer quotes (Reddit, reviews, complaints) where the buyer names this enemy spontaneously, with anger? If no → enemy is manufactured → reject the frame.

This gate runs BEFORE the 4-step composition below.

---

## The 4-Step Composition Recipe

### Step 1 — Scout Mode finds the undefended territory

Load `.claude/references/copywriting-os/frameworks/scout-mode-instructions.md`.

Mine 20+ reviews, 5+ competitor campaigns, 10+ support tickets, raw surveys. Look for:
- Repeated buyer complaints about a specific actor (brand, institution, profession)
- Frustration patterns the dominant solutions DON'T address
- Verbatim language naming the enemy (don't paraphrase)

**Output:** a 1-sentence "undefended territory" statement. E.g., "Women on iron supplements complain repeatedly that doctors dismiss their 'normal labs' even though they feel terrible."

---

### Step 2 — Coat of Arms names the failed prior attempts

Load `.claude/references/copywriting-os/frameworks/halbert-trio.md` (Coat of Arms section).

The buyer has a personal history of failed attempts. List them in the order the buyer tried them:
1. First attempt (usually generic/category-level — e.g., drugstore iron)
2. Second attempt (usually institutional — e.g., doctor visit + bloodwork)
3. Third attempt (usually mechanism-level — e.g., different brand, higher dose)

Each failed attempt is a candidate for naming as the enemy. Pick the one the buyer is MOST recently angry about.

---

### Step 3 — Legend Architecture frames brand authority over mainstream

Load `.claude/references/copywriting-os/frameworks/legend-architecture.md`.

Position the brand as the outsider who saw what the mainstream missed. Required structure:
- **Insight moment** — what the founder/brand realized that mainstream still doesn't admit
- **Defection** — why they had to break from the mainstream approach
- **Earned authority** — proof they're not just contrarian (credentials, lived experience, results)

Without earned authority, anti-mainstream positioning reads as conspiracy. With it, it reads as insider knowledge.

---

### Step 4 — Schwartz Authenticity Re-Check

Before publishing, re-run the Schwartz gate from the top of this file. The composed Common Enemy must pass:
1. Does this enemy already live in the buyer's mind? (≥10 spontaneous mentions in scout data)
2. Is the anger pre-existing, or are we manufacturing it?
3. If we removed our brand from the ad, would the buyer still recognize the enemy?

If any "no" → return to Step 1 with a different enemy candidate.

---

## 3-Tier Enemy Taxonomy

Pick the tier that matches the buyer's articulation. Mixing tiers in one ad creates confusion.

### Tier 1 — Category-Level
The enemy is a generic product class.
- **Examples:** drugstore iron, mass-market shampoo, sugar-loaded sports drinks, supermarket multivitamins
- **When to use:** buyer is angry at "what's on the shelf" without naming a brand. Broadest reach, least edge.
- **Risk:** can feel generic. Pair with Tier 3 mechanism specifics to sharpen.

### Tier 2 — Institution-Level
The enemy is a profession, gatekeeper, or organization.
- **Examples:** dismissive doctors, Big Pharma, the wellness industry, "labs are normal" specialists
- **When to use:** buyer has a specific institutional grievance with verbatim language. Strongest edge, highest risk.
- **Risk:** Schwartz authenticity gate is hardest to clear here. Manufactured-outrage trap.

### Tier 3 — Mechanism-Level
The enemy is a specific ingredient, formulation choice, or method.
- **Examples:** sulfates, synthetic hormones, low-dose pyrithione zinc, ferrous sulfate, fillers
- **When to use:** buyer is mechanism-curious or already educated. Strongest "insider" positioning.
- **Risk:** requires more on-screen education time. Less scrollable.

---

## Forbidden Patterns

- **Manufactured enemies** — enemy doesn't exist in buyer's mind. Schwartz violation.
- **Fake villains** — invented mascots, strawmen, "evil corporation X." Reads as ad-speak.
- **Tier mixing** — naming Big Pharma + drugstore brands + sulfates in one ad. Confusion.
- **Enemy without resolution** — naming the villain without offering the replacement mechanism. Creates anger with nowhere to go.
- **Brand-vs-brand attack** — naming a specific competitor by brand name. Legal risk + reads as petty.

---

## Worked Examples

### Flakes (dandruff)
- **Tier:** Category (drugstore shampoo) + Mechanism (sulfates)
- **Composition:** Scout → buyers furious dandruff returns / Coat of Arms → Head & Shoulders, Selsun Blue, "natural" alternatives all failed / Legend → "dermatologist formulated" + 1M+ bottles sold / Schwartz → "drugstore shampoo feeds the fungus" passes authenticity (buyers already suspect this)

### Nirvara (iron / ferritin)
- **Tier:** Category (pharmacy iron) + Institution (dismissive doctors)
- **Composition:** Scout → women complain "labs normal but I feel terrible" / Coat of Arms → drugstore iron, doctor visits, blood panels / Legend → nurse + cancer researcher founders / Schwartz → "doctors miss ferritin" passes (women already feel medically gaslit)

### Primal Queen (women's hormones)
- **Tier:** Institution (Big Pharma) + Mechanism (synthetic HRT)
- **Composition:** Scout → women angry at synthetic-HRT side effects / Coat of Arms → birth control, HRT, "lifestyle" advice / Legend → "I lived it. Diets, powders. Nothing worked." / Schwartz → "Big Pharma + synthetic hormones" passes (anti-pharma anger is pre-existing)

### takekine Iron-Pill-Quitter
- **Tier:** Category (drugstore iron) + Institution ("labs are normal" doctors)
- **Composition:** Scout → SG/JP women on Reddit complain about constipation from drugstore iron + dismissive GP visits / Coat of Arms → drugstore iron + GP visit + "wait and see" advice / Legend → founder/brand authority TBD / Schwartz → passes (verbatim quotes exist on r/singaporefi, takekine reviews)

---

## Cross-links

- `.claude/references/copywriting-os/frameworks/scout-mode-instructions.md` — Step 1 mining playbook
- `.claude/references/copywriting-os/frameworks/halbert-trio.md` — Step 2 Coat of Arms
- `.claude/references/copywriting-os/frameworks/legend-architecture.md` — Step 3 brand authority
- `.claude/references/copywriting-os/frameworks/schwartz-channeling.md` — Step 4 authenticity gate
- `skills/sales-letter-audit/` — post-draft discredit-check (validates composed enemy)
- `skills/video-concept-lab/references/general/stage-4-discrediting.md` (NEW-1) — pairs with this file when Solution-Aware × Stage-3
