"""
Rebuild CLAUDE.md hot cache from deep storage files.
Scans PIPELINE.md, JOBSEARCH.md, memory/glossary.md, and memory/ directories
to construct an up-to-date hot cache.

Usage:
    python scripts/memory_sync.py [workspace_dir]
"""
import re
import sys
from pathlib import Path
from datetime import datetime

STAGES = ["Discovered", "Researching", "Applied", "Phone Screen", "Interview", "Offer", "Declined / Rejected"]
ACTIVE_STAGES = ["Discovered", "Researching", "Applied", "Phone Screen", "Interview", "Offer"]


def parse_pipeline_entries(path):
    """Extract active entries from PIPELINE.md."""
    if not path.exists():
        return []
    text = path.read_text()
    entries = []
    current_stage = None

    for line in text.split("\n"):
        stage_match = re.match(r"^## (.+)$", line.strip())
        if stage_match:
            stage_name = stage_match.group(1).strip()
            if stage_name in STAGES:
                current_stage = stage_name
            continue

        if line.strip().startswith("- [") and current_stage and current_stage in ACTIVE_STAGES:
            title_match = re.search(r"\*\*(.+?)\*\*", line)
            title = title_match.group(1) if title_match else "Unknown"

            # Try to extract role and company from "Role — Company" format
            parts = title.split(" — ")
            if len(parts) >= 2:
                role = parts[0].strip()
                company = parts[1].strip()
            else:
                role = title
                company = "Unknown"

            # Try to extract deadline or next action from fields
            deadline = "—"
            next_action = "—"
            raw_parts = [p.strip() for p in line.split("|")]
            for p in raw_parts:
                if p.startswith("Scheduled:") or p.startswith("Deadline:"):
                    deadline = p.split(":", 1)[1].strip()
                elif p.startswith("Next:"):
                    next_action = p.split(":", 1)[1].strip()

            entries.append({
                "company": company,
                "role": role,
                "stage": current_stage,
                "deadline": deadline,
                "next_action": next_action,
            })

    return entries


def parse_profile(path):
    """Extract key profile info from JOBSEARCH.md."""
    if not path.exists():
        return {}
    text = path.read_text()
    profile = {"name": "", "floor": "", "notice": "", "optimizing": ""}

    current_section = None
    for line in text.split("\n"):
        if line.startswith("## "):
            current_section = line.strip("# ").strip().lower()
            continue

        if current_section == "about me" and line.strip() and not line.startswith("<!--"):
            if not profile["name"]:
                profile["name"] = line.strip()

        if current_section == "compensation":
            if "Base floor" in line and "|" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    profile["floor"] = parts[2].strip()

        if current_section == "target":
            if "Notice" in line and "|" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    profile["notice"] = parts[2].strip()

        if current_section == "preferences":
            if line.strip().startswith("- ") and not line.startswith("<!--"):
                if "optimizing" in line.lower() or "Optimizing" in line:
                    profile["optimizing"] = line.strip().lstrip("- ").strip()

    return profile


def parse_glossary_contacts(path):
    """Extract contacts from glossary.md."""
    if not path.exists():
        return []
    text = path.read_text()
    contacts = []
    in_contacts = False

    for line in text.split("\n"):
        if "## Contacts" in line:
            in_contacts = True
            continue
        if line.startswith("## ") and in_contacts:
            in_contacts = False
            continue

        if in_contacts and "|" in line and not line.strip().startswith("|--") and not "Name" in line.split("|")[1] if len(line.split("|")) > 1 else True:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 3:
                contacts.append({
                    "name": parts[0],
                    "company": parts[1],
                    "role": parts[2],
                    "last_contact": parts[3] if len(parts) > 3 else "—",
                    "notes": parts[4] if len(parts) > 4 else "",
                })

    return contacts


