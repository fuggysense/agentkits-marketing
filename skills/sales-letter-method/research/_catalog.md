# BP Library Catalog — Phase 0a Baseline
Generated: 2026-05-27 | 15 source files

Scope: cataloging the existing best-practices starter set before Phase 0b pulls external material. Honest calibration: proof-backed = case study, named example, or scraped competitor evidence; partial = framework citation only; unbacked = assertion.

## Files

### references/cohesion-check.md
- Purpose: Stitcher-stage cohesion test that scores section boundaries (continuous/bridge/jump) and rewrites jumps using 4 bridge patterns (Echo / Escalate / Pivot / Answer).
- BP claim types: Structural, Voice
- Feeds reviewer(s): structural-audit, copy-chief
- Proof-backed: no — pure heuristic. No competitor examples; no A/B data. Strong logic, unproven empirically.
- Overlap: minor with copy-gems.md "Drafting Discipline" (per-component rhythm rules). Different layer: cohesion is between sections, drafting-discipline is within sections.

### references/competitor-analysis.md
- Purpose: Scrape report on 8 live competitor pages (real estate, roofing, coaching, funding, cash-buyer) — what 8/8 do, what 8/8 miss.
- BP claim types: Component, Voice, Buyer-friction
- Feeds reviewer(s): Halbert, Hormozi, copy-chief
- Proof-backed: yes — verbatim headlines + quotes from 8 named pages with vertical/market metadata. The strongest evidentiary file in the set.
- Overlap: heavy with copy-gems.md (copy-gems is the distilled techniques layer; competitor-analysis is the raw data). Intentional, not duplication.

### references/component-matrix.md
- Purpose: Phase 0 context-scan logic for the 13-component framework — include / skip / modify rules + narrator-POV gate + vertical-specific failure modes + cross-cutting requirement pointers.
- BP claim types: Component, Structural, Brand-doc-conflict
- Feeds reviewer(s): structural-audit, copy-chief
- Proof-backed: partial — vertical failure modes drawn from real client work (SG real estate, DTC supplements, B2B SaaS, coaching) but no A/B numbers. Hormozi adaptation footnote disclaims cargo-culting.
- Overlap: serves as the index for cohesion-check, objection-architecture, qualification-patterns, trust-density, mechanism-justification, markup-convention. Not a duplicate — a hub.

### references/copy-gems.md
- Purpose: 11 distilled techniques + verbatim copy gems extracted from the 8-page scrape, plus per-component drafting-discipline rhythm rules and length-creep discipline.
- BP claim types: Component, Voice
- Feeds reviewer(s): Halbert, copy-chief
- Proof-backed: yes — every technique cites a named source page; verbatim quotes attributed. Drafting-discipline section is heuristic only (no proof).
- Overlap: tight pairing with competitor-analysis.md (data → distilled). Drafting-discipline overlaps cohesion-check intra-section guidance.

### references/frameworks.md
- Purpose: Master fundamentals — Schwartz 5 awareness levels, Desire Layer Ladder (L1-L4), Halbert Boron, Sugarman slippery slide, RMBC knowledge-gap anchor (UMP/UMS), Hormozi Value Equation + Grand Slam, Kennedy 10-point + PS, Ogilvy headline laws, component-to-framework mapping.
- BP claim types: Component, Structural, Voice
- Feeds reviewer(s): Halbert, Schwartz, Hormozi (this is the canonical source for all three named reviewers)
- Proof-backed: partial — framework citations are legitimate but examples are constructed (sleep supplement, agent, SaaS) not from real campaigns with conversion data.
- Overlap: foundational; every other file extends it. No duplication.

### references/guarantee-variants.md
- Purpose: 5 guarantee variants for no-price funnels (no-pitch / value-pay / outcome / integrity-layer / conditional) + stacking strategy + placement + format template + red flags.
- BP claim types: Component, Buyer-friction
- Feeds reviewer(s): Hormozi, copy-chief
- Proof-backed: partial — integrity-layer pattern documented in 3/8 scrapes; other variants are Hormozi-derived assertions without case-study backing.
- Overlap: minor with objection-architecture.md (risk objection → guarantee stack). Different concern: this file owns the variant taxonomy; objection-architecture owns placement logic.

### references/markup-convention.md
- Purpose: Inline bracket markup spec — (h)/(b)/(u)/italic — render-agnostic, with frequency caps and stitcher/Conversion Gate enforcement rules.
- BP claim types: Structural, Voice
- Feeds reviewer(s): copy-chief
- Proof-backed: no — pure convention. No tested-vs-untested comparison.
- Overlap: none.

