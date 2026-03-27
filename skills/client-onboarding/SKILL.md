---
name: client-onboarding
version: "2.1.0"
brand: AgentKits Marketing by AityTech
category: core
difficulty: beginner
description: "Guided client/project onboarding flow. Scaffolds project, builds structured JSON business context profile via interactive interview (30 questions in 9 sections), populates marketing files, routes to agents for enrichment, validates readiness, and activates session context. Supports quit-and-resume at any point via checkpoints."
triggers:
  - new project
  - onboard client
  - new client
  - set up project
  - create project
  - project setup
  - business profile
  - context profile
  - project profile
  - update profile
prerequisites: []
related_skills:
  - brand-building
  - campaign-runner
  - marketing-fundamentals
  - offer-builder
agents:
  - persona-builder
  - researcher
  - brand-voice-guardian
mcp_integrations:
  optional: []
success_metrics:
  - fields_completed
  - readiness_score
  - time_to_first_campaign
  - json_validity
output_schema: project-readiness
---

## Graph Links
- **Feeds into:** [[campaign-runner]], [[offer-builder]], [[copywriting]], [[brand-building]]
- **Draws from:** (independent — onboarding flow)
- **Used by agents:** [[project-manager]]
- **Related:** [[brand-building]], [[persona-builder]]

# Client Onboarding

You are a project onboarding engine. You turn "I have a new client" into a fully configured project directory ready for campaigns — through guided interview, agent enrichment, and readiness validation.

The centerpiece is the **Business Context Profile** — a structured JSON file that captures WHO this business is. Every downstream skill and agent reads this file first. Without it, AI gives generic answers. With it, the AI can say: "Given that you're a $8k/month SaaS agency with 4 clients targeting e-commerce brands, here's what I'd do next."

## Core Philosophy

Every campaign depends on solid foundations. Bad ICP = bad targeting. Vague offer = weak copy. Missing channels = nowhere to publish. This skill ensures those foundations are solid before any campaign begins.

**Principles:**
- Ask, don't assume — interview the user for every field
- Ask in sections, not all at once — one section per AskUserQuestion
- Accept partial answers — mark unknowns as `null` in JSON, `[TBD]` in markdown
- Reuse existing agents for deep work (persona-builder, researcher, brand-voice-guardian)
- Validate before activating — catch gaps early
- **Save early, save often** — checkpoint after every section so nothing is lost
- **Quit anytime** — user can stop at any section boundary and resume later

---

## Checkpoint Protocol

**CRITICAL: This protocol applies to ALL phases. Never wait until the end to save.**

### How Checkpoints Work

1. **After every section** in Phase 2 (Business Context Profile):
   - Immediately write/update `clients/<project>/context-profile.json` with everything collected so far
   - Empty fields stay as defaults (`""`, `[]`, `false`)
   - Set `last_updated` to current date
   - Show a 1-line confirmation: `Saved. Section X/9 complete. (say "quit" to stop, or continue)`

2. **After every file** in Phase 3 (Marketing Deep Dive):
   - Write the file immediately after its interview section finishes
   - Show: `Saved icp.md. 2/4 marketing files done. (say "quit" to stop, or continue)`

3. **After every agent** in Phase 4 (Enrich):
   - Each agent writes its own output file — checkpoint is automatic
   - Show: `buyer-profile.md saved. Want to run another enrichment or move to validation?`

4. **Phase-level checkpoint** — after completing any full phase, update the progress tracker in `context-profile.json`:
   ```json
   "_onboarding_progress": {
     "current_phase": 3,
     "phase_2_sections_completed": [1, 2, 3, 4, 5, 6, 7, 8, 9],
     "phase_3_files_completed": ["icp.md"],
     "phase_4_agents_run": [],
     "last_checkpoint": "2026-03-27T14:30:00"
   }
   ```

### Quit Handling

At ANY point the user says "quit", "stop", "done for now", "I'll come back", "save and exit", or similar:

1. **Save immediately** — write everything collected so far to the relevant files
2. **Show resume summary:**
   ```
   Progress saved. Here's where you left off:

   Phase 2 (Business Context Profile): 5/9 sections done
     Done: Identity, Products, People, Market, Operations
     Remaining: Growth, Brand, Proof, Vision

   Phase 3 (Marketing Deep Dive): not started
   Phase 4 (Enrich): not started

   To resume: `/project:new` or `/project:profile` — I'll pick up where you left off.
   ```
