import json
from datetime import datetime, timezone
from typing import Any

from openai import OpenAI

from shared.config import env, is_demo_mode


SYSTEM_PROMPT = """You are Career Compass AI — a professional career advisor for university students.
Respond ONLY with valid JSON matching the requested schema. No markdown, no extra text."""


def _client() -> OpenAI:
    return OpenAI(
        base_url=env("AZURE_ENDPOINT"),
        api_key=env("AZURE_API_KEY"),
    )


def call_llm_json(prompt: str) -> dict[str, Any]:
    response = _client().chat.completions.create(
        model=env("MODEL_NAME", "Phi-4-mini-instruct"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=1200,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    return json.loads(content)


def build_profile_summary(profile: dict[str, Any], search_hits: list[dict[str, Any]]) -> dict[str, Any]:
    if is_demo_mode():
        return _demo_career_summary(profile)

    skills_context = json.dumps(search_hits[:10], ensure_ascii=False)
    profile_json = json.dumps(profile, ensure_ascii=False)

    prompt = f"""Generate a career summary for this HK university student.

Profile:
{profile_json}

Relevant job-market skills from knowledge base:
{skills_context}

Return JSON with this exact shape:
{{
  "overview": "string",
  "recommendedRoles": [{{ "title": "string", "fit": "string", "growthOutlook": "string" }}],
  "industryInsights": "string",
  "nextSteps": ["string"],
  "generatedAt": "ISO-8601 timestamp"
}}"""

    return call_llm_json(prompt)


def build_skills_table(
    profile: dict[str, Any],
    career_summary: dict[str, Any],
    search_hits: list[dict[str, Any]],
) -> dict[str, Any]:
    if is_demo_mode():
        return _demo_skills_table(profile)

    prompt = f"""Build a personalized skills table for a HK university student.

Student profile:
{json.dumps(profile, ensure_ascii=False)}

Career summary:
{json.dumps(career_summary, ensure_ascii=False)}

Required skills from job market data:
{json.dumps(search_hits[:15], ensure_ascii=False)}

Return JSON:
{{
  "summary": "string",
  "skills": [
    {{
      "name": "string",
      "category": "string",
      "proficiency": "mastered|learning|missing",
      "description": "string",
      "importance": "critical|recommended|nice-to-have"
    }}
  ],
  "generatedAt": "ISO-8601 timestamp"
}}

Include 8-12 skills. Map importance from skillImportance when available."""

    return call_llm_json(prompt)


def start_interview(major: str, skills: str, target_role: str) -> dict[str, Any]:
    if is_demo_mode():
        return {
            "questions": [
                f"Why are you interested in the {target_role} role?",
                "Describe a technical project you are proud of.",
                "Tell me about a time you worked in a team under pressure.",
                "How do you handle conflicting priorities?",
                "Walk me through how you would analyze a business problem with data.",
            ]
        }

    prompt = f"""Generate exactly five interview questions for this candidate.

Major: {major}
Skills: {skills}
Target role: {target_role}

Mix: 2 technical, 2 behavioral, 1 problem-solving.
Return JSON: {{ "questions": ["...", "...", "...", "...", "..."] }}"""

    return call_llm_json(prompt)


def submit_interview_answer(question: str, answer: str) -> dict[str, Any]:
    if is_demo_mode():
        return {"followup": "Can you walk me through your reasoning in more detail?"}

    prompt = f"""Generate exactly ONE follow-up interview question.

Original question:
{question}

Candidate answer:
{answer}

Return JSON: {{ "followup": "single follow-up question" }}"""

    return call_llm_json(prompt)


def generate_interview_report(interview_history: str) -> dict[str, Any]:
    if is_demo_mode():
        return {
            "overall_score": 82,
            "technical_knowledge": 80,
            "communication": 85,
            "problem_solving": 81,
            "strengths": ["Clear communication", "Relevant examples", "Good structure"],
            "weaknesses": ["Needs more metrics", "Could go deeper technically", "Short answers"],
            "improvement_plan": [
                "Use STAR format for behavioral answers",
                "Prepare 3 quantified project stories",
                "Practice 5 follow-up drills weekly",
            ],
        }

    prompt = f"""Evaluate this mock interview transcript.

{interview_history}

Return JSON:
{{
  "overall_score": 0-100,
  "technical_knowledge": 0-100,
  "communication": 0-100,
  "problem_solving": 0-100,
  "strengths": ["...", "...", "..."],
  "weaknesses": ["...", "...", "..."],
  "improvement_plan": ["...", "...", "..."]
}}"""

    return call_llm_json(prompt)


def _demo_skills_table(profile: dict[str, Any]) -> dict[str, Any]:
    role = (profile.get("targetRoles") or ["Data Analyst"])[0]
    return {
        "summary": f"Skills landscape for {role} based on your profile and HK market requirements.",
        "skills": [
            {
                "name": "Python",
                "category": "Programming",
                "proficiency": "learning",
                "description": "Core scripting and data analysis language for analyst roles.",
                "importance": "critical",
            },
            {
                "name": "SQL",
                "category": "Data",
                "proficiency": "learning",
                "description": "Query and aggregate data from relational databases.",
                "importance": "critical",
            },
            {
                "name": "Power BI",
                "category": "BI Tools",
                "proficiency": "missing",
                "description": "Build dashboards for business stakeholders.",
                "importance": "recommended",
            },
        ],
        "generatedAt": datetime.now(timezone.utc).isoformat(),
    }


def build_resume_refinement(req: dict[str, Any]) -> dict[str, Any]:
    if is_demo_mode():
        return _demo_resume_refinement(req)

    prompt = f"""Refine this resume based on instructions. Do NOT invent fake experience.

Original resume:
{req.get('originalText', '')}

Instructions:
{req.get('instructions', '')}

Career context (optional):
{req.get('careerContext', '')}

Return JSON:
{{
  "refinedText": "full refined resume text",
  "changes": [{{ "type": "added|removed|modified", "description": "string", "section": "string" }}]
}}"""

    return call_llm_json(prompt)


def _demo_career_summary(profile: dict[str, Any]) -> dict[str, Any]:
    roles = profile.get("targetRoles") or ["Data Analyst"]
    primary = roles[0]
    return {
        "overview": (
            f"Based on your background in {profile.get('major', 'your field')} at "
            f"{profile.get('university', 'your university')}, you are well positioned for "
            f"{primary} roles in Hong Kong."
        ),
        "recommendedRoles": [
            {
                "title": primary,
                "fit": "Strong alignment with your coursework and target roles.",
                "growthOutlook": "Steady demand in HK finance and tech sectors.",
            }
        ],
        "industryInsights": "HK employers value bilingual skills and practical project experience.",
        "nextSteps": [
            "Build a portfolio project with HK open data",
            "Strengthen visualization skills (Power BI or Tableau)",
            "Network through university career fairs",
        ],
        "generatedAt": "2026-06-18T00:00:00Z",
    }


def _demo_resume_refinement(req: dict[str, Any]) -> dict[str, Any]:
    original = req.get("originalText", "")
    refined = original.strip() + "\n\n[Refined for clarity and impact — demo mode]"
    return {
        "refinedText": refined,
        "changes": [
            {
                "type": "modified",
                "description": "Improved wording and structure (demo)",
                "section": "Overall",
            }
        ],
    }
