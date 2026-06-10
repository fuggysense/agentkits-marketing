---
description: Show the next video pipeline phase without auto-dispatching a sub-agent
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [project-id-or-path]
---

## Contract

W1/W2 `/video:resume <project>` is manual-dispatch only. It reads `INDEX.md` / `lock.json`, prints the next blocked phase, and gives the recommended command or sub-agent invocation. It does not call Higgsfield and does not spend credits.

If the work has not yet been imported from Video Concept Lab, do not run `/video:resume`. First validate the campaign handoff:

```bash
python3 scripts/video_pipeline.py validate-handoff <client> <campaign> <concept-slug>
```

If approval is pending, return to the campaign folder and ask for concept approval. If approval is complete, create the resumable project:

```bash
python3 scripts/video_pipeline.py new-from-concept <client> <campaign> <concept-slug> --selected-concept <concept-id>
```

## Local Runner

```bash
python3 scripts/video_pipeline.py resume <project-id-or-path>
```
