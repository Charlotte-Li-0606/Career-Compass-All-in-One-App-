# Cosmos DB Setup

## Create in Azure Portal

1. Create **Azure Cosmos DB for NoSQL** account
2. Create database: `career-compass`
3. Create containers:

| Container | Partition key | Purpose |
|-----------|---------------|---------|
| `student_profiles` | `/userId` | One doc per user (profile fields) |
| `resumes` | `/userId` | Multiple docs per user (versioned resumes) |

Throughput: 400 RU/s shared autoscale is enough for hackathon dev.

## JSON schemas

- Profile: `schemas/student_profile.schema.json`
- Resume: `schemas/resume.schema.json`

These match `frontend/src/types/index.ts`.

## Example documents

**student_profiles**
```json
{
  "id": "user-abc123",
  "userId": "user-abc123",
  "major": "Computer Science",
  "year": 3,
  "university": "CUHK",
  "interests": ["data analytics", "fintech"],
  "targetRoles": ["Data Analyst"],
  "pastInternships": ["FinTech Innovations — Data Intern"],
  "extracurriculars": ["CS Society"],
  "createdAt": "2026-06-18T00:00:00Z",
  "updatedAt": "2026-06-18T00:00:00Z"
}
```

**resumes**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "userId": "user-abc123",
  "version": 1,
  "originalText": "...",
  "refinedText": "...",
  "instructions": "Make it more concise",
  "changes": [{ "type": "modified", "description": "Strengthened summary", "section": "Summary" }],
  "createdAt": "2026-06-18T00:00:00Z"
}
```

## Env vars

Set in `azure-functions/local.settings.json` (see `local.settings.json.example`):

- `COSMOS_ENDPOINT`
- `COSMOS_KEY`
- `COSMOS_DATABASE`
- `COSMOS_PROFILES_CONTAINER`
- `COSMOS_RESUMES_CONTAINER`

Functions auto-skip Cosmos writes when `COSMOS_ENDPOINT` is not configured.
