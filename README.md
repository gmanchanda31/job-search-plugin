# Job Search Co-Pilot Plugin

A full-lifecycle job search companion with persistent memory across sessions. From intake to offer negotiation, it tracks your entire pipeline with deep research on companies, tailored application materials, and proactive reminders.

## Getting Started

Run `/job-search:start` to kick off your job search journey. The plugin will capture your preferences, goals, and constraints in its long-term memory system.

## Commands

| Command | Description |
|---------|-------------|
| `/job-search:start` | Initialize your job search profile and preferences |
| `/job-search:find` | Discover matching roles based on your criteria |
| `/job-search:research` | Deep dive into company research and role fit analysis |
| `/job-search:apply` | Tailor resumes and cover letters for specific roles |
| `/job-search:prep` | Interview preparation with company-specific insights |
| `/job-search:negotiate` | Offer analysis and negotiation strategy |
| `/job-search:status` | Pipeline overview and opportunity tracking |
| `/job-search:briefing` | Daily/weekly briefing with proactive reminders |
| `/job-search:update` | Update job search status and new opportunities |

## Memory System

The plugin uses a two-tier architecture to keep your job search organized:

- **JOBSEARCH.md** — Hot cache containing your profile, active targets, and quick-lookup context
- **PIPELINE.md** — Opportunity tracker loaded every session with current applications and conversations
- **memory/** — Deep storage for companies, contacts, applications, and analytics enabling research and personalization

This persistent memory across sessions means you can pick up exactly where you left off without repeating context.

## What Makes It Different

- **Persistent Memory Across Sessions** — Your entire job search context stays available, not lost between conversations
- **Proactive Reminders** — Follow-ups and next steps are tracked and surfaced automatically
- **India + Global Compensation Handling** — Understands salary expectations across markets and negotiation norms
- **Visual Kanban Dashboard** — See your full pipeline at a glance with status-based organization

## Connectors

The plugin works standalone using web search and your local memory. Future connector integrations will supercharge discovery:

- **LinkedIn** — Unified profile management and direct outreach
- **Naukri** — Indian job board listings and applications
- **Job Boards** — Auto-import from multiple platforms
- **Calendar** — Seamless interview scheduling
- **Email** — Outreach tracking and follow-up management

Connect your favorite tools to transform job search from manual work into a fully automated pipeline.
