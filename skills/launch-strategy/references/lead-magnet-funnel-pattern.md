## Graph Links
- **Parent skill:** [[launch-strategy]]
- **Sibling references:** [[launch-playbook]]
- **Related skills:** [[email-sequence]], [[page-cro]], [[form-cro]]

# Lead Magnet Funnel Pattern

Reusable workflow pattern for deploying a lead magnet funnel. Stack-agnostic — adapt to whatever hosting + email automation the project uses.

## Funnel Architecture

```
Content Asset (Notion doc, PDF, guide, checklist)
    ↓
Landing Page (headline, subheadline, email form, CTA)
    ↓
Form Submit → Subscriber API (add to list) + Webhook (trigger email)
    ↓
Delivery Email (thank you + direct link to asset)
    ↓
Access Page (noindex, direct link to asset, newsletter callout)
```

## Landing Page Pattern

1. **Eyebrow badge** — "Free guide", "Free checklist", etc.
2. **Headline** — Benefit-first, specific outcome
3. **Subheadline** — 1-2 sentences expanding on the value
4. **Email form** — Single field (email only) for minimum friction
5. **CTA button** — Action-oriented ("Get the Guide", "Download Free")
6. **Transparency line** — "Join X subscribers. One email per week. Unsubscribe anytime."
7. **Preview section** — Blurred or partial preview of the content to build desire

## Access Page Pattern

- **noindex, nofollow** meta tags (don't index access pages)
- Headline: "Your [resource] is ready"
- Subheadline: "We've emailed you the full guide. Or just open it right now:"
- CTA button linking directly to the asset
- Newsletter callout section below

## Email Delivery Pattern

- Subject: "Your [Title] Is Ready"
- Body: 3 paragraphs max before the CTA button
  1. Thank you + what they got (1 line)
  2. What it covers and why it's useful (1 line)
  3. CTA line ("Open it up and start building:")
- CTA button: left-aligned, links to asset
- Newsletter section below: brief pitch + "You're already on the list"
- Keep it short — the email's job is delivery, not selling

## Routing Configuration

For clean URLs (e.g., `/my-guide` instead of `/lead-magnets/my-guide/index.html`):
- **Vercel:** Add rewrite rules to `vercel.json`
- **Netlify:** Add to `_redirects` file
- **Cloudflare:** Add redirect rules

## Form Submission Flow

```
Form POST → /api/subscribe
  → Add to newsletter list (API call)
  → Trigger email delivery webhook (await, not fire-and-forget)
  → Redirect to /[slug]/access
```

## Key Principles

- Single email field for minimum friction
- CTA must appear above the fold
- Email delivery must be awaited (not fire-and-forget) in serverless environments
- Access page should be noindex
- Asset link in email must match asset link on access page
