# Job Discovery Reference Guide

## 1. Search Query Templates by Platform

### LinkedIn Jobs
```
site:linkedin.com/jobs "{title}" {location}
site:linkedin.com/jobs {title} {company}
site:linkedin.com/jobs {title} salary:{salary_range}
```

### Naukri.com (India)
```
site:naukri.com {title} {location}
site:naukri.com {title} "experience" years
site:naukri.com {industry} {location} salary
```

### Wellfound/AngelList (Startups)
```
site:wellfound.com "{title}" {location}
site:wellfound.com {industry} startup jobs
site:angel.co jobs {title}
```

### Indeed
```
site:indeed.com "{title}" {location}
site:indeed.com {title} "{company}"
site:indeed.com {title} salary:${min}-${max}
```

### Lever.co & Greenhouse.io (Direct Boards)
```
site:lever.co "{title}" OR site:greenhouse.io "{title}"
site:lever.co {company} jobs
site:greenhouse.io {company} careers
```

### Company Career Pages
```
site:{company.com}/careers {title}
site:{company.com}/jobs {title}
{company.com} careers "{title}"
```

## 2. Constructing Effective Search Queries

**Profile-Based Template:**
- Start with primary title/keywords
- Add location modifier (city, region, or remote)
- Include salary range if specified (filters noise)
- Narrow by industry, seniority level, or company size
- Combine must-haves with OR for alternates

**Query Examples:**
```
"Senior Software Engineer" "remote" salary:$120K-$180K
Product Manager San Francisco startup
Data Scientist India "machine learning"
DevOps Engineer React "AWS" OR "Kubernetes"
```

## 3. Using Claude in Chrome for Job Browsing

**Prerequisites:** User must be logged into job platforms in Chrome.

**Process:**
1. Use read_page to scan visible job listings
2. Extract job IDs, titles, companies, key requirements
3. Click through to full job descriptions for detailed matching
4. Note: Only browse pages user explicitly requests; don't crawl entire sites

**Best For:** Accessing logged-in filters, saved jobs, application history, personalized recommendations.

## 4. Match Scoring Methodology

| Match Level | Criteria | Example |
|---|---|---|
| **High (80%+)** | 80%+ requirements met, no deal-breakers | Title match, location acceptable, salary in range, all key skills present |
| **Medium (60-80%)** | 60-80% criteria met, minor gaps | Good title fit, willing to relocate, salary slightly below range, 1-2 skill gaps |
| **Low (<60%)** | Below 60% OR deal-breaker mismatch | Wrong seniority level, incompatible location, salary far below expectation, critical skill missing |

**Deal-Breaker Checklist:**
- Location requirement conflicts user's constraints
- Salary significantly below user's minimum
- Required visa sponsorship unavailable
- Key skill requirements completely unmet
- Company/industry exclusions violated

## 5. De-duplication Across Sources

**Method:**
1. Normalize company names and job titles
2. Extract core job ID (e.g., LinkedIn job ID, Lever posting ID)
3. Track seen postings in session state
4. When duplicate found: keep earliest source, link to alternates
5. Flag cross-posts (same role on Lever + company site)

## 6. Presenting Results

**Grouped Structure:**
```
## High Match (3 jobs)
1. [Title] @ [Company]
   → Location, salary, match score
   → Key fit: [3 key reasons]

## Medium Match (5 jobs)
2. [Title] @ [Company]
   → Gap: [primary reason], Fit: [compensating factor]

## Low Match (2 jobs)
→ Location/salary mismatch, may explore if interested
```

**Quick Take:** 1-2 sentences on why job fits or doesn't fit profile.

## 7. Handling "No Results"

**Escalation Strategy:**
1. **Broaden Location:** Add "remote" or expand geographic radius
2. **Relax Keywords:** Remove seniority level, try synonym keywords
3. **Platform Shift:** Try different job boards (smaller roles on LinkedIn, startups on Wellfound)
4. **Timing Note:** Alert user if market is slow; suggest watchlist setup
5. **Suggest Alternatives:** "No Senior PM roles, but 12 PM positions found. Review?"

## 8. Watchlist Monitoring

**Setup:**
- User provides target company list or search criteria
- Run weekly/daily check with saved queries
- Track job posting date, apply deadline, salary updates

**Check Process:**
```
for company in watchlist:
  search {platform} for company careers page
  compare new postings against previous scan
  alert on: new roles, salary changes, reopened positions
```

**Report Format:**
- New postings this week (with link)
- Closed roles (no longer hiring for X)
- Hiring velocity (if tracking multiple roles)

---

**Last Updated:** 2026-02-07
**Version:** 1.0
