from flask import request, jsonify
from app.services.member_service import (
    verify_member_service,
    get_eligible_users_service,
    promote_moderator_service,
    remove_moderator_service,
)
from app.services.user_service import list_users_service
from app.repositories.application_repository import notification_sql


def verify_member_controller():
    data = request.json
    return verify_member_service(data)


def get_eligible_users_controller():
    project_id = request.args.get("project_id")
    if not project_id:
        return jsonify({"error": "Missing project_id"}), 400
    try:
        users = get_eligible_users_service(project_id)
        if not users:
            return jsonify({"message": "No eligible users found"}), 404
        return jsonify({"eligible_users": [{"roll_no": u[0], "name": u[1]} for u in users]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def promote_moderator_controller():
    data = request.json
    project_id = data.get("project_id")
    user_id = data.get("user_id")
    if not project_id or not user_id:
        return jsonify({"error": "Missing project_id or user_id"}), 400
    try:
        success, message = promote_moderator_service(project_id, user_id)
        if success:
            return jsonify({"message": message}), 200
        return jsonify({"error": message}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def demote_moderator_controller():
    data = request.json
    project_id = data.get("project_id")
    user_id = data.get("user_id")
    if not project_id or not user_id:
        return jsonify({"error": "Missing project_id or user_id"}), 400
    try:
        success = remove_moderator_service(project_id, user_id)
        if success:
            return jsonify({"message": f"User {user_id} demoted to Member."}), 200
        return jsonify({"error": "User is not a moderator or demotion failed."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def notification_controller():
    data = request.json
    return notification_sql(data)