def parse_glossary_terms(path):
    """Extract terms from glossary.md."""
    if not path.exists():
        return []
    text = path.read_text()
    terms = []
    in_terms = False

    for line in text.split("\n"):
        if "## Terms" in line:
            in_terms = True
            continue
        if line.startswith("## ") and in_terms:
            in_terms = False
            continue

        if in_terms and "|" in line and not line.strip().startswith("|--"):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2 and parts[0] != "Term":
                terms.append({"term": parts[0], "meaning": parts[1]})

    return terms


def get_preferences(path):
    """Extract preferences section from JOBSEARCH.md."""
    if not path.exists():
        return []
    text = path.read_text()
    lines = []
    in_prefs = False
    for line in text.split("\n"):
        if "## Preferences" in line:
            in_prefs = True
            continue
        if line.startswith("## ") and in_prefs:
            break
        if in_prefs and line.strip() and not line.startswith("<!--"):
            lines.append(line)
    return lines


def rebuild_claude_md(workspace_dir=None):
    """Rebuild CLAUDE.md from all memory sources."""
    if workspace_dir is None:
        workspace_dir = "."
    workspace = Path(workspace_dir)

    now = datetime.now().strftime("%B %d, %Y")

    # Gather data
    profile = parse_profile(workspace / "JOBSEARCH.md")
    entries = parse_pipeline_entries(workspace / "PIPELINE.md")
    glossary_path = workspace / "memory" / "glossary.md"
    contacts = parse_glossary_contacts(glossary_path)
    terms = parse_glossary_terms(glossary_path)
    prefs = get_preferences(workspace / "JOBSEARCH.md")

    # Build CLAUDE.md
    lines = [
        "# Job Search Memory",
        "",
        f"> Last updated: {now}",
        "",
        "## Searcher",
    ]

    if profile.get("name"):
        lines.append(profile["name"])
        extras = []
        if profile.get("floor"):
            extras.append(f"Floor: {profile['floor']}")
        if profile.get("notice"):
            extras.append(f"Notice: {profile['notice']}")
        if profile.get("optimizing"):
            extras.append(profile["optimizing"])
        if extras:
            lines.append(" | ".join(extras))
    else:
        lines.append("<!-- Run /job-search:start to fill profile -->")

    # Active targets (cap at 15)
    lines.extend(["", "## Active Targets"])
    lines.append("| Company | Role | Stage | Next Action | Deadline |")
    lines.append("|---------|------|-------|-------------|----------|")
    for entry in entries[:15]:
        lines.append(
            f"| {entry['company']} | {entry['role']} | {entry['stage']} "
            f"| {entry['next_action']} | {entry['deadline']} |"
        )

    # Key contacts (cap at 15)
    lines.extend(["", "## Key Contacts"])
    lines.append("| Who | At | Role | Last Contact | Notes |")
    lines.append("|-----|-----|------|-------------|-------|")
    for contact in contacts[:15]:
        lines.append(
            f"| {contact['name']} | {contact['company']} | {contact['role']} "
            f"| {contact.get('last_contact', '—')} | {contact.get('notes', '')} |"
        )

    # Quick reference terms (cap at 20)
    lines.extend(["", "## Quick Reference"])
    lines.append("| Term | Meaning |")
    lines.append("|------|---------|")
    for term in terms[:20]:
        lines.append(f"| {term['term']} | {term['meaning']} |")

    # Preferences
    lines.extend(["", "## Preferences"])
    if prefs:
        lines.extend(prefs)
    else:
        lines.append("<!-- Filled during /start intake -->")

    lines.append("")

    # Write
    claude_md = workspace / "CLAUDE.md"
    claude_md.write_text("\n".join(lines))

    print(f"CLAUDE.md rebuilt — {now}")
    print(f"  Active targets: {len(entries)}")
    print(f"  Contacts: {len(contacts)}")
    print(f"  Terms: {len(terms)}")

    return {
        "targets": len(entries),
        "contacts": len(contacts),
        "terms": len(terms),
    }


if __name__ == "__main__":
    workspace = sys.argv[1] if len(sys.argv) > 1 else None
    rebuild_claude_md(workspace)
