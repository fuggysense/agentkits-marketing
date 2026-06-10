#!/usr/bin/env python3
"""
Parallel builder for Copywriting OS Phase B reviewers + grounding builders.

Spawns 6 fresh `claude -p` Sonnet 4.6 workers in parallel. Each worker receives
the same stable system prompt (content-cached after first worker warms the cache)
and a unique per-task prompt. Output = fully-populated markdown spec file.

Ravan pattern (see big-angle-spotter/scripts/run_pipeline.py):
- Fresh worker per question, `--no-session-persistence`
- `--tools ""` — no tool use, pure reasoning
- `--output-format json` — parse result field
- Content-addressable prompt cache on SP

Written 2026-04-24. TODO: migrate Sonnet alias to pinned `claude-sonnet-4-6` if
alias drifts — same migration path as Opus 4.6 → 4.7 before 2026-06-15.
"""

import json
import os
import re
import subprocess
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

REPO = Path("/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing")
OS_DIR = REPO / ".claude/references/copywriting-os"
TEMPLATE = OS_DIR / "reviewers/proof-density-audit.md"
INDEX = OS_DIR / "_index.md"
LOG_DIR = OS_DIR / "builders/build-logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "claude-sonnet-4-6"
TIMEOUT = 900
_TRAIL = re.compile(r"[\x00-\x1f\s]+$")

TEMPLATE_TEXT = TEMPLATE.read_text()
INDEX_TEXT = INDEX.read_text()

# Shared system prompt — identical across all 6 workers so it hits the
# content-addressable prompt cache after the first worker warms it.
SP = f"""# Role

You are a senior copywriting-OS architect. You author reusable reviewer and builder specifications for the Copywriting OS at `.claude/references/copywriting-os/`. Your specs are executed by sub-agents against client sales letters, ads, landing pages, and emails.

# Reference pattern (follow this structure exactly)

Here is the canonical reviewer spec. Match its voice, structure, heading order, tone, and depth. Your output must be interchangeable in quality and format:

---
{TEMPLATE_TEXT}
---

# Copywriting OS index (for ecosystem context)

{INDEX_TEXT}

# Output contract

**RETURN THE SPEC AS YOUR RESPONSE TEXT.** Do NOT attempt to write to any file, upload to any service, call any MCP tool, or use any file-writing mechanism. The caller captures your response text and persists it. If you try to write to disk yourself, the caller's post-processing will overwrite your work with nothing.

Your entire response must be the markdown spec. Nothing before it. Nothing after it. No "File written to...", no "Here is what I built", no "Key decisions". Just the spec, starting at character 1 with `# <Title>`.

- Produce ONE complete, drop-in-ready markdown spec file.
- Structure to match proof-density-audit.md: title line, source line, core principle, Agent model block, procedure (numbered steps), output schema (fenced code block with REAL field names, not placeholder slots), failure thresholds, cheap-wins section, logging instruction.
- FIRST CHARACTER of response MUST be `#`. FIRST LINE MUST be the title. NO preamble whatsoever.
- LAST CHARACTER should be part of the spec body. NO trailing "Actions taken" / "Key decisions" / "File written" meta-summary.
- Use exact file paths and tool names from the index context.
- Procedure steps must be mechanical — a Sonnet sub-agent should execute without judgment.
- Severity rules must be explicit (CRITICAL / HIGH / MEDIUM / LOW) with concrete examples.
- Failure thresholds must be quantitative (percentages, counts) not vibe-based.
- Logging pattern must match: append single-line pipe-delimited entry to `clients/<slug>/copy-system/quality-gates/<name>-log.md`.
- Target length: 130-180 lines. Density matches proof-density-audit.md.
- UK English (realise, colour, behaviour). No AI-triplets. No LinkedIn-influencer tone.
"""


