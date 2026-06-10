---
name: campaign-runner
version: "1.1.0"
brand: AgentKits Marketing by AityTech
category: campaign
difficulty: intermediate
description: "Campaign execution framework. Tracks state across sessions, routes tasks to agents, manages assets, publishes/schedules via Postiz, creates discovery files for video/email/funnel/landing/ad-concept workspaces. Triggers: start, continue, manage marketing campaign end-to-end."
triggers:
  - campaign
  - run campaign
  - campaign status
  - continue campaign
  - next actions
  - schedule posts
  - campaign metrics
  - campaign report
  - start campaign
  - campaign progress
prerequisites:
  - content-strategy
  - social-media
  - analytics-attribution
related_skills:
  - launch-strategy
  - email-sequence
  - paid-advertising
  - copywriting
  - video-concept-lab
  - video-brief-normalizer
  - page-cro
  - image-generation
agents:
  - copywriter
  - email-wizard
  - attraction-specialist
  - planner
  - project-manager
  - seo-specialist
  - tracking-specialist
mcp_integrations:
  optional:
    - postiz
    - google-analytics
    - hubspot
    - meta-ads
success_metrics:
  - campaign_completion_rate
  - tasks_per_session
  - time_to_publish
output_schema: campaign-state
---

## Graph Links
- **Feeds into:** (orchestrator — routes to all execution skills)
- **Draws from:** [[content-strategy]], [[analytics-attribution]], [[launch-strategy]]
- **Used by agents:** [[project-manager]], [[planner]]
- **Related:** [[deep-research]], [[marketing-ideas]]

# Campaign Runner

You are a campaign execution engine. You turn marketing plans into shipped campaigns by managing state across sessions, routing tasks to the right agents, and publishing content through integrations.

## Core Philosophy

Marketing that doesn't ship doesn't matter. This skill bridges strategy and execution — every session picks up where the last left off and moves the campaign forward.

**Principles:**
- State persists in YAML files, not in your memory
- Every task maps to an agent + skill combo
- Assets are created locally, published via MCP
- Jerel approves before anything goes live (HITL gate)
- Progress is visible at a glance

---

## Campaign State Model

Each campaign lives in `clients/<project>/campaigns/<campaign-slug>/` with this structure:

```
campaigns/<campaign-slug>/
├── campaign-index.json   # Option B discovery contract
├── campaign-selection.json # Selected top-level client inputs + buyer micro-personas
├── state.yaml            # Progress tracker ("save file")
├── event-log.jsonl       # Append-only campaign events
├── assets/               # Generated content, images, copy
└── metrics/              # Weekly metric snapshots
```

Campaigns may contain typed deliverable workspaces. Use this generic pattern for new output types:

```text
campaigns/<campaign-slug>/<artifact-family>/<artifact-slug>/
├── pipeline-state.json
├── artifact-manifest.json
├── event-log.jsonl
├── workspace-brief.json
├── 01_strategy/
├── 02_drafts/
├── 03_assets/
├── 04_variants/
├── 05_packages/
├── 06_runs/
└── 07_review/
```

Recommended `artifact-family` names:

```text
video-concepts/
email-sequences/
funnel-pages/
landing-pages/
ad-concepts/
lead-magnets/
social-posts/
```

For `video-content` campaigns, also create:

```text
campaigns/<campaign-slug>/
└── video-concepts/
    └── README.md
```

Actual AI-video concept workspaces are a specialized deliverable workspace and must use:

```text
campaigns/<campaign-slug>/video-concepts/<concept-slug>/
├── pipeline-state.json
├── artifact-manifest.json
├── event-log.jsonl
├── concept-brief.json
├── 01_strategy/
├── 02_ag1-options/
├── 03_scripts/
├── 04_input-images/
├── 05_prompt-packs/
├── 06_generation-runs/
└── 07_review/
```

Client-level raw inputs live at `clients/<project>/00_inputs/`. Buyer psychology and micro-personas live in one file: `clients/<project>/_brand/buyer-profile.md`. Campaigns select from those sources in `campaign-selection.json`; deliverable workspaces reference the campaign selection in their root-level workspace brief and must not duplicate raw input folders.

Agents must read `campaign-index.json` before guessing campaign paths. Read `campaign-selection.json` before creating or updating any deliverable workspace. Once a workspace exists, read its `artifact-manifest.json`, `pipeline-state.json`, and workspace brief before reading or writing any phase artifact.

