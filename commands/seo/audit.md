---
description: Perform comprehensive SEO audit
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [url-or-sitemap]
---

## Prerequisites

Before running this command, ensure you have:
- [ ] Target URL or sitemap available
- [ ] Access to site (or public pages)
- [ ] MCP configured: `google-search-console`, `semrush` (optional)

## Context Loading

Load these files first:
1. `./README.md` - Product context
2. `./docs/seo/` - Previous SEO audits
3. `.claude/skills/seo-mastery/SKILL.md` - SEO frameworks

---

## Language & Quality Standards

**CRITICAL**: Respond in the same language the user is using. If Vietnamese, respond in Vietnamese. If Spanish, respond in Spanish.

**Standards**: Token efficiency, sacrifice grammar for concision, list unresolved questions at end.

**Skills**: Activate `seo-mastery`, `content-strategy` skills.

**Components**: Reference `./.claude/components/interactive-questions.md` and `./.claude/components/date-helpers.md`

---

## Interactive Parameter Collection

### Step 0: Get Current Date (MANDATORY)

**Execute BEFORE asking any questions:**

```bash
# Get current date info
CURRENT_DATE=$(date +%Y-%m-%d)
CURRENT_MONTH_NAME=$(date +"%B %Y")

# Baseline dates for comparison
DAYS_30_AGO=$(date -v-30d +%Y-%m-%d 2>/dev/null || date -d "-30 days" +%Y-%m-%d)
DAYS_90_AGO=$(date -v-90d +%Y-%m-%d 2>/dev/null || date -d "-90 days" +%Y-%m-%d)
PREV_MONTH=$(date -v-1m +"%B %Y" 2>/dev/null || date -d "-1 month" +"%B %Y")

echo "SEO Audit Date: $CURRENT_DATE"
```

---

### Step 1: Ask Audit Scope

**Question:** "What level of SEO audit do you need?"
**Header:** "Scope"
**MultiSelect:** false

**Options:**
- **Basic** - Quick health check, critical issues
- **Recommended** - Full audit with prioritized fixes
- **Complete** - Comprehensive with competitor analysis
- **Custom** - I'll select specific audit areas

---

### Step 2: Ask Audit Focus

**Question:** "Which areas should we audit?"
**Header:** "Focus"
**MultiSelect:** true

**Options:**
- **Technical SEO** - Speed, crawlability, Core Web Vitals
- **On-Page SEO** - Titles, metas, content optimization
- **Content Quality** - Thin content, gaps, keyword mapping
- **Off-Page & Links** - Backlink profile, authority, toxic links

---

### Step 3: Ask Baseline Period (DYNAMIC - use Step 0 values)

**Question:** "Compare against which baseline?"
**Header:** "Baseline"
**MultiSelect:** false

**Options (generated from Step 0):**
- **vs Last 30 days** - [DAYS_30_AGO] baseline
- **vs Last 90 days** (Recommended) - [DAYS_90_AGO] baseline
- **vs Last Month ([PREV_MONTH])** - Month-over-month
- **No baseline** - Current snapshot only

---

### Step 4: Ask Priority Output

**Question:** "How should we prioritize recommendations?"
**Header:** "Priority"
**MultiSelect:** false

**Options:**
- **Impact/Effort Matrix** (Recommended) - Quick wins first
- **By Issue Severity** - Critical → High → Medium → Low
- **By SEO Category** - Technical → On-Page → Content → Links
- **Custom priority** - I'll specify order

---

### Step 5: Confirmation

**Display summary:**

```markdown
## SEO Audit Configuration

| Parameter | Value |
|-----------|-------|
| Target | [URL or sitemap] |
| Focus Areas | [selected areas] |
| Baseline | [selected comparison] |
| Priority Method | [selected priority] |
| Scope | [Basic/Recommended/Complete] |
```

**Question:** "Proceed with SEO audit?"
**Header:** "Confirm"
**MultiSelect:** false

**Options:**
- **Yes, run audit** - Start SEO audit
- **No, change settings** - Go back to modify

---

## Data Reliability (MANDATORY)

**CRITICAL**: Follow `./workflows/data-reliability-rules.md` strictly.

### Required MCP Sources
| Data | MCP Server | Required |
|------|------------|----------|
| Rankings | `google-search-console` | For position data |
| Backlinks | `semrush` | For link profile |
| Keywords | `semrush`, `dataforseo` | For keyword analysis |

### Rules
1. **NEVER fabricate** SEO metrics (DA, rankings, traffic)
2. **Technical checks OK**: WebFetch for page speed, SSL, mobile
3. **If no MCP**: Show "⚠️ Ranking data requires GSC/Semrush MCP"

---

## Workflow: Parallel Subagent Architecture

**Pattern:** Adapted from `deep-research` MECE decomposition. Spawn 4-6 specialized agents IN PARALLEL using the Agent tool, each covering one audit category with explicit boundaries. After all return, run gap analysis and synthesize.

### Step 1: Spawn Parallel Audit Agents

