# Career Compass

An all-in-one AI career development application that assists students in synthesizing personalized career roadmaps, dynamically tailoring resumes to specific job descriptions, and conducting realistic mock interview simulations.

Built for the **Microsoft Agent Impact Lab** hackathon (June 2026) — Track: Reinvent Student Engagement (Career Readiness).

## Prerequisites

- **Node.js** (v18+) and **npm** installed
- Terminal open in the `frontend/` directory

## Quick Start

```bash
cd frontend

# 1. Install dependencies (first time only)
npm install

# 2. Start the dev server
npm run dev

# 3. Open the URL shown in the terminal (default: http://localhost:5173)
```

The app hot-reloads on save — no manual refresh needed.

## Available Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server with HMR (hot module replacement) |
| `npm run build` | TypeScript type-check + production build to `dist/` |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Run ESLint |

## Page-by-Page Testing

### Page 1 — Career Profile (`http://localhost:5173/`)

1. Fill in "Major / Field of Study" and "University"
2. Select a year from the dropdown — verify dark-themed options
3. Add some Target Roles (type and press Enter to create chips)
4. Add Interests, Past Internships, Extracurriculars — verify each chip area focuses correctly when clicked (not all jumping to Target Roles)
5. Click **"Generate Career Compass"** — wait ~1.2s for mock data
6. Verify:
   - Career Summary card appears with overview and recommended roles
   - Skills Table renders with color-coded proficiency tags (green = Mastered, amber = Learning, red = Missing)
   - Legend shows at the bottom of the skills table

### Page 2 — Resume Studio (`http://localhost:5173/resume-studio`)

1. Click **"Choose File"** — verify the button is dark-themed with cyan border (not an OS-default gray button)
2. Test with a **TXT file**:
   - Select a `.txt` file → filename appears in green
   - Verify text loads correctly
3. Test with a **PDF file**:
   - Select a `.pdf` file → "Extracting..." appears, then filename
   - Verify text is extracted and displayed correctly (not garbage)
4. Or **paste resume text** directly:
   - Paste text into the textarea
   - Click "Use Pasted Text"
5. Type refinement instructions (e.g. "Make it more concise")
6. Click **"Refine My Resume"** — wait ~1.5s
7. Verify:
   - Side-by-side diff: Original (left, red border) vs Refined (right, green border)
   - "WHAT CHANGED" list appears below with added/modified/removed items
   - "Download Refined Resume" button works

### Page 3 — Mock Interview (`http://localhost:5173/mock-interview`)

1. Verify the **"COMING SOON"** badge is visible
2. Verify the placeholder chat UI shows sample interview dialogue
3. Verify the 4 feature cards are displayed (Voice Input, Voice Output, Role-Based Questions, Performance Report)

## Mock Data Note

By default, the app uses built-in mock data (no backend required).

To connect to a real Azure Functions backend, create a `.env` file in the `frontend/` directory:

```bash
echo VITE_API_BASE=https://your-function-app.azurewebsites.net/api > .env
```

To force mock mode even with `VITE_API_BASE` set:

```bash
echo VITE_USE_MOCK=true >> .env
```

## Architecture

```
React SPA (Vite + TypeScript)  →  Azure Functions (Python)  →  Azure OpenAI GPT-4o
 (Azure Static Web Apps)            /api/get_career_summary     Azure AI Search
                                    /api/get_skills_table       Cosmos DB
                                    /api/optimize_resume
```

**3 pages:** Career Profile (summary + skills table) | Resume Studio (upload + refine) | Mock Interview (UI stub)

## Tech Stack

- **Frontend:** React 19, TypeScript, Vite 8, react-router-dom 7
- **Backend:** Azure Functions (Python), Azure OpenAI, Azure AI Search, Cosmos DB
- **PDF Parsing:** pdfjs-dist 6

---

## Hong Kong Job Market Data

The `data/` directory contains a structured taxonomy of Hong Kong job roles, required skills, salary benchmarks, and industry insights. This data feeds **Azure AI Search**, which serves as the knowledge layer for GPT-4o to generate personalized skills tables.

### Data Coverage

| Metric | Value |
|--------|-------|
| Total roles | 20 |
| Industry sectors | 10 |
| Skill categories | 16 |
| Skill-role pairs (search documents) | 210 |
| HK & Macau universities | 23 |

### Data Directory Structure

```
data/
├── README.md                       # Full documentation with usage guide
├── taxonomy/
│   ├── skill_categories.json       # 16 controlled skill categories
│   ├── industry_sectors.json       # 10 HK industry sectors
│   └── importance_levels.json      # critical / recommended / nice-to-have
├── roles/
│   ├── technology_data.json        # 5 roles: Data Analyst, SWE, BI Dev, AI/ML Eng, IT PM
│   ├── finance_banking.json        # 5 roles: IB Analyst, Risk, Wealth Mgmt, Fintech, Compliance
│   ├── professional_services.json  # 4 roles: Mgmt Consultant, Audit, ESG, HR
│   ├── marketing_ecommerce.json    # 3 roles: Digital Mktg, Product Mgr, E-commerce Ops
│   └── engineering_logistics.json  # 3 roles: Civil Eng, Supply Chain, Building Services
├── skills/
│   ├── skills_index.json           # Generated: 210 flat skill-role documents for AI Search
│   └── skills_summary.json         # Generated: role-level summary with skill counts
├── market_data/
│   ├── salary_benchmarks.json      # Entry-level salary bands by sector
│   ├── industry_insights.json      # HK hiring trends, in-demand roles, key skills
│   └── hk_universities.json        # Complete list of HK + Macau institutions
└── scripts/
    ├── validate_schema.py          # Validates role files against taxonomy
    └── generate_search_docs.py     # Transforms role files → AI Search documents
```

### How to Use the Data Scripts

```bash
cd data/scripts

# Validate all role files against the taxonomy
python validate_schema.py

# Generate flat AI Search documents from role files
python generate_search_docs.py
```

### Data Sources

Data was curated in June 2026 from CTgoodjobs 2025 Graduate Salary Survey, HKBU GBA Pay Survey, JIJIS, Glassdoor HK, employer graduate programme pages (Morgan Stanley, UBS, Citi, Big 4, FDM Group, Accenture), HK Labour Department LMI reports, and HK Government Census & Statistics Department.

See `data/README.md` for full documentation.
