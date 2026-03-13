# Reference Repo Sync Guide

## What This Is

We maintain bookmarks ("remotes") to other GitHub repos that have useful skills, agents, or workflows. Once per week, we check if they've published anything new and cherry-pick what's useful into our kit.

**We never merge their branches.** We just peek at their files and copy what we want.

## Active Remotes

| Remote | Repo | What It Has | Status |
|--------|------|-------------|--------|
| `upstream` | aitytech/agentkits-marketing | Our main fork source — marketing kit updates | **Sync every 3 days** (merge) |
| `superpowers` | obra/superpowers | Dev workflow skills — planning, execution, verification, parallel agents | **Weekly scan** (cherry-pick) |
| `claude-ads` | AgriciDaniel/claude-ads | Ad auditing — 6 agents, 12 skills, 186 checks across Google/Meta/LinkedIn/TikTok/YouTube/Microsoft | **Weekly scan** (cherry-pick) |

## How to Add a New Repo

```bash
git remote add [short-name] https://github.com/[owner]/[repo].git
```

Then add a row to the table above.

## Weekly Sync Protocol

Run this once per week (Claude does this automatically per Open Threads in CLAUDE.md):

### Step 1: Fetch All Reference Remotes

```bash
git fetch superpowers
git fetch claude-ads
# Add more as needed
```

### Step 2: Check What's New

```bash
# For each remote, check recent commits
git log superpowers/main --oneline -10 --since="1 week ago"
git log claude-ads/main --oneline -10 --since="1 week ago"
```

### Step 3: Review Interesting Changes

```bash
# View a specific file from their repo (doesn't change your files)
git show superpowers/main:skills/writing-plans/SKILL.md
git show claude-ads/main:skills/ads-audit/SKILL.md
```

### Step 4: Cherry-Pick What's Useful

```bash
# Copy a file into your structure
git show claude-ads/main:agents/audit-google.md > agents/audit-google.md
# Then edit to match our conventions (add Language Directive, Context Loading, etc.)
```

### Step 5: Summarize for Jerel

Present findings as:

```
## Weekly Repo Scan — [date]

### superpowers (obra/superpowers)
- [X new commits since last check]
- Notable: [brief description]
- **Action:** [Skip / Cherry-pick X / Worth reviewing]

### claude-ads (AgriciDaniel/claude-ads)
- [X new commits since last check]
- Notable: [brief description]
- **Action:** [Skip / Cherry-pick X / Worth reviewing]
```

Jerel decides what to pull in. Claude adapts and integrates.

## Conflict Prevention Rules

1. **Never run `git merge [remote]/main`** on reference repos — only on `upstream`
2. **Never run `git pull [remote]`** — use `git fetch` + `git show` to read files
3. **Always copy files into our structure** — don't symlink or reference their paths
4. **Adapt copied files** to match our conventions (frontmatter format, Language Directive, etc.)
5. **Track what we've pulled** in the Sync Log below

## Sync Log

| Date | Remote | What We Pulled | Adapted To |
|------|--------|---------------|------------|
| (none yet) | — | — | — |
