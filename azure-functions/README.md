# Azure Functions API 

HTTP triggers for Career Compass backend.

## Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/api/get_profile_summary` | POST | Career summary (assignment name) |
| `/api/get_career_summary` | POST | Same handler — frontend alias |
| `/api/optimize_resume` | POST | Resume refinement |

## Quick start

See `docs/ENV_SETUP.md`.

```bash
cd azure-functions
cp local.settings.json.example local.settings.json
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
func start
```

## One-time Azure setup scripts

```bash
# Create Cosmos containers (needs COSMOS_* in local.settings.json)
python scripts/setup_cosmos.py

# Upload skills index (from repo root data/scripts)
cd ../data/scripts
pip install azure-search-documents python-dotenv
python upload_to_search.py
```
