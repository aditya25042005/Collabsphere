from flask import Blueprint
from app.middleware.auth import firebase_uid_required
from app.controllers.task_controller import (
    view_sprint_tasks_controller,
    add_task_controller,
    update_task_status_controller,
    update_task_controller,
    start_task_controller,
    complete_task_controller,
    reopen_task_controller,
)

task_bp = Blueprint("task", __name__)

task_bp.add_url_rule(
    "/project/view_tasks",
    view_func=firebase_uid_required(view_sprint_tasks_controller),
    methods=["GET"],
)
task_bp.add_url_rule(
    "/project/edit_tasks/add_task",
    view_func=firebase_uid_required(add_task_controller),
    methods=["POST"],
)
task_bp.add_url_rule(
    "/project/edit_tasks/update_task_status",
    view_func=firebase_uid_required(update_task_status_controller),
    methods=["POST", "OPTIONS"],
)
task_bp.add_url_rule(
    "/project/edit_tasks/update_task",
    view_func=firebase_uid_required(update_task_controller),
    methods=["POST", "OPTIONS"],
)
task_bp.add_url_rule(
    "/project/task/start",
    view_func=firebase_uid_required(start_task_controller),
    methods=["POST"],
)
task_bp.add_url_rule(
    "/project/task/complete",
    view_func=firebase_uid_required(complete_task_controller),
    methods=["POST"],
)
task_bp.add_url_rule(
    "/project/task/reopen",
    view_func=firebase_uid_required(reopen_task_controller),
    methods=["POST"],
)
