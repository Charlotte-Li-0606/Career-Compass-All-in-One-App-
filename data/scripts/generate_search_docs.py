#!/usr/bin/env python3
"""
generate_search_docs.py — Transforms curated role JSON files into flat,
denormalized AI Search documents (one per skill-role pair).

Output: ../skills/skills_index.json — an array of documents ready for
Azure AI Search ingestion.

Each document has a composite id: {normalized-role-title}~{normalized-skill-name}
This enables unique identification and upsert operations.

Usage: python generate_search_docs.py [--data-dir PATH]
Default data-dir: ../ (relative to this script)
"""

import json
import os
import re
import sys
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = (SCRIPT_DIR / "..").resolve()
ROLES_DIR = DATA_DIR / "roles"
SKILLS_DIR = DATA_DIR / "skills"
OUTPUT_FILE = SKILLS_DIR / "skills_index.json"


def load_json(path: Path) -> dict:
    """Load a JSON file and return the parsed object."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_key(s: str) -> str:
    """Normalize a string for use in a composite key: lowercase, spaces→hyphens, remove special chars."""
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9\s\-]', '', s)
    s = re.sub(r'\s+', '-', s)
    return s


def generate_search_docs():
    """Read all role files and generate flat AI Search documents."""
    role_files = sorted(ROLES_DIR.glob("*.json"))
    if not role_files:
        print(f"ERROR: No role files found in {ROLES_DIR}")
        return []

    all_docs = []
    stats = {"roles": 0, "skills": 0, "documents": 0}

    for role_file in role_files:
        data = load_json(role_file)
        sector = data.get("sector", "")
        sub_sector = data.get("subSector", "")
        source = data.get("source", "")

        for role in data.get("roles", []):
            stats["roles"] += 1
            role_title = role.get("roleTitle", "")
            role_title_zh = role.get("roleTitleZh", "")
            is_entry_level = role.get("isEntryLevel", True)
            typical_salary = role.get("typicalSalary", "")
            growth_outlook = role.get("growthOutlook", "")
            hiring_industries = role.get("hiringIndustries", [])

            # Build keywords: role title words + common synonyms
            keywords = [w.lower() for w in role_title.split()]
            keywords.extend(["graduate", "entry-level", "junior", "fresh-graduate", "hong-kong"])
            keywords = list(set(keywords))  # deduplicate

            for skill in role.get("requiredSkills", []):
                stats["skills"] += 1
                skill_name = skill.get("skillName", "")
                skill_category = skill.get("skillCategory", "")
                skill_importance = skill.get("importance", "")
                skill_description = skill.get("description", "")
                skill_level = skill.get("typicalLevel", "")

                # Add skill name to keywords
                skill_keywords = list(keywords)
                skill_keywords.extend([w.lower() for w in skill_name.split()])
                skill_keywords = list(set(skill_keywords))

                doc = {
                    "id": f"{normalize_key(role_title)}~{normalize_key(skill_name)}",
                    "roleTitle": role_title,
                    "roleTitleZh": role_title_zh,
                    "sector": sector,
                    "subSector": sub_sector,
                    "skillName": skill_name,
                    "skillCategory": skill_category,
                    "skillImportance": skill_importance,
                    "skillDescription": skill_description,
                    "skillLevel": skill_level,
                    "typicalSalary": typical_salary,
                    "growthOutlook": growth_outlook,
                    "hiringIndustries": hiring_industries,
                    "isEntryLevel": is_entry_level,
                    "keywords": skill_keywords,
                    "source": source
                }
                all_docs.append(doc)

    stats["documents"] = len(all_docs)
    return all_docs, stats


def generate_summary(stats: dict):
    """Generate a summary JSON for reference."""
    role_files = sorted(ROLES_DIR.glob("*.json"))
    roles_summary = []

    for role_file in role_files:
        data = load_json(role_file)
        for role in data.get("roles", []):
            roles_summary.append({
                "roleTitle": role.get("roleTitle"),
                "roleTitleZh": role.get("roleTitleZh"),
                "sector": data.get("sector"),
                "skillCount": len(role.get("requiredSkills", [])),
                "isEntryLevel": role.get("isEntryLevel", True)
            })

    summary = {
        "generatedAt": "2026-06-13",
        "totalDocuments": stats["documents"],
        "totalRoles": stats["roles"],
        "totalSkillRolePairs": stats["skills"],
        "roleFiles": [f.name for f in role_files],
        "roles": roles_summary
    }
    return summary


def main():
    print("=" * 60)
    print("  CAREER COMPASS — Search Document Generator")
    print("=" * 60)
    print(f"  Source: {ROLES_DIR}")
    print(f"  Output: {OUTPUT_FILE}")
    print()

    # Generate documents
    print("[*] Generating search documents...")
    docs, stats = generate_search_docs()

    if not docs:
        print("ERROR: No documents generated. Check role files.")
        sys.exit(1)

    print(f"  [OK] Generated {stats['documents']} documents")
    print(f"     from {stats['roles']} roles")
    print(f"     across {len([f for f in ROLES_DIR.glob('*.json')])} role files")
    print()

    # Ensure output directory exists
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    # Write search documents
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

    print(f"[FILE] Wrote {OUTPUT_FILE}")
    print(f"   ({os.path.getsize(OUTPUT_FILE):,} bytes)")
    print()

    # Generate and write summary
    summary = generate_summary(stats)
    summary_path = SKILLS_DIR / "skills_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"[FILE] Wrote {summary_path}")
    print()

    # Print per-file breakdown
    print("=" * 60)
    print("  DOCUMENTS BY ROLE")
    print("=" * 60)
    for role_info in summary["roles"]:
        entry_tag = "[GRAD]" if role_info["isEntryLevel"] else "[EXP]"
        print(f"  {entry_tag} {role_info['roleTitle']} ({role_info['sector']}): {role_info['skillCount']} skills")
    print()

    print("=" * 60)
    print(f"  TOTAL: {stats['documents']} search documents ready for Azure AI Search")
    print("=" * 60)


if __name__ == "__main__":
    main()
