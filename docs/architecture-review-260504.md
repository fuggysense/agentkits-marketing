# Architecture Review: Re-Architect Copy / Ads / Image-Gen Stack
**Date:** 2026-05-04 | **Operator:** Jerel | **Reviewer Role:** Claude Code systems architect + AI model-routing engineer + direct-response copy workflow designer + brutally honest red-team
**Status:** Phase 5.1 review-only. Do not implement until HITL approval.
**Inputs:** existing project (Marketing/) + Eduba `vault-toolkit` (Jake_fulltoolkit) + zero-fluff handoff prompt + Part 1-5 marketing wisdom paste.

---

## 1. One-Sentence Verdict

**Lightly refactor — don't re-architect.** The Copywriting OS shipped 260424 (`/copy` router + gates + 9 reviewers + client template) is the right primitive. Apply Jake/Eduba's ICM L0-L4 layer model to your folder structure, extend the OS pattern to ad images + video, finish the rules-index pattern you already started. Most of the bloat is fixable structurally — you don't need a new framework.

The ReAct + ToT-lite + judges + context-packs hypothesis from your handoff is **already 80% built** in the existing system. You're closer to done than you think. The risk isn't underbuilding — it's continuing to add primitives instead of reorganizing the ones you have.

---

## 2. Context Summary

| Aspect | Finding |
|--------|---------|
| Files reviewed | ~140 marketing artifacts (75 project skills, 21 project agents × 3 files each, 45 global skills, 1 global agent), `.claude/rules/`, `.claude/references/copywriting-os/`, `clients/_template/copy-system/`, NeezaNizam client, Jake_fulltoolkit |
| Project skills | 75 — flat directory, mostly `SKILL.md + corrections.md + learnings.md + references/` |
| Project agents | 21 — flat `.md` files, each with `-attribution.md` + `-learnings.md` companions (63 files for 21 agents) |
| Global skills | 45 |
| Global agents | 1 (`buyer-language-researcher.md`) |
| Slash commands | ~150 across 30+ namespaces (`/copy:*`, `/ads:*`, `/cro:*`, etc.) |
| Context layers | `voice/<person>/` (V.O.I.C.E. — 5 files per person, shared across clients) + `clients/<slug>/{context-profile.json, icp.md, offer.md, brand-voice.md, learnings.md, buyer-profile.md, channels.json}` |
| Client placement | LOCAL to `Marketing/clients/<slug>/` |
| Model routing | `scripts/research-llm.sh` → kilo (MiniMax/Nemotron) / gemini-cli / ollama for cheap research; Anthropic Claude as primary controller for everything else |
| Main pipeline | 6-stage creative: scrape (`ad-library-scraper`) → research (`source-of-truth`, `avatar-research`) → angles (`big-angle-spotter`) → concepts (`ad-concept-engine`) → render (`image-generation`, `video-director`, `seedance-*`) → upload (`meta-ads-uploader`) → feedback (`feedback-router`) |
| Copywriting OS | `/copy` router + 5 sub-commands + 3 pre-write gates + 4 anti-hallucination reviewers + 5 persuasion-craft reviewers + `clients/_template/copy-system/` scaffold |
| Compounding loops | per-skill `corrections.md` + `learnings.md`, per-client `learnings.md`, weekly `/ops:weekly` knowledge-hygiene scan |
| Auto-load weight (estimate) | parent CLAUDE.md (~250 lines) + 3 routing files (~430 lines combined) + nested CLAUDE.md (~115 lines) + 1 global rule file (~280 lines) ≈ **~12-18K tokens loaded every session** before any work begins |

### Obvious gaps (named here, ranked in §4)
1. CLAUDE.md auto-loads `details/{commands,routing-table,skills-catalog}.md` despite the rules-index pattern explicitly forbidding this.
2. `clients/<slug>/` mixes L3 reference (brand-voice, ICP, offer) with L4 working artifacts (sales letters, campaigns, sheet snapshots) in the same flat directory.
3. No L1/L2 stage contracts — `SKILL.md` does triple duty (orientation + routing + execution).
4. 4 retired `seedance-*` skills + 1 retired global `video-director` + 1 retired `directors-cut` + 1 retired `filmmaking` skill — 7 skills marked RETIRED in their own frontmatter still present.
5. `image-generation` skill has no parallel to the Copywriting OS gates/reviewers — no quality system for ad images.
6. No `creative-os/` umbrella to share gates between `/ads:concepts`, `image-generation`, and `video-director`.

---

## 3. Current Architecture Map

```
Controller:        Claude Code main agent (no explicit Coordinator agent)
Orchestrators:     Slash commands (/copy router, /ads:concepts orchestrator)
Specialist agents: 21 project + 1 global, mostly invoked one-at-a-time
Skills:            Frontmatter-triggered (description + triggers in YAML)
Judges/Reviewers:  9 inside Copywriting OS (4 anti-hallucination + 5 persuasion-craft)
                   ZERO for ad images, ad videos, or non-copy work
Context packs:     Per-client folder, NOT layer-separated (L3 mixed with L4)
Model routing:     Cheap-research-only (kilo/gemini/ollama via shell script)
Memory loops:      corrections.md (real-time), learnings.md (confirmed patterns),
                   weekly knowledge-hygiene + monthly CLAUDE.md improver
External grounding:Buyer-language-researcher (global agent), scrapecreators,
                   ad-library-scraper, deep-research, reddit, transcribe
```

### How work passes between components today
```
User intent
  → Slash command OR skill auto-trigger
  → CLAUDE.md context gate (load context-profile.json + voice/ + brand-voice.md)
  → Skill loads framework + reads corrections.md
  → Agent invoked for execution OR main agent executes inline
  → Output written to clients/<slug>/<wherever it fits>
  → Reviewers run if Copywriting OS path; otherwise none
  → Learnings appended at session end (manual via /ops:claude-md)
```

