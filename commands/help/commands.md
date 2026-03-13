---
description: List all available commands, optionally filtered by keyword
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [search-keyword]
---

## How This Works

This command dynamically scans all command files in `.claude/commands/` and displays them organized by category. It's always up-to-date — when new commands are added, they appear here automatically.

---

## Workflow

### Step 1: Check for Search Keyword

If the user provided an argument (e.g., `/help:commands email`), filter results:

```bash
python3 .claude/scripts/list_commands.py --search "<argument>"
```

If no argument, show full list:

```bash
python3 .claude/scripts/list_commands.py --category
```

### Step 2: Display Results

Show the output from the script. The script reads frontmatter descriptions from each command file.

### Step 3: Offer Guidance

After showing the list, ask:

"Need help picking the right command? Try `/help:guide` — it walks you through what you want to achieve and suggests the best command."

---

## Maintenance

**IMPORTANT:** This command auto-generates from `.claude/commands/` directory structure. No manual updates needed. When you add a new command file with proper frontmatter (`description:` field), it appears here automatically.

The Python script is at: `.claude/scripts/list_commands.py`
