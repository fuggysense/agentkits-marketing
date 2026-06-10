# Codex handoff — Video pipeline restructure

**Run from:** `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/` (main repo root, NOT this worktree)

**Before starting:** merge `worktree-video-pipeline-council-20260512` to main so the council artifacts (`docs/council/*`) ship with the work:
```
cd "/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing"
git merge worktree-video-pipeline-council-20260512
```
Then have Codex cut a fresh branch: `feat/video-studio-week-1`.

**Source of truth for context:**
- `docs/council/council-report-20260512-211023-video-pipeline.html` — the verdict (open in browser first)
- `docs/council/council-transcript-20260512-211023-video-pipeline.md` — full transcript
- `/Users/jerel/.claude/jobs/0f7593ad/orisilver-skills-summary.md` — OriSilver back-port map
- `/Users/jerel/.claude/jobs/0f7593ad/orisilver-x-final-report.md` — OriSilver scrape digest

---

## Tasks for Codex (in order, ship each before starting next)

### TASK 0 — 3-sentence "what is this" doc (15 min)
Create `docs/video-studio.md` with this draft (Jerel to edit, do NOT auto-rewrite):

> The video studio. Tell the studio what you want (the brief). The studio picks the right crew and gear (engine + DP profile + skills), shoots it (generates), shows you takes for approval (HITL). Every shipped video teaches the studio what worked for this client, so the next one starts smarter.

### TASK 1 — Define ground-truth signal (5 min)
Append to `docs/video-studio.md` a Ground Truth section:

> A video is good if Jerel approves it on first review. (W4+ may upgrade to Meta CTR/CPA when instrumented.)

### TASK 2 — Fence off in-flight client work (15 min)
- Read `clients/*/state.json` and `clients/*/campaigns/` to list every in-flight video deliverable
- Write `docs/video-runs/_frozen-skills.md` listing which skills are touched by in-flight work
- Do NOT modify those skills in any later task without Jerel's explicit OK

### TASK 3 — Orchestrator merge (Mon work)
- Edit `skills/video-factory/SKILL.md`: add `--engine={sora|kling|veo|seedance}` flag documentation + behavior
- Edit `skills/video-director/SKILL.md`: add `deprecated: true` to frontmatter, add a banner pointing to `video-factory --engine=...`. DO NOT DELETE the file.
- Edit `.claude/rules/routing-table.md`: route `video-director` trigger phrases to `video-factory`
- Run `python .claude/scripts/link-skills.py` (or whatever the project uses — check `docs/system-rules/skill-graph-rule.md`)
- Verify by reading `.claude/skill-graph.json` — `video-director` should be flagged deprecated

### TASK 4 — Stills→motion HITL doctrine (Tue work)
- Edit `skills/video-factory/SKILL.md`: add new section "Stills Plane → Motion Plane Doctrine":
  - Stills (character sheets, outfit fuses, scene plates) must be HITL-approved before any motion generation begins
  - Source the OriSilver rationale (wardrobe-first sequencing, identity drift prevention)
  - Reference `/Users/jerel/.claude/jobs/0f7593ad/orisilver-skills-summary.md` §4

### TASK 5 — Ship one real client video (Wed-Fri — JEREL'S work, not Codex)
- Jerel picks a real client + brief
- Runs it through the merged stack end-to-end
- Logs to `docs/video-runs/run-001.md`: brief, engine chosen, prompts used, outputs, cost, time, Jerel verdict, failure modes
- This is the BASELINE — Codex cannot do this autonomously

---

## DO NOT DO (council vetoed these)

- ❌ Do NOT merge `beat-sheet-director` and `ai-filmmaking` — narrative vs ad-frame are different crafts
- ❌ Do NOT auto-inject the OriSilver DP macro as default — codify as 1 of 3-4 presets in W3 only
- ❌ Do NOT build `ugc-pipeline-bridge` skill yet — wait for usage data
- ❌ Do NOT build `video-ledger.json` or autoresearch loop yet — wait until 5 real runs exist (W4)
- ❌ Do NOT create `video-producer` agent yet — zero new capability
- ❌ Do NOT sweep OriSilver rules into every video skill — only into the skills that actually fire in W1-W2 runs (W3 work)
- ❌ Do NOT productize anything ("Branded Video Engine as a Service") — Month 3+ only

---

## 4 open questions Jerel needs to answer before W3

1. Ground-truth signal — keep Jerel-first-approval, or build Meta CTR/CPA instrumentation?
2. `ai-filmmaking` boundary — keep separate (council recommendation) or merge anyway?
3. Trigger.dev UGC pipeline — submodule into repo, stay island-mode, or build bridge?
4. Hedra Labs — thin wrapper skill for fake-podcast format, or skip?

---

## Success criteria for W1

- `video-factory --engine=...` works in routing
- `video-director` skill flagged deprecated, not deleted
- `routing-table.md` + `skill-graph.json` regenerated
- One real client video shipped end-to-end on new stack
- `docs/video-runs/run-001.md` exists and is complete
- No in-flight client video broken
