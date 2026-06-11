# CLAUDE.md — concept workspace routing card

Local routing law for THIS concept workspace. Parent `clients/{{client_slug}}/CLAUDE.md` global rules still apply.

**Before doing anything in this workspace, an agent MUST read in order:**

1. `clients/{{client_slug}}/CONTEXT.md` — Entry Protocol + folder map.
2. `clients/{{client_slug}}/campaigns/README.md` — campaign + workspace rules (esp. **Intake** and **Resume Protocol**).
3. `../../campaign-index.json` and `../../campaign-selection.json` — campaign scope + this workspace's status.
4. This workspace's `artifact-manifest.json`, `pipeline-state.json`, `concept-brief.json` — current state + selected inputs.

**Resume rule:** if `pipeline-state.json.current_phase > 0` OR any phase folder has artifacts, treat this as a RESUME — do not regenerate completed phases. Log every state-changing action to `event-log.jsonl`.
