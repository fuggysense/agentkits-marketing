# Derivative File Templates — Phase 5 Outputs

After `source-of-truth.md` is written, Phase 5 also writes derivative files so downstream skills don't parse the big doc.

**Files produced:**
1. `clients/<project>/01_research/output/<YYMMDD>-audience-insights-synthesis.md` — clean audience synthesis from structured research fields and Reddit/forum/review language
2. `clients/<project>/pain-objection-proof.md` — §6+§7+§8 standalone
3. `clients/<project>/swipe-file-buyers.md` — filtered competitor ads (buyer-side)
4. `clients/<project>/swipe-file-sellers.md` — filtered competitor ads (seller-side)
5. `clients/<project>/angles/` — wave-by-wave angle and hook library

`messaging-hierarchy.md` and root `angles-hooks-library.md` are deprecated as derivatives. Core message lives inline in source-of-truth §9. Angles and hooks live in the `angles/` folder to avoid drift.

---

## 0. audience-insights-synthesis.md

**Consumed by:** `avatar-research`, `video-concept-lab`, `ad-concept-engine`, `copywriting`, `script-skill`

Use `references/audience-insights-synthesis-template.md`.

This file answers: what did the audience actually say, what does it mean for marketing, and which personas/angles can safely be built from it?

## 1. pain-objection-proof.md

**Consumed by:** `ad-concept-engine` (for objection-handling lines), `copywriting` (for proof overlays), `page-cro` (for FAQ / objection sections on landing pages)

```markdown
# Pain · Objection · Proof — {{project_name}}

> Derived from source-of-truth.md §6, §7, §8. Refreshed: {{generated_date}}. Re-generate whenever buyer-language-dossier or paid-media-audit updates.

## Pain Points (Ranked by Research Frequency)

| Rank | Functional Pain | Emotional Reaction | Verbatim Quote Example |
|---|---|---|---|
| 1 | {{pain_1}} | {{emotion_1}} | "{{quote_1}}" — {{source_1}} |
| 2 | {{pain_2}} | {{emotion_2}} | "{{quote_2}}" — {{source_2}} |
| ... | | | |

## Objection Handling Table

| Objection (Verbatim) | Category | Root Cause | Best Proof / Answer | Where to Address |
|---|---|---|---|---|
| "{{objection_1}}" | {{cat_1}} | {{root_1}} | {{answer_1}} | {{placement_1}} |
| ... | | | | |

## Proof Inventory (Ranked by Strength × Relevance)

| Asset | What it Proves | Strength | Best Ad Use | Compliance Safe? |
|---|---|---|---|---|
| {{proof_1}} | {{proves_1}} | {{strength_1}} | {{use_1}} | {{safe_1}} |
| ... | | | | |

## Proof Gaps (Priority Order)

1. {{gap_1}} — Impact: {{impact_1}} · Owner: {{owner_1}} · Due: {{due_1}}
2. ...
```

---

## 2. messaging-hierarchy.md

**Consumed by:** `copywriting`, `page-cro`, `email-sequence`, `ad-concept-engine` (for angle-message alignment validation)

```markdown
# Messaging Hierarchy — {{project_name}}

> HITL-confirmed core message from source-of-truth.md §9. Refreshed: {{generated_date}}.

## Core Message

{{core_message}}

**Why this won (over alternatives):**
{{core_rationale}}

## Supporting Messages

1. {{supporting_1}}
2. {{supporting_2}}
3. {{supporting_3}}
4. {{supporting_4}}
5. {{supporting_5}}

## Funnel-Stage Prioritisation

| Stage | Leading Message | Goal |
|---|---|---|
| Cold | {{cold_msg}} | Stop scroll + create relevance |
| Warm | {{warm_msg}} | Build belief + reduce skepticism |
| Hot | {{hot_msg}} | Remove final friction + convert |
| Retargeting | {{retarget_msg}} | Reopen consideration + resolve objection |

## Message Ladder (for long-form ads / landing pages)

1. **Attention:** {{ladder_attention}}
2. **Problem relevance:** {{ladder_problem}}
3. **Solution mechanism:** {{ladder_mechanism}}
4. **Proof:** {{ladder_proof}}
5. **Offer:** {{ladder_offer}}
6. **CTA:** {{ladder_cta}}

## Message-to-Angle Mapping

Which §10 angles reinforce each supporting message:

| Supporting Message | Angle(s) That Reinforce It |
|---|---|
| {{supporting_1}} | {{angle_list_1}} |
| ... | |
```

---

## 3. angles-hooks-library.md

**Consumed by:** `ad-concept-engine` (PRIMARY — this is the file it reads when generating DCT batches), `script-skill`, `copywriting`

