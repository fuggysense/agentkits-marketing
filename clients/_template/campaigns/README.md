# Campaigns

Campaign folders are self-describing. Do not make agents infer nested paths from memory or from a global prompt.

## Client-Level Registry

`_campaigns-index.json` is the client-level campaign registry created by `/project:new`.

It should list every campaign once it exists:

```json
{
  "campaign_slug": "spring-launch",
  "campaign_index": "campaigns/spring-launch/campaign-index.json",
  "state_file": "campaigns/spring-launch/state.yaml",
  "status": "active"
}
```

## Per-Campaign Discovery

`/campaign:new` creates a per-campaign `campaign-index.json`.

Use this generic pattern for all campaign output work:

```text
campaigns/<campaign-slug>/<artifact-family>/<artifact-slug>/
```

Examples:

```text
campaigns/<campaign-slug>/video-concepts/<concept-slug>/
campaigns/<campaign-slug>/email-sequences/<sequence-slug>/
campaigns/<campaign-slug>/funnel-pages/<page-slug>/
campaigns/<campaign-slug>/landing-pages/<page-slug>/
campaigns/<campaign-slug>/ad-concepts/<batch-slug>/
campaigns/<campaign-slug>/lead-magnets/<asset-slug>/
```

Every deliverable workspace should have:

```text
pipeline-state.json
artifact-manifest.json
event-log.jsonl
workspace-brief.json
01_strategy/
02_drafts/
03_assets/
04_variants/
05_packages/
06_runs/
07_review/
```

For AI-video campaigns, concept workspaces specialize the generic pattern and live at:

```text
campaigns/<campaign-slug>/video-concepts/<concept-slug>/
```

Campaigns do not own the reusable product, market/buyer, competitor, or research inputs. Keep those at the client root:

```text
00_inputs/input-manifest.json
00_inputs/product/
00_inputs/market/
00_inputs/research/
```

Buyer evidence belongs inside market/buyer context under `00_inputs/market/`; do not create a separate top-level persona input family. Distilled buyer psychology and micro-personas live in `_brand/buyer-profile.md`. Demographic/firmographic qualification lives in `_brand/icp.md`.

Create each video concept workspace by copying:

```text
_templates/video-concept-workspace/
```

then replacing `{{campaign_slug}}` and `{{concept_slug}}` inside the copied files.

Every active concept workspace must contain:

```text
pipeline-state.json
artifact-manifest.json
event-log.jsonl
concept-brief.json
01_strategy/
02_ag1-options/
03_scripts/
04_input-images/input-image-manifest.json
05_prompt-packs/
06_generation-runs/
07_review/
```

`concept-brief.json` is the selected-input contract for video workspaces. Other workspace types should use a typed alias such as `sequence-brief.json`, `page-brief.json`, or the generic `workspace-brief.json`. It should reference only the specific entries from `00_inputs/input-manifest.json` and `_brand/buyer-profile.md` micro-personas that this workspace uses, with a short rationale for each selection. Do not copy the full `00_inputs/` folder into a campaign or deliverable workspace.

`02_ag1-options/` stores candidate directions and Approval Gate 1 review artifacts inside an already-selected workspace. It exists because a workspace may evaluate several candidate directions before the operator approves one.

### Simple concept-generation route

If a fresh agent receives a short task like "generate concepts", "run concept stage", or "create AG1 options", it should not guess between strategy and concept tools. Use this deterministic route:

```text
workspace/concept-brief.json
+ workspace/01_strategy/creative-diversity-map.json
+ selected workflow flow SKILL.md
+ /Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/skills/video-concept-lab/SKILL.md
  ↓
/Users/jerel/.claude/agents/video-concept-seeder.md
  ↓
workspace/02_ag1-options/concepts-draft.json
  ↓
Phase 4 synthesis creates concept-pack.* and approval-1.json
```

`creative-diversity-map` is strategy only. `video-concept-lab` is methodology/rubric only. `video-concept-seeder` is the single runtime concept generator.

Agents must read in this order:

1. Client root `CONTEXT.md` for the high-level folder map.
2. Client root `CLAUDE.md` for local routing law, if present.
3. This `campaigns/README.md` for campaign/workspace rules.
4. `campaigns/_campaigns-index.json`
5. `campaign-index.json`
6. `campaign-selection.json`
7. workspace `artifact-manifest.json`
8. workspace `pipeline-state.json`
9. workspace brief (`concept-brief.json`, `sequence-brief.json`, `page-brief.json`, or `workspace-brief.json`)

