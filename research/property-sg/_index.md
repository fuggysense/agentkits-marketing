# Property SG — Market Research

Industry-level market intelligence for Singapore property. Reusable across all property clients (propwise-sg, fuggysmedia, future).

**Scope:** NOT ads. Ads live in `swipe-files/property-sg/`. This folder is market context — sentiment, buyer language, stats, policy, trends.

---

## Structure

| Folder | What goes here | Sources |
|---|---|---|
| `sentiment/` | How Singaporeans feel about property — complaints, hopes, frustrations | Reddit (r/singaporefi, r/singapore, r/askSingapore), HardwareZone, Facebook groups, YouTube comments |
| `buyer-language/` | Raw voice-of-customer — exact phrases buyers use | Forum quotes, review mining, call transcripts (feeds `buyer-language-researcher` agent) |
| `market-data/` | Hard numbers — prices, volumes, supply | HDB resale data, URA private transactions, SRX, 99.co, PropertyGuru reports |
| `policy/` | Rules that shape buyer behavior | MOP, cooling measures, ABSD, LTV limits, CPF housing rules, HDB eligibility |
| `trends/` | What's shifting over time | News, macro shifts, sentiment trendlines, emerging buyer archetypes |

---

## Naming convention

`YYMMDD_<topic>_<source>.md` — e.g. `260315_mop-decision_reddit-singaporefi.md`

Keep raw pulls raw. Synthesize into summary docs at folder root (e.g. `sentiment/_sentiment-summary.md`).

---

## Consumers

Downstream skills/agents that read from this folder:

- `buyer-language-researcher` agent → pulls from `buyer-language/` for dossier creation
- `ads:source-of-truth` → references `sentiment/` + `market-data/` for §5.7 ICP Language Analysis
- `avatar-research` → mines `sentiment/` for Raw Inner Dialogue + Top 5 Deep Fears
- `content-strategy` → uses `trends/` for editorial angle selection
- `deep-research` → writes new findings back here

---

## How to add research

1. Drop raw pull (Reddit thread dump, URA CSV, news article) into the right subfolder
2. Name with date + topic + source
3. If it's signal-rich, add a one-paragraph synthesis at the top of the file
4. Update the relevant `_summary.md` if the insight changes the overall picture

---

## Client usage

Any property client can reference this folder:

```
propwise-sg  → reads research/property-sg/policy/ for MOP content
fuggysmedia  → reads research/property-sg/sentiment/ for agent-buyer pain points
```

Client-specific learnings stay in `clients/<slug>/learnings.md`. Industry-wide insights stay here.
