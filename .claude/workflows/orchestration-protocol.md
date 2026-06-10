# Orchestration Protocol

## Language & Quality Standards

**CRITICAL**: Respond in the same language the user is using. If Vietnamese, respond in Vietnamese. If Spanish, respond in Spanish.

**Standards**: Token efficiency, sacrifice grammar for concision, list unresolved questions at end.

---

## Sequential Chaining (Marketing)

Chain agents when tasks have dependencies or require outputs from previous steps:

### Research → Insights → Creative
- Market understanding phase
- Each agent completes fully before the next begins
- Pass context and outputs between agents

### Plan → Create → Edit
- Content production phase
- Planning informs creation, editing refines output
- Maintain consistent messaging throughout

### Publish → Measure → Optimize
- Performance loop phase
- Publishing triggers measurement
- Insights feed optimization cycle

---

## Parallel Execution (Marketing)

Spawn multiple agents simultaneously for independent tasks:

### Multi-channel Content
- Same message, platform-adapted
- Blog + Social + Email created in parallel
- Ensure consistent messaging across variants

### A/B Variants
- Test versions created simultaneously
- Headlines, CTAs, or full content variations
- Plan testing strategy before creation

### Campaign Assets
- Copy + visuals + emails in parallel
- Coordinate handoffs between creative types
- Ensure brand consistency across assets

### Research Sprints
- Multiple researchers on different topics
- Competitor analysis + market research + audience research
- Synthesize findings before planning

---

## Agent + Skill Handoffs

| From | To | Trigger |
|------|-----|---------|
| `researcher` | `seo-mastery` skill | SEO insights needed |
| `researcher` | `campaign-runner` / `plan-for-goal` skills | Research complete, planning begins |
| `seo-mastery` skill | `copywriter` | Content creation phase |
| `copywriter` | `email-sequence` skill | Email sequences needed |
| `copywriter` | `sales:battlecard` skill | Sales collateral needed |
| `leads:score` skill | `sales:pitch` skill | MQL to SQL handoff |
| `crm:segment` skill | `email-sequence` skill | Segment-specific campaigns |
| `crm:lifecycle` skill | `offer-builder` / `pricing-strategy` skills | Expansion opportunity identified |

---

## Funnel Stage Routing

### TOFU (Top of Funnel) - Awareness
**Skills:** `seo-mastery`, `content-strategy`, `linkedin-content`, `tiktok-slideshows`
**Agents:** `researcher`, `copywriter`
**Focus:** SEO content, thought leadership, social media

### MOFU (Middle of Funnel) - Consideration
**Skills:** `email-sequence`, `leads:score`, `crm:segment`, `lead magnets`
**Agents:** `copywriter`
**Focus:** Lead magnets, email nurtures, webinars

### BOFU (Bottom of Funnel) - Decision
**Skills:** `sales-letter-method`, `sales:battlecard`, `sales:pitch`, `headline-bank`
**Agents:** `copywriter`, `sales-letter-auditor`
**Focus:** Case studies, demos, proposals

### Post-Purchase
**Skills:** `crm:lifecycle`, `offer-builder`, `pricing-strategy`, `referral-program`
**Agents:** `copywriter`
**Focus:** Onboarding, retention, expansion

---

## Campaign Type Protocols

### Product Launch
1. `researcher` → Market analysis
2. `campaign-runner` / `plan-for-goal` → Launch plan
3. `seo-mastery` + `website-design` → Landing pages, SEO
4. `copywriter` → Announcement content
5. `email-sequence` → Launch sequences
6. `sales-letter-method` / `headline-bank` → Sales materials
7. Parallel: Social + PR + Ads

### Lead Generation
1. `researcher` → Audience research
2. `seo-mastery` + `website-design` → SEO strategy, landing pages
3. `copywriter` → Lead magnet content
4. `email-sequence` → Nurture sequences
5. `leads:score` → Scoring and routing

### Retention Campaign
1. `crm:lifecycle` → Churn analysis
2. `campaign-runner` → Retention strategy
3. `email-sequence` → Re-engagement sequences
4. `offer-builder` / `pricing-strategy` → Expansion opportunities

---

## Quality Gates

### Before Publishing
- [ ] Brand voice consistency check
- [ ] Readability score meets standards
- [ ] CTAs are clear and action-oriented
- [ ] Legal/compliance review (if required)
- [ ] UTM parameters configured

### Before Handoff
- [ ] Context documented
- [ ] Assets organized
- [ ] Dependencies identified
- [ ] Success criteria defined

---

## Skill Selection Protocol

### Overview

Skills are specialized knowledge modules that agents load for specific tasks. Use the skills registry for intelligent selection.

### Skill Selection Algorithm

1. **Parse User Intent**
   - Extract keywords from request
   - Identify domain (CRO, SEO, content, etc.)
   - Determine primary goal

2. **Query Skills Registry**
   - Read `.claude/skills/skills-registry.json`
   - Match against skill triggers
   - Score relevance (0-1)

3. **Load Prerequisites**
   - Check `dependencyGraph` for requirements
   - Load foundation skills first
   - Maintain depth-first order

4. **Limit Context**
   - Maximum 5 skills per request
   - Prioritize: Direct match > Prerequisites > Related
   - Avoid context overload

5. **Activate Skills**
   - Read SKILL.md files for selected skills
   - Load references on-demand
   - Apply skill instructions

### Skill Categories

| Category | Skills | Primary Use |
|----------|--------|-------------|
| core | marketing-fundamentals, marketing-psychology, marketing-ideas, seo-mastery, social-media, email-marketing, paid-advertising, content-strategy, analytics-attribution, brand-building, problem-solving | Foundation knowledge |
| cro | page-cro, form-cro, popup-cro, signup-flow-cro, onboarding-cro, paywall-upgrade-cro, ab-test-setup | Conversion optimization |
| content | copywriting, copy-editing, email-sequence | Content creation |
| seo-growth | programmatic-seo, schema-markup, competitor-alternatives, launch-strategy, pricing-strategy, referral-program, free-tool-strategy | Growth strategies |
| document | docx, pdf, pptx, xlsx | Document creation |

