# Attribution — Borrowed Code + Framework Sources

## Python helpers borrowed from external repos

### zubair-trabzada/ai-ads-claude (MIT License)

**Repo:** https://github.com/zubair-trabzada/ai-ads-claude
**File:** `scripts/generate_ads_pdf.py`
**License:** MIT

**What we borrowed (lifted patterns, rewrote specifics):**
- Color palette structure + hex values (COLORS dict)
- `score_color()` pattern → rewrote as `band_color()` for RYG system
- `create_bar_chart()` function → kept nearly verbatim, retargeted to 1-5 scale
- `standard_table_style()` helper → kept as-is
- `get_styles()` paragraph style dict → adapted, added new styles (constraint_bold, dollar_callout, dream_quote)
- 6-page layout skeleton (PageBreak structure) → inspired ours

**What we explicitly did NOT borrow:**
- `draw_score_gauge()` — rejected after Hormozi consultation (consultant theater)
- `score_grade()` letter grade (A+ → F) — rejected for same reason
- Composite 0-100 Health Score math — rejected
- Zubair's persona card layout — ours is Hormozi-framework-aligned instead
- Zubair's hardcoded demo data — our script is 100% data-driven from input JSON

**MIT License acknowledgment:**
Copyright (c) 2026 zubair-trabzada. Permission is granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction. The original repo retains its MIT terms.

---

## Framework sources

### Alex Hormozi — $100M Offers + $100M Leads

Consulted via NotebookLM notebook "Hormozi AI" on 2026-04-11 during the planning phase of this skill. Five questions asked and answered:

1. Value equation structure for paid onboarding deliverable
2. Reveal vs withhold balance (declarative vs procedural)
3. Composite score legitimacy (0-100 rejected)
4. Audit findings without defensiveness (Zero Blame + AAA framework)
5. 90-day roadmap expectation-setting language

Raw responses saved at `/tmp/hormozi-responses/q1.md` through `q5.md` during planning (ephemeral — not persisted in skill).

**Key frameworks applied:**
- **Value Equation:** Dream Outcome × Likelihood of Achievement / Time Delay × Effort & Sacrifice
- **Calculator Close:** Dollar cost of the current constraint ("Ignorance Tax")
- **AAA Framework:** Acknowledge past logic → Associate with peer success → Ask-pivot to solution
- **BAMFAM:** "Book A Meeting From A Meeting" — never end without the next one on the calendar
- **Selling Cold:** Anchor expectations to bottom-25% of past results, not averages
- **Reveal/Withhold Rule:** Declarative knowledge (the what) is revealed, procedural knowledge (the how) is the engagement

---

## Chatroom consultation

Three-agent adversarial chatroom consulted during planning:
- **Performance Marketer** agent
- **Brand Voice Guardian** agent
- **Solopreneur Operator** agent

They debated 10 items from two external repos (zubair-trabzada/ai-ads-claude and AgriciDaniel/claude-ads) and produced the chatroom verdict that drove Parts 4 and 5 of this plan (Phase A quick wins + Phase B structural borrows).

Chatroom verdict summary lives in `~/.claude/plans/zany-sprouting-prism.md`.

---

## This skill's own authorship

Built from the plan at `~/.claude/plans/zany-sprouting-prism.md` by Claude Code under direction from Jerel on 2026-04-11.
