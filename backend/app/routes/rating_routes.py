from flask import Blueprint
from app.middleware.auth import firebase_uid_required
from app.controllers.rating_controller import (
    rate_member_controller,
    rate_project_controller,
)

rating_bp = Blueprint("rating", __name__)

rating_bp.add_url_rule(
    "/rate_member",
    view_func=firebase_uid_required(rate_member_controller),
    methods=["POST"],
)
rating_bp.add_url_rule(
    "/rate_project",
    view_func=firebase_uid_required(rate_project_controller),
    methods=["POST"],
)
