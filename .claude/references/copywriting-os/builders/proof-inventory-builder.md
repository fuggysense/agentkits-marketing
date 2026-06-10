# Proof Inventory Builder — Pre-Write Grounding Support

**Source:** Pre-write grounding layer. Feeds B1 claim-verification-audit directly. Extends cai #38 Mark Masters proof framework.

**Core principle:** Before copy is drafted, harvest every citable claim from client files into one queryable inventory. Tagged by the 6 proof types (Social / Credentials / Demonstration / Logical / Specificity / Implied). This is the source-of-truth for claim verification and the drafter's lookup table for "what can I actually say about this client with support." Copy that invents claims it cannot source is not confidence — it is liability.

**Agent model:** Pre-write builder sub-agent. Runs before any drafter is invoked. Output is consumed by: B1 `claim-verification-audit.md`, B3 `specificity-audit.md`, Phase C `proof-density-audit.md`, and the drafter itself as a lookup table during writing.

## Inputs

Read all files that exist. Skip gracefully if optional files are absent; log skipped paths in the metadata block.

| File | Status | Purpose |
|------|--------|---------|
| `clients/<slug>/context-profile.json` | Required | Client identity, product claims, founding story |
| `clients/<slug>/source-of-truth.md` | Required (halt if missing) | Primary evidence well — §5 Evidence, §5.5 Golden Nuggets, §5.7 ICP Language |
| `clients/<slug>/research/*.md` | Optional | Market research, competitor data, third-party validation |
| `clients/<slug>/avatars/*.md` | Optional | Validated pain/desire language that can source implied proof |
| `clients/<slug>/testimonials/*.md` | Optional | Direct social proof with attribution |
| `clients/<slug>/learnings.md` | Optional | Validated claims from past campaigns; also contains retracted claims |
| `clients/<slug>/case-studies/*.md` | Optional | Outcome data, before/after figures |

## Procedure

### Step 1 — Load all input files

Read every file in the inputs table. Record which files were found and which were absent. If `source-of-truth.md` is missing, halt immediately — see Failure Thresholds.

### Step 2 — Scan for claim candidates

A claim candidate is any statement a reader could be asked to believe about: outcome, differentiation, mechanism, credential, timeline, or quantity. Scrape every such statement from every loaded file. Note the source file name and approximate line number for each.

### Step 3 — Tag proof type(s) per candidate

For each candidate, assign one or more of the 6 proof types it could fuel in copy:

1. **Social** — testimonial text, review quote, user count, logo, case-study result with attribution
2. **Credentials** — degree, years in practice, media mention, award, certification, featured-in placement
3. **Demonstration** — screenshot reference, before/after figure, live example, measurable product output
4. **Logical** — mechanism explained with causation ("because X → Y"), analogy, if-then chain
5. **Specificity** — exact number, precise date, named process, specific dollar figure, named client
6. **Implied** — detail depth, confident restraint, refusal to overclaim — must trace to a voice note or writing sample, not invented

### Step 4 — Assign strength and recency

For each candidate:
- **VERIFIED** — source file explicitly states the fact with attribution or measurement
- **NEAR-VERIFIED** — source implies or paraphrases; inference is reasonable but not explicit
- **UNVERIFIED** — operator assertion with no supporting source file; route to Gaps, not to usable sections

Recency: record the date if the claim appears in a dated document. Mark `UNDATED` otherwise.

### Step 5 — Deduplicate

Merge identical or near-identical claims from different source files into a single inventory entry. List all source file:line references on that entry. A claim appearing in both `source-of-truth.md` and a testimonial is stronger, not duplicated — reflect that by listing both sources.

### Step 6 — Rank within proof type

Within each proof type section: VERIFIED before NEAR-VERIFIED before UNVERIFIED. Within equal strength: dated-recent before dated-older before UNDATED.

### Step 7 — Emit proof-inventory.md

Write the output file to `clients/<slug>/copy-system/proof-inventory.md`. If a previous inventory exists, rename it to `proof-inventory.md.prev` before writing. Follow the output schema below exactly — B1 parses by section heading; heading names must not deviate.

