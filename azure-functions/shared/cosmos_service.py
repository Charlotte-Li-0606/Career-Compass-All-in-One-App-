from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from azure.cosmos import CosmosClient, PartitionKey

from shared.config import cosmos_configured, env


_client: CosmosClient | None = None


def _get_client() -> CosmosClient:
    global _client
    if _client is None:
        _client = CosmosClient(env("COSMOS_ENDPOINT"), credential=env("COSMOS_KEY"))
    return _client


def _database():
    db_name = env("COSMOS_DATABASE", "career-compass")
    return _get_client().get_database_client(db_name)


def _profiles_container():
    name = env("COSMOS_PROFILES_CONTAINER", "student_profiles")
    return _database().get_container_client(name)


def _resumes_container():
    name = env("COSMOS_RESUMES_CONTAINER", "resumes")
    return _database().get_container_client(name)


def ensure_containers() -> None:
    """Create database and containers if missing (run once during setup)."""
    if not cosmos_configured():
        raise RuntimeError("Cosmos DB is not configured")

    db_name = env("COSMOS_DATABASE", "career-compass")
    client = _get_client()
    db = client.create_database_if_not_exists(id=db_name)

    profiles = env("COSMOS_PROFILES_CONTAINER", "student_profiles")
    resumes = env("COSMOS_RESUMES_CONTAINER", "resumes")

    db.create_container_if_not_exists(
        id=profiles,
        partition_key=PartitionKey(path="/userId"),
    )
    db.create_container_if_not_exists(
        id=resumes,
        partition_key=PartitionKey(path="/userId"),
    )


def upsert_profile(user_id: str, profile: dict[str, Any]) -> dict[str, Any]:
    if not cosmos_configured():
        return profile

    now = datetime.now(timezone.utc).isoformat()
    doc = {
        "id": user_id,
        "userId": user_id,
        **profile,
        "updatedAt": now,
    }
    if "createdAt" not in doc:
        doc["createdAt"] = now

    return _profiles_container().upsert_item(doc)


def get_profile(user_id: str) -> dict[str, Any] | None:
    if not cosmos_configured():
        return None

    try:
        return _profiles_container().read_item(item=user_id, partition_key=user_id)
    except Exception:
        return None


def save_resume_version(user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    if not cosmos_configured():
        return payload

    existing = list(
        _resumes_container().query_items(
            query="SELECT VALUE MAX(c.version) FROM c WHERE c.userId = @uid",
            parameters=[{"name": "@uid", "value": user_id}],
            partition_key=user_id,
        )
    )
    latest = existing[0] if existing and existing[0] is not None else 0
    next_version = latest + 1

    doc = {
        "id": str(uuid4()),
        "userId": user_id,
        "version": next_version,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        **payload,
    }
    return _resumes_container().create_item(doc)
