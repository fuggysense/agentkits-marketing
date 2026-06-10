# Pipeline Trace — Eugene Chieng 10-5-5 DCT Wave (upgrader-ads)

Audit date: 2026-06-10. All paths relative to repo root `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/`.
Jargon key: **DCT** = one Meta ad test (here a "Flexible ad": Meta mixes up to 10 images x 5 texts x 5 headlines). **Angle** = the persuasive idea behind an ad. **Gate** = a checkpoint that must pass before the next stage runs.

## 1. What the wave is

- FACT: Two DCT workspaces exist under `clients/eugene-chieng/campaigns/upgrader-ads/dcts/`: `dct-001-cash-anxious` (PARKED — `dct-001-cash-anxious/pipeline-state.json:10-12`) and `dct-002-math-blind` (active, at phase_5_upload, blocked on launch gates — `dct-002-math-blind/pipeline-state.json:10-12`).
- FACT: The operator collapsed both into ONE shipped wave: DCT002 carries 4 avatar-2 angles from its own run plus A10 (avatar-1) promoted from dct-001's run (`dct-002-math-blind/pipeline-state.json:34`, `dct-001-cash-anxious/pipeline-state.json:34`). dct-001's own top-3 (school/P1 lane) were shelved — no funnel page exists for them (`dct-001-cash-anxious/pipeline-state.json:12`).
- FACT: Final assembled artifact: `dct-002-math-blind/dct.json` — 5 angles, 10 image prompts, 10 rendered PNGs with sidecars, 7 launch gates (`dct.json:258-266`), Drive + Canva links (`dct.json:280-291`).
- FACT: Nothing has been uploaded to Meta yet. `gate_4_preupload` is `pending` (`dct-002 pipeline-state.json:101-102, 110-116`).

## 2. Stage-by-stage handoff verification

### Stage 0 — Avatar research → inputs.json (PASS, verified)

Declared input: `_brand/avatars/avatar-2-math-blind-upgrader.md` + `_brand/buyer-profile.md` (persona "avatar-2", `dct-002 pipeline-state.json:16-25`).

Use-test (did the downstream file really come from the upstream?):
- FACT: `dcts/dct-002-math-blind/inputs.json:5` PERSONA carries the v10 master quote "To be honest, I also did not really go and look into it" — present verbatim in `_brand/avatars/avatar-2-math-blind-upgrader.md:269` with a timestamp citation `[VERBATIM — v10 [00:21], v10-square2.txt]`.
- FACT: The Derek quote ("The accrual interest from CPF ... out of my mind") in `inputs.json:5` matches `avatar-2-math-blind-upgrader.md:274` and exists in the raw transcript `_brand/brand-assets/testimonials/transcripts/raw/v01-2nd-couple.txt` (the "HDB after HDB" line is at transcript line 43, `[03:54]`).
- JUDGMENT: This is a real grounded chain — persona claims trace to actual client-testimonial transcripts on disk, not model memory.
- FACT: `inputs.json` for the angle run (`angle-run-260609/inputs.json`) is byte-identical to the DCT-level `inputs.json` except one added key `PRODUCT_IMAGE_REFS` (verified by JSON diff).
- JUDGMENT (gap): nothing owns inputs.json authoring. It is a hand-synthesized condensation of the avatar file; no script or gate checks that the condensation is faithful. A drifted PERSONA here would poison everything downstream and no gate would notice.

### Stage 1 — inputs.json → big-angle-spotter hardened run (PASS, verified, real gates)

Owner: `big-angle-spotter` (symlink `skills/big-angle-spotter -> /Users/jerel/AI workflows/big-angle-spotter`, verified). Runner per spec: `~/AI workflows/big-angle-spotter/scripts/run_pipeline.py` (`docs/methods/10-5-5/SPEC.md:119`).

