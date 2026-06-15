from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware


from schemas import (
    ProfileRequest,
    SkillRequest,
    ResumeRequest,
    InterviewQuestionRequest,
    FollowupRequest,
    InterviewReportRequest
)


from llm_service import (
    analyze_profile,
    analyze_skills,
    optimize_resume
)

from interview_service import (
    generate_interview_questions,
    generate_followup_question,
    generate_interview_report
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


# =========================
# Feature 4
# =========================


@app.post("/interview/questions")
def interview_questions(data: InterviewQuestionRequest):

    return {
        "result":
        generate_interview_questions(data)
    }


# =========================
# Feature 5
# =========================

@app.post("/interview/followup")
def interview_followup(data: FollowupRequest):

    return {
        "result":
        generate_followup_question(data)
    }


# =========================
# Feature 6
# =========================

@app.post("/interview/report")
def interview_report(data: InterviewReportRequest):

    return {
        "result":
        generate_interview_report(data)
    }