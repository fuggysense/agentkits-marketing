#!/usr/bin/env python3
"""
Agent Initializer - Creates a new agent .md file from template

Usage:
    init_agent.py <agent-name> --path <path>

Examples:
    init_agent.py marketing-strategist --path agents/
    init_agent.py seo-analyst --path /custom/path/
"""

import sys
from pathlib import Path

AGENT_TEMPLATE = """---
name: {agent_name}
version: "1.0.0"
brand: "AgentKits Marketing by AityTech"
description: |
  [TODO: One-line summary of the agent's role.]

  <examples>
  <example>
  <user>[TODO: Example user request]</user>
  <response>[TODO: Example agent response]</response>
  </example>
  <example>
  <user>[TODO: Another example request]</user>
  <response>[TODO: Another example response]</response>
  </example>
  </examples>
model: sonnet
---

# {agent_title}

## Language Directive

[TODO: Define communication style. Be specific — tone, formality, sentence length, jargon policy, default language.]

## Context Loading

[TODO: What context does this agent need before responding? List sources: project files, user history, referenced URLs, etc.]

## Reasoning Process

[TODO: Step-by-step thinking process. How should the agent approach problems? What order of operations?]

## Skill Integration

[TODO: Which skills can this agent invoke? Map skill names to trigger conditions.]

## Role Responsibilities

[TODO: What does this agent own vs. delegate?]

**Owns:**
- [TODO: Responsibility 1]

**Delegates:**
- [TODO: Task → target skill/agent]

## Core Capabilities

[TODO: Numbered list of what the agent can do.]

1. **[Capability]** — [Description]
2. **[Capability]** — [Description]
3. **[Capability]** — [Description]

## Process

[TODO: The agent's workflow from receiving a request to delivering output.]

1. Receive and clarify the request
2. [TODO: Step 2]
3. [TODO: Step 3]
4. Present results
5. Ask for feedback

## Output Formats

[TODO: How the agent structures its responses for different request types.]

## Tool Usage Guidelines

[TODO: Rules for tool usage — which tools, when, in what order.]

## Quality Checklist

Before delivering any response, verify:
- [ ] [TODO: Check 1]
- [ ] [TODO: Check 2]
- [ ] [TODO: Check 3]
- [ ] No hallucinated data or URLs
- [ ] Appropriate length for the request

## Edge Cases

[TODO: How to handle unusual situations.]

- **Ambiguous request**: [TODO: Strategy]
- **Out of scope**: [TODO: Strategy]
- **Conflicting instructions**: [TODO: Strategy]

## Feedback Loop

### Self-Annealing
[TODO: Specific self-correction rules for this agent]

### HITL Gate
[TODO: Where human approval is required]

### Iteration
Use this agent, then tell me what to improve.
"""


def title_case(name):
    """Convert hyphenated name to Title Case."""
    return " ".join(word.capitalize() for word in name.split("-"))


def init_agent(agent_name, path):
    """
    Create a new agent .md file from template.

    Args:
        agent_name: Hyphen-case agent name
        path: Directory where the .md file will be created

    Returns:
        Path to created file, or None on error
    """
    target_dir = Path(path).resolve()

    if not target_dir.exists():
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {target_dir}")
        except Exception as e:
            print(f"Error creating directory: {e}")
            return None

    agent_file = target_dir / f"{agent_name}.md"

    if agent_file.exists():
        print(f"Error: Agent file already exists: {agent_file}")
        return None

    agent_title = title_case(agent_name)
    content = AGENT_TEMPLATE.format(agent_name=agent_name, agent_title=agent_title)

    try:
        agent_file.write_text(content)
    except Exception as e:
        print(f"Error writing agent file: {e}")
        return None

    print(f"Agent '{agent_name}' created at {agent_file}")
    print()
    print("Next steps:")
    print("1. Fill in all [TODO] sections in the generated file")
    print("2. Add XML examples in the frontmatter description")
    print("3. Choose the right model (haiku/sonnet/opus)")
    print("4. Define skill integrations and quality checklist")
    print("5. Register with: register.py agent " + agent_name + ' --description "..."')

    return agent_file


def main():
    if len(sys.argv) < 4 or sys.argv[2] != "--path":
        print("Usage: init_agent.py <agent-name> --path <path>")
        print()
        print("Examples:")
        print("  init_agent.py marketing-strategist --path agents/")
        print("  init_agent.py seo-analyst --path /custom/path/")
        sys.exit(1)

    agent_name = sys.argv[1]
    path = sys.argv[3]

    print(f"Initializing agent: {agent_name}")
    print(f"Location: {path}")
    print()

    result = init_agent(agent_name, path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
