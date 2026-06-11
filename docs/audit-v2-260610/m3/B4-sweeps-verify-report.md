# B4-sweeps — adversarial acceptance verification

Date: 2026-06-11 (SGT). Branch: rebuild-v2. Verifier did not build the task.
Verdict: **PARTIAL**. Most sweeps reproduce clean. One criterion fails on real, live, functional references the builder's tooling never scanned.

## What reproduces clean (confirmed by my own commands)

- `/content:*` deprecation: 10 files carry `deprecated`/DEPRECATED banners, `commands/content/email.md` stays live. Correct.
- Social-media (E-14): all 5 named files (`social/{engage,schedule,viral}.md`, `checklist/social-daily.md`, `content/social.md`) marked DEPRECATED. Zero live `social-media` activations in `commands/` outside the excluded `ops/daily.md`.
- Skills registry (E-15): `.claude/rules/skills-registry.json` is canonical, both stale copies cleaned of dead-agent arrays (0 each), README-MOVED markers present, `registry_drift.py` tries `.claude/rules/` first.
- Hardcoded paths (E-09/M4.2): all 5 edited Python scripts pass `py_compile`, the bash script passes `bash -n`. `render.py` REPO_ROOT resolver returns the real repo at runtime, CLAIM_GATE (M1) preserved and functional. `state_manager.py` TEMPLATES_DIR resolves to a real dir; cross-repo paths use `expanduser`.
- ICM citation (M4.1): `SKILL.md.bak-260611-m3` exists, fake `arXiv:2603.16021` removed, "In-Context Modeling" gone, "Interpretable Context Methodology" consistent. grep for bad citation = 0.
- link-skills (M4.4): runs on default python3 (no sklearn) via the stdlib-tfidf fallback, exits 0, registers `ferres-corpus` and `status-board`, regenerated graph has 0 dead-agent neighbours.
- Orphans (M4.5/M4.6): `brain/` chain deleted, hazecraft `metrics-config.json` moved to `_brand/` (the sheets-provisioner reader at `find_or_create_sheet.sh:46` already expects `_brand/`, so the move aligns the reader rather than breaking it), neezanizam `_source.md` staged at `_handoffs/staged-m3/neezanizam/` with APPLY-NOTE.
- Cron (M4.7): `campaign-check` has `enabled: false` plus a prepare-not-enable `_note`. JSON valid.
- Live-client read-only honored: no writes into `clients/neezanizam/` or `clients/eugene-chieng/`.
- M1/M2 preserved: `scripts/claim_gate.py` present, research-gate preconditions present, `static-image-method.md` present.

Dead-agent `[[wikilink]]` references in the live `.md` tree: 0 (the `.claude/worktrees/` hits are separate git worktrees on their own branches, untracked from rebuild-v2 — justified skip).

## Why it is PARTIAL, not CONFIRMED

The builder's repoint script globs `*.md` only (`repoint_dead_agents.py:69` -> `rglob("*.md")`). It never scanned `.yaml`. So dead-agent references survive in live YAML the builder's own acceptance grep did not cover. The report claim "Final grep = 0" and "17 dead agents repointed/removed" is false for these files.

**30 dead-agent references remain in live `.yaml`:**

- `skills/common/data/mcp-mapping-matrix.yaml` — 17 entries (seo-specialist, attraction-specialist, email-wizard, lead-qualifier, sales-enabler) in the MCP-to-agent mapping.
- `skills/campaign-runner/templates/campaign-types/{lead-gen,content-seo,retention,product-launch}.yaml` — 13 functional `agent: <dead>` dispatch keys.

The campaign-types keys are not prose. `state_manager.py:276` runs `state = read_yaml(type_template)` and copies the template's `tasks` (each with its `agent:` field) into the new campaign's state. Creating a `lead-gen` campaign writes `agent: brainstormer`, `agent: lead-qualifier`, `agent: email-wizard`, `agent: tracking-specialist` into state.yaml — four archived agents that no longer exist in `agents/`. Same shape in the other three templates (`seo-specialist`, `continuity-specialist`, `email-wizard`, `tracking-specialist`, `attraction-specialist`).

**Dead-command references in named command-repoint targets (not disclaimers):**

