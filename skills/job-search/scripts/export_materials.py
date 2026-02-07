"""
Export all application materials for a specific company/role into a single folder.
Collects resume, cover letter, outreach drafts, research, and fit analysis.

Usage:
    python scripts/export_materials.py --company "Razorpay" --role "Senior PM" \
        [--workspace .] [--output ./exports/razorpay-senior-pm]
"""
import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime

def export_materials(company, role, workspace=".", output=None):
    workspace = Path(workspace)
    slug = f"{company.lower().replace(' ', '-')}-{role.lower().replace(' ', '-')}"

    if output is None:
        output = workspace / "exports" / slug
    else:
        output = Path(output)

    output.mkdir(parents=True, exist_ok=True)

    collected = []
    missing = []

    # 1. Company research
    company_slug = company.lower().replace(" ", "-")
    research_path = workspace / "memory" / "companies" / f"{company_slug}.md"
    if research_path.exists():
        shutil.copy2(research_path, output / "company_research.md")
        collected.append("company_research.md")
    else:
        missing.append("Company research (run /research first)")

    # 2. Application materials
    app_dir = workspace / "memory" / "applications" / slug
    if app_dir.exists():
        for f in app_dir.iterdir():
            shutil.copy2(f, output / f.name)
            collected.append(f.name)
    else:
        # Check without exact slug match
        apps_dir = workspace / "memory" / "applications"
        if apps_dir.exists():
            for d in apps_dir.iterdir():
                if company.lower() in d.name.lower():
                    for f in d.iterdir():
                        shutil.copy2(f, output / f.name)
                        collected.append(f.name)
                    break
        if not collected or collected == ["company_research.md"]:
            missing.append("Application materials (run /apply first)")

    # 3. Contact info
    contacts_dir = workspace / "memory" / "contacts"
    if contacts_dir.exists():
        for f in contacts_dir.iterdir():
            if company.lower() in f.name.lower():
                shutil.copy2(f, output / f"contact_{f.name}")
                collected.append(f"contact_{f.name}")

    # 4. JOBSEARCH.md profile (for reference)
    profile = workspace / "JOBSEARCH.md"
    if profile.exists():
        shutil.copy2(profile, output / "my_profile.md")
        collected.append("my_profile.md")

    # 5. Generate index
    index_content = f"""# Application Package: {role} @ {company}

**Exported:** {datetime.now().strftime("%B %d, %Y")}

## Contents

"""
    for f in sorted(collected):
        index_content += f"- [{f}](./{f})\n"

    if missing:
        index_content += f"\n## Missing (run these commands)\n\n"
        for m in missing:
            index_content += f"- {m}\n"

    (output / "INDEX.md").write_text(index_content)
    collected.append("INDEX.md")

    print(f"Application Package: {role} @ {company}")
    print(f"Exported to: {output}")
    print(f"\nCollected {len(collected)} files:")
    for f in collected:
        print(f"  ✓ {f}")
    if missing:
        print(f"\nMissing {len(missing)} items:")
        for m in missing:
            print(f"  ✗ {m}")

    return {"output": str(output), "collected": collected, "missing": missing}

if __name__ == "__main__":
    kwargs = {}
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            kwargs[args[i][2:]] = args[i + 1]
            i += 2
        else:
            i += 1

    if "company" not in kwargs or "role" not in kwargs:
        print("Usage: python export_materials.py --company 'X' --role 'Y' [--workspace .] [--output path]")
        sys.exit(1)

    export_materials(**kwargs)
