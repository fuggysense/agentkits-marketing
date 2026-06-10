# Creative-Director-Skill Comparison — 260520

**Audit ID:** creative-director-comparison-260520
**External target:** https://github.com/smixs/creative-director-skill (subpath `creative-director/`)
**Local clone:** `~/Downloads/creative-director-skill` (read-only, no install)
**Operator scoring lens:** Hook quality (first-frame thumbstop + specificity)
**Off-limits zones (operator-declared):** AG1/AG2 approval gates, vid-director phase pipeline
**Test corpus:** Takekine Ferrovia — `campaigns/test_2/video-concepts/dr-foundation-pilot/`
**Replacement appetite:** DECIDE-AFTER-ANALYSIS (present both cases)

Supporting detail in `/tmp/cd-comparison-260520/`:
- `phase1-S1-external-audit.md` · `phase1-S2-our-seeder-skill.md` · `phase1-S3-reference-diff.md` · `phase1-S4-schema-diff.md`
- `external-concepts.{json,md}` · `ours-concepts.{json,md}`
- `phase2-eval-universal.md` · `phase2-eval-buyerfit.md`

---

## Executive verdict

**IMPROVE — cherry-pick 5 assets from external as add-on reference nodes; keep our seeder, pipeline, and gates intact.**

One-sentence reason: external is a Cannes/D&AD brand-platform craft skill with strong idea-taxonomy and pattern-library discipline, but it has **no claim-safety mechanism, no awareness/sophistication routing, no hook schema, no JSON contract, and would force 5 hard violations of the off-limits zones** — yet it carries 2-3 portable frameworks and one empirical hook-pattern insight worth borrowing.

**REPLACE case:** rejected. External fails 0/3 on the AG1 buyer-fit hard-gate; all three of its concepts close at the wrong awareness rung; methodology has no internal mechanism to self-correct.

**BUILD-ON case:** weaker than IMPROVE. Cherry-pick gets the same upside (insight-mining + pattern library + artifact-hook pattern) with less ambiguity than running external as a parallel ideation surface.

**KEEP-AS-IS case:** leaves the empirical artifact-hook lesson and the tried-and-discounted-prose craft on the table.

---

## Structural diff matrix (Phase 1)

### Architecture

| Dimension | Ours | External |
|---|---|---|
| Dispatch | Subagent (`video-concept-seeder`) under vid-director Phase 1, persistent iterative chat | Pure Claude Code skill via NL triggers |
| Model | Opus (frontmatter) | Unspecified — runs on user's current model |
| Brief contract | 34 typed JSON fields, schema_version 2.0 | Free prose intake bullets, no schema |
| Output contract | 28-field `concepts-draft.json` + 5 sibling artifacts (approval-1, methodology_receipt, inputs-used, etc.) | Markdown via 4 templates, no JSON, no HITL artifact |
| Concept count | N=5 multi-clip / N=10 single-clip (locked) | 8-12 ideas → top 3 (warmup-first-3 rule) |
| Scoring | 4-axis Video-Native Compass (1-10 each, fail <24/40 or claim_safety <5) | 6-criterion weighted (Originality 0.25 + Strategic Fit 0.20 + Emotional 0.20 + Feasibility 0.15 + Scalability 0.10 + Simplicity 0.10), threshold 9.0 + HumanKind ≥7, recursive up to 5 passes |
| Claim safety | Hard guardrails: forbidden_expressions auto-redraft, credibility_stack, FDA/Meta-aware | None |
| HITL gate | approval-1.json + eval-buyer-fit + eval-video-universal mandatory before AG1 render | None — recursive auto-loop until threshold |
| Security | n/a (in-house) | CLEAN — no secrets, no install scripts, no network calls, MIT |

### Framework coverage (24 ours-files + 12 external framework files; S3 read all 36 end-to-end)

