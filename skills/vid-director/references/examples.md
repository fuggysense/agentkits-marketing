# vid-director — Output Format Examples

Load on demand when drift surfaces or a fresh orchestrator forgets a template shape. Not auto-loaded.

---

## §7 AG0 Compass — chat template

Emit ONE paragraph in chat before any concept dispatch:

```
AG0 COMPASS
Workspace: <abs path to concept workspace>
Workflow flow / Format: <flow> (multi_clip=true|false)
Strategy map: <map_id> (combinations=<N>, diversity_risk=<low|medium|high>)
Methodology loadout: <methodology_loadout_id from video-concept-lab/REFERENCE_GRAPH.json>
Spine: <angle_family>
Primary combination: <combination_id> = <micro_persona> × <angle> × <awareness> × <format>
Implied visual character: <visual_character_id from concept-brief.json | "none" | "inferred-from-format">
Style lanes: <list>
Awareness × Sophistication: <Stage X> × <Stage Y>
Why <format> fits the spine: <one sentence>
Why this micro-persona × angle × awareness combination: <one sentence>
Claim-risk check: <allowed | needs-review | blocked> — <reasoning vs concept-brief allowed/forbidden_expressions + platform policy>
Concept count: <N concepts × 2 hooks for multi-clip | N×2 concepts for single-clip>
Kill switches: <conditions under which operator should kill now>
```

After emission, wait for `go` / `approve AG0` / `kill`. No proceed without explicit approval.

**Preconditions (enforced before emission, per vid-director.md §7):**
- `concept-brief.json` (or legacy `concept-input-packet.json`), `campaign-selection.json`, AND `creative-diversity-map.json` must all exist on disk and be complete. No placeholder AG0 with "TBD" fields. If incomplete, return to §5.
- Scope check: the primary combination's `micro_persona_id` MUST be in `campaign-selection.json` scope. Halt + ask operator to widen scope or pick another persona otherwise.
- Claim-safety: any concept depending on a claim NOT in `concept-brief.allowed_expressions` is auto-rejected at AG0 or downstream Phase 3.

---