- FACT: `angle-run-260609/_run.log:2` shows the hardened config: `mode=fresh, threshold>=4, need>=5 winners, max_loops=3`.
- FACT: Loop 1 banked only 2/10; gate returned REVISE with named regen targets; loop 2 banked 6/10 → SET PASS (`_run.log:7-14`).
- FACT: The scored gate is real machine-readable JSON: per-angle 1-5 scores on 5 dimensions (voc_mirror, core_pain_hit, awareness_match, distinct, not_saturated), verdict, weakest dimension, evidence quote, fix-if-fail, set_verdict PASS, banked_ids [A01,A02,A03,A06,A07,A09] (`angle-run-260609/02_gate_resonance_loop2.json`).
- FACT: Gate evidence fields quote the buyer profile directly — e.g. A01 cites "Will tell people 'we're fine, the flat is paid down'... — buyer profile §2 Day-to-Day Struggles"; A02 cites "v10 [00:21], v10-square2.txt... 'the master line for this avatar'". The gate demonstrably consumed the persona input.
- FACT: The run has a **citation audit, but advisory only**: `_run.log:13` — "citation audit (advisory): 2 passing angle(s) cite evidence not found verbatim in profile: ['A01', 'A03']". It warned and did not block. A01 still shipped.
- FACT: dct-001's parallel run passed loop 1 with exactly 5/5 banked (`dct-001 .../_run.log:7-8`); its gate entry for A10 cites the v01 transcript line "why not take a smaller place..." at `v01-2nd-couple.txt:79` — the A10 angle that later shipped in DCT002 is transcript-grounded (`dct-001 .../02_gate_resonance_loop1.json`, A10 entry).
- Downstream gates in the run: `05_gate_top_angle.md` (YES + Schwartz reasoning), `06_gate_novelty.md` (YES vs EXISTING_ANGLES list), `10_gate_four_check.md` (ordered/factual/persona-fit/respect — all YES). These are prose verdicts, not scored JSON.

### Stage 2 — Angles → headlines/copy (PARTIAL: angles used, run's headline stage discarded)

- FACT: The shipped angle names/IDs in `dct.json` (A01 "The Paid-Down Illusion", A02 "To Be Honest, I Didn't Look", A06, A07, A10) match the banked angle IDs/titles in `01_angles.json` of the two runs (verified by listing both).
- FACT (discarded handoff): the angle-run's own headline stage (`08_headlines.md`, `09_ranked_headlines.md`, `10b_top_3.json`) produced 20 LONG curiosity headlines ("'To be honest, I didn't really go and look into it.' She owns a flat too. She found out she was nearly $200k under."). NONE of the 5 shipped short headlines ("He Didn't Look Either", "Your Flat Looks Fine", etc.) appear anywhere in the angle-run files (grep: zero hits).
- FACT: Shipped headlines + copy were generated fresh at the copy stage by `headline-bank v2.1` (`wave-1-copy-260610-v2.md:6`), each with a 5-candidate audit trail (`v2.md:24-30, 80-86`).
- JUDGMENT: Consequence — the angle-run's "four check" factual gate (`10_gate_four_check.md`) certified headlines that were thrown away. The headlines that will actually run never passed through any scored or factual gate; their only checks were the copy file's self-QA checklist and the operator's eyeball sign-off.
- FACT: Two copy versions exist. v1 (`wave-1-copy-260610.md`, mtime 00:50) is labelled "freestyle"; v2 (`wave-1-copy-260610-v2.md`, mtime 13:24) is the "Curiosity-Led Structured Rebuild" that "Replaces" v1 (`v2.md:7`) and records operator sign-off: "Signed off: 260610 — all 5 angles approved by Jerel. A02 as-is. A01 hook swap... A10 em-dashes cleaned" (`v2.md:5`).

### Stage 3 — Signed-off copy → dct.json (PASS, byte-faithful)

- FACT: A02 primary_text in `dct.json:18` is verbatim identical to `wave-1-copy-260610-v2.md:38-52` (every sentence matched, including "He was sitting on close to a negative $200,000"). A01 primary_text (`dct.json:39`) matches `v2.md:94-106` including the softened "Thousands of Singapore homeowners discovered this at the point of sale." Headline drafts arrays match (e.g. `dct.json:47-53` = `v2.md:82-86`).
- FACT: Assembly was manual — "dct.json assembled by hand (proof-wave DCT010 shape)" (`dct-002 pipeline-state.json:42`), because the automated emitter still writes the legacy tracker shape (declared at `dct-001 pipeline-state.json:48` blocker G1).
- FACT: A "cold-context reviewer pass" was applied at assembly: img-05 claim conflation fixed, img-03 fictional printed CPF row reworked to handwritten annotation, img-07 moved lanes, img-01/09 text aligned to copy (`dct-002 pipeline-state.json:47`). This is a fresh-agent review, recorded only as a note — no artifact of the review itself exists in the workspace.

### Stage 4 — Angle-run image prompts → dct.json image_pool (PASS with deliberate patching)

