"""
Generate a job search briefing from PIPELINE.md.
Shows pipeline status, follow-ups due, upcoming interviews, and pending offers.

Usage:
    python scripts/briefing.py [pipeline_path] [--format md|json]
"""
import re
import sys
import json
from datetime import datetime
from pathlib import Path

STAGES = ["Discovered", "Researching", "Applied", "Phone Screen", "Interview", "Offer", "Declined / Rejected"]

def parse_pipeline(path):
    text = Path(path).read_text()
    entries = []
    current_stage = None

    for line in text.split("\n"):
        stage_match = re.match(r"^## (.+)$", line.strip())
        if stage_match:
            stage_name = stage_match.group(1).strip()
            if stage_name in STAGES:
                current_stage = stage_name
            continue

        if line.strip().startswith("- [") and current_stage:
            raw = line.strip()
            completed = "[x]" in raw
            title_match = re.search(r"\*\*(.+?)\*\*", raw)
            title = title_match.group(1) if title_match else raw[6:50]

            entries.append({
                "title": title,
                "stage": current_stage,
                "completed": completed,
                "raw": raw,
            })

    return entries

def generate_briefing(pipeline_path, fmt="md"):
    entries = parse_pipeline(pipeline_path)
    today = datetime.now()

    active = [e for e in entries if e["stage"] != "Declined / Rejected"]
    by_stage = {}
    for e in entries:
        by_stage.setdefault(e["stage"], []).append(e)

    offers = by_stage.get("Offer", [])
    interviews = by_stage.get("Interview", [])
    phone_screens = by_stage.get("Phone Screen", [])
    applied = by_stage.get("Applied", [])
    discovered = by_stage.get("Discovered", [])

    if fmt == "json":
        result = {
            "date": today.strftime("%Y-%m-%d"),
            "total_active": len(active),
            "by_stage": {k: len(v) for k, v in by_stage.items()},
            "urgent": {
                "offers_pending": len(offers),
                "interviews_upcoming": len(interviews),
                "followups_needed": len(applied),
            },
            "entries": entries,
        }
        print(json.dumps(result, indent=2))
        return result

    # Markdown briefing
    briefing = f"""# Job Search Briefing — {today.strftime("%B %d, %Y")}

## Pipeline Summary

**{len(active)} active opportunities**

"""
    for stage in STAGES:
        count = len(by_stage.get(stage, []))
        if count > 0:
            emoji = {"Discovered": "🔍", "Researching": "🔬", "Applied": "📨",
                     "Phone Screen": "📞", "Interview": "🎯", "Offer": "🎉",
                     "Declined / Rejected": "❌"}.get(stage, "•")
            briefing += f"- {emoji} **{stage}:** {count}\n"

    # Urgent items
    briefing += "\n## Action Items\n\n"
    action_count = 0

    if offers:
        for o in offers:
            action_count += 1
            briefing += f"{action_count}. 🎉 **OFFER PENDING:** {o['title']} — decision needed\n"

    if interviews:
        for iv in interviews:
            action_count += 1
            briefing += f"{action_count}. 🎯 **INTERVIEW:** {iv['title']} — run `/prep` if not done\n"

    if phone_screens:
        for ps in phone_screens:
            action_count += 1
            briefing += f"{action_count}. 📞 **PHONE SCREEN:** {ps['title']} — review company basics\n"

    if applied:
        for a in applied:
            action_count += 1
            briefing += f"{action_count}. 📨 **FOLLOW UP:** {a['title']} — check for response\n"

    if discovered:
        briefing += f"\n💡 **{len(discovered)} roles discovered** — ready to research or apply\n"

    if action_count == 0:
        briefing += "No urgent actions — pipeline is on track.\n"

    # Recommendations
    briefing += "\n## Recommendations\n\n"
    if len(active) < 5:
        briefing += "- Pipeline is thin. Run `/find` to discover more matching roles.\n"
    if len(discovered) > 5:
        briefing += "- You have many undecided roles. Research and apply to narrow the funnel.\n"
    if not offers and not interviews and len(applied) > 5:
        briefing += "- Many applications, few callbacks. Consider adjusting resume or trying direct outreach.\n"
    if offers:
        briefing += "- You have a pending offer. Run `/negotiate` before responding.\n"

    print(briefing)
    return briefing

if __name__ == "__main__":
    path = "PIPELINE.md"
    fmt = "md"
    args = sys.argv[1:]
    skip_next = False
    for i, arg in enumerate(args):
        if skip_next:
            skip_next = False
            continue
        if arg == "--format" and i + 1 < len(args):
            fmt = args[i + 1]
            skip_next = True
        elif not arg.startswith("--"):
            path = arg

    generate_briefing(path, fmt)
