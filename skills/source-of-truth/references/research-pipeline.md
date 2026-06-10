# Research Pipeline — Phase 2 Parallel Orchestration

How to spawn 4-5 research sources in parallel and collect their outputs for Phase 3 synthesis.

**Critical rule:** spawn all research sources in ONE message with parallel tool calls. NEVER serialise. Serialised research takes 30-45 minutes; parallel takes 5-10.

**Canonical social/forum mining tool:** `scrapecreators` skill covers 25+ platforms (Reddit, TikTok, Instagram, YouTube, X/Twitter, Threads, Pinterest, Bluesky, LinkedIn, Facebook, etc.) via one API. Do NOT integrate GigaBrain, Reddit Answers, or other duplicate scrapers — scrapecreators is the single source for raw social/forum/comment mining. The `buyer-language-researcher` agent uses scrapecreators (and DataForSEO/NotebookLM/WebFetch) under the hood.

---

## Phase 0.5 — Raw Doc Upload (Optional Pre-Research Entry Point)

If the user has existing raw research artifacts (PDF, text dump, customer interview transcripts, survey CSVs, support-ticket exports, sales-call notes, messy Notion pages), ingest them BEFORE spawning fresh research. Existing voice-of-customer data is higher signal than fresh scrapes.

**Trigger:** ask in Phase 0 (alongside the onboarding-artifact check from corrections.md 260417): *"Do you have any raw buyer research already? PDF, transcripts, surveys, exported reviews, sales call notes — anything voice-of-customer?"*

**If yes, accept any of:**
- File path on disk (PDF, .txt, .md, .csv, .docx)
- Pasted text dump in the conversation
- Google Drive folder URL (manual download for now — Drive MCP deferred per plan)

**Processing:**
1. Save raw input to `clients/<project>/research/raw/uploaded-YYMMDD-<source>.{pdf|txt|md|csv}`
2. Extract structured fields where possible: pain_points, failed_solutions, desired_outcomes, objections, misconceptions, golden_nuggets, language_notes
3. Save extraction to `clients/<project>/research/raw-extract-YYMMDD.json`
4. Pass extraction to `buyer-language-researcher` agent in Phase 2 as a primary input alongside fresh scrapes — prevents redundant mining and grounds the dossier in user-validated material
5. Cite raw upload provenance in the final source-of-truth `_manifest.json`

**Quality bar:** raw upload supplements but does NOT replace fresh research. Always still run scrapecreators + buyer-language-researcher to triangulate against external buyer voice. Internal docs are biased toward what the brand thinks the buyer says.

---

## Research Sources

| # | Source | Tool | Output file | Always run? | Approx. duration |
|---|---|---|---|---|---|
| 1 | Competitor ads | `scrapecreators` skill | `clients/<project>/competitor-ads/raw-<competitor>.md` | Yes | 3-5 min |
| 2A | **Community discovery** | `scrapecreators` (Reddit search) + DataForSEO + WebFetch | `clients/<project>/research/community-map.md` (HITL-approved) | Yes — runs BEFORE 2B | 5-10 min |
| 2B | Buyer language (verbatim mining) | `buyer-language-researcher` agent + `reddit` skill (scrape + search) | `clients/<project>/research/buyer-language-dossier.md` | Yes — runs after 2A approval | 5-10 min |
| 3 | Market sentiment | `deep-research` skill | `clients/<project>/research/market-research.md` | Yes | 5-10 min |
| 4 | Product snapshot | WebFetch + dev-browser | `clients/<project>/research/product-snapshot.md` | Mode B only | 1-2 min |
| 5 | Account audit | `paid-media-audit` skill | updates §8, §18 | Only if ad account connected | 10-15 min |

---

## Spawn Pattern (all in one message)

```
Parallel message containing:
  - Task #1: scrapecreators invocation for top 5 competitors
  - Task #2: buyer-language-researcher Agent spawn
  - Task #3: deep-research skill invocation
  - Task #4 (Mode B): WebFetch on product URL + dev-browser deep scrape
  - Task #5 (conditional): paid-media-audit skill
```

