# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Career Compass** — an AI agent app for the **Microsoft Agent Impact Lab** hackathon (June 29, 2026 deadline). A supportive career coach for Hong Kong/Macau university students, published to Microsoft 365 Copilot Chat.

- **Track:** Reinvent Student Engagement (Career Readiness)
- **Stack:** Pro-Code (Azure-hosted)
- **Hackathon site:** https://blue-pond-0d0ece800.7.azurestaticapps.net/
- **Backend API:** `https://agentimpactlab-api.azurewebsites.net/api` (POST `/apply`, POST `/submit`)

## Architecture

```
React SPA (Vite + TypeScript)  →  Azure Functions (Python)  →  Azure OpenAI GPT-4o
 (Azure Static Web Apps)            /api/get_career_summary     Azure AI Search
                                    /api/get_skills_table       Cosmos DB
                                    /api/optimize_resume
```

**3 pages:** Career Profile (summary + skills table) | Resume Studio (upload + refine) | Mock Interview (chat-based simulator with role-specific Q&A and performance report)

**Core intelligence ("The Bridge"):** The skills table is derived from the career summary — summary identifies roles, roles map to required skills via AI Search, skills categorized as Mastered / Learning / Missing.

**Agent persona:** Supportive career coach — encouraging, specific, practical, patient. System prompt scaffold is in `General Planning.md`.

## Project Structure (Current)

```
frontend/                    React + TypeScript (Vite) SPA
  public/                    Static assets (favicon, pdf.worker.min.mjs)
  src/
    main.tsx                 Entry point — BrowserRouter + StrictMode
    App.tsx                  App shell — 3 routes, Navbar, footer
    index.css                Single-file CSS (~1070 lines) — dark theme, components, animations
    pages/
      CareerProfile.tsx       Form-driven career profile → summary + skills table
      ResumeStudio.tsx        3-step resume refinement (upload → instruct → refine)
      MockInterview.tsx       3-state interview simulator (setup → active → report)
    components/
      Navbar.tsx              Fixed top nav — 3 NavLink tabs
      ChipInput.tsx           Tag-style input (interests, internships, extracurriculars)
      PersonalSummary.tsx     Career summary card (overview, roles, insights, next steps)
      SkillsTable.tsx         Color-coded skills grid (Mastered/Learning/Missing)
      ResumeUploader.tsx      File upload + paste (PDF via pdfjs-dist, TXT/DOCX/MD)
      ResumeDiff.tsx          Side-by-side original vs refined, changes list
    services/
      api.ts                  Fetch client for Azure Functions (4 endpoints)
      mockData.ts             Mock data for development (career summary, skills, resume)
    types/
      index.ts                TypeScript interfaces (UserProfile, CareerSummary, SkillsTable, etc.)
    data/
      roles.ts                ROLE_OPTIONS — 5 sectors, 20 roles (used by all 3 pages)
      interviewQuestions.ts   Question bank helpers (types, shuffle, selectInterviewQuestions)
      interview_questions.json  20 roles × 3 levels × 3 categories (behavioral/technical/situational)
  package.json                React 19, Vite 8, TypeScript 6, pdfjs-dist, react-router-dom 7
  vite.config.ts              @vitejs/plugin-react

api/                          Azure Functions (Python) — PLANNED, not yet scaffolded
  function_app.py             HTTP triggers (to be created)
  agent_prompts.py            System prompts and persona (to be created)
  models.py                   Pydantic models (to be created)
  search_client.py            Azure AI Search helper (to be created)
  cosmos_client.py            Cosmos DB helper (to be created)

infra/                        Bicep/Terraform — PLANNED, not yet scaffolded

data/                         Seed data for Azure AI Search + mock interview
  README.md                   Data directory documentation
  taxonomy/
    industry_sectors.json     10 sectors with sub-sectors
    skill_categories.json     16 controlled categories (Programming, BI, Cloud, AI/ML, etc.)
    importance_levels.json    critical | recommended | nice-to-have (weights 3/2/1)
  roles/
    technology_data.json      5 roles (Data Analyst, Software Engineer, BI Developer, AI/ML Eng, IT PM)
    finance_banking.json      5 roles (IB Analyst, Risk Analyst, WM Trainee, Fintech Assoc, Compliance)
    professional_services.json 4 roles (Mgmt Consultant, Audit Assoc, ESG Analyst, HR Specialist)
    marketing_ecommerce.json  3 roles (Digital Marketing Spec, Product Manager, E-com Ops)
    engineering_logistics.json 3 roles (Civil Engineer, Supply Chain Analyst, Building Services Eng)
  skills/
    skills_index.json         210 search documents (one per skill-role pair), generated
    skills_summary.json       20 roles summarized with skill counts, generated
  market_data/
    salary_benchmarks.json    Entry-level salary bands by sector (HKD/month)
    industry_insights.json    7 sectors — outlook, trends, in-demand roles, key skills
    hk_universities.json      23 institutions (16 HK + 7 Macau), QS ranks
  interviews/
    interview_questions.json  20 roles × 3 levels (intern/graduate/experienced) × 3 categories
  scripts/
    validate_schema.py        Validates role JSON against taxonomy
    generate_search_docs.py   Transforms role files → flat search index (210 docs)

General Planning.md           Detailed hackathon planning — features, phases, system prompts
```

