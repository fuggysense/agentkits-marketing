# Paper.design MCP — Tool Reference & Workflow Patterns

## Tool Reference (All 24 Tools)

### Read Tools

#### `get_basic_info`
Returns file name, canvas dimensions, and basic metadata.
- **Parameters:** None
- **Returns:** `{ fileName, canvasWidth, canvasHeight, ... }`
- **Use:** Availability check at session start (3s timeout)

#### `get_tree_summary`
Returns the full node tree structure of the design file.
- **Parameters:** None (reads entire file)
- **Returns:** Nested tree of `{ id, name, type, children[] }`
- **Use:** Map design structure before code generation

#### `get_selection`
Returns currently selected node(s) in the Paper canvas.
- **Parameters:** None
- **Returns:** Array of selected node IDs
- **Use:** Export only what the user has highlighted

#### `get_node_info`
Detailed information about a specific node.
- **Parameters:** `{ nodeId: string }`
- **Returns:** `{ id, name, type, x, y, width, height, styles, ... }`
- **Use:** Deep-dive into a specific design element

#### `get_children`
Returns child nodes of a given parent node.
- **Parameters:** `{ nodeId: string }`
- **Returns:** Array of child nodes with basic info
- **Use:** Walk the tree section by section

#### `get_jsx`
Exports a node (and descendants) as JSX with Tailwind classes.
- **Parameters:** `{ nodeId: string }` (omit for full page)
- **Returns:** JSX string with `className` attributes using Tailwind
- **Use:** Primary code export — convert to HTML for builds
- **Note:** Output uses React conventions (`className`, `htmlFor`). Convert to plain HTML attributes.

#### `get_computed_styles`
Returns precise computed CSS values for a node.
- **Parameters:** `{ nodeId: string }`
- **Returns:** `{ color, fontSize, fontWeight, padding, margin, borderRadius, boxShadow, ... }`
- **Use:** Extract exact design tokens (colors, spacing, typography)
- **Advantage over Gemini vision:** Pixel-perfect values vs visual approximation

#### `get_screenshot`
Takes a screenshot of the current canvas or a specific node.
- **Parameters:** `{ nodeId?: string, scale?: number }`
- **Returns:** PNG image data
- **Use:** Visual comparison between Paper design and HTML build

#### `get_fill_image`
Extracts the fill/background image from a node.
- **Parameters:** `{ nodeId: string }`
- **Returns:** Image data (PNG/JPG)
- **Use:** Extract background images and textures for use in HTML

#### `get_font_family_info`
Returns all font families used in the design.
- **Parameters:** None
- **Returns:** Array of `{ family, weights[], styles[] }`
- **Use:** Generate correct Google Fonts `<link>` tags

#### `get_guide`
Returns layout guides, constraints, and grid settings.
- **Parameters:** None
- **Returns:** `{ guides[], grids[], constraints[] }`
- **Use:** Understand spacing system and alignment rules

### Write Tools

#### `create_artboard`
Creates a new artboard in the design file.
- **Parameters:** `{ name: string, width?: number, height?: number }`
- **Returns:** `{ nodeId }` of the new artboard
- **Use:** Create a canvas for `write_html` output

#### `write_html`
Pushes HTML content to an artboard for visual rendering.
- **Parameters:** `{ nodeId: string, html: string }`
- **Returns:** Success/failure
- **Use:** Core of bidirectional workflow — push generated HTML to Paper for visual preview
- **Requirements:** HTML must include Tailwind CDN `<script>` tag. Target must be an artboard.

#### `set_text_content`
Updates the text content of a text node.
- **Parameters:** `{ nodeId: string, text: string }`
- **Returns:** Success/failure
- **Use:** Update copy without rebuilding the design

#### `update_styles`
Modifies CSS styles on existing nodes.
- **Parameters:** `{ nodeId: string, styles: { [property]: value } }`
- **Returns:** Success/failure
- **Use:** Tweak colors, spacing, typography without full rebuild

#### `rename_nodes`
Renames one or more nodes/layers.
- **Parameters:** `{ updates: [{ nodeId: string, name: string }] }`
- **Returns:** Success/failure
- **Use:** Organize layer names to match HTML section IDs

#### `duplicate_nodes`
Duplicates existing nodes.
- **Parameters:** `{ nodeIds: string[] }`
- **Returns:** Array of new node IDs
- **Use:** Clone sections for A/B variations

#### `delete_nodes`
Removes nodes from the design.
- **Parameters:** `{ nodeIds: string[] }`
- **Returns:** Success/failure
- **Use:** Clean up unused artboards/elements

#### `find_placement`
Finds optimal placement for new content relative to existing nodes.
- **Parameters:** `{ referenceNodeId: string, position: "above"|"below"|"left"|"right" }`
- **Returns:** `{ x, y }` coordinates
- **Use:** Position new artboards near existing work

#### `start_working_on_nodes`
Locks nodes for editing (begins an atomic batch operation).
- **Parameters:** `{ nodeIds: string[] }`
- **Returns:** Lock token
- **Use:** Prevent visual flickering during multi-step edits

#### `finish_working_on_nodes`
Releases locked nodes (ends atomic batch operation).
- **Parameters:** `{ lockToken: string }`
- **Returns:** Success/failure
- **Use:** Complete a batch edit, trigger re-render

#### `group_nodes`
Groups selected nodes into a group container.
- **Parameters:** `{ nodeIds: string[] }`
- **Returns:** `{ groupNodeId }`
- **Use:** Organize related elements

