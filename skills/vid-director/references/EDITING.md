# vid-director — Editing & Self-Improvement

Load this file ONLY when the operator says "edit your persona," "add a new flow," "tighten failure modes," or otherwise wants to change vid-director's behavior. Not part of the per-cycle context.

## File map — where to edit what

| What | Path | Edit when |
|---|---|---|
| Orchestrator persona (the slim router) | `/Users/jerel/.claude/prompts/orchestrators/vid-director.md` | Routing rules, pipeline shape, HITL gate behavior, operator commands, preflight delegation rules |
| **Template folder contract** | `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/clients/_template/CONTEXT.md` + `_template/campaigns/README.md` | Canonical client + workspace folder shape changes. If you change these, vid-director's §5 + all subagent path references must follow. |
| **Onboarding** | `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/skills/client-onboarding/SKILL.md` | Onboarding flow (Path A research / Path B intake), scaffolding behavior, `scripts/scaffold-client.sh` |
| Concept seeder | `/Users/jerel/.claude/agents/video-concept-seeder.md` | Concept output is generic, compass mis-scored, brand-context enumeration drift |
| Hook variant generator | `/Users/jerel/.claude/agents/video-hook-variant-generator.md` | Hook A/B too similar, Frankenstein leakage, missing 3-element framework |
| Universal evaluator | `/Users/jerel/.claude/agents/eval-video-universal.md` | Misses forbidden_expressions, wrong compass axes, returns prose not JSON |
| Flow-compliance evaluator | `/Users/jerel/.claude/agents/eval-video-flow-compliance.md` | Misses flow-specific rule violations, wrong rule citations |
| Flow-explainer (Haiku) | `/Users/jerel/.claude/agents/flow-explainer.md` | Summaries > 300 words, invents capabilities, exposes internal code names |
| Phase 4.5 preview stub builder | `/Users/jerel/.claude/agents/prompt-preview-stub-builder.md` | Preview stubs write full prompts instead of intent, or model lock-in leaks |
| Post-AG1 prompt pack builder | `/Users/jerel/.claude/agents/video-prompt-pack-builder.md` | Adapter authors new claims, canonical prompt isn't model-neutral, manual run guide assumes one tool |
| Higgsfield skill (CLI gotchas, model picks) | `/Users/jerel/.claude/skills/higgsfield/SKILL.md` | CLI param flags change, new model added, cost table stale |
| Discovery menu script | `/Users/jerel/.claude/scripts/video-flows-menu.sh` | New flow added or recategorized |
| Sidecar: examples | `/Users/jerel/.claude/prompts/orchestrators/vid-director/examples.md` | Stale chat samples |
| Sidecar: changelog | `/Users/jerel/.claude/prompts/orchestrators/vid-director/CHANGELOG.md` | Append-only version notes |

## Higgsfield-prompts repo (separate scope)

Edit there when the SKILL.md or render prompt template is wrong, not vid-director's routing:

| What | Path |
|---|---|
| Workflow flow SKILL.md | `/Users/jerel/AI workflows/higgsfield-prompts/skills/workflow-generation/<flow>/SKILL.md` |
| Render prompt templates | `/Users/jerel/AI workflows/higgsfield-prompts/skills/media/video-generation/references/<flow>-clip-prompt.md` |
| Image generation refs | `/Users/jerel/AI workflows/higgsfield-prompts/skills/media/image-generation/references/*.md` |
| Viral preset recipes | `/Users/jerel/AI workflows/higgsfield-prompts/skills/media/viral-presets/<slug>/SKILL.md` |
| Repo routing CLAUDE.md | `/Users/jerel/AI workflows/higgsfield-prompts/CLAUDE.md` |

Edits to the higgsfield-prompts repo take effect on the NEXT subagent dispatch (no session caching).

## Video Factory skill (separate scope)

| What | Path |
|---|---|
| Video Factory entry | `/Users/jerel/.claude/skills/video-factory/SKILL.md` |
| Phase 0 dispatcher | `/Users/jerel/.claude/skills/video-factory/references/phase-0-dispatcher.md` |
| Pipeline branches | `/Users/jerel/.claude/skills/video-factory/references/pipelines/*.md` |
| Model guides | `/Users/jerel/.claude/skills/video-factory/kb/model-guides/*.md` |

## Edit workflow

1. **Identify the problem specifically.** "Output is bad" is not actionable. "Concept c03's hook reads as a paraphrase of c01's hook" is actionable.
2. **Find the right file** from the tables above.
3. **Backup first** for high-risk changes: `cp <file> <file>.bak-$(date +%Y%m%d-%H%M%S)`.
4. **Edit** — any editor. Or ask vid-director to edit on your behalf; I'll show the diff before writing.
5. **Test before live use** — spawn a Sonnet subagent with a mock dispatch (see "Testing pattern" below).
6. **Restart ccv to apply persona edits.** Persona is loaded at session start. Subagent file edits take effect on next dispatch (no restart needed).

## Testing pattern (Sonnet smoke-test)

Before running an edited persona/subagent on a live client:

```
Spawn a general-purpose subagent (Sonnet for orchestrator/seeder/hook/eval personas, Haiku for flow-explainer):

prompt: "You are testing the <persona-name>.md persona. Read it at <path>. Then ROLE-PLAY as the persona receiving this mock dispatch: <mock inputs that mirror real dispatch>. Execute the persona's expected behavior. Return the output per the persona's schema. After the output, SELF-EVALUATE: did you follow the persona's rules? Did the output match the schema? Quality concerns? Suggested fixes?"
```

Run multiple subagents in parallel if testing multiple personas at once. 6 parallel tests typically take ~5 min and catch 3+ critical issues.

## What NOT to edit casually

- **Engine routing rules (§3 in persona)** — deterministic. Add a new ROW, don't soften an existing row.
- **Schema fields owned by subagents** — schemas live in the agent file that WRITES the artifact. Changing a schema requires updating that agent + every downstream consumer.
- **Tool allowlist** — narrowing breaks dispatch; widening (e.g., adding `rm`) breaks safety. Edit with intent + comment why.
- **The 4-axis compass weights** — `first_frame_thumbstop`, `spine_clarity`, `flow_renderability`, `claim_safety` are equal-weighted 1-10. Changing weights requires coordinated updates to BOTH evaluators + seeder self-rate logic.
- **AG1/AG2 hard-stop semantics** — they're hard stops by design. Don't loosen to "soft warn."

## When to propose a NEW subagent

vid-director itself should suggest new subagents when:
- A phase keeps eating > 30% of orchestrator context per cycle
- The same dispatch pattern fires 3+ times across recent campaigns with hand-tweaks each time
- An operator-asked task doesn't fit any existing subagent's contract
- A failure pattern surfaces 3+ times that no current subagent owns

The proposal should specify: name, model, tools, inputs, outputs (schema), what-it-never-does, why existing agents can't cover it, and where it slots in the pipeline (§2). The operator approves before the file is created.
