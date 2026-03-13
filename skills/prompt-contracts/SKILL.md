---
name: prompt-contracts
version: "2.0.0"
brand: AgentKits Marketing by AityTech
category: quality-assurance
difficulty: beginner
description: >
  Define success, constraints, output format, AND explicit failure conditions in a single structured
  contract before execution. Auto-triggers on high-stakes deliverables. Includes contract library
  for reuse and Reverse Prompt workflow to extract contracts from winning assets.
triggers:
  - prompt contract
  - write a contract
  - define success criteria
  - failure conditions
  - spec this out
  - what does done look like
  - define the contract
  - structured spec
  - goal constraints format failure
  - reverse prompt
  - reverse engineer this
  - make more like this
  - what made this work
  - save this contract
prerequisites: []
related_skills:
  - verification-loops
  - multi-agent-consensus
  - campaign-runner
agents:
  - planner
  - project-manager
---

# Prompt Contracts

Define a 4-part contract before implementation: **GOAL** (quantifiable success), **CONSTRAINTS** (hard limits), **FORMAT** (exact output shape), **FAILURE** (explicit conditions that mean "not done"). The agent treats this as an engineering spec with zero ambiguity about what "done" means.

**Why this works:** Agents hallucinate and over-engineer when success is undefined. They silently cut corners when failure is undefined. A prompt contract front-loads all the reasoning about scope and edge cases. The FAILURE clause is the key innovation — it prevents the agent from taking shortcuts it would otherwise rationalize as acceptable.

## Language & Quality Standards

**CRITICAL**: Respond in the same language the user is using.

## When to Use This Skill

- Campaign briefs before execution
- Content creation specs (blog posts, landing pages, email sequences)
- Ad creative briefs with performance targets
- Any deliverable where quality matters more than speed
- When you want to prevent "it technically works but..." outcomes

**NOT for:** Quick brainstorming, rough drafts, exploratory tasks where requirements are still forming.

## Execution

### 1. Receive the task

Read the user's request. Determine whether they've already provided a contract or need help writing one.

**If the user provides a contract:** Parse it into the 4 sections and proceed to validation (step 3).

**If the user provides a plain task:** Help them convert it into a contract (step 2).

### 2. Generate the contract

If the user gave a plain task description, convert it into a structured contract. Use what you know from the project context (ICP, brand voice, offer) and reasonable defaults.

Present the draft contract to the user for approval before proceeding.

#### Contract template:

```markdown
## Contract

GOAL: [What does success look like? Include a measurable metric.]

CONSTRAINTS:
- [Hard limit 1 — brand, scope, or resource constraint]
- [Hard limit 2]
- [Hard limit 3]

FORMAT:
- [Exact output shape — files, structure, what's included]
- [File naming and organization]
- [What to include — sections, elements, assets]

FAILURE (any of these = not done):
- [Specific failure condition 1]
- [Specific failure condition 2]
- [Edge case that must be handled]
- [Quality bar that must be met]
```

#### Writing good GOAL statements:
- Include a number: "3 ad variants with distinct hooks" not "some ad options"
- Be specific: "landing page with <8 second load, 3 CTAs, hero + 4 sections" not "a landing page"
- Define the user-visible outcome: "email sequence that handles 3 objections and ends with demo CTA" not "nurture sequence"

#### Writing good CONSTRAINTS:
- Only hard limits — things that are NOT negotiable
- Brand constraints: "must use brand voice from voice/ files", "no emoji in headlines"
- Scope constraints: "single page", "under 500 words", "max 5 emails in sequence"
- Channel constraints: "must work for Meta Ads 1:1 format", "email subject <50 chars"

#### Writing good FORMAT:
- Exact file structure: "save to `clients/{project}/campaigns/{name}/`"
- What to include: "headline variants (3), body copy, CTA text, meta description"
- What to exclude: "no stock photo suggestions", "no implementation timeline"

#### Writing good FAILURE clauses:
This is the most important section. Think about how the task could "technically work" but actually be wrong:
- Missing audience: "doesn't address the ICP's primary objection"
- Generic copy: "uses phrases like 'cutting-edge', 'leverage', or 'unlock'"
- No proof: "claims without specific numbers or examples"
- Wrong tone: "doesn't match brand voice guidelines"
- Incomplete: "CTA doesn't specify next step for the reader"
- Over-engineered: "adds sections not required by GOAL"

### 3. Validate the contract

