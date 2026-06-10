# Dimension C — Prompt Quality & Client Leakage Audit

Audit date: 2026-06-10 (SGT). Repo root: `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing`. All paths repo-relative unless `~`-prefixed.
Method: every FACT below was re-read from the cited lines THIS session (not inherited from Phase-1 notes). JUDGMENT = my interpretation of verified facts.
Jargon key: **leakage** = one client's specifics (Singapore CPF/HDB rules, NeezaNizam/Eugene names) baked into a skill meant for ALL clients, so a US/other client silently inherits SG rules. **Skeleton skill** = a half-built skill still flagged "pending calibration." **Few-shot** = a worked example inside a prompt that shows the model what "good" looks like. **HITL** = human approval checkpoint.

---

## 1. CLIENT LEAKAGE in generic skills

**The single worst leak — and the operator already believes it's fixed.**
`skills/ad-concept-engine/references/high-converting-static-brief.md` is loaded "MANDATORY on every static batch" (`ad-concept-engine/SKILL.md:691`) and its own header says it applies "for every client" (`high-converting-static-brief.md:4`). Yet inside the "non-negotiable rules (apply to every single image variant)":
- Rule 3 (`:13`): "Singapore = Chinese / Malay / Indian / Eurasian. Match the target avatar's ethnicity to the primary variant."
- Rule 7 (`:17`): casting bar = "*Straits Times* feature… *Kinfolk* editorial"; rule 4 (`:14`) names SG photographers (Geraldine Kang, Sean Lee).
- Rule 8 (`:18`): "If the image shows a document (CPF, HFE, etc.), it must look like the real Singaporean document."

The trap: `ad-concept-engine/corrections.md:24` explicitly records "Applies globally, not neezanizam-only." So the operator's own memory asserts this file is client-agnostic while the SG ethnicity + CPF/HFE document rules are still hardcoded as universal. A US or UK client run that loads this file inherits "Singapore = Chinese/Malay/Indian/Eurasian" as a hard rule. **Critical** because it can steer paid-media creative for a non-SG client toward wrong-market casting and SG-document props.

**Second leak — the avatar research engine's web-search prompt.**
`skills/avatar-research/SKILL.md:309` — the GENERIC per-persona Grok prompt template hardcodes "Search r/singaporefi, r/askSingapore, HardwareZone EDMW for '{product_category} ad', 'agent marketing', 'property seminar', 'this is why I don't trust agents.'" Line 299 hardcodes "posts making fun of property ads, agent marketing, or upgrade promises." Verified: these sit in the reusable template, not a client example. A non-SG, non-property client gets steered to Singapore property forums for its buyer-voice research.

**Third leak — the Meta-copy generator's generic rules.**
`skills/headline-bank/SKILL.md:138` — the generic core-prompt read-cue example is "see the number on your flat" (an HDB-flat-specific line a naive agent copies for any client). `:176` — Hard Rule 2 bakes a specific client avatar's tonal contract into the universal banned-words rule: "for Avatar 2 life-transition: no 'investment,' 'dream home,' 'build wealth,' 'maximize returns'." That is one client's persona constraint masquerading as a global rule.

**Fourth leak — image-generation summary still says "Singaporean."**
`skills/image-generation/SKILL.md:133` instructs "real-not-AI **Singaporean**/locale casting" in the generic ad-quality bar, even though its own reference file (`gut-wrenching-ad-format.md:9`) correctly genericized this to "for SG clients: Singaporean." The SKILL body re-leaks what the reference fixed.

**Fifth leak — SG cultural rules in the standard conductor loadout.**
`ad-concept-engine/SKILL.md:465` (static batch) and `:515` (video batch) both list `references/sg-cultural-guidelines.md` in the "Skills loaded" set unconditionally. That file (`sg-cultural-guidelines.md:5`) opens "Singapore is multiracial (Chinese ~75%, Malay ~15%…)" — Singapore-specific guidance pulled into the generic conductor's default load for every client.

**Sixth leak — feedback-router defaults in S$.**
`skills/feedback-router/references/routing-criteria.md` pre-routing gates default to "min S$200/creative, S$600/batch" (Singapore dollars) and the worked example output (`feedback-router/SKILL.md:149-169`) is fully NeezaNizam-flavoured. The file does allow a per-client `feedback_router_thresholds` override, so this is default-leakage (a wrong default), not hard-coding — **Low**.

NOT leakage (verified and excluded): `references/sophistication-creative-map.md` was genuinely multi-product-ified per corrections 260418:22 — it now carries 6 product-type examples per Schwartz level (ecom/SaaS/service/info/agency/property), property is one option among many. The "Eugene" hit in the skeleton skills is Eugene Schwartz the author, not the client.