### What's missing
- **Coordinator agent.** The handoff prompt's hypothesis assumes one. You have an implicit one (the main agent + slash commands), which works but isn't explicit.
- **Stage contracts (L2 in ICM).** Each stage of the 6-stage creative pipeline should have a 200-500-token CONTEXT.md declaring inputs, outputs, success criteria. Currently this lives buried in SKILL.md files.
- **Parallel reviewer stack for non-copy.** Image-gen and video-prompt outputs ship without quality gates. A bad image prompt slips through to render → spend.
- **DPO-lite preference bank.** You have `learnings.md` (qualitative). You don't have a structured preference bank ranking past outputs. Optional, not blocking.

---

## 4. Brutal Diagnosis

Ranked by severity. Format per handoff: Problem / Severity / Evidence / Why it matters / Fix.

### Problem 1: Auto-loaded routing tables defeat the rules-index pattern you already designed
- **Severity:** HIGH
- **Evidence:** Your own CLAUDE.md says "Do NOT preload `details/*.md`" and "scan `_index.md` → fetch the specific detail file." Yet the conversation's loaded system reminder shows `details/commands.md`, `details/routing-table.md`, `details/skills-catalog.md`, `mcp-integrations.md`, AND `_index.md` ALL loaded simultaneously. Plus parent CLAUDE.md, nested CLAUDE.md, routing-overrides.md, skill-activation.md. ~12-18K tokens before any work.
- **Why it matters:** This is the bloat. Long-context attention degrades (Liu 2024). Important constraints in the middle get less weight. You're literally fighting your own rule.
- **Fix:** Audit what loads via `claudeMd` system prompt section. Move `details/*` to genuine on-demand. Trim parent CLAUDE.md to a 50-60-line map (Jake-style L0). Test with `/context` after change. **Target: cut auto-load to ≤4K tokens.**

### Problem 2: clients/<slug>/ blends L3 reference and L4 working artifacts
- **Severity:** HIGH
- **Evidence:** NeezaNizam folder mixes `context-profile.json` (L3, identity), `brand-voice.md` (L3, voice), `icp.md` (L3, audience), `offer.md` (L3, offer), with `campaigns/dct-260417/` (L4, working), `sales-letters/260421-v1.md` (L4, output), `sheet-snapshots/` (L4, frozen state), `angles/wave-1.md` (L4, in-flight wave), all at the same depth. Per Jake's constraint 03: "L3 material needs to be internalized as constraints. L4 material needs to be processed as input. Mixing them forces the model to figure out which is which on its own. Sometimes it treats your reference material as content to transform."
- **Why it matters:** Every `/copy:*` or `/ads:*` invocation has to disambiguate at runtime. This is invisible quality leakage — you don't see it in any one output, but cumulatively it's the difference between A and B work.
- **Fix:** Reorg to `clients/<slug>/_brand/` (L3, stable) + `clients/<slug>/_swipe/` (L3, research/dossiers) + `clients/<slug>/campaigns/<c>/` (L4, working). Add 1-line headers to each L3 file: `<!-- LAYER: L3 — REFERENCE. Use as constraint, do not transform. -->`. Same for L4 with `SOURCE`. Ugly but effective per Jake.

### Problem 3: 7 retired skills still present
- **Severity:** MEDIUM
- **Evidence:** `seedance-loop`, `seedance-motion`, `seedance-prompt`, `seedance-effects` all explicitly marked `RETIRED — absorbed into seedance-director` in their own SKILL.md frontmatter. Same for `filmmaking`, `directors-cut`, global `video-director`. Two `video-director` skills coexist (project + global retired). Routing tables reflect them as if live.
- **Why it matters:** Discovery cost for every new task that touches video. Trust erosion when a user picks the retired one and gets a redirect message. Every retired skill loaded into routing tables = wasted tokens.
- **Fix:** Delete retired skills. Replace with stub `SKILL.md` containing only: `---\nname: seedance-loop\ndescription: REDIRECT — use seedance-director instead\n---`. Or full delete + remove from routing-table.md + skills-catalog.md.

### Problem 4: Image-gen and video-prompt outputs have no quality gates
- **Severity:** MEDIUM
- **Evidence:** `image-generation` SKILL.md has no `reviewers/` folder. `video-director` (project) has none. The Copywriting OS reviewers (`one-person-enforcement`, `proof-density-audit`, etc.) are copy-only by design. Bad image prompts slip from `big-angle-spotter` step 12 → render → ad spend.
- **Why it matters:** You spend ~$0.07/image and minutes/video. A bad prompt batch wastes both. Worse, image hallucinations (props, faces, text overlays gone wrong) ship to upload-pause queue and require human catch.
- **Fix:** Build `creative-os/` parallel to `copywriting-os/`. Pre-render gates: brand-fit, format-spec compliance (3:4 vs 1:1 vs 9:16), ICP-resonance. Post-render reviewers: visual-claim audit (no fake testimonials in image), brand-voice-fidelity (Lexus tier vs mass-market), scroll-stop test (does the first 200ms read?), mechanism diversity across the 3 variants per Ad Set.

### Problem 5: Agent files carry 3× the file count for no compounding gain
- **Severity:** MEDIUM
- **Evidence:** 21 agents × 3 files (`X.md`, `X-attribution.md`, `X-learnings.md`) = 63 agent files. Skills use folders (`skills/X/{SKILL.md, attribution.md, learnings.md, references/}`). Inconsistent.
- **Why it matters:** Discovery friction. Folder-per-thing is cleaner. Also, agents/ is FLAT — no grouping by domain.
- **Fix:** Either (a) migrate agents to folder pattern (`agents/<name>/{AGENT.md, attribution.md, learnings.md}`) for consistency, OR (b) group flat files by domain prefix (`copy-copywriter.md`, `copy-brand-voice-guardian.md`, `ads-attraction-specialist.md`). (a) is more invasive but final.

### Problem 6: No explicit Coordinator agent
- **Severity:** LOW (your slash-command-as-orchestrator pattern works)
- **Evidence:** Handoff prompt assumes a Coordinator. You have implicit coordination via `/copy`, `/ads:concepts`, `/copy:sales-letter`. They orchestrate the gates → drafter → reviewers chain. Works fine.
- **Why it matters:** Only matters if you start running multiple agents in parallel for the same letter. You don't.
- **Fix:** Don't build one. Acknowledge the pattern in `.claude/rules/orchestration-protocol.md` and move on.

