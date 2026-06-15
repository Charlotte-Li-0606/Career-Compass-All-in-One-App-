# Career Compass AI Backend

## Overview

Career Compass AI is an AI-powered career guidance backend system designed to help university students make better career decisions.

The system uses a Large Language Model (LLM) hosted on Azure AI Foundry to provide personalized career analysis, technical skill gap evaluation, and resume optimization.

The backend exposes RESTful APIs through FastAPI and provides AI-generated career recommendations based on student profiles, target roles, and job descriptions.

---

# Features

## 1. Student Profile & Career Analysis

Analyze a student's academic background, interests, GPA, and previous experiences.

The system generates:

* Career snapshot
* Recommended career paths
* Current strengths
* Skill gaps
* Personalized learning roadmap

---

## 2. Technical Skill Gap Analysis

Evaluate the difference between a student's current skills and the requirements of a target career role.

The system provides:

* Required technical skills
* Current skill assessment
* Skill gaps
* Priority ranking
* Learning plan

---

## 3. Resume Optimization

Analyze a student's resume against a target job description.

The system provides:

* Resume compatibility analysis
* Missing keywords
* Weak resume sections
* Rewrite suggestions

The model is instructed not to fabricate projects, achievements, or technical experience.

---

# System Architecture

```
User / Frontend
        |
        |
        v
FastAPI Backend
        |
        |
        v
LLM Service Layer
        |
        |
        v
Azure AI Foundry
        |
        |
        v
Phi-4-mini-instruct
```

---

# Tech Stack

## Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

## AI

* Azure AI Foundry
* Phi-4-mini-instruct
* OpenAI Python SDK

## Configuration

* python-dotenv

---

# Project Structure

```
CareerCompass-Backend

│
├── app.py
├── llm_service.py
├── schemas.py
│
├── cache.json
│
├── requirements.txt
│
├── .env.example
├── .gitignore
│
├── README.md
│
└── docs
    └── API.md
```

---

# Installation

## 1. Clone repository

```bash
git clone <repository-url>

cd CareerCompass-Backend
```

---

## 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## 3. Configure environment variables

Create a `.env` file:

```env
AZURE_ENDPOINT=your_azure_endpoint

AZURE_API_KEY=your_api_key

MODEL_NAME=Phi-4-mini-instruct
```

---

# Running the Backend

Start FastAPI server:

```bash
uvicorn app:app --reload
```

The API documentation will be available at:

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

| Feature             | Endpoint              |
| ------------------- | --------------------- |
| Profile Analysis    | POST /profile/analyze |
| Skill Analysis      | POST /skills/analyze  |
| Resume Optimization | POST /resume/optimize |

Detailed API documentation:

```
docs/API.md
```

---

# AI Safety Rules

The LLM service follows several constraints:

* Act as a professional career advisor
* Avoid casual chatbot behavior
* Provide actionable recommendations
* Do not fabricate user experience
* Do not invent projects or achievements
* Clearly state assumptions when information is missing

---

# Development Notes

The backend currently uses a JSON-based cache layer to reduce repeated LLM requests and avoid unnecessary Azure API calls during development.

---

# Future Improvements

Possible future improvements include:

* Frontend integration
* Structured JSON responses
* User authentication
* Database storage
* Resume file upload
* Production deployment

```
```