def run_worker(prompt: str, output_path: Path, label: str) -> dict:
    session = str(uuid.uuid4())
    cmd = [
        "claude", "-p",
        "--model", MODEL,
        "--tools", "",
        "--output-format", "json",
        "--dangerously-skip-permissions",
        "--no-session-persistence",
        "--session-id", session,
        "--system-prompt", SP,
        prompt,
    ]
    t0 = datetime.now()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return {"label": label, "ok": False, "error": f"timeout after {TIMEOUT}s", "dt": TIMEOUT}

    dt = (datetime.now() - t0).total_seconds()
    if proc.returncode != 0:
        return {"label": label, "ok": False, "error": proc.stderr[:800], "dt": dt}
    try:
        data = json.loads(_TRAIL.sub("", proc.stdout))
    except json.JSONDecodeError:
        return {"label": label, "ok": False, "error": f"non-JSON stdout head: {proc.stdout[:400]}", "dt": dt}
    if data.get("is_error"):
        return {"label": label, "ok": False, "error": data.get("result", "")[:800], "dt": dt}

    result = data["result"]
    # Validation: result must start with `# ` to be a valid spec. If not, the
    # worker likely used an MCP tool to write and returned a meta-summary.
    # Preserve existing file, log error, don't clobber.
    if not result.lstrip().startswith("# "):
        return {"label": label, "ok": False,
                "error": f"response does not start with '# ' — preserving existing file. Head: {result[:200]}",
                "dt": dt}
    output_path.write_text(result.rstrip() + "\n")
    out_tok = data.get("usage", {}).get("output_tokens", 0)
    in_tok = data.get("usage", {}).get("input_tokens", 0)
    cache_read = data.get("usage", {}).get("cache_read_input_tokens", 0)
    cost = data.get("total_cost_usd", 0)
    (LOG_DIR / f"{label}.log.json").write_text(json.dumps({
        "label": label, "dt_sec": dt, "in_tok": in_tok, "out_tok": out_tok,
        "cache_read": cache_read, "cost_usd": cost, "session": session,
        "output_path": str(output_path),
    }, indent=2))
    return {"label": label, "ok": True, "path": str(output_path), "dt": dt,
            "out_tok": out_tok, "cache_read": cache_read, "cost": cost}