### Problem 7: Generic-AI-copy risk is real but partly defended
- **Severity:** MEDIUM (already attacked, not solved)
- **Evidence:** You have `unslop` (domain profiles), `copy-editing` Sweep 8 (De-AI), `voice/jerel/` V.O.I.C.E. files, `script-skill` 5-pass ad-VO loop, and `corrections.md` per skill. That's a 4-layer defense. But the reviewers in copywriting-os/reviewers/ don't yet check for the 60/30/10 violation: writing copy when a template + spreadsheet would do (e.g. Wave-2 alternate variant headlines that are just 5 mechanism × 1 angle permutations).
- **Why it matters:** Every AI-only step where a template would suffice = noise + cost + slop.
- **Fix:** Add a `layer-triage-check.md` gate to creative-os: ask "is this a template task or a judgment task?" before invoking the model.

### Problem 8: No preference bank → no DPO-lite signal
- **Severity:** LOW (nice-to-have, not blocking)
- **Evidence:** `learnings.md` is qualitative ("avoid X, prefer Y"). No structured "we picked variant B over A by margin Z" log.
- **Why it matters:** Multi-shot model improvement requires preference signal. Without it, learnings.md drifts toward vague aphorisms.
- **Fix:** `clients/<slug>/_brand/preference-bank.md` — table: date | task | variant_A | variant_B | winner | reason. Append after every comparison. Future iterations of the same task pull this as context.

---

## 5. Framework Fit Score

Per handoff format. Score 1-10 for THIS system specifically (not in general).