- FACT: 3 of 10 image prompts are declared "patched reuse" of the angle-run's `12_image_prompt_rank{1,2,3}.md`; 7 are "new 260610" (`dct.json` provenance fields, e.g. lines 132, 145, 158).
- FACT (verified patch): `angle-run-260609/12_image_prompt_rank1.md` is the same kitchen-table scene as `dct.json` img-01 but with a WOMAN ("Singaporean Chinese woman aged 46–50... coral home tee") and a consult CTA ("A free 1-on-1 read of your own numbers. We'll even tell you to wait."). dct.json img-01 (`dct.json:134`) regendered to a man and repointed the CTA to the letter ("The full story is in the letter.") — exactly matching its declared provenance "regendered male to match signed-off copy; CTA strip repointed to letter" (`dct.json:132`).
- FACT: The regendering is a CORRECTION, not a fabrication: the v10 client is male — "me and my wife, we were really shocked to see this figure" (`_brand/brand-assets/testimonials/transcripts/raw/v10-square2.txt:5`). The angle-run had drifted the testimonial's gender to "she"; the copy stage caught and fixed it.
- JUDGMENT: No gate checks image-prompt content against sources. The patch was caught by human/cold-reviewer attention, not by machinery.

### Stage 5 — dct.json prompts → rendered images (PASS, verified 10/10 exact)

- FACT: Every rendered PNG has a `.meta.json` sidecar written by `scripts/ad-images/render.py` (engine gpt-image-2, style dr-clean-static, size 1024x1024). I programmatically compared all 10 sidecar `prompt` fields against the matching `dct.json image_prompt` strings: **10/10 exact matches**.
- FACT: Sidecars show `source: inline-prompt` — prompts were fed via `--prompt`, NOT via `--from-tracker`, confirming the declared bypass of the legacy tracker bridge (`dct-002 pipeline-state.json:58`).
- FACT: Operator render gate honored: "Operator gave explicit 'go render' 2026-06-10" (`pipeline-state.json:58`); render gate is also launch_gate 6 (`dct.json:264`).

### Stage 6-7 — Allocate + creative approval (declared, thin evidence)

- FACT: Allocation wrote `status: rendered` + file paths into dct.json image_pool in place; "No separate _assets.json emitted" (`pipeline-state.json:68`).
- FACT: Creative gate: "Operator approved 2026-06-10. Visual QA: all 10 KEEP... img-05 claim-safety PASS" plus two cosmetic nits on record (`pipeline-state.json:80`). No standalone approval artifact (no approval JSON) — the pipeline-state note IS the record.

### Stage 8 — Sheet write (MANUAL, script bypassed, externally unverified)

