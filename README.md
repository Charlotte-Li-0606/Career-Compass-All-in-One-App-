# Career Compass

An AI-powered career coach for Hong Kong and Macau university students — built for the **Microsoft Agent Impact Lab** hackathon (June 2026).

**Track:** Reinvent Student Engagement (Career Readiness)
**Stack:** Pro-Code (Azure-hosted)
**Hackathon site:** [Career Compass](https://blue-pond-0d0ece800.7.azurestaticapps.net/)

---

## What It Does

Career Compass is an all-in-one AI career development app with three tools:

| Tool | What it does |
|------|-------------|
| **Career Profile** | Fill a form about yourself → get an AI-generated career summary + color-coded skills gap table |
| **Resume Studio** | Upload your resume, tell the AI what to improve → see a side-by-side diff with a change log |
| **Mock Interview** | Chat-based simulator with role-specific questions, AI follow-ups, and a scored performance report |

---

## Quick Start

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start the dev server
npm run dev

# Open http://localhost:5173
```

The app hot-reloads on save.

### Commands

| Command | What it does |
|---------|-------------|
| `npm run dev` | Start dev server with HMR |
| `npm run build` | TypeScript type-check + production build → `dist/` |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Run ESLint |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  React SPA (Vite + TypeScript)          │
│                  Azure Static Web Apps                  │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │Career Profile│  │Resume Studio │  │ Mock Interview│  │
│  │     (/)      │  │(/resume-     │  │ (/mock-       │  │
│  │              │  │   studio)    │  │   interview)  │  │
│  └──────┬───────┘  └──────┬───────┘  └───────┬───────┘  │
│         │                 │                  │          │
│         └─────────┬───────┘                  │          │
│                   │              (fully client-side)    │
│         ┌─────────▼─────────┐                           │
│         │   services/api.ts │                           │
│         └─────────┬─────────┘                           │
└───────────────────┼─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│            Azure Functions (Python)                     │
│            /get_career_summary                          │
│            /get_profile_summary                         │
│            /get_skills_table                            │
│            /optimize_resume                             │
│            /start_interview  /submit_answer  /report    │
│                                                         │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  Azure   │  │  Azure AI    │  │    Cosmos DB     │   │
│  │ OpenAI   │  │  Search      │  │  (profiles,      │   │
│  │ (Phi-4)  │  │  (210 docs)  │  │   resumes,       │   │
│  │          │  │              │  │   interviews)    │   │
│  └──────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**3 pages, 6 API endpoints, 3 Cosmos DB containers, 210 skill-role search documents.**

---

## Project Structure

```
frontend/                         React + TypeScript SPA
  src/
    main.tsx                      Entry point — StrictMode + BrowserRouter
    App.tsx                       Shell — Navbar, 3 routes, footer
    index.css                     Single-file dark theme (~1070 lines)
    pages/
      CareerProfile.tsx           Form → career summary → skills table
      ResumeStudio.tsx            3-step: upload → instructions → refine
      MockInterview.tsx           3-state: setup → chat → scored report
    components/
      Navbar.tsx                  3-tab navigation
      ChipInput.tsx               Tag-style input
      PersonalSummary.tsx         Career summary card
      SkillsTable.tsx             Color-coded skills gap grid
      ResumeUploader.tsx          File upload + paste (pdfjs-dist)
      ResumeDiff.tsx              Side-by-side original vs refined
    services/
      api.ts                      Fetch client for Azure Functions
      mockData.ts                 Mock responses for offline dev
    types/
      index.ts                    All TypeScript interfaces
    data/
      roles.ts                    20 roles across 5 sectors
      interviewQuestions.ts       Question selection + shuffling
      interview_questions.json    Role-specific Q&A bank (88 KB)

azure-functions/                  Primary backend — Azure Functions (Python)
  function_app.py                 6 HTTP triggers with CORS
  requirements.txt                azure-functions, cosmos, search, openai
  shared/
    config.py                     Environment configuration
    llm_service.py                Azure OpenAI client + prompt builders
    cosmos_service.py             Cosmos DB CRUD (3 containers)
    search_service.py             Azure AI Search client

data/                             HK job market knowledge base
  taxonomy/                       Controlled vocabularies (skills, sectors, importance)
  roles/                          20 roles with required skills (5 JSON files)
  skills/                         210 search documents (generated)
  market_data/                    Salary benchmarks, industry insights, universities
  interviews/                     Interview question bank
  scripts/                        Validation + search doc generation + upload

CareerCompass-Backend/            Legacy FastAPI backend (not integrated)
schemas/                          JSON Schema for Cosmos DB documents
docs/                             Setup guides (Cosmos DB, environment variables)
```

---

## Features In Detail

### Career Profile (`/`)

1. Fill in your academic profile: major, year, university, target roles, interests, internships, extracurriculars
2. Submit → the AI analyzes your profile against HK job market data
3. Get a **career summary** with recommended roles, industry insights, and next steps
4. Get a **skills table** showing what you've mastered, what you're learning, and what's missing — color-coded green/amber/red

### Resume Studio (`/resume-studio`)

1. Upload a resume (PDF, TXT, MD) or paste text directly
2. Tell the AI what to improve ("make it more concise", "highlight leadership")
3. See a **side-by-side diff** — original vs refined
4. Review the **change log** showing exactly what was added, modified, or removed
5. Download the refined resume as a Markdown file

### Mock Interview (`/mock-interview`)

1. Pick a role (20 roles across 5 sectors) and experience level (intern / graduate / experienced)
2. Answer **4 role-specific questions** drawn from a bank of behavioral, technical, and situational prompts
3. The AI interviewer gives follow-ups between questions
4. Get a **scored performance report** with a score ring, dimension breakdown (Communication, Content, Confidence), strengths, and areas to improve

> **Note:** In mock mode, scoring uses local heuristics (answer length, action keywords, numeric metrics). The backend's interview endpoints (`/start_interview`, `/submit_answer`, `/generate_report`) use real LLM evaluation.

---

## Mock Mode vs Real Backend

By default, the app runs entirely in **mock mode** — no backend or API keys needed. Mock mode is active when `VITE_API_BASE` is not set, or when `VITE_USE_MOCK=true`.

To connect to a real backend:

```bash
# In frontend/.env
VITE_API_BASE=https://your-function-app.azurewebsites.net/api
```

To force mock mode even with an API base set:

```bash
VITE_USE_MOCK=true
```

---

## Backend Setup

### Prerequisites

- Python 3.10+
- Azure CLI
- Azure subscriptions for: Functions, OpenAI, AI Search, Cosmos DB

### Azure Functions

```bash
cd azure-functions
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Copy and fill in local.settings.json from the example
cp local.settings.json.example local.settings.json

# Run locally
func start
```

### Environment Variables

See `azure-functions/local.settings.json.example` for the full template. Key variables:

| Variable | Description |
|----------|-------------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL |
| `AZURE_OPENAI_KEY` | Azure OpenAI API key |
| `MODEL_NAME` | Model deployment name (default: `Phi-4-mini-instruct`) |
| `COSMOS_ENDPOINT` | Cosmos DB account URL |
| `COSMOS_KEY` | Cosmos DB key |
| `SEARCH_SERVICE_ENDPOINT` | Azure AI Search URL |
| `SEARCH_API_KEY` | Azure AI Search API key |
| `DEMO_MODE` | `true` = use hardcoded responses instead of LLM |

---

## Data Pipeline

The AI's knowledge of HK job roles comes from curated data in `data/roles/`. The pipeline:

```
Role JSON files           skills_index.json       Azure AI Search
(hand-curated)    →       (210 documents)    →    (queryable index)
        ↓                        ↓                       ↓
 validate_schema.py    generate_search_docs.py    upload_to_search.py
```

```bash
cd data/scripts

# 1. Validate role files against the taxonomy
python validate_schema.py

# 2. Generate flat search documents
python generate_search_docs.py

# 3. Upload to Azure AI Search
python upload_to_search.py
```

### Data Coverage

| Category | Count |
|----------|-------|
| Roles | 20 across 10 sectors |
| Skill categories | 16 |
| Skill-role search documents | 210 |
| HK + Macau universities | 23 |
| Interview questions | 20 roles × 3 levels × 3 categories |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, TypeScript 6, Vite 8, react-router-dom 7 |
| Styling | Single CSS file, dark theme, CSS custom properties |
| PDF Parsing | pdfjs-dist 6 |
| Backend | Azure Functions (Python), FastAPI (legacy) |
| AI | Azure OpenAI (default: Phi-4-mini-instruct) |
| Search | Azure AI Search (210 skill-role documents) |
| Database | Cosmos DB (student_profiles, resumes, interview_sessions) |
| Hosting | Azure Static Web Apps |

---

## Team

Built for the **Microsoft Agent Impact Lab 2026** hackathon — Microsoft HK × Student Ambassador Program.