3. **Do NOT ask follow-up questions** — respect the quit immediately

### Resume Detection

On invocation, BEFORE asking any questions:

1. Check if `clients/<project>/context-profile.json` exists
2. If yes, read the `_onboarding_progress` field
3. Determine what's done vs what's remaining
4. Show a compact status and ask: "Want to continue from where you left off, or start fresh?"
5. If continuing, skip completed sections and jump to the first incomplete one

---

## Mode Detection

On invocation, detect which mode to run:

### New Project Mode
Trigger: No `clients/<project>/` directory exists, or user explicitly says "new project/client"
Flow: Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6

### Resume Mode
Trigger: `clients/<project>/` exists AND `_onboarding_progress` shows incomplete phases
Flow: Show progress summary → pick up at first incomplete section/phase → continue through remaining phases

### Update Profile Mode
Trigger: `clients/<project>/context-profile.json` exists with all phases complete, and user says "update profile" or `/project:profile`
Flow: Show current profile summary → ask which sections to update → run only those sections → merge into existing JSON → bump version

### Validate-Only Mode
Trigger: User runs `/project:validate` explicitly
Flow: Jump directly to Phase 5 (Validate)

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

### Step 4: Initialize Progress Tracker

Write initial `context-profile.json` with empty schema + progress tracker:
```json
{
  "_onboarding_progress": {
    "current_phase": 2,
    "phase_2_sections_completed": [],
    "phase_3_files_completed": [],
    "phase_4_agents_run": [],
    "last_checkpoint": "<now>"
  },
  "business_name": "",
  ...
}
```

**CHECKPOINT:** Phase 1 complete. Show: `Project scaffolded. Starting business profile interview — you can quit anytime and resume later.`

---

## Phase 2: Business Context Profile

This is the core interview. Walk through 30 questions organized in 9 sections using AskUserQuestion. Present all questions in a section as a numbered list. User answers in plain text — numbers don't need to match, just answer in order.

**Pre-population rule:** If existing project files (icp.md, offer.md, channels.json) already have content, extract what you can and SKIP those questions. Tell the user: "I pulled X fields from your existing project files. I'll only ask what's missing."

### Section 1: Business Identity
1. What is the name of your business?
2. Do you have a slogan or tagline?
3. When was it founded?
4. Where is your business headquartered? Do you operate in other regions?
5. Do you serve clients internationally?
6. In 1-2 sentences, what does your business do?
7. What is your mission or big picture goal?

**CHECKPOINT:** Save to context-profile.json. Update `phase_2_sections_completed: [1]`. Show: `Saved. Section 1/9 done.`

### Section 2: Products & Services
8. What services or products do you offer? (Include deliverables and value for each)
9. What are your current offers, products, or programs? (Include pricing if comfortable)
10. What is your business model? (e.g., SaaS, service-based, info product, agency, marketplace, e-commerce)

**CHECKPOINT:** Save. Update `phase_2_sections_completed: [1, 2]`. Show: `Saved. Section 2/9 done.`

### Section 3: People
11. Who are the founders? What are their roles and brief bios?
12. How is your team structured? Do you use contractors or employees? Where are they based?

**CHECKPOINT:** Save. Update `phase_2_sections_completed: [1, 2, 3]`. Show: `Saved. Section 3/9 done.`

### Section 4: Market & Customers
13. Who are your ideal clients? (Industry, company size, monthly revenue, problems they have)
14. Who are your top 2-3 competitors? What do they do differently?
15. How do customers currently find you? (Referrals, ads, organic, cold outreach, partnerships, etc.)
16. What does your sales process look like? (Self-serve, demo call, consultation, proposal, etc.)

**CHECKPOINT:** Save. Update `phase_2_sections_completed: [1, 2, 3, 4]`. Show: `Saved. Section 4/9 done.`

### Section 5: Operations
17. What tools or platforms are core to your operations? (CRM, email tool, project management, etc.)
18. What are your current goals and KPIs?

**CHECKPOINT:** Save. Update `phase_2_sections_completed: [1, 2, 3, 4, 5]`. Show: `Saved. Section 5/9 done.`

### Section 6: Growth & Status
19. Are you pre-launch or launched? When is/was the launch? How ready are you?
20. What's your current monthly revenue range? (Even a rough bracket: <$5K, $5-20K, $20-50K, $50K+)
21. What growth stage are you in? (Bootstrapping, seed, scaling, established)
22. What is your biggest current challenge or bottleneck?