After spawning, await all completion notifications. Do NOT poll intermediate outputs (per CLAUDE.md §4 context hygiene — polling pulls tool noise into main context).

---

## Source 1 — `scrapecreators` (Competitor Ads)

**Pre-requisite:** identify top 5-10 competitors. In Mode A, check `clients/<project>/competitor-ads/` for existing dossiers. In Mode B/C, infer from:
- Product category + market research first-pass
- Phase 1 intake Q2 (target market) + Q5 (constraints) context

**Invocation pattern:**
```
Call scrapecreators skill with:
  - platform: "meta_ad_library" (and "tiktok" if B2C)
  - targets: [list of competitor handles or brand search terms]
  - filters: active ads only, [country: SG if SG-based], last 30 days
  - output_dir: clients/<project>/competitor-ads/
```

**Output per competitor:**
```
clients/<project>/competitor-ads/<competitor-slug>-raw.md
```

Each file should include: ad copy, hook patterns, angles attempted, format distribution, CTA patterns, claims made, proof used.

**Failure handling:** if a competitor has 0 active ads, skip and note in manifest. Never fabricate competitor data.

---

## Source 2 — `buyer-language-researcher` (Reddit + Social)

**Agent location:** `~/.claude/agents/buyer-language-researcher.md`

### Two-stage research flow (260418 — non-negotiable)

The common failure mode: spawning the researcher with a guessed list of subreddits → wasting a research cycle on the wrong communities. Fix: SPLIT Source 2 into two stages. Discovery first, mining second.

**Stage 2A — Community Discovery (5-10 min)**

Goal: identify WHICH communities the buyer actually lives in. Output: a validated list of subreddits, forums, Discord servers, Facebook groups, Slack workspaces, TikTok creator networks, YouTube channels + their comment sections. NOTHING is mined yet.

