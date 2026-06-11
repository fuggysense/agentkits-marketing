# B4-sweeps report — M3.7 + M4 mechanical sweeps

Date: 2026-06-11 (SGT). Branch: rebuild-v2. All 10 sweeps ran sequentially, one concern at a time. Every acceptance grep came back clean (suite at bottom).

Helper scripts written (reusable, in `docs/audit-v2-260610/m3/`): `repoint_dead_agents.py` (context-aware dead-agent repointer), `dedupe_agent_frontmatter.py`.

---

## 1. DEAD AGENTS (D-11)

17 archived agents (`agents/_archive/`) referenced across ~134 live files. Built a canonical dead->survivor map (survivors: brand-voice-guardian, conversion-optimizer, copywriter, persona-builder, researcher; dead-with-no-agent-equivalent -> removed or pointed at the surviving skill/mechanism):

| dead | -> | dead | -> |
|---|---|---|---|
| attraction-specialist | researcher | planner | (removed / campaign-runner) |
| brainstormer | copywriter | project-manager | (removed / campaign-runner) |
| email-wizard | copywriter | docs-manager | (removed / knowledge-hygiene) |
| sales-enabler | copywriter | continuity-specialist | (removed / email-sequence) |
| seo-specialist | researcher | command-helper | (removed) |
| tracking-specialist | researcher | mcp-manager | (removed / use-mcp) |
| pseo-architect | researcher | solopreneur | brand-voice-guardian |
| lead-qualifier | persona-builder | startup-founder | brand-voice-guardian |
| upsell-maximizer | conversion-optimizer | | |

- Two auto-loaded rules files fixed by hand:
  - `.claude/rules/skill-activation.md:28,30` — research row -> researcher; multi-perspective row -> brand-voice-guardian + conversion-optimizer.
  - `.claude/rules/mcp-integrations.md:27` — dropped "delegate to `mcp-manager` agent" (no agent survivor; `/use-mcp` is the path).
- `repoint_dead_agents.py --apply` handled 4 reference shapes across `skills/`, `commands/`, `agents/`: YAML frontmatter list items, hand-authored `**Used by agents:** [[...]]` bullets, inline backtick/wikilink tokens, and bare-word table/prose tokens. It skips the link-skills `<!-- auto-generated -->` blocks (those regenerate in sweep 8) and a protect-list of common-noun false positives (`Budget planner`, `Company size (solopreneur`, `solo-steve`, training-persona names `startup-sam`/`manager-maria`, the sales-letter/copywriter learnings prose).
- `dedupe_agent_frontmatter.py --apply` collapsed duplicate survivor entries that appeared when multiple dead agents mapped onto one survivor (22 SKILL.md files).
- Stale `skills/skills-registry.json` + `.claude/skills/skills-registry.json` `"agents": [...]` arrays cleaned via inline JSON walker (51 each -> 0). Canonical `.claude/rules/skills-registry.json` was already clean (0).
- Tallies: 142 md files / 380 edits (skills+commands), then 5 agent files / 30 edits, then 22 frontmatter dedupes, plus the 2 rules files and 2 registries.

## 2. DEAD COMMANDS (C-07)

- Scope correction (logged): `/test:ab-setup` is NOT dead — `commands/test/ab-setup.md` exists and `test:ab-setup` is in the live registry. Left intact. Only `/ads:concepts` + `/ads:avatars` are dead.
- Repointed live-presented references to intent-routed wording (`ad-concept-engine` Conductor Mode for concepts; `avatar-research` skill for avatars) in: `commands/ads/{feedback,headlines,source-of-truth}.md`, `commands/copy/ad.md`, `skills/{ad-concept-engine,avatar-research,headline-bank,sales-letter-method,source-of-truth}/SKILL.md`, `skills/source-of-truth/references/{26-section-template,section-synthesis-frameworks,sheet-integration}.md`, `.claude/workflows/creative-pipeline.md`.
- LEFT UNTOUCHED (already M2-correct): `feedback-router/SKILL.md`, `feedback-router/references/routing-criteria.md`, `ad-concept-engine/SKILL.md:67` and the `routing-overrides.md` DCT-conductor entry — these cite the dead commands only inside "(the old command is dead)" disclaimers.

## 3. SOCIAL-MEDIA (E-14)

8 in-scope command files marked DEPRECATED (frontmatter `deprecated: true` + `deprecation-note` + body banner) with live-alternative pointers; dead `social-media` skill activations repointed to `content-strategy` / `viral-hooks-content-creator` / `ig-reel-script-writer`:
- Full deprecation: `commands/social/{engage,schedule,viral}.md`, `commands/checklist/social-daily.md`, `commands/content/social.md` (combined banner — also a /content:* casualty, see sweep 4).
- Reference repoint only (command itself still valid): `commands/campaign/calendar.md` (dropped redundant social-media; content-strategy already listed), `commands/skills/select.md` (worked-example -> content-moat), `commands/training/start-0-0.md` (catalog list -> content-moat).
- HANDOVER: `commands/ops/daily.md` is in my EXCLUDE list (other builder owns it) and still references `social-media` — not touched.

## 4. /content:* DEPRECATION (E-04)

In-file deprecation banner (frontmatter + body) added to all 10 deprecated `/content:*` files (`ads, blog, cro, editing, enhance, fast, good, landing, sales-letter, social`), each pointing at its `/copy:*` (or skill) replacement. `commands/content/email.md` left LIVE (0 markers).

## 5. SKILLS REGISTRY (E-15)