```markdown
# Angles · Hooks Library — {{project_name}}

> HITL-confirmed angles from source-of-truth.md §10. Hooks from §11. Priority angles marked ⭐. Refreshed: {{generated_date}}.

## Priority Angles (from HITL Phase 4)

### ⭐ Angle 1: {{priority_angle_1_name}}

- **Category:** {{cat_1}} (Problem-Aware / Desire-Led / Product-Led / Offer-Led / Proof-Led / Contrarian)
- **Core idea:** {{core_idea_1}}
- **Primary avatar:** {{avatar_1}}
- **Best formats:** {{formats_1}}
- **Awareness level:** {{awareness_1}}
- **Sophistication level:** {{soph_1}}
- **Risk / caveat:** {{risk_1}}

**Hooks for this angle (10):**

| # | Hook | Type | Buyer Language Source |
|---|---|---|---|
| 1 | {{hook_1_1}} | {{type_1_1}} | {{source_1_1}} |
| 2 | {{hook_1_2}} | {{type_1_2}} | {{source_1_2}} |
| ... | | | |
| 10 | {{hook_1_10}} | {{type_1_10}} | {{source_1_10}} |

**Objection-handling lines to weave in (from pain-objection-proof.md):**
- {{obj_line_1_1}}
- {{obj_line_1_2}}

**Proof assets that support this angle (from pain-objection-proof.md):**
- {{proof_1_1}}
- {{proof_1_2}}

---

### ⭐ Angle 2: {{priority_angle_2_name}}
[same structure]

---

### ⭐ Angle 3: {{priority_angle_3_name}}
[same structure]

---

## Secondary Angles (not HITL-prioritised but drafted for future waves)

### Angle 4: {{secondary_angle_1_name}}
[abbreviated — just core idea + 3 hooks, not the full 10]

### Angle 5: {{secondary_angle_2_name}}
[abbreviated]

### Angle 6+: {{...}}

---

## Hook Writing Grid (master view)

| Hook | Angle | Type | Awareness | Funnel Stage | Format | Priority |
|---|---|---|---|---|---|---|
{{hook_grid_rows}}

---

## Anti-Pattern Log (hooks NOT to write)

From competitor swipe analysis — angles/hooks that are over-saturated in this market:

| Over-used Pattern | Why Avoid | How We Differentiate |
|---|---|---|
| {{overused_1}} | {{why_avoid_1}} | {{differentiate_1}} |
| ... | | |
```

**Schema mapping for ad-concept-engine consumption:** `ad-concept-engine` expects `angles` array with each angle object containing `name, category, core_idea, hooks[]`. Ensure the markdown structure above can be regex-parsed into that JSON shape.

---

## 4. swipe-file-buyers.md

**Consumed by:** `ad-concept-engine` (reads this for competitive context)

```markdown
# Swipe File — Buyer-Side Competitor Ads — {{project_name}}

> Filtered from competitor-ads/ research. Ads targeting the BUYER (end-customer) side of the market. Refreshed: {{generated_date}}.

## Competitors Analysed

| Competitor | Active Ads | Dominant Angle | Dominant Format | Notes |
|---|---|---|---|---|
| {{comp_1}} | {{count_1}} | {{angle_1}} | {{format_1}} | {{notes_1}} |
| ... | | | | |

## Angle Distribution (Buyer-Side)

| Angle | # of Competitors Using It | Saturation Level | Our Differentiation Opportunity |
|---|---|---|---|
| {{angle_dist_1}} | {{count}} | {{saturation}} | {{opportunity}} |

## Top 10 Most Effective Ads (by engagement signals)

### Ad 1 — {{competitor}} — {{format}}

**Hook:** {{hook}}
**Body:** {{body_excerpt}}
**Angle category:** {{angle_cat}}
**Proof used:** {{proof}}
**CTA:** {{cta}}
**Why it's working (inferred):** {{analysis}}

[... 9 more]

## Hooks Worth Stealing (Adapted for Our Positioning)

| Competitor Hook | Our Adapted Hook | Angle Fit |
|---|---|---|
| "{{theirs_1}}" | "{{ours_1}}" | {{fit_1}} |

## Hooks to AVOID (Over-saturated)

- "{{avoid_1}}" — used by {{N}} competitors · dead pattern
- ...
```

---

## 5. swipe-file-sellers.md

**Consumed by:** `ad-concept-engine` (for seller-side angle generation in two-sided markets like real estate)

**Same structure as swipe-file-buyers.md**, but filtered for ads targeting the SELLER side (e.g. homeowners selling). Only write this file if the project is a two-sided market (real estate agent services, marketplace platforms, B2B platforms with both supply and demand sides). Skip for single-sided offers.

---

## Write Order (Phase 5)

1. `source-of-truth.md` first (canonical doc)
2. Then all 5 derivative files in parallel (independent Write calls in one message)

After all 6 files written, proceed to sheet-integration (if `metrics-config.json` exists for project).

---

## Naming Conventions

- All derivative files use kebab-case filenames
- All tables preserve the column orders specified here so downstream skills can regex-parse reliably
- Refresh date at the top of every file
- When regenerating, OVERWRITE existing derivative files (don't append). The canonical source is `source-of-truth.md` — derivatives are computed views.
- Never hand-edit derivative files. If a correction is needed, update `source-of-truth.md` and re-run Phase 5.

---

## Staleness Detection

During `/ops:weekly` (via `knowledge-hygiene` skill):
- If `source-of-truth.md` was regenerated but derivative files are older → flag drift, trigger re-write
- If any derivative file has manual edits (diff vs last-regenerated snapshot) → surface to Jerel, ask whether to preserve or overwrite
