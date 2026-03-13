# Skill Dependency Graph

Visual representation of skill relationships, prerequisites, and learning paths.

---

## Overview

Skills are organized into tracks with explicit dependencies. Load prerequisite skills before dependent skills for optimal context.

---

## CRO Track (Conversion Rate Optimization)

```
page-cro (Foundation)
├── form-cro
│   └── signup-flow-cro
│       └── onboarding-cro
├── popup-cro
└── ab-test-setup ← (also requires: analytics-attribution)
    └── paywall-upgrade-cro ← (also requires: pricing-strategy)
```

**Learning Path:**
1. Start with `page-cro` (foundation for all CRO)
2. Specialize: `form-cro` → `signup-flow-cro` → `onboarding-cro`
3. Add testing: `ab-test-setup`
4. Monetization: `paywall-upgrade-cro`

---

## Content Track

```
copywriting (Foundation)
├── copy-editing
└── email-sequence ← (also requires: email-marketing)
```

**Learning Path:**
1. Start with `copywriting` (write first)
2. Polish with `copy-editing`
3. Automate with `email-sequence`

---

## SEO Track

```
seo-mastery (Foundation)
├── programmatic-seo (v2.0)
│   ├── (soft) analytics-attribution — for quality monitoring + indexation tracking
│   └── (soft) content-strategy — for niche taxonomy design
│   └── (soft) website-design — for template rendering
├── schema-markup
└── competitor-alternatives ← (also requires: copywriting)
```

**Learning Path:**
1. Start with `seo-mastery` (fundamentals)
2. Scale with `programmatic-seo` v2.0 (JSON-first, quality gates, niche taxonomy)
3. Enhance with `schema-markup`
4. Compete with `competitor-alternatives`

---

## Growth Track

```
content-strategy
├── launch-strategy ← (also requires: social-media)
└── free-tool-strategy ← (also requires: seo-mastery)

marketing-fundamentals
├── referral-program
└── pricing-strategy
    └── paywall-upgrade-cro ← (also requires: page-cro)
```

**Learning Path:**
1. Start with `marketing-fundamentals` or `content-strategy`
2. Launch with `launch-strategy`
3. Grow with `referral-program` or `free-tool-strategy`
4. Monetize with `pricing-strategy`

---

## Core Marketing Track

```
marketing-fundamentals (Foundation)
├── marketing-psychology
├── content-strategy
├── brand-building
├── analytics-attribution
│   ├── ab-test-setup
│   └── paid-advertising
└── marketing-ideas
```

**Learning Path:**
1. Start with `marketing-fundamentals`
2. Deep dive: `marketing-psychology`
3. Plan: `content-strategy`
4. Measure: `analytics-attribution`
5. Scale: `paid-advertising`

---

## Creative Content Track

```
image-generation (Foundation)
└── video-director ← (also requires: copywriting for dialogue scripts)
```

**Learning Path:**
1. Start with `image-generation` (reference images, JSON prompts)
2. Extend to `video-director` (AI video prompts, 11 types, 3 pipelines)
3. Pair with `copywriting` for dialogue-heavy video types

---

## Email Track

```
copywriting
└── email-marketing
    └── email-sequence
```

**Learning Path:**
1. Start with `copywriting`
2. Channel expertise: `email-marketing`
3. Automate: `email-sequence`

---

## Social Track

```
content-strategy
└── social-media
    ├── launch-strategy
    └── linkedin-optimization
        └── linkedin-content ← (also requires: copywriting)
```

---

## Paid Media Track

```
paid-advertising (Foundation)
└── paid-media-audit ← (also requires: analytics-attribution)
```

**Learning Path:**
1. Start with `paid-advertising` (platform strategies)
2. Audit with `paid-media-audit` (systematic account review)

---

## Campaign Execution Track

```
content-strategy ──┐
social-media ──────┼── campaign-runner
analytics-attribution ┘
```

**Learning Path:**
1. Understand `content-strategy` (what to create)
2. Know `social-media` (where to publish)
3. Know `analytics-attribution` (how to measure)
4. Execute with `campaign-runner` (state tracking, agent routing, publishing)

---

## Meta Track (System Tools)

```
meta-builder (Independent — creates new artifacts)
amplifier (Independent — enhances existing artifacts)
```

