import json
import logging

import azure.functions as func

from shared.cosmos_service import save_resume_version, upsert_profile
from shared.llm_service import build_profile_summary, build_resume_refinement
from shared.search_service import search_skills_for_roles

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def _json_response(data: dict, status: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(data, ensure_ascii=False),
        status_code=status,
        mimetype="application/json",
        headers={"Access-Control-Allow-Origin": "*"},
    )


def _error(message: str, status: int = 400) -> func.HttpResponse:
    return _json_response({"error": message}, status)


def _parse_body(req: func.HttpRequest) -> dict | None:
    try:
        return req.get_json()
    except ValueError:
        return None


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


@app.route(route="get_profile_summary", methods=["POST", "OPTIONS"])
def get_profile_summary(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers={"Access-Control-Allow-Origin": "*"})
    return _handle_profile_summary(req)


@app.route(route="get_career_summary", methods=["POST", "OPTIONS"])
def get_career_summary(req: func.HttpRequest) -> func.HttpResponse:
    """Alias for frontend compatibility."""
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers={"Access-Control-Allow-Origin": "*"})
    return _handle_profile_summary(req)


@app.route(route="optimize_resume", methods=["POST", "OPTIONS"])
def optimize_resume(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers={"Access-Control-Allow-Origin": "*"})
    return _handle_optimize_resume(req)