### references/mechanism-architecture.md
- Purpose: Phase 0.7 playbook — unique characteristic + discredit old solutions (named alternatives with structural failure modes), MAGIC naming, Grand Slam offer composition, branding-via-association + bouquet narrowing, What-Who-When scene picker for the 12 components.
- BP claim types: Component, Structural, Brand-doc-conflict
- Feeds reviewer(s): structural-audit, Hormozi
- Proof-backed: partial — worked examples (Stackworks, Fuggy's Media SG real estate) are operator's own work, not third-party validated. Strong structural logic.
- Overlap: heavy overlap with mechanism-justification.md (both own Component 5). mechanism-architecture owns Phase 0.7 upstream design; mechanism-justification owns the in-letter Job-5 prose justification. Differentiated by phase but vocabulary overlaps.

### references/mechanism-justification.md
- Purpose: Adds Job 5 (Justify) to Component 5 — 4 patterns (Cause-and-Effect / Contrast / First-Principles / Constraint) + length calibration + pattern selection by vertical.
- BP claim types: Component, Voice
- Feeds reviewer(s): Halbert, Hormozi, structural-audit
- Proof-backed: partial — examples are constructed (mortgage broker, Meta cold traffic) not from real letters with conversion data.
- Overlap: see mechanism-architecture.md above. Also light overlap with frameworks.md RMBC section on UMP-UMS logic.

### references/objection-architecture.md
- Purpose: 10 canonical objections with placement map across components + NAME/LEGITIMIZE/RESOLVE/BRIDGE micro-structure + 11-element CTA architecture checklist with word budgets.
- BP claim types: Component, Structural, Buyer-friction
- Feeds reviewer(s): Schwartz, Hormozi, structural-audit, copy-chief
- Proof-backed: partial — objection ordering "post-click drop-off analysis" claimed but no data shown. CTA 11-element checklist is heuristic, not measured.
- Overlap: none significant. Risk objection cross-links to guarantee-variants.md by design.

### references/qualification-patterns.md
- Purpose: Required qualification component — 3 blocks (Who this is for / Who this isn't for / Readiness Criteria) + placement strategy + tone calibration.
- BP claim types: Component, Buyer-friction
- Feeds reviewer(s): Schwartz, copy-chief
- Proof-backed: no — pure heuristic. Assertion that selectivity reads as premium has no citation.
- Overlap: minor with trust-density.md (signal #6: "Who it isn't for"). Cross-referenced explicitly.

### references/trust-density.md
- Purpose: 10 trust signal types + density calibration (signals per 200 words) + confidence-credibility pairing rule.
- BP claim types: Voice, Buyer-friction
- Feeds reviewer(s): Schwartz, structural-audit, copy-chief
- Proof-backed: no — assertion-based. The "sophisticated buyers convert on credibility not confidence" claim is uncited.
- Overlap: light with qualification-patterns.md (signal #6) and mechanism-justification.md (constraint pattern).

### sales-letter-audit/SKILL.md
- Purpose: Inverse skill — reads finished letters, extracts letter-skeleton.json (UMP, identity ladder, motifs, CTA architecture, proof inventory, AI-pattern flags, VOC-anchored findings), produces operator + client briefs with [H]/[M]/[L] severity tags.
- BP claim types: Component, Structural, Voice, Buyer-friction, Brand-doc-conflict
- Feeds reviewer(s): structural-audit (consumes the skeleton contract directly), copy-chief
- Proof-backed: yes — references real validation fixture (V4 first-time-buyer letter, Stackworks pilot, Neeza & Nizam). Corrections log shows iteration history.
- Overlap: defines the contract that sales-letter-method must satisfy; routing table targets sales-letter-method phases. Symbiotic, not duplicative.

### sales-letter-audit/skeleton-contract.md
- Purpose: JSON schema for letter-skeleton.json + re-entry routing table (priority 0 hard stops → priority 5 motif scrubs) + V4 validation case + versioning.
- BP claim types: Structural
- Feeds reviewer(s): structural-audit
- Proof-backed: yes — V4 validation case is concrete (specific expected values for a real letter).
- Overlap: none — contract definition.

### sales-letter-audit/corrections.md
- Purpose: Skill-specific output corrections from operator feedback — 260507 pilot lessons (no copywriter names client-side, friend-tone = honest-tone, severity tagging, register split) + 260508 v0.4 upgrades (VOC anchoring, MAGIC name check, discredit-old-solutions, replacement candidates for high-leverage elements).
- BP claim types: Voice, Brand-doc-conflict
- Feeds reviewer(s): copy-chief, structural-audit
- Proof-backed: yes — every correction tied to a specific session and pilot client (Jason/Stackworks).
- Overlap: none — operator memory.

## Coverage map (matrix)

| BP type | Files | Reviewer | Proof level |
|---|---|---|---|
| Component | component-matrix, copy-gems, frameworks, guarantee-variants, mechanism-architecture, mechanism-justification, objection-architecture, qualification-patterns, competitor-analysis, audit/SKILL | Halbert, Schwartz, Hormozi, structural-audit, copy-chief | mixed — strongest in competitor-analysis + copy-gems; weakest in qualification-patterns |
| Structural | cohesion-check, component-matrix, frameworks, markup-convention, mechanism-architecture, objection-architecture, audit/SKILL, audit/skeleton-contract | structural-audit, copy-chief | mixed — audit contract is concrete; cohesion-check + markup-convention are unbacked |
| Voice | cohesion-check, copy-gems, frameworks, markup-convention, mechanism-justification, trust-density, audit/SKILL, audit/corrections | Halbert, copy-chief | mixed — copy-gems strong, trust-density assertion-only |
| Buyer-friction | competitor-analysis, guarantee-variants, objection-architecture, qualification-patterns, trust-density, audit/SKILL | Schwartz, Hormozi, copy-chief | weak overall — heuristic-heavy, no friction-data citations |
| Brand-doc-conflict | component-matrix, mechanism-architecture, audit/SKILL, audit/corrections | structural-audit, copy-chief | partial — corrections.md is the strongest evidence |

## Overlaps to resolve

- **competitor-analysis.md ↔ copy-gems.md** — intentional pairing (raw → distilled). Keep both, but ensure copy-gems explicitly cites competitor-analysis as source-of-truth so reviewers don't double-count proof.
- **mechanism-architecture.md ↔ mechanism-justification.md** — both own Component 5. They split by phase (0.7 upstream vs in-letter Job 5) but the vocabulary collision is real. Recommend a one-paragraph "boundary clarifier" header in each file pointing at the other.
- **copy-gems.md drafting-discipline section ↔ cohesion-check.md** — drafting-discipline covers intra-component rhythm; cohesion-check covers inter-component transitions. Adjacent but not redundant; clarify with a one-line scope statement at the top of each section.
- **qualification-patterns.md signal #6 ↔ trust-density.md signal #6** — already cross-referenced. No action needed beyond keeping the link bidirectional.

## Gaps for Phase 0b to fill

1. **Hook/headline taxonomy (deep)** — frameworks.md covers Schwartz awareness + Ogilvy specificity, copy-gems gives 1 hero formula ("I Will + mechanism + outcome"). No taxonomy of curiosity vs declarative vs ad-bait-cleanup vs how-to-without-X vs case-study lead etc. Pull from Schwartz Breakthrough Advertising headline chapters + swiped.co niche-segmented headline analysis.
2. **Lead types beyond what's in frameworks.md** — frameworks gives Halbert "Dear avatar" + Sugarman slippery slide only. Schwartz/Carlton/Makepeace teach 6 distinct lead types (offer / promise / problem-solution / big-secret / proclamation / story). Critical for matching lead-type to awareness level. Pull from Schwartz + Makepeace.
3. **Video Sales Letter (VSL) patterns** — entire framework assumes text long-form. Some incoming URLs are VSLs. Need: VSL pacing (5-act / 7-act), opening-frame retention triggers, transcript-vs-on-screen-text split, the "shock-disrupt-reveal" cold open, the read-along reveal of the offer. Pull from Jim Edwards VSL methodology + Stefan Georgi VSL teardowns + RMBC VSL frame.
4. **Story-bridge / origin-story architecture** — frameworks mentions Halbert specificity and Kennedy 10-point but no dedicated story spec (origin moment / lowest point / discovery / proof / mission). Coaching + identity-shift offers depend on this. Pull from Russell Brunson Epiphany Bridge + Donald Miller StoryBrand SB7.
5. **Price-justification + value-stack patterns** — guarantee-variants and offer architecture skip price reveal logic because the skill targets no-price funnels. But several incoming STRONG URLs will be priced offers (info products, courses, SaaS). Pull price-anchoring (decoy / contrast / payment-split / "less than your daily X" / cost-of-inaction math) from Hormozi $100M Offers price chapter + Stefan Georgi swipe file.

(Honorable mentions, lower priority: P.S. tactics — frameworks gives a paragraph only, could be expanded; scarcity/urgency frameworks beyond Hormozi's "deadlines drive decisions" — Kennedy and Cialdini extensions; identity-shift mechanisms beyond the Desire Layer Ladder L4 hook in frameworks.md.)

## Recommendation

The existing library is **structurally complete but evidentially thin in 3 of 5 BP types**. Component, Structural, and Voice claims are reasonably covered (competitor-analysis + copy-gems + audit fixtures provide the spine). Buyer-friction and Brand-doc-conflict are heuristic-heavy with limited citations. The 5 listed gaps — especially VSL patterns (#3) and price-justification (#5) — are blockers for any reviewer working letters outside the no-price consulting/lead-gen niche the scrape was drawn from. Phase 0b is a hard requirement, not a polish pass, and should weight pulls toward proof-backed sources (Hormozi case studies, Schwartz tested examples, swiped.co documented controls) rather than additional assertion-based heuristics.
