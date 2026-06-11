# 04_input-images/

**What lives here:** input-image manifest and any actual input images when the selected workflow uses uploaded reference frames.

Expected files:
- `input-image-manifest.json` — declares each image's role (character / product / scene-ref) and source path
- image files themselves (or links to `_brand/` or local media root if heavy)

**Load to do X:**
- Build a prompt pack that uses uploaded refs → adapters read `input-image-manifest.json` to wire payloads.

**Skip rule:** text-only or clip-only runs do NOT require an image manifest — leave the file absent.

**Owner agent:** `image-generation` (when generating refs) or `gpt-image-2-director` (for layout/character sheets).
