# Career Compass AI API Documentation

## Base URL

Local development:

```
http://127.0.0.1:8000
```

---

# 1. Student Profile Analysis

## Endpoint

```
POST /profile/analyze
```

## Description

Analyze a student's background and generate personalized career recommendations.

---

## Request Body

```json
{
    "major": "Computer Science",
    "year": 2,
    "gpa": 3.7,
    "interests": [
        "Artificial Intelligence",
        "Machine Learning"
    ],
    "experiences": [
        "Python programming project"
    ]
}
```

---

## Response

```json
{
    "result": "AI generated career analysis"
}
```

---

## Generated Content

The response includes:

* Career Snapshot
* Recommended Career Paths
* Current Strengths
* Skill Gaps
* Learning Roadmap

---

# 2. Technical Skill Gap Analysis

## Endpoint

```
POST /skills/analyze
```

## Description

Analyze missing technical skills for a target career role.

---

## Request Body

```json
{
    "target_role": "Machine Learning Engineer",

    "current_skills": [
        "Python",
        "Basic Machine Learning",
        "SQL"
    ]
}
```

---

## Response

```json
{
    "result": "AI generated skill analysis"
}
```

---

## Generated Content

The response includes:

* Skill requirement analysis
* Current skill assessment
* Gap levels
* Priority ranking
* Learning plan

---

# 3. Resume Optimization

## Endpoint

```
POST /resume/optimize
```

## Description

Compare a student's resume with a target job description and provide optimization suggestions.

---

## Request Body

```json
{
    "resume_text": "Student resume content",

    "job_description": "Target job description"
}
```

---

## Response

```json
{
    "result": "AI generated resume optimization"
}
```

---

## Generated Content

The response includes:

* Resume match score
* Missing keywords
* Weak sections
* Rewrite suggestions

---

# Error Handling

## Empty Input

Example:

```json
{
    "error": "Please provide required information"
}
```

---

## LLM Service Error

Example:

```json
{
    "error": "AI service temporarily unavailable"
}
```

---

# Integration Notes for Frontend

Frontend applications should:

1. Send JSON requests to the corresponding endpoint.
2. Display the returned AI-generated result.
3. Handle possible temporary LLM service failures.

Future versions may replace text responses with structured JSON objects for easier UI rendering.

```
```
