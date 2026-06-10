# 05_prompt-packs/

**What lives here:** canonical model-agnostic prompt pack + per-model adapters for the approved concept.

Expected files:
- `canonical-prompt-pack.json` and `canonical-prompt-pack.md` — model-agnostic source of truth
- `model-adapters/` — one file per renderer (e.g. `seedance.json`, `kling.json`, `sora.json`, `veo.json`)
- `manual-run-guide.md` — operator-facing instructions if any clips need manual rendering

**Load to do X:**
- Produce adapter payloads → load canonical pack + the renderer's adapter spec; output goes to `../06_generation-runs/<run-id>/payloads/`.

**Owner agent:** `video-prompt-pack-builder` (canonical + adapters), `cinema-worldbuilder` (Seedance formatter).

**Gate:** blocked until AG1 approved.
