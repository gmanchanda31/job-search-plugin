---
description: View your pipeline dashboard — what needs attention right now
---

# Status Command

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Show pipeline status with actionable next steps.

## Instructions

### 1. Load Pipeline

Read `PIPELINE.md`. If missing, suggest `/job-search:start`.

Run:
```
python ${CLAUDE_PLUGIN_ROOT}/skills/job-search/scripts/pipeline.py status PIPELINE.md
```

### 2. Present Summary

Show:
- Total active opportunities by stage (with emoji indicators)
- Action items (offers pending, interviews upcoming, follow-ups due)
- Stale items (discovered but not acted on for 7+ days)

### 3. Suggest Next Actions

Based on pipeline state:
- Thin pipeline (<5 active) → suggest `/job-search:find`
- Pending offers → suggest `/job-search:negotiate`
- Upcoming interviews → suggest `/job-search:prep [company]`
- Overdue follow-ups → prompt to reach out
- Many discovered, few applied → suggest narrowing and applying

### 4. Dashboard Reminder

Remind user: "Open `pipeline.html` for the visual Kanban view."
