# General Planning — Career Compass Agent

**Hackathon:** Microsoft Agent Impact Lab — Student-Led AI Agent Hackathon (HK × Student Ambassadors)
**Track:** Track 1 — Reinvent Student Engagement (Career Readiness)
**Stack:** Pro-Code (Azure-Hosted), must publish to Microsoft 365 Copilot Chat
**Deadline:** June 29, 2026 — Offline Final Presentation

---

## 1. What We're Building

**Career Compass** — a 3-page AI agent app published to Microsoft 365 Copilot Chat, designed as a supportive career coach for Hong Kong/Macau university students.

### Agent Persona

A **supportive career coach** — encouraging, specific, practical, and patient. Celebrates strengths before identifying gaps. Gives concrete, actionable advice grounded in real job markets.

| Trait | How It Shows Up |
|---|---|
| **Encouraging** | Celebrates strengths before pointing out gaps — "You've built a solid foundation in Python. Let's round that out with some cloud deployment experience." |
| **Specific** | Gives concrete, actionable advice, not vague platitudes |
| **Practical** | Understands real job markets, doesn't suggest unrealistic paths |
| **Patient** | The user might not know what they want yet — the agent guides discovery |

---

## 2. Features

| # | Feature | Priority | Description |
|---|---------|----------|-------------|
| 1 | Personal Summary | Core | User inputs profile → agent generates tailored career overview (recommended roles, industry insights, growth paths) |
| 2 | Technical Skills Table | Core | Derived from career summary → structured skills matrix color-coded as Mastered / Learning / Missing, with gap analysis |
| 3 | Resume Refinement | Core | Upload original resume + refinement instructions → agent returns refined version with tracked changes |
| 4 | Mock Interview (Audio) | Stretch | Voice-interactive AI interviewer — UI stub only for now |

### The Bridge (Core Intelligence)

The skills table must be **derived from** the personal summary's career analysis. This is the heart of the agent's value:

```
User Profile Input
        │
        ▼
Personal Summary ────→ AI identifies career path, recommended roles, trajectory
        │
        ▼
Skills Table ────→ AI maps career path → required skills
                  → proficiency levels (Mastered / Learning / Missing)
                  → gap analysis ("You need X, you have Y")
```

---

## 3. Page Structure

### Page 1: Career Profile (`/` or `/career-profile`)
- **Input form** — major, year, interests, target roles, past internships, extracurriculars
- **Personal Summary card** — AI-generated career overview with structured insights
- **Technical Skills Table** — color-coded grid of skills, derived from the summary
  - 🟢 Mastered | 🟠 Learning | 🔴 Missing
  - Updates when profile changes

### Page 2: Resume Studio (`/resume-studio`)
- **Upload area** — file upload (PDF/DOCX) or paste text
- **Instructions input** — what to optimize for (e.g., "tailor for data analyst roles", "more concise")
- **Refined output** — side-by-side or diff view: original vs AI-refined
- **Download button** — export refined resume

### Page 3: Mock Interview (`/mock-interview`)
- **UI mockup** — matches the design from `Mock Interview UI Draft.pdf`
- **Placeholder state** — "Coming Soon" message
- Preserves the full 3-page vision for the pitch

---

## 4. Architecture

```
┌─────────────────────────────────────────────────┐
│              Frontend (React SPA)                │
│  Hosted on Azure Static Web Apps                │
│  3 pages: Career Profile | Resume Studio | Mock │
└─────────────────┬───────────────────────────────┘
                  │ HTTPS
┌─────────────────▼───────────────────────────────┐
│         Azure Functions (API Layer)              │
│  /api/get_career_summary                        │
│  /api/get_skills_table                          │
│  /api/optimize_resume                           │
└─────────────────┬───────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌─────────┐ ┌──────────┐ ┌───────────┐
│ GPT-4o  │ │Azure AI  │ │Cosmos DB  │
│(OpenAI) │ │ Search   │ │(profiles, │
│         │ │(career   │ │ resumes,  │
│         │ │knowledge)│ │ sessions) │
└─────────┘ └──────────┘ └───────────┘
```

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React + TypeScript (Vite), Azure Static Web Apps | 3-page single-page application |
| API | Azure Functions (Python) with HTTP triggers | REST endpoints for each feature |
| LLM | Azure OpenAI GPT-4o | Career summarization, skills mapping, resume refinement |
| Knowledge | Azure AI Search | Indexed career/skill taxonomies, job market data |
| Storage | Azure Cosmos DB | User profiles, resume history, session state |
| Auth | Microsoft Entra ID (student email) | Only HK/Macau university students |
| Publishing | Azure AI Agent Service → M365 Copilot Chat | Meets hackathon requirement |

---

## 5. Data Models (Cosmos DB)

### StudentProfile Container
```json
{
  "id": "uuid",
  "userId": "entra-id",
  "major": "string",
  "year": 2,
  "university": "string",
  "interests": ["string"],
  "targetRoles": ["string"],
  "pastInternships": ["string"],
  "extracurriculars": ["string"],
  "careerSummary": { "...structured output from GPT-4o..." },
  "skillsTable": { "...structured output from GPT-4o..." },
  "updatedAt": "timestamp"
}
```

