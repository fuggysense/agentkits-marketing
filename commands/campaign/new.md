---
description: Create a new marketing campaign from template
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [project-name] [campaign-type]
---

## Prerequisites

- Project must exist in `clients/<project>/`
- Campaign type: `product-launch`, `content-seo`, `lead-gen`, `retention`

---

## Context Loading

1. Load campaign-runner skill: `skills/campaign-runner/SKILL.md`
2. Load project context: `clients/<project>/` (icp.md, offer.md, brand-voice.md)
3. Load V.O.I.C.E. files from `voice/<person>/`

---

## Workflow

### Step 0: Get Date
```bash
CURRENT_DATE=$(date +%y%m%d)
```

### Step 1: Identify Project
If not provided as argument, trigger context gate — list available projects from `clients/` and ask user to pick.

### Step 2: Ask Campaign Type

**Question:** "What type of campaign?"
**Options:**
- **Product Launch** — Full launch sequence (12 tasks): landing page, emails, social, ads, tracking
- **Content SEO** — Organic growth pipeline (8 tasks): keywords, blog posts, social distribution
- **Lead Gen** — Lead capture funnel (10 tasks): lead magnet, landing page, nurture emails, ads
- **Retention** — Churn reduction (8 tasks): win-back emails, NPS, engagement content
- **Custom** — Start blank and add tasks manually

### Step 3: Ask Campaign Name

**Question:** "What should we call this campaign?"
**Example:** "Launch Q2", "SEO Content Sprint", "Lead Gen - Ebook"

### Step 4: Create Campaign

```bash
python3 skills/campaign-runner/scripts/state_manager.py new <project> <slug> <type>
```

This creates:
```
clients/<project>/campaigns/<slug>/
├── state.yaml       (from template)
├── assets/
└── metrics/
```

### Step 5: Fill Campaign Name

Update `state.yaml` with the human-readable campaign name.

### Step 6: Display Dashboard

Show the campaign state:
- Campaign name, type, phase
- Total tasks with descriptions
- First 3 recommended actions
- Dependencies map

### Step 7: Ask to Start

**Question:** "Campaign created! Start with the first task?"
**Options:**
- **Yes** — Execute first available task
- **Customize first** — Modify task list before starting
- **Later** — Save and exit

---

## Output Location

Campaign saved to: `clients/<project>/campaigns/<campaign-slug>/state.yaml`
