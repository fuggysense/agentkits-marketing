---
name: knowledge-hygiene
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: specialized
difficulty: beginner
description: "Anti-decay system that detects stale docs, unintegrated learnings, and registry drift. Surfaces hygiene reports inside existing ops commands — not as standalone maintenance. Updates happen as byproducts of doing the work."
triggers:
  - hygiene
  - stale docs
  - knowledge decay
  - freshness audit
  - learnings check
  - registry drift
prerequisites: []
related_skills:
  - amplifier
  - analytics-usage
agents:
  - docs-manager
mcp_integrations: {}
success_metrics:
  - docs_freshness_rate
  - learnings_integration_rate
  - registry_accuracy_rate
output_schema: null
---

## Graph Links
- **Feeds into:** (meta-skill — maintains the system)
- **Draws from:** (all skills — audit target)
- **Used by agents:** (system-level)
- **Related:** [[analytics-usage]]

# Knowledge Hygiene

You are an anti-decay system. You detect knowledge rot and surface it during work the user is already doing — never as a separate maintenance step.

## Core Philosophy

"If updating requires you to remember to run it, it'll work for 2-3 weeks while you're motivated and then quietly stop."

This skill makes updates automatic byproducts of actual work:
1. **Passive decay detection** wired into `/ops:weekly` and `/ops:monthly` — no separate "remember to audit" step
2. **Active learnings capture** baked into session end protocol — logging what you learned IS completing the task

---

## 3 Checks

### 1. Freshness Audit
Scan `docs/*.md` files, compare last-modified date against expected update frequency from `documentation-management.md`.

```bash
python3 skills/knowledge-hygiene/scripts/freshness_audit.py --summary
```

Thresholds:
- Weekly docs → stale after 10 days
- Quarterly docs → stale after 100 days
- "As needed" / "After X" docs → stale after 90 days

### 2. Learnings Integration Check
For each `learnings.md`, count entries under "Confirmed Patterns" that haven't been integrated into the parent SKILL.md.

```bash
python3 skills/knowledge-hygiene/scripts/learnings_check.py --summary
```

Uses amplifier's `analyze_target.py` logic for unintegrated learnings detection.

### 3. Registry Drift Detection
Validate `skills-registry.json` entries against actual SKILL.md frontmatter.

```bash
python3 skills/knowledge-hygiene/scripts/registry_drift.py --summary
```

Checks: version, description, triggers, category mismatches. Also flags deprecated terminology from MEMORY.md corrections.

### 4. Corrections Pruning Check
Audit `corrections.md` files across all skills for hygiene.

Thresholds:
- Entries >20 per skill → flag for triage (too many unprocessed corrections)
- Entries >60 days old not promoted → suggest promote or discard
- 3+ similar entries → auto-suggest consolidation into that skill's `learnings.md`

Surface in `/ops:monthly` report alongside other hygiene checks.

---

## Where It Wires In

### `/ops:weekly` — Step 5
After "Next Week Planning", show 3-5 line hygiene summary. If clean: `**Hygiene:** All clean.`

### `/ops:monthly` — Full Report
All 3 checks with details. Registry drift and amplifier targets surfaced here.

### Session End Protocol — Step 1.5
If any skill/agent was used this session and produced a confirmed insight, append to that skill's `learnings.md`. This is not optional maintenance — it's part of completing the work.

### Campaign Completion
When campaign-runner marks a campaign "completed", auto-trigger mini hygiene check on skills/agents used in that campaign. Surface which learnings files should be updated.

---

## Output Format

### Summary (for weekly)
```
**Hygiene:** 2 docs overdue (campaign-playbooks 45d, channel-strategies 32d). 3 skills have unintegrated learnings (copywriting: 4, seo-mastery: 2, paid-advertising: 1). Registry clean.
```

### Full Report (for monthly)
```markdown
## Knowledge Hygiene Report

### Freshness Audit
| Document | Last Modified | Expected | Days Overdue |
|----------|--------------|----------|--------------|
| campaign-playbooks.md | 2026-01-28 | After each campaign | 45 |

### Learnings Integration
| Skill | Total Learnings | Unintegrated | Sample |
|-------|----------------|--------------|--------|
| copywriting | 11 | 4 | "So What? Chain..." |

### Registry Drift
| Skill | Field | Registry | Actual |
|-------|-------|----------|--------|
| (none) | — | — | — |
```

### Action Suggestions
- "Run `/amplify:skill copywriting` to integrate learnings"
- "Update campaign-playbooks.md with recent campaign results"

---

## Commands

This skill has no standalone command. It runs as part of:
- `/ops:weekly` (Step 5)
- `/ops:monthly` (Hygiene Report section)
- Session end protocol (Step 1.5)
- Campaign completion triggers

---

## Self-Annealing

When a hygiene check produces a false positive (flags something as stale that's actually current):
1. Fix the threshold or detection logic in the relevant script
2. Add the edge case to this skill's `learnings.md`
3. The check gets smarter over time