If a future folder layout changes, update `CONTEXT.md`, this README, and the relevant template files. Do not force every downstream agent prompt to know the new path shape.

For video generation runs, `06_generation-runs/<run-id>/` should use the lean clip-run contract by default:

```text
run-manifest.json
payloads/
clips/
review/review.json
stitch/ffmpeg-command.sh
stitch/final.mp4
```

Create `stills/`, `beat-sheets/`, `motion-prompts/`, or `rerenders/` inside a run only when the selected workflow actually uses them.

For image uploads in video workspaces, adapters should read `04_input-images/input-image-manifest.json` only when the payload uses uploaded images. Text-only or clip-only runs should not require image manifests.

## Intake — `concept-brief.json` required fields

`concept-brief.json` lives at the workspace ROOT (not under `00_inputs/`). It is the selected-input contract for AI-video concept workspaces. Run intake via `AskUserQuestion` if missing AND workspace exists. Reference `00_inputs/input-manifest.json` entries by ID — do not duplicate the bank.

| Field | Definition |
|---|---|
| `micro_persona_id` | Buyer micro-persona from `_brand/buyer-profile.md`. MUST be in `campaign-selection.json` scope. |
| `creative_pattern` | Campaign's creative pattern (replaces legacy `_brand/big-ideas/` going forward). |
| `big_idea_premise` | Campaign's creative thesis — the central premise the concept executes against. |
| `spine_angle_family` | Angle family the concept's spine belongs to. |
| `allowed_expressions` | Phrases / framings permitted for this concept. |
| `forbidden_expressions` | Phrases / framings explicitly off-limits. |
| `language_to_use` | Buyer-voice vocabulary to lean into. |
| `language_to_avoid` | Vocabulary / jargon to suppress. |
| `style_lanes` | Visual / tonal lanes available to the concept. |
| `style_lane_split` _(optional)_ | Distribution across lanes when multiple are in play. |
| `proof_hooks` | Proof beats / evidence hooks the concept can reach for. |
| `workflow_flow` | The Format axis. Left `null` at intake; populated at §6 of vid-director. |
| `script_mode` | `"spoken" \| "singing"` (default `"spoken"`). **Orthogonal to Format** — singing is not a `workflow_flow`. When `"singing"`, pack-builder loads `skills/video-concept-lab/references/direct-response/singing-ads-layer.md`. |
| `visual_character_id` _(optional)_ | On-screen presenter / mascot reference from `_brand/visual-characters/`. **Production reference, NOT a strategy axis.** Use `"none"` when no presenter appears. |
| `target_video_frame` | Aspect/frame target (e.g. 9:16, 1:1, 16:9). |
| `primary_platform` | Primary distribution platform. |
| `product` | Product/offer the concept sells. |
| `claim_risk` | Claim-risk classification for downstream gates. |

**Alias rule:** legacy `concept-input-packet.json` is an accepted alias in older workspaces. Treat it as equivalent — do not rename in place unless explicitly asked.

## Resume Protocol

When a workspace has prior state (`pipeline-state.json.current_phase > 0` OR artifacts present in `02_ag1-options/` / `03_scripts/` / `04_input-images/` / `05_prompt-packs/` / `07_review/` / `06_generation-runs/`), this is a **RESUME**, not a fresh start. Do not silently proceed.

### Artifact → phase completion mapping

