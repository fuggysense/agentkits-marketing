---
description: "Create, update, or fix CLAUDE.md files — root or nested (subdirectory)"
argument-hint: "[what changed, 'create', or folder path for nested]"
---

# CLAUDE.md Architect

Manage CLAUDE.md files — root and nested. Auto-detect what's needed and act.
No questions unless genuinely ambiguous — infer most answers from the codebase.

## The Core Principle: Router + Context

CLAUDE.md serves two jobs:

1. **Context**: Vision, principles, tech decisions with WHY, critical rules — the stuff that shapes every agent decision. Lives in the root file.
2. **Router**: Conditional loading — IF doing X, read Y. Keeps context lean without losing depth.

The common mistake is one extreme: stuffing everything inline (bloat) or stripping everything to pointers (no principles). The right balance: root has Vision + principles + critical rules + routing. Domain details live in nested files, rules, and skills.

**Rules encode preferences** (how you like things done).
**Skills encode recipes** (how to do specific things step-by-step).
CLAUDE.md routes to both: "when doing X, read rule Y" / "for task Z, use skill W."

## The Memory Hierarchy

Know where CLAUDE.md sits — don't create content that belongs elsewhere:

| Priority | File | When Loaded | Scope |
|----------|------|-------------|-------|
| 1 | Managed Policy `/etc/claude-code/CLAUDE.md` | Every session | Org-wide |
| 2 | User `~/.claude/CLAUDE.md` | Every session | All projects |
| 3 | User Rules `~/.claude/rules/*.md` | Every session | All projects |
| 4 | Auto Memory `~/.claude/projects/<proj>/memory/MEMORY.md` | First 200 lines | Per project |
| 5 | **Project `./CLAUDE.md`** | Every session | Team (via git) |
| 6 | Project Rules `./.claude/rules/*.md` | Path-conditional | Team (via git) |
| 7 | Local `./CLAUDE.local.md` | Every session | Just you (gitignored) |
| 8 | **Child `./subdir/CLAUDE.md`** | On-demand | Team (via git) |

Most specific wins. Files stack — root always active, subdirectory adds on top.

## Auto-Detect Mode

Read the project root first. Then:

**No file exists** → Create mode. Run the interview. Scan the codebase. Write a complete file.

**File exists but bad** (missing Vision, no WHY, no commands, over 400 lines, generic framework knowledge, no common mistakes) → Remake mode. Tell the user what's wrong. Restructure.

**File exists and good** → Update mode (most common). Figure out what changed: new mistakes, stale info, new decisions, stack changes. Surgical edits only.

**Nested file requested** → See "Nested / Subdirectory Files" below.

## Key Benchmarks

- **Vercel (2025)**: Good CLAUDE.md = 100% task success vs 53% without. Compressed docs index (40KB → 8KB) got BETTER results. 56% skill miss rate — always add explicit skill routing.
- **ETH Zurich (Feb 2026)**: Auto-generated files REDUCE success rate 0.5-3% and increase cost 20%+. NEVER use /init. Each unnecessary instruction adds 14-22% reasoning tokens.
- **HumanLayer (2025)**: ~150-200 instruction capacity total. Bloated files = more content ignored uniformly.

**Sweet spot**: 150-200 lines, past ~300 quality degrades.

## Quality Bar

Every root CLAUDE.md must pass:

- Under 300 lines (ideally 150-200)
- NEVER auto-generated
- No directory listings (agents find files faster on their own)
- No duplication of README/docs
- Vision explains WHY
- Every tech choice says what was rejected
- Every rule has a "because"
- Critical Rules: 3-5 max
- Common Mistakes: real incidents only
- No generic framework knowledge
- Written like amnesia notes
- "Prefer retrieval-led reasoning" present if project has docs

## When Updating

Be surgical — NEVER just append. Every update is also a prune:

1. **Generalize**: Third similar rule? Delete the three specifics, write ONE principle.
2. **Deduplicate**: Overlap? Merge into one stronger entry.
3. **Expire**: No longer true? Delete.
4. **Promote/demote**: 3x regression → Critical Rule. Irrelevant Critical Rule → deleted.

## Nested / Subdirectory Files

Nested files live in folders and stack ON TOP of root. Both active at once.

**Two rules**: (1) NEVER repeat root content. (2) NEVER describe what's discoverable.

**50-100 lines max.** Create when folder has different conventions or agent repeats mistakes there.

## After Any Mode

After writing or editing, re-read the full file and check:
1. **Line count**: Over 300 → cut until under 300.
2. **The one-line test**: For every line — "Would removing this cause Claude to make a mistake?" If no, delete it.

Then sync: `cp CLAUDE.md AGENTS.md` (cross-tool convention for Codex, OpenCode, Cursor).

## Arguments

If the user passed `$ARGUMENTS`, treat it as what changed and go directly to update mode.
