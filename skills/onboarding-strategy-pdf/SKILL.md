---
name: onboarding-strategy-pdf
description: "Generate client-ready 7-page onboarding strategy PDF (Hormozi framework). Merges context + avatar research + optional paid-media-audit. For paid calls. Triggers: onboarding strategy pdf, strategy report pdf, generate onboarding report, onboarding deliverable."
version: 1.0.0
category: client-deliverables
agents:
  - docs-manager
  - project-manager
prerequisites:
  - client-onboarding
  - avatar-research
related_skills:
  - client-onboarding
  - avatar-research
  - ad-concept-engine
  - paid-media-audit
  - document-skills/pdf
mcp_integrations:
  optional: []
---

## Graph Links
- **Feeds from:** [[client-onboarding]], [[avatar-research]], optionally [[paid-media-audit]]
- **Feeds into:** paid client onboarding call (manual step — Jerel presents the PDF)
- **Used by agents:** [[docs-manager]], [[project-manager]]
- **Related:** [[ad-concept-engine]] (downstream engagement after sign-on), [[document-skills/pdf]] (PDF engine)

---

# Onboarding Strategy Report PDF

## Purpose

Generate a **client-ready PDF** that Jerel presents at the paid onboarding call. The PDF is the deliverable the client has paid for — it must make them feel they've **already received value worth more than they paid for the onboarding**, while setting up the full engagement sign-on.

This is **not** a post-campaign audit and **not** a DCT tracker. It's a pre-engagement **sales + strategy document** with Hormozi-framework-aligned structure.

## When to Use

- Client has completed the discovery call
- Client has paid for the onboarding
- Client has completed the Fuggy's Media intake form (`business-profile` or `client-onboarding` skill, 6 sections / ~21 questions)
- Avatar research has produced avatars (`avatar-research` skill)
- **Optional:** If client has run ads before, `paid-media-audit` has been run first
- The paid onboarding call is scheduled within 1–7 days

## When NOT to Use

- Post-campaign performance reports → use `/report:weekly` or `/report:monthly`
- DCT tracker / creative approval docs → use `ad-concept-engine` Phase 4 output
- Ad audit reports for existing clients (no onboarding context) → use `paid-media-audit` directly
- Internal / working documents → keep as markdown, not PDF

## Inputs

The orchestrator (Claude) compiles a single JSON input from these sources:

| Source | Purpose | Required? |
|---|---|---|
| `clients/<project>/context-profile.json` | Business context, industry, vertical, offer, current stage, `dream_translation` inputs | Required |
| `clients/<project>/avatars/` (all avatar files) | 12-point avatar breakdowns, awareness + sophistication levels, top pains, buying triggers | Required |
| `clients/<project>/avatars/sophistication-map.md` | Evidence-backed sophistication per avatar | Required |
| `clients/<project>/swipe-file-buyers.md` (or general) | Blue ocean angle themes, competitor gaps | Optional |
| `clients/<project>/learnings.md` | Prior-engagement insights | Optional |
| `clients/<project>/paid-media-audit/*.md` (if exists) | Findings to feed the AAA-framed audit page | Optional |
| `skills/onboarding-strategy-pdf/references/benchmarks-registry.md` | Per-vertical CTR/CPL/ROAS benchmarks for Calculator Close math | Required |

## Output

Single PDF at:

```
clients/<project_slug>/deliverables/onboarding-strategy-report-YYMMDD.pdf
```

`YYMMDD` uses `bash -c 'date +%y%m%d'` (never model knowledge — per root CLAUDE.md rule).

Companion **Black Book** folder is created alongside:

```
clients/<project_slug>/deliverables/black-book-YYMMDD/
```

containing copies (or symlinks) of the referenced assets — swipe files, cultural guidelines, frameworks — that the client receives as part of engagement.

## Pipeline (orchestrator steps)

1. **Load context** — read all inputs above into memory
2. **Detect vertical** — from `context-profile.json → business_context.vertical` (or explicit override). Look up benchmarks from `references/benchmarks-registry.md`
3. **Score dimensions** — rate Audience Clarity, Creative Direction, Funnel Architecture, Competitive Position, Budget Readiness on 1–5 per the rubric in `references/page-layouts.md`
4. **Select primary constraint** — pick the ONE dimension where a score improvement has the highest leverage on the client's dream outcome. Document the rationale (client will see it).
5. **Calculator Close math** — compute `monthly_cost_of_constraint_usd` and `annual_ignorance_tax_usd` using the per-vertical benchmark from step 2
6. **Compile input JSON** — follow the schema in `templates/report-schema.json`. Adhere to the reveal/withhold rule: **angle themes only, never finished copy**. See `references/forbidden-content.md` for the full blacklist
7. **Run script**:
   ```bash
   python skills/onboarding-strategy-pdf/scripts/generate_pdf.py \
     --data <compiled.json> \
     --output clients/<project>/deliverables/onboarding-strategy-report-YYMMDD.pdf \
     --verbose
   ```