TASKS = [
    {
        "label": "1A_claim_verification",
        "output": OS_DIR / "reviewers/claim-verification-audit.md",
        "prompt": """Write the full spec for `claim-verification-audit.md` — reviewer B1 of 4 in the new Phase B anti-hallucination layer of the Copywriting OS.

Title: `# Claim Verification Audit — Post-Write Reviewer (sub-agent)`

Source line: Phase B anti-hallucination layer (internal — no external source newsletter; adapted from cai #38 proof framework).

Core principle: Every factual claim in the draft must trace to a specific line in a client grounding file. No claim without a source = potential hallucination.

Inputs the sub-agent receives:
- Draft under review (sales letter / ad / landing / email)
- `clients/<slug>/context-profile.json`
- `clients/<slug>/source-of-truth.md`
- `clients/<slug>/research/*.md` (all files in the folder)
- `clients/<slug>/avatars/*.md` (Raw Inner Dialogue, Deep Fears, Desired Transformation blocks)
- `clients/<slug>/copy-system/proof-inventory.md` (pre-populated by proof-inventory-builder — this is the primary cross-reference)

What counts as a "factual claim" (define precisely in the spec):
- Outcome claims ("saves X hours", "generates Y leads")
- Differentiation claims ("only firm that...", "first in Singapore...")
- Buyer-psychology claims that assert prevalence ("most couples feel...", "hundreds of buyers")
- Mechanism claims ("because our CRM tracks X, you get Y")
- Biographical/credential claims ("22 years of experience", "closed 500 deals")
- Testimonial income/result numbers
- Timeline claims ("in 30 days", "by week 3")
- Quantity claims ("14.3 hours per week")

What does NOT count (non-claim boundary — define in spec):
- Direct questions to reader
- Emotional framings that match buyer dossier tone (B4's concern)
- Generic truisms ("time is limited", "markets change")
- Metaphors unless they embed a specific claim
- Style choices (pacing, register)

Severity rules (give concrete examples for each):
- CRITICAL — outcome/guarantee/mechanism claim with zero source in any grounding file → auto-block
- HIGH — specific number or date without source ("22 years", "closed 500 deals") → block pending operator confirmation
- MEDIUM — broad prevalence claim with partial source ("many clients" when source says "some") → flag, propose specificity rewrite
- LOW — common-knowledge claim without source ("Singapore property market is competitive") → note, allow

Procedure (7 mechanical steps):
1. Load all grounding files into memory.
2. Parse draft into sentence-level claim candidates.
3. Apply claim/non-claim boundary rules.
4. For each confirmed claim, grep proof-inventory.md first, then fall back to source-of-truth.md, research/, avatars/, context-profile.json.
5. Record per-claim: draft line number, source file:line OR "NO SOURCE", severity, proposed proof type.
6. Compute metrics: coverage %, severity distribution.
7. Emit output schema + revision suggestions for top 3 unsourced.

Output schema (fenced markdown block with real field names):
- Total claims extracted
- Sourced count and unsourced count
- Coverage %
- Ordered list of unsourced claims with severity, draft line, near-source candidates, recommended action
- Sample of sourced claims with draft line → source path:line audit trail
- Verdict (PASS if coverage ≥ 95% AND zero CRITICAL unsourced, else FAIL)

Failure thresholds:
- Any CRITICAL unsourced claim → auto-FAIL
- Coverage < 95% → FAIL
- Coverage 95-99% with only LOW severity → PASS with warnings

Cheap-wins section (specific patterns to check first):
- Fabricated years-of-experience numbers (common LLM hallucination pattern)
- Testimonial income figures without a real testimonial file
- Made-up case study outcomes
- Invented prevalence ("hundreds of Singapore agents" without data)

Logging: `clients/<slug>/copy-system/quality-gates/claim-verification-log.md`, one pipe-delimited line per run.

Write the full spec now. UK English. Match proof-density-audit.md density (130-180 lines).""",
    },
    {
        "label": "1B_forbidden_content",
        "output": OS_DIR / "reviewers/forbidden-content-audit.md",
        "prompt": """Write the full spec for `forbidden-content-audit.md` — reviewer B2 of 4.

Title: `# Forbidden Content Audit — Post-Write Reviewer (sub-agent)`

Source line: Phase B anti-hallucination layer (internal, integrates unslop/overused-ai-patterns Layer 2).

Core principle: Every client has language, angles, framings, or claims that are off-limits — saturated phrases, brand-voice violations, legal constraints, burned angles already spent in prior DCT waves. Any violation breaks voice or trust. Plus: generic AI-tell patterns (LinkedIn-influencer tone, AI-triplets) must be caught even when not client-specific.

Inputs the sub-agent receives:
- Draft under review
- `clients/<slug>/learnings.md` (saturated phrases, voice corrections)
- `clients/<slug>/CLAUDE.md` if it exists (project constraints)
- `clients/<slug>/angles/iteration-log.md` if present (burned angles from prior waves)
- `clients/<slug>/brand-voice.md` (voice rules)
- Global `voice/<person>/brand-voice.md` (Jerel's personal voice rules if applicable)
- Global unslop profile for the content type if present (e.g., `skills/unslop/profiles/singapore-sales-letter.md`)

What counts as forbidden (define categories in spec):
- Category F1: Client-specific banned phrases (pulled from learnings.md "do not use" entries)
- Category F2: Saturated angles (angle names/themes already used in previous DCT waves — re-using burns the wave)
- Category F3: Brand-voice violations (tone mismatches — e.g., "investment" if client sells consulting not finance)
- Category F4: AI-tell patterns (LinkedIn-influencer triplets "not X, not Y, but Z", overused transitions "in today's fast-paced world", em-dash overuse, emoji-header patterns)
- Category F5: Legal/compliance words flagged in client context (e.g., "guaranteed" for regulated verticals)
- Category F6: Hard-sell language client has flagged (e.g., "act now", "limited time" if client avoids high-pressure)

Severity rules:
- CRITICAL — F1 banned phrase or F5 compliance violation → auto-block
- HIGH — F2 saturated angle re-used as primary theme → block pending operator confirm (can be deliberate if operator wants to re-test)
- MEDIUM — F3 voice drift or F6 hard-sell drift → flag with rewrite
- LOW — F4 AI-tell pattern → flag, must be fixed before ship but not blocking

Procedure (6 steps):
1. Load all forbidden-content sources into categorised lookup tables.
2. Scan draft line-by-line, matching against each category.
3. For F4 AI-tell patterns, apply regex/substring rules from the unslop profile or embed a minimal 15-pattern list in the spec.
4. For each hit: record category, severity, draft line, offending phrase, rewrite suggestion.
5. Compute violation counts per category.
6. Emit output schema.

Output schema (fenced):
- Total violations per category (F1-F6)
- Ordered violations with category/severity/line/phrase/rewrite
- Saturated-angle check: list of burned angles + verdict (new angle / re-use / collision)
- AI-tell density: violations per 1000 words
- Verdict (PASS = zero CRITICAL AND zero HIGH AND AI-tell density < 2 per 1000 words, else FAIL)

Failure thresholds:
- Any CRITICAL → auto-FAIL
- Any HIGH without operator override flag → FAIL
- AI-tell density ≥ 2 per 1000 words → FAIL
- More than 3 MEDIUM → FAIL

Cheap-wins section:
- Search for "investment" if client is not finance/property
- Search for em-dash frequency (Jerel hates >3 per 1000 words per learnings)
- Search for "in today's" / "in the world of" / "at the end of the day" (stock LinkedIn openers)
- Search for "whether you're X or Y" triplet structure

Logging: `clients/<slug>/copy-system/quality-gates/forbidden-content-log.md`, pipe-delimited.

Write the full spec. UK English. 130-180 lines.""",
    },
    {
        "label": "1C_specificity",
        "output": OS_DIR / "reviewers/specificity-audit.md",
        "prompt": """Write the full spec for `specificity-audit.md` — reviewer B3 of 4.

Title: `# Specificity Audit — Post-Write Reviewer (sub-agent)`

Source line: Phase B anti-hallucination layer. Complements cai #38 Specificity proof type (from proof-density-audit.md) — this reviewer focuses narrowly on weasel-word → concrete-number substitutions.

Core principle: Weasel words ("most", "many", "some", "a lot", "often", "usually", "several", "numerous", "a handful") are specificity leaks. If the client's grounding files contain a concrete number that applies, the draft MUST use the concrete number. "Most couples" is a failure when research says "67% of HDB upgraders aged 32-42". Round numbers ("10x", "2x", "thousands") are also suspect — push to exact.

Inputs:
- Draft under review
- `clients/<slug>/context-profile.json` (numeric fields: MRR, customer count, pricing tiers, etc.)
- `clients/<slug>/source-of-truth.md` (§5, §7.5 — market stats + misconception numbers)
- `clients/<slug>/research/*.md` (any research containing percentages, counts, timelines)

What counts as a specificity leak:
- Weasel quantifiers (see list above)
- Round multipliers ("10x faster", "2x more") without anchor number
- Vague timelines ("quickly", "soon", "in no time", "before long")
- Vague costs ("affordable", "cheap", "a fraction of", "way less")
- Vague outcomes ("better results", "significant improvement", "huge difference")
- Generic superlatives without number ("best-in-class", "top-tier", "leading")
- Plural references that mask count ("clients tell us", "buyers often say" — how many? exactly?)

What does NOT count (define boundary):
- Stylistic intensifiers where no number exists in research ("incredibly frustrating" — emotional, not factual)
- Deliberate hedging in legal-sensitive copy ("may help" where operator specifically requested non-committal)
- Rhetorical flourishes in closing sentences

Severity rules:
- CRITICAL — vague claim in a headline, hero, or CTA where research has the exact number → auto-block
- HIGH — vague claim in body where research has the number → block, demand specific rewrite
- MEDIUM — round multiplier without anchor + research supports specific multiplier → flag rewrite
- LOW — generic hedge where research genuinely lacks a number → note, may allow

Procedure (6 steps):
1. Build a lookup index from context-profile.json + source-of-truth.md §5/§7.5 + research/ of every extractable number with its context.
2. Scan draft for weasel-word list matches (provide a full 40+ term list in the spec).
3. For each match, compute: can this be specified from the index? If yes, severity = HIGH or CRITICAL.
4. Flag round-multiplier patterns separately.
5. Emit per-hit record: line, weasel phrase, available specific alternative, recommended rewrite.
6. Compute density metric (weasel words per 1000 words of draft).

Output schema (fenced):
- Weasel word density per 1000 words
- Ordered leaks with severity/line/vague phrase/available specific/proposed rewrite
- Round-multiplier leaks (separate list)
- Unspecifiable hedges (no source number — may allow, flag LOW)
- Verdict (PASS = zero CRITICAL, ≤ 1 HIGH, density < 4 per 1000 words, else FAIL)

Failure thresholds:
- Any CRITICAL → auto-FAIL
- More than 1 HIGH → FAIL
- Density ≥ 4 weasel words per 1000 words → FAIL

Cheap-wins section:
- Grep "most" and "many" first — usually 3-5 hits per sales letter
- Grep "often", "usually", "typically"
- Check headlines + CTAs first (CRITICAL severity zone)
- Look for "a lot of" — almost always replaceable with number

Logging: `clients/<slug>/copy-system/quality-gates/specificity-log.md`, pipe-delimited.

Include a 40+ term weasel-word reference list embedded in the spec so the sub-agent does not need to derive it.

Write the full spec. UK English. 130-180 lines.""",
    },
    {
        "label": "1D_buyer_language_fidelity",
        "output": OS_DIR / "reviewers/buyer-language-fidelity-audit.md",
        "prompt": """Write the full spec for `buyer-language-fidelity-audit.md` — reviewer B4 of 4.

Title: `# Buyer Language Fidelity Audit — Post-Write Reviewer (sub-agent)`

Source line: Phase B anti-hallucination layer. Integrates Schwartz "enter the conversation" + Collier + cai #42.

Core principle: Quoted buyer language must be verbatim-matched to research files. Paraphrases must preserve meaning, register, and emotional tone. A fabricated "buyer quote" is a hallucination. A paraphrase that makes the buyer sound more articulate, more polished, or more marketer-like than the raw research is WORSE — it replaces authentic voice with marketing voice and breaks the core channeling principle.

Inputs:
- Draft under review
- `clients/<slug>/research/buyer-language-dossier.md` (verbatim buyer quotes from Reddit, forums, interviews)
- `clients/<slug>/research/life-transition-dossier-*.md` (context quotes)
- `clients/<slug>/avatars/*.md` (Raw Inner Dialogue blocks — first-person voice samples)
- `clients/<slug>/source-of-truth.md` §5.7 (ICP Language Analysis section)
- Any testimonial files in `clients/<slug>/testimonials/`

What counts as "buyer language" in the draft (define in spec):
- Anything in quotation marks attributed to a buyer ("Riduan said: 'I was scared…'")
- First-person paraphrased thoughts ("you're lying awake wondering if…", "the voice in your head asks…")
- Attributed testimonial snippets
- Named case-study quotes
- "What our clients say" style framings

Detection procedure:
1. Parse draft for quotation marks, italics-as-thought, attributed statements.
2. For each detected buyer-language instance, classify as: VERBATIM_QUOTE, PARAPHRASED_THOUGHT, TESTIMONIAL, CASE_STUDY_QUOTE.
3. For VERBATIM_QUOTE and TESTIMONIAL: grep research/testimonials for exact string match (or ≥90% fuzzy match). Missing = hallucination.
4. For PARAPHRASED_THOUGHT: grep Raw Inner Dialogue + buyer-language-dossier for the concept. Extract the closest source quote. Compare register + emotional tone.
5. Score drift: PASS (preserves meaning + register), DRIFT_LOW (small polish), DRIFT_HIGH (register upshifted, buyer made more articulate/marketer-y), DRIFT_FATAL (meaning changed OR no source found).
6. For CASE_STUDY_QUOTE: verify case study exists in client files with named buyer, verify numbers match.

Register-drift patterns to catch (define with examples):
- Raw buyer: "I'm stuck lah, no clue what to do" → Draft: "I found myself in a state of uncertainty" (FATAL — upshifted register)
- Raw buyer: "Scared I buy then market drop" → Draft: "I harboured concerns about market volatility" (FATAL — formalised)
- Raw buyer: "Bo bian already" → Draft: "I had no other option" (DRIFT_HIGH — lost Singlish register)
- Raw buyer: "Macam feel like being cheated" → Draft: "It felt almost deceptive" (DRIFT_HIGH — drops local register)

Severity rules:
- CRITICAL — VERBATIM_QUOTE or TESTIMONIAL with no source match → auto-block (fabricated quote)
- CRITICAL — CASE_STUDY_QUOTE with mismatched numbers → auto-block
- HIGH — DRIFT_FATAL on paraphrased thought → block, rewrite to source-matching register
- MEDIUM — DRIFT_HIGH register upshift → flag, suggest downshift
- LOW — DRIFT_LOW polish → note, may allow

Output schema (fenced):
- Total buyer-language instances detected
- Breakdown by type (VERBATIM / PARAPHRASED / TESTIMONIAL / CASE_STUDY)
- Fidelity scores: verbatim-matched / drift-low / drift-high / drift-fatal / no-source
- Ordered violations with type/severity/draft line/raw source line/rewrite
- Register audit: does draft preserve Singlish, UK English, blue-collar, professional, or whatever register the raw research shows?
- Verdict (PASS = zero CRITICAL, zero HIGH, else FAIL)

Failure thresholds:
- Any CRITICAL (fabricated quote) → auto-FAIL
- Any HIGH (fatal drift) → FAIL
- More than 2 MEDIUM → FAIL

Cheap-wins section:
- Grep quotation marks first — every one gets source-matched
- Check for formal vocabulary ("harboured", "endeavoured", "pertaining to") in buyer-language sections — almost always drift
- Check for Singlish presence in draft vs. raw — dropped Singlish often means upshift drift
- Verify testimonial names exist in testimonials/ folder or research notes

Logging: `clients/<slug>/copy-system/quality-gates/buyer-language-fidelity-log.md`, pipe-delimited.

Write the full spec. UK English. 140-190 lines (this one runs slightly longer due to drift examples).""",
    },
    {
        "label": "2A_proof_inventory_builder",
        "output": OS_DIR / "builders/proof-inventory-builder.md",
        "prompt": """Write the full spec for `proof-inventory-builder.md` — a PRE-WRITE builder that populates `clients/<slug>/copy-system/proof-inventory.md`.

Title: `# Proof Inventory Builder — Pre-Write Grounding Support`

Source line: Pre-write grounding layer. Feeds B1 claim-verification-audit directly. Extends cai #38 Mark Masters proof framework.

Core principle: Before copy is drafted, harvest every citable claim from client files into one queryable inventory. Tagged by the 6 proof types (Social / Credentials / Demonstration / Logical / Specificity / Implied). This is the source-of-truth for claim verification and the drafter's lookup table for "what can I actually say about this client with support."

Inputs the builder reads:
- `clients/<slug>/context-profile.json` (structured client identity)
- `clients/<slug>/source-of-truth.md` (all sections, §5 Evidence + §5.5 Golden Nuggets + §5.7 ICP Language especially)
- `clients/<slug>/research/*.md`
- `clients/<slug>/avatars/*.md`
- `clients/<slug>/testimonials/*.md` if folder exists
- `clients/<slug>/learnings.md` (sometimes has validated claims)
- `clients/<slug>/case-studies/*.md` if exists

Procedure (7 steps):
1. Load all input files.
2. Scan each file for claim candidates (same taxonomy as B1: outcome, differentiation, mechanism, credential, timeline, quantity).
3. For each candidate, tag one or more of the 6 proof types it could fuel.
4. Record: claim text, source file:line, proof type(s), strength (VERIFIED / NEAR-VERIFIED / UNVERIFIED), recency (if dated).
5. Deduplicate — merge identical claims from different sources into one entry with multiple source lines.
6. Rank within proof type by strength then recency.
7. Emit output markdown.

Output schema (fenced) — THIS IS THE FORMAT THAT `clients/<slug>/copy-system/proof-inventory.md` MUST MATCH, so B1 can read it reliably:
- Metadata block: client slug, built-on date, source file count, total claims
- For each of 6 proof types:
  - Section heading
  - Numbered list of claims with fields: claim text, source(s) as `file.md:LN`, strength tag, recency, one-line usage note
- "Cross-cutting" section: claims that serve multiple proof types, reference only
- "Gaps" section: proof types with < 3 claims — flag for operator to gather more
- "Do not cite" section: claims that appeared but were flagged as unverified, stale, or retracted in learnings.md

The builder itself produces this file — the SPEC in this doc tells the sub-agent HOW to produce it.

Quality rules:
- Every entry needs a source:line reference (not just file name)
- Verbatim claim text where possible; summary allowed only if flagged as `SUMMARY:` prefix
- Strength tagging is binary-conservative: mark VERIFIED only if source explicitly states the fact; NEAR-VERIFIED if source implies; UNVERIFIED if claim is operator guess
- If a claim has no source strong enough to be NEAR-VERIFIED, flag for "Gaps" section, do not list as usable

Failure thresholds for the builder (when it should refuse to emit):
- If source-of-truth.md is missing → halt, demand upstream
- If fewer than 5 claims total can be harvested → emit with "WARNING: thin proof base" header
- If all claims are UNVERIFIED → halt, demand research refresh

Invocation pattern (include in spec):
- Can be called pre-draft by `/copy:*` sub-commands as a prerequisite step
- Can be called manually via `/copy:build-inventory <slug>` (add this command to roadmap)
- Re-runs on demand; overwrites existing inventory; backs up old to `proof-inventory.md.prev`

Logging: append summary line to `clients/<slug>/copy-system/quality-gates/builder-log.md` with date, claim count, gaps flagged.

Write the full spec. UK English. 140-190 lines.""",
    },
    {
        "label": "2B_objection_matrix_builder",
        "output": OS_DIR / "builders/objection-matrix-builder.md",
        "prompt": """Write the full spec for `objection-matrix-builder.md` — a PRE-WRITE builder that populates `clients/<slug>/copy-system/objection-matrix.md`.

Title: `# Objection Matrix Builder — Pre-Write Grounding Support`

Source line: Pre-write grounding layer. Integrates cai #36 Mark Masters 6 objection categories. Feeds the drafter + objection-coverage-audit reviewer.

Core principle: Before copy is drafted, map every objection the buyer actually raises — from research, forums, sales calls, churn interviews, support tickets — into the 6 canonical categories. Each objection pairs with a handler grounded in THIS client's real context (not generic copywriting advice). The drafter then pre-empts objections rather than ignoring them; objection-coverage-audit verifies all 6 categories were addressed.

Inputs the builder reads:
- `clients/<slug>/buyer-profile.md` (pain points, fears, hesitations)
- `clients/<slug>/learnings.md` (objections the operator has heard repeatedly)
- `clients/<slug>/source-of-truth.md` (§7 Objections if present, §7.5 Misconceptions)
- `clients/<slug>/faqs.md` if exists
- `clients/<slug>/research/buyer-language-dossier.md` (raw buyer concerns)
- `clients/<slug>/avatars/*.md` (Top 5 Deep Fears, Objections blocks)
- Sales-call transcripts or churn interviews if in `clients/<slug>/interviews/`

The 6 objection categories (cai #36) — spec must name and define each:
- O1 Price — too expensive, not in budget, cheaper alternatives exist
- O2 Trust — you might not deliver, I don't know you, social proof thin
- O3 Fit — this doesn't apply to me, my situation is different, I'm too small/big/early/late
- O4 Timing — not now, I'll come back later, need to think
- O5 Authority — I need to ask my spouse/partner/boss, I can't decide alone
- O6 Effort — too hard to implement, steep learning curve, I don't have time

Procedure (7 steps):
1. Load all input files.
2. Extract every objection-shaped statement from inputs (any sentence expressing hesitation, fear, comparison, or delay).
3. Classify each into one of O1-O6.
4. For each objection, find or synthesise a HANDLER grounded in client context. A handler is 1-3 sentences that: (a) acknowledges the objection, (b) reframes or resolves it using a specific client fact/proof/mechanism, (c) is written in the client's voice register.
5. If an objection has no grounded handler available, flag as GAP (operator must supply).
6. Rank objections within each category by frequency (how many source files it appears in).
7. Emit output markdown.

Output schema (fenced):
- Metadata block: client slug, built-on date, source count, total objections, gaps
- For each of O1-O6:
  - Category heading + definition line
  - Top 3-5 objections from this client's buyers (ordered by frequency)
  - For each objection: verbatim quote or paraphrased statement, source:line, handler text, handler proof-source:line, tone note
- "Cross-category" section: objections that span categories (e.g., price-timing hybrids)
- "Gaps" section: categories with fewer than 2 concrete objections from this client's buyers — flag for research refresh
- "Pre-emption priority" section: which objection per category should be handled FIRST in copy (usually the most frequent + most blocking)

Quality rules:
- Every objection needs a source reference
- Every handler needs a proof-source reference (which client fact/testimonial/mechanism it leans on)
- Handlers in client voice register (use buyer-language-dossier as register reference)
- Singlish / UK English preserved where client voice demands

Failure thresholds:
- Any category with zero concrete objections → flag GAP, builder emits with warning header
- Any handler without proof-source → flag HANDLER_GAP
- Fewer than 12 objections total across 6 categories → warn "thin objection base"

Invocation pattern:
- Called pre-draft by `/copy:*` sub-commands
- Manual: `/copy:build-objections <slug>` (add to roadmap)
- Re-runs overwrite; backup to `objection-matrix.md.prev`

Logging: append summary to `clients/<slug>/copy-system/quality-gates/builder-log.md` (shared log with proof-inventory-builder).

Write the full spec. UK English. 140-190 lines.""",
    },
]


