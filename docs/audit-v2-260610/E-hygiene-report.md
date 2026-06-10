# Dimension E — HYGIENE Audit Report

_Audit date: 2026-06-10 (SGT). Repo root: `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing`. All paths repo-relative unless `~`. READ-ONLY — only write was this report._

Jargon key: **stale doc** = a file an agent loads as law that contradicts the current repo. **hardcoded path** = a `/Users/jerel/...` string baked into code that breaks if the machine/vault moves. **dead pointer** = a file that cites a path which does not exist. **split-brain** = the same name living in two places with different contents. **secret** = a live credential/private key sitting on disk.

Method: I re-read every cited line this session (FACT) or label interpretation (JUDGMENT). Built on Phase-1 discovery (B-clients, E-handoffs, A2-infra, orientation) but independently re-verified each scope item.

---

## 1. STALE DOCS — agents load these as law, they are wrong

### E-01 (High, FACT) — eugene CLAUDE.md:76 forbids the exact folder that holds the live approved avatars
`clients/eugene-chieng/CLAUDE.md:76` says: "Do not use `_brand/avatars/` as buyer targeting … `_brand/avatars/` is legacy/tooling only." Reality: `_brand/avatars/avatar-1-cash-anxious-upgrader.md:2` is `status: APPROVED — Eugene signed off 2026-06-09`, `launch_priority: 1 (primary launch lane)`; `_brand/avatars/_index.md:1-5` calls these the canonical roster; `_brand/buyer-profile.md:125` states "Source of truth for buyer targeting is now the per-avatar files under `avatars/`" (restructured 2026-06-01). The folder CLAUDE.md points to instead — `_brand/visual-characters/` — contains only a 399-byte README. The live DCT workspaces are literally named after these avatars (`campaigns/upgrader-ads/dcts/dct-001-cash-anxious/`, `dct-002-math-blind/`).
**Consequence:** A fresh agent obeying client law would refuse to use the only approved targeting avatars and look in an empty folder — directly on the money path of a LIVE ad campaign.

### E-02 (Medium, FACT) — eugene CLAUDE.md:185 advertises "4 micro-personas" that no longer exist there
`clients/eugene-chieng/CLAUDE.md:185`: "| Buyer psychology + 4 micro-personas | `_brand/buyer-profile.md` |". Reality: `_brand/buyer-profile.md:125` — MP1 promoted to avatars, MP2/MP3/MP4 demoted to backlog on 2026-06-01; active roster is 2 avatars (avatar-3 retired). The count and the file role both rotted.
**Consequence:** Cold agent is sent to a file for a persona set that was moved out of it 9 days ago; wastes a load and may author against demoted personas.

### E-03 (Medium, FACT) — neezanizam CLAUDE.md:28 says "One workbook"; there are three
`clients/neezanizam/CLAUDE.md:28`: "Google Sheet: `14bh8k6S…`. … One workbook, separate tabs per metrics-campaign." Reality: `_brand/metrics-config.json` registers THREE distinct spreadsheet IDs across 4 campaigns — buyer-funnel `14bh8k6S…`, asset-progression `1D-HrqZ…`, thomson `1KqWJP0…`. This was explicitly flagged for fixing in `SESSION-HANDOFF-thomson-sheet-260608.md:102` and never fixed.
**Consequence:** An agent obeying client law writes Thomson/asset-progression metrics against the wrong workbook's assumptions — data lands in or overwrites the wrong sheet.

### E-04 (Medium, FACT) — 11 `/content:*` command files are called deprecated in the index but carry zero in-file markers
`.claude/rules/_index.md:53` declares "`/content:*` (deprecated → use `/copy:*`; EXCEPT `/content:email`)". Yet all 11 files in `commands/content/` (ads, blog, cro, editing, email, enhance, fast, good, landing, sales-letter, social) contain `0` deprecation markers (grep for deprecat/superseded/moved-to = 0 each).
**Consequence:** An agent that opens the command file directly (not the index) sees a fully live command and runs the deprecated path — splitting copy output across two competing engines.

---

## 2. DUPLICATED ARTIFACTS & SPLIT-BRAIN NAMING

### E-05 (Medium, FACT) — root `propwise-sg/` vs `clients/propwise-sg` are two different things, and the client one is a symlink OUT of the repo
`clients/propwise-sg` is a symlink → `/Users/jerel/AI workflows/V4 Agent kit marketing/propwise-sg/marketing/client` (ls -ld). Root `propwise-sg/` is a real directory (CLAUDE.md, gtm/, marketing/, tech/, Propwise Logo.png). Zero filename overlap between them (`comm -12` empty).
**Consequence:** Two unrelated "propwise-sg" trees collide on one name; the client copy is an external symlink that dies on clone/move/backup, silently emptying the client. Operator can't trust which is canonical.

