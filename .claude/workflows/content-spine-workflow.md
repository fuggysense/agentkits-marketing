# Content Spine Workflow

> The spine that keeps every channel saying the same thing. Compile the foundation once, read it many times, never re-derive a channel's message from raw transcripts. This doc sits ALONGSIDE `creative-pipeline.md` — it does not replace it. The ads sub-loop (research to concept to brief to create to test to feedback) still belongs to creative-pipeline; this spine is the layer above that feeds it and every other output.

## 1. Purpose

Every marketing output a client needs — sales letter, ads, email, organic posts, video, landing page — should say the same thing about the same offer to the same buyer. Drift happens when each channel re-invents the mechanism, the proof, and the objections from raw research on its own. This workflow stops that. You compile one foundation from raw research, then every output reads that foundation instead of going back to the transcripts.

## 2. The three layers (Layer 1 to 2 to 3, one direction)

Work flows one way only. Raw in. Compiled foundation in the middle. Outputs at the end. Nothing downstream reaches back past the foundation.

```
LAYER 1  RAW INPUT
  sales-call transcripts · buyer-language research · competitor scrapes
  lands in:  _brand/  +  research-vault
        │
        ▼  (compiled ONCE)
LAYER 2  COMPILED FOUNDATION  ← THE KEYSTONE
  WHO we sell to · WHAT we sell · the MASTER DOC (mechanism, proof,
  objections, big idea, claims) · the ANGLES
  lands in:  _brand/  +  campaigns/<c>/angles/
        │
        ▼  (every output reads Layer 2 — none re-read Layer 1)
LAYER 3  OUTPUTS
  sales letter · ads · email · organic content · video · landing page
```

The single rule that makes this work: a Layer-3 output reads Layer 2 and stops there. It never re-derives the mechanism or the proof from a raw transcript. That re-derivation is exactly how a channel drifts off-message.

## 3. Skill at each layer

| Layer | What gets built | Owning skill | Folder home |
|---|---|---|---|
| 1 — Raw | Sales-call transcripts | `transcribe` | `research-vault/` |
| 1 — Raw | Buyer-language dossier (voice of customer) | `research` / `buyer-language-researcher` | `_brand/` + `research-vault/` |
| 1 — Raw | Competitor scrapes (ads, posts) | `scrapecreators` | `_swipe/` + `research-vault/` |
| 2 — Foundation | WHO (avatars + buyer profile) | `avatar-research` | `_brand/avatars/` + `_brand/buyer-profile.md` |
| 2 — Foundation | WHAT we sell (the offer) | `offer-builder` | `_brand/offer.md` |
| 2 — Foundation | MASTER DOC (mechanism, proof, objections, big idea, claims) | `source-of-truth` | `_brand/source-of-truth.md` |
| 2 — Foundation | ANGLES (strategic, per campaign) | `big-angle-spotter` (hardened gate) | `campaigns/<c>/angles/` |
| 3 — Output | Sales letter | `sales-letter-method` | `campaigns/<c>/sales-letters/<slug>/` |
| 3 — Output | Meta ad text (primary + headline field) | `headline-bank` | per DCT (see creative-pipeline) |
| 3 — Output | Ad overlay text + image-gen prompts | `big-angle-spotter` | per DCT |
| 3 — Output | Ad batch orchestration | `ad-concept-engine` | `campaigns/<c>/dcts/` |
| 3 — Output | Email + sequences | `email-sequence` (copy) + `email-marketing` (strategy) | per campaign |
| 3 — Output | Organic content | `copywriting` | per campaign |
| 3 — Output | Video | `vid-director` | `campaigns/<c>/video-concepts/` |
| 3 — Output | Landing page | `copywriting` + `page-cro` | per campaign |

## 4. The conditional keystone rule

The keystone is the compiled Layer-2 foundation. It is NOT the sales letter, and it is NOT the raw transcripts. Everything in Layer 3 leans on Layer 2. So the one question that matters is: where is the richest Layer 2 for THIS client?

That depends on whether a sales letter exists. The letter is a special case. It is both a Layer-3 output AND the most rigorous way to forge Layer 2 — because writing one forces you to name the mechanism, audit every claim, and map every objection. Nothing else makes you do all three at once.

