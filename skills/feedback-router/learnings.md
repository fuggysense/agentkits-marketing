# Learnings — feedback-router

> Accumulated learnings from running this skill across waves and clients.

## Confirmed Patterns

### Architecture (260418)

**Rule:** feedback-router OUTPUTS routing decisions but does NOT execute them. It prints the recommended next slash command + rationale; the user approves and runs.

**Why:** keeps HITL at every loop boundary. Auto-executing the routed action would compound errors silently — a wrong NEW decision would burn an entire research cycle on the wrong premise. User as gatekeeper at each loop closure is non-negotiable.

**How to apply:** every Phase 4 hand-off ends with the recommended slash command in plain text + the rationale tied to specific metrics. User runs the command if they agree.

## What Works

<!-- Patterns that produced strong outputs in real wave runs -->

## What Doesn't Work

<!-- Approaches that consistently produced weak / wrong routing decisions -->

## Per-Client Notes

<!-- Wave-over-wave patterns specific to a client/product_type that should NOT be generalised -->