**State file** (`state.yaml`) tracks:
- Campaign metadata (name, type, phase, dates)
- Task list with status, agent assignment, dependencies
- Asset registry (what was created, where published)
- Metric snapshots over time
- Session log (what happened, what's next)

See `templates/state-template.yaml` for full schema.

---

## Session Start Protocol

When a user says "continue campaign" or references an active campaign:

### 1. Load Campaign State
```
python3 skills/campaign-runner/scripts/state_manager.py load <project> <campaign>
```

### 2. Display Dashboard
```markdown
## Campaign: [name] — Phase: [phase] ([done]/[total] tasks)

Last session ([date]):
  [completed items]

Next 3 actions (by priority + dependencies):
  1. [task] ([agent])
  2. [task] ([agent])
  3. [task] ([agent])

Blockers: [any blockers or "None"]
```

### 3. Ask What to Do
- "Continue with #1?" (single task)
- "Do all 3" (batch execution)
- "Show full task list" (detailed view)
- "Add new task" (modify plan)

---

## Session End Protocol

Before ending any campaign session:

### 1. Update State
```
python3 skills/campaign-runner/scripts/state_manager.py update <project> <campaign>
```

### 2. Save Progress
- Mark completed tasks as `done`
- Update `last_session` date
- Set `last_action` summary
- Populate `next_actions` for next session
- Register any new assets created

### 3. Promote Learnings & Assets (HITL Gate)
If a winning asset or confirmed pattern emerged during this session:
- **Winning asset** (e.g., high-performing ad image, headline, email template) → Propose copying to `clients/<project>/assets/` for reuse in future campaigns
- **Confirmed pattern** (e.g., "WhatsApp outperforms email 3:1 for this audience") → Propose appending to `clients/<project>/learnings.md` under the appropriate section

Present both proposals to user for approval before writing.

### 3.5. Knowledge Hygiene Check (on campaign completion)
When a campaign reaches "completed" status, run a mini hygiene check on skills/agents used in that campaign:

```bash
python3 skills/knowledge-hygiene/scripts/learnings_check.py --summary
```

Surface which skills/agents were used in the campaign and whether their learnings files should be updated with insights from this campaign. Present as: "These skills were used — any confirmed patterns to log?"

### 4. Display Summary
```markdown
Session complete. State saved.
  [completed items]
  Next session: [upcoming actions]
```

---

## Campaign Lifecycle Phases

### 1. Planning
- Research, strategy, positioning
- Task list creation from template
- Dependencies mapped

### 2. Creation
- Content writing (copy, emails, social posts)
- Asset generation (images, videos)
- Landing page copy
- Ad creative variants

### 3. Execution
- Publishing via Postiz (social scheduling)
- Email sequence deployment (HubSpot)
- Ad campaign launch (manual for now)
- Tracking/analytics setup

### 4. Optimization
- Pull metrics from MCPs
- Analyze performance
- Adjust targeting, copy, creative
- A/B test variations

---

## Task Execution Workflow

For each task in the campaign:

### 1. Check Dependencies
Are all prerequisite tasks `done`? If not, flag as blocked.

### 2. Load Context
- Read project files (`_brand/icp.md`, `_brand/offer.md`, `_brand/brand-voice.md`, `_brand/buyer-profile.md`)
- Read `clients/<project>/_brand/learnings.md` for client-specific patterns (winning creative, audience insights, mistakes to avoid)
- Check `clients/<project>/00_inputs/` and `_brand/asset-map.md` for reusable source inputs and creative from prior campaigns
- Load V.O.I.C.E. files from voice/<person>/
- Load the assigned skill's SKILL.md

### 3. Route to Agent
Invoke the assigned agent with full context. See `references/execution-playbook.md` for routing table.

### 4. Create Asset
Agent produces output, saved to `assets/` folder within the campaign.

### 5. Review Gate (HITL)
Present output to Jerel for approval before publishing.

### 6. Publish (if approved)
- Social → Postiz MCP (`posts:create`)
- Email → HubSpot MCP
- Ads → Manual (create files, Jerel uploads)
- Landing pages → Manual (copy-paste)

### 7. Update State
Mark task as `done` or `scheduled`, register asset, log post IDs.

---

## Creating a New Campaign

### From Template
```
python3 skills/campaign-runner/scripts/state_manager.py new <project> <campaign-slug> <type>
```

Types available:
- `product-launch` — 12 tasks, full launch sequence
- `content-seo` — 7 tasks, keyword-to-traffic pipeline
- `lead-gen` — 10 tasks, lead generation funnel
- `retention` — 8 tasks, churn reduction + engagement
- `video-content` — AI-video concept and prompt-pack campaign
- `email-sequence` — lifecycle/nurture/onboarding sequence workspace
- `funnel-build` — landing page, lead magnet, email follow-up, and ad-entry workspace

### Custom
Start with blank `state-template.yaml` and add tasks manually.

---

## Multi-Project Support

Each project has isolated campaign folders:
```
clients/
├── saas-app/campaigns/launch-q2/
├── client-abc/campaigns/lead-gen/
└── newsletter/campaigns/growth-jan/
```

Switch projects: load different `clients/<project>/` context. Campaign state is fully isolated.

---

## Publishing via Postiz

### Schedule a Social Post
1. Create content (copywriter agent + social-media skill)
2. Upload media if needed (`upload` tool)
3. Schedule via `posts:create` with date/time
4. Save post_id to state.yaml

### Pull Analytics
1. Use `analytics:post` for per-post metrics
2. Use `analytics:platform` for platform-level data
3. Append to `metrics/` snapshots

### Rate Limits
- 30 requests/hour on Postiz API
- Batch operations when possible
- Space out scheduling calls

See `skills/integrations/postiz/index.md` for full setup and usage.

---

## Commands

| Command | Purpose |
|---------|---------|
| `/campaign:new` | Create campaign from template |
| `/campaign:status` | Show current campaign dashboard |
| `/campaign:next` | Execute next priority actions |
| `/campaign:schedule` | Schedule content via Postiz |
| `/campaign:metrics` | Pull latest metrics |
| `/campaign:report` | Generate performance report |

---

## Error Handling

- **Postiz unavailable**: Save content as files, mark as "ready-to-publish"
- **MCP not configured**: Show setup instructions, continue with manual workflow
- **Dependency blocked**: Skip to next available task, flag blocker
- **Asset creation fails**: Retry with different approach, log failure in state

---

## Metrics Collection

Metrics are pulled from MCPs and stored as time-series snapshots:

```yaml
metrics:
  snapshots:
    - date: "260315"
      source: google-analytics
      visitors: 342
      signups: 28
      conversion_rate: 0.082
```

Sources:
- Google Analytics → traffic, conversions, behavior
- Postiz → social engagement, reach, impressions
- HubSpot → email opens, clicks, replies
- Meta Ads → ROAS, CPC, CPL, conversions

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[client-onboarding]] (skill, 0.14)

<!-- skill-graph:end -->
