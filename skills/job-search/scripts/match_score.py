"""
Score a job posting against the user's JOBSEARCH.md profile.

Usage:
    python scripts/match_score.py --profile JOBSEARCH.md --title "Senior PM" \
        --company "Razorpay" --industry "Fintech" --location "Bangalore" \
        --comp "₹45L" --stage "Series F" --remote "hybrid"

Returns a match score (0-100) with breakdown and deal-breaker flags.
"""
import re
import sys
import json
from pathlib import Path

def parse_profile(profile_path):
    text = Path(profile_path).read_text()
    profile = {
        "titles": [],
        "industries": [],
        "locations": [],
        "comp_floor": None,
        "comp_currency": "INR",
        "stage_pref": [],
        "avoid": [],
        "watchlist": [],
        "preferences": [],
    }

    current_section = None
    for line in text.split("\n"):
        if line.startswith("## "):
            current_section = line.strip("# ").strip().lower()
            continue

        if current_section == "target":
            if "Titles" in line and "|" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    profile["titles"] = [t.strip() for t in parts[2].split(",") if t.strip()]
            elif "Industries" in line and "|" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    profile["industries"] = [t.strip().lower() for t in parts[2].split(",") if t.strip()]
            elif "Location" in line and "|" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    profile["locations"] = [t.strip().lower() for t in parts[2].split(",") if t.strip() and t.strip() != "|"]
            elif "Stage" in line and "|" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    profile["stage_pref"] = [t.strip().lower() for t in parts[2].split(",") if t.strip()]

        elif current_section == "compensation":
            if "Base floor" in line and "|" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    comp_str = parts[2].strip()
                    numbers = re.findall(r"[\d.]+", comp_str.replace(",", ""))
                    if numbers:
                        profile["comp_floor"] = float(numbers[0])
                    if "$" in comp_str:
                        profile["comp_currency"] = "USD"
                    elif "₹" in comp_str:
                        profile["comp_currency"] = "INR"

        elif current_section == "preferences":
            if line.strip().startswith("- Avoid:") or "avoid" in line.lower():
                avoid_items = line.split(":", 1)[-1] if ":" in line else line
                profile["avoid"] = [a.strip().lower() for a in avoid_items.split(",") if a.strip()]

        elif current_section == "watchlist":
            if line.strip().startswith("- "):
                company = line.strip("- ").strip()
                if company:
                    profile["watchlist"].append(company.lower())

    return profile

def score_job(profile, title="", company="", industry="", location="", comp="", stage="", remote=""):
    score = 0
    breakdown = {}
    deal_breakers = []

    # Title match (0-30 points)
    title_score = 0
    title_lower = title.lower()
    for target_title in profile["titles"]:
        target_lower = target_title.lower()
        # Exact match
        if target_lower in title_lower or title_lower in target_lower:
            title_score = 30
            break
        # Partial match (shared key words)
        target_words = set(target_lower.split())
        title_words = set(title_lower.split())
        overlap = target_words & title_words
        if len(overlap) >= 2:
            title_score = max(title_score, 20)
        elif len(overlap) >= 1:
            title_score = max(title_score, 10)
    breakdown["title"] = title_score
    score += title_score

    # Industry match (0-20 points)
    industry_score = 0
    industry_lower = industry.lower()
    if any(ind in industry_lower for ind in profile["industries"]):
        industry_score = 20
    elif industry_lower:
        industry_score = 5  # Unknown industry, slight positive for breadth
    breakdown["industry"] = industry_score
    score += industry_score

    # Location match (0-15 points)
    location_score = 0
    location_lower = location.lower()
    if any(loc in location_lower for loc in profile["locations"]):
        location_score = 15
    elif "remote" in location_lower:
        location_score = 12  # Remote is usually fine
    elif location_lower:
        location_score = 3
    breakdown["location"] = location_score
    score += location_score

    # Compensation match (0-20 points)
    comp_score = 0
    if comp:
        comp_numbers = re.findall(r"[\d.]+", comp.replace(",", ""))
        if comp_numbers and profile["comp_floor"]:
            comp_val = float(comp_numbers[0])
            floor = profile["comp_floor"]
            if "L" in comp.upper():
                comp_val_normalized = comp_val
                floor_normalized = floor
            elif "K" in comp.upper():
                comp_val_normalized = comp_val
                floor_normalized = floor
            else:
                comp_val_normalized = comp_val
                floor_normalized = floor

            if comp_val_normalized >= floor_normalized:
                comp_score = 20
            elif comp_val_normalized >= floor_normalized * 0.9:
                comp_score = 12  # Close enough, might negotiate
            else:
                comp_score = 0
                deal_breakers.append(f"Comp ({comp}) below floor ({profile['comp_floor']})")
    else:
        comp_score = 10  # Unknown comp, neutral
    breakdown["compensation"] = comp_score
    score += comp_score

    # Watchlist bonus (0-10 points)
    watchlist_score = 0
    if company.lower() in profile["watchlist"]:
        watchlist_score = 10
    breakdown["watchlist"] = watchlist_score
    score += watchlist_score

    # Avoid list check (deal-breaker)
    for avoid_term in profile["avoid"]:
        if avoid_term in industry_lower or avoid_term in company.lower():
            deal_breakers.append(f"Company/industry matches avoid list: {avoid_term}")

    # Stage match (0-5 points)
    stage_score = 0
    if stage and profile["stage_pref"]:
        stage_lower = stage.lower()
        if any(s in stage_lower for s in profile["stage_pref"]):
            stage_score = 5
    breakdown["stage"] = stage_score
    score += stage_score

    # Determine match level
    if deal_breakers:
        match_level = "Deal-Breaker"
    elif score >= 75:
        match_level = "High"
    elif score >= 50:
        match_level = "Medium"
    elif score >= 30:
        match_level = "Low"
    else:
        match_level = "Poor"

    result = {
        "score": score,
        "max_score": 100,
        "match_level": match_level,
        "breakdown": breakdown,
        "deal_breakers": deal_breakers,
        "job": {
            "title": title,
            "company": company,
            "industry": industry,
            "location": location,
            "comp": comp,
        }
    }

    print(f"Match Score: {score}/100 ({match_level})")
    print(f"\nBreakdown:")
    for k, v in breakdown.items():
        bar = "█" * (v // 2) + "░" * ((30 - v) // 2) if v <= 30 else ""
        print(f"  {k:15s}: {v:3d} pts")
    if deal_breakers:
        print(f"\n⚠️  Deal-Breakers:")
        for db in deal_breakers:
            print(f"  - {db}")

    return result

if __name__ == "__main__":
    kwargs = {}
    args = sys.argv[1:]
    i = 0
    profile_path = "JOBSEARCH.md"
    while i < len(args):
        if args[i] == "--profile":
            profile_path = args[i + 1]
            i += 2
        elif args[i].startswith("--"):
            kwargs[args[i][2:]] = args[i + 1]
            i += 2
        else:
            i += 1

    profile = parse_profile(profile_path)
    score_job(profile, **kwargs)
