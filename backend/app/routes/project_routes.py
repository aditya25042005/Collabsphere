from flask import Blueprint
from app.middleware.auth import firebase_uid_required
from app.controllers.project_controller import (
    add_project_controller,
    best_projects_controller,
    list_projects_controller,
    list_current_projects_controller,
    list_past_projects_controller,
    list_myprojects_controller,
    view_project_details_controller,
    project_analytics_controller,
    close_project_controller,
    update_project_status_controller,
)
from app.controllers.user_controller import check_controller

# Application-related controllers live here too (per the spec)
from app.repositories.application_repository import (
    apply_project_sql,
    apply_project_status_sql,
    apply_project_status_takeback_sql,
    list_apply_project_sql,
    update_project_application_status_sql,
    admin_request_sql,
    admin_request_accept_sql,
)
from flask import request, jsonify
from app.schemas import (
    ApplyProjectSchema,
    ApplyProjectStatusSchema,
    ListApplyProjectSchema,
)

project_bp = Blueprint("project", __name__)

project_bp.add_url_rule("/check", view_func=check_controller, methods=["GET"])

project_bp.add_url_rule(
    "/add/project",
    view_func=firebase_uid_required(add_project_controller),
    methods=["POST"],
)
project_bp.add_url_rule("/best_projects", view_func=best_projects_controller, methods=["GET"])
project_bp.add_url_rule(
    "/list/projects",
    view_func=firebase_uid_required(list_projects_controller),
    methods=["POST"],
)
project_bp.add_url_rule("/list/current/projects", view_func=firebase_uid_required(list_current_projects_controller), methods=["POST"])
project_bp.add_url_rule("/list/past/projects", view_func=firebase_uid_required(list_past_projects_controller), methods=["POST"])
project_bp.add_url_rule(
    "/list/myprojects",
    view_func=firebase_uid_required(list_myprojects_controller),
    methods=["POST"],
)
project_bp.add_url_rule(
    "/project/view_details",
    view_func=firebase_uid_required(view_project_details_controller),
    methods=["GET"],
)
project_bp.add_url_rule(
    "/project/analytics",
    view_func=firebase_uid_required(project_analytics_controller),
    methods=["GET"],
)
project_bp.add_url_rule(
    "/project/close",
    view_func=firebase_uid_required(close_project_controller),
    methods=["POST"],
)
project_bp.add_url_rule(
    "/project/update_status",
    view_func=firebase_uid_required(update_project_status_controller),
    methods=["POST"],
)


# ── Application sub-routes ────────────────────────────────────────────────────

def apply_project_route():
    data = request.json
    errors = ApplyProjectSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    return apply_project_sql(data)


def apply_project_status_route():
    data = request.json
    errors = ApplyProjectStatusSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    return apply_project_status_sql(data)


def apply_project_status_takeback_route():
    data = request.json
    errors = ApplyProjectStatusSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    return apply_project_status_takeback_sql(data)


def list_apply_project_route():
    data = request.json
    errors = ListApplyProjectSchema().validate(data)
    return list_apply_project_sql(data)


def update_project_app_status_route():
    data = request.json
    return update_project_application_status_sql(data)


def admin_request_route():
    data = request.json
    return admin_request_sql(data)


def admin_request_accept_route():
    data = request.json
    return admin_request_accept_sql(data)


project_bp.add_url_rule(
    "/apply/project",
    view_func=firebase_uid_required(apply_project_route),
    methods=["POST"],
)
project_bp.add_url_rule(
    "/apply/project/status",
    view_func=firebase_uid_required(apply_project_status_route),
    methods=["POST"],
)
project_bp.add_url_rule(
    "/apply/project/status/takeback",
    view_func=firebase_uid_required(apply_project_status_takeback_route),
    methods=["POST"],
)
project_bp.add_url_rule(
    "/list/apply/status",
    view_func=firebase_uid_required(list_apply_project_route),
    methods=["POST"],
)
project_bp.add_url_rule(
    "/update/project/app/status",
    view_func=firebase_uid_required(update_project_app_status_route),
    methods=["POST"],
)
project_bp.add_url_rule(
    "/admin/request",
    view_func=firebase_uid_required(admin_request_route),
    methods=["POST"],
)
project_bp.add_url_rule(
    "/admin/request/accept",
    view_func=firebase_uid_required(admin_request_accept_route),
    methods=["POST"],
)
