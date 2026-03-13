---
description: Interactive guide — describe what you want and get command suggestions
version: "1.0.0"
brand: AgentKits Marketing by AityTech
argument-hint: [what you want to do]
---

## How This Works

This is an interactive guide. The user describes what they want to achieve (in plain language), and you suggest the best commands, agents, and workflow to get there.

---

## Workflow

### Step 1: Understand the Goal

If the user provided an argument (e.g., `/help:guide I want more signups`), use that.

Otherwise, ask:

**Question:** "What are you trying to achieve?"
**Header:** "Goal"
**MultiSelect:** false

**Options:**
- **Create content** — Write copy, blog posts, emails, social posts, ads
- **Launch something** — Product launch, feature release, campaign kickoff
- **Get more traffic** — SEO, social media, paid ads, content distribution
- **Convert more visitors** — Optimize pages, forms, popups, signup flows
- **Nurture & retain** — Email sequences, engagement, reduce churn
- **Analyze & report** — Pull metrics, generate reports, audit performance
- **Plan & strategize** — Campaign planning, content calendars, brainstorming
- **Manage brand** — Voice guidelines, brand book, consistency review
- **Something else** — I'll describe it

---

### Step 2: Map Goal to Commands

Based on the user's goal, suggest 1-3 commands with brief explanations of what each does and when to use which one.

Use this mapping:

#### Create Content
| What specifically? | Command | Notes |
|-------------------|---------|-------|
| Blog post | `/content:blog` | SEO-optimized |
| Social posts | `/content:social` | Platform-specific |
| Email copy | `/content:email` | With sequences |
| Landing page | `/content:landing` | Conversion-focused |
| Ad copy | `/content:ads` | Platform-specific with char limits |
| Quick draft | `/content:fast` | Speed over perfection |
| Polish quality | `/content:good` | Quality over speed |
| Edit existing | `/content:editing` | Improve what you have |
| Improve conversions | `/content:cro` | CRO-focused rewrite |

#### Launch Something
| What specifically? | Command | Notes |
|-------------------|---------|-------|
| Full launch plan | `/growth:launch` | Strategy + timeline |
| Campaign plan | `/campaign:plan` | Broader campaign scope |
| New campaign from template | `/campaign:new` | State-tracked execution |
| Creative brief | `/campaign:brief` | For handoff/alignment |

#### Get More Traffic
| What specifically? | Command | Notes |
|-------------------|---------|-------|
| Keyword research | `/seo:keywords` | Find opportunities |
| SEO audit | `/seo:audit` | Fix technical issues |
| Competitor SEO | `/seo:competitor` | Steal their playbook |
| Pages at scale | `/seo:programmatic` | Template-based SEO |
| Schema markup | `/seo:schema` | Rich snippets |
| Social strategy | `/social:engage` | Organic social |
| Viral content | `/social:viral` | Shareability focus |
| Paid ads | `/content:ads` + `/audit:paid-media` | Create + optimize |

#### Convert More Visitors
| What specifically? | Command | Notes |
|-------------------|---------|-------|
| Page optimization | `/cro:page` | Homepage, landing, pricing |
| Form optimization | `/cro:form` | Lead capture forms |
| Popup optimization | `/cro:popup` | Exit intent, modals |
| Signup flow | `/cro:signup` | Registration UX |
| Onboarding | `/cro:onboarding` | Post-signup activation |
| Paywall/upgrade | `/cro:paywall` | Freemium conversion |
| A/B test plan | `/test:ab-setup` | Design experiments |

#### Nurture & Retain
| What specifically? | Command | Notes |
|-------------------|---------|-------|
| Welcome emails | `/sequence:welcome` | New subscriber/user |
| Nurture sequence | `/sequence:nurture` | Lead warming |
| Win-back emails | `/sequence:re-engage` | Churning users |
| Full campaign | `/campaign:new` (retention template) | State-tracked |

#### Analyze & Report
| What specifically? | Command | Notes |
|-------------------|---------|-------|
| Campaign metrics | `/campaign:metrics` | Pull from MCPs |
| Campaign report | `/campaign:report` | Performance summary |
| ROI calculation | `/analytics:roi` | Return on investment |
| Funnel analysis | `/analytics:funnel` | Drop-off points |
| Weekly report | `/report:weekly` | Recurring summary |
| Monthly report | `/report:monthly` | Comprehensive review |
| Paid media audit | `/audit:paid-media` | 200+ checkpoints |
| Full marketing audit | `/audit:full` | Everything |

#### Plan & Strategize
| What specifically? | Command | Notes |
|-------------------|---------|-------|
| Campaign plan | `/campaign:plan` | Full campaign strategy |
| Content calendar | `/campaign:calendar` | What to publish when |
| Brainstorm ideas | `/brainstorm` | Creative concepts |
| Marketing ideas | `/marketing:ideas` | 140+ proven tactics |
| Psychology angles | `/marketing:psychology` | 70+ mental models |
| Pricing strategy | `/pricing:strategy` | Packaging + monetization |
| Referral program | `/growth:referral` | Word-of-mouth growth |
| Free tool idea | `/growth:free-tool` | Engineering-as-marketing |

#### Manage Brand
| What specifically? | Command | Notes |
|-------------------|---------|-------|
| Voice guidelines | `/brand:voice` | Define how you sound |
| Brand book | `/brand:book` | Comprehensive guide |
| Brand assets | `/brand:assets` | Manage visual identity |

#### Campaign Execution
| What specifically? | Command | Notes |
|-------------------|---------|-------|
| Start new campaign | `/campaign:new` | From template with state tracking |
| Check progress | `/campaign:status` | Dashboard view |
| Do next tasks | `/campaign:next` | Execute priority actions |
| Schedule posts | `/campaign:schedule` | Publish via Postiz |

---

### Step 3: Suggest a Starting Point

Based on the conversation, recommend ONE command to start with and explain why. If the user needs to set up a project first (context gate), mention that.

Example:
> "Start with `/campaign:new` — it'll create a state-tracked campaign with pre-built tasks. You can then use `/campaign:next` each session to execute tasks one by one."

### Step 4: Offer to Run It

**Question:** "Want me to run [suggested command] now?"

---

## If User Says "Something Else"

Ask them to describe what they want in plain language. Match their description against:
1. The command mapping above
2. Available skills (run `python3 .claude/scripts/list_commands.py --search "<keywords>"`)
3. Available agents (check CLAUDE.md routing table)

If no existing command fits, suggest:
- A combination of commands that achieves the goal
- Or flag it as a potential new command to build
