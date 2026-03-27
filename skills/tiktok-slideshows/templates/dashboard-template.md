# TikTok Slideshows Dashboard — [PROJECT NAME]

> Obsidian Dataview dashboard for TikTok slideshow campaign tracking.
> Reads from: story-ledger.md, hooks-db.md, competitor-scan-*.md
> Requires: [Dataview plugin](https://github.com/blacksmithgu/obsidian-dataview) installed in Obsidian

---

## Batch Overview

| Batch | Date | Posts | Status |
|-------|------|-------|--------|
> *Manually updated from story-ledger.md or use Dataview query below*

```dataview
TABLE batch AS "Batch", date AS "Date", posts AS "Posts", status AS "Status"
FROM "clients/<project>/campaigns/tiktok-slideshows/story-ledger"
WHERE batch
```

---

## Pillar Balance

Check story-ledger.md → Pillar Usage table for current distribution.

**Target:** No pillar >40% or <15% across all batches.

| Pillar | % | Status |
|--------|---|--------|
| The Filter | —% | — |
| Try-On Magic | —% | — |
| Style DNA | —% | — |
| Insider Access | —% | — |

---

## Available Hooks

```dataview
TABLE type AS "Type", power AS "Power", views AS "Views", WITHOUT ID file.name AS "Hook"
FROM "clients/<project>/assets/video/hooks-db"
WHERE status = "Available"
SORT power DESC
```

> If Dataview can't parse inline fields, check hooks-db.md manually for `**Status:** Available` entries.

---

## Performance Leaderboard

Top posts by engagement — populated after batch goes live (7+ days).

| Rank | Post | Pillar | Views | Eng% |
|------|------|--------|-------|------|
> *Populated from story-ledger.md → Performance by Batch table*

---

## Winners Flagged for Recreation

| Post | Hook | Why It Worked | Variation Ideas |
|------|------|---------------|-----------------|
> *Populated from story-ledger.md → Winners to Recreate table*

---

## Competitor Scan History

Latest scan reports in `campaigns/tiktok-slideshows/competitor-scan-*.md`:

```dataview
LIST
FROM "clients/<project>/campaigns/tiktok-slideshows"
WHERE file.name STARTSWITH "competitor-scan"
SORT file.name DESC
LIMIT 5
```

---

## Open Threads

Narrative promises made in content that need to be paid off in the next batch.

> *Check story-ledger.md → Narrative Arc Tracker → Open Threads*

---

## Archetypes Covered

> *Check story-ledger.md → Archetypes Covered section*

---

*Last updated: [date]*
