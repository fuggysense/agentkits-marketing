---
name: client-onboarding
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: core
difficulty: beginner
description: "Guided client/project onboarding flow. Scaffolds project files, interviews user to populate ICP/offer/voice/channels, routes to agents for enrichment, validates readiness, and activates session context."
triggers:
  - new project
  - onboard client
  - new client
  - set up project
  - create project
  - project setup
prerequisites: []
related_skills:
  - brand-building
  - campaign-runner
  - marketing-fundamentals
agents:
  - persona-builder
  - researcher
  - brand-voice-guardian
mcp_integrations:
  optional: []
success_metrics:
  - files_completed
  - readiness_score
  - time_to_first_campaign
output_schema: project-readiness
---

# Client Onboarding

You are a project onboarding engine. You turn "I have a new client" into a fully configured project directory ready for campaigns — through guided interview, agent enrichment, and readiness validation.

## Core Philosophy

Every campaign depends on solid foundations. Bad ICP = bad targeting. Vague offer = weak copy. Missing channels = nowhere to publish. This skill ensures those foundations are solid before any campaign begins.

**Principles:**
- Ask, don't assume — interview the user for every field
- Reuse existing agents for deep work (persona-builder, researcher, brand-voice-guardian)
- Validate before activating — catch gaps early
- One-time flow, not multi-session — get it done in one sitting

---

## Phase 1: Scaffold

### Step 1: Get Project Name

**Question:** "What's the project name? Use slug format (lowercase, hyphens)."
**Examples:** `acme-plumbing`, `saas-startup`, `fitness-coach`

### Step 2: Copy Template

```bash
cp -r "clients/_template/" "clients/<project-name>/"
mkdir -p "clients/<project-name>/campaigns"
mkdir -p "clients/<project-name>/feedback"
mkdir -p "clients/<project-name>/assets"
```

### Step 3: Check Voice Profile

Check if a voice profile exists in `voice/` (exclude `README.md` and templates).

- If exists: note which person's voice will be linked
- If not: flag as pending — "No voice profile found. You can create one later with `/brand:voice`"

---

## Phase 2: Discovery Interview

Walk through each file's fields in conversation. Ask questions from `references/discovery-questions.md`. After each section, write the answers directly to the file.

**Order:** ICP → Offer → Brand Voice → Channels

### ICP (icp.md)
Ask the ICP questions from the question bank. Write answers to `clients/<project>/icp.md`.

### Offer (offer.md)
Ask the Offer questions. Write answers to `clients/<project>/offer.md`.

### Brand Voice (brand-voice.md)
Ask the Brand Voice questions. Write answers to `clients/<project>/brand-voice.md`.

### Channels (channels.json)
Ask the Channels questions. Write answers to `clients/<project>/channels.json`.

**Interview rules:**
- Ask one section at a time (all questions for ICP, then all for Offer, etc.)
- Accept partial answers — fill what's given, mark empty fields as `[TBD]`
- Don't over-explain — keep questions conversational
- If user says "skip" for a section, leave template defaults and move on

---

## Phase 3: Enrich (Optional — Agent Routing)

After core files are populated, present enrichment options:

**Question:** "Core files are filled. Want to go deeper on any of these?"

| Option | Agent / Skill | What it does |
|--------|--------------|--------------|
| **Deep buyer persona** | `persona-builder` agent | Interactive deep-dive into ICP — demographics, psychographics, jobs-to-be-done |
| **Competitor research** | `researcher` agent | Research top 2-3 competitors — positioning, pricing, channels |
| **Voice profile** | `/brand:voice` skill | Build full V.O.I.C.E. files in `voice/<person>/` |
| **Brand validation** | `brand-voice-guardian` agent | Review messaging consistency across all files |
| **Skip** | — | Move straight to validation |

User picks which (if any) to run. Each is a HITL gate — propose the agent call, get approval, execute.

Multiple selections allowed. Run them sequentially.

---

## Phase 4: Validate

