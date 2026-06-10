---
description: Generate the 26-section paid ads source-of-truth for a client, URL, or idea — parallel research, HITL checkpoint, sheet integration
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [url | description | client-slug]
---

## Purpose

Produce the full paid ads source-of-truth document for any input — existing client, product URL, or free-text idea — grounded in real buyer research (not guesses). Writes the 26-section doc + 5 derivative files + optionally populates AVATARS / CREATIVES / COPY tabs in the client's Google Sheet after HITL approval.

This command sits UPSTREAM of the existing ad pipeline:

```
/ads:source-of-truth → /ads:avatars → /ads:concepts → /ads:validate → /ads:preview → /ads:upload → /test:ab-setup
```

## Input

`$ARGUMENTS` — one of:
- **Client slug** (e.g. `neezanizam`) → Mode A refresh of existing project
- **URL** (e.g. `https://example.com/pricing`) → Mode B product triage
- **Free-text description** (e.g. `"AI scheduling for property agents in SG"`) → Mode C greenfield idea

## Prerequisites

Before running, ensure:
- [ ] Context Gate passed — current session has WHO + WHAT PROJECT established (per Marketing CLAUDE.md)
- [ ] Mode A only: `clients/<slug>/` exists with at least `buyer-profile.md` OR `icp.md`
- [ ] Mode B only: URL is publicly accessible (or dev-browser has auth if gated)
- [ ] MCP configured for full run: `scrapecreators`, `dataforseo` (optional); `meta` CLI for live ad data (optional)
- [ ] If sheet write desired: `clients/<slug>/metrics-config.json` exists with `sheet_id` + AVATARS/CREATIVES/COPY tab gids

## Workflow

This command activates the `source-of-truth` skill. Full phase breakdown lives in `skills/source-of-truth/SKILL.md`. Summary:

### Phase -1 — Niche Pool Awareness (runs before everything else)

Before any research begins, check whether a shared niche pool exists for this industry:

1. Resolve industry slug from the client's `context-profile.json` → `industry` field (e.g. `property-sg`)
2. Check for `swipe-files/<industry>/research-pool.json` and `swipe-files/<industry>/avatar-registry.json`
3. If either file exists, load it into context and apply these constraints:

**Research constraint — sources:**
> "Do NOT re-mine sources already listed in `sources_mined` unless their `last_refreshed_at` is >30 days ago. Focus new mining exclusively on sources not yet in the pool. This avoids duplicating work already done for another client in this industry."

**Research constraint — avatar:**
> "The avatar produced for THIS client must claim a psychographic slice not already present in `claimed_slices` in `avatar-registry.json`. Cross-check the proposed demographic + psychographic + core_desire against existing entries before finalising. If there is overlap, redirect to an available slice in `available_slices_<industry>` or propose a new non-overlapping slice."

**Phrase constraint:**
> "Buyer-language phrases already marked `claimed_by_client` in `research-pool.json` for another client MUST NOT be used in copy for this client. They may still be cited as research context but cannot appear in headlines, hooks, or ad copy."

4. If the pool files do NOT exist yet, create them after Phase 5 completes (see below).
5. Surface a brief summary at the start of Phase 0: "Pool found: X sources mined, Y phrases extracted (Z claimed). Unclaimed slices available: [list from avatar-registry]."

### Phase 0 — Context Gate + Triage
- Detect mode (A / B / C) from input
- Mode A: freshness check — if existing `source-of-truth.md` <90 days old, ask refresh/extend/skip
- Load existing foundation files into context

### Phase 1 — Foundation Intake (Mode B/C only)
- Single batched AskUserQuestion, 5-7 minimum questions (see `skills/source-of-truth/references/triage-questions.md`)
- Covers: conversion goal, target market, price point, ad state, brand constraints, platform focus, existing assets
- Mode A skips this entirely

### Phase 2 — Parallel Research (5-10 min)
Spawn in ONE message (parallel):
1. `scrapecreators` — competitor ad library
2. `buyer-language-researcher` agent — Reddit, NotebookLM, social sentiment (verbatim quotes)
3. `deep-research` skill — market sentiment + Schwartz awareness + sophistication level
4. `WebFetch` (Mode B) — product page deep scrape
5. `paid-media-audit` (if ad account connected) — existing account findings

All outputs land in `clients/<slug>/research/` + `clients/<slug>/competitor-ads/`.

Cost optimisation: route bulk summarisation through `scripts/research-llm.sh kilo`.

### Phase 3 — Section Synthesis (26 sections)
Per-section frameworks in `skills/source-of-truth/references/section-synthesis-frameworks.md`:
- §1-4: business-profile schema + intake
- §5: avatar-research Phase 1.5 framework (14 dimensions, verbatim quotes mandatory)
- §6-8: ranked tables from research
- §9-11: **net-new synthesis** (messaging hierarchy + angles + hooks)
- §12-15: static reference (paid-advertising + ad-concept-engine knowledge)
- §16-18: ab-test-setup framework + research-driven priorities
- §19-26: asset checklists + AI prompts + QA + summary + workflow

Strategic sections (§2, §9, §10, §16) DRAFTED here but not finalised.

### Phase 4 — HITL Checkpoint (1 batched call, 4 questions)
AskUserQuestion with 4 questions (see `skills/source-of-truth/references/checkpoint-questions.md`):
1. §2 Primary KPI — single-select with rationale
2. §9 Core Message — 3 candidates with previews (Problem-led / Outcome-led / Mechanism-led)
3. §10 Priority Angles — multi-select 3 of 6-8 drafted angles
4. §16 First Test Variable — single-select (hook / angle / proof / format / CTA / offer)

