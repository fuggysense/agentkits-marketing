# Dimension B — Context-Grounding Audit (can output be traced to research; can unsourced claims reach paid media)

Audit date 2026-06-10 (SGT). Repo root `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing`. All paths repo-relative. Read-only; only write is this report.
Method: re-read every cited line this session (FACT) or marked JUDGMENT for interpretation. Prior discovery (Phase 1 A1/B/C + stage map) was the map; I re-verified the load-bearing lines and re-ran the grounding greps myself.

Jargon: **VoC** = voice of customer (real buyer quotes). **DCT** = one Meta ad test batch (images+texts+headlines). **Grounding** = output traceable to a real research source. **Gate** = checkpoint that must pass before the next stage. **Fail-closed** = refuses to proceed on missing inputs. **Laundering** = an invented phrase enters as "buyer language" and propagates downstream as if real.

---

## Headline: the central question, answered

Can output be traced to research? **Unevenly — and the gap is structural, not accidental.** Two clean traces (Eugene avatars → raw transcripts) prove the standard is achievable. But (a) no skill defines a quantified "research complete" bar, (b) the two skills that originate angles+copy from scratch have the *weakest* grounding requirements, and (c) numbers and quotes enter the pipeline at stages with NO machine gate comparing them to a source. Result: two confirmed unsourced claims — one caught, one shipped into approved/rendered creatives.

---

## 1. Minimum-research bar per generation skill (re-verified)

| Skill | Required research? | Bar type | Verified at |
|---|---|---|---|
| **avatar-research** | buyer-profile.md / icp.md / offer.md "Required"; if neither buyer-profile nor rich icp → route to persona-builder (genuine redirect) | Fail-redirect on absence, BUT thin external research "offer to fill from buyer-profile.md" — back-filled from client's own prior file, never blocked. No quantified minimum. | SKILL.md:54-69, 405-408 (read) |
| **big-angle-spotter** (default) | NONE — 6 free-text slots typed/pasted; only nudge is "demographic *and* psychographic" | Soft / no file required. Hardened scored gate exists but `--hardened` flag is undocumented in SKILL.md (grep `hardened`=0) | SKILL.md:22-32, 146; grep (read) |
| **headline-bank** | 7-item checklist, "halt and request… No improvisation on inputs" | Fail-closed input-halt (hardest input gate of the copy skills) | SKILL.md:74-86 (read) |
| **ad-concept-engine** | _brand/{buyer-profile,offer,brand-voice,icp,story-bank}; if no micro-persona map → "offer to run /ads:avatars first, or proceed in Legacy mode" | Soft — Legacy-mode escape lets the DCT engine run without avatar research | SKILL.md:248-252 (read) |
| **source-of-truth** | spawns research first; "5-7 minimum questions" is interview count, NOT a research-completeness bar | Qualitative anti-fab rails ("mark NOT AVAILABLE", "NEVER hallucinate buyer quotes") | SKILL.md:94, 126, 168 (read) |
| **image-generation** | none (assumes upstream-approved angle+headlines) | HITL prompt-review gate before spend; no claim/number source-check | SKILL.md:143-151 (read) |

**FACT — the grounding spectrum is inverted against risk.** The two skills that mint angles AND copy from a blank input (big-angle-spotter default, copywriting one-off) are the two with the weakest grounding requirements; the fail-closed skills (headline-bank, source-of-truth rails) are mostly downstream packagers. The skills that refuse are not the skills that invent.

**FACT — no skill anywhere defines "research complete" quantitatively.** Greps for a minimum quote/source count across avatar-research, source-of-truth, big-angle-spotter returned only source-of-truth's "5-7 interview questions" (SKILL.md:94,126) — an intake count, not a research bar. A DCT can be built off a thin dossier with no rule firing.

---

## 2. The trace evidence — one strength, one failure (both re-verified)

**STRENGTH — Eugene avatars trace verbatim to real transcripts.** Re-read avatar-1-cash-anxious-upgrader.md:36-42: every psychological field carries a `[file:line]` anchor. I opened the cited raw transcript: Derek's "we have seen so many webinars… so I got the turn off" sits at `_brand/brand-assets/testimonials/transcripts/raw/v01-2nd-couple.txt:60`; Cheryl's "typical middle income Singaporean" at :42. Both real. This is the repo's best-evidenced artifact and proves the standard is reachable. (Not a finding — the benchmark.)

**FAILURE (Critical) — neezanizam avatar-1.md:11 unsourced quote laundered into live pipeline.** Re-read avatar-1.md:11: Primary Emotion = "I want this mental burden off my shoulders." Case-insensitive grep for "mental burden" across `_swipe/research/` (incl. raw reddit JSONs) and `source-of-truth.md`: **zero hits**. The phrase exists ONLY in the avatar file and its downstream generated children: dct.json, dct-tracker.json, two spotter `system_prompt.txt`+`inputs.json`, dashboard.html, and a sheet-snapshot. I confirmed it sits inside the LIVE proof wave's approved copy: `dct-10-5-5-proof-260603/dct.json:23` angle_rationale quotes it verbatim as the avatar's "buying emotion," and that DCT is at `phase_3_render` with angles `gate_status: approved` (pipeline-state.json:10,21). An invented VoC phrase was minted at avatar-generation, passed every gate as if it were buyer language, and is rendering. This is exactly the laundering the DATA RELIABILITY rule exists to stop.

---

## 3. The two number cases (re-verified) + every ungated entry point

