# 06 Generation Runs

Lean clip-run folders live here after render approval or explicit operator render confirmation.

Default run shape:

```text
<run-id>/
  run-manifest.json
  payloads/
    clip-01.json
  clips/
    clip-01/output.mp4
  review/
    review.json
  stitch/
    filelist.txt
    ffmpeg-command.sh
    final.mp4
```

Optional helper folders such as `stills/`, `beat-sheets/`, `motion-prompts/`, and `rerenders/` belong inside the run only when the selected workflow uses them.