- FACT: Declared owner was `scripts/ad_concept_sheet_writer.py` reading dct.json (`dct-001 pipeline-state.json:76`), but the actual write was "direct gws write from dct.json (G4 bypassed: sheet uses wide one-row-per-wave layout; ad_concept_sheet_writer.py row-per-creative model not applicable)" (`dct-002 pipeline-state.json:87`).
- FACT: `scripts/ad_concept_sheet_writer.py:314-330` hard-requires `dct-tracker.json` with a `creatives[]` array — it cannot read this wave's `dct.json` (shape is `angles[]` + `image_pool`). It even has 10-5-5 awareness ("5 angles × 2 variations → 5 rows", line 498) but a row-per-angle model, while the actual sheet got ONE wide row per wave (`COPY!A2` 12 cells, `CREATIVES!A2` 14 cells — `dct.json:281-289`).
- FACT: This also contradicts the method spec, which locked "one row per angle (5 rows per wave)... we do NOT widen the COPY tab" (`docs/methods/10-5-5/SPEC.md:80-84`).
- FACT: Spreadsheet ID in `dct.json:283` (`1SDLzn4ce...`) matches the client's registered sheet (`clients/eugene-chieng/_brand/metrics-config.json:220-221`).
- JUDGMENT: The sheet rows themselves are UNVERIFIED from disk — no pre-write snapshot, no preview artifact, no script log exists (the bypassed script's HITL snapshot pattern was the thing that would have produced one). The only evidence is self-reported notes in pipeline-state.json and dct.json.

### Stage 9 — Meta upload (not run)

- FACT: `phase_5_upload` blocked; ads will be created PAUSED; owner `meta-ads-uploader (dct.json -> bundle.json adapter)` (`pipeline-state.json:97-105`). Launch gates 1-5 outstanding (`dct.json:259-263`), including Meta Flex live-limit verification (SPEC O4, `SPEC.md:134`).

## 3. The A01 stat — full reconstruction

The claim: A01 "The Paid-Down Illusion" originally said **"4,580 Singapore homeowners said something similar in 2020. They were not fine."** (`wave-1-copy-260610.md:99`, also line 117 "4,580 Singapore homeowners discovered this at the point of sale in 2020").

Where the number came from (it is NOT sourceless — the task brief's framing is half right):
- FACT: `_brand/avatars/avatar-2-math-blind-upgrader.md:145, 403` cites it to the research vault: `~/AI workflows/research-vault/markets/sg-property-hdb-mop-sellers/fears.md`.
- FACT: That vault file (line 18) reads "The CPF Board has confirmed 4,580 homeowners experienced this in 2020" and line 24 carries a primary citation: Stacked Homes editorial, URL `https://stackedhomes.com/why-4580-homeowners-have-negative-cash-sales-despite-high-property-prices/`.
- JUDGMENT: So the figure has a documented third-party source. What it lacked was *client* sourcing — Eugene never said it publicly, so an ad signed by Eugene asserting it puts a number in his mouth he may not stand behind.

How it was caught and softened:
- FACT: The v1 copy file's own self-QA flagged it: "**Verify the 4,580 figure is citeable before launching** — it is from the vault, not Eugene's public content... or replace with the softer version: 'thousands of Singapore homeowners...'" (`wave-1-copy-260610.md:318`).
- FACT: v2 (the operator-directed rebuild) executed the softening: "replaced with 'thousands of Singapore homeowners'... Per task brief and data-reliability rules" (`wave-1-copy-260610-v2.md:315`, change log at line 344). The shipped dct.json carries "Thousands of Singapore homeowners" (`dct.json:39`) and a standing launch gate: "A01 stat stays 'thousands...' unless Eugene confirms the 4,580 (2020) source as publicly citeable" (`dct.json:262`).
- FACT: The machinery did fire one warning earlier — the hardened run's advisory citation audit flagged A01's gate evidence as "not found verbatim in profile" (`_run.log:13`) — but it is advisory, checks angle evidence (not copy numerals), and the 4,580 figure was not yet in any artifact at that point.

Where an unsourced number enters without tripping any gate:
- JUDGMENT: The injection point is the **copy-assembly stage** (between the angle gate and dct.json). The writer pulls any figure from research/avatar files into ad text; the only checks are the writer's own checklist inside the same file and operator eyeballs. No machine gate compares copy numerals to a source manifest. The 4,580 episode was caught only because the drafting agent happened to flag itself and the operator's v2 brief enforced data-reliability rules.
- FACT (live second instance): **$214,300** appears as the printed loan balance in shipped creatives img-03 and img-04 (`dct.json:160, 173`). It originates in the angle-run image-prompt step (`angle-run-260609/12_image_prompt_rank3.md`, `11_ad_prompt_rank3.md`) and exists in NO research file (repo-wide grep: only the prompt artifacts). dct.json's own annotation calls it "illustrative set dressing on an explicitly fictional generic statement" for img-03 (`dct.json:159`), but img-04 presents it as a chart figure with no in-image fiction marker. It passed the creative gate (all 10 KEEP). A viewer cannot tell it is invented. Same failure class as the 4,580, one stage later, and this one shipped.

## 4. Gate inventory — explicit vs nothing

| Handoff | Gate | Type |
|---|---|---|
| avatar files → inputs.json | NONE (hand condensation) | — |
| inputs.json → angles | gate_resonance scored JSON, threshold 4/5, set-min 5, regen loop, fail-closed (`02_gate_resonance_loop*.json`, `_run.log:2`) | machine, hard |
| angles → top angle / novelty / headline four-check | prose YES/NO verdicts (`05/06/10_gate_*.md`) | machine-written, soft; certified later-discarded headlines |
| angle-run citation audit | advisory only, warned on A01/A03 and did not block (`_run.log:13`) | machine, soft |
| angles → shipped copy/headlines | operator sign-off recorded as a header line (`v2.md:5`) + self-QA checklist in-file; NO scored gate, NO claim-source check | human, undocumented format |
| copy → dct.json | none (manual assembly + unrecorded cold-context reviewer pass, `pipeline-state.json:47`) | human |
| image prompts → render | operator "go render" gate (`pipeline-state.json:58`, `dct.json:264`) | human, hard (credit spend) |
| renders → pool/approval | gate_3_creative operator approval, note-only (`pipeline-state.json:80`) | human, no artifact |
| dct.json → sheet | NONE — script HITL bypassed, direct manual write | — |
| sheet → Meta upload | gate_4_preupload + 7 launch gates in dct.json + ads-created-PAUSED rule | listed, pending |

JUDGMENT: gates are dense at the angle stage and at money-spending moments (render, upload), and thinnest exactly where claims/numbers get written — copy, image prompts, sheet.

## 5. Tooling vs data-shape mismatches (declared, real, worked around by hand)

- FACT: `render.py --from-tracker` parses `creatives[]/ads[]` → `variations[]` → `image_prompt` (`scripts/ad-images/render.py:73-97`). dct.json's `image_pool.images[]` is incompatible. Worked around with `--prompt` per image (sidecars confirm `inline-prompt`).
- FACT: `ad_concept_sheet_writer.py` requires `dct-tracker.json` `creatives[]` (`scripts/ad_concept_sheet_writer.py:314-323`). Worked around with direct gws writes.
- FACT: Both gaps are honestly self-declared in launch_gates item 7 (`dct.json:265`) and pipeline-state blockers G1/G4 (`dct-001 pipeline-state.json:48,79`).
- FACT (doc drift): `docs/methods/10-5-5/SPEC.md:140-145` still shows ALL phases unchecked ("Phase 1 — in progress") while `docs/methods/10-5-5/migration-log.md:7-51` marks Phases 1-6 DONE (2026-06-03). The spec's tracker schema (`SPEC.md:46-78`, locked_copy/variations) and 5-rows-per-wave sheet model (`SPEC.md:80-84`) no longer describe what this wave actually shipped (primary_text/compression_text + image_pool; one wide row per wave). The spec says "single source of truth" (`SPEC.md:7`) and currently isn't.

## 6. Timeline (file mtimes, 2026-06-09 → 06-10 SGT)

- 23:09-23:10 (06-09): dct-002 inputs + run scaffold.
- 23:10-23:41: dct-002 hardened angle run, 12 steps, fresh subagent per step, loop-2 SET PASS; total wall ~31 min (`_run.log`).
- 23:45-00:04: dct-001 angle run (avatar-1), loop-1 PASS.
- 00:50: `wave-1-copy-260610.md` (v1, freestyle, contains 4,580).
- 13:24: `wave-1-copy-260610-v2.md` (structured rebuild, 4,580 → "thousands", signed off).
- 13:58-14:08: 10 renders + sidecars (img-01/06 last after retry — matches "2 transient Azure stream failures" note).
- 14:25 / 14:31: both pipeline-states finalized; 14:45 dct.json final write.
- 15:22: Canva verification screenshots (Connect-API uploads found under Projects tab — logged as a correction at `skills/ad-concept-engine/corrections.md:34-36`).
- JUDGMENT: ~15 hours brief-to-approved-creatives including overnight gap; the morning gap (00:50→13:24) brackets the human review window.

## 7. Manual / undocumented stages (no script or skill owns them)

1. **inputs.json authoring** (avatar file → COMPANY/OFFER/PERSONA condensation) — no owner, no fidelity check.
2. **Operator wave-collapse decision** (merge dct-001 A10 into DCT002, shelve school lane) — recorded only in pipeline-state notes; no decision artifact.
3. **Copy drafting v1 → v2 rebuild** — owner declared as "headline-bank v2.1" skill but the run is unlogged; sign-off is a markdown header line, not a gate file.
4. **dct.json assembly + cold-context reviewer pass** — by hand; review has no artifact.
5. **Image-prompt patching** (regender, CTA repoint, 7 new prompts) — by hand inside dct.json.
6. **Sheet write** — direct gws calls; the one stage whose script-side HITL/snapshot safety was designed in (`corrections.md:26`) and then bypassed.
7. **AVATARS tab narrative patch** ("DRAFT->APPROVED, swapped DCT anchors corrected" — `pipeline-state.json:90`) — entirely manual, no artifact.

## 8. Open questions

1. Did the COPY!A2 / CREATIVES!A2 rows actually land with the signed-off text? No local snapshot exists; needs a one-off `gws sheets +read` against `1SDLzn4ce...` to confirm (unverified here).
2. Is the wide one-row-per-wave sheet layout the new intended 10-5-5 shape, or a one-off divergence from SPEC.md §3's 5-rows-per-wave model? Whichever wins, spec or sheet must change.
3. img-04's $214,300 chart figure: will the operator add a fiction marker or accept an invented numeral in a trust-positioned brand's ad? (Client CLAUDE.md: "Every claim needs a number, mechanism, or named case study" — an invented number arguably violates its own constraint.)
4. Who is supposed to repoint `ad_concept_sheet_writer.py` and `render.py --from-tracker` to the dct.json shape (launch_gates item 7), and is that planned before wave 2 (where hand-feeding 10 prompts won't scale)?
5. The advisory citation audit flagged A01/A03 evidence as non-verbatim — was that ever resolved, or just absorbed?
6. The `Euegene Chieng Letter Draft Spine.pages` file and `campaigns/feedback/` were not examined (out of trace scope); letter URL swap (launch gate 1) depends on the mp1-letter page going live — current letter state not traced here.
