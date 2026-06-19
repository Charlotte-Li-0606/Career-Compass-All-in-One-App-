# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Career Compass** — an AI agent app for the **Microsoft Agent Impact Lab** hackathon (June 29, 2026 deadline). A supportive career coach for Hong Kong/Macau university students, published to Microsoft 365 Copilot Chat.

- **Track:** Reinvent Student Engagement (Career Readiness)
- **Stack:** Pro-Code (Azure-hosted)
- **Hackathon site:** https://blue-pond-0d0ece800.7.azurestaticapps.net/
- **Backend API:** Azure Functions at `azure-functions/` (POST `/get_career_summary`, POST `/get_profile_summary`, POST `/optimize_resume`). A second FastAPI backend also exists at `CareerCompass-Backend/` with different route paths — see Known Issues.

## Architecture

```
React SPA (Vite + TypeScript)  →  Azure Functions (Python)  →  Azure OpenAI (GPT-4o or Phi-4-mini-instruct)
 (Azure Static Web Apps)            /get_career_summary          Azure AI Search
                                    /get_profile_summary         Cosmos DB
                                    /optimize_resume
                                    ⚠ /get_skills_table — NOT YET IMPLEMENTED (see Known Issues)
```

**⚠ The default model in config is `Phi-4-mini-instruct`, not GPT-4o.** See Known Issues #6.

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
      ResumeUploader.tsx      File upload + paste (PDF via pdfjs-dist, TXT/MD). ⚠ DOCX accepted but NOT parsed — see Known Issues #4
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

azure-functions/              Azure Functions (Python) — PRIMARY backend
  function_app.py             HTTP triggers — get_profile_summary, get_career_summary, optimize_resume
  requirements.txt            Python dependencies
  host.json                   Azure Functions host config
  local.settings.json.example Example local settings (model, Cosmos, Search config)
  shared/
    config.py                 Environment configuration
    llm_service.py            Azure OpenAI client + prompt builders
    cosmos_service.py         Cosmos DB helpers (profile upsert, resume version save)
    search_service.py         Azure AI Search client (skill lookup by role)

CareerCompass-Backend/        FastAPI (Python) — SECONDARY / legacy backend
  app.py                      FastAPI routes — /profile/analyze, /skills/analyze, /resume/tailor, interview endpoints
  schemas.py                  Pydantic models
  llm_service.py              OpenAI client (different from Azure Functions version)
  requirements.txt
  .env.example                MODEL_NAME=Phi-4-mini-instruct
  cache.json                  Empty runtime artifact — TRACKED IN GIT (see Known Issues)

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
    engineering_logistics.json 3 roles (Graduate Civil Engineer, Supply Chain Analyst, Building Services Eng)
                           ⚠ Frontend says "Civil Engineer"; data/search/index use "Graduate Civil Engineer" — see Known Issues #3
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

