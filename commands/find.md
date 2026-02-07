---
description: Search for matching roles across the web
argument-hint: "[query or blank for auto-search]"
---

# Find Command

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Discover job opportunities matching your profile.

## Instructions

### 1. Load Profile

Read `JOBSEARCH.md` from the working directory. If it doesn't exist, suggest `/job-search:start` first.

Extract: target titles, industries, locations, comp floor, watchlist companies, avoid list.

### 2. Search Strategy

Read `${CLAUDE_PLUGIN_ROOT}/skills/job-search/references/job-discovery.md` for full search templates.

Run multiple web searches in parallel:

**Role-specific:**
- `"[target title]" "[industry]" jobs [location] site:linkedin.com/jobs`
- `"[target title]" "[industry]" hiring site:wellfound.com`
- `"[target title]" remote site:lever.co OR site:greenhouse.io`

**Company-specific (for watchlist):**
- `"[company]" careers "[target title]"`
- `site:[company domain]/careers`

**Aggregator:**
- `"[target title]" [location] site:naukri.com`
- `"[target title]" [industry] site:indeed.com`

If user provided a specific query, incorporate it into searches.

If **Claude in Chrome** is connected, browse LinkedIn Jobs, Naukri, and Wellfound directly for personalized results.

### 3. Score Results

For each job found, run match scoring against profile:
```
python ${CLAUDE_PLUGIN_ROOT}/skills/job-search/scripts/match_score.py \
  --profile JOBSEARCH.md --title "X" --company "Y" --industry "Z" \
  --location "L" --comp "C" --stage "S"
```

Classify as High (75+), Medium (50-74), Low (30-49), or Deal-Breaker.

### 4. De-duplicate

Remove duplicates found across multiple sources. Keep the richest listing.

### 5. Check Memory

Before presenting, check `memory/companies/` — if we already researched a company, note that.
Check `PIPELINE.md` — if a role is already tracked, flag it as "already in pipeline".

### 6. Present Results

Group by match quality (Strong → Medium → Explore). For each:
- Match score and why
- Company, title, location, comp (if listed)
- Posted date, link
- Quick take (2 sentences on fit)
- Actions: [Research] [Apply] [Skip]

### 7. Add to Pipeline

When user shows interest, add to PIPELINE.md under "Discovered":
```
python ${CLAUDE_PLUGIN_ROOT}/skills/job-search/scripts/pipeline.py add PIPELINE.md \
  --company "X" --role "Y" --comp "Z" --location "L" --url "U"
```

### 8. Update Memory

Add any new companies encountered to `memory/glossary.md` with brief description.
Update `CLAUDE.md` Active Targets table if user adds roles to pipeline.
