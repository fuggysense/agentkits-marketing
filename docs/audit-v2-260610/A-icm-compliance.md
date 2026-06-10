# Dimension A — ICM Compliance Audit

Auditor: ICM-compliance (Dimension A). Date: 2026-06-10 (SGT).
Repo root: `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing`. All paths repo-relative unless `~`.
Method: read the validator (`~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh`) and ICM spec (`~/.claude/skills/icm/SKILL.md`) line-by-line this session; re-ran greps/file-listings to confirm every claim. FACT = re-read/re-ran this session. JUDGMENT = interpretation.

Jargon: **L0** = `CLAUDE.md` (identity). **L1** = root `CONTEXT.md` (room map). **L2** = per-room `CONTEXT.md` (the task contract). **L3** = `_brand/` factory (stable rules, read-often). **L4** = `campaigns/` per-run outputs. **ICM** = the repo's folder-layering convention. The validator (`validate-icm.sh`) is the only automated ICM check; it runs 7 rules.

---

## Headline

The ICM validator is a **structure-presence checker masquerading as a compliance gate.** It verifies files exist and counts lines. It does NOT check the two things ICM actually demands — that L2 contracts have the 3 mandated sections, and that factory (L3) never sources from product (L4). Result: it stamped "PASS / Minor Issues" on clients whose content was stale, whose contracts are malformed, and (neezanizam) whose factory layer launders an invented buyer quote onto the money path. Worse, the source-of-non-compliance — `clients/_template/` itself — fails 3 of the 7 rules, so every new client is stamped non-compliant at birth. And the validator's own verdict scale rewards *absence*: a flat folder with no CLAUDE.md scores higher (4/7 "PARTIAL") than a real, working client like eugene (3/7) — because you can't have broken pointers in files that don't exist.

---

## 1. What the 7 rules CHECK vs what ICM DEMANDS (validator blind spots)

The validator (validate-icm.sh:52–154) runs exactly: R1 CLAUDE.md ≤100 lines; R2 root CONTEXT.md exists; R3 `_brand/CONTEXT.md` exists; R4 no CONTEXT.md >100 lines; R5 four hardcoded phrases not in non-root CONTEXT.md; R6 relative-path refs in CLAUDE.md + root CONTEXT.md resolve; R7 if `_templates/concept-phases/` exists then `CONTEXT-md-pattern.md` exists. That's it. Against the SKILL.md spec, the gaps are large:

- **Blind spot 1 — the 3-section L2 contract is never checked.** SKILL.md:31–47 + checklist:222 demand "Every L2 CONTEXT.md has exactly three sections — Inputs, Process, Outputs — no more." `grep -niE 'inputs|process|outputs|section|three' validate-icm.sh` → 0 hits. FACT: even the canonical reference client takekine violates it — `clients/takekine/_brand/CONTEXT.md` has 5 sections (What lives here / Stage Contract / Files / Subfolders / Load order; headers at lines 3,7,16,34,45). `clients/eugene-chieng/_brand/brand-assets/testimonials/CONTEXT.md` has 9 sections. Both PASS the validator. The contract ICM calls load-bearing is unenforced and universally unmet.

- **Blind spot 2 — budgets are checked in LINES, ICM specifies TOKENS.** SKILL.md:24,57 set L2 = "200–500 tokens (~30–70 lines)". R4 caps at 100 lines (validate-icm.sh:88). A 100-line CONTEXT.md is ~700–1,000 tokens — ~2× over the L2 token budget the spec sets. The check is 40%+ looser than the spec it claims to enforce, and these files sit in the hottest part of prompt cache (loaded every dispatch).

- **Blind spot 3 — L3-never-references-L4 (one-way data flow) is never checked.** SKILL.md:53 "L3 never references L4 — data flows one direction only (prevents circular dependencies)." No rule inspects `_brand/` for `campaigns/`/`output/` references. See Finding A-04 for the live violation this misses.

- **Blind spot 4 — content truth / freshness is never checked.** The validator confirms a *pointer resolves to a file*, never that the file's *content is current*. This is why it passed eugene at "PARTIAL" while CLAUDE.md:76 says "`_brand/avatars/` is legacy/tooling only" and CLAUDE.md:185 says "4 micro-personas" — both contradicted by live practice (per B-clients discovery: avatars/ powers the live wave; only 2 active avatars). The validator cannot see stale truth.