| Component | Score | Why it helps | Why it may hurt | Use now / postpone / avoid |
|-----------|-------|--------------|------------------|---------------------------|
| **ReAct (think → act → observe)** | **9** | Already implicit in slash-command flow + skill triggers. Doesn't need to be named. | Risk of over-formalizing what already works. | **Use now (don't formalize)** |
| **OODA handoff between agents** | **6** | Useful for `/ads:concepts` looping `big-angle-spotter` (each loop = OODA cycle with EXISTING_ANGLES update). | You don't run agents in parallel today. Don't introduce just to introduce. | **Use now (only where loop already exists)** |
| **ToT-lite (multiple options)** | **8** | `headline-bank` (75+), `big-angle-spotter` step 7-9 (3 ranked headlines), `image-generation` (3 variants per Ad Set) all already do this. Multi-agent-consensus skill exists. | Over-applying creates option-fatigue + expensive ranking. | **Use now (already in place)** |
| **Independent judges** | **7** | Copywriting OS reviewers exist for copy. Missing for ads/images/video. | Adding judges for everything = latency + cost. Pick high-stakes only. | **Use now (extend to creative-os)** |
| **Context packs (per-client)** | **9** | `clients/<slug>/` already this. Just needs L3/L4 split. | Without separation: cross-contamination (Problem 2). | **Use now + reorg** |
| **DPO-lite preference ranking** | **5** | Compounds learning. | Manual overhead. Most teams abandon after week 2. | **Postpone — automate before introducing** |
| **Full RAG (vector store)** | **3** | Would help if reference library hits 200+ files (it won't). | Premature for ~140 artifacts. Context-mode sandbox already does this for the 47 newsletters. | **Avoid (or postpone 12+ months)** |
| **OpenRouter / aggregator** | **4** | One key, many models, cheaper batch. | Adds dependency. Anthropic + Gemini-CLI + Ollama via `research-llm.sh` already covers cost-optimization for research. | **Postpone (revisit if costs balloon)** |
| **Fireworks/Together direct** | **3** | Cheap inference for high-volume variation gen. | You don't run high-volume. ~6 statics × 4 waves/month. | **Avoid** |
| **Direct provider APIs (Anthropic / OpenAI / Gemini)** | **8** | Anthropic for copy/judgment is correct default. Gemini-CLI exists for cheap synthesis. OpenAI rarely needed but available via API. | More API keys = more secrets to manage. | **Use now (already in place)** |
| **Fine-tuning / LoRA / PEFT** | **1** | Voice-fidelity for Jerel personally. | Massive infra investment. Same outcome from V.O.I.C.E. files + corrections loop. | **Avoid** |

**Net read:** You're well-positioned. The components scoring 8+ are already running. The components scoring ≤5 are correctly absent.

---

## 6. Model Strategy Recommendation

Don't change much. Current routing is correct.

| Role | Recommendation |
|------|----------------|
| Default controller | Anthropic Claude (current — keep) |
| Long-form sales letter, emotional nuance, copy chief review | Anthropic Claude Opus tier when available, Sonnet otherwise |
| Brainstorming / idea generation | Claude Sonnet (cheap enough, taste good enough) |
| Cheap batch synthesis for research | Gemini 2.5 Flash via gemini-cli OR Nemotron-3-Super via Kilo (both already wired in `research-llm.sh`) |
| Short-form variations | Claude Sonnet — don't add OpenAI just for variant generation |
| Judging / critiques | Claude (the same model that produced the work — independent invocation, fresh context, OS reviewers fire as sub-agents) |
| Local / privacy | Ollama Qwen3 (already wired) |

**Aggregator recommendation:** No. You don't need OpenRouter or Fireworks. Direct Anthropic + Gemini-CLI + Ollama via `research-llm.sh` covers ≥95% of workloads. Adding an aggregator buys complexity without solving a stated problem.

**Direct API recommendation:** Keep Anthropic primary. Gemini direct is fine for cheap research. OpenAI: skip unless a specific task surfaces that Claude genuinely loses on (none has, in 12 months of work).

**Fallback strategy:** `research-llm.sh auto` already does kilo → gemini → ollama fallback. Extend to copy work only if Anthropic outages become a real pattern. Currently they're not.

**Cost-control:** Already doing it via `analytics-usage` weekly. Add: token-budget audit per skill. Top 5 expensive skills: review prompts for unnecessary preamble.

**Privacy:** Sensitive client data (real names, financials, transcripts) — keep on Anthropic (their data policies are clearest) or Ollama (local, free). Avoid sending to aggregators where data path is opaque.

---

## 7. Recommended Architecture: Option A-Plus (Minimal+)

Keep what works. Add 3 things. Reorg folders. That's it.

```
COORDINATOR LAYER (no new agent — slash commands continue this role)
  /copy        →  Copywriting OS (live, working)
  /ads:*       →  Ads pipeline (live, working)
  /creative    →  NEW thin router for ad-image + video work (extends OS pattern)

PRE-WRITE / PRE-RENDER GATES
  copywriting-os/gates/  (live)  — channeling, coat-of-arms, one-person
  creative-os/gates/     (NEW)   — brand-fit, format-spec, ICP-resonance, layer-triage

DRAFTER / RENDERER (existing skills, no change)
  sales-letter-method, copywriting, email-sequence  (copy)
  image-generation, video-director, seedance-director  (creative)

POST-WRITE / POST-RENDER REVIEWERS
  copywriting-os/reviewers/  (live, 9 reviewers)
  creative-os/reviewers/     (NEW, 4 reviewers)

CONTEXT PACKS (L3 reference)
  clients/<slug>/_brand/   ← ALL stable identity, voice, ICP, offer
  clients/<slug>/_swipe/   ← ALL research dossiers, big-ideas, buyer language

WORKING ARTIFACTS (L4 source/output)
  clients/<slug>/campaigns/<c>/   ← in-flight wave + outputs

FINAL COPY CHIEF (existing pattern, optional explicit naming)
  Last reviewer in copywriting-os = teardown-reviewer = de-facto copy chief
```

### Why this and not Option B (Balanced) or C (Advanced)
- **Option B** would require building 4-5 new agents (Schwartz Strategist, Halbert Offer Engineer, etc.). You explicitly said: "do not create surface-level cosplay agents like 'write exactly like Gary Halbert'." You already use them as **lenses inside the existing reviewers** (proof-density-audit *is* Halbert lens; emotional-sequence-audit *is* Schwartz lens; one-person-enforcement *is* Halbert one-person). Don't externalize.
- **Option C** would explode coordination cost. You're a 1-2 person operation. 14 named agents = 14 places to maintain corrections.md.

### What NOT to build yet
- New agent named "Coordinator"
- New agent named "Final Copy Chief" (teardown-reviewer + brand-voice-guardian + the existing copywriter agent already serve this collectively)
- Full RAG over the 47 newsletters (context-mode sandbox already handles)
- Aggregator integration
- Fine-tuning / LoRA
- Vector store
- Memory MCP server (mem0) — your `corrections.md` + `learnings.md` are sufficient for current scale

---

## 8. Agent Responsibilities (only the ones that need clarification)

**No new agents needed.** Clarifying existing roles:

### `copywriter` (existing project agent)
- Purpose: execute drafts using `copywriting` or `sales-letter-method` skill. NOT a strategist.
- When called: by `/copy:*` sub-commands after gates pass.
- Inputs: brief + L3 context pack + filled gates (coat-of-arms.md, etc.)
- Outputs: draft to `clients/<slug>/campaigns/<c>/output/`
- Should NOT: invent new brand voice, change offer terms, override reviewers.

### `brand-voice-guardian` (existing)
- Purpose: enforce voice fidelity post-draft.
- When called: as last gate before ship, after teardown-reviewer.
- Should NOT: rewrite — flag and return to copywriter.

### `conversion-optimizer` (existing)
- Purpose: CRO review of landing pages, forms, popups.
- When called: by `/cro:*` skills.
- Should NOT: write copy from scratch — that's copywriter's role.

### `attraction-specialist` (existing)
- Purpose: TOFU + landing page strategy.
- When called: by `/seo:*`, `/copy:landing` for new landing.
- Should NOT: handle ads (that's the `/ads:*` chain).

### Agents to consider deprecating
- `solopreneur`, `startup-founder` — persona reviewers. Used? `analytics-usage` weekly should answer. If <2 invocations in 90 days, delete.
- `command-helper` — `/help:guide` skill duplicates this. One should die.

---

## 9. Handoff Protocol (compact, structured)

Use these blocks between stages. They live in `clients/<slug>/campaigns/<c>/handoff/<stage>.md`.

```xml
<copy_brief>
  one-paragraph summary of what we're writing + audience + outcome metric
</copy_brief>

<context_pack_summary>
  L3 files loaded for this stage (one line each, with token estimate)
</context_pack_summary>

<section_under_review>
  the section being judged (or "full draft" for end-of-pipeline)
</section_under_review>

<judge_scores>
  reviewer_name | pass/fail | severity | one-line reason
</judge_scores>

<recommended_fixes>
  1-3 fixes the next agent should make
</recommended_fixes>

<risks>
  any open risks — compliance, claim verification, voice drift
</risks>

<decision_summary>
  what was decided + assumptions + confidence + next action
</decision_summary>
```

---

## 10. Context Pack Strategy

**Recommended default: context packs first. Postpone full RAG indefinitely** unless reference material exceeds 500 files (current: 47 newsletters in context-mode sandbox + per-client artifacts).

### Per-client folder structure (PROPOSED)

```
clients/<slug>/
  CLAUDE.md                 # L0 — slim, "you are working on Client X". <80 lines.
  context-profile.json      # L0 — structured identity, ALWAYS loaded.
  
  _brand/                   # L3 — REFERENCE. Stable. Loaded selectively.
    icp.md                  # who we serve
    offer.md                # what we sell
    brand-voice.md          # how we speak
    buyer-profile.md        # buyer psychology
    channels.json           # where we run
    preference-bank.md      # NEW — past A/B winners
    pricing.md              # if applicable
  
  _swipe/                   # L3 — REFERENCE. Research/dossiers. Stable across waves.
    buyer-language-dossier.md
    big-ideas/              # podcast Big Ideas (NeezaNizam-style)
    competitor-pool.md      # links to industry swipe-files/
    forbidden-claims.md     # legal/compliance never-do list
  
  campaigns/<c>/            # L4 — WORKING. Per-campaign artifacts.
    angles/wave-N.md
    image-prompts/
    sheet-snapshots/
    handoff/<stage>.md
    output/                 # final deliverables, dated
  
  sales-letters/<date>-vN.md   # L4 — WORKING. Each draft + version tag.
  
  learnings.md              # L3 — REFERENCE. Confirmed patterns + saturated angles + kill list.
```

### Rules for context-pack hygiene

| Issue | Rule |
|-------|------|
| Stale context | If a `_brand/*.md` hasn't been edited in 6+ months and the client is active, flag during `/ops:monthly`. Force review. |
| Conflicting context | If `brand-voice.md` and `voice/jerel/brand-voice.md` conflict, **client wins** for client work. Document conflict in `clients/<slug>/learnings.md`. |
| Missing context | `/project:validate` already exists — extend to require all 7 `_brand/*.md` files before activation. |
| Untrusted context | Anything pulled from external research (reddit, transcripts, scraped sites) lands in `_swipe/`. Never auto-promote to `_brand/`. |
| Prompt injection in context | Per `planning-with-files` skill rule: never write external content directly to files that are auto-read by hooks. Quarantine in `_swipe/raw/` first, summarize, then promote. |
| Unsupported claims | `forbidden-claims.md` is canonical. Reviewers check against it. |
| Sensitive customer data (PII) | Never log to `_swipe/`. Quote-as-archetype only ("a buyer who said X"). |
| Source attribution | Every quote in `_swipe/` includes URL + date scraped. |

---

## 11. Sales Letter / Ad Copy / Ad Image Workflow (extended Copywriting OS)

The existing 15-step sales letter workflow holds. Adding two parallel pipelines using the same OS pattern.

### Sales letter (existing, working — `/copy:sales-letter`)
1. Read brief
2. Load `_brand/*` (L3) + relevant `_swipe/*` (L3)
3. Run pre-write gates: channeling-check, coat-of-arms, one-person-seed
4. Drafter (sales-letter-method) writes
5. Phase B reviewers (4 anti-hallucination)
6. Phase C reviewers (5 persuasion-craft)
7. copy-editing Sweep 8 (De-AI)
8. unslop pattern check
9. brand-voice-guardian final
10. Save preference lessons → `_brand/preference-bank.md`

### Ad copy (PROPOSED — `/copy:ad` enhanced)
1. Load `_brand/*` (L3) + `_swipe/competitor-pool.md` (L3) + current avatar from `_brand/avatars/avatar-N.md` (L3)
2. Run pre-write gates: channeling-check (Schwartz awareness), coat-of-arms (specific avatar), layer-triage-check (NEW — is this template work or judgment work?)
3. Drafter (`big-angle-spotter` + `headline-bank` mechanism diversity)
4. Phase B reviewers: claim-verification, forbidden-content, specificity, buyer-language-fidelity
5. Phase C reviewers: mechanism-diversity (NEW — across 3 headlines), proof-density, objection-coverage
6. Output to `campaigns/<c>/<adset>/copy/`

### Ad image (PROPOSED — `/creative:image` NEW)
1. Load `_brand/brand-voice.md` (tier signal, color palette references) + `_brand/avatars/avatar-N.md` (faces, demographics, ethnicity rules from NeezaNizam pattern) + design-system output if exists
2. Pre-render gates: brand-fit (palette + tier), format-spec (3:4 / 1:1 / 9:16 per platform), ICP-resonance (does the visual match avatar age/lifestyle/income tier?), layer-triage (is this generative or template work?)
3. Renderer (image-generation skill, Nano Banana 2)
4. Post-render reviewers: visual-claim audit (no fake testimonials/logos in image), brand-voice-fidelity (Lexus tier vs mass-market — image conveys this?), scroll-stop test (first 200ms read), mechanism-diversity (3 image variants per ad set use 3 different visual hooks)
5. Output to `campaigns/<c>/<adset>/images/`

### Video prompt (PROPOSED — `/creative:video` NEW)
- Same pattern, route through `seedance-director` or `video-director`
- Anti-cinematic gate (Seedance UGC requires "no smiles, no upbeat music, no investment language")
- Room-tone audio gate
- Natural dialogue gate

---

## 12. Edge Cases & Failure Handling

| Edge case | Detection | Fallback | Owner |
|-----------|-----------|----------|-------|
| Weak/missing brief | `/copy:*` gates require minimum brief fields | Block + ask user 3 questions | Coordinator (slash command) |
| Unclear audience | `_brand/avatars/` empty | Block + run `avatar-research` | User |
| Unclear offer | `_brand/offer.md` <100 words | Block + run `offer-builder` | User |
| Unsupported claims | `claim-verification-audit` reviewer | FAIL → revise or strip claim | copywriter agent |
| Fake urgency | `forbidden-content-audit` reviewer | FAIL → strip | copywriter |
| Conflicting reviewer feedback | If 2+ reviewers FAIL with contradictory fixes | Escalate to user via `<decision_summary>` | User |
| Too many agent loops (≥3 reviewer cycles) | Counter in handoff/<stage>.md | Stop + ship best-known state + log in learnings.md | Coordinator |
| Agent disagreement | Reviewer A pass, Reviewer B fail same section | User picks (multi-agent-consensus skill if needed) | User |
| Model timeout | Bash/skill error | `research-llm.sh auto` fallback chain | System |
| Anthropic outage | API error | Switch to Gemini-CLI for non-judgment work; pause for judgment work | User |
| Provider rate limit | 429 error | Wait + retry (existing `learnings.md` rule: never brute-force) | System |
| Cost spike | `analytics-usage` weekly | Audit top-spend skill | User |
| Aggregator outage | N/A — none in use | N/A | — |
| Bad external model output | Reviewer FAIL | Retry on Claude | System |
| Large context overflow | >180K tokens | Trigger compact + write context-log.md | User |
| Prompt injection in `_swipe/` | Reviewer detects "ignore previous" patterns | Quarantine source, alert user | System |
| PII in sources | grep for emails/phones in scraped files | Strip + quote as archetype | `_swipe/` ingestion script |
| Health/finance/legal claims | `forbidden-claims.md` keyword match | FAIL hard | claim-verification-audit |
| Style imitation issues | `unslop` detects pastiche | FAIL → rewrite in voice | brand-voice-guardian |
| Hallucinated sources/quotes | `claim-verification-audit` checks against `_swipe/` | FAIL hard | reviewer |
| Stale model rankings | quarterly review | Update `mcp-integrations.md` | User |
| API key leakage | `.gitignore` + pre-commit hook | rotate key + audit | User |
| Secrets in commits | git pre-commit hook (todo) | block commit | System (TODO) |
| Unclear final owner | every output has a `decision_summary` block | User decides | User |

---

## 13. Evaluation Rubric

Per-output rubric. Score 1-10. Pass = ≥7 across all dimensions, hard-pass on FAIL flags.

| Dimension | What it measures | Where it lives today |
|-----------|------------------|---------------------|
| Buyer-awareness fit | Match to Schwartz stage | channeling-check (gate) + emotional-sequence-audit (reviewer) |
| Market sophistication fit | Mechanism vs jaded market | channeling-check + mechanism-diversity (NEW) |
| Emotional specificity | Concrete fears/desires, not abstractions | one-person-enforcement + emotional-sequence-audit |
| Offer strength | Clarity, value, guarantee | (NEW — add to copy reviewers) |
| Proof density | Type variety + specificity | proof-density-audit |
| Believability | No unsupported claims | claim-verification-audit |
| Clarity | Readable at 8th-grade level | (existing in copy-editing) |
| Rhythm | Sentence variation, no monotone | unslop |
| Voice consistency | Match to brand-voice.md | brand-voice-guardian |
| Conversion strength | Subjective copy-chief judgment | teardown-reviewer |
| Compliance risk | Forbidden claims, legal | forbidden-content-audit |
| Generic-AI-copy risk | Pastiche, slop patterns | unslop + corrections.md |

**Stop iterating when:** ≥2 reviewer cycles + no FAIL flags + voice score ≥8. Document in `learnings.md` what changed between cycle 1 and final.

**Rewrite when:** any FAIL on Phase B (anti-hallucination) reviewers, OR ≥2 FAILs on Phase C.

---

## 14. Model Benchmark Plan

**Don't build a benchmark harness.** You're a 1-2 person op writing ~10 sales letters / 30 ad sets / month. The cost of building + maintaining a benchmark exceeds the gain.

If you want lightweight comparison, use a single markdown scorecard per quarter:

`docs/model-scorecard-YYYYMM.md`:
| Task | Claude (current) | Gemini Flash | Test result |
|------|------------------|--------------|-------------|
| Sales letter draft | A | C | Claude wins (voice nuance) |
| Headline batch ×10 | B | B | Tie |
| Research synthesis | B | A | Gemini wins (cost) |
| Image prompt | A | n/a | Claude only |

Run quarterly. ~30 min of work. No code.

---

## 15. Migration Plan

| Phase | Files affected | Changes | Risk | Benefit | When |
|-------|----------------|---------|------|---------|------|
| **5.1 Audit** | docs/architecture-review-260504.md | Produce this review | None | Decision clarity | DONE |
| **5.2 Client folder reorg** | clients/<slug>/* + clients/_template/ | Create `_brand/` + `_swipe/`, move files, add layer headers, update parent CLAUDE.md context-gate paths | Medium — 2 active clients (NeezaNizam) | L3/L4 separation, less cross-contamination | NOW (after HITL) |
| **5.3 Rules-index finish** | parent CLAUDE.md, .claude/rules/* | Slim parent CLAUDE.md to <60 lines, ensure details/* never auto-loads, audit system prompt | Low | -8K to -12K tokens per session | NOW |
| **5.4 Retired skill purge** | skills/seedance-loop/, /motion/, /prompt/, /effects/, /filmmaking/, /directors-cut/, global video-director, routing-table.md, skills-catalog.md | Delete + replace with redirect stubs | Low | Discovery clarity | NOW |
| **5.5 creative-os build** | .claude/references/creative-os/ + commands/creative.md + commands/creative/* | Mirror copywriting-os pattern for ads/images/video | Medium | Quality gates for image-gen | After 5.2-5.4 |
| **5.6 Stage contracts** | clients/_template/campaigns/_template/ | 5 CONTEXT.md files for the 6-stage pipeline | Low | Cleaner stage handoffs | After 5.5 |
| **5.7 Dogfood** | clients/neezanizam/campaigns/dct-260423/ (Wave 3, hypothetical) OR new client | Run end-to-end through new structure, audit token usage | Low | Validation | After 5.6 |
| **6 (FUTURE) Agent folder migration** | agents/* | Migrate to `agents/<name>/` folder pattern OR keep flat with prefix grouping | Medium | Consistency | Decide post-5.7 |
| **7 (FUTURE) Preference bank automation** | scripts/append-preference.sh + reviewers update | Auto-append after every comparison | Low | DPO-lite signal | If/when output drift becomes measurable |

**Recommend now:** 5.2 + 5.3 + 5.4 (low/medium risk, high payoff, all in this week).
**Recommend after dogfood:** 5.5 + 5.6.
**Recommend never:** OpenRouter, mem0, fine-tuning, full RAG.

---

## 16. What NOT to Build Yet

| Don't build | Why |
|-------------|-----|
| Full RAG / vector store | 47 newsletters fit in context-mode sandbox. Per-client artifacts fit in folders. RAG is for >500 files, not 140. |
| New agents (Schwartz Strategist, etc.) | They're lenses inside existing reviewers, not roles. |
| Coordinator agent | Slash commands are your coordinator. Naming it doesn't help. |
| Final Copy Chief agent | teardown-reviewer + brand-voice-guardian + copywriter agent already collectively serve this. |
| Fine-tuning / LoRA | V.O.I.C.E. files + corrections.md are sufficient at current scale. |
| OpenRouter aggregator | research-llm.sh covers it. |
| Fireworks/Together direct | Volume doesn't justify. |
| mem0 MCP server | corrections.md + learnings.md persist across sessions. |
| Memory MCPs | Same as above. |
| Autonomous multi-agent swarm | You don't have problems that benefit from this. Latency + cost > quality gain. |
| Complex memory system | learnings.md is the system. |
| Overbuilt model router | Simple `research-llm.sh` + Anthropic default is the optimal point. |
| Provider lock-in (e.g. only Anthropic API code) | Already abstracted. Don't undo. |
| Excessive benchmarking | Markdown scorecard quarterly is enough. |

---

## 17. Pre-Mortem: Why This Fails in 6 Months

Top 5 by probability.

| # | Failure reason | Early warning | Prevention |
|---|----------------|---------------|------------|
| 1 | **Reorg done, but new clients onboard via old pattern.** `_template/` not updated, new clients get flat folders. Inconsistency creeps back. | First new client folder has no `_brand/` subdir. | Update `clients/_template/` FIRST in 5.2. Lock `/project:new` to fail if `_brand/` missing. |
| 2 | **creative-os reviewers fire, FAIL on every image, get disabled.** Reviewers too strict, slow Phase 3a, Jerel disables them, quality regresses to current state. | First 3 image batches all FAIL on the same reviewer. | Soft-gate first month (warn + log, don't block). Tune thresholds against real data. |
| 3 | **Token bloat returns within 90 days.** New routing files, new reference docs, new global rules creep into auto-load. CLAUDE.md grows from 60 to 200 lines. | `/ops:weekly` token audit shows >5K auto-load tokens. | Hard rule in CLAUDE.md: any new auto-loaded line requires deleting an equivalent. Net-zero growth. |
| 4 | **Copywriting OS gates feel like friction, get skipped.** Jerel uses `/content:sales-letter` directly to bypass `/copy:sales-letter`. Quality drift returns. | `analytics-usage` shows declining `/copy:*` invocations. | Deprecate `/content:*` aliases by Q3. Force `/copy:*` as only path. |
| 5 | **Phase 5 does 5.2 + 5.3 + 5.4, never gets to 5.5/5.6.** Reorg + cleanup ships, creative-os never built. Image-gen quality gap remains. | 30 days post-5.4 with no creative-os movement. | Schedule 5.5 in calendar at 5.4 completion + 7 days. |

---

## 18. Assumption Audit

| Assumption | What if wrong | How to verify | How rec changes |
|------------|---------------|---------------|-----------------|
| Copywriting OS shipped 260424 is functional and validated | If reviewers haven't been dogfood-tested, they may be theoretical | Check `clients/<slug>/quality-gates/` for at least 1 logged run. If empty: dogfood ASAP before extending to creative-os. | Pause 5.5. Dogfood Copywriting OS first. |
| ~12-18K tokens auto-load per session | If actual is much lower, problem 1 is overstated | Run `/context` immediately after fresh session. Count tokens. | Reprioritize. If <6K, drop 5.3 priority. |
| 7 retired skills exist as flagged | If they were already deleted, problem 3 is moot | `ls skills/seedance-* skills/filmmaking skills/directors-cut` and check global skills | Skip 5.4. |
| L3/L4 mixing is causing measurable quality issues | If outputs are fine, this is theoretical hygiene with no payoff | Pull 5 recent outputs, judge: does any show context-bleed (treating brand-voice.md as content to transform)? | If 0/5 show issues, deprioritize 5.2. |
| Image-gen lacks quality gates | If big-angle-spotter step 12 is doing this implicitly, gap is overstated | Read big-angle-spotter step 12 prompt. Does it self-review? | If yes, scope 5.5 down to just gates, no reviewers. |
| Voice = Jerel personally, business = client (two-layer model) is right | If you ever bring on team writers, voice/<person>/ proliferates | Are we hiring in next 12 months? | If yes, voice/ becomes a registry; gate on "person" field in context-profile.json. |
| `/copy` adoption is real (not just deployed but used) | If `/content:*` is still the default invocation, Copywriting OS is dead-on-arrival | `analytics-usage` → check `/copy:*` vs `/content:*` invocation count last 30 days | If <10% are `/copy:*`, fix that BEFORE building creative-os. |
| Clients stay LOCAL to Marketing/ | If you spin up a second agency (e.g. Fuggy's Media as a separate vault), this is wrong | How many distinct businesses use this stack? | If ≥2, promote `clients/` to vault root and symlink into each agency project. |
| corrections.md + learnings.md compounding loop is functional | If they're written but never re-read, no compounding happens | Open 3 random corrections.md files. Are recent entries influencing recent outputs? Check git blame. | If no, build a `/ops:learnings-replay` skill that reads top 10 corrections at session start. |
| Anthropic-primary is right for this workload | If Gemini Flash matches on copy, you're overpaying | Run §14 quarterly scorecard once. Compare on real letter. | If Gemini ties or wins, reroute by task type. |

---

## 19. Final Recommendation

```
Recommended architecture: Option A-Plus (Minimal+) — keep Copywriting OS + extend to creative-os, reorg client folders to L3/L4 split, finish rules-index pattern.

Why: Re-architecture is unnecessary. The hypothesis in your handoff is 80% built. The remaining 20% is structural cleanup (folders, retired skills, parallel pattern for ads/images), not new primitives.

First 3 changes to make:
  1. Slim parent CLAUDE.md + finish rules-index pattern (5.3) — biggest single win on bloat (~8-12K token savings/session)
  2. Reorg one client (NeezaNizam) to _brand/ + _swipe/ + campaigns/ split. If it works, propagate to _template/ and the rest. (5.2)
  3. Delete the 7 confirmed-retired skills + update routing tables (5.4)

What to delete or merge:
  - 7 retired skills (seedance-loop, -motion, -prompt, -effects, filmmaking, directors-cut, global video-director)
  - Possibly: solopreneur, startup-founder agents (verify usage first via analytics-usage)
  - Possibly: command-helper agent (overlaps with /help:guide)
  - /content:* commands deprecated in favor of /copy:* (mark, don't delete yet — 90-day grace)

What to postpone:
  - creative-os build (after 5.2-5.4 land)
  - DPO-lite preference bank automation
  - Agent folder pattern migration

What to test before committing:
  - 5.3 token reduction: run /context before vs after, target ≥40% reduction
  - 5.2 client reorg: run a /copy:sales-letter on neezanizam after reorg, verify all gates still find their files
  - 5.4 deletions: run /skills:select for "video prompt" before vs after, verify routing surfaces seedance-director cleanly
```

---

## 20. Implementation Permission Boundary

**STOP HERE. Awaiting Jerel HITL before any of the following.**

### Allowed without further approval (pure-additive, reversible)
- Updates to `task_plan.md`, `progress.md`, `findings.md` (routing/state, not content drift)
- New draft architecture docs in `docs/`
- New benchmark scorecard template in `docs/`
- New migration checklist in `docs/`

### NOT allowed without explicit approval
- Any file delete (5.4 retired skills, 5.4 unused agents)
- Any file rename or move (5.2 client folder reorg)
- Any change to parent or nested CLAUDE.md (5.3)
- Any change to .claude/rules/* (5.3)
- Any change to skills-registry.json or routing-table.md or skills-catalog.md (5.4)
- Any new skill folder (5.5 creative-os)
- Any new slash command (5.5 /creative)
- Wiring any paid external API
- Installing any dependency

### Decision points awaiting your input
1. **Approve verdict (§1) and migration plan (§15)?** Yes / No / Modify.
2. **Pick first sub-phase to execute:** 5.2 (client reorg) / 5.3 (rules-index) / 5.4 (purge retired) / different ordering.
3. **Audit assumptions (§18) you want verified before exec:** which of the 10 to spot-check first.
4. **Pre-mortem (§17) acknowledged?** Any failure mode you want tighter prevention on.
5. **Anything in §16 (don't-build list) you disagree with?**

---

## Appendix A: Jake/Eduba Pattern Application

Jake's `vault-toolkit` ICM model maps to your system as follows.

| ICM Layer | Jake's role | Your current implementation | Gap |
|-----------|-------------|----------------------------|-----|
| **L0 — CLAUDE.md (always loaded, ~800 tokens)** | "Where am I?" Map only. | Parent CLAUDE.md is ~250 lines. Loads context-discipline rules, session protocol, learnings. + nested CLAUDE.md ~115 lines. Way over budget. | Slim to ≤80 lines (5.3). |
| **L1 — CONTEXT.md (read on entry, ~300 tokens)** | "Where do I go?" Workflow routing. | `.claude/rules/_index.md` exists. Good. ~50 lines. Acceptable. | Keep. |
| **L2 — Stage contract (per-task, ~200-500 tokens)** | "What do I do?" | Lives inside SKILL.md. Mixed with execution + reference. | Build 5 stage CONTEXT.md (5.6). |
| **L3 — Reference (selectively loaded)** | "What rules apply?" Stable across runs. | clients/<slug>/{icp.md, offer.md, brand-voice.md, etc.} — but co-mingled with L4. | Reorg to `_brand/` + `_swipe/` (5.2). |
| **L4 — Working files (selectively loaded)** | "What am I working with?" Per-run. | clients/<slug>/{campaigns/, sales-letters/, sheet-snapshots/, angles/} — mixed with L3 in flat dir. | Reorg (5.2). |

### 60/30/10 audit on your stack

| Task | Should be (Jake) | Currently (you) | Action |
|------|------------------|-----------------|--------|
| Headline-bank generation (5 mechanisms × 10 angles × 5 awareness) | 60% template (cartesian product), 40% AI for nuance per cell | 100% AI | Convert to template-first: spreadsheet generates the matrix shell, AI fills cells. Token savings: ~80%. |
| Sheet writes (concept writer, meta puller) | 100% deterministic (Python script, no AI) | Already deterministic | ✓ Keep |
| Avatar 16-point breakdown | 30% AI (the psychological extraction), 70% template (the 16 points) | 100% AI | Convert template to .json schema, AI fills only the inferential fields. |
| Image prompts | 30% template (format spec, palette, ratio), 70% AI (the creative concept) | 100% AI | Add format-check gate (template). |
| Source-of-truth 26 sections | 50% AI (research synthesis), 50% template (structure) | 100% AI | Already partly templated via SKILL.md. Audit which sections are mechanical fills. |
| Sales letter drafting | 90% AI judgment | 90% AI | ✓ Correct — this is the 10% where AI earns its cost. |
| Reviewer judgments | 90% AI judgment | 90% AI | ✓ Correct |
| /ops:weekly knowledge hygiene | 80% deterministic scan + 20% AI summary | Currently 100% AI | Convert scan to script, AI only for summary. |

**Net read:** ~3-4 workflows are over-indexing on AI where templates would do. Layer-triage gate addresses this systemically.

---

## Appendix B: Decision Log (concise, auditable — replaces "show your reasoning")

```
Decision: Verdict = lightly refactor (not re-architect).
Evidence used: 
  - Existing Copywriting OS already implements 80% of handoff hypothesis
  - 7 retired skills + L3/L4 mixing + auto-loaded routing tables explain ~80% of bloat without architectural change
  - User explicitly stated "do not create surface-level cosplay agents"
Assumptions: 
  - Copywriting OS reviewers actually fire (need to spot-check, see §18)
  - Auto-load is ~12-18K tokens (need to verify, see §18)
Tradeoffs: 
  - Small risk that incremental fixes don't address root cause
  - Larger risk that re-architecture introduces new bloat AND loses working primitives
Rejected alternatives: 
  - Option B (Balanced — 9 named agents): rejected, user explicit on no cosplay
  - Option C (Advanced — 14 agents + Model Router): rejected, premature for 1-2 person ops
  - Full RAG: rejected, scale doesn't justify
  - OpenRouter aggregator: rejected, research-llm.sh covers
  - Migrate clients/ to global: rejected, two-layer model (voice=person, business=client) already correct
Confidence: HIGH on verdict, MEDIUM on phase ordering (5.3 before 5.2 may be better — quick win for token bloat)
Next action: HITL — Jerel approves §15 migration plan + picks first sub-phase to exec
```

---

*End of architecture review. No files moved, deleted, or renamed. No skills built. Awaiting approval.*
