# Test fixture: V4 first-time-buyer letter (Neeza & Nizam)

**Source letter:** `clients/neezanizam/copy/sales-letter-v4-firsttime.md`
**Skeleton output:** `clients/neezanizam/copy/sales-letter-v4-firsttime-skeleton.json`

## Expected output (Phase 1 — structural)

| Field | Expected value | Notes |
|---|---|---|
| `meta.word_count` | 1106 (body only) | Excludes YAML header + Reviewer Note section. See `tests/conventions.md` for boundary rules. |
| `meta.verticals_detected` | `["first-time SG private buyers"]` | Single vertical — V3 leakage was cleaned up |
| `ump.branded_terms.length` | 1 | Only "No-Viewings-First Method™" |
| `ump.arrival_word_index` | ~670 | Late arrival, triggers `unique-mechanism` re-entry per routing table |
| `identity_ladder.l4.location` | `"ps"` | L4 only in PS — gap from body close |
| `cta_architecture.word_count` | >210 (~240) | Over ceiling, exact count depends on PS inclusion |
| `cta_architecture.guarantee_present` | `false` | |
| `cta_architecture.self_validation_checkpoint_present` | `false` | |
| `proof_inventory.trust_chain_gaps` | includes "Why us" entry | "Why us" relies on credentials only — no named first-timer outcome |
| `motifs` | includes "Excel sheet" (7±1), "let's sleep on it" (3±1), "five months" (6±1) | Tolerance ±1 acceptable for grep-based counts |
| `concentration_alternatives` | one entry with `dismissal_type: "feeling"` (showflat) | |

## Expected output (Phase 2 — inheritance inference)

Depends on whether `stage_outputs/03_purple_ocean.md`, `04_mass_desires.md`, `05_customer_avatar.md` exist for the neezanizam project.

- If absent: `phase_2_status = "completed"`, three inferred files written to `clients/neezanizam/reverse/`
- If present (>200 words each): `phase_2_status = "skipped_upstream_present"`, `inheritance_contracts` fields = null

## Expected routing decision

Lowest-priority hit per `skeleton-contract.md` routing table: **`unique-mechanism`** (P1 — UMP arrival_word_index >500). Secondary hits: P2 (l4=ps), P3 (trust_chain_gaps), P4 (CTA over 210).

## Pass criteria

10 of 11 structural checks must match within tolerances. Single FAIL on word_count is acceptable IF caused by spec ambiguity (lock the boundary in `tests/conventions.md` rather than re-running).

## Last validated

2026-04-28 — 10 PASS / 1 FAIL (word_count expectation was a spec error, not extractor error). Spec updated. See session learnings.

## Open spec gaps surfaced by this fixture

1. word_count boundary (header in/out) — needs lockdown in `tests/conventions.md`
2. CTA `elements_present` enum not canonicalized in CTA-architecture reference
3. `anchor_claims_per_occurrence` scoring rubric missing (±0.2 inter-rater drift)
4. `identity_ladder.l2` placement tiebreaker rule
5. `headline_phrases` cap rule (V4 has 6 candidates, contract says "2-4")
6. `numbers[]` scope (life-context numbers in or out?)