**A01 "4,580 homeowners" — HAD a source; the catch was attribution (advisory-only).** Re-read: avatar-2…md:145,403 cites it to `~/AI workflows/research-vault/markets/sg-property-hdb-mop-sellers/fears.md` (Stacked Homes editorial, per C-trace). So the figure is third-party sourced — what it lacked was *Eugene* sourcing (putting a number in his mouth he never said publicly). The drafting agent self-flagged it in v1 (`wave-1-copy-260610.md:318` "Verify the 4,580 figure is citeable before launching… or replace with the softer version"), the operator's v2 softened it to "Thousands of Singapore homeowners" (dct.json:39), and a standing launch gate locks it (dct.json:262). The machine warning that fired — `_run.log:13` "citation audit (advisory): 2 passing angle(s) cite evidence not found verbatim in profile: ['A01','A03']" — is advisory, audits angle evidence not copy numerals, and did NOT block. **Caught by human discipline, not machinery.**

**$214,300 invented loan balance — SHIPPED in approved/rendered creatives (Critical).** Re-read dct.json:155-175: img-03 shows "Outstanding loan balance: $214,300" and img-04 a chart "ending at a printed figure $214,300 in calm charcoal." Repo-wide grep for 214,300/214300: only the prompt artifacts (`11/12_ad/image_prompt_rank3.md`) + dct.json + the two rendered `.meta.json` sidecars. **No research file anywhere.** Both passed the creative gate (all 10 KEEP) and rendered to PNG. Asymmetry that matters: img-03's `visual_style` carries an internal note "illustrative set dressing on an explicitly fictional generic statement" — img-04 presents the SAME number as a labeled chart figure with NO fiction marker. A viewer cannot tell it is invented. Same failure class as 4,580, one stage later, and unlike 4,580 this one was not caught.

**Every pipeline entry point where a number/claim enters WITHOUT a gate (re-verified against C-trace gate inventory + skill reads):**
1. **inputs.json authoring** — hand-condensation of the avatar file; no script/skill owns it, no fidelity check (C-trace Stage 0, §7.1). A drifted PERSONA poisons everything downstream silently.
2. **Copy drafting** — writer pulls any figure from research/avatar into ad text; only checks are the writer's own in-file checklist + operator eyeballs. No machine compares copy numerals to a source manifest. (This is where 4,580 entered.)
3. **Image-prompt numerals** — angle-run image-prompt step invents set-dressing numbers; no claim/number gate. (This is where $214,300 entered.)
4. **Sheet write** — manual gws bypass of the script that carried HITL snapshot safety; no pre-write snapshot/preview artifact (C-trace Stage 8).

---

## 4. Copy & image-prompt quality gates — paper vs practice (Eugene wave)

**FACT — the one machine-hard gate is real and worked.** The hardened angle gate is scored JSON (5 dims, threshold 4, set-min 5, fail-closed regen loop): loop 1 banked 2/10 → REVISE → loop 2 banked 6/10 → SET PASS (`_run.log:7-14`, `02_gate_resonance_loop2.json`). Gate evidence quotes the buyer profile directly. This is the strongest grounding enforcement in the pipeline.

**FACT — downstream headline regeneration is ungated.** The angle-run produced 20 gated curiosity headlines (passed `10_gate_four_check.md`). They were **all discarded**: I grepped the angle-run dir for the shipped short headlines "He Didn't Look Either" / "Your Flat Looks Fine" → zero hits; they were freshly generated at the copy stage by headline-bank v2.1 (`wave-1-copy-260610-v2.md:6`). headline-bank has NO HITL inside the skill (grep: only the `/copy:headline` wrapper note). So the headlines that will actually run never passed any scored or factual gate — the four-check certified headlines that got thrown away. Their only checks were the copy file's self-QA + operator eyeball (a markdown header line, `v2.md:5`).

**FACT — the creative gate missed fabricated numerals.** It caught a wrong-gender testimonial (img-01 regendered male to match the male v10 client — a real correction) but passed both $214,300 instances (all 10 KEEP). The gate catches *visible-to-a-human* errors; it has no source-of-truth to check numbers against.

---

## 5. Research completeness — no definition of done; ~100:1 spread

**FACT — research richness varies ~50-100:1 across clients with no floor.** I word-counted: takekine `_brand/funnel-research/` = **630,041 words** of VoC; neezanizam `_swipe/research/` dossiers = 12,230 words; takekine's own structured `_brand/*.md` = only 5,408 words (research-heavy/brand-thin — the inverse of eugene). Eugene's `00_inputs/product|market/` stubs are 14-88 words each (B-clients §1.2). No skill, stage, or contract states a minimum below which generation should refuse — MY-PIPELINE-STAGE-MAP row 2 ("Market/buyer research") gate column reads literally "NONE — no completeness bar." A thin-research client and a 630K-word client flow through identical generation skills with identical (absent) grounding floors.

---

## Severity rationale

- **Critical** = untraceable output can ship to paid media. Both confirmed: neezanizam invented quote in approved/rendering copy (B-01); $214,300 invented number rendered into approved creatives with no fiction marker on img-04 (B-02). The systemic enabler — no claim/number-to-source gate at copy/image stages (B-03) — is the mechanism behind both.
- **High** = grounding gap on the money path with real consequence: no quantified research-complete bar (B-04); big-angle-spotter default mode + undocumented `--hardened` (B-05); downstream headline regeneration ungated (B-06).
- **Medium** = the catch-was-luck pattern (advisory-only citation audit, B-07); avatar-research thin-research back-fill (B-08).