Before implementing, check that the contract is:
- **Complete** — all 4 sections filled out
- **Consistent** — CONSTRAINTS don't contradict GOAL
- **Testable** — every FAILURE condition can be mechanically verified
- **Scoped** — GOAL is achievable within the CONSTRAINTS

If anything is ambiguous, ask the user to clarify before proceeding.

### 4. Implement against the contract

Build the solution. Treat each section as a hard requirement:
- **GOAL**: The thing you're optimizing for
- **CONSTRAINTS**: Boundaries you cannot cross
- **FORMAT**: Exact shape of your output
- **FAILURE**: Conditions you must actively prevent

As you implement, mentally check each FAILURE condition. If you catch yourself about to violate one, stop and fix it before moving on.

### 5. Self-verify against FAILURE conditions

Before delivering, run through every FAILURE condition as a checklist:

```markdown
## Contract Verification

- [ ] FAILURE 1: {condition} → VERIFIED: {how you confirmed it passes}
- [ ] FAILURE 2: {condition} → VERIFIED: {how you confirmed it passes}
- [ ] FAILURE 3: {condition} → VERIFIED: {how you confirmed it passes}
- [ ] GOAL metric met: {evidence}
- [ ] All CONSTRAINTS respected: {confirmation}
- [ ] FORMAT matches spec: {confirmation}
```

If any FAILURE condition is violated, fix it before delivering. The contract says "any of these = not done" — respect that literally.

### 6. Deliver with contract status

Present the output alongside the contract verification:

```
Contract status: ALL PASS

GOAL: ✓ {metric achieved — show evidence}
CONSTRAINTS: ✓ {all respected}
FORMAT: ✓ {matches spec}
FAILURE conditions: ✓ {all verified — none triggered}
```

If any condition failed and couldn't be resolved, be explicit:

```
Contract status: 1 FAILURE

GOAL: ✓
CONSTRAINTS: ✓
FORMAT: ✓
FAILURE conditions: 1 of 4 failed
  - FAILED: "must include 3 customer proof points" — only found 2 verified examples
  - Reason: {why it failed}
  - Options: {what could fix it — additional research, relaxed constraint, etc.}
```

## Marketing Contract Examples

### Ad creative brief:
```
GOAL: 3 Meta ad variants (1:1 format) for cold audience targeting {ICP}, each with a distinct hook angle.

CONSTRAINTS:
- Primary text: 125 chars max (before "See more")
- Must use brand voice from voice/ files
- No competitor mentions by name
- Static image ads only (no video)

FORMAT:
- 3 variants, each with: headline, primary text, description, CTA button text
- Save to clients/{project}/campaigns/{name}/ad-creative.md

FAILURE:
- All 3 variants use the same hook angle
- Any variant uses generic phrases ("cutting-edge", "game-changing", "unlock")
- Primary text exceeds 125 chars
- No clear value proposition in first line
- CTA doesn't match the offer (e.g., "Shop Now" for a free trial)
```

### Landing page spec:
```
GOAL: Landing page copy converting cold traffic from Meta ads to demo booking. Target: addresses top 3 ICP objections.

CONSTRAINTS:
- Above-fold hero must work without scrolling
- Max 6 sections (hero + 5)
- No pricing on page (handled in demo)
- Must reference offer.md positioning

FORMAT:
- Hero: headline, subheadline, CTA, social proof line
- Sections: problem, solution, proof, objection handling, final CTA
- Save to clients/{project}/campaigns/{name}/landing-page.md

FAILURE:
- Hero headline doesn't pass the "so what?" test
- No social proof (numbers, logos, or testimonials)
- Objection section doesn't address ICP's #1 objection from icp.md
- Multiple CTAs with different asks (confused conversion path)
- Copy reads as AI-generated (see anti-AI patterns in context/writing/)
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| verify | true | Run self-verification before delivering |
| strict | true | Fail the task if any FAILURE condition is triggered |
| template | standard | Contract template (standard, minimal, detailed) |

## Edge cases

- **User provides incomplete contract**: Fill in missing sections with reasonable defaults and confirm with the user.
- **FAILURE conditions conflict with GOAL**: Flag the contradiction. Ask which takes priority.
- **Can't verify a FAILURE condition**: Note it as "UNVERIFIABLE" and explain why. Suggest how the user can verify manually.
- **Contract is overkill for the task**: If the task is trivial, say so. Suggest skipping the contract or using a minimal version (GOAL + FAILURE only).

---

## Auto-Trigger Rule

**Do not wait for the user to ask for a contract.** Auto-generate one before executing any of these task types:

| Task Type | Why |
|-----------|-----|
| Ad creative (any platform) | Wrong specs = wasted spend |
| Landing page copy | Conversion depends on precision |
| Email sequences (3+ emails) | Scope creep kills sequences |
| Campaign briefs | Ambiguity = misaligned execution |
| Client-facing deliverables | Quality bar must be explicit |
| Website builds | Design specs need hard constraints |

**How it works:**
1. Detect the task type from the user's request
2. Draft a quick contract (can be minimal — GOAL + FAILURE is enough for simple tasks)
3. Show it inline: "Here's the contract I'll work against — adjust anything before I start."
4. User says "go" (or tweaks) → execute against it
5. If user says "skip" → proceed without contract

This adds ~30 seconds of upfront alignment and saves hours of rework.

---

## Contract Library

Save proven contracts for reuse. When a contract produces a successful deliverable, save it as a reusable template.

### Save pattern
```
clients/<project>/contracts/
├── meta-ad-cold-v1.md
├── welcome-sequence-v2.md
├── landing-page-demo-v1.md
└── ...
```

### Contract file format
```markdown
---
name: meta-ad-cold
version: 1
created: YYMMDD
last_used: YYMMDD
success_rate: "3/3 deliverables passed verification"
---

