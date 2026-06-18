#!/usr/bin/env python3
"""One-time setup: create Cosmos DB database and containers."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shared.cosmos_service import ensure_containers
from shared.config import cosmos_configured


def main() -> None:
    if not cosmos_configured():
        print("ERROR: Set COSMOS_ENDPOINT and COSMOS_KEY in local.settings.json")
        sys.exit(1)

    ensure_containers()
    print("Cosmos DB ready: career-compass / student_profiles / resumes")


if __name__ == "__main__":
    main()