**The one-line fork check:** is a letter file present in `campaigns/<c>/sales-letters/`? Yes -> letter fork (read `letter-assets.json`). None -> source-of-truth fork (read `source-of-truth.md` + the compiled angles).

So the foundation forks:

- **When a letter exists** — its locked assets ARE the richest Layer 2. The letter's `letter-assets.json` (mechanism, proof library, objection matrix, offer stack, big idea, segment, narrator POV) is what email, ads, and landing pages read. The letter did the hard compile work; reuse it.
- **When no letter exists** — e.g. a paid-ads-first client, or a market where the long letter never gets written — Layer 2 is `source-of-truth.md` plus the compiled angles, built directly from Layer 1.

Letter-when-it-fits, source-of-truth-when-it-doesn't. Both forks feed the same Layer 3. Pick the fork per client; don't force a letter where the work is ads-only.

## 5. Siblings, not a chain

Angles and the letter are sibling branches off the same parent (avatar + offer). They are NOT a chain.

```
        avatar  +  offer
         /              \
    ANGLES            LETTER
 (big-angle-spotter)  (sales-letter-method)
```

The letter's mechanism comes from the offer, not from an angle. Do not hard-wire angles into the letter's mechanism. An angle file MAY optionally inform the letter's lead framing — that is the only permitted link, and it is optional. Wiring angles as a required input to the letter would couple two things that should move independently.

## 6. Cascade wiring (the gap to close)

Today the handoff from the letter to other outputs is a manual habit, unenforced. The skill graph shows `sales-letter-method` with `neighbours: []` — zero edges out. Nothing tells email or ads that a compiled letter exists to read from. The fix has two parts.

### 6a. The `letter-assets.json` export

`sales-letter-method` writes `letter-assets.json` next to the finished letter. It is a thin, stable wrapper on the audit skill's `letter-skeleton.json` — pulling out only the fields downstream outputs actually consume, so a consumer doesn't have to parse the full audit contract.

| Field | What it holds | Source in skeleton |
|---|---|---|
| `mechanism` | The named mechanism (the "how it works" the letter sells) | `ump.articulated_concept` + `ump.branded_terms` |
| `proof_library` | The proof points, ranked | `proof_inventory` |
| `objection_matrix` | Objections + the letter's answers | `concentration_alternatives` + identity-ladder rungs |
| `offer_stack` | The stacked offer + guarantee | (letter offer section) |
| `big_idea` | The single spine belief | `ump` + `identity_ladder` |
| `segment` | Which avatar this letter targets | `meta.audience_inferred` |
| `narrator_pov` | Whose voice the letter speaks in | `identity_ladder.chosen_rung` (the rung the letter speaks from) |

Location: `campaigns/<c>/sales-letters/<slug>/letter-assets.json`, sibling to the letter `.md` and its `-skeleton.json`.

**When it's written, and the failure mode.** The export is written on letter approval — the same step that locks the letter `.md`. If a consumer (email, ads, landing page) finds `letter-assets.json` missing, OR older than the letter `.md` it sits next to (the letter was edited after export), it must hard-fail to the operator: "letter-assets.json missing or stale — re-run the sales-letter-method export before reading." Do NOT silently fall back to re-reading Layer 1 — that re-derivation is the exact drift this spine exists to stop. Same rigor as seam 3 in Section 7.

### 6b. The skill-graph edges to add

Add these edges so the handoff is a discoverable contract, not a habit:

```
sales-letter-method  ->  email-sequence
sales-letter-method  ->  copywriting
sales-letter-method  ->  big-angle-spotter
sales-letter-method  ->  headline-bank
```

