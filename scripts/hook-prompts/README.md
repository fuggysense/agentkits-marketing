# hook-prompts

Two deterministic prompt templates that wrap `script-skill` for your specific workflow:

1. **`hooks-generate.md`** — generate 20 voice-locked hooks for a concept, medium-depth output
2. **`hooks-select.md`** — score those 20 and pick top 2 for testing

Both templates lock in the **deterministic inputs** that must be present every run, so output stays >80% complete with predictable shape. The remaining 20% is your taste in picking winners + word-level tweaks.

## Why deterministic templates instead of a new skill

You already have `script-skill` (global, voice-locked, hook database, de-AI passes). Don't fork it. Don't create `hook-generator-skill` or `content:hooks-from-concept`. That fragments your skill catalog and confuses the model about which one to invoke.

Instead: these templates lock `script-skill` into your exact workflow by enforcing locked inputs + locked output schema + locked self-check. The skill stays as one entry point; the prompts make it deterministic.

## Cherry-picked from your 4 pasted prompts

| Source | Element kept | Where it lives |
|---|---|---|
| Prompt A (Meta strategist, 25 hooks) | 5 emotional-trigger categories | Mapped onto 4 commandments + funnel-stage routing |
| Prompt B (Hook architect, 20 hooks) | 9 hook formats, 6 archetypes, 4 Commandments, 3-step formula | Full generation skeleton |
| Prompt B (heavy output) | **Dropped** — too verbose for your medium-depth pick | Available in `hooks-generate-heavy.md` if you ever want it (not built yet) |
| Prompt C (selection, top 2 of 10) | 6 scoring criteria + diversity rule | Full selection skeleton |
| Prompt D (analyzer + 7 rewrites) | 4 Fatal Mistakes checklist | Folded into generate-time self-check (no separate analyzer step for now) |
| Your v0.5.2 plan | Funnel-stage split (60/30/10), pillar split (40/30/20/10), voice-lock priority | Inputs `funnel-goal.json` |

## How to invoke

From any Claude Code conversation where `script-skill` is loaded:

```
@script-skill — Use the prompt at scripts/hook-prompts/hooks-generate.md.
Concept: <one sentence describing what to hook around>
Client: michelle-koh
```

Or wire to a slash command (not built yet — say the word when you want `/content:hooks` to autoload this).

## Order of operations

```
[concept input]
  ↓
hooks-generate.md → script-skill → 20 hooks (medium depth)
  ↓
hooks-select.md → script-skill → top 2 hooks for testing + diversity check
  ↓
(human: pick the 1-2 you actually want to film/post)
```

If a generated hook needs a deeper rewrite (e.g. your gut says "this is close but not quite"), Prompt D from your paste is the analyzer — not yet templated here. Add `hooks-analyze.md` later if you find you need it.