### E-06 (Low, FACT) — `docs/handoff/` vs `docs/handoffs/` (singular/plural, 1 file each)
`docs/handoff/2026-04-24-copywriting-os-phase-1.md` and `docs/handoffs/metrics-automation-handoff.md`. Two near-identical folder names, one file each, nothing reconciles them.
**Consequence:** Handoffs scatter; an agent looking for prior handoffs in one folder misses the other.

### E-07 (Low, FACT) — swipe-file naming collision: root `_swipe/`, root `swipe-files/`, and 6 per-client `_swipe/`
Root `_swipe/winning-ads/`, root `swipe-files/property-sg/`, plus 6 client-level `_swipe/` dirs. `ghost-sync.py:7` treats `swipe-files/<industry>/` as canonical; `_swipe/` is the per-client convention. Three names for swipe material.
**Consequence:** Agents and scripts disagree on where swipe data lives; the sync script reads `swipe-files/` while client work writes `_swipe/`.

### E-08 (Low, FACT) — `neezanizam_DCT3` run duplicated client↔`~/AI workflows` with NO marker (unlike eugene's managed dup)
`~/AI workflows/big-angle-spotter/runs/neezanizam_DCT3_260421-1748/` mirrors `clients/neezanizam/campaigns/buyer-funnel/angles/_spotter-runs/wave-1/DCT3/`. No `RELOCATED.md`/`_source.md` marker (ls grep empty) — contrast `eugene-hardened-260606`, where `~/AI workflows/.../RELOCATED.md` declares the client copy canonical and awaits operator delete-OK.
**Consequence:** Unmanaged duplicate; nobody knows which copy is authoritative or whether edits to one propagate.

---

## 3. HARDCODED ABSOLUTE PATHS (portability)

### E-09 (High, FACT) — 94 hardcoded `/Users/jerel/...` strings across 31 files; the worst are EXECUTABLE scripts that hard-break on any other machine
Count: 31 files, 94 occurrences (grep across `skills/ commands/ scripts/ .claude/`, exclusions applied). Most are docs/audit logs (cosmetic), but these are real executable breaks:
- `scripts/phase4_acceptance_test.py:22` — `REPO = Path("/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing")`
- `scripts/build_copyos_reviewers.py:29` — same hardcoded REPO
- `scripts/link-skills-watch.sh:13` — `MARKETING="/Users/jerel/Documents/…/Marketing"`
- `skills/video-concept-lab/scripts/validate_reference_graph.py:76-78` — 3 hardcoded `/Users/jerel/.claude/agents/*.md`
- `skills/campaign-runner/scripts/state_manager.py:231-233` — hardcoded `/Users/jerel/.claude/skills/video-factory/` + `/Users/jerel/AI workflows/higgsfield-prompts/`
**Consequence:** These scripts crash for anyone but Jerel, and break the moment the vault folder is renamed/moved (the vault has an apostrophe + spaces in the path — already fragile). The factory is not portable.

---

## 4. ICM CITATION (canonical skill carries a wrong/contradictory attribution)

### E-10 (Medium, FACT) — `icm/SKILL.md` expands "ICM" two different ways and cites a paper whose title doesn't match
`~/.claude/skills/icm/SKILL.md:6` titles it "ICM — Interpretable Context Methodology". But `:12` sources it to "Van Clief & McDermott, *In-Context Modeling for Agentic Software* (arXiv:2603.16021v2)" — a different expansion ("In-Context Modeling") and a different title than the methodology name. `:3` (description) also says "Interpretable Context Methodology (ICM, arXiv:2603.16021v2)". Operator states the real title is "Interpretable Context Methodology: Folder Structure as Agentic Architecture."
**Consequence:** The canonical architecture skill — loaded for every scaffold/structure decision — cites a misattributed (likely fabricated) source and contradicts its own acronym. Erodes trust in the foundational pattern; fix lands in M4.

---

## 5. ORPHANS, SECRETS & ODDITIES

### E-11 (Critical, FACT) — `credentials/` holds a LIVE Google service-account private key + OAuth refresh token on disk at repo root
`credentials/gsheets-service-account.json` contains `private_key` (RSA) + `client_email` + `project_id` (mode `-rw-------`). `credentials/oauth_token.json` contains `token` + `refresh_token` + `client_secret`. `git check-ignore -v credentials/*` → `.gitignore:113` (IGNORED, good — not in git). But these are live secrets sitting unencrypted in the working tree.
**Consequence:** Gitignore is the ONLY thing preventing these from being committed; any `git add -f`, a backup, or a copied vault leaks a service-account private key + a refresh token that can mint Google access. Data-exposure class. (Gitignore present = not Critical-leaked-yet, but live keys on disk in a synced Obsidian vault is the highest-stakes hygiene item here.)

### E-12 (Medium, FACT) — accidental empty path chain `brain/jerels brain/Marketing/...` (NOT gitignored)
`find brain` → `brain/jerels brain/Marketing/clients/{stackworks,takekine}/...` down to `.../test_2/02_script/output` — 13 nested dirs, ZERO files (`find brain -type f` = 0). `git check-ignore brain/` → NOT-IGNORED. The path `jerels brain` (no apostrophe) is a mis-resolution of the real vault `Jerel's brain` — a script wrote into a wrong relative path.
**Consequence:** A ghost mirror of the real client tree created by a path bug; not ignored, so it can get committed (as empty dirs / `.DS_Store`). Misleads anyone exploring the repo into thinking there's a second client tree.

