# HazeCraft Operations Dashboard — Claude.design Prompt

Paste this into Claude artifacts, v0.dev, or Lovable to generate the frontend.

---

## PROMPT

Build me a single-page operations dashboard for **HazeCraft**, a 2-partner marketing agency for Singapore property agents.

**Stack:** Next.js 15 (App Router), TypeScript, Tailwind CSS, shadcn/ui, lucide-react icons, framer-motion for subtle transitions. Single page, no routing. Mock all data inline as TypeScript constants — I'll wire real data later.

**Aesthetic:** Atmospheric and intentional. The name "HazeCraft" suggests fog + handcraft — soft gradients, generous whitespace, monospace for IDs/timestamps, sans-serif (Inter or Geist) for everything else. Dark mode default with a warm off-white light mode toggle. NOT a typical SaaS dashboard — closer to Linear or Raycast in restraint.

**My problem:** I'm a visual person and I can't keep track of (a) which clients need what, (b) which Claude Code sessions are running where, (c) what I should be doing right now. I'm overwhelmed by folder structures.

---

### Layout — 4 zones, vertically stacked, each collapsible

**Zone 1 — Now bar (top, sticky)**
A single horizontal strip showing what needs my attention TODAY. 3-5 cards max, each with: icon (lucide), one-line description, source (client + service line), action button. Examples: "Nisa — DCT wave 3 metrics due in 2 hours [Open sheet]", "New client onboarding incomplete [Resume]". Red dot for overdue, amber for due today. Empty state: "Nothing on fire. Go make something."

**Zone 2 — Client roster (grid, 3 columns on desktop, 1 on mobile)**
One card per client. Each card shows:
- Client name + logo placeholder (rounded square, 48px)
- Status pill: Active / Paused / Onboarding / Archived
- Two service-line rows with mini-icons:
  - 📊 Paid Ads — status (Live / Paused / Building / None) + last metric (e.g. "CPL $14.20")
  - 💬 WhatsApp Bot — status + last metric (e.g. "47 leads handled this week")
- Owner avatar (me or partner)
- Health bar at bottom (green/amber/red, single bar, no chart)
- Click expands inline to show: latest 3 events across both service lines, links to client folder, link to identity files

Mock 3 clients: Nisa & Nizam (active, both services), [New Client TBD] (onboarding, paid ads only), HazeCraft Self (active, internal — agency marketing itself).

**Zone 3 — Active Claude Code sessions (table)**
Columns: Session ID (mono, last 6 chars), Agent/Skill running, Client context, Started (relative time), Tokens used (progress bar), Status (Running / Awaiting input / Done / Errored), Action (Open / Kill).

Mock 4 rows: 1 running (`big-angle-spotter` for Nisa, 47% tokens), 1 awaiting HITL ("Approve avatar set"), 1 done (`source-of-truth` finished 12m ago), 1 errored (red).

**Zone 4 — Sanity panel (2-column split, footer)**
Left: "What I'm avoiding" — 3 markdown checkboxes for tasks I keep punting (read from a local txt, mocked). Right: "This week's wins" — 3 bullet auto-pulled from learnings (mocked, e.g. "Big-angle-spotter found 3 new angles for property niche").

---

### Interactions
- Cmd+K opens a search palette (shadcn Command component) — search clients, sessions, recent files
- Sidebar toggle (left edge) hidden by default, slides in with: Clients / Sessions / Settings / Logout
- Every "Open folder" link uses `vscode://file/...` URL scheme so clicking opens the folder in my editor
- Toast notifications for session status changes (framer-motion fade)

### Visual rules
- No skeumorphism, no shadows beyond shadcn defaults
- Animations under 200ms, easing: ease-out
- Color palette: zinc-950 (bg), zinc-100 (text), warm haze gradient accent (orange-300 → rose-400) used SPARINGLY — only for the "Now bar" highlights and the active session pulse
- Typography: Geist Sans for UI, Geist Mono for IDs/times/numbers
- All icons from lucide-react, 16px in dense areas, 20px in cards, 24px in zone headers

### Data shape (use this exact TypeScript)

```ts
type Client = {
  slug: string;
  name: string;
  status: 'active' | 'paused' | 'onboarding' | 'archived';
  owner: 'jerel' | 'partner' | 'shared';
  services: {
    paidAds?: { status: 'live'|'paused'|'building'|'none'; lastMetric?: string };
    whatsapp?: { status: 'live'|'paused'|'building'|'none'; lastMetric?: string };
  };
  health: 'green' | 'amber' | 'red';
};

type Session = {
  id: string;
  skill: string;
  clientSlug: string;
  startedAt: string;
  tokensUsed: number;
  tokensMax: number;
  status: 'running' | 'awaiting_input' | 'done' | 'errored';
};

type AttentionItem = {
  icon: string; // lucide name
  message: string;
  clientSlug?: string;
  serviceLine?: 'paid-ads' | 'whatsapp';
  urgency: 'overdue' | 'today' | 'this-week';
  actionLabel: string;
};
```

Make it feel like a tool I'd want to keep open in a second monitor. Pleasant, calm, and information-dense without being noisy. Restraint over decoration.

---

### Output
Single file: `app/page.tsx` with everything inline. shadcn components imported assuming they're already installed. Mock data at the top of the file. No comments explaining obvious code.
