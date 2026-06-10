---
description: Approve a video pipeline gate and write upstream hashes before flipping status
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [project-id-or-path] [gate]
---

## Contract

`/video:approve <project> <gate>` flips an explicit phase gate to approved. Before the status flip, it records upstream SHA-256 hashes in that phase's `_gate.json.upstream_hashes`.

Concept is implicit and already approved by `/video:new`; approving concept is a no-op status refresh.

## Local Runner

```bash
python3 scripts/video_pipeline.py approve <project-id-or-path> <gate>
```