### Skill-to-Agent Mapping

| Agent | Primary Skills |
|-------|---------------|
| conversion-optimizer | page-cro, form-cro, popup-cro, signup-flow-cro, onboarding-cro, paywall-upgrade-cro, ab-test-setup |
| copywriter | copywriting, copy-editing, email-sequence, sales-letter-method |
| brand-voice-guardian | brand-building, copywriting, copy-editing |
| researcher | deep-research, competitor-alternatives, ad-library-scraper |
| persona-builder | avatar-research |
| sales-letter-auditor | sales-letter-audit |

### MCP Integration Resolution

Before executing skills that require data:

1. Check `mcp-mapping-matrix.yaml` for skill-MCP mappings
2. Verify MCP server availability
3. If unavailable, request manual data input
4. Never fabricate metrics

### Skill Loading Examples

**Example 1: CRO Request**
```
User: "Optimize our signup form"
→ Match: signup-flow-cro (0.9)
→ Prerequisites: form-cro → page-cro
→ Load order: page-cro, form-cro, signup-flow-cro
```

**Example 2: Content Request**
```
User: "Write landing page copy"
→ Match: copywriting (0.9), page-cro (0.6)
→ Prerequisites: none
→ Load order: copywriting, page-cro
```

**Example 3: Launch Request**
```
User: "Plan Product Hunt launch"
→ Match: launch-strategy (0.95)
→ Prerequisites: content-strategy, social-media
→ Load order: content-strategy, social-media, launch-strategy
```

### Reference Data Access

Skills can reference common data files:

- `.claude/skills/common/data/benchmark-metrics.yaml` - Industry benchmarks
- `.claude/skills/common/data/conversion-formulas.yaml` - Metric calculations
- `.claude/skills/common/data/mcp-mapping-matrix.yaml` - Data source mappings
- `.claude/skills/common/templates/` - Copy templates and formulas

### Output Standardization

Use output schemas from `.claude/skills/schemas/output-schemas.yaml`:

- `cro-analysis` - CRO recommendations
- `content-plan` - Content strategy
- `campaign-brief` - Campaign planning
- `seo-audit` - SEO analysis
- `email-sequence` - Email design
- `ab-test-plan` - Test design

---

## Skill Commands

### /skills:select [task]
Intelligently select optimal skills for a task.

### Usage
When task complexity warrants multiple skills:
1. Invoke skill selector
2. Review recommended skills
3. Confirm or adjust selection
4. Execute with selected skills

---

## Conversation modes (one-shot vs iterative subagents)

Subagents can run in two modes. Pick deliberately.

**One-shot mode (default).** Single dispatch, single response, fresh context every call.
- Use for: parallel evaluator dispatches, simple generation jobs, structural audits, anything where independence is the feature.
- Pattern: `Agent(subagent_type, prompt)` — no name, no `run_in_background`.

**Iterative mode.** Subagent stays alive across turns, accumulating context in its own thread.
- Use for: concept development, draft refinement over multiple revisions, deep critic Q&A on specific findings, anything that benefits from back-and-forth in shared memory.
- Pattern: `Agent(name: "<slug-v1>", subagent_type, run_in_background: true, prompt: <briefing>)` then `SendMessage(to: "<slug-v1>", content: <follow-up>)` to continue the same thread. Optional: leave alive (visible in `claude agents`) or terminate when done.

Choosing the mode:
- **Generators benefit from iterative.** A sales letter writer or VSL scripter that goes through 3–5 revisions in one shared thread produces tighter work than 3–5 cold one-shots.
- **Evaluators stay one-shot.** Independence is the feature. Halbert and Schwartz must not see each other's notes.
- `"let's develop this together"` / `"iterate with me"` → iterative.
- `"give me your take"` / `"audit this"` → one-shot.

Name iterative subagents descriptively with a version suffix: `concept-ssl-hdb-v1`, `vsl-propwise-launch`, `halbert-deep-hook`. The name appears in `claude agents` so the thread is findable later.

**Never** use iterative mode for parallel evaluator dispatches — cross-pollination via shared memory destroys the independent-audit value.

---

## Orchestrator response shape

How orchestrator responses to the user should look:

- **Dispatch announcements:** one sentence. *"Dispatching `copy-sales-letter` because the brief is 800+ words cold traffic."* No preamble, no "I'm going to..."
- **Critique synthesis:** numbered punch list, one item per critic finding. Max 8 items. Each item: severity (P0/P1/P2), one-line fix, attribution (which evaluator flagged it).
- **Presenting copy for review:** paste copy in a fenced markdown block. NO commentary before the block. Commentary AFTER, max 3 bullets — what you'd change, what you're proud of, what's open.
- **Asking the user a question:** one question per turn. No preamble. No "I just want to make sure..."
- **Status updates mid-loop:** one short line per state change. *"Awareness call locked: Schwartz L2."* / *"3 evaluators dispatched."* / *"All 3 back."*

### Guardrails (make tradeoffs visible)

If the user asks to skip evaluators, bypass the brand voice check, ignore the awareness/sophistication call, or override the methodology — comply, but note it in one line: *"Skipping `eval-deAI` — output may carry AI-pattern residue."* / *"Bypassing brand voice — voice may drift."* Then proceed. The user is in charge; the orchestrator's job is to make the trade-off visible, not refuse.

Never apologize for the orchestrator's methodology. If a step feels slow, name it and offer to skip it — don't water it down silently.
