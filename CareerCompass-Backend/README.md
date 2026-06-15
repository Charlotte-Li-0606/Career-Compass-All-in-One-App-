# Career Compass AI Backend

AI-powered backend service for Career Compass.

## Features

### Feature 1 – Resume Analysis

Analyze uploaded resumes and provide:

* Resume score
* Strengths
* Weaknesses
* Improvement suggestions

### Feature 2 – Resume Tailoring

Compare resume against job descriptions and provide:

* Match score
* Missing skills
* Tailored recommendations

### Feature 3 – Career Roadmap

Generate personalized career development plans.

### Feature 4 – Interview Question Generator

Generate interview questions based on:

* Resume
* Job description
* Target role

### Feature 5 – Follow-up Interview Questions

Generate dynamic follow-up questions according to candidate answers.

### Feature 6 – Interview Performance Report

Generate structured interview evaluation reports including:

* Technical skills
* Communication
* Problem-solving
* Overall performance

---

## Tech Stack

* FastAPI
* Python
* Azure OpenAI
* OpenAI Python SDK
* python-dotenv

---

## Installation

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_MODEL=Phi-4-mini-instruct
DEMO_MODE=true
```

Run:

```bash
uvicorn app:app --reload
```

---

## API Endpoints

### Resume Analysis

POST

```text
/resume/analyze
```

### Resume Tailoring

POST

```text
/resume/tailor
```

### Career Roadmap

POST

```text
/career/roadmap
```

### Interview Questions

POST

```text
/interview/questions
```

### Follow-up Questions

POST

```text
/interview/followup
```

### Interview Report

POST

```text
/interview/report
```

---

## Demo Mode

To avoid Azure OpenAI rate-limit issues during development and demonstrations:

```env
DEMO_MODE=true
```

The backend will return predefined responses while preserving the complete API workflow.

---

## Team Contribution

Backend Development

* Resume Analysis
* Resume Tailoring
* Career Roadmap
* Interview Question Generation
* Follow-up Question Generation
* Interview Report Generation
* Demo Mode Support