- **Blind spot 5 — R6 produces false positives from a regex bug AND a path-resolution bug.** FACT: the regex `(\./|\.\.\/|_[a-z]|campaigns/)[...]` (validate-icm.sh:133) matches `00_inputs/input-manifest.json` by capturing from `_i` → tests for `_inputs/input-manifest.json`, which doesn't exist, so it reports "broken" — but the *real* file `clients/_template/00_inputs/input-manifest.json` EXISTS (verified by ls). Separately, refs like `02_ag1-options/concepts-draft.json` are *workspace-relative* (they exist inside concept workspaces, not at client root), but R6 only resolves relative to the anchor file's own dir, so it flags valid layered refs as broken. R6's "broken pointer" list is a mix of regex artifacts, layer-relative refs, and genuine rot — undifferentiated, so an operator can't trust it.

## 2. Cross-client compliance reality (validator JSONs + spot reads)

- FACT — Verdict scale rewards absence. Five "clients" score 4/7 "PARTIAL" — 1up-sales-ai, aura, stackworks, propwise-sg, fuggysmedia — and ALL FIVE have NO CLAUDE.md, NO root CONTEXT.md, NO `_brand/` dir (verified by ls). They pass R4/R5/R6/R7 *vacuously* (validate-icm.sh awards PASS when the file/dir is absent: R4 line 93, R6 line 121 `[[ -f ]] || continue`, R7 line 153). eugene-chieng — a LIVE campaign with a real letter, funnel page, and 10-5-5 ad wave — scores 3/7, *below* the empty skeletons. The score inverts reality. (See A-02.)
- FACT — L0 over 100 lines: eugene CLAUDE.md = 197 (matches the 197-line template skeleton), neezanizam = 114, `_template` = 197. R4 oversized CONTEXT.md: `_template/CONTEXT.md` = 127, eugene `CONTEXT.md` = 127, eugene testimonials CONTEXT.md = 101.
- FACT — R5 scans excluded dirs. validate-icm.sh:91,109 `find "$CLIENT_DIR" -name 'CONTEXT.md'` with NO `_archive/`/`_template.old/` exclusion. takekine's only R5 "fail" is `clients/takekine/_archive/2026-05-21/legacy-phases/01_research/CONTEXT.md` — a retired file in the audit's own exclusion list — and the matched phrase ("medical claims", line 33) is incidental prose, not a duplicated global rule. A false positive dropping takekine 7/7→6/7 on dead-folder noise. (See A-06.)
- FACT — Duplication detection is 4 hardcoded phrases (validate-icm.sh:101: `medical claims|manual approval|no unverified|never duplicate`). ICM SSOT (SKILL.md:61–65) demands "no file duplicates content (validate with grep -r)" — a general principle. R5 catches only literal copies of 4 strings and only outside root; any other duplicated rule block sails through.

## 3. The template stamps non-compliance into every client (R1, R3, R4, R6)

FACT (all re-verified this session against `clients/_template/`):
- **R1 FAIL:** CLAUDE.md = 197 lines (max 100). `wc -l` confirmed.
- **R3 FAIL:** `_brand/CONTEXT.md` absent (`ls` → No such file). `_brand/` has 18 files incl. `booking.json`+`tracking.json` that no real client carries (per cross-client table) — dead template features — but no CONTEXT.md, the one ICM-mandated file.
- **R4 FAIL:** root `CONTEXT.md` = 127 lines (max 100).
- **R6 FAIL:** mix of (a) regex-mangled false positives (`00_inputs/input-manifest.json` exists but is reported as `_inputs/...` broken) and (b) genuine layer-relative refs to `02_ag1-options/concepts-draft.json` / `01_strategy/creative-diversity-map.json` that exist only inside concept workspaces, not at client root.
- FACT — The template SHIPS 7 empty Jake stage folders (`00_inputs`…`06_measure`) at client root. Every new client inherits them. eugene carries all 7 *empty* (dead weight, per B-clients §1.2); takekine archived them; neezanizam never had them.
- JUDGMENT — Because client-onboarding's scaffolder copies `_template`, the 197-line CLAUDE.md, missing `_brand/CONTEXT.md`, 127-line root CONTEXT.md, and dead Jake stages reproduce in every new client. Non-compliance is a manufacturing defect, not client drift.

## 4. L3→L4 violations (factory referencing product)

