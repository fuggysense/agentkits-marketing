---
description: Generate a static-ad headline bank (75+ headlines across 5 awareness levels × 10 angle banks, anchored to one mass desire) for a client. Feeds ad-concept-engine Phase 2a.
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [client-slug]
---

## Purpose

Produce a deep, awareness-mapped headline reservoir for a client's paid static ads. Anchors to ONE mass desire per run (user picks or skill suggests). Outputs a structured markdown file at `clients/<slug>/angles/wave-<N>-headline-bank.md` that `ad-concept-engine` Phase 2a reads as the first reservoir when picking the 2 Meta headlines per DCT batch.

Pipeline placement (optional — upstream of Stage 2):

```
/ads:source-of-truth → /ads:avatars → [OPTIONAL: /ads:headlines] → /ads:concepts → /ads:upload → /ads:feedback
```

Run this command when:
- The 10 hooks per angle already in `angles/wave-N.md` feel thin for the wave you're about to test
- You want strategic coverage across awareness levels, not just one angle's tactical reservoir
- You have multiple avatars spanning different awareness levels and need a matched bank

Skip this command when:
- Wave 1 is a quick-launch pilot and the 10 hooks per angle are enough
- The project doesn't yet have a source-of-truth or avatar files (prerequisite)

## Input

`$ARGUMENTS` — a client slug (e.g. `neezanizam`). Must already have:
- `clients/<slug>/source-of-truth.md`
- `clients/<slug>/_brand/avatars/avatar-*.md`
- `clients/<slug>/_brand/buyer-profile.md` or `_swipe/research/buyer-language-dossier.md`

## Prerequisites

- [ ] Context Gate passed — current session has WHO + WHAT PROJECT established (per Marketing CLAUDE.md)
- [ ] `clients/<slug>/source-of-truth.md` exists (run `/ads:source-of-truth <slug>` first if not)
- [ ] `clients/<slug>/_brand/avatars/` has at least one avatar file or avatar hypothesis (run `/ads:avatars <slug>` first if not)
- [ ] `clients/<slug>/_brand/brand-voice.md` exists

## Workflow

This command activates the `headline-bank` skill. Full phase breakdown lives in `skills/headline-bank/SKILL.md`. Summary:

### Phase 0 — Context Load
- Load `source-of-truth.md` §5 / §5.5 / §5.7 / §9
- Load `_brand/avatars/avatar-*.md` — Top 5 Deep Fears + Raw Inner Dialogue + Desired Transformation + Relationship Impact
- Load `_brand/buyer-profile.md` + `_swipe/research/buyer-language-dossier.md` (if exists) for verbatim quotes
- Load `_brand/brand-voice.md` + `_brand/offer.md`
- Load skill references: `mass-desires-catalog.md` + `awareness-angle-matrix.md`
- Load anti-slop: `skills/copy-editing/references/overused-ai-patterns.md`
- Detect current wave by scanning `angles/wave-*.md` (default Wave 1 if none)

### Phase 1 — First Response (MANDATORY verbatim)

> *"Which mass desire from the research do you want me to focus on for these headlines? (e.g. safety, health, status, ease, freedom, connection, etc.) If you're not sure, I can suggest the strongest one based on the knowledge base."*

### Phase 2 — Mass Desire Resolution
- User named it → confirm which avatar(s) it belongs to (cross-check the knowledge base)
- User said "not sure" → surface top 3 candidates with one-sentence verbatim evidence → user picks

### Phase 3 — Evidence Gathering
Pull 3-5 verbatim buyer-language quotes that support the chosen mass desire. These anchor every headline in the bank.

### Phase 4 — Generation
Generate 75+ headlines: 15+ per awareness level × 5 awareness levels, distributed across the 10 angle banks per the matrix (★★★ clusters get priority). Top 3 per awareness level get explanation + 2 variations; the rest are listed in a tactical pool.

### Phase 5 — HITL Review Gate
Summary in chat:
- Headlines generated per awareness level
- Top 5 scroll-stoppers (one per awareness level)
- Flagged drafts (anti-slop / brand-voice / duplicate concerns → go to Anti-Pattern Log, not the bank)

Ask: *"Approve the bank as-is? Or want me to re-weight any awareness level / swap an angle / rerun for a different mass desire?"*

### Phase 6 — Write
On approval, write to `clients/<slug>/angles/wave-<N>-headline-bank.md`. Append iteration-log entry.

### Phase 7 — Downstream Handoff
Surface the exact next command:
```
/ads:concepts <slug>
```

## Output

- `clients/<slug>/angles/wave-<N>-headline-bank.md` — the full bank
- `clients/<slug>/angles/iteration-log.md` — one-line entry appended

## Downstream

`ad-concept-engine` Phase 2a now loads this bank as its first reservoir. For every DCT batch, Phase 2a picks 2 Meta headlines by matching the batch's `market_awareness` + `angle` against the bank's matrix. Falls back to `angles/wave-<N>.md` hooks only if the bank lacks a matching awareness-level cluster.
