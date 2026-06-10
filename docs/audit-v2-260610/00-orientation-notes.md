# Phase 0 — Orientation Notes (260610)

## Corpus access (Phase -1 record)
- FERRES_REPO = `~/corpora/sean-ferres` (cloned 2026-06-10 from ops-commits/sean-ferres, 269MB, gh account fuggysense)
- qmd 2.5.3 installed via bun (global). Collections: ferres-talks (transcripts/**/*.md), ferres-docs (text/**/*.txt), ferres-visuals (text/**/*.md). 1,192 chunks / 158 docs embedded.
- Smoke tests pass on all 3 (BM25 search). Semantic `qmd query` needs a 1.28GB expansion model (downloading; search works without it). Known wart: node-llama-cpp Metal compile error → CPU fallback.
- videos/ + swipe .mp4s intentionally absent. Corpus is READ-ONLY.

## What This Machine Is (draft)
Multi-client direct-response marketing factory in a git repo inside Jerel's Obsidian vault.
Flow: client onboarding (interview/research) → `clients/<slug>/` ICM workspace (_brand = L3 factory: offer, buyer-profile, voice) → avatar/micro-persona research → campaign workspaces under `campaigns/` → angle generation (big-angle-spotter, hardened gate variant) → headlines/copy (headline-bank, copywriting-os) → image prompts (ad-concept-engine / gpt-image-2) → render (scripts/ad-images/render.py → Azure GPT-Image pool) → Google Sheet tracking (sheets-provisioner/updater via gws) → Meta upload (meta CLI / meta-ads-uploader). Video sibling pipeline: vid-director AG0/AG1/AG2 + video-concept-lab → Higgsfield/Seedance.
~74 project skills + 58 global, ~190 slash commands, agents/ roster, .claude/rules routing layer.

## Key Phase 0 facts
1. **Structure mismatch vs prompt:** no root `_handoffs/`, `_shared-knowledge/`, `_config/`, or root CONTEXT.md. Handoffs scattered: `docs/handoffs/`, `docs/handoff/`, `clients/neezanizam/SESSION-HANDOFF-*.md`, takekine `_audit/session-handoff-*`. `_config/` exists per-client only. `clients/_smoketest/` does not exist (to be created). `_shared-knowledge/ferres/` will be NEW at repo root.
2. **ICM validator scoreboard (7 rules):**
   - harmony-wellness 7/7 PASS; takekine 6/7 (R5 dup rules); michelle-koh 6/7 (R3); neezanizam 5/7 (R1 size, R6 broken pointers); hazecraft 5/7 (R2,R3)
   - PARTIAL: _template 3/7 (R1,R3,R4,R6!), eugene-chieng 3/7 (R1 CLAUDE.md 197 lines, R3, R4, R6 many broken pointers), 1up-sales-ai/aura/fuggysmedia/propwise-sg/stackworks 4/7 (R1,R2,R3)
   - **The factory template itself fails 4/7** — non-compliance is stamped out at source.
   - Eugene broken pointers: CLAUDE.md+CONTEXT.md reference `_inputs/input-manifest.json`, `_strategy/creative-diversity-map.json`, `_ag1-options/*` that don't exist.
3. **Course corpus = 25 lectures** (prompt said 23; BONUS #1 Statics Playbook (#24) + BONUS #3 Swipe Vault (#25) captured 2026-06-10). 11 video transcripts ~163.5k words, 18 docs ~38.5k words. Swipe vault: 49 statics with Opus-vision descriptions + 33 videos with VO transcripts (82 creatives; INDEX header says 51+32 sheet rows).
4. **render.py --from-tracker confirmed present** (scripts/ad-images/render.py:106-148, README:22 cites neezanizam dct-tracker.json). Drift/bypass claim to verify in Phase 2.
5. ICM SKILL.md citation: "Van Clief & McDermott, *In-Context Modeling for Agentic Software* (arXiv:2603.16021v2)" — prompt says actual title is "Interpretable Context Methodology: Folder Structure as Agentic Architecture" → M4 fix candidate.

## What The Course Covers (from lecture map alone)
Sean Ferres' "AI Ads Lab" teaches freelancers/agency owners to produce winning Meta ads with AI end-to-end: opportunity framing (Pt 1), anatomy of a winning ad (Pt 2, 56min), the creation process incl. research and angles (Pt 3, 71min), getting clients/paid — outreach, $300 challenge offer, contracts, objections, CRM (Pt 4 + docs #11-15), a full live end-to-end AI ad creation demo (Pt 5, 105min), media buying/testing (#8), statics production at volume (#24), plus a curated 82-ad swipe vault (#25), master prompt list (#18), tools list (#19), sales trainings (#10, 3h49m), and ad-critique calls (#22 Roast My Ads, #9 Q&A) that reveal his quality bar in practice.

## Preliminary Phase-3 lecture clustering (refine after Phase 1)
- C1 Foundations & winning-ad anatomy: #2, #3 (+#1, #20 small)
- C2 Research flow (own cluster, runnable stage map): research segments of #4, #6, #18 prompts
- C3 Creation: angles/hooks/copy: #4, #16, #18
- C4 End-to-end SOP & quality bar: #6, #17, (+#22, #9 critique calls)
- C5 Statics playbook: #24
- C6 Media buying / testing & scaling: #8
- C7 Client acquisition & business ops (adjacent): #5, #10, #11, #12, #13, #14, #15, #7, #21, #23
- C8 Swipe vault pattern library: #25 + text/swipe_vault/*
- C9 Tools & meta: #19 (+#1, #20)

## Repo top-level
_swipe, active, agents, assets, bin, brain, build, clients(13 incl _template/_template.old/_archive), commands, context, credentials(!), docs, exports, installers, learnings, node_modules, packages, plans, plugins, propwise-sg(root-level dup of client?), research, scratch, scripts, skills, swipe-files, training, voice, whop-dl-extension, youtube-thumbnails, .claude(rules/workflows/references/skills/hooks/worktrees)
- Oddities to check in audit: `credentials/` dir at root; `propwise-sg/` at root AND in clients/; `_swipe` vs `swipe-files`; `.claude/worktrees/` holding stale repo copies (exclude from greps).
