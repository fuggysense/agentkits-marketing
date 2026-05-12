# Session Handoff — 2026-05-12 — Content OS commits + sync.sh hardening

## Where it started

Resumed from prior session's chat-only handoff (the v0.5.2 plan + plans-vault + concept-engine-fork work). Operator picked option 3: commit the session's work + clean. While committing, the husky `commit-msg` hook was found broken (unquoted `$1` choked on the spaced parent path "Jerel's brain"). Hook fixed in main repo, mirrored into the worktree's tracked copy, and shipped.

After commits landed, operator set `/goal` to also run an adversarial architecture review and apply fixes. Two reviewer agents returned 19 findings. The 3 critical + 4 high-severity fixes that were localized + testable were applied, smoke-tested, and committed.

## What shipped (6 commits, branch `worktree-content-system-plan`)

| SHA       | Type | Summary |
|-----------|------|---------|
| `bd5c964` | docs | v0.5.2 content OS plan (1,630 lines) + Michelle onboarding deck (265 lines) |
| `34f816d` | feat | plans-vault foundation: `sync.sh`, `bootstrap.sh`, `_admin/`, `_template/`, README |
| `be10eb0` | feat | /hooks command family — generate, select, analyze (still includes transitional scripts/hook-prompts/) |
| `04f52d4` | feat | concept engine fork — /content:concepts + /ads:concepts + 327-line fork visualization |
| `c06bbb1` | fix  | quote `$1` in husky commit-msg hook (unblocks worktree commits on spaced paths) |
| `6bcde46` | fix  | harden sync.sh + delete dead scripts/hook-prompts/ (157 insertions, 414 deletions) |

## Adversarial review findings — what got fixed, what's deferred

### Applied (commit `6bcde46`)
- **adv-002 (critical)** — refuse to mount with empty slug on first publish (prior path could loop infinitely if publish.sh stdout format drifted)
- **adv-003 (critical)** — validate `_state.json` is parseable JSON at startup; clear recovery instructions if corrupt
- **adv-001 (high)** — soft single-flight lock (PID file + 10-min staleness) on write paths; macOS has no `flock(1)`, so it's a guard not a kernel lock
- **adv-004 (high)** — reserved client-name list (admin, api, _admin, _template, index, root) + lowercase-alnum-hyphen regex on every entry point
- **adv-005 (high)** — all jq filters now use `--arg`, all curl URL params run through urlenc, sed uses `|` delimiter
- **adv-006 (high)** — `api_get` wrapper checks HTTP status; mount POST uses `--fail`
- **M1 (high)** — deleted `scripts/hook-prompts/` (drifted duplicate of `commands/hooks/`)

### Deferred (medium / backlog)
- **adv-007** — smoke test now reports non-2xx count but doesn't retry-until-2xx (CDN propagation can take 5-30s; current behavior surfaces the issue rather than silently passing, which is good enough for now)
- **adv-008** — `/hooks:generate` trusts file existence; can't distinguish stub `buyer-profile.md` from real one. Needs a `status:` field in the YAML/frontmatter
- **adv-009** — `docs/content-system-plan.html` has 3 places where Stage 06 is described as manual vs cron-driven; reconcile in v0.5.3
- **adv-010 / M4** — `/ads:concepts` claims to compose `unique-mechanism-problem`, `unique-mechanism-solution`, `persuasive-premise`, `problem-promise`, `usp-generator` — none of these are in `skills-catalog.md`. The `ad-concept-engine` skill referenced in `routing-table.md` doesn't exist either. Either build the skills or trim the composition.
- **M2** — `/content:concepts` and `/ads:concepts` are 90% structural twins. Merge under one `commands/concepts.md` with `--mode=organic|ads`
- **M3** — once M2 lands, collapse `docs/concept-engine-fork.html` to a 40-line ADR
- **M5** — add `./sync.sh --doctor` that prints which of the 8 setup steps are done vs missing
- **Reconciliation** — no `./sync.sh --reconcile` that diffs remote `/domains` against local `_state.json`. Drift is detectable but only by hand

## Smoke tests run

| Test | Result |
|------|--------|
| Bash `-n` syntax | ✓ pass |
| Reserved name `admin` | ✓ rejected with helpful message |
| Uppercase `BadName` | ✓ rejected |
| Leading hyphen `-foo` | ✓ rejected |
| Shell metachar `foo;rm` | ✓ rejected |
| Double hyphen `foo--bar` | ✓ rejected |
| Trailing hyphen `foo-` | ✓ rejected |
| Corrupt `_state.json` | ✓ halts with recovery instructions, doesn't crash subcommands |
| `--list` on valid state | ✓ shows michelle-koh + 3 live mounts on plans.genflos.com |
| `urlenc` helper | ✓ encodes spaces, preserves dots/hyphens |

