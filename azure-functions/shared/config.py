import os


def env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def is_demo_mode() -> bool:
    return env("DEMO_MODE", "false").lower() == "true"


def cosmos_configured() -> bool:
    return bool(env("COSMOS_ENDPOINT") and env("COSMOS_KEY"))


def search_configured() -> bool:
    return bool(env("AZURE_SEARCH_ENDPOINT") and env("AZURE_SEARCH_KEY"))
