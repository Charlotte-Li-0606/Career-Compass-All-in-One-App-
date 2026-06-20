#!/usr/bin/env python3
"""
Create Azure AI Search index and upload skills_index.json.

Requires env vars (or .env in repo root):
  AZURE_SEARCH_ENDPOINT
  AZURE_SEARCH_KEY
  AZURE_SEARCH_INDEX  (default: skills-index)

Usage:
  pip install azure-search-documents python-dotenv
  python upload_to_search.py
  python upload_to_search.py --recreate-index
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchField,
    SearchFieldDataType,
    SearchIndex,
)

SCRIPT_DIR = Path(__file__).parent
TYPE_MAP = {
    "Edm.String": SearchFieldDataType.String,
    "Edm.Boolean": SearchFieldDataType.Boolean,
    "Collection(Edm.String)": SearchFieldDataType.CollectionString,
}
DATA_DIR = SCRIPT_DIR.parent
SKILLS_FILE = DATA_DIR / "skills" / "skills_index.json"
SCHEMA_FILE = SCRIPT_DIR / "search_index_schema.json"


def load_env() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(DATA_DIR.parent / "CareerCompass-Backend" / ".env")
        load_dotenv(DATA_DIR.parent / "azure-functions" / ".env")
        load_dotenv()
    except ImportError:
        pass


def get_config() -> tuple[str, str, str]:
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "")
    key = os.getenv("AZURE_SEARCH_KEY", "")
    index_name = os.getenv("AZURE_SEARCH_INDEX", "skills-index")
    if not endpoint or not key:
        print("ERROR: Set AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_KEY")
        sys.exit(1)
    return endpoint, key, index_name


def create_index(endpoint: str, key: str, index_name: str, recreate: bool) -> None:
    index_client = SearchIndexClient(endpoint, AzureKeyCredential(key))

    if recreate:
        try:
            index_client.delete_index(index_name)
            print(f"Deleted existing index: {index_name}")
        except Exception:
            pass

    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    fields = [
        SearchField(
            name=f["name"],
            type=TYPE_MAP[f["type"]],
            key=f.get("key", False),
            searchable=f.get("searchable", False),
            filterable=f.get("filterable", False),
            facetable=f.get("facetable", False),
        )
        for f in schema["fields"]
    ]
    index = SearchIndex(name=index_name, fields=fields)

    index_client.create_or_update_index(index)
    print(f"Index ready: {index_name}")


def upload_documents(endpoint: str, key: str, index_name: str) -> None:
    docs = json.loads(SKILLS_FILE.read_text(encoding="utf-8"))
    client = SearchClient(endpoint, index_name, AzureKeyCredential(key))

    batch_size = 100
    for i in range(0, len(docs), batch_size):
        batch = docs[i : i + batch_size]
        result = client.upload_documents(documents=batch)
        failed = [r for r in result if not r.succeeded]
        if failed:
            print(f"WARNING: {len(failed)} documents failed in batch {i // batch_size + 1}")

    print(f"Uploaded {len(docs)} documents to '{index_name}'")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--recreate-index", action="store_true")
    args = parser.parse_args()

    load_env()
    endpoint, key, index_name = get_config()

    create_index(endpoint, key, index_name, args.recreate_index)
    upload_documents(endpoint, key, index_name)


if __name__ == "__main__":
    main()
