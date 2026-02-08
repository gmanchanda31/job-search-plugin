---
description: Weekly digest — new matches, company news, follow-ups due
---

# Briefing Command

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate a comprehensive weekly job search briefing.

## Instructions

### 1. Load State

Read `PIPELINE.md`, `JOBSEARCH.md`, and `CLAUDE.md`.

Run:
```
python ${CLAUDE_PLUGIN_ROOT}/skills/job-search/scripts/briefing.py PIPELINE.md
```

### 2. Search for New Matches

Run the same search strategy as `/job-search:find` to find roles posted in the last 7 days. Cross-reference against PIPELINE.md to avoid duplicates.

### 3. Company News

For each company in the pipeline and watchlist, search for recent news:
- `"[company]" news [this week/month]`
- Funding, layoffs, pivots, acquisitions, product launches

### 4. Build Briefing

Generate:
- **New Matches** — roles found this week with match scores
- **Company News** — relevant updates about tracked companies
- **Action Items** — follow-ups due, interviews to prep, offer deadlines
- **Pipeline Stats** — total active, new this week, offers pending, interviews scheduled
- **Recommendations** — based on pipeline health

### 5. Update Memory

Log briefing generation in `memory/analytics/briefings.md` with date and summary stats.
Update `CLAUDE.md` with any new active targets or changed statuses.
