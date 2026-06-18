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

**3 pages:** Career Profile (summary + skills table) | Resume Studio (upload + refine) | Mock Interview (UI stub only)

**Core intelligence ("The Bridge"):** The skills table is derived from the career summary — summary identifies roles, roles map to required skills via AI Search, skills categorized as Mastered / Learning / Missing.

**Agent persona:** Supportive career coach — encouraging, specific, practical, patient. System prompt scaffold is in `General Planning.md`.

## Key Design Rules

- **Structured outputs are mandatory.** All GPT-4o responses for career summary and skills table must use JSON structured outputs for reliable frontend rendering.
- **Skills table must derive from career summary** — never compute them independently. This is the core value of the agent.
- **Responsible AI** is a judging criterion — include confidence indicators, cite sources, never give definitive career "guarantees."
- **Mock interview page** (page 3) is a UI stub only — no audio backend yet.
- **All agents must publish to M365 Copilot Chat** — via Azure AI Agent Service.

## Planned Project Structure

```
frontend/           React + TypeScript (Vite) SPA
  src/pages/        CareerProfile, ResumeStudio, MockInterview
  src/components/   PersonalSummary, SkillsTable, ResumeUploader, ResumeDiff
  src/services/     api.ts — Axios/fetch client for Azure Functions
  src/types/        TypeScript interfaces for profile, skills, resume

api/                Azure Functions (Python)
  function_app.py   All HTTP triggers
  agent_prompts.py  System prompts and persona definitions
  models.py         Pydantic models for structured outputs
  search_client.py  Azure AI Search helper
  cosmos_client.py  Cosmos DB helper

infra/              Bicep/Terraform Azure provisioning
data/               Seed data for AI Search career/skill taxonomy index
```

## Data Models

**Cosmos DB — StudentProfile container:** `id`, `userId` (Entra ID), `major`, `year`, `university`, `interests[]`, `targetRoles[]`, `pastInternships[]`, `extracurriculars[]`, `careerSummary` (structured JSON), `skillsTable` (structured JSON), `updatedAt`

**Cosmos DB — Resume container:** `id`, `userId`, `originalText`, `refinementInstructions`, `refinedText`, `createdAt`

## Commands (Once Scaffolded)

```bash
# Frontend
cd frontend && npm run dev        # Start Vite dev server
cd frontend && npm run build      # Production build
cd frontend && npm run lint       # ESLint

# Backend (Azure Functions)
cd api && func start              # Start Functions runtime locally
cd api && func start --python     # Explicit Python worker
cd api && python -m pytest        # Run tests

# Deployment
az staticwebapp deploy            # Deploy frontend
az functionapp deployment ...     # Deploy API
```
