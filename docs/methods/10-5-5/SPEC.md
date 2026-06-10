# 10-5-5 DCT Method — Spec & Migration Contract

**Status:** Building (Phase 1 of 6) · **Owner:** Jerel · **Created:** 2026-06-03
**Supersedes for opt-in clients:** the 3-2-2 DCT method (3 creatives × 2 copies × 2 headlines = 12 combos)
**Source:** Ethan (Fuggy's Media) call, 2026-06-02 — transcript in `clients/neezanizam/meetings/` and this repo's session log.

> This file is the single source of truth for the 10-5-5 migration. An orchestrator landing here cold can read this top-to-bottom and know: what 10-5-5 is, what was decided and why, where every moving part lives, what's built vs pending, and what's still unresolved.

---

## 1. What 10-5-5 is (and why)

Meta retired the standalone **Dynamic Creative Testing (DCT) toggle** — which capped a test at **3 images / 2 primary texts / 2 headlines** — and replaced it with the **Flexible ("Flex") ad format**, which raises the ceiling to **10 media / 5 primary texts / 5 headlines**.

"10-5-5" is simply **Meta Flex's maximum**: 10 creatives, 5 copies, 5 headlines per test. The *method* (research persona → mine buyer language → draft angles → over-draft headlines → narrow → pair with visuals) is unchanged from 3-2-2. Only the multipliers moved.

**Why migrate:** more (quality) assets per test = Meta has more to optimize against = ~4× faster creative testing (30 creatives / 6 days vs 9). Ethan's framing: "the game is just finding what works as quickly as possible."

**Honest caveat (recorded, not hidden):** Ethan started using 10-5-5 "literally yesterday," says "not a lot of people might be using it," and expects the platform to shift again "in four or five months." We are fitting a pipeline to a *platform ceiling*, on a method with **zero proven results yet for our clients**. The proof wave (Phase 4) exists to validate the shape before we trust it. Verify Meta's live Flex limits against the actual ad account before the first real upload — if Meta caps differ, the column counts here change.

---

## 2. Locked decisions (operator calls, 2026-06-03)

| # | Decision | Choice | Consequence |
|---|----------|--------|-------------|
| D1 | What "10 creatives" means | **5 angles × 2 variations** | Every number derives from 5 angles: 10 images (5×2), 5 copies (1/angle), 5 headlines (1/angle). Clean angle-level attribution. |
| D2 | Sequencing | **Full automation now** | Build engines + writer + tracker + sheet in one pass (not manual-proof-first). Risk accepted by operator; flagged. |
| D3 | Engine blast radius | **Parametrize, keep defaults** | 10-5-5 is an **opt-in mode**. 3-2-2 stays the default everywhere. No existing client (takekine, stackworks, etc.) changes behavior unless it opts in. |
| D4 | First build target | **Fresh tabs on NeezaNizam + Eugene-ready** | Proof wave writes to NEW sheet tabs, never the live CREATIVES/COPY tabs or the meta_puller. Pipeline built client-agnostic so Eugene inherits it on onboarding. |

**Design principle (from D3):** every engine gets a 10-5-5 *mode*, selected by a flag/param. Absent the flag, behavior is byte-identical to today. This is the backward-compatibility contract — do not change any default.

**Eugene scope:** "for Eugene" = make the pipeline Eugene-ready. Do NOT fabricate Eugene's campaign (no business profile, avatars, offer, or sales letter exist in-repo yet). When Eugene is onboarded, he opts into 10-5-5 like any client.

---

## 3. The data model (5 angles × 2 variations)

### Unit definitions
- **DCT-wave** = one Meta Flex ad set = **5 angles**.
- **Angle** = 1 locked copy + 1 locked headline + 2 image/creative variations.
- **Per-wave totals:** 10 creatives (5×2) · 5 copies (5×1) · 5 headlines (5×1) = Meta Flex max.
- **Headline drafting:** ~5 headlines drafted *per angle* (big-angle-spotter already over-produces 10 → narrow to 1 locked + keep drafts for audit).

### Tracker schema (`dct_structure` block, 10-5-5 mode)
```json
{
  "method": "10-5-5",
  "angle_model": "five_x_two",
  "angles": 5,
  "variations_per_angle": 2,
  "copies_per_angle": 1,
  "headlines_per_angle": 1,
  "headlines_drafted_per_angle": 5,
  "total_creatives": 10,
  "total_copies": 5,
  "total_headlines": 5,
  "meta_format": "flex"
}
```
`angles[]` (5 entries), each:
```json
{
  "angle_id": "A01",
  "angle": "<one-line angle>",
  "persona": "avatar-1 (The Hesitant Calculator)",
  "market_awareness": "...",
  "market_sophistication": "...",
  "locked_copy": "<the 1 shipped copy>",
  "locked_headline": "<the 1 shipped headline>",
  "headline_drafts": ["...", "...", "...", "...", "..."],
  "variations": [
    {"variant_id": "v1", "visual_style": "...", "image_prompt": "...", "canva_link": "..."},
    {"variant_id": "v2", "visual_style": "...", "image_prompt": "...", "canva_link": "..."}
  ]
}
```

### Sheet row model — **one row per angle (5 rows per wave)**
This is the key simplification D1 buys us: because copy + headline are now **angle-scoped (1 each)**, we do NOT widen the COPY tab to 5+5 columns crammed on one row. We add **rows**. This maps onto the *existing* "one row per creative" layout (old dct-260417/419 schema), which the writer already supports — not the wide-column rebuild first feared.

- **CREATIVES tab:** 5 rows/wave. Columns unchanged (BATCH/STATUS/FORMAT/AD/AWARENESS/SOPH/ANGLE/PERSONA/CANVA LINK + blank metric cols). `AD` carries the angle id (e.g. `DCT010-A01`). The 2 image variants live in the tracker (feed image-gen); the sheet row is angle-level.
- **COPY tab:** 5 rows/wave, one per angle, each = that angle's 1 copy + 1 headline. Existing `COPY 1` + `HEADLINE 1` columns suffice; `COPY 2`/`HEADLINE 2` become optional (unused in 10-5-5, kept for 3-2-2 back-compat).

### ⚠️ Known-open: Meta Flex performance attribution
Under Flex, you upload 10 images + 5 texts + 5 headlines into **one ad**; Meta mixes combinations internally. There are **not** 5 separate Meta "ads" per wave. So:
- Our **5 angle-rows are authoring/tracking rows** (which we wrote, why).
- Meta returns performance at the **Flex-ad / ad-set level + asset breakdown**, not 5 clean per-angle rows.
- The `meta_puller` currently maps ad-name `DCT\d+` → one sheet row. Under Flex it gets one perf row per Flex ad, with angle/asset performance available only via Meta's asset-level breakdown.
- **Decision deferred to after the proof wave** (we need to see real Flex reporting first). Until then: angle-level performance is read in Meta UI, not auto-pulled into the sheet. Tracked as Open Item O1.

---

## 4. Scope & Definition of Done

**In scope:** opt-in 10-5-5 mode in the three generator skills + global angle pipeline; generalized sheet writer; 10-5-5 tracker schema; one validated NeezaNizam proof wave on new test tabs; orchestrator navigation index + this spec.

**Out of scope (this build):** Eugene onboarding/content; meta_puller Flex-reporting rework (O1); migrating other V4 clients off 3-2-2; touching live NeezaNizam CREATIVES/COPY tabs or live campaigns.

**DoD:**
1. Each engine runs 3-2-2 unchanged (default) AND 10-5-5 (flag) — verified.
2. `ad_concept_sheet_writer.py` emits 5 angle-rows from a 10-5-5 tracker in a dry-run, and still emits 3-2-2 correctly — verified.
3. One NeezaNizam proof wave (5 angles × 2, existing avatar) authored end-to-end into a 10-5-5 tracker.
4. Proof wave written to NEW sheet test tabs (after live-write gate), live tabs untouched.
5. `_campaigns-index.json` + CONTEXT.md pointers let a cold orchestrator find it.

---

## 5. Where everything lives (navigation map for orchestrator)

| Concern | Path |
|---------|------|
| This spec / contract | `docs/methods/10-5-5/SPEC.md` |
| Migration phase status | §7 below + `docs/methods/10-5-5/migration-log.md` |
| ad-concept-engine (3×2×2 hardcoded → +10-5-5 mode) | `skills/ad-concept-engine/SKILL.md` |
| headline-bank (2/2 hardcoded → +5/5 mode) | `skills/headline-bank/SKILL.md` |
| big-angle-spotter skill | `skills/big-angle-spotter/SKILL.md` |
| big-angle-spotter pipeline (GLOBAL, shared) | `~/AI workflows/big-angle-spotter/scripts/run_pipeline.py` |
| Sheet writer | `scripts/ad_concept_sheet_writer.py` |
| 10-5-5 tracker schema | `skills/ad-concept-engine/references/dct-tracker-10-5-5.schema.json` |
| NeezaNizam proof wave | `clients/neezanizam/campaigns/dct-10-5-5-proof-260603/` |
| NeezaNizam sheet config | `clients/neezanizam/_brand/metrics-config.json` |
| NeezaNizam campaign index (new) | `clients/neezanizam/campaigns/_campaigns-index.json` |
| Google Sheet | `14bh8k6S-krbg0I69JgO2e7eP-YkS6_NMC7XN2NTNKSE` (CREATIVES gid 1164222857, COPY gid 1695031878) — **new test tabs to be added** |

---

## 6. Open items

- **O1 — Meta Flex performance attribution / meta_puller.** How angle-level performance flows from Meta's asset breakdown into the sheet. Deferred until the proof wave shows real Flex reporting. (§3)
- **O2 — asset-progression sheet routing bug** (pre-existing, flagged 260529): `dct-260419` `sheet_write_plan` targets the buyer-funnel workbook (`14bh8k6S`) while `metrics-config.json` asset-progression points at `1D-HrqZH`. Out of this build's critical path (we use new test tabs) but resolve before any 10-5-5 *seller* wave.
- **O3 — DCT-ID collision** (`DCT002/003` reused across waves/avatars) worsens at 10-5-5 volume. Operator deferred the `W1-DCT002` prefix fix; revisit if it bites.
- **O4 — Meta live-limit verification.** Confirm 10/5/5 against the actual ad account before first upload.

---

## 7. Phase status

- [ ] **Phase 1 — Spec + data model** (this file) — *in progress*
- [ ] **Phase 2 — Parametrize engines** (ad-concept-engine, headline-bank, big-angle-spotter skill + GLOBAL pipeline [gated diff])
- [ ] **Phase 3 — Tracker schema + writer generalization** (dry-run verified)
- [ ] **Phase 4 — NeezaNizam proof wave** (5 angles × 2, existing avatar)
- [ ] **Phase 5 — Sheets** (new test tabs, LIVE — gated)
- [ ] **Phase 6 — Nav + recording** (`_campaigns-index.json`, CONTEXT pointers, decision log)

Detailed per-phase changes + verification results: `docs/methods/10-5-5/migration-log.md`.
