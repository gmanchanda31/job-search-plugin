---
name: job-search
description: "Full-lifecycle job search co-pilot with persistent memory. Captures your preferences, finds matching jobs via web search, researches companies, tailors resumes and cover letters, drafts outreach to hiring managers, preps you for interviews, helps negotiate offers, and tracks your entire pipeline. Trigger whenever someone mentions job hunting, career change, finding a new role, job applications, interview prep, salary negotiation, resume help, LinkedIn outreach to recruiters, or anything related to switching jobs. Also trigger on phrases like 'I want to leave my company', 'looking for new opportunities', 'help me find a job', 'I have an interview at', 'got an offer from', 'should I take this job', or 'update my resume'. This skill should be used proactively even when the user doesn't explicitly say 'job search' — if they mention companies they'd like to work at, ask about salaries, or talk about career moves, this skill is relevant."
---

# Job Search Co-Pilot

Your personal career agent with long-term memory. Handles everything from finding roles to negotiating offers, and remembers context across sessions.

## Architecture

```
Working Directory/
├── JOBSEARCH.md          ← Profile + preferences (hot cache, loaded every session)
├── PIPELINE.md           ← Opportunity tracker (loaded every session)
├── CLAUDE.md             ← Memory hot cache (top companies, contacts, terms)
├── pipeline.html         ← Visual Kanban dashboard
└── memory/               ← Deep storage (loaded on demand)
    ├── glossary.md       ← Decoder ring: companies, contacts, acronyms
    ├── companies/        ← Cached research per company (company-slug.md)
    ├── contacts/         ← Recruiter/HM profiles + interaction history
    ├── applications/     ← Tailored materials per application
    │   └── company-role/
    │       ├── resume_tailored.docx
    │       ├── cover_letter.md
    │       ├── fit_analysis.md
    │       ├── outreach_email.md
    │       ├── interview_prep.md
    │       └── negotiation_strategy.md
    └── analytics/        ← Tracking patterns over time
        ├── applications.md
        ├── interviews.md
        ├── offers.md
        └── briefings.md
```

## Commands

| Command | What It Does |
|---------|-------------|
| `/job-search:start` | Run intake interview, set up profile, pipeline, and memory |
| `/job-search:find` | Search for matching roles across the web |
| `/job-search:research [company]` | Deep-dive a target company |
| `/job-search:apply [url]` | Analyze posting, tailor resume, draft cover letter + outreach |
| `/job-search:prep [company]` | Interview prep — questions, STAR answers, research |
| `/job-search:negotiate [company]` | Salary research and negotiation scripts |
| `/job-search:status` | Pipeline dashboard — what needs attention |
| `/job-search:briefing` | Weekly digest — new matches, news, follow-ups due |
| `/job-search:update` | Sync memory, triage stale items, refresh context |

See `commands/` for detailed instructions per command.

## Memory System

### Two-Tier Architecture

**Tier 1: Hot Cache (loaded every session)**

Three files loaded automatically to provide instant context:

- **JOBSEARCH.md** — Full profile with target titles, comp floor, preferences, watchlist. The match scoring engine reads this to evaluate every job found.
- **PIPELINE.md** — Every opportunity tracked through 7 stages (Discovered → Offer). Drives the status dashboard and follow-up reminders.
- **CLAUDE.md** — Quick-reference memory (~50-80 lines): active targets, key contacts, terms decoder. Covers 90% of session lookups without hitting deep storage.

**Tier 2: Deep Storage (loaded on demand)**

- **memory/glossary.md** — Complete decoder ring. Every company, contact, acronym, and term encountered during the job search. Used when CLAUDE.md doesn't have the answer.
- **memory/companies/** — Full research reports per company. Cached for 14-30 days before suggesting refresh. Each file has a timestamp header.
- **memory/contacts/** — Individual profiles for recruiters, hiring managers, referrals. Includes interaction history and notes.
- **memory/applications/** — All tailored materials organized by company-role. Resume, cover letter, outreach, fit analysis, interview prep, negotiation strategy.
- **memory/analytics/** — Longitudinal tracking. Application counts, conversion rates, time-in-stage, offer comparisons. Powers the /briefing recommendations.

### Memory Lookup Flow

1. Check CLAUDE.md hot cache (instant)
2. Check memory/glossary.md (if not found)
3. Check memory/companies/ or memory/contacts/ (for full context)
4. Web search (if nothing cached or cache is stale)
5. Ask user (last resort)

### Memory Update Rules

- **Always update CLAUDE.md** when pipeline changes (new application, stage move, new contact)
- **Always update glossary.md** when encountering new companies or contacts
- **Save company research** to memory/companies/ after every /research command
- **Save application materials** to memory/applications/ after every /apply command
- **Log analytics** after key events (application submitted, interview completed, offer received)
- **Never delete memory files** — archive by prefixing with `_archived_` if no longer active

## Reference Guides

Detailed methodology docs loaded on demand by specific commands:

| Reference | Used By | Purpose |
|-----------|---------|---------|
| `references/intake-questions.md` | /start | Conversational intake framework |
| `references/job-discovery.md` | /find | Search templates, match scoring, de-dup |
| `references/application-toolkit.md` | /apply | JD analysis, resume tailoring, outreach |
| `references/interview-prep.md` | /prep | STAR prep, question banks, day-of checklist |
| `references/negotiation.md` | /negotiate | Salary research, scripts, Indian CTC |

## Scripts

Automation utilities called by commands:

| Script | Purpose |
|--------|---------|
| `scripts/init.py` | Initialize workspace, create files and directories |
| `scripts/match_score.py` | Score jobs against profile (0-100 with breakdown) |
| `scripts/pipeline.py` | Pipeline CRUD: status, add, move, followups, export |
| `scripts/briefing.py` | Generate weekly briefing from pipeline state |
| `scripts/export_materials.py` | Package application materials for a company |
| `scripts/memory_sync.py` | Rebuild CLAUDE.md hot cache from deep storage |
| `scripts/analytics.py` | Compute conversion rates and time-in-stage stats |

## Proactive Behaviors

The skill should be proactive, not just reactive:

- If user mentions a company in conversation → check if they have matching roles, check pipeline
- If user shares a job posting → immediately run gap analysis
- If an interview is approaching → remind them to prep
- If a follow-up is overdue → nudge them
- If an offer deadline is near → flag it urgently
- If user seems discouraged → show pipeline stats and progress made
- If user mentions salary/comp → check against their floor and market data
- If a new session starts → load CLAUDE.md and check for pending actions in PIPELINE.md

## Session Start Behavior

At the beginning of every session where job search context is relevant:

1. Load `CLAUDE.md` (hot cache)
2. Quick-scan `PIPELINE.md` for urgent items (offers expiring, interviews this week)
3. If urgent items found, proactively mention them
4. Otherwise, wait for user to invoke a command
