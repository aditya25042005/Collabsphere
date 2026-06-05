from flask import request, jsonify
from app.services.project_service import (
    add_project_service,
    best_projects_service,
    list_projects_service,
    list_current_projects_service,
    list_past_projects_service,
    list_myprojects_service,
    view_project_details_service,
    project_analytics_service,
)
from app.services.user_service import check_service
from app.schemas import AddProjectSchema, ListProjectsSchema


def check_controller():
    return check_service()


def add_project_controller():
    data = request.json
    errors = AddProjectSchema().validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    return add_project_service(data)


def best_projects_controller():
    return best_projects_service()


def list_projects_controller():
    data = request.json
    errors = ListProjectsSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    return list_projects_service(data)


def list_current_projects_controller():
    data = request.json
    errors = ListProjectsSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    return list_current_projects_service(data)


def list_past_projects_controller():
    data = request.json
    errors = ListProjectsSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    return list_past_projects_service(data)


def list_myprojects_controller():
    data = request.json or {}
    if not data.get("user_id"):
        return jsonify({"errors": "user_id required"}), 400
    errors = ListProjectsSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    return list_myprojects_service(data)


def view_project_details_controller():
    project_id = request.args.get("project_id")
    if not project_id:
        return jsonify({"error": "Missing project_id parameter"}), 400
    details = view_project_details_service(project_id)
    if not details:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(details), 200


def project_analytics_controller():
    project_id = request.args.get("project_id")
    if not project_id:
        return jsonify({"error": "Missing project_id parameter"}), 400
    try:
        project_id = int(project_id)
        analytics = project_analytics_service(project_id)
        if analytics is None:
            return jsonify({"error": "Project not found"}), 404
        return jsonify(analytics), 200
    except ValueError:
        return jsonify({"error": "Invalid project_id"}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
