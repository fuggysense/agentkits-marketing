# Letter Skeleton Contract

The `letter-skeleton.json` is the data structure produced by the `sales-letter-audit` skill and consumed by the operator (or a downstream regen skill) to decide which forward-pipeline stage to re-enter.

This is a **contract** — both producer and consumers must conform. Any field added or renamed requires updating both sides + all consumer skills.

## Status: v0.4 (draft) — locked enough to build against, expect breaking changes through V4 validation pass.

## Execution model: split-phase

The skill runs in two distinct phases:

- **Phase 1 — Structural Extraction (ALWAYS runs).** Populates `meta`, `ump`, `identity_ladder`, `motifs`, `headline_body_coherence`, `concentration_alternatives`, `cta_architecture`, `proof_inventory`. Cheap structural pass. Catches drift between upstream research and the finished letter — useful even when upstream artifacts already exist.

- **Phase 2 — Inheritance Inference (CONDITIONAL).** Populates `inheritance_contracts.*_inferred`. Only runs when upstream stage artifacts (`stage_outputs/03_purple_ocean.md`, `04_mass_desires.md`, `05_customer_avatar.md`) are absent or stale. When skipped, `inheritance_contracts` fields are set to `null` and `extraction_metadata.phase_2_status = "skipped_upstream_present"`.

This split means: clients with existing research get drift detection for free without redundant guesswork; greenfield "improve this letter" cases get full inference.

## File location

`clients/<project>/copy/<letter-name>-skeleton.json`

## Companion artifacts

