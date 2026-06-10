# Ferres Knowledge — Index

Sean Ferres' AI Ads Lab, distilled into operational rulebooks. **Load a distilled file first; drop to the QMD corpus only when you need a verbatim quote, a timestamp, or detail the distill omitted.**

## Distilled files (load one when its question is yours)

| File | Answers | Load when |
|---|---|---|
| `01-foundations-winning-ad-anatomy.md` | What makes an ad win; the 7-element anatomy; positioning | Defining what "good" looks like before drafting |
| `02-research-flow.md` | His pre-ad research process as a runnable stage map | Starting any new ad; building ICP/competitor/market docs |
| `03-angles-hooks-copy.md` | Angle taxonomy, hook rules, script structure, the AI prompts | Writing hooks, angles, or video-ad copy |
| `04-end-to-end-sop.md` | Blank page to 4 live ads (the $300 Control Challenge) | You want the full operational pipeline, step by step |
| `05-quality-bar-critique-rubric.md` | Section-by-section critique checklist | Reviewing a drafted ad before launch |
| `06-statics-playbook.md` | 5 static formats, direct/indirect, "25 before lunch" | Producing static image ads |
| `07-media-buying-testing-scaling.md` | Metrics, kill/scale rules, fatigue, feedback loop | Launching, testing, or scaling spend on Meta |
| `08-client-acquisition-business-ops.md` | Getting clients, offer doc, pricing, contract, objections | Selling the service or running the business side |
| `09-tools-and-master-prompts.md` | Tool stack + the verbatim master-prompt catalog | You need the exact prompt text or current tool routing |
| `ferres-pipeline-stage-map.md` | The whole A-to-Z process, one row per stage | You want the map across all files in one view |
| `patterns/video-pattern-library.md` | Recurring video-ad patterns pulled from the swipe vault | Modelling a proven video structure |
| `patterns/statics-pattern-library.md` | Recurring static-ad patterns + sub-recipes | Modelling a proven static structure |

## The corpus (deep lookup)

Location: `/Users/jerel/corpora/sean-ferres` — full transcripts, slide text, prompt lists, and a 51-ad swipe vault. Indexed in three QMD collections (hybrid BM25 + vector + local rerank):

- `ferres-talks` — timestamped video transcripts (`.md`)
- `ferres-docs` — slide/PDF text, cheatsheets, prompt lists (`.txt`)
- `ferres-visuals` — vision layer (`.md`): Opus-described swipe-vault ads + deck-page descriptions

Example queries:
```bash
qmd query "how do you write a scroll-stopping hook" -c ferres-talks -c ferres-docs
qmd search "objection handling" -c ferres-docs
```

## Read-only rule

This corpus is a **library, never a pipeline.** Read it, quote it, cite it. Do not write into it, restructure it, or wire it as a step in any automated flow. Distilled files here are the working layer; the corpus is the source you check against.
