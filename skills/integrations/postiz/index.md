# Postiz Integration

> Social media scheduling, publishing, and analytics via self-hosted Postiz

## Overview

Postiz is a self-hosted social media management platform. It handles multi-platform scheduling, media uploads, and analytics. We use it as the primary publishing channel for campaign content.

## Supported Platforms

- Twitter/X
- LinkedIn
- Instagram
- Facebook
- TikTok
- YouTube
- Pinterest
- Threads
- Reddit
- Bluesky
- Mastodon

## Setup

### 1. Self-Host Postiz

Recommended: $5-10/mo VPS (Hetzner or DigitalOcean).

```bash
# On your VPS
git clone https://github.com/gitroomhq/postiz-app.git
cd postiz-app
cp .env.example .env
# Edit .env with your settings
docker compose up -d
```

Full docs: docs.postiz.com/installation/docker-compose

### 2. Connect Social Accounts

In Postiz dashboard:
1. Go to Settings → Integrations
2. Connect each social platform
3. Authorize access

### 3. Get API Key

In Postiz dashboard:
1. Go to Settings → API
2. Generate new API key
3. Copy the key

### 4. Configure MCP in Claude Code

Add to your Claude Code MCP settings:

```json
{
  "mcpServers": {
    "postiz": {
      "command": "npx",
      "args": ["-y", "postiz"],
      "env": {
        "POSTIZ_API_KEY": "<your-api-key>",
        "POSTIZ_API_URL": "http://<your-vps-ip>:4007"
      }
    }
  }
}
```

## MCP Tools

| Tool | Description | Used By |
|------|-------------|---------|
| `posts:create` | Create/schedule posts (multi-platform, with media) | copywriter, social-media skill |
| `posts:list` | List scheduled/published posts | project-manager, campaign-runner |
| `posts:delete` | Remove a post | campaign-runner |
| `upload` | Upload media files | image-generation, copywriter |
| `integrations:list` | Show connected social accounts | campaign-runner (discovery) |
| `analytics:platform` | Platform-level analytics | analytics-attribution |
| `analytics:post` | Per-post analytics | campaign-runner (metrics) |

## Usage Examples

### Schedule a Social Post

```
posts:create({
  content: "Excited to announce our new feature! Here's what it means for you...",
  platforms: ["twitter", "linkedin"],
  scheduledDate: "2026-03-20T10:00:00Z",
  media: ["<media-id-from-upload>"]
})
```

### Upload Media First

```
upload({
  file: "/path/to/image.png",
  type: "image/png"
})
→ Returns: { id: "media-abc123", url: "..." }
```

### List Scheduled Posts

```
posts:list({
  status: "scheduled",
  limit: 20
})
```

### Get Post Analytics

```
analytics:post({
  postId: "post-abc123"
})
→ Returns: { impressions, engagement, clicks, ... }
```

## Platform-Specific Notes

### Twitter/X
- 280 character limit
- Up to 4 images or 1 video
- Thread support via multiple posts

### LinkedIn
- 3000 character limit
- Professional tone recommended
- Document posts (carousels) via PDF upload

### Instagram
- Requires image or video
- Caption up to 2200 characters
- Up to 30 hashtags (recommend 5-10)

### Facebook
- No hard character limit (recommend <500)
- Link previews auto-generated
- Best with eye-catching image

## Rate Limits

- **30 requests/hour** on Postiz API
- Batch operations when possible
- Space out scheduling calls (1-2 sec between)
- Use `posts:list` sparingly (cache results in state.yaml)

## Integration with Campaign Runner

### Publishing Flow
1. Agent creates content → saved to `assets/`
2. Jerel approves content (HITL gate)
3. Media uploaded via `upload` tool
4. Post scheduled via `posts:create`
5. Post ID saved to campaign `state.yaml`
6. Analytics pulled via `analytics:post` during optimization

### State Tracking
```yaml
# In state.yaml task entry
published:
  platform: postiz
  post_ids: ["abc123", "def456"]
  scheduled_dates: ["260320", "260322"]
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Check VPS is running: `docker compose ps` |
| Auth error | Regenerate API key in Postiz dashboard |
| Platform disconnected | Re-authorize in Postiz Settings → Integrations |
| Rate limited | Wait 1 hour, then retry with smaller batch |
| Media upload fails | Check file size (<10MB) and format (PNG, JPG, MP4) |

## Related

- [Crosspost](../crosspost/) — Simpler alternative for multi-platform posting
- [Twitter](../twitter/) — Twitter-specific features
- Campaign Runner skill — `skills/campaign-runner/SKILL.md`
