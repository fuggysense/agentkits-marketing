# Thin Image Skill Stack Recommendation

## Keep

| Skill | Path | Role |
|---|---|---|
| image-generation | `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/skills/image-generation/SKILL.md` | Marketing shim/router for still image requests. Patch, do not remove. |
| gpt-image-2-director | `/Users/jerel/.claude/skills/gpt-image-2-director/SKILL.md` | Prompt-only layout, diagram, poster, UI, and text-heavy image director. |
| higgsfield-generate | `/Users/jerel/.agents/skills/higgsfield-generate/SKILL.md` | Canonical generic Higgsfield CLI execution skill. |
| higgsfield-product-photoshoot | `/Users/jerel/.agents/skills/higgsfield-product-photoshoot/SKILL.md` | Canonical product/photo/ad creative image skill. |
| higgsfield-marketplace-cards | `/Users/jerel/.agents/skills/higgsfield-marketplace-cards/SKILL.md` | Canonical marketplace listing and A+ image skill. |
| higgsfield-soul-id | `/Users/jerel/.agents/skills/higgsfield-soul-id/SKILL.md` | Canonical identity/Soul training skill. |

## Archived Or Still To Retire

| Candidate | Path | Reason |
|---|---|---|
| Project higgsfield | `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/skills/higgsfield/SKILL.md` | Removed 2026-05-13. Duplicate `name: higgsfield`; browser/MCP router conflicted with newer CLI split stack. |
| Global higgsfield router | `/Users/jerel/.claude/skills/higgsfield/SKILL.md` | Duplicate broad router; overlaps `.agents/skills/higgsfield-*`. Migrate unique learnings first. |
| seedance-ugc-director | `/Users/jerel/.claude/skills/seedance-ugc-director/SKILL.md` | Active file says retired and absorbed into `seedance-director`. |
| retired Seedance fragments | `/Users/jerel/.claude/skills/seedance-*.retired-*` | Already retired but still in active skill root. Move to archive or delete if covered by git history. |
| marketing-studio-director retired file | `/Users/jerel/.claude/skills/marketing-studio-director/SKILL.md.retired-260504` | Replace stale refs with `higgsfield-generate` Marketing Studio path. |

## Routing Collisions

| Prompt | Current collision | Thin-stack route |
|---|---|---|
| Use Higgsfield to generate a photoreal UGC image | global `higgsfield`, `.agents` Higgsfield skills | `higgsfield-generate`, unless product/marketplace/identity-specific |
| Make me a product shot for Meta ads | `image-generation`, product photoshoot, generic Higgsfield | `higgsfield-product-photoshoot` |
| Create marketplace listing images / A+ cards | `image-generation`, generic Higgsfield, marketplace skill | `higgsfield-marketplace-cards` |
| Generate a character sheet | `image-generation`, `gpt-image-2-director`, `ugc-creator`, `seedance-director` | `gpt-image-2-director` for prompt/layout; execution via chosen image backend |
| Seedance UGC ad from this script | `seedance-director`, retired `seedance-ugc-director` | `seedance-director` |
| Marketing Studio UGC ad video | `higgsfield-generate`, stale `marketing-studio-director` refs | `higgsfield-generate` Marketing Studio mode |

## Cleanup Patch List

Human review checkpoint before applying any of these:

1. Patch `skills/image-generation/SKILL.md` into a router shim:
   - product/photo/ad creative -> `higgsfield-product-photoshoot`
   - marketplace/A+ listing -> `higgsfield-marketplace-cards`
   - identity/Soul/face-lock -> `higgsfield-soul-id`
   - generic Higgsfield generation -> `higgsfield-generate`
   - layout/text-heavy prompt-only -> `gpt-image-2-director`
2. Done 2026-05-13: removed `skills/higgsfield/` and routed project image generation away from the browser skill.
3. Migrate unique `/Users/jerel/.claude/skills/higgsfield/references/*` into `.agents/skills/higgsfield-*`, then retire global `/Users/jerel/.claude/skills/higgsfield/SKILL.md`.
4. Move `/Users/jerel/.claude/skills/seedance-ugc-director/SKILL.md` out of active discovery.
5. Patch stale Seedance refs in `skills/video-director/SKILL.md` and `/Users/jerel/.claude/skills/ugc-creator/SKILL.md` to `seedance-director`.
6. Replace `marketing-studio-director` refs in `/Users/jerel/.claude/skills/seedance-director/SKILL.md` and `/Users/jerel/.claude/skills/video-factory/SKILL.md` with `higgsfield-generate` Marketing Studio.
7. Move `.retired-*` files out of active skill roots into an archive folder, or delete them if git history is enough.

## Next AutoResearch Loop

The targeted loop completed. Product-ad prompt guidance should carry the blank-surface rule, while aspect ratio should become a workflow gate rather than a prompt-only rule:

> Product-ad surfaces must stay blank/unbranded unless the user explicitly asks for a product label. If a brand name is needed, place it only in overlay text or on a separate removable tag, never as an invented logo on the product.

> For feed-safe social ad renders, include true canvas wording, then verify saved dimensions after render. If the generated file is not the requested ratio, rerender within a hard cap or normalize/export deterministically.

Acceptance evidence: L1-A-001 scored 98 with no critical failures after the blank-surface mutation. L3-A-001 scored 99 with no critical failures after adding true 4:5 canvas wording. L4 reproduced aspect-ratio drift, proving prompt-only ratio control is not stable enough for scale.
