## Graph Links
- **Parent skill:** [[campaign-runner]]
- **Related skills:** [[content-strategy]], [[paid-advertising]], [[social-media]]

# Execution Playbook

Agent routing and publishing strategy for each campaign task type.

---

## Agent Routing Table

| Task Type | Primary Agent | Support Agent | Skill | Publishes Via |
|-----------|--------------|---------------|-------|---------------|
| Social posts | copywriter | — | social-media | Postiz MCP |
| Social images | (direct) | — | image-generation | Postiz upload |
| Ad creative copy | copywriter | attraction-specialist | paid-advertising + copywriting | meta-ads-uploader |
| Ad images | (direct) | — | image-generation | meta-ads-uploader |
| Email sequence | email-wizard | copywriter | email-sequence | HubSpot MCP |
| Landing page copy | copywriter | conversion-optimizer | page-cro | Manual |
| Blog posts | copywriter | seo-specialist | seo-mastery | Manual |
| SEO content | copywriter | seo-specialist | seo-mastery + schema-markup | Manual |
| Market research | researcher | — | marketing-fundamentals | State file |
| Keyword research | seo-specialist | — | seo-mastery | State file |
| Content calendar | planner | — | content-strategy | State file |
| Tracking setup | tracking-specialist | — | analytics-attribution | Config docs |
| Metrics pull | (direct) | — | analytics-attribution | State file |
| Campaign report | project-manager | — | analytics-attribution | State file |
| TikTok slideshows | copywriter | researcher | image-generation + social-media + content-moat | Postiz MCP |

---

## Publishing Channels

### Postiz (Social Scheduling)
- **Status**: MCP integration available
- **Supports**: Multi-platform posting, media upload, scheduling, analytics
- **Platforms**: Twitter/X, LinkedIn, Instagram, Facebook, TikTok, YouTube, Pinterest, Threads, Reddit, Bluesky, Mastodon
- **Flow**: Create content → upload media → schedule post → save post_id to state

### HubSpot (Email)
- **Status**: MCP integration available
- **Supports**: Contact management, email sequences, forms, deals
- **Flow**: Write sequence → create in HubSpot → activate → track metrics

### Meta Ads Uploader (Paid Ads)
- **Status**: Direct API integration
- **Applies to**: Facebook/Instagram ad creatives
- **Flow**: Generate creative bundle → validate → upload media → create creatives → create ads (PAUSED) → Jerel activates in Ads Manager

### Manual (Copy-Paste)
- **Status**: Always available (fallback)
- **Applies to**: Landing pages, blog posts
- **Flow**: Create content as file → Jerel copies to platform → mark as published in state

---

## Phase-Task Mapping

### Planning Phase Tasks
1. **Market research** → researcher agent, marketing-fundamentals skill
2. **Competitor analysis** → researcher agent, competitor-alternatives skill
3. **Keyword research** → seo-specialist agent, seo-mastery skill
4. **Content calendar** → planner agent, content-strategy skill
5. **Campaign brief** → planner agent (uses existing /campaign:brief command)

### Creation Phase Tasks
6. **Landing page copy** → copywriter + page-cro
7. **Email sequence** → email-wizard + email-sequence
8. **Social posts** → copywriter + social-media
9. **Ad creative** → copywriter + paid-advertising + copywriting
10. **Images/media** → image-generation skill (direct)
11. **Blog content** → copywriter + seo-mastery

### Execution Phase Tasks
12. **Social scheduling** → Postiz MCP
13. **Email deployment** → HubSpot MCP
14. **Ad launch** → meta-ads-uploader (bundle → upload → PAUSED ads)
15. **Tracking setup** → tracking-specialist + analytics-attribution
16. **Landing page publish** → Manual (Jerel deploys)

### Optimization Phase Tasks
17. **Metrics pull** → MCP integrations (GA, Postiz, HubSpot, Meta)
18. **Performance report** → project-manager + analytics-attribution
19. **A/B test design** → conversion-optimizer + ab-test-setup
20. **Copy optimization** → copywriter based on data
21. **Retargeting** → email-wizard + attraction-specialist

---

## Task Priority Rules

When multiple tasks are available, prioritize:

1. **Unblocked tasks** — dependencies met, ready to execute
2. **Publishing tasks** — get content live (higher impact than creating more)
3. **Creation tasks** — produce assets for later publishing
4. **Analysis tasks** — pull metrics, generate reports
5. **Planning tasks** — only if campaign scope needs expanding

Within the same priority level, prefer tasks that:
- Have the most downstream dependents (unblock other work)
- Are closest to revenue (bottom-of-funnel first)
- Can be batched (do all social posts at once)

---

## Batch Execution Patterns

### Social Media Batch
Create all social posts for the week in one session:
1. Load content calendar
2. Generate 5-7 posts (copywriter + social-media)
3. Create images if needed (image-generation)
4. Upload media to Postiz
5. Schedule all posts with dates
6. Save all post_ids to state

### Email Sequence Batch
Write full email sequence in one session:
1. Load ICP + offer context
2. Write all emails (email-wizard + email-sequence)
3. Review with brand-voice-guardian
4. Save to assets/emails/
5. Deploy to HubSpot when approved

### TikTok Slideshow Batch
Create full 2-week TikTok Photo Mode slideshow batch:
1. Research trending slideshow formats, sounds, hashtags
2. Load content pillars from project strategy (or define new)
3. Build 2-week calendar (5x/week), each slot: pillar, slide count, hook, hashtags
4. **HITL concept approval** — Jerel reviews calendar grid (5 min)
5. Write slide-by-slide text/copy for each carousel (copywriter + copywriting + content-moat)
6. Generate AI image prompts for all slides (image-generation, carousel slide set templates, 9:16)
7. Write captions + hashtag sets (copywriter + social-media)
8. Batch-generate all slide images (3-10 per post)
9. **HITL batch review** — structured table, approve/edit/cut per row
10. **HITL slideshow production** — Jerel assembles in Canva/CapCut (text overlays, music)
11. Upload final carousels to Postiz (multiple images per post for Photo Mode)
12. Schedule via Postiz `posts:create` with `platforms: ["tiktok"]`, max 5/day
13. Posts go to TikTok drafts — Jerel publishes from TikTok app (adds music)
14. After 7 days: pull analytics, repurpose top 3 to IG carousels, update learnings

### Ad Creative Batch
Create ad variants in one session:
1. Load landing page copy for consistency
2. Write 3-5 headline variants (copywriter + copywriting)
3. Write 3-5 body variants
4. Create image variants (image-generation)
5. Save all to assets/ads/
6. Jerel uploads to ad platform
