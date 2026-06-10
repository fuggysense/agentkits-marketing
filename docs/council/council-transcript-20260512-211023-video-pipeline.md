# LLM Council Transcript — Video Pipeline Restructure

**Date:** 2026-05-12 21:10 SGT
**Topic:** Consolidating 12+ video skills, integrating OriSilver techniques, building compounding learning loop
**Anonymization map:** A=Outsider · B=Contrarian · C=First Principles · D=Expansionist · E=Executor

---

## Framed question

Jerel runs `~/Documents/Jerel's brain/jerel's brain/Marketing/`. He has 12+ video-related skills with murky hand-offs (three competing orchestrators, two storyboard tools, four UGC entry points), an external Trigger.dev UGC pipeline that's not callable from skills, zero dedicated video agents, no DP-profile macro, no central learning ledger.

**Proposed restructure (9 changes):**
1. Merge orchestrators → `video-factory` absorbs `video-director`; `higgsfield` skill demoted to backend driver
2. Merge storyboard → `beat-sheet-director` absorbs `ai-filmmaking` as `--director` mode flag
3. Single UGC path → `ugc-creator` → `seedance-director` → Higgsfield CLI or Trigger.dev
4. Stills-plane → motion-plane HITL doctrine codified in `video-factory`
5. Per-client `dp-profile.json` auto-injected (OriSilver default: Alexa 35 + UV anamorphic + Pro-Mist + Vision3 250D)
6. Thin `ugc-pipeline-bridge` skill (Trigger.dev programmatic interface)
7. Per-project `video-ledger.json` + `autoresearch` mutation loop
8. New `video-producer` agent (end-to-end shepherd)
9. OriSilver back-ports as hard rules across seedance-director / ugc-creator / beat-sheet-director

**Council questions A–F** on consolidation safety, orchestrator merge, migration risk, ledger reality, OriSilver split choice, Trigger.dev bridge depth.

---

## Advisor responses

### The Outsider (Response A)

> Wait. Stop. I'm reading this as a normal person and I have questions before I can even answer yours.
>
> **What is a "skill"?** You say twelve "skills." Are these files? Prompts? Apps? Folders?
>
> **The names are a maze.** `video-factory`, `video-director`, `video-producer` (new), `video-director skill` separate from `video-director agent`. Four things with "video" + "director/factory/producer" and I cannot keep them straight reading it once.
>
> **Pick one metaphor and commit.** Kitchen (recipes), film set (director/crew), or factory (assembly line). A 12-year-old should be able to say: "Oh, I tell the [thing] what I want, and it makes a video." That's the test.
>
> **The cinematography preset scares me.** Alexa 35 + anamorphic + Pro-Mist + Vision3 + 20° dutch tilt as the DEFAULT? Every video looks like a moody indie film now? Defaults that override intent are a trap.
>
> **"Learning ledger"** — sounds like theater until you tell me: who reads it, when, and what changes because of it? If the answer is "I'll review it someday," it's a journal, not a system.
>
> **OriSilver** — never heard of him. If his split (stills vs motion) is genuinely how the work flows, copy it. If it's his branding, don't.
>
> **My one ask:** before merging anything, write the 3-sentence "what is this" a stranger would read first.

**CONFIDENCE: 7**

---

### The Contrarian (Response B)

> The "ONE of everything" instinct is the fatal flaw. You're optimizing for a tidy diagram, not for the actual cost of being wrong.
>
> **Question A landmine:** Narrative film direction and ad-frame storyboarding are not the same craft. ARQ + director profiles encode *causality and character arc*; beat-sheet-director encodes *attention curves and product reveals*. A `--director` flag does not make Villeneuve's pacing useful for a 15-second hook. In 6 months you'll have a bloated skill where the director profiles are dead weight on ad work and the ad-retention heuristics are corrupting narrative pacing.
>
> **Orchestrator merge is the real risk.** `video-director` has 14 video types and a working Vertex path. `video-factory` is a router. You're folding a *production system* into a *traffic cop*. Seams will show — at the worst possible time, on a paid client deliverable.
>
> **Question D — the loop is theater as currently described.** `video-ledger.json` + autoresearch mutating `corrections.md` is a feedback system with no ground truth. Without a hard win/loss label, autoresearch will mutate toward whatever pattern got logged most, not what worked. Compounding noise. MVP: kill autoresearch from v1. Manually triage 90 days. THEN automate.
>
> **Question F — bridge skill is a trap.** Trigger.dev pipeline lives outside the repo. Bridge skill = dependency you can't grep, version, or roll back atomically. When Trigger breaks at 2am, your skills break silently. Either pull it in as submodule or leave it explicitly external — don't half-bridge.
>
> **Unnamed 12-month landmine:** OriSilver's defaults become *your* defaults across every client. Every video starts looking the same. DP macro = one preset among 3-4, not the auto-default.

