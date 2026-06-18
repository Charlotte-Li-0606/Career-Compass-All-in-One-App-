from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from shared.config import env, search_configured


def _client() -> SearchClient:
    return SearchClient(
        endpoint=env("AZURE_SEARCH_ENDPOINT"),
        index_name=env("AZURE_SEARCH_INDEX", "skills-index"),
        credential=AzureKeyCredential(env("AZURE_SEARCH_KEY")),
    )


def search_skills_for_roles(target_roles: list[str], top: int = 15) -> list[dict[str, Any]]:
    if not search_configured() or not target_roles:
        return []

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
