# Routing Overrides (manual)

Edit this file when the auto-generated `routing-table.md` picks the wrong skill. Each entry below overrides keyword matches.

Format: `<trigger phrase or condition>` → `<skill-name>` _(why)_

## Disambiguation

- `newsletter` + client context → `email-sequence` _(newsletters in V4 = client email programs, not blog newsletters)_
- `sales letter` (any length) → `sales-letter-method` _(NOT copywriting — long-form direct-response)_
- `ad copy` + Meta/Facebook → `headline-bank` _(Halbert-style 50/150 word with short headlines)_
- `ad angles` / `10 angles` / `spot angles` → `big-angle-spotter` _(full pipeline, not single-skill)_
- `swipe file` build/scrape → `ad-library-scraper` _(industry-level scraper, not manual)_
- `source of truth` / `26 sections` → `source-of-truth` _(generates the master doc)_
- `DCT batch` / `12 combinations` → `ad-concept-engine` _(downstream of avatar-research; 3-2-2 shape. For 10-5-5 conductor clients (neezanizam, eugene) — or any "continue/resume/new wave" framing — use the DCT-conductor entry below, which adds the resume protocol.)_
- **DCT conductor (intent-routed, no command):** `new DCT` / `new ad concepts for <client>` / `ad concept wave` / `next angle wave` / `continue the DCT` / `resume the <client> ads` / `where's the DCT at` / `pick up the ad concepts` → `ad-concept-engine` in **Conductor Mode** (SKILL.md §"Conductor Mode — Entry & Resume Protocol"). For 10-5-5 clients (neezanizam, eugene) the skill is self-navigating: it establishes the context receipt, locates the DCT workspace, reads `pipeline-state.json`, and RESUMES rather than restarting. It chains `big-angle-spotter` (angles) → `headline-bank` (copy) → render/allocate/sheet/upload as sub-steps — never reinvent those. Ambiguous client/funnel → ask ONE question, don't guess (neezanizam has two funnels: `buyer-funnel` vs `asset-progression`). _(Added 260609 — replaces the dead `/ads:concepts` command reference; entry is by intent, not a slash command.)_
- `build avatar` / `build persona` / `new avatar` / `ICP` / `buyer profile` / `audience segment` / `micro-persona` / `segment the market` → `avatar-research` _(SINGLE front door for building/segmenting avatars. Do NOT freehand with `general-purpose` sub-agents — that bypass happened 260529 and produced off-process drafts. avatar-research owns the output; it CHAINS the others as sub-steps, see Combos.)_
- `video concept lab` / `paid video concepts` / `AI video ad concepts` → `video-concept-lab` _(first creative step for AI paid video ads)_
- `video brief normalizer` / `google docs video brief` / `AI video production brief` / `approval gate 2` → `video-brief-normalizer` _(post-concept brief pack before Video Factory)_
- `video factory handoff` + concept context → require `brief-pack/approval-2.json` approved before `video-factory` _(do not start production from Approval Gate 1 only)_
- Spawn a video-concept workspace (AG1/AG2 ideation) → `/video:new-concept <campaign> <concept-slug>` _(NOT `/video:new` — that one scaffolds Video Factory render-projects, different pipeline)_
- `singing ad` / `sung ad` / `Suno` / `Suno brief` / `jingle` / `audio ad` / `music brief` / `song lyrics for ad` / `lullaby ad` / `ballad ad` / `script_mode: singing` / `script_mode singing` → load `skills/video-concept-lab/references/direct-response/singing-ads-layer.md` AND route via `vid-director` skill with `dr_singing_*` loadout (e.g., `dr_singing_solution_aware_l3_concept` for Solution-Aware × L3). Added 2026-05-22 — closes the gap where natural-language Suno-ad asks reached zero canonical pipeline. Per `vid-director.md §2.0.5` BOTH `video-concept-seeder` AND `video-prompt-pack-builder` must load this layer when ANY concept is sung.
- **Data-driven singing trigger (added 2026-05-22, broadened 2026-05-22):** when reading any workspace file (`concept-brief.json`, `pipeline-state.json`, `concepts.json`, `script-drafts.json`, `approval-1.json`, OR any file with `.json` extension inside a `video-concepts/` workspace) that contains ANY of these patterns → IMMEDIATELY load `singing-ads-layer.md` + the full `dr_singing_*` `extends` chain from `REFERENCE_GRAPH.json` BEFORE dispatching any downstream agent or producing any sung output:
  - `"script_mode": "singing"` (verbatim exact match)
  - `script_mode.*(singing|sung|lullaby|jingle|suno|song)` (consolidated regex — catches all known sung-register vocabulary in TakeKine + other workspaces; also catches descriptive values like `"mixed (2 spoken c01+c02, 1 sung c03)"`) — added per test D synthesis 2026-05-22
  - `"script_mode": "mixed"` AND elsewhere in same file `singing` OR `sung` OR `lullaby` (multi-pattern match for descriptive mixed-mode values)

  This fires regardless of operator keywords — the brief content itself triggers the load. Closes both: (1) the case where workspace path was given but no singing keywords were typed (test B pre-fix), AND (2) the case where pipeline-state uses descriptive `"mixed"` values instead of clean `"singing"` (test B post-fix gap #2).

  Every downstream agent (`video-concept-seeder`, `video-prompt-pack-builder`, `eval-buyer-fit`) also carries a self-defense check that fires this same rule independently — defense-in-depth against direct-dispatch bypass (test B post-fix gap #1).

## Copy deliverable → canonical owner (added 2026-06-02)

Full owner table + hook disambiguation: `docs/copy-routing-map.md` (human-readable mirror). Terse precedence:

Sales-letter / Meta-ad-text / angles / DCT are already disambiguated under §Disambiguation above — not repeated here. Net-new precedence only:

- Page copy (landing / pricing / home / about) → `copywriting` via `/copy:landing`
- **The copywriting-vs-copy-editing-vs-copy-coach split** (previously NO override — fell to model judgment): write net-new prose → `copywriting` (pages) / `sales-letter-method` (letters); polish / de-AI an EXISTING draft → `copy-editing`; coach the Big Idea / spine / line craft interactively → `copy-coach`.
- Email / sequence → `email-sequence` (copy) + `email-marketing` (strategy) via `/content:email` _(the ONE live `/content:*` engine — every other `/content:*` is deprecated)_
- Hooks by context: paid-video-ad → `video-hook-variants`; organic short-form → `viral-hooks-content-creator`; IG Reel → `ig-reel-script-writer`. The opening line of a letter/email/ad is the LEAD (handled inside that copy skill), not a hook skill.

- `wire metrics` / `new campaign metrics` / `setup metrics cron` / `connect campaign to sheet` → `metrics-wire` _(inventory-first wiring into the Modal metrics cron + verified test write. `sheets-updater` = manual ad-hoc pulls only; the cron implementation lives at `scripts/modal/marketing_metrics.py`. Added 260612.)_

## Copy principle overrides (resolve cross-layer contradictions — added 2026-06-02)

- **Readability is audience-relative, not fixed-grade** — third-grade Singapore-English for ESL/consumer, professional/technical for insider/B2B. This OVERRIDES the global `/writing` skill's fixed grade-4–6 target for insider/B2B copy (grade 4–6 applies to consumer short-form only).
- **Always reply in English** — overrides any skill/command "respond in the user's language" boilerplate (inherited from AgentKits templates; contradicts the standing global rule).
- **One kill-list:** `forbidden-content-audit.md` is the canonical anti-slop source; `unslop`, `copy-editing` Sweep 8, and the global `/writing` banned-word list defer to it.

## GPT Image 2 generation (executor routing — added 2026-05-30)

- `generate image with GPT Image 2` / `gpt-image-2` / `make an image with GPT image two` / `start-frame image` → run `~/.claude/scripts/gpt-image-2 "<prompt>" --out <path>`. This is the **Azure gpt-image-2** Images API (5-region round-robin pool), keys in `~/.claude/.env` (`AZURE_*`). _(Do NOT route GPT Image 2 generation through Higgsfield — Higgsfield is a separate backend used only for the video/motion step. The conflation "Higgsfield using GPT Image 2" is wrong; the actual image executor is Azure. Vendored from comic-storyboard/azure_images.py.)_
- character-consistent / reference-conditioned GPT Image 2 → add `--ref <img>` (repeatable, up to 16) → routes to `/images/edits`. _(prompt-craft for these images still lives in `gpt-image-2-director` skill; this is only the executor.)_

## Combos (fire multiple)

- `new client onboarding` → `client-onboarding` THEN `business-profile` THEN `avatar-research`
- `kick off campaign` → `campaign-runner` (orchestrates the rest)
- `voice / how I write` → `script-skill` (speech patterns) + `unslop` (de-AI profile)
- `build avatar` / `avatar-research` → `avatar-research` is the ORCHESTRATOR and owns the output (`buyer-profile.md` / avatar files / micro-personas). It chains, as SUB-STEPS (not parallel siblings): (1) `buyer-language-researcher` for voice-of-customer dossier + verbatim grounding, THEN (2) `persona-builder` agent for psychological depth (emotional drivers, fears, Schwartz mapping). Existing research-vault dossiers satisfy step 1 if fresh. Never substitute a `general-purpose` agent for this chain. _(Added 260529.)_

## Hard skips

- Generic "write copy" without page type → ask which page first; do not auto-pick `copywriting`
- "research" without scope → ask scope; do not auto-pick `deep-research`

## Design system enforcement (MANDATORY pre-flight gate)

Before writing ANY HTML, deck, motion, gallery, or visual artifact for a HazeCraft-published surface, you MUST first read `clients/hazecraft/DESIGN.md` (the canonical YAML+prose source). This applies to:

- All `plans.genflos.com/<client>/...` HTML (vault landings, plans, onboarding, approval gates, concept previews)
- All HazeCraft-owned decks, case studies, dashboards
- All motion/video review surfaces published under HazeCraft
- All carousels, ad creatives, and approval galleries where HazeCraft is the visible publisher

**For other clients with their own DESIGN.md**, the same rule applies — read `clients/<that-client>/DESIGN.md` first. Use the YAML token values verbatim. Honor the Do's and Don'ts as hard rules.

**If no DESIGN.md exists for the client**, prefer to build one via `design-md-builder` before generating HTML. If the operator declines, fall back to `clients/hazecraft/DESIGN.md` as the agency-default wrapper for any artifact where HazeCraft is the visible publisher.

This is the same rule as `~/.claude/skills/plans-vault/SKILL.md` § Design Contract — surfaced here so it fires at the routing layer, before any HTML-emitting skill runs.

## Artifact provenance (MANDATORY before any vault sync)

Before copying an artifact into `~/plans-vault/<client>/` and running `sync.sh`, you MUST locate the canonical *latest* version of that artifact in the client's working tree — not the snapshot already in the vault. Default search order:

1. `clients/<client>/campaigns/<campaign>/video-concepts/<concept-slug>/02_ag1-options/` (AG1 review surfaces)
2. `clients/<client>/campaigns/<campaign>/video-concepts/<concept-slug>/07_review/` (post-AG1 review)
3. `clients/<client>/campaigns/<campaign>/04_review/` (campaign-level review)
4. `clients/<client>/output/`
5. `clients/<client>/deliverables/`

Pick the file with the most recent `mtime` matching the artifact name. If multiple candidates exist, surface them to the operator BEFORE copying — do not guess. After copying, record provenance as a sibling file `~/plans-vault/<client>/<artifact-path>/_source.txt` containing the absolute source path + `mtime` + a `sync_check` one-liner the operator can run to detect drift.

Skipping this gate is how stale concept-previews ended up live (2026-05-18 incident — takekine concept-preview vault snapshot lagged the actual latest. Root cause was campaign scaffolders creating legacy `02_script/output/` folders that agents then dutifully nested `video-concepts/` inside; both scaffolders fixed 2026-05-18, but the canonical path is now `campaigns/<campaign>/video-concepts/<concept-slug>/02_ag1-options/` — never under `02_script/`).

## Brand-alignment evaluator gate (MANDATORY before any AG1/AG2 HTML publish)

Any HTML render dispatched to `~/plans-vault/<client>/ag1/` or `~/plans-vault/<client>/ag2/` MUST first verify that `<workspace>/eval/buyer-fit-cycle-<N>.json` (latest cycle) exists with `verdict: "PASS"` for the corresponding phase (`fired_at_phase: "4.6"` for AG1, `"6.5"` for AG2). If missing or non-PASS:

- Refuse to render. Surface to operator: `eval-buyer-fit verdict not PASS — orchestrator must dispatch eval-buyer-fit (Sonnet, persistent, 3-cycle cap) before HTML publish. Path expected: <workspace>/eval/buyer-fit-cycle-<N>.json`.
- Acceptable bypass: `pipeline-state.json.eval_override` recorded by operator with timestamp + reason.

This rule fires at the html-render layer specifically because the orchestrator may dispatch html-publisher in parallel with edits and the gate must hold even on parallel flows. Full rule in vid-director.md §4 (eval-buyer-fit roster row), §9 (AG1 + AG2 hard preconditions), §11 items 21–22, §12 cycle-cap budget. Agent spec: `~/.claude/agents/eval-buyer-fit.md`. Scope: buyer fit only — claim safety remains owned by `video-concept-seeder` + `video-prompt-pack-builder`.

## Copywriting-OS auto-load (no slash command needed)

Whenever the user mentions copy work, AUTO-LOAD `.claude/references/copywriting-os/` files in this order — do not wait to be asked, do not invoke a slash command:

| User mentions | Load these files |
|---|---|
| `headline` / `lead` / `hook` | `frameworks/five-headline-mechanisms.md` |
| `proof` / `believability` / `claims` | `frameworks/six-proof-types.md` + `builders/proof-inventory-builder.md` |
| `objection` / `they won't buy because` | `frameworks/six-objection-categories.md` + `builders/objection-matrix-builder.md` |
| `emotion` / `sequence` / `flow` | `frameworks/six-emotional-states.md` |
| `who am I writing to` / `avatar` / `reader` | `frameworks/halbert-trio.md` + `gates/coat-of-arms-generator.md` + `gates/one-person-seed.md` |
| `feels generic` / `not converting` / `falls flat` | `frameworks/schwartz-channeling.md` + `gates/channeling-check.md` |
| `prompting` / `LLM copy` / `AI tells` | `frameworks/collier-principle.md` + `frameworks/failure-mode-library.md` |
| `offer` / `pricing in copy` / `stack value` | `frameworks/hormozi-offer.md` |
| `origin story` / `founder story` / `about page` | `frameworks/legend-architecture.md` |
| `research` / `voice of customer` / `swipe` | `frameworks/scout-mode-instructions.md` |
| `review` / `audit` / `check this` + draft pasted | Load entire `reviewers/` chain (B then C phase) |
| `write` / `draft` / `start a new` + page type | Load gates first, then builders, then write |

When a user pastes a draft, do BOTH the requested change AND a reviewer pass. Never reply with just the change.

If a framework file lacks specific detail, fall back to `raw-newsletters/<slug>.md` for primary-source quotes (47 newsletters, mapped in `_newsletter-index.md`).

## Video Concept Lab auto-load (Solution-Aware × Stage-3 + multi-duration execution)

Whenever the user mentions specific framework triggers below — even outside a `/video:*` or `video-concept-lab` invocation — AUTO-LOAD the referenced files alongside the standard skill:

| User mentions | Load these files |
|---|---|
| `solution-aware` / `jaded buyer` / `tried and failed` / `discredit competitor` | `.claude/references/copywriting-os/frameworks/schwartz-channeling.md` + `skills/video-concept-lab/references/general/stage-4-discrediting.md` |
| `common enemy` / `us vs them` / `competitor positioning` / `villain frame` | `skills/video-concept-lab/references/general/common-enemy-bridge.md` (transitively loads `scout-mode-instructions.md` + `halbert-trio.md` + `legend-architecture.md` + `schwartz-channeling.md`) |
| `big idea` / `new mechanism` / `reframe` / `Stage 3 sophistication` | `skills/unique-mechanism-problem/SKILL.md` + `skills/unique-mechanism-solution/SKILL.md` |
| `15 second ad` / `30 second ad` / `45 second ad` / `60 second ad` / `90 second ad` / `compress to <N>s` / `ad length` / `duration budget` | `skills/video-concept-lab/references/general/video-compression-by-duration.md` |
| `creative lane` / `Iman lane` / `lane selection` | `skills/video-concept-lab/references/general/creative-lanes-methodology.md` (per-client lanes still live in `_brand/funnel.md`) |

## vid-director skill auto-load (replaces the legacy ccv system-prompt-file)

The `vid-director` skill at `.claude/skills/vid-director/` carries the director persona + dispatch map + prompting-framework knowledge. The heavy procedural rigor (AG0/AG1/AG2 ceremony, failure modes, resume protocol, html-render envelope schemas) lives in `references/vid-director-prompt.md` and loads only when needed.

**Auto-invoke the vid-director skill BEFORE any other action when ANY of these fire:**

- cwd resolves inside `clients/*/campaigns/*/video-concepts/*/` (any concept workspace)
- user mentions: `vid-director` / `video director` / `AG0` / `AG1` / `AG2` / `concept seeder` / `hook variant` / `prompt pack builder` / `eval-buyer-fit` / `html-publisher for video` / `creative-diversity-map` / `4-axis strategy` / `viral preset clone` / `paid video concepts` / `image-to-video` / `multi-clip ad` / `resume video workspace` / `generate concepts` / `run concept stage` / `approve AG1`
- a workspace path is handed over (the Resume Protocol still fires — the skill loads `references/vid-director-prompt.md §5 Step 5` for the full Resume Card pattern)

**When the skill must load `references/vid-director-prompt.md`:** running AG0 compass emission, writing `approval-1.json` / `approval-2.json`, dispatching `html-publisher` for AG1/AG2, `eval-buyer-fit` returning `CHANGE_REQUIRED`, operator says "where am I" / "show full state" / "resume". For ideation, dispatch, and framework questions the SKILL.md body alone is enough — do NOT pre-load the procedural reference.

**Does NOT replace:** `/video:new` (scaffolds workspaces), `/campaign:new` (scaffolds campaigns), `html-publisher` (renders all HTML), individual subagent contracts. The skill is a router, not a doer.

## Pre-dispatch Schwartz/Sophistication call (one-liner gate for `/copy`)

Before picking a format or dispatching any `copy-*` generator, think through three axes and state the call in one line to the user **before** writing or dispatching:

- **Awareness level** — what Schwartz level is the reader at? L1–L2 favor long-form, story-led leads. L4–L5 favor short, offer-heavy structures.
- **Sophistication stage** — what stage is the market at? S3–S5 require mechanism leads or identity leads, not plain claims.
- **Scope** — big enough to warrant a subagent (fresh context, independent execution), or single-pass yourself?

Commit, then announce: *"Treating this as Schwartz L2 / Sophistication S3 — writing a problem-led long-form sales letter for cold traffic. Dispatching `copy-sales-letter`."* The call must be reviewable, not buried in reasoning. Fires for every `/copy` invocation; skip only for explicit one-shot tweaks (`fix this sentence`, `tighten this CTA`).
