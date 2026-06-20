import json
import os
from pathlib import Path


def load_local_settings() -> None:
    """Load azure-functions/local.settings.json into os.environ."""
    settings_path = Path(__file__).resolve().parents[1] / "local.settings.json"
    if not settings_path.exists():
        return
    data = json.loads(settings_path.read_text(encoding="utf-8"))
    for key, value in data.get("Values", {}).items():
        os.environ.setdefault(key, str(value))


load_local_settings()


def env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def is_demo_mode() -> bool:
    return env("DEMO_MODE", "false").lower() == "true"


def cosmos_configured() -> bool:
    endpoint = env("COSMOS_ENDPOINT")
    key = env("COSMOS_KEY")
    if not endpoint or not key:
        return False
    placeholders = ("paste ", "your_", "YOUR-", "here")
    return not any(p in endpoint.lower() or p in key.lower() for p in placeholders)


def search_configured() -> bool:
    endpoint = env("AZURE_SEARCH_ENDPOINT")
    key = env("AZURE_SEARCH_KEY")
    if not endpoint or not key:
        return False
    placeholders = ("paste ", "your_", "YOUR-", "here")
    return not any(p in endpoint.lower() or p in key.lower() for p in placeholders)
