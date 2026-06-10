# 04 Input Images

Input-image plan, image manifest, product references, character/style sheets, beat sheets, B-roll references, and generated start frames.

This folder is optional for text-only or clip-only runs. Use it only when the selected executor payload passes uploaded images, start frames, product references, style sheets, or other visual references.

Adapters must read `input-image-manifest.json` before uploading images to Higgsfield or external APIs. They should not require this manifest when no images are used.
