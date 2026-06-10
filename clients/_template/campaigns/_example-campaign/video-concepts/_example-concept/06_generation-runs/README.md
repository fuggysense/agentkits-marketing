# 06_generation-runs/

**What lives here:** one subfolder per render run, keyed by `<run-id>` (e.g. `run-001/`, `seedance-v1/`).

Per-run lean clip contract:
```
<run-id>/
  run-manifest.json       # which adapter, which prompt-pack revision, model, seed
  payloads/               # per-clip payloads sent to the renderer
  clips/                  # downloaded MP4s
  review/review.json      # per-clip approve/reject + notes
  stitch/ffmpeg-command.sh
  stitch/final.mp4
```

Add `stills/`, `beat-sheets/`, `motion-prompts/`, or `rerenders/` only if the selected workflow uses them.

**Owner agent:** `video-factory` (orchestrator) — invokes renderer adapters and ffmpeg stitch.

**Gate:** blocked until AG2 approved (`../07_review/approval-2.json` verdict = approved).
