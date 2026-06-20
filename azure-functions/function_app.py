import json
import logging

import azure.functions as func

from shared.cosmos_service import (
    append_interview_turn,
    complete_interview_session,
    create_interview_session,
    format_interview_history,
    get_interview_session,
    save_resume_version,
    upsert_profile,
)
from shared.llm_service import (
    build_profile_summary,
    build_resume_refinement,
    build_skills_table,
    generate_interview_report,
    start_interview,
    submit_interview_answer,
)
from shared.search_service import collect_target_roles, search_skills_for_roles

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
}


def _json_response(data: dict, status: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(data, ensure_ascii=False),
        status_code=status,
        mimetype="application/json",
        headers=CORS_HEADERS,
    )


def _error(message: str, status: int = 400) -> func.HttpResponse:
    return _json_response({"error": message}, status)


def _parse_body(req: func.HttpRequest) -> dict | None:
    try:
        return req.get_json()
    except ValueError:
        return None


def _options() -> func.HttpResponse:
    return func.HttpResponse(status_code=204, headers=CORS_HEADERS)


def _handle_profile_summary(req: func.HttpRequest) -> func.HttpResponse:
    body = _parse_body(req)
    if not body:
        return _error("Invalid JSON body")

    user_id = req.params.get("userId") or body.pop("userId", None) or "anonymous"
    target_roles = body.get("targetRoles") or []

    search_hits = search_skills_for_roles(target_roles)
    summary = build_profile_summary(body, search_hits)

    try:
        upsert_profile(user_id, body)
    except Exception as exc:
        logging.warning("Cosmos profile upsert skipped: %s", exc)

    return _json_response(summary)


def _handle_skills_table(req: func.HttpRequest) -> func.HttpResponse:
    body = _parse_body(req)
    if not body:
        return _error("Invalid JSON body")

    profile = body.get("profile") or body
    career_summary = body.get("careerSummary") or body.get("career_summary")
    if not career_summary:
        return _error("careerSummary is required")

    roles = collect_target_roles(profile, career_summary)
    search_hits = search_skills_for_roles(roles, top=20)
    table = build_skills_table(profile, career_summary, search_hits)
    return _json_response(table)


def _handle_optimize_resume(req: func.HttpRequest) -> func.HttpResponse:
    body = _parse_body(req)
    if not body:
        return _error("Invalid JSON body")

    if not body.get("originalText"):
        return _error("originalText is required")

    user_id = req.params.get("userId") or body.pop("userId", None) or "anonymous"
    result = build_resume_refinement(body)

    try:
        save_resume_version(
            user_id,
            {
                "originalText": body.get("originalText", ""),
                "refinedText": result.get("refinedText", ""),
                "instructions": body.get("instructions", ""),
                "careerContext": body.get("careerContext", ""),
                "changes": result.get("changes", []),
            },
        )
    except Exception as exc:
        logging.warning("Cosmos resume save skipped: %s", exc)

    return _json_response(result)


def _handle_start_interview(req: func.HttpRequest) -> func.HttpResponse:
    body = _parse_body(req) or {}
    major = body.get("major", "")
    skills = body.get("skills", "")
    target_role = body.get("target_role") or body.get("targetRole", "")
    user_id = body.get("userId") or "anonymous"

    if not target_role:
        return _error("target_role is required")

    llm_result = start_interview(major, skills, target_role)
    questions = llm_result.get("questions") or []

    session = create_interview_session(
        user_id,
        {
            "major": major,
            "skills": skills,
            "targetRole": target_role,
            "questions": questions,
        },
    )

    return _json_response({"sessionId": session["sessionId"], "questions": questions})


def _handle_submit_answer(req: func.HttpRequest) -> func.HttpResponse:
    body = _parse_body(req) or {}
    session_id = body.get("sessionId") or body.get("session_id")
    question = body.get("question", "")
    answer = body.get("answer", "")

    if not session_id:
        return _error("sessionId is required")
    if not question or not answer:
        return _error("question and answer are required")

    followup_result = submit_interview_answer(question, answer)
    followup = followup_result.get("followup", "")

    try:
        append_interview_turn(
            session_id,
            {"question": question, "answer": answer, "followup": followup},
        )
    except Exception as exc:
        logging.warning("Cosmos interview turn skipped: %s", exc)

    return _json_response({"followup": followup})


def _handle_generate_report(req: func.HttpRequest) -> func.HttpResponse:
    body = _parse_body(req) or {}
    session_id = body.get("sessionId") or body.get("session_id")
    interview_history = body.get("interview_history") or body.get("interviewHistory")

    if session_id:
        session = get_interview_session(session_id)
        if not session:
            return _error("Session not found", 404)
        interview_history = format_interview_history(session)

    if not interview_history:
        return _error("sessionId or interview_history is required")

    report = generate_interview_report(interview_history)

    if session_id:
        try:
            complete_interview_session(session_id, report)
        except Exception as exc:
            logging.warning("Cosmos interview report save skipped: %s", exc)

    return _json_response(report)


@app.route(route="get_profile_summary", methods=["POST", "OPTIONS"])
def get_profile_summary(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _options()
    return _handle_profile_summary(req)


@app.route(route="get_career_summary", methods=["POST", "OPTIONS"])
def get_career_summary(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _options()
    return _handle_profile_summary(req)


@app.route(route="get_skills_table", methods=["POST", "OPTIONS"])
def get_skills_table(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _options()
    return _handle_skills_table(req)


@app.route(route="optimize_resume", methods=["POST", "OPTIONS"])
def optimize_resume(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _options()
    return _handle_optimize_resume(req)


@app.route(route="start_interview", methods=["POST", "OPTIONS"])
def start_interview_route(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _options()
    return _handle_start_interview(req)


@app.route(route="submit_answer", methods=["POST", "OPTIONS"])
def submit_answer(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _options()
    return _handle_submit_answer(req)


@app.route(route="generate_report", methods=["POST", "OPTIONS"])
def generate_report(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _options()
    return _handle_generate_report(req)
