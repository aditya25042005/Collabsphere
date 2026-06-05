from flask import request, jsonify
from app.services.task_service import (
    view_sprint_tasks_service,
    add_task_service,
    update_task_status_service,
    update_task_service,
    change_task_status_service,
)
from app.extensions import engine
from sqlalchemy import text


def view_sprint_tasks_controller():
    project_id = request.args.get("project_id")
    if not project_id:
        return jsonify({"error": "Missing project_id parameter"}), 400
    try:
        project_id = int(project_id)
        sprints = view_sprint_tasks_service(project_id)
        if not sprints:
            return jsonify({"error": "No sprints found for this project"}), 404
        return jsonify({"sprints": sprints}), 200
    except ValueError:
        return jsonify({"error": "Invalid project_id format"}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


def add_task_controller():
    data = request.json
    required = ["project_id", "sprint_number", "description", "assigned_to", "points", "user_id"]
    if not all(data.get(k) for k in required):
        return jsonify({"error": "Missing required parameters"}), 400

    success, message = add_task_service(data)
    if not success:
        return jsonify({"error": message}), 400
    return jsonify({"message": message}), 201


def update_task_status_controller():
    data = request.json
    task_id = data.get("task_id")
    if not task_id:
        return jsonify({"error": "Missing required parameter: task_id"}), 400

    # Verify task exists
    try:
        with engine.connect() as conn:
            count = conn.execute(
                text("SELECT COUNT(*) FROM task WHERE id = :task_id"),
                {"task_id": task_id}
            ).scalar()
        if count == 0:
            return jsonify({"error": "Task ID does not exist"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    success, msg = update_task_status_service(task_id, data.get("status"))
    if success:
        return jsonify({"message": "Task updated successfully!"}), 200
    return jsonify({"error": msg}), 500


def update_task_controller():
    data = request.json
    task_id = data.get("task_id")
    if not task_id:
        return jsonify({"error": "Missing required parameter: task_id"}), 400

    # Verify task exists
    try:
        with engine.connect() as conn:
            count = conn.execute(
                text("SELECT COUNT(*) FROM task WHERE id = :task_id"),
                {"task_id": task_id}
            ).scalar()
        if count == 0:
            return jsonify({"error": "Task ID does not exist"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    allowed_fields = ["description", "assigned_to", "status", "points"]
    updates = {k: data[k] for k in data if k in allowed_fields}
    if not updates:
        return jsonify({"error": "No fields provided to update"}), 400

    success = update_task_service(task_id, updates)
    if success:
        return jsonify({"message": "Task updated successfully!"}), 200
    return jsonify({"error": "Failed to update task"}), 500


def start_task_controller():
    data = request.json
    task_id = data.get("task_id")
    frontend_status = data.get("status")
    if not task_id or not frontend_status:
        return jsonify({"error": "Missing task_id or status"}), 400
    success, err = change_task_status_service(task_id, frontend_status)
    if success:
        return jsonify({"message": f"Task {task_id} moved to {frontend_status}."}), 200
    return jsonify({"error": err or "Failed to update task"}), 400 if err else 500


def complete_task_controller():
    data = request.json
    task_id = data.get("task_id")
    frontend_status = data.get("status")
    if not task_id or not frontend_status:
        return jsonify({"error": "Missing task_id or status"}), 400
    success, err = change_task_status_service(task_id, frontend_status)
    if success:
        return jsonify({"message": f"Task {task_id} marked as {frontend_status}."}), 200
    return jsonify({"error": err or "Failed to update task"}), 400 if err else 500


def reopen_task_controller():
    data = request.json
    task_id = data.get("task_id")
    frontend_status = data.get("status")
    if not task_id or not frontend_status:
        return jsonify({"error": "Missing task_id or status"}), 400
    success, err = change_task_status_service(task_id, frontend_status)
    if success:
        return jsonify({"message": f"Task {task_id} reopened to {frontend_status}."}), 200
    return jsonify({"error": err or "Failed to update task"}), 400 if err else 500
