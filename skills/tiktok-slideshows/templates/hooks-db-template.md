# Hooks Database — [PROJECT NAME]

> **Purpose:** Centralized database of TikTok hooks for slideshow batches. Sourced from manual curation, competitor scanning (`competitor_scan.py`), and brainstorming sessions.
> **Hook types:** Question, Shocking claim, Contrarian, Story open, Challenge, Authority, Curiosity gap
> **Power levels:** High (proven outlier 3x+), Medium (above average), Low (untested)

---

## Manually Curated Hooks

Hooks added by the user or during brainstorming sessions.

<!-- Add hooks here in the format below:
### [Hook text]
- **Source:** Manual / brainstorm session YYMMDD
- **Type:** Contrarian | **Power:** Medium
- **Why it works:** [1-line explanation]
- **Adapted for [PROJECT]:** [rewritten for this client's voice]
- **Status:** Available
-->

---

## Scraped Hooks

Hooks added by `competitor_scan.py` (auto-deduped by video ID). Claude categorizes and adapts post-scan.

---

## Used Hooks

Hooks that have been used in a batch. Moved here with batch/post reference. Rest for 2+ batches before reuse.

<!-- Move hooks here when used:
### [Hook text]
- **Used in:** batch-XX, post Y
- **Original source:** @handle | Video ID: xxxxx
- **Status:** Resting until batch-XX
-->

---

## Resting Hooks

Hooks resting for 2+ batches after use. Move back to Scraped/Curated when rest period ends.