**CONFIDENCE: 8**

---

### The First Principles Thinker (Response C)

> The frame is wrong. "Consolidate 12 skills into N" is an org-chart problem dressed up as architecture. It optimizes for Jerel's mental load picking a skill, not for the machine getting better at making video.
>
> Strip everything. The job-to-be-done: **turn a marketing intent into a finished video that performs, and let every finished video make the next one cheaper, faster, and better.**
>
> Three primitives fall out:
> 1. A **brief** (intent + constraints + DP profile + client context)
> 2. A **generator** (whatever model/pipeline produces the asset)
> 3. A **ledger** (what was made, what worked, what to copy/avoid)
>
> Skills are interchangeable hands. The ledger is the spine. Jerel has 12 hands and no spine — that's why it feels broken. Collapsing to 6 hands without building the spine just gives him a tidier broken thing.
>
> Real questions:
> - Is there a single canonical **brief format** every generator reads? (Today: no.)
> - Is there a single project-scoped **ledger** every generator writes to? (Today: no.)
> - Can a human glance at one file and know what's authoritative? (Today: no.)
>
> If yes to those three, you could have 30 skills and it still feels like one machine.
>
> **Minimum machine:** `brief.json` (input contract) → router (picks generator by content-type, not by skill name) → `video-ledger.json` (output + scoring + learnings). Everything else becomes swappable executor behind that contract.
>
> Consolidation is downstream of contract design. Build the contract first; the skill mergers become obvious (and mostly unnecessary).
>
> **Re D:** ledger isn't theater *if* it's the input to the next brief. MVP = three fields — `what_we_tried`, `what_worked`, `dp_overrides_that_stuck` — auto-prepended to the next brief.

**CONFIDENCE: 8**

---

### The Expansionist (Response D)

> The 10x version: Jerel isn't building a video skill stack. He's building **the world's first compounding visual brand engine** — a system that gets more valuable every time anyone in his roster ships a frame.
>
> **Global ledger > per-project.** Every winning prompt across every client becomes a typed template in a shared pool, tagged by intent (hook, retention beat, product reveal, CTA). New client onboarding: "pick a DP profile, the system suggests the 12 highest-converting prompt skeletons it's ever produced in your vertical." 100x cold-start advantage.
>
> **Per-brand DP profiles = an actual moat.** OriSilver encodes craft. Jerel can encode *signatures*. Fuggy's Media looks like Fuggy's. NeezaNizam looks like NeezaNizam. Clients can't churn — their visual DNA lives in your repo. That's lock-in.
>
> **Agent council is the real unlock.** script-doctor + storyboard-critic + DP + colorist + retention-analyst reviewing every gen *before* render burn = fewer turds, less credit spend, every rejection trains the ledger.
>
> **Offer hiding in plain sight:** "Branded Video Engine as a Service." $5K setup + $2K/mo (10 production-ready videos against their encoded brand). Higgsfield API drops, you're already the workflow layer on top.
>
> **Don't merge the orchestrators yet.** Build the ledger first. Two orchestrators feeding one ledger = twice the training signal. Merge after 100 ships of data tells you which patterns dominate.
>
> The video stack isn't infrastructure. It's a category creation move.

**CONFIDENCE: 7**

---

### The Executor (Response E)