| Artifact present | Phase complete |
|---|---|
| `02_ag1-options/concepts-draft.json` | Phase 1 (seeder) |
| `02_ag1-options/hook-variants-draft.json` | Phase 2 (hook-variant — multi-clip only) |
| `02_ag1-options/eval-universal-*.json` + `eval-flow-compliance-*.json` | Phase 3 (evaluators) |
| `02_ag1-options/concepts.json` + `concept-pack.{md,json,html}` | Phase 4 (synthesis) |
| `02_ag1-options/prompt-input-preview.{json,md}` | Phase 4.5 (preview stubs) |
| `02_ag1-options/approval-1.json` (status: pending) | AG1 written, waiting on operator |
| `02_ag1-options/approval-1.json` (status: approved) | AG1 cleared |
| `03_scripts/scripts-draft.json` + `script-pack.md` | Phase 6 scripts drafted |
| `04_input-images/input-image-manifest.json` | Phase 6 input-image plan drafted |
| `05_prompt-packs/canonical-prompt-pack.{json,md}` | Phase 6 prompt pack drafted |
| `05_prompt-packs/model-adapters/` populated | Phase 6 adapters drafted |
| `05_prompt-packs/manual-run-guide.md` | Phase 6 manual run guide drafted |
| `07_review/approval-2.json` (status: pending) | AG2 written, waiting on operator |
| `07_review/approval-2.json` (status: approved) | AG2 cleared — ready for manual gen or render |
| `06_generation-runs/<run-id>/run-manifest.json` | Renders dispatched/in-flight/completed |

### Phase-ordering validation

After mapping artifacts to phases, walk `pipeline-state.json.phases[]`. For each entry where `phase_N.status: "completed"` and N is greater than the index of the current open approval gate (AG1 covers phases 1–4.6; AG2 covers phases 6–6.5), check whether that gate's `approval-N.json` exists AND has `status: "approved"`. If the gate's approval file is missing OR `status != "approved"`, surface in the Resume Card under **Blockers detected**:

```
⚠ PHASE ORDERING WARNING — phases X-Y executed before gate Z. approval-Z.json missing (or not approved).
```

Concretely: if `phase_6.status: "completed"` but `02_ag1-options/approval-1.json` is absent or pending/rejected, that is a real out-of-order execution. Surface it; do not silently continue. Operator must approve the missing gate, write the approval file, or explicitly accept the drift before the Resume Card's suggested actions become valid.

### Then read

- `event-log.jsonl` — last 10 events to understand HOW work paused (operator stop / failure / partial revision / approval pending).
- `pipeline-state.json.open_subagent_threads` (if present) — any persistent-chat subagent handles (seeder, hook-variant, pack-builder) still alive. If so, prefer reconnect via `SendMessage` over fresh dispatch.

### Resume Card (always — never auto-resume)

```
RESUME CARD — <client>/<campaign>/<concept-slug>
Last completed phase: <Phase N — short description>
Last event: <action> at <ISO timestamp> (<how long ago>)
Artifacts on disk:
  - <bulleted list with phase tags>
Open subagent threads: <handles + their phase | none>
Pending approvals: <AG1 status / AG2 status / none>
Blockers detected: <any missing upstream context | none>

Suggested next actions:
1. <Most likely continuation> — e.g., "Approve/revise AG1 in approval-gate-1.html"
2. <Surgical option> — e.g., "Re-run only c03 with stronger Pixar emphasis"
3. <Backward option> — e.g., "Go back to AG0 to rework spine before re-seeding"
4. <Restart option> — e.g., "Wipe 02_ag1-options/ and re-run from Phase 1 (destructive — confirm)"
5. Show full state — dump pipeline-state.json + event-log.jsonl tail

What would you like to do?
```

Wait for operator decision before ANY further action. The operator may have paused intentionally; do not assume the happy path.

If `pipeline-state.json` is missing but the workspace folder exists, the workspace was scaffolded but never run — treat as a fresh start (skip resume card).

### RESUME RULE — precedence on conflict

When the orchestrator is handed a workspace path instead of a fresh brief, BEFORE reading `event-log.jsonl`, `pipeline-state.json`, or any workspace artifact, walk up to `clients/<slug>/CONTEXT.md` and read it. **CONTEXT.md and this `campaigns/README.md` are the only authoritative folder/workspace maps.** Subagent files at `~/.claude/agents/<x>.md` describe ONE agent's I/O contract — they are NEVER the workspace's canonical structure. **When an agent file's path claims disagree with CONTEXT.md or this README, CONTEXT.md and this README win.**

### Bypass mechanism

Operator may bypass an unmet eval/gate by recording `pipeline-state.json.eval_override` with:

```json
{
  "eval_override": {
    "phase": "4.6" | "6.5",
    "timestamp": "<ISO>",
    "operator": "<handle>",
    "reason": "<written justification>"
  }
}
```

Override is non-reusable and applies only to the gate at the named phase.
