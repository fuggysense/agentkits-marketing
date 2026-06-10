# Legacy Avatar Index — {{client_name}}

**Created:** {{today}}
**Targeting source of truth:** `_brand/buyer-profile.md#micro-persona-map`
**Status:** Deprecated for buyer targeting. Use this directory only for legacy exports, tooling compatibility, or visual-character references.

## Contract

- Do not use `_brand/avatars/` as the buyer-targeting source of truth.
- Buyer targeting lives in `_brand/buyer-profile.md` under `## MICRO-PERSONA MAP`.
- Each buyer micro-persona is defined by motivation, pain, desired outcome, lifestyle/context, buying trigger, awareness, sophistication, core psychology, and market behavior.
- Demographics alone do not define a persona.
- Separate avatar files are allowed only for legacy/tooling exports or visual-character, mascot, presenter, and face-lock workflows.

## Legacy / Tooling Exports

| File | Source Micro-Persona | Purpose | Last Synced |
|------|----------------------|---------|-------------|
| [avatar-<slug>.md] | [Name in buyer-profile.md] | [legacy/tooling/visual-character] | {{today}} |

## Refresh Log

| Date | Action | Reason |
|------|--------|--------|
| {{today}} | Created | Legacy avatar index template |

## File Rules

- Every legacy avatar file must link back to `_brand/buyer-profile.md#micro-persona-map`.
- Use matching JSON only when downstream tooling needs structured fields.
- Do not treat a video character or mascot as a buyer target. If it is based on buyer insight, map it back to a real micro-persona in buyer-profile.md.