| Classification | Count | Notes |
|---|---|---|
| OVERLAP (full) | 1 | Scoring rubrics — both have one, different criteria sets |
| PARTIAL OVERLAP / philosophy conflict | 4 | Constitution-style judgment vs flat avg, etc. |
| OURS-UNIQUE | 16 | Schwartz Stage-3/4 discrediting, Halbert Trio, V2V matrix, Common Enemy Bridge, Specificity Shock, Six Proof Types, Creative Lanes, hook-and-format-rules, video-compression-by-duration, suno/singing layer, claim-safety guardrails, methodology_receipt protocol, et al. |
| EXTERNAL-UNIQUE | 8 | Pollard 7-level taxonomy, Legendary Pattern Map P01-P18 (571 campaign cards, ~43% stub), Insight Mining tensions, IKRA Constitution, Disney/Pixar/Sparkline/Hero's Journey storytelling frameworks, Crazy 8s + Brainwriting + Six Hats + Oblique Strategies catalog, HumanKind sub-score, Grey Scale |
| Hard conflicts | 2 | Scoring rubric criteria + recursive Phase-4 loop |
| Soft conflicts | 3 | Concept count, brand-vs-DR philosophy, output template form |

**Hook-quality coverage (operator's primary lens):** **OURS owns this.** Ours has a dedicated 4-field hook schema (verbal/visual/rendered_text/subtitle_policy), scroll-stop velocity scoring at 0.5-1.5s Meta-feed resolution, duration-specific hook beats, and lane-to-hook archetype mapping. External has no dedicated hook file; hooks are folded into narrative act-1 / opening-beat discussion at story-level resolution, not 0-3s scroll-stop resolution.

### Schema compatibility

- External → ours: **HARD FAIL.** Missing schema_version, methodology_loadout_id, micro_persona structure, awareness/sophistication stages, creative-diversity-map. 27 of our 34 brief fields have no external slot.
- Ours → external: passes loosely; external ignores ~80% of our fields.
- **Off-limits violations if external were dropped in:** 5 blocking issues — recursive PASS 0-5 loop replaces linear pipeline; no approval-1.json / eval-buyer-fit; no methodology_receipt; prose output breaks `02_ag1-options/` folder contract; concept count contract mismatch.

---

## Empirical scorecard (Phase 2 — Takekine `dr-foundation-pilot` brief)

Both generators simulated on Sonnet against the same brief. External held to its own methodology (no fallback to our frameworks). Ours held to seeder spec with full methodology_receipt.

### Video-Native Compass (eval-video-universal rubric)

| Axis | External avg (n=3) | Ours avg (n=5) | Delta |
|---|---|---|---|
| first_frame_thumbstop | **7.67** | **7.60** | **-0.07 (tie)** |
| spine_clarity | 8.33 | 8.60 | +0.27 |
| flow_renderability | 7.33 | 8.60 | +1.27 |
| claim_safety | 6.33 | 9.00 | +2.67 |
| **Total /40** | **29.67** | **33.80** | **+4.13** |

**Pass rate (24/40 + claim_safety ≥5 + structural checks):** External **0/3**, ours **5/5**. External's structural failures: missing strategy_map_id, claim_guardrails, hook schema split, credibility_stack, methodology_receipt.

**Hook quality verdict on the operator's primary lens: statistical tie.** Top concept on each side scored 9 (External's Quit Jar = our c05 Hedgehog). Bottom concept on each side scored 6 (External's Tongue Timer = our c03 Owl). **External does not exceed ours at the pack level.**

### Buyer-fit (eval-buyer-fit rubric, AG1 hard-gate)

| Axis | External | Ours |
|---|---|---|
| Mental-model alignment | Strong prose craft, hits emotion in one line | Disciplined but more generic |
| Awareness × sophistication fit | **FAILS** — all 3 close at wrong rung | Solution-Aware × L3 held on all 5 |
| Tried-and-discounted respect | **Best-in-class** (Quit Jar names ferrous sulfate, gummies, liquid drops with sympathetic epitaphs) | More generic — opportunity to import |
| Voice consistency | Honors no constraints — no input contract for allowed/forbidden expressions | All 5 pass; zero forbidden_expressions, allowed_expressions deployed verbatim |
| Stage-4 Move delivery | Absent — methodology silent on Schwartz Stage-4 | 4/4 moves on all 5 concepts |
| Proof-type delivery | Implicit only | 4+3+6 triplet enforced |
| Funnel handoff | **FAILS** — closes wrong rung, can't hand off to live SL | 0-rung gap verified per concept |
| **AG1 hard-gate verdict** | **0/3 PASS** | **5/5 PASS** (3 soft flags) |

External's deepest gap: all three concepts close at the WRONG awareness rung (E1 Problem-Aware, E2 convenience-frame, E3 overshoots Product-Aware). External methodology has **no internal mechanism** to self-correct to a sophistication-stage rubric — gap is structural, not stylistic.

### Resource cost (estimated)

- External generation: ~102K tokens, ~263s wall (Sonnet sim)
- Ours generation: ~130K tokens, ~333s wall (Sonnet sim — real seeder would run Opus)

Both are within normal Phase-1 envelope. Cost is not a discriminator.

---

## Cherry-pick list (per CLAUDE.md §15 — cherry-pick > install)

Five specific imports recommended, in priority order. All land under `skills/video-concept-lab/references/general/external-creative-director/` as new reference nodes, with attribution to source files. None modify seeder spec, AG1/AG2, or vid-director.

| # | Asset | Source | Where it lands in our stack | Why |
|---|---|---|---|---|
| 1 | **Insight Mining tension framework** (cultural/category/human tensions + 6-check Insight Quality Test) | `creative-director/references/insight-mining.md` | New node `external-creative-director/insight-mining.md` referenced from `general/big-idea-architecture.md` (or equivalent) | Sharpens "enter the conversation already in their head" — directly improves mental-model alignment, which buyer-fit shows is our weakest axis |
| 2 | **Artifact-anchored hook pattern** (empirical, not a file — derive from Quit Jar / Receipt analysis) | Phase-2 empirical findings + `external-concepts.md` | New file `general/artifact-anchored-hooks.md` derived from finding, cross-linked from `hook-and-format-rules.md` and `creative-lanes-methodology.md` | Empirical: Quit Jar and Receipt scored 9 and 8 on thumbstop — our mechanism-reveal hooks (c03 owl = 6) consistently underperform artifact-anchored hooks. Hook quality is the operator's primary scoring lens. |
| 3 | **Pollard 7-level idea taxonomy** | `creative-director/references/idea-taxonomy.md` + `tag-schema.md` | New node `external-creative-director/idea-taxonomy.md` referenced from seeder spec via REFERENCE_GRAPH.json as an OPTIONAL pre-ideation discipline check | Forces an idea-level distinction (business / brand / tagline / advertising / campaign / non-advertising / execution) before method selection. Catches concepts that drift to wrong rung — exactly the failure mode external itself fell into. |
| 4 | **Legendary Pattern Map (P01-P18)** + selected non-stub cards | `creative-director/references/legendary-patterns.md` + cards filtered for confidence | New node `external-creative-director/legendary-patterns.md` with a curated subset (drop the 246/571 stub cards — they are noise) | Provides a saturation-cap discipline ("if 50+ canonical cases exist for this mechanic, you are not being original"). Useful for `pack_audit` flow as a Stage-3+ sophistication check. |
| 5 | **Sympathetic tried-and-discounted prose craft** (one-line buyer-recognition language) | Pattern from `external-concepts.md` Quit Jar ("She didn't quit iron. She quit being punished for taking it.") | Add a "Tried-and-discounted prose patterns" section to `general/buyer-language-conventions.md` (or equivalent), with 3-5 examples extracted from Phase-2 external output | External's prose craft on this axis is best-in-class. Buyer-fit eval named it as our weakest comparative axis. Low-effort port. |

### What we are NOT porting (and why)

- **Creative Constitution / recursive Phase-4 loop** — conflicts with our linear vid-director pipeline (off-limits)
- **8-12 → top-3 concept count contract** — conflicts with our N=5 / N=10 lock (downstream HTML + diversity map dependency)
- **571-card library wholesale** — 43% stubs, signal-to-noise too low; only curated non-stub cards from P01-P18 are worth pulling
- **External scoring rubric** — overlaps with V2V matrix; ours is paid-DR-tuned, theirs is brand-craft-tuned. Keeping ours
- **Storytelling frameworks catalog (Pixar / Freytag / Monroe / Sparkline / Hero's Journey)** — operator's DR briefs don't run on these arcs; would be additive theory without operational lift
- **HumanKind sub-score** — Leo Burnett brand-resonance metric; not buyer-fit-aligned for paid-DR
- **IKRA Constitution / CAT panel / Disney Strategy** — Cannes-craft methodology, no fit with our awareness/sophistication routing
- **External SKILL.md as a peer skill** — would create two ideation surfaces, ambiguity at vid-director Phase 1 dispatch

---

## Conflicts (things external assumes that contradict our contracts)

1. **No JSON brief contract.** External cannot ingest our `concept-brief.json` schema. Wrapping it as a peer ideation surface would require an adapter layer — not worth it for the upside.
2. **Recursive PASS 0-5 loop.** External's evaluate+refine phase recurses until threshold. Our pipeline is linear with explicit HITL gates. Cannot coexist as a drop-in.
3. **No claim-safety mechanism.** External methodology is silent on FDA/Meta substantiation. For a DR brief like Takekine (supplement claims), external concepts would auto-fail downstream review.
4. **No awareness/sophistication routing.** External cannot route Solution-Aware × Stage-3 brief differently from Unaware × Stage-1. Confirmed in Phase 2 where external closed at wrong awareness rung in 3/3 concepts.
5. **No methodology_receipt protocol.** Our routing_verdict block requires a receipt. External has no equivalent. Under normal dispatch this forces `routing_verdict: fail` and `concepts_evaluated: []`.

None of these are deal-breakers for cherry-picking the 5 assets above — they are deal-breakers for full integration.

---

## Migration plan

Not applicable. Q2 = DECIDE-AFTER-ANALYSIS, verdict = IMPROVE, no migration warranted. The 5 cherry-pick items are reference-tree additions, not migrations. Recommended sequence if approved:

1. Create folder `skills/video-concept-lab/references/general/external-creative-director/` with `_SOURCE.md` attribution file pointing to original repo + commit hash + license (MIT).
2. Copy + lightly edit the 4 file-based assets (#1, #3, #4 + #5-as-section-addition) — preserve external's prose where useful, strip Cannes/brand-platform language where it conflicts with DR framing.
3. Derive the artifact-anchored hook pattern file (#2) from Phase-2 empirical findings + Quit Jar/Receipt analysis.
4. Register the 5 new nodes in `REFERENCE_GRAPH.json` as OPTIONAL loadout extensions — none become required for existing loadouts.
5. Cross-link from `hook-and-format-rules.md`, `creative-lanes-methodology.md`, and `pack_audit` loadout.
6. Re-run the 260520 routing audit against the updated graph to confirm no implicit-routing violations.
7. Validate with one re-run of the Takekine brief — does ours-with-imports score higher on `first_frame_thumbstop` and mental-model alignment?

Estimated effort: 1 working session. No code changes. No agent changes. No HITL gate changes.

---

## Open questions

1. **Should the cherry-pick #5 prose craft port be a separate file or an addition to an existing buyer-language file?** Defaulted to "addition" in the plan above; flag if a new file is preferred.
2. **Does the operator want the curated P01-P18 cards as a flat library, or filtered by Schwartz stage / proof type for routability?** Recommend filtered, but raw flat is faster to land.
3. **External MIT license attribution — `_SOURCE.md` file with commit hash is the default. Want anything stronger (e.g. inline citations in each ported file)?**
4. **Phase-2 was Sonnet simulation on both sides. Want a real Opus seeder re-run with the imports landed to confirm hook-quality lift?** Spend is ~$X (Opus tokens for one seeder cycle).
5. **`concept-brief.json` is not off-limits per Q4. Any appetite to add an optional `idea_taxonomy_level` field (Pollard) for future briefs, or strictly leave the schema untouched and route taxonomy as a seeder-side check?**

---

## Verdict restated

**IMPROVE.** Cherry-pick 5 specific assets — Insight Mining tension framework, artifact-anchored hook pattern (empirical), Pollard 7-level idea taxonomy, curated P01-P18 pattern library, sympathetic tried-and-discounted prose craft — as optional reference nodes under `references/general/external-creative-director/`. Keep our seeder, vid-director phase pipeline, AG1/AG2 gates, and `concept-brief.json` schema intact. Do not install external as a dependency. Do not run external as a peer ideation surface.

Hook quality — the operator's stated scoring lens — is a statistical tie at the pack level, with one specific portable insight (artifact-anchored hooks beat mechanism-reveal hooks). That insight alone justifies the audit. The other 4 cherry-picks are net-add for buyer-fit mental-model alignment, which Phase-2 named as our weakest comparative axis.