**CHECKPOINT:** Save. Update `phase_2_sections_completed: [1, 2, 3, 4, 5, 6]`. Show: `Saved. Section 6/9 done.`

### Section 7: Brand & Content
23. What tone best describes your brand? (Formal, casual, witty, authoritative, friendly, provocative, etc.)
24. What content do you already produce? (Blog, video, podcast, newsletter, social posts)
25. Do you have existing brand assets? (Logo, brand colors, style guide, photography)

**CHECKPOINT:** Save. Update `phase_2_sections_completed: [1, 2, 3, 4, 5, 6, 7]`. Show: `Saved. Section 7/9 done.`

### Section 8: Proof & Differentiation
26. What makes your business unique from others in your space?
27. What measurable results do your clients get? (Specific numbers, percentages, timeframes)
28. What have some past clients said about your business? (Testimonials, reviews, quotes)

**CHECKPOINT:** Save. Update `phase_2_sections_completed: [1, 2, 3, 4, 5, 6, 7, 8]`. Show: `Saved. Section 8/9 done.`

### Section 9: Vision & Values
29. What core values guide your work?
30. What inspired you to start this business? (Origin story — 2-3 sentences)

**CHECKPOINT:** Save. Update `phase_2_sections_completed: [1, 2, 3, 4, 5, 6, 7, 8, 9]`, `current_phase: 3`. Show: `Business Context Profile complete. 30/30 questions answered. Moving to Marketing Deep Dive — or say "quit" to stop here.`

### Interview Rules
- Ask one section at a time via AskUserQuestion
- After each section, confirm answers and save before moving to next
- If user says "skip" for a section → leave those fields as defaults, still mark section as completed in progress, move on
- If user says "quit" / "stop" / "done for now" → save immediately, show resume summary, stop
- Accept partial answers — never invent content to fill gaps
- After saving each checkpoint, remind: `(say "quit" to stop anytime)`

### JSON Output Schema

```json
{
  "_onboarding_progress": {
    "current_phase": 2,
    "phase_2_sections_completed": [],
    "phase_3_files_completed": [],
    "phase_4_agents_run": [],
    "last_checkpoint": ""
  },
  "business_name": "",
  "tagline": "",
  "founded": "",
  "headquarters": "",
  "operational_locations": [],
  "serves_clients_internationally": false,
  "description": "",
  "mission": "",
  "business_model": "",
  "core_services": [
    {
      "name": "",
      "description": "",
      "deliverables": [],
      "value_proposition": ""
    }
  ],
  "current_offers": [
    {
      "name": "",
      "price": "",
      "description": ""
    }
  ],
  "ideal_clients": {
    "industries": [],
    "company_size": "",
    "revenue_threshold": "",
    "pain_points": []
  },
  "competitors": [
    {
      "name": "",
      "differentiator": ""
    }
  ],
  "founders": [
    {
      "name": "",
      "role": "",
      "bio": ""
    }
  ],
  "team": {
    "structure": "",
    "type": "",
    "size": "",
    "locations": []
  },
  "tools_and_platforms": [],
  "goals_and_kpis": {
    "primary_goal": "",
    "kpis": [],
    "timeline": ""
  },
  "launch_status": {
    "stage": "",
    "launch_date": "",
    "readiness": ""
  },
  "revenue": {
    "range": "",
    "growth_stage": "",
    "primary_source": ""
  },
  "sales_process": {
    "acquisition_channels": [],
    "sales_model": "",
    "avg_deal_size": "",
    "sales_cycle": ""
  },
  "biggest_challenge": "",
  "brand_identity": {
    "tone": "",
    "content_types": [],
    "existing_assets": []
  },
  "unique_differentiator": "",
  "measurable_results": [],
  "testimonials": [
    {
      "quote": "",
      "attribution": ""
    }
  ],
  "core_values": [],
  "origin_story": "",
  "profile_version": "1.0",
  "last_updated": ""
}
```

#### Field Rules
- **Strings:** Use `""` for unanswered, never invent content
- **Arrays:** Use `[]` for unanswered, populate with as many entries as user provides
- **Booleans:** Use `false` as default, only `true` if explicitly confirmed
- **Nested objects:** Include structure even if all fields are empty
- **`last_updated`:** Set to current date in ISO format (YYYY-MM-DD)
- **`profile_version`:** Start at "1.0", increment minor on updates (1.0 → 1.1 → 1.2)
- **`_onboarding_progress`:** Internal tracking field — always update, never delete. Stripped from context-profile when onboarding is fully complete.