> Stop. You have 9 changes and a client backlog. Pick ONE that unblocks shipping.
>
> **Week 1 (ship only):** Do #1 (orchestrator merge) and #4 (stills→motion HITL doctrine). The orchestrator is the front door — fix it once, every downstream skill inherits routing.
>
> **Week-1 sequence:**
> - Mon: Add `--engine={sora|kling|veo|seedance}` flag to `video-factory`. Mark `video-director` deprecated in frontmatter (don't delete). Update `routing-table.md`.
> - Tue: Codify stills→motion HITL gate inside `video-factory/SKILL.md`. One file edit.
> - Wed–Fri: **Run one real client video end-to-end on the new stack.** This is the baseline. No baseline = no learning loop.
>
> **DEFER (until baseline exists):**
> - #5 `dp-profile.json` — premature; you don't know which params matter yet
> - #6 `ugc-pipeline-bridge` — wrapper for a thing you've run 3 times; CLI is fine
> - #7 ledger + autoresearch — **worthless without 5+ baseline runs.** Theater until then.
> - #8 `video-producer` agent — promotion ceremony, zero new capability
> - #9 OriSilver back-ports — do as inline edits when you hit relevant skill, not a sweep
>
> **4-week plan:**
> - W1: Orchestrator merge + HITL doctrine + 1 real video shipped
> - W2: Beat-sheet absorbs ai-filmmaking + UGC path documented + 2 more videos
> - W3: OriSilver rules inlined into the 3 skills that *actually fired* during W1–W2
> - W4: NOW start ledger — you have 5 runs of real data to learn from
>
> **Brutal truth:** the ledger loop is the sexiest item and the most useless one on day 0. Build the runway before the autopilot.

**CONFIDENCE: 9**

---

## Peer reviews (5 reviewers, anonymized inputs)

### Reviewer 1
1. **Strongest: E.** Only one that converts the mess into a dated sequence with defensible "ship a baseline first" logic. C is conceptually sharpest but E is what Jerel can execute Monday.
2. **Biggest blind spot: D.** Productizing "Branded Video Engine as a Service" before the internal stack ships one clean video — exact trap CLAUDE.md warns against. Moat is imagined; prompt skeletons are trivially copyable.
3. **All five missed:** (a) **Cost economics** — nobody priced a single end-to-end run; wrong default engine could 5x per-video cost. (b) **Ground-truth signal is upstream of the ledger** — client approval is lagging and noisy; no instrumentation tying prompts to Meta ad results. (c) **Existing learnings infra** — repo already has `corrections.md` per skill, `learnings/session-state.md`, global `autoresearch`. Adding parallel ledger = drift.

### Reviewer 2
1. **Strongest: E.** Only response accounting for execution reality (client backlog vs 9 competing changes).
2. **Biggest blind spot: D.** "$5K + $2K/mo" before a single repeatable video. Also: "global ledger > per-project" contradicts the per-brand DP moat — schema doesn't separate them.
3. **All five missed:** Per-video **cost and latency budget** — agent council reviewing every gen could 5x cost. **Who owns the taste verdict** when ledger says "worked" but Jerel's gut says no — 80/20 HITL should govern ledger writes, not just generation approvals.

### Reviewer 3
1. **Strongest: E.** Highest confidence (9), only response that respects sequencing under constraint. Names ledger as "sexiest, most useless day 0."
2. **Biggest blind spot: D.** Selling the brochure for a factory that doesn't exist. "2 orchestrators → 1 ledger = 2x signal" false — divergent schemas pollute the ledger.
3. **All five missed:** **Ground-truth signal definition** (B gestured, dropped it). Also: **rollback cost** to live campaigns mid-merge. Week 1 should fence off in-flight client deliverables.

### Reviewer 4
1. **Strongest: E.** Only one with falsifiable week-by-week sequence and a ship gate.
2. **Biggest blind spot: D.** Premature productization. Dodges A's naming maze and C's JTBD reframe.
3. **All five missed:** **Cost per finished video** — no unit economics named. Architecture decisions without unit economics are taste arguments in system-design costume.

### Reviewer 5
1. **Strongest: E.** Only falsifiable plan with a ship gate. B's diagnosis sharper but E's plan executes Monday.
2. **Biggest blind spot: D.** Treats a half-built internal tool as category-creation play.
3. **All five missed:** (a) **The human in the loop** — none asked what Jerel actually does between brief and final cut. (b) **Cost per finished video.** (c) **Failure-mode catalog** — prompt drift, identity-lock failures, audio sync, revision loops.
> **Synthesis:** Run E's week-1, but before week-2 spend 30 minutes on C's `brief.json` contract so the 5 real runs feed a usable schema.

---

## Chairman synthesis

### Where the council agrees

1. **E's sequencing is correct.** 4 of 5 reviewers picked E as strongest. Operating principle: ship one real client video on a minimally-merged stack before designing any ledger, autoresearch loop, agent council, or productized offer. Day-0 ledger is theater.
2. **D's productization is premature.** 5 of 5 reviewers picked D as biggest blind spot. Selling "Branded Video Engine as a Service" before one repeatable internal delivery violates Jerel's own CLAUDE.md §14 (only automate proven manual processes meeting 10x bar).
3. **The ledger needs a ground-truth signal before it can learn anything.** Without a hard win/loss label, autoresearch will compound noise. Kill autoresearch from v1. Manual weekly triage for 60–90 days.
4. **OriSilver DP macro = one preset, not the default.** Auto-injecting Alexa 35 + UV anamorphic + Pro-Mist + Vision3 250D into every prompt would homogenize every client. Codify as one of 3–4 named presets.

### Where the council clashes

**Merge now vs contract-first vs ship-first.** B says don't merge (real craft distinctions). C says stop merging until brief.json + ledger.json contracts exist. D says don't merge (2 orchestrators = 2x signal). E says merge orchestrators in Week 1 because the orchestrator is the front door.

**Resolution (Reviewer 5):** Execute E's Week 1. Slip in C's contract design (30 min) before Week 2 so 5 baseline videos feed a usable schema instead of a journal. B's narrative-vs-ad collapse veto stands — keep `ai-filmmaking` and `beat-sheet-director` separate until at least one of each has shipped.

**Bridge skill vs full integration for Trigger.dev.** B: half-bridge is a trap; commit fully or stay manual. E: don't bridge at all yet, CLI call is fine for low volume. E wins on volume.

### Blind spots only the peer-review caught

1. **No unit economics named anywhere.** Nobody priced a single end-to-end run. Sora 2 Pro, Kling, Seedance, Vertex, Higgsfield credits, operator hours — wildly different cost profiles. Wrong default engine could 5x per-video cost silently.
2. **Ground-truth signal is upstream of the ledger.** "What makes a video good?" must be answered *before* the ledger schema is designed. Candidates: client approval (lagging), render quality (operator taste), Meta CTR/CPA (2-4 week lag, requires instrumentation), or pure operator-taste verdict.
3. **Existing learnings infrastructure may collide with the new ledger.** Per-skill `corrections.md`, global `learnings/session-state.md`, `autoresearch` already exist. Adding parallel `video-ledger.json` = two competing memories that drift apart.
4. **Live campaign protection.** Skills are wired into `routing-table.md`, `skill-graph.json`, client `corrections.md`. Nobody costed breakage to in-flight client deliverables mid-merge.
5. **Operator taste-authority rule.** When ledger says "worked" but Jerel's gut says no — who wins? 80/20 HITL should govern ledger *writes* not just approvals.
6. **Failure-mode catalog missing.** Where does the pipeline currently break? Prompt drift, identity-lock failures, audio sync, revision loops? Ledger needs failure-mode field per gen, not just good/bad.

### The recommendation

**Run E's 4-week plan with three surgical inserts:**

**Week 0 (60 minutes total — this weekend):**
- Write the **3-sentence "what is this"** document. Commit to ONE metaphor (recommend: **studio**). Rename `video-factory` → keep; `video-director` skill → deprecate; `video-producer` (agent) → defer or rename `studio-producer`.
- Define ground-truth signal in one sentence. Recommended W1 default: *"A video is good if Jerel approves it on first review."* Upgrade to Meta CTR/CPA later when instrumentation exists.
- Fence off in-flight client work — list every active video, freeze touched skills until W2.

**Week 1 (execute E exactly):**
- Mon: Orchestrator merge. `video-factory` gets `--engine={sora|kling|veo|seedance}`. Deprecate `video-director` skill in frontmatter; update `routing-table.md`; rebuild `link-skills.py`.
- Tue: Codify stills → motion HITL doctrine inside `video-factory/SKILL.md`.
- Wed–Fri: Ship one real client video end-to-end on the new stack. Log to `docs/video-runs/run-001.md`: brief + engine + prompts + outputs + cost + time + Jerel verdict + failure modes.

**Week 1.5 (30-min C insert — before Week 2):**
- Extract from `run-001.md` the fields that mattered. Draft `clients/<project>/video-brief.schema.json` and `video-ledger.schema.json` from actual usage. Schema follows behavior.
- Audit: does the proposed ledger duplicate `corrections.md` / `learnings/session-state.md` / `autoresearch`? If yes, fold ledger into existing infra; don't add a fourth memory.

**Week 2:**
- Beat-sheet/ai-filmmaking — **don't merge** (B veto stands). Document boundary: `ai-filmmaking` = narrative/brand films; `beat-sheet-director` = ad-frame storyboards. Add routing rule that picks by intent.
- UGC path consolidation — documentation only, no code change.
- Ship 2 more videos.

**Week 3:**
- Inline OriSilver back-ports **only into skills that actually fired** in W1–W2. DP profile = one preset among 3–4 (B correction), not auto-default.
- Ship 2 more videos.

**Week 4:**
- Build the ledger. Schema already drafted from W1.5. 5 real runs to seed. Manual triage weekly. **No autoresearch yet.**
- If Trigger.dev pipeline ran any of the 5: decide bridge by actual call frequency. If 0: leave island-mode.

**Month 3+ (defer until 20 ship-runs prove the stack):**
- D's productization
- D's per-brand DP-as-moat
- Pre-render agent council
- Global cross-client ledger pool

### The one thing to do first

**Write the 3-sentence "what is this" document. Today. Before any code change.**

If you cannot describe the video pipeline to a stranger in 3 sentences using ONE metaphor, the merge will not fix it — it will rename it. Outsider's diagnosis is the cheapest, highest-leverage move.

Suggested draft to react to:

> **The video studio.** Tell the studio what you want (the brief). The studio picks the right crew and gear (engine + DP profile + skills), shoots it (generates), and shows you takes for approval (HITL). Every shipped video teaches the studio what worked for this client, so the next one starts smarter.

If that sentence lands, the rest of the plan executes itself. If it doesn't, fix it before Monday.
