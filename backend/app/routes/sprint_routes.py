from flask import Blueprint
from app.middleware.auth import firebase_uid_required
from app.controllers.sprint_controller import (
    get_sprints_controller,
    change_sprint_status_controller,
    create_sprint_controller,
)

sprint_bp = Blueprint("sprint", __name__)

sprint_bp.add_url_rule(
    "/project/create_sprint",
    view_func=firebase_uid_required(create_sprint_controller),
    methods=["POST"],
)
sprint_bp.add_url_rule(
    "/project/view_sprints",
    view_func=firebase_uid_required(get_sprints_controller),
    methods=["GET"],
)
sprint_bp.add_url_rule(
    "/change/sprint/status",
    view_func=firebase_uid_required(change_sprint_status_controller),
    methods=["POST"],
)
