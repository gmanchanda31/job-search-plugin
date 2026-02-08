---
name: memory-management
description: "Two-tier memory system for the job search co-pilot. Maintains CLAUDE.md as a hot cache for instant context (active targets, key contacts, preferences) and memory/ as deep storage for company research, contact profiles, application materials, and analytics. Decodes company names, recruiter names, role shorthand, and job search jargon so Claude understands context like 'check on the Stripe PM thing' without needing full details."
---

# Job Search Memory Management

Persistent memory that makes Claude a true job search partner. Understands shorthand, remembers companies, tracks contacts, and maintains context across sessions.

## Memory Architecture

### CLAUDE.md — Hot Cache

The working memory file, loaded every session. Contains the most frequently needed context (~50-80 lines). Goal: cover 90% of daily lookups without touching deep storage.

```markdown
# Job Search Memory

## Searcher
[Name], [Current Role] at [Company] ([X] years exp)
Floor: ₹[X]L / $[X]K | Notice: [X] days | Optimizing: [growth/comp/WLB]

## Active Targets
| Company | Role | Stage | Next Action | Deadline |
|---------|------|-------|-------------|----------|
| Razorpay | Senior PM | Interview | Round 2 prep | Feb 12 |
| Stripe | Product Lead | Applied | Follow up | Feb 10 |
| Notion | PM | Discovered | Research | — |

## Key Contacts
| Who | At | Role | Last Contact | Notes |
|-----|-----|------|-------------|-------|
| Priya Sharma | Razorpay | Recruiter | Feb 5 | Scheduled R2 |
| David Chen | Stripe | Eng Director | Feb 3 | LinkedIn msg sent |

## Quick Reference
| Term | Meaning |
|------|---------|
| CTC | Cost to Company (Indian total comp) |
| ESOP | Employee Stock Option Plan |
| R2 | Round 2 interview |
| HM | Hiring Manager |
| JD | Job Description |

## Preferences
- Optimizing for: growth + comp
- Async-first, no weekend culture
- Avoid: crypto, gambling, defense
- Open to: Bangalore hybrid, full remote
- Must-have: equity, health insurance
```

### memory/ — Deep Storage

Organized by category, loaded on demand:

```
memory/
├── glossary.md           ← Master decoder: all companies, contacts, terms
├── companies/            ← Full research reports
│   ├── razorpay.md      ← Company profile, culture, comp data, red flags
│   ├── stripe.md
│   └── notion.md
├── contacts/             ← Individual profiles
│   ├── priya-sharma.md  ← Recruiter at Razorpay, interaction log
│   └── david-chen.md    ← Eng Director at Stripe
├── applications/         ← Materials per application
│   ├── razorpay-senior-pm/
│   │   ├── resume_tailored.docx
│   │   ├── cover_letter.md
│   │   ├── fit_analysis.md
│   │   └── interview_prep.md
│   └── stripe-product-lead/
│       ├── resume_tailored.docx
│       └── cover_letter.md
└── analytics/            ← Tracking over time
    ├── applications.md   ← Date, company, role, source, outcome
    ├── interviews.md     ← Date, company, round, result, learnings
    ├── offers.md         ← Date, company, offer details, decision
    └── briefings.md      ← Briefing dates, stats, actions taken
```

## Glossary Format

`memory/glossary.md` is the complete decoder ring:

```markdown
# Job Search Glossary

## Companies
| Company | Industry | Stage | In Pipeline | Notes |
|---------|----------|-------|-------------|-------|
| Razorpay | Fintech | Series F | Yes - Interview | IPO-bound, payments |
| Stripe | Fintech | Public | Yes - Applied | New India office |
| Notion | Productivity | Series C | Yes - Discovered | Remote-first |
| Cred | Fintech | Series E | No | On watchlist |

## Contacts
| Name | Company | Role | Relationship | Last Contact |
|------|---------|------|-------------|-------------|
| Priya Sharma | Razorpay | Recruiter | Direct | Feb 5 |
| David Chen | Stripe | Eng Director | LinkedIn | Feb 3 |
| Amit Patel | Notion | VP Product | Referral via Ravi | — |

## Terms
| Term | Meaning |
|------|---------|
| CTC | Cost to Company (Indian total compensation) |
| ESOP | Employee Stock Option Plan |
| RSU | Restricted Stock Unit |
| ATS | Applicant Tracking System |
| JD | Job Description |
| HM | Hiring Manager |
| R1/R2/R3 | Interview round 1/2/3 |
| LPA | Lakhs Per Annum |
```

## Contact Profile Format

`memory/contacts/[name-slug].md`:

```markdown
# Priya Sharma

## Role
Recruiter at Razorpay (Talent Acquisition, Product Hiring)

## Contact
- LinkedIn: [url]
- Email: [if known]

## Interaction Log
| Date | Channel | Summary |
|------|---------|---------|
| Feb 1 | LinkedIn | Initial outreach, connected |
| Feb 3 | Email | Scheduled phone screen |
| Feb 5 | Phone | Completed screen, advanced to R2 |

## Notes
- Responsive, replies within 24h
- Mentioned team is growing from 8 to 15
- Suggested reading Razorpay engineering blog before R2
```

## Analytics Format

`memory/analytics/applications.md`:

```markdown
# Application Tracker

| Date | Company | Role | Source | Method | Stage Reached | Outcome | Days Active |
|------|---------|------|--------|--------|--------------|---------|-------------|
| Jan 15 | Razorpay | Senior PM | LinkedIn | Direct + Referral | Interview | Active | 24 |
| Jan 20 | Stripe | Product Lead | Website | Direct | Applied | Active | 19 |
| Jan 22 | Cred | PM | Naukri | Cold apply | Rejected | Closed | 5 |

## Stats
- Total applications: 3
- Active: 2 (67%)
- Interviews: 1 (33% conversion)
- Average response time: 5 days
```

## Memory Lookup Flow

When the user says something like "check on the Stripe thing" or "what's happening with Priya":

1. **CLAUDE.md** (instant) — Check Active Targets for "Stripe", Key Contacts for "Priya"
2. **memory/glossary.md** (fast) — Full company/contact lookup if not in hot cache
3. **memory/companies/ or contacts/** (on demand) — Load full research or profile
4. **Web search** (if stale or missing) — Refresh data
5. **Ask user** (last resort) — Only if truly ambiguous

## Memory Maintenance

### When to Update CLAUDE.md
- New application submitted → add to Active Targets
- Stage change (applied → interview) → update Active Targets
- New contact made → add to Key Contacts
- Term first used → add to Quick Reference
- Offer received → highlight in Active Targets
- Opportunity closed → remove from Active Targets, keep in glossary

### When to Update Deep Storage
- After /research → save company report
- After /apply → save all materials
- After interview → update contact interaction log
- After /negotiate → save strategy
- After /briefing → log in analytics

### Archival Rules
- Never delete memory files
- Prefix closed/inactive items with `_archived_` in filename
- Keep in glossary with "Closed" status
- Analytics records are permanent — they power conversion tracking

## Decoding Examples

| User Says | Claude Understands |
|-----------|-------------------|
| "check on the Stripe thing" | Stripe Product Lead application, currently in Applied stage |
| "prep me for Razorpay" | Interview prep for Senior PM at Razorpay, Round 2 coming up |
| "what did Priya say?" | Priya Sharma (Razorpay recruiter) — check interaction log |
| "my floor is now 50L" | Update CLAUDE.md comp floor from ₹45L to ₹50L |
| "skip Cred" | Remove Cred from pipeline, archive in memory |
| "how's my pipeline?" | Run /status — show all active opportunities |
```