8. **Build Black Book companion folder** — copy referenced assets into `deliverables/black-book-YYMMDD/`
9. **HITL gate** — present the PDF to Jerel for review before the onboarding call
10. **Deliver** — at the onboarding call, Jerel presents the PDF. BAMFAM prompt at end of roadmap page is filled in during the call.

## Page Layout

**7 pages** (8 if existing-ads audit is enabled):

1. **Cover** — Dream Translation in client's exact words, Primary Constraint callout, Calculator Close ($/month + $/year Ignorance Tax). **No composite score. No A+ → F grade.**
2. **Diagnostic Dashboard** — 5-dimension RYG table (1–5 scores, Red/Yellow/Green bands), primary constraint row highlighted, prescribed action per dimension, Calculator Close narrative
3. **Avatar Deep-Dive** — One card per avatar: name, awareness/sophistication chip, top pains, buying trigger, **angle THEMES** (not finished copy)
4. **Strategic Positioning + Mechanism** — Mechanism name, positioning angle, differentiation wedge, angle themes per avatar, explicit "execution specifics delivered as part of engagement" footer
5. **Existing Ads Audit (conditional)** — Zero Blame header + AAA-framed findings (Acknowledge / Associate / Ask) + skill-deficiency reframes + per-finding Calculator Close. **Skipped if** `existing_ads_audit.enabled == false`.
6. **Plus/Minus Potential Map** — Two-column visual: "Work with us → more X / less Y" vs "Stay current path → more Y / less X". Items pulled from avatar pains + dream translation
7. **90-Day Roadmap** — Activation (Days 1–30) / Value (Days 31–60) / Lock-In (Days 61–90) phases. Selling-cold language anchored to bottom-25% of past results. BAMFAM next-meeting prompt at bottom
8. **Black Book Appendix** — List of assets client receives with perceived-value annotations. Total perceived value stated.

See `references/page-layouts.md` for full per-page content rules.

## Scoring Model (Hormozi-Revised)

**NOT a composite 0–100 score.** Consulted Hormozi AI notebook via `notebooklm` during planning — the 0-100 composite was classified as consultant theater and rejected. Replaced with:

- **1–5 score per dimension** across 5 categories
- **Red / Yellow / Green band** per dimension (Red = 1–2, Yellow = 3, Green = 4–5)
- **Primary Constraint flag** — exactly ONE dimension is designated as the bottleneck
- **Calculator Close** — mandatory dollar figure (monthly + annual) for the primary constraint
- **Prescribed action per dimension** — every score ties to a specific action

See `references/page-layouts.md` for the scoring rubric per dimension and `references/benchmarks-registry.md` for per-vertical benchmark numbers used in Calculator Close math.

## Per-Client Flexibility

The Python script is **100% generic** and contains ZERO hardcoded client-specific content. Every client-specific element flows from:

1. **Input JSON** — narrative content, numbers, dream translation, avatars
2. **Benchmarks registry** — per-vertical CTR/CPL/ROAS lookups
3. **Per-client references** — `context-profile.json`, `avatars/`, `imagery-forbidden.md`, etc.

**Onboarding a new client:**
1. Scaffold `clients/<new-project>/` from `clients/_template/`
2. Run `client-onboarding` skill to populate `context-profile.json` + `avatars/`
3. If new vertical, append an entry to `references/benchmarks-registry.md` (no Python changes)
4. Populate `clients/<new-project>/imagery-forbidden.md` with vertical-appropriate guardrails
5. Run this skill — same command, same script, different data → different PDF

## Reveal vs Withhold Rule

Critical — enforced at orchestrator level and spot-checked by `references/forbidden-content.md`:

**REVEAL (declarative — the WHAT):**
- The primary constraint + its dollar cost
- The mechanism name
- Positioning angle + differentiation wedge
- Angle themes per avatar
- The 90-day phase structure

**WITHHOLD (procedural — the HOW):**
- Actual finished headlines
- Actual ad copy
- Landing page layouts
- Automation logic or trigger points
- SOPs or step-by-step playbooks

The withheld content IS the engagement. The PDF is the promise; the engagement is the delivery.

## Dependencies

- Python 3.10+ (tested on 3.14)
- `reportlab >= 4.0` (see `requirements.txt`)
- Standard library only beyond reportlab

Install:
```bash
pip install -r skills/onboarding-strategy-pdf/requirements.txt
```

## Related

- **Plan document:** `~/.claude/plans/zany-sprouting-prism.md` (rationale, decisions, Hormozi consultation log)
- **Hormozi consultation responses:** `/tmp/hormozi-responses/q1.md` through `q5.md` (scratch — not persisted)
- **Upstream skills:** `client-onboarding`, `avatar-research`
- **Downstream:** paid onboarding call → engagement → `ad-concept-engine` full DCT pipeline

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[business-profile]] (skill, 0.17)

<!-- skill-graph:end -->