- **Structured outputs are mandatory.** All LLM responses for career summary and skills table must use JSON structured outputs for reliable frontend rendering.
- **Skills table must derive from career summary** — never compute them independently. This is the core value of the agent ("The Bridge").
- **Responsible AI** is a judging criterion — include confidence indicators, cite sources, never give definitive career "guarantees."
- **All agents must publish to M365 Copilot Chat** — via Azure AI Agent Service.
- **Mock mode is default.** When `VITE_USE_MOCK=true` or `VITE_API_BASE` is not set, the app runs entirely client-side with simulated data and delays. All three pages function fully without any backend.
- **Mock interview page** is a fully functional client-side simulator with three states (setup → active → report). Questions are now served from `interviewQuestions.ts` + `interview_questions.json` (role-specific, difficulty-leveled — 20 roles × 3 levels × 3 categories). Heuristic scoring is based on answer length, action keywords, and numeric metrics. Speech-to-text (mic button) is UI-only (3-second placeholder with a stale-closure bug — see Known Issues #9). ⚠ Markdown in chat messages (e.g. `**bold**`) is NOT rendered — users see literal asterisks (see Known Issues #8). The performance report uses simplistic heuristics with no disclaimer that scores are mock-simulated, not genuine AI evaluation.
- **⚠ The `/get_skills_table` endpoint does NOT exist in the backend.** This is the critical missing piece of "The Bridge." See Known Issues #2.

## Data Models

**Cosmos DB — student_profiles container:** `id`, `userId` (Entra ID), `major`, `year`, `university`, `interests[]`, `targetRoles[]`, `pastInternships[]`, `extracurriculars[]`, `careerSummary` (structured JSON), `skillsTable` (structured JSON), `updatedAt`

> **Note:** The actual container name in code is `student_profiles` (via `COSMOS_PROFILES_CONTAINER` env var), not `StudentProfile`.

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
1. Upload resume via `<ResumeUploader>` — PDF (pdfjs-dist extraction), TXT, MD, or paste. ⚠ DOCX is in the accept list but NOT actually parsed (binary read as text → garbage)
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
- **`infra/` is planned only** — not yet scaffolded. Backends exist at `azure-functions/` and `CareerCompass-Backend/` (not at the documented `api/` path).
- **Python scripts** in `data/scripts/` require Python 3.10+ with no external dependencies (stdlib only).
- **No React Error Boundaries** — any unhandled component render error will unmount the entire SPA (white screen). See Known Issues #7.
- **No `prefers-reduced-motion` support** — three CSS animations and `scroll-behavior: smooth` have no reduced-motion overrides.
- **No Vite dev server CORS proxy** — cross-origin requests from `localhost:5173` to any backend will fail unless the backend explicitly sets CORS headers.
- **⚠ Duplicate `interview_questions.json`** — identical 88KB copies exist at `data/interviews/` and `frontend/src/data/`. The frontend imports from its local copy. Any update must be manually synced. See Known Issues #12.
- **⚠ `__pycache__/*.pyc` files tracked in git** — 6 compiled Python bytecode files under `CareerCompass-Backend/__pycache__/` are committed to the repo. See Known Issues #10.
- **⚠ `CareerCompass-Backend/cache.json` tracked in git** — empty runtime artifact (`{}`) that should be in `.gitignore`. See Known Issues #25.
- **⚠ Keyword noise in search index** — `generate_search_docs.py` splits skill names by whitespace without stripping punctuation, producing standalone `&`, `/`, `(`, `)` tokens in 97 of 210 search documents. See Known Issues #13.

## Known Issues

This section catalogs all problems found during the June 2026 codebase audit. Fix these before or immediately after the hackathon deadline (June 29, 2026).

### 🔴 CRITICAL

**#1 — Broken API fallback URL** (`frontend/src/services/api.ts:10`)
```typescript
const API_BASE = import.meta.env.VITE_API_BASE ?? 'https://hub-career-compass-ai.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview';
```
When `VITE_API_BASE` is unset, `request()` builds URLs like `...chat/completions?api-version=2024-05-01-preview/get_career_summary` — appending path segments AFTER the query string. Every API call will fail with a malformed URL. Fix: change fallback to `http://localhost:7071/api` (matching `.env.example`), or remove the fallback and require the env var.

**#2 — `/get_skills_table` endpoint missing from backend** (`frontend/src/services/api.ts:36` vs `azure-functions/function_app.py`)
The frontend calls `POST /get_skills_table` to derive skills from a career summary — this is the core "Bridge" feature. Neither `azure-functions/` (3 routes) nor `CareerCompass-Backend/` (FastAPI, different route paths) implements this endpoint. The call will 404 in production, breaking the skills table. Fix: either add the endpoint to `function_app.py`, wire the frontend to use the existing profile summary response's inline skills data, or implement as part of `get_career_summary`.

**#3 — "Graduate Civil Engineer" vs "Civil Engineer" name mismatch**
- `frontend/src/data/roles.ts:47` — `'Civil Engineer'`
- `data/roles/engineering_logistics.json:8` — `"Graduate Civil Engineer"`
- `data/skills/skills_index.json` — all 30 documents use `"Graduate Civil Engineer"`
- `data/interviews/interview_questions.json:967` — `"Graduate Civil Engineer"`
When a user selects "Civil Engineer", the backend searches `roleTitle eq 'Civil Engineer'` — zero results. The entire career summary and skills pipeline silently fails for this role. Fix: choose one name and update all 4 locations consistently.

**#4 — DOCX accepted but not parsed** (`frontend/src/components/ResumeUploader.tsx:82-87`)
File input `accept=".txt,.pdf,.docx,.md"` and label says "PDF, TXT, DOCX, MD" — but the code only handles `.pdf` (via pdfjs-dist) and plain text (`FileReader.readAsText()`). DOCX is a binary ZIP archive; `readAsText()` produces garbled content. Fix: either install `mammoth.js` to parse DOCX, or remove `.docx` from the accept list and label.

### 🟠 HIGH

**#5 — Two separate backends with no integration**
- `azure-functions/` — Azure Functions (Python), 3 HTTP triggers, Azure AI Search + Cosmos DB
- `CareerCompass-Backend/` — FastAPI (Python), 6 endpoints, different route paths, separate OpenAI client
The frontend targets Azure Functions paths. The FastAPI backend has completely different routes (`/profile/analyze`, `/skills/analyze`, `/resume/tailor`, `/interview/questions`, `/interview/followup`, `/interview/report`). There is no proxy, gateway, or documentation connecting them. Fix: choose one as the canonical backend and retire/migrate the other.

**#6 — GPT-4o in all docs vs Phi-4-mini-instruct in actual config**
CLAUDE.md, README.md, and General Planning.md all reference GPT-4o. Both `azure-functions/local.settings.json.example` and `CareerCompass-Backend/.env.example` default to `Phi-4-mini-instruct` (3.8B parameters, dramatically less capable). Fix: align documentation with the actual model choice, and verify that Phi-4-mini-instruct can produce the structured outputs required.

**#7 — No React Error Boundaries** (entire frontend)
Zero `ErrorBoundary` components anywhere. If any page or component throws during render (malformed API response, missing property), the entire SPA shows a white screen. Fix: add an Error Boundary wrapping `<Routes>` in `App.tsx`, and consider per-page boundaries.

**#8 — Markdown in Mock Interview chat never rendered** (`frontend/src/pages/MockInterview.tsx:130,154,190-192`)
Chat messages contain `**bold**` markdown syntax in intro, follow-ups, and closing messages. The UI renders text in plain `<div>` elements with only `white-space: pre-wrap`. Users see literal asterisks. Fix: use `react-markdown` or a simple regex-to-JSX converter to render markdown in chat bubbles.

**#9 — Stale closure in `toggleMic` can overwrite user input** (`frontend/src/pages/MockInterview.tsx:213-225`)
`toggleMic` starts a `setTimeout` that closes over the `input` state at call time. After 3 seconds, the callback checks `if (!input.trim())` using the stale empty value. If the user types anything during the simulated "recording", their text is overwritten by the placeholder. Fix: use a ref to track the current input value, or cancel the timeout on input change.

**#10 — `__pycache__/*.pyc` files tracked in git**
Six compiled bytecode files under `CareerCompass-Backend/__pycache__/` are committed (from initial upload). Root `.gitignore` has `__pycache__/` but the files predate the rule. Fix: `git rm --cached CareerCompass-Backend/__pycache__/*.pyc`

**#11 — Referenced script `upload_to_search.py` does not exist**
`azure-functions/README.md:35` and `docs/ENV_SETUP.md:62` reference `data/scripts/upload_to_search.py` for uploading skills index to Azure AI Search. This file does not exist. Fix: create the script, or document the alternative upload method (Azure Portal, az CLI, etc.).

### 🟡 MEDIUM

**#12 — Duplicate `interview_questions.json` (88KB × 2)**
Identical copies at `data/interviews/interview_questions.json` (canonical) and `frontend/src/data/interview_questions.json` (imported by the app). Any update must be manually synced — divergence is inevitable. Fix: have the frontend import from `data/interviews/` (requires path alias or symlink), or make the data directory the single source of truth with a copy/build step.

**#13 — Keyword noise in search index — 97 documents affected**
`data/scripts/generate_search_docs.py` splits skill names by whitespace but never strips punctuation. Standalone `&`, `/`, `(`, `)` tokens pollute keyword arrays. Fix: add `str.strip(punctuation)` to tokenization in the generator script and regenerate `skills_index.json`.

**#14 — `saveProfile` is dead code with broken error handling** (`frontend/src/services/api.ts:47-53`)
Exported but never imported/called. Bypasses the shared `request()` helper, calls `fetch` directly, never checks `res.ok`. If used, HTTP errors would silently pass through. Fix: either wire it to a profile save feature, or remove it.

**#15 — Supply Chain Analyst sector inconsistency**
- `data/roles/engineering_logistics.json` assigns it to "Engineering & Construction"
- `data/market_data/industry_insights.json` lists it under "Logistics & Supply Chain" (a separate sector in `data/taxonomy/industry_sectors.json`)
Fix: move Supply Chain Analyst to a logistics sector, or create a new "Logistics & Supply Chain" role file.

**#16 — `RUN_AND_TEST.txt` describes a non-existent placeholder**
Documents Mock Interview as having a "COMING SOON" badge with "4 feature cards" — the actual page is a fully functional 3-state simulator. Anyone following these test instructions cannot verify the page. Fix: update or remove this file.

**#17 — Unused/dead code**
- `ApiResponse<T>` in `frontend/src/types/index.ts` — defined, never imported
- `ALL_ROLES` in `frontend/src/data/roles.ts:55` — exported, never imported
- CSS classes `.nav-badge`, `.section-tag`, `.card-line`, `.success-banner` — defined in `src/index.css`, never used
Fix: remove dead code or wire it to its intended use.

### 🟢 LOW

**#18 — 7 accessibility gaps**
- SVG score ring has no `<title>`/`<desc>` — invisible to screen readers (`MockInterview.tsx:339-358`)
- Mic button (🎤) has no `aria-label` (`MockInterview.tsx:518`)
- `<nav>` in Navbar has no `aria-label` (`Navbar.tsx:5`)
- Role checkboxes/radios use `appearance: none` without custom `focus-visible` styles (`index.css:371-400,908-936`)
- Interview chat lacks `aria-live="polite"` for dynamic message announcements (`index.css:789`)
- Error banners lack `role="alert"` (`CareerProfile.tsx:78`, `ResumeStudio.tsx:72`)
- PDF `<embed>` in ResumeDiff has no `title` (`ResumeDiff.tsx:47`)

**#19 — Blob URL lifecycle issues**
- `ResumeDiff.tsx:17-35` — blob URLs created during render may leak under React 19 concurrent rendering (aborted renders don't revoke)
- `ResumeStudio.tsx:52-58` — Blob URL revoked immediately after `a.click()` before download may complete in some browsers

**#20 — No `prefers-reduced-motion` support**
Three animations (`spin`, `fadeSlideIn`, `typingBounce`) and `scroll-behavior: smooth` on `<html>` have no `@media (prefers-reduced-motion: reduce)` overrides.

**#21 — Cosmos DB container name wrong in documentation**
CLAUDE.md previously documented `StudentProfile` (PascalCase). Actual code uses `student_profiles` (snake_case via `COSMOS_PROFILES_CONTAINER` env var). Now corrected above.

**#22 — No Vite dev server CORS proxy**
`vite.config.ts` has no `server.proxy` configuration. Cross-origin requests from `localhost:5173` fail without backend CORS headers.

**#23 — Blockchain/Web3 miscategorized as "AI & Machine Learning"**
`data/roles/finance_banking.json:78` — Fintech Associate role lists "Blockchain / Web3 Fundamentals" under `"AI & Machine Learning"`. Should be `"Domain Knowledge"`.

**#24 — AI/ML Engineer has fewer interview questions (28 vs typical 30)**
Intern level has 3 behavioral questions instead of the usual 4. Total: 28 questions vs 30 for most other roles.

**#25 — `cache.json` (empty `{}`) tracked in git**
`CareerCompass-Backend/cache.json` is a runtime LLM cache artifact. Should be in `.gitignore`.

### Fix Priority Order

1. **#1** — Fix API fallback URL (one-line change)
2. **#2** — Wire `/get_skills_table` (or merge into existing endpoints)
3. **#3** — Align "Graduate Civil Engineer" naming
4. **#4** — Fix DOCX (add mammoth.js or remove from accept list)
5. **#7** — Add Error Boundary to App.tsx
6. **#10** — `git rm --cached` pycache files
7. **#12** — Consolidate duplicate interview_questions.json
8. **#11** — Create or document upload_to_search.py alternative
9. **#8** — Render markdown in chat messages
10. **#9** — Fix stale closure in toggleMic
11. Then: #13 (keyword noise), #17 (dead code cleanup), #5 (backend consolidation), #6 (model docs), #18-#25 (accessibility, misc)
