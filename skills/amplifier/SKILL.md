---
name: amplifier
version: "2.0.0"
updated: "260313"
category: quality-assurance
description: Enhances and updates EXISTING agents and skills. Scans for conflicts, detects similarity overlaps, analyzes gaps, suggests merges, and tracks attribution. Runs prompt-contracts for structured improvement specs, timestamps versions, and tracks contributors. Use when you need to improve, audit, or evolve an existing agent or skill — not create new ones (use meta-builder for that).
related_skills:
  - prompt-contracts
  - verification-loops
  - meta-builder
---

# Agent & Skill Amplifier

## Overview

The Amplifier skill enhances existing agents and skills through systematic analysis, conflict detection, and improvement tracking. While meta-builder creates new artifacts, amplifier makes existing ones better.

**Think of it like this:** Meta-builder is the architect that designs new rooms. Amplifier is the renovation contractor that makes existing rooms work better — fixing leaks, upgrading wiring, and making sure doors don't open into each other.

## Decision Logic: Amplify vs Build New

| Signal | Action |
|--------|--------|
| Existing artifact has gaps, stale TODOs, or unintegrated learnings | **Amplify** |
| Two artifacts overlap heavily (>80% similarity) | **Amplify** (merge them) |
| Triggers conflict across skills | **Amplify** (resolve conflicts) |
| No artifact exists for the need | **Build New** (use meta-builder) |
| Gap is so large it needs a whole new workflow | **Build New** (use meta-builder) |

## Workflow

### Phase 1: TARGET

**Goal:** Identify what to amplify.

**Accept:**
- A skill name (e.g., `copywriting`)
- An agent name (e.g., `attraction-specialist`)
- `scan all` — run full conflict + similarity scan

**Steps:**
1. Validate the target exists in `skills/` or `agents/`
2. If `scan all`:
   - Run `scripts/scan_conflicts.py` to find trigger overlaps and capability collisions
   - Run `scripts/scan_similarity.py` to find content overlaps
   - Present ranked list of items needing attention (highest severity first)
   - Ask user which to amplify first
3. If specific target: proceed to Phase 2

### Phase 2: ANALYZE

**Goal:** Understand current state — strengths and gaps.

**Steps:**
1. Run `scripts/analyze_target.py <path>` to get:
   - Completeness score (% of canonical sections present)
   - Missing sections compared to patterns
   - Stale TODO placeholders
   - Unintegrated learnings (entries in learnings.md not reflected in main file)
   - Registry drift (frontmatter vs skills-registry.json mismatch)
2. Run `scripts/scan_conflicts.py --target <name>` to get:
   - Trigger overlaps with other skills
   - Capability collisions with other agents
   - Naming proximity issues
3. Present report:
   ```
   ## Analysis: {name}

   **Completeness:** X/10
   **Conflicts:** N found
   **Learnings to integrate:** N entries

   ### Strengths
   - ...

   ### Gaps
   - ...
   ```

### Phase 2.5: CONTRACT

**Goal:** Generate a prompt contract for the amplification work — structured spec of what "improved" means.

**Steps:**
1. Decide which contract mode fits:
   - **Prompt Contract** (default) — when building new improvements from gap analysis
   - **Reverse Prompt** — when the user provides a reference ("make it more like this one", "this agent works great, bring others up to its level")
2. Auto-generate a contract using the `prompt-contracts` skill:
   ```
   GOAL: [What the amplified artifact should achieve — measurable improvement]
   CONSTRAINTS: [Don't break existing triggers, don't duplicate other artifacts]
   FORMAT: [Updated SKILL.md/agent.md with version bump, timestamp, contributor]
   FAILURE: [Gaps still present, new conflicts introduced, learnings not integrated]
   ```
3. Present contract to user: "Here's the improvement contract — adjust anything before I proceed."
4. User approves → proceed to Phase 3
5. User says "skip" → proceed without contract (note: contract skipped in attribution log)

**Why this matters:** Without a contract, amplification drifts into "technically improved" but doesn't hit the actual gap. The contract locks in what "better" means before touching the file.

### Phase 3: PROPOSE

**Goal:** Prioritized list of changes with before/after previews.

**Priority levels:**
- **P0 (Critical):** Conflicts with other artifacts, missing required sections, broken dependencies
- **P1 (High):** Unintegrated learnings, missing skill/agent mappings in registry
- **P2 (Medium):** Trigger expansion, related_skills updates, version bump needed
- **P3 (Nice-to-have):** Better examples, richer edge cases, improved descriptions

**Each proposal includes:**
- What: The specific change
- Why: The rationale
- Before/After: Preview of the change
- Source: Where the improvement idea came from (attribution)

**HITL GATE:** Present all proposals to user. Only proceed with approved changes.

### Phase 4: EXECUTE

**Goal:** Apply approved changes cleanly.