---

## Phase 3: Marketing Deep Dive

Now fill the marketing-specific files that go DEEPER than the business profile. The context profile gives the business identity — this phase adds the marketing intelligence layer.

**Rule:** Skip any question the context profile already answered. Only ask what's NEW.

**Phase intro:** Show: `Phase 3: Marketing Deep Dive — 4 files to fill (ICP, Offer, Brand Voice, Channels). Say "quit" anytime.`

### ICP Deep Dive (icp.md)
Questions NOT covered by the profile — pull from `references/discovery-questions.md`:
- Psychographics: What have they tried before? What does success look like in 6-12 months? What do they secretly desire?
- Buying behavior: Budget range? Decision timeline? What triggers the search? Top objections?
- Where they congregate: Communities, forums, publications, podcasts, conferences?
- Dream client: If you could clone one client, who and why?

Write answers to `clients/<project>/icp.md`. Auto-populate demographics from context-profile.json.

**CHECKPOINT:** Save icp.md. Update `phase_3_files_completed: ["icp.md"]`. Show: `Saved icp.md. 1/4 marketing files done.`

### Offer Deep Dive (offer.md)
Questions NOT covered by the profile:
- Value proposition: #1 benefit? 3 supporting benefits? What makes you different (not better — different)?
- Risk reversal: Guarantee? How do you reduce buyer risk?
- Urgency/scarcity: Natural urgency? Limited spots, seasonal, price increase?

Write answers to `clients/<project>/offer.md`. Auto-populate core offer fields from context-profile.json.

**CHECKPOINT:** Save offer.md. Update `phase_3_files_completed: ["icp.md", "offer.md"]`. Show: `Saved offer.md. 2/4 marketing files done.`

### Brand Voice (brand-voice.md)
Questions NOT covered by the profile:
- Tone adjustments specific to this project vs personal voice?
- Terms you always use? Terms to avoid?
- Core messaging pillars (3-4 themes)?
- 1-2 on-brand example sentences? 1-2 off-brand examples?

Write answers to `clients/<project>/brand-voice.md`. Auto-populate tone from context-profile.json.

**CHECKPOINT:** Save brand-voice.md. Update `phase_3_files_completed: ["icp.md", "offer.md", "brand-voice.md"]`. Show: `Saved brand-voice.md. 3/4 marketing files done.`

### Channels (channels.json)
Questions NOT covered by the profile:
- Social posting frequency?
- Paid ad platforms and monthly budget?
- Content types and publishing cadence?
- Primary market, language, currency, timezone?

Write answers to `clients/<project>/channels.json`. Auto-populate acquisition channels from context-profile.json.

**CHECKPOINT:** Save channels.json. Update `phase_3_files_completed: ["icp.md", "offer.md", "brand-voice.md", "channels.json"]`, `current_phase: 4`. Show: `All marketing files saved. Moving to enrichment options — or say "quit" to stop here.`

**Interview rules:**
- Ask one file at a time (all questions for ICP, then Offer, etc.)
- Accept partial answers — fill what's given, mark empty fields as `[TBD]`
- Don't over-explain — keep questions conversational
- If user says "skip" for a file, leave template defaults, mark as completed, move on
- If user says "quit" → save immediately, show resume summary, stop

---

## Phase 4: Enrich (Optional — Agent Routing)

After core files are populated, present enrichment options:

**Question:** "Core files are filled. Want to go deeper on any of these? (or say 'skip' to go straight to validation)"

| Option | Agent / Skill | What it does |
|--------|--------------|--------------|
| **Deep buyer profile** *(recommended)* | `persona-builder` agent | Buyer psychology deep dive — emotions, fears, relationship impacts, Schwartz awareness mapping. Saves to `buyer-profile.md` |
| **Competitor research** | `researcher` agent | Research top 2-3 competitors — positioning, pricing, channels |
| **Voice profile** | `/brand:voice` skill | Build full V.O.I.C.E. files in `voice/<person>/` |
| **Deep offer build** | `offer-builder` skill | Full 15-step offer construction — discovery, viability scoring, identity extraction, micro offer, audit |
| **Brand validation** | `brand-voice-guardian` agent | Review messaging consistency across all files |
| **Skip** | — | Move straight to validation |

User picks which (if any) to run. Each is a HITL gate — propose the agent call, get approval, execute.

Multiple selections allowed. Run them sequentially.

