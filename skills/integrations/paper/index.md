# Paper.design Integration

> Visual design editing, JSX/Tailwind export, and HTML preview via Paper.design MCP

## Overview

Paper.design is a modern web-based design tool that exposes 24 MCP tools for reading and writing design files. It enables bidirectional design workflows — Claude reads designs from Paper, pushes HTML back for visual preview, and exports Tailwind code from Paper designs.

- **App:** `/Applications/Paper.app` (macOS)
- **MCP endpoint:** `http://127.0.0.1:29979/mcp` (HTTP transport)
- **Tier:** Free
- **Requirement:** Paper must be running with a file open for the MCP to respond

## Setup

### 1. Install Paper.design

Download from [paper.design](https://paper.design) or use the installed app at `/Applications/Paper.app`.

### 2. Configure MCP in Claude Code

Already configured in `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "paper": {
      "url": "http://127.0.0.1:29979/mcp"
    }
  }
}
```

Note: Uses `url` key (HTTP transport), not `command` (stdio).

### 3. Verify Connection

1. Open Paper.app
2. Open or create a design file
3. Test with `get_basic_info` — should return file name and canvas info

## MCP Tools (24 total)

### Read Tools (11)

| Tool | Description | Used By |
|------|-------------|---------|
| `get_basic_info` | File name, canvas size, basic metadata | website-design (availability check) |
| `get_tree_summary` | Full node tree structure of the design | website-design (Mode D analysis) |
| `get_selection` | Currently selected node(s) | website-design (targeted export) |
| `get_node_info` | Detailed info for a specific node | website-design (section analysis) |
| `get_children` | Child nodes of a given parent | website-design (section mapping) |
| `get_jsx` | Export node as JSX with Tailwind classes | website-design (Mode D code export) |
| `get_computed_styles` | Precise computed CSS values for a node | website-design (design token extraction) |
| `get_screenshot` | Screenshot of current canvas or selection | website-design (visual comparison) |
| `get_fill_image` | Extract fill/background image from a node | website-design (asset extraction) |
| `get_font_family_info` | Font families used in the design | website-design (typography matching) |
| `get_guide` | Layout guides and constraints | website-design (spacing/grid analysis) |

### Write Tools (13)

| Tool | Description | Used By |
|------|-------------|---------|
| `create_artboard` | Create new artboard in the design | website-design (HTML preview canvas) |
| `write_html` | Push HTML content to an artboard | website-design (bidirectional preview) |
| `set_text_content` | Update text content of a node | website-design (copy updates) |
| `update_styles` | Modify styles on existing nodes | website-design (style refinement) |
| `rename_nodes` | Rename layers/nodes | website-design (organization) |
| `duplicate_nodes` | Duplicate existing nodes | website-design (iteration) |
| `delete_nodes` | Remove nodes from the design | website-design (cleanup) |
| `find_placement` | Find optimal placement for new content | website-design (layout) |
| `start_working_on_nodes` | Lock nodes for editing (begin batch) | website-design (atomic edits) |
| `finish_working_on_nodes` | Release nodes after editing (end batch) | website-design (atomic edits) |
| `group_nodes` | Group selected nodes | website-design (organization) |
| `ungroup_nodes` | Ungroup a group node | website-design (restructuring) |
| `set_fill_image` | Set fill/background image on a node | website-design (asset placement) |

## Usage with Website-Design Skill

### Bidirectional Workflow Pattern

The core Paper integration pattern is a push/pull cycle:

```
Generate HTML → push to Paper (write_html) → user edits in canvas
→ read back (get_jsx) → refine code → push again → repeat
```

### Mode A (Recreation) Enhancement
After generating HTML from a reference screenshot, push to Paper via `write_html` for visual comparison. Use `get_computed_styles` for precise design token extraction (more accurate than Gemini vision for exact values).

### Mode B (Creation) Enhancement
After generating HTML, push to Paper for visual editing. User adjusts layout in canvas → read back via `get_jsx` → integrate changes into code.

### Mode C (Hybrid) Enhancement
Mode A enhancement for analysis phase + Mode B enhancement for redesign phase.

### Mode D (Paper-First) — Full Workflow
When user has an existing Paper design to convert to code:

1. **Read:** `get_basic_info` → `get_tree_summary` → `get_font_family_info` → `get_screenshot` → `get_jsx` (per section)
2. **Analyze:** Map node tree to HTML sections, extract design tokens via `get_computed_styles`
3. **Generate:** Build `index.html` using Tailwind CDN, converting JSX to plain HTML
4. **Push back:** `write_html` to new artboard, screenshot both, compare
5. **Iterate:** Fix mismatches, re-push, or user edits in Paper → `get_jsx` → update code

## JSX → HTML Conversion Notes

When converting `get_jsx` output to plain HTML:
- `className` → `class`
- Self-closing tags: `<img />` → `<img>` (HTML5)
- `htmlFor` → `for`
- `onChange` → remove (static HTML)
- Tailwind classes transfer directly — no conversion needed
- React fragments `<>...</>` → remove wrapper

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection refused | Paper not running | Open Paper.app and open/create a file |
| Connection refused | No file open | Open a design file in Paper |
| Timeout on `get_jsx` | Large/complex node tree | Export sections individually, not entire page |
| `write_html` renders blank | Invalid HTML structure | Ensure valid HTML with Tailwind CDN script tag |
| Styles don't match | CSS specificity conflicts | Use inline Tailwind classes, avoid external CSS |
| Font mismatch | Font not available in Paper | Check `get_font_family_info`, fall back to similar Google Font |

## Free Tier Notes

- All 24 MCP tools available on free tier
- No API key required — runs locally
- No rate limits (local server)
- No usage tracking or analytics sent externally

## Related

- Website Design skill — `skills/website-design/SKILL.md`
- Paper reference — `skills/website-design/references/paper-integration.md`
- Firecrawl — `skills/integrations/firecrawl/` (web scraping fallback)