---

## 2. CONFLICTING OWNERSHIP

**headline-bank internal contradiction — verified, quoted.**
The core prompt's output format (`SKILL.md:158-168`) defines:
> `## COPY A — PRIMARY (~150 words) / HEADLINE 1` then `## COPY B — COMPRESSION (~50 words) / HEADLINE 2`

The output-FILE template (`SKILL.md:206-216`) defines:
> `## COPY 1 (~50 words) / HEADLINE 1` then `## COPY 2 (~150 words) / HEADLINE 2`

So HEADLINE 1 attaches to the ~150-word PRIMARY in the prompt but to the ~50-word copy in the file template — the headline↔copy↔length mapping is inverted between the two templates in the same skill. The sheet-mapping table at `:220-224` keys off "HEADLINE 1" without resolving which copy that is. Whichever the sheet writer assumes, ~half the runs mislabel which headline locks to which copy length. **High** — it sits on the path that writes the Meta COPY tab, and the Eugene wave already shows the angle-run's gated headlines were discarded and regenerated (`C-pipeline-trace.md` Stage 2), so the lock fidelity matters.

**The 9-rule static standard — duplicated and diverged, verified.**
Same 9-rule "scroll-stop / physically ill" standard exists in two files with two owners:
- `ad-concept-engine/references/high-converting-static-brief.md` (rule 3 = "Singapore = Chinese/Malay/Indian/Eurasian", universal).
- `image-generation/references/gut-wrenching-ad-format.md` (rule 3 = "match the target market's ethnicity/locale (for SG clients: Singaporean…)", genericized).

They have already diverged on the exact field (locale handling) that matters for non-SG clients. Two sources of truth for the image-quality bar means a fix to one never propagates. **Medium.**

---

## 3. SKELETON SKILLS (5 copywriting-foundation skills)

Verified all five: `persuasive-premise`, `problem-promise`, `unique-mechanism-problem`, `unique-mechanism-solution`, `usp-generator`. Each:
- `version: "0.1.0-skeleton"`, `status: skeleton-pending-calibration` (frontmatter, all five).
- Cites `references/canonical-sources.md (TODO)` as its Source authority (e.g. `persuasive-premise/SKILL.md:45`) — `ls skills/<each>/references/` returns "No such file or directory" for all five. The cited authority file does not exist; the references/ dir does not exist.
- Uses LEGACY flat paths for required inputs: `clients/<project>/offer.md` + `clients/<project>/research/buyer-language-dossier.md` (`persuasive-premise/SKILL.md:65-66`), while repo canon (CLAUDE.md AGENT ENTRY CONTRACT, sales-letter-method, avatar-research) is `_brand/offer.md`. A compliant agent looks in the wrong place.
- "REQUIRED if exists" (`persuasive-premise/SKILL.md:67`) is an oxymoron — operationalizes as optional; there is NO halt/refuse language, so any of these emits a premise/mechanism/USP from a thin or absent dossier.
- "Worked Examples — TODO" + "Calibration Set — TODO" (`persuasive-premise/SKILL.md:104-112`) — by the skill's own admission, zero few-shot, so the disagreeability/uniqueness tests have no anchor.
- Claims downstream wiring: "Cross-reference in headline-bank, ad-concept-engine, sales-letter-method… as required input" (`:118`) — headline-bank's actual input checklist (`SKILL.md:74-86`) does NOT include any premise/mechanism file. Aspirational, not wired.

JUDGMENT: these five are husks that present as production skills (no "do not use" guard). They are routable (`/copy:premise` trigger exists in frontmatter). If invoked, they generate foundational positioning beliefs from thin input with no gate and a dead source citation. **Medium** — they actively mislead an agent that routes to them, but they are off the main DCT money-path (which uses big-angle-spotter).

---

## 4. VAGUE vs OPERATIONAL — the 3 load-bearing generation prompts

**(a) big-angle-spotter STEP_1 — the angle engine (most load-bearing on the statics path).**
`~/AI workflows/big-angle-spotter/scripts/run_pipeline.py:122-128`. Verbatim opener: "You are a god-tier marketer… A hybrid between Steve Jobs, Gary Halbert, Eugene Schwartz, and David Ogilvy… 10 high converting, gut wrenching, curiosity driving, emotion provoking reasons." Structural ask is real (cause-effect form, numbered 1-10, one conversion-logic sentence each) but there is **zero few-shot** — no model angle anchors "good." The only inputs are 3 free-text slots ({OFFER}/{COMPANY}/{PERSONA}). JUDGMENT: with a rich persona this works; with a one-line persona it produces adjective-driven vibes. This is the thinnest-grounded generator on the money path AND its source lives outside the repo (symlink to `~/AI workflows`). **Medium** (quality risk, not safety).