Related but independent: meta-builder creates, amplifier improves. If amplifier finds a gap too large to fill, it recommends meta-builder.

---

## Research Track (Independent)

```
deep-research (Independent — orchestrates parallel sub-agents)
```

Multi-agent parallel research. No skill dependencies — spawns researcher sub-agents with MECE decomposition.

---

## Document Track (Independent)

```
document-skills/docx (Independent)
document-skills/pdf (Independent)
document-skills/pptx (Independent)
document-skills/xlsx (Independent)
```

No dependencies - can be loaded as needed.

---

## Quick Reference: Dependencies

| Skill | Prerequisites |
|-------|---------------|
| `form-cro` | `page-cro` |
| `popup-cro` | `page-cro` |
| `signup-flow-cro` | `form-cro` |
| `onboarding-cro` | `signup-flow-cro` |
| `paywall-upgrade-cro` | `page-cro`, `pricing-strategy` |
| `ab-test-setup` | `page-cro`, `analytics-attribution` |
| `copy-editing` | `copywriting` |
| `email-sequence` | `email-marketing`, `copywriting` |
| `programmatic-seo` | `seo-mastery` (hard), `analytics-attribution` (soft), `content-strategy` (soft), `website-design` (soft — for template rendering) |
| `schema-markup` | `seo-mastery` |
| `competitor-alternatives` | `seo-mastery`, `copywriting` |
| `launch-strategy` | `content-strategy`, `social-media` |
| `referral-program` | `marketing-fundamentals` |
| `free-tool-strategy` | `seo-mastery`, `content-strategy` |
| `paid-media-audit` | `paid-advertising`, `analytics-attribution` |
| `linkedin-optimization` | `social-media` |
| `linkedin-content` | `linkedin-optimization`, `copywriting` |
| `campaign-runner` | `content-strategy`, `social-media`, `analytics-attribution` |
| `video-director` | `image-generation` (hard), `copywriting` (soft — for dialogue scripts) |

---

## Foundation Skills (No Prerequisites)

These skills can be loaded independently:

- `marketing-fundamentals`
- `marketing-psychology`
- `marketing-ideas`
- `page-cro`
- `copywriting`
- `seo-mastery`
- `social-media`
- `email-marketing`
- `paid-advertising`
- `content-strategy`
- `analytics-attribution`
- `brand-building`
- `problem-solving`
- `pricing-strategy`
- `deep-research`
- All document skills

---

## Skill Selection Algorithm

When selecting skills for a task:

1. **Match triggers** - Find skills matching user intent
2. **Load prerequisites** - Recursively load all required skills
3. **Limit context** - Load max 3-5 skills to avoid context rot
4. **Prioritize** - Foundation → Specialized → Related

Example:
```
User: "Optimize our signup form"
├── Primary match: signup-flow-cro
├── Prerequisites: form-cro, page-cro
└── Related (optional): ab-test-setup

Skills loaded: page-cro → form-cro → signup-flow-cro
```

---

## Agent-Skill Mappings

| Agent | Primary Skills |
|-------|----------------|
| `conversion-optimizer` | page-cro, form-cro, popup-cro, signup-flow-cro, onboarding-cro, paywall-upgrade-cro, ab-test-setup |
| `attraction-specialist` | seo-mastery, schema-markup, content-strategy, paid-advertising, competitor-alternatives |
| `pseo-architect` | programmatic-seo, seo-mastery, schema-markup, content-strategy, analytics-attribution |
| `copywriter` | copywriting, copy-editing, email-sequence, linkedin-content, video-director |
| `email-wizard` | email-marketing, email-sequence |
| `seo-specialist` | seo-mastery, schema-markup, programmatic-seo |
| `brand-voice-guardian` | brand-building, copywriting, copy-editing, linkedin-content |
| `brainstormer` | marketing-ideas, marketing-psychology, problem-solving, linkedin-content |
| `planner` | content-strategy, launch-strategy |
| `researcher` | marketing-fundamentals, analytics-attribution, pricing-strategy |
| `upsell-maximizer` | paywall-upgrade-cro, pricing-strategy, referral-program |
| `tracking-specialist` | analytics-attribution, paid-advertising, paid-media-audit |
| `continuity-specialist` | onboarding-cro, email-sequence, referral-program |
| `project-manager` | campaign-runner, content-strategy |