### E-13 (High, FACT) — `ghost-sync.py` reads `swipe-files/<industry>/ads-db.sqlite` as canonical input; that sqlite exists NOWHERE
`scripts/ghost-sync.py:7` — "Reads `swipe-files/<industry>/ads-db.sqlite` (canonical source)"; `:106,167,269` execute SELECTs against `sqlite_conn`. Repo-wide `find *.db/*.sqlite` returns only Cloudflare miniflare cache files (`clients/neezanizam/website/propnex-listings-widget/.wrangler/...`) — no `ads-db.sqlite` anywhere.
**Consequence:** The Ghost/swipe-vault sync is non-runnable as documented — its required input artifact has never existed in the repo. Anyone trying to populate the swipe encyclopedia hits an immediate `OperationalError`.

### E-14 (Medium, FACT) — `skills/_archive/social-media/` is still activated by 9 command files via a dead path
The skill lives only at `skills/_archive/social-media/` (archived). Neither `.claude/skills/social-media/` nor `skills/social-media/` exists. Yet 9 command files reference `social-media`: `commands/social/{engage,schedule,viral}.md`, `commands/content/social.md`, `commands/checklist/social-daily.md`, `commands/campaign/calendar.md`, `commands/ops/daily.md`, `commands/skills/select.md`, `commands/training/start-0-0.md`. `commands/social/engage.md:20` cites `.claude/skills/social-media/SKILL.md` (dead).
**Consequence:** 9 commands instruct agents to "Activate `social-media` skill" / load `.claude/skills/social-media/SKILL.md` — a path that doesn't exist. Social commands silently lose their framework or error.

### E-15 (Medium, FACT) — `skills-registry.json` exists in THREE copies; the one agents are TOLD to load is the stale 51-skill one with 8 dead pointers
Three copies: `skills/skills-registry.json` (51 skills, lastUpdated 2026-03-14), `.claude/skills/skills-registry.json` (51 skills, 2026-03-14, byte-different from rules copy), `.claude/rules/skills-registry.json` (132 skills, no version — the fresh/complete one). `_index.md:71`, `orchestration-protocol.md:154`, and `skills-catalog.md:8` all point agents at `.claude/skills/skills-registry.json` — the STALE 51-entry copy. That copy has 8 entries whose SKILL.md is missing: 5 archived (`social-media`, `document-skills/{docx,pdf,pptx,xlsx}`), 2 truly orphaned (`agent-chatrooms`, `autoresearch`), 1 global false-positive (`transcribe`). The fresh 132-skill registry is referenced by nothing.
**Consequence:** The orchestrator loads a 3-month-stale catalog missing ~80 current skills and pointing at 7 non-existent ones; skill discovery is silently degraded while a correct registry sits unused.

---

## 6. NAMING INCONSISTENCIES THAT MISLEAD AGENTS

### E-16 (Medium, FACT) — `metrics-config.json` lives in two locations across clients
`_brand/metrics-config.json` for takekine, neezanizam, eugene-chieng, harmony-wellness, `_template`; but `clients/hazecraft/metrics-config.json` at the client root (no `_brand/`). One client breaks the convention.
**Consequence:** A script or agent resolving `<client>/_brand/metrics-config.json` finds nothing for hazecraft and either errors or falls back wrong.

### E-17 (Low, FACT) — two live state-file schemas (`pipeline-state.json` ×18 vs `state.yaml` ×1); `plan-state` referenced nowhere
18 `pipeline-state.json` vs 1 `state.yaml` (takekine `campaigns/test_2/`). `plan-state*` = 0 files and 0 references in skills/commands/.claude. (Note: the stage-map's "three schemas" overstates — only two are live; `plan-state` appears to be a phantom.) Also `dct-tracker.json` (6, legacy) coexists with `dct.json` (7, new) mid-migration.
**Consequence:** takekine's lone `state.yaml` + JSON elsewhere means any state-reader must handle two formats; agents told to read `pipeline-state.json` find nothing in takekine's campaign and may misjudge phase.

---

## Notes for orchestrator
- E-10 (ICM citation) fix is owned by M4 per the prompt — flagged here as the canonical-skill defect, not for me to fix.
- E-05 propwise symlink-out-of-repo is the single most fragile portability item after E-09; confirm with operator whether root or symlinked copy is canonical.
- E-11 credentials: gitignored = not leaked, but live private key on disk in a synced vault warrants the operator moving them to keychain/env (matches the `gws`/`sheets-provisioner` two-identity model the repo already documents).
- E-15: the trivial fix (repoint the three docs at `.claude/rules/skills-registry.json`, the 132-skill copy) likely closes most of the "51 issues" the knowledge-hygiene tool reports.