**(b) headline-bank core prompt — operational.**
`SKILL.md:136-168`: explicit 5-beat structure (curiosity → pain → problem → hope → loop-CTA), banned-word list, CTA-as-read-cue rule, length targets, exact output format. The most operational of the three. Its flaw is the §2 length↔number inversion, not vagueness.

**(c) ad-concept-engine Phase 1 — operational contract, but a loader not a generator.**
`SKILL.md:325-364`: precise about what to load (micro-persona row, sophistication map, swipe patterns), how to score (rubric), how to present (grouped table), and the HITL gate. But it "NO LONGER generates angles directly" (`:120`) — it delegates to big-angle-spotter. So the operational rigor is in the orchestration; the actual creative generation inherits (a)'s no-few-shot weakness.

Synthesis: the two skills that ORIGINATE angles/copy from scratch (big-angle-spotter STEP_1, the 5 skeletons) are the two with the weakest examples; the downstream packagers (headline-bank, ad-concept-engine) are operational. Few-shot is missing exactly where creative quality is set.

---

## 5. DEAD REFERENCES in prompts

**Dead slash-commands cited in live skills.** Verified `.claude/commands/ads/` contains ONLY: feedback, headlines, scrape-advertiser, scrape-library, source-of-truth (`ls`). No `concepts.md`, no `avatars.md`; `find .claude/commands -iname "*concept*" -o -iname "*avatar*"` returns nothing. Yet these are cited as runnable next-steps:
- `/ads:concepts` — `feedback-router/SKILL.md:59,60,125,130,163,188,189,206` (it is the ACTION of all three feedback routes), `source-of-truth/SKILL.md:256`, `avatar-research/SKILL.md:449,481`, `headline-bank/SKILL.md:56`.
- `/ads:avatars` — `avatar-research/SKILL.md:50,449,481`, `ad-concept-engine/SKILL.md:250`, `source-of-truth/SKILL.md:255`.
- `/test:ab-setup` — `source-of-truth/SKILL.md:257`.

Internal inconsistency inside one skill: `ad-concept-engine/SKILL.md:68` correctly says "there is no `/ads:concepts` to memorise" while `:250` still tells the agent to "offer to run `/ads:avatars` first." **High** for feedback-router specifically: its entire output is a NEW/BETTER/MORE recommendation that resolves to `/ads:concepts <slug>` — a command the operator cannot run, so the iteration loop dead-ends. Replacement (intent-routing) exists only for the DCT conductor (routing-overrides 260609); avatar/feedback entries have no documented replacement.

**meta-ads MCP required but the MCP does not exist.**
`feedback-router/SKILL.md:28-30` frontmatter declares `mcp_integrations.required: meta-ads`; description (`:7`) repeats "Requires: meta-ads." But `.claude/rules/mcp-integrations.md` states plainly: "Meta / Facebook Ads = CLI, not MCP… there is no meta-ads MCP server." A compliant agent that honors the required-dependency halts on a server that cannot exist. **High** — it blocks the one fail-closed feedback skill from running at all.

**meta-ads-uploader env-var mismatch.**
`skills/meta-ads-uploader/scripts/meta_api.py:149,152` reads `META_ADS_ACCESS_TOKEN`; the documented repo/global standard (global CLAUDE.md, mcp-integrations.md) is `META_ACCESS_TOKEN` (the never-expiring "Jerel-cli" system token). An operator who set up the documented var hits "META_ADS_ACCESS_TOKEN not set" at upload. **High** — breaks the upload step on the live-money path unless the operator knows the undocumented var name.

---

## 6. What is genuinely healthy (for balance)

- headline-bank input gate is fail-closed: 7-item checklist, "halt and request… No improvisation on inputs" (`SKILL.md:74-86`).
- ad-concept-engine `corrections.md` is the repo's healthiest (12+ dated entries) and `learnings.md` opens with an honest "N=1 WARNING… priors, not laws."
- The Eugene wave's copy→dct.json handoff was byte-faithful and a cold-reviewer caught a wrong-gender testimonial (per C-pipeline-trace) — the human gates work where they fire.
- `gut-wrenching-ad-format.md:3` correctly self-labels "Client-agnostic — always reconcile against the active client's brand kill-list" — the right pattern, which the ACE twin file fails to follow.