def main():
    import sys as _sys
    filter_labels = None
    if len(_sys.argv) > 1 and _sys.argv[1] == "--labels":
        filter_labels = set(_sys.argv[2].split(","))
    tasks_to_run = [t for t in TASKS if filter_labels is None or t["label"] in filter_labels]
    print(f"[{datetime.now():%H:%M:%S}] Copywriting-OS builder — {len(tasks_to_run)} parallel Sonnet 4.6 workers", flush=True)
    print(f"[{datetime.now():%H:%M:%S}] Model: {MODEL}, timeout: {TIMEOUT}s per worker", flush=True)
    print(f"[{datetime.now():%H:%M:%S}] SP length: {len(SP)} chars ({len(SP)//4} est tokens)", flush=True)
    if filter_labels:
        print(f"[{datetime.now():%H:%M:%S}] Running filtered labels: {sorted(filter_labels)}", flush=True)
    print("", flush=True)

    t0 = datetime.now()
    results = []
    with ThreadPoolExecutor(max_workers=max(1, len(tasks_to_run))) as pool:
        futures = {
            pool.submit(run_worker, t["prompt"], t["output"], t["label"]): t["label"]
            for t in tasks_to_run
        }
        for f in as_completed(futures):
            r = f.result()
            results.append(r)
            status = "OK " if r["ok"] else "FAIL"
            if r["ok"]:
                cache = r.get("cache_read", 0)
                print(f"[{datetime.now():%H:%M:%S}] {status} [{r['label']}] {r['dt']:.1f}s "
                      f"out={r['out_tok']} cache_read={cache} ${r['cost']:.4f} → {Path(r['path']).name}",
                      flush=True)
            else:
                print(f"[{datetime.now():%H:%M:%S}] {status} [{r['label']}] {r['dt']:.1f}s — {r['error'][:200]}",
                      flush=True)

    total_dt = (datetime.now() - t0).total_seconds()
    ok_count = sum(1 for r in results if r["ok"])
    total_cost = sum(r.get("cost", 0) for r in results)
    print("", flush=True)
    print(f"[{datetime.now():%H:%M:%S}] SUMMARY: {ok_count}/6 ok, total {total_dt:.1f}s, ${total_cost:.4f}",
          flush=True)
    (LOG_DIR / f"run-{datetime.now():%Y%m%d-%H%M%S}.json").write_text(
        json.dumps({"results": results, "total_dt": total_dt, "total_cost": total_cost}, indent=2, default=str)
    )
    return 0 if ok_count == 6 else 1


if __name__ == "__main__":
    sys.exit(main())
