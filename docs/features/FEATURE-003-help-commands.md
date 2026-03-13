---
number: "003"
name: "Help Commands & Guide"
status: "shipped"
proposed_date: "260312"
feasibility_date: "260312"
build_date: "260312"
shipped_date: "260312"
satisfaction: ""
usage_frequency: ""
production_ready: "yes"
---

# FEATURE-003: Help Commands & Guide

## Idea

What: Auto-generated command list (`/help:commands`) and interactive guide (`/help:guide`) that suggests commands based on what user wants to achieve
Why: 84+ commands are hard to remember — need discovery and guidance
Proposed by: Jerel

## Feasibility Assessment

- **Fits current codebase?** Yes — Python script scans existing command files
- **Dependencies:** None
- **Effort estimate:** Small
- **Verdict:** Feasible

## Build Log

| Date | What was done |
|------|--------------|
| 260312 | Created `list_commands.py` — scans .claude/commands/, reads frontmatter, outputs organized list |
| 260312 | Created `/help:commands` — calls Python script, supports keyword search |
| 260312 | Created `/help:guide` — interactive goal→command mapping with full routing table |

### Files Created/Modified

- `.claude/scripts/list_commands.py`
- `.claude/commands/help/commands.md`
- `.claude/commands/help/guide.md`

## Testing

| Test | Result | Notes |
|------|--------|-------|
| Full command list | PASS | 84 commands detected and organized |
| Keyword search (`--search email`) | PASS | 3 results returned correctly |
| Category grouping | PASS | All categories display properly |

## Ship Notes

- **Shipped date:** 260312
- **How to use:** `/help:commands` (list all), `/help:commands email` (search), `/help:guide` (interactive)
- **Known limitations:** None — auto-updates when new commands are added

## Usage & Feedback

| Date | Feedback | Action Taken |
|------|----------|-------------|
| | | |

### Satisfaction
**Rating:**
**Would I miss it if removed?**

### Usage Frequency
**Frequency:**
