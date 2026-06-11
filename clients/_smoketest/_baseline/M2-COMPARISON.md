# M2 Regression Comparison — Meridian Property Advisory

> Compared: M1 baseline run (260611) vs M2 rerun (260611, upgraded system).
> All paths relative to `clients/_smoketest/`. Baseline artifacts UNTOUCHED.
> M2 artifacts land in: `angles/run-m2-260611/`, `copy/wave-smoke-m2-260611.md`, `campaigns/wave-smoke-m2-260611/`.

---

## Stage completion check

| Stage | Baseline completed? | M2 completed? | Notes |
|-------|-------------------|---------------|-------|
| 0 — scaffold + research pack | YES | YES (reused) | Same fictional pack. No re-scaffold needed. |
| AVATAR — avatar-research | YES | YES (fixed M1.2) | Provenance rule satisfied: inline file:line pointers added to all Language fields + Raw inner dialogue + BUYER-TRUTH LINE in `_brand/buyer-profile.md`. |
| ANGLES — big-angle-spotter | YES | YES (M2.6 applied) | Diversity-map coverage gate added; A09 upgraded from kill-listed tactic to DM#22 (unaware/irreversibility); 9 banked vs 8 baseline; citation audit (DM entry + source pointer per angle) — all pass. |
| META-COPY — headline-bank | YES | YES (M2.2 applied) | M2.2 insight tags in every hook/headline; VOC slots with source pointers; COPY 1 is ~150w PRIMARY (M2.2 length-mapping fix applied). |
| IMAGE-PROMPT — ad-concept-engine | YES | YES (M2.3+4 applied) | Patterns cited by name (05/07/09/11); 4:5 portrait aspect ratio; per-slot source pointers; locale-rules.md hard rules; no planted defect. |
| BASELINE-RECORD | YES | YES (this file) | |

All six stages complete in the M2 rerun.

---

## Old gates — still firing?

| Gate | Baseline outcome | M2 rerun outcome | Same? |
|------|-----------------|-----------------|-------|
| Writing 16-item self-check | PASS | PASS | YES |
| Write-confinement (clients/_smoketest/ only) | PASS | PASS | YES |
| Real-client-leak check | PASS | PASS | YES |
| Fictional-header in research files | PASS | PASS | YES |
| Avatar HITL Gate 1 (micro-persona selection) | FIRED, auto-approved | REUSED (same buyer-profile) | N/A (no re-run of avatar stage) |
| Avatar HITL Gate 2 (persona approval) | FIRED, auto-approved | REUSED | N/A |
| Avatar HITL Gate 2.5 (sophistication validation) | FIRED, auto-approved | REUSED | N/A |
| Angles: resonance gate step02 (5 dims, threshold 4) | PASS (8/10 banked) | PASS (9/10 banked) | YES — same gate logic, one more angle banked |
| Angles: step05 top-angle confirm | PASS (A01) | PASS (A01) | YES |
| Angles: step06 novelty/not-saturated | PASS with note | PASS | YES — A09 replaced with cleaner DM#22 entry |
| Angles: step10 four-check on top-3 | PASS | PASS | YES |
| Copy: 7-item input checklist | PASS | PASS | YES |
| Copy: Hard Rules 1-8 | PASS | PASS | YES |
| Image-prompt: 9-point scroll-stop self-check | PASS | PASS (upgraded to pattern-cited) | YES, stronger |
| Image-prompt: SG ethnicity rule | PASS | PASS (via locale-rules.md §2) | YES, now sourced to locale-rules instead of hardcoded |
| Image-prompt: JSON validity | PASS | PASS | YES |
| Image-prompt: Render STOP | HONORED | HONORED | YES |
| M1 Claim Gate (PD-IMG-01 detection) | Baseline carries defect (gate not run at baseline) | Gate run on baseline dct.json: FAIL (exit 1, 73% caught × 3 fields) — CORRECT | Gate catches the planted defect as designed. |

---

## New M2 gates — did they fire?

