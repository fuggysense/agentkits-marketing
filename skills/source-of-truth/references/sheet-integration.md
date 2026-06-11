# Sheet Integration — Write Strategy to Google Sheets

Maps source-of-truth outputs to the client's Google Sheet (defined in `clients/<project>/metrics-config.json`). Uses existing `scripts/modal/sheets_writer.py` infrastructure — no new auth, no new service account.

**Scope (corrected 260417):** this skill writes the **AVATARS tab ONLY**.

- AVATARS tab → owned by this skill via `scripts/source_of_truth_sheet_writer.py`
- CREATIVES tab (strategy columns) → **owned by ad-concept-engine** via `scripts/ad_concept_sheet_writer.py` (not yet built — dependency gap)
- COPY tab → **owned by ad-concept-engine** via same writer (not yet built)
- Metric columns on CREATIVES (CTR/CVR/CPA/CALLS/SPEND/DURATION) → owned by `sheets-updater` via `scripts/modal/sheets_writer.py` (already exists)

**Separation rule:** source-of-truth owns STRATEGY (angles, hooks, messaging, avatars). ad-concept-engine owns EXECUTION (DCT tracker, creative specs, copy, headlines). They do not overlap. Violation of this rule in a prior run shipped DCT data into source-of-truth outputs — see `corrections.md` (260417 entry).

---

## Gate — Only Run If Config Exists

Before any sheet write, verify:

```python
config_path = f"clients/{project_slug}/metrics-config.json"
if not exists(config_path):
    log("No metrics-config.json — skipping sheet integration")
    return

config = load(config_path)
required_tabs = ["avatars", "creatives", "copy"]
missing = [t for t in required_tabs if t not in config["tabs"]]
if missing:
    log(f"Sheet missing tabs: {missing} — skipping or partial write")
```

If `metrics-config.json` doesn't exist, the skill surfaces:
> "No sheet wired for this project. Run `/sheets:provision` first to create the dashboard. For now, outputs written to markdown files only."

---

## Tab 1 — AVATARS (`format: narrative_sections`)

**Gid lookup:** `config["tabs"]["avatars"]["gid"]` (example value: `1060043551` — actual gid per client in their `metrics-config.json`)
**Write mode:** manual (per config)
**Format:** narrative blocks per avatar (no column structure — writes into cells as text)

### Write pattern

For each avatar in `clients/<project>/avatars/avatar-*.md`:

1. Convert the 12-point breakdown markdown to a SINGLE long-form cell value (Sheets supports newlines in cells via `\n`)
2. Write each avatar as a row in column A (label) and column B (full narrative)

```python
from scripts.modal.sheets_writer import SheetsWriter

writer = SheetsWriter(service_account_path="scripts/modal/credentials.json")
sheet = writer.get_sheet(config["sheet_id"])
avatars_tab = writer.get_tab(sheet, config["tabs"]["avatars"]["gid"])

# Clear existing avatar content (narrative format = wipe + rewrite)
avatars_tab.clear()

# Write header row
avatars_tab.append_row(["AVATAR", "NARRATIVE", "LAST UPDATED"], value_input_option="USER_ENTERED")

# Write one row per avatar
for avatar_file in sorted(avatars_dir.glob("avatar-*.md")):
    avatar_name = parse_avatar_name(avatar_file)  # "Avatar 1: The Hesitant Calculator"
    narrative = avatar_file.read_text()  # full markdown as a cell
    avatars_tab.append_row(
        [avatar_name, narrative, today_date_sgt()],
        value_input_option="USER_ENTERED"
    )
```

**Neezanizam example:** 3 rows written (Hesitant Calculator, Burned Sceptic, Faith-First Family)

---

## Tab 2 — CREATIVES — NOT THIS SKILL'S RESPONSIBILITY

**Owned by:** ad-concept-engine
**Writer script (not yet built):** `scripts/ad_concept_sheet_writer.py`
**Input file:** `clients/<project>/campaigns/dct-YYMMDD/dct-tracker.json` (ad-concept-engine output)

This section is retained as a reference for the ad-concept-engine skill to implement. The source-of-truth skill must NOT write to this tab. If you find yourself about to, stop and re-read `corrections.md` entry 260417.