### Phase 5 — Write + Optional Sheet Integration
- Write `clients/<slug>/source-of-truth.md` (canonical)
- Write derivative files: `pain-objection-proof.md`, `swipe-file-buyers.md`, `swipe-file-sellers.md` + `angles/` folder (README, wave-1.md, wave-2.md, hook-library.md, iteration-log.md). NO `messaging-hierarchy.md` (lives in SoT §9). NO root `angles-hooks-library.md` (replaced by `angles/` folder for wave stability — 260418 architecture decision).
- Write research manifest + quote audit JSON
- If `metrics-config.json` exists: HITL preview → approve → write AVATARS / CREATIVES / COPY tabs via `scripts/source_of_truth_sheet_writer.py`

**After write — pool update (always runs):**
- Resolve `swipe-files/<industry>/research-pool.json`: if file exists, APPEND any newly mined sources and phrases; if file does not exist, create it using the schema at `swipe-files/property-sg/research-pool.json` as the template.
- Resolve `swipe-files/<industry>/avatar-registry.json`: if file exists, ADD the new client's claimed slice; if file does not exist, create it using the schema at `swipe-files/property-sg/avatar-registry.json` as the template.
- Update `last_updated` timestamp in both files.
- New phrase entries: set `claimed_by_client` to this client's slug for any verbatim quotes used directly in the produced source-of-truth (§5 verbatim quotes + §9 hooks). Leave `claimed_by_client: null` for phrases extracted but not used in copy.

### Phase 6 — Citation Verification (HITL gate before doc is "approved")

Run `scripts/verify-research-citations.py` against the final `source-of-truth.md`:

```bash
python3 scripts/verify-research-citations.py clients/<slug>/source-of-truth.md --out clients/<slug>/research/citation-verification.csv
```

Evaluate results:
- **All passed (exit 0):** proceed — doc is approved.
- **Failures present (exit 2):** surface each failed citation to the user in a HITL gate:
  - Show: `citation_id`, truncated quote, URL, http_status, similarity_pct
  - Ask: for each failure, is this (a) a valid quote at a now-deleted URL — mark as `source_archived`, (b) a paraphrase not verbatim — correct or remove, or (c) a fabricated citation — remove and flag in learnings.md?
  - Block doc approval until all failures are resolved or explicitly accepted by the user.
- **Bot-protected URLs (skip):** note in the handoff message; do not block approval for these.
- Write the final CSV to `clients/<slug>/research/citation-verification.csv` regardless of outcome.

## Hand-off Message Format

```
✓ Source of truth complete: clients/<slug>/source-of-truth.md
  26 sections · [N] verbatim buyer quotes · [N] competitor ads analysed
  Strategic decisions: KPI=<X> · Message=<Y> · Angles=<1>,<2>,<3> · First test=<Z>

Derivative files written:
  - pain-objection-proof.md
  - swipe-file-buyers.md / swipe-file-sellers.md
  - angles/ folder (README + wave-1.md + wave-2.md + hook-library.md + iteration-log.md) ← ad-concept-engine reads angles/wave-N.md

Sheet integration: [completed | skipped | preview-only]
  AVATARS tab: [N rows written]
  CREATIVES tab: [N rows appended as DCT00X-Y]
  COPY tab: [N rows appended as DRAFT]

Suggested next commands:
  1. /ads:avatars <slug>     → refine avatar files with source-of-truth depth
  2. /ads:concepts <slug>    → generate DCT batches from angles/wave-N.md
  3. /ads:preview <slug>     → dry-run what would upload to Meta
  4. /ads:upload <slug>      → push to Meta paused
  5. /test:ab-setup          → design first DCT split test using §16 priority
```

## Quality Gates

Before this command reports success:
- [ ] All §5 dimensions have ≥1 verbatim quote OR are marked `⚠️ NOT AVAILABLE`
- [ ] §9 / §10 / §16 / §22 reflect Phase 4 HITL answers
- [ ] `quote_count >= 30` OR user was warned of thin research
- [ ] UK English spelling throughout
- [ ] Data reliability: no fabricated statistics, quotes, or competitor data
- [ ] SG cultural guidelines applied if project is SG-based
- [ ] If sheet write ran: snapshot taken before any destructive op

## Failure Modes

| Failure | Recovery |
|---|---|
| Phase 2 research thin (<10 quotes) | Abort synthesis, recommend broader buyer-language-researcher run |
| Phase 4 HITL skipped | Use AI defaults, flag in §22, log to learnings.md |
| Sheet write rejected by user | Keep markdown files, skip sheet integration cleanly |
| Partial sheet write | Roll back to snapshot, surface exact row failures |
| Phase 1 thin answers (3+ skips in Mode B/C) | Stop, recommend `/project:profile` first |

## Related

- `/project:profile` — build context-profile.json first (if missing)
- `/ads:avatars` — downstream: builds 3+ DCT avatars from this
- `/ads:concepts` — downstream: generates DCT batches
- `/audit:paid-media` — upstream (optional): feeds §8 + §18 if ad account connected
- `/audit:competitor-ads` — alternative to scrapecreators for Meta Ad Library

## Self-Annealing

Per Marketing CLAUDE.md Self-Annealing Rule — log corrections to `skills/source-of-truth/corrections.md` after every user correction. Promote 3+ repeating corrections to `learnings.md` during `/ops:weekly`.