Lock contention not live-tested (would need a real cmd_sync run). Logic verified by syntax check + visual review.

## Running state

- **Branch:** `worktree-content-system-plan`, 6 commits ahead of `8bded3a`. Not pushed to origin.
- **Working tree:** clean.
- **Worktree path:** `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/.claude/worktrees/content-system-plan`
- **Tooling note:** `@commitlint/cli@20.5.3` + `@commitlint/config-conventional` got installed at the main repo's `node_modules/` (transient, `--no-save`, doesn't touch `package-lock.json`). Required because husky's commit-msg hook calls them via `npx --no`. Future operators on a fresh checkout will need `npm install` once.
- **Husky hook:** fixed in both main and worktree. Tracked at `.husky/commit-msg`.
- **plans-vault live state:** `~/plans-vault/_state.json` has 1 client (michelle-koh, slug `earthy-opera-7wp3`). 3 mounts on plans.genflos.com: `/`, `/admin`, `/michelle-koh`.

## Verification — how to confirm things still work

```bash
# From the worktree:
cd "/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/.claude/worktrees/content-system-plan"
git log --oneline -7                                 # see 6 new commits on top
bash -n scripts/plans-vault/sync.sh                  # syntax OK

# Live infra:
~/plans-vault/sync.sh --list                         # should print michelle-koh + 3 mounts
curl -sSI https://plans.genflos.com/michelle-koh/plan   # should 200
curl -sS https://plans.genflos.com/admin/manifest.json | jq '(.clients|length), .generated_at'

# Validation gates (read-only, fast):
~/plans-vault/sync.sh --new admin    # should refuse "Reserved client name"
~/plans-vault/sync.sh --new BadName  # should refuse "Invalid client name"
```

## Pick up here (priority-ordered)

1. **Michelle sign-off on v0.5.2 plan** (highest leverage, lowest effort). 3 open decisions block Phase 1a:
   - Cadence: 3 vs 4 posts/week
   - BOFU CTA destination (DM keyword "AUDIT" → T1 PDF, or direct call booking)
   - Plan tone (technical operator-facing or warmer client-facing in shared doc)
2. **Skills-catalog drift** — `/ads:concepts` references 5 skills that don't exist (`unique-mechanism-problem`, `unique-mechanism-solution`, `persuasive-premise`, `problem-promise`, `usp-generator`) plus `ad-concept-engine`. Decide: build the skills, or trim the composition + remove from `routing-table.md`. This is a 30-min cleanup + a real call about whether paid-side concept generation needs its own skill or can stay composed.
3. **Validate /content:concepts on propwise-sg** — original "Pick up here" from prior handoff. Extract `buyer-profile.md` from `icp.md` Persona A (Jing Ting & Wei Liang), then run `/content:concepts "MOP timing for HDB upgraders" --client propwise-sg` and eyeball whether each concept has a TENSION (felt-but-unspoken) + a BELIEF flipped.
4. **Backlog from review** — adv-007, adv-008, adv-009, M2, M3, M5 (see Deferred above)
5. **Push to origin** — branch is local-only. `git push -u origin worktree-content-system-plan` when ready

## Open questions

- Should `worktree-content-system-plan` merge to main now, or wait for Michelle's sign-off on v0.5.2 first? (Merging now ships the plan; sign-off is operator-facing not code-facing, so merging shouldn't block.)
- The transient `node_modules/@commitlint/*` install in main repo — should `npm install` be added to bootstrap.sh or README to prevent the next operator hitting the same hook failure?
- ad-concept-engine skill: build it, or accept that `/ads:concepts` composes 6 existing skills as a permanent design?

## Files touched this session

- `docs/content-system-plan.html` — 1,630 lines, v0.5.2 master spec
- `docs/michelle-onboarding.html` — 265 lines, client-facing
- `docs/concept-engine-fork.html` — 327 lines, fork visualization
- `scripts/plans-vault/{sync.sh,bootstrap.sh,README.md,_admin/,_template/}` — full publishing stack
- `commands/hooks/{README,generate,select,analyze}.md` — hook command family
- `commands/content/concepts.md` — organic concept engine
- `commands/ads/concepts.md` — paid concept engine
- `.husky/commit-msg` — quote fix
- `scripts/hook-prompts/` — deleted (was drifted duplicate)
- `docs/handoffs/2026-05-12-content-os-commits-and-hardening.md` — this file
