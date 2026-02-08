"""
Pipeline manager — read, update, and query the PIPELINE.md tracker.

Usage:
    python scripts/pipeline.py status [pipeline_path]
    python scripts/pipeline.py add [pipeline_path] --company "X" --role "Y" --stage "Discovered" ...
    python scripts/pipeline.py move [pipeline_path] --company "X" --to "Applied"
    python scripts/pipeline.py followups [pipeline_path]
    python scripts/pipeline.py export [pipeline_path] --format json

All commands default to ./PIPELINE.md if no path is given.
"""
import re
import json
import sys
from datetime import datetime, timedelta
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
            if stage_name in STAGES or stage_name == "Declined / Rejected":
                current_stage = stage_name
            continue

        entry_match = re.match(r"^- \[[ x]\] \*?\*?(.+?)(?:\*\*)?(?:\s*\|\s*(.+))?$", line.strip())
        if entry_match and current_stage:
            raw = line.strip()
            parts = [p.strip() for p in raw.split("|")]
            title_part = parts[0] if parts else raw

            company_role = ""
            title_clean = re.sub(r"^- \[[ x]\] ", "", title_part)
            title_clean = title_clean.replace("**", "").replace("~~", "").strip()

            entry = {
                "raw": raw,
                "title": title_clean,
                "stage": current_stage,
                "completed": "[x]" in raw,
                "fields": {},
            }

            for p in parts[1:]:
                p = p.strip()
                if p.startswith("http"):
                    entry["fields"]["url"] = p
                elif "₹" in p or "$" in p:
                    entry["fields"]["comp"] = p
                elif any(loc in p.lower() for loc in ["remote", "bangalore", "mumbai", "delhi", "hybrid", "onsite", "india"]):
                    entry["fields"]["location"] = p
                elif p.startswith("Found:") or p.startswith("Applied:") or p.startswith("Scheduled:"):
                    key, val = p.split(":", 1)
                    entry["fields"][key.strip().lower()] = val.strip()
                elif p.startswith("Follow-up:"):
                    entry["fields"]["followup"] = p.split(":", 1)[1].strip()
                else:
                    entry["fields"]["extra"] = p

            entries.append(entry)

    return entries

def get_status(path):
    entries = parse_pipeline(path)
    active = [e for e in entries if e["stage"] != "Declined / Rejected"]

    stage_counts = {}
    for e in entries:
        stage_counts[e["stage"]] = stage_counts.get(e["stage"], 0) + 1

    print(f"Pipeline: {len(active)} active opportunities\n")
    for stage in STAGES:
        count = stage_counts.get(stage, 0)
        if count > 0:
            emoji = {"Discovered": "🔍", "Researching": "🔬", "Applied": "📨",
                     "Phone Screen": "📞", "Interview": "🎯", "Offer": "🎉",
                     "Declined / Rejected": "❌"}.get(stage, "•")
            print(f"  {emoji} {stage}: {count}")

    # Check for action items
    print("\n⚡ Action needed:")
    action_count = 0
    for e in entries:
        if e["stage"] == "Offer":
            action_count += 1
            print(f"  {action_count}. Offer pending: {e['title']} — decision needed")
        if "followup" in e.get("fields", {}):
            action_count += 1
            print(f"  {action_count}. Follow up: {e['title']} ({e['fields']['followup']})")

    if action_count == 0:
        print("  None — pipeline is on track")

    return {"total_active": len(active), "stage_counts": stage_counts}