- Source letter: `clients/<project>/copy/<letter-name>.md`
- Inferred research (sandbox, requires approval): `clients/<project>/reverse/{purple-ocean,mass-desires,customer-avatar}-inferred.md`
- Audit (separate concern, produced by a structural reviewer such as `Marketing/skills/sales-letter-method/reviewers/pre-ship-checklist-reviewer.md`): `clients/<project>/copy/<letter-name>-audit.md`

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "LetterSkeleton",
  "type": "object",
  "required": ["meta", "ump", "identity_ladder", "motifs", "headline_body_coherence", "concentration_alternatives", "cta_architecture", "proof_inventory", "inheritance_contracts", "extraction_metadata"],
  "properties": {
    "meta": {
      "type": "object",
      "required": ["source_path", "word_count", "audience_inferred", "verticals_detected"],
      "properties": {
        "source_path": { "type": "string", "description": "Absolute path to source letter" },
        "word_count": { "type": "integer" },
        "audience_inferred": { "type": "string", "description": "Best guess at target segment from letter content" },
        "verticals_detected": {
          "type": "array",
          "items": { "type": "string" },
          "description": "All audience verticals the letter touches. If >1, may indicate segment leakage (e.g., a 'first-timer' headline that contains upgrader signals)."
        }
      }
    },
    "ump": {
      "type": "object",
      "required": ["articulated_concept", "branded_terms", "arrival_word_index", "prior_solution_link"],
      "properties": {
        "articulated_concept": { "type": "string" },
        "branded_terms": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "occurrence_count": { "type": "integer" },
              "first_appearance_word_index": { "type": "integer" }
            }
          },
          "description": "Inventory of trademarked / capitalized mechanism names. >1 entry suggests proliferation risk."
        },
        "arrival_word_index": { "type": "integer", "description": "Word position where mechanism is first articulated. >500 = late arrival, flag for UMP visibility regen." },
        "prior_solution_link": { "enum": ["structural", "implicit", "absent"], "description": "How explicitly the UMP contrasts against existing alternatives." },
        "magic_name_check": {
          "type": "object",
          "description": "v0.4. MAGIC framework score against the primary branded mechanism name. Score <=2 surfaces as [M] finding and routes to sales-letter-method Phase 0.7 (mechanism architecture).",
          "properties": {
            "name_under_test": { "type": "string" },
            "m": { "type": "boolean", "description": "Magnetic reason — does the name imply WHY this exists / WHY now?" },
            "a": { "type": "boolean", "description": "Avatar — does the name call out the specific buyer segment?" },
            "g": { "type": "boolean", "description": "Goal — does the name state the dream outcome?" },
            "i": { "type": "boolean", "description": "Interval — does the name include a timeline?" },
            "c": { "type": "boolean", "description": "Container — does the name use a unique container word (Blueprint / Protocol / System / Method / Stack)?" },
            "score": { "type": "integer", "minimum": 0, "maximum": 5 },
            "missing": { "type": "array", "items": { "enum": ["m", "a", "g", "i", "c"] } }
          }
        },
        "discredit_old_solutions": {
          "type": "array",
          "description": "v0.4. Each named alternative the letter dismisses at the UMP/positioning level. Distinct from concentration_alternatives (Step 7), which catches dismissals at prose level. Empty array OR all entries 'category-only' surfaces as [H] finding (no discredit work). Entries with type 'named-no-structural-failure' surface as [M] (named but unexplained).",
          "items": {
            "type": "object",
            "required": ["alternative_name", "dismissal_quote", "dismissal_word_index", "dismissal_type"],
            "properties": {
              "alternative_name": { "type": "string" },
              "dismissal_quote": { "type": "string" },
              "dismissal_word_index": { "type": "integer" },
              "dismissal_type": { "enum": ["named-with-structural-failure", "named-no-structural-failure", "category-only", "absent"] },
              "structural_failure_mode": { "type": ["string", "null"] }
            }
          }
        }
      }
    },
    "identity_ladder": {
      "type": "object",
      "required": ["l1", "l2", "l3", "l4"],
      "description": "Schwartz-style awareness layers. Each entry: where this layer lands in the structure.",
      "properties": {
        "l1": { "$ref": "#/definitions/identity_layer" },
        "l2": { "$ref": "#/definitions/identity_layer" },
        "l3": { "$ref": "#/definitions/identity_layer" },
        "l4": { "$ref": "#/definitions/identity_layer" }
      }
    },
    "motifs": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["phrase", "count", "anchor_claims_per_occurrence"],
        "properties": {
          "phrase": { "type": "string" },
          "count": { "type": "integer" },
          "anchor_claims_per_occurrence": { "type": "number", "description": "0.0–1.0 — what fraction of occurrences carry proof weight vs decorative repetition. <0.5 = motif not earning its repetition." }
        }
      }
    },
    "headline_body_coherence": {
      "type": "object",
      "properties": {
        "headline_phrases": { "type": "array", "items": { "type": "string" } },
        "echo_count_per_phrase": { "type": "object", "additionalProperties": { "type": "integer" } }
      }
    },
    "concentration_alternatives": {
      "type": "array",
      "description": "Each alternative being dismissed (e.g., showflat visit, agent-led tour). Type matters: 'feeling' is weak, 'structural-failure-mode' is strong.",
      "items": {
        "type": "object",
        "properties": {
          "alternative": { "type": "string" },
          "dismissal_type": { "enum": ["feeling", "structural-failure-mode"] },
          "quote": { "type": "string" }
        }
      }
    },
    "cta_architecture": {
      "type": "object",
      "required": ["elements_present", "word_count", "guarantee_present", "self_validation_checkpoint_present"],
      "properties": {
        "elements_present": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Subset of the 11-element CTA checklist (canonical reference: Marketing/skills/sales-letter-method/references/objection-architecture.md → CTA Architecture)."
        },
        "word_count": { "type": "integer", "description": ">210 = over ceiling, flag for tightening." },
        "guarantee_present": { "type": "boolean" },
        "self_validation_checkpoint_present": { "type": "boolean" }
      }
    },
    "proof_inventory": {
      "type": "object",
      "required": ["named_outcomes", "numbers", "trust_chain_gaps", "ai_pattern_flags"],
      "properties": {
        "named_outcomes": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "person": { "type": "string", "description": "Named individual or [PLACEHOLDER]" },
              "outcome": { "type": "string" },
              "is_placeholder": { "type": "boolean" }
            }
          }
        },
        "numbers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "value": { "type": "string" },
              "claim_backed": { "type": "string" },
              "is_placeholder": { "type": "boolean" }
            }
          }
        },
        "trust_chain_gaps": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Sections where credibility breaks (e.g., 'Why us' relied on credentials, no named first-timer outcome). This is the lens-blind track — must extract even when structural audit passes."
        },
        "ai_pattern_flags": {
          "type": "array",
          "description": "Anti-AI pattern matches found in the source letter. Surfaced in the plain-English brief's 'Patterns to flag' section.",
          "items": {
            "type": "object",
            "required": ["pattern", "source_file", "quote", "word_index", "severity"],
            "properties": {
              "pattern": { "type": "string", "description": "Pattern name from the checklist (e.g. 'Big Contrast', 'Negative parallelism', 'Revelation Hook')" },
              "source_file": { "enum": ["overused-ai-patterns.md", "anti-ai-patterns.md"] },
              "quote": { "type": "string", "description": "Verbatim text from the source letter" },
              "word_index": { "type": "integer" },
              "severity": { "enum": ["soft-flag", "hard-flag"] }
            }
          }
        },
        "voc_anchored_findings": {
          "type": "array",
          "description": "v0.4. Step 9c output. For every brief-bound finding, the dossier match (or no-match) that anchors it to verbatim buyer language. Loaded path only — empty array on cold path. Findings with match_strength 'no-match' must be tagged [no-VOC] in the brief.",
          "items": {
            "type": "object",
            "required": ["finding_id", "letter_quote", "letter_word_index", "match_strength"],
            "properties": {
              "finding_id": { "type": "string", "description": "Stable id, e.g. 'trust_chain_gap_2', 'ump_arrival_late', 'cta_missing_guarantee'" },
              "letter_quote": { "type": "string" },
              "letter_word_index": { "type": "integer" },
              "buyer_quote": { "type": ["string", "null"], "description": "Verbatim quote from buyer-profile.md or avatars/*.md. Null when match_strength is 'no-match'." },
              "buyer_source": { "type": ["string", "null"], "description": "Source attribution, e.g. 'u/Kind-Onion-6015, r/singaporefi' or 'avatar-03 / verbatim quotes'. Null when match_strength is 'no-match'." },
              "match_strength": { "enum": ["direct", "adjacent", "no-match"] }
            }
          }
        }
      }
    },
    "inheritance_contracts": {
      "type": "object",
      "description": "Back-inferred upstream research. Writes to clients/<project>/reverse/ sandbox, NEVER directly to stage artifacts.",
      "required": ["purple_ocean_inferred", "mass_desires_inferred", "customer_avatar_inferred", "source_confidence"],
      "properties": {
        "purple_ocean_inferred": { "type": "string" },
        "mass_desires_inferred": { "type": "array", "items": { "type": "string" } },
        "customer_avatar_inferred": { "type": "string" },
        "source_confidence": {
          "type": "object",
          "additionalProperties": { "enum": ["high", "partial", "speculation"] },
          "description": "Per-field confidence. If >30% of fields are 'speculation', consumer MUST halt for human review before regen."
        }
      }
    },
    "extraction_metadata": {
      "type": "object",
      "required": ["extracted_at", "extractor_version", "speculation_ratio", "declared_anchors", "context_branch"],
      "properties": {
        "extracted_at": { "type": "string", "format": "date-time" },
        "extractor_version": { "type": "string" },
        "speculation_ratio": { "type": "number", "description": "Computed from inheritance_contracts.source_confidence. 0.0–1.0. >0.30 triggers human gate." },
        "declared_anchors": {
          "type": "object",
          "required": ["purpose_of_letter", "cta_target", "final_goal"],
          "description": "The three pre-audit goals declared by the operator/caller before any audit work runs. Hard-required input — if any of the three is null or missing, the skill must halt and ask before proceeding.",
          "properties": {
            "purpose_of_letter": { "type": "string", "description": "One sentence on what the letter is trying to make happen." },
            "cta_target": { "type": "string", "description": "One sentence on what the CTA button needs to achieve." },
            "final_goal": { "type": "string", "description": "One sentence on the actual outcome being chased." }
          }
        },
        "context_branch": {
          "enum": ["loaded", "cold"],
          "description": "Records which audit path was selected during pre-audit context detection. 'loaded' = clients/<project>/ exists with populated context files; light path runs (Schwartz awareness/sophistication off the letter, grounded in loaded context). 'cold' = no client folder or sparse; cold-audit heavy path runs (full Purple Ocean / Mass Desires / Customer Avatar inference from letter alone)."
        },
        "voc_anchor_coverage": {
          "type": "object",
          "description": "v0.4. Aggregate of Step 9c VOC anchor pass. Used to detect dossier incompleteness and flag for buyer-language-researcher refresh.",
          "properties": {
            "total_findings": { "type": "integer" },
            "direct_match_count": { "type": "integer" },
            "adjacent_match_count": { "type": "integer" },
            "no_match_count": { "type": "integer" },
            "no_match_ratio": { "type": "number", "description": "no_match_count / total_findings. >0.5 flags dossier incompleteness." }
          }
        },
        "client_facing_brief": {
          "type": "object",
          "description": "Tracks whether the optional client-facing lead-magnet brief was produced (Gate A in the procedure). Omit if Gate A was not reached.",
          "required": ["produced", "path", "register"],
          "properties": {
            "produced": { "type": "boolean", "description": "True if Gate A passed and the brief was generated." },
            "path": { "type": ["string", "null"], "description": "Relative path to the brief file, or null if not produced." },
            "register": { "type": "string", "const": "client-facing", "description": "Constant — always 'client-facing' for this artifact." }
          }
        }
      }
    }
  },
  "definitions": {
    "identity_layer": {
      "type": "object",
      "properties": {
        "quote": { "type": "string" },
        "word_index": { "type": "integer" },
        "location": { "enum": ["headline", "lede", "body", "close", "ps", "absent"] }
      }
    }
  }
}
```

## Re-entry routing (consumer contract)

The operator (or a downstream regen skill) reads the skeleton and routes to the lowest-numbered matching rule:

| Priority | Skeleton signal | Re-enter at | Rationale |
|----------|-----------------|-------------|-----------|
| 0 (HARD STOP) | `meta.verticals_detected.length > 1` AND any vertical ≠ declared segment | **HALT — segment audit** | Segment leakage; cannot regen until segment confirmed |
| 0 (HARD STOP) | `extraction_metadata.speculation_ratio > 0.30` | **HALT — human review of `reverse/` sandbox** | Inferred research too uncertain to route from |
| 0 (SOFT FLAG, v0.4) | `extraction_metadata.voc_anchor_coverage.no_match_ratio > 0.5` (loaded path only) | **Recommend buyer-language-researcher refresh before re-audit** | Dossier likely incomplete; majority of findings unanchored |
| 1 | `ump.branded_terms.length > 1` OR `ump.arrival_word_index > 500` | UMP regen (`sales-letter-method` Phase 0.5 + Phase 1 Mechanism re-derivation) | Mechanism naming or visibility broken |
| 1 (v0.4) | `ump.magic_name_check.score <= 2` | `sales-letter-method` Phase 0.7 (mechanism architecture, Track B) | Branded mechanism name is generic / not MAGIC-wrapped |
| 1 (v0.4) | `ump.discredit_old_solutions.length == 0` OR all entries `dismissal_type == "category-only"` | `sales-letter-method` Phase 0.7 (mechanism architecture, Track B) | No discredit work — letter sits in a vacuum vs named alternatives |
| 1 (v0.4) | Any `ump.discredit_old_solutions[*].dismissal_type == "named-no-structural-failure"` | `sales-letter-method` Phase 0.7 (mechanism architecture, Track B) | Named dismissals lack structural failure modes |
| 2 | `identity_ladder.l4.location IN ["ps", "absent"]` | Avatar / desire layer re-derivation | Layer 4 missing from body close |
| 3 | `proof_inventory.trust_chain_gaps.length > 0` | Voice mining → proof inventory | Need new proof material before regen |
| 4 | `cta_architecture.elements_present.length < 9` OR `cta_architecture.word_count > 210` | CTA rewrite (see `Marketing/skills/sales-letter-method/references/objection-architecture.md` → CTA Architecture) | CTA below quality bar |
| 5 | Any `motifs[*].anchor_claims_per_occurrence < 0.5` | Coherence audit / motif scrub | Motifs not earning repetition |
| 6 | `concentration_alternatives[*].dismissal_type == "feeling"` | targeted body rewrite | Soft dismissals weakening concentration |
| ∞ | None of the above match | **No regen needed — letter is structurally clean** | |

## V4 expected output (validation case)

When `sales-letter-audit` runs against `sales-letter-v4-firsttime.md`, the skeleton MUST contain:

- `ump.branded_terms.length == 1` (only "No-Viewings-First Method™")
- `identity_ladder.l4.location == "ps"`
- `cta_architecture.word_count > 210` (243)
- `cta_architecture.guarantee_present == false`
- `cta_architecture.self_validation_checkpoint_present == false`
- `proof_inventory.trust_chain_gaps` includes "Why us" section
- `motifs` includes "Excel sheet" (~8), "let's sleep on it" (~4), "five months" (~7)
- One `concentration_alternatives` entry with `dismissal_type: "feeling"` (showflat)

If the skill ships and these don't appear, the extractor is under-specified — iterate.

## Versioning

- v0.1 — initial draft, pre-skill-implementation
- v0.2 — added phase split (structural extraction + inheritance inference), re-entry routing table, V4 validation case
- v0.3 — Added `declared_anchors`, `context_branch`, `client_facing_brief` fields to extraction_metadata. Anchors are hard-required pre-audit gate. Branch records light-vs-cold path selection. Brief tracks optional Gate A artifact.
- v0.4 — VOC-anchored upgrade. Added `ump.magic_name_check` (5-boolean MAGIC scoring), `ump.discredit_old_solutions[]` (named-vs-category dismissal tracking), `proof_inventory.voc_anchored_findings[]` (Step 9c output), and `extraction_metadata.voc_anchor_coverage` (dossier completeness signal). Loaded path now mandates buyer-profile.md + avatars/*.md read before scoring. Routing table extended with three Phase 0.7 entries (MAGIC ≤2, empty/category-only discredit, named-no-structural-failure dismissals) and a soft-flag for >50% no-match findings. All v0.3 fields preserved (additive change, backwards-compatible).
- v1.0 — after V4 validation pass
- Breaking changes require: bumping `extractor_version`, updating all consumer skills, re-running existing skeletons.