**Gid lookup:** `config["tabs"]["creatives"]["gid"]` (example value: `1164222857` — actual gid per client in their `metrics-config.json`)
**Write mode:** append rows for new DCT batches, update_metric_columns for existing (but metric updates are `sheets-updater`'s job)
**Columns:** `BATCH, STATUS, FORMAT, AD, MARKET AWARENESS, MARKET SOPHISTICATION, ANGLE, PERSONA, CTR, CVR, CPA, CALLS, SPEND, DURATION`
**Protected columns (WE WRITE THESE):** `BATCH, FORMAT, AD, MARKET AWARENESS, MARKET SOPHISTICATION, ANGLE, PERSONA`
**Metric columns (WE NEVER WRITE):** `STATUS, CTR, CVR, CPA, CALLS, SPEND, DURATION`

### Row construction from source-of-truth

Each DCT ad variant = 1 row. For a 3-angle × 3-creative × 2-headline × 2-copy DCT batch = 3 × 3 × 2 × 2 = 36 Meta combinations, but in the sheet we track the CREATIVE level, not every combination. Typically:

- 3 angles (from §10 priority) × 3 creatives per angle = 9 rows per DCT batch
- Each row has a unique BATCH ID (e.g. `DCT001`, `DCT002`, …, `DCT009`)

### Write pattern

```python
creatives_tab = writer.get_tab(sheet, config["tabs"]["creatives"]["gid"])
protected_cols = config["tabs"]["creatives"]["protected_columns"]
full_cols = config["tabs"]["creatives"]["columns"]

# Check existing batch IDs to avoid duplicates
existing_batches = get_column_values(creatives_tab, "BATCH")
next_batch_num = max_batch_num(existing_batches) + 1

for angle in priority_angles:
    for creative_idx, creative_spec in enumerate(angle.creatives, 1):
        batch_id = f"DCT{next_batch_num:03d}"
        row = {
            "BATCH": batch_id,
            "FORMAT": creative_spec.format,  # "UGC" / "Founder" / "Static" / etc.
            "AD": f"{angle.name} - Creative {creative_idx}",
            "MARKET AWARENESS": angle.awareness_level,  # from §4/§5
            "MARKET SOPHISTICATION": angle.sophistication_level,  # from §4
            "ANGLE": angle.name,
            "PERSONA": angle.primary_avatar,  # "Avatar 1: The Hesitant Calculator"
            # STATUS and metric columns intentionally empty — sheets-updater fills
        }
        writer.append_row(creatives_tab, row, full_cols)
        next_batch_num += 1
```

### Idempotency rule

Before appending, check for existing BATCH IDs in column A. If a row with the same BATCH ID already exists:
- **Strategy column update:** forbidden by default (protected columns). Raise warning: "BATCH DCT00X exists with different strategy. Append as DCT00X-v2 or abort?"
- **Metric column update:** forbidden for this skill (that's `sheets-updater`'s job).

The only clean path: append NEW batch IDs. Never mutate existing rows.

---

## Tab 3 — COPY — NOT THIS SKILL'S RESPONSIBILITY

**Owned by:** ad-concept-engine (same writer as CREATIVES tab)
**Input file:** `clients/<project>/campaigns/dct-YYMMDD/dct-tracker.json` (copy fields per creative)

Retained as reference for ad-concept-engine to implement. Source-of-truth does NOT write here.

**Gid lookup:** `config["tabs"]["copy"]["gid"]` (example value: `1695031878` — actual gid per client in their `metrics-config.json`)
**Write mode:** manual (per config) — actually treated as append
**Columns:** `STATUS, COPY 1, COPY 2, HEADLINE 1, HEADLINE 2`

### Row construction

Each CREATIVES row should have a corresponding COPY row (same BATCH ID is implicit by row order — the config doesn't have a batch column in COPY, so we rely on parallel ordering).

Actually — verify this during first write. The protected_columns for CREATIVES include `AD` (the creative name). Check if COPY tab has a similar identifier column, or if it's strict row-parallel.

```python
copy_tab = writer.get_tab(sheet, config["tabs"]["copy"]["gid"])
copy_cols = config["tabs"]["copy"]["columns"]

for angle in priority_angles:
    for creative_idx, creative_spec in enumerate(angle.creatives, 1):
        # Per angle-hooks-library.md, each angle has 10 hooks → we pick top 2 per creative for 2 headlines
        # And 2 distinct copy frameworks (e.g. PAS + Story) per creative for 2 copies
        row = {
            "STATUS": "DRAFT",  # valid values: DRAFT, REVIEW, UPLOAD, LIVE
            "COPY 1": creative_spec.copy_variants[0],  # e.g. PAS framework
            "COPY 2": creative_spec.copy_variants[1],  # e.g. Story framework
            "HEADLINE 1": creative_spec.headline_variants[0],
            "HEADLINE 2": creative_spec.headline_variants[1],
        }
        writer.append_row(copy_tab, row, copy_cols)
```

### STATUS state machine

- `DRAFT` — just written by this skill
- `REVIEW` — user reviewed and approved copy, flagged for final polish
- `UPLOAD` — ready for `meta-ads-uploader`
- `LIVE` — currently running in Meta

This skill only writes `DRAFT`. State transitions happen manually or via other skills.

---

## HITL Preview Before Any Sheet Write

Per `sheets-updater` convention (`hitl.daily_write: preview_then_approve`), always preview before write:

```markdown
## Sheet Write Preview — {{project_name}} — {{date}}

### AVATARS tab ({{gid}})
Will write 3 rows (replacing existing):
  1. "Avatar 1: The Hesitant Calculator" — {{narrative_preview_100chars}}...
  2. "Avatar 3: The Burned Sceptic" — {{narrative_preview_100chars}}...
  3. "Avatar 4: The Faith-First Family" — {{narrative_preview_100chars}}...

### CREATIVES tab ({{gid}})
Will append 9 new rows (next batch: DCT001):

| BATCH | FORMAT | AD | MARKET AWARENESS | MARKET SOPHISTICATION | ANGLE | PERSONA |
|-------|--------|----|----|----|-------|---------|
| DCT001 | Static | The 3-Number Test — Creative 1 | Problem-Aware | L4 | The 3-Number Test | Avatar 1: The Hesitant Calculator |
| DCT002 | UGC | The 3-Number Test — Creative 2 | Problem-Aware | L4 | The 3-Number Test | Avatar 1: The Hesitant Calculator |
| ... 7 more rows |

### COPY tab ({{gid}})
Will append 9 new rows matching CREATIVES by parallel order:

| STATUS | COPY 1 (first 80 chars) | COPY 2 (first 80 chars) | HEADLINE 1 | HEADLINE 2 |
|--------|------------------------|------------------------|-----------|-----------|
| DRAFT | "[ad copy variant 1, 80-char preview]" | "[ad copy variant 2, 80-char preview]" | "[headline 1]" | "[headline 2]" |
| ... |

---

Proceed? (yes / preview-each-tab / skip-sheet-write)
```

User answers → write / partial-write / skip.

---

## Error Handling

| Error | Recovery |
|---|---|
| `ProtectedColumnError` raised by sheets_writer | Should never happen for this skill — we only WRITE strategy columns + only APPEND. If it fires, investigate before continuing. |
| Batch ID collision (DCT00X exists) | Offer: append as next available ID, OR abort |
| Sheet not found / auth failure | Surface: "Sheet access failed. Verify `scripts/modal/credentials.json` has edit access to {{sheet_id}}. Run `/sheets:verify` to diagnose." |
| Tab gid not found | Surface: "Tab with gid X not found. Sheet structure may have changed — re-run `/sheets:provision` or update `metrics-config.json`." |
| Partial write (some rows succeeded, some failed) | Log partial state. Surface exactly which rows wrote vs failed. Offer retry on failed rows only. |

---

## Roll-back

If user rejects a sheet write AFTER partial rows have been written:
- CREATIVES / COPY: delete by BATCH ID (safe — we control the batch IDs we just wrote)
- AVATARS: restore from the preview snapshot taken before `clear()` was called (the skill should take a snapshot before any destructive write)

Always take a snapshot before any destructive operation. Write the snapshot to `clients/<project>/sheet-snapshots/YYMMDD-HHMM-pre-write.json`.

---

## Call Pattern From source-of-truth Skill

End of Phase 5 write sequence:

```python
# 1. Write markdown files (source-of-truth.md + 5 derivatives)
write_markdown_files()

# 2. If metrics-config.json exists, AVATARS-only sheet integration
if sheet_integration_available():
    preview = build_avatars_preview()
    if hitl_approve(preview):
        take_snapshot()          # snapshots AVATARS tab only
        write_avatars_tab()       # replaces AVATARS tab rows with source-of-truth avatars
        log_to_learnings("sheet-avatars-write", rows_written)
    else:
        log_to_learnings("sheet-avatars-write-skipped", reason=user_reason)

# 3. CREATIVES + COPY tabs — note dependency, don't write
print_dependency_note(
    "CREATIVES + COPY tabs will be populated by ad-concept-engine when "
    "a Conductor Mode run executes. That skill is expected to ship ad_concept_sheet_writer.py."
)

# 4. Output hand-off message
print_handoff()
```

---

## Extension Hook — Future Capabilities (v1.1+)

- **Avatar change detection:** before overwriting AVATARS tab, diff new vs existing. If user manually edited an avatar row in the sheet, preserve those edits or flag conflict.
- **DCT results feedback loop:** after 7 days of spend data in CREATIVES metric columns, trigger refresh: route winning BATCH IDs back into `angles/wave-N.md` as "confirmed winners" + log promotion in `angles/iteration-log.md`.
- **Copy status automation:** when `sheets-updater` sees STATUS=LIVE on a row AND spend > 0 in Meta → auto-flag for inclusion in §18 Performance Feedback Loop of the next source-of-truth refresh.

Not in v1.0.0 scope — surfaced here so future maintainers know where to extend.
