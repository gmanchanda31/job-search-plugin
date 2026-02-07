---
description: Deep-dive a target company — culture, comp, team, red flags
argument-hint: "<company name>"
---

# Research Command

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Research a company thoroughly from a job seeker's perspective.

## Instructions

### 1. Check Memory First

Look for existing research in `memory/companies/[company-slug].md`. If found and less than 14 days old, present cached version with option to refresh.

### 2. Web Research

Search for:
1. **Company profile:** what they do, size, funding, revenue, growth
2. **Culture signals:** Glassdoor/AmbitionBox rating, engineering blog, LinkedIn sentiment
3. **Leadership:** team lead backgrounds, tenure, reporting structure
4. **Recent news:** funding, layoffs, acquisitions, product launches
5. **Hiring signals:** open roles count, department growth, velocity
6. **Tech stack / tools:** what they use
7. **Employee trajectory:** where people go after (LinkedIn alumni)

### 3. Red Flag Detection

Automatically flag:
- Recent layoffs or hiring freezes
- Glassdoor below 3.5 or declining
- High leadership turnover (3+ C-suite exits in 2 years)
- Funding runway concerns
- Negative patterns (lawsuits, regulatory, toxic culture)

### 4. Compensation Intelligence

Search salary data:
- `"[role]" "[company]" salary site:glassdoor.com OR site:ambitionbox.com`
- `"[role]" "[level]" compensation site:levels.fyi`

Compare against user's floor from JOBSEARCH.md.

### 5. Save to Memory

Write comprehensive research to `memory/companies/[company-slug].md` with timestamp.

Update `memory/glossary.md` with company entry.

If hiring manager identified, create/update `memory/contacts/[name-slug].md`.

Update `CLAUDE.md` if this is an active target company.

### 6. Present Output

Follow the research template from the main SKILL.md: Should You Apply verdict, Quick Take, Company Profile, Culture Assessment, Your Team, Compensation Intelligence, Red Flags, Insider Path.
