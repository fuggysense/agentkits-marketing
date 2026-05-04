---
name: higgsfield
version: "0.1.0"
brand: AgentKits Marketing by AityTech
category: image-generation
difficulty: intermediate
description: >
  Browser-automated image generation on higgsfield.ai. Drives Higgsfield's web UI via dev-browser to
  generate images using the 365 Unlimited model bucket (zero credit cost), with a credit-based
  fallback to Nano Banana 2 / GPT Image 2 only when unlimited models fail a sub-agent quality review.
  Self-improving loop via verification-loops + corrections.md. Called by image-generation skill as
  an alternate execution backend.
triggers:
  - generate via higgsfield
  - use higgsfield
  - higgsfield image
  - make an image on higgsfield
  - flux 2 image
  - kling o1 image
  - seedream 4.5 image
  - cartoon image higgsfield
  - photoreal image higgsfield
prerequisites:
  - dev-browser
related_skills:
  - image-generation
  - verification-loops
  - ugc-creator
agents:
  - copywriter
---

## Graph Links
- **Feeds into:** [[image-generation]] (alternate execution backend)
- **Draws from:** [[verification-loops]] (quality sub-agent loop)
- **Related:** [[ugc-creator]] (Higgsfield UGC prompt craft — prompts only, not browser)

## READ FIRST on every invocation

1. **Corrections file** — `skills/higgsfield/corrections.md`. Apply every entry as a hard constraint for this run. These are past failure → fix mappings. Do NOT repeat past mistakes.
2. **Reference file** — `skills/higgsfield/reference.md` — DOM selectors, slug map, gotchas.
3. **Allowed models** — `skills/higgsfield/lib/allowed-models.json` — the only models this skill may drive. Everything else is off-limits.

# Higgsfield (MCP-first, browser-fallback)

## Execution backend selection — CHECK FIRST

Before any generation, detect which execution backend is available and pick in this order:

1. **Higgsfield MCP** — if `mcp__higgsfield__*` tools are available in the current session, use them. Preferred path: faster, no browser session, no Clerk maintenance, no DOM-selector breakage.
2. **dev-browser** — if MCP unavailable (current default in most projects), drive `higgsfield.ai` via `dev-browser` per the rest of this skill.

To detect: check the loaded MCP tool list. If `mcp__higgsfield__*` namespace is present, branch to MCP path. Otherwise fall through to browser path.

### Higgsfield MCP — what it does (capabilities)

The Higgsfield MCP exposes Higgsfield's image and video generation as direct tool calls. Verify exact tool names against the actual MCP at install time — expected surface:

| Tool | Purpose |
|------|---------|
| `mcp__higgsfield__generate_image` | Fire image generation (model + prompt + params) |
| `mcp__higgsfield__generate_video` | Fire video generation (Higgsfield video models) |
| `mcp__higgsfield__list_models` | Get current model catalog (replaces `lib/allowed-models.json` at runtime) |
| `mcp__higgsfield__check_credits` | Replaces `session-check.js` browser flow |
| `mcp__higgsfield__get_generation` | Poll generation status / fetch result URL |

When MCP is installed, the **same model router below applies** — only the execution layer changes (tool call vs browser automation). All unlimited-bucket-first / credit-warn / sub-agent-quality-review logic stays identical.

### When MCP not installed
Continue with the browser path documented below. Install the higgsfield MCP via the user's MCP installer of choice when ready, then this skill auto-prefers it on next session.

---

# Higgsfield Browser Automation (fallback)

Drives `higgsfield.ai` via `dev-browser` (daemon-managed Chromium with a persistent Clerk session). One skill, multiple models, one router.

## When to use

- User wants an image and says anything that maps to Higgsfield / Flux 2 / Kling O1 / Seedream 4.5 / "the browser one"
- `image-generation` skill delegates here when user explicitly picks Higgsfield as the backend
- Cost-conscious runs that must stay in the unlimited bucket

## When NOT to use

