---
description: Schedule social content via Postiz
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [project-name] [campaign-slug]
---

## Prerequisites

- Postiz MCP configured (see `skills/integrations/postiz/index.md`)
- Social accounts connected in Postiz
- Content assets created in campaign `assets/` folder

---

## Context Loading

1. Load campaign-runner skill: `skills/campaign-runner/SKILL.md`
2. Load Postiz integration: `skills/integrations/postiz/index.md`
3. Load campaign state

---

## Workflow

### Step 1: Check Postiz Connection

Use `integrations:list` to verify connected platforms.
If not available, show setup instructions from `skills/integrations/postiz/index.md`.

### Step 2: Find Schedulable Content

Scan campaign state for tasks with:
- Status: `done` or `review` (content created)
- Type: social posts, images
- Not yet published (no `post_ids`)

List what's ready to schedule.

### Step 3: Present Content for Approval

For each post:
```markdown
**Post [N]** — [platform(s)]
Scheduled: [date/time]
---
[content preview]
[media: image name if any]
---
```

**HITL Gate:** "Approve these posts for scheduling?"
**Options:**
- **Approve all** — Schedule everything as shown
- **Edit first** — Modify content before scheduling
- **Change dates** — Adjust scheduling times
- **Cancel** — Don't schedule yet

### Step 4: Upload Media (if needed)

For posts with images:
1. Use Postiz `upload` tool to upload each image
2. Get media IDs back
3. Attach to post

### Step 5: Schedule Posts

For each approved post:
1. Call `posts:create` with content, platforms, scheduled date, media
2. Save returned `post_id` to campaign state
3. Update task status to `scheduled`

### Step 6: Confirm

```markdown
Scheduled [N] posts:
  [platform] — [date] — [first 50 chars of content]...
  ...

Post IDs saved to campaign state.
Next: Pull analytics after posts go live with /campaign:metrics
```

---

## Rate Limit Handling

Postiz allows 30 requests/hour. If scheduling many posts:
- Batch uploads first, then schedule posts
- Space calls 2 seconds apart
- If rate limited, save remaining as "ready-to-publish" and note in state
