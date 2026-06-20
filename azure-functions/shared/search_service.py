from pathlib import Path
from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from shared.config import env, search_configured

SKILLS_INDEX_PATH = Path(__file__).resolve().parents[2] / "data" / "skills" / "skills_index.json"
_local_cache: list[dict[str, Any]] | None = None


def _client() -> SearchClient:
    return SearchClient(
        endpoint=env("AZURE_SEARCH_ENDPOINT"),
        index_name=env("AZURE_SEARCH_INDEX", "skills-index"),
        credential=AzureKeyCredential(env("AZURE_SEARCH_KEY")),
    )


def _load_local_index() -> list[dict[str, Any]]:
    global _local_cache
    if _local_cache is None:
        import json

        _local_cache = json.loads(SKILLS_INDEX_PATH.read_text(encoding="utf-8"))
    return _local_cache


def _local_skills_for_roles(target_roles: list[str], top: int = 20) -> list[dict[str, Any]]:
    if not SKILLS_INDEX_PATH.exists():
        return []

    roles = {r.lower() for r in target_roles if r}
    hits: list[dict[str, Any]] = []
    for doc in _load_local_index():
        if doc.get("roleTitle", "").lower() in roles:
            hits.append(doc)
        if len(hits) >= top:
            break
    return hits


def search_skills_for_roles(target_roles: list[str], top: int = 15) -> list[dict[str, Any]]:
    if search_configured() and target_roles:
        role_filter = " or ".join(
            f"roleTitle eq '{role.replace(chr(39), chr(39) + chr(39))}'" for role in target_roles[:3]
        )
        query = " ".join(target_roles)

        results = _client().search(
            search_text=query or "*",
            filter=role_filter if role_filter else None,
            top=top,
            select=[
                "roleTitle",
                "skillName",
                "skillCategory",
                "skillImportance",
                "skillDescription",
                "typicalSalary",
                "growthOutlook",
            ],
        )
        return [dict(r) for r in results]

    return _local_skills_for_roles(target_roles, top)


def collect_target_roles(profile: dict[str, Any], career_summary: dict[str, Any]) -> list[str]:
    roles = list(profile.get("targetRoles") or [])
    for item in career_summary.get("recommendedRoles") or []:
        title = item.get("title") if isinstance(item, dict) else None
        if title and title not in roles:
            roles.append(title)
    return roles