## Key Design Rules

- **Structured outputs are mandatory.** All GPT-4o responses for career summary and skills table must use JSON structured outputs for reliable frontend rendering.
- **Skills table must derive from career summary** — never compute them independently. This is the core value of the agent ("The Bridge").
- **Responsible AI** is a judging criterion — include confidence indicators, cite sources, never give definitive career "guarantees."
- **All agents must publish to M365 Copilot Chat** — via Azure AI Agent Service.
- **Mock mode is default.** When `VITE_USE_MOCK=true` or `VITE_API_BASE` is not set, the app runs entirely client-side with simulated data and delays. All three pages function fully without any backend.
- **Mock interview page** is a fully functional client-side simulator with three states (setup → active → report). Questions come from a hardcoded `SECTOR_QUESTIONS` record (5 sector banks, 6 questions each, 4 shuffled per session). The difficulty selector (intern/graduate/experienced) is rendered in the UI but not yet wired — all levels pull from the same question pool. Heuristic scoring is based on answer length, action keywords, and numeric metrics. Speech-to-text (mic button) is UI-only (3-second placeholder). An expanded data module (`interviewQuestions.ts` + `interview_questions.json`) exists with role-specific, difficulty-leveled questions ready to wire in.

## Data Models

**Cosmos DB — StudentProfile container:** `id`, `userId` (Entra ID), `major`, `year`, `university`, `interests[]`, `targetRoles[]`, `pastInternships[]`, `extracurriculars[]`, `careerSummary` (structured JSON), `skillsTable` (structured JSON), `updatedAt`

**Cosmos DB — Resume container:** `id`, `userId`, `originalText`, `refinementInstructions`, `refinedText`, `createdAt`

**TypeScript interfaces** (`frontend/src/types/index.ts`):
- `UserProfile` — major, year, university, interests[], targetRoles[], pastInternships[], extracurriculars[]
- `CareerSummary` — overview, recommendedRoles (CareerRole[]), industryInsights, nextSteps[]
- `CareerRole` — title, fit, growthOutlook
- `Proficiency` — `'mastered' | 'learning' | 'missing'`
- `SkillEntry` — name, category, proficiency, description, importance (`'critical' | 'recommended' | 'nice-to-have'`)
- `SkillsTable` — skills[], summary
- `ResumeRefinementRequest`, `ResumeChange`, `ResumeRefinementResponse`
- `ApiResponse<T>` — generic wrapper: `{ data: T, error?: string, loading: boolean }`

**Role data schema** (`data/roles/*.json`):
- `sector`, `subSector`, `lastUpdated`, `source`
- `roles[]` — `roleTitle`, `roleTitleZh`, `isEntryLevel`, `typicalSalary`, `growthOutlook`, `hiringIndustries[]`, `requiredSkills[]`
- Each skill: `skillName`, `skillCategory`, `importance`, `description`, `typicalLevel`

**Interview question schema** (`data/interviews/interview_questions.json`):
- Top-level: `lastUpdated`, `source`, `description`, `roles{}`
- Per role: `sector`, `intern{}`, `graduate{}`, `experienced{}`
- Per level: `behavioral[]`, `technical[]`, `situational[]` (string arrays, ~8-11 questions total per role per level)

## Frontend Page Behavior

### Career Profile (`/`)
1. User fills form (major, year, university, targetRoles, interests, extracurriculars)
2. Submit triggers `getCareerSummary()` → `getSkillsTable()` (API or mock)
3. Displays `<PersonalSummary>` (overview, recommended roles, industry insights, next steps)
4. Displays `<SkillsTable>` (sorted grid with proficiency tags and importance labels)
5. Role multi-select uses `ROLE_OPTIONS` from `data/roles.ts` (20 roles, 5 sectors)

