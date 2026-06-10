# Image-Generation Integration Plan

**Date:** 2026-05-19 SGT
**Author:** vid-director synthesis from 4-agent parallel research swarm
**Status:** AWAITING APPROVAL (Phase 5 of 6 — execution blocked on Jerel's sign-off)
**Inputs:** `/tmp/image-gen-research/agent-{A,B1,B2,C}-*.md`

---

## Executive Summary

The two `image-generation` skills are **architecturally complementary, not duplicative.** Research confirmed they serve different tiers of a single coherent pipeline:

- **Marketing skill** = Tier-1 orchestrator (intent routing + HITL gate + Vertex direct backend + carousel mode)
- **Global `higgsfield` skill** = Tier-2 CLI router (sub-area dispatch)
- **higgsfield-prompts skill** = Tier-3 executor (Higgsfield CLI payload formatter, IMAGE_HANDOFF receiver)
- **`gpt-image-2-director`** = independent peer (GPT Image 2.0 prompt engineering)

**Recommendation: Option B — Split by Layer (clean boundaries, fix anomalies, no content moves).** Merging the two is explicitly contraindicated by the consumer dependency map.

**Net effort:** ~30 minutes of surgical edits across 6 files. Zero high-risk sections touched.

**Net token savings:** ~10 lines from Marketing skill (broken pointer rewrite) + 2 reference files un-orphaned + 1 empty file resolved. Real win is **drift prevention**, not token reduction.

---

## Current Architecture (verified by research)

```
USER REQUEST
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ TIER 1: Marketing/skills/image-generation                    │
│ (521 lines SKILL.md + 450 lines references)                  │
│                                                              │
│ • Thin-Stack Routing Gate — intent → which downstream tool  │
│ • Vertex AI Direct Backend (Imagen / NB2 / NB Pro via API)  │
│ • HITL Prompt Review Gate (mandatory before generate)        │
│ • TikTok Photo Mode Carousel templates                       │
│ • Video Reference Image Mode (handoff to video-director)     │
│ • Marketing-flavor JSON prompt schema                        │
│ • Iteration protocol + failure diagnostics                   │
└─────┬───────────────────────────────┬───────────────────────┘
      │                               │
      │ (route: Higgsfield CLI)       │ (route: GPT Image 2.0)
      ▼                               ▼
┌──────────────────────────────┐   ┌─────────────────────────────┐
│ TIER 2: ~/.claude/skills/    │   │ ~/.claude/skills/           │
│ higgsfield/SKILL.md          │   │ gpt-image-2-director/       │
│ (162 lines, CLI router)      │   │ SKILL.md (247 lines, peer)  │
│                              │   │                             │
│ Step -1: viral preset hard   │   │ Format A: JSON for layouts  │
│         redirect             │   │ Format B: cinematic prose   │
│ Step 0: CLI auth check       │   │ Format C: meta-prompt       │
│ Sub-areas table → loads      │   │ Routes face-lock/product    │
│  references/<area>/_index.md │   │   back to higgsfield        │
└──────┬───────────────────────┘   └─────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────┐
│ TIER 2.5: ~/.claude/skills/higgsfield/references/  │
│ Sub-area reference packages (NOT standalone skills) │
│  • generate/    (full model catalog + patterns)    │
│  • soul-id/     (face-faithful training)           │
│  • product-photoshoot/  (brand product images)     │
│  • marketplace-cards/   (Amazon/Shopee listings)   │
│  • marketing-studio/    (avatar+product ad pipe)   │
└────────────────────────────────────────────────────┘
       │
       ▼ (when payload construction needed for higgsfield_generate)
┌─────────────────────────────────────────────────────────────┐
│ TIER 3: higgsfield-prompts/skills/media/image-generation     │
│ (447 lines SKILL.md + 4,715 lines across 18 references)      │
│                                                              │
│ • Model selection table (14 models)                          │
│ • Workflow D: IMAGE_HANDOFF schema v2 (research → image)     │
│ • Brand book deliverables (multi-asset batches)              │
│ • Format-Specific References (18 reference files)            │
│ • Batch generation (Visual DNA lock, parallel requests)      │
│ • Error handling                                             │
└─────────────────────────────────────────────────────────────┘
       ▲
       │
   Upstream callers (Tier 1 in higgsfield-prompts):
   brand-analyser, product-analyser, 8 workflow-generation flows
```

**This is a working layered architecture.** Each tier owns one responsibility. Nothing is duplicated at the level of behavior.

---

## Research Findings

### Inventory facts

| Skill | Files | Total lines | Role |
|---|---|---|---|
| Marketing `image-generation` | 5 (+ DS_Store) | ~1,221 | Tier-1 orchestrator |
| `~/.claude/skills/higgsfield` | 1 SKILL + ~20 refs | ~162 SKILL + sub-areas | Tier-2 router |
| `~/.claude/skills/gpt-image-2-director` | 1 SKILL | 247 | Peer prompt engineer |
| higgsfield-prompts `image-generation` | 19 (SKILL + 18 refs) | ~5,162 | Tier-3 executor |

### Anomalies surfaced (must fix regardless of architecture choice)

| # | Where | Anomaly | Severity |
|---|-------|---------|---------|
| 1 | Marketing SKILL.md lines 40-53 | Routes to `higgsfield-product-photoshoot`, `higgsfield-soul-id`, `higgsfield-marketplace-cards`, `higgsfield-generate` as if they are standalone skills. They are not — they are `references/<area>/` sub-packages of the global `higgsfield` skill. Callers checking `Skill("higgsfield-product-photoshoot")` would fail. | HIGH |
| 2 | Marketing SKILL.md line 57 | Cross-skill reference to `../video-director/references/vertex-ai-api.md`. Fragile — silently breaks if video-director moves. | MEDIUM |
| 3 | Marketing references/*.md | Both reference files (`nano-banana-examples.md`, `nano-banana-full-guide.md`) start with `## Graph Links` instead of YAML frontmatter — created from a template with the frontmatter stripped. | LOW (cosmetic) |
| 4 | Marketing skill-graph block | Only `[[video-director]]` (0.24) is listed despite the prose routing to ≥4 neighbors (`tiktok-slideshows`, `higgsfield`, `gpt-image-2-director`, `video-factory`). Graph is incomplete. | LOW |
| 5 | higgsfield-prompts references | `soul-v2-avatar.md` and `soul-v2-ugc-character.md` cited 5+ times across SKILL.md and downstream boards. **Files do not exist on disk.** | HIGH |
| 6 | higgsfield-prompts references | `ugc-boards.md` is 1 line — empty file despite being a Format-Specific Reference entry. | MEDIUM |
| 7 | Marketing corrections.md | Empty (no entries). Either the correction-capture hook isn't writing here OR the skill genuinely hasn't been corrected. | LOW |

### Top-3 LOAD-BEARING sections (do not touch without coordinated caller updates)

1. **Marketing Thin-Stack Routing Gate** — 8+ callers route through this at runtime (ad-concept-engine Phase 3a, video-director Image-First pipeline, tiktok-slideshows, creative-pipeline workflow, ugc-creator, video-factory, video-prompt-pack-builder, routing-table)
2. **Vertex/NB2 JSON Prompt Schema** (Marketing) — 4+ skills pass NB2 JSON directly. ad-concept-engine Phase 3a explicitly states: *"NB2 JSON prompts produced in Phase 2a are passed directly — image-generation knows how to render them."* This is a data contract.
3. **IMAGE_HANDOFF schema v2** (higgsfield-prompts Workflow D) — 8+ workflow-generation flows + brand-analyser + product-analyser produce this schema. Coupling contract between Tier-1 analysts and Tier-3 executor.

### Orphan callers (low-impact, surface but don't act on)

- `script-skill/SKILL.md` and `linkedin-content` — listed as image-generation callers in `creative-pipeline.md` line 171, but no specific section dependency identified. May be stale references.

---

## Architectural Options Evaluated

### Option A — Status Quo + Anomaly Fixes Only
**What:** Leave both skills in place at their current tiers. Fix the 7 anomalies. No restructuring.
**Pros:** Lowest risk. Zero caller updates. Preserves the working architecture.
**Cons:** Doesn't address the fact that Marketing's routing pointers are pointing at things that aren't standalone skills (could continue to confuse future readers).
**Verdict:** Viable baseline.

### Option B — Split by Layer (RECOMMENDED) ⭐
**What:**
- Lock in the existing tiered architecture explicitly.
- Update Marketing skill's routing language to reflect reality (point at `higgsfield` skill with sub-area hint, not at non-existent standalone skills).
- Fix all 7 anomalies.
- Add a tier-architecture preamble at the top of each skill so future drift is harder.
- Update skill-graph for Marketing to include the real neighbors.

**Pros:**
- Single source of truth per tier (matches user's simplicity bias).
- Routing pointers become accurate.
- Drift prevention via architectural preamble.
- Minimal change risk — high-risk sections untouched.

**Cons:**
- Two skills still exist with similar names. Some conceptual overlap will remain at the "what does this skill do" level (both deal with images).

**Verdict:** Strongly recommended. Matches the actual architecture; clarifies what was already true.

### Option C — Merge into Marketing (REJECTED)
**What:** Move higgsfield-prompts content into Marketing skill.
**Pros:** One skill to maintain.
**Cons:**
- Agent-C explicit warning: *"Merging sections between them risks collapsing two distinct responsibilities into one file, confusing orchestrators with executors."*
- Marketing skill bloats from 521 → ~5,500+ lines.
- Marketing repo would own higgsfield-CLI-specific content, misplaced.
- Breaks the Tier 1/Tier 3 separation that 8+ callers depend on.
**Verdict:** Rejected by data.

### Option D — Extract Shared Helper Skill (REJECTED)
**What:** Create third skill `image-prompts-shared` for cross-tier shared content.
**Pros:** DRY in theory.
**Cons:**
- The actual "shared" content is small (~10 lines of model name reference).
- Adds a third file, three-way routing complexity, new entry in routing-table.
- Solves a problem we don't have.
**Verdict:** Rejected — adds indirection without payoff.

---

## RECOMMENDED OPTION: B — Split by Layer

### Why this option

1. **It matches the architecture that already works.** Research surfaced ~30 callers depending on the two-tier split. None depend on merge.
2. **It honors your simplicity bias correctly.** Simplicity here means *clean boundaries per skill*, not *one file with everything*. Merging would actually hurt readability and increase coupling.
3. **It's reversible.** Every change is a surgical Edit, not a rewrite. `git stash` undoes any individual step.
4. **It fixes the dangerous bits.** Broken pointers and missing reference files get caught now instead of failing during the next runtime call.

---

## Migration Steps (Phase 6, gated on approval)

### Group 1: Marketing skill pointer fixes (HIGH priority)

#### Step 1.1 — Fix Thin-Stack Routing Gate pointer language
**File:** `Marketing/skills/image-generation/SKILL.md`
**Lines:** 40-53
**Change:** Rewrite the routing table to clarify that the "downstream" entries are sub-areas of the `higgsfield` skill, not standalone skills.

Before:
```
| Product photos... | `higgsfield-product-photoshoot` |
| Marketplace listing images... | `higgsfield-marketplace-cards` |
```

After:
```
| Product photos... | `higgsfield` skill → sub-area `product-photoshoot` |
| Marketplace listing images... | `higgsfield` skill → sub-area `marketplace-cards` |
```

Add 1-line note above the table: *"Sub-areas are reference packages under `~/.claude/skills/higgsfield/references/<area>/` — invoke the `higgsfield` skill with intent context; the router handles the sub-area dispatch."*

**Rollback:** Edit reverts the table to the original wording.

#### Step 1.2 — Fix the fragile Vertex AI cross-reference
**File:** `Marketing/skills/image-generation/SKILL.md`
**Line:** 57 (the `../video-director/references/vertex-ai-api.md` reference)
**Change:** Inline the 3-4 lines of Vertex setup needed here OR move that file to a shared location (`Marketing/skills/image-generation/references/vertex-ai-api.md` — keep a copy local).
**Decision needed:** copy-vs-move. Default = copy (no caller breakage).

**Rollback:** Delete the local copy.

#### Step 1.3 — Add tier-architecture preamble
**File:** `Marketing/skills/image-generation/SKILL.md`
**Insert at:** Top of file body, just below YAML (line ~30 area).
**Content:** ~10-line block describing the 3-tier architecture so future editors don't accidentally collapse boundaries. Quote: *"This is Tier-1. We route or run-Vertex. We never format `higgsfield_generate` payloads directly — that's Tier-3 in higgsfield-prompts."*

**Rollback:** Delete the block.

### Group 2: Marketing skill cosmetic fixes (LOW priority)

#### Step 2.1 — Fix orphan `## Graph Links` headers in reference files
**Files:**
- `Marketing/skills/image-generation/references/nano-banana-examples.md`
- `Marketing/skills/image-generation/references/nano-banana-full-guide.md`
**Change:** Add proper YAML frontmatter (skill, type, parent) or remove the orphan `## Graph Links` header.

**Rollback:** Revert via git.

#### Step 2.2 — Update skill-graph block
**File:** `Marketing/skills/image-generation/SKILL.md` (lines 514-521)
**Change:** Either regenerate via `scripts/link-skills.py` OR manually add the missing edges: `[[higgsfield]]`, `[[gpt-image-2-director]]`, `[[tiktok-slideshows]]`, `[[video-factory]]`.

Prefer regen — let the linker compute weights. Note: linker is `skills/_meta/link-skills.py` or similar — confirm path first.

**Rollback:** Revert via git.

### Group 3: higgsfield-prompts skill anomaly fixes (HIGH priority)

⚠️ **This is in a different repo (`~/AI workflows/higgsfield-prompts/`). Confirm before editing — this plan covers cross-repo work.**

#### Step 3.1 — Resolve `soul-v2-avatar.md` + `soul-v2-ugc-character.md` orphans
**File:** `higgsfield-prompts/skills/media/image-generation/SKILL.md` + 4 downstream board files
**Change:** Either (a) create the two missing reference files with placeholder content + TODO note, OR (b) remove the 5+ references that point to them.
**Decision needed:** create-vs-remove. Default = remove the references unless you actually want those files to exist.

**Rollback:** Revert via git.

#### Step 3.2 — Resolve empty `ugc-boards.md`
**File:** `higgsfield-prompts/skills/media/image-generation/references/ugc-boards.md`
**Change:** Either populate with 3-slot UGC board template OR remove the reference from the Format-Specific References table in SKILL.md line 135.
**Decision needed:** populate-vs-remove. Default = remove the reference for now; populate later when you actually use 3-slot UGC boards.

**Rollback:** Revert via git.

### Group 4: Verification (after all Groups complete)

#### Step 4.1 — Grep verification
Run:
```bash
grep -rln "higgsfield-product-photoshoot\|higgsfield-soul-id\|higgsfield-marketplace-cards\|higgsfield-generate" "<Marketing-root>" --exclude-dir=_archive --exclude-dir=.git
```
**Pass criteria:** Zero matches in Marketing/skills/image-generation/SKILL.md. The rest of the matches (routing-table.md, routing-overrides.md) should be marked as documentation-only references.

#### Step 4.2 — Refresh routing-table.md
Run: `node .claude/hooks/refresh-registry.js` (or whatever the registry refresher is). Confirm `image-generation` still appears with accurate triggers + description.

#### Step 4.3 — Smoke test the routing
Invoke the skill in a fresh session with a test prompt: *"Generate a product hero shot for a luxury watch."* Confirm it:
1. Triggers `image-generation`
2. Routes to `higgsfield` sub-area `product-photoshoot` (not a phantom `higgsfield-product-photoshoot` skill)
3. Hits the HITL prompt review gate before generation

---

## Caller Updates Needed

Most callers reference `image-generation` by skill name only and won't break. The two that need attention:

| Caller | What to update | Severity |
|---|---|---|
| `Marketing/.claude/rules/routing-table.md` (auto-generated) | Auto-refreshes after the SKILL.md description changes. No manual edit. | Auto-handled |
| `Marketing/.claude/rules/routing-overrides.md` | Currently routes `image-generation` to `image-generation` skill — keep, but add a one-liner clarifying it's the Marketing Tier-1 orchestrator, not the higgsfield-prompts Tier-3 executor. | Manual, low |

Orphan callers (`script-skill`, `linkedin-content`) flagged by Agent-C in `creative-pipeline.md` line 171 — leave alone for now. They reference image-generation generically; if they fail at runtime, we'll know.

---

## Token-Cost Estimate

| Skill | Before | After | Δ |
|---|---|---|---|
| Marketing/skills/image-generation/SKILL.md | 521 lines | ~525 lines | +4 (tier preamble - 6 from compressed routing table) = net ~−2 |
| Marketing references | 450 lines | 458 lines | +8 (proper frontmatter) |
| higgsfield-prompts SKILL.md + references | 5,162 lines | ~5,154 lines | −8 (orphan ref removal) |

**Net:** Essentially flat. The win is correctness + drift prevention, not bytes saved.

---

## Verification Checklist (post-execution)

- [ ] Grep `Marketing/skills/image-generation/SKILL.md` for the 4 phantom skill names — should return 0 outside table cells that explicitly say "sub-area X".
- [ ] `node .claude/hooks/refresh-registry.js` runs clean
- [ ] `image-generation` shows up in fresh-session skill list with correct triggers
- [ ] Test prompt routes correctly through Tier 1 → Tier 2 → sub-area
- [ ] HITL gate fires before any generation
- [ ] `ls higgsfield-prompts/skills/media/image-generation/references/soul-v2-avatar.md` either returns the file OR confirms it's been removed from references
- [ ] `wc -l higgsfield-prompts/skills/media/image-generation/references/ugc-boards.md` — either >1 line OR removed from Format-Specific References table
- [ ] Marketing skill-graph block contains ≥4 edges
- [ ] Run `ad-concept-engine` Phase 3a smoke test — confirms NB2 JSON Prompt Schema still consumes correctly
- [ ] Run `video-director` Image-First pipeline smoke test — confirms reference image generation works
- [ ] Run `tiktok-slideshows` smoke test — confirms carousel handoff works

---

## Rollback Path

Each Step is independently revertible via `git stash` or `git checkout`. The plan is structured so:
- **Group 1 (Marketing pointer fixes)** can revert without touching higgsfield-prompts repo
- **Group 3 (higgsfield-prompts fixes)** can revert without touching Marketing repo
- **Group 2 (cosmetic)** is purely additive — no revert needed if it goes wrong, just remove

Commit each Group as a separate commit:
```bash
git commit -m "image-gen: fix Marketing routing pointers (Tier-1)"
git commit -m "image-gen: tier-architecture preamble"
git commit -m "image-gen: cosmetic — frontmatter, skill-graph regen"
# (Group 3 commits separately in higgsfield-prompts repo)
```

---

## Non-Goals

- **NOT touching the high-risk sections** (Thin-Stack Routing Gate, NB2 JSON Schema, IMAGE_HANDOFF schema). They're load-bearing; 8+ callers depend on each.
- **NOT merging the two skills.** Agent-C's data rejects this.
- **NOT changing skill names.** Renaming would require updating ~30 callers across two repos.
- **NOT investigating the orphan callers** (`script-skill`, `linkedin-content`). Out of scope; if they fail we'll diagnose then.
- **NOT auditing the corrections.md hook.** Marketing corrections.md is empty — likely a hook config issue. Separate ticket.

---

## Outstanding Decisions for Jerel

Before execution, three small decisions:

1. **Step 1.2 (Vertex AI cross-reference):** Copy or move `vertex-ai-api.md` to live alongside Marketing's image-generation? Default = copy.
2. **Step 3.1 (soul-v2-avatar orphans):** Create stubs for the missing files, or remove the references? Default = remove.
3. **Step 3.2 (empty ugc-boards.md):** Populate now, or remove from Format-Specific References table? Default = remove.

You can reply "all defaults" to accept the recommended path, or override individually.

---

## What This Plan Does NOT Solve

- The general drift between Marketing repo and higgsfield-prompts repo. They live in different filesystems, can drift independently. A real fix would be a CI check that grep's for cross-references and flags broken pointers. Out of scope here.
- The fact that Marketing skill's `routing-table.md` (auto-generated) lists `image-generation` triggers but the actual auto-route table at the top of that file doesn't include image-generation as a target (only the description block). Minor cosmetic issue, easy follow-up.
- The corrections.md empty-state — the auto-capture hook may be misconfigured for this skill. Separate investigation.

---

## Approval Gate

**Reply with:**
- ✅ `approve` or `go` — I execute all 4 Groups, commit each separately, run verification checklist.
- 🔧 `modify <step>` — I revise the plan before execution.
- ❓ `clarify <question>` — I explain a section before you decide.
- ⛔ `reject` — I stash this plan and we discuss alternatives.

Token budget for Phase 6 execution: ~15K (small surgical Edits).
Estimated wall-clock for Phase 6: ~25 min.
