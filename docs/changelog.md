# Changelog

## 260324

### Updated
- **`website-design`** skill — Integrated 3 aesthetic modes (Soft, Minimalist, Brutalist) as new reference file `aesthetic-modes.md`. Added option 5 to Mode B Step 2 aesthetic direction. Added 4 banned patterns to `aesthetic-guidelines.md` (serif in dashboards, uncustomized shadcn defaults, emojis in markup, Space Grotesk). Added 3 fonts to `cinematic-presets.md` (Fraunces, Monument Extended, Switzer). Each mode defines complete palette, typography, surface treatment (Double-Bezel, ultra-flat, zero-radius), component rules, and motion philosophy translated to HTML+Tailwind+GSAP stack.
  - Inspired by: Leonxlnx/taste-skill (repo — soft-skill, minimalist-skill, brutalist-skill sub-skills)
  - Contributor: Jerel

---

## 260320

### Updated
- **`copy-editing`** skill — Sweep 8 quality gate (5-dimension scoring rubric, 35/50 minimum to deliver), 3 new sections in `overused-ai-patterns.md` (Performative Emphasis & Meta-Commentary, Vague Declaratives, Structural Anti-Patterns), new `de-ai-transformations.md` reference with 10 before/after examples. Checklist updated with quality gate item.
  - Inspired by: hardikpandya/stop-slop (repo — MIT, curated de-AI rubric + examples)
  - Contributor: Jerel

---

## 260319

### Created
- **`unslop`** skill (v1.0.0) — Domain-specific AI pattern detection using mshumer/unslop. Generates empirical avoidance profiles by sampling model defaults for specific content domains (LinkedIn posts, SaaS landing pages, emails, etc.). Becomes Layer 1 of the 4-layer de-AI stack: unslop profile (soft) → overused-ai-patterns (hard) → corrections.md (hard) → V.O.I.C.E. (positive target). Commands: `/unslop:profile`, `/unslop:refresh`, `/unslop:list`. Profiles stored in `skills/unslop/profiles/`, domain metadata in `references/domain-catalog.md`.
  - Inspired by: mshumer/unslop (tool — empirical AI default detection)
  - Contributor: Jerel

### Updated
- **`copy-editing`** skill — Sweep 8 (De-AI) now loads unslop profiles as Layer 1 soft constraints alongside overused-ai-patterns.md hard constraints. Updated process steps, checklist, and references.
- **`copywriting`** skill — Added De-AI Layer Loading section before writing to pre-load domain-matching unslop profiles.
- **`linkedin-content`** skill — Added Unslop Profile subsection under Banned AI Vocabulary for domain-specific layer loading.
- **`email-sequence`** skill — Added De-AI Layer Loading section for email-specific AI default avoidance.
- **`copywriter`** agent — Context Loading step 3.7 now loads matching unslop profile from `skills/unslop/profiles/`.
- **`brand-voice-guardian`** agent — Context Loading step 3.5 now loads matching unslop profile for content type review.
- Updated `skills-registry.json`, `routing-table.md`, `skills-catalog.md`, `commands.md` with unslop registration.

---

## 260317

### Updated
- **`website-design`** skill (v4.1.0 → v5.0.0) — Paper.design MCP integration for bidirectional visual design workflows. New Mode D (Paper-First) for importing designs from Paper and converting to HTML/Tailwind. Modes A-C enhanced with optional Paper push/pull when available. 24 MCP tools (11 read, 13 write) for design token extraction, JSX export, HTML preview. New reference file `paper-integration.md`. Paper integration docs added to `skills/integrations/paper/`. Updated registry, routing table, skills catalog, MCP integrations.
  - Inspired by: Paper.design (tool — MCP-enabled design editor)
  - Contributor: Jerel

---

## 260316