#### `ungroup_nodes`
Ungroups a group node, releasing children.
- **Parameters:** `{ nodeId: string }`
- **Returns:** Array of released child node IDs
- **Use:** Restructure design hierarchy

#### `set_fill_image`
Sets a fill/background image on a node.
- **Parameters:** `{ nodeId: string, imageData: string }` (base64)
- **Returns:** Success/failure
- **Use:** Place generated images into the design

---

## Bidirectional Workflow Patterns

### Pattern 1: Code → Paper → Iterate

```
1. Generate index.html (Tailwind CDN)
2. create_artboard({ name: "HTML Preview", width: 1440, height: 900 })
3. write_html({ nodeId: artboardId, html: fullHtmlString })
4. get_screenshot({ nodeId: artboardId }) → compare visually
5. User edits in Paper canvas (drags, resizes, recolors)
6. get_jsx({ nodeId: artboardId }) → read changes back
7. Update index.html with changes
8. Repeat from step 3
```

### Pattern 2: Paper → Code (Mode D)

```
1. get_basic_info() → confirm file is loaded
2. get_tree_summary() → map all sections
3. get_font_family_info() → build Google Fonts link
4. For each top-level section:
   a. get_jsx({ nodeId }) → get Tailwind code
   b. get_computed_styles({ nodeId }) → get exact tokens
   c. Convert JSX → HTML (className → class, etc.)
5. Assemble full index.html
6. create_artboard({ name: "Code Output" })
7. write_html → push for comparison
8. get_screenshot of both → compare
9. Fix mismatches → repeat
```

### Pattern 3: Design Token Extraction

```
1. get_tree_summary() → find key elements
2. For each brand element:
   a. get_computed_styles({ nodeId }) → extract exact values
3. Build Tailwind config:
   - colors: from computed color values
   - spacing: from padding/margin values
   - borderRadius: from border-radius values
   - fontFamily: from get_font_family_info()
   - fontSize: from computed font sizes
```

---

## JSX → HTML Conversion Reference

| JSX (from `get_jsx`) | HTML equivalent |
|-----------------------|-----------------|
| `className="..."` | `class="..."` |
| `htmlFor="..."` | `for="..."` |
| `<img src="..." />` | `<img src="...">` |
| `<input ... />` | `<input ...>` |
| `<br />` | `<br>` |
| `<hr />` | `<hr>` |
| `<>...</>` | (remove fragment wrapper) |
| `{/* comment */}` | `<!-- comment -->` |
| `onClick={...}` | (remove or convert to inline) |
| `style={{ color: 'red' }}` | `style="color: red"` |
| `tabIndex={0}` | `tabindex="0"` |

Tailwind utility classes transfer 1:1 — no conversion needed.

---

## `get_computed_styles` vs Gemini Vision

| Aspect | Paper `get_computed_styles` | Gemini vision (`design-analyze`) |
|--------|---------------------------|----------------------------------|
| Color accuracy | Exact hex/rgba values | Approximate — may be off by 5-10% |
| Font size | Exact px/rem | Approximate — rounds to nearest common size |
| Spacing | Exact px values | Approximate — often guesses Tailwind tokens |
| Border radius | Exact px | Usually correct for standard values |
| Shadows | Full CSS shadow string | Approximate — loses spread/blur precision |
| Gradients | Full CSS gradient syntax | Describes direction + colors, imprecise stops |
| Best for | Precise token extraction, exact recreation | Quick overview, layout understanding, mood |

**Recommendation:** Use Paper for exact values when available. Fall back to Gemini vision when Paper isn't running or for quick visual analysis.

---

## `write_html` Input Format

The HTML string must be a complete, self-contained document or fragment:

```html
<!-- Minimal working example -->
<script src="https://cdn.tailwindcss.com"></script>
<div class="p-8 bg-white">
  <h1 class="text-4xl font-bold text-gray-900">Hello Paper</h1>
  <p class="mt-4 text-lg text-gray-600">This renders inside Paper.</p>
</div>
```

**Known limitations:**
- External CSS files won't load (use Tailwind CDN + inline styles)
- JavaScript interactions won't execute (static render only)
- Google Fonts via `<link>` tags may not load — use `@import` in a `<style>` tag as fallback
- Very large HTML (>50KB) may render slowly — split into sections if needed
- iframes and embedded media won't render

---

## Free Tier Notes

- All 24 tools available — no premium gating
- No API key required — local-only communication
- No rate limits — Paper runs on your machine
- No telemetry concerns — MCP traffic stays on localhost
- File size limited by your machine's memory, not by tier

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Connection refused` on any tool | Paper.app not running | Launch Paper.app |
| `Connection refused` after launch | No file open in Paper | Open or create a design file |
| `get_basic_info` returns empty | File still loading | Wait 2-3 seconds, retry |
| `write_html` shows blank artboard | Missing Tailwind CDN script | Add `<script src="https://cdn.tailwindcss.com"></script>` |
| `get_jsx` returns empty string | Node has no renderable content | Check node type — may be a group/frame, try children |
| `get_computed_styles` missing values | Node is hidden or zero-size | Ensure node is visible and has dimensions |
| Fonts render differently | Font not installed locally | Use Google Fonts `@import` in the HTML |
| Screenshot is cropped | Artboard too small for content | Set explicit width/height on `create_artboard` |