FACT — `grep -rnE '/campaigns/|/output/' clients/*/_brand/` (non-archive) returns real hits, the worst in takekine:
- `clients/takekine/_brand/funnel-research/voc/product-claim-context.md` is an L3 factory file (takekine CLAUDE.md L3-VOC row declares `_brand/funnel-research/voc/` as "input to buyer-profile.md"). It sources its claims FROM L4 product outputs: lines 35,37,98,135,140–143,160–165,177–178 all cite `clients/takekine/campaigns/test_2/01_research/output/concept-input-packet-*.json` and `…/02_script/output/.../draft-winner-script.md`. ICM SKILL.md:53 forbids exactly this (L3→L4 = circular dependency). Most damaging: it is the *product-claim substantiation* file (the compliance-critical layer) grounding itself in per-run generated packets rather than raw research. (See A-04.)
- Lower-severity: `neezanizam/_brand/source-of-truth.md:36,939,1092` and `source-of-truth-draft.json:72` reference `campaigns/dct-*/dct-tracker.json` — but these are scope-boundary *pointers* ("execution artefacts live there, do not duplicate"), arguably the legitimate exception. JUDGMENT: takekine's is a true grounding-direction violation; neezanizam's are mostly ownership disclaimers.

## 5. Three clients on three template generations → no "template-first" discipline

FACT (structural diff re-run this session):
- `_template` (current) ships Jake stages 00–06 + 197-line CLAUDE.md.
- eugene-chieng = current vintage: all 7 Jake stages present and EMPTY.
- takekine = ICM-migrated: Jake stages archived 2026-05-21, CONTEXT.md in every room, `_config/refresh-claude-map.sh` drift-log tooling unique to it.
- neezanizam = oldest (Apr-6 onboarding): never had Jake stages; fully custom `_TEMPLATE/{_assets,_drafts,_inbox,angles,avatars,dcts,landing-pages}` campaign layout that exists in NO other client and NOT in `_template`.
- FACT — `schema_version` is frozen at "1.0" across all three clients and the template (B-clients §4) — the version stamp does NOT distinguish the generations; only folder shape does. There is no migration path and no version signal.
- FACT — Per-client innovations (takekine's drift-log + per-room CONTEXT.md; neezanizam's `_sheet-snapshots/` + `_TEMPLATE` campaign scaffold) were never back-ported to `_template`. Each client is a fork, not an instance.
- FACT — The template's own rule is unenforceable and already broken: `_template/CLAUDE.md:61` forbids "broad duplicated `00_inputs/` folders inside campaigns or concept workspaces" — yet all 6 takekine concept workspaces carry their own `00_inputs/` (verified by find). The validator cannot see it.

## 6. Spec/practice/validator terminology drift

- FACT — SKILL.md's generic structure (lines 154–172) names the L3 factory `_shared-knowledge/`; `find clients -type d -name _shared-knowledge` → ZERO. Every client uses `_brand/`. The validator hardcodes `_brand/` (R3, line 73). So the spec names one thing, practice does another, and the validator silently agrees with practice — meaning the published SKILL.md no longer describes the system it validates.
- FACT — ICM citation is fabricated-looking: SKILL.md:12 + frontmatter cite "Van Clief & McDermott, *In-Context Modeling for Agentic Software* (arXiv:2603.16021v2)". Orientation notes flag the actual referenced title differs ("Interpretable Context Methodology…"). A future arXiv id (2603 = March 2026) on a foundational citation; low-stakes but it undermines the doc's authority.

---

## Findings (12)

See JSON for structured list. Severity rationale: Critical reserved for the invented-quote-on-money-path that the validator is blind to. High for the systemic gates that let bad content through on the money path (template defect, vacuous-pass scale inversion, L2 contract unenforced, L3→L4 grounding). Medium for drift that misleads. Low for citation/regex hygiene.

## Open questions
1. Should `validate-icm.sh` add a 3-section L2 check + token-based budget + L3→L4 grep, or is a richer linter out of scope (the SKILL.md itself only ships the line-count version)?
2. Is the template's 197-line CLAUDE.md intended (the spec says ≤100) — i.e., is the template the spec's reference, or its biggest violator?
3. Who owns back-porting takekine's CONTEXT.md-everywhere + drift-log discipline into `_template` so new clients inherit compliance instead of debt?
4. neezanizam "mental burden off my shoulders": real-but-undocumented (from an uncaptured call) or invented at avatar time? If invented, it is live in the proof-wave `dct.json` now.
