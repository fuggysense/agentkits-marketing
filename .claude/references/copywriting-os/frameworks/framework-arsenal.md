---
name: Framework Arsenal — canonical copy framework inventory
source: cai #14, raw-newsletters/framework-arsenal-claude-projects-skills.md
loaded_by: copywriting (top-of-loop framework selector), copy-editing, sales-letter-method, email-sequence, page-cro reviewers, any skill that says "use my [X] framework"
purpose: Index of every named copywriting framework Mark Masters publishes plus the architecture (Project + Skills) for deploying them as permanent infrastructure. Loaded so the writer/reviewer knows which canonical framework name to invoke and where the full spec lives.
---

# Framework Arsenal — Canonical Copy Framework Inventory

## What this is

A meta-inventory: a Claude Project (static framework storage) paired with Application Skills (dynamic methodology). The Project holds Mark's proven frameworks as permanent knowledge; the Skills teach Claude how to apply them automatically. The 45-minute "explain my framework to Claude" tax becomes a 30-second "Use my [X] Framework" deployment. This file is the catalog index — the full spec for each framework lives in a sibling `frameworks/*.md` file.

> Critical warning Mark publishes: **Your Framework Arsenal is only as good as the frameworks you put in it.** If they don't convert, systematizing them just produces garbage faster. Prove them with real money first; then systematize.

## Inputs / prerequisites