- User wants fast batch generation via API (route to `image-generation` → Nano Banana default instead)
- Video generation (not in this skill's scope — future phase)
- Anything involving Face Swap, Soul 2.0, Soul Cinema, Z-Image, Reve, Seedream V5 Lite, Flux Kontext variants — out of scope per owner decision

## Model router (hard rules)

Classify the brief, then route:

| Brief type | Primary (unlimited, free) | Fallback chain |
|---|---|---|
| Photoreal, no text | `flux_2` (FLUX.2 Pro) | → `kling-o1-image` → `nano_banana` → [credits warn] `nano-banana-2` → `imagegen_2_0` |
| Cartoon / Pixar / stylized | `seedream_v4_5` (Seedream 4.5) | (no fallback — escalate to user) |
| Strong or complex text required | `imagegen_2_0` (GPT Image 2) — **CREDITS WARN BEFORE RUN** | none |
| Light / simple text | `nano_banana` | → [credits warn] `imagegen_2_0` |
| Photoreal **fantasy / sci-fi** | `grok_image` (Grok Imagine by xAI — inside Higgsfield) | → chain above if it fails |

**Escalation trigger:** sub-agent reviewer returns `pass: false` → go to next step in chain. Max 3 iterations per run (CLAUDE.md 3-strike rule).

**Credits warning protocol:** before running any credit-based model, print current credit balance (from session-check) + cost estimate + ask "proceed?". If the owner has pre-approved credit fallback in this session, skip the ask.

## Hard constraints

- **Prompt enhancer: OFF.** The skill writes its own prompts using image-generation craft. Never toggle the "On" button in the UI.
- **Unlimited models first, always.** Credit-based only after a quality failure, with a warn.
- **Unlimited toggle: ON when the model is in the unlimited bucket.** flux_2, seedream_v4_5, nano_banana, kling-o1-image and grok_image are unlimited tier. When selected, the Unlimited switch (the single `[role="switch"]` in the gen pane, sits near the Generate button) MUST be enabled — it makes batched generations genuinely free. Verify with `session-check.js` that `credits_remaining` does NOT drop after a batch.
- **Batch size: `count=1` per Generate click.** The `N/4` slider exists but we keep it at 1. Parallelism comes from rapid-fire sequential Generate clicks, NOT from the slider.
- **Parallel generation pattern (Plus/Ultra tier = up to 8 concurrent image jobs per Higgsfield pricing, confirmed 260422):** Fire Generate click → immediately fill the next prompt → click Generate again → continue up to N (max 8 on Plus/Ultra, lower on Starter). Do NOT `await` the prior generation before clicking again. Then poll the history panel for all N new image URLs at the end. This is a producer/consumer pattern, not sequential awaiting. See `scripts/generate-parallel.js` (to build) for the pattern.
- **Tier check:** Higgsfield Plus = 8 parallel images + 6 videos. Ultra = 8 for both. Starter = lower (TBD — verify in-UI before firing 8 clicks). If unknown, start with 4 and check credits/queue behavior.
- **Reference-image workflow for character/subject consistency** — MANDATORY for any multi-frame sequence (storyboards, character sheets, ad variants with recurring protagonist):
  1. Generate Frame 1 to establish the character.
  2. In the Higgsfield history panel, hover the image → click the **reference icon** (bottom-left of hover controls per owner screenshot 260422) → it auto-loads the image as reference for the next gen.
  3. All subsequent frames in the sequence use that reference. Description-only consistency drifts (~70% fidelity observed in the 260422 "The Letter" 2×2 storyboard test — hair/wardrobe carried, face drifted across frames).
  4. If the next model in the chain does not support reference images (router responsibility to check), escalate to the caller — don't silently degrade.
- **Copy-prompt icon** — hover any library image → the **copy icon** (top-right of hover controls) exposes the exact prompt + reference image that produced it. Use this to reverse-engineer an approved reference image's recipe when iterating.
- **Skip list — never drive these models:** `gpt` (unlimited GPT Image), `soul-v2`, Soul Cinema, `app/face-swap`, Seedream 4.0, Seedream V5 Lite, Z-Image, Reve, Flux Kontext Max.

## Aspect ratio defaults

7 options available in UI: `1:1, 3:4, 4:3, 16:9, 9:16, 3:2, 2:3`.

| Use case | Ratio |
|---|---|
| Static ad creative (Meta, Google Display, general) | **1:1** ← default |
| Story / Reels / TikTok / vertical short-form | **9:16** |
| YouTube thumbnail / landscape web hero | **16:9** |
| Pinterest portrait | `3:4` |
| Website banner wide | `3:2` |

Rarely pick anything else. If unsure → 1:1.

## Inputs (from caller, typically `image-generation`)

```json
{
  "brief": "one-line description of the image needed",
  "style": "photoreal | cartoon | stylized | text-heavy | light-text",
  "aspect": "1:1 | 3:4 | 4:3 | 16:9 | 9:16 | 3:2 | 2:3",
  "count": 1,
  "reference_images": ["/abs/path.png"],
  "output_dir": "clients/<slug>/assets/higgsfield/",
  "allow_credits": false
}
```

## Output contract

**Images stay in Higgsfield Library — no local downloads.** The skill returns URLs; downstream consumers fetch on demand.

```json
{
  "ok": true,
  "model_used": "flux_2",
  "iterations": 1,
  "image_url": "https://images.higgs.ai/?...",
  "prompt_final": "...",
  "review_verdict": { "pass": true, "score": 8.5, "failures": [] },
  "credit_cost": 0,
  "seconds_waited": 15
}
```

Every run also appends one line to `skills/higgsfield/usage-log.jsonl` — used by the router to learn which model best fits which prompt type over time.

Error surface (when `ok: false`): `auth_required | rate_limited | quality_failed_chain | generation_timeout | output_not_found`.

## Flow

1. **Pre-flight** — read `corrections.md`, `reference.md`, `allowed-models.json`. Run `session-check.js` → verify Clerk cookies + get credit balance.
2. **Classify brief** — pick starting model via router.
3. **Navigate** — `https://higgsfield.ai/ai/image?model=<slug>` (or `/app/face-swap` if ever unlocked; currently out of scope).
4. **Set options** — aspect, count. Prompt enhancer OFF (assert, don't assume).
5. **Fill prompt** — target selector `[id="hf:tour-image-prompt"]` (contenteditable div, `role="textbox"`).
6. **Attach references** if any — two `<input type="file">` slots available on most models.
7. **Generate** — click `Generate` button (label format: `Generate <N>`). Wait for output (typically 10–40s).
8. **Review** — spawn sub-agent (see Quality Loop below). Reviewer reads the image **from the URL directly** (multimodal) — no local download. If `pass: false`, step to next model in chain, rerun from step 3.
9. **Log** — append one line to `usage-log.jsonl` with `{ts, model, prompt_type, aspect, seconds_waited, verdict}`. Append to `corrections.md` only if the run surfaced a new failure pattern.

## Quality Loop (mandatory)

Uses `verification-loops` skill pattern. **See `scripts/review-image.md` for the exact invocation — it's not optional.** Reviewer sub-agent MUST Read a temp-file copy of the image (multimodal). WebFetch on the URL fails silently — returns a fabricated verdict. `/tmp/hf-review-<hash>.webp` is transient review-only; deleted after.

The reviewer sees:
- The generated image file at `/tmp/hf-review-<hash>.webp` (via Read)
- The original brief
- The rubric below

**Rubric (failure triggers — any ONE = fail):**
1. **Text garbled / jumbled** (highest weight — text is the #1 problem we've seen)
2. **Subject doesn't match the prompt** (e.g., wrong person count, wrong object, wrong action)
3. **Physics wrong** (impossible shadows, broken reflections, items defying gravity without artistic intent)
4. **Broken fingers / hands / anatomy**

**Ignore (per owner):**
- Realism grade — not a reject reason
- "AI look" / waxy skin
- Wrong style (fine if subject matches)

Reviewer returns JSON: `{ "pass": bool, "score": 0-10, "failures": ["text"|"subject"|"physics"|"anatomy", ...], "prompt_edits_suggested": [...] }`.

If `pass: false` → escalate to next model in the router chain. Do NOT simply retry the same model with the same prompt (violates CLAUDE.md 3-strike rule).

## Session expiry

Clerk cookies persist in `~/.dev-browser/` for weeks. When expired, `session-check.js` returns `auth_required` → skill halts with a clear re-login instruction ("Use Continue with Email — Google OAuth is blocked by Playwright fingerprint").

## Corrections loop (self-improving)

Every run — pass or fail — writes one line to `skills/higgsfield/corrections.md`:

```
YYMMDD | brief-summary | model_used | iterations | verdict | lesson
```

On the next invocation, step 1 reads this file and applies the lessons as hard constraints. This is the compounding loop.

## See also
- [[image-generation]] — upstream caller (JSON prompt planning lives there)
- [[verification-loops]] — the quality sub-agent pattern this skill depends on
- [[ugc-creator]] — complementary, prompt-craft-only, for Higgsfield UGC talking-head videos
- `skills/higgsfield/reference.md` — selectors, slug map, known gotchas
- `docs/plans/260422-higgsfield-browser-skill/` — build history and findings

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[image-generation]] (skill, 0.14)

<!-- skill-graph:end -->
