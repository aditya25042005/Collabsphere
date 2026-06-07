from flask import request, jsonify
from app.services.rating_service import (
    rate_member_service,
    rate_project_service,
    get_project_ratings_service,
    get_ratings_given_by_user_service,
    get_member_ratings_received_service,
)


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

        success, reason = rate_project_service(user_id, project_id, score, comment)
        if success:
            return jsonify({"message": "Project rating added successfully"}), 201
        if reason == "team_member":
            return jsonify({"error": "Team members cannot rate their own project."}), 403
        if reason == "not_completed":
            return jsonify({"error": "Only completed projects can be rated."}), 403
        if reason == "already_rated":
            return jsonify({"error": "You have already rated this project."}), 409
        return jsonify({"error": "Failed to submit rating."}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


def get_project_ratings_controller():
    try:
        project_id = request.args.get("project_id")
        if not project_id:
            return jsonify({"error": "project_id required"}), 400
        ratings = get_project_ratings_service(int(project_id))
        return jsonify({"ratings": ratings}), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


def get_ratings_given_controller():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id required"}), 400
        ratings = get_ratings_given_by_user_service(user_id)
        return jsonify({"ratings": ratings}), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


def get_member_ratings_received_controller():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id required"}), 400
        ratings = get_member_ratings_received_service(user_id)
        return jsonify({"ratings": ratings}), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
