"""
Initialize the job search workspace with memory system.
Creates JOBSEARCH.md, PIPELINE.md, CLAUDE.md, memory directories, and copies dashboard.

Usage:
    python scripts/init.py [workspace_dir]
"""
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

def init_workspace(workspace_dir=None):
    if workspace_dir is None:
        workspace_dir = os.getcwd()

    workspace = Path(workspace_dir)
    skill_dir = Path(__file__).parent.parent
    created = []
    skipped = []

    # 1. JOBSEARCH.md — user profile (hot cache tier 1)
    jobsearch = workspace / "JOBSEARCH.md"
    if not jobsearch.exists():
        jobsearch.write_text("""# Job Search Profile

## About Me
<!-- Fill in during /start intake -->

## Target
| Field | Value |
|-------|-------|
| Titles | |
| Industries | |
| Stage | |
| Location | |
| Notice period | |

## Compensation
| Field | Value |
|-------|-------|
| Base floor | |
| Target total comp | |
| Must-haves | |
| Nice-to-haves | |

## Preferences
<!-- What you're optimizing for, culture signals, red flags to avoid -->

## Watchlist
<!-- Companies you're especially interested in -->

## Resume
<!-- Path to uploaded resume file -->
""")
        created.append("JOBSEARCH.md")
    else:
        skipped.append("JOBSEARCH.md (already exists)")

    # 2. PIPELINE.md — opportunity tracker (hot cache tier 1)
    pipeline = workspace / "PIPELINE.md"
    if not pipeline.exists():
        pipeline.write_text("""# Job Search Pipeline

## Discovered

## Researching

## Applied

## Phone Screen

## Interview

## Offer

## Declined / Rejected
""")
        created.append("PIPELINE.md")
    else:
        skipped.append("PIPELINE.md (already exists)")

    # 3. CLAUDE.md — memory hot cache
    claude_md = workspace / "CLAUDE.md"
    if not claude_md.exists():
        claude_md.write_text(f"""# Job Search Memory

> Last updated: {datetime.now().strftime("%B %d, %Y")}

## Searcher
<!-- [Name], [Current Role] at [Company] ([X] years exp) -->
<!-- Floor: ₹[X]L / $[X]K | Notice: [X] days | Optimizing: [growth/comp/WLB] -->

## Active Targets
| Company | Role | Stage | Next Action | Deadline |
|---------|------|-------|-------------|----------|

## Key Contacts
| Who | At | Role | Last Contact | Notes |
|-----|-----|------|-------------|-------|

## Quick Reference
| Term | Meaning |
|------|---------|
| CTC | Cost to Company (Indian total comp) |
| ESOP | Employee Stock Option Plan |
| ATS | Applicant Tracking System |
| JD | Job Description |
| HM | Hiring Manager |

## Preferences
<!-- Filled during /start intake -->
""")
        created.append("CLAUDE.md")
    else:
        skipped.append("CLAUDE.md (already exists)")

    # 4. Memory directories
    memory_dirs = [
        "memory/companies",
        "memory/contacts",
        "memory/applications",
        "memory/analytics",
    ]
    for d in memory_dirs:
        dirpath = workspace / d
        if not dirpath.exists():
            dirpath.mkdir(parents=True, exist_ok=True)
            created.append(f"{d}/")
        else:
            skipped.append(f"{d}/ (already exists)")

    # 5. Glossary (deep storage index)
    glossary = workspace / "memory" / "glossary.md"
    if not glossary.exists():
        glossary.write_text("""# Job Search Glossary

## Companies
| Company | Industry | Stage | In Pipeline | Notes |
|---------|----------|-------|-------------|-------|

## Contacts
| Name | Company | Role | Relationship | Last Contact |
|------|---------|------|-------------|-------------|

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
""")
        created.append("memory/glossary.md")
    else:
        skipped.append("memory/glossary.md (already exists)")

    # 6. Analytics templates
    analytics_files = {
        "memory/analytics/applications.md": """# Application Tracker

| Date | Company | Role | Source | Method | Stage Reached | Outcome | Days Active |
|------|---------|------|--------|--------|--------------|---------|-------------|

## Stats
- Total applications: 0
- Active: 0
- Interview conversion: —
- Average response time: —
""",
        "memory/analytics/interviews.md": """# Interview Tracker

| Date | Company | Role | Round | Format | Result | Learnings |
|------|---------|------|-------|--------|--------|-----------|

## Stats
- Total interviews: 0
- Pass rate: —
- Average rounds per company: —
""",
        "memory/analytics/offers.md": """# Offer Tracker

| Date | Company | Role | Base | Total Comp | Equity | Decision | Notes |
|------|---------|------|------|-----------|--------|----------|-------|

## Stats
- Total offers: 0
- Average offer: —
- Accepted: 0
""",
        "memory/analytics/briefings.md": """# Briefing Log

| Date | Active Pipeline | New This Week | Interviews | Offers | Actions Taken |
|------|----------------|---------------|------------|--------|---------------|
""",
    }
    for fpath, content in analytics_files.items():
        filepath = workspace / fpath
        if not filepath.exists():
            filepath.write_text(content)
            created.append(fpath)
        else:
            skipped.append(f"{fpath} (already exists)")

    # 7. Pipeline dashboard
    dashboard_src = skill_dir / "assets" / "pipeline.html"
    dashboard_dst = workspace / "pipeline.html"
    if not dashboard_dst.exists() and dashboard_src.exists():
        shutil.copy2(dashboard_src, dashboard_dst)
        created.append("pipeline.html")
    elif dashboard_dst.exists():
        skipped.append("pipeline.html (already exists)")
    else:
        skipped.append("pipeline.html (source not found)")

    # Report
    print("Job Search Workspace Initialized")
    print(f"Location: {workspace}")
    print()
    if created:
        print("Created:")
        for f in created:
            print(f"  + {f}")
    if skipped:
        print("Skipped:")
        for f in skipped:
            print(f"  ~ {f}")
    print()
    print("Files ready:")
    print(f"  Hot cache: JOBSEARCH.md, PIPELINE.md, CLAUDE.md")
    print(f"  Deep storage: memory/ ({len([d for d in memory_dirs if workspace.joinpath(d).exists()])} dirs)")
    print(f"  Dashboard: pipeline.html")
    print()
    print("Next: Run /job-search:start to fill in your profile")
    return {"created": created, "skipped": skipped, "workspace": str(workspace)}

if __name__ == "__main__":
    workspace = sys.argv[1] if len(sys.argv) > 1 else None
    init_workspace(workspace)
