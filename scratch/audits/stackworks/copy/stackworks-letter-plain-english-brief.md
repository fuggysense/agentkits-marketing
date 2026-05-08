# Stack Letter — Audit Brief

**Source:** `scratch/audits/stackworks/copy/stackworks-letter.md`
**Audited:** 2026-05-07
**Reading-level target:** Hemingway grade ≤5
**Audit type:** First-pass review for operator decision-making
**Deeper diagnostic:** [stackworks-letter-skeleton.json](stackworks-letter-skeleton.json) (data) + [skeleton-summary.md](stackworks-letter-skeleton-summary.md) (technical)

---

## Purpose & Scope

This audit evaluates the source letter on four dimensions: **conversion potential**, **grammar & clarity**, **anti-AI patterns**, and **next moves**. It's a first-pass review for operator decision-making. It does not replace the structural skeleton (the deep diagnostic) and does not produce a rewrite (that's `sales-letter-method` Phase 4 — Polish).

## Summary scores (1–5, 5 = strongest)

| Dimension | Score | One-line read |
|---|---|---|
| Conversion potential | **3** | Strong structural moves. Trust chain broken by zero named investor outcomes. |
| Grammar & clarity | **4** | Mostly tight. A few run-on sentences and worn motifs. |
| Anti-AI patterns | **2** | 9 patterns surfaced — 2 hard flags, 7 soft. |
| Mobile readability | **4** | Sections short; bullets help; some long quoted blocks. |
| **Overall ship readiness** | **2** | Trust gap + UMP collision + headline AI-tell are blockers. |

---

## 1. Conversion Potential

### What's working

- **The headline names the real problem in one sentence:** *"You don't have a strategy problem. You have an execution problem."* Most readers walk in blaming strategy. The headline points them at execution. *(Note: form of this headline is flagged in §3.)*
- **The two competing paths are dismissed with real reasons.** The private banker has a conflict of interest built into their job. The DIY investor cannot stay calm enough to act. Both reasons hold up for a $500K reader.
- **The Tesla / Amazon / Nvidia example uses a habit the reader already has.** They run systems in their business. The line *"you run your business on systems. Your capital deserves the same"* moves that habit to their money.
- **The before/after section is concrete:** *"You check the market between meetings... You stop watching."*

### What's broken

1. **No customer outcomes anywhere.** Every trust signal is founder credentials (JPMorgan, Citibank, two decades) or one anonymous quote: *"an investment bank and a global family office are keen to acquire Stack."* Both unnamed. The reader cannot check either claim. A reader with $500K decides on what happened to people like them. The letter shows zero. **→ See Recommendation 1.**
2. **Two product names compete for the same job.** "Stack" arrives word 50. "TripleStack™" arrives word 510. By the time TripleStack lands, the reader has built a picture of Stack and now must merge two ideas. **→ See Recommendation 2.**
3. **The closing CTA gives the reader no way to self-check "is this me?"** The mid-letter "Stack is for you if / not for you if" section gives the test. The close at the bottom does not. **→ See Recommendation 3.**

### Headline / benefits / CTA quick-check

- **Headline grabs attention:** ✅ Yes (problem reframe in one sentence).
- **Benefits clear:** ⚠️ Partly — *what* the system does is clear; *what the reader gets* (returns? Sharpe? AUM growth?) is never quantified.
- **CTA strength:** ⚠️ Soft — "Request Private Access" repeated 3×, application-only framing is good, but no self-check at close, no PS, no value recap.

## 2. Grammar & Clarity

### Sentence-level findings (rewrite candidates)

- **62-word run-on in The Guide:** *"Two decades inside JPMorgan and Citibank gave me a precise view of how institutional execution actually works — the infrastructure, the discipline, the edge that institutional desks have built and private investors were simply never given access to."* — Three clauses chained with em-dash + "and." **Suggested split:** *"Two decades inside JPMorgan and Citibank showed me how institutional execution works. Private investors never get the same access."*
- **Long Path-One sentence:** *"Sounds like the sophisticated choice — until you realise those advisors are managing dozens of relationships, answering to their own institutions and optimising for their interests as much as yours."* — 30+ words, three present participles. **Suggested split:** *"Sounds like the sophisticated choice. Then you realise: those advisors juggle dozens of clients. They answer to their own bank. They optimise for the bank's interests, not yours."*

### Repetition fatigue

- *"Execution"* appears 17× across ~1,300 words (≥1% of the letter). After the third use, the reader stops registering it. Cut decorative uses, keep claim-bearing ones.
- *"Time, energy, attention"* recited 4× as a triplet. Each repeat doesn't add new claim weight.

### Mobile readability

