# Team Environment Setup (同学 B)

Copy the example files below, fill in real values, and **never commit secrets**.

## 1. Azure Functions (backend API)

```bash
cd azure-functions
cp local.settings.json.example local.settings.json
# Edit local.settings.json with your Azure keys
```

Run locally:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
func start
```

Default local URL: `http://localhost:7071/api`

## 2. Frontend

```bash
cd frontend
cp .env.example .env
```

Set `VITE_API_BASE=http://localhost:7071/api` for local Functions, or your deployed URL.

## 3. FastAPI backend (legacy / interview features)

```bash
cd CareerCompass-Backend
cp .env.example .env
```

## Environment variables reference

| Variable | Used by | Purpose |
|----------|---------|---------|
| `AZURE_ENDPOINT` | Functions, FastAPI | Azure OpenAI endpoint URL |
| `AZURE_API_KEY` | Functions, FastAPI | Azure OpenAI API key |
| `MODEL_NAME` | Functions, FastAPI | Model deployment name (e.g. `Phi-4-mini-instruct`) |
| `DEMO_MODE` | Functions, FastAPI | `true` = mock responses, no Azure calls |
| `COSMOS_ENDPOINT` | Functions | Cosmos DB account URI |
| `COSMOS_KEY` | Functions | Cosmos DB primary key |
| `COSMOS_DATABASE` | Functions | Database name (default: `career-compass`) |
| `COSMOS_PROFILES_CONTAINER` | Functions | Container for profiles (default: `student_profiles`) |
| `COSMOS_RESUMES_CONTAINER` | Functions | Container for resumes (default: `resumes`) |
| `AZURE_SEARCH_ENDPOINT` | Functions, upload script | AI Search service URL |
| `AZURE_SEARCH_KEY` | Functions, upload script | AI Search admin/query key |
| `AZURE_SEARCH_INDEX` | Functions, upload script | Index name (default: `skills-index`) |
| `VITE_API_BASE` | Frontend | Base URL for API calls |
| `VITE_USE_MOCK` | Frontend | `true` = force mock data |

## Azure resources to create (Portal)

1. **Cosmos DB** — NoSQL, database `career-compass`, containers `student_profiles` and `resumes` (partition key `/userId`)
2. **Azure AI Search** — Basic tier, index `skills-index` (see `data/scripts/upload_to_search.py`)
3. **Function App** — Python 3.11, deploy `azure-functions/`
4. **Azure OpenAI** — existing hub (`hub-career-compass-ai`)

Share keys via team password manager — not GitHub, not chat.
