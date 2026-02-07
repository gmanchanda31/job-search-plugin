"""
Compute job search analytics from memory/analytics/ files.
Shows conversion rates, time-in-stage, and trends.

Usage:
    python scripts/analytics.py [workspace_dir] [--format md|json]
"""
import re
import sys
import json
from pathlib import Path
from datetime import datetime


def parse_analytics_table(path):
    """Parse a markdown table into list of dicts."""
    if not path.exists():
        return []
    text = path.read_text()
    rows = []
    headers = []
    header_found = False

    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            if header_found and not line:
                break  # End of table
            continue

        if "|" in line:
            parts = [p.strip() for p in line.split("|")]
            # Remove empty strings from split
            parts = [p for p in parts if p]

            if not headers and parts:
                headers = [h.lower().replace(" ", "_") for h in parts]
                header_found = True
                continue

            # Skip separator line
            if header_found and all(c in "-| " for c in line):
                continue

            if header_found and parts:
                row = {}
                for i, h in enumerate(headers):
                    row[h] = parts[i] if i < len(parts) else ""
                rows.append(row)

    return rows


def compute_analytics(workspace_dir=None, fmt="md"):
    """Compute and display job search analytics."""
    if workspace_dir is None:
        workspace_dir = "."
    workspace = Path(workspace_dir)

    analytics_dir = workspace / "memory" / "analytics"

    if not analytics_dir.exists():
        print("No analytics directory found. Run /job-search:start first.")
        return None

    applications = parse_analytics_table(analytics_dir / "applications.md")
    interviews = parse_analytics_table(analytics_dir / "interviews.md")
    offers = parse_analytics_table(analytics_dir / "offers.md")
    briefings = parse_analytics_table(analytics_dir / "briefings.md")

    # Compute stats
    total_apps = len(applications)
    active_apps = len([a for a in applications if a.get("outcome", "").lower() in ["active", ""]])
    closed_apps = len([a for a in applications if a.get("outcome", "").lower() in ["rejected", "closed", "withdrawn"]])
    interview_count = len(interviews)
    offer_count = len(offers)
    accepted_offers = len([o for o in offers if o.get("decision", "").lower() == "accepted"])

    # Conversion rates
    app_to_interview = (interview_count / total_apps * 100) if total_apps > 0 else 0
    interview_to_offer = (offer_count / interview_count * 100) if interview_count > 0 else 0
    app_to_offer = (offer_count / total_apps * 100) if total_apps > 0 else 0

    # Stage distribution from applications
    stage_dist = {}
    for app in applications:
        stage = app.get("stage_reached", "Unknown")
        stage_dist[stage] = stage_dist.get(stage, 0) + 1

    # Source distribution
    source_dist = {}
    for app in applications:
        source = app.get("source", "Unknown")
        source_dist[source] = source_dist.get(source, 0) + 1

    # Method distribution
    method_dist = {}
    for app in applications:
        method = app.get("method", "Unknown")
        method_dist[method] = method_dist.get(method, 0) + 1

    # Average days active
    days_active_list = []
    for app in applications:
        try:
            days = int(app.get("days_active", 0))
            if days > 0:
                days_active_list.append(days)
        except (ValueError, TypeError):
            pass
    avg_days = sum(days_active_list) / len(days_active_list) if days_active_list else 0

    if fmt == "json":
        result = {
            "total_applications": total_apps,
            "active": active_apps,
            "closed": closed_apps,
            "interviews": interview_count,
            "offers": offer_count,
            "accepted": accepted_offers,
            "conversion": {
                "app_to_interview": round(app_to_interview, 1),
                "interview_to_offer": round(interview_to_offer, 1),
                "app_to_offer": round(app_to_offer, 1),
            },
            "avg_days_active": round(avg_days, 1),
            "stage_distribution": stage_dist,
            "source_distribution": source_dist,
            "method_distribution": method_dist,
            "briefings_generated": len(briefings),
        }
        print(json.dumps(result, indent=2))
        return result

    # Markdown output
    report = f"""# Job Search Analytics

> Generated: {datetime.now().strftime("%B %d, %Y")}

## Overview
- Total applications: {total_apps}
- Active: {active_apps}
- Closed: {closed_apps}
- Interviews: {interview_count}
- Offers: {offer_count}
- Accepted: {accepted_offers}
- Average days active: {avg_days:.0f}

## Conversion Funnel
- Applications -> Interviews: {app_to_interview:.1f}%
- Interviews -> Offers: {interview_to_offer:.1f}%
- Applications -> Offers: {app_to_offer:.1f}%
"""

    if source_dist:
        report += "\n## Sources\n"
        for source, count in sorted(source_dist.items(), key=lambda x: x[1], reverse=True):
            pct = count / total_apps * 100 if total_apps > 0 else 0
            report += f"- {source}: {count} ({pct:.0f}%)\n"

    if method_dist:
        report += "\n## Application Methods\n"
        for method, count in sorted(method_dist.items(), key=lambda x: x[1], reverse=True):
            pct = count / total_apps * 100 if total_apps > 0 else 0
            report += f"- {method}: {count} ({pct:.0f}%)\n"

    report += "\n## Recommendations\n"
    if total_apps == 0:
        report += "- No applications yet. Run `/job-search:find` to discover roles.\n"
    elif app_to_interview < 20:
        report += "- Low interview rate ({:.0f}%). Consider tailoring resumes more or trying direct outreach.\n".format(app_to_interview)
    elif interview_to_offer < 30 and interview_count >= 3:
        report += "- Interview-to-offer conversion is low ({:.0f}%). Run `/job-search:prep` for deeper preparation.\n".format(interview_to_offer)

    if total_apps > 10 and offer_count == 0:
        report += "- {0} applications with no offers. Consider narrowing focus or adjusting target companies.\n".format(total_apps)

    if source_dist:
        best_source = max(source_dist, key=source_dist.get)
        report += f"- Top source: {best_source} ({source_dist[best_source]} apps). Double down here.\n"

    if method_dist and "referral" in [m.lower() for m in method_dist]:
        ref_key = next(m for m in method_dist if m.lower() == "referral")
        report += f"- Referrals: {method_dist[ref_key]} used. Referrals typically have 3-5x higher conversion.\n"

    report += f"\n## Activity\n- Briefings generated: {len(briefings)}\n"

    print(report)
    return report


if __name__ == "__main__":
    workspace = None
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
            workspace = arg

    compute_analytics(workspace, fmt)