### Created
- **`meta-ads-uploader`** skill (v1.0.0) — End-to-end pipeline for uploading ad creatives to Meta (Facebook/Instagram). MetaAdsClient class with image/video upload, single + dynamic creative creation, PAUSED ad creation. CLI with validate/preview/upload-media/full/status commands. Creative bundle JSON format bridges copywriting + image-generation output → Meta API. Resumable runs via results sidecar file. Auto-converts WebP/TIFF/HEIC to PNG. HITL gates: bundle review, media confirm, creative preview, go-live (always PAUSED). Updated campaign-runner execution-playbook (Manual → meta-ads-uploader), skills-registry, dependency-graph, routing-table, skills-catalog, commands.
  - Inspired by: ScrapeCreatorsClient (pattern), Meta Marketing API v22.0 (API)
  - Contributor: Jerel

---

## 260315

### Created
- **`scrapecreators`** skill (v1.0.0) — Universal social intelligence API client for 25+ platforms. ScrapeCreatorsClient class with 100+ endpoint methods, CLI with subcommands per platform, auto-pagination, credit tracking, typed exceptions. Extracted and generalized from `tiktok-slideshows/scripts/competitor_scan.py`. Refactored competitor_scan.py to import from shared module.
  - Inspired by: ScrapeCreators API (service), competitor_scan.py (existing pattern)
  - Contributor: Jerel

---

## 260314

