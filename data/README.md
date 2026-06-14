# Career Compass — Data Directory

Hong Kong and Macau job market data for the Career Compass AI career coach. This directory contains a structured taxonomy of Hong Kong job roles, their required skills, salary benchmarks, and industry insights. The data feeds **Azure AI Search**, which serves as the knowledge layer for GPT-4o to generate personalized skills tables.

## Data Coverage

| Metric | Value |
|--------|-------|
| Total roles | 20 |
| Industry sectors | 10 |
| Skill categories | 16 |
| Skill-role pairs (search documents) | 210 |
| HK & Macau universities | 23 |

## Directory Structure

```
data/
├── README.md                       # This file
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

## Sources

Data was curated in June 2026 from:

- **CTgoodjobs** — 2025 Graduate Salary & Employment Survey
- **HKBU Greater Bay Area** — Pay and Benefits Survey 2025
- **JIJIS** — Joint University Job Information System
- **Glassdoor HK & Indeed HK** — Salary and skill requirement data
- **Employer graduate programme pages** — Morgan Stanley, UBS, Citi, Big 4 (PwC, Deloitte, EY, KPMG), FDM Group, Accenture, Airport Authority HK
- **HK Labour Department** — Labour Market Information reports
- **HK Government Census & Statistics Department** — Employment statistics
- **HKIHRM** — Salary survey press releases (2025)
- **HKIB ECF** — Enhanced Competency Framework modules for compliance, risk, and banking

## How to Use

### 1. Validate role data

```bash
cd data/scripts
python validate_schema.py
```

Ensures every skill references a valid category, importance level, and sector from the taxonomy.

### 2. Generate search documents

```bash
python generate_search_docs.py
```

Transforms the role JSON files into `skills/skills_index.json` — a flat array of documents ready for Azure AI Search ingestion. One document per skill-role pair.

### 3. Upload to Azure AI Search

The `skills_index.json` file is ready for your teammate to ingest into Azure AI Search. Each document has:
- `id` — composite key `{role}~{skill}` for upsert operations
- `searchFields` — `roleTitle`, `skillName`, `skillCategory`, `skillDescription`
- `filterable` fields — `sector`, `skillImportance`, `isEntryLevel`
- `hiringIndustries` and `keywords` for faceted search

## How to Update

1. Edit the relevant role file(s) in `data/roles/`
2. If adding a new skill category, update `data/taxonomy/skill_categories.json`
3. If adding a new sector, update `data/taxonomy/industry_sectors.json`
4. Run `validate_schema.py` to check consistency
5. Run `generate_search_docs.py` to regenerate the search index
6. Re-upload to Azure AI Search (teammate's responsibility)

## Design Notes

- **One document per skill-role pair** (not per role). This enables GPT-4o to query at skill granularity.
- **Importance levels** (critical / recommended / nice-to-have) define how essential a skill is for a given role, not how proficient a student is.
- **Proficiency** (mastered / learning / missing) is inferred by GPT-4o based on the student's profile and is NOT in this data.
- **The Skills Table** is always derived from the Career Summary — the summary identifies roles, roles map to required skills via AI Search, and GPT-4o maps student experience to proficiency.
- **Languages** (Cantonese, Mandarin, English) are treated as skills in the taxonomy because language proficiency is a critical differentiator in the HK job market.
