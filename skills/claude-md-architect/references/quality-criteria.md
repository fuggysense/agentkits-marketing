## Graph Links
- **Parent skill:** [[claude-md-architect]]

# CLAUDE.md Quality Criteria

## Scoring Rubric (100 points)

### 1. Workflows & Routing (20 points)

**20**: Complete skill/agent routing, key commands documented, context load order clear
- Skill activation rules present
- Agent delegation table
- Command shortcuts for common tasks
- Context gate (WHO/WHAT before any skill)

**15**: Most routing present, some gaps

**10**: Basic commands only, no skill routing

**5**: Few commands, agents not referenced

**0**: No workflow or routing info

### 2. Architecture Clarity (20 points)

**20**: Clear system map
- Memory hierarchy documented
- File relationships explained (skills → agents → context → clients)
- Context load order specified
- What goes where (CLAUDE.md vs learnings.md vs corrections.md vs USER.md)

**15**: Good structure, minor gaps

**10**: Basic directory listing only

**5**: Vague or incomplete

**0**: No architecture info

### 3. Non-Obvious Patterns (15 points)

**15**: Gotchas from real incidents
- Known issues with "because" clauses
- Workarounds documented
- Edge cases noted (e.g., Telegram state dir mismatch)
- "Why we do it this way" for unusual patterns

**10**: Some patterns documented

**5**: Minimal, no "because" clauses

**0**: No patterns or gotchas

### 4. Conciseness (15 points)

**15**: Dense, valuable content
- Under 200 lines (ideal)
- No filler or obvious info
- Each line passes the one-line test
- Heavy content extracted to `.claude/rules/`

**10**: Mostly concise, some padding (200-250 lines)

**5**: Verbose in places (250-300 lines)

**0**: Over 300 lines, lots of filler

### 5. Currency (15 points)

**15**: Reflects current state
- File path references valid
- Skills/agents referenced actually exist
- Learnings section current (updated within last 2 weeks)
- No stale "Open Threads" older than 30 days

**10**: Mostly current, minor staleness

**5**: Several outdated references

**0**: Severely outdated

### 6. Actionability (15 points)

**15**: Instructions are executable
- Commands copy-pasteable
- Steps concrete, not vague
- Paths real and verified
- Protocol steps numbered and ordered

**10**: Mostly actionable

**5**: Some vague instructions

**0**: Vague or theoretical

## Grades

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90-100 | Comprehensive, current, actionable |
| B | 70-89 | Good coverage, minor gaps |
| C | 50-69 | Basic info, missing key sections |
| D | 30-49 | Sparse or outdated |
| F | 0-29 | Missing or severely outdated |

**Target: B+ (75+)**

## Assessment Process

1. Read the CLAUDE.md file completely
2. Cross-reference with actual codebase:
   - Check if referenced files/skills exist (`ls skills/<name>/SKILL.md`)
   - Verify path references are valid
   - Check learnings section freshness
3. Score each criterion
4. Calculate total and assign grade
5. List specific issues found
6. Propose concrete improvements (diff format)

## Red Flags (auto-fail items)

- References to deleted skills/agents
- Generic marketing advice not specific to this kit
- Over 300 lines without extraction to `.claude/rules/`
- "TODO" items older than 30 days
- Duplicate content across CLAUDE.md files
- Directory listings (agents find files faster on their own)
- Auto-generated content (ETH Zurich: reduces success rate)

## Output Format

```markdown
## CLAUDE.md Quality Report

### Summary
- Files found: X
- Average score: XX/100
- Files needing update: X

### File: ./CLAUDE.md (Project Root)
**Score: XX/100 (Grade: X)**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Workflows & Routing | X/20 | ... |
| Architecture Clarity | X/20 | ... |
| Non-Obvious Patterns | X/15 | ... |
| Conciseness | X/15 | ... |
| Currency | X/15 | ... |
| Actionability | X/15 | ... |

**Issues:**
- [specific problem]

**Proposed fixes:**
### Update: ./CLAUDE.md
**Why:** [one-line reason]
```diff
+ [the fix]
- [what it replaces]
```
```
