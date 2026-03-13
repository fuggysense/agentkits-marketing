# Amplification Patterns

> Catalog of proven enhancement patterns for skills and agents.

## Pattern 1: Learnings Integration

**When:** Skill/agent has `learnings.md` with confirmed patterns not reflected in main file.
**How:** Extract confirmed patterns, add them to the relevant section (workflow steps, edge cases, quality checklist).
**Example:** If learnings.md says "always check mobile viewport for CRO audits" and the CRO skill doesn't mention mobile — add it to the workflow.

## Pattern 2: Trigger Expansion

**When:** Users frequently describe a task in words not matching existing triggers.
**How:** Add natural-language variations to the skill's triggers in skills-registry.json.
**Example:** Users say "make my page convert better" but triggers only include "CRO" and "conversion rate optimization" — add "improve conversions", "convert better".

## Pattern 3: Cross-Skill Wiring

**When:** A skill frequently needs another skill's output but doesn't reference it.
**How:** Add to `relatedSkills` in registry, add a "Prerequisites" or "Works With" note in SKILL.md.
**Example:** `email-sequence` skill doesn't mention `copywriting` patterns for subject lines — wire them together.

## Pattern 4: Agent Capability Sharpening

**When:** Two agents have overlapping capabilities causing confusion about who handles what.
**How:** Clarify boundaries in both agents, add "When NOT to use this agent" section, update skill integrations.
**Example:** `attraction-specialist` and `seo-specialist` both handle SEO — clarify that attraction-specialist handles strategy, seo-specialist handles technical review.

## Pattern 5: Reference Enrichment

**When:** A skill has `hasReferences: false` but would benefit from reference material.
**How:** Create targeted reference docs with frameworks, benchmarks, or examples.
**Example:** `page-cro` has no references — add a reference doc with conversion benchmarks by industry.

## Pattern 6: Quality Checklist Addition

**When:** Agent produces inconsistent output quality.
**How:** Add or expand the Quality Checklist section with specific, checkable criteria.
**Example:** Copywriter agent sometimes forgets CTAs — add "Every piece includes at least one CTA" to checklist.

## Pattern 7: Edge Case Documentation

**When:** Users hit scenarios the skill/agent doesn't handle well.
**How:** Add an "Edge Cases" section documenting the scenario and recommended approach.
**Example:** Pricing strategy skill doesn't cover "what if the product is free with paid add-ons" — document it.

## Pattern 8: Version Bump + Changelog

**When:** Multiple small improvements accumulate.
**How:** Bump version (patch for fixes, minor for features), log changes in attribution.md.
**Versioning rules:**
- x.x.+1 (patch): Bug fixes, typo corrections, minor wording improvements
- x.+1.0 (minor): New sections, new capabilities, significant workflow changes
- +1.0.0 (major): Complete rewrite, breaking changes to workflow

## Pattern 9: Registry Sync

**When:** Skill frontmatter and registry entry have drifted apart.
**How:** Run `update_registry.py` to sync, then manually verify triggers and agents arrays.
**Common drift:** Description updated in SKILL.md but not in registry, or new references added without updating `hasReferences`.

## Pattern 10: Merge Consolidation

**When:** Two skills have >80% similarity and serve the same user intent.
**How:** Pick the stronger one as the base, fold in unique content from the other, archive the weaker one.
**Decision factors:** Which has more content? Which has the better name/triggers? Which has more usage?

## Pattern 11: Cross-Awareness Wiring

**When:** Agent is missing "Agent Collaboration" or "When NOT to Use This Agent" sections.
**How:** Add both sections using orchestration-protocol.md handoff table and funnel routing as source data.
**Agent Collaboration table:** Lists agents this one works with, the relationship direction, and when handoffs happen.
**When NOT to Use table:** Lists common misrouted tasks and the correct agent to use instead.
**Why it matters:** Without cross-awareness, agents get invoked for wrong tasks, produce suboptimal outputs, and miss opportunities to hand off to specialists. These sections are now mandatory for all agents (enforced by `analyze_target.py`).
