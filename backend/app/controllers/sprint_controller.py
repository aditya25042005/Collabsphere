from flask import request, jsonify
from app.services.sprint_service import (
    get_sprints_service,
    change_sprint_status_service,
    create_sprint_service,
)


def get_sprints_controller():
    project_id = request.args.get("project_id")
    if not project_id:
        return jsonify({"error": "Missing required parameter: project_id"}), 400
    try:
        sprints = get_sprints_service(project_id)
        return jsonify({
            "sprints": [
                {"sprint_id": s[0], "name": s[1], "Start": s[2], "End": s[3], "Status": s[4]}
                for s in sprints
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def change_sprint_status_controller():
    data = request.json
    return change_sprint_status_service(data)


def create_sprint_controller():
    data = request.get_json()
    user_id = data.get("user_id")
    project_id = data.get("project_id")
    name = data.get("name")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not all([user_id, project_id, name, start_date, end_date]):
        return jsonify({"error": "Missing required fields"}), 400

    return create_sprint_service(user_id, project_id, name, start_date, end_date)