### Resume Studio (`/resume-studio`)
1. Upload resume via `<ResumeUploader>` — PDF (pdfjs-dist extraction), TXT, DOCX, MD, or paste
2. Enter refinement instructions (free text)
3. Call `optimizeResume()` → `<ResumeDiff>` side-by-side original vs refined
4. Download refined resume as `.md` file via Blob
5. Mock data provides a sample fintech internship resume with 5 changes

### Mock Interview (`/mock-interview`)
1. **Setup** — select role (radio buttons from ROLE_OPTIONS) and experience level (intern/graduate/experienced)
2. **Active** — chat-based Q&A with simulated AI interviewer. Questions from `SECTOR_QUESTIONS` (5 sector banks, 6 questions each). 4 shuffled questions per session. Follow-ups use generic encouraging phrases. Mic button is UI-only (3-second timer → placeholder text). Enter to send, Shift+Enter for newline. Can end early via "End Interview" button.
3. **Report** — heuristic scoring (answer length, action keywords, numeric metrics). SVG score ring with gradient. Dimension bars: Communication, Content, Confidence. Strengths and improvements lists. Buttons to retry or return to Career Profile.

## API Service (`frontend/src/services/api.ts`)

All endpoints POST unless noted. Base URL from `VITE_API_BASE` env var:

| Function | Method | Path |
|----------|--------|------|
| `getCareerSummary(profile)` | POST | `/get_career_summary` |
| `getSkillsTable(profile, careerSummary)` | POST | `/get_skills_table` |
| `optimizeResume(req)` | POST | `/optimize_resume` |
| `saveProfile(userId, profile)` | PUT | `/profile/{userId}` |

Generic `request<T>()` wrapper handles JSON serialization, error formatting, and loading state.

## Data Pipeline

1. **Validate** role files against taxonomy: `cd data && python scripts/validate_schema.py`
2. **Generate** search documents: `cd data && python scripts/generate_search_docs.py`
3. Upload `data/skills/skills_index.json` to Azure AI Search (210 skill-role documents)
4. At runtime, GPT-4o queries Azure AI Search to match career summary roles → required skills
5. Proficiency (mastered/learning/missing) is inferred by GPT-4o per user, not stored in the index

## Commands

```bash
# Frontend
cd frontend && npm install           # Install dependencies
cd frontend && npm run dev           # Start Vite dev server (http://localhost:5173)
cd frontend && npm run build         # Production build → dist/
cd frontend && npm run preview       # Preview production build
cd frontend && npm run lint          # ESLint
cd frontend && npx tsc --noEmit     # TypeScript type-check

# Data validation
cd data && python scripts/validate_schema.py
cd data && python scripts/generate_search_docs.py

# Backend (once scaffolded)
cd api && func start                 # Start Functions runtime locally
cd api && func start --python        # Explicit Python worker
cd api && python -m pytest           # Run tests

# Deployment
az staticwebapp deploy               # Deploy frontend
az functionapp deployment ...        # Deploy API
```

## Mock Data Configuration

Set in `frontend/.env`:
```
VITE_USE_MOCK=true                  # Force mock mode
VITE_API_BASE=<azure-functions-url> # Connect to real backend
```

Mock data in `frontend/src/services/mockData.ts`:
- `mockCareerSummary` — overview, 3 roles (Data Analyst, BI Developer, AI/ML Eng), industry insights, 4 next steps
- `mockSkillsTable` — 10 skills with proficiency/importance (Python/SQL mastered, Tableau/Stats/Cloud learning, ML missing)
- `mockResumeRefinement` — refined resume for "John Doe" (CUHK CS, fintech internship), 5 changes

## Technical Notes

- **Single CSS file** — all styles in `src/index.css`. No Tailwind, CSS modules, or CSS-in-JS. Dark theme with cyan (`#00f5ff`) and purple (`#a855f7`) accent gradient.
- **No state management library** — plain React `useState` throughout. No Redux, Zustand, or Context.
- **PDF extraction** — `ResumeUploader` dynamically imports `pdfjs-dist` v6. Worker served from `/pdf.worker.min.mjs` in `public/`.
- **No test files** — no `*.test.ts` or `*.spec.ts` exist yet.
- **`api/` and `infra/` are planned only** — neither directory has been scaffolded.
- **Python scripts** in `data/scripts/` require Python 3.10+ with no external dependencies (stdlib only).