**Steps:**
1. Edit the target file with approved changes
2. If triggers or dependencies changed:
   - Run `scripts/update_registry.py <skill-name>` to sync skills-registry.json
3. If prerequisites changed:
   - Update `.claude/skills/dependency-graph.md`
4. **Bump version + timestamp in frontmatter:**
   - Patch (x.x.+1) for minor improvements
   - Minor (x.+1.0) for new sections or significant capability changes
   - Add/update `updated: "YYMMDD"` field (use `bash -c 'date +%y%m%d'` for today's date)
   - Example frontmatter after amplification:
     ```yaml
     version: "1.1.0"
     updated: "260313"
     contributors:
       - "Jerel (260313) — added objection handling section"
       - "Claude (260310) — integrated meta-ads learnings"
     ```
5. **Append contributor:**
   - If user mentioned who requested/contributed the change, add them
   - If NOT mentioned, ask: "Who should I credit for this improvement? (name or 'me')"
   - Format: `"Name (YYMMDD) — brief description of contribution"`
   - Add to `contributors:` list in frontmatter (create field if missing)
   - Never overwrite existing contributors — always append
6. Validate with meta-builder's `quick_validate.py`:
   ```bash
   python skills/meta-builder/scripts/quick_validate.py <skill-path>
   ```
7. Log attribution:
   ```bash
   python skills/amplifier/scripts/log_attribution.py <target-path> \
     --source "..." --type "..." --summary "..."
   ```
8. **Append changelog entry** to `docs/changelog.md` under today's date (`## YYMMDD`), section `### Amplified`:
   - **What:** `**\`{name}\`** {type} — one-line summary`
   - **Inspired by:** source name + type (repo/person/article/campaign-result/internal-review/competitor-analysis)
   - **Contributor:** who drove the change (ask if not clear)
9. **Verify against contract** (if Phase 2.5 was not skipped):
   - Run through each FAILURE condition from the contract
   - Present contract verification status (ALL PASS / N FAILURES)
   - If any FAILURE triggered, fix before marking complete

### Phase 5: VERIFY & IMPROVE

**Goal:** Confirm changes are clean, no new conflicts, and the target is genuinely better.

**Steps:**
1. Show diff of all changes made
2. Re-run `scripts/scan_conflicts.py` to confirm no new conflicts
3. **Contract check** (if Phase 2.5 was used):
   - Walk through each FAILURE condition
   - Show pass/fail status for each
   - If any fail, loop back to Phase 4 to fix before completing
4. **Improvement pass** — read the updated artifact end-to-end and check:
   - Does the skill/agent actually teach something better now? (not just more words)
   - Are there stale examples that should be refreshed?
   - Are learnings.md entries integrated into the main body (not just listed)?
   - Does it connect well with related skills (cross-references, handoffs)?
   - If any quick wins spotted during this read, apply them (P3 level, no HITL gate needed)
5. Update `skills/amplifier/learnings.md` with patterns discovered during this amplification
6. End with: *"Use this updated [agent/skill], then tell me what to improve."*

## Commands

| Command | Action |
|---------|--------|
| `/amplify:skill` | Enhance an existing skill — runs full 5-phase workflow |
| `/amplify:agent` | Enhance an existing agent — runs full 5-phase workflow |
| `/amplify:scan` | Scan all skills and agents for conflicts and overlaps |
| `/amplify:merge` | Suggest merges for tightly coupled artifacts |

## Resources

### scripts/
- `scan_conflicts.py` — Detects trigger overlaps, capability collisions, naming proximity
- `scan_similarity.py` — TF-IDF cosine similarity scanner (pure Python, no deps)
- `analyze_target.py` — Gap analysis for a single skill or agent
- `suggest_merge.py` — Merge recommendations for tightly coupled pairs
- `update_registry.py` — Syncs skills-registry.json after changes
- `log_attribution.py` — Records origin/inspiration for every amplification

### references/
- `amplification-patterns.md` — Catalog of enhancement patterns
- `merge-decision-tree.md` — When to merge vs. keep separate

## Integration with Meta-Builder

| Concern | Meta-Builder | Amplifier |
|---------|-------------|-----------|
| Create new artifacts | Yes | No |
| Enhance existing | No | Yes |
| Validate structure | `quick_validate.py` | `analyze_target.py` (deeper) + calls quick_validate |
| Register | `register.py` (new entry) | `update_registry.py` (update entry) |
| Conflict detection | Duplicate name only | Triggers, capabilities, naming, similarity |

If amplifier finds a gap so large it needs a new artifact, it recommends using meta-builder instead.

## Self-Annealing

After each amplification:
1. Record what worked in `learnings.md`
2. If a pattern repeats 3+ times, add it to `references/amplification-patterns.md`
3. If a merge suggestion is accepted, update `references/merge-decision-tree.md` with the reasoning
