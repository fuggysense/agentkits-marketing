---
description: Print canonical video project status
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [project-id-or-path]
---

## Contract

`/video:status <project>` prints the schema §12.5 canonical status format. The leading gate symbols are load-bearing:

- `[✓]` approved
- `[⏳]` pending
- `[⚠]` blocked
- `[▶]` executing
- `[—]` not-started

## Local Runner

```bash
python3 scripts/video_pipeline.py status <project-id-or-path>
```