### Resume Container
```json
{
  "id": "uuid",
  "userId": "entra-id",
  "originalText": "string",
  "refinementInstructions": "string",
  "refinedText": "string",
  "createdAt": "timestamp"
}
```

---

## 6. API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/get_career_summary` | Takes user profile → returns career summary (structured JSON) |
| POST | `/api/get_skills_table` | Takes career summary + profile → returns skills table (structured JSON) |
| POST | `/api/optimize_resume` | Takes resume text + instructions → returns refined resume |
| GET | `/api/profile/{userId}` | Fetches stored user profile |
| PUT | `/api/profile/{userId}` | Updates profile fields |

---

## 7. Agent System Prompt (Scaffold)

```
You are Career Compass, a supportive career coach for university students
in Hong Kong and Macau. Your tone is encouraging, specific, practical,
and patient. You help students understand their career paths, identify
skill gaps, and refine their professional materials.

When a student shares their profile:
1. Celebrate what they've accomplished so far
2. Identify promising career directions with specific reasoning
3. Surface concrete next steps they can take

When discussing skill gaps:
1. Frame gaps as growth opportunities, not deficiencies
2. Suggest specific courses, projects, or resources
3. Connect each skill to real job requirements

Never give vague advice. Always ground recommendations in the student's
specific context and real job market data.
```

---

## 8. Implementation Phases

### Phase 1: Backend Foundation (Azure + APIs)
1. **Provision Azure resources**
   - Azure OpenAI (GPT-4o deployment)
   - Azure AI Search (create career knowledge index)
   - Cosmos DB (create database + containers)
   - Azure Functions app
2. **Build and populate Azure AI Search index**
   - Seed with career/skill taxonomy data (curated from job market sources)
   - Create search index schema for skills, roles, industries
3. **Implement core Azure Functions**
   - `get_career_summary` — GPT-4o with system prompt → structured JSON output
   - `get_skills_table` — takes career summary roles, queries AI Search, GPT-4o maps to categorized table
   - `optimize_resume` — takes original text + instructions, GPT-4o rewrites
4. **Test APIs** with curl or Postman

### Phase 2: Frontend (React SPA)
1. **Scaffold React app** with TypeScript, routing (react-router), Vite
2. **Page 1: Career Profile**
   - Profile input form
   - Career Summary display card (animated reveal)
   - Skills Table component (color-coded: green/amber/red)
   - Skills table updates when profile changes
3. **Page 2: Resume Studio**
   - Upload area (file upload or paste text)
   - Instructions input (what to optimize for)
   - Side-by-side diff view: original vs refined
   - Download button
4. **Page 3: Mock Interview** (stub only)
   - Mockup UI matching `Mock Interview UI Draft.pdf`
   - "Coming Soon" / disabled state message
5. **Styling** — dark theme, cyberpunk/tech aesthetic with cyan/purple accents

### Phase 3: Integration & Deployment
1. Connect frontend to Azure Functions
2. Deploy frontend to Azure Static Web Apps
3. Register agent with Azure AI Agent Service
4. Publish to Microsoft 365 Copilot Chat
5. End-to-end testing — full user flow

### Phase 4: Submission Prep
1. **Pitch Deck** (max 6 slides) — problem, solution, architecture, demo, impact, roadmap
2. **GitHub repository** — clean README, architecture diagram, setup instructions
3. **Demo video** — walk through all working features (2-3 minutes)

---

## 9. Key Design Decisions

1. **Structured Outputs are critical.** GPT-4o responses for career summary and skills table must use JSON structured outputs to ensure reliable parsing and rendering.

2. **The Bridge matters most for judging.** The intelligence of "summary → skills table" derivation separates this from a simple chatbot. Invest prompt engineering effort here.

3. **Responsible AI is a judging dimension.** Include confidence indicators, cite sources when possible, and have clear guardrails about not giving definitive career "guarantees."

4. **Mock interview page stays as a stub.** Preserves the 3-page vision, shows forward thinking, costs nothing to include.

---

## 10. Project Files

### New Files to Create
```
frontend/
├── src/
│   ├── pages/
│   │   ├── CareerProfile.tsx
│   │   ├── ResumeStudio.tsx
│   │   └── MockInterview.tsx          (stub)
│   ├── components/
│   │   ├── PersonalSummary.tsx
│   │   ├── SkillsTable.tsx
│   │   ├── ResumeUploader.tsx
│   │   └── ResumeDiff.tsx
│   ├── services/
│   │   └── api.ts                     (Azure Function client)
│   └── types/
│       └── index.ts                   (TypeScript interfaces)

api/
├── function_app.py                    (all HTTP trigger functions)
├── agent_prompts.py                   (system prompts & persona)
├── models.py                          (Pydantic models)
├── search_client.py                   (Azure AI Search helper)
├── cosmos_client.py                   (Cosmos DB helper)
└── requirements.txt

infra/                                 (Azure provisioning)
data/                                  (AI Search seed data)
```

---

## 11. Verification Plan

- **API testing:** curl each endpoint with sample payloads, verify structured JSON responses
- **Frontend testing:** Run React dev server, walk through all 3 pages, verify loading/success/error states
- **Integration:** Full flow — enter profile → career summary → skills table → upload resume → refined version
- **Copilot Chat:** Verify agent appears in M365 Copilot Chat with correct persona
- **Demo:** Record 2-3 minute walkthrough covering all working features
