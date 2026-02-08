---
description: Analyze posting, tailor resume, draft cover letter and outreach
argument-hint: "<job URL or description>"
---

# Apply Command

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate a complete application package for a specific role.

## Instructions

### 1. Load Context

Read `JOBSEARCH.md` (profile) and check `memory/companies/` for existing research.
Read `${CLAUDE_PLUGIN_ROOT}/skills/job-search/references/application-toolkit.md` for the full workflow.

### 2. Analyze Job Description

If URL provided, fetch the posting. Extract:
- Required vs nice-to-have skills
- Years of experience expected
- Key responsibilities
- Hidden signals (urgency, team size hints, growth indicators)
- ATS keywords

### 3. Gap Analysis

Compare JD requirements against JOBSEARCH.md profile:
- Strong matches (checkmarks)
- Transferable skills (needs framing)
- Gaps (acknowledge and bridge)
- ATS keywords to inject

### 4. Tailor Resume

If user uploaded a resume: reorder bullets, inject ATS keywords, adjust summary.
If no resume: generate targeted resume from profile.
Output as tailored .docx or .pdf.

### 5. Draft Cover Letter

- Opening: reference something specific about company (from research)
- Bridge: most relevant experience mapped to top requirements
- Closer: specific enthusiasm + call to action
- Tone: confident, specific, not generic. No "I'm excited to apply..." openings.

### 6. Research Hiring Manager

Web search for the hiring manager. Research their background for personalized outreach.
Save to `memory/contacts/[name-slug].md`.

### 7. Draft Outreach

- Email to hiring manager (research-backed opening, fit statement, low-friction ask)
- LinkedIn connection request (under 300 chars, genuine interest hook)

### 8. Save Materials

Save everything to `memory/applications/[company]-[role]/`:
- resume_tailored.docx
- cover_letter.md
- outreach_email.md
- fit_analysis.md

### 9. Update Pipeline

Move opportunity from "Discovered" to "Applied" in PIPELINE.md with date.

### 10. Update Memory

Update `CLAUDE.md` Active Targets table.
Update `memory/glossary.md` with any new contacts or terms.
Record application date in analytics: `memory/analytics/applications.md`.