Spawn these agents **in a single message** (all tool calls in one response) so they run concurrently:

| Agent | Focus | Boundaries | Tools |
|-------|-------|-----------|-------|
| **1: Technical** | Crawlability, indexability, Core Web Vitals, mobile, site speed, XML sitemap, robots.txt, HTTPS, redirects | NOT content quality, NOT backlinks | Chrome MCP, WebFetch, DataForSEO `onpage_task_post` |
| **2: On-Page** | Title tags, meta descriptions, headers, content structure, image optimization, internal linking, URL structure | NOT external links, NOT technical infra | Chrome MCP snapshot, WebFetch |
| **3: Content** | E-E-A-T signals, thin content detection, keyword mapping, content gaps, search intent match, duplicate content | NOT technical SEO, NOT link building | WebFetch, DataForSEO `labs_google_keyword_ideas` |
| **4: Off-Page** | Backlink profile, link velocity, domain authority, referring domains, toxic links | NOT on-page, NOT technical | DataForSEO `backlinks_summary`, `backlinks_backlinks` |

**Optional agents** (include for "Complete" scope or if user selected):

| Agent | Focus | When to Include |
|-------|-------|-----------------|
| **5: GEO/AEO** | AI search visibility, answer block readiness, FAQ schema, citation-friendly structure, speakable markup | Complete scope, or user asked for GEO |
| **6: Competitive** | SERP positions, content gaps vs competitors, competitor backlink opportunities | Complete scope, or user asked for competitors |

### Agent Prompt Template

Each agent receives this structured prompt:

```
You are performing a [CATEGORY] SEO audit for [URL/SITE].

TODAY'S DATE: [CURRENT_DATE]

YOUR FOCUS: [specific scope from table above]
BOUNDARIES: Do NOT cover [other categories] — other agents handle those.

TOOLS AVAILABLE:
- Chrome MCP (mcp__chrome__*) for live page analysis and screenshots
- WebFetch for page content
- DataForSEO MCP (if available) for metrics — see skills/seo-mastery/references/dataforseo-commands.md
- If DataForSEO unavailable, note "⚠️ DataForSEO not configured" and do manual analysis

REFERENCE:
- skills/seo-mastery/references/seo-audit-checklist.md — your category's checklist items
- skills/seo-mastery/references/geo-optimization.md — if you are Agent 5 (GEO)
- skills/seo-mastery/references/dataforseo-commands.md — API reference

OUTPUT FORMAT:
## [Category] Audit Findings

### Critical Issues (fix immediately)
- [Issue]: [Impact] | [Fix]

### High Priority (this week)
- [Issue]: [Impact] | [Fix]

### Medium Priority (this month)
- [Issue]: [Impact] | [Fix]

### Low Priority (next quarter)
- [Issue]: [Impact] | [Fix]

### Metrics Captured
| Metric | Value | Target | Status |
|--------|-------|--------|--------|

### Recommendations (top 3)
1. [Specific, actionable recommendation]
2. [Specific, actionable recommendation]
3. [Specific, actionable recommendation]
```

### Step 2: Gap Analysis

After ALL agents return:
1. Review all findings — check if any category has insufficient data
2. Look for contradictions between agents (e.g., technical says site is fast, but content agent found slow pages)
3. If significant gaps exist, spawn 1 targeted follow-up agent

### Step 3: Synthesize

Cross-reference all agent findings into ONE audit document:
- Deduplicate issues found by multiple agents
- Create unified priority matrix
- Calculate overall Health Score (weight: Technical 30%, On-Page 25%, Content 25%, Off-Page 20%)
- Generate executive summary
- Output to `./docs/seo/audits/[domain]-audit-[YYYY-MM-DD].md`

---

## Output Format

### Basic Scope

```markdown
# SEO Audit: [URL]
**Date:** [CURRENT_DATE]

## Health Score: [X/100]

## Critical Issues
| Issue | Impact | Pages Affected | Fix |
|-------|--------|----------------|-----|
| [Issue 1] | High | X | [Quick fix] |

## Quick Wins (Impact/Effort)
1. [High impact, low effort fix]
2. [High impact, low effort fix]

## Data Sources
- ✅ [MCP used] or ⚠️ [Not available]
```

### Recommended Scope

[Include Basic + Full Technical Audit + On-Page Analysis + Content Review + Prioritized Roadmap]

### Complete Scope

[Include all + Competitor Analysis + Link Building Strategy + 90-Day Action Plan]

---

## Pre-Delivery Validation

Before delivering SEO audit:
- [ ] All issues categorized by severity
- [ ] Quick wins clearly identified
- [ ] Metrics from verified sources
- [ ] Actionable recommendations
- [ ] Priority roadmap included

---

## Output Location

Save audit to: `./docs/seo/audits/[domain]-audit-[YYYY-MM-DD].md`

---

## Next Steps

After SEO audit, consider:
- `/seo:optimize` - Optimize specific pages
- `/seo:schema` - Add schema markup
- `/seo:keywords` - Conduct keyword research