def add_entry(path, company, role, stage="Discovered", comp=None, location=None, url=None, notes=None):
    pipeline_path = Path(path)
    text = pipeline_path.read_text()
    today = datetime.now().strftime("%b %d")

    parts = [f"**{role} — {company}**"]
    if comp:
        parts.append(comp)
    if location:
        parts.append(location)
    if url:
        parts.append(f"[link]({url})")
    parts.append(f"Found: {today}")

    entry_line = f"- [ ] {' | '.join(parts)}"
    if notes:
        entry_line += f"\n  - {notes}"

    stage_header = f"## {stage}"
    if stage_header in text:
        lines = text.split("\n")
        insert_idx = None
        for i, line in enumerate(lines):
            if line.strip() == stage_header:
                insert_idx = i + 1
                break
        if insert_idx is not None:
            lines.insert(insert_idx, entry_line)
            pipeline_path.write_text("\n".join(lines))
            print(f"Added: {role} — {company} → {stage}")
            return True

    print(f"Error: Stage '{stage}' not found in pipeline")
    return False

def move_entry(path, search_term, to_stage):
    pipeline_path = Path(path)
    text = pipeline_path.read_text()
    lines = text.split("\n")

    entry_line = None
    entry_idx = None
    for i, line in enumerate(lines):
        if search_term.lower() in line.lower() and line.strip().startswith("- ["):
            entry_line = line
            entry_idx = i
            break

    if entry_line is None:
        print(f"Error: No entry matching '{search_term}' found")
        return False

    lines.pop(entry_idx)

    stage_header = f"## {to_stage}"
    for i, line in enumerate(lines):
        if line.strip() == stage_header:
            lines.insert(i + 1, entry_line)
            pipeline_path.write_text("\n".join(lines))
            print(f"Moved '{search_term}' → {to_stage}")
            return True

    print(f"Error: Stage '{to_stage}' not found")
    return False

def get_followups(path):
    entries = parse_pipeline(path)
    followups = []
    for e in entries:
        if e["stage"] == "Applied":
            if "applied" in e.get("fields", {}):
                followups.append({"entry": e["title"], "stage": e["stage"],
                                  "action": f"Follow up (applied {e['fields']['applied']})"})
        elif e["stage"] in ["Phone Screen", "Interview"]:
            followups.append({"entry": e["title"], "stage": e["stage"],
                              "action": "Prep needed" if e["stage"] == "Interview" else "Confirm scheduling"})
        elif e["stage"] == "Offer":
            followups.append({"entry": e["title"], "stage": e["stage"],
                              "action": "Decision needed — review offer"})

    if followups:
        print("Follow-ups due:\n")
        for i, f in enumerate(followups, 1):
            print(f"  {i}. [{f['stage']}] {f['entry']}")
            print(f"     → {f['action']}")
    else:
        print("No follow-ups due")

    return followups

def export_json(path):
    entries = parse_pipeline(path)
    output = json.dumps(entries, indent=2)
    print(output)
    return entries

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py [status|add|move|followups|export] [pipeline_path] [options]")
        sys.exit(1)

    command = sys.argv[1]
    path = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "PIPELINE.md"

    if command == "status":
        get_status(path)
    elif command == "followups":
        get_followups(path)
    elif command == "export":
        export_json(path)
    elif command == "add":
        kwargs = {}
        args = sys.argv[2:]
        i = 0
        while i < len(args):
            if args[i].startswith("--"):
                key = args[i][2:]
                val = args[i + 1] if i + 1 < len(args) else None
                kwargs[key] = val
                i += 2
            else:
                if "path" not in kwargs:
                    path = args[i]
                i += 1
        add_entry(path, kwargs.get("company", ""), kwargs.get("role", ""),
                  kwargs.get("stage", "Discovered"), kwargs.get("comp"),
                  kwargs.get("location"), kwargs.get("url"), kwargs.get("notes"))
    elif command == "move":
        kwargs = {}
        args = sys.argv[3:] if len(sys.argv) > 3 else []
        i = 0
        while i < len(args):
            if args[i].startswith("--"):
                key = args[i][2:]
                val = args[i + 1] if i + 1 < len(args) else None
                kwargs[key] = val
                i += 2
            else:
                i += 1
        move_entry(path, kwargs.get("company", ""), kwargs.get("to", "Applied"))
    else:
        print(f"Unknown command: {command}")
