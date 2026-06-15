from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware


from schemas import (
    ProfileRequest,
    SkillRequest,
    ResumeRequest
)


from llm_service import (
    analyze_profile,
    analyze_skills,
    optimize_resume
)



app = FastAPI(
    title="Career Compass AI API"
)



app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)



@app.get("/")
def root():

    return {
        "message":
        "Career Compass AI Backend Running"
    }




# =========================
# Feature 1
# =========================

@app.post("/profile/analyze")
def profile_analysis(
        data: ProfileRequest
):

    result = analyze_profile(data)


    return {

        "feature":
        "Student Profile Analysis",

        "result":
        result

    }





# =========================
# Feature 2
# =========================

@app.post("/skills/analyze")
def skills_analysis(
        data: SkillRequest
):

    result = analyze_skills(data)


    return {

        "feature":
        "Technical Skills Analysis",

        "result":
        result

    }





# =========================
# Feature 3
# =========================

@app.post("/resume/tailor")
def resume_tailor(
        data: ResumeRequest
):

    result = optimize_resume(data)


    return {

        "feature":
        "Resume Optimization",

        "result":
        result

    }