All four edges point letter-as-source to consumer (the consumer reads the letter's assets). The `sales-letter-method -> big-angle-spotter` edge does NOT re-couple the siblings from Section 5: it means the spotter MAY read the finished letter's assets, not that the letter waits on angles. Direction stays one-way, letter out.

Run `link-skills.py` after editing so the graph regenerates. With the edges in place, a downstream skill can find the letter's compiled assets by following the graph instead of relying on the operator to remember.

## 7. Ownership contract (one job per skill)

Each skill owns one thing. The 4 seams below are real overlaps that cause double-work and drift. They are stated here and marked **DIAGNOSIS-PENDING** — Jerel chose to diagnose first (via `routing-tester` and `skill-cleaner`) before any skill body gets trimmed. Do NOT TRIM a skill body to close a seam until the diagnosis confirms the cut.

This bars trimming, not adding. ADDING the `letter-assets.json` export to `sales-letter-method` (Section 11 step 2) is additive — it removes nothing and breaks no caller — so it is not gated by the diagnosis. Closing a seam REMOVES behaviour other skills may depend on, which is what the diagnosis exists to de-risk.

The table below restates the Section 3 layer map as exclusion rules — what each skill must NOT do. Section 3 answers "where does X live"; this one answers "what is X forbidden from touching." Same skills, different question.

| Skill | OWNS | Must NOT |
|---|---|---|
| `avatar-research` | Targeting — the buyer-profile micro-persona map + sophistication matrix | Touch anything creative |
| `big-angle-spotter` | Strategic angles + on-IMAGE overlay text + image-gen prompts | Touch the Meta headline FIELD or Meta primary-text copy |
| `headline-bank` | Meta ad-text fields only — primary text (50w + 150w) + the short Meta headline | — |
| `ad-concept-engine` | Orchestration only — batch loop, tracker + sheet, HITL gates, static-vs-video routing | Generate Meta copy inline · generate angles · author video briefs (route those to `vid-director`) |
| `sales-letter-method` | The long-form letter + the `letter-assets.json` export | — |

### The 4 seams (DIAGNOSIS-PENDING)

1. **"Headline" means two different things.** `big-angle-spotter` makes overlay text on the image; `headline-bank` makes the Meta headline field. Same word, two fields. Fix: rename to "overlay copy" (spotter) vs "Meta headline field" (headline-bank).
2. **Meta copy generated in two places.** `ad-concept-engine` generates Meta copy inline AND `headline-bank` owns it. Fix: `ad-concept-engine` drops inline generation, calls `headline-bank`.
3. **Angle ideation in two `ad-concept-engine` modes.** A legacy angle-gen path overlaps with `big-angle-spotter`. Fix: kill the legacy angle-gen; hard-fail to the operator if the spotter is unavailable rather than silently improvising angles.
4. **Video-brief generation strays out of the static lane.** `ad-concept-engine` should route video briefs to `vid-director`, not author them. Fix: route to `vid-director`.

Each fix waits on the `routing-tester` / `skill-cleaner` diagnosis. The seams are named now so the diagnosis has a target list.

## 8. Folder homes to add

The spine introduces three durable folder homes. Add them to the client tree and backfill the `_template` so a new client gets them for free.

| Folder | Holds | Owning skill |
|---|---|---|
| `_brand/avatars/` | Canonical avatar files + `_index.md` registry — the only home for avatars | `avatar-research` |
| `campaigns/<c>/angles/` | Compiled angles per campaign + `_ledger.json` | `big-angle-spotter` |
| `campaigns/<c>/sales-letters/<slug>/` | The letter `.md`, its `-skeleton.json`, and `letter-assets.json` | `sales-letter-method` |

**`_template` backfill:** `clients/_template/_brand/avatars/` is present on disk (verified) — leave it. The campaign skeleton is the snag: the NeezaNizam reorg spec locks `_TEMPLATE/` as the folder you `cp -r` to scaffold a campaign, but `clients/_template/campaigns/_TEMPLATE/` does NOT exist yet — the live skeleton is `_example-campaign/`. So this backfill runs WITH the reorg, not before it: when the reorg creates `_TEMPLATE/`, add `angles/` and `sales-letters/<slug>/` skeletons into it. Until `_TEMPLATE/` exists, add the two skeletons to `_example-campaign/` so any campaign copied today still gets all three homes. Verify the target folder before writing; don't assume it's there.

## 9. Feedback loop

Performance flows back up so the next wave learns. One ad set runs one angle, so the ad-set metric IS that angle's verdict.

**This is a structuring rule, not an assumption — enforce it.** Map exactly one angle per ad set when building the DCT batch, so attribution stays clean. If a batch puts more than one angle in a single ad set (DCT combinatorics can do this), the ad-set metric no longer reads as one angle's verdict — flag it to the operator and do NOT write a per-angle verdict to `_ledger.json` for that ad set. A muddied ad set produces no angle verdict rather than a false one.

```
ad-set metrics (one ad set = one angle)
        │
        ▼
campaigns/<c>/dcts/<id>/metrics.json   (read-only Meta pull)
        │
        ▼
campaigns/<c>/angles/_ledger.json      (per-angle verdict: winner | killed | saturated)
        │
        ▼
_brand/learnings.md
   winners   -> promoted (other campaigns read them)
   saturated -> excluded from the next wave's angle generation
```

`big-angle-spotter` reads `learnings.md` on the next wave: it builds on proven angles and avoids the saturated ones. This matches the NeezaNizam reorg's THE LOOP (SENSE to ATTRIBUTE to JUDGE to LEARN to BUILD) — the spine just names where each artifact lives across clients.

## 10. Backward-compat (sacred — do not break)

These are locked. The spine adds to them; it does not change them.

- **3-2-2 DCT is the default everywhere.** 10-5-5 is opt-in via flag and byte-identical when the flag is absent (locked decision D3).
- **`big-angle-spotter`'s soft non-hardened path stays.** Other clients depend on it. `--hardened` is additive, not a replacement.
- **Existing `.claude/workflows/` specs stay.** This spine slots alongside `creative-pipeline.md`, which still owns the ads sub-loop. Do NOT replace it.
- **NeezaNizam's LIVE 10-5-5 proof wave stays untouched.**

## 11. Build sequence

Phases run in order. The APPROVAL GATE is hard.

**What the gate protects:** live CLIENT folders (no migration, no reorg, no client-data move before Jerel approves the map) AND any TRIM to a shared skill body (Section 10 — other clients depend on `big-angle-spotter` and `sales-letter-method`). Steps 1-4 are allowed before the gate because they are spec-doc, additive skill edits, and read-only diagnosis — none remove behaviour a client relies on. Step 2 does edit a shared skill body, but only ADDS the export (per Section 7, additive is not gated); the diagnosed TRIMS in step 7 are.

1. **Write the spine doc** (this file) — spec only, nothing else touched.
2. **Add the `letter-assets.json` export** to `sales-letter-method` + the 4 skill-graph edges; run `link-skills.py`. Additive only — no behaviour removed.
3. **Backfill `_template`** with `angles/` and `sales-letters/<slug>/` skeletons.
4. **Diagnose the 4 seams** via `routing-tester` + `skill-cleaner`. Output a cut list. No skill body trimmed yet.
5. ⛔ **APPROVAL GATE — Jerel reviews the migration map.** Nothing below this line runs until he approves.
6. **Execute the NeezaNizam reorg** in full (run `_reorg-spec.md` phases) — only after the gate clears.
7. **Trim the seams** — apply the diagnosed cuts to the skill bodies, one seam at a time, verifying each.

## 12. The 10-5-5 reality check (honest note)

10-5-5 is an unproven platform bet — it's Meta-DCT framing that may not survive contact with the algorithm. Build the durable cascade for the things that compound regardless of platform: letter, email, landing page, organic content. Treat the 10-5-5 ad framing as the most disposable consumer of the foundation. If Meta changes how DCT works tomorrow, the foundation still stands and the ads re-wire around it. Don't anchor the spine to the ad format; anchor the ads to the spine.

## Related

- `creative-pipeline.md` — the 6-stage ads sub-loop this spine feeds (research to concept to brief to create to test to feedback).
- `clients/neezanizam/_reorg-spec.md` — the per-client reorg that THE LOOP and the folder homes are modeled on (temporary; delete after it ships).
- `skills/sales-letter-audit/skeleton-contract.md` — the full `letter-skeleton.json` contract that `letter-assets.json` thin-wraps.
- `.claude/skill-graph.json` — where the new `sales-letter-method` edges land after `link-skills.py`.