Run readiness checklist against project files. Read each file and score:

### Readiness Checklist

**ICP (icp.md):**
- [ ] Demographics section has at least Industry + Company Size filled
- [ ] Psychographics has at least 2 pain points (specific, not generic)
- [ ] "Where They Congregate" has at least 1 entry

**Offer (offer.md):**
- [ ] Price or pricing model listed
- [ ] One-Line Description filled (not empty)
- [ ] At least 1 proof element (case study, testimonial, or data point)
- [ ] Primary benefit stated

**Brand Voice (brand-voice.md):**
- [ ] At least 2 messaging pillars or tone adjustments
- [ ] At least 1 on-brand example provided

**Channels (channels.json):**
- [ ] At least 1 primary channel listed
- [ ] Market info present (if channels.json has market fields)

**Learnings & Assets:**
- [ ] `learnings.md` exists in project directory
- [ ] `assets/` directory exists

**Voice Profile:**
- [ ] Voice directory exists in `voice/` and is linked

### Asset Inventory Scan

After the checklist, scan ALL locations where marketing assets may exist for this project. Assets are not always stored inside `clients/<project>/assets/` — they may live in other repo directories.

**Scan these locations (non-empty files only):**

| Location | What lives here |
|----------|----------------|
| `clients/<project>/assets/` | Client-specific assets (images, PDFs, downloads) |
| `clients/<project>/campaigns/` | Campaign state files, plans, briefs |
| `docs/content/ads/` | Ad copy, ad scripts, image generation prompts |
| `docs/content/emails/` | Email sequences, templates |
| `docs/content/landing-pages/` | Landing page copy |
| `docs/content/social/` | Social media posts, calendars |
| `docs/content/blog/` | Blog posts, articles |
| `docs/content/` | Any other content subdirectories |

**How to scan:** List all non-`.gitkeep` files in each location. For each file found, read the first 5 lines to extract: title, date, type/format, and which project it's for.

**Output an asset inventory table:**

```
## Generated Assets

| Asset | Location | Date | Type |
|-------|----------|------|------|
| Meta Lead Gen Ads (8 variants) | docs/content/ads/meta-lead-gen-... | 260312 | Ad copy |
| Image Prompts (5 prompts) | docs/content/ads/meta-lead-gen-image-... | 260312 | Image prompts |
| ... | ... | ... | ... |

Total: X assets found
```

If no assets are found in any location, report: "No generated assets found yet."

This inventory prevents the common mistake of thinking nothing has been created when assets exist outside the client folder.

### Scoring

Count passing checks out of total. Output:

```
Readiness: X/Y sections complete
✅ Passing: [list]
❌ Missing: [list with specific gaps]
📋 Next actions: [what to fill to reach 100%]

## Generated Assets
[asset inventory table from scan above]
```

---

## Phase 5: Activate

After validation (even if not 100%):

1. **Set active context** — This project is now the session's active project
2. **Load both layers:**
   - Voice files from `voice/<person>/` (if exists)
   - Project files from `clients/<project>/`
3. **Suggest next action** — Based on channels + offer + existing assets from the inventory scan:
   - Has existing ad copy but no landing page → suggest building the landing page next
   - Has existing ad copy + landing page but no email sequence → suggest building nurture sequence
   - Has paid channels + proof elements but no ad copy → suggest `lead-gen` template
   - Has content channels (blog, newsletter) → suggest `content-seo` template
   - Has social platforms → suggest starting with organic social
   - New product / no traction yet → suggest `product-launch` template
4. **Show the suggestion:**

```
Project "<name>" is active.

Suggested first move: `/campaign:new <project> <type>`
Reason: [why this type fits their setup]
```

---

## Error Handling

- If `clients/<project-name>/` already exists: warn and ask to overwrite or pick a different name
- If template directory is missing: error — "Template not found at `clients/_template/`"
- If user abandons mid-interview: files are already saved with partial data — can resume by running `/project:validate` later
