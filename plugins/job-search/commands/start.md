---
description: Run intake interview, set up profile, pipeline tracker, and memory system
---

# Start Command

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Initialize the job search workspace and run the intake interview to build your profile.

## Instructions

### 1. Check What Exists

Check the working directory for:
- `JOBSEARCH.md` — your search profile (hot cache)
- `PIPELINE.md` — opportunity tracker
- `pipeline.html` — visual Kanban dashboard
- `memory/` — deep storage directory
- `memory/glossary.md` — company/contact decoder

### 2. Create What's Missing

Run `python ${CLAUDE_PLUGIN_ROOT}/skills/job-search/scripts/init.py [working_dir]` to initialize.

This creates:
- JOBSEARCH.md (profile template)
- PIPELINE.md (empty pipeline)
- memory/ directories (companies, contacts, applications, analytics)
- pipeline.html (copied from assets)
- memory/glossary.md (empty decoder)

### 3. Run Intake Interview

If JOBSEARCH.md is empty/template, start the conversational intake. Read `${CLAUDE_PLUGIN_ROOT}/skills/job-search/references/intake-questions.md` for the full framework.

**Don't make the user fill a form — have a conversation.** Cover:

1. **Identity & Experience** — current role, company, years, core skills, education, resume
2. **Target Role** — titles, industries, company stage, team size preferences
3. **Logistics** — location, visa status, notice period, start timeline
4. **Compensation** — base floor (₹ or $), total comp target, must-haves vs nice-to-haves
5. **Culture & Values** — what they optimize for, red flags, good-fit signals
6. **Current Pipeline** — already applying? interviews scheduled? contacts at targets?
7. **Dream Companies** — watchlist of companies they'd love to work at

### 4. Write Profile

Write everything captured to `JOBSEARCH.md` using the structured format with tables for Target, Compensation, and a Watchlist section.

### 5. Bootstrap Memory

Create `memory/glossary.md` with initial entries:
- Companies from watchlist with brief descriptions
- Any contacts mentioned during intake
- Industry terms and acronyms used

Create `CLAUDE.md` as the hot cache (~50-80 lines):
```markdown
# Job Search Memory

## Searcher
[Name], [Current Role] at [Company] ([X] years)

## Active Targets
| Company | Role | Stage | Next Action |
|---------|------|-------|-------------|

## Key Contacts
| Who | At | Role | How We Know |
|-----|-----|------|-------------|

## Quick Reference
| Term | Meaning |
|------|---------|

## Preferences
- Optimizing for: [growth/comp/WLB/etc]
- Floor: [₹X / $X]
- Avoid: [industries/signals]
- Notice: [X days]
```

### 6. Open Dashboard

Tell the user: "Dashboard is ready at `pipeline.html`. Open it from your file browser to track your pipeline visually."

### 7. Report

```
Job search workspace ready:
- Profile: JOBSEARCH.md (filled)
- Pipeline: PIPELINE.md (empty — run /job-search:find to discover roles)
- Memory: X companies, X contacts in glossary
- Dashboard: pipeline.html

Next steps:
- /job-search:find to discover matching roles
- /job-search:research [company] to deep-dive a target
```
