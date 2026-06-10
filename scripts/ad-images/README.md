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

If a `dct-tracker.json` already holds `image_prompt` fields (from big-angle-spotter / ad-concept-engine), skip hand-crafting:

```
python3 render.py --from-tracker clients/<client>/campaigns/<slug>/dct-tracker.json \
        --batch DCT010-A01 --variant v1 --style dr-clean-static --dry-run
```

It reads the prompt straight from the tracker (inline `image_prompt` or the `image_prompt_file` reference), auto-targets `campaigns/<slug>/image-prompts/renders/<batch>-<variant>.png`.

## Add a new engine later

Write one function in `render.py` — `(prompt, out, size, quality, refs, dry_run) -> dict` — and register it in `ENGINES`. Example targets: Nano Banana 2 (Vertex), Higgsfield, fal.ai Flux. The default stays GPT Image 2 until you change `DEFAULT_ENGINE`.

## Add a new style later

Drop `styles/my-style.md` (visual-director instructions) and add an entry to `styles/_registry.json`. Done — it shows up in `--list-styles` and `--style my-style`.

## Where this sits vs the rest

- **big-angle-spotter** (`skills/big-angle-spotter/`) already runs the angle → headline → image-prompt chain. This tool is the *render* step that pipeline stops short of, plus the style library it never had.
- It does **not** edit that global skill — it reads its output. Keeps the shared skill clean.
