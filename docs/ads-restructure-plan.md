# Ads Restructure Plan — Meta Hierarchy Mapping

**Status:** Proposed, awaiting 3 decisions from Jerel before execution.
**Scope:** File structure + naming conventions for ad campaigns across all clients. Starts with NeezaNizam, becomes template for future clients. Also updates `ad-concept-engine` skill output.

---

## Target: Meta Platform Hierarchy

```
Account
├── Campaign: [Objective]_[Test/Scale]_[Theme/Offer/Month]
│   ├── Ad Set: [AudienceType]_[Targeting]_[Hook/Angle]_[Budget if ABO]
│   │   ├── Ad: [Date]_[Angle/Hook]_[Format+Hook#]
│   │   ├── Ad
│   │   └── Ad
│   └── Ad Set
└── Campaign
```

## Current → Target Mapping

| Now | Maps to | Becomes |
|-----|---------|---------|
| `campaigns/dct-260419/` (wave folder) | Campaign | `campaigns/CBO_Test_BuyerComfort_Apr26/` |
| `DCT002` (one angle) | Ad Set | `Broad_None_CognitiveOverwhelm_50/` |
| `DCT002-A/B/C` (creative variants) | Ad | `260420_CognitiveOverwhelm_S1.json` |

## Proposed Folder Structure (per client)

```
clients/<slug>/campaigns/<metrics-campaign>/<campaign-name>/
├── campaign.json                          # objective, budget, wave#, avatars, kpi_targets, kill_rules
├── dct-tracker.json                       # rolled-up audit trail (kept)
└── <adset-name>/
    ├── adset.json                         # targeting, budget, ICP anchor, angle, avatar ref
    └── ads/
        ├── 260420_CognOverwhelm_S1.json   # headlines + copy + CTA + image ref + meta combinations
        ├── 260420_CognOverwhelm_S1.png    # or link to Canva/asset
        ├── 260420_CognOverwhelm_S2.json
        └── 260420_CognOverwhelm_S3.json
```

## Naming Conventions (Locked)

**Campaign** — `[Objective]_[Test|Scale]_[Theme]_[MonYY]`
- `CBO_Test_BuyerComfort_Apr26`
- `ASC_Scale_MothersDayPromo_Jun26`
- `CBO_Retargeting_BundleOffer_Apr26`

**Ad Set** — `[AudienceType]_[Targeting]_[Angle]_[Budget if ABO]`
- `Broad_None_FounderStory`
- `LAL_180Site_UGCReact_20` (LAL = Lookalike)
- `INT_EngagedShoppers_BenefitHook`
- `Broad_None_SocialProof_25` ($25/day ABO)

**Ad** — `[YYMMDD]_[Angle]_[Format+Hook#]`
- `260420_FounderStory_S1` — Square (1x1), Hook 1
- `260420_SocialProof_V2` — Vertical (9x16), Hook 2
- `260420_ConfidenceAngle_C1` — Carousel, Hook 1
- `260420_BundleOffer_S3` — Square, Hook 3
- `260420_ResultsProof_ST1` — Static image, Hook 1

**Format keys:**
- `S#` = Square 1x1
- `V#` = Vertical 9x16
- `P#` = Portrait 4x5 or 1080x1350
- `C#` = Carousel
- `ST#` = Static image (if distinguishing from motion)

## 3 Open Decisions (Need Jerel's Call)

1. **Date format** — `YYMMDD` (existing convention, e.g. `260420`) vs `YYYYMMDD` (user's examples, e.g. `20260420`). Recommendation: **YYMMDD** for consistency.
2. **Creative format collision** — two formats appeared in the brief:
   - `[Date]_[Angle/Hook]_[Format+Hook#]` (platform ad name — Epic Ads Lab standard)
   - `[Angle]_[Format]_[Hook#]_[CreatorInitials]` (asset filename)
   - Recommendation: **use one** — `YYMMDD_Angle_F#`, drop creator initials (solo founder = redundant).
3. **Legacy migration** — existing `dct-260408/`, `dct-260417/`, `dct-260419/` folders:
   - (a) Leave as legacy, use new structure going forward ← recommended
   - (b) Rename in-place to new format
   - (c) Symlink old → new

## Changes Required (If Approved)

### Files to update
- `skills/ad-concept-engine/SKILL.md` — replace old `[PLATFORM]_[OBJECTIVE]_[AUDIENCE]_[GEO]_[DATE]` naming spec; add nested output structure spec
- `skills/ad-concept-engine/references/dct-tracker-template.md` — rewrite tracker shape to nest `campaigns → adsets → ads`
- `scripts/ad_concept_sheet_writer.py` — update `AD` column emission to `YYMMDD_Angle_F#`; consider adding `CAMPAIGN NAME` + `ADSET NAME` columns (check sheet schema first)
- `clients/_template/campaigns/` — scaffold new folder shape as template
- `clients/neezanizam/CLAUDE.md` — update file-routing table + "common commands" section to reflect nested path

### Files NOT to touch (yet)
- Live `dct-260419/` Wave 2 work — 6 statics in DRAFT, mid-flight. Do not disturb.
- `dct-260417/` Wave 1 — shipped. Leave as legacy.

## Example: NeezaNizam Wave 2 Under New Structure

```
clients/neezanizam/campaigns/buyer-funnel/CBO_Test_BuyerComfort_Apr26/
├── campaign.json  (wave: 2, avatar: 2, budget: S$1500, CPA target: S$300)
├── dct-tracker.json
├── Broad_SG25-60_CognitiveOverwhelm_50/     ← was DCT002
│   ├── adset.json  (angle: "Cognitive Overwhelm Validation", avatar-2.md, S$50/day)
│   └── ads/
│       ├── 260420_CognOverwhelm_S1.json  (divorce sub-trigger, verbatim photo)
│       ├── 260420_CognOverwhelm_S2.json  (widow sub-trigger, text-only bold)
│       └── 260420_CognOverwhelm_S3.json  (inheritance sub-trigger, infographic)
└── Broad_SG25-60_MultiCrisis_50/            ← was DCT003
    ├── adset.json  (angle: "Multi-Crisis Coordination")
    └── ads/
        ├── 260420_MultiCrisis_S1.json  (Lisa scene photo)
        ├── 260420_MultiCrisis_S2.json  (coordinator text)
        └── 260420_MultiCrisis_S3.json  (3-tabs infographic)
```

---

**Next step:** Jerel confirms 3 decisions above → execute changes in order (template first, skill second, neezanizam CLAUDE.md third, sheet writer last after schema check).
