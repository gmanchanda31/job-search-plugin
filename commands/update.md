---
description: Sync memory, triage stale pipeline items, and refresh context
argument-hint: "[--comprehensive]"
---

# Update Command

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Keep your job search state current. Two modes:

- **Default:** Triage stale pipeline items, refresh memory, check for gaps
- **`--comprehensive`:** Deep scan all memory files, rebuild hot cache, audit consistency

## Usage

```
/job-search:update
/job-search:update --comprehensive
```

## Default Mode

### 1. Load State

Read `JOBSEARCH.md`, `PIPELINE.md`, `CLAUDE.md`, and `memory/glossary.md`.
If any don't exist, suggest `/job-search:start` first.

### 2. Triage Pipeline

Review PIPELINE.md for:
- Entries in "Discovered" for 7+ days → ask: research, apply, or remove?
- Entries in "Applied" for 14+ days with no update → suggest follow-up
- Entries in "Phone Screen" or "Interview" → check if dates have passed, update stage
- Any entries with stale info → prompt user to update

### 3. Check Memory Freshness

Review `memory/companies/`:
- Research older than 30 days for active pipeline companies → suggest refresh
- Companies no longer in pipeline → note for archival

Review `memory/contacts/`:
- Contacts with no recent interaction → suggest outreach or archive

### 4. Sync CLAUDE.md Hot Cache

Rebuild the Active Targets table from PIPELINE.md (only active stages).
Update Key Contacts from recent memory/contacts/ files.
Ensure Quick Reference terms are current.

### 5. Report

```
Update complete:
- Pipeline: X active, Y triaged, Z follow-ups due
- Memory: X companies cached, Y contacts tracked
- Hot cache: CLAUDE.md refreshed
```

## Comprehensive Mode

Everything in Default, plus:

### Extra: Audit All Memory Files

- Check for orphaned files (company research for companies not in pipeline or watchlist)
- Check for missing files (pipeline companies without research)
- Verify glossary completeness against all memory files
- Rebuild CLAUDE.md from scratch

### Extra: Analytics Summary

Read `memory/analytics/` files and present:
- Total applications over time
- Conversion rates (discovered → applied → interview → offer)
- Average time in each stage
- Most active companies/industries

### Extra: Profile Drift Check

Compare JOBSEARCH.md preferences against actual pipeline:
- Are you applying to roles that match your stated preferences?
- Any patterns suggesting your preferences have shifted?
- Suggest profile updates if drift detected
