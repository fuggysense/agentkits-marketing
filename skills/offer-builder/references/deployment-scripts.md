## Graph Links
- **Parent skill:** [[offer-builder]]
- **Sibling references:** [[audit-checklists]], [[carrier-trust-signals]], [[identity-frameworks]], [[offer-document-template]], [[raw-pour-questions]], [[viability-scoring]]
- **Related skills:** [[pricing-strategy]], [[copywriting]], [[launch-strategy]]

# Deployment Scripts

## Purpose
Steps 13-15 of the offer-building process. After the offer passes audit, these scripts turn it into action — outreach messages, a 30-day launch plan, and a go-live checklist.

---

## Step 13: Outreach Scripts

Generate 3 outreach templates from the offer document. Each uses a different angle.

### Template 1: Direct Offer (Cold)
For cold outreach — email, DM, LinkedIn message.

```
Subject: [11PM Thought as a question]

Hey [name],

[1 sentence acknowledging their situation — use Raw Pour Q2 language]

I built [mechanism name] specifically for [their market segment]. In short: [one-line description].

[1 proof point — specific result with numbers]

[CTA — low commitment: "Worth a quick look?" or "Want me to send the details?"]

[Your name]
```

### Template 2: Value-First (Warm)
For warm leads — people who've engaged with content, downloaded something, or shown interest.

```
Subject: [Specific result] — how [customer name] did it

Hey [name],

You [engagement trigger — downloaded X, attended Y, commented on Z].

Wanted to share something relevant: [1 case study in 2-3 sentences with numbers].

The method behind it is [mechanism name] — [1 sentence explanation].

[CTA — medium commitment: "Want me to walk you through how it'd work for [their company]?"]

[Your name]
```

### Template 3: Micro Offer (Entry)
For introducing the micro offer as a low-risk entry point.

```
Subject: Quick win for [their pain point]

Hey [name],

I have a [micro offer name] that [micro offer promise] in [micro offer timeline].

It's [micro offer price] and you'll walk away with [specific deliverable].

[1 sentence on why — connects to bigger transformation without overselling]

[CTA — direct: "Want in?" or "Grab a spot here: [link]"]

[Your name]
```

### Customization Notes
- Pull exact language from Raw Pour answers (Q2 for pain, Q4 for transformation, Q5 for proof)
- Match tone to brand voice files if loaded
- Adjust formality based on channel (LinkedIn = professional, email = direct, DM = casual)

---

## Step 14: 30-Day Launch Plan

A week-by-week plan to take the offer to market.

### Week 1: Foundation
| Day | Action | Details |
|-----|--------|---------|
| 1-2 | **Publish offer page** | Landing page or sales page with full offer document content |
| 3 | **Set up tracking** | UTMs, conversion pixel, analytics events |
| 4-5 | **Create demonstration asset** | Free resource that proves your expertise (guide, audit, tool) |
| 6-7 | **Seed social proof** | Reach out to past clients for testimonials, screenshot results |

### Week 2: Warm Launch
| Day | Action | Details |
|-----|--------|---------|
| 8-9 | **Email existing list** | Value-first template to warm contacts |
| 10-11 | **Direct outreach** | 20 personalized messages using outreach templates |
| 12 | **Social content** | Share the demonstration asset publicly |
| 13-14 | **Collect feedback** | Ask first responders what's confusing, what resonates |

### Week 3: Expand
| Day | Action | Details |
|-----|--------|---------|
| 15-16 | **Refine based on feedback** | Update offer page, scripts, proof elements |
| 17-18 | **Content push** | 3-5 pieces addressing common objections from Audit Pass 3 |
| 19-20 | **Micro offer campaign** | Launch micro offer to new audience as entry point |
| 21 | **Review metrics** | Conversion rate, response rate, objection patterns |

### Week 4: Scale Decision
| Day | Action | Details |
|-----|--------|---------|
| 22-23 | **Double down or pivot** | If converting > 2%: increase volume. If < 1%: diagnose and fix |
| 24-25 | **Add paid distribution** | If organic is validating, test small paid budget |
| 26-27 | **Build nurture sequence** | Email sequence for non-buyers (address remaining objections) |
| 28-30 | **Month 1 retrospective** | Score results, update offer document, plan Month 2 |

---

## Step 15: Go-Live Checklist

Final checklist before the offer goes live. All items must be confirmed.

### Offer Readiness
- [ ] Offer document complete (all 8 sections filled or intentionally marked [TBD])
- [ ] Vending Machine Score ≥ 7.0
- [ ] All 3 audit passes completed
- [ ] Price confirmed and published
- [ ] Guarantee terms finalized

### Assets Ready
- [ ] Landing page / sales page live
- [ ] Outreach templates customized and ready
- [ ] Demonstration asset published (free content / tool / audit)
- [ ] At least 1 case study or testimonial ready
- [ ] Payment processing set up (if applicable)

### Tracking Ready
- [ ] UTM parameters defined for all channels
- [ ] Conversion tracking installed
- [ ] Lead capture form working
- [ ] CRM / spreadsheet ready to receive leads

### Communication Ready
- [ ] Outreach list built (minimum 20 contacts for warm launch)
- [ ] Social content scheduled for launch week
- [ ] Email sequence drafted for non-converters
- [ ] Response templates ready for common questions

### Go / No-Go
```
## Go-Live Decision

- [ ] All "Offer Readiness" items confirmed
- [ ] At least 3/4 "Assets Ready" items confirmed
- [ ] At least 2/4 "Tracking Ready" items confirmed
- [ ] At least 2/4 "Communication Ready" items confirmed

Decision: [GO / HOLD — with specific blockers]
Launch date: [date]
```

---

## Integration with Campaign Runner

After the go-live checklist passes, the natural next step is `/campaign:new <project> lead-gen` or `/campaign:new <project> product-launch` to execute the 30-day plan using the campaign-runner skill's state tracking and agent routing.