Inputs:
- Phase 1 intake (product_type, target market, geography, constraints)
- Phase 0 onboarding artifacts (founder's own mentions of where customers come from)
- Competitor swipe file (Phase 0.5) — where are competitor fans concentrated?

Tools per discovery channel:
- **Reddit:** DataForSEO "related search" queries for product terms → collect subreddit names that appear in SERPs. Also: `scrapecreators` Reddit subreddit-search endpoint (ranked by activity). Cross-validate.
- **Forums + niche sites:** WebFetch on "best forum for <category>" Google queries.
- **Instagram + TikTok:** `scrapecreators` to find 10-20 creator accounts in the niche; their COMMENT sections become the mining targets in Stage 2B.
- **YouTube:** same pattern — find the 5-10 most-watched videos on the topic; their comments are mineable.
- **Facebook groups:** if intake flagged an SG/local focus, surface known community group names from `sg-cultural-guidelines.md` or equivalent. Verify they still exist.

Output: `clients/<project>/research/community-map.md` with a ranked table:

| Community | Platform | Why this one | Activity signal | Mining priority |
|---|---|---|---|---|
| r/singaporefi | Reddit | Financial-decision-heavy SG buyers discuss property upgrade math | 120k members, daily posts | HIGH |
| r/singapore | Reddit | General SG discussion, includes upgrade regret + counter-narrative | 2M members | MEDIUM |
| HardwareZone Money Mind forum | Forum | Long-form SG financial discussion, older demographic | moderate | MEDIUM |
| @damien.tan IG comments | Instagram | Competitor account — exact buyer segment | 50k followers, high comment rate | HIGH |

**HITL checkpoint:** present `community-map.md` to user. They pick which communities to mine (default: all HIGH + top 2 MEDIUM). User can add/remove. Without this checkpoint, the next stage scrapes blindly.

**Stage 2B — Verbatim Mining (5-10 min)**

Only runs AFTER Stage 2A + HITL approval. Goal: pull verbatim quotes from the approved communities.

Target sources in priority order:
1. Reddit: ONLY the subreddits validated in Stage 2A (not a guessed list). Pull top posts + comments from last 12 months using `reddit` skill — `reddit scrape` for deep comment trees (recursive 'more' stub resolution) and `reddit search` for discovery within those subs.
2. NotebookLM: check `clients/<project>/notebooklm.json` for existing corpora; query if relevant
3. DataForSEO: related keyword searches to find PUBLIC forum threads (not community discovery — that was Stage 2A)
4. Social: Instagram / TikTok comment mining on the creator accounts + competitor accounts validated in Stage 2A (via scrapecreators). Target 100+ comments per approved account.
5. Quora / Stack Exchange: category-specific threads (only if 2A validated as active in the niche)

**Why this order matters:** mining blindly on 20 subreddits wastes 80% of the time on communities where the buyer doesn't live. Discovery-first means mining is focused. For neezanizam: Stage 2A would've flagged that r/singaporefi is high-signal + r/singapore medium + HardwareZone Malay forums NEEDED but are an English-Reddit blind spot. Stage 2B would've known to schedule a manual mining pass on HardwareZone instead of producing the dossier with a known gap.

---

**Legacy prompt construction (updated to reflect Stage 2B only):**

```
Research the buyer language for [category] in [geography].

Target sources (VALIDATED IN STAGE 2A — do not expand without user approval):
1. Reddit: r/[validated subreddits from community-map.md]
2. NotebookLM: [validated corpus from notebooklm.json]
3. DataForSEO: [validated keyword queries]
4. Social: [validated creator accounts + competitor accounts from community-map.md]
5. Forums: [validated niche forums from community-map.md]

Goal: verbatim buyer phrasings on:
- How they describe the problem (exact words)
- What they've already tried and why it failed
- What they're tired of / frustrated by
- What they want instead
- Why they hesitate to buy
- What would convince them
- Objections they voice (price, trust, fit, timing, effort, proof, alternative)
- Who or what they blame

CRITICAL: preserve exact wording. Do NOT paraphrase. Attribute every quote with source + approximate date.

Output format: markdown dossier organised by problem dimension, with minimum 3 verbatim quotes per dimension OR a marker noting "insufficient data" for that dimension.

Write to: clients/<project>/research/buyer-language-dossier.md
```

**Quality gate after return:** count verbatim quotes. If < 20 total across all dimensions, re-run with broader source list OR mark §5 Buyer Profile as partially-grounded.

---

## Source 3 — `deep-research` (Market Sentiment + Awareness)

**Skill location:** `skills/deep-research/SKILL.md`

**MECE decomposition for this skill invocation:**

```
Research decomposition (4 sub-agents):

Agent 1 — Market State
  - Market size, growth rate, saturation
  - Key players (top 10) with rough market share estimates
  - Recent shifts (last 12 months)
  - Regulatory / compliance changes

Agent 2 — Competitor Positioning
  - How top 5 competitors position themselves (category, audience, mechanism)
  - What's over-saturated vs blue ocean
  - Common claims / common failures
  - Gap analysis: what nobody is saying

Agent 3 — Awareness Distribution
  - What % of target market is Unaware / Problem-Aware / Solution-Aware / Product-Aware / Most Aware (Schwartz)
  - Evidence: search volume for problem-terms vs solution-terms vs brand-terms
  - Implication: where's the largest addressable pool?

Agent 4 — Sophistication Level (1-5)
  - How many established competitors making similar claims
  - Whether market has been burned by prior category claims
  - Schwartz stage (1-5) assessment with justification
  - Implication: what messaging stage should we play in?
```

**Output:** `clients/<project>/research/market-research.md` — 4 sections corresponding to the 4 sub-agents + a synthesis section with strategic implications.

---

## Source 4 — Product Snapshot (Mode B only)

**Tools:** WebFetch (primary) + dev-browser (authenticated or interactive pages)

**Scrape targets (in priority order):**
1. Homepage — value prop, hero claims, primary CTA
2. Pricing page — tiers, features, promos, guarantees
3. Testimonials / case studies page
4. FAQ — surfaces the objections the brand already knows about
5. About / founder — authority markers
6. Comparison / alternatives pages (if exists) — positioning claims

**Output:** `clients/<project>/research/product-snapshot.md` with structured sections for each scrape target.

**Cost optimisation:** for text-heavy pages (blog posts, long-form case studies), route summarisation through `scripts/research-llm.sh kilo "<extract the key buyer-language phrases and proof elements from this page>"` instead of Claude.

---

## Source 5 — `paid-media-audit` (Conditional)

**Only run if:** `clients/<project>/metrics-config.json` exists AND has a valid `ad_account_id`.

**Detection rule:** load `clients/<project>/metrics-config.json` → check for `ad_account_id` key → if present and non-null, run paid-media-audit. If missing, skip and note in manifest.

**What feeds back:**
- Top-performing creatives → §8 Proof Inventory (real performance data)
- Fatigue signals → §17 Iteration Rules (project-specific triggers)
- Audience gaps → §4 Segment Breakdown (which segments have thin coverage)
- Objection patterns in ad copy → §7 Objections (which objections are being handled vs ignored)

---

## Research Manifest

After all sources complete, write `clients/<project>/research/_manifest.json`:

```json
{
  "generated_at": "2026-04-17T14:32:00+08:00",
  "mode": "A",
  "project_slug": "<project-slug>",
  "sources": {
    "scrapecreators": {
      "status": "success",
      "competitors_pulled": ["<competitor-1>", "<competitor-2>", "<competitor-3>"],
      "ad_count": 47,
      "output_files": ["competitor-ads/<competitor-1>-raw.md", "competitor-ads/<competitor-2>-raw.md", "competitor-ads/<competitor-3>-raw.md"]
    },
    "buyer_language_researcher": {
      "status": "success",
      "sources_mined": ["reddit:r/<sub-1>", "reddit:r/<sub-2>", "notebooklm:<project-corpus>", "instagram:comments"],
      "verbatim_quote_count": 83,
      "output_file": "research/buyer-language-dossier.md"
    },
    "deep_research": {
      "status": "success",
      "sub_agents_completed": 4,
      "output_file": "research/market-research.md"
    },
    "product_snapshot": {
      "status": "skipped",
      "reason": "Mode A — product context already in clients/<project-slug>/offer.md"
    },
    "paid_media_audit": {
      "status": "success",
      "ad_account": "act_<ad_account_id>",
      "ads_analysed": 15,
      "output_file": "metrics/audit-YYMMDD.md"
    }
  },
  "total_duration_minutes": 8.2,
  "cost_optimisations_used": ["kilo-gateway for competitor-page summaries"]
}
```

This manifest feeds §26 Appendix of the source-of-truth doc (research provenance).

---

## Context Hygiene Rules

Per CLAUDE.md §4:

- **Spawn all 4-5 sources in ONE message** — parallel tool calls.
- **Do NOT poll** individual sub-agent output files mid-run.
- **Wait for completion notifications** before reading any output.
- **When reading outputs for Phase 3 synthesis**, read only the synthesised sections you need (not full 10k-word dossiers) — offset/limit where possible.
- **Use bash grep / jq** for extracting specific quotes from dossiers during synthesis, not full re-reads.

If any single research source fails:
- Mark status as "failed" in manifest with reason
- Continue synthesis with remaining sources
- Flag affected sections with ⚠️ NOT AVAILABLE in the final doc
- NEVER fabricate to fill gaps

---

## Performance Target

| Mode | Parallel research duration |
|---|---|
| Mode A (no product scrape, possibly audit) | 5-8 minutes |
| Mode B (full — all 5 sources) | 8-12 minutes |
| Mode C (no product scrape, no audit) | 5-10 minutes |

If any single source exceeds 20 minutes, abort it and continue. A source-of-truth with 4 of 5 sources is better than a source-of-truth that blocks indefinitely.