- ✅ Sections are short, headers help scrolling.
- ✅ Bullets and numbered lists break up text.
- ⚠️ The TripleStack roman-numeral block (I — Price / II — Time / III — Position Size) takes vertical space on a phone. Consider tighter prose form for mobile.
- ⚠️ The Tesla / Amazon / Nvidia analogy block is heavy on a small screen. Trim or merge.

### Singapore-streets test (no Singlish, simple English)

- ⚠️ *"structural execution discipline"* — too jargony for a reader on the MRT. Replace with *"running your money on rules instead of mood."*
- ⚠️ *"Architect of the TripleStack™ execution method"* — reads pompous. *"Built TripleStack™"* is enough.
- ✅ Most other language is plain enough.

## 3. Anti-AI Detection

Both anti-AI checklists were applied to the source letter: `skills/copy-editing/references/overused-ai-patterns.md` (marketing register: Big Contrast, Revelation Hook, Elliptical Setup, Great Reframe, Philosophical Reduction) and `skills/copy-editing/references/anti-ai-patterns.md` (analytical register: negative parallelisms, vague attributions, rule of three, em-dash density, copulative avoidance). Nine patterns surfaced.

### Hard flags — rewrite before ship

1. **Headline uses Big Contrast.** Form: *"You don't have X. You have Y."* (`overused-ai-patterns.md §3`). AI-default rhetorical move in 2026. **A/B candidate:** *"Most private investors fail to pull the trigger when the window opens."*
2. **Big Contrast repeats 3× in body.** *"Conflict of interest is not an accusation. It is the structure of the relationship."* / *"Stack is execution, not education."* / *"Rules run. Not feelings."* Once is a flourish. Three+ is a tic. **Pick one to keep, rewrite the others as direct claims.**

### Soft flags — work for buyers, A/B-worthy

3. **Rule of three, used 8+ times.** Triplets across the letter: *"Time, energy, attention"* (4×), *"Tesla, Amazon, Nvidia"*, *"the infrastructure, the discipline, the edge"*, *"capital, knowledge, opportunity"*, *"cleanly, consistently and without emotion"*, *"Consistent, tireless, independent"*. Each tidy. Stacked, the letter sounds preset. **Cut 3–4 of the weakest.**
4. **Negative parallelism, 3 places.** *"not because they were wrong... but because they could not execute"* / *"not intelligence, not opportunity, not strategy"* / *"is not a neutral hour. The market moved. Your capital didn't."* AI overuses this to sound balanced. **Replace with direct positive claims.**
5. **Aphoristic reduction, 3 places.** *"Rules run. Not feelings."* / *"Your capital stays active. Your life stays yours."* / *"They built systems."* Each works alone. Stacked, reads as AI poetics. **Keep one.**
6. **Revelation Hook, 2 places.** *"Private investors were simply never given access to it."* / *"the edge that institutional desks have held for decades is now accessible."* Trips the "selling-me-something" sensor.
7. **"No X" stacking, 2× in close range.** *"No screens... No daily burden... No emotional execution"* + *"No discretion. No emotion. No second-guessing."* Pattern fatigue.
8. **Em-dashes used as parentheticals, 10+ times.** Density became an AI-default after 2024. **Halve them.** Replace with periods or commas.
9. **Before/After binary template.** Familiar AI-shape. Content survives because it's concrete. Soft flag — keep the structure, vary surrounding rhythm.

## 4. Notes & Recommendations

1. **Find one named investor outcome for "The Guide" section.** A real person, initials and city for privacy, with one specific result. If Stack is too new for client testimonials, replace the anonymous *"investment bank and family office"* line with one specific institutional credential Jason can name and verify. *(Resolves: Conversion #1, ship-readiness blocker.)*

2. **Decide whether the brand-mechanism is "Stack" or "TripleStack™."** Likely: Stack stays as the company name; TripleStack™ moves up to first appearance by word 200. *(Resolves: Conversion #2, UMP collision.)*

3. **Add a 3–4 line self-check just before the final "Request Private Access" button.** The reader needs to answer "is this me?" one last time without scrolling back. *(Resolves: Conversion #3, CTA gap.)*

4. **Cut 3–4 weakest Rule-of-three triplets and halve em-dashes.** Each repetition should attach to a specific claim or come out. *(Resolves: Grammar repetition fatigue + Anti-AI #3 + Anti-AI #8.)*

5. **Rewrite the headline + the 3 body Big Contrasts as direct claims.** Pick one Big Contrast to keep as flourish; the others get rewritten without the flip. *(Resolves: Anti-AI #1, #2.)*

6. **Split the two flagged run-on sentences** (The Guide + Path One). Use the suggested rewrites in Grammar §1. *(Resolves: Grammar sentence-level findings.)*

---

*Companion files: skeleton.json (data), skeleton-summary.md (technical), reverse/* (back-inferred research). Anti-AI checklists: skills/copy-editing/references/{anti-ai-patterns,overused-ai-patterns}.md.*
