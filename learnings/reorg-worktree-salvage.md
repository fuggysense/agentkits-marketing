# Learning: never delete a worktree on an audit's say-so

**Date:** 2026-06-08 · **Context:** NeezaNizam ICM reorg execution

## What happened

The read-only audit (and the cold-review pass that revised the migration map) both flagged the gitignored worktree `clients/neezanizam/.claude/worktrees/mystifying-wu-249e7d/` (1,061 files) as "pure noise, referenced by nothing — DELETE before migrating." During execution, verify-before-delete found the opposite:

- It was a **git-registered worktree**, not an orphan clone (needed `git worktree remove`, not `rm -rf`).
- **Two real files referenced its path** (`_brand/learnings.md`, `firsttime-letter-260512/v4-revision-brief.md`); the brief literally warned the V4 letter path would break if the worktree were cleaned up.
- Its working dir held the **only copy** of 11 gitignored client deliverables (the v2→v4 first-time-buyer sales-letter lineage + 3 reverse-avatar docs) plus an untracked global skill. None were in main; none were in the first backup (which `--exclude`d the worktree path).

Blind deletion would have permanently destroyed a real sales-letter deliverable — no git history (gitignored), not in the backup.

## Why the audit missed it

The audit treated the worktree as a black-box file-count distortion ("a full repo clone, delete it"). Neither the audit nor the cold-reviewer looked *inside* the worktree's working dir for gitignored client files, because their scope was "is every file in the MAIN tree accounted for" — the worktree was out of scope by construction. Gitignored deliverables inside a gitignored worktree are invisible to both git and a main-tree audit.

## The rule (applies to every reorg / cleanup from now)

Before deleting ANY worktree or "stray clone":
1. `git -C <repo> worktree list` — is it registered? (use `git worktree remove`, never `rm -rf` on a registered worktree)
2. `grep -rIl "<worktree-name>"` outside the worktree — who references its path?
3. `diff -rq <worktree>/<client-tree> <main>/<client-tree>` — enumerate files UNIQUE to the worktree (these are the salvage set; gitignored client files won't show in git).
4. Check the worktree's working tree for untracked dirs (`git status --porcelain`) — new skills/work-in-progress.
5. Salvage uniques + re-take the backup INCLUDING them, THEN remove.

## Backup gotcha

`--exclude='.../.claude/worktrees'` in the backup tar is correct for excluding the 1,061-file clone bloat — BUT it also excludes any salvageable gitignored deliverables living inside. Salvage FIRST (copy uniques into the main tree), THEN take the authoritative backup so the rescued files are captured.

Related: [[reference_client_file_map]] · `docs/neezanizam-reorg-migration-map.md` ADDENDUM