- Canonical = `.claude/rules/skills-registry.json` (132 skills). Repointed the 4 active docs at it: `.claude/workflows/orchestration-protocol.md:154`, `.claude/rules/_index.md:71`, `docs/system-rules/details/skills-catalog.md:8`, `commands/skills/select.md:17,38`.
- `skills/knowledge-hygiene/scripts/registry_drift.py` search order now tries `.claude/rules/` first.
- README-MOVED markers beside both stale copies (`skills/README-MOVED.md` written; `.claude/skills/README-MOVED.md` already existed from another builder — left as-is, it covers the same intent).

## 6. HARDCODED PATHS (E-09, M4.2)

Repo-internal `/Users/jerel/...Marketing` absolutes -> `MARKETING_REPO_ROOT` env then script-relative discovery; cross-repo `~/.claude` + `~/AI workflows` -> `os.path.expanduser` / `Path.home()`:
- `scripts/ad-images/render.py:45` (CLAIM_GATE — M1 work preserved), `scripts/build_copyos_reviewers.py:29`, `scripts/phase4_acceptance_test.py:22`, `scripts/link-skills-watch.sh:13`.
- `skills/campaign-runner/scripts/state_manager.py:231-236` (cross-repo dict values -> expanduser), `skills/video-concept-lab/scripts/validate_reference_graph.py:76-119` (~/.claude paths -> `CLAUDE_HOME = Path.home()/".claude"`).
- LEFT (documented exception): `scripts/seed-netlify-blobs.py:57` — `/Users/jerel/.darkbloom/bin/ffmpeg` is inside a docstring comment explaining a broken binary, not a functional path. Per scope (NOT prose).
- All edited scripts compile (`py_compile` / `bash -n`); resolvers runtime-tested to find their targets.

## 7. ICM CITATION (M4.1, A-12/E-10)

`~/.claude/skills/icm/SKILL.md` (backed up to `SKILL.md.bak-260611-m3` first). Line 12 source -> "Van Clief & McDermott, *Interpretable Context Methodology: Folder Structure as Agentic Architecture*."; removed the unverifiable `arXiv:2603.16021v2` from the line-3 description. "In-Context Modeling" expansion eliminated; "Interpretable Context Methodology" consistent throughout.

## 8. LINK-SKILLS (M4.4)

`scripts/link-skills.py` no longer hard-exits without sklearn. Added a pure-stdlib TF-IDF (sublinear tf, smoothed idf) + cosine fallback (`_stdlib_similarity`, using `math`/`collections` only); `HAVE_SKLEARN` branch keeps sklearn when present. Startup line prints the engine. Ran on default python3 (no sklearn) -> `[similarity: stdlib-tfidf]`, exit 0, regenerated `.claude/skill-graph.json`. ferres-corpus (3 neighbours, top ad-library-scraper 0.17) and status-board (5 neighbours, top ad-concept-engine 0.22) now registered. The regen also purged the 13 stale dead-agent `[[x]] (agent, 0.XX)` lines from the auto-gen blocks (closing sweep 1's deferred items).

## 9. ORPHANS (M4.5 + M4.6)

- `brain/jerels brain/...` empty chain (13 nested dirs, 0 files, NOT gitignored) deleted via depth-first empty-dir removal (E-12).
- DCT3 duplicate marker: `_source.md` staged at `_handoffs/staged-m3/neezanizam/` (neezanizam read-only) declaring the client copy canonical (newer, 2026-05-31) vs the older `~/AI workflows/big-angle-spotter/runs/neezanizam_DCT3_260421-1748/` (no deletion). APPLY-NOTE appended (E-08).
- hazecraft metrics-config moved `clients/hazecraft/metrics-config.json` -> `clients/hazecraft/_brand/metrics-config.json` (M4.6). hazecraft is agency-own/idle (not a live client). All sheet writers already search both locations, so no reader breaks; no script hardcoded the old root path.

## 10. CRON (M4.7)

`cron-registry.json` campaign-check entry: added `_note` field "Left disabled on purpose. Re-enable pending operator cadence decision (rebuild M4.7)..." `enabled` stays `false` (prepare-not-enable). JSON still valid.

---

## Acceptance suite (final, all clean)

```
1.  dead agents (non-autogen, non-FP):        0   (want 0)
2.  live /ads:concepts|/ads:avatars:          0   (want 0)
3.  live social-media activations:            0   (want 0)
4.  /content:* deprecated:                    10  (want 10)
4b. content:email live (0 markers):           0   (want 0)
5.  active docs -> rules registry:            4   (want 4)
6.  hardcoded repo /Users/jerel in scripts:   0   (want 0, comments excluded)
7.  ICM bad citation:                         0   (want 0)
8.  link-skills exit on default python3:      0 + ferres/status registered
9.  brain/ chain:                             gone
10. cron note present + still disabled:       yes
```

All edited `.py`/`.sh` compile; all edited `.json` valid.

## Out-of-scope observations (logged, not fixed)

- The "respond in the user's language" boilerplate (`commands/social/*`, `commands/content/*` line ~26) contradicts the standing "always reply in English" rule (`routing-overrides.md`). Not in any sweep's scope — flagging for a future copy-routing pass.
- `commands/ops/daily.md` still references the archived `social-media` skill — EXCLUDED (other builder owns it). Handover.
- The pre-existing `.claude/skills/README-MOVED.md` (another builder) describes `skills/skills-registry.json` as the stale copy while sitting in `.claude/skills/` — slightly mislabeled but the canonical-pointer intent is correct. Left as-is to avoid clobbering.
- Many `/ads:upload`, `/ads:preview`, `/ads:validate`, `/ads:big-angle-spotter`, `/project:profile` references in command bodies point at commands that do not exist on disk — out of this bundle's scope (only concepts/avatars/ab-setup were named). Flagging the broader dead-`/ads:*` set for a follow-up.
