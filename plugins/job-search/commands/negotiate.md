---
description: Salary research and negotiation scripts for an offer
argument-hint: "<company name>"
---

# Negotiate Command

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Research market rates and build a negotiation strategy for an offer.

## Instructions

### 1. Load Context

Read `JOBSEARCH.md` for comp expectations.
Check `memory/companies/[company].md` for existing compensation data.
Read `${CLAUDE_PLUGIN_ROOT}/skills/job-search/references/negotiation.md` for the full framework.

### 2. Salary Research

Web search:
- `"[role]" "[company]" salary site:glassdoor.com OR site:ambitionbox.com`
- `"[role]" "[level]" compensation site:levels.fyi`
- `"[company]" "[role]" CTC site:ambitionbox.com`
- `"[role]" salary "[city]" site:blind`

### 3. Build Negotiation Package

Generate:
- **Market Data** table with ranges from multiple sources
- **Your Leverage** assessment (competing offers, skills scarcity, their urgency)
- **Negotiation Script** — opening statement, pushback responses, creative alternatives
- **Walk-Away Number** — below this, not worth the move
- **Current vs Offer Comparison** — side-by-side with delta
- **Indian-Specific Notes** if applicable (CTC structure, variable pay, notice buyout, gratuity)

### 4. Save and Update Memory

Save to `memory/applications/[company]-[role]/negotiation_strategy.md`.
Update `CLAUDE.md` with offer details.
Log in `memory/analytics/offers.md`.