## Output schema

```
---
client: <slug>
built: YYMMDD-HHMM
source_files_loaded: N
source_files_missing: [list or none]
total_claims: N
verified: N | near-verified: N | unverified: N
---

⚠️ WARNING: THIN PROOF BASE — fewer than 5 usable claims harvested.
[Remove this line if total_claims ≥ 5]

## Social Proof
1. **Claim:** "<verbatim or SUMMARY: paraphrase>"
   Source: `source-of-truth.md:L42`, `testimonials/rachel-h.md:L3`
   Strength: VERIFIED
   Recency: YYYY-MM-DD | UNDATED
   Usage note: <one line — which copy element this supports>

[Repeat per entry. Section flag suppressed only if ≥ 3 VERIFIED or NEAR-VERIFIED entries exist.]

## Credentials
[same structure]

## Demonstration
[same structure]

## Logical
[same structure]

## Specificity
[same structure]

## Implied
[same structure]

## Cross-Cutting Claims
Claims that serve 2+ proof types. Reference only — full entry listed above.
- "<short claim>" → Social + Specificity — see Social #2

## Gaps
Proof types with fewer than 3 VERIFIED or NEAR-VERIFIED entries. Operator must gather before copy ships.
- **Social:** only 1 usable entry — gather 2+ testimonials with measurable outcomes
- **Demonstration:** 0 entries — screenshots, before/after, or product walkthroughs needed

## Do Not Cite
Claims that appeared in source files but are blocked from copy use.
1. "<claim text>" — Reason: UNVERIFIED / stale (dated YYYY-MM) / retracted in learnings.md:LN
```

## Failure thresholds

- `source-of-truth.md` absent → **halt**. Emit: `ERROR: source-of-truth.md not found for <slug>. Run /ads:source-of-truth first.` Do not produce a partial inventory.
- Fewer than 5 total claims across all types → emit with `⚠️ WARNING: THIN PROOF BASE` header. Do not halt — the warning is itself the deliverable. Flag in Gaps.
- All harvested claims UNVERIFIED → **halt**. Emit: `ERROR: zero verifiable claims found. Research refresh required before copy proceeds.`
- Any claim retracted or disproved in `learnings.md` → move to Do Not Cite regardless of how strong other sources appear.

## Quality rules

**Source:line is mandatory.** A claim without a file reference is noise, not an inventory entry. If line number cannot be pinned precisely, use the nearest section heading as anchor (e.g. `source-of-truth.md:§5.5`).

**Verbatim first.** Use exact words from the source wherever possible. Summaries introduce drift — if unavoidable, prefix with `SUMMARY:` so downstream reviewers know to re-verify wording before use.

**The two richest sections to mine first:**

1. **§5.5 Golden Nuggets** in `source-of-truth.md` — selected for persuasive weight; treat as highest-priority Specificity and Demonstration candidates.
2. **Testimonials folder** — even a thin testimonial yields Social proof. A single attributed sentence with a name is a usable entry.

**Implied proof needs a source.** It cannot be invented. It must trace to a voice note, a writing sample, or a specific detail that demonstrates expertise. Without that trace, it is not Implied proof — it is wishful thinking. Do not create an Implied entry from nothing.

## Invocation pattern

- **Auto-invoked** as a prerequisite step by all `/copy:*` sub-commands before the drafter fires.
- **Manual invocation:** `/copy:build-inventory <slug>` — add to command roadmap.
- **Re-runs overwrite** the existing inventory after backing up to `proof-inventory.md.prev`.
- If an inventory already exists and was built within the same calendar day, `/copy:*` sub-commands may skip rebuild and use the cached file — the builder logs the timestamp in the metadata block for this check.

## Logging

Append to `clients/<slug>/copy-system/quality-gates/builder-log.md`:
`| YYMMDD-HHMM | proof-inventory.md | sources N | claims N | verified N | gaps [list types] | status OK/WARN/HALT |`
