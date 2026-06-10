---
description: Spawn bounded parallel sub-agents for client or campaign research, with explicit write scopes and synthesis output
version: "0.1.0"
brand: AgentKits Marketing by AityTech
argument-hint: [client-slug] [campaign-slug] [task]
---

## Purpose

Use this when a client/campaign needs parallel research or review before a strategic decision. It is designed for Jake-style client folders and avoids uncontrolled agents by assigning each worker a narrow evidence question and one output file.

## Inputs

- `client-slug` — required, maps to `clients/<client-slug>/`
- `campaign-slug` — optional but preferred, maps to `clients/<client-slug>/campaigns/<campaign-slug>/`
- `task` — optional focus such as `market-awareness`, `asset-audit`, `video-concepts`, `claims-risk`, or `buyer-language`

## Context Loading

Load only the files needed for the task:

- `clients/<client-slug>/context-profile.json`
- `clients/<client-slug>/_brand/offer.md`
- `clients/<client-slug>/_brand/icp.md`
- `clients/<client-slug>/_brand/buyer-profile.md`
- `clients/<client-slug>/_brand/avatars/`
- `clients/<client-slug>/_brand/asset-map.md`
- `clients/<client-slug>/_brand/video-style.md`
- `clients/<client-slug>/_swipe/research/`
- `clients/<client-slug>/campaigns/<campaign-slug>/campaign-brief.md`
- `clients/<client-slug>/campaigns/<campaign-slug>/CONTEXT.md`

## Default Agent Set

Spawn only the agents needed for the task. For a new video campaign, the default set is:

1. **Market Awareness Researcher**
   - Question: what awareness/sophistication level is the buyer likely in, and what proof is needed?
   - Output: `clients/<client>/campaigns/<campaign>/01_research/output/agent-1-market-awareness.md`

2. **Buyer Language Miner**
   - Question: what phrases, anxieties, objections, and desired outcomes should copy and video concepts echo?
   - Output: `clients/<client>/campaigns/<campaign>/01_research/output/agent-2-buyer-language.md`

3. **Existing Asset Auditor**
   - Question: which real/approved assets can be reused as brand, product, avatar, beat-sheet, or render input references?
   - Output: `clients/<client>/campaigns/<campaign>/01_research/output/agent-3-existing-assets.md`

4. **Claims Risk Reviewer**
   - Question: which claims are safe, which require proof, and which should be avoided or softened?
   - Output: `clients/<client>/campaigns/<campaign>/01_research/output/agent-4-claims-risk.md`

5. **Concept Space Mapper**
   - Question: which concept territories are most promising for this campaign, and what input assets would each require?
   - Output: `clients/<client>/campaigns/<campaign>/01_research/output/agent-5-concept-space.md`

## Worker Contract

Every sub-agent prompt must include:

- "You are not alone in the codebase; do not revert or modify unrelated files."
- The exact files/folders it may read.
- The exact output file it may write.
- A requirement to cite local file paths, URLs, or source snippets for every substantive claim.
- A requirement to separate confirmed facts from assumptions and open questions.

## Parent Synthesis

After workers finish, synthesize their findings into:

`clients/<client>/campaigns/<campaign>/01_research/output/research-synthesis.md`

The synthesis should contain:

- Market awareness and sophistication verdict
- Buyer avatar/segment recommendation
- Asset readiness verdict
- Claims/compliance risk list
- Concept shortlist
- Required missing inputs
- Recommended next command or skill
