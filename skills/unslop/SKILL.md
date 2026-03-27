---
name: unslop
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: utility
difficulty: intermediate
description: "Domain-specific AI pattern detection — generates empirical avoidance profiles by sampling model defaults. Run infrequently to produce profiles that consumer skills (copywriting, linkedin-content, email-sequence, etc.) load at activation time. Adds Layer 1 to the 4-layer de-AI stack."
triggers:
  - unslop
  - ai pattern detection
  - domain profile
  - avoidance profile
  - de-ai profile
  - slop detection
  - ai defaults
prerequisites: []
related_skills:
  - copy-editing
  - copywriting
  - linkedin-content
  - email-sequence
  - website-design
agents:
  - copywriter
  - brand-voice-guardian
mcp_integrations:
  optional: []
success_metrics:
  - patterns_detected
  - profile_specificity
  - consumer_skill_improvement
---

## Graph Links
- **Feeds into:** [[copy-editing]], [[copywriting]], [[linkedin-content]], [[email-sequence]], [[website-design]], [[programmatic-seo]]
- **Draws from:** (standalone generator)
- **Used by agents:** [[copywriter]], [[brand-voice-guardian]]
- **Related:** [[content-moat]], [[knowledge-hygiene]]

# Unslop: Domain-Specific AI Pattern Detection

Generate empirical avoidance profiles by sampling model defaults for a specific content domain. Profiles become Layer 1 of the 4-layer de-AI stack:

```
Layer 1: Unslop profile      (domain-specific baseline, empirical)  ← THIS SKILL
Layer 2: overused-ai-patterns (universal static prohibitions)
Layer 3: corrections.md       (user-accumulated session fixes)
Layer 4: V.O.I.C.E.           (positive voice target)
```

Layers 1-3 = "avoid this." Layer 4 = "sound like this instead."

## When to Use

- **Generate profiles** when adding a new content domain or after a major model update
- **Do NOT use** for day-to-day content creation (consumer skills load profiles automatically)
- Profiles are **soft constraints** (prefer to avoid) vs `overused-ai-patterns.md` which are **hard constraints**

## Prerequisites

- Python 3.10+
- Claude Code CLI installed
- Unslop repo cloned at `~/AI workflows/unslop/`

## Commands

| Command | Purpose |
|---------|---------|
| `/unslop:profile <domain>` | Generate avoidance profile for a domain |
| `/unslop:refresh` | Re-run all existing profiles |
| `/unslop:list` | Show all generated profiles with metadata |

---

## Profile Generation Workflow

### Step 1: Determine Domain & Type

Identify the content domain and whether it's `text` or `visual`:

| Domain | Type | Count | Notes |
|--------|------|-------|-------|
| LinkedIn posts | text | 50 | Short-form, conversational |
| SaaS landing pages | text | 50 | Conversion copy |
| Email sequences | text | 50 | Nurture/sales emails |
| Blog writing | text | 50 | Long-form articles |
| Video scripts | text | 50 | Hook + body scripts |
| TikTok hooks | text | 50 | Ultra-short hooks only |
| pSEO templates | text | 50 | Template-driven content |
| Landing page design | visual | 20 | HTML/CSS patterns |

### Step 2: Run Unslop

```bash
cd ~/AI\ workflows/unslop
source .venv/bin/activate

# Text domain
python3 unslop.py --domain "<domain>" --count 50 --concurrency 5

# Visual domain (install Playwright first)
pip install playwright && playwright install chromium
python3 unslop.py --domain "<domain>" --type visual --count 20 --concurrency 3
```

### Step 3: Review Output

Check `unslop-output/analysis.md` and `unslop-output/skill.md`:

1. **Specificity check** — Are patterns concrete with examples, not vague?
2. **Count check** — Does analysis include frequency counts?
3. **Overlap check** — Flag patterns already in `overused-ai-patterns.md`
4. **Quality check** — Would following this profile make the output noticeably different?

If analysis is thin, rerun with higher `--count`.

### Step 4: Deduplicate Against Static List

Compare generated profile against `skills/copy-editing/references/overused-ai-patterns.md`:

- **Remove** patterns already covered by the static list
- **Keep** only net-new, domain-specific patterns
- **Note** in the profile header which patterns were deduped

### Step 5: HITL Review

Present the deduped profile to the user for approval. They may:
- Remove patterns that are actually desirable for their voice
- Add patterns they've noticed but unslop missed
- Adjust severity (some patterns are fine occasionally)

### Step 6: Save Profile

Save the approved profile to `skills/unslop/profiles/<domain-slug>.md` with this header:

```markdown
# Unslop Profile: <Domain Name>

Generated: YYMMDD | Samples: N | Model: <model> | Type: text|visual
Deduped against: overused-ai-patterns.md (N patterns removed)

---

## Phrases to never use
...

## Structural patterns to avoid
...

## Tonal patterns to avoid
...

## Word-level patterns to avoid
...
```

### Step 7: Update Domain Catalog

Append entry to `skills/unslop/references/domain-catalog.md`.

---

## Consumer Skill Integration

After generating a profile, consumer skills load it automatically. The wiring:

| Consumer Skill | Profile | Load Point |
|---|---|---|
| `copy-editing` (Sweep 8) | Match by content type | Second layer alongside `overused-ai-patterns.md` |
| `copywriting` | `saas-landing-pages.md` or `blog-writing.md` | Context step before drafting |
| `linkedin-content` | `linkedin-posts.md` | Merged with existing Banned AI Vocabulary |
| `email-sequence` | `email-sequences.md` | Context step before drafting |
| `website-design` | `landing-page-design.md` | Alongside `aesthetic-guidelines.md` |
| `script-skill` | `video-scripts.md` | Before de-AI pass |
| `tiktok-slideshows` | `tiktok-hooks.md` | For hook writing |
| `programmatic-seo` | `pseo-templates.md` | For template content |
| `brand-voice-guardian` agent | Match by content type | Added to review context |
| `copywriter` agent | Match by content type | Added to context loading |

### How Consumer Skills Should Load Profiles

```
1. Check if a matching profile exists in skills/unslop/profiles/
2. If yes, load it as SOFT constraints (prefer to avoid, not absolute ban)
3. Load overused-ai-patterns.md as HARD constraints (never use)
4. Load corrections.md as HARD constraints (never repeat)
5. Load V.O.I.C.E. as positive target (write like this)
```

**Constraint hierarchy:** corrections.md > overused-ai-patterns.md > unslop profile

---

## Profile Maintenance

- **Freshness:** Profiles older than 90 days should be regenerated (model defaults drift)
- **Model updates:** Re-profile after major model updates (Sonnet 4.x, Opus 4.x, etc.)
- **Track model version** in `domain-catalog.md` so you know when to refresh
- **Knowledge-hygiene** integration: flagged in `/ops:monthly` freshness checks

## References

- `references/domain-catalog.md` — Tracks all profiled domains with metadata
- `~/AI workflows/unslop/` — Upstream unslop tool
- `skills/copy-editing/references/overused-ai-patterns.md` — Static prohibition list (dedup target)

## Related Skills

- **copy-editing** — Primary consumer (Sweep 8: De-AI)
- **copywriting** — Loads profile before drafting
- **linkedin-content** — Merges with existing banned vocabulary
- **knowledge-hygiene** — Monitors profile freshness
