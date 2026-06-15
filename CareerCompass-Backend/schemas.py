from pydantic import BaseModel
from typing import List


# =========================
# Feature 1
# Student Profile Analysis
# =========================

class ProfileRequest(BaseModel):

    major: str

    year: int

    gpa: float

    interests: List[str]

    experiences: List[str]



class ProfileResponse(BaseModel):

    career_summary: str

    recommended_paths: List[str]

    skill_gaps: List[str]

    roadmap: List[str]



# =========================
# Feature 2
# Technical Skills Table
# =========================

class SkillRequest(BaseModel):

    target_role: str

    current_skills: List[str]



class SkillResponse(BaseModel):

    skills_analysis: str



# =========================
# Feature 3
# Resume Optimization
# =========================

class ResumeRequest(BaseModel):

    resume_text: str

    job_description: str



class ResumeResponse(BaseModel):

    resume_feedback: str