### Created
- **`autoresearch`** meta-skill (v1.0.0) — Autonomous skill optimization via Karpathy's generate → evaluate → mutate → keep/discard pattern. Global skill at `~/.claude/skills/autoresearch/`. 7 Python scripts (orchestrator, rubric_bootstrap, scenario_generator, safety, scheduler, trust_tracker, feedback_loop), 4 YAML templates, 1 deep reference doc, 12 slash commands. Phase 1 (MVP) active, Phases 2-4 scaffolded. Per-client isolation via `clients/<project>/autoresearch/`. Trust graduation L0→L3. Safety rails: budget caps, kill switch, auto-revert. ~$0.50-1.00/run.
  - Inspired by: Karpathy (person — [autoresearch](https://github.com/karpathy/autoresearch) pattern), Jerel (person — skill booster concept)
  - Contributor: Jerel

### Amplified
- **`video-director`** skill (v1.0.0 → v2.0.0) — Major upgrade: 11 → 14 video types (+Walk-and-Talk, Driver's Seat, At-Home Demo), 3 new reference files (character-bible-template, seed-management, client-campaign-audit), Sora 2 Pro platform features (Characters API, Video Edits, Clip Extension, Batch API, Storyboard Mode), UGC automation via Kie.ai, 8K shot prompting, emotional block dialogue cues, weak→strong prompt transformations, post-production pipeline, Creative Director pattern, seed bracketing (~60% cost reduction)
  - Inspired by: Mikoslab (11 PDFs — character bibles, 8K prompting, seed bracketing, post-production, campaign audit), OpenAI (Sora 2 Prompting Guide), Lucas Walter (UGC automation, 3 archetypes, Kie.ai pipeline)
  - Contributor: Jerel
- **`image-generation`** skill — Added NB Pro advanced features (style saving, annotation), two image workflows (Objects vs Characters paths), Seedream 4 character alternative
  - Inspired by: Mikoslab (NB Pro features), Jerel
  - Contributor: Jerel
- **`model-selection-guide.md`** reference — Added VEO 3.1 ingredients approach, production budget rule, image-to-video dominance (90%), two image workflows, Sora 2 Pro platform features (Characters API, clip extension 6x/120s, video edits, batch API, storyboard mode), Kie.ai API gateway, seed bracketing cross-reference, discrete duration values, creativity tradeoff
  - Inspired by: Mikoslab, OpenAI Sora 2 Guide, Lucas Walter
  - Contributor: Jerel
- **`cinematography-reference.md`** reference — Added 8K Shot Prompting section with camera body specifications (RED Komodo, ARRI Alexa LF, Sony FX6, Canon C70, Blackmagic 6K)
  - Inspired by: Mikoslab (8K shot prompting)
  - Contributor: Jerel
- **`realism-tricks.md`** reference — Added Post-Production Pipeline, Emotional Block Dialogue Cues, Weak→Strong Prompt Transformations, Image Input First-Frame Control, Dialogue Formatting Best Practice, Characters API + text fallback to Character Consistency Framework
  - Inspired by: Mikoslab (emotional blocks, post-production), OpenAI (dialogue formatting), Lucas Walter (weak→strong)
  - Contributor: Jerel
- **`nano-banana-full-guide.md`** reference — Added NB Pro advanced features, style prompt saving, annotation workflow, Seedream 4 character alternative
  - Inspired by: Mikoslab (NB Pro)
  - Contributor: Jerel
- **`tiktok-content.yaml`** template — Added slideshow script framework, viral format study step, character-based account option
  - Inspired by: Mikoslab (TikTok script framework)
  - Contributor: Jerel

### Updated
- `skills/skills-registry.json` — added autoresearch entry in specialized category
- `skills/dependency-graph.md` — added autoresearch to Meta Track
- `.claude/rules/routing-table.md` — added autoresearch to skills table
- `.claude/rules/skills-catalog.md` — added autoresearch to System Tools
- `.claude/rules/commands.md` — added 12 `/autoresearch:*` commands
- `commands/ops/weekly.md` — added Step 6: autoresearch rotation check
- `commands/ops/monthly.md` — added autoresearch summary section to knowledge hygiene

---

## 260313

### Created
- **`content-moat`** skill (v1.0.0) — Content ideation + layering strategy for copycat-resistant content. 5 originality frameworks (Collision, Proprietary Insight, Perspective Flip, Format Translation, Compound Stacking), 10-layer catalog with implementation guides, copycat resistance scoring, pipeline integration with video-director/image-generation/copywriting/linkedin-content. Verified via prompt-contract + verification-loop.
  - Inspired by: Jerel (person — observations on AI content wave), beechinour (person — layering concept), yangmun (person — format originality case study)
  - Contributor: Jerel
- **`video-director`** skill (v1.0.0) — AI video prompt generation for marketing ads. 11 video types, 3 pipelines (Direct, Image-First, Localized), 5-Part Prompt Formula, HITL review gates, full Production SOP, 4 reference files (video-type-catalog, realism-tricks, model-selection-guide, cinematography-reference)
  - Inspired by: David Roberts (AI Ad Guys — @recap_david), snubroot (Veo 3.1 Meta Framework — GitHub snubroot/Veo-3-Meta-Framework)
  - Contributor: Jerel
- **`changelog`** — Central change log with inspired-by attribution tracking
  - Inspired by: Jerel (person) — need for cross-session visibility into what changed
  - Contributor: Jerel

### Amplified
- **`image-generation`** skill — added HITL Prompt Review Gate, Video Reference Image Mode, `video-director` to related_skills
  - Inspired by: David Roberts (AI Ad Guys), Jerel (HITL philosophy)
  - Contributor: Jerel
- **`realism-tricks.md`** reference — added Character Consistency Framework, Transition Realism, Negative Prompt Format Guide
  - Inspired by: snubroot (Veo 3.1 Meta Framework)
  - Contributor: Jerel
- **`model-selection-guide.md`** reference — updated to Kling 3.0, added prompt length constraints table, technical specs
  - Inspired by: snubroot (Veo 3.1 Meta Framework)
  - Contributor: Jerel
- **`learnings.md`** (video-director) — added troubleshooting matrix, additional confirmed patterns
  - Inspired by: snubroot (Veo 3.1 Meta Framework)
  - Contributor: Jerel
- **`copywriting`** references — added cross-references to video-director in ad-creative-frameworks.md and video-ad-scripts.md
  - Inspired by: Jerel (pipeline integration)
  - Contributor: Jerel
- **`copywriter`** agent — added video-director to skill integrations
  - Inspired by: Jerel (pipeline integration)
  - Contributor: Jerel

### Updated
- **`amplifier`** skill — added changelog append step to Phase 4
  - Inspired by: Jerel (person) — changelog integration
  - Contributor: Jerel
- **`meta-builder`** skill — added changelog append on new artifact creation
  - Inspired by: Jerel (person) — changelog integration
  - Contributor: Jerel
- **`CLAUDE.md`** — added changelog step to Session End Protocol
  - Inspired by: Jerel (person) — changelog integration
  - Contributor: Jerel
