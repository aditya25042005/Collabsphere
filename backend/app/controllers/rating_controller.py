from flask import request, jsonify
from app.services.rating_service import rate_member_service, rate_project_service


def rate_member_controller():
    try:
        data = request.get_json()
        rated_by = data.get("rated_by")
        rated_user = data.get("rated_user")
        project_id = data.get("project_id")
        score = data.get("score")
        comment = data.get("comment", "")

        if not all([rated_by, rated_user, project_id, score]):
            return jsonify({"error": "Missing required fields"}), 400

        success = rate_member_service(rated_by, rated_user, project_id, score, comment)
        if success:
            return jsonify({"message": "Rating added successfully"}), 201
        return jsonify({"error": "Failed to add rating"}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


def rate_project_controller():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        project_id = data.get("project_id")
        score = data.get("score")
        comment = data.get("comment", "")

        if not all([user_id, project_id, score]):
            return jsonify({"error": "Missing required fields"}), 400

        success = rate_project_service(user_id, project_id, score, comment)
        if success:
            return jsonify({"message": "Project rating added successfully"}), 201
        return jsonify({"error": "You are a team member and cannot rate this project."}), 403
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