GOAL: ...
CONSTRAINTS: ...
FORMAT: ...
FAILURE: ...
```

### When to save
- Deliverable passed all FAILURE conditions AND user approved the output
- Ask: "This contract worked well — save it for reuse?" (auto-execute, no gate needed)

### When to reuse
- Before generating a new contract, check `clients/<project>/contracts/` for a match
- If found: "I have a proven contract for this type of task — want to reuse it or start fresh?"
- Reused contracts inherit the version number and get bumped on modification

### When to update
- If a deliverable passes contract but user requests changes → update the FAILURE conditions to catch that gap next time
- Bump version: `meta-ad-cold-v1.md` → `meta-ad-cold-v2.md`

---

## Reverse Prompt → Contract

Take something that already works (a winning ad, high-converting page, great email) and reverse-engineer it into a reusable contract. This captures "what made it good" as a reproducible spec.

### When to use
- User says "make more like this" or "this one worked, do another"
- A campaign has a clear winner and you need to scale it
- Onboarding a new project where good examples exist but no contracts do

### Process

#### 1. Receive the reference
User provides the winning asset — could be text, a URL, a screenshot, or a file.

#### 2. Decompose what made it work
Analyze the reference and extract:

| Element | Question |
|---------|----------|
| **GOAL** | What did this achieve? What metric would prove success? |
| **Structure** | How is it organized? What sections/elements are present? |
| **Constraints** | What did it NOT do? (no jargon, no pricing, short paragraphs, etc.) |
| **Tone** | What voice/style choices were made? |
| **Hooks** | What grabs attention in the first line/fold? |
| **Proof** | What evidence or social proof is included? |
| **CTA** | What's the ask, and how is it framed? |
| **Anti-patterns** | What common mistakes does it avoid? |

#### 3. Generate the contract
Convert the decomposition into a standard 4-part contract:

- **GOAL** ← from what it achieved + structure
- **CONSTRAINTS** ← from what it avoided + tone choices
- **FORMAT** ← from structure + elements present
- **FAILURE** ← invert the anti-patterns + what would break the magic

#### 4. Present for refinement
Show the user: "Here's the contract I reverse-engineered from your reference. This is what made it work — anything to adjust?"

#### 5. Save to library
Save to `clients/<project>/contracts/` with a `reverse_engineered_from` field in the frontmatter linking back to the original asset.

### Example

**Input:** User shares a Meta ad that got 4.2% CTR

**Reverse-engineered contract:**
```
GOAL: Meta ad (1:1 static) for cold audience. Hook stops scroll in <1 second.
Target: >3% CTR.

CONSTRAINTS:
- Primary text: 2 lines max before "See more"
- No feature lists — one sharp benefit only
- Conversational tone, not corporate
- No stock photo aesthetic

FORMAT:
- Headline: question format, under 40 chars
- Primary text: open with surprising stat or contrarian claim
- Image: founder photo or product-in-use (not mockup)
- CTA: "Learn More" (low commitment for cold)

FAILURE:
- Opens with brand name (nobody cares yet)
- Uses "we" before establishing relevance to reader
- Headline is a statement, not a question or challenge
- More than one idea per ad (confused message)
- Image looks like a template or AI-generated
```

This contract can now produce 10 more ads with the same DNA as the winner.
