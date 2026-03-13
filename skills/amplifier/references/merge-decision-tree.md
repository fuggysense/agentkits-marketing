# Merge Decision Tree

> When to merge two artifacts vs. keep them separate.

## Quick Decision

```
Two artifacts seem similar. Should you merge?

1. Are they in the SAME category?
   ├── NO → Almost certainly KEEP SEPARATE
   └── YES → Continue...

2. Do they share >50% of their triggers?
   ├── NO → Probably KEEP SEPARATE (different user intents)
   └── YES → Continue...

3. Is one a strict subset of the other?
   ├── YES → MERGE (absorb the subset into the larger one)
   └── NO → Continue...

4. Do they have different difficulty levels?
   ├── YES → KEEP SEPARATE (serve different skill levels)
   └── NO → Continue...

5. Do both have >20 lines of unique, valuable content?
   ├── YES → KEEP SEPARATE but add cross-references
   └── NO → MERGE (one is likely too thin to stand alone)
```

## Merge Scores (from suggest_merge.py)

| Score | Recommendation | Action |
|-------|---------------|--------|
| > 2 | MERGE | Combine into one artifact |
| 1-2 | REVIEW | Human judgment needed |
| < 1 | KEEP SEPARATE | Add cross-references instead |

## How to Execute a Merge

1. **Pick the base:** The artifact with more content, better name, or more registry connections
2. **Inventory unique content:** List what the absorbed artifact has that the base doesn't
3. **Integrate:** Add unique sections, triggers, and examples to the base
4. **Update registry:**
   - Combine triggers (deduplicate)
   - Combine agents arrays
   - Update relatedSkills
   - Bump version (minor)
5. **Update dependency graph:** Redirect anything that depended on the absorbed artifact
6. **Archive (don't delete):** Rename absorbed artifact with `-archived` suffix, add redirect note
7. **Log attribution:** Record the merge decision and rationale

## When NOT to Merge (Even if Scores Say So)

- **Different audiences:** Even if content overlaps, if skill A is for beginners and skill B for advanced users, keep them separate
- **Different output formats:** If they produce fundamentally different deliverables
- **One is a prerequisite of the other:** Parent-child relationships should stay as separate skills
- **Active campaign dependency:** If a running campaign references the skill by name, don't merge mid-campaign

## Merge History

> Record merges here for reference.

(none yet — populated through use)
