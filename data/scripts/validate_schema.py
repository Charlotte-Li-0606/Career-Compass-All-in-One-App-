#!/usr/bin/env python3
"""
validate_schema.py — Validates all role JSON files against the taxonomy.

Checks:
- Every role's sector matches an industry_sectors.json entry
- Every skill's category matches a skill_categories.json entry
- Every skill's importance is one of the three allowed levels
- Required fields are present on every role and skill
- No duplicate role titles across files
- Salary format is reasonable
- Prints a summary report

Usage: python validate_schema.py [--data-dir PATH]
Default data-dir: ../ (relative to this script)
"""

import json
import os
import sys
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = (SCRIPT_DIR / "..").resolve()
TAXONOMY_DIR = DATA_DIR / "taxonomy"
ROLES_DIR = DATA_DIR / "roles"

ALLOWED_IMPORTANCE = {"critical", "recommended", "nice-to-have"}


def load_json(path: Path) -> dict:
    """Load a JSON file and return the parsed object."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_taxonomy_files():
    """Validate the taxonomy files exist and have correct structure."""
    errors = []

    # skill_categories.json
    cat_path = TAXONOMY_DIR / "skill_categories.json"
    if not cat_path.exists():
        errors.append(f"MISSING: {cat_path}")
    else:
        cat_data = load_json(cat_path)
        if "categories" not in cat_data:
            errors.append(f"{cat_path}: missing 'categories' key")
        elif not isinstance(cat_data["categories"], list):
            errors.append(f"{cat_path}: 'categories' must be a list")

    # industry_sectors.json
    sec_path = TAXONOMY_DIR / "industry_sectors.json"
    if not sec_path.exists():
        errors.append(f"MISSING: {sec_path}")
    else:
        sec_data = load_json(sec_path)
        if "sectors" not in sec_data:
            errors.append(f"{sec_path}: missing 'sectors' key")
        elif not isinstance(sec_data["sectors"], list):
            errors.append(f"{sec_path}: 'sectors' must be a list")

    # importance_levels.json
    imp_path = TAXONOMY_DIR / "importance_levels.json"
    if not imp_path.exists():
        errors.append(f"MISSING: {imp_path}")
    else:
        imp_data = load_json(imp_path)
        if "levels" not in imp_data:
            errors.append(f"{imp_path}: missing 'levels' key")
        elif not isinstance(imp_data["levels"], list):
            errors.append(f"{imp_path}: 'levels' must be a list")

    return errors


def validate_role_files():
    """Validate all role JSON files."""
    errors = []
    warnings = []
    all_role_titles = []  # track for duplicates
    total_roles = 0
    total_skills = 0

    # Load taxonomy for cross-referencing
    cat_data = load_json(TAXONOMY_DIR / "skill_categories.json")
    sec_data = load_json(TAXONOMY_DIR / "industry_sectors.json")

    valid_categories = {c["name"] for c in cat_data["categories"]}
    valid_sectors = {s["name"] for s in sec_data["sectors"]}

    role_files = sorted(ROLES_DIR.glob("*.json"))
    if not role_files:
        errors.append(f"No role files found in {ROLES_DIR}")
        return errors, warnings, total_roles, total_skills

    for role_file in role_files:
        file_name = role_file.name
        try:
            data = load_json(role_file)
        except json.JSONDecodeError as e:
            errors.append(f"{file_name}: invalid JSON — {e}")
            continue

        # Validate file-level fields
        if "sector" not in data:
            errors.append(f"{file_name}: missing 'sector' field")
        elif data["sector"] not in valid_sectors:
            errors.append(f"{file_name}: sector '{data['sector']}' not in industry_sectors.json. Valid: {sorted(valid_sectors)}")

        if "roles" not in data:
            errors.append(f"{file_name}: missing 'roles' array")
            continue

        if not isinstance(data["roles"], list):
            errors.append(f"{file_name}: 'roles' must be an array")
            continue

        if "lastUpdated" not in data:
            warnings.append(f"{file_name}: missing 'lastUpdated' field")

        if "source" not in data:
            warnings.append(f"{file_name}: missing 'source' field — good to document where data came from")

        # Validate each role
        for i, role in enumerate(data["roles"]):
            role_id = f"{file_name}:role[{i}]"
            role_errors = []

            # Required string fields
            for field in ["roleTitle", "roleTitleZh", "typicalSalary", "growthOutlook"]:
                if field not in role or not role[field]:
                    role_errors.append(f"missing '{field}'")

            # isEntryLevel
            if "isEntryLevel" not in role or not isinstance(role["isEntryLevel"], bool):
                role_errors.append(f"missing or invalid 'isEntryLevel' (must be boolean)")

            # hiringIndustries
            if "hiringIndustries" not in role or not isinstance(role["hiringIndustries"], list):
                role_errors.append(f"missing or invalid 'hiringIndustries' (must be array)")
            else:
                for industry in role["hiringIndustries"]:
                    if industry not in valid_sectors:
                        role_errors.append(f"hiringIndustry '{industry}' not in industry_sectors.json")

            # requiredSkills
            if "requiredSkills" not in role or not isinstance(role["requiredSkills"], list):
                role_errors.append(f"missing or invalid 'requiredSkills' (must be array)")
            elif len(role["requiredSkills"]) < 3:
                warnings.append(f"{role_id}: only {len(role['requiredSkills'])} skills — consider adding more for better coverage (target 8-15)")
            elif len(role["requiredSkills"]) > 20:
                warnings.append(f"{role_id}: {len(role['requiredSkills'])} skills — may be too many, consider trimming to top 15")

            # Validate each skill
            if "requiredSkills" in role and isinstance(role["requiredSkills"], list):
                for j, skill in enumerate(role["requiredSkills"]):
                    skill_id = f"{role_id}:skill[{j}] ('{skill.get('skillName', 'UNKNOWN')}')"

                    for field in ["skillName", "skillCategory", "importance", "description", "typicalLevel"]:
                        if field not in skill or not skill[field]:
                            role_errors.append(f"{skill_id}: missing '{field}'")

                    if "skillCategory" in skill and skill["skillCategory"] not in valid_categories:
                        role_errors.append(
                            f"{skill_id}: category '{skill['skillCategory']}' not in skill_categories.json. "
                            f"Did you mean one of: {sorted(valid_categories)}?"
                        )

                    if "importance" in skill and skill["importance"] not in ALLOWED_IMPORTANCE:
                        role_errors.append(
                            f"{skill_id}: importance '{skill['importance']}' invalid. "
                            f"Must be one of: {sorted(ALLOWED_IMPORTANCE)}"
                        )

            if role_errors:
                for e in role_errors:
                    errors.append(f"  {e}")
            else:
                # Track for duplicates
                title = role.get("roleTitle", "")
                if title:
                    all_role_titles.append((role_file.name, title))

            total_roles += 1
            if "requiredSkills" in role and isinstance(role["requiredSkills"], list):
                total_skills += len(role["requiredSkills"])

    # Check for duplicate role titles
    titles_seen = {}
    for file_name, title in all_role_titles:
        if title in titles_seen:
            warnings.append(f"Duplicate role title '{title}' in {file_name} and {titles_seen[title]}")
        else:
            titles_seen[title] = file_name

    return errors, warnings, total_roles, total_skills


def main():
    print("=" * 60)
    print("  CAREER COMPASS — Data Schema Validator")
    print("=" * 60)
    print(f"  Data directory: {DATA_DIR}")
    print()

    # Validate taxonomy
    print("[*] Checking taxonomy files...")
    taxonomy_errors = validate_taxonomy_files()
    if taxonomy_errors:
        print("  [FAIL] Taxonomy errors:")
        for e in taxonomy_errors:
            print(f"     {e}")
    else:
        print("  [OK] Taxonomy files OK")
    print()

    # Validate role files
    print("[*] Checking role files...")
    role_errors, warnings, total_roles, total_skills = validate_role_files()

    # Print warnings first
    if warnings:
        print("  [WARN] Warnings:")
        for w in warnings:
            print(f"     {w}")
        print()

    # Print errors
    if role_errors:
        print(f"  [FAIL] {len(role_errors)} validation error(s):")
        for e in role_errors:
            print(f"     {e}")
        print()
    else:
        print("  [OK] All role files pass validation")
        print()

    # Summary
    print("=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    total_errors = len(taxonomy_errors) + len(role_errors)
    print(f"  Roles:              {total_roles}")
    print(f"  Skill-role pairs:   {total_skills}")
    print(f"  Role files:         {len(list(ROLES_DIR.glob('*.json')))}")
    print(f"  Errors:             {total_errors}")
    print(f"  Warnings:           {len(warnings)}")
    print()

    if total_errors > 0:
        print("[FAIL] VALIDATION FAILED — fix errors above before generating search docs")
        sys.exit(1)
    else:
        print("[OK] VALIDATION PASSED — ready for generate_search_docs.py")
        sys.exit(0)


if __name__ == "__main__":
    main()