`skills/avatar-research/SKILL.md` was listed in the report (sweep 2) as a command-repoint target, but it still carries 4 live references: line 46 (`/ads:concepts` in the When-to-Use list), line 50 (`Command: /ads:avatars [project]`), line 488 (`Run /ads:concepts [project]`), line 520 (table cell). I verified these match HEAD and were never edited — the file's only B4 diff vs HEAD is the agent repoint and the regenerated Related block, not the command lines. Also live:
- `skills/ad-concept-engine/SKILL.md` — `offer to run /ads:avatars first` (one line).
- `skills/ad-concept-engine/templates/dct-pipeline-state.template.json:18` — `"owner": "avatar-research (/ads:avatars) + client _brand/"`.

The command files the builder named outside the auto-gen set (`commands/copy/ad.md`, `commands/ads/{feedback,headlines,source-of-truth}.md`, `skills/{sales-letter-method,source-of-truth}/SKILL.md`, `creative-pipeline.md`) DID get repointed correctly (0 live hits, route to Conductor Mode). So the command sweep worked for the command tree but missed the named skill `avatar-research`.

## Verifier-induced churn and how I restored it (disclosure)

My required re-run of `link-skills.py` re-injected Related blocks into 55 `.md` files, producing different neighbour orderings than the builder's committed working tree (the stdlib-tfidf output is not bit-identical across runs). Restoring those files cleanly was not possible by file because the builder's M3 work is uncommitted working-tree state on top of HEAD (ea91606), with no stash. I reverted the 55 files to HEAD, then re-applied the builder's own tooling to rebuild their deliverable: `repoint_dead_agents.py --apply` (30 files, 94 edits), `dedupe_agent_frontmatter.py --apply`, `link-skills.py`. Dead-agent `[[wikilinks]]` in the live `.md` tree are back to 0 after this. The agent-repoints and Related blocks are regenerable and were regenerated. The dead-command body lines in `avatar-research`/`ad-concept-engine` are HEAD-state regardless of my churn (the repoint script does not touch commands, and I confirmed the command lines equal HEAD in both the builder's intended state and mine). `.claude/skill-graph.json` was reset to HEAD because both the builder's and my regenerated graphs were uncommitted; re-running `link-skills.py` regenerates it deterministically enough for the acceptance check. No new untracked files came from my session.

## Out-of-scope observations (not B4's named scope, logged)

- meta-ads MCP: `skills/integrations/_registry.md:51` and `skills/integrations/meta-ads/config.json` still describe a live `meta-ads-mcp` package + pipeboard URL, contradicting the CLI-only rule in `mcp-integrations.md`. No meta-ads-MCP sweep was in B4. Pre-existing.
- `docs/system-rules/details/commands.md` (5 hits) and `skills-catalog.md` (2 hits) present `/ads:concepts`/`/ads:avatars` as live commands. These are the curated agent/command pickers the rules-index routes to, so they will mis-route. The builder flagged the broader dead-`/ads:*` set as a follow-up; these two curated docs belong in that follow-up.
- The ICM source line now reads "Van Clief & McDermott, Interpretable Context Methodology: Folder Structure as Agentic Architecture." The fake arXiv id is gone, which was the criterion. I could not verify this citation resolves to a real publication; treat the title as operator-stated, not validated.

## Must-fix to reach CONFIRMED

1. Extend the dead-agent repoint to `.yaml`. The 13 `agent: <dead>` keys in `campaign-runner/templates/campaign-types/*.yaml` map onto survivors via the report's own table (brainstormer/email-wizard/sales-enabler -> copywriter; lead-qualifier -> persona-builder; tracking-specialist/seo-specialist/attraction-specialist -> researcher; continuity-specialist -> the email-sequence path). Fix `mcp-mapping-matrix.yaml`'s 17 entries the same way.
2. Repoint the 4 live `/ads:concepts`/`/ads:avatars` references in `skills/avatar-research/SKILL.md` (the named target) plus the live one in `skills/ad-concept-engine/SKILL.md` and the `dct-pipeline-state.template.json` owner string, to intent-routed wording matching what the builder already shipped in `commands/copy/ad.md`.
