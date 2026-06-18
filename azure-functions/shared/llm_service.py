import json
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


def _call_json(prompt: str) -> dict[str, Any]:
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

    return _call_json(prompt)


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

    return _call_json(prompt)


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