- Frameworks already validated against real campaign performance (don't systematize unproven hypotheses)
- A Claude Project named "Framework Arsenal" with knowledge base capacity
- Settings → Capabilities → "Create and edit files with Claude" enabled (required for Skills)
- Each framework documented using the standard template (Purpose / When to Deploy / Structure / Sequence / Examples / Benchmarks / Mistakes / Activation Language)

## The framework / process

### Architecture

```
FRAMEWORK ARSENAL PROJECT          FRAMEWORK APPLICATION SKILLS
(stores your proven frameworks) +  (teaches Claude how to use them) = TOTAL DEPLOYMENT ADVANTAGE
```

**Project = static storage.** Documents available across all chats in the Project, auto-cached, auto-RAG'd.

**Skills = dynamic procedures.** Activate automatically based on description match, work everywhere in Claude (not just in the Project).

### Standard framework documentation template

Every framework Mark publishes follows this structure — sibling `frameworks/*.md` files in this library use the same skeleton:

```
# [FRAMEWORK NAME]
## Purpose
## When to Deploy
## Framework Structure
## Deployment Sequence
## Success Examples
## Performance Benchmarks
## Common Mistakes
## Activation Language ("Use my [X] Framework")
```

## The Inventory — every named framework Mark catalogs

### Core Conversion Frameworks

| Framework | One-line definition | Where it applies | Full spec |
|-----------|---------------------|------------------|-----------|
| **The Masters Headline Formula** | `[Curiosity Hook] + [Credibility Marker] + [Clear Benefit]` — generates headlines targeting 40+/50 score across curiosity, specificity, clarity, credibility, emotional resonance | Email subject lines, landing page H1s, ad headlines, social hooks, article titles | `five-headline-mechanisms.md` (cai #39) |
| **PAS Framework (Problem-Agitate-Solution)** | 25% problem, 40% agitate, 35% solution. Amplify pain before solution to create psychological readiness. | Landing pages, sales letters, first emails in sequence, ads | Inline in cai #14 |
| **CTA Optimization Framework** | `Clarity + Friction Removal + Urgency + Risk Reversal`. Action verb + specific outcome, value reinforcement above, risk reversal below, single primary CTA per page. | Landing pages, sequence final emails, sales pages, webinar offers | Inline in cai #14 |
| **Objection Pre-Handle Matrix** | 5 objection categories × 4 pre-handle techniques (Reframe / Preempt / Validate-then-redirect / Eliminate-through-proof). Map every major objection to a placement (early/mid/late copy). | Sales pages, VSLs, high-ticket offers, sequence emails 4-6 | `six-objection-categories.md` (cai #36) |

### Complete Campaign Structures

| Framework | One-line definition | Where it applies | Full spec |
|-----------|---------------------|------------------|-----------|
| **7-Email Sequence Architecture** | Pattern Interrupt → Problem Amplification → Solution Introduction → Mechanism Reveal → Social Proof Cascade → Objection Annihilation → Urgency + Close. Day 1, 2, 3, 5, 6, 8, 9 timing. | Product launches, lead magnet follow-up, course/program sales, high-ticket service sales | Inline in cai #14; emotional sequencing nuance in `six-emotional-states.md` (cai #37) |
| **VSL Blueprint** | Video Sales Letter structure. Referenced as a named asset in the Project but not fully detailed in cai #14. | High-ticket VSLs, webinar replays | Referenced (separate Mark asset) |
| **Landing Page Formula** | Composite of PAS + CTA Optimization applied to a single conversion surface. | Standalone LPs, ad-targeted pages | Composite — see PAS + CTA entries |
| **Webinar Conversion Structure** | Referenced in the Project index. | Live and replay webinar funnels | Referenced (separate Mark asset) |

### Strategic Methodologies

| Framework | One-line definition | Where it applies | Full spec |
|-----------|---------------------|------------------|-----------|
| **Desire Amplification System** | Strategic methodology referenced in Mark's Project index, paired with social proof in consideration-stage copy. | Sales page mid-section, sequence emails 3-5, VSL build-up | Referenced (separate Mark asset) |
| **Brand Voice Development Protocol** | Voice extraction + codification. Sister system to the Voice Vault Project. | New client onboarding, retainer voice consistency | Referenced (separate Mark asset) |
| **Market Sophistication Mapping** | Schwartz-style 5-stage sophistication scoring; channels existing desire rather than creating it. | Pre-write strategy on every cold-traffic asset | `schwartz-channeling.md` (cai #41) |
| **Competitive Positioning Framework** | Maps undefended competitor territory; pairs with Competitive Scout output. | Positioning briefs, differentiation copy | See `scout-mode-instructions.md` (cai #35) |

### Application Skills (dynamic layer)

Three Skills that activate automatically and apply Arsenal frameworks without explicit invocation:

| Skill | Activates on | What it does |
|-------|--------------|--------------|
| **Framework Selector** | Any copywriting request | Analyzes objective + deliverable + audience → recommends primary framework, supporting frameworks, application sequence, expected performance |
| **Masters Headline Generator** | Headlines, subject lines, ad titles, hooks | Generates 10-15 variations using the Masters Headline Formula, scores each on 5 criteria, ranks top 5 with A/B test recommendation |
| **Email Sequence Architect** | Email sequences, drip campaigns, launch sequences | Builds 7-email sequence with subject lines (via Headline Formula), opening hook, core content, transition, sequence-appropriate CTA, timing |

### Skill chaining example

User prompt inside Framework Arsenal Project: *"I need a 7-email sequence for a SaaS product launch. Product helps agencies automate client reporting. Target: agency owners billing $50K-200K/month."*

Behind the scenes:
1. Framework Selector activates → recommends 7-Email Sequence Architecture
2. Email Sequence Architect activates → references the architecture from Project knowledge base
3. Masters Headline Generator activates for subject lines
4. Output: complete sequence matching Mark's standards in first draft

## Outputs

This file's outputs:
- A canonical name for every Mark Masters framework (so writers can `"use my [X] framework"` instead of re-explaining)
- Pointer to the sibling `frameworks/*.md` file with the full spec
- Coverage map showing which frameworks have full specs vs which are referenced-only

## Application rules / scoring

How to know your Framework Arsenal is operational:
- Every named framework in the inventory above either has a documented sibling file OR is explicitly marked "Referenced (separate asset)"
- Each documented framework follows the standard template (Purpose → Activation Language)
- Skills auto-activate without explicit invocation
- "Use my [X] Framework" produces output matching standards in the first draft (no re-explanation needed)

If output doesn't match standards on first draft → the framework documentation is too vague. Tighten the spec, don't tighten the prompt.

## Exact prompts / templates / system instructions

### Framework Documentation Template (use for every new framework added)

```
# [FRAMEWORK NAME]

## Purpose
[What specific problem this framework solves]

## When to Deploy
[Exact contexts where this framework applies]

## Framework Structure
[The actual framework with all components detailed]

## Deployment Sequence
[Step-by-step application process]

## Success Examples
[2-3 real examples with results]

## Performance Benchmarks
[Typical conversion rates or metrics this achieves]

## Common Mistakes
[What people get wrong when applying this]

## Activation Language
"Use my [Framework Name]"
"Apply [framework] structure"
```

### Framework Arsenal Index document (paste as first file in Project knowledge base)

```
# Framework Arsenal Index

## Core Conversion Frameworks
- PAS Framework (Problem-Agitate-Solution)
- The Masters Headline Formula
- CTA Optimization Framework
- Objection Pre-Handle Matrix

## Complete Campaign Structures
- 7-Email Sequence Architecture
- VSL Blueprint (Video Sales Letter)
- Landing Page Formula
- Webinar Conversion Structure

## Strategic Methodologies
- Desire Amplification System
- Brand Voice Development Protocol
- Market Sophistication Mapping
- Competitive Positioning Framework
```

### Skill description guidelines

- Description must be under 200 characters (hard limit for auto-activation)
- Description must clearly state what the Skill does so Claude can match intent
- Bad: "Analyzes text"
- Good: "Generate high-performance headlines using Masters Headline Formula combining curiosity, credibility, and clear benefit"

## Common failures

1. **Treating frameworks as inspiration instead of infrastructure.** Saving "Use emotional triggers" as a note isn't a framework — that's a reminder. A framework has structure, components, sequence, success criteria.
2. **Building infrastructure for unproven frameworks.** The system amplifies effectiveness. If your frameworks haven't earned real money on real campaigns, systematizing them produces faster garbage.
3. **ZIPing the SKILL.md instead of the folder.** Skills won't load. ZIP the folder itself.
4. **Skipping the Activation Language section.** Without "Use my [X] Framework" phrasing built into the doc, deployment requires re-explanation. The activation phrase is the API.

## When to use vs skip

**Use when:**
- A reviewer or writer needs to invoke a canonical framework by name and wants the right pointer
- Auditing whether copy actually deploys a named framework or just gestures at one
- Onboarding a new client and need to map their use-case to the right framework stack
- Building or maintaining a Claude Project knowledge base for repeatable copy production

**Skip when:**
- You need the full spec for a single framework — go directly to its sibling file
- The work isn't framework-driven (e.g. pure VOC mining; use `scout-mode-instructions.md` instead)
- You're still validating which frameworks actually work in your market — gather data first