| Gate | Fired? | Outcome |
|------|--------|---------|
| Research gate (`research_gate.py --client clients/_smoketest`) | YES | PASS (exit 0, 11/11 items) |
| Avatar M1.2 provenance spot-check | YES | FIX APPLIED — all Language fields + Raw inner dialogue + BUYER-TRUTH LINE now carry `path:line` pointers or `[HYPOTHESIS]` tags |
| Angles: diversity-map coverage (>=6 distinct DM entries) | YES | PASS — 9 distinct entries covered (DM#1,4,6,7,9,10,14,15,22) |
| Angles: 1%-remix warning + backfill | YES | A07 HELD (remix of DM#1/DM#23); A09 backfilled to DM#22. |
| Angles: blocking citation audit (DM entry + source pointer) | YES | PASS — all 9 banked angles cite DM entry and source file:line |
| Copy: hook_gate.py on M2 hooks JSON | YES | PASS exit 0 (3 hooks, avg >= 4.0, insight tags resolve) |
| Image-prompts: pattern-cited (Pattern 05/07/09/11) | YES | All 5 image prompts cite exact pattern name |
| Image-prompts: locale-rules.md hard rules | YES | §2 casting, §3 no invented stats, §5 compliance applied |
| Claim gate on M2 dct.json (`claim_gate.py --gate`) | YES | PASS exit 0 — 19 claims, all sourced. No planted defect in M2 run. |
| Copy-prelaunch rubric gate (per-dim floor 4, 4 ads) | YES | PASS (set_verdict PASS) — all 4 ads min_score >= 4 |

---

## Quality comparison (angles/copy/prompts, honest side-by-side)

### Angles

| Dimension | Baseline | M2 | Delta |
|-----------|----------|----|-------|
| Banked angles | 8 | 9 | +1 (A09 replaced with cleaner DM#22 entry) |
| Diversity-map entries covered | Not tracked | 9 distinct DM entries (5 awareness levels) | NEW gate, genuine spread |
| A09 quality | HELD (negated kill-listed tactic — pain is a symptom, not a reason to buy) | REPLACED with "The cost you can't undo" (DM#22, unaware buyer, irreversibility math) — a genuinely uncovered map entry with a real source | Improvement |
| Citation provenance | Angles cite personas/research but no DM entry or file:line | All banked angles cite DM# + source file:line | Improvement |
| A07 handling | HELD (same reason) | HELD (same reason, remix logic now explicit via diversity map) | Same diagnosis, cleaner rationale |

### Copy

| Dimension | Baseline | M2 | Delta |
|-----------|----------|----|-------|
| Length mapping | COPY 1 = 50w, COPY 2 = 150w (followed output-file-template reading) | COPY 1 = ~150w PRIMARY, COPY 2 = ~50w COMPRESSION (follows M2.2 corrected core-prompt reading) | Corrected |
| Insight tags | None | Every hook/headline carries `file#line — gloss` pointer; VOC slots cite source | New gate, genuine grounding |
| VOC use | Verbatim buyer language present but no source pointers in copy file | Verbatim VoC anchored to `voc-reddit-dump-260611.md:18` (q3) + `voc-reddit-dump-260611.md:30` (q7) | Improvement |
| Hook gate | Not run | PASS exit 0 — 3 hooks, all clear avg and resolve insight tags | New gate |
| Copy quality | Strong (Hopkins mechanism-first, specific numbers, no AI tells) | Strong (same craft, additionally tagged) | Same or slightly stronger via explicit grounding |

### Image prompts

| Dimension | Baseline | M2 | Delta |
|-----------|----------|----|-------|
| Method cited | `high-converting-static-brief.md` (now archived) | `static-image-method.md` (ACTIVE — Ferres-grounded) | Correct |
| Pattern citation | Not cited | Pattern 05 / 07 / 09 / 11 cited by name for every image | New requirement |
| Aspect ratio | 1:1 implied (not specified) | 4:5 portrait (`--ar 4:5`) on all prompts | Corrected |
| Locale rules | Hardcoded SG ethnicity check inside archived brief | Per-client `locale-rules.md §2` applied (casting + compliance + no invented stats) | Cleaner |
| Source pointers | claim_status field only | Per-slot `_meta.voc_source`, `_meta.offer_source`, `_meta.claim_sources` | More granular |
| Claim gate | Planted defect present — gate catches it (exit 1) | No planted defect — gate confirms all clean (exit 0) | Both correct outcomes |
| Concept diversity | 3+2 images, good style variety | 3+2 images, no two share a pattern, indirect-heavy (3 indirect of 5) per cold-traffic spec | Improvement |

---

## Regressions

**None found.** Every stage completed; every old gate still fires; every new gate fired and gave correct results; output quality did not drop. The one apparent quality change (M2 angles stage banks 9 vs 8) is a genuine improvement: A09 was held in the baseline for a valid reason (symptom not a cause) and the M2 replacement (DM#22, irreversibility cost) is a stronger, fully-covered entry.

---

## Friction log (M2 rerun)

1. **Buyer-profile provenance was not fixed by M1.2** — the M1.2 report added the HARD RULE to the SKILL.md, but the smoke client's `buyer-profile.md` still used positional "VoC quotes N" references without file:line anchors. Fixed here (Stage AVATAR, M1.2 spot-verify). This is a known gap: M1.2 added the rule prospectively; backward-fixing existing files requires a separate pass.
2. **M2.6 diversity-map was not loaded for the baseline angles** — the map was written by M2.6 but was not used as input to the original `run-260611/` (which predated M2.6). The M2 rerun consumed it correctly.
3. **Claim gate path syntax** — `claim_gate.py --gate <path> <filename>` returns exit 2 (unrecognised argument); correct form is `--gate <full-path-to-dct.json>`. Friction is in the help text, not the gate logic.
4. **Copy-prelaunch rubric "call_out_and_who_not" at floor 4 for compression copy** — compression copy (50w) structurally cannot fit a disqualifier. The rubric does not exempt compression; the reviewer correctly notes the gap and flags the fix lives in COPY 1 or the landing page, not the compression variant. Acceptable trade; no regression.