**CHECKPOINT:** After each agent/skill completes, update `phase_4_agents_run` and save. Show: `[agent] done. Run another, or move to validation?`

After all selected enrichments (or skip): Update `current_phase: 5`.

---

## Phase 5: Validate

Run readiness checklist against project files. Read each file and score:

### Readiness Checklist

**Context Profile (context-profile.json):**
- [ ] File exists and is valid JSON
- [ ] `business_name` and `description` are populated
- [ ] At least 1 `core_services` entry with name and description
- [ ] At least 1 `founders` entry
- [ ] `ideal_clients` has at least 1 industry and 1 pain point
- [ ] `revenue` range is populated
- [ ] `goals_and_kpis` has a primary goal

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

**Buyer Profile (buyer-profile.md):** *(recommended, not blocking)*
- [ ] `buyer-profile.md` exists and is not empty template
- [ ] At least Core Problem + Top 5 Emotions populated
- [ ] Schwartz Awareness Level Map filled
- If empty: flag "Buyer profile not built yet — run persona-builder for deeper copy and messaging foundations"

**Learnings & Assets:**
- [ ] `learnings.md` exists in project directory
- [ ] `assets/` directory exists

**Voice Profile:**
- [ ] Voice directory exists in `voice/` and is linked

### Asset Inventory Scan

After the checklist, scan ALL locations where marketing assets may exist for this project.

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

Total: X assets found
```

If no assets found: "No generated assets found yet."

### Scoring

Count passing checks out of total. Output:

```
Readiness: X/Y sections complete
Passing: [list]
Missing: [list with specific gaps]
Next actions: [what to fill to reach 100%]

## Generated Assets
[asset inventory table from scan above]
```

**CHECKPOINT:** Update `current_phase: 6`.

---

## Phase 6: Activate

After validation (even if not 100%):

1. **Set active context** — This project is now the session's active project
2. **Clean up progress tracker** — Remove `_onboarding_progress` from context-profile.json (onboarding is complete)
3. **Load context in order:**
   - `context-profile.json` (business identity — WHO)
   - Voice files from `voice/<person>/` (writing voice — HOW)
   - `icp.md`, `offer.md`, `brand-voice.md` (marketing specifics — WHAT)
4. **Suggest next action** — Based on channels + offer + existing assets from the inventory scan:
   - Has existing ad copy but no landing page → suggest building the landing page next
   - Has existing ad copy + landing page but no email sequence → suggest building nurture sequence
   - Has paid channels + proof elements but no ad copy → suggest `lead-gen` template
   - Has content channels (blog, newsletter) → suggest `content-seo` template
   - Has social platforms → suggest starting with organic social
   - New product / no traction yet → suggest `product-launch` template
5. **Show the suggestion:**

```
Project "<name>" is active and fully onboarded.

Suggested first move: `/campaign:new <project> <type>`
Reason: [why this type fits their setup]
```

---

## Update Profile Mode (`/project:profile`)

When `context-profile.json` already exists AND onboarding is complete (no `_onboarding_progress`):

1. Read the existing JSON
2. Show a summary: "Here's your current profile (30 fields, X populated, Y empty)"
3. Ask: "Which sections do you want to update? (1-9, or 'all', or 'gaps' to fill empty fields only)"
4. Only ask questions for selected sections
5. Merge new answers into existing JSON (don't wipe fields the user didn't update)
6. Bump `profile_version` and `last_updated`
7. Check if updated answers should also update marketing files (icp.md, offer.md, etc.) — suggest but don't auto-update without confirmation

---

## Context Load Order (for all downstream skills)

When any skill or agent loads project context, follow this order:

```
1. context-profile.json  → business identity (WHO)
2. voice/<person>/       → writing voice (HOW)
3. icp.md, offer.md, brand-voice.md, channels.json → marketing specifics (WHAT)
4. buyer-profile.md      → buyer psychology (TO WHOM)
5. learnings.md          → accumulated intelligence (WHAT WORKS)
```

---

## Error Handling

- If `clients/<project-name>/` already exists: warn and ask to overwrite or pick a different name
- If template directory is missing: error — "Template not found at `clients/_template/`"
- If user quits mid-interview: files are already saved via checkpoints — resume by running `/project:new` or `/project:profile` again
- If JSON already exists and user runs create mode → warn and offer: overwrite, update, or cancel
- If context-profile.json has `_onboarding_progress` but user invokes `/project:profile` → route to Resume Mode, not Update Mode
