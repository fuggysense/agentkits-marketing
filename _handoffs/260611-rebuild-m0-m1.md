# Session Handoff — Rebuild Session A (M0 + M1) complete
Date: 2026-06-11 (SGT) · Branch: rebuild-v2 · Commits: 5e867e5 (baseline), fce3dd0 (M0), 5223bf8 (M1)

## Done
- **M0**: clients tarball at `~/marketing-backups/260611-pre-rebuild-clients.tar.gz` (735MB); validator baseline (12 clients) in `docs/audit-v2-260610/baseline/`; `clients/_smoketest/` built + full pipeline BASELINE run (avatar → angles[hardened, EMULATED — script can't run headless] → copy → image prompts; 33 gates, 31 friction items, sha256 manifest, planted defect PD-IMG-01). _smoketest now git-tracked.
- **M1** (6/6 independently verified CONFIRMED + 2 inline):
  - `scripts/claim_gate.py` — source-or-cut. Catches Eugene $214,300 (img-03+img-04) and smoke "73%" planted defect; passes sourced claims (Eugene 2.5% CPF). Reads claims ledger → offer.md whitelist → auto-trace (client research + `~/AI workflows/research-vault`). Wired into ad-concept-engine gate sequence + render.py precondition (fail-closed, `--skip-claim-gate` logged override).
  - avatar-research: quotes need source pointers, refuses otherwise. neezanizam unsourced-quote decision note: `_handoffs/neezanizam-quote-flag-260611.md` (second unsourced quote found at avatar-1.md ~line 295, logged).
  - render.py reads current `image_pool` shape (10/10 Eugene prompts byte-identical dry-run); legacy behind flag; `--confirm-all` guard.
  - tr_10_5_5_sheet_writer config-driven; dual-path metrics-config lookup back-ported to 2 sibling scripts. DRY-RUN verified only.
  - provisioner `--into` append-only now (was deleting all pre-existing tabs); collision guard + `--dry-run`.
  - big-angle-spotter: hardened = default (`--fast` opt-out), citation audit BLOCKING in hardened. Lives at `~/AI workflows/big-angle-spotter` (outside repo) — `run_pipeline.py.bak-260611` created there.
  - Handoff mirror (`_handoffs/mirror/`, 5 files) + operator-action sheet (`_handoffs/operator-actions-260611.md`).
- Full per-task reports: `docs/audit-v2-260610/m1/`.

## Pending operator
1. **M1.7 Eugene diffs** — `_handoffs/eugene-m17-preview-260611.md` ("apply eugene diffs 1-4" or subset).
2. Operator-action sheet items (credentials key, DCT008, roster triage, school/shame angles, neezanizam quote decision).
3. Claim-gate policy nuance from the builder: should percentages be ledger-only (never auto-traced)? Current behavior: a percentage with real research support auto-passes. One-line change if you want stricter.
4. Eugene's dct.json launch_gates note still says render.py can't read dct.json — now stale, but the file is protected; clear it with the G1/G4 blocker note when convenient.

## Next: Session B = M2 (the merge)
research-completeness brief (+ your "good enough research" working session) → hook system + script-skill fold-in → Meta-copy gate → image-prompt rebuild (5 formats + 11-pattern library, old brief archived switchable) → VOC injection → diversity spec → feedback repair + media doctrine → synthesis sections → video hook-swap lane → swipe curation. Then M2 smoke-test rerun vs BASELINE before the milestone counts.
