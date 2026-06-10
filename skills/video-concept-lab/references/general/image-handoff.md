# Image Handoff

During Video Concept Lab, define the first-pass image and style-sheet needs for the selected concept. This is an early production hypothesis, not the final prompt plan.

## Product Reference Gate

Before any agent creates product-inclusive scene images, product style sheets, beat sheets, or client-pack visuals, it must verify that approved product reference images exist in the client workspace:

```text
clients/<project>/_brand/brand-assets/<product>/product-packshots/
clients/<project>/_brand/brand-assets/<product>/packaging/
clients/<project>/_brand/brand-assets/<product>/strip-references/
```

Pass condition: at least one real product pack/packaging reference and one strip reference are present as `.png`, `.jpg`, `.jpeg`, or `.webp`.

When working from the repo root, run the gate before product-inclusive visuals:

```bash
python3 skills/video-concept-lab/scripts/check_product_reference_gate.py --client clients/<project> --product <product-slug>
```

If repo-local product references are missing:

1. Check `_brand/asset-map.md` for an external local source folder.
2. List the candidate references for the user.
3. Stop before generating product-inclusive visuals.
4. Ask the user whether to promote/copy selected references into `_brand/brand-assets/`.

Do not invent product packaging, label layout, strip shape, colors, dosage, certifications, or claims. If the user asks for a concept-only mockup before product references are approved, use non-product placeholders and clearly mark them as placeholders.

When a `product-reference-manifest.json` exists, treat it as product truth. Do not reproduce claim-card text marked `unapproved_do_not_reproduce`.

## Required Handoff Fields

```json
{
  "character_style_sheets": [
    {
      "name": "",
      "purpose": "",
      "views_required": ["front", "3/4", "side", "back"],
      "expressions_required": [],
      "wardrobe_lock": "",
      "approval_required": true
    }
  ],
  "product_style_sheets": [
    {
      "product": "",
      "angles_required": [],
      "opened_closed_states": [],
      "label_accuracy_notes": "",
      "approval_required": true
    }
  ],
  "environment_sheets": [
    {
      "scene": "",
      "layout_requirements": "",
      "lighting": "",
      "props": []
    }
  ],
  "style_reference_sheets": [
    {
      "style": "",
      "material_rules": "",
      "negative_rules": ""
    }
  ],
  "props_or_ui_sheets": []
}
```

## Stage Boundary

Video Concept Lab does not write final image prompts, create beat sheets, or call Video Factory.

After Approval Gate 1:

1. Refine the script and visual concept.
2. Run `video-brief-normalizer`.
3. Approve the client-facing brief and internal AI production brief at Approval Gate 2.
4. Let Video Factory generate the actual input-image prompts, beat-sheet prompts, and render prompt pack.

## GPT Image 2 Director Link

Use `gpt-image-2-director` when:
- Creating character turnaround sheets.
- Creating product sheets.
- Creating environment sheets.
- Creating style boards.
- Creating rendered text/UI reference frames.

Do not call Beat Sheet Director yet. Beat sheets happen after input images are approved.

## Downstream Order

`Video Concept Lab -> Approval Gate 1 -> script/visual refinement -> video-brief-normalizer -> Approval Gate 2 -> Video Factory -> input image prompts -> input image approval -> Beat Sheet Director -> render prompts -> Higgsfield approval`
