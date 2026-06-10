# My-Pipeline Stage Map — current machine, A→Z, as practiced (260610)

Synthesized from Phase 1 crawls (A1/A2/B/C/D/E). Format: STAGE | inputs | gate | outputs | owner.
"(undocumented)" = stage exists in practice but no skill/contract owns it — lives in Jerel's head or ad-hoc prompts.

| # | Stage | Inputs | Gate | Outputs | Owner |
|---|-------|--------|------|---------|-------|
| 0 | Client onboarding | interview answers (Path B 21-q) or scrape targets (Path A) | HITL interview | Jake-structure client folder + campaign indexes | skills/client-onboarding (template itself fails 4/7 ICM rules; 3 clients on 3 template generations) |
| 1 | Brand/business profiling | onboarding artifacts, transcripts, competitor data | HITL approval of scaffolded files | _brand/{offer,buyer-profile,funnel,voice...}.md | skills/business-profile + brand-scaffolder |
| 2 | Market/buyer research | subreddits, scrapes, ad-library, interviews, research-vault | **NONE — no completeness bar, no minimum research definition** | research dossiers, _swipe/research, 00_inputs | global /research + reddit + scrapecreators + ad-library-scraper (+ judgment, undocumented) |
| 3 | Source-of-truth synthesis | research + onboarding artifacts (4-5 parallel agents) | Phase 4 HITL (4 strategic decisions); anti-fabrication = "mark NOT AVAILABLE", no quantified minimum | source-of-truth.md (26 sections) + angles/ | skills/source-of-truth |
| 4 | Avatar / micro-personas | _brand files + pasted LLM research (manual paste step) | HITL Gate 1 persona selection + Gate 2 approval; thin research back-filled, not blocked | buyer-profile.md MICRO-PERSONA MAP or _brand/avatars/*.md | skills/avatar-research (chains buyer-language-researcher + persona-builder). Failure mode: unsourced persona quotes laundered downstream (neezanizam avatar-1:11) |
| 5 | Campaign/workspace scaffold | campaign brief | none | campaign folder + state file — **3 competing schemas** (pipeline-state.json / state.yaml / plan-state) | /campaign:new, /video:new-concept, ad-concept-engine conductor |
| 6 | Angle generation | DEFAULT: 6 typed free-text slots, **no research files required**; HARDENED (opt-in, undocumented in SKILL.md): buyer-profile.md required | DEFAULT: soft logged gates; HARDENED: scored JSON gate (5 dims, threshold 4, fail-closed regen) — the only machine-hard gate in the pipeline; citation audit ADVISORY only | run dir: 12 step files, top-3 angles + headlines + image prompts | big-angle-spotter (symlink → ~/AI workflows; documented launch path dead) |
| 7 | Meta ad copy (headlines/primaries) | 7-item checklist (halt if missing) | input-halt only; angle-run's gated headlines DISCARDED, downstream regeneration gets operator eyeball only | halbert-copy.md → COPY tab | skills/headline-bank v2.1 (internal HEADLINE/COPY mapping contradiction) |
| 8 | Long-form copy (letters/pages) | 8 ordered _brand files (letters) / _brand or interview (pages) | letters: Phase 0/0.5/0.7 HITL + 5 mandatory reviewers + FAIL-stops-ship (strongest gate in repo); pages: defer to /copy:* + copy-editing ≥35/50 | clients/<slug>/copy/*.md | sales-letter-method, copywriting, copy-editing + copywriting-os |
| 9 | DCT assembly | _brand + micro-persona map + swipe-files/<industry> | 5 HITL gates (persona, angle, copy, creative, tracker) | dct.json + pipeline-state.json + sheet rows | skills/ad-concept-engine conductor (10-5-5 hardcodes neezanizam/eugene; copy→dct byte-faithful — verified strength) |
| 10 | Image prompts | approved angle + headlines (assumed, not enforced) | HITL prompt review before spend; **no claim/number gate — invented $214,300 shipped in img-03/04** | image_pool.images[].image_prompt in dct.json | ad-concept-engine static brief (SG/CPF hardcoded "for every client") + image-generation + gpt-image-2-director; 9-rule standard duplicated in 2 skills, diverged |
| 11 | Render | dct.json prompts — in practice hand-fed via --prompt because --from-tracker reads dead legacy shape | render "go" HITL + post-render dimension gate; sidecar provenance written (strength) | renders/*.png + sidecars | scripts/ad-images/render.py (Azure GPT-Image pool) |
| 12 | Creative approval | rendered images | HITL gallery review — caught a wrong-gender testimonial, missed fabricated numerals | approved image set | operator (undocumented rubric) |
| 13 | Sheet/tracking write | dct.json | scripts have HITL snapshot; live practice = manual gws writes, snapshot safety lost; SPEC says 5 rows/wave, live sheet got 1 wide row | COPY/CREATIVES tab rows | ad_concept_sheet_writer.py (legacy shape only) / tr_10_5_5_sheet_writer.py (thomson-hardcoded) / manual gws (practice) |
| 14 | Upload to Meta | sheet + creatives | PAUSED-only upload; operator enables in Ads Manager | paused ads in act_* | meta-ads-uploader (cites nonexistent MCP; token-var mismatch) / meta CLI manual |
| 15 | Measure | Meta insights | protected columns | metrics rows in client workbook | sheets-updater + Modal cron 9am SGT (neezanizam live; token expiry risk 6/15) |
| 16 | Feedback/iteration | dct-tracker + sheet metrics | fail-closed thresholds (min S$200/creative, 7d, 5k impressions) → INSUFFICIENT_DATA (strength) | NEW/BETTER/MORE routing — points at dead /ads:concepts | skills/feedback-router (requires nonexistent meta-ads MCP) |
| 17 | Session memory/handoff | session work | session-end protocol exists but DEAD (learnings stale 5 wks; handoffs in 5 scattered locations, gitignored single-copies) | SESSION-HANDOFF-*.md ad-hoc | (undocumented in practice) |

Sibling lane — paid VIDEO: vid-director (AG0/AG1/AG2) + video-concept-lab + video-hook-variants + eval-buyer-fit HARD gate at AG1/AG2/html-publish. Strongest gating architecture in the repo; statics lane has no equivalent of eval-buyer-fit.

## Key structural observations for gap analysis
1. Gates cluster at angle stage + money moments (render/upload); claims ENTER at ungated stages (persona authoring, copy drafting, image-prompt numerals, sheet write).
2. Research has no definition of done anywhere; richness varies ~50:1 across clients (takekine ~630K words VoC; others thin).
3. The strongest patterns exist but are OPT-IN or lane-specific: hardened angle gate (opt-in, undocumented), eval-buyer-fit (video lane only), sales-letter reviewer chain (letters only).
4. Automation owners drift → operators route around them manually → HITL safety nets silently lost (render, sheet).
5. State/index files lag folder truth across all 3 crawled clients; agents are told to trust indexes that omit live campaigns.
