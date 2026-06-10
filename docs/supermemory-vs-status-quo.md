# Supermemory.ai vs. the Real Competitive Set (May 2026)

For Jerel — marketing operator running Claude Code + Obsidian + per-project auto-memory.

## Comparison Table

| Tool | One-liner | Best at | Worst at | OSS / Self-host | Pricing | Claude API / Code / MCP | Memory model |
|---|---|---|---|---|---|---|---|
| **Supermemory.ai** | Managed memory API + universal MCP across tools | Cross-tool recall (Claude + ChatGPT + Cursor sharing one brain) via MCP; fast hybrid retrieval (<300ms); SaaS connectors (Notion/Slack/Gdrive/Gmail) | Core engine is proprietary; self-host gated behind enterprise contract | SDKs OSS; **core closed**; self-host = enterprise only | Free 1M tok / 10K queries; $0.01/1K tok, $0.10/1K searches overage | Yes / Yes (MCP) / Yes (native MCP server) | Hybrid vector + graph + user profile |
| **Mem0** | Open-source memory extraction layer for chatbots | Drop-in personalization for LLM apps; managed cloud option; broad SDK | Shallow on knowledge-graph reasoning; chatbot-shaped, not operator-shaped | Apache 2.0, self-hostable | OSS free; managed cloud tiered | Yes / via MCP wrapper / Yes | Vector + extracted facts |
| **Letta** (MemGPT) | Stateful agent runtime with editable memory blocks | Long-running autonomous agents that persist identity across days/weeks | Overkill for a human-in-the-loop operator; agent-framework lock-in | Apache 2.0, self-hostable | OSS free; Letta Cloud tiered | Yes / Indirect / Community MCP | Hierarchical memory blocks |
| **Zep** (Graphiti) | Temporal knowledge graph memory | State changes over time ("used to live in X, now Y"); enterprise user state | Requires Neo4j; heavy infra; not a personal tool | Graphiti OSS (Apache 2.0); Zep Cloud closed | OSS free; Cloud from ~$0/dev | Yes / Indirect / Community MCP | Temporal knowledge graph |
| **Cognee** | GraphRAG over messy multi-doc corpora | Deep retrieval across many unstructured sources (PDFs, wikis) | Setup complexity; not built for chat session continuity | Apache 2.0, self-hostable | OSS free; managed tier | Yes / Indirect / Community MCP | Knowledge graph + vector |
| **Claude Code native auto-memory** | Per-project markdown at `~/.claude/projects/.../memory/` | Zero-setup, zero-cost, lives in your CLAUDE.md flow; survives `/clear` | **Per-project only — no cross-project, no cross-tool**; no mobile; no sharing | N/A (local files) | Free | Native / Native / N/A | File-based markdown |
| **Obsidian + Claude (your current)** | Markdown vault as source of truth | Total ownership; portable; human-readable; works with all tools that can read files | Manual curation; no semantic search without plugins; not real-time across devices for AI tools | Fully local | Free (Obsidian Sync $4/mo optional) | Via file reads / Native / Filesystem MCP | File-based |
| **Claude 1M context (lazy baseline)** | Just dump everything into one giant context | Zero infra; no memory drift inside a session | Resets every session; expensive at scale; no cross-session learning | N/A | Pay-per-token | Native / Native / N/A | None — ephemeral |

Sources: [Supermemory site](https://supermemory.ai/), [Supermemory MCP](https://supermemory.ai/mcp/), [Supermemory GitHub](https://github.com/supermemoryai/supermemory), [Vectorize comparison](https://vectorize.io/articles/supermemory-alternatives), [n1n.ai 2026 comparison](https://explore.n1n.ai/blog/ai-agent-memory-comparison-2026-mem0-zep-letta-cognee-2026-04-23), [Letta forum thread](https://forum.letta.com/t/agent-memory-letta-vs-mem0-vs-zep-vs-cognee/88), [Atlan 2026 ranking](https://atlan.com/know/best-ai-agent-memory-frameworks-2026/).

---

## What Supermemory Uniquely Offers vs. Your Status Quo

- **Cross-tool memory via MCP.** Record in ChatGPT mobile, recall in Claude Code, recall in Cursor — one shared brain. Your Obsidian vault can't do that without you manually shuttling files. This is the real unlock if you actually use multiple AI tools.
- **Sub-300ms hybrid retrieval at scale.** Once your vault crosses ~10K notes, `Read`/`Grep` over Obsidian gets sluggish. Supermemory's vector+graph index beats file grep on fuzzy semantic queries ("that thing I said about Halbert's coat-of-arms last month").
- **Mobile + non-technical teammate access.** Web UI + connectors (Notion/Slack/Gmail/Gdrive). Your Obsidian vault is single-operator and CLI-bound. If you ever bring on a VA or a client into the memory loop, files won't cut it.

## Where It's Redundant vs. Your Status Quo

- **Per-project session memory is already solved.** Your `~/.claude/projects/.../memory/MEMORY.md` plus Claude Code's auto-capture covers in-flow recall inside Claude Code. Supermemory duplicates this layer.
- **Canonical knowledge is already in Obsidian.** Your voice/, client/, learnings/ folders are version-controlled, human-readable, and survive any vendor going dark. Re-homing canonical knowledge into a closed proprietary engine is a downgrade in ownership.
- **You're not multi-tool yet.** You're 95% Claude Code. The MCP cross-tool magic only pays off if ChatGPT/Cursor are also daily drivers. They aren't.

## Final Recommendation: **SELECTIVELY USE**

Use Supermemory **only as a thin MCP layer for cross-tool transient memory** — never as canonical storage. Specifically:

1. Install the Supermemory MCP in Claude Code + ChatGPT mobile only. Free tier (1M tok / 10K queries) covers a solo operator easily.
2. Use it for **session-scoped scratch** ("remember this for tomorrow's call") — not for client briefs, voice files, or learnings. Those stay in Obsidian.
3. Hard rule: if it would belong in `clients/<project>/` or `learnings/`, it goes to Obsidian. If it's "remind me of this across tools this week," it goes to Supermemory.

Skip the paid tier until you cross 1M tokens — which, given your discipline around context-mode and lean-loading, is unlikely soon.

**Reality check:** The bullshit-detector read here is that Supermemory is selling a real problem (cross-tool fragmentation) to a market that mostly hasn't earned it yet. For Jerel specifically, the gap it fills is narrow. Your file-system-as-memory discipline is already 80% of the value, and the remaining 20% is mostly mobile/cross-tool — which you can solve with a free-tier MCP install and zero lock-in.
