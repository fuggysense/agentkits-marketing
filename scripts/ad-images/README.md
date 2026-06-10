# ad-images — swappable prompt styles + image executor

Stops the manual "paste a prompt, download the image, repeat" grind. Two moving parts:

1. **`styles/`** — a library of visual-director prompt templates you swap between. Each is a `.md` instruction set the orchestrator loads to *craft* a final image prompt. Add one = drop a `.md` + a line in `_registry.json`.
2. **`render.py`** — the executor. Takes a finished prompt and renders it to a PNG through a swappable engine. Default GPT Image 2 (Azure). The creative judgement stays with you + Claude; only the mechanical render is automated.

## The two swaps

| Swap | Where | How |
|---|---|---|
| **Style** (clean DR ↔ chumbox native ↔ future) | `styles/*.md` | Claude loads a different style file to write the prompt; `--style <key>` stamps it on the render log |
| **Engine** (GPT Image 2 ↔ future API/CLI) | `render.py` `ENGINES` dict | `--engine <key>` |

## Seeded styles

- `dr-clean-static` — clean Singapore direct-response static ad (real faces, headline baked in, the 9 rules). Default.
- `chumbox-native` — uncanny "wait, what am I looking at" native/chumbox ad. Cold curiosity clicks.

`python3 render.py --list-styles` to see them.

## The flow (with the approval gate)

```
1. Pick a style.            Claude reads styles/<key>.md
2. Claude crafts prompts.   angle + headline + style  ->  final image prompt(s)
3. GATE — preview:          render.py --prompt "..." --out out/a01-v1.png --style <key> --dry-run
4. You approve.             eyeball the prompt + target path, no credits spent
5. Render:                  same command, drop --dry-run
```

Every real render writes a `<image>.png.meta.json` sidecar — prompt, style, engine, settings — so you can always see what produced an image.

## Run it from a real pipeline output

If a `dct.json` already holds `image_prompt` fields (from ad-concept-engine / big-angle-spotter), skip hand-crafting. The current shape is an `image_pool.images[]` array where each image carries an `id`, `angle_id`, `variant_id`, and `image_prompt`:

```
# one pool image by id
python3 render.py \
  --from-tracker clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/dct.json \
  --image DCT002-img-01 --style dr-clean-static --dry-run

# the whole pool at once (dry-run resolves every prompt; a real render of >1 image needs --confirm-all)
python3 render.py --from-tracker .../dct.json --style dr-clean-static --dry-run

# filter the pool by angle, then variant
python3 render.py --from-tracker .../dct.json --batch A02 --variant v1 --dry-run
```

It reads the prompt straight from the file (inline `image_prompt` or the `image_prompt_file` reference) and auto-targets `<dct-dir>/images/<id>.png` — the same path the pool already references.

**Legacy shape.** The older `creatives[]` / `variations[]` tracker (`dct-tracker.json`) is auto-detected; force it with `--legacy-shape`. There `--batch` is the batch id and `--variant` is required:

```
python3 render.py --from-tracker .../dct-tracker.json \
        --batch DCT010-A01 --variant v1 --style dr-clean-static --dry-run
```

Legacy renders auto-target `campaigns/<slug>/image-prompts/renders/<batch>-<variant>.png`.

**Claim gate.** Before any tracker render, `render.py` runs `scripts/claim_gate.py --gate <tracker>` if that script exists. It is being built in parallel, so the hook NO-OPs with a warning when absent. `--skip-claim-gate` opts out explicitly (also logged).

## Add a new engine later

Write one function in `render.py` — `(prompt, out, size, quality, refs, dry_run) -> dict` — and register it in `ENGINES`. Example targets: Nano Banana 2 (Vertex), Higgsfield, fal.ai Flux. The default stays GPT Image 2 until you change `DEFAULT_ENGINE`.

## Add a new style later

Drop `styles/my-style.md` (visual-director instructions) and add an entry to `styles/_registry.json`. Done — it shows up in `--list-styles` and `--style my-style`.

## Where this sits vs the rest

- **big-angle-spotter** (`skills/big-angle-spotter/`) already runs the angle → headline → image-prompt chain. This tool is the *render* step that pipeline stops short of, plus the style library it never had.
- It does **not** edit that global skill — it reads its output. Keeps the shared skill clean.
